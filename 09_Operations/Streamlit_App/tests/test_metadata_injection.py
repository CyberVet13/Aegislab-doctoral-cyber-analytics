"""
Tests for aegislab_ui.metadata (YAML front-matter injection and parsing).
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aegislab_ui.metadata import inject_frontmatter, parse_frontmatter


def test_inject_frontmatter():
    body = "# Title\n\nContent here."
    out = inject_frontmatter(
        body,
        session_date="2025-02-07",
        model_used="Claude Sonnet 4.5",
        prompt_summary="Test prompt",
        output_path="02_Agents/02_Applied_Research_Methodologist/Outputs/out.md",
        pi_review_status="Draft",
    )
    assert out.startswith("---")
    assert "Session_Date: 2025-02-07" in out
    assert "Model_Used: Claude Sonnet 4.5" in out
    assert "PI_Review_Status: Draft" in out
    assert "AI_Assisted: True" in out or "AI_Assisted: true" in out
    assert "# Title" in out
    assert "Content here." in out


def test_parse_frontmatter():
    text = """---
Session_Date: 2025-02-07
Model_Used: Claude Sonnet 4.5
PI_Review_Status: Draft
---

# Body
Content.
"""
    meta, body = parse_frontmatter(text)
    assert meta.get("Session_Date") == "2025-02-07"
    assert meta.get("Model_Used") == "Claude Sonnet 4.5"
    assert "# Body" in body
    assert "Content." in body


def test_parse_no_frontmatter():
    text = "# No front matter\nJust content."
    meta, body = parse_frontmatter(text)
    assert meta == {}
    assert body == text
