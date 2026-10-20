# Function Definitions

## Configuration

| Function | Intent | Inputs | Outputs |
| --- | --- | --- | --- |
| `config.require_env` | Resolve an environment variable, falling back to ignored local credentials. | Variable name; environment; sibling `secrets.local.json`. | Nonempty string; raises `RuntimeError` for missing/invalid credentials or unreadable/invalid local JSON without exposing contents. |

## Confluence Templates

| Function | Intent | Inputs | Outputs |
| --- | --- | --- | --- |
| `ConfluenceFetcher._score_story_block` | Rank candidate story blocks. | Text. | Score based on length and section markers. |
| `ConfluenceFetcher._extract_story_description` | Extract content between headings. | BeautifulSoup heading. | Description HTML or text. |
| `ConfluenceFetcher.get_page_html` | Fetch the configured page through the Confluence API. | Configuration credentials and page ID. | HTML; raises `ConfluenceError` on failure. |
| `ConfluenceFetcher.parse_story_templates` | Fetch and parse story templates. | Configured Confluence page. | Mapping of story numbers to title/description dictionaries; raises on missing stories. |
| `ConfluenceFetcher._parse_story_blocks_from_text` | Parse normalized text as a fallback. | BeautifulSoup document. | Mapping of story numbers to template dictionaries. |

## Story Formatting

| Function | Intent | Inputs | Outputs |
| --- | --- | --- | --- |
| `StoryBuilder.__init__` | Store templates and formatting settings. | Parsed stories, internal-interface flag, release tag. | Initialized builder. |
| `StoryBuilder._clean_heading_title` | Remove story prefixes and generic headings. | Raw title, story number. | Clean title or empty string. |
| `StoryBuilder._is_generic_story_text` | Detect a bare story marker. | Text. | Boolean. |
| `StoryBuilder._normalize_line` | Normalize whitespace and list markers. | Line. | Normalized string. |
| `StoryBuilder._extract_sections_from_description` | Split HTML/text into named sections. | Description. | Preamble/title/description/acceptance line lists. |
| `StoryBuilder._title_from_sections` | Select an informative title. | Sections, story number. | Title; raises `ValueError` if none is usable. |
| `StoryBuilder._format_description` | Format required sections for Jira. | Sections, story number. | Description; raises for missing required content. |
| `StoryBuilder._format_summary` | Format a story title and description. | Story dictionary, story number. | Title/description tuple. |
| `StoryBuilder.ordered_stories` | Build stories in template order. | Stored templates and settings. | Title/description/number tuples; optionally excludes story 5. |

## Issue Creation

| Function | Intent | Inputs | Outputs |
| --- | --- | --- | --- |
| `ViraClient.__init__` | Configure API authentication and field caches. | Configuration. | Initialized client. |
| `ViraClient._fetch_feature_fields` | Fetch/cache inherited feature fields. | Feature issue key. | Field mapping; raises `ViraClientError` on failure. |
| `ViraClient.create_story` | Create a story with inherited feature fields. | Summary, description, feature key. | Created issue key; performs a network POST. |
| `generate_feature_package.main` | Fetch templates, format stories, and create issues. | Configuration and user inputs. | Console status; creates issues; exits on failure. |

## Credential Regression Tests

| Function | Intent | Inputs | Outputs |
| --- | --- | --- | --- |
| `CredentialConfigTests.setUp` | Isolate configuration from real secrets. | Temporary directory and cleared environment. | Test fixture; cleanup registered. |
| `CredentialConfigTests.load_config` | Import the isolated configuration. | Fixture config file. | Module or credential validation exception. |
| `CredentialConfigTests.write_secrets` | Write synthetic local JSON. | Test data. | Temporary credential file. |
| `test_environment_only` | Verify environment-only loading. | Fake environment values. | Assertions. |
| `test_local_file_only` | Verify local-only loading. | Fake JSON values. | Assertions. |
| `test_environment_overrides_local_file` | Verify precedence and mixed sources. | Fake environment and JSON values. | Assertions. |
| `test_missing_credentials_fail` | Verify missing-credential failure. | No credentials. | Expected exception assertion. |
| `test_invalid_local_values_fail` | Reject non-string/blank credentials. | Invalid synthetic JSON values. | Expected exception assertions. |
| `test_nonobject_json_fails` | Reject non-object credential JSON. | Synthetic array. | Expected exception assertion. |
| `test_malformed_json_does_not_expose_contents` | Keep JSON parse failures private. | Synthetic malformed JSON. | Error-redaction assertion. |