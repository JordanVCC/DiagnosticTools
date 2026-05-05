#!/usr/bin/env python3
"""Decode Hostlog binary files to HDF5 using hostlog-client.

Defaults are read from the local "Paths" file if present.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional


def parse_paths_file(paths_file: Path) -> Dict[str, str]:
    """Parse simple key-value lines from the Paths file."""
    out: Dict[str, str] = {}
    if not paths_file.exists():
        return out

    for raw in paths_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip().strip('"').strip("'")

        if "hostlog location" in key:
            out["hostlog_dir"] = value
        elif "log file location" in key:
            out["log_file"] = value

    return out


def find_latest_tdf_dir(hostlog_dir: Path) -> Optional[Path]:
    """Find the newest tdf folder under hostlog/tdf."""
    tdf_root = hostlog_dir / "hostlog" / "tdf"
    if not tdf_root.exists() or not tdf_root.is_dir():
        return None

    candidates = [p for p in tdf_root.iterdir() if p.is_dir()]
    if not candidates:
        return None

    # Prefer folders matching tdf-* naming, then newest by mtime.
    preferred = [p for p in candidates if re.match(r"^tdf[-_]", p.name, re.IGNORECASE)]
    pool = preferred if preferred else candidates
    return max(pool, key=lambda p: p.stat().st_mtime)


def build_command(
    hostlog_bat: Path,
    binary_file: Path,
    output_dir: Path,
    definitions: Path,
    decode_enum_as_int: bool,
    enable_named_datasets: bool,
) -> str:
    appconfig = (
        f"output.files.hdf5_decode_enum_as_int={str(decode_enum_as_int)}"
        f",output.files.enable_hdf5_named_datasets={str(enable_named_datasets)}"
    )

    # Build command string with properly quoted paths to handle spaces
    cmd = (
        f'"{hostlog_bat}" offline binary-playback '
        f'--binary-files "{binary_file}" '
        f'--output "{output_dir}" '
        f'--definitions "{definitions}" '
        f'--to-hdf5 '
        f'--appconfig "{appconfig}"'
    )
    return cmd


def parse_args(defaults: Dict[str, str], script_dir: Path) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Decode a hostlog binary file to HDF5 using hostlog-client."
    )

    parser.add_argument(
        "--paths-file",
        type=Path,
        default=script_dir / "Paths",
        help="Path to Paths file (default: HostlogDecoder/Paths).",
    )
    parser.add_argument(
        "--hostlog-dir",
        type=Path,
        default=Path(defaults["hostlog_dir"]) if defaults.get("hostlog_dir") else None,
        help="Path to hostlog-client directory.",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=Path(defaults["log_file"]) if defaults.get("log_file") else None,
        help="Path to .bin hostlog file to decode.",
    )
    parser.add_argument(
        "--definitions",
        type=Path,
        default=None,
        help="Path to TDF definitions folder or file. If omitted, newest hostlog/tdf folder is used.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output folder for decoded HDF5 (default: <bin_parent>/decoded_hdf5).",
    )
    parser.add_argument(
        "--decode-enum-as-int",
        action="store_true",
        help="Decode enums as integer values (default: False).",
    )
    parser.add_argument(
        "--disable-named-datasets",
        action="store_true",
        help="Disable human-readable HDF5 dataset names.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print resolved command without executing.",
    )

    return parser.parse_args()


def main() -> int:
    script_dir = Path(__file__).resolve().parent

    initial_defaults = parse_paths_file(script_dir / "Paths")
    args = parse_args(initial_defaults, script_dir)

    # Re-parse if user passed a custom Paths file.
    defaults = parse_paths_file(args.paths_file)
    hostlog_dir = args.hostlog_dir or (Path(defaults["hostlog_dir"]) if defaults.get("hostlog_dir") else None)
    log_file = args.log_file or (Path(defaults["log_file"]) if defaults.get("log_file") else None)

    if hostlog_dir is None:
        print("Error: hostlog directory not provided and not found in Paths.", file=sys.stderr)
        return 2
    if log_file is None:
        print("Error: log file not provided and not found in Paths.", file=sys.stderr)
        return 2

    hostlog_dir = hostlog_dir.expanduser().resolve()
    log_file = log_file.expanduser().resolve()

    hostlog_bat = hostlog_dir / "hostlog.bat"
    if not hostlog_bat.exists():
        print(f"Error: hostlog.bat not found at {hostlog_bat}", file=sys.stderr)
        return 2
    if not log_file.exists():
        print(f"Error: log file not found at {log_file}", file=sys.stderr)
        return 2

    definitions = args.definitions
    if definitions is None:
        definitions = find_latest_tdf_dir(hostlog_dir)
        if definitions is None:
            print(
                "Error: no TDF definitions found automatically. Use --definitions.",
                file=sys.stderr,
            )
            return 2
    definitions = definitions.expanduser().resolve()
    if not definitions.exists():
        print(f"Error: definitions path not found at {definitions}", file=sys.stderr)
        return 2

    output_dir = (args.output or (log_file.parent / "decoded_hdf5")).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = build_command(
        hostlog_bat=hostlog_bat,
        binary_file=log_file,
        output_dir=output_dir,
        definitions=definitions,
        decode_enum_as_int=args.decode_enum_as_int,
        enable_named_datasets=not args.disable_named_datasets,
    )

    print("Resolved settings:")
    print(f"  hostlog_dir : {hostlog_dir}")
    print(f"  log_file    : {log_file}")
    print(f"  definitions : {definitions}")
    print(f"  output_dir  : {output_dir}")
    print("\nCommand:")
    print(cmd)

    if args.dry_run:
        print("\nDry run complete. No decoding executed.")
        return 0

    try:
        completed = subprocess.run(cmd, cwd=hostlog_dir, shell=True, check=False)
    except Exception as exc:
        print(f"Error while starting decoder: {exc}", file=sys.stderr)
        return 1

    # Check if HDF5 output file was created (hostlog-client returns exit code 1 for warnings)
    hdf5_file = output_dir / "logs" / (log_file.stem + ".hdf5")
    if hdf5_file.exists():
        print("\nDecoding complete.")
        print(f"HDF5 output: {hdf5_file}")
        print(f"Output folder: {output_dir}")
        return 0
    
    if completed.returncode != 0:
        print(f"Decoder failed with exit code {completed.returncode}", file=sys.stderr)
        return completed.returncode

    print("\nDecoding complete.")
    print(f"Check output in: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
