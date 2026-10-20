# NUC DTC to DLT Fault Correlator

This tool correlates DTC occurrences from ADLS data with NUC DLT logs, searches for the DTC report line, and maps nearby camera-service fault reasons.

## What It Does

1. Reads DTC occurrence records from ADLS parquet (`data_uds_dtcs_v2`) for a selected time range.
2. Filters by selected DTC list.
3. Downloads relevant NUC DLT files for each occurrence window (`+/- N` minutes).
4. Parses DLT messages and finds likely DTC report lines.
5. Searches around each DTC line for configured fault reason tokens.
6. Writes a grouped HTML report and a JSON sidecar with referenced DLT files.
7. Supports storage cleanup actions:
- Cleanup all downloaded files (keeps report artifacts)
- Keep only DLT files referenced by report
8. Provides an `Open Report` button in the GUI to launch the latest generated report.

## Time Window Options

- `24h`
- `7d`
- `30d`
- `90d`
- `Manual` start/end datetime (UTC)

## Requirements

- Python 3.10+
- Azure CLI installed and logged in (`az login`)
- Python packages in `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

## Output

Each run creates a timestamped run folder inside the configured output directory:

- `dtc_dlt_fault_report.html`
- `report_references.json`
- `raw/` downloaded payloads
- `extracted/` extracted `.dlt` files

## Fault Reason Catalog

Update `fault_reasons.txt` to add/remove tokens without changing code.
