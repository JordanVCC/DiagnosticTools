"""Local web service for interactive requirement-link maps."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.staticfiles import StaticFiles

from req_link_map import build_graph, merge_requirements, parse_pdf


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
MAX_UPLOAD_BYTES = 100 * 1024 * 1024

app = FastAPI(title="ReqLink Map")


def _analyse_paths(paths: list[Path]) -> dict[str, object]:
    requirements = merge_requirements(
        requirement
        for path in paths
        for requirement in parse_pdf(path)
    )
    if not requirements:
        raise HTTPException(status_code=422, detail="No REQ-<number> requirement headers were found.")

    graph = build_graph(requirements)
    graph["stats"] = {
        "documents": len(paths),
        "requirements": sum(not node["external"] for node in graph["nodes"]),
        "external": sum(bool(node["external"]) for node in graph["nodes"]),
        "links": len(graph["edges"]),
    }
    return graph


@app.get("/api/workspace-files")
def workspace_files() -> dict[str, list[str]]:
    """List PDFs available directly in the application folder."""
    return {"files": sorted(path.name for path in BASE_DIR.glob("*.pdf"))}


@app.post("/api/analyse-workspace")
def analyse_workspace() -> dict[str, object]:
    """Analyse all PDFs located directly in the application folder."""
    paths = sorted(BASE_DIR.glob("*.pdf"))
    if not paths:
        raise HTTPException(status_code=404, detail="No PDFs were found in the application folder.")
    return _analyse_paths(paths)


@app.post("/api/analyse")
async def analyse_uploads(files: list[UploadFile] = File(...)) -> dict[str, object]:
    """Save uploaded PDFs temporarily and return their merged requirement graph."""
    if not files:
        raise HTTPException(status_code=400, detail="Select at least one PDF.")

    with TemporaryDirectory(prefix="req-link-map-") as temp_directory:
        paths: list[Path] = []
        for index, upload in enumerate(files):
            filename = Path(upload.filename or f"document-{index}.pdf").name
            if Path(filename).suffix.casefold() != ".pdf":
                raise HTTPException(status_code=415, detail=f"{filename} is not a PDF.")

            content = await upload.read(MAX_UPLOAD_BYTES + 1)
            if len(content) > MAX_UPLOAD_BYTES:
                raise HTTPException(status_code=413, detail=f"{filename} exceeds 100 MB.")
            path = Path(temp_directory) / filename
            path.write_bytes(content)
            paths.append(path)

        try:
            return _analyse_paths(paths)
        except HTTPException:
            raise
        except Exception as error:
            raise HTTPException(status_code=422, detail=f"PDF extraction failed: {error}") from error


app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")