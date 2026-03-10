import os

def require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(
            f"Environment variable {var_name} is missing. "
            f"Set {var_name} before running the script."
        )
    return value

# PATs
CONFLUENCE_PAT = "YOUR PAT HERE"
VIRA_PAT = "YOUR PAT HERE"

# Base URLs
CONFLUENCE_BASE = "YOUR PAT HERE"
VIRA_BASE = "YOUR PAT HERE"

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
