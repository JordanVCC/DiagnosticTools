# DID vs GMRDB Mapping Checker

This tool compares DID software labels from `spa2_vision_diagnostics` against DID ID
mappings in `cs-software-product/configuration/GMRDB_sync_config_*.yaml`.

## What it checks

For every DID entry found in the diagnostics repo that has a `sw_label`, it verifies
that the same software label exists in one of these mapping files:

- `GMRDB_sync_config_hpagen3_ad.yaml`
- `GMRDB_sync_config_hpagen3_adas.yaml`
- `GMRDB_sync_config_hpagen4.yaml`
- `GMRDB_sync_config_hpb.yaml`

It outputs a Markdown table with:

- SW label
- Diagnostic DID value (if present in manifest)
- Mapped DID ID from cs-software product
- Status (`OK` or `MISSING`)
- Source file references

## Usage

1. Edit `user_inputs.py` and set:
   - `DIAGNOSTICS_REPO_PATH`
   - `CS_REPO_PATH`
   - `CS_CONFIGURATION_PATH` (optional fallback if cs repo cannot be cloned)
   - `OUTPUT_FILE` (optional)
   - `INCLUDE_PATH_REGEX` (optional)
   - `UPDATE_TO_LATEST` (default `True`)
   - `DIAGNOSTICS_TARGET_REF` and `CS_TARGET_REF` (optional)

2. Run:

```bash
python compare_did_mappings.py
```

Notes:
- By default, the script always runs `git fetch --all --prune` and `git pull --ff-only` for both repos.
- If `DIAGNOSTICS_TARGET_REF` or `CS_TARGET_REF` is set (branch, tag, or commit), the script checks out that ref first.
- For pinned commit/tag refs, pulling is skipped when Git is in detached HEAD.
- If Gerrit clone/download is blocked, set `CS_CONFIGURATION_PATH` to a folder containing:
   - `GMRDB_sync_config_hpagen3_ad.yaml`
   - `GMRDB_sync_config_hpagen3_adas.yaml`
   - `GMRDB_sync_config_hpagen4.yaml`
   - `GMRDB_sync_config_hpb.yaml`
