# Function Definitions

## `load_fault_reasons(catalog_path: Path) -> list[str]`
Intent: Load and deduplicate fault reason tokens from file.
Inputs: Fault-catalog file path.
Outputs: Ordered list of fault reason tokens.

## `parse_dtc_list(text: str) -> list[str]`
Intent: Parse comma/space-separated DTC input into normalized unique values.
Inputs: User-entered DTC text.
Outputs: Uppercase DTC IDs.

## `resolve_analysis_range(mode: str, manual_start: datetime | None, manual_end: datetime | None, now_utc: datetime) -> tuple[datetime, datetime]`
Intent: Convert selected time-window mode into UTC start/end timestamps.
Inputs: Mode (`24h`, `7d`, `30d`, `90d`, `Manual`) and optional manual datetimes.
Outputs: Inclusive UTC range.

## `build_month_globs(start_utc: datetime, end_utc: datetime) -> list[str]`
Intent: Build ADLS month partition globs for the selected range.
Inputs: UTC start and end timestamps.
Outputs: ABFS glob paths.

## `get_storage_options(log_fn) -> dict[str, str]`
Intent: Obtain Azure Storage bearer token used by parquet scans and cache it locally.
Inputs: Logging callback.
Outputs: Storage options dict with account name and bearer token.
Notes: Reuses non-expired token from `.token_cache.json`; otherwise fetches via Azure CLI with retry/backoff and extended per-attempt process timeout.

## `fetch_occurrences(...) -> list[Occurrence]`
Intent: Query ADLS DTC parquet and return filtered occurrence records.
Inputs: Date range, selected DTCs, storage options.
Outputs: Occurrence list for analysis.
Notes: Uses retry with backoff for transient Azure object-store failures and can refresh credentials via callback during retries. Also extracts top-level DTC booleans (`Confirmed`, `Pending`, `TestFailedSinceLastClear`) and nested `dtc_dict` status-byte flags (`B0..B7`) into each `Occurrence`. Also extracts onboard `TS20__UTC`/`TS21__UTC` "DTC time stamp" fields (see `dtc_ts20_utc`/`dtc_ts21_utc` below). Repeated readouts of the same VIN/DTC/variant are deduplicated by onboard trigger timestamp (`TS21__UTC`, then `TS20__UTC`), and each unique occurrence records its `read_count`. Discovers filename-timestamp-relevant parquet files via `build_month_globs_filtered`, then passes those concrete remote paths directly to polars for selective remote Parquet reads (no file download on the normal path). All app-level scans use `PARQUET_SCAN_CAST_OPTIONS`, which inserts missing struct fields and ignores newly added fields so evolving `dtc_dict` schemas across partitions do not abort the query. If direct remote reading fails, it switches to `download_parquet_files_locally` and retries from the persistent local cache; this fallback preserves operation during Azure/polars transport failures.

## `build_month_globs_filtered(start_utc: datetime, end_utc: datetime, log_fn) -> tuple[list[str], list[str]]`
Intent: Narrow month-level parquet partition globs down to only files whose filename timestamp falls within the requested window (+/- `FILE_LISTING_MARGIN_HOURS_BEFORE`/`_AFTER` for ingestion lag), instead of scanning every file in the month.
Inputs: UTC start/end, logging callback.
Outputs: `(discovered_remote_file_paths, fallback_month_globs)` — concrete remote file paths to scan directly, plus full-month `*.parquet` globs (per month) as a safety-net fallback when listing fails or nothing matched.
Notes: Uses `_get_listing_azure_fs()` (a cached `nuc.create_azure_fs()` handle) purely for cheap directory listing; parses filenames via `parse_month_partition_filename_ts`. The current safety margins are 12 hours before and 6 hours after the requested window.

## `download_parquet_files_locally(remote_paths: list[str], log_fn) -> list[Path]`
Intent: Download discovered parquet files to a persistent local cache (`PARQUET_CACHE_DIR`) via the same chunked, retrying `fs.open()` reader already used for DLT downloads, as a fallback when polars' direct remote Parquet reads fail.
Inputs: Remote file paths, logging callback.
Outputs: Local `Path` list for files that were already cached or successfully downloaded (partition files are immutable once written, so cache entries never go stale).
Notes: Downloads run concurrently (`PARQUET_FETCH_WORKERS` threads); failures are logged and simply omitted (caller falls back to a direct remote read for those specific files). Calls `_prune_parquet_cache(PARQUET_CACHE_MAX_BYTES)` afterward to bound total local cache size (oldest-by-mtime files evicted first).

## `collect_parallel_by_file(files: list[str], build_lazy_fn, label: str) -> pl.DataFrame`
Intent: Fetch multiple parquet files (local cache paths and/or remote fallback paths) concurrently (via `PARQUET_FETCH_WORKERS` threads) and concatenate results, instead of one serial combined `scan_parquet` over all files.
Inputs: File path list, a callable building a `pl.LazyFrame` for a given file subset, and a log label.
Outputs: Concatenated `pl.DataFrame` across all successfully fetched files.
Notes: Falls back to a single `collect_with_retry` call when 0-1 files are given (e.g. the full-month glob fallback case, where per-file parallelism isn't possible).

## `build_occurrence_cache_key(start_utc: datetime, end_utc: datetime, selected_dtcs: list[str]) -> str`
Intent: Build a stable hash key for caching first-stage occurrence results.
Inputs: Analysis time window and selected DTC IDs.
Outputs: Cache key string.

## `load_occurrence_cache(cache_key: str) -> tuple[list[Occurrence], str] | None`
Intent: Load cached occurrences and timestamp column by cache key.
Inputs: Cache key.
Outputs: Cached occurrences + timestamp column or None if unavailable.

## `save_occurrence_cache(cache_key: str, ts_col: str, occurrences: list[Occurrence]) -> None`
Intent: Persist occurrence query results and prune old cache files.
Inputs: Cache key, timestamp column, occurrence list.
Outputs: None.

## `load_occurrence_schema_cache() -> dict[str, str] | None`
Intent: Load cached parquet column mapping and timestamp dtype code to skip schema discovery on warm runs.
Inputs: None.
Outputs: Cached schema mapping or None.

## `save_occurrence_schema_cache(cache: dict[str, str]) -> None`
Intent: Persist parquet schema mapping for later occurrence-query runs.
Inputs: Schema mapping dictionary.
Outputs: None.

## `occurrence_to_dict(occ: Occurrence) -> dict[str, Any]` / `occurrence_from_dict(data: dict[str, Any]) -> Occurrence`
Intent: Convert `Occurrence` objects to/from JSON-safe dictionaries.
Inputs: `Occurrence` instance or dictionary payload.
Outputs: Serialized dictionary or reconstructed `Occurrence`.

## `match_to_dict(match: MatchResult) -> dict[str, Any]` / `match_from_dict(data: dict[str, Any]) -> MatchResult`
Intent: Convert `MatchResult` objects to/from JSON-safe dictionaries for persistence.
Inputs: `MatchResult` instance or dictionary payload.
Outputs: Serialized dictionary or reconstructed `MatchResult`.
Notes: Persisted match payloads now also carry correlated ConfigHub-style baseline summaries (`SPA*_INT`), optional delta-from-DTC timing, and baseline provenance (`DIRECT` vs `VIN_FALLBACK:<file>`).

## `summarize_confighub_baseline(line: str) -> str | None`
Intent: Parse a DLT payload line into a compact ConfigHub baseline summary.
Inputs: DLT message text.
Outputs: Compact `SPA*_INT` or startup software-build summary when present.
Notes: Also recognizes `cs-software-product@<build>, built@<date-time>` records found near the beginning of DLT logging cycles and returns them as `STARTUP_BUILD: <build> (built <date-time>)`.

## `find_confighub_baseline(messages, anchor_index) -> tuple[str | None, float | None]`
Intent: Find the best nearby ConfigHub baseline marker to use as baseline context for a DTC occurrence.
Inputs: Parsed DLT messages and optional anchor message index.
Outputs: Compact baseline summary and optional delta in seconds relative to the anchor message.

## `find_message_index_near_event_ts(messages, event_ts) -> int | None`
Intent: Find the message index nearest to an occurrence timestamp for cross-file baseline correlation.
Inputs: Parsed DLT messages and occurrence event timestamp.
Outputs: Closest message index with a valid timestamp, or None.

## `save_analysis_checkpoint(...) -> None`
Intent: Persist crash-safe per-run progress after each processed occurrence.
Inputs: Checkpoint path, run metadata, ordered occurrence list, next index, partial matches, failures, completion flag.
Outputs: None.
Notes: Uses write-to-temp then atomic replace to reduce risk of partial/corrupt checkpoint files.

## `load_analysis_checkpoint(checkpoint_path: Path) -> dict[str, Any] | None`
Intent: Load a run checkpoint JSON document.
Inputs: Checkpoint file path.
Outputs: Parsed checkpoint dictionary or None.

## `find_latest_incomplete_checkpoint(output_dir: Path) -> Path | None`
Intent: Find the newest unfinished checkpoint under `run_*/analysis_checkpoint.json`.
Inputs: Runs output directory.
Outputs: Checkpoint path or None.

## `build_timestamp_expr_from_code(ts_col: str, ts_dtype_code: str) -> pl.Expr`
Intent: Build timestamp parsing expression from cached dtype code without reading parquet schema.
Inputs: Timestamp column name and cached dtype code.
Outputs: Polars expression for normalized event timestamp.

## `download_dlt_window_for_occurrence(...) -> list[Path]`
Intent: Download and extract DLT payloads for one occurrence window.
Inputs: Occurrence data, output directory, NUC helper module.
Outputs: Local DLT file paths for that occurrence.
Notes: Uses in-memory Azure variant-path and day-listing caches, resumable Azure download retries with size checks, and zstd re-download-on-failure fallback before giving up. Multiple candidate DLT payloads for the same occurrence are downloaded/extracted concurrently via `PARALLEL_FILE_WORKERS` (12) threads, and each zstd payload first attempts `stream_decompress_remote_zst_to_file` to avoid a local copy of the compressed archive. Variant-path lookup, day-listing lookup, and per-payload processing are each serialized with a per-key lock (`App._get_keyed_lock`) so concurrent callers (main loop + background prefetch, see `_run_analysis`) targeting the same Azure key never duplicate work or race; actual network stream opens are additionally bounded by `App._azure_io_semaphore` (`MAX_CONCURRENT_AZURE_STREAMS`, 16) across all callers combined.

## `App._get_keyed_lock(key: Any) -> threading.Lock`
Intent: Return (creating if needed) a lock scoped to an arbitrary cache key, so concurrent work on the same key is serialized while different keys proceed in parallel.
Inputs: Hashable key, e.g. `("variant", (vin, variant))`, `("day", day_path)`, `("payload", remote_path)`.
Outputs: A `threading.Lock` for that key.
Notes: Backed by `App._keyed_locks` + `App._keyed_locks_meta_lock`; used by `_download_occurrence_files` and `process_payload` to make occurrence-level prefetch safe.

## `_order_occurrences_for_reuse(occurrences: list[Occurrence]) -> list[Occurrence]`
Intent: Reorder occurrences by VIN/variant/day/time to maximize cache hits during Azure listing and payload reuse.
Inputs: Occurrence list.
Outputs: Reordered occurrence list.
Notes: Run loop also reuses already-downloaded DLT files per VIN/variant before downloading new files.

## Background prefetch pipeline in `_run_analysis`
Intent: Overlap network downloads for upcoming occurrences with parsing/scanning of the current occurrence, since the main occurrence loop is otherwise strictly sequential (required for checkpoint ordering and per-vehicle cache reuse).
Mechanism: A `PREFETCH_WORKERS`-sized (4) background `ThreadPoolExecutor` is created alongside `azure_fs`. On each main-loop iteration, `_schedule_prefetch_ahead_of(idx)` submits best-effort "standard" `_download_occurrence_files` calls for the next `PREFETCH_LOOKAHEAD` (4) occurrences that are not already fully covered by `reuse_files_by_vehicle`; all occurrences are eligible regardless of current TestFailed/Confirmed/Pending values. Results are only used as a disk/cache warm-up — the main loop still performs its own (now cache-hitting) download call and all real status/error handling when it reaches that occurrence. Prefetch failures are swallowed silently. Concurrency correctness relies on `App._get_keyed_lock` (dedup) and `App._azure_io_semaphore` (connection cap); `prefetch_executor.shutdown(wait=False, cancel_futures=True)` runs in the outer `finally` so cancellation/completion never hangs on in-flight prefetch work.

## `occurrence_event_ts_for_dlt(occurrence: Occurrence) -> datetime`
Intent: Determine the UTC timestamp used to center the DLT search window for an occurrence.
Inputs: Occurrence (including source timestamp column and onboard `dtc_ts20_utc`/`dtc_ts21_utc`).
Outputs: UTC-normalized timestamp used to center DLT download window.
Notes: Prefers `dtc_ts21_utc` then `dtc_ts20_utc` (onboard "DTC time stamp" extended-data fields, already UTC — when the ECU actually detected/confirmed the DTC) over the read/ingestion timestamp. Falls back to legacy behavior treating `TS21_local`, `TS20_local`, and `vtStart` as Europe/Stockholm local timestamps and converting to UTC when neither onboard field is available.

## `occurrence_trigger_ts(occurrence: Occurrence) -> datetime`
Intent: Return the canonical timestamp at which the ECU set/detected the DTC for analysis.
Inputs: Occurrence.
Outputs: `dtc_ts21_utc`, then `dtc_ts20_utc`, then the legacy converted event timestamp.
Notes: Used for DLT file selection, message anchoring, baseline correlation, retry decisions, run logging, and report grouping. `Occurrence.event_ts` remains the read/poll timestamp and is displayed separately for provenance; `Occurrence.read_count` records how many DTC readouts were collapsed into that trigger occurrence.

## `build_candidate_dlt_centers(occurrence: Occurrence) -> list[datetime]`
Intent: Build an ordered list of timestamp centers used to pick the best DLT file.
Inputs: Occurrence timestamp and source column.
Outputs: Candidate center timestamps from both converted and raw occurrence times, with ±1h/±2h/±3h/±4h probes.

## `pick_first_after_dlt_candidate(all_candidates, center_ts) -> tuple[str, str, int | None] | None`
Intent: Select the first DLT whose filename timestamp is strictly greater than the given occurrence timestamp.
Inputs: Candidate DLT entries with parsed filename timestamps and the occurrence center timestamp.
Outputs: A single candidate tuple or None when no later file exists.

## `pick_first_after_dlt_candidate_for_centers(all_candidates, centers) -> list[tuple[str, str, int | None]]`
Intent: Apply strict first-after selection across ordered centers (raw first, converted second) without duplicates.
Inputs: Candidate DLT entries and ordered center timestamps.
Outputs: Ordered candidate tuples for first-attempt download.

## `select_relevant_dlt_candidates(all_candidates, center_ts, max_count=2) -> list[tuple[str, str, int | None]]`
Intent: Choose a small prioritized candidate set around a center timestamp (prefer nearest <= center, then nearest > center).
Inputs: Parsed DLT filename candidates with timestamps and center timestamp.
Outputs: Ordered candidate tuples for download/scan, bounded by `max_count`.
Notes: Used by standard scan modes. First-attempt mode now uses strict first-after filename timestamp selection.

## `pick_adjacent_dlt_candidates(all_candidates, selected_remote_paths, max_per_side=1) -> list[tuple[str, str, int | None]]`
Intent: When a selected DLT does not contain a FAILED line, explicitly probe neighboring files in timeline order.
Inputs: Full candidate timeline and selected remote paths.
Outputs: Up to one earlier and one later candidate per selected file.

## `DownloadBatchResult`
Intent: Carry download/extract outcomes beyond just extracted file paths.
Fields: `files`, `attempted_payloads`, `extraction_failures`.
Usage: Enables report statuses that distinguish "no DLT found" from "DLT candidate failed extraction".

## `decompress_zst_stream_to_file(source: Path, destination: Path) -> bool`
Intent: Stream-decompress zstd payloads directly to file to avoid large-memory decompression failures.
Inputs: Source compressed payload path and destination output path.
Outputs: True on success, False on failure.
Notes: Compression handling now uses strict magic-byte detection first; `.zst` extraction uses streaming decompression as primary path with DLT magic-byte validation, then falls back to downloader extractor and optional 7zip CLI only if needed.

## `stream_decompress_remote_zst_to_file(azure_fs, remote_path: str, destination: Path, io_semaphore: threading.Semaphore | None = None) -> tuple[bool, bytes]`
Intent: Read a remote zstd DLT payload straight from Azure and decompress it in-flight to the final `.dlt` path, without ever writing the compressed archive to local disk.
Inputs: Open Azure filesystem handle, remote payload path, destination `.dlt` path, optional semaphore bounding concurrent Azure stream opens.
Outputs: `(True, magic_bytes)` on success; `(False, magic_bytes)` when the payload isn't zstd or `zstandard` is unavailable; `(False, b"")` on stream/decompression failure.
Notes: Used as the first attempt in `process_payload` (inside `_download_occurrence_files`); falls back to the existing download-then-extract path on any failure or non-zstd magic. Called with `App._azure_io_semaphore` to cap total concurrent Azure connections across the main loop and background prefetch workers.

## `extract_with_7zip_cli(archive_path: Path, output_dir: Path) -> list[Path]`
Intent: Provide a best-effort external extractor fallback compatible with manual 7zip results.
Inputs: Archive payload path and extraction output directory.
Outputs: Extracted `.dlt` paths; empty list when 7zip is unavailable or extraction fails.

## `parse_dlt_file_messages(...) -> list[DltMessage]`
Intent: Parse DLT files into searchable message records.
Inputs: Local DLT path and parser module.
Outputs: Parsed messages.

## `scan_messages_for_match(...) -> MatchResult`
Intent: Locate a strict FAILED DTC report line and correlate a fault reason near it.
Inputs: Occurrence, parsed messages, reason token list.
Outputs: Match object with DTC line, reason, snippets, source file, and correlated ConfigHub baseline context.
Notes: Correlation is restricted to catalog `k...` fault reason tokens. It prioritizes same-camera (`SRCB/SRCF/SRCL/SRCR`) reason lines closest in message timestamp to the FAILED DTC line (preferring preceding lines), with a narrow line-window fallback only when message timestamps are unavailable. It also records reason delta time (seconds), the first post-reason camera service state (`Deactivated`, `selfhealing`, `relinking`, `streaming`, `cooldown`) with state line and delta-from-reason time, and the nearest `SPA*_INT` baseline summary from DLT messages (with hint-boost for lines mentioning ConfigHub/baseline/software version).

## `scan_and_log_match(...) -> MatchResult`
Intent: Run `scan_messages_for_match` and emit progress messages when a FAILED DTC line or catalog fault reason is found.
Inputs: Occurrence, DLT path, parsed messages.
Outputs: The same `MatchResult` returned by `scan_messages_for_match`.
Notes: Logs the VIN, DTC, trigger timestamp, DLT filename, and correlated reason through the existing analysis log queue. It is used for reused files and all retry phases.

## `log_scan_outcome(...) -> None`
Intent: Emit an explicit completion message after an initial or retry DLT scan.
Inputs: Occurrence, phase label, best `MatchResult`, and number of DLT files examined.
Outputs: None.
Notes: Reports whether the phase found both a FAILED line and fault reason, found only the FAILED line, found no FAILED line, found no DLT files, or encountered extraction failure. This prevents retry phases from appearing to silently advance to the next occurrence.

## Discovery pass ordering in `_run_analysis`
For each occurrence that has not yet been matched (MAPPED/UNMAPPED):
0. **Crash-safe resume**: if the user chooses to resume and the checkpoint is valid/incomplete, restore the checkpoint snapshot (`start/end`, DTC set, ordered occurrence list, `matches`, `failures`) and continue from `next_index` without recomputing a moving time-window query.
1. **All occurrences**: every occurrence proceeds to DLT analysis. `TestFailed`, `Confirmed`, and `Pending` values are retained as evidence in the report but do not suppress analysis.
2. **Standard**: initial `_download_occurrence_files` call centered on `occurrence_trigger_ts(occurrence)` (onboard TS21/TS20 DTC trigger time when available; legacy Stockholm→UTC conversion for vtStart columns otherwise).
3. **Adjacent**: if no FAILED line found, expand by one neighboring DLT file each side.
4. **Widened**: if still no FAILED line, re-query with `FAILED_DISCOVERY_EXTRA_FILES` quota.
5. **UTC-assumed TZ retry**: if still no FAILED line and no onboard TS20/TS21 trigger timestamp exists, re-query treating vtStart as pure UTC (neutralises the Stockholm -2 h offset). Targets vehicles whose NUC logger has been updated to ≥ 8.2.36 (post-2026-05-21), which switched vtStart from Swedish local time to UTC.
6. **Memory guardrails**: parsed DLT message arrays are cached with an LRU cap (`PARSED_DLT_CACHE_MAX_FILES`) and reset when VIN/variant changes, preventing unbounded RAM growth in long runs.
7. **Retry-phase visibility**: retries emit both a start log in the form `[occurrence_index/total_occurrences] Retry phase X/Y: ...` and an explicit completion outcome identifying success, partial match, no match, no DLT, or extraction failure.
8. **Checkpoint update**: after every processed occurrence (including error statuses), write `analysis_checkpoint.json` with updated `next_index`, partial results, and failures.
9. **Baseline fallback**: when no baseline is found in the primary DLT analysis path, search up to 200 already-downloaded DLTs for the same VIN/variant in chronological filename order, including the earliest startup/logging-cycle files; use the nearest `SPA*_INT` or startup software-build marker by timestamp and report provenance as `VIN_FALLBACK:<file>`.

## `build_html_report(...) -> str`
Intent: Generate grouped mapped/unmapped/failure HTML report.
Inputs: Run metadata, matches, failures.
Outputs: HTML report content, including total DTC readouts, unique trigger-based DTC occurrences, grouped mapped reasons by trigger date, separate DTC trigger/read timestamps, per-occurrence correlation details (correlated ConfigHub/startup baseline summary, baseline source, baseline delta seconds, reason, correlated line, reason delta seconds, camera service state, state line, state delta seconds), top-level DTC boolean badges, status-byte (`B0..B7`) summaries, and two unmapped sections: (a) `testFailed == 1` not mapped, and (b) `testFailed == 0 or unknown`; both sections are analyzed for DLT mapping and include a per-row `DLT Mapping Attempted` indicator.

## `_open_report() -> None`
Intent: Open the latest generated report file in the default system browser.
Inputs: Last report path tracked by the GUI state.
Outputs: None.

## `find_incomplete_checkpoints(output_dir: Path) -> list[Path]`
Intent: Find every valid unfinished analysis checkpoint under the configured output directory.
Inputs: Output directory.
Outputs: Incomplete checkpoint paths, newest first.
Notes: Ignores unreadable checkpoints and completed runs. Used by the incomplete-runs manager; `find_latest_incomplete_checkpoint` remains a compatibility wrapper returning its first result.

## `App._show_incomplete_runs_manager(output_dir: Path) -> Path | None`
Intent: Present all incomplete runs in a selectable manager before a new analysis begins.
Inputs: Configured output directory.
Outputs: Selected checkpoint path when Resume Selected is chosen, otherwise None.
Notes: Shows run folder, saved progress, last update time, and DTC list. Supports Resume Selected (including double-click), Remove Selected, Remove All, and Start New Analysis. Removals require confirmation and use `_remove_incomplete_run` safety checks.

## `App._remove_incomplete_run(checkpoint_path: Path, output_dir: Path) -> bool`
Intent: Remove an incomplete run's checkpoint and associated files after the user explicitly chooses Remove progress.
Inputs: Checkpoint path and configured output directory.
Outputs: True when the run folder was removed; False when validation or deletion failed.
Notes: Deletes only a `run_*` directory directly beneath the configured output directory, preventing accidental deletion outside the analysis output tree.

## `write_report_artifacts(...) -> ReportArtifacts`
Intent: Persist report and sidecar reference files.
Inputs: Report content, referenced paths, output folder.
Outputs: Paths to generated artifacts.

## `compute_storage_summary(run_dir: Path, referenced_paths: set[Path]) -> StorageSummary`
Intent: Compute total and referenced file counts/sizes.
Inputs: Run output directory and referenced DLT set.
Outputs: Storage summary values for UI.

## `cleanup_all_downloads(run_dir: Path, keep_paths: set[Path]) -> CleanupResult`
Intent: Delete run downloads while preserving report artifacts.
Inputs: Run folder and explicit keep set.
Outputs: Deleted count/size summary.

## `cleanup_keep_referenced(run_dir: Path, referenced_paths: set[Path], keep_paths: set[Path]) -> CleanupResult`
Intent: Delete all unreferenced DLT files while preserving report artifacts.
Inputs: Run folder, referenced DLT set, explicit keep set.
Outputs: Deleted count/size summary.
