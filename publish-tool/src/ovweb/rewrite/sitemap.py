"""The two sitemaps a publish produces, and why both are needed.

`sitemap.xml` at the root is the one search engines read: `robots.txt` names it, and it is a
plain `urlset` rather than a sitemap index, so it has to list every URL itself.

`<X.Y>/sitemap.xml` is **not** for crawlers — nothing links to it and `robots.txt` does not name
it — but it is not dead either. **MkDocs Material's version selector fetches it at runtime.**
When a reader picks another version, `setupVersionSelector` requests `sitemap.xml` under the
selected version and looks for the page they are currently on; if it finds it they stay on that
page in the new version, and if the fetch fails or the page is absent they are dropped on the
version root instead. So this file is what makes "switch version, keep reading the same page"
work, and two properties of it are load-bearing — see :func:`prune_version_sitemap`.

This was learned the hard way: the file was deleted as unreferenced, because no *link* to it
exists anywhere in the built site. The reference is a `fetch()` in the theme's JavaScript.
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
    non-versioned pages at `<X.Y>/pricing/` and friends. The publish moves those pages to the
    site root, where they are served exactly once, so those URLs never resolve.

    Removing them is not cosmetic. The version selector resolves the reader's current path
    against the selected version's sitemap, and a reader on `/pricing/` — a root page, still
    showing the selector — would otherwise be sent to `/3.6/pricing/`, a 404. Pruning makes the
    selector fall back to the version root for them, which is correct: that page has no
    per-version counterpart to switch to.

    The entry for the version root itself is **kept**, and must be: the selector takes the
    longest common prefix of every URL in the sitemap and requires that prefix to itself be an
    entry before it will resolve anything. With only page entries left the prefix is still
    `https://openvidu.io/<X.Y>/`, which would no longer be in the file, and every switch would
    fall back to the version root — the whole feature off, from one missing line.
    """
    dropped = tuple(f"/{version}/{page}/" for page in layout.non_versioned_pages)

    def keep(match: re.Match[str]) -> str:
        entry = match.group(0)
        return "" if any(path in entry for path in dropped) else entry

    return URL_ENTRY.sub(keep, text)
