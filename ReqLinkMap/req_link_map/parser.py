"""Extract requirements and their cross-references from PDF text."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
import re
from typing import Iterable


HEADER_RE = re.compile(
    r"^\s*REQ\s*-\s*(?P<number>\d+)(?:v(?P<version>\d+))?\s+(?P<title>\S.*)\s*$",
    re.IGNORECASE,
)
REFERENCE_RE = re.compile(r"\bREQ\s*-\s*(\d+)\b", re.IGNORECASE)
URL_RE = re.compile(r"https?://[^\s<>\"]+", re.IGNORECASE)
PAGE_MARKER_RE = re.compile(r"^\s*-\s*\d+\s*-\s*$")


@dataclass
class Requirement:
    """A requirement recovered from one source document."""

    id: str
    version: str | None
    title: str
    text: str
    source: str
    pages: list[int] = field(default_factory=list)


@dataclass(frozen=True)
class Reference:
    """A resolved relationship between two requirements."""

    source: str
    target: str
    type: str
    match: str


def _normalise_space(value: str) -> str:
    return " ".join(value.casefold().split())


def parse_pages(page_texts: Iterable[str], source: str) -> list[Requirement]:
    """Parse requirement blocks from page text while retaining page provenance."""
    requirements: list[Requirement] = []
    current: Requirement | None = None
    body_lines: list[str] = []

    def finish_current() -> None:
        nonlocal current, body_lines
        if current is None:
            return
        current.text = "\n".join(body_lines).strip()
        requirements.append(current)
        current = None
        body_lines = []

    for page_number, page_text in enumerate(page_texts, start=1):
        for line in page_text.splitlines():
            header = HEADER_RE.match(line)
            if header:
                finish_current()
                current = Requirement(
                    id=f"REQ-{header.group('number')}",
                    version=header.group("version"),
                    title=header.group("title").strip(),
                    text="",
                    source=source,
                    pages=[page_number],
                )
                body_lines = [line.strip()]
                continue

            if current is not None:
                if page_number not in current.pages:
                    current.pages.append(page_number)
                if not PAGE_MARKER_RE.match(line):
                    body_lines.append(line.rstrip())

    finish_current()
    return requirements


def parse_pdf(path: str | Path) -> list[Requirement]:
    """Extract page text from a PDF and parse its requirements."""
    import fitz

    pdf_path = Path(path)
    with fitz.open(pdf_path) as document:
        pages = [page.get_text("text") for page in document]
    return parse_pages(pages, pdf_path.name)


def merge_requirements(requirements: Iterable[Requirement]) -> list[Requirement]:
    """Deduplicate requirements, preferring the highest numeric version."""
    merged: dict[str, Requirement] = {}
    for requirement in requirements:
        existing = merged.get(requirement.id)
        existing_version = int(existing.version or 0) if existing else -1
        candidate_version = int(requirement.version or 0)
        if existing is None or candidate_version >= existing_version:
            merged[requirement.id] = requirement
    return list(merged.values())


def _find_references(requirements: list[Requirement]) -> list[Reference]:
    by_id = {requirement.id: requirement for requirement in requirements}
    references: dict[tuple[str, str, str], Reference] = {}

    for requirement in requirements:
        body = "\n".join(requirement.text.splitlines()[1:])
        url_spans: list[tuple[int, int]] = []
        for url_match in URL_RE.finditer(body):
            url_spans.append(url_match.span())
            for id_match in REFERENCE_RE.finditer(url_match.group(0)):
                target_id = f"REQ-{id_match.group(1)}"
                if target_id != requirement.id:
                    key = (requirement.id, target_id, "direct")
                    references[key] = Reference(
                        source=requirement.id,
                        target=target_id,
                        type="direct",
                        match=url_match.group(0).rstrip(".,);"),
                    )

        for match in REFERENCE_RE.finditer(body):
            if any(start <= match.start() < end for start, end in url_spans):
                continue
            target_id = f"REQ-{match.group(1)}"
            if target_id != requirement.id:
                key = (requirement.id, target_id, "id")
                references[key] = Reference(
                    source=requirement.id,
                    target=target_id,
                    type="id",
                    match=match.group(0),
                )

        normalised_body = _normalise_space(body)
        for candidate in requirements:
            if candidate.id == requirement.id or len(candidate.title) < 8:
                continue
            if _normalise_space(candidate.title) in normalised_body:
                key = (requirement.id, candidate.id, "name")
                references.setdefault(
                    key,
                    Reference(
                        source=requirement.id,
                        target=candidate.id,
                        type="name",
                        match=candidate.title,
                    ),
                )

    return list(references.values())


def build_graph(requirements: list[Requirement]) -> dict[str, list[dict[str, object]]]:
    """Create JSON-ready nodes and ID/name/direct-link edges."""
    references = _find_references(requirements)
    known_ids = {requirement.id for requirement in requirements}
    references_by_source: dict[str, list[dict[str, str]]] = {}
    for reference in references:
        references_by_source.setdefault(reference.source, []).append(asdict(reference))

    nodes: list[dict[str, object]] = []
    for requirement in requirements:
        node = asdict(requirement)
        node["references"] = references_by_source.get(requirement.id, [])
        node["external"] = False
        nodes.append(node)

    referenced_ids = {reference.target for reference in references}
    for external_id in sorted(referenced_ids - known_ids):
        nodes.append(
            {
                "id": external_id,
                "version": None,
                "title": "Referenced requirement not included",
                "text": "This requirement is referenced but was not found in the uploaded PDFs.",
                "source": "External reference",
                "pages": [],
                "references": [],
                "external": True,
            }
        )

    return {
        "nodes": nodes,
        "edges": [asdict(reference) for reference in references],
    }