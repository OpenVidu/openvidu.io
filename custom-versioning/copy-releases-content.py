#!/usr/bin/env python3
"""Copy the *content* of a built releases page into another version's built releases page.

The releases pages (OpenVidu Meet and OpenVidu Platform) list the notes of every release, so
every documentation version must serve the same, most-recent list. What must NOT travel across
versions is the rest of the page: header, tabs, navigation, footer, canonical URL, asset URLs
and Material's runtime config all belong to the version folder they live in. Copying the whole
built HTML (what this repository used to do) made an old version's releases page navigate the
visitor straight out of that version.

So only two regions are spliced from SRC into DST:

  1. The release notes body:  <article class="md-content__inner md-typeset"> ... </article>
     One occurrence per page.
  2. The table of contents:   <nav class="md-nav md-nav--secondary" aria-label="Table of contents"> ... </nav>
     TWO byte-identical occurrences per page: the right-hand secondary sidebar, and the copy
     Material embeds under the active item of the primary navigation (used by the mobile
     drawer). Both are replaced, or the sidebar would keep listing the destination version's
     own, shorter list of releases.

Nothing else is touched, and the spliced fragments need no link rewriting: every link inside a
release-notes section is authored as an absolute, version-pinned URL (a documented convention of
these two pages, see the repository README), and the table of contents only holds "#anchor"
links. Both are verified before splicing, so a future page that breaks the convention is
reported instead of being published with links that resolve against the wrong version folder.

Usage:
    copy-releases-content.py SRC_HTML DST_HTML

Exit codes:
    0  DST was rewritten.
    1  SRC could not be read, a region is missing from it, or it holds a relocatable link.
       Fatal for the caller: SRC is the freshly built latest page, so a failure here means the
       assumptions above no longer hold and every copy would be wrong.
    2  DST could not be read or a region is missing from it. The caller warns and skips this
       page: an old version folder may have been built by a different theme version.
"""

import re
import sys

ARTICLE_MARKER = '<article class="md-content__inner md-typeset">'
TOC_MARKER = '<nav class="md-nav md-nav--secondary" aria-label="Table of contents">'

# Any href/src that is not an absolute URL (or a bare "#anchor") resolves against the folder the
# page lives in, so it would point at the wrong version once the fragment is copied elsewhere.
RELOCATABLE_LINK = re.compile(r'(?:href|src)="(?!https?://|mailto:|#)([^"]*)"')


class RegionError(Exception):
    pass


def find_region(html, marker, start=0):
    """Return (start, end) of the element opened by `marker`, closing tag included.

    The end tag is found by counting nested tags of the same name: the table of contents nests
    a <nav> per heading level, so a plain search for the first "</nav>" would cut it short.
    """
    open_at = html.find(marker, start)
    if open_at == -1:
        raise RegionError(f"marker not found: {marker}")

    tag = re.match(r"<(\w+)", marker).group(1)
    depth = 1
    pos = open_at + len(marker)
    for match in re.finditer(rf"<(/?){tag}\b", html[pos:]):
        depth += -1 if match.group(1) else 1
        if depth == 0:
            close_at = html.index(">", pos + match.start()) + 1
            return open_at, close_at

    raise RegionError(f"unbalanced <{tag}> opened by: {marker}")


def check_links(fragment, what):
    relocatable = sorted({m.group(1) for m in RELOCATABLE_LINK.finditer(fragment)})
    if relocatable:
        raise RegionError(
            f"{what} holds {len(relocatable)} link(s) relative to the version folder, which "
            f"would break once copied into another version: {relocatable[:5]}. Links in the "
            f"releases pages must be absolute and version-pinned."
        )


def read(path, exit_code):
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read()
    except OSError as error:
        if exit_code == 1:
            sys.exit(f"error: cannot read {path}: {error}")
        print(f"warning: cannot read {path}: {error}", file=sys.stderr)
        sys.exit(2)


def main(argv):
    if len(argv) != 3:
        sys.exit(f"usage: {argv[0]} SRC_HTML DST_HTML")

    src_path, dst_path = argv[1], argv[2]
    src = read(src_path, 1)
    dst = read(dst_path, 2)

    # Extract from the source, failing hard: this is the freshly built latest page.
    try:
        article_start, article_end = find_region(src, ARTICLE_MARKER)
        article = src[article_start:article_end]
        check_links(article, "the release notes body")

        toc_start, toc_end = find_region(src, TOC_MARKER)
        toc = src[toc_start:toc_end]
        check_links(toc, "the table of contents")
    except RegionError as error:
        sys.exit(f"error: in source {src_path}: {error}")

    # Splice into the destination, warning and skipping: an old version folder may have been
    # built by a theme version that named these regions differently.
    try:
        dst_article_start, dst_article_end = find_region(dst, ARTICLE_MARKER)
        result = dst[:dst_article_start] + article + dst[dst_article_end:]

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
            raise RegionError(f"marker not found: {TOC_MARKER}")
    except RegionError as error:
        print(f"warning: in destination {dst_path}: {error}", file=sys.stderr)
        return 2

    with open(dst_path, "w", encoding="utf-8") as handle:
        handle.write(result)

    print(
        f"Spliced release notes ({len(article)} bytes) and {replaced} table(s) of contents "
        f"from '{src_path}' into '{dst_path}'"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
