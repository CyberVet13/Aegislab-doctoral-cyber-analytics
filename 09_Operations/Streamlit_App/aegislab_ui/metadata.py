"""
AegisLab UI — YAML front-matter injection and parsing.
- Every AI-assisted artifact gets metadata block per AI_Use_Disclosure.
"""

import re
from typing import Any, Dict, Optional

DEFAULT_FIELDS = [
    "AI_Assisted",
    "Session_Date",
    "Model_Used",
    "Prompt_Summary",
    "PI_Review_Status",
    "Output_Path",
]


def inject_frontmatter(
    body: str,
    *,
    session_date: str,
    model_used: str,
    prompt_summary: str,
    output_path: str = "",
    pi_review_status: str = "Draft",
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Prepend YAML front-matter to body. Body must not already start with ---.
    """
    meta: Dict[str, Any] = {
        "AI_Assisted": True,
        "Session_Date": session_date,
        "Model_Used": model_used,
        "Prompt_Summary": prompt_summary[:200] + ("..." if len(prompt_summary) > 200 else ""),
        "PI_Review_Status": pi_review_status,
        "Output_Path": output_path,
    }
    if extra:
        meta.update(extra)
    lines = ["---"]
    for k, v in meta.items():
        if isinstance(v, bool):
            lines.append(f"{k}: {str(v)}")
        elif isinstance(v, str) and (":" in v or "\n" in v):
            lines.append(f'{k}: "{v}"')
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines) + (body.lstrip() if body else "")


def parse_frontmatter(text: str) -> tuple[Dict[str, Any], str]:
    """
    Parse YAML front-matter from start of text. Return (meta dict, body).
    If no ---...---, return ({}, text).
    """
    if not text.strip().startswith("---"):
        return {}, text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)", text, re.DOTALL)
    if not match:
        return {}, text
    yaml_block, body = match.group(1), match.group(2)
    meta: Dict[str, Any] = {}
    for line in yaml_block.split("\n"):
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if v.lower() in ("true", "yes"):
            meta[k] = True
        elif v.lower() in ("false", "no"):
            meta[k] = False
        else:
            meta[k] = v
    return meta, body
