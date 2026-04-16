# DSA Log Filter — GUI App

A lightweight desktop window that filters camera DTC entries from a DSA diagnostic log file.

## Running the app

Double-click **`DSA_Filter.exe`** — no installation required, nothing else needed.

---

## How to use

1. **Drag and drop** your `DsaLog.txt` file onto the blue drop zone in the window.  
   — or — click **Browse…** to pick the file manually.
2. The filtered output appears instantly in the text area below.
3. Click **Save filtered file** to write `<original_name>_filtered.txt` next to the source file.

---

## What the filter does

- Leaves all content untouched **except** "Read DTC Information" request blocks.
- Inside those blocks: keeps only exterior camera DTC entries and removes everything else.
- Camera prefixes recognised: `D4D5` `D50A` `D50B` `D50C` `D509` `D4EE` `D4EF` `D606` `D607`

---

## Files

| File | Purpose |
|------|---------|
| `DSA_Filter.exe` | Standalone application — share this file |
| `dsa_filter_app.pyw` | Source script (for rebuilding) |
| `README.md` | This file |
