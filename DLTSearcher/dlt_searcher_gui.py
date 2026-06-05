"""
DLT Log Searcher - Lightweight GUI
"""

import struct
import os
import sys
import re
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
from threading import Thread


DLT_STORAGE_HEADER_PATTERN = b"DLT\x01"

# Pre-compiled regex: extract runs of printable ASCII characters.
# Replaces byte-by-byte Python loop with the C-level regex engine.
_PRINTABLE_RUN = re.compile(rb'[\x20-\x7e]+')

# Tuple field indices (avoids per-object dataclass overhead for millions of messages)
_F_PATH = 0
_F_IDX = 1
_F_TS_S = 2
_F_TS_US = 3
_F_ECU = 4
_F_APP = 5
_F_CTX = 6
_F_TEXT = 7


def extract_readable_text(data: bytes) -> str:
    parts = _PRINTABLE_RUN.findall(data)
    return b" ".join(parts).decode("ascii") if parts else ""


def parse_dlt_file(file_path: str) -> tuple[list[tuple], list[str]]:
    """
    Parse a single DLT file.
    Returns (messages, search_texts) where:
      - messages: list of tuples (path, idx, ts_s, ts_us, ecu, app, ctx, text)
      - search_texts: pre-computed lowercase search strings (one per message)
    """
    messages = []
    search_texts = []
    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except (OSError, IOError):
        return messages, search_texts

    pos = 0
    msg_index = 0
    data_len = len(data)
    # Local references for hot-loop performance
    _find = data.find
    _unpack = struct.unpack_from
    _marker = DLT_STORAGE_HEADER_PATTERN
    _extract = extract_readable_text

    while pos < data_len - 16:
        next_marker = _find(_marker, pos)
        if next_marker == -1:
            break
        pos = next_marker

        if pos + 16 > data_len:
            break

        try:
            _, timestamp_s, timestamp_us = _unpack("<4sII", data, pos)
            storage_ecu_id = data[pos + 12:pos + 16].split(b"\x00", 1)[0].decode("ascii", errors="replace")
        except struct.error:
            pos += 4
            continue

        pos += 16

        if pos + 4 > data_len:
            break

        try:
            htyp, mcnt, length = _unpack(">BBH", data, pos)
        except struct.error:
            pos += 1
            continue

        if length < 4 or pos + length > data_len:
            pos += 1
            continue

        msg_start = pos
        std_hdr_pos = pos + 4

        ecu_id = storage_ecu_id
        if htyp & 0x04:
            if std_hdr_pos + 4 > data_len:
                pos = msg_start + length
                continue
            ecu_id = data[std_hdr_pos:std_hdr_pos + 4].split(b"\x00", 1)[0].decode("ascii", errors="replace")
            std_hdr_pos += 4

        if htyp & 0x08:
            std_hdr_pos += 4

        if htyp & 0x10:
            std_hdr_pos += 4

        app_id = ""
        context_id = ""
        if htyp & 0x01:
            if std_hdr_pos + 10 > data_len:
                pos = msg_start + length
                continue
            app_id = data[std_hdr_pos + 2:std_hdr_pos + 6].split(b"\x00", 1)[0].decode("ascii", errors="replace")
            context_id = data[std_hdr_pos + 6:std_hdr_pos + 10].split(b"\x00", 1)[0].decode("ascii", errors="replace")
            std_hdr_pos += 10

        payload_start = std_hdr_pos
        payload_end = msg_start + length
        if payload_start < payload_end and payload_end <= data_len:
            payload_text = _extract(data[payload_start:payload_end])
        else:
            payload_text = ""

        if payload_text:
            messages.append((
                file_path,
                msg_index,
                timestamp_s,
                timestamp_us,
                ecu_id,
                app_id,
                context_id,
                payload_text,
            ))
            search_texts.append(f"{ecu_id} {app_id} {context_id} {payload_text}".lower())

        msg_index += 1
        pos = msg_start + length

    return messages, search_texts


class DltSearcherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DLT Log Searcher")
        self.root.geometry("1200x700")
        self.root.minsize(800, 400)

        self.all_messages: list[tuple] = []
        self._search_texts: list[str] = []
        self.loading = False
        self._search_generation = 0
        self.root_folder = ""

        self._build_ui()

    def _build_ui(self):
        # Top frame - folder selection
        top = ttk.Frame(self.root, padding=5)
        top.pack(fill=tk.X)

        ttk.Label(top, text="Folder:").pack(side=tk.LEFT)
        self.folder_var = tk.StringVar()
        self.folder_entry = ttk.Entry(top, textvariable=self.folder_var, width=80)
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ttk.Button(top, text="Browse", command=self._browse).pack(side=tk.LEFT)
        self.load_btn = ttk.Button(top, text="Load", command=self._load_files)
        self.load_btn.pack(side=tk.LEFT, padx=5)

        # Search frame
        search_frame = ttk.Frame(self.root, padding=5)
        search_frame.pack(fill=tk.X)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=60)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind("<Return>", lambda e: self._search())

        self.regex_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(search_frame, text="Regex", variable=self.regex_var).pack(side=tk.LEFT)

        self.case_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(search_frame, text="Case sensitive", variable=self.case_var).pack(side=tk.LEFT, padx=5)

        ttk.Button(search_frame, text="Search", command=self._search).pack(side=tk.LEFT)

        # Progress frame
        progress_frame = ttk.Frame(self.root, padding=(5, 2))
        progress_frame.pack(fill=tk.X)

        self.status_var = tk.StringVar(value="Select a folder and click Load")
        ttk.Label(progress_frame, textvariable=self.status_var).pack(side=tk.LEFT, fill=tk.X, expand=True, anchor=tk.W)

        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100, length=200)
        self.progress_bar.pack(side=tk.RIGHT)

        # Results tree
        columns = ("file", "timestamp", "app", "ctx", "message")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("file", text="File", anchor=tk.W)
        self.tree.heading("timestamp", text="Timestamp", anchor=tk.W)
        self.tree.heading("app", text="App", anchor=tk.W)
        self.tree.heading("ctx", text="Context", anchor=tk.W)
        self.tree.heading("message", text="Message", anchor=tk.W)
        self.tree.column("file", width=220, minwidth=100)
        self.tree.column("timestamp", width=140, minwidth=80)
        self.tree.column("app", width=60, minwidth=40)
        self.tree.column("ctx", width=60, minwidth=40)
        self.tree.column("message", width=700, minwidth=200)

        scrollbar_y = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Right-click context menu for copying
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Copy row", command=self._copy_row)
        self.context_menu.add_command(label="Copy message", command=self._copy_message)
        self.context_menu.add_command(label="Copy all results", command=self._copy_all)
        self.tree.bind("<Button-3>", self._show_context_menu)
        self.tree.bind("<Control-c>", lambda e: self._copy_row())

    def _show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def _copy_row(self):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], "values")
        text = "\t".join(str(v) for v in values)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def _copy_message(self):
        sel = self.tree.selection()
        if not sel:
            return
        values = self.tree.item(sel[0], "values")
        self.root.clipboard_clear()
        self.root.clipboard_append(values[-1])  # message is last column

    def _copy_all(self):
        lines = []
        for item in self.tree.get_children():
            values = self.tree.item(item, "values")
            lines.append("\t".join(str(v) for v in values))
        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(lines))

    def _browse(self):
        folder = filedialog.askdirectory(title="Select folder containing DLT logs")
        if folder:
            self.folder_var.set(folder)

    def _load_files(self):
        if self.loading:
            return
        folder = self.folder_var.get().strip()
        if not folder or not Path(folder).is_dir():
            self.status_var.set("Invalid folder path")
            return

        self.loading = True
        self.root_folder = folder
        self.load_btn.config(state=tk.DISABLED)
        self.all_messages.clear()
        self._search_texts.clear()
        self._clear_results()
        self.status_var.set("Scanning for .dlt files...")

        Thread(target=self._load_worker, args=(folder,), daemon=True).start()

    def _load_worker(self, folder: str):
        dlt_files = sorted(Path(folder).rglob("*.dlt"))
        total = len(dlt_files)
        if total == 0:
            self.root.after(0, self._load_done, 0, 0)
            return

        self.root.after(0, self.status_var.set, f"Found {total} .dlt file(s). Parsing...")

        all_msgs = []
        all_search = []
        for i, f in enumerate(dlt_files):
            msgs, search = parse_dlt_file(str(f))
            all_msgs.extend(msgs)
            all_search.extend(search)
            pct = ((i + 1) / total) * 100
            self.root.after(0, self._update_load_progress,
                            i + 1, total, len(all_msgs), f.name, pct)

        self.all_messages = all_msgs
        self._search_texts = all_search
        self.root.after(0, self._load_done, total, len(all_msgs))

    def _update_load_progress(self, current: int, total: int, msg_count: int, filename: str, pct: float):
        self.status_var.set(f"Loading file {current}/{total} ({msg_count:,} messages so far) — {filename}")
        self.progress_var.set(pct)

    def _load_done(self, file_count: int, msg_count: int):
        self.loading = False
        self.load_btn.config(state=tk.NORMAL)
        self.progress_var.set(100)
        if file_count == 0:
            self.status_var.set("No .dlt files found in folder")
            self.progress_var.set(0)
        else:
            self.status_var.set(f"Loaded {msg_count:,} messages from {file_count} file(s). Ready to search.")

    def _search(self):
        query = self.search_var.get().strip()
        if not query:
            return
        if not self.all_messages:
            self.status_var.set("Load files first")
            return

        self._search_generation += 1
        gen = self._search_generation
        self._clear_results()
        self.status_var.set("Searching...")
        self.progress_var.set(0)

        use_regex = self.regex_var.get()
        case_sensitive = self.case_var.get()

        Thread(target=self._search_worker,
               args=(query, use_regex, case_sensitive, gen),
               daemon=True).start()

    def _search_worker(self, query, use_regex, case_sensitive, generation):
        all_msgs = self.all_messages
        search_texts = self._search_texts
        total = len(all_msgs)
        result_indices = []

        if use_regex:
            flags = 0 if case_sensitive else re.IGNORECASE
            try:
                pattern = re.compile(query, flags)
            except re.error:
                self.root.after(0, self.status_var.set, "Invalid regex pattern")
                self.root.after(0, self.progress_var.set, 0)
                return
            _search = pattern.search
            if case_sensitive:
                for i in range(total):
                    if self._search_generation != generation:
                        return
                    if i % 100000 == 0:
                        self.root.after(0, self._update_search_progress, i, total, len(result_indices))
                    msg = all_msgs[i]
                    if _search(f"{msg[_F_ECU]} {msg[_F_APP]} {msg[_F_CTX]} {msg[_F_TEXT]}"):
                        result_indices.append(i)
            else:
                for i in range(total):
                    if self._search_generation != generation:
                        return
                    if i % 100000 == 0:
                        self.root.after(0, self._update_search_progress, i, total, len(result_indices))
                    if _search(search_texts[i]):
                        result_indices.append(i)
        else:
            if case_sensitive:
                for i in range(total):
                    if self._search_generation != generation:
                        return
                    if i % 100000 == 0:
                        self.root.after(0, self._update_search_progress, i, total, len(result_indices))
                    msg = all_msgs[i]
                    if query in f"{msg[_F_ECU]} {msg[_F_APP]} {msg[_F_CTX]} {msg[_F_TEXT]}":
                        result_indices.append(i)
            else:
                query_lower = query.lower()
                for i in range(total):
                    if self._search_generation != generation:
                        return
                    if i % 100000 == 0:
                        self.root.after(0, self._update_search_progress, i, total, len(result_indices))
                    if query_lower in search_texts[i]:
                        result_indices.append(i)

        if self._search_generation != generation:
            return
        self.root.after(0, self._search_done, result_indices, total)

    def _update_search_progress(self, current, total, matches):
        pct = (current / total) * 100
        self.progress_var.set(pct)
        self.status_var.set(f"Searching... {current:,}/{total:,} messages checked, {matches:,} matches")

    def _search_done(self, result_indices, total_msgs):
        total_results = len(result_indices)
        display_count = min(total_results, 10000)
        all_msgs = self.all_messages
        root_folder = self.root_folder

        for idx in result_indices[:display_count]:
            msg = all_msgs[idx]
            try:
                rel_path = os.path.relpath(msg[_F_PATH], root_folder)
            except ValueError:
                rel_path = msg[_F_PATH]
            self.tree.insert("", tk.END, values=(
                rel_path,
                f"{msg[_F_TS_S]}.{msg[_F_TS_US]:06d}",
                msg[_F_APP],
                msg[_F_CTX],
                msg[_F_TEXT],
            ))

        if total_results > 10000:
            self.status_var.set(
                f"{total_results:,} matches found (showing first 10,000) — searched {total_msgs:,} messages")
        else:
            self.status_var.set(
                f"{total_results:,} match(es) found — searched {total_msgs:,} messages")

    def _clear_results(self):
        children = self.tree.get_children()
        if children:
            self.tree.delete(*children)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    DltSearcherApp().run()
