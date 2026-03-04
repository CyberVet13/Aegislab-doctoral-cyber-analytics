"""
AegisLab Operational Console — kickoff UI and main shell.
- Landing: Launch pad for agentic AI environment.
- Multipage: Dashboard, Run Agent, Review Queue, Governance Audit, Settings.
"""

import sys
import streamlit as st
from pathlib import Path

# Ensure app directory is on path and load .env
_app_dir = str(Path(__file__).resolve().parent)
if _app_dir not in sys.path:
    sys.path.insert(0, _app_dir)

from aegislab_ui.config import load_env, get_root, get_path, AGENT_NAMES, SESSION_LOGS_DIR
from aegislab_ui.repo_validator import RepoValidator
from aegislab_ui.review_queue import load_review_queue

load_env()

st.set_page_config(
    page_title="AegisLab — Agentic AI Environment",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state for review queue
if "review_queue" not in st.session_state:
    st.session_state["review_queue"] = load_review_queue()

# --- Sidebar ---
st.sidebar.markdown("### Navigation")
st.sidebar.markdown("Dashboard • Run Agent • Review Queue • Governance • Settings")
st.sidebar.markdown("---")
root = get_root()
st.sidebar.markdown("**AEGISLAB_ROOT**")
st.sidebar.code(str(root), language=None)
with st.sidebar.expander("Tips"):
    st.markdown("- **Auto-route** unless you need an override (overrides are logged).")
    st.markdown("- Build **RAG** once after repo changes; use *Augment* when helpful.")
    st.markdown("- **Review Queue** is persisted (shared with Gradio and CLI).")

# --- Kickoff / Launcher UI ---
st.title("🛡️ AegisLab — Agentic AI Environment")
st.caption("Doctoral research environment • Committee-defensible • Full audit trail")

# Repo info
REPO_URL = "https://github.com/CyberVet13/Aegislab-doctoral-cyber-analytics"
REPO_BRANCH = "branch02132026"
st.markdown(f"**Repository:** [{REPO_URL}]({REPO_URL}) • **Branch:** `{REPO_BRANCH}`")
st.markdown("---")

# Quick status
validator = RepoValidator()
ok, missing = validator.validate_structure()
logs_dir = get_path(SESSION_LOGS_DIR)
session_count = len([f for f in logs_dir.glob("*.md")]) if logs_dir.exists() else 0
queue_count = len(st.session_state.get("review_queue", []))

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Repo structure", "✓ Valid" if ok else "⚠ Issues")
with col2:
    st.metric("Session logs", session_count)
with col3:
    st.metric("Pending reviews", queue_count)
with col4:
    st.metric("Agents", "11")

# Primary action: Launch Run Agent
st.markdown("### Launch")
st.markdown("Start an agent run: select agent, template, context, and output path.")

if st.button("▶ **Run Agent**", type="primary", use_container_width=True):
    st.switch_page("pages/2_Run_Agent.py")

st.markdown("---")

# Agent quick reference
st.markdown("### Agents (11)")
cols = st.columns(3)
for i, (num, name) in enumerate(AGENT_NAMES.items()):
    with cols[i % 3]:
        st.markdown(f"**{num}** {name}")

st.markdown("---")

# Quick links
st.markdown("### Quick links")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("📊 Dashboard", use_container_width=True):
        st.switch_page("pages/1_Dashboard.py")
with c2:
    if st.button("📋 Review Queue", use_container_width=True):
        st.switch_page("pages/3_Review_Queue.py")
with c3:
    if st.button("⚙️ Settings", use_container_width=True):
        st.switch_page("pages/5_Settings_Routing.py")

st.info(
    "Every agent run is logged; outputs require PI approval before committee use. "
    "Use **Run Agent** to execute; **Review Queue** to approve or request changes."
)
