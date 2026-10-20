from __future__ import annotations

import datetime as dt
import concurrent.futures
import hashlib
import html
import importlib.util
import json
import os
import queue
import re
import shutil
import subprocess
import threading
import time
import traceback
from collections import OrderedDict
from dataclasses import dataclass, field, replace as dc_replace
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import polars as pl
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

PARQUET_SCAN_CAST_OPTIONS = pl.ScanCastOptions(
    missing_struct_fields="insert",
    extra_struct_fields="ignore",
)

try:
    import zstandard
    HAS_ZSTANDARD = True
except ImportError:
    HAS_ZSTANDARD = False


SCRIPT_DIR = Path(__file__).resolve().parent
SETTINGS_FILE = SCRIPT_DIR / "settings.json"
TOKEN_CACHE_FILE = SCRIPT_DIR / ".token_cache.json"
FAULT_CATALOG_FILE = SCRIPT_DIR / "fault_reasons.txt"
OCCURRENCE_CACHE_DIR = SCRIPT_DIR / ".occurrence_cache"
OCCURRENCE_CACHE_MAX_FILES = 20
OCCURRENCE_SCHEMA_CACHE_FILE = SCRIPT_DIR / ".occurrence_schema_cache.json"
# Persistent local cache of downloaded DTC parquet partition files. Reading remote parquet
# directly via polars' native Azure integration proved unreliable/slow in practice; the
# chunked fs.open() downloader (same mechanism already used for DLT files) is fast and
# stable, and since these partition files are immutable once written, caching them locally
# makes repeat/overlapping-window queries near-instant.
PARQUET_CACHE_DIR = SCRIPT_DIR / ".parquet_cache"
PARQUET_CACHE_MAX_BYTES = 4 * 1024 * 1024 * 1024
ANALYSIS_CHECKPOINT_FILE_NAME = "analysis_checkpoint.json"
ANALYSIS_CHECKPOINT_VERSION = 1
PARALLEL_FILE_WORKERS = 12
PARSED_DLT_CACHE_MAX_FILES = 3
MAX_DLT_CANDIDATES_PER_OCCURRENCE = 12
MAX_DLT_FILES_PER_VEHICLE = 4
FAILED_DISCOVERY_EXTRA_FILES = 12
PREFETCH_LOOKAHEAD = 4
PREFETCH_WORKERS = 4
MAX_CONCURRENT_AZURE_STREAMS = 16
# Safety margin (beyond the requested window) applied when pre-filtering DTC parquet
# partition files by filename timestamp, to tolerate ingestion/upload lag.
FILE_LISTING_MARGIN_HOURS_BEFORE = 12
FILE_LISTING_MARGIN_HOURS_AFTER = 6
# Per-file Azure round-trip latency dominates occurrence queries, so fetch discovered
# parquet files concurrently rather than in one serial combined scan.
PARQUET_FETCH_WORKERS = 12
DLT_STORAGE_MAGIC = b"DLT\x01"
ZSTD_MAGIC = b"\x28\xb5\x2f\xfd"
CONFIGHUB_BASELINE_TOKEN_RE = re.compile(r"\bSPA[0-9A-Za-z./-]*_INT[0-9A-Za-z._-]*\b", re.IGNORECASE)
CONFIGHUB_HINT_RE = re.compile(r"config\s*hub|confighub|baseline|sw\s*version|software\s*version", re.IGNORECASE)
STARTUP_BUILD_BASELINE_RE = re.compile(
    r"\b(?:cs-software-product|software-product)@([^,\s]+)(?:,\s*built@([^\s]+))?",
    re.IGNORECASE,
)
BASELINE_FALLBACK_MAX_FILES_PER_VEHICLE = 200

ACCOUNT = "sys34e8eca5"
ADLS_ROOT = f"abfs://default@{ACCOUNT}.dfs.core.windows.net"
DTC_GLOB_PREFIX = f"{ADLS_ROOT}/data_refined/data_uds_dtcs_v2"

WINDOW_OPTIONS = ["24h", "7d", "30d", "90d", "Manual"]
DEFAULT_SETTINGS: dict[str, Any] = {
    "window_mode": "7d",
    "manual_start": "2026-07-01 00:00:00",
    "manual_end": "2026-07-07 23:59:59",
    "dtc_list": "D50996",
    "output_dir": str(SCRIPT_DIR / "runs"),
}


@dataclass(frozen=True)
class Occurrence:
    vin: str
    variant: str
    dtc_id: str
    dtc_altvalue: str
    ecu_addr: str
    event_ts: dt.datetime
    source_ts_col: str
    confirmed: bool = False
    pending: bool = False
    test_failed_since_last_clear: bool = False
    status_byte_b0_test_failed: bool | None = None
    status_byte_b1_test_failed_this_cycle: bool | None = None
    status_byte_b2_pending: bool | None = None
    status_byte_b3_confirmed: bool | None = None
    status_byte_b4_test_not_completed_since_last_clear: bool | None = None
    status_byte_b5_test_failed_since_last_clear: bool | None = None
    status_byte_b6_test_not_completed_this_cycle: bool | None = None
    status_byte_b7_warning_indicator_requested: bool | None = None
    # Onboard "DTC time stamp" extended-data fields (already UTC): when the ECU actually
    # recorded this DTC's status change, as opposed to event_ts which may be the readout time.
    dtc_ts20_utc: dt.datetime | None = None
    dtc_ts21_utc: dt.datetime | None = None
    read_count: int = 1


@dataclass
class MatchResult:
    occurrence: Occurrence
    dlt_file: Path | None
    dtc_line: str | None
    reason: str | None
    reason_line: str | None
    reason_offset_lines: int | None
    dlt_line_index: int | None
    status: str
    error: str = ""
    reason_time_delta_seconds: float | None = None
    camera_state: str | None = None
    camera_state_line: str | None = None
    camera_state_time_delta_seconds: float | None = None
    baseline_summary: str | None = None
    baseline_time_delta_seconds: float | None = None
    baseline_source: str | None = None


@dataclass
class GroupedMapped:
    vin: str
    dtc_id: str
    reason: str
    count: int = 0
    days: set[str] = field(default_factory=set)
    files: set[Path] = field(default_factory=set)


@dataclass
class StorageSummary:
    total_files: int
    total_bytes: int
    referenced_files: int
    referenced_bytes: int


@dataclass
class DownloadBatchResult:
    files: list[Path]
    attempted_payloads: int = 0
    extraction_failures: list[str] = field(default_factory=list)


def dynamic_import(module_path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module at {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_fault_reasons(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"Fault catalog not found: {path}")
    seen: set[str] = set()
    ordered: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        token = line.strip()
        if not token or token.startswith("#"):
            continue
        low = token.lower()
        if low in seen:
            continue
        seen.add(low)
        ordered.append(token)
    if not ordered:
        raise RuntimeError("Fault catalog is empty")
    return ordered


def parse_dtc_list(text: str) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for chunk in re.split(r"[\s,;]+", text.strip()):
        token = re.sub(r"[^A-Za-z0-9]", "", chunk).upper()
        if not token:
            continue
        if token in seen:
            continue
        seen.add(token)
        out.append(token)
    return out


def load_settings() -> dict[str, Any]:
    if SETTINGS_FILE.exists():
        try:
            loaded = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
            return {**DEFAULT_SETTINGS, **loaded}
        except Exception:
            pass
    return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict[str, Any]) -> None:
    SETTINGS_FILE.write_text(json.dumps(settings, indent=2), encoding="utf-8")


def build_occurrence_cache_key(
    start_utc: dt.datetime,
    end_utc: dt.datetime,
    selected_dtcs: list[str],
) -> str:
    payload = "|".join([
        "occ_cache_v4_trigger_dedupe_read_counts",
        start_utc.isoformat(),
        end_utc.isoformat(),
        ",".join(sorted(selected_dtcs)),
    ])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]


def parse_optional_bool(value: Any) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        if value == 1:
            return True
        if value == 0:
            return False
        return None
    if isinstance(value, str):
        norm = value.strip().lower()
        if norm in {"1", "true", "yes", "y", "set", "active"}:
            return True
        if norm in {"0", "false", "no", "n", "clear", "inactive"}:
            return False
        return None
    return None


def parse_dtc_status_byte_flag(dtc_dict_value: Any, key: str) -> bool | None:
    if not isinstance(dtc_dict_value, dict):
        return None
    return parse_optional_bool(dtc_dict_value.get(key))


def occurrence_to_dict(occ: Occurrence) -> dict[str, Any]:
    return {
        "vin": occ.vin,
        "variant": occ.variant,
        "dtc_id": occ.dtc_id,
        "dtc_altvalue": occ.dtc_altvalue,
        "ecu_addr": occ.ecu_addr,
        "event_ts": occ.event_ts.isoformat(),
        "source_ts_col": occ.source_ts_col,
        "confirmed": occ.confirmed,
        "pending": occ.pending,
        "test_failed_since_last_clear": occ.test_failed_since_last_clear,
        "status_byte_b0_test_failed": occ.status_byte_b0_test_failed,
        "status_byte_b1_test_failed_this_cycle": occ.status_byte_b1_test_failed_this_cycle,
        "status_byte_b2_pending": occ.status_byte_b2_pending,
        "status_byte_b3_confirmed": occ.status_byte_b3_confirmed,
        "status_byte_b4_test_not_completed_since_last_clear": occ.status_byte_b4_test_not_completed_since_last_clear,
        "status_byte_b5_test_failed_since_last_clear": occ.status_byte_b5_test_failed_since_last_clear,
        "status_byte_b6_test_not_completed_this_cycle": occ.status_byte_b6_test_not_completed_this_cycle,
        "status_byte_b7_warning_indicator_requested": occ.status_byte_b7_warning_indicator_requested,
        "dtc_ts20_utc": occ.dtc_ts20_utc.isoformat() if occ.dtc_ts20_utc is not None else None,
        "dtc_ts21_utc": occ.dtc_ts21_utc.isoformat() if occ.dtc_ts21_utc is not None else None,
        "read_count": occ.read_count,
    }


def parse_optional_datetime(value: Any) -> dt.datetime | None:
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(str(value))
    except Exception:
        return None


def occurrence_from_dict(data: dict[str, Any]) -> Occurrence:
    return Occurrence(
        vin=str(data.get("vin", "")),
        variant=str(data.get("variant", "")),
        dtc_id=str(data.get("dtc_id", "")),
        dtc_altvalue=str(data.get("dtc_altvalue", "")),
        ecu_addr=str(data.get("ecu_addr", "")),
        event_ts=dt.datetime.fromisoformat(str(data.get("event_ts"))),
        source_ts_col=str(data.get("source_ts_col", "")),
        confirmed=bool(data.get("confirmed", False)),
        pending=bool(data.get("pending", False)),
        test_failed_since_last_clear=bool(data.get("test_failed_since_last_clear", False)),
        status_byte_b0_test_failed=parse_optional_bool(data.get("status_byte_b0_test_failed")),
        status_byte_b1_test_failed_this_cycle=parse_optional_bool(data.get("status_byte_b1_test_failed_this_cycle")),
        status_byte_b2_pending=parse_optional_bool(data.get("status_byte_b2_pending")),
        status_byte_b3_confirmed=parse_optional_bool(data.get("status_byte_b3_confirmed")),
        status_byte_b4_test_not_completed_since_last_clear=parse_optional_bool(data.get("status_byte_b4_test_not_completed_since_last_clear")),
        status_byte_b5_test_failed_since_last_clear=parse_optional_bool(data.get("status_byte_b5_test_failed_since_last_clear")),
        status_byte_b6_test_not_completed_this_cycle=parse_optional_bool(data.get("status_byte_b6_test_not_completed_this_cycle")),
        status_byte_b7_warning_indicator_requested=parse_optional_bool(data.get("status_byte_b7_warning_indicator_requested")),
        dtc_ts20_utc=parse_optional_datetime(data.get("dtc_ts20_utc")),
        dtc_ts21_utc=parse_optional_datetime(data.get("dtc_ts21_utc")),
        read_count=max(1, int(data.get("read_count", 1) or 1)),
    )


def match_to_dict(match: MatchResult) -> dict[str, Any]:
    return {
        "occurrence": occurrence_to_dict(match.occurrence),
        "dlt_file": str(match.dlt_file) if match.dlt_file else "",
        "dtc_line": match.dtc_line,
        "reason": match.reason,
        "reason_line": match.reason_line,
        "reason_offset_lines": match.reason_offset_lines,
        "dlt_line_index": match.dlt_line_index,
        "status": match.status,
        "error": match.error,
        "reason_time_delta_seconds": match.reason_time_delta_seconds,
        "camera_state": match.camera_state,
        "camera_state_line": match.camera_state_line,
        "camera_state_time_delta_seconds": match.camera_state_time_delta_seconds,
        "baseline_summary": match.baseline_summary,
        "baseline_time_delta_seconds": match.baseline_time_delta_seconds,
        "baseline_source": match.baseline_source,
    }


def match_from_dict(data: dict[str, Any]) -> MatchResult:
    dlt_file_value = str(data.get("dlt_file", "")).strip()
    return MatchResult(
        occurrence=occurrence_from_dict(data.get("occurrence", {})),
        dlt_file=Path(dlt_file_value) if dlt_file_value else None,
        dtc_line=data.get("dtc_line") if data.get("dtc_line") is None else str(data.get("dtc_line")),
        reason=data.get("reason") if data.get("reason") is None else str(data.get("reason")),
        reason_line=data.get("reason_line") if data.get("reason_line") is None else str(data.get("reason_line")),
        reason_offset_lines=int(data.get("reason_offset_lines")) if data.get("reason_offset_lines") is not None else None,
        dlt_line_index=int(data.get("dlt_line_index")) if data.get("dlt_line_index") is not None else None,
        status=str(data.get("status", "")),
        error=str(data.get("error", "")),
        reason_time_delta_seconds=float(data.get("reason_time_delta_seconds")) if data.get("reason_time_delta_seconds") is not None else None,
        camera_state=data.get("camera_state") if data.get("camera_state") is None else str(data.get("camera_state")),
        camera_state_line=data.get("camera_state_line") if data.get("camera_state_line") is None else str(data.get("camera_state_line")),
        camera_state_time_delta_seconds=float(data.get("camera_state_time_delta_seconds")) if data.get("camera_state_time_delta_seconds") is not None else None,
        baseline_summary=data.get("baseline_summary") if data.get("baseline_summary") is None else str(data.get("baseline_summary")),
        baseline_time_delta_seconds=float(data.get("baseline_time_delta_seconds")) if data.get("baseline_time_delta_seconds") is not None else None,
        baseline_source=data.get("baseline_source") if data.get("baseline_source") is None else str(data.get("baseline_source")),
    )


def message_epoch_us(msg: tuple[Any, ...]) -> int | None:
    try:
        seconds = int(msg[2])
        micros = int(msg[3])
        return seconds * 1_000_000 + micros
    except Exception:
        return None


def summarize_confighub_baseline(line: str) -> str | None:
    tokens = [token.upper() for token in CONFIGHUB_BASELINE_TOKEN_RE.findall(line)]
    if tokens:
        ordered_unique = list(dict.fromkeys(tokens))
        preview = ordered_unique[:3]
        suffix = "" if len(ordered_unique) <= 3 else f" (+{len(ordered_unique) - 3})"
        summary = ", ".join(preview) + suffix
    else:
        startup_match = STARTUP_BUILD_BASELINE_RE.search(line)
        if not startup_match:
            return None
        product = startup_match.group(1)
        built = startup_match.group(2)
        summary = f"STARTUP_BUILD: {product}"
        if built:
            summary += f" (built {built})"
    if len(summary) > 220:
        summary = summary[:217] + "..."
    return summary


def find_confighub_baseline(
    messages: list[tuple[Any, ...]],
    anchor_index: int | None,
) -> tuple[str | None, float | None]:
    anchor_ts_us = message_epoch_us(messages[anchor_index]) if anchor_index is not None and 0 <= anchor_index < len(messages) else None
    best_summary: str | None = None
    best_delta_seconds: float | None = None
    best_score: tuple[int, int, int, int] | tuple[int, int, int] | None = None

    for idx, msg in enumerate(messages):
        line = str(msg[7])
        summary = summarize_confighub_baseline(line)
        if not summary:
            continue
        hint_penalty = 0 if CONFIGHUB_HINT_RE.search(line) else 1

        if anchor_index is None:
            score = (hint_penalty, idx, 0)
            delta_seconds = None
        else:
            ts_us = message_epoch_us(msg)
            if anchor_ts_us is not None and ts_us is not None:
                delta_us = ts_us - anchor_ts_us
                score = (hint_penalty, abs(delta_us), 0 if delta_us <= 0 else 1, abs(idx - anchor_index))
                delta_seconds = delta_us / 1_000_000.0
            else:
                line_delta = idx - anchor_index
                score = (hint_penalty, abs(line_delta), 0 if line_delta <= 0 else 1, abs(line_delta))
                delta_seconds = None

        if best_score is None or score < best_score:
            best_score = score
            best_summary = summary
            best_delta_seconds = delta_seconds

    return best_summary, best_delta_seconds


def find_message_index_near_event_ts(messages: list[tuple[Any, ...]], event_ts: dt.datetime) -> int | None:
    target_us = int(event_ts.timestamp() * 1_000_000)
    best_idx: int | None = None
    best_abs_delta: int | None = None

    for idx, msg in enumerate(messages):
        ts_us = message_epoch_us(msg)
        if ts_us is None:
            continue
        delta = abs(ts_us - target_us)
        if best_abs_delta is None or delta < best_abs_delta:
            best_abs_delta = delta
            best_idx = idx

    return best_idx


def save_analysis_checkpoint(
    checkpoint_path: Path,
    *,
    start_utc: dt.datetime,
    end_utc: dt.datetime,
    selected_dtcs: list[str],
    ts_col: str,
    ordered_occurrences: list[Occurrence],
    next_index: int,
    matches: list[MatchResult],
    failures: list[str],
    completed: bool,
) -> None:
    payload = {
        "version": ANALYSIS_CHECKPOINT_VERSION,
        "updated_utc": dt.datetime.utcnow().isoformat() + "Z",
        "completed": completed,
        "start_utc": start_utc.isoformat(),
        "end_utc": end_utc.isoformat(),
        "selected_dtcs": list(selected_dtcs),
        "ts_col": ts_col,
        "next_index": int(next_index),
        "ordered_occurrences": [occurrence_to_dict(occ) for occ in ordered_occurrences],
        "matches": [match_to_dict(match) for match in matches],
        "failures": list(failures),
    }
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = checkpoint_path.with_suffix(checkpoint_path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp_path.replace(checkpoint_path)


def load_analysis_checkpoint(checkpoint_path: Path) -> dict[str, Any] | None:
    if not checkpoint_path.exists():
        return None
    try:
        return json.loads(checkpoint_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def find_latest_incomplete_checkpoint(output_dir: Path) -> Path | None:
    checkpoints = find_incomplete_checkpoints(output_dir)
    return checkpoints[0] if checkpoints else None


def find_incomplete_checkpoints(output_dir: Path) -> list[Path]:
    if not output_dir.exists() or not output_dir.is_dir():
        return []
    candidates = sorted(
        output_dir.glob(f"run_*/{ANALYSIS_CHECKPOINT_FILE_NAME}"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    incomplete: list[Path] = []
    for checkpoint_path in candidates:
        data = load_analysis_checkpoint(checkpoint_path)
        if data is None:
            continue
        if bool(data.get("completed", False)):
            continue
        incomplete.append(checkpoint_path)
    return incomplete


def load_occurrence_cache(cache_key: str) -> tuple[list[Occurrence], str] | None:
    cache_file = OCCURRENCE_CACHE_DIR / f"{cache_key}.json"
    if not cache_file.exists():
        return None
    try:
        raw = json.loads(cache_file.read_text(encoding="utf-8"))
        ts_col = str(raw.get("ts_col", ""))
        items = raw.get("occurrences", [])
        occurrences: list[Occurrence] = []
        for item in items:
            occurrences.append(
                Occurrence(
                    vin=str(item["vin"]),
                    variant=str(item["variant"]),
                    dtc_id=str(item["dtc_id"]),
                    dtc_altvalue=str(item.get("dtc_altvalue", "")),
                    ecu_addr=str(item.get("ecu_addr", "")),
                    event_ts=dt.datetime.fromisoformat(str(item["event_ts"])),
                    source_ts_col=ts_col,
                    confirmed=bool(item.get("confirmed", False)),
                    pending=bool(item.get("pending", False)),
                    test_failed_since_last_clear=bool(item.get("test_failed_since_last_clear", False)),
                    status_byte_b0_test_failed=parse_optional_bool(item.get("status_byte_b0_test_failed")),
                    status_byte_b1_test_failed_this_cycle=parse_optional_bool(item.get("status_byte_b1_test_failed_this_cycle")),
                    status_byte_b2_pending=parse_optional_bool(item.get("status_byte_b2_pending")),
                    status_byte_b3_confirmed=parse_optional_bool(item.get("status_byte_b3_confirmed")),
                    status_byte_b4_test_not_completed_since_last_clear=parse_optional_bool(item.get("status_byte_b4_test_not_completed_since_last_clear")),
                    status_byte_b5_test_failed_since_last_clear=parse_optional_bool(item.get("status_byte_b5_test_failed_since_last_clear")),
                    status_byte_b6_test_not_completed_this_cycle=parse_optional_bool(item.get("status_byte_b6_test_not_completed_this_cycle")),
                    status_byte_b7_warning_indicator_requested=parse_optional_bool(item.get("status_byte_b7_warning_indicator_requested")),
                    dtc_ts20_utc=parse_optional_datetime(item.get("dtc_ts20_utc")),
                    dtc_ts21_utc=parse_optional_datetime(item.get("dtc_ts21_utc")),
                    read_count=max(1, int(item.get("read_count", 1) or 1)),
                )
            )
        return occurrences, ts_col
    except Exception:
        return None


def save_occurrence_cache(cache_key: str, ts_col: str, occurrences: list[Occurrence]) -> None:
    try:
        OCCURRENCE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = OCCURRENCE_CACHE_DIR / f"{cache_key}.json"
        payload = {
            "ts_col": ts_col,
            "occurrences": [
                {
                    "vin": occ.vin,
                    "variant": occ.variant,
                    "dtc_id": occ.dtc_id,
                    "dtc_altvalue": occ.dtc_altvalue,
                    "ecu_addr": occ.ecu_addr,
                    "event_ts": occ.event_ts.isoformat(),
                    "confirmed": occ.confirmed,
                    "pending": occ.pending,
                    "test_failed_since_last_clear": occ.test_failed_since_last_clear,
                    "status_byte_b0_test_failed": occ.status_byte_b0_test_failed,
                    "status_byte_b1_test_failed_this_cycle": occ.status_byte_b1_test_failed_this_cycle,
                    "status_byte_b2_pending": occ.status_byte_b2_pending,
                    "status_byte_b3_confirmed": occ.status_byte_b3_confirmed,
                    "status_byte_b4_test_not_completed_since_last_clear": occ.status_byte_b4_test_not_completed_since_last_clear,
                    "status_byte_b5_test_failed_since_last_clear": occ.status_byte_b5_test_failed_since_last_clear,
                    "status_byte_b6_test_not_completed_this_cycle": occ.status_byte_b6_test_not_completed_this_cycle,
                    "status_byte_b7_warning_indicator_requested": occ.status_byte_b7_warning_indicator_requested,
                    "dtc_ts20_utc": occ.dtc_ts20_utc.isoformat() if occ.dtc_ts20_utc is not None else None,
                    "dtc_ts21_utc": occ.dtc_ts21_utc.isoformat() if occ.dtc_ts21_utc is not None else None,
                    "read_count": occ.read_count,
                }
                for occ in occurrences
            ],
        }
        cache_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

        files = sorted(OCCURRENCE_CACHE_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime)
        for old in files[:-OCCURRENCE_CACHE_MAX_FILES]:
            old.unlink(missing_ok=True)
    except Exception:
        pass


def load_occurrence_schema_cache() -> dict[str, str] | None:
    if not OCCURRENCE_SCHEMA_CACHE_FILE.exists():
        return None
    try:
        raw = json.loads(OCCURRENCE_SCHEMA_CACHE_FILE.read_text(encoding="utf-8"))
        required = ["vin_col", "dtc_col", "ts_col", "ts_dtype_code"]
        if any(not raw.get(key) for key in required):
            return None
        if "ts21_utc_col" not in raw or "ts20_utc_col" not in raw:
            return None
        return {
            "vin_col": str(raw.get("vin_col", "")),
            "dtc_col": str(raw.get("dtc_col", "")),
            "variant_col": str(raw.get("variant_col", "")),
            "alt_col": str(raw.get("alt_col", "")),
            "ecu_addr_col": str(raw.get("ecu_addr_col", "")),
            "ts_col": str(raw.get("ts_col", "")),
            "ts_dtype_code": str(raw.get("ts_dtype_code", "Utf8")),
            "confirmed_col": str(raw.get("confirmed_col", "")),
            "pending_col": str(raw.get("pending_col", "")),
            "test_failed_col": str(raw.get("test_failed_col", "")),
            "dtc_dict_col": str(raw.get("dtc_dict_col", "")),
            "ts20_utc_col": str(raw.get("ts20_utc_col", "")),
            "ts21_utc_col": str(raw.get("ts21_utc_col", "")),
        }
    except Exception:
        return None


def save_occurrence_schema_cache(cache: dict[str, str]) -> None:
    try:
        OCCURRENCE_SCHEMA_CACHE_FILE.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    except Exception:
        pass


def parse_manual_datetime(value: str) -> dt.datetime:
    value = value.strip()
    fmts = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]
    for fmt in fmts:
        try:
            parsed = dt.datetime.strptime(value, fmt)
            if fmt == "%Y-%m-%d":
                return parsed.replace(hour=0, minute=0, second=0)
            return parsed
        except ValueError:
            continue
    raise ValueError(f"Invalid datetime '{value}'. Use YYYY-MM-DD HH:MM:SS")


def resolve_analysis_range(
    mode: str,
    manual_start: dt.datetime | None,
    manual_end: dt.datetime | None,
    now_utc: dt.datetime,
) -> tuple[dt.datetime, dt.datetime]:
    mode = mode.strip()
    if mode == "Manual":
        if manual_start is None or manual_end is None:
            raise ValueError("Manual mode requires start and end datetimes")
        if manual_end <= manual_start:
            raise ValueError("Manual end must be after manual start")
        if (manual_end - manual_start).days > 365:
            raise ValueError("Manual range cannot exceed 365 days")
        return manual_start, manual_end

    if mode == "24h":
        return now_utc - dt.timedelta(hours=24), now_utc
    if mode == "7d":
        return now_utc - dt.timedelta(days=7), now_utc
    if mode == "30d":
        return now_utc - dt.timedelta(days=30), now_utc
    if mode == "90d":
        return now_utc - dt.timedelta(days=90), now_utc

    raise ValueError(f"Unsupported mode: {mode}")


def build_month_globs(start_utc: dt.datetime, end_utc: dt.datetime) -> list[str]:
    paths: list[str] = []
    current = start_utc.date().replace(day=1)
    end_month = end_utc.date().replace(day=1)
    while current <= end_month:
        paths.append(f"{DTC_GLOB_PREFIX}/date={current.strftime('%Y-%m')}/*.parquet")
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)
    return paths


_LISTING_AZURE_FS_CACHE: Any = None


def _get_listing_azure_fs():
    """Lazily create (and cache) an Azure filesystem handle used only for cheap file listing."""
    global _LISTING_AZURE_FS_CACHE
    if _LISTING_AZURE_FS_CACHE is not None:
        return _LISTING_AZURE_FS_CACHE
    nuc = dynamic_import(
        SCRIPT_DIR.parent / "NucDltWindowDownloader" / "nuc_dlt_window_downloader.py",
        "nuc_downloader_module_for_listing",
    )
    _LISTING_AZURE_FS_CACHE = nuc.create_azure_fs()
    return _LISTING_AZURE_FS_CACHE


def parse_month_partition_filename_ts(name: str) -> dt.datetime | None:
    match = re.search(r"(\d{4}-\d{2}-\d{2}T\d{6})", name)
    if not match:
        return None
    try:
        return dt.datetime.strptime(match.group(1), "%Y-%m-%dT%H%M%S")
    except ValueError:
        return None


def build_month_globs_filtered(start_utc: dt.datetime, end_utc: dt.datetime, log_fn) -> tuple[list[str], list[str]]:
    """
    Narrow the month-level partition glob(s) down to only the parquet files whose filename
    timestamp falls within the requested window (+/- a safety margin for ingestion lag),
    instead of scanning every file in the month(s).
    Returns (discovered_remote_file_paths, fallback_month_globs). Fallback globs are used
    for any month where listing fails or no filename matched, so results are never dropped.
    """
    month_globs = build_month_globs(start_utc, end_utc)
    window_start = start_utc - dt.timedelta(hours=FILE_LISTING_MARGIN_HOURS_BEFORE)
    window_end = end_utc + dt.timedelta(hours=FILE_LISTING_MARGIN_HOURS_AFTER)

    try:
        fs = _get_listing_azure_fs()
    except Exception as exc:
        log_fn(f"File-level listing unavailable ({exc}); scanning full month partition(s).")
        return [], month_globs

    discovered: list[str] = []
    fallback: list[str] = []
    for month_glob in month_globs:
        month_dir = month_glob.rsplit("/", 1)[0]
        list_path = month_dir.replace(ADLS_ROOT + "/", "default/")
        try:
            entries = fs.ls(list_path, detail=False)
        except Exception as exc:
            log_fn(f"Listing failed for {month_dir} ({exc}); scanning full month partition.")
            fallback.append(month_glob)
            continue

        matched_files: list[str] = []
        for entry in entries:
            name = entry.rstrip("/").rsplit("/", 1)[-1]
            if not name.lower().endswith(".parquet"):
                continue
            file_ts = parse_month_partition_filename_ts(name)
            if file_ts is None or (window_start <= file_ts <= window_end):
                matched_files.append(f"{month_dir}/{name}")

        if matched_files:
            log_fn(f"Selected {len(matched_files)}/{len(entries)} file(s) in {month_dir} within the time window.")
            discovered.extend(matched_files)
        else:
            log_fn(f"No filename-timestamp matches in {month_dir}; scanning full month partition as a safety net.")
            fallback.append(month_glob)

    return discovered, fallback


def _local_parquet_cache_path(remote_path: str) -> Path:
    suffix = remote_path.split(f"{DTC_GLOB_PREFIX}/", 1)[-1]
    return PARQUET_CACHE_DIR / suffix


def _prune_parquet_cache(max_bytes: int) -> None:
    try:
        files = sorted(
            (p for p in PARQUET_CACHE_DIR.rglob("*.parquet") if p.is_file()),
            key=lambda p: p.stat().st_mtime,
        )
    except Exception:
        return
    total = sum(p.stat().st_size for p in files if p.exists())
    for p in files:
        if total <= max_bytes:
            break
        try:
            size = p.stat().st_size
            p.unlink(missing_ok=True)
            total -= size
        except Exception:
            pass


def download_parquet_files_locally(remote_paths: list[str], log_fn) -> list[Path]:
    """
    Download discovered parquet partition files to a local cache via the same chunked,
    retrying fs.open() reader already proven reliable for DLT downloads, instead of relying
    on polars' native remote Parquet reads (observed to be slow/unstable over this link).
    Already-cached files (immutable once written) are reused without re-downloading.
    """
    if not remote_paths:
        return []
    try:
        fs = _get_listing_azure_fs()
        nuc = dynamic_import(
            SCRIPT_DIR.parent / "NucDltWindowDownloader" / "nuc_dlt_window_downloader.py",
            "nuc_downloader_module_for_listing",
        )
    except Exception as exc:
        log_fn(f"Local parquet cache unavailable ({exc}); falling back to remote reads.")
        return []

    attempts = max(1, int(getattr(nuc, "AZURE_DOWNLOAD_RETRY_ATTEMPTS", 4)))
    chunk_size = int(getattr(nuc, "IO_CHUNK_SIZE_AZURE", 8 * 1024 * 1024))
    local_paths: list[Path | None] = [None] * len(remote_paths)
    cache_hits = 0

    def fetch_one(idx: int, remote_path: str) -> None:
        nonlocal cache_hits
        local_path = _local_parquet_cache_path(remote_path)
        if local_path.exists() and local_path.stat().st_size > 0:
            local_paths[idx] = local_path
            cache_hits += 1
            return

        local_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = local_path.with_name(local_path.name + ".part")
        last_exc: Exception | None = None
        for attempt in range(1, attempts + 1):
            try:
                with fs.open(remote_path, "rb") as src, tmp_path.open("wb") as dst:
                    while True:
                        chunk = src.read(chunk_size)
                        if not chunk:
                            break
                        dst.write(chunk)
                tmp_path.replace(local_path)
                local_paths[idx] = local_path
                return
            except Exception as exc:
                last_exc = exc
                tmp_path.unlink(missing_ok=True)
                if attempt >= attempts:
                    break
                time.sleep(min(5.0, float(2 ** attempt)))
        log_fn(f"Failed to cache {remote_path} locally after {attempts} attempt(s): {last_exc}")

    max_workers = min(PARQUET_FETCH_WORKERS, len(remote_paths))
    to_fetch = [p for p in remote_paths if not _local_parquet_cache_path(p).exists()]
    if to_fetch:
        log_fn(f"Caching {len(to_fetch)}/{len(remote_paths)} new parquet file(s) locally ({max_workers} parallel worker(s))...")
    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(fetch_one, i, rp) for i, rp in enumerate(remote_paths)]
        concurrent.futures.wait(futures)

    result = [p for p in local_paths if p is not None]
    log_fn(f"Local parquet cache ready: {len(result)} file(s) ({cache_hits} already cached) in {time.time() - t0:.1f}s.")
    _prune_parquet_cache(PARQUET_CACHE_MAX_BYTES)
    return result


def get_storage_options(log_fn) -> dict[str, str]:
    import time
    from azure.identity import AzureCliCredential

    if TOKEN_CACHE_FILE.exists():
        try:
            cached = json.loads(TOKEN_CACHE_FILE.read_text(encoding="utf-8"))
            if float(cached.get("expires_at", 0)) > time.time() + 120:
                log_fn("Using cached Azure token.")
                return {"account_name": ACCOUNT, "bearer_token": cached["token"]}
        except Exception:
            pass

    log_fn("Fetching Azure token via Azure CLI...")
    cli_timeout_seconds = 45
    max_attempts = 3
    token = None
    last_exc: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            credential = AzureCliCredential(process_timeout=cli_timeout_seconds)
            token = credential.get_token("https://storage.azure.com/.default")
            break
        except Exception as exc:
            last_exc = exc
            if attempt >= max_attempts:
                break
            wait_s = min(8.0, float(2 ** attempt))
            log_fn(
                f"Azure CLI token fetch failed (attempt {attempt}/{max_attempts}); "
                f"retrying in {wait_s:.1f}s..."
            )
            time.sleep(wait_s)

    if token is None:
        raise RuntimeError(
            f"Failed to fetch Azure token via Azure CLI after {max_attempts} attempts "
            f"(timeout {cli_timeout_seconds}s per attempt)."
        ) from last_exc

    try:
        TOKEN_CACHE_FILE.write_text(
            json.dumps({"token": token.token, "expires_at": float(token.expires_on)}),
            encoding="utf-8",
        )
    except Exception:
        pass
    return {"account_name": ACCOUNT, "bearer_token": token.token}


def format_bytes(value: int) -> str:
    if value < 1024:
        return f"{value} B"
    units = ["KB", "MB", "GB", "TB"]
    current = float(value)
    for unit in units:
        current /= 1024.0
        if current < 1024.0:
            return f"{current:.1f} {unit}"
    return f"{current:.1f} PB"


def normalize_text_token(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", value).upper()


def detect_variant(raw_variant: str) -> str:
    value = (raw_variant or "").strip().upper()
    if value in {"HPA", "HPB"}:
        return value
    return "HPA"


def occurrence_event_ts_for_dlt(occurrence: Occurrence) -> dt.datetime:
    """
    Determine the UTC timestamp to center DLT file search on for this occurrence.

    Prefers the onboard "DTC time stamp" extended-data fields (dtc_ts21_utc/dtc_ts20_utc,
    sourced from TS21__UTC/TS20__UTC), which record when the ECU actually detected/
    confirmed this DTC, over event_ts which may reflect when the vehicle was read/polled
    (e.g. vtStart) rather than when the fault was actually triggered. Falls back to the
    legacy local-timestamp-column handling when those fields are unavailable.
    """
    if occurrence.dtc_ts21_utc is not None:
        return occurrence.dtc_ts21_utc
    if occurrence.dtc_ts20_utc is not None:
        return occurrence.dtc_ts20_utc

    ts = occurrence.event_ts
    source = (occurrence.source_ts_col or "").lower()
    local_columns = {"ts21_local", "ts20_local", "vtstart"}
    if "local" in source or source in local_columns:
        try:
            local_tz = ZoneInfo("Europe/Stockholm")
            local_dt = ts.replace(tzinfo=local_tz)
            return local_dt.astimezone(dt.timezone.utc).replace(tzinfo=None)
        except Exception:
            # Conservative fallback for summer-time datasets when timezone data is unavailable.
            return ts - dt.timedelta(hours=2)
    return ts


def occurrence_trigger_ts(occurrence: Occurrence) -> dt.datetime:
    """Return the best available timestamp for when the ECU set this DTC."""
    return occurrence_event_ts_for_dlt(occurrence)


def build_candidate_dlt_centers(occurrence: Occurrence) -> list[dt.datetime]:
    base = occurrence_trigger_ts(occurrence)
    raw = occurrence.event_ts
    candidates: list[dt.datetime] = []
    seen: set[str] = set()

    def add(ts: dt.datetime) -> None:
        key = ts.isoformat()
        if key in seen:
            return
        seen.add(key)
        candidates.append(ts)

    # Prioritize actual DTC trigger time(s) over the read/ingestion timestamp: base is
    # dtc_ts21_utc (most recent trigger) when available, dtc_ts20_utc is the other onboard
    # extended-data trigger timestamp, and raw is the read-time fallback used previously.
    add(base)
    if occurrence.dtc_ts20_utc is not None:
        add(occurrence.dtc_ts20_utc)
    add(raw)

    # Probe both converted and raw timestamps in both directions to cover
    # ambiguous local/UTC semantics and DST handling mismatches.
    for offset_hours in (-4, -3, -2, -1, 1, 2, 3, 4):
        add(base + dt.timedelta(hours=offset_hours))
        add(raw + dt.timedelta(hours=offset_hours))

    return candidates


def build_fast_attempt_dlt_centers(occurrence: Occurrence) -> list[dt.datetime]:
    base = occurrence_trigger_ts(occurrence)
    centers = [base]
    if occurrence.dtc_ts20_utc is not None and occurrence.dtc_ts20_utc != base:
        centers.append(occurrence.dtc_ts20_utc)
    raw = occurrence.event_ts
    if raw != base and raw not in centers:
        centers.append(raw)
    return centers


def select_relevant_dlt_candidates(
    all_candidates: list[tuple[str, str, int | None, dt.datetime]],
    center_ts: dt.datetime,
    max_count: int = 2,
) -> list[tuple[str, str, int | None]]:
    if not all_candidates:
        return []

    sorted_by_distance = sorted(
        all_candidates,
        key=lambda item: (abs((item[3] - center_ts).total_seconds()), item[3]),
    )
    selected: list[tuple[str, str, int | None]] = []
    seen_paths: set[str] = set()
    for item in sorted_by_distance:
        if item[1] in seen_paths:
            continue
        seen_paths.add(item[1])
        selected.append((item[0], item[1], item[2]))
        if len(selected) >= max_count:
            break
    return selected


def pick_adjacent_dlt_candidates(
    all_candidates: list[tuple[str, str, int | None, dt.datetime]],
    selected_remote_paths: list[str],
    max_per_side: int = 1,
) -> list[tuple[str, str, int | None]]:
    if not all_candidates or not selected_remote_paths or max_per_side <= 0:
        return []

    timeline: list[tuple[str, str, int | None, dt.datetime]] = []
    seen_remote: set[str] = set()
    for item in sorted(all_candidates, key=lambda x: (x[3], x[1])):
        if item[1] in seen_remote:
            continue
        seen_remote.add(item[1])
        timeline.append(item)

    if not timeline:
        return []

    index_by_remote = {item[1]: idx for idx, item in enumerate(timeline)}
    selected_set = set(selected_remote_paths)
    out: list[tuple[str, str, int | None]] = []
    out_seen: set[str] = set()

    for remote_path in selected_remote_paths:
        idx = index_by_remote.get(remote_path)
        if idx is None:
            continue

        # Explicitly probe one earlier and one later DLT around the selected file.
        for step in range(1, max_per_side + 1):
            prev_idx = idx - step
            if prev_idx >= 0:
                item = timeline[prev_idx]
                rp = item[1]
                if rp not in selected_set and rp not in out_seen:
                    out_seen.add(rp)
                    out.append((item[0], rp, item[2]))

        for step in range(1, max_per_side + 1):
            next_idx = idx + step
            if next_idx < len(timeline):
                item = timeline[next_idx]
                rp = item[1]
                if rp not in selected_set and rp not in out_seen:
                    out_seen.add(rp)
                    out.append((item[0], rp, item[2]))

    return out


def pick_first_after_dlt_candidate(
    all_candidates: list[tuple[str, str, int | None, dt.datetime]],
    center_ts: dt.datetime,
) -> tuple[str, str, int | None] | None:
    if not all_candidates:
        return None

    ordered = sorted(all_candidates, key=lambda x: (x[3], x[1]))
    for item in ordered:
        if item[3] > center_ts:
            return (item[0], item[1], item[2])
    return None


def pick_first_after_dlt_candidate_for_centers(
    all_candidates: list[tuple[str, str, int | None, dt.datetime]],
    centers: list[dt.datetime],
) -> list[tuple[str, str, int | None]]:
    out: list[tuple[str, str, int | None]] = []
    seen: set[str] = set()
    for center in centers:
        pick = pick_first_after_dlt_candidate(all_candidates, center)
        if pick is None or pick[1] in seen:
            continue
        seen.add(pick[1])
        out.append(pick)
    return out


def choose_first_column(existing: set[str], candidates: list[str]) -> str | None:
    for col in candidates:
        if col in existing:
            return col
    return None


def build_timestamp_expr_from_code(ts_col: str, ts_dtype_code: str) -> pl.Expr:
    code = (ts_dtype_code or "").strip()
    if code == "Date":
        return pl.col(ts_col).cast(pl.Datetime)
    if code == "Datetime":
        return pl.col(ts_col).cast(pl.Datetime)
    if code == "Epoch":
        return pl.from_epoch(pl.col(ts_col), time_unit="ms").cast(pl.Datetime)
    return pl.col(ts_col).cast(pl.Utf8).str.to_datetime(strict=False)


def fetch_occurrences(
    storage_options: dict[str, str],
    start_utc: dt.datetime,
    end_utc: dt.datetime,
    selected_dtcs: list[str],
    log_fn,
    refresh_storage_options_fn=None,
) -> tuple[list[Occurrence], str]:
    cache_key = build_occurrence_cache_key(start_utc, end_utc, selected_dtcs)
    cached = load_occurrence_cache(cache_key)
    if cached is not None:
        log_fn(f"Loaded occurrences from local cache ({len(cached[0])} rows).")
        return cached

    discovered_files, fallback_globs = build_month_globs_filtered(start_utc, end_utc, log_fn)
    # The user's frontend-style approach is the preferred path: pass only concrete,
    # filename-filtered remote files to polars so it can issue selective Parquet reads
    # without downloading whole files locally. Local caching remains an automatic fallback.
    globs = discovered_files + fallback_globs
    if not globs:
        return [], ""

    active_storage_options = dict(storage_options)
    direct_remote_read = bool(discovered_files) and not fallback_globs
    local_fallback_prepared = False

    def switch_to_local_parquet_fallback() -> None:
        nonlocal globs, direct_remote_read, local_fallback_prepared
        if local_fallback_prepared:
            return
        local_files = download_parquet_files_locally(discovered_files, log_fn)
        undownloaded = [p for p in discovered_files if _local_parquet_cache_path(p) not in local_files]
        globs = [str(p) for p in local_files] + undownloaded + fallback_globs
        direct_remote_read = False
        local_fallback_prepared = True
        log_fn("Switched to local parquet cache fallback after direct remote read failure.")

    def should_retry_azure_error(exc: Exception) -> bool:
        msg = str(exc).lower()
        return any(
            key in msg
            for key in [
                "object-store error",
                "microsoftazure",
                "error sending request",
                "http error",
                "unauthorized",
                "expired",
                "timed out",
                "timeout",
                "tempor",
                "connection reset",
            ]
        )

    def refresh_storage_options() -> None:
        nonlocal active_storage_options
        if refresh_storage_options_fn is None:
            return
        try:
            updated = refresh_storage_options_fn()
            if isinstance(updated, dict) and updated:
                active_storage_options = updated
                log_fn("Refreshed Azure storage credentials for occurrence query retry.")
        except Exception as refresh_exc:
            log_fn(f"Token refresh failed during retry: {refresh_exc}")

    def collect_with_retry(lazy_df: pl.LazyFrame, label: str) -> pl.DataFrame:
        nonlocal direct_remote_read
        for attempt in range(1, 4):
            try:
                return lazy_df.collect(streaming=True)
            except OSError as exc:
                if direct_remote_read:
                    log_fn(f"{label} direct remote read failed ({exc}); using local parquet fallback.")
                    switch_to_local_parquet_fallback()
                    raise
                if attempt >= 3 or not should_retry_azure_error(exc):
                    raise
                wait_s = min(5.0, float(2 ** attempt))
                log_fn(f"{label} failed (attempt {attempt}/3): {exc}")
                refresh_storage_options()
                time.sleep(wait_s)
        return lazy_df.collect(streaming=True)

    def collect_schema_with_retry() -> dict[str, pl.DataType]:
        nonlocal direct_remote_read
        for attempt in range(1, 4):
            try:
                return pl.scan_parquet(
                    globs,
                    storage_options=active_storage_options,
                    cast_options=PARQUET_SCAN_CAST_OPTIONS,
                ).collect_schema()
            except OSError as exc:
                if direct_remote_read:
                    log_fn(f"Schema direct remote read failed ({exc}); using local parquet fallback.")
                    switch_to_local_parquet_fallback()
                    return pl.scan_parquet(
                        globs,
                        storage_options=active_storage_options,
                        cast_options=PARQUET_SCAN_CAST_OPTIONS,
                    ).collect_schema()
                if attempt >= 3 or not should_retry_azure_error(exc):
                    raise
                wait_s = min(5.0, float(2 ** attempt))
                log_fn(f"Schema read failed (attempt {attempt}/3): {exc}")
                refresh_storage_options()
                time.sleep(wait_s)
        return pl.scan_parquet(
            globs,
            storage_options=active_storage_options,
            cast_options=PARQUET_SCAN_CAST_OPTIONS,
        ).collect_schema()

    log_fn(f"Scanning {len(globs)} parquet file/partition source(s)...")
    schema_cache = load_occurrence_schema_cache()
    vin_col: str | None = None
    dtc_col: str | None = None
    variant_col: str | None = None
    alt_col: str | None = None
    ecu_addr_col: str | None = None
    ts_col: str | None = None
    ts_dtype_code = "Utf8"
    confirmed_col: str | None = None
    pending_col: str | None = None
    test_failed_col: str | None = None
    dtc_dict_col: str | None = None
    ts20_utc_col: str | None = None
    ts21_utc_col: str | None = None
    schema: dict[str, pl.DataType] | None = None

    if schema_cache is not None:
        vin_col = schema_cache.get("vin_col") or None
        dtc_col = schema_cache.get("dtc_col") or None
        variant_col = schema_cache.get("variant_col") or None
        alt_col = schema_cache.get("alt_col") or None
        ecu_addr_col = schema_cache.get("ecu_addr_col") or None
        ts_col = schema_cache.get("ts_col") or None
        ts_dtype_code = schema_cache.get("ts_dtype_code") or "Utf8"
        confirmed_col = schema_cache.get("confirmed_col") or None
        pending_col = schema_cache.get("pending_col") or None
        test_failed_col = schema_cache.get("test_failed_col") or None
        dtc_dict_col = schema_cache.get("dtc_dict_col") or None
        ts20_utc_col = schema_cache.get("ts20_utc_col") or None
        ts21_utc_col = schema_cache.get("ts21_utc_col") or None
        if ts_col == "rvdc_ingestion_ts":
            log_fn("Cached timestamp column is ingestion time. Refreshing schema to prefer local event time columns.")
            schema_cache = None
            vin_col = None
            dtc_col = None
            variant_col = None
            alt_col = None
            ecu_addr_col = None
            ts_col = None
            ts_dtype_code = "Utf8"
            confirmed_col = None
            pending_col = None
            test_failed_col = None
            dtc_dict_col = None
            ts20_utc_col = None
            ts21_utc_col = None
        else:
            log_fn("Using cached parquet schema mapping.")

    if schema_cache is None:
        log_fn("Reading parquet schema (one-time; cached for next run)...")
        schema = collect_schema_with_retry()
        columns = set(schema)

        vin_col = choose_first_column(columns, ["pvin", "vin", "PVIN"])
        dtc_col = choose_first_column(columns, ["dtc_id", "dtcid", "DTC_ID"])
        variant_col = choose_first_column(columns, ["ecu", "variant", "ECU"])
        alt_col = choose_first_column(columns, ["dtc_altvalue", "dtc_alt", "pcbu_dtcid"])
        ecu_addr_col = choose_first_column(columns, ["ecuAddr", "ecu_addr", "ECUADDR"])
        confirmed_col = choose_first_column(columns, ["Confirmed", "confirmed"])
        pending_col = choose_first_column(columns, ["Pending", "pending"])
        test_failed_col = choose_first_column(columns, ["TestFailedSinceLastClear", "test_failed_since_last_clear"])
        dtc_dict_col = choose_first_column(columns, ["dtc_dict", "dtcDict", "DTC_DICT"])
        # Per-DTC onboard trigger timestamps (already UTC), distinct from vtStart/rvdc_ingestion_ts
        # which reflect when the vehicle was read/polled rather than when the fault occurred.
        ts21_utc_col = choose_first_column(columns, ["TS21__UTC", "TS21_UTC"])
        ts20_utc_col = choose_first_column(columns, ["TS20__UTC", "TS20_UTC"])

        ts_candidates = ["TS21_local", "TS20_local", "vtStart", "timestamp", "rvdc_ingestion_ts"]
        ts_col = choose_first_column(columns, ts_candidates)

        ts_dtype = schema[ts_col] if ts_col else pl.Utf8
        if ts_dtype == pl.Date:
            ts_dtype_code = "Date"
        elif hasattr(ts_dtype, "is_temporal") and ts_dtype.is_temporal():
            ts_dtype_code = "Datetime"
        elif ts_dtype in (pl.Int32, pl.Int64, pl.UInt32, pl.UInt64):
            ts_dtype_code = "Epoch"
        else:
            ts_dtype_code = "Utf8"

        save_occurrence_schema_cache(
            {
                "vin_col": vin_col or "",
                "dtc_col": dtc_col or "",
                "variant_col": variant_col or "",
                "alt_col": alt_col or "",
                "ecu_addr_col": ecu_addr_col or "",
                "ts_col": ts_col or "",
                "ts_dtype_code": ts_dtype_code,
                "confirmed_col": confirmed_col or "",
                "pending_col": pending_col or "",
                "test_failed_col": test_failed_col or "",
                "dtc_dict_col": dtc_dict_col or "",
                "ts20_utc_col": ts20_utc_col or "",
                "ts21_utc_col": ts21_utc_col or "",
            }
        )

    missing = []
    if vin_col is None:
        missing.append("VIN column (pvin/vin)")
    if dtc_col is None:
        missing.append("DTC column (dtc_id/dtcid)")
    if ts_col is None:
        missing.append("timestamp column")
    if missing:
        raise RuntimeError("Required columns missing: " + ", ".join(missing))

    ts_expr = build_timestamp_expr_from_code(ts_col, ts_dtype_code)

    select_exprs: list[pl.Expr] = [
        pl.col(vin_col).cast(pl.Utf8).alias("vin"),
        pl.col(dtc_col).cast(pl.Utf8).alias("dtc_id_raw"),
        ts_expr.alias("event_ts"),
    ]
    if variant_col is not None:
        select_exprs.append(pl.col(variant_col).cast(pl.Utf8).alias("variant_raw"))
    else:
        select_exprs.append(pl.lit("HPA").alias("variant_raw"))

    if alt_col is not None:
        select_exprs.append(pl.col(alt_col).cast(pl.Utf8).alias("dtc_alt_raw"))
    else:
        select_exprs.append(pl.lit("").alias("dtc_alt_raw"))

    if ecu_addr_col is not None:
        select_exprs.append(pl.col(ecu_addr_col).cast(pl.Utf8).alias("ecu_addr_raw"))
    else:
        select_exprs.append(pl.lit("").alias("ecu_addr_raw"))

    if confirmed_col is not None:
        select_exprs.append(pl.col(confirmed_col).cast(pl.Boolean).alias("confirmed_raw"))
    else:
        select_exprs.append(pl.lit(False).cast(pl.Boolean).alias("confirmed_raw"))

    if pending_col is not None:
        select_exprs.append(pl.col(pending_col).cast(pl.Boolean).alias("pending_raw"))
    else:
        select_exprs.append(pl.lit(False).cast(pl.Boolean).alias("pending_raw"))

    if test_failed_col is not None:
        select_exprs.append(pl.col(test_failed_col).cast(pl.Boolean).alias("test_failed_raw"))
    else:
        select_exprs.append(pl.lit(False).cast(pl.Boolean).alias("test_failed_raw"))

    if dtc_dict_col is not None:
        select_exprs.append(pl.col(dtc_dict_col).alias("dtc_dict_raw"))
    else:
        select_exprs.append(pl.lit(None).alias("dtc_dict_raw"))

    if ts20_utc_col is not None:
        select_exprs.append(pl.col(ts20_utc_col).cast(pl.Datetime).alias("dtc_ts20_utc_raw"))
    else:
        select_exprs.append(pl.lit(None).cast(pl.Datetime).alias("dtc_ts20_utc_raw"))

    if ts21_utc_col is not None:
        select_exprs.append(pl.col(ts21_utc_col).cast(pl.Datetime).alias("dtc_ts21_utc_raw"))
    else:
        select_exprs.append(pl.lit(None).cast(pl.Datetime).alias("dtc_ts21_utc_raw"))

    normalized_targets = sorted(set(selected_dtcs))
    def build_base_lazy(files: list[str]) -> pl.LazyFrame:
        return (
            pl.scan_parquet(
                files,
                storage_options=active_storage_options,
                cast_options=PARQUET_SCAN_CAST_OPTIONS,
            )
            .select(select_exprs)
            .filter(
                (pl.col("event_ts") >= pl.lit(start_utc))
                & (pl.col("event_ts") <= pl.lit(end_utc))
            )
        )

    def build_fast_filtered(files: list[str]) -> pl.LazyFrame:
        base = build_base_lazy(files)
        return (
            base
            .with_columns([
                pl.col("dtc_id_raw").cast(pl.Utf8).str.to_uppercase().alias("dtc_id_fast"),
                pl.col("dtc_alt_raw").cast(pl.Utf8).str.to_uppercase().alias("dtc_alt_fast"),
            ])
            .filter(
                pl.col("dtc_id_fast").is_in(normalized_targets)
                | pl.col("dtc_alt_fast").is_in(normalized_targets)
            )
            .drop(["dtc_id_fast", "dtc_alt_fast"])
        )

    def build_normalized_filtered(files: list[str]) -> pl.LazyFrame:
        base = build_base_lazy(files)
        return (
            base
            .with_columns([
                pl.col("dtc_id_raw").cast(pl.Utf8).str.replace_all(r"[^A-Za-z0-9]", "").str.to_uppercase().alias("dtc_id_norm"),
                pl.col("dtc_alt_raw").cast(pl.Utf8).str.replace_all(r"[^A-Za-z0-9]", "").str.to_uppercase().alias("dtc_alt_norm"),
            ])
            .filter(
                pl.col("dtc_id_norm").is_in(normalized_targets)
                | pl.col("dtc_alt_norm").is_in(normalized_targets)
            )
            .drop(["dtc_id_norm", "dtc_alt_norm"])
        )

    def collect_parallel_by_file(files: list[str], build_lazy_fn, label: str) -> pl.DataFrame:
        # Azure round-trip latency per file (not file size) dominates wall time here, so
        # fetch multiple discovered files concurrently instead of one combined serial scan.
        if len(files) <= 1:
            return collect_with_retry(build_lazy_fn(files), label)

        max_workers = min(PARQUET_FETCH_WORKERS, len(files))
        log_fn(f"{label}: fetching {len(files)} file(s) with {max_workers} parallel worker(s)...")
        results: list[pl.DataFrame] = []
        results_lock = threading.Lock()
        first_exc: list[Exception] = []

        def fetch_one(file_path: str) -> None:
            try:
                file_label = f"{label} ({file_path.rsplit('/', 1)[-1]})"
                df = collect_with_retry(build_lazy_fn([file_path]), file_label)
                with results_lock:
                    results.append(df)
            except Exception as exc:
                with results_lock:
                    if not first_exc:
                        first_exc.append(exc)

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            list(executor.map(fetch_one, files))

        if not results:
            if first_exc:
                raise first_exc[0]
            return build_lazy_fn(files[:1]).collect()
        return pl.concat(results, how="vertical_relaxed")

    def collect_occurrence_frame(build_lazy_fn, label: str) -> pl.DataFrame:
        if direct_remote_read:
            try:
                return collect_with_retry(build_lazy_fn(globs), label)
            except OSError:
                # collect_with_retry switched the source list to local paths.
                return collect_parallel_by_file(globs, build_lazy_fn, label)
        return collect_parallel_by_file(globs, build_lazy_fn, label)

    log_fn("Collecting occurrences (fast exact match path)...")
    df = collect_occurrence_frame(build_fast_filtered, "Fast occurrence collect")

    # Fallback: normalized alnum-only match for variant spellings.
    if df.is_empty():
        log_fn("No rows in fast path. Retrying with normalized match...")
        df = collect_occurrence_frame(build_normalized_filtered, "Normalized occurrence collect")
    if df.is_empty():
        return [], ts_col

    records = sorted(
        df.to_dicts(),
        key=lambda row: (
            row.get("event_ts") if isinstance(row.get("event_ts"), dt.datetime) else dt.datetime.max,
            str(row.get("vin") or ""),
            str(row.get("dtc_id_raw") or ""),
        ),
    )
    occurrences: list[Occurrence] = []
    seen: set[tuple[str, str, str, str]] = set()
    occurrence_by_key: dict[tuple[str, str, str, str], Occurrence] = {}
    occurrence_index_by_key: dict[tuple[str, str, str, str], int] = {}

    for row in records:
        vin = (row.get("vin") or "").strip().upper()
        if not vin:
            continue

        event_ts = row.get("event_ts")
        if not isinstance(event_ts, dt.datetime):
            continue
        if event_ts.tzinfo is not None:
            event_ts = event_ts.astimezone(dt.timezone.utc).replace(tzinfo=None)

        def _normalize_utc_naive(value: Any) -> dt.datetime | None:
            if not isinstance(value, dt.datetime):
                return None
            if value.tzinfo is not None:
                return value.astimezone(dt.timezone.utc).replace(tzinfo=None)
            return value

        dtc_ts20_utc = _normalize_utc_naive(row.get("dtc_ts20_utc_raw"))
        dtc_ts21_utc = _normalize_utc_naive(row.get("dtc_ts21_utc_raw"))

        dtc_id = normalize_text_token(str(row.get("dtc_id_raw") or ""))
        dtc_alt = normalize_text_token(str(row.get("dtc_alt_raw") or ""))
        variant = detect_variant(str(row.get("variant_raw") or ""))
        ecu_addr = normalize_text_token(str(row.get("ecu_addr_raw") or ""))
        confirmed = bool(row.get("confirmed_raw") or False)
        pending = bool(row.get("pending_raw") or False)
        test_failed_since_last_clear = bool(row.get("test_failed_raw") or False)
        dtc_dict_raw = row.get("dtc_dict_raw")

        status_byte_b0 = parse_dtc_status_byte_flag(dtc_dict_raw, "null/null/status_byte_b0_TestFailed")
        status_byte_b1 = parse_dtc_status_byte_flag(dtc_dict_raw, "null/null/status_byte_b1_TestFailedThisOperationCycle")
        status_byte_b2 = parse_dtc_status_byte_flag(dtc_dict_raw, "null/null/status_byte_b2_Pending")
        status_byte_b3 = parse_dtc_status_byte_flag(dtc_dict_raw, "null/null/status_byte_b3_Confirmed")
        status_byte_b4 = parse_dtc_status_byte_flag(dtc_dict_raw, "null/null/status_byte_b4_TestNotCompletedSinceLastClear")
        status_byte_b5 = parse_dtc_status_byte_flag(dtc_dict_raw, "null/null/status_byte_b5_TestFailedSinceLastClear")
        status_byte_b6 = parse_dtc_status_byte_flag(dtc_dict_raw, "null/null/status_byte_b6_TestNotCompletedThisOperationCycle")
        status_byte_b7 = parse_dtc_status_byte_flag(dtc_dict_raw, "null/null/status_byte_b7_WarningIndicatorRequested")

        if status_byte_b2 is None:
            status_byte_b2 = pending
        if status_byte_b3 is None:
            status_byte_b3 = confirmed
        if status_byte_b5 is None:
            status_byte_b5 = test_failed_since_last_clear

        trigger_ts = dtc_ts21_utc or dtc_ts20_utc or event_ts
        dedupe_key = (vin, dtc_id or dtc_alt, variant, trigger_ts.isoformat())
        if dedupe_key in seen:
            existing = occurrence_by_key[dedupe_key]
            updated = dc_replace(existing, read_count=existing.read_count + 1)
            occurrence_by_key[dedupe_key] = updated
            occurrences[occurrence_index_by_key[dedupe_key]] = updated
            continue
        seen.add(dedupe_key)

        occurrences.append(
            Occurrence(
                vin=vin,
                variant=variant,
                dtc_id=dtc_id,
                dtc_altvalue=dtc_alt,
                ecu_addr=ecu_addr,
                event_ts=event_ts,
                source_ts_col=ts_col,
                confirmed=confirmed,
                pending=pending,
                test_failed_since_last_clear=test_failed_since_last_clear,
                status_byte_b0_test_failed=status_byte_b0,
                status_byte_b1_test_failed_this_cycle=status_byte_b1,
                status_byte_b2_pending=status_byte_b2,
                status_byte_b3_confirmed=status_byte_b3,
                status_byte_b4_test_not_completed_since_last_clear=status_byte_b4,
                status_byte_b5_test_failed_since_last_clear=status_byte_b5,
                status_byte_b6_test_not_completed_this_cycle=status_byte_b6,
                status_byte_b7_warning_indicator_requested=status_byte_b7,
                dtc_ts20_utc=dtc_ts20_utc,
                dtc_ts21_utc=dtc_ts21_utc,
                read_count=1,
            )
        )
        occurrence_by_key[dedupe_key] = occurrences[-1]
        occurrence_index_by_key[dedupe_key] = len(occurrences) - 1

    occurrences.sort(key=lambda x: (x.event_ts, x.vin, x.dtc_id))
    save_occurrence_cache(cache_key, ts_col, occurrences)
    return occurrences, ts_col


def build_dtc_tokens(occ: Occurrence) -> list[str]:
    tokens: set[str] = set()
    for raw in [occ.dtc_id, occ.dtc_altvalue]:
        token = normalize_text_token(raw)
        if not token:
            continue
        tokens.add(token.lower())
        tokens.add(raw.lower())
        if token.startswith(("D", "U", "B", "C")) and len(token) > 1:
            body = token[1:]
            tokens.add(body.lower())
            # Heuristic: some DTC renderings insert an extra nibble in hex-like forms
            # (example: D50996 can appear as D50A96 / 0xD50A96 in DLT).
            if re.fullmatch(r"[A-F0-9]{5}", body):
                expanded = f"{body[:2]}A{body[2:]}"
                tokens.add(f"{token[0]}{expanded}".lower())
                tokens.add(expanded.lower())
                tokens.add(f"0x{token[0]}{expanded}".lower())
                tokens.add(f"0x{expanded}".lower())
            if re.fullmatch(r"[A-F0-9]{6}", body):
                tokens.add(f"0x{token[0]}{body}".lower())
                tokens.add(f"0x{body}".lower())
        if re.fullmatch(r"[A-F0-9]{5,8}", token):
            tokens.add(f"0x{token.lower()}")

    return [t for t in tokens if t]


def safe_rel_link(target: Path, base: Path) -> str:
    rel = os.path.relpath(target, base)
    return rel.replace("\\", "/")


def _esc(value: str) -> str:
    return html.escape(value, quote=True)


def _peek_magic_bytes(path: Path, size: int = 8) -> bytes:
    try:
        with path.open("rb") as f:
            return f.read(size)
    except Exception:
        return b""


def detect_compression_magic(path: Path) -> str | None:
    magic = _peek_magic_bytes(path, size=8)
    if magic.startswith(b"PK"):
        return "zip"
    if magic.startswith(b"\x1f\x8b"):
        return "gz"
    if magic.startswith(b"BZ"):
        return "bz2"
    if magic.startswith(b"\xfd7zXZ\x00"):
        return "xz"
    if magic.startswith(ZSTD_MAGIC):
        return "zst"
    return None


def is_raw_dlt_payload(path: Path) -> bool:
    return _peek_magic_bytes(path, size=4).startswith(DLT_STORAGE_MAGIC)


def decompress_zst_stream_to_file(source: Path, destination: Path) -> bool:
    if not HAS_ZSTANDARD:
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        dctx = zstandard.ZstdDecompressor()
        with source.open("rb") as src:
            with destination.open("wb") as dst:
                with dctx.stream_reader(src) as reader:
                    shutil.copyfileobj(reader, dst, length=1024 * 1024)
                dst.flush()
        return True
    except Exception:
        destination.unlink(missing_ok=True)
        return False


class _PrefixedByteStream:
    """Wraps a network stream so already-peeked bytes are replayed before further reads."""

    def __init__(self, prefix: bytes, stream: Any) -> None:
        self._prefix = prefix
        self._stream = stream

    def read(self, size: int = -1) -> bytes:
        if not self._prefix:
            return self._stream.read(size)
        if size is None or size < 0:
            chunk, self._prefix = self._prefix, b""
            rest = self._stream.read()
            return chunk + (rest or b"")
        chunk, self._prefix = self._prefix[:size], self._prefix[size:]
        if len(chunk) < size:
            rest = self._stream.read(size - len(chunk))
            chunk += rest or b""
        return chunk


def stream_decompress_remote_zst_to_file(
    azure_fs,
    remote_path: str,
    destination: Path,
    io_semaphore: threading.Semaphore | None = None,
) -> tuple[bool, bytes]:
    """
    Attempt to read a remote zstd payload directly from Azure and decompress it straight
    to `destination`, without ever writing the compressed archive to local disk.
    Returns (success, peeked_magic_bytes). On failure/non-zstd magic, caller should fall
    back to the download-then-extract path.
    """
    if not HAS_ZSTANDARD:
        return False, b""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if io_semaphore is not None:
        io_semaphore.acquire()
    try:
        with azure_fs.open(remote_path, "rb") as src:
            magic = src.read(8)
            if not magic.startswith(ZSTD_MAGIC):
                return False, magic
            dctx = zstandard.ZstdDecompressor()
            prefixed = _PrefixedByteStream(magic, src)
            with destination.open("wb") as dst:
                with dctx.stream_reader(prefixed) as reader:
                    shutil.copyfileobj(reader, dst, length=1024 * 1024)
                dst.flush()
        return True, magic
    except Exception:
        destination.unlink(missing_ok=True)
        return False, b""
    finally:
        if io_semaphore is not None:
            io_semaphore.release()


def extract_with_7zip_cli(archive_path: Path, output_dir: Path) -> list[Path]:
    """
    Best-effort fallback extraction using an installed 7zip CLI.
    Returns extracted .dlt paths, or an empty list if unavailable/failure.
    """
    tools = ["7z", "7za", "7zr"]
    tool = next((t for t in tools if shutil.which(t)), None)
    if tool is None:
        return []

    output_dir.mkdir(parents=True, exist_ok=True)
    before = {p.resolve() for p in output_dir.rglob("*.dlt") if p.exists()}
    cmd = [tool, "x", "-y", f"-o{output_dir}", str(archive_path)]
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=300,
            check=False,
        )
        if proc.returncode != 0:
            return []
    except Exception:
        return []

    after = [p for p in output_dir.rglob("*.dlt") if p.exists()]
    created = [p for p in after if p.resolve() not in before]
    if created:
        return created
    return after


def scan_messages_for_match(
    occurrence: Occurrence,
    dlt_file: Path,
    messages: list[tuple[Any, ...]],
    reasons: list[str],
) -> MatchResult:
    def detect_camera_state_after_reason(
        from_index: int,
        from_ts_us: int | None,
        camera_tag: str | None,
    ) -> tuple[str | None, str | None, float | None]:
        state_patterns: list[tuple[str, re.Pattern[str]]] = [
            ("Deactivated", re.compile(r"\\bdeactivat(?:ed|e|ion)?\\b", re.IGNORECASE)),
            ("selfhealing", re.compile(r"self[\\s_-]*healing", re.IGNORECASE)),
            ("relinking", re.compile(r"\\brelink(?:ing)?\\b", re.IGNORECASE)),
            ("streaming", re.compile(r"\\bstream(?:ing)?\\b", re.IGNORECASE)),
            ("cooldown", re.compile(r"cool[\\s_-]*down", re.IGNORECASE)),
        ]

        max_scan_lines = 200_000
        max_time_delta_us = 30_000_000

        best_same: tuple[int, str, str] | None = None
        best_any: tuple[int, str, str] | None = None

        end_idx = min(len(messages), from_index + max_scan_lines + 1)
        for idx in range(from_index + 1, end_idx):
            line = str(messages[idx][7])
            matched_state: str | None = None
            for state_name, pattern in state_patterns:
                if pattern.search(line):
                    matched_state = state_name
                    break
            if matched_state is None:
                continue

            ts_us = message_epoch_us(messages[idx])
            if from_ts_us is not None and ts_us is not None:
                delta_us = ts_us - from_ts_us
                if delta_us < 0:
                    continue
                if delta_us > max_time_delta_us:
                    continue
                rank = int(delta_us)
            else:
                rank = idx - from_index

            candidate = (rank, matched_state, line)
            if camera_tag and camera_tag in line.upper():
                if best_same is None or candidate[0] < best_same[0]:
                    best_same = candidate
            else:
                if best_any is None or candidate[0] < best_any[0]:
                    best_any = candidate

        pick = best_same or best_any
        if pick is None:
            return None, None, None

        delta_seconds = None if from_ts_us is None else pick[0] / 1_000_000.0
        return pick[1], pick[2], delta_seconds

    if not messages:
        return MatchResult(
            occurrence=occurrence,
            dlt_file=dlt_file,
            dtc_line=None,
            reason=None,
            reason_line=None,
            reason_offset_lines=None,
            dlt_line_index=None,
            status="NO_DTC_LINE",
        )

    reason_map = {r.lower(): r for r in reasons}
    reason_pattern = re.compile(
        "|".join(re.escape(token) for token in sorted(reasons, key=len, reverse=True)),
        re.IGNORECASE,
    )
    tokens = build_dtc_tokens(occurrence)

    best_idx: int | None = None
    best_score = -1
    best_line = ""

    for idx, msg in enumerate(messages):
        line = str(msg[7])
        low = line.lower()
        token_hits = [tok for tok in tokens if tok in low]

        # Do not consider lines that have no DTC token evidence.
        if not token_hits:
            continue

        # Hard requirement: only FAILED entries are valid DTC report lines.
        if "reported status failed" not in low:
            continue

        score = 0
        score += min(10, len(token_hits) * 5)
        if "setevent" in low:
            score += 2
        score += 2
        if "dtc" in low:
            score += 1

        if score > best_score and score >= 5:
            best_score = score
            best_idx = idx
            best_line = line

    if best_idx is None:
        baseline_summary, baseline_delta_seconds = find_confighub_baseline(messages, None)
        return MatchResult(
            occurrence=occurrence,
            dlt_file=dlt_file,
            dtc_line=None,
            reason=None,
            reason_line=None,
            reason_offset_lines=None,
            dlt_line_index=None,
            baseline_summary=baseline_summary,
            baseline_time_delta_seconds=baseline_delta_seconds,
            baseline_source="DIRECT" if baseline_summary else None,
            status="NO_FAILED_DTC_LINE",
        )

    dtc_line = best_line
    dtc_msg = messages[best_idx]
    dtc_ts_us = message_epoch_us(dtc_msg)
    camera_match = re.search(r"Z_(SRCB|SRCF|SRCL|SRCR)_", dtc_line, re.IGNORECASE)
    target_camera = camera_match.group(1).upper() if camera_match else None
    baseline_summary, baseline_delta_seconds = find_confighub_baseline(messages, best_idx)
    max_time_delta_us = 15_000_000

    nearest_reason: str | None = None
    nearest_line: str | None = None
    nearest_offset: int | None = None
    best_reason_score: tuple[int, int, int, int] | None = None

    for idx, msg in enumerate(messages):
        if idx == best_idx:
            continue

        line = str(msg[7])
        match = reason_pattern.search(line)
        if not match:
            continue

        reason_text = reason_map.get(match.group(0).lower(), match.group(0))

        ts_us = message_epoch_us(msg)
        if dtc_ts_us is not None and ts_us is not None:
            delta_us = ts_us - dtc_ts_us
            abs_delta_us = abs(delta_us)
            if abs_delta_us > max_time_delta_us:
                continue
            direction_penalty = 0 if delta_us <= 0 else 1
        else:
            abs_delta_us = abs(idx - best_idx)
            direction_penalty = 0 if idx <= best_idx else 1

        camera_penalty = 0
        if target_camera:
            camera_penalty = 0 if target_camera in line.upper() else 1

        score = (camera_penalty, abs_delta_us, direction_penalty, abs(idx - best_idx))
        if best_reason_score is None or score < best_reason_score:
            best_reason_score = score
            nearest_reason = reason_text
            nearest_line = line
            nearest_offset = idx - best_idx

    if nearest_reason is None:
        # Fallback for logs where message timestamps are missing or malformed.
        start = max(0, best_idx - 120)
        end = min(len(messages), best_idx + 121)
        for idx in range(start, end):
            if idx == best_idx:
                continue
            line = str(messages[idx][7])
            match = reason_pattern.search(line)
            if not match:
                continue
            nearest_reason = reason_map.get(match.group(0).lower(), match.group(0))
            nearest_line = line
            nearest_offset = idx - best_idx
            break

    reason_delta_seconds: float | None = None
    camera_state: str | None = None
    camera_state_line: str | None = None
    camera_state_delta_seconds: float | None = None

    if nearest_offset is not None:
        reason_idx = best_idx + nearest_offset
        if 0 <= reason_idx < len(messages):
            reason_ts_us = message_epoch_us(messages[reason_idx])
            if dtc_ts_us is not None and reason_ts_us is not None:
                reason_delta_seconds = (reason_ts_us - dtc_ts_us) / 1_000_000.0

            camera_state, camera_state_line, camera_state_delta_seconds = detect_camera_state_after_reason(
                reason_idx,
                reason_ts_us,
                target_camera,
            )

    return MatchResult(
        occurrence=occurrence,
        dlt_file=dlt_file,
        dtc_line=best_line,
        reason=nearest_reason,
        reason_line=nearest_line,
        reason_offset_lines=nearest_offset,
        reason_time_delta_seconds=reason_delta_seconds,
        camera_state=camera_state,
        camera_state_line=camera_state_line,
        camera_state_time_delta_seconds=camera_state_delta_seconds,
        baseline_summary=baseline_summary,
        baseline_time_delta_seconds=baseline_delta_seconds,
        baseline_source="DIRECT" if baseline_summary else None,
        dlt_line_index=best_idx,
        status="MAPPED" if nearest_reason else "UNMAPPED",
    )


def build_html_report(
    start_utc: dt.datetime,
    end_utc: dt.datetime,
    selected_dtcs: list[str],
    matches: list[MatchResult],
    failures: list[str],
    report_path: Path,
) -> tuple[str, set[Path]]:
    mapped: dict[tuple[str, str, str], GroupedMapped] = {}
    unmapped: list[MatchResult] = []
    referenced: set[Path] = set()

    for match in matches:
        if match.dlt_file:
            referenced.add(match.dlt_file)
        occ = match.occurrence
        if match.reason:
            key = (occ.vin, occ.dtc_id or occ.dtc_altvalue, match.reason)
            group = mapped.get(key)
            if group is None:
                group = GroupedMapped(vin=occ.vin, dtc_id=occ.dtc_id or occ.dtc_altvalue, reason=match.reason)
                mapped[key] = group
            group.count += 1
            group.days.add(occurrence_trigger_ts(occ).date().isoformat())
            if match.dlt_file:
                group.files.add(match.dlt_file)
        else:
            unmapped.append(match)

    generated_utc = dt.datetime.utcnow().isoformat() + "Z"
    mapped_total = sum(group.count for group in mapped.values())
    total_dtc_reads = sum(max(1, item.occurrence.read_count) for item in matches)

    def failed_found_text(item: MatchResult) -> str:
        if item.status in {"MAPPED", "UNMAPPED"} and (item.dtc_line or "").strip():
            return "YES"
        if item.status == "SKIPPED_STATUS_GATE":
            return "N/A (LEGACY CHECKPOINT)"
        if item.status == "NO_DLT":
            return "NO (NO DLT)"
        if item.status == "NO_DLT_EXTRACT_FAILED":
            return "NO (EXTRACT FAILED)"
        if item.status == "NO_FAILED_DTC_LINE_WITH_EXTRACT_FAILURE":
            return "NO (EXTRACT FAILED IN CANDIDATES)"
        return "NO"

    def mapping_attempted_text(item: MatchResult) -> str:
        return "NO (LEGACY CHECKPOINT)" if item.status == "SKIPPED_STATUS_GATE" else "YES"

    def unmapped_note_text(item: MatchResult) -> str:
        if item.status == "SKIPPED_STATUS_GATE":
            return "Legacy checkpoint result created before status-gate skipping was removed."
        if item.status in {"NO_DLT_EXTRACT_FAILED", "NO_FAILED_DTC_LINE_WITH_EXTRACT_FAILURE"}:
            return (item.error or "Extraction failed for at least one candidate DLT payload")[:220]
        if item.status == "ERROR" and item.error:
            return item.error[:220]
        return ""

    def short_line(text: str | None, limit: int = 180) -> str:
        if not text:
            return ""
        return text if len(text) <= limit else (text[: limit - 3] + "...")

    def format_delta(value: float | None) -> str:
        if value is None:
            return ""
        return f"{value:.3f}"

    def trigger_time_text(occ: Occurrence) -> str:
        return occurrence_trigger_ts(occ).isoformat()

    def dtc_status_badges(occ: Occurrence) -> str:
        parts: list[str] = []
        if occ.confirmed:
            parts.append('<span class="badge badge-confirmed">Confirmed</span>')
        if occ.pending:
            parts.append('<span class="badge badge-pending">Pending</span>')
        if occ.test_failed_since_last_clear:
            parts.append('<span class="badge badge-testfailed">FailedSinceClr</span>')
        return "".join(parts) if parts else '<span style="color:#9ca3af">—</span>'

    def bit_to_text(value: bool | None) -> str:
        if value is True:
            return "1"
        if value is False:
            return "0"
        return "?"

    def status_byte_summary(occ: Occurrence) -> str:
        return (
            f"TestFailed={bit_to_text(occ.status_byte_b0_test_failed)} | "
            f"TestFailedThisOperationCycle={bit_to_text(occ.status_byte_b1_test_failed_this_cycle)} | "
            f"Pending={bit_to_text(occ.status_byte_b2_pending)} | "
            f"Confirmed={bit_to_text(occ.status_byte_b3_confirmed)} | "
            f"TestNotCompletedSinceLastClear={bit_to_text(occ.status_byte_b4_test_not_completed_since_last_clear)} | "
            f"TestFailedSinceLastClear={bit_to_text(occ.status_byte_b5_test_failed_since_last_clear)} | "
            f"TestNotCompletedThisOperationCycle={bit_to_text(occ.status_byte_b6_test_not_completed_this_cycle)} | "
            f"WarningIndicatorRequested={bit_to_text(occ.status_byte_b7_warning_indicator_requested)}"
        )

    def row_class(occ: Occurrence) -> str:
        return ' class="confirmed"' if occ.confirmed else ""

    lines: list[str] = [
        "<!doctype html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"utf-8\">",
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
        "  <title>DTC to DLT Fault Correlation Report</title>",
        "  <style>",
        "    body { font-family: Segoe UI, Tahoma, Arial, sans-serif; margin: 20px; color: #1f2937; }",
        "    h1, h2 { margin-bottom: 8px; }",
        "    .meta { margin: 0 0 16px 0; padding: 10px 12px; background: #f4f6f8; border: 1px solid #d8dde3; border-radius: 6px; }",
        "    .meta p { margin: 4px 0; }",
        "    table { border-collapse: collapse; width: 100%; margin-bottom: 18px; }",
        "    th, td { border: 1px solid #d8dde3; padding: 8px; text-align: left; vertical-align: top; }",
        "    th { background: #eef2f6; }",
        "    .small { color: #6b7280; font-size: 12px; }",
        "    ul { margin-top: 6px; }",
        "    tr.confirmed { background-color: #fffbeb; }",
        "    tr.confirmed td { border-left-color: #f59e0b; }",
        "    tr.confirmed td:first-child { border-left: 3px solid #f59e0b; }",
        "    .badge { display: inline-block; padding: 1px 6px; border-radius: 10px; font-size: 11px; font-weight: 600; margin-right: 3px; }",
        "    .badge-confirmed { background: #fef3c7; color: #92400e; border: 1px solid #fcd34d; }",
        "    .badge-pending { background: #e0f2fe; color: #0c4a6e; border: 1px solid #7dd3fc; }",
        "    .badge-testfailed { background: #fce7f3; color: #831843; border: 1px solid #f9a8d4; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <h1>DTC to DLT Fault Correlation Report</h1>",
        "  <div class=\"meta\">",
        f"    <p><strong>Generated:</strong> {_esc(generated_utc)}</p>",
        f"    <p><strong>Analysis range (UTC):</strong> {_esc(start_utc.isoformat())} to {_esc(end_utc.isoformat())}</p>",
        f"    <p><strong>Requested DTCs:</strong> {_esc(', '.join(selected_dtcs))}</p>",
        f"    <p><strong>Total DTC reads:</strong> {total_dtc_reads}</p>",
        f"    <p><strong>Unique DTC occurrences:</strong> {len(matches)}</p>",
        f"    <p><strong>Mapped occurrences:</strong> {mapped_total}</p>",
        f"    <p><strong>Unmapped occurrences:</strong> {len(unmapped)}</p>",
        "    <p><strong>ConfigHub baseline signal:</strong> Correlated from DLT messages containing SPA*_INT-style tokens (for example SPA2_INT, SPA3_INT, SPA2/3_INT).</p>",
        "  </div>",
        "",
        "  <h2>Grouped Mapped Fault Reasons</h2>",
    ]

    if mapped:
        lines.extend([
            "  <table>",
            "    <thead><tr><th>VIN</th><th>DTC</th><th>Fault Reason</th><th>Occurrences</th><th>Days</th><th>DLT Files</th></tr></thead>",
            "    <tbody>",
        ])
        for key in sorted(mapped.keys()):
            group = mapped[key]
            link_html: list[str] = []
            for file_path in sorted(group.files):
                rel = _esc(safe_rel_link(file_path, report_path.parent))
                label = _esc(file_path.name)
                link_html.append(f"<a href=\"{rel}\">{label}</a>")
            lines.append(
                "      <tr>"
                f"<td>{_esc(group.vin)}</td>"
                f"<td>{_esc(group.dtc_id)}</td>"
                f"<td>{_esc(group.reason)}</td>"
                f"<td>{group.count}</td>"
                f"<td>{len(group.days)}</td>"
                f"<td>{'<br>'.join(link_html)}</td>"
                "</tr>"
            )
        lines.extend(["    </tbody>", "  </table>"])
    else:
        lines.append("  <p>No mapped fault reasons found.</p>")

    correlation_rows = [
        item
        for item in matches
        if item.reason and (item.status in {"MAPPED", "UNMAPPED"}) and (item.dtc_line or "").strip()
    ]
    lines.append("  <h2>Correlation Details</h2>")
    if correlation_rows:
        lines.extend([
            "  <table>",
            "    <thead><tr><th>DTC Trigger Time (UTC)</th><th>Read Time (UTC)</th><th>VIN</th><th>DTC</th><th>DTC Status</th><th>Status Byte (B0..B7)</th><th>DLT File</th><th>ConfigHub Baseline</th><th>Baseline Source</th><th>Baseline Delta (s)</th><th>Correlated Reason</th><th>Correlated Line</th><th>Reason Delta (s)</th><th>Camera State</th><th>State Line</th><th>State Delta From Reason (s)</th></tr></thead>",
            "    <tbody>",
        ])
        for item in correlation_rows:
            occ = item.occurrence
            if item.dlt_file:
                rel = _esc(safe_rel_link(item.dlt_file, report_path.parent))
                label = _esc(item.dlt_file.name)
                dlt_cell = f"<a href=\"{rel}\">{label}</a>"
            else:
                dlt_cell = "-"
            lines.append(
                f"      <tr{row_class(occ)}>"
                f"<td>{_esc(trigger_time_text(occ))}</td>"
                f"<td>{_esc(occ.event_ts.isoformat())}</td>"
                f"<td>{_esc(occ.vin)}</td>"
                f"<td>{_esc(occ.dtc_id or occ.dtc_altvalue)}</td>"
                f"<td>{dtc_status_badges(occ)}</td>"
                f"<td>{_esc(status_byte_summary(occ))}</td>"
                f"<td>{dlt_cell}</td>"
                f"<td>{_esc(short_line(item.baseline_summary, 220))}</td>"
                f"<td>{_esc(item.baseline_source or '')}</td>"
                f"<td>{_esc(format_delta(item.baseline_time_delta_seconds))}</td>"
                f"<td>{_esc(item.reason or '')}</td>"
                f"<td>{_esc(short_line(item.reason_line))}</td>"
                f"<td>{_esc(format_delta(item.reason_time_delta_seconds))}</td>"
                f"<td>{_esc(item.camera_state or '')}</td>"
                f"<td>{_esc(short_line(item.camera_state_line))}</td>"
                f"<td>{_esc(format_delta(item.camera_state_time_delta_seconds))}</td>"
                "</tr>"
            )
        lines.extend(["    </tbody>", "  </table>"])
    else:
        lines.append("  <p>No correlated reason details available.</p>")

    unmapped_test_failed = [item for item in unmapped if item.occurrence.status_byte_b0_test_failed is True]
    unmapped_other = [item for item in unmapped if item.occurrence.status_byte_b0_test_failed is not True]

    def append_unmapped_table(title: str, items: list[MatchResult]) -> None:
        lines.append(f"  <h2>{_esc(title)}</h2>")
        if not items:
            lines.append("  <p>None</p>")
            return
        lines.extend([
            "  <table>",
            "    <thead><tr><th>DTC Trigger Time (UTC)</th><th>Read Time (UTC)</th><th>VIN</th><th>DTC</th><th>DTC Status</th><th>Status Byte (B0..B7)</th><th>DLT Mapping Attempted</th><th>DLT File</th><th>ConfigHub Baseline</th><th>Baseline Source</th><th>FAILED DTC Found</th><th>DTC Line</th><th>Note</th></tr></thead>",
            "    <tbody>",
        ])
        for item in items:
            occ = item.occurrence
            if item.dlt_file:
                rel = _esc(safe_rel_link(item.dlt_file, report_path.parent))
                label = _esc(item.dlt_file.name)
                dlt_cell = f"<a href=\"{rel}\">{label}</a>"
            else:
                dlt_cell = "-"
            dtc_line = item.dtc_line or ""
            if len(dtc_line) > 140:
                dtc_line = dtc_line[:137] + "..."
            lines.append(
                f"      <tr{row_class(occ)}>"
                f"<td>{_esc(trigger_time_text(occ))}</td>"
                f"<td>{_esc(occ.event_ts.isoformat())}</td>"
                f"<td>{_esc(occ.vin)}</td>"
                f"<td>{_esc(occ.dtc_id or occ.dtc_altvalue)}</td>"
                f"<td>{dtc_status_badges(occ)}</td>"
                f"<td>{_esc(status_byte_summary(occ))}</td>"
                f"<td>{_esc(mapping_attempted_text(item))}</td>"
                f"<td>{dlt_cell}</td>"
                f"<td>{_esc(short_line(item.baseline_summary, 220))}</td>"
                f"<td>{_esc(item.baseline_source or '')}</td>"
                f"<td>{_esc(failed_found_text(item))}</td>"
                f"<td>{_esc(dtc_line)}</td>"
                f"<td>{_esc(unmapped_note_text(item))}</td>"
                "</tr>"
            )
        lines.extend(["    </tbody>", "  </table>"])

    append_unmapped_table("Unmapped DTCs (testFailed == 1)", unmapped_test_failed)
    append_unmapped_table("Other Unmapped DTCs (testFailed == 0 or unknown)", unmapped_other)

    lines.append("  <h2>Failures</h2>")
    if failures:
        lines.append("  <ul>")
        for failure in failures:
            lines.append(f"    <li>{_esc(failure)}</li>")
        lines.append("  </ul>")
    else:
        lines.append("  <p>None</p>")

    lines.extend([
        "  <p class=\"small\">Links are relative to this report file and open local DLT artifacts.</p>",
        "</body>",
        "</html>",
        "",
    ])

    return "\n".join(lines), referenced


def compute_storage_summary(run_dir: Path, referenced_paths: set[Path]) -> StorageSummary:
    total_files = 0
    total_bytes = 0
    referenced_files = 0
    referenced_bytes = 0

    existing_referenced = {p.resolve() for p in referenced_paths if p.exists()}

    for path in run_dir.rglob("*"):
        if not path.is_file():
            continue
        total_files += 1
        size = path.stat().st_size
        total_bytes += size
        if path.resolve() in existing_referenced:
            referenced_files += 1
            referenced_bytes += size

    return StorageSummary(
        total_files=total_files,
        total_bytes=total_bytes,
        referenced_files=referenced_files,
        referenced_bytes=referenced_bytes,
    )


def cleanup_all_downloads(run_dir: Path, keep_files: set[Path]) -> tuple[int, int]:
    deleted_files = 0
    deleted_bytes = 0
    keep_resolved = {p.resolve() for p in keep_files}

    for path in run_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.resolve() in keep_resolved:
            continue
        size = path.stat().st_size
        path.unlink(missing_ok=True)
        deleted_files += 1
        deleted_bytes += size

    for path in sorted(run_dir.rglob("*"), reverse=True):
        if path.is_dir():
            try:
                path.rmdir()
            except OSError:
                pass

    return deleted_files, deleted_bytes


def cleanup_keep_referenced(run_dir: Path, referenced_paths: set[Path], keep_files: set[Path]) -> tuple[int, int]:
    deleted_files = 0
    deleted_bytes = 0
    keep_resolved = {p.resolve() for p in keep_files}
    keep_resolved.update({p.resolve() for p in referenced_paths if p.exists()})

    for path in run_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.resolve() in keep_resolved:
            continue
        size = path.stat().st_size
        path.unlink(missing_ok=True)
        deleted_files += 1
        deleted_bytes += size

    for path in sorted(run_dir.rglob("*"), reverse=True):
        if path.is_dir():
            try:
                path.rmdir()
            except OSError:
                pass

    return deleted_files, deleted_bytes


class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("DTC to DLT Fault Correlator")
        self.root.geometry("1280x780")

        self.log_queue: queue.Queue[tuple[str, str]] = queue.Queue()
        self.cancel_event = threading.Event()
        self.worker: threading.Thread | None = None

        self.referenced_paths: set[Path] = set()
        self.keep_artifacts: set[Path] = set()
        self.last_run_dir: Path | None = None
        self.last_report_path: Path | None = None
        self._azure_variant_path_cache: dict[tuple[str, str], str | None] = {}
        self._azure_day_listing_cache: dict[str, list[tuple[str, str, dt.datetime]]] = {}
        self._remote_payload_cache: dict[str, list[str]] = {}
        self._remote_payload_lock = threading.Lock()
        self._keyed_locks: dict[Any, threading.Lock] = {}
        self._keyed_locks_meta_lock = threading.Lock()
        # Bounds total concurrent Azure network streams across the main occurrence loop
        # and background prefetch workers combined, to avoid connection storms/throttling.
        self._azure_io_semaphore = threading.BoundedSemaphore(MAX_CONCURRENT_AZURE_STREAMS)

        self.nuc_module = dynamic_import(
            SCRIPT_DIR.parent / "NucDltWindowDownloader" / "nuc_dlt_window_downloader.py",
            "nuc_downloader_module",
        )
        self.dlt_parser_module = dynamic_import(
            SCRIPT_DIR.parent / "DLTSearcher" / "dlt_searcher_gui.py",
            "dlt_searcher_module",
        )

        self.fault_reasons = load_fault_reasons(FAULT_CATALOG_FILE)
        self.settings = load_settings()

        self._build_ui()
        self._apply_settings()
        self.root.after(120, self._drain_log_queue)

    def _build_ui(self) -> None:
        top = ttk.Frame(self.root, padding=8)
        top.pack(fill=tk.X)

        ttk.Label(top, text="Analysis Window").grid(row=0, column=0, sticky="w", padx=(0, 6), pady=4)
        self.window_mode_var = tk.StringVar(value="7d")
        self.window_mode_combo = ttk.Combobox(
            top,
            textvariable=self.window_mode_var,
            values=WINDOW_OPTIONS,
            state="readonly",
            width=10,
        )
        self.window_mode_combo.grid(row=0, column=1, sticky="w", pady=4)
        self.window_mode_combo.bind("<<ComboboxSelected>>", lambda _e: self._update_manual_fields_state())

        ttk.Label(top, text="Manual Start (UTC)").grid(row=0, column=2, sticky="w", padx=(12, 6), pady=4)
        self.manual_start_var = tk.StringVar()
        self.manual_start_entry = ttk.Entry(top, textvariable=self.manual_start_var, width=22)
        self.manual_start_entry.grid(row=0, column=3, sticky="w", pady=4)

        ttk.Label(top, text="Manual End (UTC)").grid(row=0, column=4, sticky="w", padx=(12, 6), pady=4)
        self.manual_end_var = tk.StringVar()
        self.manual_end_entry = ttk.Entry(top, textvariable=self.manual_end_var, width=22)
        self.manual_end_entry.grid(row=0, column=5, sticky="w", pady=4)

        ttk.Label(top, text="DTC List").grid(row=1, column=0, sticky="w", padx=(0, 6), pady=4)
        self.dtc_list_var = tk.StringVar()
        self.dtc_entry = ttk.Entry(top, textvariable=self.dtc_list_var, width=70)
        self.dtc_entry.grid(row=1, column=1, columnspan=3, sticky="ew", pady=4)

        ttk.Label(top, text="Output Folder").grid(row=2, column=0, sticky="w", padx=(0, 6), pady=4)
        self.output_dir_var = tk.StringVar()
        self.output_entry = ttk.Entry(top, textvariable=self.output_dir_var, width=90)
        self.output_entry.grid(row=2, column=1, columnspan=4, sticky="ew", pady=4)
        ttk.Button(top, text="Browse", command=self._browse_output).grid(row=2, column=5, sticky="w", pady=4)

        controls = ttk.Frame(self.root, padding=(8, 0, 8, 6))
        controls.pack(fill=tk.X)
        self.run_button = ttk.Button(controls, text="Run Analysis", command=self._start_run)
        self.run_button.pack(side=tk.LEFT)
        self.stop_button = ttk.Button(controls, text="Stop", command=self._stop_run, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(6, 0))

        self.cleanup_all_button = ttk.Button(
            controls,
            text="Cleanup All Downloaded Files",
            command=self._cleanup_all,
            state=tk.DISABLED,
        )
        self.cleanup_all_button.pack(side=tk.LEFT, padx=(18, 0))

        self.cleanup_keep_button = ttk.Button(
            controls,
            text="Keep Only Report-Referenced DLT Files",
            command=self._cleanup_keep_referenced,
            state=tk.DISABLED,
        )
        self.cleanup_keep_button.pack(side=tk.LEFT, padx=(6, 0))

        self.open_report_button = ttk.Button(
            controls,
            text="Open Report",
            command=self._open_report,
            state=tk.DISABLED,
        )
        self.open_report_button.pack(side=tk.LEFT, padx=(18, 0))

        storage = ttk.Frame(self.root, padding=(8, 0, 8, 6))
        storage.pack(fill=tk.X)
        self.storage_var = tk.StringVar(value="Storage: no run yet")
        ttk.Label(storage, textvariable=self.storage_var).pack(side=tk.LEFT)

        log_frame = ttk.Frame(self.root, padding=8)
        log_frame.pack(fill=tk.BOTH, expand=True)
        self.log_text = tk.Text(log_frame, wrap="word")
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        top.columnconfigure(3, weight=1)

    def _apply_settings(self) -> None:
        s = self.settings
        self.window_mode_var.set(str(s.get("window_mode", "7d")))
        self.manual_start_var.set(str(s.get("manual_start", DEFAULT_SETTINGS["manual_start"])))
        self.manual_end_var.set(str(s.get("manual_end", DEFAULT_SETTINGS["manual_end"])))
        self.dtc_list_var.set(str(s.get("dtc_list", "D50996")))
        self.output_dir_var.set(str(s.get("output_dir", DEFAULT_SETTINGS["output_dir"])))
        self._update_manual_fields_state()

    def _collect_settings(self) -> dict[str, Any]:
        return {
            "window_mode": self.window_mode_var.get().strip(),
            "manual_start": self.manual_start_var.get().strip(),
            "manual_end": self.manual_end_var.get().strip(),
            "dtc_list": self.dtc_list_var.get().strip(),
            "output_dir": self.output_dir_var.get().strip(),
        }

    def _update_manual_fields_state(self) -> None:
        manual = self.window_mode_var.get().strip() == "Manual"
        state = "normal" if manual else "disabled"
        self.manual_start_entry.configure(state=state)
        self.manual_end_entry.configure(state=state)

    def _browse_output(self) -> None:
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_dir_var.set(folder)

    def _append_log(self, text: str) -> None:
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)

    def _queue_log(self, level: str, message: str) -> None:
        self.log_queue.put((level, message))

    def _drain_log_queue(self) -> None:
        while True:
            try:
                level, msg = self.log_queue.get_nowait()
            except queue.Empty:
                break
            prefix = {
                "info": "[INFO]",
                "ok": "[ OK ]",
                "err": "[ERR ]",
                "dim": "[ ...]",
            }.get(level, "[INFO]")
            self._append_log(f"{prefix} {msg}")
        self.root.after(120, self._drain_log_queue)

    def _show_incomplete_runs_manager(self, output_dir: Path) -> Path | None:
        result: dict[str, Path | None] = {"checkpoint": None}
        dialog = tk.Toplevel(self.root)
        dialog.title("Incomplete analysis runs")
        dialog.transient(self.root)
        dialog.geometry("820x360")
        dialog.minsize(680, 280)
        dialog.grab_set()

        body = ttk.Frame(dialog, padding=16)
        body.grid(row=0, column=0, sticky="nsew")
        dialog.columnconfigure(0, weight=1)
        dialog.rowconfigure(0, weight=1)
        body.columnconfigure(0, weight=1)
        body.rowconfigure(1, weight=1)

        ttk.Label(body, text="Select an incomplete run to resume, remove selected stale runs, or start a new analysis.").grid(
            row=0, column=0, sticky="w", pady=(0, 10)
        )
        columns = ("run", "progress", "updated", "dtcs")
        tree = ttk.Treeview(body, columns=columns, show="headings", selectmode="browse")
        tree.heading("run", text="Run")
        tree.heading("progress", text="Progress")
        tree.heading("updated", text="Last Updated (UTC)")
        tree.heading("dtcs", text="DTCs")
        tree.column("run", width=195, stretch=False)
        tree.column("progress", width=105, stretch=False)
        tree.column("updated", width=185, stretch=False)
        tree.column("dtcs", width=290, stretch=True)
        tree.grid(row=1, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(body, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        tree.configure(yscrollcommand=scrollbar.set)

        def refresh() -> None:
            tree.delete(*tree.get_children())
            for checkpoint_path in find_incomplete_checkpoints(output_dir):
                data = load_analysis_checkpoint(checkpoint_path) or {}
                next_index = int(data.get("next_index", 0) or 0)
                total = len(data.get("ordered_occurrences", []))
                progress = f"{next_index}/{total}" if total else str(next_index)
                updated = str(data.get("updated_utc", ""))
                dtcs = ", ".join(str(dtc) for dtc in data.get("selected_dtcs", [])[:6])
                if len(data.get("selected_dtcs", [])) > 6:
                    dtcs += " ..."
                tree.insert("", tk.END, iid=str(checkpoint_path), values=(checkpoint_path.parent.name, progress, updated, dtcs))
            children = tree.get_children()
            if children:
                tree.selection_set(children[0])

        def selected_checkpoint() -> Path | None:
            selected = tree.selection()
            return Path(selected[0]) if selected else None

        def resume_selected() -> None:
            checkpoint_path = selected_checkpoint()
            if checkpoint_path is None:
                messagebox.showinfo("Select a run", "Select an incomplete run to resume.", parent=dialog)
                return
            result["checkpoint"] = checkpoint_path
            dialog.destroy()

        def remove_selected() -> None:
            checkpoint_path = selected_checkpoint()
            if checkpoint_path is None:
                messagebox.showinfo("Select a run", "Select an incomplete run to remove.", parent=dialog)
                return
            if not messagebox.askyesno("Remove progress", f"Remove all files for:\n{checkpoint_path.parent.name}?", parent=dialog):
                return
            if self._remove_incomplete_run(checkpoint_path, output_dir):
                refresh()

        def remove_all() -> None:
            checkpoints = find_incomplete_checkpoints(output_dir)
            if not checkpoints:
                return
            if not messagebox.askyesno(
                "Remove all progress",
                f"Remove all files for {len(checkpoints)} incomplete run(s)?",
                parent=dialog,
            ):
                return
            failures = [path for path in checkpoints if not self._remove_incomplete_run(path, output_dir)]
            refresh()
            if failures:
                messagebox.showerror("Some progress was not removed", f"Could not remove {len(failures)} run(s).", parent=dialog)

        buttons = ttk.Frame(body)
        buttons.grid(row=2, column=0, columnspan=2, sticky="e", pady=(12, 0))
        ttk.Button(buttons, text="Start New Analysis", command=dialog.destroy).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(buttons, text="Remove All", command=remove_all).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(buttons, text="Remove Selected", command=remove_selected).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(buttons, text="Resume Selected", command=resume_selected).grid(row=0, column=3)
        tree.bind("<Double-1>", lambda _event: resume_selected())
        dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
        refresh()
        self.root.wait_window(dialog)
        return result["checkpoint"]

    def _remove_incomplete_run(self, checkpoint_path: Path, output_dir: Path) -> bool:
        run_dir = checkpoint_path.parent.resolve()
        if run_dir.parent != output_dir.resolve() or not run_dir.name.startswith("run_"):
            messagebox.showerror("Cannot remove progress", "The incomplete run folder is outside the configured output directory.")
            return False
        try:
            shutil.rmtree(run_dir)
        except Exception as exc:
            messagebox.showerror("Cannot remove progress", f"Could not remove:\n{run_dir}\n\n{exc}")
            return False
        return True

    def _start_run(self) -> None:
        if self.worker and self.worker.is_alive():
            return

        try:
            settings = self._collect_settings()
        except Exception as exc:
            messagebox.showerror("Invalid settings", str(exc))
            return

        if not parse_dtc_list(settings["dtc_list"]):
            messagebox.showerror("Missing DTC list", "Provide at least one DTC.")
            return

        output_dir = Path(settings["output_dir"]).expanduser().resolve()
        if find_incomplete_checkpoints(output_dir):
            checkpoint_path = self._show_incomplete_runs_manager(output_dir)
            if checkpoint_path is not None:
                settings["resume_checkpoint_path"] = str(checkpoint_path)
            else:
                settings.pop("resume_checkpoint_path", None)

        save_settings(settings)

        self.cancel_event.clear()
        self.run_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        self.cleanup_all_button.configure(state=tk.DISABLED)
        self.cleanup_keep_button.configure(state=tk.DISABLED)
        self.open_report_button.configure(state=tk.DISABLED)

        self.worker = threading.Thread(target=self._run_analysis, args=(settings,), daemon=True)
        self.worker.start()

    def _stop_run(self) -> None:
        self.cancel_event.set()
        self._queue_log("dim", "Stop requested.")

    def _analysis_range_from_settings(self, settings: dict[str, Any]) -> tuple[dt.datetime, dt.datetime]:
        mode = str(settings["window_mode"])
        manual_start = None
        manual_end = None
        if mode == "Manual":
            manual_start = parse_manual_datetime(str(settings["manual_start"]))
            manual_end = parse_manual_datetime(str(settings["manual_end"]))
        now_utc = dt.datetime.utcnow()
        return resolve_analysis_range(mode, manual_start, manual_end, now_utc)

    def _ensure_not_cancelled(self) -> None:
        if self.cancel_event.is_set():
            raise RuntimeError("Run cancelled by user")

    def _get_keyed_lock(self, key: Any) -> threading.Lock:
        # Serializes concurrent work (e.g. main loop vs. background prefetch) targeting
        # the same Azure listing/payload key without blocking unrelated keys.
        with self._keyed_locks_meta_lock:
            lock = self._keyed_locks.get(key)
            if lock is None:
                lock = threading.Lock()
                self._keyed_locks[key] = lock
            return lock

    def _order_occurrences_for_reuse(self, occurrences: list[Occurrence]) -> list[Occurrence]:
        # Group adjacent work by VIN/variant/day so discovery and payload caches hit more often.
        return sorted(
            occurrences,
            key=lambda occ: (occ.vin, occ.variant, occ.event_ts.date().isoformat(), occ.event_ts),
        )

    def _download_occurrence_files(
        self,
        azure_fs,
        occurrence: Occurrence,
        center_ts: dt.datetime,
        run_dir: Path,
        max_new_files: int,
        include_adjacent_neighbors: bool = False,
        attempt_mode: str = "standard",
        adjacent_span: int = 1,
    ) -> DownloadBatchResult:
        nuc = self.nuc_module
        output_raw = run_dir / "raw" / occurrence.vin / occurrence.variant
        output_extracted = run_dir / "extracted" / occurrence.vin / occurrence.variant
        output_raw.mkdir(parents=True, exist_ok=True)
        output_extracted.mkdir(parents=True, exist_ok=True)

        variant_cache_key = (occurrence.vin, occurrence.variant)
        variant_path = self._azure_variant_path_cache.get(variant_cache_key)
        if variant_path is None:
            # Serialize discovery per VIN/variant so a background prefetch thread and the
            # main loop don't issue duplicate Azure listing calls for the same vehicle.
            with self._get_keyed_lock(("variant", variant_cache_key)):
                variant_path = self._azure_variant_path_cache.get(variant_cache_key)
                if variant_path is None:
                    azure_vin = nuc.azure_find_child_name(azure_fs, nuc.AZURE_NUC_ROOT, occurrence.vin)
                    if not azure_vin:
                        self._azure_variant_path_cache[variant_cache_key] = None
                        return DownloadBatchResult(files=[])

                    vin_root_path = f"{nuc.AZURE_NUC_ROOT}/{azure_vin}"
                    dlt_dir = nuc.azure_find_dlt_dir_name(azure_fs, vin_root_path)
                    if not dlt_dir:
                        self._azure_variant_path_cache[variant_cache_key] = None
                        return DownloadBatchResult(files=[])

                    variant_root = f"{vin_root_path}/{dlt_dir}"
                    variant_name = nuc.azure_find_child_name(azure_fs, variant_root, occurrence.variant)
                    if not variant_name:
                        self._azure_variant_path_cache[variant_cache_key] = None
                        return DownloadBatchResult(files=[])

                    variant_path = f"{variant_root}/{variant_name}"
                    self._azure_variant_path_cache[variant_cache_key] = variant_path

        if not variant_path:
            return DownloadBatchResult(files=[])

        matched: list[tuple[str, str, int | None]] = []
        all_candidates: list[tuple[str, str, int | None, dt.datetime]] = []

        candidate_centers = (
            build_candidate_dlt_centers(occurrence)
            if attempt_mode == "standard"
            else build_fast_attempt_dlt_centers(occurrence)
        )
        scan_start_day = min(candidate_centers).date()
        scan_end_day = max(candidate_centers).date()
        for day in nuc.daterange(scan_start_day, scan_end_day):
            self._ensure_not_cancelled()
            day_path = f"{variant_path}/{day.year:04d}/{day.month:02d}/{day.day:02d}"
            day_entries = self._azure_day_listing_cache.get(day_path)
            if day_entries is None:
                with self._get_keyed_lock(("day", day_path)):
                    day_entries = self._azure_day_listing_cache.get(day_path)
                    if day_entries is None:
                        day_entries = []
                        for file_name, file_size in nuc.azure_list_files(azure_fs, day_path):
                            if not nuc.is_supported_dlt_payload_name(file_name):
                                continue
                            file_ts = nuc.parse_filename_timestamp(file_name)
                            if file_ts is None:
                                continue
                            day_entries.append((file_name, f"{day_path}/{file_name}", file_ts, file_size))
                        self._azure_day_listing_cache[day_path] = day_entries

            for entry in day_entries:
                if len(entry) == 4:
                    file_name, remote_path, file_ts, file_size = entry
                else:
                    file_name, remote_path, file_ts = entry
                    file_size = None
                all_candidates.append((file_name, remote_path, file_size, file_ts))

        selected_center: dt.datetime | None = None
        seen_remote_paths: set[str] = set()
        matched = []
        if attempt_mode != "standard":
            first_after = pick_first_after_dlt_candidate_for_centers(
                all_candidates,
                [occurrence.event_ts, occurrence_event_ts_for_dlt(occurrence)],
            )
            for pick in first_after:
                remote_path = pick[1]
                if remote_path in seen_remote_paths:
                    continue
                seen_remote_paths.add(remote_path)
                matched.append(pick)
                if len(matched) >= MAX_DLT_CANDIDATES_PER_OCCURRENCE:
                    break

        for candidate_center in candidate_centers if attempt_mode == "standard" else []:
            if attempt_mode == "standard":
                per_center_count = 2 if max_new_files <= MAX_DLT_FILES_PER_VEHICLE else 4
            else:
                per_center_count = 1
            picks = select_relevant_dlt_candidates(
                all_candidates,
                candidate_center,
                max_count=per_center_count,
            )
            if picks and selected_center is None:
                selected_center = candidate_center
            for pick in picks:
                remote_path = pick[1]
                if remote_path in seen_remote_paths:
                    continue
                seen_remote_paths.add(remote_path)
                matched.append(pick)
                if len(matched) >= MAX_DLT_CANDIDATES_PER_OCCURRENCE:
                    break
            if len(matched) >= MAX_DLT_CANDIDATES_PER_OCCURRENCE:
                break

        if matched and selected_center is not None:
            self._queue_log(
                "dim",
                f"Selected DLT by UTC file-start rule around {selected_center.isoformat()} (source column {occurrence.source_ts_col}).",
            )

        if attempt_mode == "standard" and include_adjacent_neighbors and matched:
            adjacent = pick_adjacent_dlt_candidates(
                all_candidates,
                [item[1] for item in matched],
                max_per_side=max(1, int(adjacent_span)),
            )
            for pick in adjacent:
                remote_path = pick[1]
                if remote_path in seen_remote_paths:
                    continue
                seen_remote_paths.add(remote_path)
                matched.append(pick)
                if len(matched) >= MAX_DLT_CANDIDATES_PER_OCCURRENCE:
                    break

        if max_new_files <= 0:
            return DownloadBatchResult(files=[])

        matched = matched[:max_new_files]
        if not matched:
            return DownloadBatchResult(files=[])

        extraction_failures: list[str] = []
        extraction_failures_lock = threading.Lock()

        def record_extraction_failure(file_name: str, reason: str) -> None:
            with extraction_failures_lock:
                extraction_failures.append(f"{file_name}: {reason}")

        def download_with_retry(remote_path: str, local_raw: Path, remote_size: int | None) -> None:
            attempts = max(1, int(getattr(nuc, "AZURE_DOWNLOAD_RETRY_ATTEMPTS", 4)))
            chunk_size = int(getattr(nuc, "IO_CHUNK_SIZE_AZURE", 8 * 1024 * 1024))
            temp_path = local_raw.with_name(local_raw.name + ".part")

            for attempt in range(1, attempts + 1):
                self._ensure_not_cancelled()
                try:
                    current_size = temp_path.stat().st_size if temp_path.exists() else 0
                    if remote_size is not None and current_size > remote_size:
                        temp_path.unlink(missing_ok=True)
                        current_size = 0

                    self._azure_io_semaphore.acquire()
                    try:
                        with azure_fs.open(remote_path, "rb") as src, temp_path.open("ab") as dst:
                            if current_size > 0:
                                try:
                                    src.seek(current_size)
                                except Exception:
                                    remaining_skip = current_size
                                    while remaining_skip > 0:
                                        skip_chunk = src.read(min(chunk_size, remaining_skip))
                                        if not skip_chunk:
                                            raise RuntimeError("Failed to skip to resume offset")
                                        remaining_skip -= len(skip_chunk)

                            while True:
                                self._ensure_not_cancelled()
                                chunk = src.read(chunk_size)
                                if not chunk:
                                    break
                                dst.write(chunk)
                    finally:
                        self._azure_io_semaphore.release()

                    final_size = temp_path.stat().st_size if temp_path.exists() else 0
                    if remote_size is not None and final_size < remote_size:
                        raise RuntimeError(f"Incomplete download {final_size}/{remote_size} bytes")

                    temp_path.replace(local_raw)
                    return
                except Exception as exc:
                    transient = bool(getattr(nuc, "is_transient_network_error", lambda _e: True)(exc))
                    if attempt >= attempts or not transient:
                        raise
                    wait_s = min(5.0, float(2 ** min(attempt, 3)))
                    self._queue_log("dim", f"Retry {attempt}/{attempts} for {local_raw.name}: {exc}")
                    time.sleep(wait_s)

        def process_payload(file_name: str, remote_path: str, remote_size: int | None) -> list[Path]:
            # Serialize per-remote-path work so a background prefetch thread and the main
            # loop never download/decompress the same payload concurrently.
            with self._remote_payload_lock:
                cached = self._remote_payload_cache.get(remote_path)
            if cached:
                cached_paths = [Path(p) for p in cached if Path(p).exists()]
                if cached_paths:
                    return cached_paths
            with self._get_keyed_lock(("payload", remote_path)):
                return _process_payload_locked(file_name, remote_path, remote_size)

        def _process_payload_locked(file_name: str, remote_path: str, remote_size: int | None) -> list[Path]:
            out: list[Path] = []
            self._ensure_not_cancelled()

            with self._remote_payload_lock:
                cached = self._remote_payload_cache.get(remote_path)
            if cached:
                cached_paths = [Path(p) for p in cached if Path(p).exists()]
                if cached_paths:
                    return cached_paths

            # Fastest path: if this payload has already been extracted in this run,
            # reuse the existing .dlt directly and skip any download.
            existing_target = nuc.get_single_file_dlt_counterpart_path(file_name, output_extracted)
            if existing_target is not None:
                if (
                    existing_target.exists()
                    and existing_target.name.lower().endswith(".dlt")
                    and nuc.get_compression_format(existing_target) is None
                    and is_raw_dlt_payload(existing_target)
                ):
                    out.append(existing_target)
                    with self._remote_payload_lock:
                        self._remote_payload_cache[remote_path] = [str(p.resolve()) for p in out if p.exists()]
                    return out

            local_raw = output_raw / file_name

            # Fastest path: stream directly from Azure and decompress in-flight, so the
            # compressed archive never touches local disk (saves a full download+read pass).
            if not local_raw.exists():
                fast_target = nuc.get_single_file_dlt_counterpart_path(file_name, output_extracted)
                if fast_target is None:
                    fast_target = output_extracted / Path(file_name).stem
                    if not fast_target.name.lower().endswith(".dlt"):
                        fast_target = fast_target.with_suffix(fast_target.suffix + ".dlt")
                if not (
                    fast_target.exists()
                    and fast_target.name.lower().endswith(".dlt")
                    and nuc.get_compression_format(fast_target) is None
                    and is_raw_dlt_payload(fast_target)
                ):
                    fast_target.unlink(missing_ok=True)
                    stream_ok, _peeked = stream_decompress_remote_zst_to_file(
                        azure_fs, remote_path, fast_target, io_semaphore=self._azure_io_semaphore
                    )
                    if stream_ok and is_raw_dlt_payload(fast_target) and nuc.get_compression_format(fast_target) is None:
                        out.append(fast_target)
                        with self._remote_payload_lock:
                            self._remote_payload_cache[remote_path] = [str(p.resolve()) for p in out if p.exists()]
                        return out
                    fast_target.unlink(missing_ok=True)

            if not local_raw.exists():
                download_with_retry(remote_path, local_raw, remote_size)

            def adopt_raw_dlt_file(raw_path: Path) -> Path:
                if raw_path.name.lower().endswith(".dlt"):
                    return raw_path
                target = nuc.get_single_file_dlt_counterpart_path(raw_path.name, output_extracted)
                if target is None:
                    target = output_extracted / raw_path.stem
                    if not target.name.lower().endswith(".dlt"):
                        target = target.with_suffix(target.suffix + ".dlt")
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    raw_path.unlink(missing_ok=True)
                    return target
                shutil.move(str(raw_path), str(target))
                return target

            if is_raw_dlt_payload(local_raw):
                adopted = adopt_raw_dlt_file(local_raw)
                out.append(adopted)
                with self._remote_payload_lock:
                    self._remote_payload_cache[remote_path] = [str(p.resolve()) for p in out if p.exists()]
                return out

            magic_fmt = detect_compression_magic(local_raw)
            fmt = magic_fmt or nuc.get_compression_format(local_raw)

            # Some payloads are compressed but still named with a .dlt extension.
            # Trust magic-byte detection over filename extension before parsing.
            if fmt is None and local_raw.name.lower().endswith(".dlt"):
                out.append(local_raw)
                return out

            if not fmt:
                return out

            if fmt == "zst":
                if magic_fmt is not None and magic_fmt != "zst":
                    self._queue_log("dim", f"Skipping unexpected non-zstd payload for {local_raw.name} (magic={magic_fmt}).")
                    return out

                def keep_only_uncompressed_dlt(paths: list[Path]) -> list[Path]:
                    good: list[Path] = []
                    for p in paths:
                        if not p.exists() or not p.name.lower().endswith(".dlt"):
                            continue
                        if nuc.get_compression_format(p) is not None:
                            p.unlink(missing_ok=True)
                            continue
                        good.append(p)
                    return good

                first_exc: Exception | None = None
                stream_target = nuc.get_single_file_dlt_counterpart_path(local_raw.name, output_extracted)
                if stream_target is None:
                    stream_target = output_extracted / local_raw.stem
                    if not stream_target.name.lower().endswith(".dlt"):
                        stream_target = stream_target.with_suffix(stream_target.suffix + ".dlt")

                # Fast path: if a validated extracted file already exists, reuse it.
                if (
                    stream_target.exists()
                    and stream_target.name.lower().endswith(".dlt")
                    and nuc.get_compression_format(stream_target) is None
                    and is_raw_dlt_payload(stream_target)
                ):
                    out.append(stream_target)
                    local_raw.unlink(missing_ok=True)
                    with self._remote_payload_lock:
                        self._remote_payload_cache[remote_path] = [str(p.resolve()) for p in out if p.exists()]
                    return out

                for attempt in (1, 2):
                    try:
                        stream_target.unlink(missing_ok=True)
                        ok = decompress_zst_stream_to_file(local_raw, stream_target)
                        if not ok:
                            if first_exc is None:
                                first_exc = RuntimeError(f"decompress_zst_stream_to_file returned False for {local_raw.name}")
                        else:
                            # Retry magic-bytes validation up to 4 times with growing delays.
                            # A fresh 200 MB write can be temporarily locked by antivirus or
                            # OS buffering, causing _peek_magic_bytes to silently return b"".
                            is_valid = False
                            for magic_attempt in range(4):
                                if magic_attempt > 0:
                                    time.sleep(0.5 * magic_attempt)
                                exists = stream_target.exists()
                                sz = stream_target.stat().st_size if exists else 0
                                fmt_check = nuc.get_compression_format(stream_target) if exists else "N/A"
                                magic_ok = is_raw_dlt_payload(stream_target) if exists else False
                                is_valid = (
                                    exists
                                    and stream_target.name.lower().endswith(".dlt")
                                    and fmt_check is None
                                    and magic_ok
                                )
                                if is_valid:
                                    break
                                self._queue_log(
                                    "dim",
                                    f"zstd magic check attempt {magic_attempt + 1}/4 for {stream_target.name}: "
                                    f"exists={exists}, size={sz}, fmt={fmt_check}, dlt_magic={magic_ok}",
                                )
                            if is_valid:
                                out.append(stream_target)
                                local_raw.unlink(missing_ok=True)
                                with self._remote_payload_lock:
                                    self._remote_payload_cache[remote_path] = [str(p.resolve()) for p in out if p.exists()]
                                return out
                            if first_exc is None:
                                exists = stream_target.exists()
                                out_fmt = nuc.get_compression_format(stream_target) if exists else None
                                out_magic = is_raw_dlt_payload(stream_target) if exists else False
                                out_sz = stream_target.stat().st_size if exists else 0
                                out_peek = _peek_magic_bytes(stream_target, size=8).hex() if exists else "file_missing"
                                first_exc = RuntimeError(
                                    f"stream output invalid (exists={exists}, size={out_sz}, "
                                    f"fmt={out_fmt}, dlt_magic={out_magic}, hex={out_peek})"
                                )
                    except Exception as exc:
                        if first_exc is None:
                            first_exc = exc

                    if attempt == 1:
                        self._queue_log("dim", f"zstd extract failed/invalid for {local_raw.name}; retrying fresh download")
                        local_raw.unlink(missing_ok=True)
                        download_with_retry(remote_path, local_raw, remote_size)

                if is_raw_dlt_payload(local_raw):
                    adopted = adopt_raw_dlt_file(local_raw)
                    out.append(adopted)
                    with self._remote_payload_lock:
                        self._remote_payload_cache[remote_path] = [str(p.resolve()) for p in out if p.exists()]
                    return out

                # Fallback to downloader extractor if streaming path still fails.
                try:
                    _e, _s, _f, paths = nuc.extract_dlt_files_from_archive(local_raw, output_extracted, skip_existing=True)
                    valid_paths = keep_only_uncompressed_dlt(paths)
                    if valid_paths:
                        out.extend(valid_paths)
                        local_raw.unlink(missing_ok=True)
                        with self._remote_payload_lock:
                            self._remote_payload_cache[remote_path] = [str(p.resolve()) for p in out if p.exists()]
                        return out
                except Exception:
                    pass

                cli_paths = extract_with_7zip_cli(local_raw, output_extracted)
                cli_valid = keep_only_uncompressed_dlt(cli_paths)
                if cli_valid:
                    out.extend(cli_valid)
                    local_raw.unlink(missing_ok=True)
                    with self._remote_payload_lock:
                        self._remote_payload_cache[remote_path] = [str(p.resolve()) for p in out if p.exists()]
                    return out

                self._queue_log("dim", f"zstd extract failed after retry for {local_raw.name}: {first_exc}")
                record_extraction_failure(local_raw.name, f"zstd extract failed after retry ({first_exc})")
                return out

            try:
                _e, _s, _f, paths = nuc.extract_dlt_files_from_archive(local_raw, output_extracted, skip_existing=True)
                out.extend(paths)
                local_raw.unlink(missing_ok=True)
            except Exception:
                cli_paths = extract_with_7zip_cli(local_raw, output_extracted)
                if cli_paths:
                    out.extend(cli_paths)
                    local_raw.unlink(missing_ok=True)
                else:
                    self._queue_log("dim", f"Archive extract failed for {local_raw.name}; keeping raw file.")
                    record_extraction_failure(local_raw.name, "archive extraction failed")
            with self._remote_payload_lock:
                self._remote_payload_cache[remote_path] = [str(p.resolve()) for p in out if p.exists()]
            return out

        extracted_paths: list[Path] = []
        if len(matched) == 1:
            extracted_paths.extend(process_payload(matched[0][0], matched[0][1], matched[0][2]))
        else:
            workers = min(PARALLEL_FILE_WORKERS, len(matched))
            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                futures = [
                    executor.submit(process_payload, file_name, remote_path, remote_size)
                    for file_name, remote_path, remote_size in matched
                ]
                for future in concurrent.futures.as_completed(futures):
                    extracted_paths.extend(future.result())

        unique = []
        seen = set()
        for path in extracted_paths:
            rp = path.resolve()
            if rp in seen or not path.exists() or not path.name.lower().endswith(".dlt"):
                continue
            # Guardrail: skip any output that is still compressed.
            if nuc.get_compression_format(path) is not None:
                self._queue_log("dim", f"Skipping still-compressed payload: {path.name}")
                continue
            seen.add(rp)
            unique.append(path)
        return DownloadBatchResult(
            files=unique,
            attempted_payloads=len(matched),
            extraction_failures=extraction_failures,
        )

    def _run_analysis(self, settings: dict[str, Any]) -> None:
        failures: list[str] = []
        matches: list[MatchResult] = []
        self.referenced_paths = set()
        self.keep_artifacts = set()
        prefetch_executor: concurrent.futures.ThreadPoolExecutor | None = None

        try:
            output_dir = Path(settings["output_dir"]).expanduser().resolve()
            resume_checkpoint_raw = str(settings.get("resume_checkpoint_path", "")).strip()
            requested_resume_checkpoint = Path(resume_checkpoint_raw).expanduser().resolve() if resume_checkpoint_raw else None

            run_id = dt.datetime.utcnow().strftime("run_%Y%m%dT%H%M%SZ")
            run_dir = output_dir / run_id
            checkpoint_path = run_dir / ANALYSIS_CHECKPOINT_FILE_NAME
            resumed_from_checkpoint = False
            resume_start_index = 0

            start_utc: dt.datetime
            end_utc: dt.datetime
            dtcs: list[str]
            ordered_occurrences: list[Occurrence]
            ts_col: str

            def _normalize_utc_iso(ts_text: str) -> dt.datetime:
                parsed = dt.datetime.fromisoformat(ts_text)
                if parsed.tzinfo is not None:
                    return parsed.astimezone(dt.timezone.utc).replace(tzinfo=None)
                return parsed

            resume_checkpoint_data = None
            if requested_resume_checkpoint is not None and requested_resume_checkpoint.exists():
                resume_checkpoint_data = load_analysis_checkpoint(requested_resume_checkpoint)

            resume_loaded_from_snapshot = False
            if resume_checkpoint_data is not None:
                try:
                    saved_version = int(resume_checkpoint_data.get("version", 0))
                    saved_completed = bool(resume_checkpoint_data.get("completed", False))
                    saved_start = str(resume_checkpoint_data.get("start_utc", "")).strip()
                    saved_end = str(resume_checkpoint_data.get("end_utc", "")).strip()
                    saved_dtcs_raw = resume_checkpoint_data.get("selected_dtcs", [])
                    saved_occurrences_raw = resume_checkpoint_data.get("ordered_occurrences", [])

                    if (
                        saved_version == ANALYSIS_CHECKPOINT_VERSION
                        and not saved_completed
                        and saved_start
                        and saved_end
                        and isinstance(saved_dtcs_raw, list)
                        and isinstance(saved_occurrences_raw, list)
                    ):
                        parsed_occurrences: list[Occurrence] = []
                        for raw_occ in saved_occurrences_raw:
                            if not isinstance(raw_occ, dict):
                                continue
                            parsed_occurrences.append(occurrence_from_dict(raw_occ))

                        if parsed_occurrences:
                            start_utc = _normalize_utc_iso(saved_start)
                            end_utc = _normalize_utc_iso(saved_end)
                            dtcs = parse_dtc_list(" ".join(str(v) for v in saved_dtcs_raw))
                            if not dtcs:
                                raise RuntimeError("Checkpoint has no DTCs to resume.")

                            ordered_occurrences = parsed_occurrences
                            ts_col = str(resume_checkpoint_data.get("ts_col", ""))

                            restored_matches: list[MatchResult] = []
                            for raw_match in resume_checkpoint_data.get("matches", []):
                                try:
                                    if not isinstance(raw_match, dict):
                                        continue
                                    restored_matches.append(match_from_dict(raw_match))
                                except Exception:
                                    continue

                            raw_failures = resume_checkpoint_data.get("failures", [])
                            failures = [str(item) for item in raw_failures] if isinstance(raw_failures, list) else []
                            raw_next = int(resume_checkpoint_data.get("next_index", 0) or 0)
                            resume_start_index = max(0, min(len(ordered_occurrences), max(raw_next, len(restored_matches))))
                            matches = restored_matches[:resume_start_index]

                            run_dir = requested_resume_checkpoint.parent
                            checkpoint_path = requested_resume_checkpoint
                            resumed_from_checkpoint = True
                            resume_loaded_from_snapshot = True
                except Exception as exc:
                    self._queue_log("dim", f"Resume checkpoint could not be loaded: {exc}")

            if not resume_loaded_from_snapshot:
                start_utc, end_utc = self._analysis_range_from_settings(settings)
                dtcs = parse_dtc_list(settings["dtc_list"])
                self._queue_log("info", f"Analysis range UTC: {start_utc.isoformat()} to {end_utc.isoformat()}")
                self._queue_log("info", f"Selected DTCs: {', '.join(dtcs)}")

                storage_options = get_storage_options(lambda msg: self._queue_log("dim", msg))
                occurrences, ts_col = fetch_occurrences(
                    storage_options,
                    start_utc,
                    end_utc,
                    dtcs,
                    lambda m: self._queue_log("dim", m),
                    refresh_storage_options_fn=lambda: get_storage_options(lambda msg: self._queue_log("dim", msg)),
                )
                self._queue_log("ok", f"Occurrences loaded: {len(occurrences)} (timestamp column: {ts_col})")

                if not occurrences:
                    raise RuntimeError("No matching occurrences found for selected DTCs and range.")

                ordered_occurrences = self._order_occurrences_for_reuse(occurrences)
                self._queue_log("dim", "Reordered occurrences by VIN/day to improve listing/download cache reuse.")
            else:
                self._queue_log("info", f"Analysis range UTC: {start_utc.isoformat()} to {end_utc.isoformat()}")
                self._queue_log("info", f"Selected DTCs: {', '.join(dtcs)}")
                self._queue_log(
                    "ok",
                    f"Loaded resume checkpoint snapshot with {len(ordered_occurrences)} occurrence(s) and next index {resume_start_index}.",
                )

            self._ensure_not_cancelled()
            nuc = self.nuc_module
            azure_fs = nuc.create_azure_fs()
            self._queue_log("dim", "Connected to NUC Azure storage.")
            prefetch_executor = concurrent.futures.ThreadPoolExecutor(max_workers=PREFETCH_WORKERS)

            run_dir.mkdir(parents=True, exist_ok=True)
            self.last_run_dir = run_dir
            self._queue_log("info", f"Run folder: {run_dir}")
            if resumed_from_checkpoint:
                self._queue_log(
                    "ok",
                    f"Resuming from checkpoint at occurrence index {resume_start_index}/{len(ordered_occurrences)}.",
                )

            def persist_checkpoint(next_index: int, completed: bool = False) -> None:
                try:
                    save_analysis_checkpoint(
                        checkpoint_path,
                        start_utc=start_utc,
                        end_utc=end_utc,
                        selected_dtcs=dtcs,
                        ts_col=ts_col,
                        ordered_occurrences=ordered_occurrences,
                        next_index=next_index,
                        matches=matches,
                        failures=failures,
                        completed=completed,
                    )
                except Exception as exc:
                    self._queue_log("dim", f"Checkpoint write failed: {exc}")

            def append_result_and_checkpoint(result: MatchResult, next_index: int) -> None:
                matches.append(result)
                persist_checkpoint(next_index)

            persist_checkpoint(resume_start_index)

            parsed_cache: OrderedDict[Path, list[tuple[Any, ...]]] = OrderedDict()
            reuse_files_by_vehicle: dict[tuple[str, str], list[Path]] = {}
            current_vehicle_key: tuple[str, str] | None = None

            def get_parsed_messages(dlt_file: Path) -> list[tuple[Any, ...]]:
                cached = parsed_cache.pop(dlt_file, None)
                if cached is not None:
                    parsed_cache[dlt_file] = cached
                    return cached

                msgs, _search = self.dlt_parser_module.parse_dlt_file(str(dlt_file))
                parsed_cache[dlt_file] = msgs
                while len(parsed_cache) > PARSED_DLT_CACHE_MAX_FILES:
                    evicted_path, _evicted_msgs = parsed_cache.popitem(last=False)
                    self._queue_log("dim", f"Evicted parsed DLT cache entry to reduce memory: {evicted_path.name}")
                return msgs

            def scan_and_log_match(
                occurrence: Occurrence,
                dlt_file: Path,
                messages: list[tuple[Any, ...]],
            ) -> MatchResult:
                result = scan_messages_for_match(occurrence, dlt_file, messages, self.fault_reasons)
                prefix = (
                    f"{occurrence.vin} {occurrence.dtc_id or occurrence.dtc_altvalue} "
                    f"trigger={occurrence_trigger_ts(occurrence).isoformat()} in {dlt_file.name}"
                )
                if result.dtc_line:
                    self._queue_log("ok", f"FAILED DTC line found: {prefix}")
                if result.reason:
                    self._queue_log("ok", f"Fault reason found: {prefix} -> {result.reason}")
                return result

            def log_scan_outcome(
                occurrence: Occurrence,
                phase: str,
                result: MatchResult | None,
                file_count: int,
            ) -> None:
                if result is None:
                    outcome = "no result"
                elif result.reason:
                    outcome = f"SUCCESS: FAILED DTC line and fault reason found -> {result.reason}"
                elif result.dtc_line:
                    outcome = "FAILED DTC line found, but no configured fault reason matched"
                elif result.status == "NO_DLT":
                    outcome = "no DLT files found"
                elif result.status in {"NO_DLT_EXTRACT_FAILED", "NO_FAILED_DTC_LINE_WITH_EXTRACT_FAILURE"}:
                    outcome = f"no match; extraction failure: {result.error or 'unknown extraction failure'}"
                else:
                    outcome = "no FAILED DTC line found"
                self._queue_log(
                    "ok" if result is not None and (result.dtc_line or result.reason) else "dim",
                    f"{phase} complete for {occurrence.vin} {occurrence.dtc_id or occurrence.dtc_altvalue}: "
                    f"{outcome}; DLT files examined={file_count}",
                )

            def get_vehicle_fallback_files(vehicle_key: tuple[str, str]) -> list[Path]:
                vin, variant = vehicle_key
                candidates: list[Path] = []
                seen: set[Path] = set()

                for path in reuse_files_by_vehicle.get(vehicle_key, []):
                    if not path.exists():
                        continue
                    rp = path.resolve()
                    if rp in seen:
                        continue
                    seen.add(rp)
                    candidates.append(path)

                vehicle_dir = run_dir / "extracted" / vin / variant
                if vehicle_dir.exists():
                    for path in sorted(
                        vehicle_dir.glob("*.dlt"),
                        key=lambda p: (self.nuc_module.parse_filename_timestamp(p.name) or dt.datetime.max, p.name),
                    ):
                        rp = path.resolve()
                        if rp in seen:
                            continue
                        seen.add(rp)
                        candidates.append(path)
                        if len(candidates) >= BASELINE_FALLBACK_MAX_FILES_PER_VEHICLE:
                            break

                if len(candidates) > BASELINE_FALLBACK_MAX_FILES_PER_VEHICLE:
                    candidates = candidates[:BASELINE_FALLBACK_MAX_FILES_PER_VEHICLE]
                return candidates

            def apply_vin_baseline_fallback(result: MatchResult, vehicle_key: tuple[str, str]) -> MatchResult:
                if result.baseline_summary:
                    return result

                candidate_files = get_vehicle_fallback_files(vehicle_key)
                best_summary: str | None = None
                best_delta: float | None = None
                best_source_file: Path | None = None
                best_score: tuple[int, float] | None = None

                for fallback_file in candidate_files:
                    msgs = get_parsed_messages(fallback_file)
                    anchor_idx = find_message_index_near_event_ts(msgs, occurrence_trigger_ts(result.occurrence))
                    summary, delta = find_confighub_baseline(msgs, anchor_idx)
                    if not summary:
                        continue

                    if delta is None:
                        score = (1, float("inf"))
                    else:
                        score = (0, abs(delta))

                    if best_score is None or score < best_score:
                        best_score = score
                        best_summary = summary
                        best_delta = delta
                        best_source_file = fallback_file

                if best_summary:
                    result.baseline_summary = best_summary
                    result.baseline_time_delta_seconds = best_delta
                    result.baseline_source = f"VIN_FALLBACK:{best_source_file.name}" if best_source_file is not None else "VIN_FALLBACK"

                return result

            prefetch_submitted: set[int] = set()

            def _prefetch_one(array_idx: int) -> None:
                try:
                    if array_idx in prefetch_submitted or array_idx < 0 or array_idx >= len(ordered_occurrences):
                        return
                    prefetch_submitted.add(array_idx)
                    occ = ordered_occurrences[array_idx]
                    vehicle_key = (occ.vin, occ.variant)
                    existing_count = len([p for p in reuse_files_by_vehicle.get(vehicle_key, []) if p.exists()])
                    if existing_count >= MAX_DLT_FILES_PER_VEHICLE:
                        return
                    quota = max(0, MAX_DLT_FILES_PER_VEHICLE - existing_count)

                    def _do_prefetch() -> None:
                        if self.cancel_event.is_set():
                            return
                        try:
                            self._download_occurrence_files(
                                azure_fs,
                                occ,
                                occurrence_event_ts_for_dlt(occ),
                                run_dir,
                                quota,
                            )
                        except Exception:
                            # Best-effort warm-up only; the main loop will retry/handle
                            # errors for real when it reaches this occurrence.
                            pass

                    assert prefetch_executor is not None
                    prefetch_executor.submit(_do_prefetch)
                except Exception:
                    pass

            def _schedule_prefetch_ahead_of(idx_1based: int) -> None:
                base_array_idx = idx_1based - 1
                for offset in range(1, PREFETCH_LOOKAHEAD + 1):
                    _prefetch_one(base_array_idx + offset)

            for idx, occurrence in enumerate(ordered_occurrences[resume_start_index:], start=resume_start_index + 1):
                self._ensure_not_cancelled()
                self._queue_log(
                    "info",
                    f"[{idx}/{len(ordered_occurrences)}] {occurrence.vin} {occurrence.variant} {occurrence.dtc_id or occurrence.dtc_altvalue} trigger={occurrence_trigger_ts(occurrence).isoformat()} read={occurrence.event_ts.isoformat()}",
                )
                next_index = idx
                _schedule_prefetch_ahead_of(idx)

                center_ts = occurrence_event_ts_for_dlt(occurrence)

                vehicle_key = (occurrence.vin, occurrence.variant)
                if current_vehicle_key is None:
                    current_vehicle_key = vehicle_key
                elif vehicle_key != current_vehicle_key:
                    parsed_cache.clear()
                    current_vehicle_key = vehicle_key
                reuse_candidates = [p for p in reuse_files_by_vehicle.get(vehicle_key, []) if p.exists()]

                best: MatchResult | None = None
                reuse_hit = False
                for dlt_file in reuse_candidates:
                    self._ensure_not_cancelled()
                    msgs = get_parsed_messages(dlt_file)
                    result = scan_and_log_match(occurrence, dlt_file, msgs)

                    if best is None:
                        best = result
                    elif best.status != "MAPPED" and result.status == "MAPPED":
                        best = result
                    elif best.status == "NO_FAILED_DTC_LINE" and result.status == "UNMAPPED":
                        best = result

                    if result.status in {"MAPPED", "UNMAPPED"}:
                        reuse_hit = True
                        break

                if reuse_hit and best is not None:
                    log_scan_outcome(occurrence, "Reused DLT scan", best, len(reuse_candidates))
                    best = apply_vin_baseline_fallback(best, vehicle_key)
                    append_result_and_checkpoint(best, next_index)
                    continue

                needs_deep_discovery = best is None or best.status == "NO_FAILED_DTC_LINE"
                if len(reuse_candidates) >= MAX_DLT_FILES_PER_VEHICLE and not needs_deep_discovery:
                    if best is None:
                        best = MatchResult(
                            occurrence=occurrence,
                            dlt_file=None,
                            dtc_line=None,
                            reason=None,
                            reason_line=None,
                            reason_offset_lines=None,
                            dlt_line_index=None,
                            status="NO_FAILED_DTC_LINE",
                        )
                    best = apply_vin_baseline_fallback(best, vehicle_key)
                    append_result_and_checkpoint(best, next_index)
                    continue

                dlt_files: list[Path] = []
                occurrence_extraction_failures: list[str] = []
                last_exc: Exception | None = None
                try:
                    if len(reuse_candidates) >= MAX_DLT_FILES_PER_VEHICLE:
                        remaining_quota = FAILED_DISCOVERY_EXTRA_FILES
                    else:
                        remaining_quota = max(0, MAX_DLT_FILES_PER_VEHICLE - len(reuse_candidates))
                    download_result = self._download_occurrence_files(
                        azure_fs,
                        occurrence,
                        center_ts,
                        run_dir,
                        remaining_quota,
                    )
                    dlt_files = download_result.files
                    occurrence_extraction_failures.extend(download_result.extraction_failures)
                except Exception as exc:
                    last_exc = exc

                if last_exc is not None and not dlt_files:
                    failures.append(f"Download failed for {occurrence.vin}/{occurrence.event_ts.isoformat()}: {last_exc}")
                    append_result_and_checkpoint(
                        apply_vin_baseline_fallback(MatchResult(
                            occurrence=occurrence,
                            dlt_file=None,
                            dtc_line=None,
                            reason=None,
                            reason_line=None,
                            reason_offset_lines=None,
                            dlt_line_index=None,
                            status="ERROR",
                            error=str(last_exc),
                        ), vehicle_key),
                        next_index,
                    )
                    continue

                if not dlt_files:
                    try:
                        adjacent_result = self._download_occurrence_files(
                            azure_fs,
                            occurrence,
                            center_ts,
                            run_dir,
                            max_new_files=2,
                            include_adjacent_neighbors=True,
                        )
                        dlt_files = adjacent_result.files
                        occurrence_extraction_failures.extend(adjacent_result.extraction_failures)
                    except Exception:
                        pass

                if not dlt_files:
                    status = "NO_DLT_EXTRACT_FAILED" if occurrence_extraction_failures else "NO_DLT"
                    append_result_and_checkpoint(
                        apply_vin_baseline_fallback(MatchResult(
                            occurrence=occurrence,
                            dlt_file=None,
                            dtc_line=None,
                            reason=None,
                            reason_line=None,
                            reason_offset_lines=None,
                            dlt_line_index=None,
                            status=status,
                            error="; ".join(occurrence_extraction_failures[:3]),
                        ), vehicle_key),
                        next_index,
                    )
                    continue

                for dlt_file in dlt_files:
                    self._ensure_not_cancelled()
                    msgs = get_parsed_messages(dlt_file)
                    result = scan_and_log_match(occurrence, dlt_file, msgs)

                    if best is None:
                        best = result
                    elif best.status != "MAPPED" and result.status == "MAPPED":
                        best = result
                    elif best.status == "NO_FAILED_DTC_LINE" and result.status == "UNMAPPED":
                        best = result

                    if result.status == "MAPPED":
                        break

                log_scan_outcome(occurrence, "Initial DLT scan", best, len(dlt_files))

                retry_phase_total = 2 + (1 if occurrence_trigger_ts(occurrence) != center_ts else 0)
                retry_phase_index = 0

                def log_retry_phase(message: str) -> None:
                    nonlocal retry_phase_index
                    retry_phase_index += 1
                    self._queue_log(
                        "dim",
                        f"[{idx}/{len(ordered_occurrences)}] Retry phase {retry_phase_index}/{retry_phase_total}: {message}",
                    )

                if (
                    (best is None or best.status == "NO_FAILED_DTC_LINE")
                    and len(dlt_files) > 0
                    and occurrence.dtc_ts21_utc is None
                    and occurrence.dtc_ts20_utc is None
                ):
                    log_retry_phase(f"No FAILED DTC line for {occurrence.vin}; trying one earlier/later DLT file.")
                    try:
                        adjacent_result = self._download_occurrence_files(
                            azure_fs,
                            occurrence,
                            center_ts,
                            run_dir,
                            max_new_files=2,
                            include_adjacent_neighbors=True,
                        )
                        occurrence_extraction_failures.extend(adjacent_result.extraction_failures)
                        adjacent_files = [p for p in adjacent_result.files if p not in dlt_files]
                        dlt_files.extend(adjacent_files)

                        for dlt_file in adjacent_files:
                            self._ensure_not_cancelled()
                            msgs = get_parsed_messages(dlt_file)
                            result = scan_and_log_match(occurrence, dlt_file, msgs)

                            if best is None:
                                best = result
                            elif best.status != "MAPPED" and result.status == "MAPPED":
                                best = result
                            elif best.status == "NO_FAILED_DTC_LINE" and result.status == "UNMAPPED":
                                best = result

                            if result.status == "MAPPED":
                                break
                    except Exception as exc:
                        self._queue_log("dim", f"Adjacent file probe failed for {occurrence.vin}: {exc}")
                    log_scan_outcome(occurrence, "Retry phase adjacent-file probe", best, len(dlt_files))

                if (best is None or best.status == "NO_FAILED_DTC_LINE") and len(dlt_files) > 0:
                    log_retry_phase(f"No FAILED DTC line for {occurrence.vin}; widening DLT discovery.")
                    try:
                        extra_result = self._download_occurrence_files(
                            azure_fs,
                            occurrence,
                            center_ts,
                            run_dir,
                            FAILED_DISCOVERY_EXTRA_FILES,
                        )
                        occurrence_extraction_failures.extend(extra_result.extraction_failures)
                        extra_files = extra_result.files
                        for dlt_file in extra_files:
                            self._ensure_not_cancelled()
                            msgs = get_parsed_messages(dlt_file)
                            result = scan_and_log_match(occurrence, dlt_file, msgs)

                            if best is None:
                                best = result
                            elif best.status != "MAPPED" and result.status == "MAPPED":
                                best = result
                            elif best.status == "NO_FAILED_DTC_LINE" and result.status == "UNMAPPED":
                                best = result

                            if result.status == "MAPPED":
                                break
                    except Exception as exc:
                        self._queue_log("dim", f"Deep discovery failed for {occurrence.vin}: {exc}")
                    log_scan_outcome(occurrence, "Retry phase widened discovery", best, len(dlt_files))

                # Timezone ambiguity retry: NUC logger 8.2.36 (2026-05-21) switched vtStart
                # from Swedish local time to UTC. For vehicles on new firmware the existing
                # -2 h Stockholm conversion overshoots by 2 h. Retry with vtStart treated as
                # pure UTC so the search window centres on the actual event time.
                if (
                    (best is None or best.status == "NO_FAILED_DTC_LINE")
                    and len(dlt_files) > 0
                    and occurrence.dtc_ts21_utc is None
                    and occurrence.dtc_ts20_utc is None
                ):
                    utc_center_ts = occurrence.event_ts  # vtStart as-is, no offset
                    if utc_center_ts != center_ts:
                        shift_h = int(round((utc_center_ts - center_ts).total_seconds() / 3600))
                        log_retry_phase(
                            f"No FAILED DTC line for {occurrence.vin}; retrying with UTC-assumed vtStart "
                            f"(+{shift_h}h TZ shift)."
                        )
                        self._queue_log(
                            "dim",
                            f"No FAILED DTC line yet for {occurrence.vin}; retrying with UTC-assumed vtStart "
                            f"(+{shift_h}h TZ shift — logger may have updated to UTC timestamps).",
                        )
                        # Neutralise the Stockholm conversion by using a source_ts_col that
                        # does not trigger the local-time branch of occurrence_event_ts_for_dlt.
                        tz_occurrence = dc_replace(occurrence, source_ts_col="utc")
                        try:
                            tz_result = self._download_occurrence_files(
                                azure_fs,
                                tz_occurrence,
                                utc_center_ts,
                                run_dir,
                                FAILED_DISCOVERY_EXTRA_FILES,
                            )
                            occurrence_extraction_failures.extend(tz_result.extraction_failures)
                            tz_files = [p for p in tz_result.files if p not in dlt_files]
                            dlt_files.extend(tz_files)
                            for dlt_file in tz_files:
                                self._ensure_not_cancelled()
                                msgs = get_parsed_messages(dlt_file)
                                result = scan_and_log_match(occurrence, dlt_file, msgs)

                                if best is None:
                                    best = result
                                elif best.status != "MAPPED" and result.status == "MAPPED":
                                    best = result
                                elif best.status == "NO_FAILED_DTC_LINE" and result.status == "UNMAPPED":
                                    best = result

                                if result.status == "MAPPED":
                                    break
                        except Exception as exc:
                            self._queue_log("dim", f"UTC-shift TZ retry failed for {occurrence.vin}: {exc}")
                        log_scan_outcome(occurrence, "Retry phase UTC-assumed timestamp", best, len(dlt_files))

                if best is None:
                    best = MatchResult(
                        occurrence=occurrence,
                        dlt_file=None,
                        dtc_line=None,
                        reason=None,
                        reason_line=None,
                        reason_offset_lines=None,
                        dlt_line_index=None,
                        status="NO_FAILED_DTC_LINE_WITH_EXTRACT_FAILURE" if occurrence_extraction_failures else "NO_FAILED_DTC_LINE",
                        error="; ".join(occurrence_extraction_failures[:3]),
                    )
                elif best.status == "NO_FAILED_DTC_LINE" and occurrence_extraction_failures:
                    best.status = "NO_FAILED_DTC_LINE_WITH_EXTRACT_FAILURE"
                    best.error = "; ".join(occurrence_extraction_failures[:3])

                existing = reuse_files_by_vehicle.get(vehicle_key, [])
                seen = {p.resolve() for p in existing if p.exists()}
                for p in dlt_files:
                    if len(existing) >= MAX_DLT_FILES_PER_VEHICLE:
                        break
                    rp = p.resolve()
                    if rp in seen:
                        continue
                    seen.add(rp)
                    existing.append(p)
                reuse_files_by_vehicle[vehicle_key] = existing

                best = apply_vin_baseline_fallback(best, vehicle_key)
                append_result_and_checkpoint(best, next_index)

            report_path = run_dir / "dtc_dlt_fault_report.html"
            report_text, referenced = build_html_report(start_utc, end_utc, dtcs, matches, failures, report_path)
            report_path.write_text(report_text, encoding="utf-8")

            sidecar_path = run_dir / "report_references.json"
            sidecar = {
                "generated_utc": dt.datetime.utcnow().isoformat() + "Z",
                "report_file": str(report_path),
                "referenced_dlt_files": [str(path.resolve()) for path in sorted(referenced)],
                "total_matches": len(matches),
                "failures": failures,
            }
            sidecar_path.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
            persist_checkpoint(len(ordered_occurrences), completed=True)

            self.referenced_paths = referenced
            self.keep_artifacts = {report_path, sidecar_path, checkpoint_path}
            self.last_report_path = report_path

            summary = compute_storage_summary(run_dir, referenced)
            self.storage_var.set(
                "Storage: "
                f"total {summary.total_files} file(s), {format_bytes(summary.total_bytes)} | "
                f"referenced {summary.referenced_files} file(s), {format_bytes(summary.referenced_bytes)}"
            )

            mapped_count = sum(1 for m in matches if m.reason)
            self._queue_log("ok", f"Report written: {report_path}")
            self._queue_log("ok", f"Mapped: {mapped_count} | Unmapped: {len(matches) - mapped_count}")

            self.cleanup_all_button.configure(state=tk.NORMAL)
            self.cleanup_keep_button.configure(state=tk.NORMAL)
            self.open_report_button.configure(state=tk.NORMAL)

        except Exception as exc:
            self._queue_log("err", str(exc))
            self._queue_log("err", traceback.format_exc())
            self.storage_var.set("Storage: run failed")
        finally:
            if prefetch_executor is not None:
                prefetch_executor.shutdown(wait=False, cancel_futures=True)
            self.run_button.configure(state=tk.NORMAL)
            self.stop_button.configure(state=tk.DISABLED)

    def _refresh_storage_after_cleanup(self) -> None:
        if self.last_run_dir is None:
            return
        summary = compute_storage_summary(self.last_run_dir, self.referenced_paths)
        self.storage_var.set(
            "Storage: "
            f"total {summary.total_files} file(s), {format_bytes(summary.total_bytes)} | "
            f"referenced {summary.referenced_files} file(s), {format_bytes(summary.referenced_bytes)}"
        )

    def _cleanup_all(self) -> None:
        if self.last_run_dir is None:
            messagebox.showinfo("No run", "No run directory available.")
            return
        deleted_files, deleted_bytes = cleanup_all_downloads(self.last_run_dir, self.keep_artifacts)
        self._queue_log("ok", f"Cleanup all completed: removed {deleted_files} file(s), {format_bytes(deleted_bytes)}")
        self._refresh_storage_after_cleanup()

    def _cleanup_keep_referenced(self) -> None:
        if self.last_run_dir is None:
            messagebox.showinfo("No run", "No run directory available.")
            return
        deleted_files, deleted_bytes = cleanup_keep_referenced(
            self.last_run_dir,
            self.referenced_paths,
            self.keep_artifacts,
        )
        self._queue_log(
            "ok",
            f"Cleanup keep-referenced completed: removed {deleted_files} file(s), {format_bytes(deleted_bytes)}",
        )
        self._refresh_storage_after_cleanup()

    def _open_report(self) -> None:
        if self.last_report_path is None or not self.last_report_path.exists():
            messagebox.showinfo("Report not available", "No generated report is available yet.")
            return
        try:
            os.startfile(str(self.last_report_path))  # type: ignore[attr-defined]
        except Exception as exc:
            messagebox.showerror("Open report failed", str(exc))

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    App().run()
