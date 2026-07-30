"""Rewrites for the Markdown exports published alongside the HTML.

The `llmstxt` plugin writes an `index.md` next to every `index.html`, indexes them all in
`llms.txt`, and concatenates them into `llms-full.txt`. Together they are the site's AI-facing
channel, and they carry the same links as the HTML pages they mirror — but as absolute URLs,
resolved by the plugin against the build's `site_url`.

That absolutisation is what makes these files a separate problem. mike builds each version with
its own versioned `site_url`, so every internal link in every export comes out pinned to the
version that produced it, and the HTML rewrites cannot reach them: those patterns match
`href="…"` and `src="…"`, which Markdown link syntax does not have. Left alone, an export
advertises URLs that go stale at the next release — plus a handful that never resolved at all,
because a page served only from the site root has no versioned URL.

The rules below mirror the HTML ones so that a page and its export send a reader to the same
place. Which rule applies depends on where the export is served from, exactly as it does for
HTML:

* :func:`rewrite_versioned_markdown` — the export of a versioned page. Links into the same
  version stay pinned, so a reader who arrived at one version's documentation keeps reading that
  version. Everything served from the root loses the version.
* :func:`rewrite_promoted_markdown` — the export of a page promoted to the root. It has no
  version of its own, so links into versioned documentation go to `/latest/`.
* :func:`rewrite_llms_file` — `llms.txt` and `llms-full.txt`. Root files, so the promoted rules
  apply, plus one more that only they need.
"""

from __future__ import annotations

import re

from ..model import SiteLayout

#: Markdown link or image target that is root-relative. `](//host/…)` is excluded: a
#: protocol-relative URL already names a host.
ROOT_RELATIVE_TARGET = re.compile(r"\]\(/(?!/)")

#: The suffix of the exports. Used by the pipeline to pick between these rules and the HTML ones.
SUFFIX = ".md"


def rewrite_versioned_markdown(text: str, *, version: str, layout: SiteLayout) -> str:
    """Rewrite the Markdown export of a page inside a version's versioned-page folder.

    Mirrors :func:`ovweb.rewrite.versioned.rewrite_versioned_file`: links that stay inside the
    version folder are left pinned to it, and links to anything served from the site root lose
    the version segment they were built with.
    """
    text = _drop_version_from_page_urls(text, version=version, pages=layout.non_versioned_pages)
    return _drop_version_from_file_urls(text, version=version, files=layout.root_files)


def rewrite_promoted_markdown(text: str, *, version: str, layout: SiteLayout) -> str:
    """Rewrite the Markdown export of a page promoted to the site root.

    Mirrors :func:`ovweb.rewrite.nonversioned.rewrite_non_versioned_file`: the page is served
    from the root, so it carries no version of its own, and its links into versioned
    documentation point at `/latest/`.

    Unlike the HTML, this does *not* shield an author-pinned link to the version being
    published. The two are indistinguishable here — the plugin absolutises every link into the
    same shape an author would have written by hand — and they are overwhelmingly the plugin's,
    so treating them as the plugin's is right far more often than not. A pin to a *different*
    version is untouched either way, which is the form a deliberately archival link takes: the
    release notes link back to the previous release, not to the one being published.
    """
    for page in layout.versioned_pages:
        text = text.replace(f"/{version}/{page}/", f"/latest/{page}/")
    text = _drop_version_from_page_urls(text, version=version, pages=layout.non_versioned_pages)
    return _drop_version_from_file_urls(text, version=version, files=layout.root_files)


def rewrite_llms_file(text: str, *, version: str, layout: SiteLayout) -> str:
    """Rewrite `llms.txt` or `llms-full.txt`.

    Both are served from the site root, so the promoted rules apply to them unchanged: the URLs
    they hand an assistant have to be the ones the site actually serves, and versioned
    documentation is reached at `/latest/`.

    `llms-full.txt` needs the promoted rules even though most of what it concatenates is
    versioned-page content, because the file itself is only ever fetched from the root. That is
    the same asymmetry the search index has, and for the same reason: each version's own export
    keeps its version so an in-version reader stays in it, while the root's single copy points
    at the URL that does not go stale.
    """
    text = rewrite_promoted_markdown(text, version=version, layout=layout)
    return _absolutise_root_relative_targets(text, layout=layout)


def _drop_version_from_page_urls(text: str, *, version: str, pages: tuple[str, ...]) -> str:
    """`https://openvidu.io/3.8/pricing/` -> `https://openvidu.io/pricing/`.

    These pages are built inside the version folder but published once at the site root, so
    the versioned URL the plugin wrote is not merely stale — it has never existed, and returns
    a hard 404.
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


def _absolutise_root_relative_targets(text: str, *, layout: SiteLayout) -> str:
    """`](/pricing/#openvidu-pro)` -> `](https://openvidu.io/pricing/#openvidu-pro)`.

    These two files are the only ones meant to be read away from the site: an assistant fetches
    them once and works from the text, with no document URL left to resolve a root-relative path
    against. Every other export is read at its own URL, where such a path still resolves, so this
    rule is not applied to them.

    Anchored to Markdown link syntax, so a root-relative path quoted in prose or inside a code
    sample is left alone.
    """
    return ROOT_RELATIVE_TARGET.sub(lambda _match: f"]({layout.base_url}/", text)
