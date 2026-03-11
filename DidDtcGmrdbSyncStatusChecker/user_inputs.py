"""User-editable configuration for DID mapping checker.

Update these values once, then run compare_did_mappings.py without CLI args.
"""

from pathlib import Path

# Local repository locations.
DIAGNOSTICS_REPO_PATH = Path(r"C:\Users\JHARVEY\OneDrive - Volvo Cars\Documents\06_Repos\spa2_vision_diagnostics")
CS_REPO_PATH = Path(r"C:\Users\JHARVEY\OneDrive - Volvo Cars\Documents\06_Repos\cs-software-product")

# Optional fallback: set this to a local folder containing the four
# GMRDB_sync_config_*.yaml files when cs repo cloning is unavailable.
# Example: Path(r"C:\Users\JHARVEY\Downloads\cs_configuration")
CS_CONFIGURATION_PATH = ""

# Optional manual-download folder containing files like:
# cs-software-product-refs_heads_master.tar.gz
# cs-software-product-refs_heads_master (1).tar.gz
# The script automatically picks the archive with the highest number.
CS_MANUAL_DOWNLOAD_DIR = Path(r"C:\Users\JHARVEY\OneDrive - Volvo Cars\Documents\06_Repos\cs-software-product-manual-download")

# Markdown output report path.
OUTPUT_FILE = Path("did_mapping_report.md")

# File filter for diagnostics repo scanning.
INCLUDE_PATH_REGEX = r"(?i)(manifest|did|hpa|hpb)"

# Default behavior: always update to latest on current branch.
UPDATE_TO_LATEST = True

# Optional pinned versions (branch, tag, or commit SHA).
# Leave empty string to use the current branch latest.
DIAGNOSTICS_TARGET_REF = ""
CS_TARGET_REF = ""
