"""User-configurable inputs for the Exovision DTC Analyser.

WORKFLOW:
  1. Run with DISCOVER_SCHEMA = True to print available columns and sample
     file paths, then exit.
  2. Update TIMESTAMP_COLUMN with the real column name from the discovery output.
  3. Update EXOVISION_ECU_ADDRESSES and/or EXOVISION_DTC_ID_PREFIXES to narrow
     results to Exovision-related DTCs.
  4. Set DISCOVER_SCHEMA = False and run the full analysis.
"""

# ── Date range ───────────────────────────────────────────────────────────────
# Format: "YYYY-MM-DD"
START_DATE = "2026-01-01"
END_DATE   = "2026-03-31"

# ── Exovision filter ─────────────────────────────────────────────────────────
# ECU addresses that belong to the Exovision (camera / vision) system.
# Values can be integers (0x12) or hex-strings ("0x12" / "12").
# Leave empty ([]) to include DTCs from ALL ECUs.
EXOVISION_ECU_ADDRESSES = [0x1D12, 0x1D01]   # e.g. [0x12, 0x34]

# DTC ID prefixes to include (matched as a starts-with on the string
# representation of dtc_id).  Leave empty ([]) to include all DTC IDs.
EXOVISION_DTC_ID_PREFIXES = []  # e.g. ["A1B2", "C3"]

# ── Column names ─────────────────────────────────────────────────────────────
# Column that contains the timestamp / datetime of each DTC event.
# Run with DISCOVER_SCHEMA = True first to find the correct name.
TIMESTAMP_COLUMN = "timestamp"

# ── Schema / path discovery ───────────────────────────────────────────────────
# Set True to print columns + a few sample file paths, then exit.
# Switch to False once TIMESTAMP_COLUMN and filters are confirmed.
DISCOVER_SCHEMA = True
