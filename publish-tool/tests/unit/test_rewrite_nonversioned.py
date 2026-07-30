"""Rewrites applied to the pages that are promoted to the site root."""

from __future__ import annotations

import pytest

from ovweb.model import KEEPVERSION_SENTINEL
from ovweb.rewrite.nonversioned import (
    RewriteError,
    rewrite_404,
    rewrite_feed,
    rewrite_non_versioned_file,
)

VERSION = "3.8"


def promote(text, layout):
    return rewrite_non_versioned_file(text, version=VERSION, layout=layout)


# -- links into versioned sections -------------------------------------------------------


@pytest.mark.parametrize("depth", ["", "../", "../../"])
@pytest.mark.parametrize("page", ["docs", "meet"])
def test_points_versioned_links_at_latest(layout, depth, page):
    text = f'<a href="{depth}{page}/self-hosting/">x</a>'
    assert promote(text, layout) == f'<a href="/latest/{page}/self-hosting/">x</a>'


# -- the page's own URL ------------------------------------------------------------------


def test_strips_the_version_from_self_urls(layout):
    text = (
        '<link rel="canonical" href="https://openvidu.io/3.8/pricing/">'
        '<meta property="og:url" content="https://openvidu.io/3.8/pricing/">'
        '<script type="application/ld+json">{"@id":"https://openvidu.io/3.8/pricing/"}</script>'
    )
    assert promote(text, layout) == (
        '<link rel="canonical" href="https://openvidu.io/pricing/">'
        '<meta property="og:url" content="https://openvidu.io/pricing/">'
        '<script type="application/ld+json">{"@id":"https://openvidu.io/pricing/"}</script>'
    )


def test_strips_the_version_from_the_home_url(layout):
    text = '<link rel="canonical" href="https://openvidu.io/3.8/">'
    assert promote(text, layout) == '<link rel="canonical" href="https://openvidu.io/">'


@pytest.mark.parametrize("pinned", ["3.4", "3.8", "3.0"])
def test_shields_author_pinned_versioned_links(layout, pinned):
    """A blog post's release-notes links are pinned on purpose and must survive the strip.

    This is the single most destructive thing the rewrite could get wrong: stripping the
    version here silently sends every historical release note to the newest documentation.
    """
    text = f'<a href="https://openvidu.io/{pinned}/docs/releases/">notes</a>'
    assert promote(text, layout) == text


def test_shields_a_pinned_link_while_stripping_its_own_url(layout):
    """Both happen on the same page, which is exactly the blog index."""
    text = (
        '<link rel="canonical" href="https://openvidu.io/3.8/blog/">'
        '<a href="https://openvidu.io/3.8/docs/releases/">notes</a>'
    )
    assert promote(text, layout) == (
        '<link rel="canonical" href="https://openvidu.io/blog/">'
        '<a href="https://openvidu.io/3.8/docs/releases/">notes</a>'
    )


def test_never_leaves_the_sentinel_behind(layout):
    text = '<a href="/3.8/docs/x/">a</a><a href="/3.8/meet/y/">b</a><span>/3.8/</span>'
    assert KEEPVERSION_SENTINEL not in promote(text, layout)


def test_rejects_content_that_already_holds_the_sentinel(layout):
    """Otherwise the unshield step would rewrite author content into a version path."""
    text = f"<p>{KEEPVERSION_SENTINEL}</p><span>/3.8/</span>"
    with pytest.raises(RewriteError, match="sentinel"):
        promote(text, layout)


# -- the 404 page ------------------------------------------------------------------------


def test_404_strips_the_version_and_sends_versioned_links_to_latest(layout):
    text = (
        '<link rel="canonical" href="https://openvidu.io/3.8/404.html">'
        '<a href="/3.8/pricing/">pricing</a>'
        '<a href="/3.8/docs/">docs</a>'
    )
    assert rewrite_404(text, version=VERSION, layout=layout) == (
        '<link rel="canonical" href="https://openvidu.io/404.html">'
        '<a href="/pricing/">pricing</a>'
        '<a href="/latest/docs/">docs</a>'
    )


def test_404_handles_a_version_link_without_a_trailing_slash(layout):
    """The theme emits `href="/3.8"` for the home link on some pages."""
    text = '<a href="/3.8">home</a>'
    assert rewrite_404(text, version=VERSION, layout=layout) == '<a href="/">home</a>'


# -- feeds -------------------------------------------------------------------------------


def test_feed_strips_the_version(layout):
    text = "<link>https://openvidu.io/3.8/blog/a-post/</link>"
    assert rewrite_feed(text, version=VERSION) == "<link>https://openvidu.io/blog/a-post/</link>"
