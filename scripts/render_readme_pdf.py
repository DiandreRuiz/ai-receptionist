#!/usr/bin/env python3
"""Render README.md to README.pdf (markdown-pdf: markdown-it-py → HTML → PyMuPDF).

uv run python scripts/render_readme_pdf.py
"""

from __future__ import annotations

import argparse
from pathlib import Path

from markdown_pdf import MarkdownPdf, Section

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MD = REPO_ROOT / "README.md"
DEFAULT_PDF = REPO_ROOT / "README.pdf"
DEFAULT_CSS = Path(__file__).resolve().parent / "readme-pdf.css"

_BORDERS = (63, 63, -63, -63)


def render_pdf(md_path: Path, pdf_path: Path, css_path: Path) -> None:
    md_text = md_path.read_text(encoding="utf-8")
    user_css = css_path.read_text(encoding="utf-8")

    pdf = MarkdownPdf(toc_level=2)
    section = Section(
        md_text,
        toc=True,
        root=str(REPO_ROOT),
        paper_size="letter",
        borders=_BORDERS,
    )
    pdf.add_section(section, user_css=user_css)
    pdf.meta["title"] = "SK Quality Roofing — AI phone receptionist (demo)"

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.save(pdf_path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--md", type=Path, default=DEFAULT_MD, help="Source markdown")
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF, help="Output PDF")
    parser.add_argument("--css", type=Path, default=DEFAULT_CSS, help="Stylesheet")
    args = parser.parse_args()
    render_pdf(args.md, args.pdf, args.css)
    print(f"Wrote {args.pdf}")


if __name__ == "__main__":
    main()
