# DSA Log Filter Tool – Quick Instructions

## What this tool does
`parse_dsa_log_to_easy_to_read.py` reads a DSA log file and creates a filtered copy.

It keeps all content unchanged **except** inside "Read DTC Information" request blocks, where it:
- keeps only exterior camera DTC entries,
- removes non-camera DTC entries,
- preserves non-DTC lines in those blocks.

Output is written to:
- `DsaLog_filtered.txt`

## How to use
1. Put your source log file in this folder.
2. Open `parse_dsa_log_to_easy_to_read.py` and set `INPUT_FILE` if needed (default is `DsaLog.txt`).
3. Run:

```bash
python parse_dsa_log_to_easy_to_read.py
```
or click the run button in vscode

4. Check the generated `*_filtered.txt` file.

## Notes
- Original file is not modified.
- File is read as UTF-8 with replacement for invalid characters.
- Camera DTC filtering is based on configured camera DTC prefixes in the script.