"""The two sitemaps a publish produces.

`sitemap.xml` at the root is the one search engines read: `robots.txt` names it, and it is a plain
`urlset` rather than a sitemap index, so it has to list every URL itself.

`<X.Y>/sitemap.xml` is **not** for crawlers. **The theme's version selector fetches it at
runtime**: when a reader picks another version, `setupVersionSelector` requests `sitemap.xml` under
that version and looks up the page they are on, keeping them there if it is listed and dropping
them on the version root if it is not. So this file is what makes "switch version, keep reading the
same page" work, and two properties of it are load-bearing — see :func:`prune_version_sitemap`.

Nothing in the built site *links* to it; the only reference is that `fetch()`, which no link
checker or grep will find. Treat it as referenced.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping

from ..model import SiteLayout

#: One `<url>…</url>` entry, with the whitespace that separates it from the next one. Captured so
#: rejoining the kept entries reproduces the original indentation byte for byte.
URL_ENTRY = re.compile(r"[ \t]*<url>.*?</url>\n?", re.DOTALL)

LOC = re.compile(r"<loc>([^<]+)</loc>")
LASTMOD = re.compile(r"[ \t]*<lastmod>[^<]*</lastmod>\n?")


def date_sitemap(text: str, *, version: str, base_url: str, dates: Mapping[str, str]) -> str:
    """Give every entry whose page has a dated source a `<lastmod>`.

    Zensical's sitemap carries no `<lastmod>` at all (MkDocs' hook used to set one per page from
    git). `dates` maps a page's site-relative URL (`meet/`, `blog/2026/04/30/x/`, `""` for the
    home page) to its `YYYY-MM-DD`; an entry with no date — a generated blog view, a page git has
    never seen — is left without one, which the sitemap spec allows per URL, rather than given the
    build date, which would claim every page changed on every publish.

    Runs on the version's own sitemap before it is promoted or pruned, so both copies carry the
    dates. An existing `<lastmod>` is replaced, never duplicated.
    """
    prefix = f"{base_url}/{version}/"

    def dated(match: re.Match[str]) -> str:
        entry = match.group(0)
        found = LOC.search(entry)
        if found is None or not found.group(1).startswith(prefix):
            return entry
        date = dates.get(found.group(1)[len(prefix) :])
        entry = LASTMOD.sub("", entry)
        if date is None:
            return entry
        indent = " " * (found.start() - entry.rfind("\n", 0, found.start()) - 1)
        return entry.replace(
            found.group(0), f"{found.group(0)}\n{indent}<lastmod>{date}</lastmod>", 1
        )

    return URL_ENTRY.sub(dated, text)


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


def stub_loc(base_url: str, stub_path: str) -> str:
    """The sitemap `<loc>` for a generated redirect: its URL, directory-form for an index.html."""
    path = stub_path[: -len("index.html")] if stub_path.endswith("index.html") else stub_path
    return f"{base_url}/{path}"


#: Marks an entry this tool added, so a later sync can drop it once its stub is gone. Inside
#: the `<url>` block, where both the selector's DOM queries and crawlers ignore it.
STUB_MARK = "<!-- ovweb:stub -->"


def sync_version_sitemap(text: str, *, base_url: str, stubs: Iterable[str]) -> str:
    """List the version's generated redirects so the version selector can resolve moved pages.

    The selector keeps a reader on the page they were reading only if the rebased URL is an
    entry in this file, so a moved page resolves only through its listed stub — unlisted, every
    switch onto it drops the reader on the version root.

    Reconciles rather than appends: every marked entry, and every entry naming a current stub,
    is dropped first and rewritten from `stubs` — the tree-relative `.html` paths of the
    generated redirects. Stub entries carry no `<lastmod>`: a redirect has no modification date
    of its own.
    """
    locs = {stub_loc(base_url, stub) for stub in stubs}

    def keep(match: re.Match[str]) -> str:
        entry = match.group(0)
        if STUB_MARK in entry:
            return ""
        found = LOC.search(entry)
        return "" if found and found.group(1) in locs else entry

    kept = URL_ENTRY.sub(keep, text)
    entries = "".join(
        f"    <url>\n         {STUB_MARK}\n         <loc>{loc}</loc>\n    </url>\n"
        for loc in sorted(locs)
    )
    return kept.replace("</urlset>", f"{entries}</urlset>", 1)
