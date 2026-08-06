"""Rewrites applied to `search/search_index.json`.

Two indexes exist and they say different things, because a page loads the index beside it: Material
records the folder to resolve against in its runtime config (`"base": "../.."`), which the publish
leaves relative, so a page under `/3.4/docs/` fetches `/3.4/search/search_index.json` while a root
page fetches `/search/search_index.json`.

:func:`rewrite_search_index` prepares a version's own index, where a hit on versioned documentation
stays **inside that version** — searching the 3.4 docs must return 3.4 results.
:func:`promote_search_index` then adjusts the copy that becomes the root index, where such a hit
points at `/latest/`, like every other root-to-versioned reference: the root pages are evergreen,
and a pinned version goes stale at the next release.
"""

from __future__ import annotations

from ..model import SiteLayout


def rewrite_search_index(text: str, *, version: str, layout: SiteLayout) -> str:
    """Make every location in a version's own index absolute.

    Material writes locations relative to the folder the index lives in, which stops resolving
    once the pages those locations describe are moved to the site root.
    """
    for page in layout.versioned_pages:
        text = text.replace(f'"location":"{page}/', f'"location":"/{version}/{page}/')
    for page in layout.non_versioned_pages:
        text = text.replace(f'"location":"{page}/', f'"location":"/{page}/')
    return text.replace('"location":""', '"location":"/"')


def promote_search_index(text: str, *, version: str, layout: SiteLayout) -> str:
    """Point the root index's versioned hits at `/latest/`.

    Only `"location":` values are touched: a blanket version replace would also rewrite the indexed
    page *text*, which legitimately holds version numbers in command samples and release notes.
    """
    for page in layout.versioned_pages:
        text = text.replace(f'"location":"/{version}/{page}/', f'"location":"/latest/{page}/')
    return text
