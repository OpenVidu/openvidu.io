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


def on_page_content(html, page, config, **kwargs):
    """Use the page's own `description` frontmatter as its llms.txt description.

    `llmstxt` takes the description of each entry from the value written beside the path in
    mkdocs.yml. That meant maintaining the same sentence twice — once as the page's meta
    description, once in the plugin config — and a glob entry could only carry *one*
    description for every page it matched, so the 97 deployment guides all claimed to be the
    same page. Reading it off the page instead makes the frontmatter the single source, and
    lets a glob select pages that each describe themselves.

    This is a hook rather than a change to `plugin.config.sections` in `on_config` because by
    the time pages are rendered the plugin has already expanded the globs, and `page.meta` is
    the description as MkDocs parsed it — including anything the `meta` plugin injected from a
    directory-wide `.meta.yml`.

    Ordering is guaranteed, not lucky: `hooks` is validated after `plugins` and appended to the
    same collection, so a hook's handler for an event always runs after the plugins'.
    """
    plugin = config["plugins"].get("llmstxt")
    if plugin is None:
        return None

    # `_sections` is {section title: {src_uri: description}}, built in the plugin's `on_files`
    # and read in its `on_post_build`. It is private, so assert its shape rather than skipping
    # quietly: a plugin upgrade that renames it must fail the build, not silently publish an
    # llms.txt with no descriptions at all.
    sections = getattr(plugin, "_sections", None)
    if not isinstance(sections, dict):
        raise PluginError(
            "mkdocs-llmstxt no longer exposes `_sections`, so descriptions cannot be taken "
            "from the pages. Update publish-tool/mkdocs_hook.py to the new API."
        )

    listed = [pages for pages in sections.values() if page.file.src_uri in pages]
    if not listed:
        return None

    description = (page.meta or {}).get("description")
    if not description or not str(description).strip():
        raise PluginError(
            f"'{page.file.src_uri}' is listed in the llmstxt sections but has no `description` "
            "in its frontmatter. Every exported page needs one: it is the line that tells an "
            "assistant whether to read the page."
        )
    for pages in listed:
        pages[page.file.src_uri] = " ".join(str(description).split())
    return None
