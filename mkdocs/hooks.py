"""MkDocs hooks for documentation rendering and agent artifact validation."""

import ssl
from pathlib import Path

import certifi
from mkdocs.exceptions import PluginError
from mkdocs.plugins import event_priority

from check_agent_docs import check, expected_markdown_path

_STOCK_FENCED_CODE = frozenset(("fenced_code", "markdown.extensions.fenced_code"))
_navigated_pages: set[Path] = set()


def on_config(config, **kwargs):
    """Drop stock fenced_code; pymdownx.superfences replaces it (see pymdown-extensions docs)."""
    extensions = config.get("markdown_extensions")
    if not extensions:
        return config

    filtered = []
    for item in extensions:
        if isinstance(item, str):
            if item in _STOCK_FENCED_CODE:
                continue
        elif isinstance(item, dict) and len(item) == 1:
            name = next(iter(item.keys()))
            if name in _STOCK_FENCED_CODE:
                continue
        filtered.append(item)

    config["markdown_extensions"] = filtered
    return config


def on_nav(nav, **kwargs):
    """Record the pages shown in the resolved MkDocs navigation."""
    global _navigated_pages
    _navigated_pages = {
        expected_markdown_path(Path(page.file.src_uri)) for page in nav.pages
    }
    return nav


@event_priority(-100)
def on_post_build(config, **kwargs):
    """Check agent-readable files after the llmstxt plugin writes them."""
    try:
        check(Path(config.site_dir), _navigated_pages)
    except (OSError, ValueError) as error:
        raise PluginError(
            f"Agent-readable documentation check failed: {error}"
        ) from error


# Monkey patch urllib to use certifi's certificate bundle
def on_startup(**kwargs):
    """Configure SSL context to use certifi certificates."""
    import urllib.request

    # Create SSL context with certifi's certificate bundle
    ssl_context = ssl.create_default_context(cafile=certifi.where())

    # Set the default opener to use this context
    https_handler = urllib.request.HTTPSHandler(context=ssl_context)
    opener = urllib.request.build_opener(https_handler)
    urllib.request.install_opener(opener)
