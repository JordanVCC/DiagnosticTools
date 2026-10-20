import json
import os
from pathlib import Path

def require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        secrets_path = Path(__file__).with_name("secrets.local.json")
        if secrets_path.is_file():
            try:
                secrets = json.loads(secrets_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                raise RuntimeError("Cannot read secrets.local.json as valid JSON.") from None
            if not isinstance(secrets, dict):
                raise RuntimeError("secrets.local.json must contain a JSON object.")
            value = secrets.get(var_name)
    if not isinstance(value, str) or not value.strip():
        raise RuntimeError(
            f"Credential {var_name} is missing or invalid. "
            f"Set the environment variable or add it to secrets.local.json."
        )
    return value

# PATs
CONFLUENCE_PAT = require_env("CONFLUENCE_PAT")
VIRA_PAT = require_env("VIRA_PAT")

# Base URLs
CONFLUENCE_BASE = "https://confluence.volvocars.biz"
VIRA_BASE = "https://jira-vira.volvocars.biz"

# Confluence Page ID for Exovision WoW
EXOVISION_PAGE_ID = "1037013667"

# VIRA defaults
VIRA_PROJECT_KEY = os.getenv("VIRA_PROJECT_KEY", "ARTADADAS")
VIRA_ISSUE_TYPE = os.getenv("VIRA_ISSUE_TYPE", "Story")

# Custom field IDs
FIELD_LEAD_PROJECT = os.getenv("VIRA_FIELD_LEAD_PROJECT", "customfield_11001")
FIELD_UNIT = os.getenv("VIRA_FIELD_UNIT", "customfield_11002")
FIELD_SECTION_FACTORY = os.getenv("VIRA_FIELD_SECTION_FACTORY", "customfield_11003")
FIELD_DEVELOPMENT_TASK = os.getenv("VIRA_FIELD_DEVELOPMENT_TASK", "customfield_11004")
FIELD_LEADING_WORK_GROUP = os.getenv("VIRA_FIELD_LEADING_WORK_GROUP", "customfield_14400")
FIELD_FEATURE_LINK = os.getenv("VIRA_FIELD_FEATURE_LINK", "customfield_10702")

# Custom field values
# Lead Project / Unit / Section Factory / Development Task are inherited from the feature.
VALUE_LEADING_WORK_GROUP = os.getenv("VIRA_VALUE_LEADING_WORK_GROUP", "ART ADADAS - Exovision")
