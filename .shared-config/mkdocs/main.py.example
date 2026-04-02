"""MkDocs macros: shared variables (from mkdocs.yml `extra`) and reusable helpers."""

from __future__ import annotations

import html
import os


def define_env(env):
    """Register variables and macros for mkdocs-macros-plugin."""

    env.variables["docs_build_version"] = os.environ.get("VERSION", "dev")

    @env.macro
    def var_tag(label: str, hint: str = "") -> str:
        """Inline tag for env vars, flags, or keys. Use [[[ var_tag('MY_ENV') ]]] in Markdown."""
        safe_label = html.escape(str(label), quote=True)
        safe_hint = html.escape(str(hint), quote=True) if hint else ""
        title = f' title="{safe_hint}"' if safe_hint else ""
        return (
            f'<span class="doc-var-tag"{title}>'
            f"<code>{safe_label}</code></span>"
        )
