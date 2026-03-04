"""
AegisLab Workflow API — HTTP endpoint for Zapier (or other tools) to trigger agent runs.
- POST /run-agent with JSON body → runs agent via run_agent_cli.run(); returns JSON.
- POST /upload with multipart/form-data → saves files to 10_Input.
- Bind to 127.0.0.1:8002 (localhost only).
"""

import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

_MAX_PARALLEL_WORKERS = 3

_API_DIR = Path(__file__).resolve().parent
_DASHBOARD_DIR = _API_DIR.parent / "Aegislab_Dashboard"
_START_TIME = time.time()
_REPO_ROOT = _API_DIR.parent.parent
_INPUT_DIR = _REPO_ROOT / "10_Input"
_SCRIPTS_DIR = _API_DIR.parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import RedirectResponse, HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from run_agent_cli import run as run_agent, pre_extract_cache

app = FastAPI(title="AegisLab Workflow API", description="Trigger agent runs for Zapier or other callers")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def root():
    """Serve the AegisLab Dashboard."""
    dashboard_file = _DASHBOARD_DIR / "aegislab-dashboard.html"
    if dashboard_file.exists():
        return FileResponse(dashboard_file, media_type="text/html")
    return HTMLResponse("<h1>AegisLab</h1><p>Dashboard not found. <a href='/docs'>API docs</a></p>", status_code=404)


@app.get("/favicon.ico")
def favicon():
    from fastapi.responses import Response
    return Response(status_code=204)


class RunAgentRequest(BaseModel):
    input_path: str = Field(..., description="Repo-relative path to context file, e.g. 10_Input/brief.md")
    agent_num: int = Field(..., ge=1, le=11, description="Agent number 1-11")
    template_type: str = Field(default="Daily Driver", description="Daily Driver | Deep Dive | Review/QA")
    output_path: str = Field(..., description="Repo-relative output path, e.g. 11_Results/artifact.md")
    assumptions: str = Field(default="", description="Optional assumptions")
    constraints: str = Field(default="", description="Optional constraints")
    model_override: str = Field(default="", description="Override model; requires override_rationale")
    override_rationale: str = Field(default="", description="Rationale for override (logged)")
    confirm_defensive_scope: bool = Field(default=False, description="When topic may involve offensive security, must be true (human-in-the-loop)")


@app.post("/run-agent")
def run_agent_endpoint(body: RunAgentRequest):
    """Run one agent. Returns { success, message } or { success, error }."""
    ok, msg = run_agent(
        input_path=body.input_path,
        agent_num=body.agent_num,
        template_type=body.template_type,
        output_path=body.output_path,
        assumptions=body.assumptions or "",
        constraints=body.constraints or "",
        model_override=body.model_override or "",
        override_rationale=body.override_rationale or "",
        confirm_defensive_scope=body.confirm_defensive_scope,
    )
    if ok:
        return {"success": True, "message": msg}
    raise HTTPException(status_code=400, detail=msg)


@app.get("/health")
def health():
    """Health check with uptime for dashboard."""
    uptime_sec = int(time.time() - _START_TIME)
    branch = ""
    try:
        r = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=str(_REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=2,
        )
        if r.returncode == 0 and r.stdout:
            branch = r.stdout.strip()
    except Exception:
        pass
    queued = 0
    if _INPUT_DIR.exists():
        queued = sum(
            1 for p in _INPUT_DIR.iterdir()
            if p.is_file() and p.suffix.lower() in {".pdf", ".docx", ".txt", ".md", ".xlsx", ".pptx", ".json"}
            and not p.name.startswith(".") and "~" not in p.name
        )
    return {
        "status": "ok",
        "uptime_seconds": uptime_sec,
        "branch": branch or "unknown",
        "tasks_queued": queued,
    }


_OUTPUT_DIR = _REPO_ROOT / "11_Results"
_ALLOWED_EXT = {".pdf", ".docx", ".txt", ".md", ".xlsx", ".pptx", ".json"}


def _open_folder_in_explorer(path: Path) -> bool:
    """Open folder in system file explorer. Returns True if successful."""
    path = path.resolve()
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
    try:
        if sys.platform == "win32":
            os.startfile(str(path))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])
        return True
    except Exception:
        return False


@app.post("/open-folder")
def open_folder(folder: str = "11_Results"):
    """Open 10_Input or 11_Results in system file explorer."""
    if folder == "10_Input":
        path = _INPUT_DIR
    elif folder == "11_Results":
        path = _OUTPUT_DIR
    else:
        raise HTTPException(status_code=400, detail="Use 10_Input or 11_Results")
    ok = _open_folder_in_explorer(path)
    return {"success": ok, "path": str(path)}


@app.get("/results")
def list_results():
    """List files in 11_Results for download."""
    if not _OUTPUT_DIR.exists():
        return {"files": [], "path": str(_OUTPUT_DIR)}
    files = [
        {"name": p.name, "size": p.stat().st_size, "url": f"/results/download/{p.name}"}
        for p in sorted(_OUTPUT_DIR.iterdir())
        if p.is_file() and not p.name.startswith(".") and "~" not in p.name
    ]
    return {"files": files, "path": str(_OUTPUT_DIR)}


@app.get("/results/download/{filename:path}")
def download_result(filename: str):
    """Download a file from 11_Results."""
    path = (_OUTPUT_DIR / filename).resolve()
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    if not str(path).startswith(str(_OUTPUT_DIR.resolve())):
        raise HTTPException(status_code=403, detail="Invalid path")
    from fastapi.responses import Response
    content = path.read_bytes()
    return Response(content=content, media_type="application/octet-stream", headers={
        "Content-Disposition": f'attachment; filename="{path.name}"'
    })


@app.get("/assignment-status")
def assignment_status():
    """Return queued (10_Input) and completed (11_Results) assignments for status widget."""
    queued = []
    completed = []
    if _INPUT_DIR.exists():
        for p in sorted(_INPUT_DIR.iterdir()):
            if p.is_file() and p.suffix.lower() in _ALLOWED_EXT and not p.name.startswith(".") and "~" not in p.name:
                queued.append({"name": p.name})
    if _OUTPUT_DIR.exists():
        for p in sorted(_OUTPUT_DIR.iterdir()):
            if p.is_file() and not p.name.startswith(".") and "~" not in p.name:
                completed.append({"name": p.name})
    return {"queued": queued, "completed": completed}


@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(alias="files")):
    """Save uploaded files to 10_Input. Accepts .docx, .xlsx, .pdf, .md, .txt, .pptx, .json."""
    if not files:
        raise HTTPException(status_code=400, detail="No files received. Use form field 'files'.")
    _INPUT_DIR.mkdir(parents=True, exist_ok=True)
    allowed = {".docx", ".xlsx", ".pdf", ".md", ".txt", ".pptx", ".json"}
    saved = []
    rejected = []
    for f in files:
        ext = Path(f.filename or "").suffix.lower()
        if ext not in allowed:
            rejected.append(f.filename or "(unnamed)")
            continue
        dest = _INPUT_DIR / (f.filename or "upload")
        try:
            content = await f.read()
            dest.write_bytes(content)
            if ext in (".pdf", ".docx"):
                try:
                    pre_extract_cache(dest)
                except Exception:
                    pass
            saved.append(f.filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save {f.filename}: {e}")
    if not saved:
        raise HTTPException(
            status_code=400,
            detail=f"No valid files. Allowed: .docx, .xlsx, .pdf, .md, .txt, .pptx, .json. Rejected: {rejected}",
        )
    return {"success": True, "saved": saved, "count": len(saved)}


def _process_one_file(p: Path) -> tuple[str, bool, str]:
    """Process one file; return (filename, ok, message)."""
    rel_input = f"10_Input/{p.name}"
    safe_base = "".join(c if c.isalnum() or c in " -_" else "_" for c in p.stem)
    rel_output = f"11_Results/{safe_base}_deliverable.md"
    try:
        ok, msg = run_agent(
            input_path=rel_input,
            agent_num=2,
            template_type="Daily Driver",
            output_path=rel_output,
        )
        return (p.name, ok, msg)
    except Exception as e:
        return (p.name, False, str(e))


def _run_process_input():
    """Background worker: process all files in 10_Input in parallel (max 3 workers)."""
    _INPUT_DIR.mkdir(parents=True, exist_ok=True)
    allowed = {".pdf", ".docx", ".txt", ".md", ".xlsx", ".pptx", ".json"}
    files_to_process = [
        p for p in sorted(_INPUT_DIR.iterdir())
        if p.is_file() and p.suffix.lower() in allowed
        and not p.name.startswith(".") and "~" not in p.name
    ]
    with ThreadPoolExecutor(max_workers=_MAX_PARALLEL_WORKERS) as executor:
        futures = {executor.submit(_process_one_file, p): p for p in files_to_process}
        for future in as_completed(futures):
            name, ok, msg = future.result()
            print(f"[Auto-Process] {name}: {'OK' if ok else msg}")


@app.post("/process-input")
def process_input():
    """Start processing all documents in 10_Input in background. Returns immediately."""
    _INPUT_DIR.mkdir(parents=True, exist_ok=True)
    allowed = {".pdf", ".docx", ".txt", ".md", ".xlsx", ".pptx", ".json"}
    count = sum(
        1 for p in _INPUT_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in allowed and not p.name.startswith(".") and "~" not in p.name
    )
    if count == 0:
        return {"success": True, "processed": 0, "message": "No files in 10_Input to process."}
    threading.Thread(target=_run_process_input, daemon=True).start()
    return {
        "success": True,
        "processed": count,
        "message": f"Processing {count} file(s) in background. Check 11_Results in a few minutes. Watch the API window for progress.",
    }


if __name__ == "__main__":
    import webbrowser
    import threading

    def open_browser():
        import time
        time.sleep(2)
        webbrowser.open("http://127.0.0.1:8002/")

    threading.Thread(target=open_browser, daemon=True).start()
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
