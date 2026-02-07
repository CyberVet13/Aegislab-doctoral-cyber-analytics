"""
AegisLab Operational Console — main Streamlit shell.
- Multipage app: Dashboard, Run Agent, Review Queue, Governance Audit, Settings/Routing.
- No chatbot; agent management, LLM session execution, governance, audit trail.
"""

import sys
import streamlit as st
from pathlib import Path

# Ensure app directory is on path and load .env
_app_dir = str(Path(__file__).resolve().parent)
if _app_dir not in sys.path:
    sys.path.insert(0, _app_dir)

from aegislab_ui.config import load_env, get_root, AGENT_NAMES

load_env()

st.set_page_config(
    page_title="AegisLab — Operational Console",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🛡️ AegisLab — Operational Console")
st.caption("Doctoral research environment • Committee-defensible • Full audit trail")

st.sidebar.markdown("### Navigation")
st.sidebar.markdown("- **Dashboard** — Repository health, pending reviews")
st.sidebar.markdown("- **Run Agent** — Execute agent session with governance")
st.sidebar.markdown("- **Review Queue** — PI approval / Request changes / Archive")
st.sidebar.markdown("- **Governance Audit** — Session logs, hashes, export")
st.sidebar.markdown("- **Settings / Routing** — Model defaults, rationale logging")

root = get_root()
st.sidebar.markdown("---")
st.sidebar.markdown(f"**AEGISLAB_ROOT**")
st.sidebar.code(str(root), language=None)

# Initialize session state for review queue (drafts pending PI action)
if "review_queue" not in st.session_state:
    st.session_state["review_queue"] = []

st.info(
    "Use the sidebar or **Dashboard** to start. Every agent run is logged; "
    "outputs require PI approval before committee use."
)
