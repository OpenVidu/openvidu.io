"""Rewrites applied to the pages that are built under a version but served from the root.

Applied only when the publish refreshes the root pages, i.e. when `latest` moves to the version
being published.
"""

from __future__ import annotations

import re

from ..model import KEEPVERSION_SENTINEL, SiteLayout


class RewriteError(Exception):
    """A file cannot be rewritten safely."""


def strip_own_version_segment(text: str, *, version: str, site_url: str) -> str:
    """Drop `/<version>/` from the site's own URLs and leave every other URL alone.

    Own URLs are the absolute ones under `site_url` (canonical, `og:url`, JSON-LD, feed links)
    and root-relative paths. A third-party URL that happens to carry the same segment, such as
    `github.com/OpenVidu/openvidu/tree/3.8/`, is not touched: the segment there is preceded by
    a host or path character, never by a quote, a delimiter or whitespace.
    """
    site = site_url.rstrip("/")
    text = text.replace(f"{site}/{version}/", f"{site}/")
    return re.sub(rf"(?<![\w./:-])/{re.escape(version)}/", "/", text)


def rewrite_404(text: str, *, version: str, layout: SiteLayout) -> str:
    """Strip the version from the 404 page, then send its versioned links to `latest`.

    The 404 page is served for every unmatched URL at the site root, so nothing in it may carry a
    version — except links into versioned sections, which must resolve to the newest release.
    """
    text = strip_own_version_segment(text, version=version, site_url=layout.site_url)
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
    self-referencing URLs the theme generates — `<link rel="canonical">`, `og:url`, and the JSON-LD
    `@id`/`url`/`mainEntityOfPage` — must not carry a version.

    Author-written, version-pinned links to versioned pages (`/3.4/docs/…`, as used by the
    release-notes links in blog posts) must survive, so they are shielded behind a sentinel while
    the version is removed and restored afterwards.
    """
    if KEEPVERSION_SENTINEL in text:
        raise RewriteError(
            f"the page already contains {KEEPVERSION_SENTINEL!r}, which is the sentinel used "
            "to shield version-pinned links while the version segment is stripped. Rename it "
            "in the source content."
        )

    for page in layout.versioned_pages:
        text = text.replace(f"/{version}/{page}/", f"/{KEEPVERSION_SENTINEL}/{page}/")
    text = strip_own_version_segment(text, version=version, site_url=layout.site_url)
    return text.replace(f"/{KEEPVERSION_SENTINEL}/", f"/{version}/")


def rewrite_feed(text: str, *, version: str, layout: SiteLayout) -> str:
    """Strip the version from an RSS/JSON feed: they are only served from the root."""
    return strip_own_version_segment(text, version=version, site_url=layout.site_url)
