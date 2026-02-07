"""
Governance Audit — filterable session logs table (date, agent, model, hashes), diff-friendly summaries, optional committee packet export.
"""

import streamlit as st
from pathlib import Path
import re
import zipfile
from datetime import datetime

sys_path = str(Path(__file__).resolve().parent.parent)
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from aegislab_ui.config import load_env, get_path, SESSION_LOGS_DIR, DECISION_LOGS_DIR

load_env()

st.title("Governance Audit")
st.caption("Session logs and decision logs; filter by date/agent; export committee packet ZIP.")

logs_dir = get_path(SESSION_LOGS_DIR)
decision_dir = get_path(DECISION_LOGS_DIR)

session_files = sorted(logs_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True) if logs_dir.exists() else []
session_files = [f for f in session_files if f.name != "README.md"]

filter_date = st.text_input("Filter by date (YYYY-MM-DD)", key="audit_date")
filter_agent = st.text_input("Filter by agent (e.g. 02)", key="audit_agent")

rows = []
for f in session_files:
    name = f.name
    date_part = name[:10] if len(name) >= 10 else ""
    agent_part = ""
    m = re.search(r"Agent(\d+)", name)
    if m:
        agent_part = m.group(1)
    if filter_date and filter_date not in date_part:
        continue
    if filter_agent and filter_agent not in agent_part:
        continue
    try:
        text = f.read_text(encoding="utf-8", errors="replace")
    except Exception:
        text = ""
    prompt_hash = ""
    output_hash = ""
    for line in text.split("\n"):
        if "prompt_payload_sha256" in line:
            prompt_hash = line.split("`")[1] if "`" in line else ""
        if "model_output_sha256" in line:
            output_hash = line.split("`")[1] if "`" in line else ""
    model_used = "—"
    for line in text.split("\n"):
        if line.startswith("- **Model:**"):
            model_used = line.replace("- **Model:**", "").strip()
            break
    rows.append({"date": date_part, "agent": agent_part, "model": model_used, "prompt_hash": prompt_hash[:16] + "…" if len(prompt_hash) > 16 else prompt_hash, "output_hash": output_hash[:16] + "…" if len(output_hash) > 16 else output_hash, "file": name})

if rows:
    st.dataframe(rows, use_container_width=True, column_config={"file": st.column_config.TextColumn("Log file")})
else:
    st.info("No session logs match filters (or no logs yet).")

st.subheader("Session log content (diff-friendly)")
log_choice = st.selectbox("Select log", [r["file"] for r in rows], key="audit_log_choice") if rows else None
if log_choice and logs_dir.exists():
    fp = logs_dir / log_choice
    if fp.exists():
        st.text(fp.read_text(encoding="utf-8", errors="replace"))

st.subheader("Committee packet export")
if st.button("Generate ZIP (session + decision logs)"):
    zip_path = get_path("09_Operations", "committee_packet.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in session_files:
            zf.write(f, str(Path(SESSION_LOGS_DIR) / f.name))
        if decision_dir.exists():
            for f in decision_dir.glob("*.md"):
                zf.write(f, str(Path(DECISION_LOGS_DIR) / f.name))
    st.success(f"Created {zip_path}. Download below.")
    st.download_button("Download ZIP", data=zip_path.read_bytes(), file_name="committee_packet.zip", mime="application/zip", key="dl_zip")
