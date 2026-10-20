# ReqLink Map

ReqLink Map extracts requirements from one or more PDFs and renders their relationships as an interactive graph. Click a node to inspect the complete extracted text. References in the text and graph use matching colors for `REQ-xxxx` IDs, exact requirement names, and direct URLs.

Use **Mark node** in the requirement detail panel to keep important nodes highlighted in amber. Marks are stored in the browser and restored when PDFs are mapped again or the page is reloaded. **Hide unmarked** fades everything except marked nodes and their directly connected requirements; use **Show all** to restore the complete map.

## Run

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app:app --host 127.0.0.1 --port 8765
```

Open <http://127.0.0.1:8765>. `Launch_ReqLink_Map.bat` performs the second command and opens the page.

PDFs stored directly beside `app.py` can be processed with **Map folder PDFs**. **Open PDFs** accepts one or more files from any location. When the same requirement appears in multiple PDFs, the highest numeric `v<number>` version is retained.

## Recognized format

A requirement starts on a line matching either of these forms:

```text
REQ-461325v2 CPDD - AD&ADAS configuration handling
REQ - 461325v2 CPDD - AD&ADAS configuration handling
```

References are resolved when requirement body text contains:

- An ID such as `REQ-445663` or `REQ - 445663`.
- The exact name of another requirement in the loaded PDFs.
- A URL containing a requirement ID.

Referenced IDs missing from the loaded PDFs remain visible as dashed external nodes. PDF text extraction uses PyMuPDF; image-only scans require OCR before analysis.

## Agent

Select **Req Link Mapper** from the VS Code agent picker to validate extraction, adjust parser coverage, and launch the application. Its workspace definition is `.github/agents/req-link-mapper.agent.md`.

## Validate

```powershell
python -m unittest discover -s tests -v
```