"""
AegisLab UI — load prompt templates from 02_Agents/*/Prompt_Templates.md.
- Parse sections: Daily Driver, Deep Dive, Review/QA.
"""

from pathlib import Path
from typing import Dict, List, Optional

from .config import get_path, AGENTS_DIR, AGENT_NAMES, TEMPLATE_TYPES

SECTION_MARKERS = {
    "Daily Driver": ("1. Daily Driver", "2. Deep Dive"),
    "Deep Dive": ("2. Deep Dive", "3. Review"),
    "Review/QA": ("3. Review", "## "),
}


class TemplatesLoader:
    """Load and parse Prompt_Templates.md per agent."""

    def __init__(self) -> None:
        self._cache: Dict[str, Dict[str, str]] = {}

    def _agent_dir(self, agent_num: int) -> Path:
        """Return 02_Agents/XX_Name for agent 1-11."""
        name = AGENT_NAMES.get(agent_num, "")
        if not name:
            return get_path(AGENTS_DIR, "01_PI_Orchestrator")
        # 01 PI/Orchestrator -> 01_PI_Orchestrator (folder uses underscore)
        folder = name.replace(" ", "_").replace("/", "_")
        return get_path(AGENTS_DIR, folder)

    def available_agents(self) -> List[int]:
        """Return list of agent numbers that have Prompt_Templates.md."""
        out: List[int] = []
        for i in range(1, 12):
            p = self._agent_dir(i) / "Prompt_Templates.md"
            if p.exists():
                out.append(i)
        return sorted(out) if out else list(range(1, 12))

    def get_template_path(self, agent_num: int) -> Path:
        """Return path to Prompt_Templates.md for agent."""
        return self._agent_dir(agent_num) / "Prompt_Templates.md"

    def _extract_section(self, text: str, start_marker: str, end_marker: str) -> str:
        """Extract content between start_marker and end_marker (exclusive)."""
        idx = text.find(start_marker)
        if idx == -1:
            return ""
        start = idx + len(start_marker)
        end_idx = text.find(end_marker, start)
        if end_idx == -1:
            return text[start:].strip()
        return text[start:end_idx].strip()

    def get_template(self, agent_num: int, template_type: str) -> str:
        """
        Return template body for agent and type (Daily Driver, Deep Dive, Review/QA).
        Uses cached content per file path.
        """
        path = self.get_template_path(agent_num)
        cache_key = str(path)
        if cache_key not in self._cache:
            if not path.exists():
                return f"*Prompt_Templates.md not found: {path}*"
            self._cache[cache_key] = self._parse_sections(path.read_text(encoding="utf-8", errors="replace"))
        sections = self._cache[cache_key]
        return sections.get(template_type, "")

    def _parse_sections(self, text: str) -> Dict[str, str]:
        """Parse Daily Driver, Deep Dive, Review/QA sections from full markdown."""
        sections: Dict[str, str] = {}
        for label, (start, end) in SECTION_MARKERS.items():
            sections[label] = self._extract_section(text, start, end)
        return sections

    def get_full_content(self, agent_num: int) -> str:
        """Return full Prompt_Templates.md content for preview."""
        path = self.get_template_path(agent_num)
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
