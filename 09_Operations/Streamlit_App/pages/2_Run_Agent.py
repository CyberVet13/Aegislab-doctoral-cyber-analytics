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

from aegislab_ui.config import load_env, get_path, AGENT_NAMES, TEMPLATE_TYPES, MODEL_IDS
from aegislab_ui.repo_validator import RepoValidator
from aegislab_ui.templates_loader import TemplatesLoader
from aegislab_ui.router import Router
from aegislab_ui.model_gateway import ModelGateway
from aegislab_ui.logging_audit import LoggingAudit
from aegislab_ui.metadata import inject_frontmatter
from aegislab_ui.safety import SafetyGuard

load_env()

st.title("Run Agent")
st.markdown("Select agent, template, and model; provide context. Output is logged and queued for PI review.")

validator = RepoValidator()
loader = TemplatesLoader()
router = Router()
gateway = ModelGateway()
safety = SafetyGuard()

agent_options = loader.available_agents()
agent_num = st.selectbox(
    "Agent",
    options=agent_options,
    format_func=lambda x: AGENT_NAMES.get(x, f"Agent {x}"),
    key="run_agent_num",
)
template_type = st.selectbox("Template type", options=TEMPLATE_TYPES, key="run_template_type")
template_body = loader.get_template(agent_num, template_type)
st.expander("Template preview").markdown(template_body or "*No template content*")

research_objective = st.text_area("Research objective / context", height=100, key="run_objective")
assumptions = st.text_input("Assumptions (optional)", key="run_assumptions")
constraints = st.text_input("Constraints (optional)", key="run_constraints")
citations_required = st.checkbox("Citations required", value=False, key="run_citations")
output_path = st.text_input(
    "Output path (relative to repo, e.g. 02_Agents/02_Applied_Research_Methodologist/Outputs/artifact.md)",
    key="run_output_path",
)

if safety.defensive_scope_confirmation_required(research_objective or ""):
    st.warning(safety.get_defensive_scope_warning())
    defensive_confirmed = st.checkbox("I confirm this is defensive/authorized scope only", value=False, key="run_defensive")
else:
    defensive_confirmed = True

use_auto_route = st.radio("Model", ["Auto-route (recommended)", "Manual override"], key="run_model_choice")
recommended = router.get_recommended_model(agent_num, template_type)
if use_auto_route == "Manual override":
    model_choice = st.selectbox("Model", list(MODEL_IDS.keys()), key="run_model_override")
    rationale = st.text_area("Rationale for override (required)", key="run_rationale")
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
                validator.ensure_output_dir(output_path)
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
                st.success(f"Run complete. Output written to `{output_path}`. Session logged. Draft added to Review Queue.")
                st.expander("Model output preview").markdown(content[:2000] + ("..." if len(content) > 2000 else ""))
