# Function Definitions

## `req_link_map.parser`

| Function | Intent | Inputs | Output |
| --- | --- | --- | --- |
| `parse_pages` | Split extracted page text into versioned requirement records while retaining source pages. | Page text iterable and source name. | List of `Requirement` records. |
| `parse_pdf` | Extract text from a PDF with PyMuPDF and pass it to `parse_pages`. | PDF path. | List of `Requirement` records. |
| `merge_requirements` | Merge records from multiple PDFs and retain the highest numeric version of duplicate IDs. | Requirement iterable. | Deduplicated requirement list. |
| `build_graph` | Resolve requirement-ID, exact-name, and URL references; retain missing targets as external nodes. | Parsed requirements. | Dictionary containing JSON-ready nodes and edges. |

Private helpers normalize text, finish requirement blocks, and resolve references; they are implementation details rather than reusable API.

## `app`

| Function | Intent | Inputs | Output |
| --- | --- | --- | --- |
| `_analyse_paths` | Parse, merge, and graph a set of local PDF paths with summary statistics. | List of PDF paths. | JSON-ready graph dictionary. |
| `workspace_files` | List PDFs stored directly in the application folder. | None. | Sorted PDF filenames. |
| `analyse_workspace` | Analyze all PDFs stored directly in the application folder. | None. | Graph API response. |
| `analyse_uploads` | Validate temporary PDF uploads and analyze them. | FastAPI upload list. | Graph API response. |

## `static/app.js`

| Function | Intent | Inputs | Output |
| --- | --- | --- | --- |
| `escapeHtml` | Escape extracted PDF text before inserting it into HTML. | Text string. | HTML-safe string. |
| `loadMarkedIds` | Restore persistently marked requirement IDs from browser storage. | None. | Set of requirement IDs. |
| `saveMarkedIds` | Persist the current marked requirement IDs in browser storage. | None. | No return value; updates local storage. |
| `formatNodeLabel` | Create a compact, wrapped graph label with ID, version, and bounded title. | Requirement node. | Label string. |
| `toggleMarked` | Toggle and persist a node's marked state, then refresh its graph and detail styling. | Requirement ID. | No return value; updates state and the UI. |
| `applyMarkedFilter` | Keep marked-node neighborhoods visible and fade everything outside them when filtering is enabled. | None. | No return value; updates graph classes and filter control. |
| `toggleMarkedFilter` | Toggle the hide-unmarked graph mode. | None. | No return value; updates state and the graph. |
| `highlightedText` | Render a requirement's full text with typed reference highlights. | Requirement node. | HTML string. |
| `showDetails` | Populate and open the node detail panel. | Requirement node. | No return value; updates the DOM. |
| `focusNodeConnections` | Emphasize every edge incident to the selected node and mute unrelated edges. | Cytoscape node. | No return value; updates edge classes. |
| `clearConnectionFocus` | Restore default edge emphasis when the graph background is selected. | None. | No return value; updates edge classes. |
| `separateOverlappingNodes` | Resolve residual box collisions after natural layout while preserving nearby clusters. | Optional separation padding. | No return value; updates node positions. |
| `runLayout` | Arrange nodes in natural relationship clusters and optionally fit the completed layout to the viewport. | Optional animation and fit-all flags. | No return value; updates the graph and viewport. |
| `renderGraph` | Create the interactive Cytoscape graph and update controls and counters. | Graph API response. | No return value; updates application state and the DOM. |
| `setBusy` | Disable loading controls and display progress. | Status message. | No return value; updates the DOM. |
| `setReady` | Re-enable loading controls and display status. | Optional status message. | No return value; updates the DOM. |
| `requestGraph` | Submit an analysis request and render its response. | Endpoint URL and optional fetch options. | Promise completed after rendering or error display. |
| `refreshWorkspaceFiles` | Load and display PDFs found beside the application. | None. | Promise completed after updating the file list. |