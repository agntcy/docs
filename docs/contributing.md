# How to Contribute

Thanks for your interest in contributing to the AGNTCY documentation! Here are a few general guidelines on contributing and
reporting bugs that we ask you to review.

## Reporting Issues

Before reporting a new issue, please ensure that the issue was not already reported or fixed by searching through our
[issues list](https://github.com/agntcy/docs/issues).

When creating a new issue, please be use the **New Issue** template, and provide as much relevant information as
possible.

## Sending Pull Requests

All pull requests should solve an existing issue. Make sure to add the issue number to the pull request, linking them together.

To submit a new pull request, fork the repository. Create a new branch for your feature or fix. Make your changes then submit a pull request.

## Moving or Renaming Documentation Files

If you move or rename a documentation file, **you must add a redirect** to preserve existing links. This ensures that bookmarks, external links, and search engine results continue to work.

To add a redirect:

1. Open `mkdocs/mkdocs.yml`
1. Add an entry to the `redirect_maps` under the `redirects` plugin:

    ```yaml
    plugins:
      - redirects:
          redirect_maps:
            'old/path/to/file.md': 'new/path/to/file.md'
    ```

1. Test the redirect locally by running `task build` or `task run` and verifying the old URL redirects to the new location

!!! warning

    Failing to add redirects will result in broken links and a poor user experience. Always add redirects when moving content.

## Markdown and Writing Style

Generic markdown intro (if needed):
    - [commonmark.org/help/tutorial](https://commonmark.org/help/tutorial/)
    - [www.markdownguide.org](https://www.markdownguide.org)

Don't add hard line breaks at a certain line-length, enable line-wrapping in your editor instead. Otherwise searching for sentences in the code becomes a pain.

### Headings

- Start with level 1 heading (#).
- Use hashmarks for headings.
- Use title case (`# Start Every Word with Uppercase Except for Articles and Coordinating Conjunctions`)
- Keep titles reasonably short (they show up in the right-hand toc)
- Do not skip heading levels.

### Lists

- Use dash (`-`) for bulleted lists
- Use only `1.` for ordered lists, they are automatically numbered in the output
- Indent additional stuff that belongs to a list element by 4 spaces, for example:

    ```md
    1. Step one

        More text for the same item

        ![Screenshot alt text](screenshot.png)

    1. Next step

        - Nested list

            More text for the nested element
    ```

### Links

- When linking to an external URL, or to a static HTML file within the project, use normal markdown linking `[text](url)`
- When linking to a file within the docs, use `[link text](/docs/path/to/file.md)`.
- Use project-absolute paths in the links/refs: start with a /, then the path relative to the `content` directory, for example: `/docs/getting-started/example.md` (easier to update when a file is moved, and easier to recognize where it is pointing).

### Images

Use plain markdown syntax: `![alt-text](image.png)`. Use it for full-screen screenshots, so the labels remain legible.

You can use HTML if needed, but that's usually needed only if you want to adjust the size of the image (typically only needed for not-fullscreen screenshots, like modal dialogue windows that look too big full-size).

Place the image files in the `/docs/assets` folder.

### Code Samples

Include code within the markdown file by enclosing the code between three backticks. Highlighting is automatic if you specify the type of the code.

For example, this code:

````md
```python
print("Hello, World!")
```
````

Is displayed as:

```python
print("Hello, World!")
```

### Admonitions

Use blocks starting with `!!! [keyword]` to denote admonitions. The keyword designates the symbol and the color of the element. Use the following keywords:

- Note
- Info
- Warning
- Example

For example, this note:

```md
!!! note

    This is a note.
```

Is displayed as:

!!! note

    This is a note.

For more information, see the [Material for MkDocs reference](https://squidfunk.github.io/mkdocs-material/reference/).
