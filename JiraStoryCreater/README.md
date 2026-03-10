# Exovision Feature Story Generator (Confluence -> VIRA)

This tool automatically creates all 9 Exovision Feature WoW Stories in VIRA, using the templates stored on Confluence.

The following fields are copied from the selected Feature automatically for every created Story:
- Lead Project
- Unit
- Section Factory
- Development Task

## 1. Requirements

- Python 3.9+
- `pip install requests beautifulsoup4`

## 2. Environment Variables

Set your PATs securely in config.py:

```powershell
$env:CONFLUENCE_PAT="your_confluence_pat"
$env:VIRA_PAT="your_vira_pat"
```

These you can get from confluence and Vira settings respectively.

Optional overrides (defaults are already configured in code):

```powershell
$env:VIRA_FIELD_LEADING_WORK_GROUP="customfield_14400"
$env:VIRA_VALUE_LEADING_WORK_GROUP="ART ADADAS - Exovision"
```

## 3. Run

Set your inputs in `userInputs.py`:

```python
FEATURE_KEY = "ARTADADAS-123"
RELEASE_TAG = "REL16"
INCLUDE_INTERNAL_INTERFACES = True
```

Run the code by clicking run in VS Code or run the below command

```powershell
python .\generate_feature_package.py
```
