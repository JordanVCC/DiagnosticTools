"""Build dtc_lookup.csv from spa2_vision_diagnostics repo YAML files.

Phase 1: Parse *-configuration.yaml for  name → DTC hex code
Phase 2: Parse *-information.yaml / *-manifest.yaml for  name → human description
Phase 3: Join and write dtc_lookup.csv

Run this script whenever the diagnostics repo is updated to regenerate the lookup.
"""
from __future__ import annotations
import re
import pathlib
import csv
import sys

REPO = pathlib.Path(r"C:\Users\JHARVEY\OneDrive - Volvo Cars\Documents\06_Repos\spa2_vision_diagnostics")
OUT  = pathlib.Path(r"C:\Users\JHARVEY\Documents\DiagnosticTools\NucDataAnalyser\dtc_lookup.csv")

# ── Regex helpers ─────────────────────────────────────────────────────────────
_NAME_RE  = re.compile(r"^\s*-?\s*name:\s*(.+)")
_DTC_RE   = re.compile(r"\s*DTC:\s*['\"]?0x([0-9A-Fa-f]+)['\"]?")
# Matches: do_not_edit: 'first line' or brief: 'text'
_BRIEF_RE = re.compile(r"(?:do_not_edit|brief):\s*['\"]?(.+?)(?:['\"]?\s*$)", re.IGNORECASE)


def platform_from_path(p: pathlib.Path) -> str:
    for part in p.parts:
        if part.upper() in ("HPA", "HPB"):
            return part.upper()
    return "?"


# ── Phase 1: event name → hex code (configuration files) ─────────────────────
name_to_hex: dict[str, str] = {}      # event_name → 6-char hex
name_to_platform: dict[str, str] = {}

for f in sorted(REPO.rglob("*.yaml")):
    if "configuration" not in f.name.lower():
        continue
    platform = platform_from_path(f)
    current = None
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        m = _NAME_RE.match(line)
        if m:
            current = m.group(1).strip()
            continue
        m = _DTC_RE.match(line)
        if m and current:
            raw = m.group(1).upper()
            hex6 = (raw.lstrip("0") or "0").zfill(6)
            if current not in name_to_hex:          # first file wins
                name_to_hex[current] = hex6
                name_to_platform[current] = platform
            current = None

print(f"Phase 1: {len(name_to_hex)} name→hex mappings")

# ── Phase 2: event name → human description (information / manifest files) ────
name_to_desc: dict[str, str] = {}

for f in sorted(REPO.rglob("*.yaml")):
    if not any(kw in f.name.lower() for kw in ("information", "manifest")):
        continue
    current = None
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        m = _NAME_RE.match(line)
        if m:
            candidate = m.group(1).strip()
            current = candidate if candidate in name_to_hex else None
            continue
        if current and current not in name_to_desc:
            m = _BRIEF_RE.search(line)
            if m:
                desc = m.group(1).strip().strip("'\"").split("\n")[0].strip()
                if desc and desc.lower() not in ("[alternative comment]", ""):
                    name_to_desc[current] = desc

print(f"Phase 2: {len(name_to_desc)} name→description mappings")


def make_label(name: str, desc: str) -> str:
    if desc:
        return desc
    # Humanise the AUTOSAR event name when no description found
    suffix = name.rsplit("_", 1)[0] if "_" in name else name
    suffix = re.sub(r"^(?:HPA|HPB|HP)_", "", suffix, flags=re.IGNORECASE)
    return re.sub(r"([a-z])([A-Z])", r"\1 \2", suffix)


# ── Phase 3: join and write CSV ───────────────────────────────────────────────
records: list[dict] = []
for name, hex6 in sorted(name_to_hex.items(), key=lambda x: x[1]):
    desc  = name_to_desc.get(name, "")
    plat  = name_to_platform.get(name, "?")
    label = make_label(name, desc)
    records.append({"dtc_id": hex6, "description": label,
                    "autosar_name": name, "platform": plat})

with open(OUT, "w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=["dtc_id", "description", "autosar_name", "platform"])
    writer.writeheader()
    writer.writerows(records)

print(f"\nWritten {len(records)} entries → {OUT}")
print("\nSample (with descriptions):")
for r in [x for x in records if x["description"]][:8]:
    print(f"  {r['dtc_id']}  [{r['platform']}]  {r['description'][:72]}")

# ── Coverage check vs observed production DTCs ────────────────────────────────
print("\n--- Coverage vs top-22 production DTCs ---")
lookup_map = {r["dtc_id"]: r["description"] for r in records}
observed = ["D4AB87","C03713","99E700","D50268","D33B93","985C96","D4EF96",
            "D50168","D4EE96","D44F68","516E02","F00047","C03700","0D678C",
            "2D778C","F04B86","C0E38C","D4EE54","D4D596","D4EF54","F00096","0F4851"]
found = sum(1 for d in observed if d in lookup_map)
print(f"Covered: {found}/{len(observed)}")
for d in observed:
    hit = lookup_map.get(d)
    print(f"  {d}: {(hit[:68] if hit else 'NOT IN THIS REPO')}")
