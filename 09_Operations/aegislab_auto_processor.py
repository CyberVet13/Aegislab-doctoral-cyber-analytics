"""
AegisLab Auto-Processor — Monitors 10_Input and triggers agent runs when new files appear.
- Uses watchdog to detect new files in 10_Input
- Processes up to 3 files in parallel (ThreadPoolExecutor)
- Outputs saved to 11_Results
Usage: python aegislab_auto_processor.py
"""

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("Installing watchdog...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "watchdog", "-q"])
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

# Paths
_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent
_INPUT_DIR = _REPO_ROOT / "10_Input"
_OUTPUT_DIR = _REPO_ROOT / "11_Results"
_SCRIPTS_DIR = _SCRIPT_DIR / "scripts"  # 09_Operations/scripts
_RUN_AGENT = _SCRIPTS_DIR / "run_agent_cli.py"

ALLOWED_EXT = {".pdf", ".docx", ".txt", ".md", ".xlsx", ".pptx", ".json"}
_MAX_PARALLEL = 3
_executor = ThreadPoolExecutor(max_workers=_MAX_PARALLEL)


def _process_file_worker(file_path: Path) -> None:
    """Run agent on one file (called from thread pool)."""
    rel_input = f"10_Input/{file_path.name}"
    base = file_path.stem
    safe_base = "".join(c if c.isalnum() or c in " -_" else "_" for c in base)
    rel_output = f"11_Results/{safe_base}_deliverable.md"

    print(f"\n{'='*60}")
    print(f"📁 NEW FILE: {file_path.name}")
    print(f"   Size: {file_path.stat().st_size / 1024:.1f} KB")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    print("🚀 Starting agentic AI workflow...")
    print(f"   Input:  {rel_input}")
    print(f"   Output: {rel_output}")
    print()

    cmd = [
        sys.executable,
        str(_RUN_AGENT),
        "--input", rel_input,
        "--agent", "2",
        "--template-type", "Daily Driver",
        "--output", rel_output,
    ]
    try:
        result = subprocess.run(cmd, cwd=str(_REPO_ROOT), capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(f"✅ Complete: {rel_output}")
        else:
            print(f"❌ Error: {result.stderr or result.stdout}")
    except subprocess.TimeoutExpired:
        print("❌ Timeout (5 min)")
    except Exception as e:
        print(f"❌ {e}")
    print(f"\n📂 Results: {_OUTPUT_DIR}\n")


class InputHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.processed = set()

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() not in ALLOWED_EXT:
            return
        if path.name.startswith(".") or "~" in path.name:
            return
        # Debounce: avoid processing same file twice
        key = str(path)
        if key in self.processed:
            return
        self.processed.add(key)
        _executor.submit(_process_file_worker, path)


def main():
    if not _INPUT_DIR.exists():
        _INPUT_DIR.mkdir(parents=True)
    if not _OUTPUT_DIR.exists():
        _OUTPUT_DIR.mkdir(parents=True)
    if not _RUN_AGENT.exists():
        print(f"Error: run_agent_cli.py not found at {_RUN_AGENT}")
        sys.exit(1)

    print("=" * 60)
    print("🤖 AEGISLAB AUTO-PROCESSOR")
    print("=" * 60)
    print(f"Monitoring: {_INPUT_DIR}")
    print(f"Output to:  {_OUTPUT_DIR}")
    print()
    print("Waiting for files in 10_Input... (Ctrl+C to stop)")
    print("=" * 60)

    handler = InputHandler()
    observer = Observer()
    observer.schedule(handler, str(_INPUT_DIR), recursive=False)
    observer.start()
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        _executor.shutdown(wait=False)
        print("\nStopped.")


if __name__ == "__main__":
    main()
