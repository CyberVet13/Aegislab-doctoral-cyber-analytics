"""
Review Queue — list drafts with metadata, artifact content viewer, PI actions: Approve / Request Changes / Archive.
"""

import streamlit as st
from pathlib import Path
from datetime import datetime

sys_path = str(Path(__file__).resolve().parent.parent)
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from aegislab_ui.config import load_env, get_path, AGENT_NAMES
from aegislab_ui.metadata import parse_frontmatter, inject_frontmatter
from aegislab_ui.logging_audit import append_decision_log
from aegislab_ui.review_queue import save_review_queue, load_review_queue

load_env()

st.title("Review Queue")
st.caption("Drafts awaiting PI action. Approve (committee-ready), request changes, or archive (logged).")

col_refresh, col_batch, col_select = st.columns([1, 1, 1])
with col_refresh:
    if st.button("Refresh from disk", help="Reload queue from shared file (picks up items added by Gradio or CLI)"):
        st.session_state["review_queue"] = load_review_queue()
        st.rerun()

if "review_queue" not in st.session_state:
    st.session_state["review_queue"] = load_review_queue()
queue = st.session_state["review_queue"]

if "batch_selected" not in st.session_state:
    st.session_state["batch_selected"] = {}

with col_batch:
    if st.button("✓ Approve all", help="Approve all items in queue (batch); log each to Decision_Log"):
        approved = []
        remaining = []
        for item in queue:
            path = item.get("path", "")
            full_path = get_path(path)
            if full_path.exists():
                text = full_path.read_text(encoding="utf-8", errors="replace")
                meta, body = parse_frontmatter(text)
                meta["PI_Review_Status"] = "Approved"
                extra = {k: v for k, v in meta.items() if k not in ("Session_Date", "Model_Used", "Prompt_Summary", "Output_Path", "PI_Review_Status", "AI_Assisted")}
                new_text = inject_frontmatter(
                    body,
                    session_date=meta.get("Session_Date", item.get("date", "")),
                    model_used=meta.get("Model_Used", item.get("model", "")),
                    prompt_summary=meta.get("Prompt_Summary", ""),
                    output_path=path,
                    pi_review_status="Approved",
                    extra=extra if extra else None,
                )
                full_path.write_text(new_text, encoding="utf-8")
                append_decision_log(
                    datetime.utcnow().strftime("%Y-%m-%d"),
                    "PI_Approval",
                    f"\n- **Artifact:** {path}\n- **Action:** Approved (batch)\n",
                )
                approved.append(path)
            else:
                remaining.append(item)
        st.session_state["review_queue"] = remaining
        save_review_queue(remaining)
        st.success(f"Approved {len(approved)} item(s).")
        st.rerun()

with col_select:
    selected_paths = [path for path, checked in st.session_state.get("batch_selected", {}).items() if checked]
    if st.button("✓ Approve selected", help="Approve only checked items; review before approving", disabled=len(selected_paths) == 0):
        approved = []
        remaining = []
        for item in queue:
            path = item.get("path", "")
            if path not in selected_paths:
                remaining.append(item)
                continue
            full_path = get_path(path)
            if full_path.exists():
                text = full_path.read_text(encoding="utf-8", errors="replace")
                meta, body = parse_frontmatter(text)
                meta["PI_Review_Status"] = "Approved"
                extra = {k: v for k, v in meta.items() if k not in ("Session_Date", "Model_Used", "Prompt_Summary", "Output_Path", "PI_Review_Status", "AI_Assisted")}
                new_text = inject_frontmatter(
                    body,
                    session_date=meta.get("Session_Date", item.get("date", "")),
                    model_used=meta.get("Model_Used", item.get("model", "")),
                    prompt_summary=meta.get("Prompt_Summary", ""),
                    output_path=path,
                    pi_review_status="Approved",
                    extra=extra if extra else None,
                )
                full_path.write_text(new_text, encoding="utf-8")
                append_decision_log(
                    datetime.utcnow().strftime("%Y-%m-%d"),
                    "PI_Approval",
                    f"\n- **Artifact:** {path}\n- **Action:** Approved (selected)\n",
                )
                approved.append(path)
            else:
                remaining.append(item)
        st.session_state["review_queue"] = remaining
        st.session_state["batch_selected"] = {k: v for k, v in st.session_state.get("batch_selected", {}).items() if k not in selected_paths}
        save_review_queue(remaining)
        st.success(f"Approved {len(approved)} selected item(s).")
        st.rerun()

if not queue:
    st.info("No items in review queue. Run an agent from **Run Agent** (or Gradio/CLI) to add drafts. Use **Refresh from disk** if you added items elsewhere.")
    st.stop()

st.caption("Check items to approve, then click **Approve selected**. Or use **Approve all** to approve everything.")
st.markdown("---")

for i, item in enumerate(queue[:20]):
    path = item.get("path", "")
    agent = item.get("agent", 0)
    model = item.get("model", "")
    date = item.get("date", "")
    preview = item.get("preview", "")
    agent_label = AGENT_NAMES.get(agent, f"Agent {agent}")
    with st.container():
        col_chk, col_info = st.columns([0.5, 9.5])
        with col_chk:
            key = f"select_{i}_{path.replace('/', '_')}"
            checked = st.checkbox("", key=key, value=st.session_state["batch_selected"].get(path, False), label_visibility="collapsed")
            st.session_state["batch_selected"][path] = checked
        with col_info:
            st.markdown(f"**{path}**")
        st.caption(f"{agent_label} · {model} · {date}")
        full_path = get_path(path)
        if full_path.exists():
            content = full_path.read_text(encoding="utf-8", errors="replace")
            meta, body = parse_frontmatter(content)
            with st.expander("View content"):
                st.markdown(body or content[:3000])
        else:
            st.caption("File not found at path.")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✓ Approve", key=f"approve_{i}_{path.replace('/', '_')}", help="Mark artifact approved; update front-matter; log decision"):
                if full_path.exists():
                    text = full_path.read_text(encoding="utf-8", errors="replace")
                    meta, body = parse_frontmatter(text)
                    meta["PI_Review_Status"] = "Approved"
                    extra = {k: v for k, v in meta.items() if k not in ("Session_Date", "Model_Used", "Prompt_Summary", "Output_Path", "PI_Review_Status", "AI_Assisted")}
                    new_text = inject_frontmatter(
                        body,
                        session_date=meta.get("Session_Date", date),
                        model_used=meta.get("Model_Used", model),
                        prompt_summary=meta.get("Prompt_Summary", ""),
                        output_path=path,
                        pi_review_status="Approved",
                        extra=extra if extra else None,
                    )
                    full_path.write_text(new_text, encoding="utf-8")
                    append_decision_log(
                        datetime.utcnow().strftime("%Y-%m-%d"),
                        "PI_Approval",
                        f"\n- **Artifact:** {path}\n- **Action:** Approved\n",
                    )
                    st.session_state["review_queue"] = [q for q in queue if q.get("path") != path]
                    save_review_queue(st.session_state["review_queue"])
                    st.rerun()
                else:
                    st.error("Artifact file not found. Cannot approve; remove from queue or fix path.")
        with col2:
            if st.button("↻ Request changes", key=f"request_{i}_{path.replace('/', '_')}", help="Log decision; remove from queue"):
                append_decision_log(
                    datetime.utcnow().strftime("%Y-%m-%d"),
                    "PI_Request_Changes",
                    f"\n- **Artifact:** {path}\n- **Action:** Request changes\n",
                )
                st.session_state["review_queue"] = [q for q in queue if q.get("path") != path]
                save_review_queue(st.session_state["review_queue"])
                st.rerun()
        with col3:
            if st.button("Archive", key=f"archive_{i}_{path.replace('/', '_')}", help="Log as archived (not for committee); remove from queue"):
                append_decision_log(
                    datetime.utcnow().strftime("%Y-%m-%d"),
                    "PI_Archive",
                    f"\n- **Artifact:** {path}\n- **Action:** Archived (not for committee use)\n",
                )
                st.session_state["review_queue"] = [q for q in queue if q.get("path") != path]
                save_review_queue(st.session_state["review_queue"])
                st.rerun()
        st.markdown("---")
