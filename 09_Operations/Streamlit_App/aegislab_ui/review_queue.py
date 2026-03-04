"""
Shared review queue — load/save to 09_Operations/Gradio_App/review_queue.json.
Streamlit and Gradio (and CLI/Workflow API) use this file so the queue is shared and persisted.
Uses filelock for safe concurrent access across processes.
"""

import json
from .config import get_path, REVIEW_QUEUE_PATH

try:
    from filelock import FileLock
except ImportError:
    FileLock = None


def _queue_path():
    parts = REVIEW_QUEUE_PATH.replace("\\", "/").split("/")
    return get_path(*parts)


def _with_lock(fn):
    """Acquire file lock before read/write. Lock file is queue_path + '.lock'."""
    path = _queue_path()
    lock_path = path.parent / (path.name + ".lock")
    if FileLock:
        lock = FileLock(lock_path, timeout=10)
        lock.acquire()
        try:
            return fn(path)
        finally:
            lock.release()
    return fn(path)


def load_review_queue():
    """Load queue from disk; return list of items (path, agent, model, date, preview)."""
    def _read(p):
        if not p.exists():
            return []
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except Exception:
            return []
    return _with_lock(_read)


def save_review_queue(queue: list):
    """Write queue to disk (shared with Gradio and CLI)."""
    def _write(p):
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(queue, indent=2), encoding="utf-8")
    _with_lock(_write)


def append_to_review_queue(output_path: str, agent_num: int, model_choice: str, date: str, content: str) -> None:
    """Append one item to queue with lock. Used by run_agent_cli."""
    def _append(p):
        queue = []
        if p.exists():
            try:
                queue = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                pass
            queue = queue if isinstance(queue, list) else []
        queue.append({
            "path": output_path,
            "agent": agent_num,
            "model": model_choice,
            "date": date,
            "preview": content[:500],
        })
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(queue, indent=2), encoding="utf-8")
    _with_lock(_append)
