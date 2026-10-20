# Function Definitions

## monitor_core.py
| Function | Intent | Inputs | Output |
| --- | --- | --- | --- |
| redact | Remove ANSI escapes and common credential forms before display/storage | Log text | Sanitized text |
| stream_url | Validate a Carbit viewer URL and select the authoritative Zeta stream | URL | Stream URL; raises ValueError on unsupported input |
| message_and_time | Normalize the two Carbit logging layouts and extract a timestamp | Line, fallback seconds | Message, seconds, timestamp identity |
| Detector.__init__ | Initialize one job's detection state | Retry count and minimum duration | Detector |
| Detector.reset_iterations | Clear per-test iteration count and timing samples | None | None |
| Detector.average_iteration_seconds | Compute average measured start-to-start duration (property) | None | Seconds or None before a measured interval |
| Detector.estimated_remaining_seconds | Multiply the measured average by iterations still to finish, including the current iteration; suppress unknown/failed estimates | None | Seconds, zero on confirmed success, or None |
| Detector.track_iteration | Recognize cycle total and exact iteration-start markers, reset at test boundaries, measure consecutive intervals | Message, log seconds, timestamp identity | Non-alerting progress events |
| Detector.connection_phase | Reset retry sequences at VCU power/suspend/wake/readiness boundaries and apply expected-downtime grace | Normalized message, log time | Whether connection failure is within expected downtime |
| Detector.consume | Classify unique messages without treating ordinary errors or partial completion as terminal | Line, current time | List of Event records |
| Event | Store evidence with independent job status, alert flag and display kind (info/success/progress) | Status, title, detail, alert flag, kind | Immutable event |
| ReplayGuard.__init__ | Initialize bounded replay tracking | None | Guard |
| ReplayGuard.reconnect | Reset stream position for a replay from the beginning | None | None |
| ReplayGuard.accept | Suppress replayed lines and reject changed source content | Line fingerprint | True for new content; raises ValueError on rotation/limit |

## transport.py
| Function | Intent | Inputs | Output |
| --- | --- | --- | --- |
| decode_event | Validate a JSON SSE event and select Zeta log lines | SSE data fields | Line or None |
| StreamWorker.__init__ | Configure a background reader | URL, bounded queue, stop event, timeout | Worker thread |
| StreamWorker.emit | Deliver ordered messages with cancellation-aware backpressure | Kind, value | None |
| StreamWorker.read_stream | Read bounded SSE frames and suppress replay | None | None; raises on disconnect/invalid source |
| StreamWorker.run | Reconnect with interruptible backoff, or stop on source mismatch | None | None |

## Tests
`tests/test_monitor.py` tests the supplied incomplete log (including no connection alarms), runner return codes, partial completion, duplicated retry messages, power-cycle retry separation, wake-deadline failure, DoIP versus SSH recovery, success classification/deduplication, timestamp-based iteration averages, missing/gapped markers and resets, ordinary errors, aborts, redaction, URL validation, replay and rotation. Each `test_*` method accepts no arguments and returns no value; assertions raise on regression.

`tests/test_transport.py`: `setUp` starts a local HTTP/SSE fixture and worker state; `tearDown` cancels and joins threads and closes the server. `Handler.do_GET` serves deterministic SSE frames, and `Handler.log_message` suppresses access logging. `test_sse_delivery_completion_and_replay` validates network delivery, terminal detection and reconnect suppression; the other `test_*` methods validate invalid MIME and JSON handling. All return None.

`tests/test_app.py`: `setUp` builds a withdrawn Tk window with notifications disabled (skips when Tk cannot open a display); `tearDown` destroys it. Its `test_*` methods check alert acknowledgement, terminal cancellation, bounded sanitized rendering, silence without false completion, success row styling/alert preservation, and progress display/session resets. All return None.

## app.py
| Function | Intent | Inputs | Output |
| --- | --- | --- | --- |
| desktop_toast | Send a best-effort silent Windows toast off the UI thread | Title, detail | None |
| AlarmApp.__init__ | Initialize one monitor window and session state | Tk root | Application |
| build_ui | Construct monitoring controls, status, events and log panes | None | None |
| set_status | Update the text/color banner with responsive evidence wrapping | Status, optional detail | None |
| prepare | Validate thresholds and reset a session | None | Whether session started |
| start | Validate URL and launch SSE worker | None | None |
| replay | Start offline example replay | None | None |
| replay_step | Process a bounded example chunk without blocking UI | None | None |
| process_line | Buffer sanitized lines, run detection and stop on terminal result | Line | None |
| update_progress | Display current iteration (one-based with raw index), total, measured average duration and estimated iteration time remaining | None | None |
| flush_log | Render a batch of sanitized lines and bound the visible history | None | None |
| record | Retain/display bounded event history and activate persistent alerts | Event | None |
| tick | Drain queue, check silence/disconnection and repeat sound | None | None |
| acknowledge | Silence persistent alerts and release always-on-top state | None | None |
| stop | Cancel monitoring without changing the remote job | Preserve-status flag | None |
| show_event | Open full selected event evidence | Optional Tk event | None |
| open_source | Open the validated viewer URL in browser | None | None |
| export | Save sanitized event history through a file chooser | None | None |
| close | Confirm closing an active monitor and cancel its worker | None | None |
| main | Start the Tk event loop | None | None |