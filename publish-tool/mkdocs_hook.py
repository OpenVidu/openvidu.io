"""MkDocs hook: exposes ovweb.yaml to the templates, and makes llms.txt and the sitemap true.

Wired up through `hooks:` in mkdocs.yml. Three jobs, all of them about keeping one fact in one
place:

* `on_config` publishes the layout and the redirect patterns on `config.extra.ovweb`, so the
  404 router (docs/overrides/404.html) compiles them from the same configuration ovweb
  publishes with instead of hardcoding a list that has to be kept in sync by hand.
* `on_env` fixes up what a page cannot say about itself: every page's `update_date`, so
  `sitemap.xml` carries a real per-page `<lastmod>` instead of the build date on every URL, and
  the title and description of the blog views the plugin generates, which have no source file to
  carry frontmatter.
* `on_page_content` gives the `llmstxt` plugin each page's own `title` and `description`
  frontmatter, so its llms.txt entry is the name and the sentence written on the page.

The import shim below keeps a plain `mkdocs serve` working in a checkout where the package is
not installed — including inside the Docker images, which mount the repository rather than
installing anything. It does not duplicate any logic: the config loader, the pattern expansion
and the source-date rules have exactly one implementation, in `ovweb`.
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

from ovweb.config import load_site_config  # noqa: E402
from ovweb.gitrepo import Git, GitError  # noqa: E402
from ovweb.redirects import resolve_patterns  # noqa: E402
from ovweb.sources import newest_dates, parse_git_log  # noqa: E402

#: Anything the sitemap dates can be read out of lives under one of these, relative to the
#: repository root: the pages themselves, and the snippets they include.
_DATED_TREES = ("docs", "shared")

#: Descriptions for the blog views the plugin generates, which have no source file to carry
#: frontmatter and so fell back to `site_description` — the same defect as issue 7-b, on the pages
#: 7-b did not enumerate. Written as templates rather than a hard-coded list because a post a week
#: means a new archive month every month and a new category whenever one is introduced.
_VIEW_DESCRIPTIONS = {
    "archive": "Every OpenVidu Blog article published in {name}{page}: {posts}, on {topic}.",
    "category": "Every OpenVidu Blog article filed under {name}{page}: {posts}, on {topic}.",
    #: Page 1 of the blog index has its own frontmatter; only its paginated copies need this.
    "index": "Page {number} of the OpenVidu Blog: more articles on {topic}.",
}
_VIEW_TOPIC = "self-hosted video conferencing and WebRTC engineering"

_log = logging.getLogger(f"mkdocs.hooks.{Path(__file__).stem}")


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


def _source_dates(root: Path) -> dict[str, str] | None:
    """`{repository-relative path: date of its last commit}`, or None when git cannot answer.

    Returning None means "leave MkDocs' build date alone". Three ordinary situations reach it,
    and none of them may fail the build: a shallow clone (`validate-web.yaml` checks out at the
    default depth, where `git log` succeeds but reports the fetched commit for every path — wrong
    data, which is worse than no data), no git binary, and git refusing a repository whose files
    belong to another user, which is what happens inside the Docker images because they mount the
    working copy from the host.

    Logged at INFO on purpose: `mkdocs build --strict` fails on a WARNING, so warning here would
    break every PR's validation build.
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
    classes, for two reasons: an internal import that moves breaks the whole build, and these
    options are what actually decide the paths, so honouring them keeps working if they change.
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
    """Title and description for one generated blog view, derived from what the view *is*.

    The view kind comes from its path, the name from its own heading ("July 2026", "AI") and the
    count from the posts it lists, so a month or a category that does not exist yet is described
    correctly the first time it appears.
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
        metadata["description"] = _VIEW_DESCRIPTIONS[kind].format(
            number=number, topic=_VIEW_TOPIC
        )
    else:
        count = len(getattr(page, "posts", ()))
        metadata["description"] = _VIEW_DESCRIPTIONS[kind].format(
            name=str(page.title),
            page=f", page {number}" if paginated else "",
            posts=f"{count} post" if count == 1 else f"{count} posts",
            topic=_VIEW_TOPIC,
        )
    if paginated:
        # Otherwise `/blog/page/2/` is a byte-identical <title> to `/blog/`: paginated views are
        # copies of the view they page, and the plugin has no option to differentiate them.
        base = (page.meta or {}).get("title") or str(page.title)
        metadata["title"] = f"{base} — page {number}"
    return metadata


def on_env(env, config, files, **kwargs):
    """Fix up what a page cannot say about itself: its `update_date`, and a generated view's meta.

    **`update_date`** is what `sitemap.xml` publishes as `<lastmod>`, and MkDocs sets it to the
    build date for every page — so the sitemap asserted that all 261 URLs changed on every publish.
    A date computed from the page's sources is both true and useful: it lets a crawler tell an
    edited page from an untouched one, and it stops the file churning on publishes that changed
    nothing.

    **A generated blog view** (archive, category, or a paginated copy of any view) has no source
    file, so it carried no frontmatter: all twelve fell back to `site_description`, and
    `/blog/page/2/` was the site's only duplicate `<title>`, byte-identical to `/blog/`. Both get a
    description derived from the view itself, and a paginated copy also gets the page number in its
    title. They still get **no** `<lastmod>`, because there is no source file to date and a
    made-up one would be the original problem in miniature; `update_date = ""` is falsy and the
    sitemap template omits the element, which the spec allows per URL.

    `on_env` is the only hook that can set `update_date`. MkDocs renders the theme's static
    templates — `sitemap.xml` among them — *before* it renders the pages, so `on_page_content` and
    `on_page_context` both run too late. Here every `file.page` already exists, and the work
    happens once rather than once per page.
    """
    # `docs/` and `shared/` are named relative to the project root, which is also the repository
    # root here, and is what pymdownx.snippets resolves an include against.
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
