"""Exovision DTC Analyser — self-contained GUI
================================================
Double-click  run.bat  (or this file) to launch.

• Required packages are installed automatically on first run — no terminal needed.
• Settings and run-time history are saved to settings.json and restored on next launch.
• One-time prerequisite: run  az login  in any terminal once for Azure CLI auth.
"""

# ── stdlib only — heavy packages are imported AFTER the auto-installer ───────
from __future__ import annotations

import importlib
import json
import logging
import logging.handlers
import math
import os
import re
import subprocess
import sys
import threading
import time
import traceback
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, scrolledtext, ttk

# ─────────────────────────────────────────────────────────────────────────────
_SCRIPT_DIR    = Path(__file__).parent.resolve()
_SETTINGS_FILE = _SCRIPT_DIR / "settings.json"
_LOG_FILE      = _SCRIPT_DIR / "debug.log"

# ── File logger (set up immediately so even bootstrap/import errors are caught)
_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
_file_handler = logging.handlers.RotatingFileHandler(
    _LOG_FILE, maxBytes=2 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
_file_handler.setFormatter(
    logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s",
                      datefmt="%Y-%m-%d %H:%M:%S")
)
log = logging.getLogger("exovision")
log.setLevel(logging.DEBUG)
log.addHandler(_file_handler)

log.info("=" * 60)
log.info(f"Exovision DTC Analyser started  (Python {sys.version.split()[0]})")
log.info(f"Script dir: {_SCRIPT_DIR}")


def _install_crash_hooks() -> None:
    """Route all unhandled exceptions — main thread and daemon threads — to the log file."""

    def _handle(exc_type, exc_value, exc_tb):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_tb)
            return
        log.critical("Unhandled exception on main thread:",
                     exc_info=(exc_type, exc_value, exc_tb))

    sys.excepthook = _handle

    # Python 3.8+ threading hook
    def _thread_handle(args):
        if args.exc_type is SystemExit:
            return
        log.critical(
            f"Unhandled exception in thread '{args.thread.name if args.thread else '?'}':",
            exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
        )

    threading.excepthook = _thread_handle


_install_crash_hooks()


# ── Suppress console window flashes on Windows for ALL subprocesses ──────────
# azure-identity spawns 'az account get-access-token' on every token refresh;
# pip install also runs as a subprocess.  Neither should show a CMD window.
if sys.platform == "win32":
    _orig_popen = subprocess.Popen.__init__

    def _popen_no_window(self, *args, **kwargs):
        kwargs.setdefault("creationflags", subprocess.CREATE_NO_WINDOW)
        _orig_popen(self, *args, **kwargs)

    subprocess.Popen.__init__ = _popen_no_window
    log.debug("Subprocess console-window suppression applied.")


# ── Azure CLI path discovery ──────────────────────────────────────────────────
# pythonw.exe does not inherit the interactive shell PATH, so 'az' may be
# invisible even though it is installed.  Search well-known locations and
# inject the directory into os.environ['PATH'] so azure-identity can find it.
_AZ_SEARCH_PATHS = [
    Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"))
    / "Microsoft SDKs" / "Azure" / "CLI2" / "wbin",
    Path(os.environ.get("ProgramFiles", r"C:\Program Files"))
    / "Microsoft SDKs" / "Azure" / "CLI2" / "wbin",
    Path(os.environ.get("LOCALAPPDATA", "")) / "Programs" / "Azure CLI" / "wbin",
    Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Azure CLI" / "wbin",
]


def _ensure_az_on_path() -> bool:
    """Return True if az.cmd is already reachable; else inject its parent dir."""
    import shutil
    if shutil.which("az"):
        return True
    for candidate in _AZ_SEARCH_PATHS:
        az = candidate / "az.cmd"
        if az.exists():
            os.environ["PATH"] = str(candidate) + os.pathsep + os.environ.get("PATH", "")
            log.info("Azure CLI found at %s — added to PATH", candidate)
            return True
    log.warning("Azure CLI (az.cmd) not found in any known location.")
    return False

_DEFAULT_SETTINGS: dict = {
    "start_date":          "2026-01-01",
    "end_date":            str(date.today()),
    "timestamp_column":    "TS20__UTC",
    "ecu_addresses":       "1D12, 1D01",
    "dtc_prefixes":        "",
    "discover_schema":     True,
    "dtc_repo_filter":     False,
    # timing history — rolling list of last 5 completed-run durations (seconds)
    "run_durations":       [],
}

_PACKAGES = {
    "adlfs":          "adlfs",
    "azure-identity": "azure.identity",
    "polars":         "polars",
    "pyarrow":        "pyarrow",
    "pandas":         "pandas",
    "fsspec":         "fsspec",
    "matplotlib":     "matplotlib",
}

# ── macOS-inspired colour palette ────────────────────────────────────────────
_C = {
    "bg":          "#f5f5f7",   # macOS window background
    "sidebar":     "#e8e8ed",   # slightly darker panel
    "card":        "#ffffff",   # white card
    "accent":      "#0071e3",   # Apple blue
    "accent_dark": "#0051a8",
    "accent_text": "#ffffff",
    "text":        "#1d1d1f",   # near-black
    "subtext":     "#6e6e73",   # grey label
    "border":      "#d2d2d7",
    "success":     "#34c759",   # Apple green
    "error":       "#ff3b30",   # Apple red
    "log_bg":      "#1c1c1e",   # dark console
    "log_fg":      "#f2f2f7",
    "log_dim":     "#8e8e93",
    "log_ok":      "#32d74b",
    "log_err":     "#ff453a",
    "log_ts":      "#636366",
    "pb_trough":   "#d2d2d7",
    "pb_fill":     "#0071e3",
}

_FONT_SANS   = "SF Pro Display" if sys.platform == "darwin" else "Segoe UI"
_FONT_MONO   = "SF Mono"        if sys.platform == "darwin" else "Consolas"


# ═════════════════════════════════════════════════════════════════════════════
# Bootstrap installer
# ═════════════════════════════════════════════════════════════════════════════

def _missing() -> list[str]:
    out = []
    for pip_name, mod in _PACKAGES.items():
        try:
            importlib.import_module(mod.split(".")[0])
        except ImportError:
            out.append(pip_name)
    return out


def _bootstrap() -> bool:
    """Silently install missing packages behind a small progress window."""
    missing = _missing()
    if not missing:
        return True

    root = tk.Tk()
    root.title("Exovision DTC Analyser")
    root.resizable(False, False)
    root.configure(bg=_C["bg"])

    # Centre on screen
    root.update_idletasks()
    w, h = 560, 280
    x = (root.winfo_screenwidth()  - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    outer = tk.Frame(root, bg=_C["bg"])
    outer.pack(fill="both", expand=True, padx=24, pady=20)

    tk.Label(outer, text="Setting up Exovision DTC Analyser",
             bg=_C["bg"], fg=_C["text"],
             font=(_FONT_SANS, 14, "bold")).pack(anchor="w")
    tk.Label(outer, text="Installing required packages — just a moment…",
             bg=_C["bg"], fg=_C["subtext"],
             font=(_FONT_SANS, 11)).pack(anchor="w", pady=(2, 10))

    log = tk.Text(outer, height=6, state="disabled",
                  font=(_FONT_MONO, 9), bg=_C["log_bg"], fg=_C["log_fg"],
                  relief="flat", bd=0, padx=6, pady=4)
    log.pack(fill="both", expand=True)

    # Custom progress bar drawn on canvas
    pb_canvas = tk.Canvas(outer, height=6, bg=_C["bg"], highlightthickness=0)
    pb_canvas.pack(fill="x", pady=(10, 0))
    _pb_anim = [0.0]

    def _draw_pb():
        pb_canvas.update_idletasks()
        W = pb_canvas.winfo_width() or w - 48
        pb_canvas.delete("all")
        pb_canvas.create_rectangle(0, 0, W, 6, fill=_C["pb_trough"], outline="")
        seg = 0.35 * W
        off = (_pb_anim[0] % 1.0) * (W + seg) - seg
        x0 = max(0, off)
        x1 = min(W, off + seg)
        if x1 > x0:
            pb_canvas.create_rectangle(x0, 0, x1, 6,
                                       fill=_C["pb_fill"], outline="")
        _pb_anim[0] += 0.012
        if root.winfo_exists():
            root.after(30, _draw_pb)

    root.after(100, _draw_pb)
    ok = [True]

    def _append(text: str, colour: str = _C["log_fg"]) -> None:
        log.config(state="normal")
        log.insert("end", text + "\n")
        log.see("end")
        log.config(state="disabled")

    def _install() -> None:
        cmd = [sys.executable, "-m", "pip", "install", "--quiet"] + missing
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        for line in proc.stdout:
            line = line.rstrip()
            if line:
                root.after(0, _append, line)
        proc.wait()
        if proc.returncode != 0:
            ok[0] = False
            root.after(0, _append, "\n✗  Installation failed.")
            root.after(0, _append, f"   Run manually:  pip install {' '.join(missing)}")
            root.after(3000, root.destroy)
        else:
            root.after(0, _append, "\n✓  All packages ready — launching app…")
            root.after(1200, root.destroy)

    threading.Thread(target=_install, daemon=True).start()
    root.mainloop()
    return ok[0]


if not _bootstrap():
    log.error("Bootstrap failed — package installation did not complete.")
    sys.exit(1)


# ── Heavy imports (packages now guaranteed present) ───────────────────────────
import fsspec                                                      # noqa: E402
import matplotlib                                                  # noqa: E402
matplotlib.use("TkAgg")
import matplotlib.dates as mdates                                 # noqa: E402
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg   # noqa: E402
from matplotlib.figure import Figure                              # noqa: E402
import pandas as pd                                               # noqa: E402
import polars as pl                                               # noqa: E402


# ── Azure constants ───────────────────────────────────────────────────────────
_ACCOUNT      = "sys34e8eca5"
_ADLS_ROOT    = f"abfs://default@{_ACCOUNT}.dfs.core.windows.net"
_DTC_GLOB     = f"{_ADLS_ROOT}/data_refined/data_uds_dtcs_v2/**/*.parquet"
_DATE_RE      = re.compile(r"(\d{4})[/\-_](\d{2})[/\-_](\d{2})")
_TOKEN_CACHE      = _SCRIPT_DIR / ".dtc_token_cache.json"
_RESULT_CACHE     = _SCRIPT_DIR / ".dtc_result_cache"  # dir; one .parquet per query hash
_DTC_LOOKUP_CSV   = _SCRIPT_DIR / "dtc_lookup.csv"
_DTC_LOOKUP_JSON  = _SCRIPT_DIR / "dtc_lookup.json"


# ── Settings ──────────────────────────────────────────────────────────────────
def _load_settings() -> dict:
    if _SETTINGS_FILE.exists():
        try:
            saved = json.loads(_SETTINGS_FILE.read_text(encoding="utf-8"))
            return {**_DEFAULT_SETTINGS, **saved}
        except Exception:
            pass
    return dict(_DEFAULT_SETTINGS)


def _save_settings(s: dict) -> None:
    _SETTINGS_FILE.write_text(json.dumps(s, indent=2), encoding="utf-8")


def _load_dtc_lookup() -> dict[str, str]:
    """Return a dict mapping UPPERCASE DTC ID → description string.

    Reads  dtc_lookup.csv  or  dtc_lookup.json  from the script directory if
    either file exists.  Returns an empty dict when neither is present.

    CSV format (first row is a header; column names are case-insensitive):
        dtc_id,description
        D4AB87,Short Range Camera Back Electric Failure
        C03713,Chassis Stability: Vehicle Speed Signal

    JSON format (keys are DTC IDs, values are descriptions):
        { "D4AB87": "Short Range Camera Back Electric Failure", ... }
    """
    import csv as _csv

    # ── CSV lookup ────────────────────────────────────────────────────────────
    if _DTC_LOOKUP_CSV.exists():
        try:
            lookup: dict[str, str] = {}
            with open(_DTC_LOOKUP_CSV, newline="", encoding="utf-8-sig") as fh:
                reader = _csv.DictReader(fh)
                if reader.fieldnames:
                    key_col  = next(
                        (c for c in reader.fieldnames
                         if c.strip().lower() in ("dtc_id", "id", "code", "dtc")),
                        None,
                    )
                    desc_col = next(
                        (c for c in reader.fieldnames
                         if c.strip().lower() in ("description", "name", "label",
                                                   "desc", "fault", "text")),
                        None,
                    )
                    if key_col and desc_col:
                        for row in reader:
                            k = str(row.get(key_col, "")).strip().upper()
                            v = str(row.get(desc_col, "")).strip()
                            if k:
                                lookup[k] = v
            if lookup:
                return lookup
        except Exception:
            pass  # fall through to JSON

    # ── JSON lookup ───────────────────────────────────────────────────────────
    if _DTC_LOOKUP_JSON.exists():
        try:
            raw = json.loads(_DTC_LOOKUP_JSON.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                return {str(k).strip().upper(): str(v).strip()
                        for k, v in raw.items()}
        except Exception:
            pass

    return {}


def _get_storage_opts(log_fn=None) -> dict:
    """Return Azure ADLS storage options with a valid bearer token.

    The token is cached in .dtc_token_cache.json beside the script and reused
    for up to 58 minutes.  This avoids a ~4-5 s Azure CLI subprocess call on
    every run after the first.
    """
    import time as _time
    if _TOKEN_CACHE.exists():
        try:
            cached = json.loads(_TOKEN_CACHE.read_text(encoding="utf-8"))
            if float(cached.get("expires_at", 0)) > _time.time() + 120:
                if log_fn:
                    log_fn("Using cached Azure token (still valid).", "dim")
                return {"account_name": _ACCOUNT, "bearer_token": cached["token"]}
        except Exception:
            pass  # corrupt cache — re-fetch
    from azure.identity import AzureCliCredential  # local import (boot-time cost)
    token = AzureCliCredential().get_token("https://storage.azure.com/.default")
    try:
        _TOKEN_CACHE.write_text(
            json.dumps({"token": token.token, "expires_at": float(token.expires_on)}),
            encoding="utf-8",
        )
    except Exception:
        pass  # cache write failure is non-fatal
    return {"account_name": _ACCOUNT, "bearer_token": token.token}


def _result_cache_key(start_date, end_date, ecu_addrs, dtc_prefixes, ts_col, repo_filter: bool = False) -> str:
    """Return a short hex hash that uniquely identifies a query configuration."""
    import hashlib
    parts = [str(start_date), str(end_date), ",".join(sorted(ecu_addrs)),
             ",".join(sorted(dtc_prefixes)), ts_col, "1" if repo_filter else "0"]
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]


def _load_result_cache(key: str):
    """Return a polars DataFrame from disk cache, or None if not cached."""
    import polars as pl
    cache_file = _RESULT_CACHE / f"{key}.parquet"
    if cache_file.exists():
        try:
            return pl.read_parquet(cache_file)
        except Exception:
            pass  # corrupt cache
    return None


def _save_result_cache(key: str, df_dedup) -> None:
    """Write df_dedup to disk cache; silently ignore any errors."""
    try:
        _RESULT_CACHE.mkdir(exist_ok=True)
        cache_file = _RESULT_CACHE / f"{key}.parquet"
        df_dedup.write_parquet(cache_file)
        # Keep only the 10 most-recent cache files to avoid unbounded growth
        files = sorted(_RESULT_CACHE.glob("*.parquet"), key=lambda p: p.stat().st_mtime)
        for old in files[:-10]:
            old.unlink(missing_ok=True)
    except Exception:
        pass


# ── Analysis helpers ──────────────────────────────────────────────────────────
def _abs_paths(paths: list[str]) -> list[str]:
    return [_ADLS_ROOT + "/" + p.replace("default/", "") for p in paths]


def _path_date(path: str) -> Optional[date]:
    # Handle Hive-style date=YYYY-MM partitions (monthly) — treat as first of that month
    m = re.search(r"date=(\d{4})-(\d{2})(?:[^-/]|$)", path)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), 1)
        except ValueError:
            pass
    # Fallback: look for any YYYY-MM-DD pattern in the path
    m2 = _DATE_RE.search(path)
    if m2:
        try:
            return date(int(m2.group(1)), int(m2.group(2)), int(m2.group(3)))
        except ValueError:
            pass
    return None


def _parse_ecu_addresses(text: str) -> list[str]:
    """Return a list of uppercase hex ECU address strings, e.g. ['1D12', '1D01'].
    Accepts  1D12 / 0x1D12 / 7442 (decimal) — all normalised to upper hex.
    """
    if not text.strip():
        return []
    result = []
    for part in re.split(r"[,;\s]+", text):
        part = part.strip()
        if not part:
            continue
        try:
            if part.lower().startswith("0x"):
                result.append(format(int(part, 16), "X"))
            elif re.fullmatch(r"[0-9A-Fa-f]+", part):
                # Ambiguous: could be hex or decimal.  If it looks like a known
                # address length (3-4 hex chars e.g. "1D12"), treat as hex.
                if len(part) in (3, 4):
                    result.append(part.upper())
                else:
                    result.append(format(int(part), "X"))
            else:
                raise ValueError()
        except (ValueError, OverflowError):
            raise ValueError(
                f"Invalid ECU address '{part}' — use hex like 1D12 or 0x1D12")
    return result


def _parse_dtc_prefixes(text: str) -> list[str]:
    if not text.strip():
        return []
    return [p.strip() for p in re.split(r"[,;]", text) if p.strip()]


def _fmt_duration(secs: float) -> str:
    if secs < 60:
        return f"{secs:.0f}s"
    m, s = divmod(int(secs), 60)
    return f"{m}m {s:02d}s"


def _build_month_globs(start: "date", end: "date") -> list[str]:
    """Construct direct ADLS partition URIs from the date range.

    The data is partitioned as  data_uds_dtcs_v2/date=YYYY-MM/
    so for a Jan–Mar range we generate three paths instead of globbing
    2000+ files.  This skips the expensive recursive directory listing.
    """
    paths: list[str] = []
    d = start.replace(day=1)
    while d <= end:
        paths.append(
            f"{_ADLS_ROOT}/data_refined/data_uds_dtcs_v2/"
            f"date={d.strftime('%Y-%m')}/*.parquet"
        )
        # advance to first day of next month
        if d.month == 12:
            d = d.replace(year=d.year + 1, month=1)
        else:
            d = d.replace(month=d.month + 1)
    return paths


def _build_trend_chart(
    df_daily,         # pandas DataFrame: _event_date, dtc_count, car_count
    start_date: str,
    end_date: str,
    filter_label: str,
    total_dtc: int,
    peak_cars: int,
    prefix: str = "",
) -> "Figure":
    """Dual-axis line chart: DTC events + unique cars per day."""
    _CLR_DTC = _C["accent"]    # Apple blue  — DTC events line
    _CLR_CAR = _C["success"]   # Apple green — unique cars line

    fig = Figure(figsize=(11, 5.5), facecolor=_C["card"])
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    ax1.set_facecolor(_C["card"])

    ln1, = ax1.plot(
        df_daily["_event_date"], df_daily["dtc_count"],
        color=_CLR_DTC, linewidth=2, marker="o", markersize=3,
        label="DTC events", zorder=3,
    )
    ax1.fill_between(df_daily["_event_date"], df_daily["dtc_count"],
                     color=_CLR_DTC, alpha=0.07)
    ln2, = ax2.plot(
        df_daily["_event_date"], df_daily["car_count"],
        color=_CLR_CAR, linewidth=2, marker="s", markersize=3,
        linestyle="--", label="Unique cars", zorder=3,
    )
    ax2.fill_between(df_daily["_event_date"], df_daily["car_count"],
                     color=_CLR_CAR, alpha=0.07)

    for spine in ax1.spines.values(): spine.set_color(_C["border"])
    for spine in ax2.spines.values(): spine.set_color(_C["border"])
    ax1.set_ylabel("DTC events",  color=_CLR_DTC, fontsize=10, labelpad=8)
    ax2.set_ylabel("Unique cars", color=_CLR_CAR, fontsize=10, labelpad=8)
    ax1.set_xlabel("Date", fontsize=10, color=_C["subtext"], labelpad=6)
    ax1.tick_params(axis="y", colors=_CLR_DTC,     labelsize=9)
    ax1.tick_params(axis="x", colors=_C["subtext"], labelsize=9)
    ax2.tick_params(axis="y", colors=_CLR_CAR,      labelsize=9)
    ax1.yaxis.grid(True, linestyle="--", color=_C["border"], alpha=0.6)
    ax1.set_axisbelow(True)
    ax1.legend([ln1, ln2], ["DTC events", "Unique cars"],
               loc="upper left", framealpha=0.9, fontsize=9,
               edgecolor=_C["border"])
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d %b %Y"))
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=4, maxticks=16))
    for _lbl in ax1.get_xticklabels():
        _lbl.set_rotation(35)
        _lbl.set_ha("right")
    ax1.set_title(
        f"{prefix}Exovision DTC Events & Unique Vehicles per Day\n"
        f"{start_date}  →  {end_date}   ·   {filter_label}   ·   "
        f"Total events: {total_dtc:,}   Peak vehicles/day: {peak_cars:,}",
        fontsize=11, color=_C["text"], pad=10,
    )
    fig.tight_layout(pad=1.8)
    return fig


def _build_breakdown_chart(
    df_dtc,           # pandas DataFrame: label, occurrences, unique_cars
    filter_label: str,
    prefix: str = "",
) -> "Figure":
    """Horizontal bar chart of top-25 DTC occurrences."""
    _CLR_BAR = _C["accent"]

    n_dtcs = min(len(df_dtc), 25)
    # 0.55" per bar gives comfortable spacing with no label overlap
    fig_h = max(5.0, n_dtcs * 0.55)

    fig = Figure(figsize=(11, fig_h), facecolor=_C["card"])
    ax  = fig.add_subplot(111)
    ax.set_facecolor(_C["card"])

    top   = df_dtc.head(n_dtcs).iloc[::-1]   # reverse so highest is at top
    y_pos = range(len(top))
    bars  = ax.barh(list(y_pos), top["occurrences"],
                    color=_CLR_BAR, alpha=0.85, height=0.65)
    for bar, val, cars in zip(bars, top["occurrences"], top["unique_cars"]):
        ax.text(
            bar.get_width() + max(top["occurrences"]) * 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"{int(val):,}  ({int(cars):,} cars)",
            va="center", ha="left", fontsize=9, color=_C["subtext"],
        )

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(top["label"].tolist(), fontsize=9.5)
    ax.set_xlabel("Occurrences (deduplicated per vehicle per day)",
                  fontsize=9, color=_C["subtext"], labelpad=6)
    ax.set_title(
        f"{prefix}Top {n_dtcs} DTC Occurrences   ·   {filter_label}",
        fontsize=11, color=_C["text"], pad=10,
    )
    ax.xaxis.grid(True, linestyle="--", color=_C["border"], alpha=0.5)
    ax.set_axisbelow(True)
    for spine in ax.spines.values(): spine.set_color(_C["border"])
    ax.tick_params(colors=_C["subtext"], labelsize=9)
    if len(top):
        ax.set_xlim(0, top["occurrences"].max() * 1.30)

    # Scale left margin so the longest Y-axis label is never clipped
    _max_chars = max((len(s) for s in top["label"].tolist()), default=10)
    _left = min(0.65, max(0.15, _max_chars * 0.008))
    fig.tight_layout(pad=1.8)
    fig.subplots_adjust(left=_left)
    return fig


# \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
# Custom macOS-style widgets
# ═════════════════════════════════════════════════════════════════════════════

class _MacButton(tk.Canvas):
    """Pill-shaped button that mimics macOS style."""

    def __init__(self, parent, text: str, command=None,
                 primary: bool = True, **kw):
        kw.setdefault("bg", parent.cget("bg"))
        super().__init__(parent, height=32, highlightthickness=0, **kw)
        self._text    = text
        self._command = command
        self._primary = primary
        self._hover   = False
        self.bind("<Configure>", lambda e: self._draw())
        self.bind("<Enter>",     lambda e: self._on_enter())
        self.bind("<Leave>",     lambda e: self._on_leave())
        self.bind("<Button-1>",  lambda e: self._on_click())

    def _fill(self) -> str:
        if not self._primary:
            return _C["sidebar"] if not self._hover else _C["border"]
        return _C["accent_dark"] if self._hover else _C["accent"]

    def _draw(self):
        self.delete("all")
        W = self.winfo_width() or 120
        H = 32
        r = H // 2
        fill  = self._fill()
        tcolr = _C["accent_text"] if self._primary else _C["text"]
        # rounded rectangle
        self.create_oval(0, 0, H, H, fill=fill, outline="")
        self.create_oval(W - H, 0, W, H, fill=fill, outline="")
        self.create_rectangle(r, 0, W - r, H, fill=fill, outline="")
        self.create_text(W // 2, H // 2, text=self._text,
                         fill=tcolr, font=(_FONT_SANS, 11, "bold"))

    def _on_enter(self):
        self._hover = True; self._draw()

    def _on_leave(self):
        self._hover = False; self._draw()

    def _on_click(self):
        if self._command:
            self._command()

    def set_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.config(state=state)
        self._draw()


class _MacEntry(tk.Frame):
    """Text entry with rounded outline, macOS style."""

    def __init__(self, parent, textvariable: tk.StringVar,
                 width: int = 200, **kw):
        super().__init__(parent, bg=_C["bg"], **kw)
        self._var = textvariable
        self._canvas = tk.Canvas(self, height=30, width=width,
                                 bg=_C["bg"], highlightthickness=0)
        self._canvas.pack()
        self._entry = tk.Entry(self._canvas, textvariable=textvariable,
                               font=(_FONT_SANS, 11), bg=_C["card"],
                               fg=_C["text"], insertbackground=_C["text"],
                               relief="flat", bd=0)
        self._canvas.bind("<Configure>", lambda e: self._draw())
        self._entry.bind("<FocusIn>",  lambda e: self._draw(focused=True))
        self._entry.bind("<FocusOut>", lambda e: self._draw(focused=False))
        self._draw()

    def _draw(self, focused: bool = False):
        self._canvas.delete("all")
        W = self._canvas.winfo_width() or self._canvas.cget("width")
        W = int(W)
        H = 30
        r = 7
        border = _C["accent"] if focused else _C["border"]
        # rounded rect background
        for x0, y0, x1, y1 in [
            (0, r, W, H - r), (r, 0, W - r, H)
        ]:
            self._canvas.create_rectangle(x0, y0, x1, y1,
                                          fill=_C["card"], outline="")
        for cx, cy in [(r, r), (W - r, r), (r, H - r), (W - r, H - r)]:
            self._canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                     fill=_C["card"], outline="")
        # border outline
        self._canvas.create_arc(0, 0, 2 * r, 2 * r, start=90,  extent=90,  outline=border, style="arc")
        self._canvas.create_arc(W - 2 * r, 0, W, 2 * r, start=0, extent=90, outline=border, style="arc")
        self._canvas.create_arc(0, H - 2 * r, 2 * r, H, start=180, extent=90, outline=border, style="arc")
        self._canvas.create_arc(W - 2 * r, H - 2 * r, W, H, start=270, extent=90, outline=border, style="arc")
        self._canvas.create_line(r, 0, W - r, 0, fill=border)
        self._canvas.create_line(r, H, W - r, H, fill=border)
        self._canvas.create_line(0, r, 0, H - r, fill=border)
        self._canvas.create_line(W, r, W, H - r, fill=border)
        self._canvas.create_window(W // 2, H // 2,
                                    window=self._entry, width=W - 18)


class _Spinner(tk.Canvas):
    """Circular macOS-style activity spinner."""

    _SEGMENTS = 12

    def __init__(self, parent, size: int = 20, **kw):
        kw.setdefault("bg", parent.cget("bg"))
        super().__init__(parent, width=size, height=size,
                         highlightthickness=0, **kw)
        self._size  = size
        self._angle = 0
        self._running = False
        self._job: Optional[str] = None

    def start(self):
        self._running = True
        self._tick()

    def stop(self):
        self._running = False
        if self._job:
            self.after_cancel(self._job)
            self._job = None
        self.delete("all")

    def _tick(self):
        if not self._running:
            return
        self.delete("all")
        S = self._size
        cx = cy = S / 2
        r_outer = S / 2 - 1
        r_inner = r_outer * 0.45
        seg_angle = 360 / self._SEGMENTS
        for i in range(self._SEGMENTS):
            a = math.radians(self._angle - i * seg_angle)
            alpha = max(0.08, 1.0 - i / self._SEGMENTS)
            grey = int(160 + (1 - alpha) * 75)
            colour = f"#{grey:02x}{grey:02x}{grey:02x}"
            x0 = cx + r_inner * math.cos(a)
            y0 = cy - r_inner * math.sin(a)
            x1 = cx + r_outer * math.cos(a)
            y1 = cy - r_outer * math.sin(a)
            w  = max(1, int(2.6 * alpha))
            self.create_line(x0, y0, x1, y1, fill=colour, width=w,
                             capstyle="round")
        self._angle = (self._angle + 30) % 360
        self._job = self.after(80, self._tick)


class _ProgressBar(tk.Canvas):
    """
    Smooth macOS-style progress bar.

    In indeterminate mode the fill bounces continuously; call set_progress(0–1)
    to switch to determinate mode.
    """

    def __init__(self, parent, height: int = 5, **kw):
        kw.setdefault("bg", _C["bg"])
        super().__init__(parent, height=height,
                         highlightthickness=0, **kw)
        self._h        = height
        self._phase    = 0.0       # indeterminate animation phase
        self._progress = -1.0      # <0 = indeterminate
        self._running  = False
        self._job: Optional[str] = None

    def start_indeterminate(self):
        self._progress = -1.0
        self._running  = True
        self._tick()

    def set_progress(self, frac: float):
        """Switch to determinate mode and set fill 0.0–1.0."""
        self._progress = max(0.0, min(1.0, frac))
        self._draw()

    def stop(self):
        self._running = False
        if self._job:
            self.after_cancel(self._job)
            self._job = None
        self.delete("all")

    def _tick(self):
        if not self._running:
            return
        self._phase = (self._phase + 0.008) % 1.0
        self._draw()
        self._job = self.after(18, self._tick)

    def _draw(self):
        self.delete("all")
        W = self.winfo_width() or 300
        H = self._h
        r = H // 2
        # trough
        self.create_oval(0, 0, H, H, fill=_C["pb_trough"], outline="")
        self.create_oval(W - H, 0, W, H, fill=_C["pb_trough"], outline="")
        self.create_rectangle(r, 0, W - r, H, fill=_C["pb_trough"], outline="")

        if self._progress >= 0:
            # determinate
            fill_w = max(H, int(self._progress * W))
            fill_w = min(fill_w, W)
            self.create_oval(0, 0, H, H, fill=_C["pb_fill"], outline="")
            self.create_oval(fill_w - H, 0, fill_w, H, fill=_C["pb_fill"], outline="")
            self.create_rectangle(r, 0, fill_w - r, H, fill=_C["pb_fill"], outline="")
        else:
            # indeterminate — bouncing pill
            seg = 0.38 * W
            offset = math.sin(self._phase * 2 * math.pi) * 0.5 + 0.5
            x0 = offset * (W - seg)
            x1 = x0 + seg
            self.create_oval(x0, 0, x0 + H, H,     fill=_C["pb_fill"], outline="")
            self.create_oval(x1 - H, 0, x1, H,     fill=_C["pb_fill"], outline="")
            self.create_rectangle(x0 + r, 0, x1 - r, H,
                                  fill=_C["pb_fill"], outline="")


# ═════════════════════════════════════════════════════════════════════════════
# Main Application
# ═════════════════════════════════════════════════════════════════════════════

class App:

    def __init__(self) -> None:
        self._settings    = _load_settings()
        self._repo_filter_var:    Optional[tk.BooleanVar]      = None
        self._canvas_trend:       Optional[FigureCanvasTkAgg]  = None
        self._canvas_breakdown:   Optional[FigureCanvasTkAgg]  = None
        self._current_fig:        Optional[Figure]             = None
        self._run_start:   Optional[float]  = None
        self._elapsed_job: Optional[str]    = None

        self.root = tk.Tk()
        self.root.title("Exovision DTC Analyser")
        self.root.configure(bg=_C["bg"])
        self.root.geometry("1040x780")
        self.root.minsize(860, 640)

        self._apply_style()
        self._build_ui()
        self._populate_ui()

    # ── ttk style ─────────────────────────────────────────────────────────────

    def _apply_style(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(".",
            background=_C["bg"],
            foreground=_C["text"],
            font=(_FONT_SANS, 11),
            borderwidth=0,
            relief="flat",
        )
        style.configure("TNotebook",
            background=_C["bg"],
            tabmargins=[0, 0, 0, 0],
            borderwidth=0,
        )
        style.configure("TNotebook.Tab",
            background=_C["sidebar"],
            foreground=_C["subtext"],
            padding=[18, 8],
            font=(_FONT_SANS, 11),
            borderwidth=0,
        )
        style.map("TNotebook.Tab",
            background=[("selected", _C["bg"])],
            foreground=[("selected", _C["text"])],
        )
        style.configure("TCheckbutton",
            background=_C["bg"],
            foreground=_C["text"],
            font=(_FONT_SANS, 11),
        )
        style.configure("Heading.TLabel",
            background=_C["bg"],
            foreground=_C["text"],
            font=(_FONT_SANS, 12, "bold"),
        )
        style.configure("Sub.TLabel",
            background=_C["bg"],
            foreground=_C["subtext"],
            font=(_FONT_SANS, 10),
        )
        style.configure("Card.TFrame",
            background=_C["card"],
            relief="flat",
        )

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # Tab bar
        self._nb = ttk.Notebook(self.root)
        self._nb.pack(fill="both", expand=True, padx=0, pady=0)

        tab_s = tk.Frame(self._nb, bg=_C["bg"])
        self._nb.add(tab_s, text="  Settings  ")
        self._build_settings_tab(tab_s)

        tab_r = tk.Frame(self._nb, bg=_C["bg"])
        self._nb.add(tab_r, text="  Results  ")
        self._build_results_tab(tab_r)

    # ── Settings tab ──────────────────────────────────────────────────────────

    def _build_settings_tab(self, parent: tk.Frame) -> None:
        # Scrollable container
        scrollbar = ttk.Scrollbar(parent, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        scroll_canvas = tk.Canvas(parent, bg=_C["bg"], highlightthickness=0,
                                   yscrollcommand=scrollbar.set)
        scroll_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=scroll_canvas.yview)

        inner = tk.Frame(scroll_canvas, bg=_C["bg"])
        _win = scroll_canvas.create_window((0, 0), window=inner, anchor="nw")

        def _on_inner_configure(e):
            scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))
            # Keep inner frame width in sync with canvas
            scroll_canvas.itemconfig(_win, width=scroll_canvas.winfo_width())

        def _on_canvas_configure(e):
            scroll_canvas.itemconfig(_win, width=e.width)

        inner.bind("<Configure>", _on_inner_configure)
        scroll_canvas.bind("<Configure>", _on_canvas_configure)

        # Mousewheel scrolling
        def _on_mousewheel(e):
            scroll_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        scroll_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        pad = {"padx": 36}

        def section(title: str, subtitle: str = "") -> tk.Frame:
            tk.Frame(inner, bg=_C["border"], height=1).pack(
                fill="x", **pad, pady=(18, 0))
            hdr = tk.Frame(inner, bg=_C["bg"])
            hdr.pack(fill="x", **pad, pady=(10, 6))
            tk.Label(hdr, text=title, bg=_C["bg"], fg=_C["text"],
                     font=(_FONT_SANS, 13, "bold")).pack(anchor="w")
            if subtitle:
                tk.Label(hdr, text=subtitle, bg=_C["bg"], fg=_C["subtext"],
                         font=(_FONT_SANS, 10)).pack(anchor="w", pady=(1, 0))
            card = tk.Frame(inner, bg=_C["card"],
                            highlightbackground=_C["border"],
                            highlightthickness=1)
            card.pack(fill="x", **pad, pady=(0, 4))
            return card

        def field_row(card: tk.Frame, label: str, var: tk.StringVar,
                      hint: str = "", entry_width: int = 220,
                      last: bool = False) -> None:
            row = tk.Frame(card, bg=_C["card"])
            row.pack(fill="x", padx=16, pady=(10, 2 if hint else 10))
            tk.Label(row, text=label, bg=_C["card"], fg=_C["text"],
                     font=(_FONT_SANS, 11)).pack(anchor="w")
            _MacEntry(row, textvariable=var, width=entry_width).pack(
                anchor="w", pady=(4, 0))
            if hint:
                tk.Label(row, text=hint, bg=_C["card"], fg=_C["subtext"],
                         font=(_FONT_SANS, 9)).pack(anchor="w", pady=(2, 8))
            if not last:
                tk.Frame(card, bg=_C["border"], height=1).pack(
                    fill="x", padx=16)

        # ── Date range ────────────────────────────────────────────────────────
        card1 = section("Date Range", "Analysis window for DTC detections")
        self._start_var = tk.StringVar()
        self._end_var   = tk.StringVar()
        field_row(card1, "Start date", self._start_var, "YYYY-MM-DD")
        field_row(card1, "End date",   self._end_var,   "YYYY-MM-DD", last=True)

        # ── Filters ───────────────────────────────────────────────────────────
        card2 = section("Exovision Filters",
                         "Narrow results to specific ECUs or DTC codes")
        self._ecu_var    = tk.StringVar()
        self._prefix_var = tk.StringVar()
        field_row(card2, "ECU addresses (hex, comma-separated)",
                  self._ecu_var, "e.g. 0x1D12, 0x1D01  —  leave blank for all ECUs",
                  entry_width=360)
        field_row(card2, "DTC ID prefixes (comma-separated)",
                  self._prefix_var,
                  "e.g. A1B2, C3  —  leave blank for all DTC IDs",
                  entry_width=360)

        # Repo filter checkbox (inside Exovision Filters card)
        repo_cb_row = tk.Frame(card2, bg=_C["card"])
        repo_cb_row.pack(fill="x", padx=16, pady=(4, 12))
        self._repo_filter_var = tk.BooleanVar(value=bool(self._settings.get("dtc_repo_filter", False)))
        _lookup_exists_early = _DTC_LOOKUP_CSV.exists() or _DTC_LOOKUP_JSON.exists()
        repo_cb = tk.Checkbutton(
            repo_cb_row,
            text="Only include DTCs known to the diagnostics repo "
                 "(exact ID match or matching code-family prefix)",
            variable=self._repo_filter_var,
            bg=_C["card"], fg=_C["text"],
            activebackground=_C["card"], activeforeground=_C["text"],
            selectcolor=_C["sidebar"],
            font=(_FONT_SANS, 10),
            anchor="w",
        )
        repo_cb.pack(anchor="w")
        if not _lookup_exists_early:
            repo_cb.configure(state="disabled", fg=_C["subtext"],
                              text="Only include DTCs from the diagnostics repo "
                                   "(requires dtc_lookup.csv — see DTC Name Lookup below)")

        # ── Advanced ──────────────────────────────────────────────────────────
        card3 = section("Advanced")
        self._ts_col_var = tk.StringVar()
        field_row(card3, "Timestamp column name", self._ts_col_var,
                  entry_width=240)

        chk_row = tk.Frame(card3, bg=_C["card"])
        chk_row.pack(fill="x", padx=16, pady=(4, 12))
        self._discover_var = tk.BooleanVar()
        ttk.Checkbutton(
            chk_row,
            text="Discover schema only  (prints column names — use on first run)",
            variable=self._discover_var,
            style="TCheckbutton",
        ).pack(anchor="w")

        # ── DTC Name Lookup info ───────────────────────────────────────────────
        _lookup_exists = _DTC_LOOKUP_CSV.exists() or _DTC_LOOKUP_JSON.exists()
        _lookup_status = (
            f"✓  {_DTC_LOOKUP_CSV.name} loaded  ({sum(1 for _ in open(_DTC_LOOKUP_CSV, encoding='utf-8')) - 1} entries)"
            if _DTC_LOOKUP_CSV.exists()
            else (f"✓  {_DTC_LOOKUP_JSON.name} loaded" if _DTC_LOOKUP_JSON.exists()
                  else "✗  No lookup file found — DTC IDs will show without descriptions")
        )
        card4 = section("DTC Name Lookup",
                         "Optional file mapping DTC codes to human-readable names")
        info_row = tk.Frame(card4, bg=_C["card"])
        info_row.pack(fill="x", padx=16, pady=(10, 4))
        tk.Label(info_row, text=_lookup_status,
                 bg=_C["card"],
                 fg=_C["log_ok"] if _lookup_exists else _C["subtext"],
                 font=(_FONT_MONO, 9)).pack(anchor="w")
        hint_lines = [
            f"Place  dtc_lookup.csv  next to this script:  {_SCRIPT_DIR}",
            "Required columns:  dtc_id  (e.g. D4D596),  description  (human-readable name)",
            "Optional columns:  autosar_name,  platform",
            "",
            "To regenerate from the diagnostics repo, run:  _build_dtc_lookup.py",
        ]
        for ln in hint_lines:
            tk.Label(info_row, text=ln, bg=_C["card"], fg=_C["subtext"],
                     font=(_FONT_SANS, 9)).pack(anchor="w")
        tk.Frame(card4, bg=_C["border"], height=1).pack(fill="x", padx=16)
        regen_row = tk.Frame(card4, bg=_C["card"])
        regen_row.pack(fill="x", padx=16, pady=(6, 10))

        def _regen_lookup():
            import subprocess as _sp
            script = _SCRIPT_DIR / "_build_dtc_lookup.py"
            if not script.exists():
                messagebox.showerror("Not found",
                    f"_build_dtc_lookup.py not found in {_SCRIPT_DIR}")
                return
            self._log("Regenerating dtc_lookup.csv from diagnostics repo…", "dim")
            try:
                result = _sp.run(
                    [sys.executable, str(script)],
                    capture_output=True, text=True, timeout=60
                )
                out = (result.stdout + result.stderr).strip()
                self._log(out if out else "(no output)", "dim")
                if result.returncode == 0:
                    self._log("dtc_lookup.csv regenerated. Restart the app to apply.", "ok")
                else:
                    self._log(f"Script exited with code {result.returncode}", "err")
            except Exception as exc:
                self._log(f"Failed to run build script: {exc}", "err")

        _MacButton(regen_row, "Regenerate dtc_lookup.csv",
                   command=_regen_lookup, primary=False,
                   width=210).pack(side="left")

        # ── Action strip ──────────────────────────────────────────────────────
        tk.Frame(inner, bg=_C["border"], height=1).pack(
            fill="x", padx=36, pady=(18, 0))

        act = tk.Frame(inner, bg=_C["bg"])
        act.pack(fill="x", padx=36, pady=14)

        self._run_btn = _MacButton(act, "Run Analysis",
                                   command=self._on_run, primary=True,
                                   width=140)
        self._run_btn.pack(side="left", padx=(0, 10))

        _MacButton(act, "Demo Chart",
                   command=self._on_demo, primary=False,
                   width=110).pack(side="left", padx=(0, 10))

        _MacButton(act, "Save Settings",
                   command=self._on_save, primary=False,
                   width=130).pack(side="left")

        self._status_var = tk.StringVar(value="Ready")
        tk.Label(act, textvariable=self._status_var,
                 bg=_C["bg"], fg=_C["subtext"],
                 font=(_FONT_SANS, 10)).pack(side="left", padx=(18, 0))

        # Extra bottom padding
        tk.Frame(inner, bg=_C["bg"], height=24).pack()

    # ── Results tab ───────────────────────────────────────────────────────────

    def _build_results_tab(self, parent: tk.Frame) -> None:
        # ── Top status bar ────────────────────────────────────────────────────
        status_bar = tk.Frame(parent, bg=_C["sidebar"],
                              highlightbackground=_C["border"],
                              highlightthickness=1)
        status_bar.pack(fill="x", padx=20, pady=(14, 0))

        left = tk.Frame(status_bar, bg=_C["sidebar"])
        left.pack(side="left", padx=14, pady=10)

        self._spinner = _Spinner(left, size=18, bg=_C["sidebar"])
        self._spinner.pack(side="left", padx=(0, 8))

        self._progress_label_var = tk.StringVar(value="Waiting to run…")
        tk.Label(left, textvariable=self._progress_label_var,
                 bg=_C["sidebar"], fg=_C["text"],
                 font=(_FONT_SANS, 11, "bold")).pack(side="left")

        right = tk.Frame(status_bar, bg=_C["sidebar"])
        right.pack(side="right", padx=14, pady=10)

        self._eta_var = tk.StringVar(value="")
        tk.Label(right, textvariable=self._eta_var,
                 bg=_C["sidebar"], fg=_C["subtext"],
                 font=(_FONT_SANS, 10)).pack(side="right")

        # ── Progress bar ──────────────────────────────────────────────────────
        self._pb = _ProgressBar(parent, height=5)
        self._pb.pack(fill="x", padx=20, pady=(8, 0))

        # ── Sub-tab notebook: Log | Trend | DTC Breakdown ─────────────────────
        self._results_nb = ttk.Notebook(parent)
        self._results_nb.pack(fill="both", expand=True, padx=20, pady=(8, 14))

        # ── Log sub-tab ────────────────────────────────────────────────────────
        tab_log = tk.Frame(self._results_nb, bg=_C["log_bg"])
        self._results_nb.add(tab_log, text="  Log  ")

        log_outer = tk.Frame(tab_log, bg=_C["log_bg"],
                             highlightbackground=_C["border"],
                             highlightthickness=1)
        log_outer.pack(fill="both", expand=True)

        self._log_text = tk.Text(
            log_outer, state="disabled",
            font=(_FONT_MONO, 9), bg=_C["log_bg"], fg=_C["log_fg"],
            relief="flat", bd=0, padx=10, pady=6,
            selectbackground=_C["accent"], wrap="word",
        )
        sb = ttk.Scrollbar(log_outer, orient="vertical",
                           command=self._log_text.yview)
        self._log_text.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._log_text.pack(fill="both", expand=True)

        # Tag colours
        self._log_text.tag_configure("ts",  foreground=_C["log_ts"])
        self._log_text.tag_configure("ok",  foreground=_C["log_ok"])
        self._log_text.tag_configure("err", foreground=_C["log_err"])
        self._log_text.tag_configure("dim", foreground=_C["log_dim"])
        self._log_text.tag_configure("hdr", foreground=_C["accent"],
                                     font=(_FONT_MONO, 9, "bold"))

        # ── Trend sub-tab ──────────────────────────────────────────────────────
        tab_trend = tk.Frame(self._results_nb, bg=_C["bg"])
        self._results_nb.add(tab_trend, text="  Trend  ")
        self._trend_frame = tab_trend
        self._placeholder_trend = tk.Label(
            tab_trend,
            text="Run an analysis to see the trend chart here.",
            bg=_C["bg"], fg=_C["subtext"],
            font=(_FONT_SANS, 13),
        )
        self._placeholder_trend.place(relx=0.5, rely=0.5, anchor="center")

        # ── DTC Breakdown sub-tab ──────────────────────────────────────────────
        tab_breakdown = tk.Frame(self._results_nb, bg=_C["bg"])
        self._results_nb.add(tab_breakdown, text="  DTC Breakdown  ")
        self._breakdown_frame = tab_breakdown
        self._placeholder_breakdown = tk.Label(
            tab_breakdown,
            text="Run an analysis to see the DTC breakdown here.",
            bg=_C["bg"], fg=_C["subtext"],
            font=(_FONT_SANS, 13),
        )
        self._placeholder_breakdown.place(relx=0.5, rely=0.5, anchor="center")

    # ── Settings helpers ──────────────────────────────────────────────────────

    def _populate_ui(self) -> None:
        s = self._settings
        self._start_var.set(s["start_date"])
        self._end_var.set(s["end_date"])
        self._ecu_var.set(s["ecu_addresses"])
        self._prefix_var.set(s["dtc_prefixes"])
        self._ts_col_var.set(s["timestamp_column"])
        self._discover_var.set(bool(s["discover_schema"]))
        if self._repo_filter_var is not None:
            self._repo_filter_var.set(bool(s.get("dtc_repo_filter", False)))
        self._update_eta_label()

    def _gather_settings(self) -> dict:
        return {
            "start_date":       self._start_var.get().strip(),
            "end_date":         self._end_var.get().strip(),
            "timestamp_column": self._ts_col_var.get().strip() or "timestamp",
            "ecu_addresses":    self._ecu_var.get().strip(),
            "dtc_prefixes":     self._prefix_var.get().strip(),
            "discover_schema":  self._discover_var.get(),
            "dtc_repo_filter":  self._repo_filter_var.get() if self._repo_filter_var is not None else False,
            "run_durations":    self._settings.get("run_durations", []),
        }

    def _on_save(self) -> None:
        self._settings = self._gather_settings()
        _save_settings(self._settings)
        self._status_var.set("Settings saved")

    def _update_eta_label(self) -> None:
        durations = self._settings.get("run_durations", [])
        if durations:
            avg = sum(durations) / len(durations)
            self._eta_var.set(f"Estimated run time: ~{_fmt_duration(avg)}")
        else:
            self._eta_var.set("No run history yet")

    # ── Elapsed-time ticker (main thread) ─────────────────────────────────────

    def _start_elapsed_ticker(self) -> None:
        self._run_start = time.monotonic()
        self._tick_elapsed()

    def _stop_elapsed_ticker(self) -> None:
        if self._elapsed_job:
            self.root.after_cancel(self._elapsed_job)
            self._elapsed_job = None

    def _tick_elapsed(self) -> None:
        if self._run_start is None:
            return
        elapsed = time.monotonic() - self._run_start
        durations = self._settings.get("run_durations", [])
        if durations:
            avg = sum(durations) / len(durations)
            frac = min(0.97, elapsed / avg)   # cap at 97% until done
            self._pb.set_progress(frac)
            remaining = max(0, avg - elapsed)
            if remaining > 2:
                self._eta_var.set(
                    f"Elapsed: {_fmt_duration(elapsed)}  ·  "
                    f"~{_fmt_duration(remaining)} remaining"
                )
            else:
                self._eta_var.set(
                    f"Elapsed: {_fmt_duration(elapsed)}  ·  almost done…"
                )
        else:
            self._eta_var.set(f"Elapsed: {_fmt_duration(elapsed)}")
        self._elapsed_job = self.root.after(500, self._tick_elapsed)

    # ── Run / analysis ────────────────────────────────────────────────────────

    def _on_demo(self) -> None:
        """Generate a sample chart from synthetic data — no Azure needed."""
        s = self._gather_settings()
        try:
            start = datetime.strptime(s["start_date"], "%Y-%m-%d").date()
            end   = datetime.strptime(s["end_date"],   "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Invalid date",
                                 "Dates must be YYYY-MM-DD.", parent=self.root)
            return
        if start > end:
            messagebox.showerror("Invalid range",
                                 "Start must be ≤ end date.", parent=self.root)
            return

        self._run_btn.set_enabled(False)
        self._status_var.set("Demo running…")
        self._nb.select(1)
        self._clear_log()
        self._progress_label_var.set("Generating demo…")
        self._pb.start_indeterminate()
        self._spinner.start()
        self._start_elapsed_ticker()

        def _run():
            try:
                self._do_demo_analysis(s)
            except Exception as exc:
                tb = traceback.format_exc()
                log.error("Demo crashed:\n%s", tb)
                self._log("Demo error: " + str(exc), "err")
            finally:
                self.root.after(0, self._on_run_finished)
        threading.Thread(target=_run, daemon=True).start()

    def _do_demo_analysis(self, s: dict) -> None:
        """Build a chart from synthetic DTC data (no Azure required)."""
        import random
        random.seed(42)
        start_date = datetime.strptime(s["start_date"], "%Y-%m-%d").date()
        end_date   = datetime.strptime(s["end_date"],   "%Y-%m-%d").date()
        days = (end_date - start_date).days + 1

        self._log("── Demo Mode ─ synthetic data ──", "hdr")
        self._log(
            "No Azure connection used.  "
            "Data is randomly generated to demonstrate the chart.", "dim"
        )

        import datetime as _dt
        dates, dtc_counts, car_counts = [], [], []
        for i in range(days):
            d = start_date + _dt.timedelta(days=i)
            dtc_base = 8 if d.weekday() >= 5 else 25
            dtc_cnt  = max(0, int(random.gauss(dtc_base, dtc_base * 0.4)))
            if dtc_cnt > 0:
                car_base = max(1, dtc_cnt // 4)
                car_cnt  = max(1, int(random.gauss(car_base, car_base * 0.25)))
                dates.append(d)
                dtc_counts.append(dtc_cnt)
                car_counts.append(car_cnt)

        if not dates:
            self._log("Date range too narrow for demo — try at least 7 days.", "err")
            self._set_progress_label("Demo: no data")
            return

        df_daily_pd = pd.DataFrame({
            "_event_date": pd.to_datetime(dates),
            "dtc_count":   dtc_counts,
            "car_count":   car_counts,
        })
        total_dtc = int(df_daily_pd["dtc_count"].sum())
        peak_cars = int(df_daily_pd["car_count"].max())
        self._log(f"Sample covers {days} days — {len(dates)} active days.", "ok")
        self._log(f"Synthetic total DTC events: {total_dtc:,}  ·  Peak cars/day: {peak_cars:,}", "ok")

        # Synthetic DTC breakdown
        _demo_dtc_ids = [
            "98C44B", "983786", "980604", "98060C", "7056",
            "C10000", "C10001", "E03912", "E0392A", "B1234",
            "D5678", "F1001", "F1002", "A2222", "A3333",
        ]
        _demo_names = [
            "Lost comm. with exovision module", "Sensor signal out of range",
            "Camera calibration fault", "Radar timeout", "Lane assist disabled",
            "Power supply low voltage", "Power supply high voltage",
            "Ethernet link failure", "CAN bus off", "Vision processor temp",
            "Lens obstruction detected", "NUC heartbeat lost",
            "NUC heartbeat delayed", "Firmware CRC mismatch", "Config invalid",
        ]
        _occ = sorted(
            [max(1, int(random.gauss(total_dtc // len(_demo_dtc_ids),
                                     total_dtc // len(_demo_dtc_ids) * 0.4)))
             for _ in _demo_dtc_ids],
            reverse=True,
        )
        df_dtc_pd = pd.DataFrame({
            "dtc_id":      _demo_dtc_ids,
            "occurrences": _occ,
            "unique_cars": [max(1, o // 4) for o in _occ],
            "label":       [f"{did}  —  {nm}" for did, nm
                            in zip(_demo_dtc_ids, _demo_names)],
        })

        ecu_addrs    = _parse_ecu_addresses(s.get("ecu_addresses", ""))
        dtc_prefixes = _parse_dtc_prefixes(s.get("dtc_prefixes", ""))
        filter_parts = []
        if ecu_addrs:
            filter_parts.append(f"ECU: {ecu_addrs}")
        if dtc_prefixes:
            filter_parts.append(f"DTC prefix: {dtc_prefixes}")
        filter_label = ("  ·  ".join(filter_parts) if filter_parts
                        else "All ECUs / DTC IDs")

        fig_trend = _build_trend_chart(
            df_daily_pd,
            s["start_date"], s["end_date"], filter_label,
            total_dtc, peak_cars, prefix="[DEMO] ",
        )
        fig_breakdown = _build_breakdown_chart(
            df_dtc_pd, filter_label, prefix="[DEMO] ",
        )

        out_file = _SCRIPT_DIR / "exovision_dtc_demo.png"
        fig_trend.savefig(out_file, dpi=150, facecolor=_C["card"])
        self._log(f"Demo chart saved → {out_file}", "dim")
        self.root.after(0, self._show_charts, fig_trend, fig_breakdown)
        self._set_progress_label(f"Demo done — {total_dtc:,} events · {peak_cars:,} peak cars/day")
        self._set_status(f"Demo — {total_dtc:,} synthetic DTC events")

    def _on_run(self) -> None:
        s = self._gather_settings()
        try:
            start = datetime.strptime(s["start_date"], "%Y-%m-%d").date()
            end   = datetime.strptime(s["end_date"],   "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Invalid date",
                                 "Dates must be YYYY-MM-DD.", parent=self.root)
            return
        if start > end:
            messagebox.showerror("Invalid range",
                                 "Start date must be ≤ end date.", parent=self.root)
            return
        try:
            _parse_ecu_addresses(s["ecu_addresses"])
        except ValueError as exc:
            messagebox.showerror("Invalid ECU address", str(exc), parent=self.root)
            return

        self._settings = s
        _save_settings(s)

        self._run_btn.set_enabled(False)
        self._status_var.set("Running…")
        self._nb.select(1)
        self._clear_log()

        self._progress_label_var.set("Starting…")
        self._pb.start_indeterminate()
        self._spinner.start()
        self._start_elapsed_ticker()

        threading.Thread(target=self._run_analysis, args=(s,), daemon=True).start()

    def _run_analysis(self, s: dict) -> None:
        t0 = time.monotonic()
        log.info("Analysis started — settings: %s", {
            k: v for k, v in s.items() if k != "run_durations"
        })
        try:
            self._do_analysis(s)
            duration = time.monotonic() - t0
            log.info("Analysis finished in %.1f s", duration)
            # record duration for future estimates (keep last 5)
            durations = self._settings.get("run_durations", [])
            durations = (durations + [duration])[-5:]
            self._settings["run_durations"] = durations
            _save_settings(self._settings)
        except Exception as exc:
            tb = traceback.format_exc()
            log.error("Analysis crashed:\n%s", tb)
            self._log(f"Unexpected crash — details written to debug.log", tag="err")
            self._log(str(exc), tag="err")
            self._set_progress_label("Crashed — see debug.log")
        finally:
            self.root.after(0, self._on_run_finished)

    def _on_run_finished(self) -> None:
        self._stop_elapsed_ticker()
        self._spinner.stop()
        self._pb.stop()
        self._run_btn.set_enabled(True)
        self._update_eta_label()
        elapsed = time.monotonic() - self._run_start if self._run_start else 0
        self._eta_var.set(
            f"Last run: {_fmt_duration(elapsed)}  ·  "
            f"Est. next: ~{_fmt_duration(sum(self._settings.get('run_durations', [elapsed])) / max(1, len(self._settings.get('run_durations', [elapsed]))))}"
        )
        self._run_start = None

    # ── Log helpers (thread-safe) ─────────────────────────────────────────────

    def _log(self, text: str, tag: str = "") -> None:
        self.root.after(0, self._append_log, text, tag)

    def _append_log(self, text: str, tag: str = "") -> None:
        self._log_text.config(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        self._log_text.insert("end", f"[{ts}] ", "ts")
        self._log_text.insert("end", text + "\n", tag or "")
        self._log_text.see("end")
        self._log_text.config(state="disabled")
        # Mirror to file log
        level = logging.ERROR if tag == "err" else logging.DEBUG
        log.log(level, "[GUI] %s", text)

    def _clear_log(self) -> None:
        self._log_text.config(state="normal")
        self._log_text.delete("1.0", "end")
        self._log_text.config(state="disabled")

    def _set_status(self, text: str) -> None:
        self.root.after(0, self._status_var.set, text)

    def _set_progress_label(self, text: str) -> None:
        self.root.after(0, self._progress_label_var.set, text)

    # ── Core analysis (background thread) ────────────────────────────────────

    def _do_analysis(self, s: dict) -> None:
        start_date   = datetime.strptime(s["start_date"], "%Y-%m-%d").date()
        end_date     = datetime.strptime(s["end_date"],   "%Y-%m-%d").date()
        ts_col       = s["timestamp_column"]
        ecu_addrs    = _parse_ecu_addresses(s["ecu_addresses"])
        dtc_prefixes = _parse_dtc_prefixes(s["dtc_prefixes"])
        discover     = bool(s["discover_schema"])
        repo_filter  = bool(s.get("dtc_repo_filter", False))

        # ── Result cache check (skip multi-minute download on repeat runs) ────
        # A sha256 of the query parameters is used as filename.  If a matching
        # local parquet exists it is loaded instantly; the full ADLS download is
        # only done the first time (or when parameters change).
        _result_key  = _result_cache_key(start_date, end_date,
                                         ecu_addrs, dtc_prefixes, ts_col, repo_filter)
        df_dedup     = None if discover else _load_result_cache(_result_key)
        _from_cache  = df_dedup is not None
        _dtc_name_field: Optional[str] = (
            "_dtc_name" if (_from_cache and "_dtc_name" in df_dedup.columns)
            else None
        )

        if _from_cache:
            cache_file  = _RESULT_CACHE / f"{_result_key}.parquet"
            import os as _os
            cache_mb    = _os.path.getsize(cache_file) / 1e6
            self._set_progress_label("Loading from local cache…")
            self._log(
                f"Loaded {len(df_dedup):,} rows from local cache "
                f"({cache_mb:.1f} MB)  [key: {_result_key[:8]}]",
                "ok",
            )
            self._log(
                "Cache hit — skipping ADLS download.  "
                "To force a fresh download, change any query parameter "
                "or delete the .dtc_result_cache/ folder.", "dim"
            )
        else:
            # ── Azure auth: get bearer token (cached on disk) ─────────────────
            # The token is cached in .dtc_token_cache.json so the expensive Azure
            # CLI subprocess is only called once per hour instead of every run.
            self._set_progress_label("Authenticating with Azure CLI…")
            self._log("Locating Azure CLI…")
            az_found = _ensure_az_on_path()
            if not az_found:
                self._log("Azure CLI (az.cmd) not found — cannot authenticate.", "err")
                self._log("Install it:  winget install Microsoft.AzureCLI", "dim")
                self._log("Then run:    az login",                           "dim")
                self._set_progress_label("Azure CLI not found")
                self._set_status("Azure CLI not installed — see Results log.")
                return
            self._log("Fetching Azure storage token…")
            try:
                storage_opts = _get_storage_opts(log_fn=self._log)
            except Exception as exc:
                self._log(f"Azure auth failed: {exc}", "err")
                self._log("Run  az login  in a terminal, then retry.", "dim")
                self._set_progress_label("Auth failed — see log")
                self._set_status("Azure auth failed — see Results log.")
                return

            # ── Build partition paths directly — no glob needed ───────────────
            # Data is partitioned as  date=YYYY-MM/  so we construct the exact
            # month URIs from the requested date range instead of listing 2000+
            # files recursively.  For Jan–Mar we get 3 paths, not 1033.
            month_globs = _build_month_globs(start_date, end_date)
            self._log(
                f"Scanning {len(month_globs)} month partition(s): "
                + ", ".join(g.split("/date=")[1].split("/")[0] for g in month_globs),
                "ok",
            )

            # ── Schema discovery (optional first-run mode) ────────────────────
            if discover:
                # Clear any cached schema so the user gets fresh info next run too
                s.pop("_schema_cache", None)
                _save_settings(s)
                self._set_progress_label("Discovering schema…")
                self._log("── Schema Discovery ─", "hdr")
                df_s = pl.scan_parquet(month_globs, storage_options=storage_opts)
                try:
                    sc = df_s.collect_schema()
                    self._log(f"Columns ({len(sc)}): {list(sc)}", "ok")
                    preview = df_s.limit(3).collect()
                    self._log(f"First 3 rows:\n{preview}")
                except Exception as exc:
                    self._log(f"Discovery failed: {exc}", "err")
                self._log(
                    "Next: set Timestamp column name, enter ECU addresses, "
                    "uncheck Discover schema only, then Run Analysis again.", "dim"
                )
                self._set_progress_label("Schema discovery complete")
                self._set_status("Schema discovery complete — see log.")
                return

            # ── Load & filter ─────────────────────────────────────────────────
            self._set_progress_label("Loading data from Azure…")
            self._log("Loading data…")
            df_lazy = pl.scan_parquet(month_globs, storage_options=storage_opts)

            if ecu_addrs:
                df_lazy = df_lazy.filter(pl.col("ecuAddr").is_in(ecu_addrs))
                self._log(f"ECU filter: {ecu_addrs}")

            if dtc_prefixes:
                pf = pl.lit(False)
                for px in dtc_prefixes:
                    pf = pf | pl.col("dtc_id").cast(pl.Utf8).str.starts_with(px)
                df_lazy = df_lazy.filter(pf)
                self._log(f"DTC prefix filter: {dtc_prefixes}")

            if repo_filter:
                _lookup = _load_dtc_lookup()
                if _lookup:
                    # Derive 4-char code-family prefixes from the known IDs so that
                    # codes from the same family (but not yet in the lookup) are also
                    # included (e.g. D4EE96 matches prefix D4EE from D4EE11).
                    known_ids       = set(_lookup.keys())           # already upper-hex
                    known_prefixes  = sorted({k[:4] for k in known_ids})
                    rf = pl.col("dtc_id").cast(pl.Utf8).str.to_uppercase().is_in(known_ids)
                    for px in known_prefixes:
                        rf = rf | pl.col("dtc_id").cast(pl.Utf8).str.to_uppercase().str.starts_with(px)
                    df_lazy = df_lazy.filter(rf)
                    self._log(
                        f"Repo filter: {len(known_ids)} exact IDs + "
                        f"{len(known_prefixes)} prefix patterns  "
                        f"({', '.join(known_prefixes[:8])}"
                        f"{', …' if len(known_prefixes) > 8 else ''})",
                        "ok",
                    )
                else:
                    self._log(
                        "Repo filter enabled but dtc_lookup.csv not found — "
                        "filter skipped.  Run Regenerate dtc_lookup.csv first.",
                        "err",
                    )

            # ── Schema (use disk cache when available — skips ~7 s of footer reads) ─
            # The first time (no cache), we call collect_schema() to discover column
            # types and save the result in settings.json.  Every subsequent run uses
            # the cached values and skips the parquet-footer enumeration entirely.
            _sc_cache  = s.get("_schema_cache", {})
            _cache_hit = (_sc_cache.get("ts_col") == ts_col
                          and "ts_col_dtype_code" in _sc_cache)

            if _cache_hit:
                self._log("Using cached schema (tick 'Discover schema only' to refresh).", "dim")
                _use_vtstart    = _sc_cache.get("has_vtstart", False)
                _dtc_name_field = _sc_cache.get("dtc_name_field")
                _ts_dtype_code  = _sc_cache["ts_col_dtype_code"]
                schema          = None
            else:
                self._set_progress_label("Reading schema from parquet files…")
                self._log("Reading schema from parquet files (one-time; result will be cached)…")
                schema = df_lazy.collect_schema()
                if ts_col not in schema:
                    self._log(
                        f"Column '{ts_col}' not found in data.\n"
                        f"Available: {list(schema)}\n"
                        "Update 'Timestamp column name' in Settings.", "err"
                    )
                    self._set_progress_label(f"Column '{ts_col}' not found")
                    self._set_status(f"Column '{ts_col}' not found — check Settings.")
                    return
                ts_dtype        = schema[ts_col]
                _use_vtstart    = (ts_col == "TS20__UTC" and "vtStart" in schema)
                _dtc_name_field = None
                if "dtc_dict" in schema:
                    _dtyp = schema["dtc_dict"]
                    if hasattr(_dtyp, "fields"):
                        for _cand in ("name", "Name", "description",
                                      "Description", "dtcName", "dtc_name"):
                            if _cand in [f.name for f in _dtyp.fields]:
                                _dtc_name_field = _cand
                                break
                # Encode dtype as a short string for JSON storage
                if ts_dtype == pl.Date:
                    _ts_dtype_code = "Date"
                elif hasattr(ts_dtype, "is_temporal") and ts_dtype.is_temporal():
                    _ts_dtype_code = "Datetime"
                elif ts_dtype in (pl.Int32, pl.Int64, pl.UInt32, pl.UInt64):
                    _ts_dtype_code = "Epoch"
                else:
                    _ts_dtype_code = "Utf8"
                # Save to settings for future runs
                s["_schema_cache"] = {
                    "ts_col":            ts_col,
                    "ts_col_dtype_code": _ts_dtype_code,
                    "has_vtstart":       _use_vtstart,
                    "dtc_name_field":    _dtc_name_field,
                }
                _save_settings(s)
                self._log("Schema cached — subsequent runs will skip this step.", "dim")

            # ── Column pushdown ──────────────────────────────────────────────
            # Only read the columns we actually need — skips 35+ irrelevant
            # columns in a wide parquet file.
            _need = ["ecuAddr", "dtc_id", "pvin", ts_col]
            if _use_vtstart:
                _need.append("vtStart")
            if _dtc_name_field:
                _need.append("dtc_dict")
            if schema is not None:
                df_lazy = df_lazy.select([c for c in _need if c in schema])
            else:
                df_lazy = df_lazy.select(_need)  # cached: columns assumed present
            # Extract dtc name from struct before we drop dtc_dict
            if _dtc_name_field:
                df_lazy = df_lazy.with_columns(
                    pl.col("dtc_dict").struct.field(_dtc_name_field).alias("_dtc_name")
                ).drop("dtc_dict")

            if _ts_dtype_code == "Date":
                date_expr = pl.col(ts_col)
            elif _ts_dtype_code == "Datetime":
                ts_expr = (pl.col(ts_col).fill_null(pl.col("vtStart"))
                           if _use_vtstart else pl.col(ts_col))
                date_expr = ts_expr.cast(pl.Datetime).dt.date()
            elif _ts_dtype_code == "Epoch":
                date_expr = (pl.from_epoch(pl.col(ts_col), time_unit="ms")
                             .cast(pl.Datetime).dt.date())
            else:
                date_expr = (pl.col(ts_col).cast(pl.Utf8)
                             .str.to_datetime(strict=False).dt.date())

            df_lazy = (
                df_lazy
                .with_columns(date_expr.alias("_event_date"))
                .filter(
                    (pl.col("_event_date") >= pl.lit(start_date))
                    & (pl.col("_event_date") <= pl.lit(end_date))
                )
            )

            # ── Single collect ───────────────────────────────────────────────
            # Deduplicate first (pvin × dtc_id per day = one event per car per
            # DTC).  Then collect ONCE and do both aggregations in-memory.
            self._set_progress_label("Downloading and deduplicating…")
            self._log("Deduplicating and downloading (one network pass)…")
            _select_cols = ["_event_date", "dtc_id", "pvin"]
            if _dtc_name_field:
                _select_cols.append("_dtc_name")

            def _do_collect(lazy_df, columns):
                try:
                    return lazy_df.unique(subset=["pvin", "dtc_id", "_event_date"]).select(columns).collect(engine="streaming")
                except TypeError:
                    return lazy_df.unique(subset=["pvin", "dtc_id", "_event_date"]).select(columns).collect(streaming=True)  # type: ignore[call-arg]

            try:
                df_dedup = _do_collect(df_lazy, _select_cols)
            except OSError as _exc:
                if "401" in str(_exc) or "Unauthorized" in str(_exc) or "expired" in str(_exc).lower():
                    # Token expired mid-analysis — refresh and rebuild the lazy plan
                    self._log("Token expired mid-analysis — refreshing and retrying…", "dim")
                    storage_opts = _get_storage_opts(log_fn=None)  # force refresh
                    df_lazy = pl.scan_parquet(month_globs, storage_options=storage_opts)
                    if ecu_addrs:
                        df_lazy = df_lazy.filter(pl.col("ecuAddr").is_in(ecu_addrs))
                    if dtc_prefixes:
                        pf = pl.lit(False)
                        for _px in dtc_prefixes:
                            pf = pf | pl.col("dtc_id").cast(pl.Utf8).str.starts_with(_px)
                        df_lazy = df_lazy.filter(pf)
                    _need2 = ["ecuAddr", "dtc_id", "pvin", ts_col]
                    if _use_vtstart:
                        _need2.append("vtStart")
                    if _dtc_name_field:
                        _need2.append("dtc_dict")
                    df_lazy = df_lazy.select(_need2)
                    if _dtc_name_field:
                        df_lazy = df_lazy.with_columns(
                            pl.col("dtc_dict").struct.field(_dtc_name_field).alias("_dtc_name")
                        ).drop("dtc_dict")
                    df_lazy = df_lazy.with_columns(date_expr.alias("_event_date")).filter(
                        (pl.col("_event_date") >= pl.lit(start_date))
                        & (pl.col("_event_date") <= pl.lit(end_date))
                    )
                    df_dedup = _do_collect(df_lazy, _select_cols)
                else:
                    raise

            # Save to local result cache so next run is near-instant
            _save_result_cache(_result_key, df_dedup)
            self._log(f"Result cached  [key: {_result_key[:8]}].", "dim")
        # ── end of else (download) block ──────────────────────────────────────

        if df_dedup.is_empty():
            self._log("No DTCs found for this date range and filter set.", "err")
            self._set_progress_label("No DTCs found")
            self._set_status("No DTCs found — adjust date range or filters.")
            return

        self._log(f"Deduplicated rows: {len(df_dedup):,}", "ok")

        # — Daily aggregation (in-memory, instant) —————————————————————
        df_daily = (
            df_dedup
            .group_by("_event_date")
            .agg([
                pl.len().alias("dtc_count"),
                pl.col("pvin").n_unique().alias("car_count"),
            ])
            .sort("_event_date")
        )
        df_daily_pd = df_daily.to_pandas()
        df_daily_pd["_event_date"] = pd.to_datetime(df_daily_pd["_event_date"])
        df_daily_pd = df_daily_pd.sort_values("_event_date").reset_index(drop=True)

        total_dtc = int(df_daily_pd["dtc_count"].sum())
        peak_cars = int(df_daily_pd["car_count"].max())
        self._log(
            f"Total DTC events: {total_dtc:,}  ·  "
            f"Peak cars/day: {peak_cars:,}  ·  Active days: {len(df_daily_pd)}",
            "ok",
        )

        # — DTC breakdown aggregation (in-memory, instant) ————————————————
        _dtc_group = ["dtc_id"] + (["_dtc_name"] if _dtc_name_field else [])
        df_dtc_agg = (
            df_dedup
            .group_by(_dtc_group)
            .agg([
                pl.len().alias("occurrences"),
                pl.col("pvin").n_unique().alias("unique_cars"),
            ])
            .sort("occurrences", descending=True)
            .head(25)
        )
        df_dtc_pd = df_dtc_agg.to_pandas()

        # Enrich labels with human-readable names.
        # Priority: 1) name from parquet struct (_dtc_name_field), 2) dtc_lookup file
        _dtc_lookup = _load_dtc_lookup()
        if _dtc_lookup:
            self._log(f"DTC lookup: {len(_dtc_lookup)} entries loaded from dtc_lookup.csv/.json", "dim")

        def _make_label(row) -> str:
            dtc_upper = str(row["dtc_id"]).upper() if row["dtc_id"] else ""
            # 1. name from parquet struct (data source wins)
            if _dtc_name_field and "_dtc_name" in df_dtc_pd.columns:
                n = str(row.get("_dtc_name", "")).strip()
                if n:
                    return f"{dtc_upper}  —  {n[:50]}"
            # 2. name from local lookup file
            if _dtc_lookup and dtc_upper in _dtc_lookup:
                desc = _dtc_lookup[dtc_upper][:55]
                return f"{dtc_upper}  —  {desc}"
            return dtc_upper

        df_dtc_pd["label"] = df_dtc_pd.apply(_make_label, axis=1)

        self._log(
            df_dtc_pd[["label", "occurrences", "unique_cars"]].to_string(index=False),
            "dim",
        )

        # ── Build combined chart ─────────────────────────────────────────────────
        self._set_progress_label("Rendering chart…")
        filter_parts = []
        if ecu_addrs:
            filter_parts.append(f"ECU: {ecu_addrs}")
        if dtc_prefixes:
            filter_parts.append(f"DTC prefix: {dtc_prefixes}")
        filter_label = "  ·  ".join(filter_parts) if filter_parts else "All ECUs / DTC IDs"

        fig_trend = _build_trend_chart(
            df_daily_pd,
            s["start_date"], s["end_date"], filter_label,
            total_dtc, peak_cars, prefix="",
        )
        fig_breakdown = _build_breakdown_chart(
            df_dtc_pd, filter_label, prefix="",
        )

        out_file = _SCRIPT_DIR / "exovision_dtc_graph.png"
        fig_trend.savefig(out_file, dpi=150, facecolor=_C["card"])
        self._log(f"Chart saved → {out_file}", "dim")

        self.root.after(0, self._show_charts, fig_trend, fig_breakdown)
        self._set_progress_label(
            f"Done — {total_dtc:,} DTC events · {peak_cars:,} peak cars/day"
        )
        self._set_status(f"Done — {total_dtc:,} DTC events · {peak_cars:,} peak cars/day")

    # ── Chart display (main thread) ───────────────────────────────────────────

    def _show_charts(self, fig_trend: Figure, fig_breakdown: Figure) -> None:
        # ── Trend chart ────────────────────────────────────────────────────────
        if self._canvas_trend:
            self._canvas_trend.get_tk_widget().destroy()
            self._canvas_trend = None
        self._placeholder_trend.place_forget()
        self._canvas_trend = FigureCanvasTkAgg(fig_trend, master=self._trend_frame)
        self._canvas_trend.draw()
        w = self._canvas_trend.get_tk_widget()
        w.configure(bg=_C["card"], highlightthickness=0)
        w.pack(fill="both", expand=True)

        # ── Breakdown chart ────────────────────────────────────────────────────
        if self._canvas_breakdown:
            self._canvas_breakdown.get_tk_widget().destroy()
            self._canvas_breakdown = None
        self._placeholder_breakdown.place_forget()
        self._canvas_breakdown = FigureCanvasTkAgg(fig_breakdown, master=self._breakdown_frame)
        self._canvas_breakdown.draw()
        w = self._canvas_breakdown.get_tk_widget()
        w.configure(bg=_C["card"], highlightthickness=0)
        w.pack(fill="both", expand=True)

        self._current_fig = fig_trend
        # Switch to Trend sub-tab so the user sees results immediately
        self._results_nb.select(1)

    # ── Entry point ───────────────────────────────────────────────────────────

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    App().run()
