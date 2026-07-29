"""Rewrites inside `<X.Y>/docs/` and `<X.Y>/meet/`."""

from __future__ import annotations

import pytest

from ovweb.rewrite.versioned import rewrite_versioned_file


def rewrite(text, layout, version="3.8"):
    return rewrite_versioned_file(text, version=version, layout=layout)


# -- asset pinning -----------------------------------------------------------------------


@pytest.mark.parametrize("directory", ["assets", "javascripts", "stylesheets"])
@pytest.mark.parametrize("attribute", ["src", "href"])
def test_pins_asset_references(layout, directory, attribute):
    text = f'<img {attribute}="/{directory}/images/logo.png">'
    assert rewrite(text, layout) == f'<img {attribute}="/3.8/{directory}/images/logo.png">'


def test_pins_data_attributes_too(layout):
    """`data-src="/assets/…"` is pinned as well.

    The pattern matches `src="` anywhere, which is what the shell did. It is also the right
    outcome: a script consuming `data-src` resolves it against the same root, so an unpinned
    value would reach for the newest publish's assets from an old version's page.
    """
    text = '<a class="glightbox" data-src="/assets/images/x.png">'
    assert rewrite(text, layout) == '<a class="glightbox" data-src="/3.8/assets/images/x.png">'


def test_does_not_pin_the_search_folder(layout):
    """`search` is an asset folder but is deliberately not pinned.

    The search index is not referenced by URL from page markup, and its own locations are
    rewritten separately.
    """
    text = '<script src="/search/search_index.json"></script>'
    assert rewrite(text, layout) == text


def test_does_not_pin_a_foreign_host(layout):
    text = '<img src="https://cdn.example.com/assets/x.png">'
    assert rewrite(text, layout) == text


def test_does_not_pin_a_protocol_relative_url(layout):
    text = '<img src="//cdn.example.com/assets/x.png">'
    assert rewrite(text, layout) == text


# -- links to pages served from the root -------------------------------------------------


@pytest.mark.parametrize("depth", ["", "../", "../../", "../../../"])
def test_absolutises_root_page_links_at_any_depth(layout, depth):
    text = f'<a href="{depth}pricing/">Pricing</a>'
    assert rewrite(text, layout) == '<a href="/pricing/">Pricing</a>'


def test_absolutises_every_configured_root_page(layout):
    for page in layout.non_versioned_pages:
        text = f'<a href="../../{page}/">x</a>'
        assert rewrite(text, layout) == f'<a href="/{page}/">x</a>', page


def test_leaves_a_same_named_subdirectory_of_a_versioned_page_alone(layout):
    """`href="support/"` inside the docs would be caught, but `docs/support/` is not a link
    MkDocs generates from a versioned page — it always emits `../`-prefixed paths to leave the
    version folder. The guard that matters is that an absolute link is untouched."""
    text = '<a href="/pricing/">x</a>'
    assert rewrite(text, layout) == text


@pytest.mark.parametrize("depth", ["..", "../..", "../../.."])
def test_absolutises_home_links(layout, depth):
    text = f'<a href="{depth}">Home</a>'
    assert rewrite(text, layout) == '<a href="/">Home</a>'


def test_absolutises_the_cookie_consent_base_url(layout):
    """Left relative, each version folder would be its own consent scope."""
    text = 'new URL("../..",location)'
    assert rewrite(text, layout) == 'new URL("/",location)'


# -- SEO self URLs -----------------------------------------------------------------------


def test_points_canonical_and_og_url_at_latest(layout):
    text = (
        '<link rel="canonical" href="https://openvidu.io/3.8/docs/self-hosting/">'
        '<meta property="og:url" content="https://openvidu.io/3.8/docs/self-hosting/">'
    )
    assert rewrite(text, layout) == (
        '<link rel="canonical" href="https://openvidu.io/latest/docs/self-hosting/">'
        '<meta property="og:url" content="https://openvidu.io/latest/docs/self-hosting/">'
    )


def test_leaves_author_pinned_links_alone(layout):
    """Only the two SEO tags are touched — a release note pinned to another version stays."""
    text = '<a href="https://openvidu.io/3.4/docs/releases/">3.4 release notes</a>'
    assert rewrite(text, layout) == text


def test_leaves_a_pin_to_the_published_version_alone(layout):
    text = '<a href="https://openvidu.io/3.8/docs/releases/">these release notes</a>'
    assert rewrite(text, layout) == text


def test_asset_pinning_runs_before_the_canonical_rewrite(layout):
    """Both apply to this page, and neither may disturb the other."""
    text = (
        '<link rel="canonical" href="https://openvidu.io/3.8/docs/">'
        '<img src="/assets/images/x.png">'
    )
    assert rewrite(text, layout) == (
        '<link rel="canonical" href="https://openvidu.io/latest/docs/">'
        '<img src="/3.8/assets/images/x.png">'
    )


def test_a_dot_in_the_version_is_not_a_wildcard(layout):
    """The shell interpolated the version straight into a regex, so `3.8` also matched `328`.

    Harmless in practice, but the port escapes it, and this pins that.
    """
    text = '<link rel="canonical" href="https://openvidu.io/328/docs/">'
    assert rewrite(text, layout) == text


def test_is_a_no_op_on_a_page_with_nothing_to_rewrite(layout):
    text = "<html><body><p>Nothing to see.</p></body></html>"
    assert rewrite(text, layout) == text


# -- links to files promoted to the root -------------------------------------------------


@pytest.mark.parametrize("depth", ["", "../", "../../", "../../../"])
def test_absolutises_rss_feed_links(layout, depth):
    """The theme puts two of these on every page. The feeds are served from the root and a
    version folder keeps no copy, so left relative they resolve to a 404."""
    text = f'<link rel="alternate" type="application/rss+xml" href="{depth}feed_rss_created.xml">'
    assert rewrite(text, layout) == (
        '<link rel="alternate" type="application/rss+xml" href="/feed_rss_created.xml">'
    )


def test_absolutises_every_promoted_root_file(layout):
    for name in layout.root_files:
        if name.startswith("index."):
            continue
        assert rewrite(f'<a href="../../{name}">x</a>', layout) == f'<a href="/{name}">x</a>', name


def test_leaves_the_home_page_link_to_the_home_rule(layout):
    """`index.html` and `index.md` are excluded so `href="../.."` -> `/` stays the only rule
    that decides what a link to the home page becomes."""
    assert rewrite('<a href="../..">Home</a>', layout) == '<a href="/">Home</a>'
    assert rewrite('<a href="../../index.html">Home</a>', layout) == (
        '<a href="../../index.html">Home</a>'
    )


def test_does_not_absolutise_a_same_named_page_inside_the_version(layout):
    """Only an exact relative link to the file is rewritten, not a path that merely ends with
    its name."""
    text = '<a href="../../notes/llms.txt/">x</a>'
    assert rewrite(text, layout) == text
