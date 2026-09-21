"""MkDocs hook that gives each llms.txt entry the page's own `title` and `description`.

Neither half of an entry may come from anywhere but the page. The `mkdocs-llmstxt` plugin would
take the description from the value written beside the path in mkdocs.yml — the same sentence
maintained twice, and a glob entry can only carry *one* description for every page it matches —
and the link text from `page.title`, which MkDocs resolves as the *nav label* first: clear beside
its parent in a sidebar, useless in a flat list. A listed page missing either fails the build.

Both values are private plugin attributes, read in its `on_post_build`: `_sections`
({section title: {src_uri: description}}, built in its `on_files`) and `_md_pages`
({src_uri: _MDPageInfo(title, path_md, md_url, content)}, built in its `on_page_content`). A
hook's handler runs after the plugins' for the same event, which is what lets this overwrite what
the plugin recorded. Their shape is asserted rather than skipped quietly, so a plugin upgrade that
renames either fails the build instead of publishing an llms.txt of nav labels and no descriptions.

This file is copied verbatim onto the `X.Y` version branches from 3.4 and into
livekit-tutorials-docs (`hooks/`): MkDocs loads a hook by path from the checked-out branch. Edit it
here, then re-copy it; `ovweb doctor` reports a copy that differs.
"""

from mkdocs.exceptions import PluginError


def on_page_content(html, page, config, **kwargs):
    plugin = config["plugins"].get("llmstxt")
    if plugin is None:
        return None

    # Both are private, and both are read in the plugin's `on_post_build`:
    #   `_sections`  {section title: {src_uri: description}}, built in its `on_files`
    #   `_md_pages`  {src_uri: _MDPageInfo(title, path_md, md_url, content)}, built in its
    #                `on_page_content`
    # Their shape is asserted rather than skipped quietly, so a plugin upgrade that renames either
    # fails the build instead of publishing an llms.txt full of nav labels and no descriptions.
    sections = getattr(plugin, "_sections", None)
    exported = getattr(plugin, "_md_pages", None)
    if not isinstance(sections, dict) or not isinstance(exported, dict):
        raise PluginError(
            "mkdocs-llmstxt no longer exposes `_sections` and `_md_pages`, so llms.txt entries "
            "cannot be taken from the pages. Update llmstxt_entries_hook.py to the new API."
        )

    src_uri = page.file.src_uri
    listed = [pages for pages in sections.values() if src_uri in pages]
    if not listed:
        return None

    meta = page.meta or {}
    title = _required(meta, "title", src_uri)
    description = _required(meta, "description", src_uri)

    for pages in listed:
        pages[src_uri] = description

    info = exported.get(src_uri)
    if info is None:  # pragma: no cover - the plugin records every page it selected
        raise PluginError(
            f"mkdocs-llmstxt selected '{src_uri}' but did not record it, so its llms.txt title "
            "would keep the nav label. Update llmstxt_entries_hook.py to the new API."
        )
    exported[src_uri] = info._replace(title=title)
    return None


def _one_line(value) -> str:
    """A frontmatter value as a single line, so it cannot break llms.txt's one-entry-per-line."""
    return " ".join(str(value).split())


def _required(meta, key: str, src_uri: str) -> str:
    value = meta.get(key)
    if not value or not str(value).strip():
        raise PluginError(
            f"'{src_uri}' is listed in the llmstxt sections but has no `{key}` in its "
            f"frontmatter. Every exported page needs a `title` and a `description`: together "
            f"they are the line that tells an assistant whether to read the page."
        )
    return _one_line(value)
