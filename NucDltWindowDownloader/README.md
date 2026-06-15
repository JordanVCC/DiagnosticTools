# NUC DLT Window Downloader

A tool to download diagnostic DLT (Diagnostic Log Trace) files from NUC (NUC Data Vault) within a precise date-time window.

## Quick Start

### Prerequisites
- Python 3.13+
- Windows or Linux
- Internet connection to NUC drive

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Tool

**Option 1: Launch via Batch File (Windows)**
```bash
Launch_NUC_DLT_Window_Downloader.bat
```

**Option 2: Launch via Python**
```bash
python nuc_dlt_window_downloader.py
```

## How to Use

1. **Enter VIN**: Type or select a VIN number from the searchable list
2. **Choose Variant**: Select HPA or HPB
3. **Set Time Window**: 
   - Start Date/Time: Beginning of log window
   - End Date/Time: End of log window
   - Use calendar popup or type dates as YYYY-MM-DD
4. **Choose Output Folder**: Where to save downloaded files
5. **Options**:
   - **Skip Existing Files**: Don't re-download files already present
   - **Combine DLT Files**: Merge all downloaded files into single file (enabled by default)
6. **Click "Download Logs"**: Start the download process
7. **Monitor Progress**: Watch the progress bar and status updates

## Features

- 📁 **Multi-format Support**: Automatically extracts ZIP, Zstandard (.zst), GZIP, BZIP2, XZ, and TAR formats
- ⚡ **Fast Downloads**: 4 concurrent downloads + 1MB chunk size for optimal speed
- 📊 **Live Progress**: Real-time download speed and ETA display
- ⏸️ **Resume Support**: Automatically resume interrupted downloads from where they stopped
- 🔁 **Robust Retry**: Automatic retry on network timeouts with adaptive backoff
- 📦 **Smart Combining**: Merge extracted DLT files into a single file
- 🔍 **VIN Search**: Auto-loaded VIN suggestions with prefix and contains filtering

## Output

Downloaded files appear in your chosen output folder:
- Individual extracted DLT files from each archive
- Combined DLT file (if combining is enabled)
- Temporary archives are automatically cleaned up

## Keyboard & Mouse Tips

- **Date field**: Click calendar icon or type `YYYY-MM-DD`
- **Time field**: Click dropdowns or type values directly (Hour: 0-23, Minute: 0-59, Second: 0-59)
- **VIN field**: Start typing to filter suggestions; use arrow keys to navigate
- **"Now" button**: Quickly set current date/time
- **"Refresh VINs"**: Reload VIN list from NUC (runs in background)

## Troubleshooting

**"Missing dependency" error?**
```bash
pip install -r requirements.txt
```

**Download stuck?**
- Click "Stop" to cancel
- Close and reopen the tool
- Partially downloaded files will be resumed next time

**No files found?**
- Verify VIN is correct and in the list
- Check date range matches available logs
- Ensure variant (HPA/HPB) is correct
- Try expanding date range to verify connectivity

**Files not combining?**
- Ensure "Combine all DLT files into one" checkbox is enabled
- Check that at least 2 DLT files were extracted
- Verify output folder has write permissions

## Support

For developers and technical details, see the `_support/` folder:
- `BUG_FIXES_SUMMARY.md` - Code quality and improvements
- `PARALLEL_OPTIMIZATION.md` - Performance optimization details
- Test files for verification and development

## Technical Details

- Built with Python 3.13+, tkinter GUI framework
- Connects to NUC drive at `https://drive.nuc.volvocars.net/data_nuc/`
- Supports 9 compression formats with magic byte detection
- Thread-safe parallel downloads with progress monitoring
- File matching based on timestamp extraction from filenames (yyyymmddThhmmss format)

- During downloads, status text shows real transferred bytes (not per-file step counting):
  - Current file bytes (`File: downloaded / file target` when known)
  - Total bytes transferred in this run (`Total: downloaded / target` when fully known)
- Byte counters update at least 5 times per second while data is flowing.
- Live transfer speed is shown in the status line (`Speed: .../s`).
- Speed status is refreshed at least 4 times per second during download phase, including between file transitions.
- Download timeouts are handled with retries and longer socket timeouts to improve stability on large transfers.
- Per-file resume is supported: if a partially downloaded file exists, the tool resumes from the existing byte offset.
- UI uses a VS Code-like dark theme for improved readability in low-light workflows.
- Whole-window vertical and horizontal scrollbars are available when the UI does not fit on screen.
- Supports multiple archive and compression formats:
  - **ZIP archives** (`.zip`)
  - **Zstandard** (`.zst`) - highly compressed format
  - **GZIP** (`.gz`, `.tar.gz`, `.tgz`)
  - **BZIP2** (`.bz2`, `.tar.bz2`, `.tbz2`)
  - **XZ/LZMA** (`.xz`, `.tar.xz`, `.txz`)
  - **TAR archives** (`.tar`)
  - Automatically detects format by magic bytes and extension
- Downloaded archives are automatically extracted and only `.dlt` files are kept in the selected output folder.
- Archive folder paths are flattened (only the `.dlt` file names are kept), and processed archive files are deleted.
- If enabled, all DLT files involved in that run are combined into one additional `.dlt` file in the output folder.
- Original individual DLT files are preserved.
- Network and directory access failures are shown with clear messages, and individual day-level scan errors are logged while the tool continues scanning remaining days.
- If no matching files are found in the selected window, the tool reports that cleanly.
- Existing files can be skipped with the `Skip existing files` option.

## Requirements

- Python 3.10+
- `tkcalendar` (for calendar dropdown date picker)
- `zstandard` (for `.zst` decompression support)
