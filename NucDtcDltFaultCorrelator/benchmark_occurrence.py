from __future__ import annotations

import datetime as dt
import shutil
import time
from pathlib import Path

import app


def main() -> int:
    settings = app.load_settings()
    mode = str(settings["window_mode"])
    manual_start = app.parse_manual_datetime(str(settings["manual_start"])) if mode == "Manual" else None
    manual_end = app.parse_manual_datetime(str(settings["manual_end"])) if mode == "Manual" else None
    now_utc = dt.datetime.utcnow()
    start_utc, end_utc = app.resolve_analysis_range(mode, manual_start, manual_end, now_utc)
    dtcs = app.parse_dtc_list(str(settings["dtc_list"]))

    shutil.rmtree(app.OCCURRENCE_CACHE_DIR, ignore_errors=True)
    print("cache_cleared", not app.OCCURRENCE_CACHE_DIR.exists())

    storage_options = app.get_storage_options(lambda m: None)

    t0 = time.perf_counter()
    occ1, ts1 = app.fetch_occurrences(storage_options, start_utc, end_utc, dtcs, print)
    t1 = time.perf_counter()

    t2 = time.perf_counter()
    occ2, ts2 = app.fetch_occurrences(storage_options, start_utc, end_utc, dtcs, print)
    t3 = time.perf_counter()

    cold_s = t1 - t0
    warm_s = t3 - t2

    print("cold_seconds", round(cold_s, 3))
    print("warm_seconds", round(warm_s, 3))
    print("rows_cold", len(occ1), "ts_col", ts1)
    print("rows_warm", len(occ2), "ts_col", ts2)
    if cold_s > 0:
        print("speedup_x", round(cold_s / max(warm_s, 1e-6), 2))

    # Show cache artifact for traceability.
    cache_files = sorted(Path(app.OCCURRENCE_CACHE_DIR).glob("*.json"))
    print("cache_files", len(cache_files))
    for p in cache_files[:3]:
        print("cache", p.name, p.stat().st_size)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
