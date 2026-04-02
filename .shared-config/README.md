# AGNTCY shared docs theme

Drop this `.shared-config` directory at the root of a repository to reuse the AGNTCY MkDocs Material look (CSS, logos, favicon, header logo partials).

## Layout

| Path | Purpose |
|------|---------|
| `stylesheets/custom.css` | Theme variables and layout tweaks (source) |
| `assets/` | `favicon.ico`, `img/logo-light.svg`, `img/logo-dark.svg`, optional `logo.svg` |
| `mkdocs/overrides/` | Material `partials` (light/dark logo swap, footer copyright block) |
| `mkdocs/mkdocs.template.yml` | Full starter `mkdocs.yml` (theme, mike, macros, redirects, nav, API docs, Swagger, includes, analytics) |
| `mkdocs/hooks.py` | SSL via `certifi` for `include-markdown` (referenced from the template; keep path in sync) |
| `mkdocs/mike_version.py` | Resolves version label from `mike_versions.ini` (for Task / CI) |
| `mkdocs/mike_versions.ini` | `[versions]` `local` / `release` labels for mike |
| `mkdocs/main.py.example` | Copy to `mkdocs/main.py` for `var_tag()` and `docs_build_version` |
| `requirements-agntcy-docs-theme.txt` | All template plugins (Material, mike, macros, redirects, awesome-pages, mkdocstrings, swagger UI, `include-markdown`, `certifi`, …) |
| `requirements-agntcy-docs-lint.txt` | `codespell` and `pymarkdown` for lint tasks |
| `Taskfile.yml` | Local build, serve (`run`), and lint tasks ([Task](https://taskfile.dev/) ≥ 3.35) |
| `codespellrc` | Spelling check config (used by `lint:spelling`) |
| `pymarkdown.yaml` | Markdown style config (used by `lint:markdown`) |
| `lychee.toml` | Link checker config (used by `lint:links`) |
| `install.sh` | Copies CSS and assets into `docs/`; optional `--with-mike-macros` installs mike + `main.py` |
| `github/workflows/` | CI, docs release (mike + tag), links, PR link checks — see below |

## GitHub Actions

Copy the YAML files from `github/workflows/` into `.github/workflows/` at the repository root (keep filenames). They assume `.shared-config/` exists beside `docs/` and `mkdocs/`.

| Workflow | Role |
|----------|------|
| `reusable-docs.yml` | Build docs (`workflow_call` + `workflow_dispatch`); used by `cicd.yml`. |
| `cicd.yml` | On PR/push (paths: `docs/**`, `mkdocs/**`, `.shared-config/**`) and on `v*.*.*` tags, runs the reusable build. |
| `docs-release.yml` | Manual Docs release: build → mike deploy to gh-pages → git tag `v{version}` → optional GitHub Release. Set `[versions] release` in `mkdocs/mike_versions.ini` first. |
| `links.yml` | Scheduled / manual lychee on `.build/site`, config `.shared-config/lychee.toml`. |
| `pr-links.yml` | PRs to main/master: lychee on HTML for changed `docs/**/*.md` only. Add a `--remap` in the workflow if you need production URLs rewritten to the local build (see comment in the file). |

Each workflow runs `./.shared-config/install.sh` (and `--with-mike-macros`) before `task -t .shared-config/Taskfile.yml build`, then `uv sync` in `mkdocs/` when `pyproject.toml` or `uv.lock` exists, otherwise `python3 -m pip install -r .shared-config/requirements-agntcy-docs-theme.txt`.

Enable GitHub Pages from the gh-pages branch if you use mike. Grant Actions appropriate permissions (the release workflow uses `contents: write`).

## What the template enables

Aligned with `agntcy/docs` `mkdocs.yml`:

- `hooks` — `../.shared-config/mkdocs/hooks.py` (paths are relative to the directory that contains `mkdocs/mkdocs.yml`); uses `certifi` for HTTPS when using `include-markdown`.
- `extra.version` / `mike` — versioned docs and Material’s version menu.
- `extra.var` + `macros` — `[[[ var.docs_url ]]]`, etc., with `[[[` / `]]]` delimiters; `main.py` from `main.py.example` (or `./install.sh --with-mike-macros`).
- `redirects` — same `redirect_maps` as the main docs site (trim or replace for a new project).
- `awesome-pages` — `.index` navigation files.
- `mkdocstrings` — Python API docs (install the packages you document in the same environment; `griffe-pydantic` is configured).
- `swagger-ui-tag` and `include-markdown` — OpenAPI embeds and Markdown includes.
- `extra.analytics` / `extra.consent` — Google Analytics + cookie consent; replace `G-XXXXXXXXXX` with your Measurement ID (or remove those blocks).

Copy `mike_version.py`, `mike_versions.ini`, and `main.py` into `mkdocs/` when using mike/macros:

```bash
./.shared-config/install.sh --with-mike-macros
```

Use `task -t .shared-config/Taskfile.yml mike:deploy-local`, `mike:deploy`, and `mike:serve` (requires mike via `uv run` or on `PATH`).

**Important:** Copy `mkdocs.template.yml` into `mkdocs/mkdocs.yml` (do not point `-f` at the template inside `.shared-config/`, or `docs_dir`, `hooks`, and `theme.custom_dir` paths will resolve incorrectly).

## Build and lint with Task

From the repository root (expects `docs/` and `mkdocs/mkdocs.yml`):

```bash
task -t .shared-config/Taskfile.yml build   # → .build/site
task -t .shared-config/Taskfile.yml run     # mkdocs serve
task -t .shared-config/Taskfile.yml lint    # spelling + markdown + links
task -t .shared-config/Taskfile.yml lint:fix  # auto-fix spelling + markdown
task -t .shared-config/Taskfile.yml mike:deploy-local  # local gh-pages + mike (after install.sh --with-mike-macros)
task -t .shared-config/Taskfile.yml mike:serve
```

Or include the file from your main `Taskfile.yml`:

```yaml
includes:
  docs: .shared-config/Taskfile.yml
```

Then run namespaced tasks such as `task docs:build`.

**Tools:** `lint:links` needs [lychee](https://github.com/lycheeverse/lychee) on your `PATH`. Spelling and Markdown lint use either `uv run` (if `mkdocs/uv.lock` or `mkdocs/pyproject.toml` exists) or global `codespell` / `pymarkdown` after:

```bash
pip install -r .shared-config/requirements-agntcy-docs-lint.txt
```

Tune `codespellrc`, `pymarkdown.yaml`, and `lychee.toml` in `.shared-config/` for your project (for example, extend `ignore-words-list` or `exclude` URL patterns).

## Why `install.sh`?

MkDocs loads `extra_css` and theme static paths relative to `docs_dir`. Files under `.shared-config/` are not inside `docs/` unless you copy or symlink them. Running `install.sh` places:

- `docs/stylesheets/agntcy-docs.css`
- `docs/assets/agntcy/favicon.ico`
- `docs/assets/agntcy/img/logo-*.svg`

Re-run after updating `.shared-config` from upstream.

## Quick start

1. Add or create a `docs/` tree with at least `docs/index.md`.
2. From the repository root:

   ```bash
   chmod +x .shared-config/install.sh
   ./.shared-config/install.sh
   ./.shared-config/install.sh --with-mike-macros   # optional: mike + macros files in mkdocs/
   ```

3. Copy `.shared-config/mkdocs/mkdocs.template.yml` to `mkdocs/mkdocs.yml` and set `site_name`, `site_url`, `repo_*`, `edit_uri`, `extra.var`, `extra.analytics.property`, and edit `plugins.redirects` as needed. Remove plugins you do not use (for example `mkdocstrings` if you have no API pages).

4. Install deps and serve:

   ```bash
   cd mkdocs
   pip install -r ../.shared-config/requirements-agntcy-docs-theme.txt
   mkdocs serve
   ```

If `mkdocs.yml` lives somewhere else, adjust `docs_dir`, `theme.custom_dir`, and paths in the template so `custom_dir` still points at `.shared-config/mkdocs/overrides` relative to that file.

## Merging into an existing site

- Set `theme.custom_dir` to `../.shared-config/mkdocs/overrides` (from `mkdocs/mkdocs.yml`).
- Add `stylesheets/agntcy-docs.css` to `extra_css` (after running `install.sh`).
- Set `theme.favicon`, `theme.logo_light`, and `theme.logo_dark` to the `assets/agntcy/...` paths from the template, or merge the `theme.palette` / `theme.features` blocks as needed.
