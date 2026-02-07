"""
AegisLab UI — path, env, and constants.
- AEGISLAB_ROOT from env; fallback to repo-relative resolution.
- No hardcoded absolute Windows paths.
"""

import os
from pathlib import Path

# Resolve AegisLab root: env var > fallback relative to this package
_THIS_DIR = Path(__file__).resolve().parent
_STREAMLIT_APP = _THIS_DIR.parent
_FALLBACK_ROOT = _STREAMLIT_APP.parent.parent  # Streamlit_App -> 09_Operations -> AegisLab

def get_root() -> Path:
    """Return AegisLab repository root. Prefer AEGISLAB_ROOT env."""
    root = os.environ.get("AEGISLAB_ROOT")
    if root:
        return Path(root).resolve()
    return _FALLBACK_ROOT

def get_path(*parts: str) -> Path:
    """Return path under AegisLab root. Parts are relative segments."""
    return get_root().joinpath(*parts)

def load_env() -> None:
    """Load .env from AegisLab root if present (python-dotenv)."""
    try:
        from dotenv import load_dotenv
        env_file = get_root() / ".env"
        if env_file.exists():
            load_dotenv(env_file)
    except ImportError:
        pass

# Constants
AGENTS_DIR = "02_Agents"
GOVERNANCE_DIR = "00_Governance"
SESSION_LOGS_DIR = "09_Operations/Session_Logs"
DECISION_LOGS_DIR = "09_Operations/Decision_Logs"
AUTHORSHIP_LOG_PATH = "00_Governance/Authorship_Log.md"
CHANGE_LOG_PATH = "00_Governance/Change_Log.md"

TEMPLATE_TYPES = ["Daily Driver", "Deep Dive", "Review/QA"]
MODEL_IDS = {
    "GPT-5.2": "gpt-4o",  # map to available model id
    "Claude Opus 4.6": "claude-sonnet-4-20250514",
    "Claude Sonnet 4.5": "claude-3-5-sonnet-20241022",
}

AGENT_NAMES = {
    1: "01 PI/Orchestrator",
    2: "02 Applied Research Methodologist",
    3: "03 Engineering Praxis Architect",
    4: "04 Cyber Threat & Adversary Analysis",
    5: "05 Cybersecurity Architecture & Zero Trust",
    6: "06 Applied Cryptography & Data Protection",
    7: "07 Security Data Analytics",
    8: "08 Visualization & Decision Support",
    9: "09 Doctoral Writing & Argumentation",
    10: "10 Committee & Defense Simulation",
    11: "11 Ethics, Governance & Risk",
}
