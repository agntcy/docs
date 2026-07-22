# Build the docs

## Local dev

```sh
uv run mkdocs serve
```

## Build

```sh
uv run mkdocs build
```

## Variable tags (mkdocs-macros)

Shared values are defined under `extra` in `mkdocs.yml` and rendered with custom
`[[ ... ]]` tags (instead of Jinja2's default `{{ ... }}`) so they do not clash
with React/JSX-style braces in markdown pages.

Example in a page:

```markdown
See the [Agent Directory Service]([[ agntcy.dir_url ]]) docs.
```

Available variables:

| Variable | Value |
| --- | --- |
| `agntcy.dir_url` | Agent Directory Service docs base URL |
| `agntcy.slim_url` | SLIM docs base URL |

Built-in objects such as `config`, `page`, and `navigation` use the same `[[ ... ]]` syntax, e.g. `[[ config.site_name ]]`.

For page-local values, use block tags:

```markdown
[[% set product = "SLIM" %]]
Learn more about [[ product ]].
```
