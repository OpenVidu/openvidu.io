"""The pages of a checkout, mapped from the URL each is served at to the file it is built from.

The build knows this mapping and keeps it to itself. The post-processing needs it twice, for what
two MkDocs hooks used to do inside the build before the move to Zensical, which has no hooks:

* the sitemap's `<lastmod>` is the date of a page's sources — the page and the snippets it
  includes, from git (:mod:`ovweb.sources`);
* an `llms.txt` entry's title and description are the page's own frontmatter, where Zensical
  writes the nav label and nothing.

Only the URL scheme the site uses is modelled: directory URLs, and blog posts at
`blog/YYYY/MM/DD/<slug>/` from their `date.created` and `slug`. A draft, a future-dated post or
a page the build left out is simply never looked up.
"""

from __future__ import annotations

import datetime as dt
import posixpath
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import yaml

FRONTMATTER = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*\n", re.DOTALL)

#: Where the blog plugin keeps the posts, relative to docs/, and the URL it gives each.
POST_DIR = "blog/posts"
POST_URL = "blog/{created:%Y/%m/%d}/{slug}/"


@dataclass(frozen=True)
class SourcePage:
    url: str
    """Site-relative, directory form: `""` for the home page, `meet/`, `blog/2026/04/30/x/`."""

    path: str
    """Repository-relative: `docs/meet/index.md`."""

    meta: dict

    def field(self, key: str) -> str | None:
        """A frontmatter value as one line, or None when it is missing or blank."""
        value = self.meta.get(key)
        if value is None or not str(value).strip():
            return None
        return " ".join(str(value).split())


def read_frontmatter(text: str) -> dict:
    """The YAML block a page opens with, or `{}`."""
    match = FRONTMATTER.match(text)
    if match is None:
        return {}
    try:
        loaded = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def page_url(src_uri: str, meta: dict) -> str | None:
    """The URL a source file is served at, or None for a file that is not a page of its own.

    `index.md` collapses to its folder; any other page becomes a folder of its own. A blog post
    is the exception: its URL comes from the post's date and slug, not from its path.
    """
    if not src_uri.endswith(".md"):
        return None
    if src_uri.startswith(f"{POST_DIR}/"):
        return _post_url(src_uri, meta)
    if posixpath.basename(src_uri) == "index.md":
        return src_uri[: -len("index.md")]
    return src_uri[: -len(".md")] + "/"


def _post_url(src_uri: str, meta: dict) -> str | None:
    created = meta.get("date")
    if isinstance(created, dict):
        created = created.get("created")
    if isinstance(created, dt.datetime):
        created = created.date()
    if not isinstance(created, dt.date):
        return None
    slug = meta.get("slug") or posixpath.basename(src_uri)[: -len(".md")]
    return POST_URL.format(created=created, slug=str(slug).strip().lower())


def scan_pages(root: Path, *, docs_dir: str = "docs") -> dict[str, SourcePage]:
    """Every page under `docs/`, keyed by the URL it is served at."""
    pages: dict[str, SourcePage] = {}
    base = root / docs_dir
    for path in sorted(base.rglob("*.md")):
        src_uri = path.relative_to(base).as_posix()
        meta = read_frontmatter(path.read_text(encoding="utf-8"))
        url = page_url(src_uri, meta)
        if url is not None:
            pages[url] = SourcePage(url=url, path=f"{docs_dir}/{src_uri}", meta=meta)
    return pages


def page_dates(
    pages: dict[str, SourcePage], *, dates: dict[str, str], read: Callable[[str], str | None]
) -> dict[str, str]:
    """`{url: YYYY-MM-DD}` for every page git can date — see :func:`ovweb.sources.newest_dates`."""
    from .sources import newest_dates

    by_path = {page.path: url for url, page in pages.items()}
    resolved = newest_dates(by_path, dates=dates, read=read)
    return {by_path[path]: date for path, date in resolved.items()}
