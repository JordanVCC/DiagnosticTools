import requests
from config import (
    VIRA_BASE,
    VIRA_PAT,
    VIRA_PROJECT_KEY,
    VIRA_ISSUE_TYPE,
    FIELD_LEAD_PROJECT,
    FIELD_UNIT,
    FIELD_SECTION_FACTORY,
    FIELD_DEVELOPMENT_TASK,
    FIELD_LEADING_WORK_GROUP,
    FIELD_FEATURE_LINK,
    VALUE_LEADING_WORK_GROUP,
)


class ViraClientError(Exception):
    pass

class ViraClient:

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {VIRA_PAT}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        self._feature_fields_cache = {}

    def _fetch_feature_fields(self, feature_key):
        if feature_key in self._feature_fields_cache:
            return self._feature_fields_cache[feature_key]

        fields_to_copy = [
            FIELD_LEAD_PROJECT,
            FIELD_UNIT,
            FIELD_SECTION_FACTORY,
            FIELD_DEVELOPMENT_TASK,
        ]
        url = f"{VIRA_BASE}/rest/api/2/issue/{feature_key}"
        params = {"fields": ",".join(fields_to_copy)}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
        except requests.RequestException as exc:
            raise ViraClientError(f"Failed to fetch feature {feature_key}: {exc}") from exc

        if response.status_code in (401, 403):
            raise ViraClientError(
                "VIRA PAT is expired or invalid. "
                "Update VIRA_PAT and run again."
            )
        if response.status_code == 404:
            raise ViraClientError(f"Feature {feature_key} was not found in VIRA.")
        if response.status_code >= 400:
            raise ViraClientError(
                f"Failed reading feature {feature_key} ({response.status_code}): {response.text}"
            )

        payload = response.json()
        fields = payload.get("fields", {})
        copied = {}
        missing = []
        for field_id in fields_to_copy:
            value = fields.get(field_id)
            if value is None or value == "":
                missing.append(field_id)
            else:
                copied[field_id] = value

        if missing:
            raise ViraClientError(
                "Feature is missing required fields to copy into stories: "
                + ", ".join(missing)
            )

        self._feature_fields_cache[feature_key] = copied
        return copied

    def create_story(self, summary, description, feature_key):
        if not summary or not summary.strip():
            raise ViraClientError("Missing fields: summary is required.")
        if not description or not description.strip():
            raise ViraClientError("Missing fields: description is required.")
        if not feature_key or not feature_key.strip():
            raise ViraClientError("Missing fields: feature key is required.")

        copied_feature_fields = self._fetch_feature_fields(feature_key)

        url = f"{VIRA_BASE}/rest/api/2/issue"
        payload = {
            "fields": {
                "project": {"key": VIRA_PROJECT_KEY},
                "issuetype": {"name": VIRA_ISSUE_TYPE},

                # Required business fields
                "summary": summary,
                "description": description,

                # Inherit custom values from the selected feature.
                **copied_feature_fields,

                # Static custom field(s)
                FIELD_LEADING_WORK_GROUP: {"value": VALUE_LEADING_WORK_GROUP},

                # Feature Link
                FIELD_FEATURE_LINK: feature_key,
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
        except requests.RequestException as exc:
            raise ViraClientError(f"VIRA create issue request failed: {exc}") from exc

        if response.status_code in (401, 403):
            raise ViraClientError(
                "VIRA PAT is expired or invalid. "
                "Update VIRA_PAT and run again."
            )

        if response.status_code not in (200, 201):
            try:
                error_body = response.json()
            except ValueError:
                error_body = response.text
            raise ViraClientError(
                f"Create issue failed ({response.status_code}): {error_body}"
            )

        issue_key = response.json().get("key")
        if not issue_key:
            raise ViraClientError("Create issue response missing issue key.")

        return issue_key