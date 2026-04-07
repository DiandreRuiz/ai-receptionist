#!/usr/bin/env python3
"""Render docs/executive-demo-brief.md to docs/executive-demo-brief.pdf (PyMuPDF Story).

Run from repo root after editing the markdown:

    uv run python scripts/render_executive_pdf.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

import fitz
import markdown

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MD = REPO_ROOT / "docs" / "executive-demo-brief.md"
DEFAULT_PDF = REPO_ROOT / "docs" / "executive-demo-brief.pdf"

USER_CSS = """
body {
    font-family: sans-serif;
    font-size: 11pt;
    line-height: 1.45;
    color: #222222;
}
h1 {
    font-size: 20pt;
    font-weight: bold;
    margin: 0 0 14pt 0;
    line-height: 1.2;
}
h2 {
    font-size: 13pt;
    font-weight: bold;
    margin: 20pt 0 8pt 0;
    padding-bottom: 3pt;
    border-bottom: 1px solid #cccccc;
}
hr {
    border: none;
    border-top: 1px solid #cccccc;
    margin: 16pt 0;
}
p { margin: 0 0 9pt 0; }
ol, ul { margin: 0 0 10pt 20pt; padding-left: 4pt; }
li { margin: 0 0 5pt 0; }
code {
    font-family: ui-monospace, monospace;
    font-size: 10pt;
    background-color: #f4f4f4;
    padding: 1px 4px;
}
strong { font-weight: bold; }
em { font-style: italic; }
"""


def _md_to_html_fragment(md_text: str) -> str:
    return markdown.markdown(
        md_text,
        extensions=["extra", "sane_lists", "nl2br"],
    )


def render_pdf(md_path: Path, pdf_path: Path) -> None:
    md_text = md_path.read_text(encoding="utf-8")
    fragment = _md_to_html_fragment(md_text)
    html = f"<html><body>{fragment}</body></html>"

    mediabox = fitz.paper_rect("letter")
    where = fitz.Rect(
        mediabox.x0 + 72,
        mediabox.y0 + 72,
        mediabox.x1 - 72,
        mediabox.y1 - 72,
    )

    story = fitz.Story(html=html, user_css=USER_CSS, em=11)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    writer = fitz.DocumentWriter(pdf_path)
    dev = writer.begin_page(mediabox)
    more = 1
    while more:
        more, _filled = story.place(where)
        story.draw(dev)
        if more:
            writer.end_page()
            dev = writer.begin_page(mediabox)
    writer.end_page()
    writer.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--md",
        type=Path,
        default=DEFAULT_MD,
        help="Source markdown path",
    )
    parser.add_argument(
        "--pdf",
        type=Path,
        default=DEFAULT_PDF,
        help="Output PDF path",
    )
    args = parser.parse_args()
    render_pdf(args.md, args.pdf)
    print(f"Wrote {args.pdf}")


if __name__ == "__main__":
    main()
