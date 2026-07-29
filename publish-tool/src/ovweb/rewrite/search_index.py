"""Rewrites applied to `search/search_index.json`.

Two indexes exist and they must say different things, because a page loads the index that sits
beside it. Material records the folder to resolve against in its own runtime config
(`"base": "../.."`), which the publish leaves alone, so a page under `/3.4/docs/` fetches
`/3.4/search/search_index.json` while a page served from the site root fetches
`/search/search_index.json`.

:func:`rewrite_search_index` prepares a version's own index, where a hit on versioned
documentation has to stay **inside that version** — searching the 3.4 docs must return 3.4
results. :func:`promote_search_index` then adjusts the copy that becomes the root index, where a
hit on versioned documentation should point at `/latest/`, for the same reason every other
root-to-versioned reference does: the root pages are evergreen, `/latest/…` is the canonical URL
of the page being linked, and a pinned version would send a visitor searching from `/pricing/`
into documentation that goes stale at the next release.
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

    Only `"location":` values are touched. A blanket version replace would also rewrite the
    indexed page *text*, which legitimately contains version numbers in command samples and
    release notes.
    """
    for page in layout.versioned_pages:
        text = text.replace(f'"location":"/{version}/{page}/', f'"location":"/latest/{page}/')
    return text
