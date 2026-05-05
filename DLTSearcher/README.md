# DLT Log Searcher

A lightweight GUI tool that recursively finds all `.dlt` files in a given folder and provides text search across all of them.

## Usage

```bash
python dlt_searcher_gui.py
```

## Features

- Browse or paste a folder path, then click **Load** to recursively find and parse all `.dlt` files
- Progress bar and live counter showing files loaded and messages parsed
- Search across all loaded messages (case-insensitive by default)
- Regex and case-sensitive search options
- Results table showing file path, timestamp, App ID, Context ID, and full message
- Right-click to copy a row, message, or all results (also Ctrl+C)

## Requirements

- Python 3.10+ (no external dependencies, uses tkinter)
