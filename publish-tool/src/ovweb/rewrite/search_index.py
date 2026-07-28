"""Rewrites applied to a version's `search/search_index.json`.

Port of `changeSearchIndexLinks` from push-new-version.sh. Applied on every publish.
"""

from __future__ import annotations

from ..model import SiteLayout


def rewrite_search_index(text: str, *, version: str, layout: SiteLayout) -> str:
    """Make every search hit an absolute URL.

    Material writes locations relative to the folder the index lives in. That index is
    copied to the site root, where a relative location would resolve against the root
    rather than the version folder.

    Note the asymmetry with the page links, and keep it: a search hit on a versioned page
    points at the **explicit version** (`/3.8/docs/…`), not at `/latest/`. The root index is
    the newest publish's, so its versioned hits do name a version — which is deliberate:
    a hit describes the page that was indexed, and `latest` will move under it at the next
    release.
    """
    for page in layout.versioned_pages:
        text = text.replace(f'"location":"{page}/', f'"location":"/{version}/{page}/')
    for page in layout.non_versioned_pages:
        text = text.replace(f'"location":"{page}/', f'"location":"/{page}/')
    return text.replace('"location":""', '"location":"/"')
