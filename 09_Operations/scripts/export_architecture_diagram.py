#!/usr/bin/env python3
"""
Export AegisLab architecture diagrams from Mermaid to PNG and SVG.

Uses Kroki.io API (free, no auth) to render Mermaid diagrams.
Run from repo root: python 09_Operations/scripts/export_architecture_diagram.py

Output: 04_Praxis_Artifact/Architecture/diagrams/
"""

import re
import urllib.request
import urllib.error
from pathlib import Path


KROKI_URL = "https://kroki.io"
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
ARCH_DOC = REPO_ROOT / "04_Praxis_Artifact" / "Architecture" / "AegisLab_Architecture_For_Visio_Lucidchart.md"
OUTPUT_DIR = REPO_ROOT / "04_Praxis_Artifact" / "Architecture" / "diagrams"


DIAGRAM_NAMES = ["architecture_full", "architecture_simple", "data_flow"]


def extract_mermaid_blocks(md_path: Path) -> list[tuple[str, str]]:
    """Extract Mermaid code blocks from markdown. Returns [(name, code), ...]."""
    text = md_path.read_text(encoding="utf-8")
    blocks = []
    pattern = r"```(?:mermaid)?\s*\n(.*?)```"
    for i, match in enumerate(re.finditer(pattern, text, re.DOTALL)):
        code = match.group(1).strip()
        if not code or not code.startswith(("flowchart", "graph", "sequenceDiagram", "classDiagram")):
            continue
        name = DIAGRAM_NAMES[i] if i < len(DIAGRAM_NAMES) else f"diagram_{i}"
        blocks.append((name, code))
    return blocks


def render_via_kroki(mermaid_code: str, fmt: str) -> bytes:
    """Render Mermaid via Kroki API. fmt: 'png' or 'svg'."""
    url = f"{KROKI_URL}/mermaid/{fmt}"
    req = urllib.request.Request(url, data=mermaid_code.encode("utf-8"), method="POST")
    req.add_header("Content-Type", "text/plain")
    req.add_header(
        "User-Agent",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def main() -> None:
    if not ARCH_DOC.exists():
        print(f"Architecture doc not found: {ARCH_DOC}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    blocks = extract_mermaid_blocks(ARCH_DOC)

    if not blocks:
        print("No Mermaid blocks found in architecture doc.")
        return

    for name, code in blocks:
        for fmt in ("png", "svg"):
            out_path = OUTPUT_DIR / f"AegisLab_{name}.{fmt}"
            try:
                data = render_via_kroki(code, fmt)
                out_path.write_bytes(data)
                print(f"  Wrote {out_path}")
            except urllib.error.URLError as e:
                print(f"  Failed {out_path}: {e}")

    print(f"\nDiagrams saved to: {OUTPUT_DIR}")
    print("Use PNG/SVG in Visio (Insert > Pictures) or Lucidchart (Import).")


if __name__ == "__main__":
    main()
