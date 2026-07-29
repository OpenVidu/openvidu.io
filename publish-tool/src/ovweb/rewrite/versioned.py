"""Rewrites applied to every file under `<X.Y>/docs/` and `<X.Y>/meet/`.

Applied on every publish, whether or not the root pages are refreshed.
"""

from __future__ import annotations

import re

from ..model import SiteLayout


def rewrite_versioned_file(text: str, *, version: str, layout: SiteLayout) -> str:
    """Rewrite one built file that lives inside a version's versioned-page folder.

    No step can undo or trigger another, but the order is fixed so that a step added later
    inherits the same guarantee.
    """
    text = _pin_asset_references(text, version=version, layout=layout)
    text = _absolutise_non_versioned_links(text, layout=layout)
    text = _absolutise_root_file_links(text, layout=layout)
    text = _absolutise_home_links(text)
    text = _absolutise_storage_scope(text)
    return _point_self_urls_at_latest(text, version=version, layout=layout)


def _pin_asset_references(text: str, *, version: str, layout: SiteLayout) -> str:
    """`src="/assets/x.png"` -> `src="/3.8/assets/x.png"`.

    The root `/assets/` folder always holds the newest publish's assets, so a versioned page has
    to reference its own copy: its assets may change or disappear in a later release.

    Matches `src="` / `href="` anywhere, so `data-src="/assets/…"` is pinned too, which is what
    you want — a `data-src` consumed by a script resolves against the same root.
    """
    for directory in layout.pinned_assets:
        text = re.sub(
            rf'(src|href)="/{re.escape(directory)}/',
            rf'\1="/{version}/{directory}/',
            text,
        )
    return text


def _absolutise_non_versioned_links(text: str, *, layout: SiteLayout) -> str:
    """`href="../../pricing/"` -> `href="/pricing/"`.

    A versioned page sits at an arbitrary depth inside the version folder, but the pages it
    links to are served once from the site root, so the relative path MkDocs generated is
    wrong by exactly the version segment.
    """
    for page in layout.non_versioned_pages:
        text = re.sub(
            rf'href="(?:\.\./)*{re.escape(page)}/',
            f'href="/{page}/',
            text,
        )
    return text


def _absolutise_root_file_links(text: str, *, layout: SiteLayout) -> str:
    """`href="../../feed_rss_created.xml"` -> `href="/feed_rss_created.xml"`.

    Same reasoning as the folders above, for the individual files promoted to the root. The
    theme emits two `<link rel="alternate">` RSS references on every page, relative to the
    version folder — where the feeds do not survive the publish, because they are moved to the
    root (or deleted, when an older version is republished). Left alone, every versioned page
    advertises two URLs that 404.

    `index.html` and `index.md` are excluded: a link to the home page is a link to `/`, which
    :func:`_absolutise_home_links` already handles.
    """
    for name in layout.root_files:
        if name.startswith("index."):
            continue
        text = re.sub(
            rf'href="(?:\.\./)*{re.escape(name)}"',
            f'href="/{name}"',
            text,
        )
    return text


def _absolutise_home_links(text: str) -> str:
    """`href="../.."` -> `href="/"` — the home page is served from the root."""
    return re.sub(r'href="(?:\.\./)*\.\."', 'href="/"', text)


def _absolutise_storage_scope(text: str) -> str:
    """`__md_scope = new URL("../..",location)` -> `new URL("/",location)`.

    Material keys its `localStorage`/`sessionStorage` entries by this scope's path — cookie
    consent among them. Left relative, every version folder would be its own scope and the
    consent prompt would reappear on each one.

    Note this is *not* Material's `base`, which stays relative in the runtime config and is what
    makes a versioned page load its own search index and assets.
    """
    return re.sub(r'URL\("(?:\.\./)*\.\.",location\)', 'URL("/",location)', text)


def _point_self_urls_at_latest(text: str, *, version: str, layout: SiteLayout) -> str:
    """`canonical`/`og:url` of `/3.8/docs/x/` -> `/latest/docs/x/`.

    Ranking signals then consolidate on one evergreen URL per page instead of churning every
    release. These two tags are the only ones carrying `page.canonical_url` for a versioned page:
    the JSON-LD emitted for the two documentation index pages already hardcodes `/latest/` (see
    docs/overrides/partials/json-ld.html), and no other versioned page emits JSON-LD at all.

    Only these tags are touched. The `/3.8/assets/` pins applied above, and any author-pinned
    `/X.Y/…` link elsewhere on the page, are deliberately left alone.
    """
    base = re.escape(layout.base_url)
    pinned = re.escape(version)
    text = re.sub(rf'(rel="canonical" href="{base})/{pinned}/', r"\1/latest/", text)
    return re.sub(rf'(property="og:url" content="{base})/{pinned}/', r"\1/latest/", text)
