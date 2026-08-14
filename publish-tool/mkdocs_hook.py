"""MkDocs hook, wired up through `hooks:` in mkdocs.yml. Two jobs:

* `on_env` sets every page's `update_date`, so `sitemap.xml` carries a real per-page `<lastmod>`
  rather than the build date on every URL, and gives the blog views the plugin generates a title
  and description, which they have no source file to carry.
* `on_page_content` gives the `llmstxt` plugin each page's own `title` and `description`
  frontmatter, so its llms.txt entry is the name and the sentence written on the page.

The import shim keeps a plain `mkdocs serve` working in a checkout where the package is not
installed, including inside the Docker images, which mount the repository rather than installing
anything. No logic is duplicated: the source-date rules have one implementation, in `ovweb`.
"""

from __future__ import annotations

import logging
import re
import sys
from pathlib import Path

from mkdocs.exceptions import PluginError

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from ovweb.gitrepo import Git, GitError  # noqa: E402
from ovweb.sources import newest_dates, parse_git_log  # noqa: E402

#: Everything the sitemap dates are read out of, relative to the repository root: the pages
#: themselves, and the snippets they include.
_DATED_TREES = ("docs", "shared")

#: Descriptions for the blog views the plugin generates, which have no source file to carry
#: frontmatter and would otherwise fall back to `site_description`. Templates rather than a
#: hard-coded list, because a post a week means a new archive month every month.
_VIEW_DESCRIPTIONS = {
    "archive": "Every OpenVidu Blog article published in {name}{page}: {posts}, on {topic}.",
    "category": "Every OpenVidu Blog article filed under {name}{page}: {posts}, on {topic}.",
    #: Page 1 of the blog index has its own frontmatter; only its paginated copies need this.
    "index": "Page {number} of the OpenVidu Blog: more articles on {topic}.",
}
_VIEW_TOPIC = "self-hosted video conferencing and WebRTC engineering"

_log = logging.getLogger(f"mkdocs.hooks.{Path(__file__).stem}")


def _source_dates(root: Path) -> dict[str, str] | None:
    """`{repository-relative path: date of its last commit}`, or None when git cannot answer.

    None means "leave MkDocs' build date alone". Three ordinary situations reach it, none of which
    may fail the build: a shallow clone (`validate-web.yaml` checks out at the default depth, where
    `git log` succeeds but reports the fetched commit for every path), no git binary, and git
    refusing a repository whose files belong to another user, which is what the Docker images do
    when they mount the working copy from the host.

    Logged at INFO: `mkdocs build --strict` fails on a WARNING, which would break every PR.
    """
    git = Git(root)
    try:
        if git.is_shallow():
            _log.info("Shallow clone: sitemap <lastmod> falls back to the build date.")
            return None
        return parse_git_log(git.log_dates_for(*_DATED_TREES))
    except (GitError, OSError) as error:
        _log.info(
            "Could not read dates from git (%s): <lastmod> falls back to the build date.", error
        )
        return None


def _blog_url_shapes(config) -> dict[str, str] | None:
    """How the blog plugin is configured to build its view URLs, or None if it is not enabled.

    Read from the plugin's **public** config rather than by importing its `Archive`/`Category`
    classes: these options are what decide the paths, so honouring them keeps working if the
    formats change, and no internal import can move underneath the build.
    """
    for plugin in config.get("plugins", {}).values():
        options = getattr(plugin, "config", None)
        if options is not None and hasattr(options, "archive_url_format"):
            return {
                "blog": options["blog_dir"],
                "archive": options["archive_url_format"],
                "category": options["categories_url_format"],
                "pagination": options["pagination_url_format"],
            }
    return None


def _literal_prefix(url_format: str) -> str:
    """The fixed part of a URL format, up to its first placeholder.

    `archive/{date}` -> `archive/`, which is enough to classify a view by its path.
    """
    return url_format.split("{", 1)[0]


def _view_metadata(page, src_uri: str, shapes: dict[str, str]) -> dict[str, str]:
    """Title and description for one generated blog view, derived from what the view is.

    The kind comes from its path, the name from its own heading ("July 2026", "AI") and the count
    from the posts it lists, so a month or category that does not exist yet is described correctly
    the first time it appears. Returns `{}` for a view shape this hook does not recognise.
    """
    page_pattern = re.compile(
        re.escape(shapes["pagination"]).replace(r"\{page\}", r"(\d+)") + r"(?:/index)?\.md$"
    )
    paginated = page_pattern.search(src_uri)
    number = paginated.group(1) if paginated else ""

    within = src_uri.removeprefix(f"{shapes['blog']}/")
    if within.startswith(_literal_prefix(shapes["archive"])):
        kind = "archive"
    elif within.startswith(_literal_prefix(shapes["category"])):
        kind = "category"
    elif paginated:
        kind = "index"  # a paginated copy of the blog index itself
    else:
        return {}  # an author profile, or a view shape this hook has not been taught

    metadata = {}
    if kind == "index":
        metadata["description"] = _VIEW_DESCRIPTIONS[kind].format(number=number, topic=_VIEW_TOPIC)
    else:
        count = len(getattr(page, "posts", ()))
        metadata["description"] = _VIEW_DESCRIPTIONS[kind].format(
            name=str(page.title),
            page=f", page {number}" if paginated else "",
            posts=f"{count} post" if count == 1 else f"{count} posts",
            topic=_VIEW_TOPIC,
        )
    if paginated:
        # A paginated view is a copy of the view it pages and the plugin has no option to
        # differentiate them, so without this `/blog/page/2/` repeats `/blog/`'s title exactly.
        base = (page.meta or {}).get("title") or str(page.title)
        metadata["title"] = f"{base} — page {number}"
    return metadata


def on_env(env, config, files, **kwargs):
    """Set each page's `update_date`, and describe the blog views the plugin generates.

    **`update_date`** is what `sitemap.xml` publishes as `<lastmod>`. MkDocs sets it to the build
    date for every page, which asserts that the whole site changed on every publish; a date
    computed from the page's sources lets a crawler tell an edited page from an untouched one.

    **A generated blog view** — archive, category, or a paginated copy of either — has no source
    file and so no frontmatter, leaving it with `site_description` and, for a paginated copy, a
    `<title>` byte-identical to the view it pages. Both are derived from the view itself. They get
    **no** `<lastmod>` at all, because there is no source file to date: `update_date = ""` is falsy,
    so the sitemap template omits the element, which the spec allows per URL.

    `on_env` is the only hook that can set `update_date`: MkDocs renders the theme's static
    templates — `sitemap.xml` among them — *before* the pages, so `on_page_content` and
    `on_page_context` both run too late. Here every `file.page` exists and the work happens once.
    """
    # `_DATED_TREES` is relative to the project root, which is also the repository root here and
    # what pymdownx.snippets resolves an include against.
    docs_dir = Path(config["docs_dir"]).resolve()
    root = docs_dir.parent
    shapes = _blog_url_shapes(config)

    pages, generated, described = {}, 0, 0
    for file in files.documentation_pages():
        if file.page is None:
            continue
        if file.generated_by is not None:
            file.page.update_date = ""
            generated += 1
            if shapes is not None:
                metadata = _view_metadata(file.page, file.src_uri, shapes)
                file.page.meta.update(metadata)
                described += bool(metadata)
            continue
        pages[f"{docs_dir.name}/{file.src_uri}"] = file.page

    _log.info("Described %d of %d generated blog views from the view itself.", described, generated)

    dates = _source_dates(root)
    if dates is None:
        return env

    def read(path: str) -> str | None:
        candidate = root / path
        try:
            return candidate.read_text(encoding="utf8") if candidate.is_file() else None
        except OSError:
            return None

    resolved = newest_dates(pages, dates=dates, read=read)
    for path, date in resolved.items():
        pages[path].update_date = date

    _log.info(
        "sitemap <lastmod>: %d pages dated from git, %d left on the build date, "
        "%d generated pages with no date.",
        len(resolved),
        len(pages) - len(resolved),
        generated,
    )
    return env


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


_GLIGHTBOX_JS = re.compile(r'<script src="([^"]*glightbox\.min\.js)"></script>')
_GLIGHTBOX_INIT = '<script id="init-glightbox">'


def on_post_page(output, page, config, **kwargs):
    """Move glightbox.min.js out of <head> to just before its init script.

    The glightbox plugin injects its ~57 KB library as a synchronous head script on every page
    with lightbox content, blocking first paint. The library is only needed by the
    `#init-glightbox` script the plugin appends at the end of <body>, so it loads there instead.
    Runs after the plugin's own `on_post_page` (hooks run after plugins for the same event).
    """
    match = _GLIGHTBOX_JS.search(output)
    if match is None:
        return None
    init_pos = output.find(_GLIGHTBOX_INIT)
    if init_pos == -1:
        return None
    output = output[: match.start()] + output[match.end() :]
    init_pos = output.find(_GLIGHTBOX_INIT)
    return output[:init_pos] + match.group(0) + output[init_pos:]


def on_page_content(html, page, config, **kwargs):
    """Use the page's own `title` and `description` frontmatter for its llms.txt entry.

    Both halves stop llms.txt taking its text from somewhere other than the page:

    * **The description** would be the value written beside the path in mkdocs.yml, maintaining the
      same sentence twice — and a glob entry can only carry *one* description for every page it
      matches, so every page a glob covers would claim to be the same page.
    * **The title** would be `page.title`, which MkDocs resolves as the *nav label* first, falling
      back to the frontmatter `title` and then the first H1. Most of this site's nav entries are
      labelled, so entries rendered as `[Install]`, `[Overview]` or `[Releases]` — clear beside
      their parent in a sidebar, useless in a flat list.

    A hook rather than a change to `plugin.config.sections` in `on_config`, because by the time
    pages are rendered the plugin has expanded its globs, and `page.meta` is the frontmatter as
    MkDocs parsed it, including anything the `meta` plugin injected from a directory `.meta.yml`.

    Ordering is guaranteed: `hooks` is validated after `plugins` and appended to the same
    collection, so a hook's handler for an event always runs after the plugins'. That is what lets
    this overwrite `_md_pages`, which the plugin fills in during its own `on_page_content`.
    """
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
