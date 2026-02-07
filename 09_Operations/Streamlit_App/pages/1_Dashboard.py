"""
Dashboard — repository health, missing files, last 10 sessions, pending reviews count.
"""

import streamlit as st
from pathlib import Path
from datetime import datetime, timedelta

sys_path = str(Path(__file__).resolve().parent.parent)
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from aegislab_ui.config import load_env, get_path, SESSION_LOGS_DIR
from aegislab_ui.repo_validator import RepoValidator

load_env()

st.title("Dashboard")
st.markdown("Repository health, recent sessions, and pending PI reviews.")

validator = RepoValidator()
ok, missing = validator.validate_structure()

if ok:
    st.success("✅ Repository structure valid — required dirs and key files present.")
else:
    st.error("❌ Repository structure issues:")
    for m in missing:
        st.markdown(f"- {m}")

st.subheader("Last 10 sessions")
logs_dir = get_path(SESSION_LOGS_DIR)
if not logs_dir.exists():
    st.warning("No session logs directory yet.")
else:
    files = sorted(logs_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    files = [f for f in files if f.name != "README.md"][:10]
    if not files:
        st.info("No session logs yet. Run an agent from **Run Agent** to create logs.")
    else:
        for f in files:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            st.markdown(f"- `{f.name}` — {mtime.strftime('%Y-%m-%d %H:%M')}")

st.subheader("Pending reviews")
queue = st.session_state.get("review_queue", [])
count = len(queue)
if count == 0:
    st.info("No drafts in review queue. Approved/archived artifacts are removed from queue.")
else:
    st.warning(f"**{count}** draft(s) awaiting PI action. Open **Review Queue** to approve or request changes.")
