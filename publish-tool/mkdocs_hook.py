"""MkDocs hook: exposes ovweb.yaml to the templates, and feeds llms.txt its descriptions.

Wired up through `hooks:` in mkdocs.yml. Two jobs, both of them about keeping one fact in one
place:

* `on_config` publishes the layout and the redirect patterns on `config.extra.ovweb`, so the
  404 router (docs/overrides/404.html) compiles them from the same configuration ovweb
  publishes with instead of hardcoding a list that has to be kept in sync by hand.
* `on_page_content` gives the `llmstxt` plugin each page's own `description` frontmatter, so
  the entry a page gets in llms.txt is the description already written on the page.

The import shim below keeps a plain `mkdocs serve` working in a checkout where the package is
not installed — including inside the Docker images, which mount the repository rather than
installing anything. It does not duplicate any logic: the config loader and the pattern
expansion have exactly one implementation, in `ovweb`.
"""

from __future__ import annotations

import sys
from pathlib import Path

from mkdocs.exceptions import PluginError

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from ovweb.config import load_site_config  # noqa: E402
from ovweb.redirects import resolve_patterns  # noqa: E402


def on_config(config, **kwargs):
    """Publish the layout and the 404 redirect patterns on `config.extra.ovweb`.

    ovweb sets `$OVWEB_SITE_CONFIG` when it invokes mike, so a publish build and the
    post-processing that follows it always read the same file — which matters for a past
    version, whose branch carries its own stale copy of ovweb.yaml.
    """
    site_config = load_site_config()
    config["extra"]["ovweb"] = {
        "versioned_pages": list(site_config.layout.versioned_pages),
        "non_versioned_pages": list(site_config.layout.non_versioned_pages),
        "redirect_patterns": [
            {"id": pattern.id, "match": pattern.match, "to": pattern.to}
            for pattern in resolve_patterns(site_config)
        ],
    }
    return config


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


def on_page_content(html, page, config, **kwargs):
    """Use the page's own `title` and `description` frontmatter for its llms.txt entry.

    Both halves fix the same class of problem — llms.txt taking its text from somewhere other
    than the page:

    * **The description** was the value written beside the path in mkdocs.yml, so the same
      sentence was maintained twice, and a glob entry could only carry *one* description for
      every page it matched — the 97 deployment guides all claimed to be the same page.
    * **The title** is `page.title`, which MkDocs resolves as *the nav label first*, falling back
      to the frontmatter `title` and then the first H1. Since 183 of this site's nav entries are
      labelled (`- Install: docs/.../install.md`), 180 entries were rendering as `[Install]`,
      `[Overview]` or `[Releases]` — labels that are perfectly clear next to their parent in a
      sidebar and say nothing at all in a flat list. The 66 that already looked right were the
      section-index and non-nav pages, where `page.title` had nothing to fall back *from*.

    This is a hook rather than a change to `plugin.config.sections` in `on_config` because by
    the time pages are rendered the plugin has already expanded the globs, and `page.meta` is
    the frontmatter as MkDocs parsed it — including anything the `meta` plugin injected from a
    directory-wide `.meta.yml`.

    Ordering is guaranteed, not lucky: `hooks` is validated after `plugins` and appended to the
    same collection, so a hook's handler for an event always runs after the plugins'. That is
    what lets this overwrite `_md_pages`, which the plugin fills in during *its* own
    `on_page_content`.
    """
    plugin = config["plugins"].get("llmstxt")
    if plugin is None:
        return None

    # Both are private, and both are read in the plugin's `on_post_build`:
    #   `_sections`  {section title: {src_uri: description}}, built in its `on_files`
    #   `_md_pages`  {src_uri: _MDPageInfo(title, path_md, md_url, content)}, built in its
    #                `on_page_content`
    # Assert their shape rather than skipping quietly: a plugin upgrade that renames either must
    # fail the build, not silently publish an llms.txt full of nav labels and no descriptions.
    sections = getattr(plugin, "_sections", None)
    exported = getattr(plugin, "_md_pages", None)
    if not isinstance(sections, dict) or not isinstance(exported, dict):
        raise PluginError(
            "mkdocs-llmstxt no longer exposes `_sections` and `_md_pages`, so llms.txt entries "
            "cannot be taken from the pages. Update publish-tool/mkdocs_hook.py to the new API."
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
            "would keep the nav label. Update publish-tool/mkdocs_hook.py to the new API."
        )
    exported[src_uri] = info._replace(title=title)
    return None
