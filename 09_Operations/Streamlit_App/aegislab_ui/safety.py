"""
AegisLab UI — safety guardrails.
- No malware, hacking, exploitation instructions.
- Defensive-scope confirmation for offensive security topics.
- Block writes outside AEGISLAB_ROOT (enforced in repo_validator).
"""

import re
from typing import Tuple

BLOCK_PATTERNS = [
    r"\b(malware|ransomware|exploit|payload)\s+(generat|creat|writ|inject)",
    r"\b(unauthorized\s+access|bypass\s+(auth|security))",
    r"\b(hack|penetrat)\s+(into|network)\s+without",
    r"\b(weaponiz|offensive\s+tool)\s+",
    r"\b(crack|pirat)\s+(software|key)\s*",
]

DEFENSIVE_SCOPE_WARNING = (
    "This topic may involve offensive security. You must reframe all content "
    "within defensive, authorized scope only (e.g., threat modeling, detection, "
    "authorized testing with permission). No instructions for unauthorized access."
)


class SafetyGuard:
    """Check prompts and outputs for policy violations."""

    def __init__(self) -> None:
        self._compiled = [re.compile(p, re.I) for p in BLOCK_PATTERNS]

    def check_prompt(self, text: str) -> Tuple[bool, str]:
        """
        Return (allowed, message). If not allowed, message explains.
        """
        if not text or not text.strip():
            return True, ""
        for pat in self._compiled:
            if pat.search(text):
                return False, (
                    "Prompt appears to request content outside defensive scope. "
                    "Reframe for authorized, defensive use only."
                )
        return True, ""

    def defensive_scope_confirmation_required(self, text: str) -> bool:
        """Heuristic: topic might need defensive-scope checkbox."""
        lower = text.lower()
        triggers = [
            "exploit", "offensive", "red team", "penetration test",
            "attack vector", "weaponize", "bypass", "crack",
        ]
        return any(t in lower for t in triggers)

    @staticmethod
    def get_defensive_scope_warning() -> str:
        return DEFENSIVE_SCOPE_WARNING
