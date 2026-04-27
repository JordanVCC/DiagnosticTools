# Local Snapshot Data Parser

This viewer is used with the snapshot extraction flow to make Diagnostic Kernel event logs readable.

It loads snapshot log files, decodes event payloads, and helps you inspect camera snapshot data and fault-category related values quickly.

## What it does

- Parses and displays Diagnostic Kernel events in a readable UI
- Supports drag-and-drop loading of snapshot files
- Decodes payload values, including bitfields and snapshot-related entries
- Provides filters for ECU, event type, and DTC
- Includes free-text search across event content

## Supported input formats

- NDJSON (newline-delimited JSON)
- Length-prefixed binary protobuf event stream

You can use the included sample file success.json to test quickly.

## How to use

1. Open snapshot_viewer.html in a browser.
2. Drag and drop your snapshot file into the drop area.
3. After loading, use the filter bar to narrow results:
	 - ECU filter
	 - Event filter
	 - DTC picker (with search, select all, clear)
	 - Text search for descriptions or DTC IDs
4. Click an event card to expand and inspect full decoded payload details.

## Notes

- The tool attempts to detect whether the file is NDJSON or binary automatically.
- Malformed lines in NDJSON are skipped so partially valid files can still be viewed.

## Troubleshooting

- No events shown:
	- Verify the file is a supported format.
	- Try loading success.json to confirm the viewer is working.
- Wrong/partial decode:
	- Confirm the input came from the expected Diagnostic Kernel snapshot pipeline.
- Browser blocks local file:
	- Open the HTML file directly in a modern browser (Edge/Chrome) and drag-drop the data file into the page.
