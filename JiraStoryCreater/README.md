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

Keep PATs out of `config.py`. Set environment variables for the current session:

```powershell
$env:CONFLUENCE_PAT="your_confluence_pat"
$env:VIRA_PAT="your_vira_pat"
```

These you can get from confluence and Vira settings respectively.

Alternatively, copy `secrets.example.json` to `secrets.local.json` in this folder
and enter the PATs there. `secrets.local.json` is ignored by Git. Environment
variables take precedence over the local file. Missing or invalid credentials
stop the script before any requests are made. Existing local credentials were
migrated to this file during the repository cleanup.

Never commit the local file or real values in the example. Rotate any PAT that
has previously been committed, since deleting it does not remove Git history.

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

## 4. Credential Tests

From the repository root, run `python -m unittest discover -s JiraStoryCreater -p test_config.py -v`.
Tests use isolated temporary files and fake credentials, without network access.
See `FUNCTION_DEFINITIONS.md` for the function reference.
