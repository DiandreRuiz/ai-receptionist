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

# Tuned for Letter + Story: spacing and hierarchy read better than default browser-ish CSS.
USER_CSS = """
html {
    margin: 0;
    padding: 0;
}
body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #1a1a1a;
    margin: 0;
    padding: 0;
}
h1 {
    font-size: 17pt;
    font-weight: bold;
    line-height: 1.25;
    margin: 0 0 4pt 0;
    padding: 0;
    color: #0d2137;
    letter-spacing: -0.02em;
}
h2 {
    font-size: 11.5pt;
    font-weight: bold;
    line-height: 1.3;
    margin: 18pt 0 8pt 0;
    padding: 0 0 4pt 0;
    color: #0d2137;
    border-bottom: 0.75pt solid #c5d0dc;
}
h2:first-of-type {
    margin-top: 14pt;
}
p {
    margin: 0 0 9pt 0;
    text-align: left;
}
ul, ol {
    margin: 4pt 0 12pt 0;
    padding-left: 18pt;
}
li {
    margin: 0 0 7pt 0;
    padding-left: 2pt;
}
li:last-child {
    margin-bottom: 0;
}
blockquote {
    margin: 10pt 0 14pt 0;
    padding: 11pt 14pt 11pt 16pt;
    background-color: #eef2f7;
    border-left: 3pt solid #1e4d7a;
}
blockquote p {
    margin: 0 0 6pt 0;
    font-size: 10.5pt;
}
blockquote p:last-child {
    margin-bottom: 0;
}
code {
    font-family: Courier, monospace;
    font-size: 9.5pt;
    background-color: #e8ecf1;
    padding: 1pt 4pt;
}
strong {
    font-weight: bold;
    color: #111111;
}
em {
    font-style: italic;
}
"""


def _md_to_html_fragment(md_text: str) -> str:
    # Omit nl2br: it turns single newlines into <br>, which often fragments PDF lines awkwardly.
    return markdown.markdown(
        md_text,
        extensions=["extra", "sane_lists"],
    )


def render_pdf(md_path: Path, pdf_path: Path) -> None:
    md_text = md_path.read_text(encoding="utf-8")
    fragment = _md_to_html_fragment(md_text)
    html = (
        "<!DOCTYPE html><html><head>"
        '<meta charset="utf-8">'
        "</head><body>"
        f"{fragment}"
        "</body></html>"
    )

    mediabox = fitz.paper_rect("letter")
    where = fitz.Rect(
        mediabox.x0 + 63,
        mediabox.y0 + 63,
        mediabox.x1 - 63,
        mediabox.y1 - 63,
    )

    story = fitz.Story(html=html, user_css=USER_CSS, em=10.5)
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
