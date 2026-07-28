"""Rewrites applied to every file under `<X.Y>/docs/` and `<X.Y>/meet/`.

Port of `changeVersionedPagesLinks` from push-new-version.sh. Applied on every publish,
whether or not the root pages are refreshed.
"""

from __future__ import annotations

import re

from ..model import SiteLayout


def rewrite_versioned_file(text: str, *, version: str, layout: SiteLayout) -> str:
    """Rewrite one built file that lives inside a version's versioned-page folder.

    The five steps run in the order the shell applied them. None of them can undo or
    trigger another, but the order is preserved so that a future step added here inherits
    the same guarantee.
    """
    text = _pin_asset_references(text, version=version, layout=layout)
    text = _absolutise_non_versioned_links(text, layout=layout)
    text = _absolutise_home_links(text)
    text = _absolutise_cookie_consent_base_url(text)
    return _point_self_urls_at_latest(text, version=version, layout=layout)


def _pin_asset_references(text: str, *, version: str, layout: SiteLayout) -> str:
    """`src="/assets/x.png"` -> `src="/3.8/assets/x.png"`.

    Matches `src="` / `href="` anywhere, so `data-src="/assets/…"` is pinned too — the
    shell behaved the same way, and it is what you want: a `data-src` consumed by a script
    resolves against the same root.
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


def _absolutise_home_links(text: str) -> str:
    """`href="../.."` -> `href="/"` — the home page is served from the root."""
    return re.sub(r'href="(?:\.\./)*\.\."', 'href="/"', text)


def _absolutise_cookie_consent_base_url(text: str) -> str:
    """`URL("../..",location)` -> `URL("/",location)`.

    Material derives the cookie-consent scope from this base URL. Left relative, every
    version folder would be its own scope and the consent prompt would reappear on each.
    """
    return re.sub(r'URL\("(?:\.\./)*\.\.",location\)', 'URL("/",location)', text)


def _point_self_urls_at_latest(text: str, *, version: str, layout: SiteLayout) -> str:
    """`canonical`/`og:url` of `/3.8/docs/x/` -> `/latest/docs/x/`.

    Ranking signals then consolidate on one evergreen URL per page instead of churning
    every release. These two tags are the only ones carrying `page.canonical_url` for a
    versioned page: the JSON-LD emitted for the two documentation index pages already
    hardcodes `/latest/` (docs/overrides/partials/json-ld.html), and no other versioned page
    emits JSON-LD at all.

    Only these tags are touched. The `/3.8/assets/` pins applied above, and any
    author-pinned `/X.Y/…` link elsewhere on the page, are deliberately left alone.
    """
    base = re.escape(layout.base_url)
    pinned = re.escape(version)
    text = re.sub(
        rf'(rel="canonical" href="{base})/{pinned}/',
        r"\1/latest/",
        text,
    )
    return re.sub(
        rf'(property="og:url" content="{base})/{pinned}/',
        r"\1/latest/",
        text,
    )
