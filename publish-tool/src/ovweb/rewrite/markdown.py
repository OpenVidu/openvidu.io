"""Rewrites for the Markdown exports published alongside the HTML.

The `llmstxt` plugin writes an `index.md` next to every `index.html` and indexes them all in
`llms.txt`. They need their own rules because the plugin makes every link **absolute**, resolved
against the build's `site_url` — which mike makes versioned. So every internal link comes out
pinned to the version that produced it, and the HTML patterns cannot reach any of them: those
match `href="…"` and `src="…"`, which Markdown link syntax does not have.

The rules mirror the HTML ones, so a page and its export send a reader to the same place, and
which one applies depends on where the export is served from:

* :func:`rewrite_versioned_markdown` — the export of a versioned page. Links into the same version
  stay pinned; anything served from the root loses the version.
* :func:`rewrite_promoted_markdown` — the export of a page promoted to the root, and `llms.txt`.
  Neither has a version of its own, so links into versioned documentation go to `/latest/`.

Two more rules apply to every export wherever it is served from, because they are about the *form*
of a link rather than its target: :func:`absolutise_root_relative_targets` and
:func:`repair_export_links`.
"""

from __future__ import annotations

import re

from ..model import SiteLayout

#: Markdown link or image target that is root-relative. `](//host/…)` is excluded: a
#: protocol-relative URL already names a host.
ROOT_RELATIVE_TARGET = re.compile(r"\]\(/(?!/)")

#: A Markdown link or image target naming a page's Markdown export on this site, with any
#: fragment. The plugin only ever writes `<directory>/index.md`, so that is the only shape to look
#: for. Anchored to the site's own base URL, so an external `.md` link is not a candidate.
_EXPORT_TARGET = r"\]\({base}(?P<page>(?:[^)\s#]*/)?)index\.md(?P<frag>#[^)\s]*)?\)"

#: The suffix of the exports. Used by the pipeline to pick between these rules and the HTML ones.
SUFFIX = ".md"


def rewrite_versioned_markdown(text: str, *, version: str, layout: SiteLayout) -> str:
    """Rewrite the Markdown export of a page inside a version's versioned-page folder.

    Mirrors :func:`ovweb.rewrite.versioned.rewrite_versioned_file`: links that stay inside the
    version folder are left pinned to it, and links to anything served from the site root lose
    the version segment they were built with.
    """
    text = _drop_version_from_page_urls(text, version=version, pages=layout.non_versioned_pages)
    text = _drop_version_from_file_urls(text, version=version, files=layout.root_files)
    return absolutise_root_relative_targets(text, layout=layout)


def rewrite_promoted_markdown(text: str, *, version: str, layout: SiteLayout) -> str:
    """Rewrite the Markdown export of a page promoted to the site root.

    Mirrors :func:`ovweb.rewrite.nonversioned.rewrite_non_versioned_file`: the page is served from
    the root, so it carries no version of its own and its links into versioned documentation point
    at `/latest/`.

    Unlike the HTML, this does *not* shield an author-pinned link to the version being published:
    in Markdown a hand-written pin and the plugin's absolutised link are the same bytes, and the
    plugin wrote almost all of them. A pin to a *different* version — what an archival link to a
    previous release looks like — is untouched either way.
    """
    for page in layout.versioned_pages:
        text = text.replace(f"/{version}/{page}/", f"/latest/{page}/")
    text = _drop_version_from_page_urls(text, version=version, pages=layout.non_versioned_pages)
    text = _drop_version_from_file_urls(text, version=version, files=layout.root_files)
    return absolutise_root_relative_targets(text, layout=layout)


def _drop_version_from_page_urls(text: str, *, version: str, pages: tuple[str, ...]) -> str:
    """`https://openvidu.io/3.8/pricing/` -> `https://openvidu.io/pricing/`.

    These pages are built inside the version folder but published once at the site root, so the
    versioned URL the plugin wrote has never existed and returns a hard 404.
    """
    for page in pages:
        text = text.replace(f"/{version}/{page}/", f"/{page}/")
    return text


def _drop_version_from_file_urls(text: str, *, version: str, files: tuple[str, ...]) -> str:
    """`https://openvidu.io/3.8/index.md` -> `https://openvidu.io/index.md`.

    Same reasoning as the folders above, for the individual files promoted to the root. `index.md`
    is the one that occurs in practice: it is the home page's export, which every section links
    back to.
    """
    for name in files:
        text = text.replace(f"/{version}/{name}", f"/{name}")
    return text


def absolutise_root_relative_targets(text: str, *, layout: SiteLayout) -> str:
    """`](/pricing/#openvidu-pro)` -> `](https://openvidu.io/pricing/#openvidu-pro)`.

    The plugin absolutises a relative link but returns a root-relative one untouched, so whether an
    export hands out a resolvable URL would otherwise depend on how the author wrote the link.

    This cannot be done in the build: the plugin resolves against `site_url`, which mike makes
    versioned, so absolutising there yields `/3.8/pricing/` — a page served only from the root, and
    therefore a 404. Only the publish knows the final layout.

    Anchored to Markdown link syntax, so a root-relative path in prose or a code sample is left
    alone.
    """
    return ROOT_RELATIVE_TARGET.sub(lambda _match: f"]({layout.base_url}/", text)


def repair_export_links(text: str, *, exports: frozenset[str], layout: SiteLayout) -> str:
    """Point a link at the HTML page when the Markdown export it names does not exist.

    The plugin appends `index.md` to every relative directory link **without checking that the
    target has an export**, and only pages in its `sections` get one, so every export linking to a
    page outside that list advertises a URL that 404s.

    Listing more pages shrinks the problem but cannot close it: `docs/reference-docs/` is vendored
    TypeDoc output with no Markdown source, and a JavaScript shell like `/account/` would export as
    a bare heading. `exports` is read from the tree that was just built, so this needs no list to
    keep in step, and a repaired link gives an assistant the HTML rather than nothing.
    """
    base = f"{layout.base_url}/"
    pattern = re.compile(_EXPORT_TARGET.format(base=re.escape(base)))

    def repair(match: re.Match[str]) -> str:
        page = match.group("page")
        if f"{page}index.md" in exports:
            return match.group(0)
        return f"]({base}{page}{match.group('frag') or ''})"

    return pattern.sub(repair, text)
