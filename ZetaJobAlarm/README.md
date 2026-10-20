# Zeta Job Alarm

Windows desktop monitor for a Carbit/Zeta live-log URL. It never launches, stops, or changes the remote job or carbit repository.

## Run

Double-click `Launch_Zeta_Job_Alarm.bat`. Paste a URL such as `http://10.246.64.251:8766/view?file=zeta_log.txt` and select **Start Monitoring**. Keep the application open. **Stop** only stops monitoring.

Python 3.10+ with Tk is required. The launcher prefers the workspace's existing `.venv`, otherwise uses `py -3`. Install optional Windows toast support in that interpreter with `python -m pip install -r requirements.txt`. Without it, the banner, focus alert and sound still work. Windows notification settings / Do Not Disturb can suppress toasts. Windows must have network/VPN access to the rig.

## Detection

- Uses the actual `/stream?file=zeta_log.txt` JSON SSE endpoint, not HTML scraping.
- Confirms execution completion from `Run finished with return code N`, or the runner's exact 40-star Success/Failed/Abort banner. Partial setup/session/thread completion never counts.
- Confirms execution failure from `Run failed with error: ...` and recognizes explicit runtime/startup abort messages.
- Alerts on sustained connection failures: by default at least three distinct attempts spanning 60 seconds, grouped by address/target. Duplicate logging formats do not inflate retries. Gaps over twice the retry span (minimum 120 seconds) reset the retry sequence. This indicates a possible blocker, not proof the job failed.
- VCU power-off, confirmed suspend, power-on, wake requests, and readiness markers separate retry sequences. Connection failures during powered-off/suspended periods and wake/startup grace remain visible without interrupting alarms. An explicit `Waiting for VCU to become on (timeout: Ns)...` sets the grace deadline; otherwise power-on/wake uses the configured retry span. A new connection failure after that deadline alerts even before the ordinary retry threshold is reached. Deadline passage alone does not prove failure; absent output is handled by the silence warning.
- VCU readiness / platform `Run` clears prior phase retry evidence, but does not prove SSH recovered. DoIP vehicle connection success alone never clears SSH retry evidence. The sample's four HPA failures spanning 109 seconds cross separate power/wake phases and no longer produce a persistent-connection alarm.
- Tracebacks/critical errors need attention; ordinary ERROR messages are recorded without declaring failure. Optional HPA failures can trigger sustained-connection warnings; inspect the evidence before assuming the VCU is inaccessible.
- No output for five minutes triggers an attention alert, not completion. Adjust thresholds before monitoring. Unavailable source for 15 seconds triggers an unknown-status alert; reconnects use bounded backoff.
- The source replays from the beginning on reconnect. Matching fingerprints suppress that replay; changed content stops monitoring with an explicit source-change alert. Start a fresh session for a new job on the same URL.

**Important:** The pipeline stops accepting new live-log connections before final reporting. Existing stream connections may still receive final lines, but shutdown/network loss can hide them. A disconnect never proves success. Reported completion is execution completion, not confirmation that artifact uploads are finished. For guaranteed notification when terminal markers cannot be streamed, the runner needs a durable job-status endpoint or a longer-lived log service; this tool does not change carbit.

## Alerts And History

**Est. remaining** multiplies the measured average iteration duration by the number of iterations still to finish, including the current unfinished iteration. It refreshes at iteration boundaries rather than acting as a second-by-second countdown, and stays `--` until a total and a measured average are available. It resets for a new test, becomes zero on confirmed execution success, and is unavailable after failure/abort. This estimates iteration work only, not later cleanup or artifact uploads; unusually slow iterations or recovery can change the estimate.

The Events tab includes green **Success reported** entries for SUCCESS-level messages, explicit success wording, and confirmed VCU suspend/readiness milestones. Iteration starts also appear as non-interrupting progress events. These entries do not declare job completion, clear attention alerts, or play sounds.

A progress row above the tabs shows the current iteration, the configured standby-cycle total when logged, and average time per iteration. Zero-based logs display **Iteration 1 / 200 (log #0)** for the first cycle. The average uses timestamps between consecutive iteration-start markers, not monitor receive time, so replay and reconnect do not distort it. It includes recovery and other work between starts, excludes setup before the first start and the currently unfinished interval, and remains `--` until a timed interval is available. Duplicate starts and gaps in iteration numbering do not create timing samples. A new test case or restarted iteration sequence resets the average. Starting the next iteration is progress evidence, not proof that the previous iteration passed.

Sound repeats every ten seconds until **Acknowledge**. With **Bring to front**, the window stays above other windows until acknowledged. Turn either option off independently. **Test Alert** checks local notifications without contacting a rig. **Replay Example** exercises the supplied incomplete log without network access.

Events and the last approximately 5,000 sanitized log lines are kept in memory. **Export Events** writes up to 1,000 recent events as JSON; double-click an event to see full evidence. No logs or URL are automatically written to disk. Redaction covers common credential labels, JWTs and URL user-info, but is not a guarantee against every possible secret format. Treat original logs and exported evidence as sensitive. The supplied example itself contains credential-like values and should not be shared publicly.

Streaming has a 1 MB per-event limit, a bounded delivery queue, and a one-million-line replay limit. The app reports unsupported sources/rotation rather than silently mixing jobs. Closing the app stops notifications; there is no background service or system-tray mode.

## Tests

From this folder: `python -m unittest discover -s tests -t . -v`.

See `FUNCTION_DEFINITIONS.md` for the implementation reference.