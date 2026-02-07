"""
AegisLab UI — model routing rules and rationale logging.
- Default routing by template type and agent.
- Manual override with mandatory rationale → Decision_Log.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

from .config import (
    get_path,
    AGENT_NAMES,
    TEMPLATE_TYPES,
    MODEL_IDS,
    DECISION_LOGS_DIR,
)
from .logging_audit import append_decision_log

# Default: template_type -> model display name
DEFAULT_BY_TEMPLATE = {
    "Daily Driver": "Claude Sonnet 4.5",
    "Deep Dive": "Claude Opus 4.6",
    "Review/QA": "Claude Opus 4.6",
}

# Per-agent overrides (display name). Empty = use template default.
AGENT_DEFAULT_MODEL: dict[int, Optional[str]] = {
    1: None,
    2: None,
    3: None,
    4: None,
    5: None,
    6: None,
    7: None,
    8: None,
    9: None,
    10: None,
    11: None,
}


class Router:
    """Resolve model for (agent, template_type) and log overrides."""

    @staticmethod
    def get_recommended_model(agent_num: int, template_type: str) -> str:
        """Return recommended model display name."""
        agent_override = AGENT_DEFAULT_MODEL.get(agent_num)
        if agent_override:
            return agent_override
        return DEFAULT_BY_TEMPLATE.get(template_type, "Claude Sonnet 4.5")

    @staticmethod
    def resolve_model_id(display_name: str) -> str:
        """Map display name to API model id."""
        return MODEL_IDS.get(display_name, list(MODEL_IDS.values())[0])

    @staticmethod
    def log_override_rationale(
        agent_num: int,
        template_type: str,
        recommended: str,
        chosen: str,
        rationale: str,
    ) -> None:
        """Append decision log entry for manual model override."""
        date = datetime.utcnow().strftime("%Y-%m-%d")
        agent_name = AGENT_NAMES.get(agent_num, f"Agent_{agent_num}")
        content = f"""## {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")} UTC — Model override

- **Agent:** {agent_name}
- **Template:** {template_type}
- **Recommended model:** {recommended}
- **Chosen model:** {chosen}
- **Rationale:** {rationale}

"""
        append_decision_log(date, "Decision_Routing", content)
