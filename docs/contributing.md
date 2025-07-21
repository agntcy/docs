# How to Contribute

Thanks for your interest in contributing to the AGNTCY documentation! Here are a few general guidelines on contributing and
reporting bugs that we ask you to review.

## Reporting Issues

Before reporting a new issue, please ensure that the issue was not already reported or fixed by searching through our
[issues list](https://github.com/agntcy/docs/issues).

When creating a new issue, please be use the **New Issue** template, and provide as much relevant information as
possible.

## Sending Pull Requests

All pull requests should solve an existing issue.

To submit a new pull request, fork the repository. Create a new branch for your feature or fix. Make your
changes then submit a pull request.

## Markdown and Writing Style

Generic markdown intro (if needed):
    - https://commonmark.org/help/tutorial/
    - https://www.markdownguide.org

Don't add hard line breaks at a certain line-length, enable line-wrapping in your editor instead. Otherwise searching for sentences in the code becomes a pain.

### Headings

- Start with level 1 heading (#).
- Use hashmarks for headings.
- Use title case (`# Start Every Word with Uppercase Except for Articles and Coordinating Conjunctions`)
- Keep titles reasonbly short (they show up in the right-hand toc)
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

Include wode within the markdown file by enclosing the code between three backticks. Highlighting is automatic if you specify the type of the code.

### Admonitions

Use blocks starting with `!!! [keyword]` to denote admonitions. The keyword designates the symbol and the color of the element. Use the following keywords:

- Note
- Info
- Warning
- Example

For example, this note:

```
!!! note

    This is a note.
```

Is disoplayed as:

!!! note

    This is a note.

For more information, see the [Material for MkDocs reference](https://squidfunk.github.io/mkdocs-material/reference/).