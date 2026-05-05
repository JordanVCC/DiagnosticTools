# Hostlog Decoder Tool

This folder now includes a lightweight GUI so you can decode hostlogs to HDF5 without typing commands.

## Easiest Use (No Typing)

1. Double-click `Launch_Hostlog_Decoder_GUI.bat`
2. In the GUI, verify or browse paths
3. Click `Decode to HDF5`

The GUI preloads defaults from `Paths` and can auto-fill:
- latest TDF folder from `hostlog-client/hostlog/tdf`
- output folder as `<log-folder>/decoded_hdf5`

## Files

- `hostlog_decoder_gui.py`: desktop GUI
- `Launch_Hostlog_Decoder_GUI.bat`: one-click launcher
- `decode_hostlog_to_hdf5.py`: CLI decoder backend
- `Paths`: default path values for `hostlog-client` and one example log file

## Requirements

- Windows
- Python 3.9+
- `hostlog-client` installed and accessible via the path in `Paths`
- A valid TDF folder (typically under `hostlog-client/hostlog/tdf/...`)

## Optional CLI Usage

If needed, you can still use the CLI version:

```powershell
python .\decode_hostlog_to_hdf5.py
```

Dry run:

```powershell
python .\decode_hostlog_to_hdf5.py --dry-run
```

