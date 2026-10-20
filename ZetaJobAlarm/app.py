from collections import deque
from datetime import datetime
import json
from pathlib import Path
import queue
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

from monitor_core import Detector, Event, redact, stream_url
from transport import StreamWorker


COLORS = {"Running": "#16786b", "Completed Successfully": "#137a3e", "Failed": "#ba283d", "Aborted": "#ba283d", "Needs Attention": "#9a6100", "Connection Lost / Status Unknown": "#ba283d", "Stopped": "#555f65", "Connecting": "#555f65"}


def desktop_toast(title: str, detail: str) -> None:
    try:
        from winotify import Notification, audio

        toast = Notification(app_id="Zeta Job Alarm", title=title, msg=detail[:240], duration="long")
        toast.set_audio(audio.Silent, loop=False)
        toast.show()
    except Exception:
        pass


class AlarmApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Zeta Job Alarm")
        self.root.geometry("1060x760")
        self.root.minsize(780, 580)
        self.messages: queue.Queue = queue.Queue(maxsize=4000)
        self.stop_event = threading.Event()
        self.detector = Detector()
        self.active = False
        self.started = 0.0
        self.ended = 0.0
        self.last_output = 0.0
        self.lost_since = 0.0
        self.connection_alerted = False
        self.stall_alerted = False
        self.unacknowledged = False
        self.last_sound = 0.0
        self.events: deque[dict] = deque(maxlen=1000)
        self.pending_log: list[str] = []
        self.url = tk.StringVar()
        self.retry_count = tk.StringVar(value="3")
        self.retry_seconds = tk.StringVar(value="60")
        self.stall_seconds = tk.StringVar(value="300")
        self.sound = tk.BooleanVar(value=True)
        self.toasts = tk.BooleanVar(value=True)
        self.focus = tk.BooleanVar(value=True)
        self.follow = tk.BooleanVar(value=True)
        self.status = tk.StringVar(value="Stopped")
        self.detail = tk.StringVar(value="")
        self.metrics = tk.StringVar(value="Elapsed 00:00:00   |   Last output --   |   Source: stopped")
        self.progress = tk.StringVar(value="Iteration --   |   Avg / iteration --   |   Est. remaining --")
        self.source = "stopped"
        self.build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.after(100, self.tick)

    def build_ui(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f3f5f4")
        style.configure("TLabel", background="#f3f5f4", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10), padding=7)
        style.configure("TCheckbutton", background="#f3f5f4", font=("Segoe UI", 10))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=27)
        style.configure("Treeview.Heading", font=("Segoe UI Semibold", 10))
        self.root.configure(background="#f3f5f4")
        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)
        ttk.Label(main, text="Zeta Job Alarm", font=("Segoe UI Semibold", 23)).pack(anchor="w", pady=(0, 14))
        url_row = ttk.Frame(main)
        url_row.pack(fill="x")
        ttk.Label(url_row, text="Live log URL").pack(side="left", padx=(0, 12))
        self.url_entry = ttk.Entry(url_row, textvariable=self.url, font=("Segoe UI", 11))
        self.url_entry.pack(side="left", fill="x", expand=True)
        self.start_button = ttk.Button(url_row, text="Start Monitoring", command=self.start)
        self.start_button.pack(side="left", padx=(10, 0))
        self.stop_button = ttk.Button(url_row, text="Stop", command=self.stop, state="disabled")
        self.stop_button.pack(side="left", padx=(6, 0))
        options = ttk.Frame(main)
        options.pack(fill="x", pady=12)
        self.threshold_widgets = []
        for label, variable, lower, upper in [("Retry count", self.retry_count, 2, 100), ("Retry span (s)", self.retry_seconds, 10, 3600), ("No output (s)", self.stall_seconds, 30, 86400)]:
            ttk.Label(options, text=label).pack(side="left", padx=(0, 6))
            widget = ttk.Spinbox(options, from_=lower, to=upper, textvariable=variable, width=6)
            widget.pack(side="left", padx=(0, 16))
            self.threshold_widgets.append(widget)
        alerts = ttk.Frame(main)
        alerts.pack(fill="x", pady=(0, 12))
        for label, variable in [("Sound", self.sound), ("Desktop notifications", self.toasts), ("Bring to front", self.focus)]:
            ttk.Checkbutton(alerts, text=label, variable=variable).pack(side="left", padx=(0, 18))
        ttk.Button(alerts, text="Test Alert", command=lambda: self.record(Event(self.status.get(), "Notification test", "Zeta Job Alarm notification test.", True))).pack(side="right")
        self.banner = tk.Frame(main, background=COLORS["Stopped"], padx=16, pady=14)
        self.banner.pack(fill="x")
        self.status_label = tk.Label(self.banner, textvariable=self.status, font=("Segoe UI Semibold", 22), fg="white", bg=COLORS["Stopped"], anchor="w")
        self.status_label.pack(fill="x")
        self.detail_label = tk.Label(self.banner, textvariable=self.detail, font=("Segoe UI", 11), fg="white", bg=COLORS["Stopped"], anchor="w", justify="left", wraplength=950)
        self.detail_label.pack(fill="x", pady=(6, 0))
        self.banner.bind("<Configure>", lambda event: self.detail_label.configure(wraplength=max(200, event.width - 32)))
        info = ttk.Frame(main)
        info.pack(fill="x", pady=10)
        ttk.Label(info, textvariable=self.metrics).pack(side="left")
        self.ack_button = ttk.Button(info, text="Acknowledge", command=self.acknowledge, state="disabled")
        self.ack_button.pack(side="right")
        self.progress_label = ttk.Label(main, textvariable=self.progress, font=("Segoe UI Semibold", 12), wraplength=950)
        self.progress_label.pack(fill="x", pady=(0, 12))
        self.progress_label.bind("<Configure>", lambda event: self.progress_label.configure(wraplength=max(200, event.width)))
        notebook = ttk.Notebook(main)
        notebook.pack(fill="both", expand=True)
        event_frame = ttk.Frame(notebook)
        log_frame = ttk.Frame(notebook)
        notebook.add(event_frame, text="Events")
        notebook.add(log_frame, text="Live Log")
        self.event_view = ttk.Treeview(event_frame, columns=("time", "event", "detail"), show="headings")
        self.event_view.tag_configure("success", foreground="#137a3e")
        self.event_view.tag_configure("progress", foreground="#16786b")
        for name, title, width in [("time", "Time", 95), ("event", "Event", 270), ("detail", "Evidence", 570)]:
            self.event_view.heading(name, text=title)
            self.event_view.column(name, width=width, minwidth=70, stretch=name != "time")
        self.event_view.pack(side="left", fill="both", expand=True)
        event_scroll = ttk.Scrollbar(event_frame, orient="vertical", command=self.event_view.yview)
        event_scroll.pack(side="right", fill="y")
        self.event_view.configure(yscrollcommand=event_scroll.set)
        self.event_view.bind("<Double-1>", self.show_event)
        self.log = tk.Text(log_frame, font=("Consolas", 10), bg="#1c2428", fg="#e8eeeb", wrap="word", state="disabled", borderwidth=0, padx=10, pady=10)
        self.log.pack(side="left", fill="both", expand=True)
        log_scroll = ttk.Scrollbar(log_frame, orient="vertical", command=self.log.yview)
        log_scroll.pack(side="right", fill="y")
        self.log.configure(yscrollcommand=log_scroll.set)
        footer = ttk.Frame(main)
        footer.pack(fill="x", pady=(12, 0))
        ttk.Checkbutton(footer, text="Follow log", variable=self.follow).pack(side="left")
        ttk.Button(footer, text="Replay Example", command=self.replay).pack(side="left", padx=10)
        ttk.Button(footer, text="Open Source", command=self.open_source).pack(side="right")
        ttk.Button(footer, text="Export Events", command=self.export).pack(side="right", padx=8)

    def set_status(self, status: str, detail: str = "") -> None:
        self.status.set(status)
        if detail:
            self.detail.set(detail)
        color = COLORS.get(status, COLORS["Stopped"])
        for widget in [self.banner, self.status_label, self.detail_label]:
            widget.configure(background=color)

    def prepare(self) -> bool:
        if self.active:
            return False
        try:
            count = int(self.retry_count.get())
            span = int(self.retry_seconds.get())
            self.stall_limit = int(self.stall_seconds.get())
            if not 2 <= count <= 100 or not 10 <= span <= 3600 or not 30 <= self.stall_limit <= 86400:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid thresholds", "Retry count: 2-100; retry span: 10-3600 seconds; no output: 30-86400 seconds.", parent=self.root)
            return False
        self.detector = Detector(count, span)
        self.update_progress()
        self.messages = queue.Queue(maxsize=4000)
        self.stop_event = threading.Event()
        self.events.clear()
        self.pending_log.clear()
        self.event_view.delete(*self.event_view.get_children())
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")
        self.started = self.last_output = time.monotonic()
        self.ended = 0
        self.lost_since = 0
        self.connection_alerted = self.stall_alerted = False
        self.acknowledge()
        self.active = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.url_entry.configure(state="disabled")
        for widget in self.threshold_widgets:
            widget.configure(state="disabled")
        self.source = "connecting"
        self.set_status("Connecting", "Waiting for the live-log source.")
        return True

    def start(self) -> None:
        try:
            endpoint = stream_url(self.url.get())
        except ValueError as error:
            messagebox.showerror("Invalid URL", str(error), parent=self.root)
            return
        if self.prepare():
            StreamWorker(endpoint, self.messages, self.stop_event).start()

    def replay(self) -> None:
        if not self.prepare():
            return
        self.source = "example replay"
        self.set_status("Running", "Example replay; not a live job.")
        path = Path(__file__).parent / "Examples" / "ExampleLiveLog.txt"
        self.replay_lines = iter(path.read_text(encoding="utf-8").splitlines())
        self.root.after(10, self.replay_step)

    def replay_step(self) -> None:
        if not self.active or self.source != "example replay":
            return
        for _ in range(25):
            line = next(self.replay_lines, None)
            if line is None:
                self.flush_log()
                self.record(Event("Needs Attention", "Example replay finished", "The example is incomplete; no final job result was found."))
                self.stop(preserve=True)
                return
            self.process_line(line)
        self.flush_log()
        self.root.after(40, self.replay_step)

    def process_line(self, line: str) -> None:
        self.last_output = time.monotonic()
        self.stall_alerted = False
        self.pending_log.append(redact(line))
        for event in self.detector.consume(line, time.time()):
            self.record(event)
        self.update_progress()
        if self.detector.terminal:
            self.stop(preserve=True)

    def update_progress(self) -> None:
        detector = self.detector
        current = "--"
        if detector.iteration is not None:
            number = detector.iteration + 1 if detector.iteration_base == 0 else detector.iteration
            total = f" / {detector.iteration_total}" if detector.iteration_total is not None else ""
            current = f"{number}{total} (log #{detector.iteration})"
        average = "--"
        if detector.average_iteration_seconds is not None:
            minutes, seconds = divmod(round(detector.average_iteration_seconds), 60)
            average = f"{minutes}m {seconds:02d}s ({detector.iteration_samples} measured)"
        remaining = "--"
        if detector.estimated_remaining_seconds is not None:
            hours, remainder = divmod(round(detector.estimated_remaining_seconds), 3600)
            minutes, seconds = divmod(remainder, 60)
            remaining = f"{hours}h {minutes:02d}m {seconds:02d}s" if hours else f"{minutes}m {seconds:02d}s"
        self.progress.set(f"Iteration {current}   |   Avg / iteration {average}   |   Est. remaining {remaining}")

    def flush_log(self) -> None:
        if not self.pending_log:
            return
        self.log.configure(state="normal")
        self.log.insert("end", "\n".join(self.pending_log) + "\n")
        self.pending_log.clear()
        line_count = int(self.log.index("end-1c").split(".")[0])
        if line_count > 5001:
            self.log.delete("1.0", f"{line_count - 5000}.0")
        self.log.configure(state="disabled")
        if self.follow.get():
            self.log.see("end")

    def record(self, event: Event) -> None:
        if event.alert or self.detector.terminal or (not self.unacknowledged and event.status == "Needs Attention" and event.kind not in {"success", "progress"}):
            self.set_status(event.status, event.detail)
        stamp = datetime.now().strftime("%H:%M:%S")
        kind = "success" if event.status == "Completed Successfully" else event.kind
        self.events.append({"time": stamp, "status": event.status, "title": event.title, "detail": redact(event.detail), "kind": kind})
        item = self.event_view.insert("", "end", values=(stamp, event.title, redact(event.detail)), tags=(kind,))
        children = self.event_view.get_children()
        if len(children) > 1000:
            self.event_view.delete(children[0])
        self.event_view.see(item)
        if event.alert:
            self.unacknowledged = True
            self.last_sound = 0
            self.ack_button.configure(state="normal")
            if self.focus.get():
                self.root.deiconify()
                self.root.lift()
                self.root.attributes("-topmost", True)
            if self.toasts.get():
                threading.Thread(target=desktop_toast, args=(event.title, redact(event.detail)), daemon=True).start()

    def tick(self) -> None:
        now = time.monotonic()
        if self.active:
            for _ in range(200):
                try:
                    kind, value = self.messages.get_nowait()
                except queue.Empty:
                    break
                if kind == "line":
                    self.process_line(value)
                elif kind == "connected":
                    self.source = "connected"
                    self.lost_since = 0
                    self.connection_alerted = False
                    if not self.detector.terminal and not self.unacknowledged:
                        self.set_status(self.detector.status, "Receiving the live stream.")
                elif kind == "source_error":
                    self.record(Event("Connection Lost / Status Unknown", "Source changed or invalid", value, True))
                    self.stop(preserve=True)
                elif kind == "disconnected":
                    self.source = "reconnecting"
                    if not self.lost_since:
                        self.lost_since = now
                    self.set_status("Connection Lost / Status Unknown", value)
                elif kind == "retry":
                    self.source = "checking idle source"
                if not self.active:
                    break
            if self.active and self.lost_since and now - self.lost_since >= 15 and not self.connection_alerted:
                self.connection_alerted = True
                self.record(Event("Connection Lost / Status Unknown", "Live-log source unavailable", "No confirmed final result. Reconnecting automatically.", True))
            if self.active and not self.lost_since and now - self.last_output >= self.stall_limit and not self.stall_alerted:
                self.stall_alerted = True
                self.record(Event("Needs Attention", "No recent log output", f"No new output for {self.stall_limit} seconds. The job may be busy or stalled; completion is unconfirmed.", True))
        self.flush_log()
        if self.unacknowledged and self.sound.get() and now - self.last_sound >= 10:
            self.last_sound = now
            try:
                import winsound

                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS | winsound.SND_ASYNC)
            except (ImportError, RuntimeError):
                self.root.bell()
        elapsed = int((self.ended or now) - self.started) if self.started else 0
        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)
        age = f"{int(now - self.last_output)}s ago" if self.last_output else "--"
        self.metrics.set(f"Elapsed {hours:02d}:{minutes:02d}:{seconds:02d}   |   Last output {age}   |   Source: {self.source}")
        self.root.after(100, self.tick)

    def acknowledge(self) -> None:
        self.unacknowledged = False
        self.root.attributes("-topmost", False)
        self.ack_button.configure(state="disabled")

    def stop(self, preserve: bool = False) -> None:
        self.stop_event.set()
        self.ended = time.monotonic()
        self.active = False
        self.source = "stopped"
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.url_entry.configure(state="normal")
        for widget in self.threshold_widgets:
            widget.configure(state="normal")
        if not preserve:
            self.set_status("Stopped", "Monitoring stopped. The remote job was not changed.")

    def show_event(self, _event=None) -> None:
        selection = self.event_view.selection()
        if selection:
            values = self.event_view.item(selection[0], "values")
            messagebox.showinfo(values[1], values[2], parent=self.root)

    def open_source(self) -> None:
        try:
            stream_url(self.url.get())
        except ValueError:
            return
        webbrowser.open(self.url.get())

    def export(self) -> None:
        name = filedialog.asksaveasfilename(parent=self.root, defaultextension=".json", filetypes=[("JSON events", "*.json")], initialfile="zeta_job_events.json")
        if name:
            try:
                Path(name).write_text(json.dumps(list(self.events), indent=2), encoding="utf-8")
            except OSError as error:
                messagebox.showerror("Export failed", str(error), parent=self.root)

    def close(self) -> None:
        if self.active and not messagebox.askyesno("Close monitor?", "The remote job will continue, but notifications will stop.", parent=self.root):
            return
        self.stop_event.set()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    AlarmApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()