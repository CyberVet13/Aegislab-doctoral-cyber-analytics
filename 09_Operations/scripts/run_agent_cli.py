"""
AegisLab — CLI to run one agent (for n8n Execute Command or manual use).
- Reads context from a file (e.g. 10_Input/brief.md) or from stdin.
- Writes output to repo path, session log, and appends to review queue (Gradio_App/review_queue.json).
Usage:
  python run_agent_cli.py --input 10_Input/brief.md --agent 2 --template-type "Daily Driver" --output 11_Results/artifact.md
  python run_agent_cli.py --input 10_Input/brief.md --agent 2 --output 02_Agents/02_Applied_Research_Methodologist/Outputs/out.md
"""

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# Add Streamlit_App so we can import aegislab_ui
_SCRIPT_DIR = Path(__file__).resolve().parent
_OPERATIONS = _SCRIPT_DIR.parent
_STREAMLIT_APP = _OPERATIONS / "Streamlit_App"
if str(_STREAMLIT_APP) not in sys.path:
    sys.path.insert(0, str(_STREAMLIT_APP))

from aegislab_ui.config import load_env, get_path, get_root, INPUT_DIR
from aegislab_ui.repo_validator import RepoValidator
from aegislab_ui.templates_loader import TemplatesLoader
from aegislab_ui.router import Router
from aegislab_ui.model_gateway import ModelGateway
from aegislab_ui.logging_audit import LoggingAudit
from aegislab_ui.metadata import inject_frontmatter
from aegislab_ui.safety import SafetyGuard

load_env()


def _read_input(path: str) -> str:
    """Read content from repo-relative path or absolute path."""
    if not path or path == "-":
        return sys.stdin.read()
    p = get_path(path) if not Path(path).is_absolute() else Path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="replace")


def _append_review_queue(output_path: str, agent_num: int, model_choice: str, date: str, content: str) -> None:
    """Append draft to Gradio review queue file so UI shows it."""
    queue_file = _OPERATIONS / "Gradio_App" / "review_queue.json"
    queue = []
    if queue_file.exists():
        try:
            queue = json.loads(queue_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    queue.append({
        "path": output_path,
        "agent": agent_num,
        "model": model_choice,
        "date": date,
        "preview": content[:500],
    })
    queue_file.parent.mkdir(parents=True, exist_ok=True)
    queue_file.write_text(json.dumps(queue, indent=2), encoding="utf-8")


def run(
    input_path: str,
    agent_num: int,
    template_type: str,
    output_path: str,
    assumptions: str = "",
    constraints: str = "",
    model_override: str = "",
    override_rationale: str = "",
) -> tuple[bool, str]:
    """Run agent; return (success, message)."""
    research_objective = _read_input(input_path if input_path else "-")
    if not research_objective and input_path and input_path != "-":
        return False, f"Could not read input: {input_path}"

    if not output_path or not output_path.strip():
        return False, "Missing --output path"

    validator = RepoValidator()
    if not validator.allowed_output_path(output_path):
        return False, "Output path must be inside repo (no '..')"

    safety = SafetyGuard()
    allowed, msg = safety.check_prompt(research_objective or "")
    if not allowed:
        return False, msg

    use_override = bool(model_override and model_override.strip())
    if use_override and not (override_rationale and override_rationale.strip()):
        return False, "Provide --override-rationale when using --model-override"

    loader = TemplatesLoader()
    router = Router()
    gateway = ModelGateway()
    template_body = loader.get_template(agent_num, template_type)
    recommended = router.get_recommended_model(agent_num, template_type)
    model_choice = model_override if use_override else recommended
    if use_override:
        router.log_override_rationale(agent_num, template_type, recommended, model_choice, override_rationale or "")

    user_content = f"""**Context:** {research_objective}
**Assumptions:** {assumptions or 'None'}
**Constraints:** {constraints or 'None'}

**Task:** Execute the {template_type} template for this context. Output in markdown suitable for the given output path."""
    messages = [{"role": "user", "content": template_body + "\n\n---\n\n" + user_content}]

    try:
        result = gateway.call(model_choice, messages, temperature=0.5, max_tokens=4096)
        content = result.get("content", "")
    except Exception as e:
        return False, f"Model call failed: {e}"

    if not content:
        return False, "No content returned from model"

    if not validator.ensure_output_dir(output_path):
        return False, "Output path invalid or outside repo"

    session_id = str(uuid.uuid4())[:8]
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
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
        agent_num=agent_num,
        model_used=model_choice,
        template_type=template_type,
        prompt_summary=prompt_summary,
        output_path=output_path,
        prompt_payload={
            "agent": agent_num,
            "template_type": template_type,
            "model": model_choice,
            "research_objective": research_objective,
            "output_path": output_path,
        },
        model_output_text=content,
        artifact_name=out_full.stem,
    )
    _append_review_queue(output_path, agent_num, model_choice, date, content)
    return True, f"Output written to {output_path}; session logged; added to Review Queue."


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AegisLab agent (for n8n or CLI)")
    parser.add_argument("--input", "-i", default="", help="Repo-relative path to context file (e.g. 10_Input/brief.md), or '-' for stdin")
    parser.add_argument("--agent", "-a", type=int, required=True, choices=range(1, 12), metavar="1-11", help="Agent number (1-11)")
    parser.add_argument("--template-type", "-t", default="Daily Driver", choices=["Daily Driver", "Deep Dive", "Review/QA"], help="Template type")
    parser.add_argument("--output", "-o", required=True, help="Repo-relative output path (e.g. 11_Results/artifact.md)")
    parser.add_argument("--assumptions", default="", help="Optional assumptions")
    parser.add_argument("--constraints", default="", help="Optional constraints")
    parser.add_argument("--model-override", default="", help="Override model (e.g. Claude Opus 4.6); requires --override-rationale")
    parser.add_argument("--override-rationale", default="", help="Rationale for model override (logged)")
    args = parser.parse_args()

    ok, msg = run(
        input_path=args.input,
        agent_num=args.agent,
        template_type=args.template_type,
        output_path=args.output,
        assumptions=args.assumptions or "",
        constraints=args.constraints or "",
        model_override=args.model_override or "",
        override_rationale=args.override_rationale or "",
    )
    if ok:
        print(msg)
        sys.exit(0)
    else:
        print(f"Error: {msg}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
