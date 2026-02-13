"""
Tests for aegislab_ui.repo_validator.
"""

import pytest
from pathlib import Path

# Add parent so aegislab_ui is importable
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aegislab_ui.repo_validator import RepoValidator, REQUIRED_DIRS, REQUIRED_FILES


def test_is_under_root():
    v = RepoValidator()
    assert v.is_under_root("02_Agents") is True
    assert v.is_under_root("09_Operations/Session_Logs") is True
    assert v.is_under_root("../other") is False
    assert v.is_under_root("02_Agents/../../etc") is False


def test_allowed_output_path():
    v = RepoValidator()
    assert v.allowed_output_path("02_Agents/01_PI_Orchestrator/Outputs/out.md") is True
    assert v.allowed_output_path("") is False
    assert v.allowed_output_path("02_Agents/../00_Governance/x.md") is False


def test_validate_structure():
    v = RepoValidator()
    ok, missing = v.validate_structure()
    # At least some required dirs/files should exist in real repo
    assert isinstance(ok, bool)
    assert isinstance(missing, list)
    for m in missing:
        assert "Directory:" in m or "File:" in m
