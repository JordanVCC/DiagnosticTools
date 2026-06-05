#!/usr/bin/env python3
"""
pdf_to_markdown.py
------------------
Converts a PDF file to Markdown using the marker-pdf engine.

marker uses deep-learning layout detection (surya) to correctly classify
blocks as headings, paragraphs, tables, code, lists etc. — it does NOT
use font-size heuristics, which is why it avoids the 'IF / OR turned into
headings' problem seen with pymupdf4llm.

Usage:
    python pdf_to_markdown.py <input.pdf> [output.md]

If output path is omitted, the result is written to <input_stem>.md
alongside the input file.

ML models are downloaded once on first run (~500 MB, cached in
%USERPROFILE%/.cache/huggingface) and reused on every subsequent call.
"""

import re
import sys
import argparse
from pathlib import Path

# ---------------------------------------------------------------------------
# Page counter — fast, no full parse needed
# ---------------------------------------------------------------------------

def _count_pdf_pages(path) -> int | None:
    """Return page count of *path* without a full PDF parse."""
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(path)).pages)
    except Exception:
        pass
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(str(path))
        n = len(doc)
        doc.close()
        return n
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# tqdm stderr interceptor — feeds page progress back to caller
# ---------------------------------------------------------------------------

def _parse_tqdm_line(line: str, callback) -> None:
    """Parse a tqdm progress line and call callback(current, total, stage)."""
    m = re.search(r'(\d+)/(\d+)\s*\[', line) or re.search(r'\b(\d+)/(\d+)\b', line)
    if not m:
        return
    current, total = int(m.group(1)), int(m.group(2))
    stage_m = re.match(r'^\s*([\w][\w\s]+?)\s*:\s*\d+%', line)
    stage = stage_m.group(1).strip() if stage_m else ""
    callback(current, total, stage)


def _convert_with_progress(converter, input_path_str: str, callback):
    """Run *converter* while intercepting tqdm stderr output for progress."""

    class _StderrCapture:
        def __init__(self, real):
            self._real = real
            self._buf = ""

        def write(self, text):
            if self._real:
                try:
                    self._real.write(text)
                except Exception:
                    pass
            self._buf += text
            # Process complete lines delimited by \r or \n
            while True:
                r = self._buf.find('\r')
                n = self._buf.find('\n')
                if r == -1 and n == -1:
                    break
                idx = min(x for x in (r, n) if x != -1)
                line = self._buf[:idx]
                self._buf = self._buf[idx + 1:]
                if line.strip():
                    _parse_tqdm_line(line, callback)

        def flush(self):
            if self._real:
                try:
                    self._real.flush()
                except Exception:
                    pass

        def isatty(self):
            return False  # makes tqdm emit \n-terminated lines

        def fileno(self):
            raise OSError("no fileno on progress capture")

        @property
        def encoding(self):
            return getattr(self._real, 'encoding', 'utf-8')

    real = sys.stderr
    sys.stderr = _StderrCapture(real)
    try:
        return converter(input_path_str)
    finally:
        sys.stderr = real


# ---------------------------------------------------------------------------
# Model cache — loaded once per process, reused for all conversions
# ---------------------------------------------------------------------------
_model_dict = None


def _get_models():
    """Load marker models once and cache them in the module."""
    global _model_dict
    if _model_dict is None:
        from marker.models import create_model_dict
        _model_dict = create_model_dict()
    return _model_dict


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def convert_pdf_to_markdown(
    input_path,
    output_path=None,
    *,
    write_images: bool = False,
    image_dir=None,
    margins=None,
    dpi: int = 150,
    progress_callback=None,
) -> str:
    """
    Convert a PDF file to Markdown text using marker-pdf.

    Parameters
    ----------
    input_path:
        Path to the source PDF file.
    output_path:
        Path where the Markdown file will be written. If None the file is
        written next to the PDF with the same stem and a .md extension.
    write_images:
        Extract embedded images and save them alongside the output file.
    image_dir:
        Directory for extracted images. Defaults to a sub-folder named
        ``<stem>_images`` beside the output file.

    Returns
    -------
    str
        The full Markdown string.
    """
    from marker.converters.pdf import PdfConverter
    from marker.output import text_from_rendered
    from marker.config.parser import ConfigParser

    input_path = Path(input_path).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"PDF not found: {input_path}")
    if input_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {input_path.suffix}")

    if output_path is None:
        output_path = input_path.with_suffix(".md")
    output_path = Path(output_path).resolve()

    if write_images and image_dir is None:
        image_dir = output_path.parent / f"{output_path.stem}_images"
    if image_dir is not None:
        image_dir = Path(image_dir)
        image_dir.mkdir(parents=True, exist_ok=True)

    # Count pages so the GUI can show a total
    doc_pages = _count_pdf_pages(input_path)
    if progress_callback and doc_pages:
        progress_callback(0, doc_pages, f"{doc_pages} pages detected")

    print(f"Converting: {input_path}")
    print(f"      -> MD: {output_path}")
    print("       (using marker-pdf ML engine)")

    config: dict = {"output_format": "markdown"}
    if not write_images:
        config["disable_image_extraction"] = True

    # --- Speed optimisations (accuracy-preserving) ---
    import os
    import torch

    # Allow reduced-precision matmul (still highly accurate, ~10-20% faster)
    torch.set_float32_matmul_precision("high")

    # Use all CPU cores for PDF text extraction (default is 4)
    config["pdftext_workers"] = os.cpu_count() or 4

    # GPU: scale batch sizes to available VRAM
    if torch.cuda.is_available():
        vram_gb = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        bs = max(6, int(vram_gb // 1.5))
        config["layout_batch_size"] = bs * 2
        config["detection_batch_size"] = bs
        config["recognition_batch_size"] = bs
        print(f"       GPU detected ({vram_gb:.1f} GB) — batch size {bs}")

    config_parser = ConfigParser(config)

    converter = PdfConverter(
        config=config_parser.generate_config_dict(),
        artifact_dict=_get_models(),
        processor_list=config_parser.get_processors(),
        renderer=config_parser.get_renderer(),
    )
    if progress_callback:
        rendered = _convert_with_progress(converter, str(input_path), progress_callback)
    else:
        rendered = converter(str(input_path))
    md_text, _, images = text_from_rendered(rendered)

    if write_images and images:
        for img_name, img_data in images.items():
            img_path = image_dir / img_name
            if isinstance(img_data, bytes):
                img_path.write_bytes(img_data)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(md_text, encoding="utf-8")

    char_count = len(md_text)
    line_count = md_text.count("\n")
    print(f"   Done.  {line_count:,} lines / {char_count:,} characters written.")

    return md_text


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf_to_markdown",
        description="Convert a PDF file to Markdown (powered by marker-pdf).",
    )
    parser.add_argument("input", metavar="INPUT.PDF", help="Path to the source PDF file.")
    parser.add_argument("output", metavar="OUTPUT.MD", nargs="?", default=None,
                        help="Destination Markdown file (default: same name as PDF, .md).")
    parser.add_argument("--images", action="store_true",
                        help="Extract embedded images and save them next to the output file.")
    parser.add_argument("--image-dir", metavar="DIR", default=None,
                        help="Directory for extracted images (implies --images).")
    return parser


def main(argv=None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    write_images = args.images or bool(args.image_dir)
    try:
        convert_pdf_to_markdown(
            input_path=args.input,
            output_path=args.output,
            write_images=write_images,
            image_dir=args.image_dir,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
