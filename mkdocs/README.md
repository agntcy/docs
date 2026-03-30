# Build the docs

# Local dev

```sh
uv run mkdocs serve
```

## Build

```sh
uv run mkdocs build
```

## Macros

[mkdocs-macros-plugin](https://mkdocs-macros-plugin.readthedocs.io/) expands **`[[[ ... ]]]`** on the **whole page source before** Markdown runs, so substitutions work **inside fenced code blocks** as well as in prose:

````markdown
```bash
curl "[[[ var.docs_url ]]]"
```
````

To show the literal characters `[[[ var.org ]]]` in the docs (e.g. in a macro how-to), wrap that part in a Jinja raw block (block delimiters stay the default `{%` / `%}`):

````markdown
{% raw %}
```text
[[[ var.org ]]]
```
{% endraw %}
````
