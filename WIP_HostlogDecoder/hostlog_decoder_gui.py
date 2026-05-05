#!/usr/bin/env python3
"""Lightweight GUI for decoding hostlog binary files to HDF5."""

from __future__ import annotations

import re
import subprocess
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

from decode_hostlog_to_hdf5 import build_command, find_latest_tdf_dir, parse_paths_file


class HostlogDecoderGui:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Hostlog Decoder to HDF5")
        self.root.geometry("900x560")

        self.script_dir = Path(__file__).resolve().parent
        self.defaults = parse_paths_file(self.script_dir / "Paths")

        self.hostlog_var = tk.StringVar(value=self.defaults.get("hostlog_dir", ""))
        self.log_file_var = tk.StringVar(value=self.defaults.get("log_file", ""))
        self.definitions_var = tk.StringVar(value="")
        self.output_var = tk.StringVar(value="")

        self.decode_enum_as_int_var = tk.BooleanVar(value=False)
        self.enable_named_datasets_var = tk.BooleanVar(value=True)

        self._build_ui()
        self._autofill_paths()

    def _build_ui(self) -> None:
        container = tk.Frame(self.root, padx=12, pady=12)
        container.pack(fill=tk.BOTH, expand=True)

        self._row_with_browse(
            container,
            row=0,
            label="Hostlog client folder",
            var=self.hostlog_var,
            browse_cmd=self._browse_hostlog_dir,
        )
        self._row_with_browse(
            container,
            row=1,
            label="Hostlog .bin file",
            var=self.log_file_var,
            browse_cmd=self._browse_log_file,
        )
        self._row_with_browse(
            container,
            row=2,
            label="TDF definitions folder",
            var=self.definitions_var,
            browse_cmd=self._browse_definitions,
        )
        self._row_with_browse(
            container,
            row=3,
            label="Output folder",
            var=self.output_var,
            browse_cmd=self._browse_output,
        )

        options = tk.Frame(container)
        options.grid(row=4, column=0, columnspan=3, sticky="w", pady=(8, 6))
        tk.Checkbutton(
            options,
            text="Decode enum as int",
            variable=self.decode_enum_as_int_var,
        ).pack(side=tk.LEFT, padx=(0, 12))
        tk.Checkbutton(
            options,
            text="Enable named datasets",
            variable=self.enable_named_datasets_var,
        ).pack(side=tk.LEFT)

        actions = tk.Frame(container)
        actions.grid(row=5, column=0, columnspan=3, sticky="ew", pady=(4, 8))
        actions.columnconfigure(2, weight=1)

        self.btn_autofill = tk.Button(actions, text="Auto-fill", width=10, command=self._autofill_paths)
        self.btn_autofill.grid(row=0, column=0, padx=(0, 8), sticky="w")

        self.btn_decode = tk.Button(actions, text="Decode to HDF5", width=16, command=self._start_decode)
        self.btn_decode.grid(row=0, column=1, padx=(0, 8), sticky="w")

        self.status_label = tk.Label(actions, text="Ready.", anchor="w")
        self.status_label.grid(row=0, column=2, sticky="ew")

        tk.Label(container, text="Output log").grid(row=6, column=0, columnspan=3, sticky="w")

        self.log_box = ScrolledText(container, height=18, wrap=tk.WORD)
        self.log_box.grid(row=7, column=0, columnspan=3, sticky="nsew", pady=(4, 0))
        self.log_box.configure(state=tk.DISABLED)

        container.columnconfigure(1, weight=1)
        container.rowconfigure(7, weight=1)

    def _row_with_browse(self, parent: tk.Frame, row: int, label: str, var: tk.StringVar, browse_cmd) -> None:
        tk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        tk.Entry(parent, textvariable=var).grid(row=row, column=1, sticky="ew", pady=4, padx=(8, 8))
        tk.Button(parent, text="Browse", width=10, command=browse_cmd).grid(row=row, column=2, sticky="e", pady=4)

    def _append_log(self, text: str) -> None:
        self.log_box.configure(state=tk.NORMAL)
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)
        self.log_box.configure(state=tk.DISABLED)

    def _set_status(self, text: str) -> None:
        self.status_label.config(text=text)

    def _browse_hostlog_dir(self) -> None:
        chosen = filedialog.askdirectory(title="Select hostlog-client folder")
        if chosen:
            self.hostlog_var.set(chosen)
            if not self.definitions_var.get().strip():
                latest = find_latest_tdf_dir(Path(chosen))
                if latest:
                    self.definitions_var.set(str(latest))

    def _browse_log_file(self) -> None:
        chosen = filedialog.askopenfilename(
            title="Select hostlog binary file",
            filetypes=[("Binary files", "*.bin *.bin.gz"), ("All files", "*.*")],
        )
        if chosen:
            self.log_file_var.set(chosen)
            if not self.output_var.get().strip():
                self.output_var.set(str(Path(chosen).resolve().parent / "decoded_hdf5"))

    def _browse_definitions(self) -> None:
        chosen = filedialog.askdirectory(title="Select TDF definitions folder")
        if chosen:
            self.definitions_var.set(chosen)

    def _browse_output(self) -> None:
        chosen = filedialog.askdirectory(title="Select output folder")
        if chosen:
            self.output_var.set(chosen)

    def _autofill_paths(self) -> None:
        hostlog_dir = Path(self.hostlog_var.get().strip()) if self.hostlog_var.get().strip() else None
        log_file = Path(self.log_file_var.get().strip()) if self.log_file_var.get().strip() else None

        if hostlog_dir and hostlog_dir.exists() and not self.definitions_var.get().strip():
            latest = find_latest_tdf_dir(hostlog_dir)
            if latest:
                self.definitions_var.set(str(latest))

        if log_file and log_file.exists() and not self.output_var.get().strip():
            self.output_var.set(str(log_file.parent / "decoded_hdf5"))

        self._set_status("Paths auto-filled.")

    def _validate_inputs(self) -> tuple[Path, Path, Path, Path] | None:
        hostlog_dir = Path(self.hostlog_var.get().strip())
        log_file = Path(self.log_file_var.get().strip())
        definitions = Path(self.definitions_var.get().strip()) if self.definitions_var.get().strip() else None
        output = Path(self.output_var.get().strip()) if self.output_var.get().strip() else None

        if not hostlog_dir:
            messagebox.showerror("Missing input", "Hostlog client folder is required.")
            return None
        if not log_file:
            messagebox.showerror("Missing input", "Hostlog .bin file is required.")
            return None

        hostlog_dir = hostlog_dir.expanduser().resolve()
        log_file = log_file.expanduser().resolve()

        hostlog_bat = hostlog_dir / "hostlog.bat"
        if not hostlog_bat.exists():
            messagebox.showerror("Invalid input", f"hostlog.bat not found in:\n{hostlog_dir}")
            return None

        if not log_file.exists():
            messagebox.showerror("Invalid input", f"Log file not found:\n{log_file}")
            return None

        if definitions is None:
            detected = find_latest_tdf_dir(hostlog_dir)
            if detected is None:
                messagebox.showerror(
                    "Missing definitions",
                    "Could not auto-find TDF folder. Please select definitions folder.",
                )
                return None
            definitions = detected
            self.definitions_var.set(str(definitions))
        else:
            definitions = definitions.expanduser().resolve()

        if not definitions.exists():
            messagebox.showerror("Invalid input", f"Definitions path not found:\n{definitions}")
            return None

        if output is None:
            output = log_file.parent / "decoded_hdf5"
            self.output_var.set(str(output))
        output = output.expanduser().resolve()

        return hostlog_dir, log_file, definitions, output

    def _start_decode(self) -> None:
        validated = self._validate_inputs()
        if validated is None:
            return

        hostlog_dir, log_file, definitions, output = validated
        output.mkdir(parents=True, exist_ok=True)

        cmd = build_command(
            hostlog_bat=hostlog_dir / "hostlog.bat",
            binary_file=log_file,
            output_dir=output,
            definitions=definitions,
            decode_enum_as_int=self.decode_enum_as_int_var.get(),
            enable_named_datasets=self.enable_named_datasets_var.get(),
        )

        self.btn_decode.config(state=tk.DISABLED)
        self._set_status("Decoding...")
        self._append_log("Starting decoder...")
        self._append_log(cmd)

        worker = threading.Thread(target=self._run_decode, args=(cmd, hostlog_dir, output, log_file), daemon=True)
        worker.start()

    @staticmethod
    def _strip_ansi(text: str) -> str:
        """Remove ANSI escape sequences from text."""
        return re.sub(r"\x1b\[[0-9;]*m", "", text)

    @staticmethod
    def _summarize_output(raw: str) -> str:
        """Build a clean summary from hostlog-client output."""
        clean = re.sub(r"\x1b\[[0-9;]*m", "", raw)
        lines = clean.splitlines()

        warnings: list[str] = []
        errors: list[str] = []
        info: list[str] = []

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("="):
                continue
            if "WARNING" in line:
                continue  # skip the long shallow-topics header
            if "ERROR" in line:
                # Extract the meaningful part
                if "Exception when decoding" in line:
                    m = re.search(r"'(Channel_id:.*?)'", line)
                    if m:
                        errors.append(m.group(1))
                elif "Message size is inconsistent" in line:
                    continue  # duplicate of the line above
                else:
                    errors.append(stripped)
            elif "occurrences:" in stripped:
                # Summary table row from DECODING ISSUES block
                warnings.append(stripped)
            elif "HDF5 saved to" in line:
                m = re.search(r"HDF5 saved to '(.+?)'", line)
                if m:
                    info.append(f"HDF5 saved to: {m.group(1)}")
            elif "BinaryPlaybackDecodingException" in line:
                continue  # already captured above
            elif "Traceback" in line or "raise " in line or "File \"" in line:
                continue  # suppress internal traceback noise

        # De-duplicate errors (hostlog shows first-occurrence + summary)
        seen_errors = set()
        unique_errors: list[str] = []
        for e in errors:
            key = re.sub(r"\s+", " ", e)
            if key not in seen_errors:
                seen_errors.add(key)
                unique_errors.append(e)

        parts: list[str] = []
        for i in info:
            parts.append(f"[OK] {i}")

        if warnings:
            parts.append(f"\n[WARNINGS] {len(warnings)} topic(s) had decoding issues (TDF mismatch):")
            for w in warnings[:10]:
                parts.append(f"  - {w}")
            if len(warnings) > 10:
                parts.append(f"  ... and {len(warnings) - 10} more")

        if unique_errors:
            parts.append(f"\n[ERRORS] {len(unique_errors)} unique decoding error(s):")
            for e in unique_errors[:10]:
                parts.append(f"  - {e}")
            if len(unique_errors) > 10:
                parts.append(f"  ... and {len(unique_errors) - 10} more")

        return "\n".join(parts) if parts else clean

    def _run_decode(self, cmd: str, cwd: Path, output: Path, log_file: Path) -> None:
        try:
            proc = subprocess.run(
                cmd,
                cwd=cwd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
            stdout = proc.stdout or ""
        except Exception as exc:
            self.root.after(0, self._decode_failed, f"Failed to run decoder: {exc}")
            return

        # Check if HDF5 file was created (hostlog-client returns exit code 1 for warnings)
        hdf5_file = output / "logs" / (log_file.stem + ".hdf5")
        if hdf5_file.exists():
            self.root.after(0, self._decode_done, output, stdout, hdf5_file)
            return

        if proc.returncode != 0:
            msg = f"Decoder failed with exit code {proc.returncode}."
            self.root.after(0, self._decode_failed, msg, stdout)
            return

        self.root.after(0, self._decode_done, output, stdout, hdf5_file)

    def _decode_failed(self, message: str, output_text: str = "") -> None:
        summary = self._summarize_output(output_text) if output_text.strip() else ""
        self._append_log("\n" + "=" * 60)
        self._append_log("DECODE FAILED")
        self._append_log("=" * 60)
        if summary:
            self._append_log(summary)
        self._append_log(f"\n{message}")
        self._set_status("Decode failed.")
        self.btn_decode.config(state=tk.NORMAL)
        messagebox.showerror("Decode failed", message)

    def _decode_done(self, output: Path, output_text: str, hdf5_file: Path) -> None:
        summary = self._summarize_output(output_text) if output_text.strip() else ""
        self._append_log("\n" + "=" * 60)
        self._append_log("DECODE COMPLETE")
        self._append_log("=" * 60)
        if summary:
            self._append_log(summary)
        else:
            self._append_log(f"[OK] HDF5 saved to: {hdf5_file}")
        self._append_log(f"\nOutput folder: {output}")
        self._set_status("Decode complete.")
        self.btn_decode.config(state=tk.NORMAL)
        messagebox.showinfo("Decode complete", f"HDF5 decoded successfully.\n\nOutput:\n{hdf5_file}")


def main() -> int:
    root = tk.Tk()
    HostlogDecoderGui(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
