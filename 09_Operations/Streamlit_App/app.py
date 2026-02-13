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
from aegislab_ui.review_queue import load_review_queue

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
st.sidebar.markdown("Use the page list below. Dashboard = health & metrics; Run Agent = execute; Review Queue = PI actions.")
st.sidebar.markdown("---")
root = get_root()
st.sidebar.markdown("**AEGISLAB_ROOT**")
st.sidebar.code(str(root), language=None)
with st.sidebar.expander("Tips"):
    st.markdown("- **Auto-route** unless you need an override (overrides are logged).")
    st.markdown("- Build **RAG** once after repo changes; use *Augment* when helpful.")
    st.markdown("- **Review Queue** is persisted (shared with Gradio and CLI).")

# Initialize session state for review queue (load from shared file so Streamlit + Gradio share one queue)
if "review_queue" not in st.session_state:
    st.session_state["review_queue"] = load_review_queue()

st.info(
    "Use the sidebar or **Dashboard** to start. Every agent run is logged; "
    "outputs require PI approval before committee use."
)
