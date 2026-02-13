"""
Shared review queue — load/save to 09_Operations/Gradio_App/review_queue.json.
Streamlit and Gradio (and CLI/Workflow API) use this file so the queue is shared and persisted.
"""

import json
from .config import get_path, REVIEW_QUEUE_PATH


def _queue_path():
    parts = REVIEW_QUEUE_PATH.replace("\\", "/").split("/")
    return get_path(*parts)


def load_review_queue():
    """Load queue from disk; return list of items (path, agent, model, date, preview)."""
    path = _queue_path()
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_review_queue(queue: list):
    """Write queue to disk (shared with Gradio and CLI)."""
    path = _queue_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(queue, indent=2), encoding="utf-8")
