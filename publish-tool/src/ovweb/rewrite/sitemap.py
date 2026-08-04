"""The two sitemaps a publish produces.

`sitemap.xml` at the root is the one search engines read: `robots.txt` names it, and it is a plain
`urlset` rather than a sitemap index, so it has to list every URL itself.

`<X.Y>/sitemap.xml` is **not** for crawlers. **MkDocs Material's version selector fetches it at
runtime**: when a reader picks another version, `setupVersionSelector` requests `sitemap.xml` under
that version and looks up the page they are on, keeping them there if it is listed and dropping
them on the version root if it is not. So this file is what makes "switch version, keep reading the
same page" work, and two properties of it are load-bearing — see :func:`prune_version_sitemap`.

Nothing in the built site *links* to it; the only reference is that `fetch()`, which no link
checker or grep will find. Treat it as referenced.
"""

from __future__ import annotations

import re

from ..model import SiteLayout

#: One `<url>…</url>` entry, with the whitespace that separates it from the next one. Captured so
#: rejoining the kept entries reproduces the original indentation byte for byte.
URL_ENTRY = re.compile(r"[ \t]*<url>.*?</url>\n?", re.DOTALL)


def promote_root_sitemap(text: str, *, version: str, layout: SiteLayout) -> str:
    """Turn a version's sitemap into the site-root sitemap.

    Versioned pages become `/latest/…` so the sitemap keeps naming one evergreen URL per page
    across releases; the promoted pages and the home page lose the version.
    """
    for page in layout.versioned_pages:
        text = text.replace(f"/{version}/{page}/", f"/latest/{page}/")
    for page in layout.non_versioned_pages:
        text = text.replace(f"/{version}/{page}/", f"/{page}/")
    return text.replace(f"/{version}/</loc>", "/</loc>")


def prune_version_sitemap(text: str, *, version: str, layout: SiteLayout) -> str:
    """Drop the entries for pages that are not served under this version.

    mike builds the whole site into the version folder, so the sitemap it writes lists the
    non-versioned pages at `<X.Y>/pricing/` and friends — URLs that never resolve, because those
    pages are moved to the site root and served exactly once.

    Removing them is not cosmetic: the selector is shown on root pages too, so a reader on
    `/pricing/` picking 3.6 would be sent to `/3.6/pricing/`, a 404. Pruned, they fall back to the
    version root, which is right — that page has no per-version counterpart.

    The entry for the version root itself is **kept**, and must be: the selector takes the longest
    common prefix of every URL in the sitemap and requires that prefix to be an entry before it
    resolves anything. Without it every switch falls back to the version root, which is the whole
    feature off from one missing line.
    """
    dropped = tuple(f"/{version}/{page}/" for page in layout.non_versioned_pages)

    def keep(match: re.Match[str]) -> str:
        entry = match.group(0)
        return "" if any(path in entry for path in dropped) else entry

    return URL_ENTRY.sub(keep, text)
