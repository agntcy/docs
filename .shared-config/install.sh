#!/usr/bin/env bash
# Copy AGNTCY theme assets into docs/ (MkDocs serves extra_css and theme static files from docs_dir).
# Optional: ./install.sh --with-mike-macros  → copies mike_version.py, mike_versions.ini, main.py into mkdocs/
set -euo pipefail

SHARED_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SHARED_ROOT/.." && pwd)"
DOCS="$REPO_ROOT/docs"
MKDOCS="$REPO_ROOT/mkdocs"

mkdir -p "$DOCS/stylesheets" "$DOCS/assets/agntcy/img"
cp -f "$SHARED_ROOT/stylesheets/custom.css" "$DOCS/stylesheets/agntcy-docs.css"
cp -f "$SHARED_ROOT/assets/favicon.ico" "$DOCS/assets/agntcy/"
cp -f "$SHARED_ROOT/assets/img/"*.svg "$DOCS/assets/agntcy/img/"
if [[ -f "$SHARED_ROOT/assets/logo.svg" ]]; then
  cp -f "$SHARED_ROOT/assets/logo.svg" "$DOCS/assets/agntcy/"
fi

echo "AGNTCY docs theme installed under $DOCS (stylesheets/agntcy-docs.css, assets/agntcy/)."

if [[ "${1:-}" == "--with-mike-macros" ]]; then
  mkdir -p "$MKDOCS"
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
