"""Python-Markdown extensions for the Zensical build, listed under `markdown_extensions` in
mkdocs.yml.

Zensical has no `hooks:`, so what the site needs beyond Python-Markdown's own output is done
here, inside the Markdown conversion that Zensical still delegates to Python:

* `root_links` — root-absolute `.md` links resolved against `docs/`, which MkDocs 1.6 did with
  `validation.links.absolute_links: relative_to_docs`.
* `fence_title` — the linked filename above a code block, restored from the escape Pygments
  2.20+ applies to the `title=` option.

`zensical build` imports them by name, so the `ovweb` package must be installed in the
environment running the build (`pip install ./publish-tool`); the Docker image installs it.
"""
