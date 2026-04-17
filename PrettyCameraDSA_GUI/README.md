# DSA Log Filter

Filters camera DTC entries from a DSA diagnostic log file.

## How to use

Double-click **`DSA_Filter.html`** — opens instantly in your browser, nothing to install.

1. **Drag and drop** your `DsaLog.txt` onto the blue zone — or click **Browse…**
2. Filtered output appears immediately in the text area.
3. Click **Save filtered file** to download `<original_name>_filtered.txt`

## What the filter does

- Leaves all content untouched **except** "Read DTC Information" request blocks.
- Inside those blocks: keeps only exterior camera DTC entries.
- Camera prefixes: `D4D5` `D50A` `D50B` `D50C` `D509` `D4EE` `D4EF` `D606` `D607`

## Files

| File | Purpose |
|------|---------|
| `DSA_Filter.html` | The app — share this single file |
| `README.md` | This file |
