#!/usr/bin/env python3
"""
app.py — PDF to Markdown Converter GUI

Launch via 'Launch PDF to Markdown.vbs' (no terminal window).
Can also be run directly:  python app.py
"""

import os
import sys
import io
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# pythonw.exe (used by the VBS launcher) sets stdout/stderr to None.
# Redirect them to a no-op buffer so print() calls don't crash.
if sys.stdout is None:
    sys.stdout = io.StringIO()
if sys.stderr is None:
    sys.stderr = io.StringIO()

# Ensure the tool directory is on the path so pdf_to_markdown is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdf_to_markdown import convert_pdf_to_markdown  # noqa: E402

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TITLE    = "PDF → Markdown Converter"
W, H     = 660, 360
BG_DARK  = "#1a1a2e"
FG_LIGHT = "#ffffff"
ACCENT   = "#0066cc"


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(TITLE)
        self.geometry(f"{W}x{H}")
        self.resizable(False, False)
        self._last_output: Path | None = None

        # DPI scaling hint
        try:
            self.tk.call("tk", "scaling", 1.25)
        except Exception:
            pass

        # Theme — 'vista' looks best on Windows; fall back gracefully
        style = ttk.Style(self)
        for theme in ("vista", "winnative", "clam", "alt", "default"):
            if theme in style.theme_names():
                style.theme_use(theme)
                break

        # Make "Convert" button stand out slightly
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))

        self._build_ui()
        self._enable_drop()   # register drag-and-drop if tkinterdnd2 is available

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        # ── Header bar ────────────────────────────────────────────────
        header = tk.Frame(self, bg=BG_DARK, height=52)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(
            header, text="  PDF  →  Markdown",
            bg=BG_DARK, fg=FG_LIGHT,
            font=("Segoe UI", 14, "bold"),
            anchor="w",
        ).pack(fill=tk.BOTH, expand=True, padx=20)

        # ── Body ──────────────────────────────────────────────────────
        body = ttk.Frame(self, padding=(22, 16, 22, 14))
        body.pack(fill=tk.BOTH, expand=True)
        body.columnconfigure(1, weight=1)

        # Row 0 – PDF input
        ttk.Label(body, text="PDF File:").grid(
            row=0, column=0, sticky="w", pady=(0, 6))
        self.input_var = tk.StringVar()
        self._input_entry = ttk.Entry(
            body, textvariable=self.input_var, width=54)
        self._input_entry.grid(
            row=0, column=1, sticky="ew", padx=(10, 8), pady=(0, 6))
        ttk.Button(
            body, text="Browse…", width=9, command=self._browse_input,
        ).grid(row=0, column=2, pady=(0, 6))

        # Row 1 – Markdown output
        ttk.Label(body, text="Save as:").grid(
            row=1, column=0, sticky="w", pady=(0, 6))
        self.output_var = tk.StringVar()
        ttk.Entry(body, textvariable=self.output_var, width=54).grid(
            row=1, column=1, sticky="ew", padx=(10, 8), pady=(0, 6))
        ttk.Button(
            body, text="Browse…", width=9, command=self._browse_output,
        ).grid(row=1, column=2, pady=(0, 6))

        # Row 2 – Options + Convert button
        opt_row = ttk.Frame(body)
        opt_row.grid(row=2, column=0, columnspan=3, sticky="ew",
                     pady=(4, 10))
        self.images_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            opt_row, text="Extract embedded images",
            variable=self.images_var,
        ).pack(side=tk.LEFT)
        self.convert_btn = ttk.Button(
            opt_row, text="Convert  →", width=14,
            style="Accent.TButton", command=self._start_convert,
        )
        self.convert_btn.pack(side=tk.RIGHT)

        # Row 3 – Progress bar (determinate)
        self.progress = ttk.Progressbar(
            body, mode="determinate", maximum=100, length=100)
        self.progress.grid(
            row=3, column=0, columnspan=3, sticky="ew", pady=(0, 2))

        # Row 4 – Page / percentage detail label  (NEW)
        self.progress_info_var = tk.StringVar(value="")
        ttk.Label(
            body, textvariable=self.progress_info_var,
            foreground="#0066cc", font=("Segoe UI", 9),
            anchor="w",
        ).grid(row=4, column=0, columnspan=3, sticky="w", pady=(0, 4))

        # Row 5 – Status text
        self.status_var = tk.StringVar(
            value="Select a PDF file — or drag one onto the window — to get started.\n"
                  "Note: first conversion downloads ML models (~500 MB) and may take a few minutes.")
        ttk.Label(
            body, textvariable=self.status_var,
            foreground="#444", wraplength=610, justify="left",
        ).grid(row=5, column=0, columnspan=3, sticky="w")

        # Row 6 – Post-conversion buttons (packed dynamically)
        self.result_frame = ttk.Frame(body)
        self.result_frame.grid(
            row=6, column=0, columnspan=3, sticky="w", pady=(6, 0))
        self._open_file_btn = ttk.Button(
            self.result_frame, text="Open Markdown", command=self._open_file)
        self._open_folder_btn = ttk.Button(
            self.result_frame, text="Open Folder", command=self._open_folder)

    # ------------------------------------------------------------------
    # Drag-and-drop (optional — requires tkinterdnd2)
    # ------------------------------------------------------------------

    def _enable_drop(self) -> None:
        try:
            from tkinterdnd2 import DND_FILES  # type: ignore
            self.drop_target_register(DND_FILES)
            self.dnd_bind("<<Drop>>", self._on_drop)
        except Exception:
            pass   # tkinterdnd2 not installed — drop is silently unavailable

    def _on_drop(self, event) -> None:
        # Strip braces that Tk adds around paths with spaces
        path = event.data.strip().strip("{}")
        if path.lower().endswith(".pdf") and Path(path).exists():
            self.input_var.set(path)
            if not self.output_var.get():
                self.output_var.set(str(Path(path).with_suffix(".md")))
            self.status_var.set("Ready — click  Convert →  to begin.")
            self._hide_result_buttons()

    # ------------------------------------------------------------------
    # File dialogs
    # ------------------------------------------------------------------

    def _browse_input(self) -> None:
        path = filedialog.askopenfilename(
            title="Select a PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
        )
        if not path:
            return
        self.input_var.set(path)
        if not self.output_var.get():
            self.output_var.set(str(Path(path).with_suffix(".md")))
        self.status_var.set("Ready — click  Convert →  to begin.")
        self._hide_result_buttons()

    def _browse_output(self) -> None:
        inp = self.input_var.get().strip()
        initial = str(Path(inp).with_suffix(".md")) if inp else ""
        path = filedialog.asksaveasfilename(
            title="Save Markdown file as",
            initialfile=Path(initial).name if initial else "",
            initialdir=str(Path(initial).parent) if initial else "",
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
        )
        if path:
            self.output_var.set(path)

    # ------------------------------------------------------------------
    # Conversion
    # ------------------------------------------------------------------

    def _start_convert(self) -> None:
        inp = self.input_var.get().strip()
        if not inp:
            messagebox.showwarning(
                "No file selected", "Please select a PDF file first.")
            return
        if not Path(inp).exists():
            messagebox.showerror(
                "File not found", f"Cannot find:\n{inp}")
            return

        out = self.output_var.get().strip() or None
        self._last_output = (
            Path(out).resolve() if out
            else Path(inp).with_suffix(".md").resolve()
        )

        self.convert_btn.config(state="disabled")
        self.progress['value'] = 0
        self.progress_info_var.set("Loading ML models…")
        self.status_var.set(
            "Converting — please wait. On CPU this takes 30–60 min for a typical document.\n"
            "The progress bar will update once layout detection begins."
        )
        self._hide_result_buttons()

        def _worker() -> None:
            try:
                convert_pdf_to_markdown(
                    inp, out,
                    write_images=self.images_var.get(),
                    progress_callback=self._on_progress,
                )
                self.after(0, self._on_success)
            except Exception as exc:  # noqa: BLE001
                self.after(0, lambda e=exc: self._on_error(e))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_progress(self, current: int, total: int, stage: str = "") -> None:
        """Called from the worker thread — schedules a safe GUI update."""
        pct = int(current / total * 100) if total > 0 else 0
        pages_str = f"Page {current} of {total}"
        stage_str = f"  ·  {stage}" if stage else ""
        info = f"{pages_str}{stage_str}  —  {pct}%"
        self.after(0, lambda p=pct, t=info: (
            self.progress.__setitem__('value', p),
            self.progress_info_var.set(t),
        ))

    def _on_success(self) -> None:
        self.progress['value'] = 100
        self.progress_info_var.set("")
        self.convert_btn.config(state="normal")
        self.status_var.set(f"✔  Saved to:  {self._last_output}")
        self._open_file_btn.pack(side=tk.LEFT, padx=(0, 8))
        self._open_folder_btn.pack(side=tk.LEFT)

    def _on_error(self, exc: Exception) -> None:
        self.progress['value'] = 0
        self.progress_info_var.set("")
        self.convert_btn.config(state="normal")
        self.status_var.set(f"✘  {exc}")
        messagebox.showerror("Conversion failed", str(exc))

    # ------------------------------------------------------------------
    # Open result
    # ------------------------------------------------------------------

    def _open_file(self) -> None:
        if self._last_output and self._last_output.exists():
            os.startfile(str(self._last_output))

    def _open_folder(self) -> None:
        if self._last_output:
            os.startfile(str(self._last_output.parent))

    def _hide_result_buttons(self) -> None:
        for w in self.result_frame.winfo_children():
            w.pack_forget()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app = App()
    app.mainloop()
