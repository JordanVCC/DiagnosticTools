import re
from bs4 import BeautifulSoup


class StoryBuilder:

    def __init__(self, parsed_stories, include_internal_interfaces=True, release_tag="RELXX"):
        self.parsed = parsed_stories
        self.include_internal = include_internal_interfaces
        self.release_tag = release_tag.strip().strip("[]")

    def _clean_heading_title(self, raw_title, story_number):
        title = raw_title.strip()
        # Remove leading icon + "Story N" prefix when present.
        title = re.sub(rf"^.*?\bStory\s*{story_number}\b\s*[:\-\)]*\s*", "", title, flags=re.IGNORECASE)
        title = re.sub(r"\s+", " ", title).strip(" -:\t")
        if re.fullmatch(r"\(?\s*conditional\s*\)?", title, flags=re.IGNORECASE):
            return ""
        if title and not re.fullmatch(rf"Story\s*{story_number}", title, flags=re.IGNORECASE):
            return title
        return ""

    @staticmethod
    def _is_generic_story_text(text):
        return bool(
            re.fullmatch(
                r"(?:[^A-Za-z0-9]*)?story\s*[1-9]\b(?:\s*\(conditional\))?\s*",
                text.strip(),
                flags=re.IGNORECASE,
            )
        )

    @staticmethod
    def _normalize_line(line):
        cleaned = re.sub(r"\s+", " ", line).strip()
        cleaned = cleaned.strip("*#>\t -")
        return cleaned

    def _extract_sections_from_description(self, description):
        soup = BeautifulSoup(description, "html.parser")
        raw_text = soup.get_text("\n", strip=True) if hasattr(soup, "get_text") else str(description)
        lines = [self._normalize_line(line) for line in raw_text.splitlines()]
        lines = [line for line in lines if line]

        sections = {"preamble": [], "title": [], "description": [], "acceptance": []}
        current_section = None

        label_pattern = re.compile(
            r"^(story\s*title|title|description|acceptance\s*criteria)\s*:?\s*(.*)$",
            flags=re.IGNORECASE,
        )

        for line in lines:
            label_match = label_pattern.match(line)
            if label_match:
                label = label_match.group(1).lower()
                inline_value = self._normalize_line(label_match.group(2))
                if "acceptance" in label:
                    current_section = "acceptance"
                elif "description" in label:
                    current_section = "description"
                else:
                    current_section = "title"

                if inline_value:
                    sections[current_section].append(inline_value)
                continue

            if current_section:
                sections[current_section].append(line)
            else:
                # Content before first known label often contains "Story N" then the actual title.
                sections["preamble"].append(line)

        return sections

    def _title_from_sections(self, sections, story_number):
        candidates = (
            sections.get("title", [])
            + sections.get("preamble", [])
            + sections.get("description", [])
        )
        for text in candidates:
            cleaned = self._normalize_line(text)
            if not cleaned:
                continue
            if self._is_generic_story_text(cleaned):
                continue
            if len(cleaned) < 12:
                continue
            return cleaned
        raise ValueError(
            f"Could not derive an informative title for Story {story_number}. "
            "Ensure the Confluence section includes a Title or meaningful Description line."
        )

    def _format_description(self, sections, story_number):
        description_lines = [self._normalize_line(x) for x in sections.get("description", []) if self._normalize_line(x)]
        acceptance_lines = [self._normalize_line(x) for x in sections.get("acceptance", []) if self._normalize_line(x)]

        if not description_lines:
            raise ValueError(
                f"Story {story_number} is missing 'Description' content in Confluence."
            )
        if not acceptance_lines:
            raise ValueError(
                f"Story {story_number} is missing 'Acceptance Criteria' content in Confluence."
            )

        formatted_acceptance = []
        for line in acceptance_lines:
            if re.match(r"^([-*]|\d+[.)])\s+", line):
                formatted_acceptance.append(line)
            else:
                formatted_acceptance.append(f"- {line}")

        return (
            "h3. Description\n"
            + "\n".join(description_lines)
            + "\n\nh3. Acceptance Criteria\n"
            + "\n".join(formatted_acceptance)
        )

    def _format_summary(self, story_data, story_number):
        heading_title = story_data.get("title", "")
        description = story_data.get("description", "")
        sections = self._extract_sections_from_description(description)

        informative_title = self._clean_heading_title(heading_title, story_number)
        if not informative_title:
            informative_title = self._title_from_sections(sections, story_number)

        formatted_description = self._format_description(sections, story_number)
        return f"[{self.release_tag}] - {informative_title}", formatted_description

    def ordered_stories(self):
        result = []

        for i in range(1, 10):
            if i not in self.parsed:
                raise ValueError(f"Missing Story {i} in parsed content.")

            if i == 5 and not self.include_internal:
                print("[INFO] Skipping conditional Story 5.")
                continue

            story_data = self.parsed[i]
            description = story_data.get("description", "").strip()
            if not description:
                raise ValueError(f"Story {i} is missing description.")

            title, jira_description = self._format_summary(story_data, i)

            result.append((title, jira_description, i))

        return result