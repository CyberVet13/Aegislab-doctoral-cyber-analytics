"""
Dashboard — repository health, missing files, last 10 sessions, pending reviews count.
"""

import streamlit as st
from pathlib import Path
from datetime import datetime

sys_path = str(Path(__file__).resolve().parent.parent)
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from aegislab_ui.config import load_env, get_path, SESSION_LOGS_DIR
from aegislab_ui.repo_validator import RepoValidator

load_env()

st.title("Dashboard")
st.caption("Repository health, recent sessions, and pending PI reviews.")

validator = RepoValidator()
ok, missing = validator.validate_structure()

# Metric cards
logs_dir = get_path(SESSION_LOGS_DIR)
session_files = []
if logs_dir.exists():
    session_files = [f for f in logs_dir.glob("*.md") if f.name != "README.md"]
queue = st.session_state.get("review_queue", [])
queue_count = len(queue)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Session logs", len(session_files))
with col2:
    st.metric("Pending reviews", queue_count)
with col3:
    status = "Valid" if ok else "Issues"
    st.metric("Repo structure", status)

if ok:
    st.success("Repository structure valid — required dirs and key files present.")
else:
    st.error("Repository structure issues:")
    for m in missing:
        st.markdown(f"- {m}")

st.subheader("Last 10 sessions")
if not logs_dir.exists():
    st.warning("No session logs directory yet.")
else:
    files = sorted(session_files, key=lambda p: p.stat().st_mtime, reverse=True)[:10]
    if not files:
        st.info("No session logs yet. Use **Run Agent** to create logs.")
    else:
        for f in files:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            st.markdown(f"- `{f.name}` — {mtime.strftime('%Y-%m-%d %H:%M')}")

st.subheader("Pending reviews")
if queue_count == 0:
    st.info("No drafts in review queue. Approved/archived artifacts are removed from queue.")
else:
    st.warning(f"**{queue_count}** draft(s) awaiting PI action. Open **Review Queue** to approve or request changes.")
