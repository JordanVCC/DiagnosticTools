const edgeColors = { id: "#d1493f", name: "#1769aa", direct: "#7d3c98" };
const edgeOffsets = { id: -24, name: 24, direct: 0 };
const MARK_STORAGE_KEY = "req-link-map-marked-nodes";
const state = { graph: null, nodes: new Map(), cytoscape: null, marked: loadMarkedIds(), hideUnmarked: false };

const elements = {
  detail: document.querySelector("#detailPanel"),
  empty: document.querySelector("#emptyState"),
  externalCount: document.querySelector("#externalCount"),
  fileInput: document.querySelector("#fileInput"),
  fileList: document.querySelector("#fileList"),
  fitButton: document.querySelector("#fitButton"),
  folderButton: document.querySelector("#folderButton"),
  hideUnmarkedButton: document.querySelector("#hideUnmarkedButton"),
  layoutButton: document.querySelector("#layoutButton"),
  linkCount: document.querySelector("#linkCount"),
  requirementCount: document.querySelector("#requirementCount"),
  searchInput: document.querySelector("#searchInput"),
  status: document.querySelector("#status"),
};

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, character => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#039;",
  })[character]);
}

function loadMarkedIds() {
  try {
    const ids = JSON.parse(localStorage.getItem(MARK_STORAGE_KEY) || "[]");
    return new Set(Array.isArray(ids) ? ids : []);
  } catch {
    return new Set();
  }
}

function saveMarkedIds() {
  localStorage.setItem(MARK_STORAGE_KEY, JSON.stringify([...state.marked]));
}

function formatNodeLabel(node) {
  const title = node.title.length > 58 ? `${node.title.slice(0, 55).trim()}...` : node.title;
  return `${node.id}${node.version ? ` v${node.version}` : ""}\n${title}`;
}

function toggleMarked(nodeId) {
  const isMarked = state.marked.has(nodeId);
  if (isMarked) state.marked.delete(nodeId);
  else state.marked.add(nodeId);
  saveMarkedIds();
  state.cytoscape?.getElementById(nodeId).toggleClass("marked", !isMarked);
  applyMarkedFilter();
  showDetails(state.nodes.get(nodeId));
}

function applyMarkedFilter() {
  const cytoscapeGraph = state.cytoscape;
  if (!cytoscapeGraph) return;

  const markedNodes = cytoscapeGraph.nodes().filter(node => state.marked.has(node.id()));
  elements.hideUnmarkedButton.disabled = markedNodes.length === 0;
  if (markedNodes.length === 0) state.hideUnmarked = false;

  cytoscapeGraph.elements().removeClass("mark-filter-muted");
  if (state.hideUnmarked) {
    let visibleElements = markedNodes;
    markedNodes.forEach(node => {
      visibleElements = visibleElements.union(node.closedNeighborhood());
    });
    cytoscapeGraph.elements().not(visibleElements).addClass("mark-filter-muted");
  }

  elements.hideUnmarkedButton.setAttribute("aria-pressed", String(state.hideUnmarked));
  elements.hideUnmarkedButton.textContent = state.hideUnmarked ? "Show all" : "Hide unmarked";
}

function toggleMarkedFilter() {
  state.hideUnmarked = !state.hideUnmarked;
  applyMarkedFilter();
}

function highlightedText(node) {
  const matches = [];
  for (const reference of node.references) {
    const needle = reference.match;
    let start = node.text.toLocaleLowerCase().indexOf(needle.toLocaleLowerCase());
    while (start >= 0) {
      matches.push({ start, end: start + needle.length, type: reference.type, target: reference.target });
      start = node.text.toLocaleLowerCase().indexOf(needle.toLocaleLowerCase(), start + needle.length);
    }
  }
  matches.sort((left, right) => left.start - right.start || right.end - left.end);

  let cursor = 0;
  let html = "";
  for (const match of matches) {
    if (match.start < cursor) continue;
    html += escapeHtml(node.text.slice(cursor, match.start));
    html += `<mark class="reference ${match.type}" title="Links to ${escapeHtml(match.target)}">${escapeHtml(node.text.slice(match.start, match.end))}</mark>`;
    cursor = match.end;
  }
  return html + escapeHtml(node.text.slice(cursor));
}

function showDetails(node) {
  const pageText = node.pages.length ? `Pages ${node.pages.join(", ")}` : "No source page";
  const isMarked = state.marked.has(node.id);
  elements.detail.innerHTML = `
    <div class="detail-header">
      <div class="detail-heading-row">
        <div class="detail-id">${escapeHtml(node.id)}${node.version ? ` v${escapeHtml(node.version)}` : ""}${node.external ? '<span class="external-badge">EXTERNAL</span>' : ""}</div>
        <button id="markButton" class="mark-button${isMarked ? " active" : ""}" type="button" aria-pressed="${isMarked}" title="${isMarked ? "Remove persistent highlight" : "Keep this node highlighted"}">${isMarked ? "Unmark" : "Mark node"}</button>
      </div>
      <h2>${escapeHtml(node.title)}</h2>
      <div class="detail-meta">${escapeHtml(node.source)} &middot; ${pageText}</div>
    </div>
    <div class="detail-body"><pre>${highlightedText(node)}</pre></div>`;
  document.querySelector("#markButton").addEventListener("click", () => toggleMarked(node.id));
  elements.detail.classList.add("open");
}

function focusNodeConnections(node) {
  const edges = state.cytoscape?.edges();
  if (!edges) return;
  edges.removeClass("connection-focus connection-muted");
  edges.not(node.connectedEdges()).addClass("connection-muted");
  node.connectedEdges().addClass("connection-focus");
}

function clearConnectionFocus() {
  state.cytoscape?.edges().removeClass("connection-focus connection-muted");
}

function separateOverlappingNodes(padding = 24) {
  const nodes = state.cytoscape?.nodes();
  if (!nodes) return;

  for (let pass = 0; pass < 24; pass++) {
    let moved = false;
    for (let leftIndex = 0; leftIndex < nodes.length; leftIndex++) {
      const leftNode = nodes[leftIndex];
      for (let rightIndex = leftIndex + 1; rightIndex < nodes.length; rightIndex++) {
        const rightNode = nodes[rightIndex];
        const horizontalDistance = rightNode.position("x") - leftNode.position("x");
        const verticalDistance = rightNode.position("y") - leftNode.position("y");
        const horizontalOverlap = (leftNode.width() + rightNode.width()) / 2 + padding - Math.abs(horizontalDistance);
        const verticalOverlap = (leftNode.height() + rightNode.height()) / 2 + padding - Math.abs(verticalDistance);
        if (horizontalOverlap <= 0 || verticalOverlap <= 0) continue;

        moved = true;
        if (horizontalOverlap < verticalOverlap) {
          const direction = horizontalDistance >= 0 ? 1 : -1;
          leftNode.position("x", leftNode.position("x") - direction * horizontalOverlap / 2);
          rightNode.position("x", rightNode.position("x") + direction * horizontalOverlap / 2);
        } else {
          const direction = verticalDistance >= 0 ? 1 : -1;
          leftNode.position("y", leftNode.position("y") - direction * verticalOverlap / 2);
          rightNode.position("y", rightNode.position("y") + direction * verticalOverlap / 2);
        }
      }
    }
    if (!moved) break;
  }
}

function runLayout(animate = true, fitAll = true) {
  if (!state.cytoscape) return;
  state.cytoscape.layout({
    name: "fcose",
    quality: "default",
    randomize: true,
    animate,
    fit: false,
    animationDuration: 650,
    nodeDimensionsIncludeLabels: true,
    nodeSeparation: 120,
    nodeRepulsion: () => 12000,
    idealEdgeLength: () => 170,
    edgeElasticity: () => 0.35,
    gravity: 0.2,
    numIter: 2800,
    tile: true,
    tilingPaddingVertical: 60,
    tilingPaddingHorizontal: 60,
    stop: () => {
      separateOverlappingNodes();
      if (fitAll) state.cytoscape.fit(undefined, 50);
    },
  }).run();
}

function renderGraph(graph) {
  if (typeof cytoscape === "undefined") {
    throw new Error("The graph library could not be loaded. Check the network connection.");
  }
  state.graph = graph;
  state.nodes = new Map(graph.nodes.map(node => [node.id, node]));
  if (state.cytoscape) state.cytoscape.destroy();

  const graphElements = [
    ...graph.nodes.map(node => ({
      data: { ...node, label: formatNodeLabel(node) },
      classes: state.marked.has(node.id) ? "marked" : "",
    })),
    ...graph.edges.map((edge, index) => ({
      data: { id: `edge-${index}`, ...edge, color: edgeColors[edge.type], offset: edgeOffsets[edge.type] },
    })),
  ];

  state.cytoscape = cytoscape({
    container: document.querySelector("#graph"),
    elements: graphElements,
    wheelSensitivity: 0.33,
    minZoom: 0.12,
    maxZoom: 2.4,
    style: [
      { selector: "node", style: {
        "background-color": "#fbfaf6", "border-color": "#172326", "border-width": 2,
        "label": "data(label)", "shape": "round-rectangle", "width": 190, "height": 70,
        "font-family": "Bahnschrift", "font-size": 11, "font-weight": 600, "color": "#172326",
        "text-wrap": "wrap", "text-max-width": 166, "text-valign": "center", "text-halign": "center",
        "line-height": 1.25,
      } },
      { selector: "node[?external]", style: { "border-style": "dashed", "border-color": "#667477", "color": "#667477" } },
      { selector: "node.marked", style: { "background-color": "#ffe296", "border-color": "#9b6811", "border-width": 5 } },
      { selector: "node:selected", style: { "border-color": "#e5b84a", "border-width": 5 } },
      { selector: "edge", style: {
        "width": 2.2, "line-color": "data(color)", "target-arrow-color": "data(color)",
        "target-arrow-shape": "triangle", "curve-style": "unbundled-bezier",
        "control-point-distances": "data(offset)", "control-point-weights": 0.5, "opacity": 0.78,
      } },
      { selector: "edge.connection-muted", style: { "opacity": 0.48 } },
      { selector: "edge.connection-focus", style: {
        "width": 5, "opacity": 1, "z-index": 20,
        "underlay-color": "#172326", "underlay-opacity": 0.24, "underlay-padding": 5,
      } },
      { selector: ".faded", style: { "opacity": 0.1 } },
      { selector: ".mark-filter-muted", style: { "opacity": 0.1 } },
    ],
  });

  state.cytoscape.on("tap", "node", event => {
    focusNodeConnections(event.target);
    showDetails(state.nodes.get(event.target.id()));
  });
  state.cytoscape.on("tap", event => {
    if (event.target === state.cytoscape) {
      clearConnectionFocus();
      elements.detail.classList.remove("open");
    }
  });
  elements.empty.hidden = true;
  elements.searchInput.disabled = false;
  elements.fitButton.disabled = false;
  applyMarkedFilter();
  elements.layoutButton.disabled = false;
  elements.requirementCount.textContent = graph.stats.requirements;
  elements.linkCount.textContent = graph.stats.links;
  elements.externalCount.textContent = graph.stats.external;
  runLayout(false, false);
  state.cytoscape.fit(undefined, 38);
  if (state.cytoscape.zoom() < 0.8) {
    state.cytoscape.zoom(0.8);
    state.cytoscape.center();
  }
}

function setBusy(message) {
  elements.status.textContent = message;
  elements.folderButton.disabled = true;
  elements.fileInput.disabled = true;
}

function setReady(message = "Ready") {
  elements.status.textContent = message;
  elements.folderButton.disabled = false;
  elements.fileInput.disabled = false;
}

async function requestGraph(url, options = {}) {
  setBusy("Extracting requirements and resolving links...");
  try {
    const response = await fetch(url, { method: "POST", ...options });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || "Analysis failed.");
    renderGraph(payload);
    setReady(`${payload.stats.requirements} requirements mapped from ${payload.stats.documents} PDF${payload.stats.documents === 1 ? "" : "s"}`);
  } catch (error) {
    setReady(`Error: ${error.message}`);
  }
}

async function refreshWorkspaceFiles() {
  try {
    const response = await fetch("/api/workspace-files");
    const payload = await response.json();
    elements.fileList.innerHTML = payload.files.length
      ? payload.files.map(file => `<div class="file-item">${escapeHtml(file)}</div>`).join("")
      : '<span class="muted">No PDFs in this folder</span>';
    elements.folderButton.disabled = payload.files.length === 0;
  } catch {
    elements.fileList.innerHTML = '<span class="muted">Folder unavailable</span>';
  }
}

elements.fileInput.addEventListener("change", () => {
  if (!elements.fileInput.files.length) return;
  const form = new FormData();
  [...elements.fileInput.files].forEach(file => form.append("files", file));
  elements.fileList.innerHTML = [...elements.fileInput.files]
    .map(file => `<div class="file-item">${escapeHtml(file.name)}</div>`).join("");
  requestGraph("/api/analyse", { body: form });
});

elements.folderButton.addEventListener("click", () => requestGraph("/api/analyse-workspace"));
elements.fitButton.addEventListener("click", () => state.cytoscape?.fit(undefined, 38));
elements.hideUnmarkedButton.addEventListener("click", toggleMarkedFilter);
elements.layoutButton.addEventListener("click", () => runLayout(true, true));
elements.searchInput.addEventListener("input", event => {
  const query = event.target.value.trim().toLocaleLowerCase();
  const nodes = state.cytoscape?.nodes();
  if (!nodes) return;
  state.cytoscape.elements().removeClass("faded");
  if (!query) return;
  nodes.forEach(node => {
    const record = state.nodes.get(node.id());
    const matches = `${record.id} ${record.title} ${record.text}`.toLocaleLowerCase().includes(query);
    if (!matches) node.addClass("faded").connectedEdges().addClass("faded");
  });
});

refreshWorkspaceFiles();