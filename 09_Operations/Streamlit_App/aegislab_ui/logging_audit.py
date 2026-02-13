"""
AegisLab UI — session logs, hashes, authorship log append, decision logs.
- Session log: 09_Operations/Session_Logs/YYYY-MM-DD_AgentXX_SessionID.md
- Decision log: 09_Operations/Decision_Logs/YYYY-MM-DD_Decision_Topic.md
- Append-only Authorship_Log.md entry.
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from .config import (
    get_path,
    SESSION_LOGS_DIR,
    DECISION_LOGS_DIR,
    AUTHORSHIP_LOG_PATH,
    AGENT_NAMES,
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def write_session_log(
    *,
    session_id: str,
    agent_num: int,
    model_used: str,
    template_type: str,
    prompt_summary: str,
    output_path: str,
    prompt_payload_hash: str,
    model_output_hash: str,
    prompt_payload_json: Optional[Dict[str, Any]] = None,
    extra: Optional[Dict[str, str]] = None,
) -> Path:
    """
    Write session log file. Returns path to written file.
    Filename: YYYY-MM-DD_AgentXX_SessionID.md
    """
    date = datetime.utcnow().strftime("%Y-%m-%d")
    agent_name = AGENT_NAMES.get(agent_num, f"Agent_{agent_num}")
    agent_xx = f"Agent{agent_num:02d}"
    fname = f"{date}_{agent_xx}_{session_id}.md"
    log_path = get_path(SESSION_LOGS_DIR, fname)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Session Log",
        "",
        f"- **Date:** {date}",
        f"- **Agent:** {agent_name}",
        f"- **Model:** {model_used}",
        f"- **Template:** {template_type}",
        f"- **Prompt summary:** {prompt_summary[:300]}{'...' if len(prompt_summary) > 300 else ''}",
        f"- **Output path:** {output_path}",
        "",
        "## Reproducibility hashes",
        "",
        f"- **prompt_payload_sha256:** `{prompt_payload_hash}`",
        f"- **model_output_sha256:** `{model_output_hash}`",
        "",
    ]
    if extra:
        lines.append("## Extra")
        for k, v in extra.items():
            lines.append(f"- **{k}:** {v}")
        lines.append("")
    if prompt_payload_json:
        lines.append("## Prompt payload (summary)")
        lines.append("```json")
        lines.append(json.dumps(prompt_payload_json, indent=2)[:2000])
        if len(json.dumps(prompt_payload_json)) > 2000:
            lines.append("... (truncated)")
        lines.append("```")

    log_path.write_text("\n".join(lines), encoding="utf-8")
    return log_path


def append_decision_log(date: str, topic: str, content: str) -> Path:
    """Append to or create 09_Operations/Decision_Logs/YYYY-MM-DD_Decision_Topic.md."""
    fname = f"{date}_Decision_{topic}.md"
    log_path = get_path(DECISION_LOGS_DIR, fname)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if log_path.exists():
        existing = log_path.read_text(encoding="utf-8")
        log_path.write_text(existing + "\n" + content, encoding="utf-8")
    else:
        log_path.write_text(f"# Decision log — {topic}\n\n{content}", encoding="utf-8")
    return log_path


def append_authorship_log(
    artifact_name: str,
    file_path: str,
    creation_date: str,
    ai_contribution: str,
    pi_contribution: str,
    validation_method: str,
    status: str = "Draft",
    approval_date: str = "—",
) -> None:
    """Append one row to 00_Governance/Authorship_Log.md (Active Artifacts Log table)."""
    path = get_path(AUTHORSHIP_LOG_PATH)
    path.parent.mkdir(parents=True, exist_ok=True)
    row = f"| {artifact_name} | {file_path} | {creation_date} | {ai_contribution} | {pi_contribution} | {validation_method} | {status} | {approval_date} |"
    if not path.exists():
        path.write_text(
            "# Authorship Log - AegisLab\n\n## Active Artifacts Log\n\n| Artifact Name | File Path | Creation Date | AI Contribution | PI Contribution | Validation Method | Status | Approval Date |\n"
            "|---------------|-----------|---------------|------------------|-----------------|-------------------|--------|---------------|\n"
            + row + "\n",
            encoding="utf-8",
        )
        return
    text = path.read_text(encoding="utf-8")
    if "| Artifact Name |" not in text:
        text += "\n## Active Artifacts Log\n\n| Artifact Name | File Path | Creation Date | AI Contribution | PI Contribution | Validation Method | Status | Approval Date |\n|---------------|-----------|---------------|------------------|-----------------|-------------------|--------|---------------|\n"
    text += "\n" + row
    path.write_text(text, encoding="utf-8")


class LoggingAudit:
    """Convenience wrapper for session log + hashes + authorship."""

    @staticmethod
    def run(
        session_id: str,
        agent_num: int,
        model_used: str,
        template_type: str,
        prompt_summary: str,
        output_path: str,
        prompt_payload: Dict[str, Any],
        model_output_text: str,
        artifact_name: Optional[str] = None,
    ) -> Path:
        """Write session log with hashes; append authorship log row. Returns session log path."""
        payload_hash = sha256_text(json.dumps(prompt_payload, sort_keys=True))
        output_hash = sha256_text(model_output_text)
        log_path = write_session_log(
            session_id=session_id,
            agent_num=agent_num,
            model_used=model_used,
            template_type=template_type,
            prompt_summary=prompt_summary,
            output_path=output_path,
            prompt_payload_hash=payload_hash,
            model_output_hash=output_hash,
            prompt_payload_json=prompt_payload,
        )
        date = datetime.utcnow().strftime("%Y-%m-%d")
        name = artifact_name or Path(output_path).stem
        append_authorship_log(
            artifact_name=name,
            file_path=output_path,
            creation_date=date,
            ai_contribution="AI-generated draft; see session log",
            pi_contribution="Pending PI review",
            validation_method="PI review required",
            status="Draft",
        )
        return log_path
