#!/usr/bin/env python3
"""Compare diagnostic DID software labels against cs-software DID ID mappings.

This script scans a diagnostics repository for DID entries that expose a software
label (sw_label), then checks whether each label exists in the cs-software
product GMRDB sync configuration files.

Output is a Markdown table so the result can be pasted directly into Jira,
Confluence, or pull requests.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tarfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from user_inputs import (
    CS_CONFIGURATION_PATH,
    CS_MANUAL_DOWNLOAD_DIR,
    CS_REPO_PATH,
    CS_TARGET_REF,
    DIAGNOSTICS_REPO_PATH,
    DIAGNOSTICS_TARGET_REF,
    INCLUDE_PATH_REGEX,
    OUTPUT_FILE,
    UPDATE_TO_LATEST,
)

# Mapping files requested by the user inside cs-software-product/configuration
CS_MAPPING_FILES = (
    "GMRDB_sync_config_hpagen3_ad.yaml",
    "GMRDB_sync_config_hpagen3_adas.yaml",
    "GMRDB_sync_config_hpagen4.yaml",
    "GMRDB_sync_config_hpb.yaml",
)

# Candidate file extensions to inspect in diagnostics repo manifests.
CANDIDATE_EXTENSIONS = {
    ".yaml",
    ".yml",
    ".json",
    ".xml",
    ".txt",
    ".cfg",
    ".ini",
    ".arxml",
    ".manifest",
}

SW_LABEL_KEYS = ("sw_label", "swlabel", "software_label", "softwarelabel")
DID_KEYS = ("did", "did_id", "didid", "identifier", "id")

SW_LABEL_RE = re.compile(
    r"(?i)\b(?:sw_label|swLabel|software_label|softwareLabel)\b\s*[:=]\s*[\"']?([A-Za-z0-9_./:-]+)[\"']?"
)
DID_KEY_VALUE_RE = re.compile(
    r"(?i)\b(?:did|did_id|didId|identifier)\b\s*[:=]\s*[\"']?(0x[0-9A-Fa-f]{2,8}|[0-9]{2,6})[\"']?"
)
DID_HEX_RE = re.compile(r"\b0x[0-9A-Fa-f]{2,8}\b")
YAML_MAPPING_RE = re.compile(r"^\s*([A-Za-z0-9_./:-]+)\s*:\s*(0x[0-9A-Fa-f]{2,8})\b")
MANUAL_ARCHIVE_RE = re.compile(r"^cs-software-product-refs_heads_master(?:\s*\((\d+)\))?\.tar\.gz$", re.IGNORECASE)


@dataclass(frozen=True)
class DidEntry:
    sw_label: str
    source_file: str
    source_line: int
    diagnostic_did: str | None = None


@dataclass(frozen=True)
class MappingEntry:
    sw_label: str
    mapped_did: str
    source_file: str
    source_line: int


def run_git_command(repo_path: Path, args: list[str]) -> str:
    command = ["git", "-C", str(repo_path)] + args
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        details = stderr or stdout or "Unknown git error"
        raise RuntimeError(f"Command failed: {' '.join(command)}\\n{details}")
    return result.stdout.strip()


def run_git_update(repo_path: Path, target_ref: str, update_to_latest: bool) -> None:
    if not (repo_path / ".git").exists():
        return

    commands = [["fetch", "--all", "--prune"]]

    if target_ref.strip():
        commands.append(["checkout", target_ref.strip()])
        if update_to_latest:
            # Pull only if we're on a local branch (not detached HEAD).
            head_name = run_git_command(repo_path, ["rev-parse", "--abbrev-ref", "HEAD"])
            if head_name != "HEAD":
                commands.append(["pull", "--ff-only"])
    elif update_to_latest:
        commands.append(["pull", "--ff-only"])

    for cmd in commands:
        run_git_command(repo_path, cmd)


def try_git_update(repo_path: Path, target_ref: str, update_to_latest: bool) -> None:
    try:
        run_git_update(repo_path, target_ref, update_to_latest)
    except Exception as exc:
        # Continue with local checkout when remote update is unavailable.
        print(f"WARNING: Git update skipped for {repo_path}: {exc}")


def looks_like_candidate_file(rel_path: str, include_path_re: re.Pattern[str], ext: str) -> bool:
    if ext and ext.lower() not in CANDIDATE_EXTENSIONS:
        return False
    return bool(include_path_re.search(rel_path))


def normalize_did(raw: str | None) -> str | None:
    if not raw:
        return None
    raw = raw.strip()
    if not raw:
        return None
    if raw.lower().startswith("0x"):
        return f"0x{raw[2:].upper()}"
    if raw.isdigit():
        return f"0x{int(raw):X}"
    return raw


def collect_did_entries_from_json_obj(obj: object, source_file: str) -> list[DidEntry]:
    entries: list[DidEntry] = []

    def walk(node: object) -> None:
        if isinstance(node, dict):
            lowered = {str(k).lower(): v for k, v in node.items()}
            label_val = None
            for key in SW_LABEL_KEYS:
                if key in lowered and isinstance(lowered[key], str):
                    label_val = lowered[key].strip()
                    break

            did_val: str | None = None
            for key in DID_KEYS:
                if key in lowered:
                    did_val = normalize_did(str(lowered[key]))
                    break

            if label_val:
                entries.append(
                    DidEntry(
                        sw_label=label_val,
                        source_file=source_file,
                        source_line=1,
                        diagnostic_did=did_val,
                    )
                )

            for child in node.values():
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)

    walk(obj)
    return entries


def collect_did_entries_from_text(content: str, source_file: str) -> list[DidEntry]:
    entries: list[DidEntry] = []
    lines = content.splitlines()

    for idx, line in enumerate(lines, start=1):
        label_match = SW_LABEL_RE.search(line)
        if not label_match:
            continue

        sw_label = label_match.group(1).strip()
        did_value = None

        # Look nearby for an explicit DID key/value first.
        window_start = max(0, idx - 6)
        window_end = min(len(lines), idx + 5)
        window = "\n".join(lines[window_start:window_end])

        did_key_match = DID_KEY_VALUE_RE.search(window)
        if did_key_match:
            did_value = normalize_did(did_key_match.group(1))
        else:
            # Fall back to first hex literal in the nearby context.
            hex_match = DID_HEX_RE.search(window)
            if hex_match:
                did_value = normalize_did(hex_match.group(0))

        entries.append(
            DidEntry(
                sw_label=sw_label,
                source_file=source_file,
                source_line=idx,
                diagnostic_did=did_value,
            )
        )

    return entries


def collect_diagnostics_dids(
    diagnostics_repo: Path,
    include_path_regex: str,
) -> list[DidEntry]:
    include_path_re = re.compile(include_path_regex)
    all_entries: list[DidEntry] = []

    for path in diagnostics_repo.rglob("*"):
        if not path.is_file():
            continue

        rel = path.relative_to(diagnostics_repo).as_posix()
        ext = path.suffix.lower()
        if not looks_like_candidate_file(rel, include_path_re, ext):
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        if ext == ".json":
            try:
                obj = json.loads(text)
                entries = collect_did_entries_from_json_obj(obj, rel)
                if entries:
                    all_entries.extend(entries)
                    continue
            except json.JSONDecodeError:
                pass

        entries = collect_did_entries_from_text(text, rel)
        all_entries.extend(entries)

    # De-duplicate by label while preserving first seen source reference.
    seen: set[str] = set()
    unique_entries: list[DidEntry] = []
    for entry in sorted(all_entries, key=lambda e: (e.sw_label.lower(), e.source_file, e.source_line)):
        key = entry.sw_label
        if key in seen:
            continue
        seen.add(key)
        unique_entries.append(entry)

    return unique_entries


def parse_cs_mappings(configuration_dir: Path) -> dict[str, MappingEntry]:
    mappings: dict[str, MappingEntry] = {}
    found_mapping_files = 0

    for file_name in CS_MAPPING_FILES:
        file_path = configuration_dir / file_name
        if not file_path.exists():
            continue
        found_mapping_files += 1

        try:
            lines = file_path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue

        for idx, line in enumerate(lines, start=1):
            match = YAML_MAPPING_RE.match(line)
            if not match:
                continue
            label = match.group(1).strip()
            did = normalize_did(match.group(2))
            if not did:
                continue
            # Keep first mapping if duplicates appear.
            mappings.setdefault(
                label,
                MappingEntry(sw_label=label, mapped_did=did, source_file=f"configuration/{file_name}", source_line=idx),
            )

    if found_mapping_files == 0:
        raise RuntimeError(
            f"No GMRDB_sync_config_*.yaml files were found in: {configuration_dir}"
        )

    return mappings


def manual_archive_rank(path: Path) -> tuple[int, str]:
    match = MANUAL_ARCHIVE_RE.match(path.name)
    if not match:
        return (-1, path.name.lower())
    suffix_number = int(match.group(1)) if match.group(1) else 0
    return (suffix_number, path.name.lower())


def resolve_manual_configuration_dir(manual_download_dir: Path, work_dir: Path) -> Path:
    if not manual_download_dir.exists():
        raise ValueError(f"Manual download directory not found: {manual_download_dir}")

    archives = [
        p
        for p in manual_download_dir.iterdir()
        if p.is_file() and MANUAL_ARCHIVE_RE.match(p.name)
    ]
    if not archives:
        raise ValueError(
            "No manual archives found. Expected files like "
            "cs-software-product-refs_heads_master (1).tar.gz"
        )

    latest_archive = max(archives, key=manual_archive_rank)
    print(f"Using manual archive: {latest_archive}")
    extract_base = work_dir / ".manual_cs_extract"
    extract_dir = extract_base / latest_archive.name.replace(".tar.gz", "")
    marker = extract_dir / ".source_archive"

    should_extract = True
    if marker.exists() and extract_dir.exists():
        try:
            marker_content = marker.read_text(encoding="utf-8", errors="replace").strip()
            should_extract = marker_content != str(latest_archive)
        except OSError:
            should_extract = True

    if should_extract:
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
        extract_dir.mkdir(parents=True, exist_ok=True)
        with tarfile.open(latest_archive, mode="r:gz") as tar:
            tar.extractall(path=extract_dir, filter="data")
        marker.write_text(str(latest_archive), encoding="utf-8")

    direct_configuration = extract_dir / "configuration"
    if direct_configuration.exists():
        return direct_configuration

    for candidate in extract_dir.rglob("configuration"):
        if candidate.is_dir():
            return candidate

    raise RuntimeError(
        f"Could not find 'configuration' folder after extracting: {latest_archive}"
    )


def to_markdown_table(entries: Iterable[DidEntry], mappings: dict[str, MappingEntry]) -> str:
    def _table_header() -> list[str]:
        return [
            "| SW Label | Diagnostic DID (if present) | Mapped DID ID | Status | Diagnostic Source | Mapping Source |",
            "|---|---|---|---|---|---|",
        ]

    def _table_row(entry: DidEntry, mapping: MappingEntry | None) -> str:
        mapped = mapping.mapped_did if mapping else ""
        status = "OK" if mapping else "MISSING"
        diag_did = entry.diagnostic_did or ""
        diag_src = f"`{entry.source_file}:{entry.source_line}`"
        map_src = f"`{mapping.source_file}:{mapping.source_line}`" if mapping else ""
        return (
            f"| `{entry.sw_label}` | `{diag_did}` | `{mapped}` | {status} | {diag_src} | {map_src} |"
        )

    def _diagnostics_group(entry: DidEntry) -> str:
        parts = entry.source_file.split("/", 1)
        return parts[0] if parts and parts[0] else "(root)"

    def _mapped_did_sort_key(entry: DidEntry) -> tuple[int, int, str]:
        mapping = mappings.get(entry.sw_label)
        if not mapping:
            return (1, 2**31 - 1, entry.sw_label.lower())
        mapped = mapping.mapped_did.strip()
        if mapped.lower().startswith("0x"):
            try:
                return (0, int(mapped[2:], 16), entry.sw_label.lower())
            except ValueError:
                return (1, 2**31 - 1, entry.sw_label.lower())
        return (1, 2**31 - 1, entry.sw_label.lower())

    sorted_entries = sorted(entries, key=lambda e: ( _diagnostics_group(e).lower(), e.sw_label.lower()))
    total = len(sorted_entries)
    missing_entries = [e for e in sorted_entries if e.sw_label not in mappings]
    missing_count = len(missing_entries)

    report_sections: list[str] = []

    header = [
        "# DID Mapping Verification Report",
        "",
        f"- Total DID software labels in diagnostics repo: **{total}**",
        f"- Missing mappings in cs-software product repo: **{missing_count}**",
        "",
    ]

    report_sections.extend(header)

    report_sections.append("## Grouped By Diagnostics Folder")
    report_sections.append("")

    grouped: dict[str, list[DidEntry]] = {}
    for entry in sorted_entries:
        grouped.setdefault(_diagnostics_group(entry), []).append(entry)

    for folder in sorted(grouped.keys(), key=str.lower):
        report_sections.append(f"### `{folder}`")
        report_sections.append("")
        report_sections.extend(_table_header())
        missing_in_group = sorted(
            [e for e in grouped[folder] if e.sw_label not in mappings],
            key=lambda e: e.sw_label.lower(),
        )
        mapped_in_group = sorted(
            [e for e in grouped[folder] if e.sw_label in mappings],
            key=_mapped_did_sort_key,
        )
        for entry in missing_in_group + mapped_in_group:
            report_sections.append(_table_row(entry, mappings.get(entry.sw_label)))
        report_sections.append("")

    return "\n".join(report_sections) + "\n"


def validate_inputs(
    diagnostics_repo: Path,
    cs_repo: Path,
    cs_configuration_path: Path | None,
    manual_download_dir: Path | None,
    script_dir: Path,
) -> Path:
    if not diagnostics_repo.exists() or not (diagnostics_repo / ".git").exists():
        raise ValueError(f"Diagnostics repo not found or not a git repo: {diagnostics_repo}")

    if cs_configuration_path is not None:
        if not cs_configuration_path.exists():
            raise ValueError(f"CS configuration path does not exist: {cs_configuration_path}")
        return cs_configuration_path

    if manual_download_dir is not None:
        return resolve_manual_configuration_dir(manual_download_dir, script_dir)

    if not cs_repo.exists():
        raise ValueError(f"CS repo path not found: {cs_repo}")
    return cs_repo / "configuration"


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    diagnostics_repo = Path(DIAGNOSTICS_REPO_PATH).resolve()
    cs_repo = Path(CS_REPO_PATH).resolve()
    cs_configuration_path = None
    if str(CS_CONFIGURATION_PATH).strip():
        cs_configuration_path = Path(CS_CONFIGURATION_PATH).resolve()
    manual_download_dir = None
    if str(CS_MANUAL_DOWNLOAD_DIR).strip():
        manual_download_dir = Path(CS_MANUAL_DOWNLOAD_DIR).resolve()
    configured_output = Path(OUTPUT_FILE)
    output_file = configured_output if configured_output.is_absolute() else (script_dir / configured_output)
    output_file = output_file.resolve()

    try:
        configuration_dir = validate_inputs(
            diagnostics_repo,
            cs_repo,
            cs_configuration_path,
            manual_download_dir,
            script_dir,
        )

        try_git_update(diagnostics_repo, DIAGNOSTICS_TARGET_REF, UPDATE_TO_LATEST)
        try_git_update(cs_repo, CS_TARGET_REF, UPDATE_TO_LATEST)

        did_entries = collect_diagnostics_dids(diagnostics_repo, INCLUDE_PATH_REGEX)
        if not did_entries:
            raise RuntimeError(
                "No DID entries with sw_label were found in diagnostics repo. "
                "Adjust INCLUDE_PATH_REGEX in user_inputs.py if manifests use a different path pattern."
            )

        mappings = parse_cs_mappings(configuration_dir)
        report = to_markdown_table(did_entries, mappings)

        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(report, encoding="utf-8")

        missing = sum(1 for e in did_entries if e.sw_label not in mappings)
        print(f"Report written: {output_file}")
        print(f"Diagnostics DID labels found: {len(did_entries)}")
        print(f"Missing mappings: {missing}")
        return 0

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
