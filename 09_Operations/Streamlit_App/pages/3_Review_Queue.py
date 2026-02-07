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
from aegislab_ui.metadata import parse_frontmatter
from aegislab_ui.logging_audit import append_decision_log

load_env()

st.title("Review Queue")
st.markdown("Drafts awaiting PI action. Approve, request changes, or archive.")

queue = st.session_state.get("review_queue", [])
if not queue:
    st.info("No items in review queue. Run an agent from **Run Agent** to add drafts.")
    st.stop()

for i, item in enumerate(queue[:20]):
    path = item.get("path", "")
    agent = item.get("agent", 0)
    model = item.get("model", "")
    date = item.get("date", "")
    preview = item.get("preview", "")
    with st.container():
        st.markdown(f"**{path}** — Agent {agent} — {model} — {date}")
        full_path = get_path(path)
        if full_path.exists():
            content = full_path.read_text(encoding="utf-8", errors="replace")
            meta, body = parse_frontmatter(content)
            st.expander("View content").markdown(body or content[:3000])
        else:
            st.caption("File not found at path.")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Approve", key=f"approve_{i}_{path.replace('/', '_')}"):
                if full_path.exists():
                    text = full_path.read_text(encoding="utf-8", errors="replace")
                    meta, body = parse_frontmatter(text)
                    meta["PI_Review_Status"] = "Approved"
                    from aegislab_ui.metadata import inject_frontmatter
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
                    st.rerun()
                else:
                    st.error("Artifact file not found. Cannot approve; remove from queue or fix path.")
        with col2:
            if st.button("Request changes", key=f"request_{i}_{path.replace('/', '_')}"):
                append_decision_log(
                    datetime.utcnow().strftime("%Y-%m-%d"),
                    "PI_Request_Changes",
                    f"\n- **Artifact:** {path}\n- **Action:** Request changes\n",
                )
                st.session_state["review_queue"] = [q for q in queue if q.get("path") != path]
                st.rerun()
        with col3:
            if st.button("Archive", key=f"archive_{i}_{path.replace('/', '_')}"):
                append_decision_log(
                    datetime.utcnow().strftime("%Y-%m-%d"),
                    "PI_Archive",
                    f"\n- **Artifact:** {path}\n- **Action:** Archived (not for committee use)\n",
                )
                st.session_state["review_queue"] = [q for q in queue if q.get("path") != path]
                st.rerun()
        st.markdown("---")
