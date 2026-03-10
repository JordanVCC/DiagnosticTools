import sys
import userInputs

FEATURE_KEY = getattr(userInputs, "FEATURE_KEY", "")
INCLUDE_INTERNAL_INTERFACES = getattr(userInputs, "INCLUDE_INTERNAL_INTERFACES", True)
RELEASE_TAG = getattr(userInputs, "RELEASE_TAG", "")

try:
    from confluence_fetcher import ConfluenceFetcher, ConfluenceError
    from story_builder import StoryBuilder
    from vira_client import ViraClient, ViraClientError
except ModuleNotFoundError as exc:
    missing_module = getattr(exc, "name", "unknown")
    print(f"[ERROR] Missing Python dependency: {missing_module}")
    print("[FIX] Install required packages:")
    print("      pip install requests beautifulsoup4")
    sys.exit(1)
except RuntimeError as exc:
    print(f"[ERROR] {exc}")
    print("[FIX] Set required PAT environment variables: CONFLUENCE_PAT and VIRA_PAT")
    sys.exit(1)
except ImportError as exc:
    print(f"[ERROR] Import failed: {exc}")
    print("[FIX] Check local file names and symbols in this folder.")
    sys.exit(1)

def main():
    feature_key = (FEATURE_KEY or "").strip()
    release_tag = (RELEASE_TAG or "").strip()
    if not feature_key:
        print("[ERROR] FEATURE_KEY is missing in userInputs.py")
        print("[FIX] Set FEATURE_KEY in userInputs.py, for example: FEATURE_KEY = \"ARTADADAS-123\"")
        sys.exit(1)
    if not release_tag:
        print("[ERROR] RELEASE_TAG is missing in userInputs.py")
        print("[FIX] Set RELEASE_TAG in userInputs.py, for example: RELEASE_TAG = \"REL16\"")
        sys.exit(1)

    include_internal = bool(INCLUDE_INTERNAL_INTERFACES)

    print("[INFO] Fetching story templates from Confluence...")
    fetcher = ConfluenceFetcher()
    try:
        parsed = fetcher.parse_story_templates()
    except ConfluenceError as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)

    print("[INFO] Building Story package...")
    builder = StoryBuilder(parsed, include_internal, release_tag)
    try:
        stories = builder.ordered_stories()
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)

    print("[INFO] Connecting to VIRA and creating stories...")
    vira = ViraClient()

    created = []
    for title, html, story_number in stories:
        print(f"[INFO] Creating: {title}")
        try:
            story_key = vira.create_story(
                summary=title,
                description=html,
                feature_key=feature_key,
            )
        except ViraClientError as exc:
            print(f"[ERROR] Failed creating Story {story_number}: {exc}")
            sys.exit(1)

        created.append(story_key)
        print(f"[SUCCESS] Created {story_key}")

    print("\n======== DONE ========")
    print(f"Feature: {feature_key}")
    print("Stories created:")
    for s in created:
        print(f" - {s}")

if __name__ == "__main__":
    main()