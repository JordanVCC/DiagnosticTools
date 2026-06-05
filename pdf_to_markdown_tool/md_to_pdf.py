#!/usr/bin/env python3
"""
md_to_pdf.py
------------
Converts a Markdown file to PDF using the Markdown + PyMuPDF Story pipeline.
Requires only packages already installed with pymupdf4llm (no GTK/Pango needed).

Usage:
    python md_to_pdf.py <input.md> [output.pdf]
"""

import sys
import argparse
from pathlib import Path

import markdown
import fitz  # PyMuPDF


# ---------------------------------------------------------------------------
# CSS – clean stylesheet that PyMuPDF's Story renderer understands
# ---------------------------------------------------------------------------
_STORY_CSS = """
body {
    font-family: sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #111;
    font-variant-ligatures: none;
}
h1 { font-size: 20pt; margin-top: 18pt; margin-bottom: 8pt; color: #1a1a2e; }
h2 { font-size: 14pt; margin-top: 14pt; margin-bottom: 4pt; color: #16213e; }
h3 { font-size: 12pt; margin-top: 10pt; margin-bottom: 3pt; color: #0f3460; }
h4 { font-size: 11pt; margin-top: 8pt;  margin-bottom: 2pt; }

p  { margin: 4pt 0 6pt 0; }

blockquote {
    margin: 6pt 0 6pt 16pt;
    padding: 4pt 8pt;
    border-left: 3pt solid #0066cc;
    color: #333;
    font-style: italic;
}

code {
    font-family: monospace;
    font-size: 9pt;
    background-color: #f0f0f0;
}

pre {
    font-family: monospace;
    font-size: 8pt;
    background-color: #f4f4f4;
    padding: 6pt;
    margin: 6pt 0;
    white-space: pre-wrap;
    word-break: break-all;
    page-break-inside: avoid;
}

table {
    border-collapse: collapse;
    margin: 8pt 0;
    font-size: 9.5pt;
}
th {
    background-color: #1a1a2e;
    color: #ffffff;
    font-weight: bold;
    padding: 4pt 6pt;
    border: 0.5pt solid #555;
    text-align: left;
}
td {
    padding: 3pt 6pt;
    border: 0.5pt solid #aaa;
    vertical-align: top;
}

ul, ol { margin: 4pt 0 6pt 18pt; padding: 0; }
li { margin: 2pt 0; }

hr { border-top: 1pt solid #aaa; margin: 10pt 0; }

strong { font-weight: bold; }
em     { font-style: italic; }
"""

# Markdown extensions for maximum fidelity
_MD_EXTENSIONS = [
    "extra",       # tables, fenced_code, footnotes, attr_list, def_list, abbr
    "toc",         # table of contents anchors
    "sane_lists",  # better list handling
    "nl2br",       # newlines become <br>
    "meta",        # front-matter metadata
]

_MD_EXT_CONFIGS: dict = {
    "toc": {"permalink": False},
}


def convert_markdown_to_pdf(
    input_path: str | Path,
    output_path: str | Path | None = None,
) -> Path:
    """
    Convert a Markdown file to PDF using PyMuPDF's Story renderer.

    Parameters
    ----------
    input_path:
        Path to the source Markdown (.md) file.
    output_path:
        Destination PDF path.  Defaults to the same stem with .pdf extension.

    Returns
    -------
    Path
        Resolved path to the written PDF file.
    """
    input_path = Path(input_path).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {input_path}")

    if output_path is None:
        output_path = input_path.with_suffix(".pdf")
    output_path = Path(output_path).resolve()

    print(f"Converting: {input_path}")
    print(f"     → PDF: {output_path}")

    md_text = input_path.read_text(encoding="utf-8")

    # Convert Markdown → HTML
    md_obj = markdown.Markdown(
        extensions=_MD_EXTENSIONS,
        extension_configs=_MD_EXT_CONFIGS,
    )
    body_html = md_obj.convert(md_text)

    full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body>{body_html}</body></html>"""

    # Render HTML → PDF via PyMuPDF Story
    # A4 page with 2 cm margins
    A4 = fitz.paper_rect("a4")
    MARGIN = 36  # ~1.3 cm in points — narrower for wider text area
    clip = A4 + (MARGIN, MARGIN, -MARGIN, -MARGIN)

    story = fitz.Story(html=full_html, user_css=_STORY_CSS)
    writer = fitz.DocumentWriter(str(output_path))

    more = True
    while more:
        device = writer.begin_page(A4)
        more, _ = story.place(clip)
        story.draw(device)
        writer.end_page()

    writer.close()

    size_kb = output_path.stat().st_size // 1024
    print(f"   Done.  PDF size: {size_kb:,} KB")
    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="md_to_pdf",
        description="Convert a Markdown file to PDF (preserving tables, code blocks, etc.)",
    )
    parser.add_argument("input", metavar="INPUT.MD", help="Source Markdown file.")
    parser.add_argument(
        "output",
        metavar="OUTPUT.PDF",
        nargs="?",
        default=None,
        help="Destination PDF (default: same name, .pdf extension).",
    )
    args = parser.parse_args(argv)

    try:
        convert_markdown_to_pdf(args.input, args.output)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
