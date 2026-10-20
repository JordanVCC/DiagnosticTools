# Function Definitions

Data flow: DLT Viewer → plugin (`AiAgentPlugin`) → localhost bridge (`AgentBridge`) ↔ agent process (`dlt_agent.py`) ↔ GitHub Copilot.

## plugin/agentbridge.cpp — `AgentBridge`

Localhost JSON-lines server (127.0.0.1, random port, random 256-bit token). Read-only access to the open `QDltFile`, plus table navigation.

| Function | Intent | Inputs | Outputs |
| --- | --- | --- | --- |
| `dltMessageToJson` | Serialise one message for the agent. | Global index, `QDltMsg`, max payload chars (0 = omit). | `{index,time,uptime_s,ecu,app,ctx,type,level,mode,payload}`. |
| `listen` / `port` / `token` | Open the localhost server and expose its credentials for the agent process. | — | Success; port; token. |
| `setFile` / `setTableView` / `setMessageDecoder` / `setSelected` | Receive DLT Viewer state from the plugin. New file cancels running scans. | File, table, decoder, selected message. | — |
| `sendEvent` | Push an event to the agent. | Event name, data. | JSON line `{"event":...}`. |
| `jumpTo` | Select and scroll the main table to a message (nearest visible message if filtered out). | `{index}`. | `{jumped_to_row, exact}` or error. |
| `handleLine` | Authenticate (first line must be `hello` + token) and dispatch requests/events. | JSON line. | Request handling or `agentEvent` signal. |
| `handleRequest` | Route agent methods: `file_info`, `get_selected`, `get_message`, `messages_around`, `rows`, `jump_to`, `search`, `statistics`. | id, method, params. | `{"id",result}` or `{"id",error}`. |
| `fileInfo` | Overview of the open log. | — | Files, total/visible counts, filter state, selected index. |
| `messagesAround` | Context around a message in the filtered or full view. | `{index,before≤100,after≤100,filtered}`. | Messages + whether the index is visible. |
| `rows` | Page of consecutive rows. | `{start_row,count≤200,filtered}`. | Messages with row numbers, total rows. |
| `runAsync` | Run `search`/`statistics` on a worker thread; replies only to the requesting connection. | id, method, params. | Deferred reply. |
| `runSearch` (static) | Bounded scan matching text/regex on `ECU APP CTX LEVEL PAYLOAD`, with level/app/ctx filters. | Query, regex, case, levels, app, ctx, max_results≤200, start_row. | Matches, rows scanned, truncation + `next_start_row`. |
| `runStatistics` (static) | Count messages per group and per level over the view. | group_by (`app_ctx`/`app`/`ctx`/`ecu`/`level`/`type`), top≤200. | Top groups with first/last index, level counts, time range. |
| `rowOfIndex` | Map a global index to a table row, mirroring DLT Viewer's jump behaviour. | Global index. | Row. |
| `readMessage` | Parse one message and apply decoder plugins (UI thread only). | Index, max payload chars. | Message JSON or empty. |

## plugin/agentpanel.cpp — `AgentPanel`

| Function | Intent | Inputs | Outputs |
| --- | --- | --- | --- |
| `appendUser` / `appendAssistantDelta` / `setAssistantMessage` / `appendTool` / `appendError` | Update the transcript (streamed text accumulates into the current reply). | Text. | Throttled Markdown re-render. |
| `setStatus` / `setSelectedIndex` / `setBusy` / `clearTranscript` | Panel state. | Text / index / flag. | — |
| signals `promptSubmitted`, `stopRequested`, `newChatRequested`, `jumpRequested` | User actions; `dlt://<index>` links emit `jumpRequested`. | — | — |

## plugin/aiagentplugin.cpp — `AiAgentPlugin`

Implements DLT Viewer's Plugin, Viewer and Control interfaces.

| Function | Intent | Inputs | Outputs |
| --- | --- | --- | --- |
| `initViewer` | Create the docked panel and wire its actions. | — | Panel widget. |
| `initFileStart` / `selectedIdxMsgDecoded` / `initMainTableView` / `initMessageDecoder` | Forward DLT Viewer state to the bridge. | File / selected message / table / decoder. | — |
| `onPrompt` | Queue a prompt and start the agent if needed. | Prompt text. | `user_prompt` event. |
| `onAgentEvent` | Render agent events: `assistant_delta`, `assistant_message`, `tool`, `status`, `error`, `turn_end`. | Event. | Panel updates. |
| `startAgent` / `stopAgent` | Launch `agent/.venv/Scripts/python.exe dlt_agent.py` (no console window) with port/token in its environment; shut down on unload. | `DLT_AGENT_DIR` (optional). | Agent process. |

## agent/dlt_agent.py

| Function | Intent | Inputs | Outputs |
| --- | --- | --- | --- |
| `BridgeClient.connect` / `request` / `send_event` | Authenticated JSON-lines client for the bridge; requests time out after 180 s. | Port, token, method, params. | Result dict or `BridgeError`; events on `events` queue. |
| `build_tools` | Define the eight read-only `dlt_*` Copilot tools mapped to bridge methods, plus `knowledge_lookup`. | Bridge. | Tool list. |
| `knowledge_files` / `knowledge_title` | List indexable files in `agent/knowledge/` (`.md .txt .csv .json .yaml`, excluding its README and dot-files such as the sync manifest) and derive each title from the first heading or `title:`. | — / path. | Paths / title. |
| `knowledge_index` | Compact file list (max 80) appended to the system prompt at session start. | — | Index text or empty. |
| `knowledge_sections` | Split a file into tokenised `Section`s of at most 1500 chars (headings capped at 120 chars): markdown headings, with long sections (e.g. register tables) and non-markdown files split on line boundaries as `heading (part n)`. Cached until the file's mtime changes. | Path. | `Section` list. |
| `knowledge_search` | Rank sections: first by how many identifier-like query terms (J349, MAX20087, VIDEO_LOCK) they contain, then BM25 with title (path + heading) boost. | Query. | Top 5 sections. |
| `knowledge_lookup` | Tool: `knowledge_search` results (max 1500 chars each), or read one file (max 12000 chars). Rejects paths outside the folder. | `{query}` or `{file}`. | Section text or error. |
| `deny_other_tools` | Reject any permission request outside the agent's own tools. | Request. | Reject decision. |
| `Agent.start` / `new_session` / `stop` | Start Copilot (logged-in user) and create a streaming session restricted to the agent's own tools, with the knowledge index in the system prompt and session store and memory disabled. | — | Session. |
| `Agent.prompt` / `abort` | Send a user prompt / cancel the running turn. | Text. | Session events forwarded to the panel. |
| `Agent._on_event` | Translate Copilot events into panel events. | Session event. | `assistant_delta`, `assistant_message`, `tool`, `error`, `turn_end`. |
| `run` / `main` | Connect, start Copilot, process `user_prompt` / `abort` / `reset` / `shutdown`. Logs to `agent/logs/agent.log`. | `DLT_AGENT_PORT`, `DLT_AGENT_TOKEN`. | Exit code. |

## agent/sync_knowledge.py

Runs in the agent environment (`agent/.venv`). Mirrors each folder in `agent/knowledge_sources.txt` to `agent/knowledge/sources/<folder name>/`.

| Function | Intent | Inputs | Outputs |
| --- | --- | --- | --- |
| `read_sources` | Source folders, one per line; `#` comments ignored. | `knowledge_sources.txt`. | Paths. |
| `output_path` | Mirrored output path; converted files get `.md`. | Source root, file. | Output path. |
| `convert_pdf` | PDF to Markdown with `pymupdf4llm` per page (about 1 s/page, CPU, tables as Markdown), with title and source header. Drawing pages (>20000 vector paths) use word-level text; pages keeping <85% of the PDF's words get their word-level text appended; text-less PDFs go to `convert_pdf_ocr`. Logs coverage. | PDF, output. | `.md` file. |
| `coverage_words` / `page_word_text` | Words used for coverage checks; page text rebuilt from PDF words line by line so labels like `AH41` stay separate. | Text / page. | Word set / text. |
| `convert_pdf_ocr` | OCR text-less PDFs (scans, outlined text) by running `pdf_to_markdown_tool` (marker-pdf) in `C:\pmt`. Slow (~45 s/page on CPU). | PDF, output. | `.md` file. |
| `convert_xlsx` | One Markdown table per non-empty sheet; fully empty columns dropped. | Workbook, output. | `.md` file. |
| `convert_url` | Record a `.url` shortcut's target as a link note. | Shortcut, output. | `.md` file. |
| `copy_text` | Copy text formats unchanged. | File, output. | Copied file. |
| `main` | Convert new/changed files (size + mtime + `CONVERTER_VERSION` in `.sync_manifest.json`), delete outputs whose source is gone, continue past failures. | — | Summary; exit 1 if any failure. |

## Build

| File | Intent |
| --- | --- |
| `build.bat` | MSVC 2022 + Qt 6.8.3 + Ninja build of upstream DLT Viewer with the plugin injected; deploys Qt DLLs and the offscreen platform. |
| `plugin/inject.cmake` | Adds the `aiagentplugin` target at the end of the upstream configure (via `CMAKE_PROJECT_dlt-viewer_INCLUDE`). |
