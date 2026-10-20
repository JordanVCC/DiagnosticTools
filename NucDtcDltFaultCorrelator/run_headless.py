from __future__ import annotations

import datetime as dt
import concurrent.futures
import importlib.util
import json
import shutil
import time
from pathlib import Path

import app


PARALLEL_FILE_WORKERS = 6
MAX_DLT_CANDIDATES_PER_OCCURRENCE = 12
MAX_DLT_FILES_PER_VEHICLE = 4
FAILED_DISCOVERY_EXTRA_FILES = 12
_AZURE_VARIANT_PATH_CACHE: dict[tuple[str, str], str | None] = {}
_AZURE_DAY_LISTING_CACHE: dict[str, list[tuple[str, str, dt.datetime]]] = {}
_REMOTE_PAYLOAD_CACHE: dict[str, list[str]] = {}


def load_module(module_path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def ensure_not_cancelled() -> None:
    return


def download_occurrence_files(
    nuc,
    azure_fs,
    occurrence: app.Occurrence,
    center_ts: dt.datetime,
    run_dir: Path,
    max_new_files: int,
    include_adjacent_neighbors: bool = False,
    attempt_mode: str = "standard",
    adjacent_span: int = 1,
) -> app.DownloadBatchResult:
    output_raw = run_dir / "raw" / occurrence.vin / occurrence.variant
    output_extracted = run_dir / "extracted" / occurrence.vin / occurrence.variant
    output_raw.mkdir(parents=True, exist_ok=True)
    output_extracted.mkdir(parents=True, exist_ok=True)

    variant_cache_key = (occurrence.vin, occurrence.variant)
    variant_path = _AZURE_VARIANT_PATH_CACHE.get(variant_cache_key)
    if variant_path is None:
        azure_vin = nuc.azure_find_child_name(azure_fs, nuc.AZURE_NUC_ROOT, occurrence.vin)
        if not azure_vin:
            _AZURE_VARIANT_PATH_CACHE[variant_cache_key] = None
            return app.DownloadBatchResult(files=[])

        vin_root_path = f"{nuc.AZURE_NUC_ROOT}/{azure_vin}"
        dlt_dir = nuc.azure_find_dlt_dir_name(azure_fs, vin_root_path)
        if not dlt_dir:
            _AZURE_VARIANT_PATH_CACHE[variant_cache_key] = None
            return app.DownloadBatchResult(files=[])

        variant_root = f"{vin_root_path}/{dlt_dir}"
        variant_name = nuc.azure_find_child_name(azure_fs, variant_root, occurrence.variant)
        if not variant_name:
            _AZURE_VARIANT_PATH_CACHE[variant_cache_key] = None
            return app.DownloadBatchResult(files=[])

        variant_path = f"{variant_root}/{variant_name}"
        _AZURE_VARIANT_PATH_CACHE[variant_cache_key] = variant_path

    if not variant_path:
        return app.DownloadBatchResult(files=[])
    all_candidates: list[tuple[str, str, int | None, dt.datetime]] = []

    candidate_centers = (
        app.build_candidate_dlt_centers(occurrence)
        if attempt_mode == "standard"
        else app.build_fast_attempt_dlt_centers(occurrence)
    )
    scan_start_day = min(candidate_centers).date()
    scan_end_day = max(candidate_centers).date()
    for day in nuc.daterange(scan_start_day, scan_end_day):
        ensure_not_cancelled()
        day_path = f"{variant_path}/{day.year:04d}/{day.month:02d}/{day.day:02d}"
        day_entries = _AZURE_DAY_LISTING_CACHE.get(day_path)
        if day_entries is None:
            day_entries = []
            for file_name, file_size in nuc.azure_list_files(azure_fs, day_path):
                if not nuc.is_supported_dlt_payload_name(file_name):
                    continue
                file_ts = nuc.parse_filename_timestamp(file_name)
                if file_ts is None:
                    continue
                day_entries.append((file_name, f"{day_path}/{file_name}", file_ts, file_size))
            _AZURE_DAY_LISTING_CACHE[day_path] = day_entries

        for entry in day_entries:
            if len(entry) == 4:
                file_name, remote_path, file_ts, file_size = entry
            else:
                file_name, remote_path, file_ts = entry
                file_size = None
            all_candidates.append((file_name, remote_path, file_size, file_ts))

    matched: list[tuple[str, str, int | None]] = []
    selected_center: dt.datetime | None = None
    seen_remote_paths: set[str] = set()
    if attempt_mode != "standard":
        first_after = app.pick_first_after_dlt_candidate_for_centers(
            all_candidates,
            [occurrence.event_ts, app.occurrence_event_ts_for_dlt(occurrence)],
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
        picks = app.select_relevant_dlt_candidates(
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
        print(f"INFO selected DLT by UTC file-start rule around {selected_center.isoformat()} (source column {occurrence.source_ts_col})")

    if attempt_mode == "standard" and include_adjacent_neighbors and matched:
        adjacent = app.pick_adjacent_dlt_candidates(
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
        return app.DownloadBatchResult(files=[])

    matched = matched[:max_new_files]
    if not matched:
        return app.DownloadBatchResult(files=[])

    extraction_failures: list[str] = []

    def download_with_retry(remote_path: str, local_raw: Path, remote_size: int | None) -> None:
        attempts = max(1, int(getattr(nuc, "AZURE_DOWNLOAD_RETRY_ATTEMPTS", 4)))
        chunk_size = int(getattr(nuc, "IO_CHUNK_SIZE_AZURE", 8 * 1024 * 1024))
        temp_path = local_raw.with_name(local_raw.name + ".part")

        for attempt in range(1, attempts + 1):
            ensure_not_cancelled()
            try:
                current_size = temp_path.stat().st_size if temp_path.exists() else 0
                if remote_size is not None and current_size > remote_size:
                    temp_path.unlink(missing_ok=True)
                    current_size = 0

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
                        ensure_not_cancelled()
                        chunk = src.read(chunk_size)
                        if not chunk:
                            break
                        dst.write(chunk)

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
                print(f"WARN retry {attempt}/{attempts} for {local_raw.name}: {exc}")
                time.sleep(wait_s)

    def process_payload(file_name: str, remote_path: str, remote_size: int | None) -> list[Path]:
        out: list[Path] = []
        ensure_not_cancelled()
        cached = _REMOTE_PAYLOAD_CACHE.get(remote_path)
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
                and app.is_raw_dlt_payload(existing_target)
            ):
                out.append(existing_target)
                _REMOTE_PAYLOAD_CACHE[remote_path] = [str(p.resolve()) for p in out if p.exists()]
                return out

        local_raw = output_raw / file_name
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

        if app.is_raw_dlt_payload(local_raw):
            adopted = adopt_raw_dlt_file(local_raw)
            out.append(adopted)
            _REMOTE_PAYLOAD_CACHE[remote_path] = [str(p.resolve()) for p in out if p.exists()]
            return out

        magic_fmt = app.detect_compression_magic(local_raw)
        fmt = magic_fmt or nuc.get_compression_format(local_raw)
        if fmt is None and local_raw.name.lower().endswith(".dlt"):
            out.append(local_raw)
            return out

        if not fmt:
            return out

        if fmt == "zst":
            if magic_fmt is not None and magic_fmt != "zst":
                print(f"WARN unexpected non-zstd payload for {local_raw.name} (magic={magic_fmt}); skipping")
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

            if (
                stream_target.exists()
                and stream_target.name.lower().endswith(".dlt")
                and nuc.get_compression_format(stream_target) is None
                and app.is_raw_dlt_payload(stream_target)
            ):
                out.append(stream_target)
                local_raw.unlink(missing_ok=True)
                _REMOTE_PAYLOAD_CACHE[remote_path] = [str(p.resolve()) for p in out if p.exists()]
                return out

            for attempt in (1, 2):
                try:
                    stream_target.unlink(missing_ok=True)
                    ok = app.decompress_zst_stream_to_file(local_raw, stream_target)
                    is_valid = (
                        ok
                        and stream_target.exists()
                        and stream_target.name.lower().endswith(".dlt")
                        and nuc.get_compression_format(stream_target) is None
                        and app.is_raw_dlt_payload(stream_target)
                    )
                    if is_valid:
                        out.append(stream_target)
                        local_raw.unlink(missing_ok=True)
                        _REMOTE_PAYLOAD_CACHE[remote_path] = [str(p.resolve()) for p in out if p.exists()]
                        return out
                    if first_exc is None:
                        out_fmt = nuc.get_compression_format(stream_target) if stream_target.exists() else None
                        out_magic = app.is_raw_dlt_payload(stream_target) if stream_target.exists() else False
                        first_exc = RuntimeError(f"stream output invalid (fmt={out_fmt}, dlt_magic={out_magic})")
                except Exception as exc:
                    if first_exc is None:
                        first_exc = exc

                if attempt == 1:
                    print(f"WARN zstd extract failed/invalid for {local_raw.name}; retrying fresh download")
                    local_raw.unlink(missing_ok=True)
                    download_with_retry(remote_path, local_raw, remote_size)

            if app.is_raw_dlt_payload(local_raw):
                adopted = adopt_raw_dlt_file(local_raw)
                out.append(adopted)
                _REMOTE_PAYLOAD_CACHE[remote_path] = [str(p.resolve()) for p in out if p.exists()]
                return out

            try:
                _e, _s, _f, paths = nuc.extract_dlt_files_from_archive(local_raw, output_extracted, skip_existing=True)
                valid_paths = keep_only_uncompressed_dlt(paths)
                if valid_paths:
                    out.extend(valid_paths)
                    local_raw.unlink(missing_ok=True)
                    _REMOTE_PAYLOAD_CACHE[remote_path] = [str(p.resolve()) for p in out if p.exists()]
                    return out
            except Exception:
                pass

            cli_paths = app.extract_with_7zip_cli(local_raw, output_extracted)
            cli_valid = keep_only_uncompressed_dlt(cli_paths)
            if cli_valid:
                out.extend(cli_valid)
                local_raw.unlink(missing_ok=True)
                _REMOTE_PAYLOAD_CACHE[remote_path] = [str(p.resolve()) for p in out if p.exists()]
                return out

            print(f"WARN zstd extract failed after retry for {local_raw.name}: {first_exc}")
            extraction_failures.append(f"{local_raw.name}: zstd extract failed after retry ({first_exc})")
            return out

        try:
            _e, _s, _f, paths = nuc.extract_dlt_files_from_archive(local_raw, output_extracted, skip_existing=True)
            out.extend(paths)
            local_raw.unlink(missing_ok=True)
        except Exception as exc:
            cli_paths = app.extract_with_7zip_cli(local_raw, output_extracted)
            if cli_paths:
                out.extend(cli_paths)
                local_raw.unlink(missing_ok=True)
            else:
                print(f"WARN extract failed for {local_raw.name}: {exc}")
                extraction_failures.append(f"{local_raw.name}: archive extraction failed ({exc})")
        _REMOTE_PAYLOAD_CACHE[remote_path] = [str(p.resolve()) for p in out if p.exists()]
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

    unique: list[Path] = []
    seen: set[Path] = set()
    for path in extracted_paths:
        rp = path.resolve()
        if rp in seen or not path.exists() or not path.name.lower().endswith(".dlt"):
            continue
        if nuc.get_compression_format(path) is not None:
            print(f"WARN still compressed: {path.name}")
            continue
        seen.add(rp)
        unique.append(path)
    return app.DownloadBatchResult(
        files=unique,
        attempted_payloads=len(matched),
        extraction_failures=extraction_failures,
    )


def main() -> int:
    settings = app.load_settings()
    now_utc = dt.datetime.utcnow()

    mode = str(settings["window_mode"])
    manual_start = app.parse_manual_datetime(str(settings["manual_start"])) if mode == "Manual" else None
    manual_end = app.parse_manual_datetime(str(settings["manual_end"])) if mode == "Manual" else None
    start_utc, end_utc = app.resolve_analysis_range(mode, manual_start, manual_end, now_utc)

    dtcs = app.parse_dtc_list(str(settings["dtc_list"]))

    run_id = dt.datetime.utcnow().strftime("headless_%Y%m%dT%H%M%SZ")
    run_dir = Path(settings["output_dir"]).expanduser().resolve() / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    print("Run dir:", run_dir)
    print("Range:", start_utc.isoformat(), "->", end_utc.isoformat())
    print("DTCs:", dtcs)

    storage_options = app.get_storage_options(lambda msg: print("[token]", msg))
    occurrences, ts_col = app.fetch_occurrences(
        storage_options,
        start_utc,
        end_utc,
        dtcs,
        lambda msg: print("[occ]", msg),
        refresh_storage_options_fn=lambda: app.get_storage_options(lambda msg: print("[token]", msg)),
    )
    print("Occurrences:", len(occurrences), "ts_col:", ts_col)

    nuc = load_module(Path(__file__).resolve().parent.parent / "NucDltWindowDownloader" / "nuc_dlt_window_downloader.py", "nuc")
    dlt_parser = load_module(Path(__file__).resolve().parent.parent / "DLTSearcher" / "dlt_searcher_gui.py", "dlt")
    azure_fs = nuc.create_azure_fs()

    matches: list[app.MatchResult] = []
    failures: list[str] = []
    parsed_cache: dict[Path, list[tuple]] = {}
    fault_reasons = app.load_fault_reasons(app.FAULT_CATALOG_FILE)
    reuse_files_by_vehicle: dict[tuple[str, str], list[Path]] = {}
    ordered_occurrences = sorted(
        occurrences,
        key=lambda occ: (occ.vin, occ.variant, occ.event_ts.date().isoformat(), occ.event_ts),
    )

    for idx, occ in enumerate(ordered_occurrences, start=1):
        print(f"[{idx}/{len(ordered_occurrences)}] {occ.vin} {occ.variant} {occ.dtc_id or occ.dtc_altvalue} @ {occ.event_ts.isoformat()}")
        vehicle_key = (occ.vin, occ.variant)
        reuse_candidates = [p for p in reuse_files_by_vehicle.get(vehicle_key, []) if p.exists()]

        best: app.MatchResult | None = None
        reuse_hit = False
        for dlt_file in reuse_candidates:
            if dlt_file not in parsed_cache:
                msgs, _ = dlt_parser.parse_dlt_file(str(dlt_file))
                parsed_cache[dlt_file] = msgs
            result = app.scan_messages_for_match(occ, dlt_file, parsed_cache[dlt_file], fault_reasons)
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
            matches.append(best)
            continue

        needs_deep_discovery = best is None or best.status == "NO_FAILED_DTC_LINE"
        if len(reuse_candidates) >= MAX_DLT_FILES_PER_VEHICLE and not needs_deep_discovery:
            if best is None:
                best = app.MatchResult(occurrence=occ, dlt_file=None, dtc_line=None, reason=None, reason_line=None, reason_offset_lines=None, dlt_line_index=None, status="NO_FAILED_DTC_LINE")
            matches.append(best)
            continue

        dlt_files: list[Path] = []
        occurrence_extraction_failures: list[str] = []
        last_exc: Exception | None = None
        center_ts = app.occurrence_event_ts_for_dlt(occ)
        try:
            if len(reuse_candidates) >= MAX_DLT_FILES_PER_VEHICLE:
                remaining_quota = FAILED_DISCOVERY_EXTRA_FILES
            else:
                remaining_quota = max(0, MAX_DLT_FILES_PER_VEHICLE - len(reuse_candidates))
            download_result = download_occurrence_files(nuc, azure_fs, occ, center_ts, run_dir, remaining_quota)
            dlt_files = download_result.files
            occurrence_extraction_failures.extend(download_result.extraction_failures)
        except Exception as exc:
            last_exc = exc

        if last_exc is not None and not dlt_files:
            failures.append(f"Download failed for {occ.vin}/{occ.event_ts.isoformat()}: {last_exc}")
            matches.append(app.MatchResult(occurrence=occ, dlt_file=None, dtc_line=None, reason=None, reason_line=None, reason_offset_lines=None, dlt_line_index=None, status="ERROR", error=str(last_exc)))
            continue

        if not dlt_files:
            try:
                adjacent_result = download_occurrence_files(
                    nuc,
                    azure_fs,
                    occ,
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
            matches.append(
                app.MatchResult(
                    occurrence=occ,
                    dlt_file=None,
                    dtc_line=None,
                    reason=None,
                    reason_line=None,
                    reason_offset_lines=None,
                    dlt_line_index=None,
                    status=status,
                    error="; ".join(occurrence_extraction_failures[:3]),
                )
            )
            continue

        for dlt_file in dlt_files:
            if dlt_file not in parsed_cache:
                msgs, _ = dlt_parser.parse_dlt_file(str(dlt_file))
                parsed_cache[dlt_file] = msgs
            result = app.scan_messages_for_match(occ, dlt_file, parsed_cache[dlt_file], fault_reasons)
            if best is None:
                best = result
            elif best.status != "MAPPED" and result.status == "MAPPED":
                best = result
            elif best.status == "NO_FAILED_DTC_LINE" and result.status == "UNMAPPED":
                best = result
            if result.status == "MAPPED":
                break

        if (best is None or best.status == "NO_FAILED_DTC_LINE") and len(dlt_files) > 0:
            print(f"[dim] No FAILED DTC line yet for {occ.vin}; trying one earlier/later DLT file.")
            try:
                adjacent_result = download_occurrence_files(
                    nuc,
                    azure_fs,
                    occ,
                    center_ts,
                    run_dir,
                    max_new_files=2,
                    include_adjacent_neighbors=True,
                )
                occurrence_extraction_failures.extend(adjacent_result.extraction_failures)
                adjacent_files = [p for p in adjacent_result.files if p not in dlt_files]
                dlt_files.extend(adjacent_files)

                for dlt_file in adjacent_files:
                    if dlt_file not in parsed_cache:
                        msgs, _ = dlt_parser.parse_dlt_file(str(dlt_file))
                        parsed_cache[dlt_file] = msgs
                    result = app.scan_messages_for_match(occ, dlt_file, parsed_cache[dlt_file], fault_reasons)
                    if best is None:
                        best = result
                    elif best.status != "MAPPED" and result.status == "MAPPED":
                        best = result
                    elif best.status == "NO_FAILED_DTC_LINE" and result.status == "UNMAPPED":
                        best = result
                    if result.status == "MAPPED":
                        break
            except Exception as exc:
                print(f"[dim] Adjacent file probe failed for {occ.vin}: {exc}")

        if (best is None or best.status == "NO_FAILED_DTC_LINE") and len(dlt_files) > 0:
            print(f"[dim] No FAILED DTC line yet for {occ.vin}; widening DLT discovery.")
            try:
                extra_result = download_occurrence_files(
                    nuc,
                    azure_fs,
                    occ,
                    center_ts,
                    run_dir,
                    FAILED_DISCOVERY_EXTRA_FILES,
                )
                occurrence_extraction_failures.extend(extra_result.extraction_failures)
                extra_files = extra_result.files
                for dlt_file in extra_files:
                    if dlt_file not in parsed_cache:
                        msgs, _ = dlt_parser.parse_dlt_file(str(dlt_file))
                        parsed_cache[dlt_file] = msgs
                    result = app.scan_messages_for_match(occ, dlt_file, parsed_cache[dlt_file], fault_reasons)
                    if best is None:
                        best = result
                    elif best.status != "MAPPED" and result.status == "MAPPED":
                        best = result
                    elif best.status == "NO_FAILED_DTC_LINE" and result.status == "UNMAPPED":
                        best = result
                    if result.status == "MAPPED":
                        break
            except Exception as exc:
                print(f"[dim] Deep discovery failed for {occ.vin}: {exc}")

        if best is None:
            best = app.MatchResult(
                occurrence=occ,
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

        matches.append(best)

    report_path = run_dir / "dtc_dlt_fault_report.html"
    report_text, referenced = app.build_html_report(start_utc, end_utc, dtcs, matches, failures, report_path)
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

    mapped_count = sum(1 for m in matches if m.reason)
    non_empty_dtc_line = sum(1 for m in matches if (m.dtc_line or "").strip())

    print("mapped_count", mapped_count)
    print("non_empty_dtc_line", non_empty_dtc_line)
    print("referenced", len(referenced))
    print("report", report_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
