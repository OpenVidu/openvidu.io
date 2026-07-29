"""Splice the *content* of one built releases page into another version's releases page.

The releases pages (OpenVidu Meet and OpenVidu Platform) list the notes of every release, so
every documentation version must serve the same, most-recent list. What must NOT travel
across versions is the rest of the page: header, tabs, navigation, footer, canonical URL,
asset URLs and Material's runtime config all belong to the version folder they live in.
Copying the whole built HTML would make an old version's releases page navigate the visitor
straight out of that version.

So only two regions are spliced:

1. The release notes body: ``<article class="md-content__inner md-typeset">…</article>``.
   One occurrence per page.
2. The table of contents:
   ``<nav class="md-nav md-nav--secondary" aria-label="Table of contents">…</nav>``.
   Two byte-identical occurrences per page — the right-hand secondary sidebar, and the copy
   Material embeds under the active primary-navigation item for the mobile drawer. Both are
   replaced, or the sidebar would keep listing the destination version's own shorter list.

The spliced fragments need no link rewriting: every link inside a release-notes section is
authored as an absolute, version-pinned URL (a documented convention of these two pages) and
the table of contents holds only ``#anchor`` links. Both are verified before splicing, so a
page that breaks the convention is reported instead of being published with links resolving
against the wrong version folder.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

ARTICLE_MARKER = '<article class="md-content__inner md-typeset">'
TOC_MARKER = '<nav class="md-nav md-nav--secondary" aria-label="Table of contents">'

# Any href/src that is not an absolute URL (or a bare "#anchor") resolves against the folder
# the page lives in, so it would point at the wrong version once the fragment is copied.
RELOCATABLE_LINK = re.compile(r'(?:href|src)="(?!https?://|mailto:|#)([^"]*)"')


class RegionError(Exception):
    """A page does not expose the expected regions, or holds a relocatable link."""


class SourceRegionError(RegionError):
    """The problem is in the source page.

    Fatal: the source is the freshly built newest page, so a failure here means the
    conventions above no longer hold and every copy would be wrong.
    """


class DestinationRegionError(RegionError):
    """The problem is in the destination page.

    Recoverable: an old version folder may have been built by a theme version that named
    these regions differently. The caller warns and leaves that page as built rather than
    aborting a publish that is already half done.
    """


@dataclass(frozen=True)
class SpliceResult:
    html: str
    article_bytes: int
    tocs_replaced: int


def splice_releases(source_html: str, destination_html: str) -> SpliceResult:
    """Return `destination_html` with the two regions taken from `source_html`."""
    try:
        article = _extract(source_html, ARTICLE_MARKER)
        _check_links(article, "the release notes body")
        toc = _extract(source_html, TOC_MARKER)
        _check_links(toc, "the table of contents")
    except RegionError as error:
        raise SourceRegionError(str(error)) from error

    try:
        start, end = find_region(destination_html, ARTICLE_MARKER)
    except RegionError as error:
        raise DestinationRegionError(str(error)) from error
    result = destination_html[:start] + article + destination_html[end:]

    # Every occurrence of the table of contents, wherever the theme placed it.
    replaced = 0
    offset = 0
    while True:
        try:
            start, end = find_region(result, TOC_MARKER, offset)
        except RegionError:
            break
        result = result[:start] + toc + result[end:]
        offset = start + len(toc)
        replaced += 1

    if replaced == 0:
        raise DestinationRegionError(f"marker not found: {TOC_MARKER}")

    return SpliceResult(html=result, article_bytes=len(article), tocs_replaced=replaced)


def find_region(html: str, marker: str, start: int = 0) -> tuple[int, int]:
    """Return `(start, end)` of the element opened by `marker`, closing tag included.

    The end tag is found by counting nested tags of the same name: the table of contents
    nests a ``<nav>`` per heading level, so a plain search for the first ``</nav>`` would cut
    it short.
    """
    open_at = html.find(marker, start)
    if open_at == -1:
        raise RegionError(f"marker not found: {marker}")

    tag_match = re.match(r"<(\w+)", marker)
    if tag_match is None:  # pragma: no cover - the markers are module constants
        raise RegionError(f"marker does not open a tag: {marker}")
    tag = tag_match.group(1)

    depth = 1
    position = open_at + len(marker)
    for match in re.finditer(rf"<(/?){tag}\b", html[position:]):
        depth += -1 if match.group(1) else 1
        if depth == 0:
            close_at = html.index(">", position + match.start()) + 1
            return open_at, close_at

    raise RegionError(f"unbalanced <{tag}> opened by: {marker}")


def _extract(html: str, marker: str) -> str:
    start, end = find_region(html, marker)
    return html[start:end]


def _check_links(fragment: str, what: str) -> None:
    relocatable = sorted({match.group(1) for match in RELOCATABLE_LINK.finditer(fragment)})
    if relocatable:
        raise RegionError(
            f"{what} holds {len(relocatable)} link(s) relative to the version folder, which "
            f"would break once copied into another version: {relocatable[:5]}. Links in the "
            "releases pages must be absolute and version-pinned."
        )
