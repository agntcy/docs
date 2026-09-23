# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: CC-BY-4.0

"""Check the agent-readable artifacts produced by the MkDocs build."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE_HOST = "docs.agntcy.org"
MAX_INDEX_LENGTH = 50_000
LINK = re.compile(r"(?m)^- \[[^\]]+\]\(([^)]+)\)")
UNRESOLVED_MACRO = re.compile(r"\[\[\s*agntcy\.")


def expected_markdown_path(source: Path) -> Path:
    """Return the pretty-URL Markdown path for a source page."""
    if source.name == "index.md":
        return source
    return source.with_suffix("") / "index.md"


def check(site: Path, docs: Path) -> None:
    """Validate the index and every generated Markdown page."""
    index_path = site / "llms.txt"
    if not index_path.is_file():
        raise ValueError("Missing llms.txt")

    index = index_path.read_text(encoding="utf-8")
    if not index.startswith("# Agntcy\n\n> "):
        raise ValueError("llms.txt needs a title and a blockquote summary")
    if len(index) > MAX_INDEX_LENGTH:
        raise ValueError("llms.txt exceeds the 50,000-character limit")

    links = LINK.findall(index)
    if not links:
        raise ValueError("llms.txt contains no links")

    linked_pages: set[Path] = set()
    for link in links:
        parsed = urlsplit(link)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError(f"Index link must be an absolute HTTPS URL: {link}")
        if parsed.netloc == SITE_HOST:
            local_path = Path(unquote(parsed.path.lstrip("/")))
            if local_path.is_absolute() or ".." in local_path.parts:
                raise ValueError(f"Index link has an unsafe path: {link}")
            if local_path.suffix != ".md":
                raise ValueError(f"Index link must point to Markdown: {link}")
            if not (site / local_path).is_file():
                raise ValueError(f"Index link has no generated page: {link}")
            linked_pages.add(local_path)

    expected_pages = {
        expected_markdown_path(source.relative_to(docs))
        for source in docs.rglob("*.md")
    }
    if linked_pages != expected_pages:
        missing = sorted(expected_pages - linked_pages)
        extra = sorted(linked_pages - expected_pages)
        raise ValueError(f"Index/page mismatch; missing: {missing}; extra: {extra}")

    for relative_path in expected_pages:
        content = (site / relative_path).read_text(encoding="utf-8")
        if not content.strip():
            raise ValueError(f"Generated Markdown is empty: {relative_path}")
        if UNRESOLVED_MACRO.search(content):
            raise ValueError(f"Unresolved AGNTCY macro in: {relative_path}")
        for link in re.findall(r"\]\((https://docs\.agntcy\.org/[^)]+)\)", content):
            path = Path(unquote(urlsplit(link).path.lstrip("/")))
            if not (site / path).is_file():
                raise ValueError(f"Generated Markdown links to a missing page: {link}")

    print(f"Validated llms.txt and {len(expected_pages)} Markdown pages")


if __name__ == "__main__":
    try:
        check(Path(sys.argv[1]), Path(sys.argv[2]))
    except (IndexError, OSError, ValueError) as error:
        sys.exit(f"Agent-readable documentation check failed: {error}")
