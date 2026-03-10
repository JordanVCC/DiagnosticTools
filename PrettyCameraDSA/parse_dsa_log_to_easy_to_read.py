#!/usr/bin/env python3
# Usage: see INSTRUCTIONS.md in this folder.
from pathlib import Path
import re

# ---------------------------------------------------------
# CONFIGURATION — set your input log file here
# ---------------------------------------------------------
INPUT_FILE = "DsaLog.txt"   # <— change if needed
# ---------------------------------------------------------

# Detect the start of a request block
REQUEST_START_RE = re.compile(r"^#\s*Sending Request:\s*Tester\s*->", re.IGNORECASE)

# Heuristic to detect "Read DTC Information" request blocks
# (Matches typical text found in your logs; extend if needed)
IS_READ_DTC_HINTS = (
    re.compile(r"\bRead\s+DTC\s+Information\b", re.IGNORECASE),
    re.compile(r"\bReport\s+DTC\b", re.IGNORECASE),
    re.compile(r"\b19\s+0[0-9A-Fa-f]\b"),  # UDS service 0x19 variants present in request line
)

# Exterior camera DTC prefixes (first 2 bytes / first 4 hex chars)
CAMERA_PREFIX_SET = {
    "D4D5",  # FLCW
    "D50A",  # SRCF
    "D50B",  # SRCL
    "D50C",  # SRCR
    "D509",  # SRCB
    "D4EE",  # LRBL
    "D4EF",  # LRBR
    "D606",  # LRIL
    "D607",  # LRIR
}

# DTC header lines look like:
#   D50A55        Short Range Camera Front (SRCF)- ...
DTC_HEAD_RE = re.compile(r"^\s*([A-F0-9]{4,8})\s+\t?\t?.*")
# Status detail lines look like:
#   " 01          Test failed", " 02", " 04", " 08", " 20", " 80"
DTC_STATUS_RE = re.compile(r"^\s{1,}(0[1-9]|20|80)\s+.*")


def _is_dtc_header(line: str):
    m = DTC_HEAD_RE.match(line)
    if not m:
        return False, None
    code = m.group(1).strip()
    return True, code


def _is_camera_dtc_code(code: str) -> bool:
    return bool(code and len(code) >= 4 and code[:4] in CAMERA_PREFIX_SET)


def _block_is_read_dtc(block_lines: list[str]) -> bool:
    """Return True if a request block represents a 'Read DTC Information' request."""
    # The "Tester -> ..." lines typically carry the operation description.
    # Scan the first few lines for the hints.
    scan_span = block_lines[:10] if len(block_lines) > 10 else block_lines
    chunk = "\n".join(scan_span)
    return any(p.search(chunk) for p in IS_READ_DTC_HINTS)


def _append_blank_line_once(dst: list[str]):
    """Append exactly one blank line unless the last line is already blank or list is empty."""
    if not dst:
        return
    if dst[-1].strip() != "":
        dst.append("")


def filter_log_file(input_path: Path):
    text = input_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    out_lines: list[str] = []
    i, n = 0, len(lines)

    while i < n:
        line = lines[i]

        # ---------------------------------------------------------
        # REQUEST BLOCK
        # ---------------------------------------------------------
        if REQUEST_START_RE.match(line):
            # Capture the entire block [start .. before next start]
            block_start_idx = i
            block = [line]
            i += 1
            while i < n and not REQUEST_START_RE.match(lines[i]):
                block.append(lines[i])
                i += 1

            # Decide if this is a Read-DTC block
            if _block_is_read_dtc(block):
                # Filter DTC entries inside the block:
                # - keep camera DTC header + status
                # - drop non-camera DTC header + status
                # - keep all other non-DTC lines as-is
                j = 0
                filtered_block: list[str] = []
                while j < len(block):
                    L = block[j]

                    is_hdr, code = _is_dtc_header(L)
                    if is_hdr:
                        if _is_camera_dtc_code(code):
                            # Keep header
                            filtered_block.append(L)
                            # Keep subsequent status lines
                            k = j + 1
                            while k < len(block) and DTC_STATUS_RE.match(block[k]):
                                filtered_block.append(block[k])
                                k += 1
                            # Insert single blank line after the DTC block (for readability)
                            _append_blank_line_once(filtered_block)
                            j = k
                            continue
                        else:
                            # Skip non-camera DTC header and its status lines
                            k = j + 1
                            while k < len(block) and DTC_STATUS_RE.match(block[k]):
                                k += 1
                            j = k
                            continue
                    else:
                        # Not a DTC header; copy as-is
                        filtered_block.append(L)
                        j += 1

                out_lines.extend(filtered_block)
            else:
                # Not a Read-DTC request; DO NOT TOUCH IT — copy entire block verbatim
                out_lines.extend(block)

            # Continue main loop (i already points to next line after the block)
            continue

        # ---------------------------------------------------------
        # OUTSIDE REQUEST BLOCKS — DO NOT TOUCH ANYTHING
        # ---------------------------------------------------------
        out_lines.append(line)
        i += 1

    # Write filtered output (ensure single trailing newline)
    out_path = input_path.with_name(input_path.stem + "_filtered.txt")
    out_path.write_text("\n".join(out_lines).rstrip() + "\n", encoding="utf-8")
    print(f"Filtered file created: {out_path}")


if __name__ == "__main__":
    input_path = Path(INPUT_FILE)
    if not input_path.is_absolute():
        script_dir = Path(__file__).resolve().parent
        script_relative_path = script_dir / input_path
        if script_relative_path.exists():
            input_path = script_relative_path
    filter_log_file(input_path)
