"""
AegisLab Workflow API — HTTP endpoint for n8n (or other tools) to trigger agent runs.
- POST /run-agent with JSON body → runs agent via run_agent_cli.run(); returns JSON.
- Bind to 127.0.0.1:8000 (localhost only).
"""

import sys
from pathlib import Path

_API_DIR = Path(__file__).resolve().parent
_SCRIPTS_DIR = _API_DIR.parent / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from run_agent_cli import run as run_agent

app = FastAPI(title="AegisLab Workflow API", description="Trigger agent runs for n8n or other callers")


class RunAgentRequest(BaseModel):
    input_path: str = Field(..., description="Repo-relative path to context file, e.g. 10_Input/brief.md")
    agent_num: int = Field(..., ge=1, le=11, description="Agent number 1-11")
    template_type: str = Field(default="Daily Driver", description="Daily Driver | Deep Dive | Review/QA")
    output_path: str = Field(..., description="Repo-relative output path, e.g. 11_Results/artifact.md")
    assumptions: str = Field(default="", description="Optional assumptions")
    constraints: str = Field(default="", description="Optional constraints")
    model_override: str = Field(default="", description="Override model; requires override_rationale")
    override_rationale: str = Field(default="", description="Rationale for override (logged)")


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
    )
    if ok:
        return {"success": True, "message": msg}
    raise HTTPException(status_code=400, detail=msg)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
