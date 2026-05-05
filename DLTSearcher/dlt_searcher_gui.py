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
from dataclasses import dataclass


DLT_STORAGE_HEADER_PATTERN = b"DLT\x01"


@dataclass
class DltMessage:
    file_path: str
    message_index: int
    timestamp_s: int
    timestamp_us: int
    ecu_id: str
    app_id: str
    context_id: str
    payload_text: str


def extract_readable_text(data: bytes) -> str:
    text_parts = []
    current = []
    for byte in data:
        if 32 <= byte < 127:
            current.append(chr(byte))
        elif byte == 0 and current:
            text_parts.append("".join(current))
            current = []
        else:
            if len(current) >= 3:
                text_parts.append("".join(current))
            current = []
    if len(current) >= 3:
        text_parts.append("".join(current))
    return " ".join(text_parts)


def parse_dlt_file(file_path: str) -> list[DltMessage]:
    messages = []
    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except (OSError, IOError):
        return messages

    pos = 0
    msg_index = 0
    data_len = len(data)

    while pos < data_len - 16:
        next_marker = data.find(DLT_STORAGE_HEADER_PATTERN, pos)
        if next_marker == -1:
            break
        pos = next_marker

        if pos + 16 > data_len:
            break

        try:
            _, timestamp_s, timestamp_us = struct.unpack_from("<4sII", data, pos)
            storage_ecu_id = data[pos + 12:pos + 16].split(b"\x00")[0].decode("ascii", errors="replace")
        except struct.error:
            pos += 4
            continue

        pos += 16

        if pos + 4 > data_len:
            break

        try:
            htyp, mcnt, length = struct.unpack_from(">BBH", data, pos)
        except struct.error:
            pos += 1
            continue

        if length < 4 or pos + length > data_len:
            pos += 1
            continue

        msg_start = pos
        std_hdr_pos = pos + 4

        use_extended_header = bool(htyp & 0x01)
        with_ecu_id = bool(htyp & 0x04)
        with_session_id = bool(htyp & 0x08)
        with_timestamp = bool(htyp & 0x10)

        ecu_id = storage_ecu_id
        if with_ecu_id:
            if std_hdr_pos + 4 > data_len:
                pos = msg_start + length
                continue
            ecu_id = data[std_hdr_pos:std_hdr_pos + 4].split(b"\x00")[0].decode("ascii", errors="replace")
            std_hdr_pos += 4

        if with_session_id:
            std_hdr_pos += 4

        if with_timestamp:
            std_hdr_pos += 4

        app_id = ""
        context_id = ""
        if use_extended_header:
            if std_hdr_pos + 10 > data_len:
                pos = msg_start + length
                continue
            app_id = data[std_hdr_pos + 2:std_hdr_pos + 6].split(b"\x00")[0].decode("ascii", errors="replace")
            context_id = data[std_hdr_pos + 6:std_hdr_pos + 10].split(b"\x00")[0].decode("ascii", errors="replace")
            std_hdr_pos += 10

        payload_start = std_hdr_pos
        payload_end = msg_start + length
        if payload_start < payload_end and payload_end <= data_len:
            payload_data = data[payload_start:payload_end]
            payload_text = extract_readable_text(payload_data)
        else:
            payload_text = ""

        if payload_text.strip():
            messages.append(DltMessage(
                file_path=file_path,
                message_index=msg_index,
                timestamp_s=timestamp_s,
                timestamp_us=timestamp_us,
                ecu_id=ecu_id,
                app_id=app_id,
                context_id=context_id,
                payload_text=payload_text,
            ))

        msg_index += 1
        pos = msg_start + length

    return messages


class DltSearcherApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DLT Log Searcher")
        self.root.geometry("1200x700")
        self.root.minsize(800, 400)

        self.all_messages: list[DltMessage] = []
        self.loading = False
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
        for i, f in enumerate(dlt_files):
            pct = ((i + 1) / total) * 100
            msg_count = len(all_msgs)
            self.root.after(0, self._update_load_progress, i + 1, total, msg_count, f.name, pct)
            msgs = parse_dlt_file(str(f))
            all_msgs.extend(msgs)

        self.all_messages = all_msgs
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

        self._clear_results()
        self.status_var.set("Searching...")
        self.progress_var.set(0)
        self.root.update_idletasks()

        use_regex = self.regex_var.get()
        case_sensitive = self.case_var.get()
        flags = 0 if case_sensitive else re.IGNORECASE
        total_msgs = len(self.all_messages)
        query_lower = query.lower() if not case_sensitive else query

        results = []
        for i, msg in enumerate(self.all_messages):
            # Update progress every 5000 messages
            if i % 5000 == 0:
                pct = (i / total_msgs) * 100
                self.progress_var.set(pct)
                self.status_var.set(f"Searching... {i:,}/{total_msgs:,} messages checked, {len(results):,} matches")
                self.root.update_idletasks()

            search_text = f"{msg.ecu_id} {msg.app_id} {msg.context_id} {msg.payload_text}"
            if use_regex:
                try:
                    if re.search(query, search_text, flags):
                        results.append(msg)
                except re.error:
                    self.status_var.set("Invalid regex pattern")
                    self.progress_var.set(0)
                    return
            else:
                if case_sensitive:
                    if query in search_text:
                        results.append(msg)
                else:
                    if query_lower in search_text.lower():
                        results.append(msg)

        self.progress_var.set(100)
        self.status_var.set(f"Populating results...")
        self.root.update_idletasks()

        # Populate tree (cap at 10000 for UI responsiveness)
        display_count = min(len(results), 10000)
        for msg in results[:display_count]:
            try:
                rel_path = os.path.relpath(msg.file_path, self.root_folder)
            except ValueError:
                rel_path = msg.file_path
            timestamp = f"{msg.timestamp_s}.{msg.timestamp_us:06d}"
            self.tree.insert("", tk.END, values=(
                rel_path,
                timestamp,
                msg.app_id,
                msg.context_id,
                msg.payload_text,
            ))

        if len(results) > 10000:
            self.status_var.set(f"{len(results):,} matches found (showing first 10,000) — searched {total_msgs:,} messages")
        else:
            self.status_var.set(f"{len(results):,} match(es) found — searched {total_msgs:,} messages")

    def _clear_results(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    DltSearcherApp().run()
