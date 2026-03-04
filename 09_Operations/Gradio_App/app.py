"""
AegisLab Gradio — workflow manager.
- Reuses aegislab_ui from Streamlit_App (config, router, model_gateway, logging_audit, etc.).
- Tabs: Workflow (10_Input + Run Agent), Review Queue, Session Logs, Settings.
- Review queue persisted in review_queue.json (Gradio_App folder).
"""

import sys
import uuid
from pathlib import Path
from datetime import datetime

# Add Streamlit_App so we can import aegislab_ui
_GRADIO_DIR = Path(__file__).resolve().parent
_STREAMLIT_APP = _GRADIO_DIR.parent / "Streamlit_App"
if _GRADIO_DIR.parent / "Streamlit_App" != _STREAMLIT_APP:
    _STREAMLIT_APP = _GRADIO_DIR.parent / "Streamlit_App"
if str(_STREAMLIT_APP) not in sys.path:
    sys.path.insert(0, str(_STREAMLIT_APP))

from aegislab_ui.config import (
    load_env,
    get_root,
    get_path,
    AGENT_NAMES,
    TEMPLATE_TYPES,
    MODEL_IDS,
    INPUT_DIR,
    SESSION_LOGS_DIR,
)
from aegislab_ui.review_queue import load_review_queue, save_review_queue
from aegislab_ui.repo_validator import RepoValidator
from aegislab_ui.templates_loader import TemplatesLoader
from aegislab_ui.router import Router
from aegislab_ui.model_gateway import ModelGateway
from aegislab_ui.logging_audit import LoggingAudit, append_decision_log
from aegislab_ui.metadata import inject_frontmatter, parse_frontmatter
from aegislab_ui.safety import SafetyGuard

load_env()


def _load_queue():
    return load_review_queue()


def _save_queue(queue):
    save_review_queue(queue)


def list_input_files():
    input_dir = get_path(INPUT_DIR)
    if not input_dir.exists():
        return []
    return sorted(
        [f.name for f in input_dir.iterdir() if f.is_file() and f.suffix.lower() in (".md", ".txt", ".json")],
        key=lambda n: (input_dir / n).stat().st_mtime,
        reverse=True,
    )


def load_input_into_context(filename):
    if not filename or filename == "(none)":
        return ""
    input_dir = get_path(INPUT_DIR)
    fp = input_dir / filename
    if not fp.exists():
        return ""
    try:
        return fp.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def run_agent(agent_num, template_type, model_choice, research_objective, assumptions, constraints, output_path, use_override, override_rationale, defensive_confirmed=True):
    if not output_path or not output_path.strip():
        return "Error: Set an output path.", ""
    validator = RepoValidator()
    if not validator.allowed_output_path(output_path):
        return "Error: Output path must be inside the repo (no '..').", ""
    safety = SafetyGuard()
    allowed, msg = safety.check_prompt(research_objective or "")
    if not allowed:
        return f"Error: {msg}", ""
    if safety.defensive_scope_confirmation_required(research_objective or "") and not defensive_confirmed:
        return f"Error: {safety.get_defensive_scope_warning()} Check the defensive-scope confirmation box.", ""
    if use_override and (not override_rationale or not override_rationale.strip()):
        return "Error: Provide a rationale for manual model override.", ""
    loader = TemplatesLoader()
    router = Router()
    gateway = ModelGateway()
    template_body = loader.get_template(int(agent_num), template_type)
    recommended = router.get_recommended_model(int(agent_num), template_type)
    if use_override:
        router.log_override_rationale(int(agent_num), template_type, recommended, model_choice, override_rationale or "")
    else:
        model_choice = recommended
    user_content = f"""**Context:** {research_objective}
**Assumptions:** {assumptions or 'None'}
**Constraints:** {constraints or 'None'}

**Task:** Execute the {template_type} template for this context. Output in markdown suitable for the given output path."""
    messages = [{"role": "user", "content": template_body + "\n\n---\n\n" + user_content}]
    try:
        result = gateway.call(model_choice, messages, temperature=0.5, max_tokens=4096)
        content = result.get("content", "")
    except Exception as e:
        return f"Error calling model: {e}", ""
    if not content:
        return "Error: No content returned.", ""
    if not validator.ensure_output_dir(output_path):
        return "Error: Output path invalid or outside repo.", ""
    session_id = str(uuid.uuid4())[:8]
    date = datetime.utcnow().strftime("%Y-%m-%d")
    prompt_summary = (research_objective or "")[:200]
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
        agent_num=int(agent_num),
        model_used=model_choice,
        template_type=template_type,
        prompt_summary=prompt_summary,
        output_path=output_path,
        prompt_payload={"agent": agent_num, "template_type": template_type, "model": model_choice, "research_objective": research_objective, "output_path": output_path},
        model_output_text=content,
        artifact_name=out_full.stem,
    )
    queue = _load_queue()
    queue.append({
        "path": output_path,
        "agent": int(agent_num),
        "model": model_choice,
        "date": date,
        "preview": content[:500],
    })
    _save_queue(queue)
    return f"Done. Output written to {output_path}. Session logged. Draft added to Review Queue.", content[:2000] + ("..." if len(content) > 2000 else "")


def get_review_queue_display():
    queue = _load_queue()
    if not queue:
        return "No items in review queue."
    lines = []
    for i, item in enumerate(queue[:20]):
        path = item.get("path", "")
        agent = item.get("agent", 0)
        model = item.get("model", "")
        date = item.get("date", "")
        label = AGENT_NAMES.get(agent, f"Agent {agent}")
        lines.append(f"**{path}** — {label} · {model} · {date}")
    return "\n".join(lines)


def review_approve(path):
    queue = _load_queue()
    queue = [q for q in queue if q.get("path") != path]
    _save_queue(queue)
    full_path = get_path(path)
    if full_path.exists():
        text = full_path.read_text(encoding="utf-8", errors="replace")
        meta, body = parse_frontmatter(text)
        meta["PI_Review_Status"] = "Approved"
        extra = {k: v for k, v in meta.items() if k not in ("Session_Date", "Model_Used", "Prompt_Summary", "Output_Path", "PI_Review_Status", "AI_Assisted")}
        new_text = inject_frontmatter(
            body,
            session_date=meta.get("Session_Date", ""),
            model_used=meta.get("Model_Used", ""),
            prompt_summary=meta.get("Prompt_Summary", ""),
            output_path=path,
            pi_review_status="Approved",
            extra=extra if extra else None,
        )
        full_path.write_text(new_text, encoding="utf-8")
        append_decision_log(datetime.utcnow().strftime("%Y-%m-%d"), "PI_Approval", f"\n- **Artifact:** {path}\n- **Action:** Approved\n")
    return get_review_queue_display()


def review_request_changes(path):
    queue = _load_queue()
    queue = [q for q in queue if q.get("path") != path]
    _save_queue(queue)
    append_decision_log(datetime.utcnow().strftime("%Y-%m-%d"), "PI_Request_Changes", f"\n- **Artifact:** {path}\n- **Action:** Request changes\n")
    return get_review_queue_display()


def review_archive(path):
    queue = _load_queue()
    queue = [q for q in queue if q.get("path") != path]
    _save_queue(queue)
    append_decision_log(datetime.utcnow().strftime("%Y-%m-%d"), "PI_Archive", f"\n- **Artifact:** {path}\n- **Action:** Archived (not for committee)\n")
    return get_review_queue_display()


def review_approve_all():
    """Approve all items in queue (batch)."""
    queue = _load_queue()
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
            append_decision_log(datetime.utcnow().strftime("%Y-%m-%d"), "PI_Approval", f"\n- **Artifact:** {path}\n- **Action:** Approved (batch)\n")
        else:
            remaining.append(item)
    _save_queue(remaining)
    return get_review_queue_display()


def list_session_logs(filter_date, filter_agent):
    logs_dir = get_path(SESSION_LOGS_DIR)
    if not logs_dir.exists():
        return []
    files = [f for f in logs_dir.glob("*.md") if f.name != "README.md"]
    out = []
    for f in sorted(files, key=lambda p: p.stat().st_mtime, reverse=True):
        n = f.name
        date_part = n[:10] if len(n) >= 10 else ""
        agent_part = ""
        for i in range(1, 12):
            if f"Agent{i:02d}" in n or f"Agent{i}" in n:
                agent_part = str(i)
                break
        if filter_date and filter_date.strip() and filter_date not in date_part:
            continue
        if filter_agent and filter_agent.strip() and filter_agent not in agent_part:
            continue
        out.append(n)
    return out


def get_log_content(filename):
    if not filename:
        return ""
    logs_dir = get_path(SESSION_LOGS_DIR)
    fp = logs_dir / filename
    if not fp.exists():
        return ""
    return fp.read_text(encoding="utf-8", errors="replace")


def build_ui():
    import gradio as gr

    root = get_root()
    loader = TemplatesLoader()
    router = Router()
    agent_options = loader.available_agents()
    agent_labels = [f"{AGENT_NAMES.get(a, a)}" for a in agent_options]
    input_files = list_input_files() or ["(none)"]

    with gr.Blocks(title="AegisLab — Workflow Manager", theme=gr.themes.Soft()) as app:
        gr.Markdown("# AegisLab — Workflow Manager")
        gr.Markdown("Manage workflow: **10_Input** → Run Agent → Review Queue. Same backend as Streamlit (aegislab_ui).")

        with gr.Tabs():
            # --- Workflow ---
            with gr.Tab("Workflow"):
                gr.Markdown("## 10_Input (trigger) — Load context, then Run Agent")
                with gr.Row():
                    input_dropdown = gr.Dropdown(
                        choices=input_files,
                        value=input_files[0] if input_files else "(none)",
                        label="Load context from 10_Input",
                    )
                    load_btn = gr.Button("Load into context")
                context_box = gr.Textbox(
                    label="Research objective / context",
                    placeholder="Describe the task and what the agent should produce. Or load from 10_Input above.",
                    lines=6,
                )
                load_btn.click(
                    fn=lambda x: load_input_into_context(x),
                    inputs=[input_dropdown],
                    outputs=[context_box],
                )

                gr.Markdown("## Run Agent")
                with gr.Row():
                    agent_dropdown = gr.Dropdown(choices=list(zip(agent_labels, agent_options)), value=agent_options[0] if agent_options else 1, label="Agent")
                    template_dropdown = gr.Dropdown(choices=TEMPLATE_TYPES, value=TEMPLATE_TYPES[0], label="Template type")
                with gr.Row():
                    model_radio = gr.Radio(choices=["Auto-route (recommended)", "Manual override"], value="Auto-route (recommended)", label="Model")
                    model_override = gr.Dropdown(choices=list(MODEL_IDS.keys()), label="Override model (if manual)")
                    override_rationale = gr.Textbox(placeholder="Rationale for override (logged)", label="Override rationale", lines=2)
                output_path = gr.Textbox(placeholder="e.g. 02_Agents/02_Applied_Research_Methodologist/Outputs/artifact.md or 11_Results/artifact.md", label="Output path (relative to repo)")
                with gr.Row():
                    assumptions = gr.Textbox(placeholder="Assumptions (optional)", label="Assumptions")
                    constraints = gr.Textbox(placeholder="Constraints (optional)", label="Constraints")
                defensive_scope_cb = gr.Checkbox(
                    label="I confirm this is defensive/authorized scope only (required when topic may involve offensive security)",
                    value=False,
                )
                run_btn = gr.Button("Run agent")
                run_status = gr.Textbox(label="Status", interactive=False)
                run_preview = gr.Textbox(label="Output preview", interactive=False, lines=10)

                def do_run(agent_val, template_val, model_radio_val, model_override_val, context_val, assumptions_val, constraints_val, output_val, override_ratio_val, defensive_val):
                    use_over = model_radio_val == "Manual override"
                    rec = router.get_recommended_model(int(agent_val), template_val)
                    model_choice = model_override_val if use_over and model_override_val else rec
                    return run_agent(
                        agent_val,
                        template_val,
                        model_choice,
                        context_val,
                        assumptions_val or "",
                        constraints_val or "",
                        output_val or "",
                        use_over,
                        override_ratio_val or "",
                        defensive_confirmed=defensive_val,
                    )

                run_btn.click(
                    fn=do_run,
                    inputs=[agent_dropdown, template_dropdown, model_radio, model_override, context_box, assumptions, constraints, output_path, override_rationale, defensive_scope_cb],
                    outputs=[run_status, run_preview],
                )

            # --- Review Queue ---
            with gr.Tab("Review Queue"):
                gr.Markdown("Drafts awaiting PI action. Use Approve / Request changes / Archive (logged to Decision_Log).")
                queue_display = gr.Markdown(get_review_queue_display())
                path_for_action = gr.Textbox(placeholder="Paste exact output path from queue to act on", label="Artifact path")
                with gr.Row():
                    btn_approve = gr.Button("Approve")
                    btn_request = gr.Button("Request changes")
                    btn_archive = gr.Button("Archive")
                    btn_approve_all = gr.Button("✓ Approve all")
                btn_approve.click(fn=review_approve, inputs=[path_for_action], outputs=[queue_display])
                btn_request.click(fn=review_request_changes, inputs=[path_for_action], outputs=[queue_display])
                btn_archive.click(fn=review_archive, inputs=[path_for_action], outputs=[queue_display])
                btn_approve_all.click(fn=review_approve_all, inputs=[], outputs=[queue_display])
                gr.Markdown("After an action, paste the next path and click again. **Approve all** approves all items in queue. Refresh the tab to see updated list.")

            # --- Session Logs ---
            with gr.Tab("Session Logs"):
                gr.Markdown("Filter and view session logs (governance audit).")
                with gr.Row():
                    log_filter_date = gr.Textbox(placeholder="YYYY-MM-DD", label="Filter by date")
                    log_filter_agent = gr.Textbox(placeholder="e.g. 02", label="Filter by agent")
                log_choices = list_session_logs("", "")
                first_log = log_choices[0] if log_choices else None
                log_dropdown = gr.Dropdown(choices=log_choices, value=first_log, label="Select log")
                log_content = gr.Textbox(label="Log content", lines=15, interactive=False, value=get_log_content(first_log) if first_log else "")
                def update_log_choices(d, a):
                    choices = list_session_logs(d or "", a or "")
                    return gr.update(choices=choices, value=choices[0] if choices else None)
                log_filter_date.change(fn=update_log_choices, inputs=[log_filter_date, log_filter_agent], outputs=[log_dropdown])
                log_filter_agent.change(fn=update_log_choices, inputs=[log_filter_date, log_filter_agent], outputs=[log_dropdown])
                log_dropdown.change(fn=get_log_content, inputs=[log_dropdown], outputs=[log_content])

            # --- Settings ---
            with gr.Tab("Settings"):
                gr.Markdown("**AEGISLAB_ROOT**")
                gr.Code(value=str(root), language=None)
                gr.Markdown("**Default by template:** Daily Driver → Claude Sonnet 4.5; Deep Dive / Review/QA → Claude Opus 4.6. Override rationale is logged to Decision_Log.")

        return app


if __name__ == "__main__":
    demo = build_ui()
    demo.launch(server_name="127.0.0.1", server_port=7860)
