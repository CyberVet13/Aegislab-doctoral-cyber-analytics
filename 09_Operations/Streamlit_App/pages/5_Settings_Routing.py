"""
Settings / Routing — display routing rules, per-agent default model (editable via local config), change rationale, log to Change_Log + Decision_Logs.
"""

import streamlit as st
from pathlib import Path

sys_path = str(Path(__file__).resolve().parent.parent)
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from aegislab_ui.config import (
    load_env,
    get_path,
    AGENT_NAMES,
    TEMPLATE_TYPES,
    MODEL_IDS,
    CHANGE_LOG_PATH,
)
from aegislab_ui.router import Router, DEFAULT_BY_TEMPLATE, AGENT_DEFAULT_MODEL
from aegislab_ui.logging_audit import append_decision_log

load_env()

st.title("Settings / Routing")
st.caption("Routing rules and model defaults. Override rationale is logged to Decision_Logs.")

st.subheader("Default by template type")
for tt in TEMPLATE_TYPES:
    rec = Router.get_recommended_model(1, tt)
    st.markdown(f"- **{tt}:** {rec}")

st.subheader("Per-agent default (overrides template default when set)")
for agent_num in range(1, 12):
    override = AGENT_DEFAULT_MODEL.get(agent_num)
    name = AGENT_NAMES.get(agent_num, f"Agent {agent_num}")
    st.markdown(f"- **{name}:** {override or 'Use template default'}")

st.subheader("Available models")
for display, api_id in MODEL_IDS.items():
    st.code(f"{display} → {api_id}", language=None)

st.subheader("Change log")
st.markdown("Routing or config changes should be recorded in `00_Governance/Change_Log.md` and in `09_Operations/Decision_Logs/`.")
change_log_path = get_path(CHANGE_LOG_PATH)
if change_log_path.exists():
    st.expander("View Change_Log.md").markdown(change_log_path.read_text(encoding="utf-8", errors="replace")[:3000])
else:
    st.caption("Change_Log.md not found.")

rationale_note = st.text_area("Note for auditors: routing rationale (saved to Decision_Log on next override)", key="settings_rationale_note")
if st.button("Append routing note to Decision_Log"):
    if rationale_note.strip():
        from datetime import datetime
        append_decision_log(
            datetime.utcnow().strftime("%Y-%m-%d"),
            "Routing_Note",
            f"\n**Note:** {rationale_note}\n",
        )
        st.success("Appended to Decision_Log.")
    else:
        st.warning("Enter a note first.")
