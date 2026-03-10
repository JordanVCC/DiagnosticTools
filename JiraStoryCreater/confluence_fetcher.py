import requests
import re
from bs4 import BeautifulSoup
from config import CONFLUENCE_BASE, CONFLUENCE_PAT, EXOVISION_PAGE_ID


class ConfluenceError(Exception):
    pass

class ConfluenceFetcher:

    @staticmethod
    def _score_story_block(text):
        lowered = text.lower()
        score = len(text)
        if "description" in lowered:
            score += 500
        if "acceptance criteria" in lowered:
            score += 500
        return score

    @staticmethod
    def _extract_story_description(heading):
        """Extract story content after a heading until the next heading."""
        content_parts = []

        # Primary path: preserve HTML from direct sibling nodes.
        for sibling in heading.next_siblings:
            if getattr(sibling, "name", None) and re.match(r"^h[1-6]$", sibling.name):
                break
            text = str(sibling).strip()
            if text:
                content_parts.append(text)

        description_html = "\n".join(content_parts).strip()
        if description_html:
            return description_html

        # Fallback path: gather text content in document order until next heading.
        text_lines = []
        for elem in heading.next_elements:
            if elem is heading:
                continue
            # Skip text that belongs to the heading itself.
            if getattr(elem, "parent", None) is heading:
                continue
            if getattr(elem, "name", None) and re.match(r"^h[1-6]$", elem.name):
                break
            if isinstance(elem, str):
                line = elem.strip()
                if line:
                    text_lines.append(line)

        # Keep text compact and stable even for complex macro-based Confluence markup.
        deduped = []
        for line in text_lines:
            if not deduped or deduped[-1] != line:
                deduped.append(line)
        return "\n".join(deduped).strip()

    def get_page_html(self):
        url = f"{CONFLUENCE_BASE}/rest/api/content/{EXOVISION_PAGE_ID}?expand=body.storage"
        headers = {
            "Authorization": f"Bearer {CONFLUENCE_PAT}",
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, headers=headers, timeout=30)
        except requests.RequestException as exc:
            raise ConfluenceError(
                f"Confluence page inaccessible at {url}: {exc}"
            ) from exc

        if response.status_code in (401, 403):
            raise ConfluenceError(
                "Confluence PAT expired or invalid. "
                "Update CONFLUENCE_PAT and run again."
            )
        if response.status_code == 404:
            raise ConfluenceError(
                f"Confluence page {EXOVISION_PAGE_ID} not found."
            )
        if response.status_code >= 400:
            raise ConfluenceError(
                f"Confluence request failed ({response.status_code}): {response.text}"
            )

        data = response.json()
        html = data.get("body", {}).get("storage", {}).get("value")
        if not html:
            raise ConfluenceError(
                "Confluence response is missing body.storage.value content."
            )
        return html

    def parse_story_templates(self):
        """Return a map of story number to title/description for Story 1-9."""
        html = self.get_page_html()
        soup = BeautifulSoup(html, "html.parser")

        # Primary strategy: parse story blocks from normalized text lines.
        parsed = self._parse_story_blocks_from_text(soup)
        if all(i in parsed for i in range(1, 10)):
            return parsed

        # Fallback strategy: parse from heading blocks when line parsing is incomplete.
        heading_pattern = re.compile(r"\bStory\s*([1-9])\b", re.IGNORECASE)

        headings = soup.find_all(re.compile(r"^h[1-6]$"))

        for heading in headings:
            heading_text = heading.get_text(" ", strip=True)
            match = heading_pattern.search(heading_text)
            if not match:
                continue

            story_num = int(match.group(1))
            description_html = self._extract_story_description(heading)
            if not description_html:
                continue

            candidate = {
                "title": heading_text,
                "description": description_html,
            }

            if story_num not in parsed:
                parsed[story_num] = candidate
                continue

            existing = parsed[story_num]
            if self._score_story_block(candidate["description"]) > self._score_story_block(existing["description"]):
                parsed[story_num] = candidate

        missing = [str(i) for i in range(1, 10) if i not in parsed]
        if missing:
            raise ConfluenceError(
                "Missing expected story sections in Confluence template: "
                + ", ".join(missing)
            )

        return parsed

    def _parse_story_blocks_from_text(self, soup):
        text_blob = soup.get_text("\n", strip=True)
        raw_lines = [line.strip() for line in text_blob.splitlines() if line and line.strip()]

        story_line_pattern = re.compile(r"^(?:[^A-Za-z0-9]*)?Story\s*([1-9])\b.*$", re.IGNORECASE)

        starts = []
        for idx, line in enumerate(raw_lines):
            match = story_line_pattern.match(line)
            if match:
                starts.append((int(match.group(1)), idx))

        parsed = {}
        for pos, (story_num, start_idx) in enumerate(starts):
            end_idx = starts[pos + 1][1] if pos + 1 < len(starts) else len(raw_lines)
            block_lines = raw_lines[start_idx:end_idx]
            if not block_lines:
                continue

            # Keep the entire text block so StoryBuilder can extract Title/Description/AC deterministically.
            description_text = "\n".join(block_lines).strip()
            if not description_text:
                continue

            if story_num not in parsed or len(description_text) > len(parsed[story_num]["description"]):
                parsed[story_num] = {
                    "title": block_lines[0],
                    "description": description_text,
                }

        return parsed