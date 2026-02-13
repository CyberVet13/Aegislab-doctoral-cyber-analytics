"""
Run Agent — agent dropdown, template type, template preview, inputs, model selection, run → log + draft + review queue.
"""

import streamlit as st
from pathlib import Path
import json
import uuid

sys_path = str(Path(__file__).resolve().parent.parent)
if sys_path not in __import__("sys").path:
    __import__("sys").path.insert(0, sys_path)

from aegislab_ui.config import load_env, get_path, AGENT_NAMES, TEMPLATE_TYPES, MODEL_IDS, INPUT_DIR
from aegislab_ui.repo_validator import RepoValidator
from aegislab_ui.templates_loader import TemplatesLoader
from aegislab_ui.router import Router
from aegislab_ui.model_gateway import ModelGateway
from aegislab_ui.logging_audit import LoggingAudit
from aegislab_ui.metadata import inject_frontmatter
from aegislab_ui.safety import SafetyGuard
from aegislab_ui.rag import RAG
from aegislab_ui.review_queue import save_review_queue

load_env()

st.title("Run Agent")
st.caption("Select agent, template, and model; provide context. Output is logged and queued for PI review.")

validator = RepoValidator()
loader = TemplatesLoader()
router = Router()
gateway = ModelGateway()
safety = SafetyGuard()

# --- Start from Input (10_Input) — kick off workflow ---
input_dir = get_path(INPUT_DIR)
input_files = []
if input_dir.exists():
    input_files = sorted([f for f in input_dir.iterdir() if f.is_file() and f.suffix.lower() in (".md", ".txt", ".json")], key=lambda p: p.stat().st_mtime, reverse=True)
if input_files:
    st.caption("**Workflow trigger:** Content in `10_Input/` starts the process. Load a file below to fill context, then run the agent.")
    input_options = ["(none — type context manually)"] + [f.name for f in input_files]
    input_choice = st.selectbox("Load context from 10_Input", options=input_options, key="run_input_file")
    if input_choice and input_choice != "(none — type context manually)":
        if st.button("Load into context", key="run_load_input"):
            fp = input_dir / input_choice
            if fp.exists():
                try:
                    content = fp.read_text(encoding="utf-8", errors="replace")
                    st.session_state["run_objective"] = content
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not read file: {e}")
else:
    st.caption("Place prompts or briefs in **10_Input/** to start the workflow; they will appear here to load into context.")
st.markdown("---")

# --- Context ---
st.subheader("Context")
agent_options = loader.available_agents()
agent_num = st.selectbox(
    "Agent",
    options=agent_options,
    format_func=lambda x: AGENT_NAMES.get(x, f"Agent {x}"),
    key="run_agent_num",
)
template_type = st.selectbox("Template type", options=TEMPLATE_TYPES, key="run_template_type")
template_body = loader.get_template(agent_num, template_type)
with st.expander("Template preview", expanded=False):
    st.markdown(template_body or "*No template content*")

research_objective = st.text_area("Research objective / context", height=100, key="run_objective", placeholder="Describe the task and what the agent should produce.")
assumptions = st.text_input("Assumptions (optional)", key="run_assumptions", placeholder="e.g. Data is already normalized")
constraints = st.text_input("Constraints (optional)", key="run_constraints", placeholder="e.g. Max 2 pages")
citations_required = st.checkbox("Citations required", value=False, key="run_citations")

# --- Output ---
st.subheader("Output path")
output_placeholder = "e.g. 02_Agents/02_Applied_Research_Methodologist/Outputs/artifact.md or 11_Results/artifact.md"
output_path = st.text_input(
    "Path (relative to repo)",
    key="run_output_path",
    placeholder=output_placeholder,
    help="File will be created under AEGISLAB_ROOT. Use 02_Agents/.../Outputs/, 04_Praxis_Artifact/..., or 11_Results/ for completed deliverables.",
)

with st.expander("RAG (optional — augment with repo docs)"):
    rag = RAG()
    rag_ready = rag.is_ready()
    if rag_ready:
        st.caption("Index ready. Check below to inject retrieved context into the prompt.")
    else:
        st.caption("Build the index once (requires OPENAI_API_KEY). Indexes 00_Governance, 02_Agents, 03_Research_Methods, 04_Praxis_Artifact, Session_Logs, Decision_Logs.")
        if st.button("Build RAG index", key="run_build_rag"):
            with st.spinner("Building index..."):
                n, msg = rag.build_index()
                st.info(f"{msg}")
                st.rerun()
    augment_rag = st.checkbox("Augment this run with retrieved context from repo docs", value=False, key="run_augment_rag")
    if augment_rag and not rag_ready:
        st.warning("Build the RAG index first (click above) to use augmentation.")

if safety.defensive_scope_confirmation_required(research_objective or ""):
    st.warning(safety.get_defensive_scope_warning())
    defensive_confirmed = st.checkbox("I confirm this is defensive/authorized scope only", value=False, key="run_defensive")
else:
    defensive_confirmed = True

# --- Model ---
st.subheader("Model")
recommended = router.get_recommended_model(agent_num, template_type)
st.caption(f"Recommended for this agent/template: **{recommended}** (auto-route uses this).")
use_auto_route = st.radio("Model choice", ["Auto-route (recommended)", "Manual override"], key="run_model_choice", horizontal=True)
if use_auto_route == "Manual override":
    model_choice = st.selectbox("Override model", list(MODEL_IDS.keys()), key="run_model_override")
    rationale = st.text_area("Rationale for override (required; logged to Decision_Log)", key="run_rationale", placeholder="e.g. Need longer context for this task")
else:
    model_choice = recommended
    rationale = ""

if not validator.allowed_output_path(output_path or ""):
    if output_path:
        st.error("Output path must be inside the repository and not contain '..'.")

run_clicked = st.button("Run agent")
if run_clicked:
    if not output_path or not output_path.strip():
        st.error("Please set an output path.")
    elif not defensive_confirmed:
        st.error("Confirm defensive scope when the topic may involve offensive security.")
    elif use_auto_route == "Manual override" and not (rationale and rationale.strip()):
        st.error("Provide a rationale for manual model override.")
    else:
        allowed, msg = safety.check_prompt(research_objective or "")
        if not allowed:
            st.error(msg)
        else:
            if use_auto_route == "Manual override" and rationale:
                from aegislab_ui.logging_audit import append_decision_log
                router.log_override_rationale(agent_num, template_type, recommended, model_choice, rationale)
            prompt_summary = (research_objective or "")[:200]
            user_content = f"""**Context:** {research_objective}
**Assumptions:** {assumptions or 'None'}
**Constraints:** {constraints or 'None'}
**Citations required:** {citations_required}

**Task:** Execute the {template_type} template for this context. Output in markdown suitable for the given output path."""
            rag_block = ""
            if augment_rag:
                try:
                    rag = RAG()
                    if rag.is_ready():
                        rag_block = rag.get_context_block(research_objective or "", k=5)
                except Exception:
                    pass
            if rag_block:
                user_content = rag_block + "\n\n---\n\n" + user_content
            messages = [
                {"role": "user", "content": template_body + "\n\n---\n\n" + user_content},
            ]
            payload = {
                "agent": agent_num,
                "template_type": template_type,
                "model": model_choice,
                "research_objective": research_objective,
                "output_path": output_path,
            }
            try:
                result = gateway.call(model_choice, messages, temperature=0.5, max_tokens=4096)
                content = result.get("content", "")
            except Exception as e:
                st.exception(e)
                content = ""
            if content:
                if not validator.ensure_output_dir(output_path):
                    st.error("Output path is invalid or outside the repository. Choose a path under the repo (e.g. 02_Agents/02_Applied_Research_Methodologist/Outputs/artifact.md).")
                else:
                    session_id = str(uuid.uuid4())[:8]
                    from datetime import datetime
                    date = datetime.utcnow().strftime("%Y-%m-%d")
                    body_with_meta = inject_frontmatter(
                        content,
                        session_date=date,
                        model_used=model_choice,
                        prompt_summary=prompt_summary,
                        output_path=output_path,
                        pi_review_status="Draft",
                    )
                    out_full = get_path(output_path)
                    out_full.write_text(body_with_meta, encoding="utf-8")
                    LoggingAudit.run(
                        session_id=session_id,
                        agent_num=agent_num,
                        model_used=model_choice,
                        template_type=template_type,
                        prompt_summary=prompt_summary,
                        output_path=output_path,
                        prompt_payload=payload,
                        model_output_text=content,
                        artifact_name=out_full.stem,
                    )
                    if "review_queue" not in st.session_state:
                        st.session_state["review_queue"] = []
                    st.session_state["review_queue"].append({
                        "path": output_path,
                        "agent": agent_num,
                        "model": model_choice,
                        "date": date,
                        "preview": content[:500],
                    })
                    save_review_queue(st.session_state["review_queue"])
                    st.success(f"Run complete. Output written to `{output_path}`. Session logged. Draft added to Review Queue.")
                    st.expander("Model output preview").markdown(content[:2000] + ("..." if len(content) > 2000 else ""))
