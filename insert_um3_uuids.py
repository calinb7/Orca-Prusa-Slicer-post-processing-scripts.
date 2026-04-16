#!/usr/bin/env python3
"""
insert_um3_uuids.py
Usage: insert_um3_uuids.py input.gcode [output.gcode]
If output.gcode omitted, input.gcode is replaced.
Creates input.gcode.bak and a hidden log file .insert_um3_uuids.log next to the input file.

Behavior:
- Removes the very first line.
- Finds filament UUIDs in the gcode (up to two).
- Inserts ;EXTRUDER_TRAIN.0.MATERIAL.GUID:<uuid> into the header if found.
- Inserts ;EXTRUDER_TRAIN.1.MATERIAL.GUID:<uuid> into the header only if the header already contains any EXTRUDER_TRAIN.1.* line.
- Silent stdout/stderr; writes a hidden log file for debugging.
"""

# With help from Duck.ai

import re
import sys
import shutil
from pathlib import Path
from datetime import datetime

def log(path, msg):
    try:
        with path.open("a", encoding="utf-8") as f:
            f.write(f"{datetime.utcnow().isoformat()}Z {msg}\n")
    except Exception:
        pass  # never raise from logger

if len(sys.argv) < 2:
    sys.exit(2)

input_path = Path(sys.argv[1])
if not input_path.exists():
    sys.exit(1)

output_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else input_path

log_path = input_path.with_name(".insert_um3_uuids.log")

# Backup original input file
bak_path = input_path.with_suffix(input_path.suffix + ".bak")
try:
    shutil.copy2(input_path, bak_path)
    log(log_path, f"Backup created: {bak_path}")
except Exception as e:
    log(log_path, f"Backup failed: {e}")

try:
    text = input_path.read_text(encoding="utf-8", errors="ignore")
except Exception as e:
    log(log_path, f"Read failed: {e}")
    sys.exit(1)

# Remove the very first line
if "\n" in text:
    first_line = text.split("\n", 1)[0]
    text = text.split("\n", 1)[1]
    log(log_path, "Removed first line of file.")
    first_line = text.split("\n", 1)[0]
    text = text.split("\n", 1)[1]
    log(log_path, "Removed second line of file.")
else:
    text = ""
    log(log_path, "File had no newline; result empty after removing first line.")

# Patterns to find UUIDs in filament section
uuid_patterns = [
    re.compile(r";\s*EXTRUDER_TRAIN\.(\d+)\.MATERIAL\.GUID\s*[:=]\s*([0-9a-fA-F\-]{36})"),
    re.compile(r";\s*FILAMENT_UUID\s*:\s*(?:([0-9])\s*[:=]\s*)?([0-9a-fA-F\-]{36})"),
]

found = {}
# Prefer explicit EXTRUDER_TRAIN.* entries
for m in uuid_patterns[0].finditer(text):
    idx = int(m.group(1))
    if idx in (0, 1) and idx not in found:
        found[idx] = m.group(2)
if found:
    log(log_path, f"Found explicit EXTRUDER_TRAIN GUIDs: {found}")

# If less than two, find generic FILAMENT_UUID entries
if len(found) < 2:
    for m in uuid_patterns[1].finditer(text):
        idx = 0 if 0 not in found else 1
        if idx not in found:
            found[idx] = m.group(2)
        if len(found) >= 2:
            break
if found:
    log(log_path, f"Found filament GUIDs after generic search: {found}")
else:
    log(log_path, "No filament GUIDs found.")

# Locate header block
start_hdr = re.search(r"^;START_OF_HEADER\s*$", text, flags=re.MULTILINE)
end_hdr = re.search(r"^;END_OF_HEADER\s*$", text, flags=re.MULTILINE)

inserted = {}
if start_hdr and end_hdr and end_hdr.start() > start_hdr.start():
    hdr_start_idx = start_hdr.end()
    hdr_end_idx = end_hdr.start()
    header_block = text[hdr_start_idx:hdr_end_idx]

    # Detect whether header indicates extruder 1 exists
    has_extruder1 = bool(re.search(r"^\s*;\s*EXTRUDER_TRAIN\.1\.", header_block, flags=re.MULTILINE))
    log(log_path, f"Header indicates extruder1 present: {has_extruder1}")

    # Remove existing GUID lines for extruders 0/1
    header_block = re.sub(r";\s*EXTRUDER_TRAIN\.[01]\.MATERIAL\.GUID\s*[:=].*\n?", "", header_block)

    # Prepare insertion lines
    insert_lines = []
    if 0 in found:
        insert_lines.append(f";EXTRUDER_TRAIN.0.MATERIAL.GUID:{found[0]}\n")
        inserted[0] = found[0]
    if 1 in found and has_extruder1:
        insert_lines.append(f";EXTRUDER_TRAIN.1.MATERIAL.GUID:{found[1]}\n")
        inserted[1] = found[1]

    if insert_lines:
        new_header_block = header_block + "".join(insert_lines)
        text = text[:hdr_start_idx] + new_header_block + text[hdr_end_idx:]
        log(log_path, f"Inserted GUIDs into header: {inserted}")
    else:
        log(log_path, "No GUIDs inserted into header (none found or extruder1 not present).")
else:
    log(log_path, "Header block not found or malformed; no insertion attempted.")

# Write output
try:
    output_path.write_text(text, encoding="utf-8")
    log(log_path, f"Wrote output file: {output_path}")
except Exception as e:
    log(log_path, f"Write failed: {e}")
    sys.exit(1)
