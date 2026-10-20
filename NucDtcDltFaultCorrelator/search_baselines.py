import sys
import os
import re
from pathlib import Path
import importlib.util
import glob

# Load dlt_searcher_gui
dlt_searcher_path = Path("../DLTSearcher/dlt_searcher_gui.py").resolve()
spec = importlib.util.spec_from_file_location("dlt_searcher", dlt_searcher_path)
dlt_searcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dlt_searcher)

pattern = re.compile(r'SPA[0-9A-Za-z./-]*_INT[0-9A-Za-z._-]*', re.IGNORECASE)

# Find files matching runs/**/extracted/**/*.dlt
all_files = [Path(p) for p in glob.glob("runs/**/extracted/**/*.dlt", recursive=True)]

# Sort by newest mtime descending
all_files_sorted = sorted(all_files, key=lambda p: p.stat().st_mtime, reverse=True)

# Up to first 250 files
scanned_files = all_files_sorted[:250]

num_scanned = len(scanned_files)
matches_by_file = {}

for idx, fpath in enumerate(scanned_files, 1):
    try:
        messages, _ = dlt_searcher.parse_dlt_file(str(fpath))
    except Exception as e:
        continue
    
    unique_tokens = set()
    for msg in messages:
        text = msg[7]
        found = pattern.findall(text)
        if found:
            for token in found:
                unique_tokens.add(token)
                
    if unique_tokens:
        matches_by_file[fpath] = sorted(list(unique_tokens))

print(f"Number of files scanned: {num_scanned}")
print(f"Number of files with matches: {len(matches_by_file)}")

if not matches_by_file:
    print("NO_BASELINES_FOUND_IN_SCANNED_FILES")
else:
    for fpath, tokens in matches_by_file.items():
        rel_path_str = fpath.as_posix()
        print(f"{rel_path_str}: {', '.join(tokens)}")
