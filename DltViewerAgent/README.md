# DLT Viewer Agent

The official [COVESA DLT Viewer](https://github.com/COVESA/dlt-viewer) 2.31.0, built from source, plus an **AI Agent Plugin**: a chat panel docked inside DLT Viewer, backed by a GitHub Copilot agent that can read and navigate the open log. Your filters (`.dlf`), projects (`.dlp`) and workflow are unchanged — upstream sources are not modified.

## Use

1. Run `Launch_DLT_Viewer_Agent.bat` (or drag `.dlt` / `.dlf` files onto it).
2. First time only: in the **Project** pane, open the **Plugins** tab, select **AI Agent Plugin**, then choose **Plugin > Plugin Show**. The panel docks on the left; drag it wherever you like.
3. Open a log, then ask in the panel, for example:
   - "Summarise the errors and warnings in what I'm looking at."
   - "Explain the selected message and what happened just before it."
   - "When did HPA start reporting faults? Show the first one."
4. Message references like **#1234** in answers are clickable and jump to the message. **Stop** cancels a reply; **New chat** starts over.

The agent starts with your first message and stops when DLT Viewer closes.

## What the agent can do

Read-only access to the open log through eight tools: file overview, selected message, single message, messages around an index, a page of rows, bounded search (text/regex, levels, app, context), statistics, and jump-to-message. It defaults to the **filtered view you see**. Shell, file editing, web and all other Copilot tools are disabled.

## Knowledge base

Put reference material in `agent\knowledge\`: app/context ID meanings, fault signatures, procedures. The agent sees a list of file titles and searches the files only when needed; answers cite `(knowledge: <file>)`. See [agent/knowledge/README.md](agent/knowledge/README.md). New files are picked up in a **New chat**.

**Datasheets and other folders:** list folders in `agent\knowledge_sources.txt` and run `Sync_Knowledge.bat`. PDFs are converted with PyMuPDF4LLM (about 1 s per page), Excel sheets become tables, and the results are mirrored into `agent\knowledge\sources\`. Re-running converts only new or changed files. Progress: `agent\logs\sync.log` when run in the background.

## Setup (one time)

Already done on this machine; repeat on a new one.

1. Admin PowerShell:
   ```powershell
   winget install --id Microsoft.VisualStudio.2022.BuildTools -e --override "--quiet --wait --norestart --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
   winget install --id Microsoft.PowerShell -e
   winget install --id GitHub.Copilot -e
   ```
2. Restart VS Code / terminals, run `copilot`, then `/login` once.
3. Build tools and Qt 6.8.3 (no admin), from this folder:
   ```powershell
   python -m venv .venv; .\.venv\Scripts\pip install aqtinstall cmake ninja
   .\.venv\Scripts\aqt install-qt windows desktop 6.8.3 win64_msvc2022_64 -m qtserialport -O "$env:USERPROFILE\Qt"
   git clone --depth 1 --branch 2.31.0 https://github.com/COVESA/dlt-viewer.git dlt-viewer
   python -m venv agent\.venv; .\agent\.venv\Scripts\pip install -r agent\requirements.txt
   ```
4. Run `build.bat`. Output: `build\bin\dlt-viewer.exe` and `build\bin\plugins\aiagentplugin.dll`.

## Notes

- Log content you ask about is sent to GitHub Copilot under your licence; follow company data-handling rules. Each question uses Copilot AI credits.
- Logs and Copilot session files stay local: `agent\logs\agent.log`, `agent\workdir\`.
- The plugin finds the agent at `..\..\agent` relative to `dlt-viewer.exe`; set `DLT_AGENT_DIR` to override.
- Search, statistics and payload text use DLT Viewer's verbose decoding. Messages decoded only by other plugins (e.g. non-verbose/FIBEX) show decoded text when read individually, but searches match the raw text.
- Silent command-line mode of `dlt-viewer.exe` (`-s`) hangs in this build; use `build\bin\dlt-commander.exe` for headless conversion.

## Layout

| Path | Purpose |
| --- | --- |
| `plugin\` | AI Agent Plugin (C++/Qt), injected into the upstream build via `inject.cmake` |
| `agent\dlt_agent.py` | Copilot SDK agent started by the plugin |
| `build.bat` | Configure + build + deploy Qt runtime |
| `dlt-viewer\` | Upstream source (git clone, not committed) |
| [FUNCTION_DEFINITIONS.md](FUNCTION_DEFINITIONS.md) | Component and function reference |
