#!/usr/bin/env python3
"""DSA Log Filter — GUI Application
Drop a DSA log file onto the window to filter and view camera DTC entries.
"""

import re
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from pathlib import Path

# ── Filter logic ──────────────────────────────────────────────────────────────
REQUEST_START_RE = re.compile(r"^#\s*Sending Request:\s*Tester\s*->", re.IGNORECASE)

IS_READ_DTC_HINTS = (
    re.compile(r"\bRead\s+DTC\s+Information\b", re.IGNORECASE),
    re.compile(r"\bReport\s+DTC\b", re.IGNORECASE),
    re.compile(r"\b19\s+0[0-9A-Fa-f]\b"),
)

CAMERA_PREFIX_SET = {
    "D4D5",  # FLCW
    "D50A",  # SRCF
    "D50B",  # SRCL
    "D50C",  # SRCR
    "D509",  # SRCB
    "D4EE",  # LRBL
    "D4EF",  # LRBR
    "D606",  # LRIL
    "D607",  # LRIR
}

DTC_HEAD_RE   = re.compile(r"^\s*([A-F0-9]{4,8})\s+\t?\t?.*")
DTC_STATUS_RE = re.compile(r"^\s{1,}(0[1-9]|20|80)\s+.*")


def _is_dtc_header(line):
    m = DTC_HEAD_RE.match(line)
    return (True, m.group(1).strip()) if m else (False, None)


def _is_camera_dtc_code(code):
    return bool(code and len(code) >= 4 and code[:4] in CAMERA_PREFIX_SET)


def _block_is_read_dtc(block_lines):
    chunk = "\n".join(block_lines[:10])
    return any(p.search(chunk) for p in IS_READ_DTC_HINTS)


def _append_blank_line_once(dst):
    if dst and dst[-1].strip() != "":
        dst.append("")


def filter_log(input_path):
    text  = input_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    out   = []
    i, n  = 0, len(lines)

    while i < n:
        line = lines[i]
        if REQUEST_START_RE.match(line):
            block = [line]; i += 1
            while i < n and not REQUEST_START_RE.match(lines[i]):
                block.append(lines[i]); i += 1
            if _block_is_read_dtc(block):
                j, fb = 0, []
                while j < len(block):
                    L = block[j]
                    is_hdr, code = _is_dtc_header(L)
                    if is_hdr:
                        if _is_camera_dtc_code(code):
                            fb.append(L); k = j + 1
                            while k < len(block) and DTC_STATUS_RE.match(block[k]):
                                fb.append(block[k]); k += 1
                            _append_blank_line_once(fb); j = k
                        else:
                            k = j + 1
                            while k < len(block) and DTC_STATUS_RE.match(block[k]):
                                k += 1
                            j = k
                    else:
                        fb.append(L); j += 1
                out.extend(fb)
            else:
                out.extend(block)
            continue
        out.append(line)
        i += 1

    return "\n".join(out).rstrip() + "\n"


# ── GUI ───────────────────────────────────────────────────────────────────────
_BG_IDLE = "#dce8fc"; _FG_IDLE = "#1a56db"
_BG_DONE = "#d4edda"; _FG_DONE = "#155724"

_HAS_DND   = False
_DND_FILES = None


class DSAFilterApp:
    def __init__(self, root):
        self.root              = root
        self._filtered_content = None
        self._current_path     = None

        root.title("DSA Log Filter")
        root.geometry("1050x760")
        root.minsize(700, 500)
        root.configure(bg="#f4f4f4")

        self._build_ui()

        if _HAS_DND:
            self._drop_zone.drop_target_register(_DND_FILES)
            self._drop_zone.dnd_bind("<<Drop>>", self._on_drop)

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",           padding=6,  font=("Segoe UI", 10))
        style.configure("TLabelframe.Label",             font=("Segoe UI", 10, "bold"))
        style.configure("Status.TLabel",                 font=("Segoe UI", 9), foreground="#555")

        input_frame = ttk.LabelFrame(self.root, text="Input File")
        input_frame.pack(fill=tk.X, padx=14, pady=(14, 6))

        drop_text = "Drop DSA log file here" if _HAS_DND else "Use Browse button to open file"
        self._drop_zone = tk.Label(
            input_frame, text=drop_text,
            bg=_BG_IDLE, fg=_FG_IDLE,
            font=("Segoe UI", 13), relief="groove", bd=2, pady=26,
        )
        self._drop_zone.pack(fill=tk.X, padx=10, pady=(8, 4))

        btn_row = ttk.Frame(input_frame)
        btn_row.pack(fill=tk.X, padx=10, pady=(4, 10))

        ttk.Button(btn_row, text="Browse\u2026", width=12, command=self._browse).pack(side=tk.LEFT)

        self._save_btn = ttk.Button(
            btn_row, text="Save filtered file", width=20,
            command=self._save, state=tk.DISABLED,
        )
        self._save_btn.pack(side=tk.RIGHT)

        self._status_var = tk.StringVar(value="No file loaded.")
        ttk.Label(btn_row, textvariable=self._status_var, style="Status.TLabel").pack(
            side=tk.LEFT, padx=12
        )

        out_frame = ttk.LabelFrame(self.root, text="Filtered Output")
        out_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=(4, 14))

        self._text = ScrolledText(
            out_frame, wrap=tk.WORD, font=("Consolas", 10),
            bg="white", fg="#1a1a1a", insertbackground="#1a1a1a",
            relief="flat", borderwidth=0,
        )
        self._text.pack(fill=tk.BOTH, expand=True, padx=6, pady=(6, 6))

        # Allow selection/copy (Ctrl+anything passes through), block edits.
        def _guard_edits(event):
            if event.state & 0x4:
                return None
            if len(event.char) == 1 or event.keysym in (
                "BackSpace", "Delete", "Return", "Tab"
            ):
                return "break"
        self._text.bind("<Key>", _guard_edits)

    def _on_drop(self, event):
        raw = event.data.strip()
        if raw.startswith("{") and raw.endswith("}"):
            raw = raw[1:-1]
        self._load(Path(raw))

    def _browse(self):
        p = filedialog.askopenfilename(
            title="Select DSA Log File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if p:
            self._load(Path(p))

    def _load(self, path):
        if not path.exists():
            messagebox.showerror("File not found", "Could not find:\n{}".format(path))
            return
        try:
            self._status_var.set("Processing: {} \u2026".format(path.name))
            self.root.update_idletasks()
            content = filter_log(path)
            self._filtered_content = content
            self._current_path     = path
            self._text.delete("1.0", tk.END)
            self._text.insert("1.0", content)
            self._status_var.set("Loaded: {}".format(path.name))
            self._save_btn.config(state=tk.NORMAL)
            self._drop_zone.config(
                text="\u2714  {}  \u2014  drop another file to replace".format(path.name),
                bg=_BG_DONE, fg=_FG_DONE,
            )
        except Exception as exc:
            messagebox.showerror("Processing error", str(exc))
            self._status_var.set("Error \u2014 see message.")

    def _save(self):
        if not self._filtered_content or not self._current_path:
            return
        out = self._current_path.with_name(self._current_path.stem + "_filtered.txt")
        out.write_text(self._filtered_content, encoding="utf-8")
        messagebox.showinfo("Saved", "Saved to:\n{}".format(out))


# ── Splash ────────────────────────────────────────────────────────────────────
def _show_splash(root):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.attributes("-topmost", True)
    splash.configure(bg="#1a2540")

    outer = tk.Frame(splash, bg="#0d1526", padx=3, pady=3)
    outer.pack()
    inner = tk.Frame(outer, bg="#1a2540", padx=40, pady=34)
    inner.pack()

    tk.Label(inner, text="DSA Log Filter",
             font=("Segoe UI", 22, "bold"), bg="#1a2540", fg="white").pack()
    tk.Label(inner, text="Camera DTC log viewer",
             font=("Segoe UI", 11), bg="#1a2540", fg="#8aafd4").pack(pady=(4, 0))

    ttk.Separator(inner, orient="horizontal").pack(fill=tk.X, pady=18)

    tk.Label(
        inner,
        text=(
            "First launch only: the app is unpacking itself in the background.\n"
            "This takes a few seconds once \u2014 every launch after this is near-instant."
        ),
        font=("Segoe UI", 9), bg="#1a2540", fg="#a0bcd8",
        justify="center", wraplength=380,
    ).pack()

    tk.Label(inner, text="Starting up\u2026",
             font=("Segoe UI", 9, "italic"), bg="#1a2540", fg="#5a7fa8").pack(pady=(16, 0))

    splash.update_idletasks()
    w  = splash.winfo_width()
    h  = splash.winfo_height()
    sw = splash.winfo_screenwidth()
    sh = splash.winfo_screenheight()
    splash.geometry("+{}+{}".format((sw - w) // 2, (sh - h) // 2))
    splash.update()
    return splash


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    global _HAS_DND, _DND_FILES

    # Show splash as early as possible once Python starts.
    root = tk.Tk()
    root.withdraw()
    splash = _show_splash(root)

    # Load tkinterdnd2 while splash is visible.
    try:
        from tkinterdnd2 import TkinterDnD, DND_FILES
        TkinterDnD._require(root)
        _HAS_DND   = True
        _DND_FILES = DND_FILES
    except Exception:
        pass

    # Build main UI, then hand off.
    app = DSAFilterApp(root)
    splash.destroy()
    root.deiconify()
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    root.mainloop()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""DSA Log Filter — GUI Application
Drop a DSA log file onto the window to filter and view camera DTC entries.
"""

import re
import sys
import ctypes
import ctypes.wintypes as wintypes
import threading
from pathlib import Path

# tkinter symbols are populated by _import_gui() inside main() so that the
# native Win32 splash can appear before the slow Tcl/Tk DLLs are loaded.
# Method bodies reference these as globals (looked up at call time, not at
# class-definition time), so deferred assignment is safe.
tk           = None
ttk          = None
filedialog   = None
messagebox   = None
ScrolledText = None

_HAS_DND   = False
_DND_FILES = None

_BG_IDLE = "#dce8fc"; _FG_IDLE = "#1a56db"
_BG_DONE = "#d4edda"; _FG_DONE = "#155724"

# ── Filter logic ──────────────────────────────────────────────────────────────
REQUEST_START_RE = re.compile(r"^#\s*Sending Request:\s*Tester\s*->", re.IGNORECASE)

IS_READ_DTC_HINTS = (
    re.compile(r"\bRead\s+DTC\s+Information\b", re.IGNORECASE),
    re.compile(r"\bReport\s+DTC\b", re.IGNORECASE),
    re.compile(r"\b19\s+0[0-9A-Fa-f]\b"),
)

CAMERA_PREFIX_SET = {
    "D4D5",  # FLCW
    "D50A",  # SRCF
    "D50B",  # SRCL
    "D50C",  # SRCR
    "D509",  # SRCB
    "D4EE",  # LRBL
    "D4EF",  # LRBR
    "D606",  # LRIL
    "D607",  # LRIR
}

DTC_HEAD_RE   = re.compile(r"^\s*([A-F0-9]{4,8})\s+\t?\t?.*")
DTC_STATUS_RE = re.compile(r"^\s{1,}(0[1-9]|20|80)\s+.*")


def _is_dtc_header(line):
    m = DTC_HEAD_RE.match(line)
    return (True, m.group(1).strip()) if m else (False, None)


def _is_camera_dtc_code(code):
    return bool(code and len(code) >= 4 and code[:4] in CAMERA_PREFIX_SET)


def _block_is_read_dtc(block_lines):
    chunk = "\n".join(block_lines[:10])
    return any(p.search(chunk) for p in IS_READ_DTC_HINTS)


def _append_blank_line_once(dst):
    if dst and dst[-1].strip() != "":
        dst.append("")


def filter_log(input_path):
    text  = input_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    out   = []
    i, n  = 0, len(lines)

    while i < n:
        line = lines[i]
        if REQUEST_START_RE.match(line):
            block = [line]; i += 1
            while i < n and not REQUEST_START_RE.match(lines[i]):
                block.append(lines[i]); i += 1

            if _block_is_read_dtc(block):
                j, fb = 0, []
                while j < len(block):
                    L = block[j]
                    is_hdr, code = _is_dtc_header(L)
                    if is_hdr:
                        if _is_camera_dtc_code(code):
                            fb.append(L); k = j + 1
                            while k < len(block) and DTC_STATUS_RE.match(block[k]):
                                fb.append(block[k]); k += 1
                            _append_blank_line_once(fb); j = k
                        else:
                            k = j + 1
                            while k < len(block) and DTC_STATUS_RE.match(block[k]):
                                k += 1
                            j = k
                    else:
                        fb.append(L); j += 1
                out.extend(fb)
            else:
                out.extend(block)
            continue

        out.append(line)
        i += 1

    return "\n".join(out).rstrip() + "\n"


# ── GUI class ─────────────────────────────────────────────────────────────────
class DSAFilterApp:
    def __init__(self, root):
        self.root              = root
        self._filtered_content = None
        self._current_path     = None

        root.title("DSA Log Filter")
        root.geometry("1050x760")
        root.minsize(700, 500)
        root.configure(bg="#f4f4f4")

        self._build_ui()

        if _HAS_DND:
            self._drop_zone.drop_target_register(_DND_FILES)
            self._drop_zone.dnd_bind("<<Drop>>", self._on_drop)

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",           padding=6,  font=("Segoe UI", 10))
        style.configure("TLabelframe.Label",             font=("Segoe UI", 10, "bold"))
        style.configure("Status.TLabel",                 font=("Segoe UI", 9), foreground="#555")

        input_frame = ttk.LabelFrame(self.root, text="Input File")
        input_frame.pack(fill=tk.X, padx=14, pady=(14, 6))

        drop_text = "Drop DSA log file here" if _HAS_DND else "Use Browse button to open file"
        self._drop_zone = tk.Label(
            input_frame, text=drop_text,
            bg=_BG_IDLE, fg=_FG_IDLE,
            font=("Segoe UI", 13), relief="groove", bd=2, pady=26,
        )
        self._drop_zone.pack(fill=tk.X, padx=10, pady=(8, 4))

        btn_row = ttk.Frame(input_frame)
        btn_row.pack(fill=tk.X, padx=10, pady=(4, 10))

        ttk.Button(btn_row, text="Browse\u2026", width=12, command=self._browse).pack(side=tk.LEFT)

        self._save_btn = ttk.Button(
            btn_row, text="Save filtered file", width=20,
            command=self._save, state=tk.DISABLED,
        )
        self._save_btn.pack(side=tk.RIGHT)

        self._status_var = tk.StringVar(value="No file loaded.")
        ttk.Label(btn_row, textvariable=self._status_var, style="Status.TLabel").pack(
            side=tk.LEFT, padx=12
        )

        out_frame = ttk.LabelFrame(self.root, text="Filtered Output")
        out_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=(4, 14))

        self._text = ScrolledText(
            out_frame, wrap=tk.WORD, font=("Consolas", 10),
            bg="white", fg="#1a1a1a", insertbackground="#1a1a1a",
            relief="flat", borderwidth=0,
        )
        self._text.pack(fill=tk.BOTH, expand=True, padx=6, pady=(6, 6))

        # Keep widget NORMAL so Ctrl+C / selection work freely.
        # Block editing keys but allow any Ctrl+key combo.
        def _guard_edits(event):
            if event.state & 0x4:
                return None
            if len(event.char) == 1 or event.keysym in (
                "BackSpace", "Delete", "Return", "Tab"
            ):
                return "break"
        self._text.bind("<Key>", _guard_edits)

    def _on_drop(self, event):
        raw = event.data.strip()
        if raw.startswith("{") and raw.endswith("}"):
            raw = raw[1:-1]
        self._load(Path(raw))

    def _browse(self):
        p = filedialog.askopenfilename(
            title="Select DSA Log File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if p:
            self._load(Path(p))

    def _load(self, path):
        if not path.exists():
            messagebox.showerror("File not found", "Could not find:\n{}".format(path))
            return
        try:
            self._status_var.set("Processing: {} \u2026".format(path.name))
            self.root.update_idletasks()
            content = filter_log(path)
            self._filtered_content = content
            self._current_path     = path
            self._text.delete("1.0", tk.END)
            self._text.insert("1.0", content)
            self._status_var.set("Loaded: {}".format(path.name))
            self._save_btn.config(state=tk.NORMAL)
            self._drop_zone.config(
                text="\u2714  {}  \u2014  drop another file to replace".format(path.name),
                bg=_BG_DONE, fg=_FG_DONE,
            )
        except Exception as exc:
            messagebox.showerror("Processing error", str(exc))
            self._status_var.set("Error \u2014 see message.")

    def _save(self):
        if not self._filtered_content or not self._current_path:
            return
        out = self._current_path.with_name(self._current_path.stem + "_filtered.txt")
        out.write_text(self._filtered_content, encoding="utf-8")
        messagebox.showinfo("Saved", "Saved to:\n{}".format(out))


# ── Native Win32 splash (appears before Python/Tk DLLs load) ─────────────────
def _native_splash_start():
    """Create a borderless Win32 window in a background thread using only
    ctypes — no extra DLL loading required, appears in under 100 ms.
    Returns a stop() callable."""
    if sys.platform != "win32":
        return lambda: None

    u32 = ctypes.windll.user32
    g32 = ctypes.windll.gdi32
    k32 = ctypes.windll.kernel32

    # Set critical restypes to avoid 64-bit truncation
    g32.CreateSolidBrush.restype  = wintypes.HBRUSH
    g32.CreateFontW.restype       = wintypes.HANDLE
    g32.SelectObject.restype      = wintypes.HANDLE
    u32.BeginPaint.restype        = wintypes.HDC
    u32.CreateWindowExW.restype   = wintypes.HWND
    k32.GetModuleHandleW.restype  = wintypes.HMODULE

    WM_PAINT   = 0x000F
    WM_CLOSE   = 0x0010
    WM_DESTROY = 0x0002
    WS_POPUP   = 0x80000000
    WS_VISIBLE = 0x10000000
    WS_EX_TOPMOST    = 0x00000008
    WS_EX_TOOLWINDOW = 0x00000080
    TRANSPARENT      = 1
    DT_CENTER     = 0x0001
    DT_VCENTER    = 0x0004
    DT_SINGLELINE = 0x0020

    # Colors: COLORREF is 0x00BBGGRR
    C_BG     = 0x40251A   # #1A2540
    C_ACCENT = 0xDB561A   # #1A56DB
    C_WHITE  = 0xFFFFFF
    C_MUTED  = 0xD8BCA0   # #A0BCD8

    W, H = 480, 160
    sw = u32.GetSystemMetrics(0)
    sh = u32.GetSystemMetrics(1)
    x  = (sw - W) // 2
    y  = (sh - H) // 2

    WNDPROC_T = ctypes.WINFUNCTYPE(
        ctypes.c_ssize_t,
        wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM,
    )

    class PAINTSTRUCT(ctypes.Structure):
        _fields_ = [
            ("hdc",        wintypes.HDC),
            ("fErase",     wintypes.BOOL),
            ("rcPaint",    wintypes.RECT),
            ("fRestore",   wintypes.BOOL),
            ("fIncUpdate", wintypes.BOOL),
            ("reserved",   ctypes.c_byte * 32),
        ]

    class WNDCLASSEXW(ctypes.Structure):
        _fields_ = [
            ("cbSize",        ctypes.c_uint),
            ("style",         ctypes.c_uint),
            ("lpfnWndProc",   WNDPROC_T),
            ("cbClsExtra",    ctypes.c_int),
            ("cbWndExtra",    ctypes.c_int),
            ("hInstance",     wintypes.HMODULE),
            ("hIcon",         wintypes.HANDLE),
            ("hCursor",       wintypes.HANDLE),
            ("hbrBackground", wintypes.HBRUSH),
            ("lpszMenuName",  wintypes.LPCWSTR),
            ("lpszClassName", wintypes.LPCWSTR),
            ("hIconSm",       wintypes.HANDLE),
        ]

    class MSG(ctypes.Structure):
        _fields_ = [
            ("hwnd",    wintypes.HWND),
            ("message", wintypes.UINT),
            ("wParam",  wintypes.WPARAM),
            ("lParam",  wintypes.LPARAM),
            ("time",    wintypes.DWORD),
            ("pt",      wintypes.POINT),
        ]

    hwnd_holder = [None]
    ready       = threading.Event()

    def _fill(hdc, l, t, r, b, color):
        rc  = wintypes.RECT(l, t, r, b)
        hbr = g32.CreateSolidBrush(color)
        u32.FillRect(hdc, ctypes.byref(rc), hbr)
        g32.DeleteObject(hbr)

    def _text(hdc, txt, l, t, r, b, color, size, bold=False):
        g32.SetBkMode(hdc, TRANSPARENT)
        g32.SetTextColor(hdc, color)
        hf = g32.CreateFontW(
            size, 0, 0, 0, 700 if bold else 400,
            0, 0, 0, 0, 0, 0, 5, 0, "Segoe UI"
        )
        old = g32.SelectObject(hdc, hf)
        rc  = wintypes.RECT(l, t, r, b)
        u32.DrawTextW(hdc, txt, -1, ctypes.byref(rc), DT_CENTER | DT_VCENTER | DT_SINGLELINE)
        g32.SelectObject(hdc, old)
        g32.DeleteObject(hf)

    def _wndproc(hwnd, msg, wp, lp):
        if msg == WM_PAINT:
            ps  = PAINTSTRUCT()
            hdc = u32.BeginPaint(hwnd, ctypes.byref(ps))
            _fill(hdc, 0,   0,   W,   H,   C_BG)
            _fill(hdc, 0,   0,   W,   5,   C_ACCENT)
            _fill(hdc, 0,   H-5, W,   H,   C_ACCENT)
            _text(hdc, "DSA Log Filter",          0, 20,  W, 80,  C_WHITE, 26, bold=True)
            _text(hdc, "Starting up\u2026",        0, 90,  W, 130, C_MUTED, 13)
            u32.EndPaint(hwnd, ctypes.byref(ps))
            return 0
        if msg == WM_DESTROY:
            u32.PostQuitMessage(0)
            return 0
        return u32.DefWindowProcW(hwnd, msg, wp, lp)

    _proc_cb = WNDPROC_T(_wndproc)
    _keepers  = [_proc_cb]   # prevent GC of the ctypes callback

    def _thread():
        hInst  = k32.GetModuleHandleW(None)
        cls_nm = "DSAFilterSplash"

        wc             = WNDCLASSEXW()
        wc.cbSize      = ctypes.sizeof(WNDCLASSEXW)
        wc.lpfnWndProc = _proc_cb
        wc.hInstance   = hInst
        wc.lpszClassName = cls_nm
        wc.hCursor     = u32.LoadCursorW(None, 32512)  # IDC_ARROW
        u32.RegisterClassExW(ctypes.byref(wc))

        hwnd = u32.CreateWindowExW(
            WS_EX_TOPMOST | WS_EX_TOOLWINDOW,
            cls_nm, "",
            WS_POPUP | WS_VISIBLE,
            x, y, W, H,
            None, None, hInst, None,
        )
        hwnd_holder[0] = hwnd
        u32.UpdateWindow(hwnd)
        ready.set()

        msg = MSG()
        while u32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            u32.TranslateMessage(ctypes.byref(msg))
            u32.DispatchMessageW(ctypes.byref(msg))

        _keepers.clear()

    t = threading.Thread(target=_thread, daemon=True)
    t.start()
    ready.wait(timeout=1.0)

    def stop():
        hwnd = hwnd_holder[0]
        if hwnd:
            u32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
            hwnd_holder[0] = None

    return stop


# ── Tkinter splash (shown after Tk is ready, native splash closes first) ──────
def _show_splash(root):
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    splash.attributes("-topmost", True)
    splash.configure(bg="#1a2540")

    outer = tk.Frame(splash, bg="#0d1526", padx=3, pady=3)
    outer.pack()
    inner = tk.Frame(outer, bg="#1a2540", padx=40, pady=34)
    inner.pack()

    tk.Label(inner, text="DSA Log Filter", font=("Segoe UI", 22, "bold"),
             bg="#1a2540", fg="white").pack()
    tk.Label(inner, text="Camera DTC log viewer",
             font=("Segoe UI", 11), bg="#1a2540", fg="#8aafd4").pack(pady=(4, 0))

    ttk.Separator(inner, orient="horizontal").pack(fill=tk.X, pady=18)

    is_frozen = getattr(sys, "frozen", False)
    note = (
        "First launch?  Windows is setting up the app in the background.\n"
        "This takes a few seconds once \u2014 every launch after is instant."
        if is_frozen else "Running from source."
    )
    tk.Label(inner, text=note, font=("Segoe UI", 9), bg="#1a2540",
             fg="#a0bcd8", justify="center", wraplength=380).pack()

    tk.Label(inner, text="Almost ready\u2026", font=("Segoe UI", 9, "italic"),
             bg="#1a2540", fg="#5a7fa8").pack(pady=(16, 0))

    splash.update_idletasks()
    w  = splash.winfo_width()
    h  = splash.winfo_height()
    sw = splash.winfo_screenwidth()
    sh = splash.winfo_screenheight()
    splash.geometry("+{}+{}".format((sw - w) // 2, (sh - h) // 2))
    splash.update()
    return splash


# ── Deferred tkinter import ───────────────────────────────────────────────────
def _import_gui():
    """Import tkinter and set module-level globals. Called while the native
    splash is visible so the user sees something during this slow step."""
    global tk, ttk, filedialog, messagebox, ScrolledText
    import tkinter as _tk
    from tkinter import ttk as _ttk
    from tkinter import filedialog as _fd, messagebox as _mb
    from tkinter.scrolledtext import ScrolledText as _ST
    tk           = _tk
    ttk          = _ttk
    filedialog   = _fd
    messagebox   = _mb
    ScrolledText = _ST


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    global _HAS_DND, _DND_FILES

    # 1. Native Win32 splash — appears instantly (no Tk needed, ctypes only)
    stop_native = _native_splash_start()

    # 2. Import tkinter (loads tcl90.dll / tk90.dll) — slow, native splash visible
    _import_gui()

    # 3. Create Tk root (hidden)
    root = tk.Tk()
    root.withdraw()

    # 4. Load tkinterdnd2 into the existing root (while native splash still up)
    try:
        from tkinterdnd2 import TkinterDnD, DND_FILES
        TkinterDnD._require(root)
        _HAS_DND   = True
        _DND_FILES = DND_FILES
    except Exception:
        pass

    # 5. Show Tkinter splash, close native splash
    splash = _show_splash(root)
    stop_native()

    # 6. Build the main UI
    app = DSAFilterApp(root)

    # 7. Hand off to main window
    splash.destroy()
    root.deiconify()
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    root.mainloop()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""DSA Log Filter — GUI Application
Drop a DSA log file onto the window to filter and view camera DTC entries.
"""

import re
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from pathlib import Path

# tkinterdnd2 is loaded lazily inside main() so the splash can appear first.
# These module-level flags are set before DSAFilterApp is instantiated.
_HAS_DND   = False
_DND_FILES = None

# ── Filter logic ──────────────────────────────────────────────────────────────
REQUEST_START_RE = re.compile(r"^#\s*Sending Request:\s*Tester\s*->", re.IGNORECASE)

IS_READ_DTC_HINTS = (
    re.compile(r"\bRead\s+DTC\s+Information\b", re.IGNORECASE),
    re.compile(r"\bReport\s+DTC\b", re.IGNORECASE),
    re.compile(r"\b19\s+0[0-9A-Fa-f]\b"),
)

CAMERA_PREFIX_SET = {
    "D4D5",  # FLCW
    "D50A",  # SRCF
    "D50B",  # SRCL
    "D50C",  # SRCR
    "D509",  # SRCB
    "D4EE",  # LRBL
    "D4EF",  # LRBR
    "D606",  # LRIL
    "D607",  # LRIR
}

DTC_HEAD_RE   = re.compile(r"^\s*([A-F0-9]{4,8})\s+\t?\t?.*")
DTC_STATUS_RE = re.compile(r"^\s{1,}(0[1-9]|20|80)\s+.*")


def _is_dtc_header(line):
    m = DTC_HEAD_RE.match(line)
    return (True, m.group(1).strip()) if m else (False, None)


def _is_camera_dtc_code(code):
    return bool(code and len(code) >= 4 and code[:4] in CAMERA_PREFIX_SET)


def _block_is_read_dtc(block_lines):
    chunk = "\n".join(block_lines[:10])
    return any(p.search(chunk) for p in IS_READ_DTC_HINTS)


def _append_blank_line_once(dst):
    if dst and dst[-1].strip() != "":
        dst.append("")


def filter_log(input_path):
    text  = input_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    out   = []
    i, n  = 0, len(lines)

    while i < n:
        line = lines[i]
        if REQUEST_START_RE.match(line):
            block = [line]; i += 1
            while i < n and not REQUEST_START_RE.match(lines[i]):
                block.append(lines[i]); i += 1

            if _block_is_read_dtc(block):
                j, fb = 0, []
                while j < len(block):
                    L = block[j]
                    is_hdr, code = _is_dtc_header(L)
                    if is_hdr:
                        if _is_camera_dtc_code(code):
                            fb.append(L); k = j + 1
                            while k < len(block) and DTC_STATUS_RE.match(block[k]):
                                fb.append(block[k]); k += 1
                            _append_blank_line_once(fb); j = k
                        else:
                            k = j + 1
                            while k < len(block) and DTC_STATUS_RE.match(block[k]):
                                k += 1
                            j = k
                    else:
                        fb.append(L); j += 1
                out.extend(fb)
            else:
                out.extend(block)
            continue

        out.append(line)
        i += 1

    return "\n".join(out).rstrip() + "\n"


# ── GUI ───────────────────────────────────────────────────────────────────────
_BG_IDLE  = "#dce8fc"; _FG_IDLE  = "#1a56db"
_BG_DONE  = "#d4edda"; _FG_DONE  = "#155724"


class DSAFilterApp:
    def __init__(self, root):
        self.root              = root
        self._filtered_content = None
        self._current_path     = None

        root.title("DSA Log Filter")
        root.geometry("1050x760")
        root.minsize(700, 500)
        root.configure(bg="#f4f4f4")

        self._build_ui()

        if _HAS_DND:
            self._drop_zone.drop_target_register(_DND_FILES)
            self._drop_zone.dnd_bind("<<Drop>>", self._on_drop)

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",           padding=6,  font=("Segoe UI", 10))
        style.configure("TLabelframe.Label",             font=("Segoe UI", 10, "bold"))
        style.configure("Status.TLabel",                 font=("Segoe UI", 9), foreground="#555")

        input_frame = ttk.LabelFrame(self.root, text="Input File")
        input_frame.pack(fill=tk.X, padx=14, pady=(14, 6))

        drop_text = "Drop DSA log file here" if _HAS_DND else "Use Browse button to open file"
        self._drop_zone = tk.Label(
            input_frame, text=drop_text,
            bg=_BG_IDLE, fg=_FG_IDLE,
            font=("Segoe UI", 13), relief="groove", bd=2, pady=26,
        )
        self._drop_zone.pack(fill=tk.X, padx=10, pady=(8, 4))

        btn_row = ttk.Frame(input_frame)
        btn_row.pack(fill=tk.X, padx=10, pady=(4, 10))

        ttk.Button(btn_row, text="Browse…", width=12, command=self._browse).pack(side=tk.LEFT)

        self._save_btn = ttk.Button(
            btn_row, text="Save filtered file", width=20,
            command=self._save, state=tk.DISABLED,
        )
        self._save_btn.pack(side=tk.RIGHT)

        self._status_var = tk.StringVar(value="No file loaded.")
        ttk.Label(btn_row, textvariable=self._status_var, style="Status.TLabel").pack(
            side=tk.LEFT, padx=12
        )

        out_frame = ttk.LabelFrame(self.root, text="Filtered Output")
        out_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=(4, 14))

        self._text = ScrolledText(
            out_frame, wrap=tk.WORD, font=("Consolas", 10),
            bg="white", fg="#1a1a1a", insertbackground="#1a1a1a",
            relief="flat", borderwidth=0,
        )
        self._text.pack(fill=tk.BOTH, expand=True, padx=6, pady=(6, 6))

        # Keep widget NORMAL so Ctrl+C / selection work freely.
        # Only block actual editing keys. Ctrl+anything is always allowed.
        def _guard_edits(event):
            if event.state & 0x4:   # Ctrl held — allow Ctrl+C, Ctrl+A, etc.
                return None
            if len(event.char) == 1 or event.keysym in (
                "BackSpace", "Delete", "Return", "Tab"
            ):
                return "break"
        self._text.bind("<Key>", _guard_edits)

    # ── Callbacks ─────────────────────────────────────────────────────────────
    def _on_drop(self, event):
        raw = event.data.strip()
        # tkinterdnd2 wraps paths with spaces in curly braces
        if raw.startswith("{") and raw.endswith("}"):
            raw = raw[1:-1]
        self._load(Path(raw))

    def _browse(self):
        p = filedialog.askopenfilename(
            title="Select DSA Log File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if p:
            self._load(Path(p))

    def _load(self, path):
        if not path.exists():
            messagebox.showerror("File not found", "Could not find:\n{}".format(path))
            return
        try:
            self._status_var.set("Processing: {} …".format(path.name))
            self.root.update_idletasks()
            content = filter_log(path)
            self._filtered_content = content
            self._current_path     = path
            self._text.delete("1.0", tk.END)
            self._text.insert("1.0", content)
            self._status_var.set("Loaded: {}".format(path.name))
            self._save_btn.config(state=tk.NORMAL)
            self._drop_zone.config(
                text="\u2714  {}  \u2014  drop another file to replace".format(path.name),
                bg=_BG_DONE, fg=_FG_DONE,
            )
        except Exception as exc:
            messagebox.showerror("Processing error", str(exc))
            self._status_var.set("Error — see message.")

    def _save(self):
        if not self._filtered_content or not self._current_path:
            return
        out = self._current_path.with_name(self._current_path.stem + "_filtered.txt")
        out.write_text(self._filtered_content, encoding="utf-8")
        messagebox.showinfo("Saved", "Saved to:\n{}".format(out))


# ── Splash screen ─────────────────────────────────────────────────────────────
def _show_splash(root):
    """Show a borderless splash window centred on screen. Returns the splash."""
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)          # no title bar / border
    splash.attributes("-topmost", True)
    splash.configure(bg="#1a2540")

    # ── Drop-shadow illusion via a slightly larger darker frame ──
    outer = tk.Frame(splash, bg="#0d1526", padx=3, pady=3)
    outer.pack()
    inner = tk.Frame(outer, bg="#1a2540", padx=40, pady=34)
    inner.pack()

    tk.Label(inner, text="DSA Log Filter", font=("Segoe UI", 22, "bold"),
             bg="#1a2540", fg="white").pack()
    tk.Label(inner, text="Camera DTC log viewer",
             font=("Segoe UI", 11), bg="#1a2540", fg="#8aafd4").pack(pady=(4, 0))

    ttk.Separator(inner, orient="horizontal").pack(fill=tk.X, pady=18)

    # Detect first run (Nuitka cache absent means extraction just happened or
    # about to on the next relaunch — show the first-run note regardless so the
    # user is never confused by a slow start.)
    import os, sys
    cache_marker = os.path.join(
        os.environ.get("LOCALAPPDATA", ""), "DSAFilter", "_nuitka_onefile_"
    )
    # A simpler heuristic: check if sys.frozen is set (we're inside Nuitka exe)
    is_frozen = getattr(sys, "frozen", False)

    if is_frozen:
        note = (
            "First launch?  Windows is setting up the app in the background.\n"
            "This takes a few seconds once — every launch after is instant."
        )
    else:
        note = "Running from source."

    tk.Label(inner, text=note, font=("Segoe UI", 9), bg="#1a2540",
             fg="#a0bcd8", justify="center", wraplength=380).pack()

    tk.Label(inner, text="Starting up…", font=("Segoe UI", 9, "italic"),
             bg="#1a2540", fg="#5a7fa8").pack(pady=(16, 0))

    # Centre on screen
    splash.update_idletasks()
    w, h = splash.winfo_width(), splash.winfo_height()
    sw   = splash.winfo_screenwidth()
    sh   = splash.winfo_screenheight()
    splash.geometry("+{}+{}".format((sw - w) // 2, (sh - h) // 2))

    splash.update()
    return splash


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    global _HAS_DND, _DND_FILES

    # 1. Create a plain Tk root and show splash immediately — this is fast
    #    because it doesn't load the tkdnd DLL yet.
    root = tk.Tk()
    root.withdraw()
    splash = _show_splash(root)

    # 2. Load tkinterdnd2 while the splash is visible (this is the slow step).
    try:
        from tkinterdnd2 import TkinterDnD, DND_FILES
        TkinterDnD._require(root)   # adds DnD support to the existing root
        _HAS_DND   = True
        _DND_FILES = DND_FILES
    except Exception:
        pass

    # 3. Build the main UI (fast — Tk is already initialised).
    app = DSAFilterApp(root)

    # 4. Swap splash for main window.
    splash.destroy()
    root.deiconify()
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    root.mainloop()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""DSA Log Filter — GUI Application
Drop a DSA log file onto the window to filter and view camera DTC entries.
"""

import re
import sys
import ctypes
import ctypes.wintypes as wintypes
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from pathlib import Path

# ── Windows native drag-and-drop via ctypes (no external dependencies) ───────
_WIN32     = sys.platform == "win32"
_WNDPROC_T = None
if _WIN32:
    _shell32           = ctypes.windll.shell32
    _user32            = ctypes.windll.user32
    _WM_DROPFILES      = 0x0233
    _WM_COPYGLOBALDATA = 0x0049   # must also be allowed through UIPI
    _MSGFLT_ALLOW      = 1
    _GWL_WNDPROC       = -4

    # Return type must be c_ssize_t (LRESULT) — not LPARAM — so 64-bit values
    # are sign-extended correctly on 64-bit Windows.
    _WNDPROC_T = ctypes.WINFUNCTYPE(
        ctypes.c_ssize_t,
        wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM,
    )

    # Explicitly type the APIs we use so ctypes doesn't guess wrong sizes.
    _shell32.DragAcceptFiles.argtypes = [wintypes.HWND, wintypes.BOOL]
    _shell32.DragQueryFileW.argtypes  = [
        wintypes.HANDLE, wintypes.UINT, wintypes.LPWSTR, wintypes.UINT
    ]
    _shell32.DragQueryFileW.restype   = wintypes.UINT
    _shell32.DragFinish.argtypes      = [wintypes.HANDLE]
    _user32.ChangeWindowMessageFilterEx.argtypes = [
        wintypes.HWND, wintypes.UINT, wintypes.DWORD, ctypes.c_void_p
    ]
    _user32.ChangeWindowMessageFilterEx.restype  = wintypes.BOOL
    _user32.GetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int]
    _user32.GetWindowLongPtrW.restype  = ctypes.c_ssize_t
    _user32.SetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_ssize_t]
    _user32.SetWindowLongPtrW.restype  = ctypes.c_ssize_t
    _user32.CallWindowProcW.argtypes   = [
        ctypes.c_ssize_t, wintypes.HWND, wintypes.UINT,
        wintypes.WPARAM, wintypes.LPARAM
    ]
    _user32.CallWindowProcW.restype    = ctypes.c_ssize_t

# ── Filter logic ──────────────────────────────────────────────────────────────
REQUEST_START_RE = re.compile(r"^#\s*Sending Request:\s*Tester\s*->", re.IGNORECASE)

IS_READ_DTC_HINTS = (
    re.compile(r"\bRead\s+DTC\s+Information\b", re.IGNORECASE),
    re.compile(r"\bReport\s+DTC\b", re.IGNORECASE),
    re.compile(r"\b19\s+0[0-9A-Fa-f]\b"),
)

CAMERA_PREFIX_SET = {
    "D4D5",  # FLCW
    "D50A",  # SRCF
    "D50B",  # SRCL
    "D50C",  # SRCR
    "D509",  # SRCB
    "D4EE",  # LRBL
    "D4EF",  # LRBR
    "D606",  # LRIL
    "D607",  # LRIR
}

DTC_HEAD_RE   = re.compile(r"^\s*([A-F0-9]{4,8})\s+\t?\t?.*")
DTC_STATUS_RE = re.compile(r"^\s{1,}(0[1-9]|20|80)\s+.*")


def _is_dtc_header(line):
    m = DTC_HEAD_RE.match(line)
    return (True, m.group(1).strip()) if m else (False, None)


def _is_camera_dtc_code(code):
    return bool(code and len(code) >= 4 and code[:4] in CAMERA_PREFIX_SET)


def _block_is_read_dtc(block_lines):
    chunk = "\n".join(block_lines[:10])
    return any(p.search(chunk) for p in IS_READ_DTC_HINTS)


def _append_blank_line_once(dst):
    if dst and dst[-1].strip() != "":
        dst.append("")


def filter_log(input_path):
    text  = input_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    out   = []
    i, n  = 0, len(lines)

    while i < n:
        line = lines[i]
        if REQUEST_START_RE.match(line):
            block = [line]; i += 1
            while i < n and not REQUEST_START_RE.match(lines[i]):
                block.append(lines[i]); i += 1

            if _block_is_read_dtc(block):
                j, fb = 0, []
                while j < len(block):
                    L = block[j]
                    is_hdr, code = _is_dtc_header(L)
                    if is_hdr:
                        if _is_camera_dtc_code(code):
                            fb.append(L); k = j + 1
                            while k < len(block) and DTC_STATUS_RE.match(block[k]):
                                fb.append(block[k]); k += 1
                            _append_blank_line_once(fb); j = k
                        else:
                            k = j + 1
                            while k < len(block) and DTC_STATUS_RE.match(block[k]):
                                k += 1
                            j = k
                    else:
                        fb.append(L); j += 1
                out.extend(fb)
            else:
                out.extend(block)
            continue

        out.append(line)
        i += 1

    return "\n".join(out).rstrip() + "\n"


# ── GUI ───────────────────────────────────────────────────────────────────────
_BG_IDLE  = "#dce8fc"; _FG_IDLE  = "#1a56db"
_BG_DONE  = "#d4edda"; _FG_DONE  = "#155724"


class DSAFilterApp:
    def __init__(self, root):
        self.root              = root
        self._filtered_content = None
        self._current_path     = None
        self._wndproc_ref      = None  # keep ctypes callback alive

        root.title("DSA Log Filter")
        root.geometry("1050x760")
        root.minsize(700, 500)
        root.configure(bg="#f4f4f4")

        self._build_ui()

        if _WIN32:
            root.after(50, self._setup_drop)

    # ── Windows drag-and-drop ─────────────────────────────────────────────────
    def _setup_drop(self):
        hwnd = self.root.winfo_id()

        # Allow WM_DROPFILES + WM_COPYGLOBALDATA through Windows UIPI so
        # Explorer drops reach this window even without elevation matches.
        _user32.ChangeWindowMessageFilterEx(hwnd, _WM_DROPFILES,      _MSGFLT_ALLOW, None)
        _user32.ChangeWindowMessageFilterEx(hwnd, _WM_COPYGLOBALDATA, _MSGFLT_ALLOW, None)

        _shell32.DragAcceptFiles(hwnd, True)

        old_proc = _user32.GetWindowLongPtrW(hwnd, _GWL_WNDPROC)

        def _wndproc(h, msg, wparam, lparam):
            if msg == _WM_DROPFILES:
                buf = ctypes.create_unicode_buffer(260)
                _shell32.DragQueryFileW(wparam, 0, buf, 260)
                _shell32.DragFinish(wparam)
                self.root.after(0, lambda p=buf.value: self._load(Path(p)))
                return 0
            return _user32.CallWindowProcW(old_proc, h, msg, wparam, lparam)

        self._wndproc_ref = _WNDPROC_T(_wndproc)
        _user32.SetWindowLongPtrW(hwnd, _GWL_WNDPROC, self._wndproc_ref)

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",           padding=6,  font=("Segoe UI", 10))
        style.configure("TLabelframe.Label",             font=("Segoe UI", 10, "bold"))
        style.configure("Status.TLabel",                 font=("Segoe UI", 9), foreground="#555")

        input_frame = ttk.LabelFrame(self.root, text="Input File")
        input_frame.pack(fill=tk.X, padx=14, pady=(14, 6))

        drop_text = "Drop DSA log file here" if _WIN32 else "Use Browse button to open file"
        self._drop_zone = tk.Label(
            input_frame, text=drop_text,
            bg=_BG_IDLE, fg=_FG_IDLE,
            font=("Segoe UI", 13), relief="groove", bd=2, pady=26,
        )
        self._drop_zone.pack(fill=tk.X, padx=10, pady=(8, 4))

        btn_row = ttk.Frame(input_frame)
        btn_row.pack(fill=tk.X, padx=10, pady=(4, 10))

        ttk.Button(btn_row, text="Browse…", width=12, command=self._browse).pack(side=tk.LEFT)

        self._save_btn = ttk.Button(
            btn_row, text="Save filtered file", width=20,
            command=self._save, state=tk.DISABLED,
        )
        self._save_btn.pack(side=tk.RIGHT)

        self._status_var = tk.StringVar(value="No file loaded.")
        ttk.Label(btn_row, textvariable=self._status_var, style="Status.TLabel").pack(
            side=tk.LEFT, padx=12
        )

        out_frame = ttk.LabelFrame(self.root, text="Filtered Output")
        out_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=(4, 14))

        self._text = ScrolledText(
            out_frame, wrap=tk.NONE, font=("Consolas", 10),
            bg="white", fg="#1a1a1a", insertbackground="#1a1a1a",
            relief="flat", borderwidth=0,
        )
        self._text.pack(fill=tk.BOTH, expand=True, padx=6, pady=(6, 0))
        # Allow selecting and copying but block any keyboard edits.
        self._text.bind("<Key>", lambda e: "break" if (
            len(e.char) == 1 or e.keysym in (
                "BackSpace", "Delete", "Return", "Tab"
            )
        ) else None)

        h_sb = ttk.Scrollbar(out_frame, orient=tk.HORIZONTAL, command=self._text.xview)
        h_sb.pack(fill=tk.X, side=tk.BOTTOM, padx=6, pady=(0, 6))
        self._text.configure(xscrollcommand=h_sb.set)

    # ── Callbacks ─────────────────────────────────────────────────────────────
    def _browse(self):
        p = filedialog.askopenfilename(
            title="Select DSA Log File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if p:
            self._load(Path(p))

    def _load(self, path):
        if not path.exists():
            messagebox.showerror("File not found", "Could not find:\n{}".format(path))
            return
        try:
            self._status_var.set("Processing: {} …".format(path.name))
            self.root.update_idletasks()
            content = filter_log(path)
            self._filtered_content = content
            self._current_path     = path
            self._text.delete("1.0", tk.END)
            self._text.insert("1.0", content)
            self._status_var.set("Loaded: {}".format(path.name))
            self._save_btn.config(state=tk.NORMAL)
            self._drop_zone.config(
                text="\u2714  {}  \u2014  drop another file to replace".format(path.name),
                bg=_BG_DONE, fg=_FG_DONE,
            )
        except Exception as exc:
            messagebox.showerror("Processing error", str(exc))
            self._status_var.set("Error — see message.")

    def _save(self):
        if not self._filtered_content or not self._current_path:
            return
        out = self._current_path.with_name(self._current_path.stem + "_filtered.txt")
        out.write_text(self._filtered_content, encoding="utf-8")
        messagebox.showinfo("Saved", "Saved to:\n{}".format(out))


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    root = tk.Tk()
    DSAFilterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
