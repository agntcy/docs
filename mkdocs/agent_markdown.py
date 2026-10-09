# Copyright AGNTCY Contributors (https://github.com/agntcy)
# SPDX-License-Identifier: CC-BY-4.0

"""Remove presentation-only markup from the generated Markdown pages."""

from urllib.parse import urlsplit, urlunsplit

from bs4 import BeautifulSoup


def preprocess(soup: BeautifulSoup, output: str) -> None:
    """Keep navigation useful after the plugin converts page HTML to Markdown."""
    del output  # The same content rules apply to every page.

    for selector in (
        ".agntcy-hero__partner",
        ".agntcy-connect__links",
        ".grid.cards hr",
    ):
        for element in soup.select(selector):
            element.decompose()

    # Superfences renders Mermaid blocks as <pre class="mermaid"><code>.
    # Markdownify inspects the <pre> class to choose the fence language.
    for block in soup.select("pre.mermaid"):
        block["class"] = [*(block.get("class") or []), "language-mermaid"]

    # The plugin already maps links ending in "/" to index.md. A fragment
    # prevents that conversion, so normalize those links before it runs.
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if not isinstance(href, str):
            continue
        parsed = urlsplit(href)
        if (
            not parsed.scheme
            and not parsed.netloc
            and parsed.path.endswith("/")
            and parsed.fragment
        ):
            anchor["href"] = urlunsplit(
                ("", "", parsed.path + "index.md", parsed.query, parsed.fragment)
            )
