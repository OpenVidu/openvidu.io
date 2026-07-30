"""Rewrites applied to the pages that are built under a version but served from the root.

Applied only when the publish refreshes the root pages, i.e. when `latest` moves to the version
being published.
"""

from __future__ import annotations

import re

from ..model import KEEPVERSION_SENTINEL, SiteLayout


class RewriteError(Exception):
    """A file cannot be rewritten safely."""


def rewrite_404(text: str, *, version: str, layout: SiteLayout) -> str:
    """Strip the version from the 404 page, then send its versioned links to `latest`.

    The 404 page is served for every unmatched URL at the site root, so nothing in it may
    carry a version — except the links into versioned sections, which must resolve to the
    newest release.
    """
    text = text.replace(f"/{version}/", "/")
    text = text.replace(f'"/{version}"', '"/"')
    for page in layout.versioned_pages:
        text = text.replace(f'href="/{page}/', f'href="/latest/{page}/')
    return text


def rewrite_non_versioned_file(text: str, *, version: str, layout: SiteLayout) -> str:
    """Rewrite one built page that will be promoted to the site root.

    Two steps: relative links into versioned sections become `/latest/…`, then the page's
    own URL loses the version segment.
    """
    text = _point_versioned_links_at_latest(text, layout=layout)
    return _strip_version_from_self_urls(text, version=version, layout=layout)


def _point_versioned_links_at_latest(text: str, *, layout: SiteLayout) -> str:
    """`href="../docs/self-hosting/"` -> `href="/latest/docs/self-hosting/"`."""
    for page in layout.versioned_pages:
        text = re.sub(
            rf'href="(?:\.\./)*{re.escape(page)}/',
            f'href="/latest/{page}/',
            text,
        )
    return text


def _strip_version_from_self_urls(text: str, *, version: str, layout: SiteLayout) -> str:
    """Remove the version segment from a promoted page's own URLs.

    These pages are built under the version folder but served from the root, so the
    self-referencing URLs the theme generates — `<link rel="canonical">`, `og:url`, and the
    JSON-LD `@id`/`url`/`mainEntityOfPage` — must not carry a version.

    Author-written, version-pinned links to versioned pages (`/3.4/docs/…`, used by the
    release-notes links in blog posts) MUST survive. A blanket strip would silently break
    them, so they are shielded behind a sentinel while the version is removed, then
    restored.
    """
    if KEEPVERSION_SENTINEL in text:
        raise RewriteError(
            f"the page already contains {KEEPVERSION_SENTINEL!r}, which is the sentinel used "
            "to shield version-pinned links while the version segment is stripped. Rename it "
            "in the source content."
        )

    for page in layout.versioned_pages:
        text = text.replace(f"/{version}/{page}/", f"/{KEEPVERSION_SENTINEL}/{page}/")
    text = text.replace(f"/{version}/", "/")
    return text.replace(f"/{KEEPVERSION_SENTINEL}/", f"/{version}/")


def rewrite_feed(text: str, *, version: str) -> str:
    """Strip the version from an RSS/JSON feed: they are only served from the root."""
    return text.replace(f"/{version}/", "/")
