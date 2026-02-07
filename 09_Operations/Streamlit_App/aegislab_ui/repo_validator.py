"""
AegisLab UI — repository structure validation.
- Required folders and key files.
- Paths constrained to repo; no writes outside AEGISLAB_ROOT.
"""

from pathlib import Path
from typing import List, Tuple

from .config import get_root, get_path, AGENTS_DIR, GOVERNANCE_DIR, SESSION_LOGS_DIR, DECISION_LOGS_DIR

REQUIRED_DIRS = [
    "00_Governance",
    "01_Program_Context",
    "02_Agents",
    "03_Research_Methods",
    "04_Praxis_Artifact",
    "05_Data",
    "06_Analysis",
    "07_Writing",
    "08_Defense",
    "09_Operations",
    "10_Input",
    "11_Results",
]

REQUIRED_FILES = [
    "00_Governance/Academic_Integrity_Policy.md",
    "00_Governance/AI_Use_Disclosure.md",
    "00_Governance/Authorship_Log.md",
    "09_Operations/Session_Logs/README.md",
    "09_Operations/Decision_Logs/README.md",
]


class RepoValidator:
    """Validate AegisLab repo structure and path safety."""

    def __init__(self) -> None:
        self.root = get_root()

    def is_under_root(self, path: str) -> bool:
        """Return True if path is under AegisLab root (no escape)."""
        try:
            resolved = (self.root / path).resolve()
            return resolved.is_relative_to(self.root) or resolved == self.root
        except (ValueError, OSError):
            return False

    def validate_structure(self) -> Tuple[bool, List[str]]:
        """
        Check required dirs and files exist.
        Returns (all_ok, list of missing items).
        """
        missing: List[str] = []
        for d in REQUIRED_DIRS:
            if not get_path(d).is_dir():
                missing.append(f"Directory: {d}")
        for f in REQUIRED_FILES:
            if not get_path(f).is_file():
                missing.append(f"File: {f}")
        return (len(missing) == 0, missing)

    def allowed_output_path(self, rel_path: str) -> bool:
        """Return True if rel_path is a valid output path under repo (no .., under root)."""
        if not rel_path or ".." in rel_path:
            return False
        return self.is_under_root(rel_path)

    def ensure_output_dir(self, rel_path: str) -> bool:
        """Ensure parent directory exists for rel_path under root. Return True if safe and done."""
        if not self.allowed_output_path(rel_path):
            return False
        try:
            full = get_path(rel_path)
            full.parent.mkdir(parents=True, exist_ok=True)
            return True
        except OSError:
            return False
