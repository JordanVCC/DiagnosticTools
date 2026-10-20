from pathlib import Path
import re
import importlib.util

root = Path('c:/Users/JHARVEY/Documents/DiagnosticTools/NucDtcDltFaultCorrelator')
parser_path = root.parent / 'DLTSearcher' / 'dlt_searcher_gui.py'
spec = importlib.util.spec_from_file_location('dlt_searcher_gui', parser_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

pat = re.compile(r'SPA[0-9A-Za-z./-]*_INT[0-9A-Za-z._-]*', re.IGNORECASE)
files = sorted((root / 'runs').glob('**/extracted/**/*.dlt'), key=lambda p: p.stat().st_mtime, reverse=True)
files = files[:250]

hits = []
for fp in files:
    try:
        msgs, _ = mod.parse_dlt_file(str(fp))
    except Exception:
        continue
    tokens = set()
    for m in msgs:
        line = str(m[7])
        for t in pat.findall(line):
            tokens.add(t.upper())
    if tokens:
        hits.append((fp, sorted(tokens)))

print(f'SCANNED_FILES={len(files)}')
print(f'FILES_WITH_BASELINE={len(hits)}')
if not hits:
    print('NO_BASELINES_FOUND_IN_SCANNED_FILES')
else:
    for fp, toks in hits:
        rel = fp.relative_to(root)
        print(f'{rel} :: {", ".join(toks)}')
