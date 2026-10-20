# Function Definitions

Inputs below omit `self`. Unless stated otherwise, GUI methods return `None`
and communicate through widgets or thread-safe queues. Exceptions report invalid
inputs, authentication failures, network errors, or cancellation.

## Sources And Authentication

Authenticated NUC Drive HTTP is preferred when `HTTP_OPENER` is available.
Otherwise Azure reads only `raw-archive-storage/data_nuc/public`; recent drive
logs may not be archived yet. Browser session cookies remain in memory only.
An empty Azure scan triggers interactive Drive authentication and retries the
same download on HTTP. Authentication failure is reported, not treated as an
empty archive result. Explicit sign-in failures also display an error dialog.

| Function | Intent | Inputs | Outputs |
| --- | --- | --- | --- |
| `open_http_response` | Open HTTP with current session; reject authentication redirects | Request, timeout seconds | Response; `NucAuthenticationError` on redirect |
| `create_authenticated_http_opener` | Import only cookies applicable to NUC Drive | Browser cookie dictionaries | Cookie-aware urllib opener |
| `authenticate_nuc_drive` | Sign in interactively with bundled Chromium; verify session; explain timeout or premature closure | None | Authenticated opener; browser closes; `NucAuthenticationError` for timeout/closure |
| `create_azure_fs` | Initialize Azure credentials and filesystem | None | fsspec filesystem |
| `azure_list_names` | List immediate children | Filesystem, path | Names; empty list for missing path |
| `azure_list_files` | List files and sizes | Filesystem, path | `(name, size)` pairs; empty list for missing path |
| `azure_find_child_name` | Match child case-insensitively | Filesystem, parent, target | Name or `None` |
| `azure_find_dlt_dir_name` | Resolve exact or containing DLT directory | Filesystem, VIN root | Name or `None` |
| `fetch_links` | Parse HTTP directory listing | URL | `(name, URL, is_directory)` tuples |
| `find_child_dir` | Resolve named directory | Parent URL, target | URL or `None` |
| `find_child_dir_numeric` | Resolve padded or unpadded numeric directory | Parent URL, integer | URL or `None` |
| `find_dlt_dir` | Resolve exact or containing DLT directory | VIN URL | URL or `None` |

`create_azure_fs` nests `_sync_close_wrapper()` and `_async_close_wrapper()`:
no inputs; invoke the credential close method and adapt its result to awaitable cleanup.

## File Processing

| Function | Intent | Inputs | Outputs |
| --- | --- | --- | --- |
| `format_bytes` | Format byte count | Nonnegative integer | Human-readable string |
| `parse_filename_timestamp` | Parse YYYYMMDDTHHMMSS timestamp | Filename | Naive datetime or `None` |
| `is_archive_candidate_name` | Recognize archive extensions | Filename | Boolean |
| `is_supported_dlt_payload_name` | Recognize raw DLT or archive | Filename | Boolean |
| `daterange` | Iterate inclusive dates | Start and end date | Date iterator |
| `is_timeout_error` | Recognize timeout errors | Exception | Boolean |
| `is_transient_network_error` | Recognize retryable network errors | Exception | Boolean |
| `get_compression_format` | Detect magic bytes or extension | Path | Format name or `None` |
| `is_archive_file` | Check detected archive format | Path | Boolean |
| `is_valid_dlt_file` | Check nonempty regular DLT file | Path | Boolean; not a full DLT protocol validator |
| `remove_stray_path` | Remove unwanted file or directory | Path | None; filesystem mutation |
| `get_single_file_dlt_counterpart_path` | Resolve decompressed DLT filename | Filename, output directory | Path or `None` |
| `get_remote_file_size` | Read Content-Length with retries | URL, retry count | Byte count or `None`; authentication failures propagate |
| `ensure_unique_path` | Choose unused numbered path | Path | Available path |
| `get_local_file_size` | Read file size | Path | Byte count; zero if missing/error |
| `download_file` | Stream download with retry, resume, cancellation | URL, destination, chunk callback, retries, resume offset, cancel event, retry callback | None; writes destination |
| `extract_dlt_files_from_archive` | Dispatch extraction and remove processed archive | Archive, output directory, skip-existing flag | `(extracted, skipped, archives_removed, paths)` |
| `_extract_zip` | Extract flattened ZIP DLT members | ZIP path, output directory, skip flag | `(extracted, skipped, found, paths)` |
| `_extract_compressed_single` | Decompress individual DLT | Archive, output directory, skip flag, format | `(extracted, skipped, found, paths)` |
| `_extract_tar` | Extract flattened TAR DLT members | TAR path, output directory, skip flag | `(extracted, skipped, found, paths)` |
| `_extract_tar_from_stream` | Decompress and extract TAR stream | Archive, output directory, skip flag, format | `(extracted, skipped, found, paths)` |
| `_decompress_file` | Decompress to file | Source path, destination path, format | None; writes file |
| `_decompress_to_bytes` | Decompress in memory | Source path, format | Bytes |
| `combine_dlt_files` | Concatenate source DLT files in order | Source paths, output path | None; writes combined file |
| `main` | Run application | None | None; Tk event loop |

## GUI Methods

| Method | Intent | Inputs | Outputs / Side Effects |
| --- | --- | --- | --- |
| `LinkParser.__init__` | Initialize link parser | None | Initializes links |
| `LinkParser.handle_starttag` | Collect anchor hrefs | Tag, attributes | Appends links |
| `DateTimeSelector.__init__` | Create date/time controls | Parent, title, default datetime | Widgets |
| `DateTimeSelector.set_now` | Set current date/time | None | Updates fields |
| `DateTimeSelector._parse_component` | Validate time component | Value, label, lower/upper bounds | Integer |
| `DateTimeSelector.get_datetime` | Validate combined date/time | None | Naive datetime |
| `DownloaderApp.__init__` | Initialize theme, state, queues, VIN loading | None | Application window |
| `_build_ui` | Create controls and scrolling | None | Widgets and bindings |
| `_on_vin_selected`, `_on_vin_keyrelease` | Filter VIN choices after input | Optional event | Dropdown changes |
| `_filter_vin_values` | Prioritize prefix/substring matches | Query | Dropdown changes |
| `_start_http_sign_in` | Start sign-in when idle | None | Background thread; disables sign-in/refresh |
| `_http_sign_in_worker` | Authenticate, prefer Drive, reload VINs; surface failures | None | In-memory opener; queued UI updates and error dialog on failure |
| `_start_vin_refresh` | Start VIN lookup | None | Background thread |
| `_load_vins_worker` | Load VINs from authenticated Drive or Azure/fallback | None | VIN/error actions queued |
| `_set_loaded_vins` | Apply loaded choices | VIN names | Widgets/log updated |
| `_set_vin_load_error` | Show lookup error | Error text | Widgets/log updated |
| `_browse_output` | Choose output directory | None | Output field updated |
| `_clear_log` | Clear log | None | Log widget cleared |
| `_append_log` | Display log text | Text | Log widget updated |
| `log` | Queue timestamped text | Message | Log queue updated |
| `_drain_queues` | Dispatch background messages | None | Widgets updated; schedules next drain |
| `_handle_ui_action` | Handle queued action | Action tuple | Widgets/dialogs updated |
| `_set_progress_mode` | Configure progress bar | Mode, maximum, value | Progress widgets updated |
| `stop_download` | Request cancellation | None | Cancellation event set |
| `_raise_if_cancelled` | Check cancellation | None | Raises `DownloadCancelledError` if set |
| `set_running` | Toggle operation controls | Running flag | Button states updated |
| `start_download` | Validate window and launch worker | None | Download thread |
| `_run_download` | Discover, download, extract, combine; authenticate and retry Drive on archive miss | VIN, variant, start/end datetime, output directory, skip/combine flags | Files; in-memory session on fallback; progress and completion/error actions |
| `_on_closing` | Cancel operations and close | None | Waits briefly for workers; destroys window |

Nested `_build_ui` handlers: `_on_root_configure(event=None)` updates scroll
bounds; `_on_canvas_configure(event)` sizes the inner window; `_on_mouse_wheel(event)`
scrolls eligible widgets and returns `"break"` when handled.

Nested `_run_download` helpers: `estimate_single_file(args)` accepts filename,
URL, day and index and returns those with remote size; `emit_speed_update()` queues
speed/progress; `speed_monitor()` periodically emits speed until stopped;
`process_single_file(args)` accepts index, filename, URL, day and remote size and
returns per-file results; its `on_chunk(chunk_len)` updates byte counters.

`DownloadCancelledError` signals cancellation; `NucAuthenticationError` distinguishes
expired/missing HTTP sessions from recoverable day-level scan errors.