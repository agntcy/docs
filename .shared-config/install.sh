#!/usr/bin/env bash
# Copy AGNTCY theme assets into docs/ (MkDocs serves extra_css and theme static files from docs_dir).
# Bootstraps mkdocs/mkdocs.yml from mkdocs.starter.yml and placeholder docs when those files are missing.
# Optional: ./install.sh --with-mike-macros  → copies mike_version.py, mike_versions.ini, main.py into mkdocs/
set -euo pipefail

SHARED_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SHARED_ROOT/.." && pwd)"
DOCS="$REPO_ROOT/docs"
MKDOCS="$REPO_ROOT/mkdocs"

mkdir -p "$DOCS/stylesheets" "$DOCS/assets/agntcy/img" "$MKDOCS"
cp -f "$SHARED_ROOT/stylesheets/custom.css" "$DOCS/stylesheets/agntcy-docs.css"
cp -f "$SHARED_ROOT/assets/favicon.ico" "$DOCS/assets/agntcy/"
cp -f "$SHARED_ROOT/assets/img/"*.svg "$DOCS/assets/agntcy/img/"
if [[ -f "$SHARED_ROOT/assets/logo.svg" ]]; then
  cp -f "$SHARED_ROOT/assets/logo.svg" "$DOCS/assets/agntcy/"
fi

echo "AGNTCY docs theme installed under $DOCS (stylesheets/agntcy-docs.css, assets/agntcy/)."

created_mkdocs=0
if [[ ! -f "$MKDOCS/mkdocs.yml" ]]; then
  cp -f "$SHARED_ROOT/mkdocs/mkdocs.starter.yml" "$MKDOCS/mkdocs.yml"
  created_mkdocs=1
  echo "Created $MKDOCS/mkdocs.yml from mkdocs.starter.yml (replace placeholders; use mkdocs.template.yml for full agntcy/docs parity)."
else
  echo "Leaving existing $MKDOCS/mkdocs.yml unchanged."
fi

# Placeholder pages only when bootstrapping a new mkdocs.yml (avoids adding stubs to mature docs trees).
if [[ "$created_mkdocs" -eq 1 ]]; then
  if [[ ! -f "$DOCS/index.md" ]]; then
    cp -f "$SHARED_ROOT/docs-stub/index.md" "$DOCS/index.md"
    echo "Created $DOCS/index.md (placeholder)."
  else
    echo "Leaving existing $DOCS/index.md unchanged."
  fi
  if [[ ! -f "$DOCS/getting-started.md" ]]; then
    cp -f "$SHARED_ROOT/docs-stub/getting-started.md" "$DOCS/getting-started.md"
    echo "Created $DOCS/getting-started.md (placeholder)."
  else
    echo "Leaving existing $DOCS/getting-started.md unchanged."
  fi
fi

if [[ "${1:-}" == "--with-mike-macros" ]]; then
  cp -f "$SHARED_ROOT/mkdocs/mike_version.py" "$MKDOCS/"
  cp -f "$SHARED_ROOT/mkdocs/mike_versions.ini" "$MKDOCS/"
  if [[ ! -f "$MKDOCS/main.py" ]]; then
    cp -f "$SHARED_ROOT/mkdocs/main.py.example" "$MKDOCS/main.py"
    echo "Created $MKDOCS/main.py from main.py.example"
  else
    echo "Leaving existing $MKDOCS/main.py unchanged."
  fi
  echo "Mike + macros helpers installed under $MKDOCS (mike_version.py, mike_versions.ini, main.py)."
fi
