# Exovision DTC Analyser

Plots the number of Exovision-related DTC detections per day over a user-defined
time window, pulling data from Azure ADLS.

---

## Running the tool

**Double-click `run.bat`** — that's it.

| Situation | What happens |
|---|---|
| First launch | A setup window appears and installs the required Python packages automatically |
| Subsequent launches | The GUI opens immediately with your last-used settings |

> **One-time requirement:** Azure CLI must be installed and you must run `az login` in a terminal once before using the tool. Download from [aka.ms/installazurecliwindows](https://aka.ms/installazurecliwindows).

---

## GUI walkthrough

### Settings tab

| Field | Description |
|---|---|
| **Start / End date** | Analysis window in `YYYY-MM-DD` format |
| **ECU addresses** | Comma-separated hex addresses for Exovision ECUs, e.g. `0x1D12, 0x1D01`. Leave blank to include all ECUs |
| **DTC ID prefixes** | Comma-separated DTC code prefixes to filter on. Leave blank for all |
| **Timestamp column name** | Name of the datetime column in the parquet data |
| **Discover schema only** | When checked, prints column names and sample rows instead of plotting — use this on first run to find the correct timestamp column name |

All settings are saved automatically to `settings.json` whenever you click **Run Analysis** or **Save Settings**, and are restored next time the app opens.

### Results tab

- **Log** — live output from the analysis (file counts, applied filters, per-day table)
- **Chart** — interactive bar chart embedded in the window; also saved as `exovision_dtc_graph.png`

---

## First-run workflow

1. Launch `run.bat`
2. Leave **Discover schema only** checked and click **Run Analysis**
3. Read the column list in the Log — find the timestamp column name
4. Go back to Settings, update **Timestamp column name** and set the correct **ECU addresses**
5. Uncheck **Discover schema only**, set your date range, click **Run Analysis**
