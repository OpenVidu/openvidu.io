"""Splicing release notes between versions."""

from __future__ import annotations

import pytest

from ovweb.releases import (
    ARTICLE_MARKER,
    TOC_MARKER,
    DestinationRegionError,
    SourceRegionError,
    find_region,
    splice_releases,
)


def page(article: str, toc: str, *, tocs: int = 2, chrome: str = "3.8") -> str:
    """A page shaped like Material's output: one article, `tocs` copies of the sidebar."""
    rendered_toc = f'{TOC_MARKER}<nav class="md-nav"><a href="#x">{toc}</a></nav></nav>' * tocs
    return (
        f'<html><head><link rel="canonical" href="https://openvidu.io/{chrome}/docs/releases/">'
        f"</head><body>{rendered_toc}"
        f"{ARTICLE_MARKER}<h2>{article}</h2></article>"
        f"<footer>{chrome}</footer></body></html>"
    )


def test_splices_the_article_and_every_toc():
    source = page("3.9.0 notes", "3.9.0")
    destination = page("3.4.0 notes", "3.4.0", chrome="3.4")

    result = splice_releases(source, destination)

    assert "3.9.0 notes" in result.html
    assert "3.4.0 notes" not in result.html
    assert result.tocs_replaced == 2
    assert result.html.count('<a href="#x">3.9.0</a>') == 2


def test_leaves_the_destination_chrome_untouched():
    """This is the whole point: an old version's releases page must stay inside that version."""
    source = page("3.9.0 notes", "3.9.0")
    destination = page("3.4.0 notes", "3.4.0", chrome="3.4")

    html = splice_releases(source, destination).html

    assert 'href="https://openvidu.io/3.4/docs/releases/"' in html
    assert "<footer>3.4</footer>" in html
    assert "https://openvidu.io/3.8/" not in html


def test_counts_nested_navs_rather_than_stopping_at_the_first_close():
    """The table of contents nests one <nav> per heading level — the reason this is not sed."""
    nested = (
        f"{TOC_MARKER}"
        '<nav class="md-nav"><nav class="md-nav"><a href="#deep">deep</a></nav></nav>'
        "</nav>"
    )
    start, end = find_region(nested, TOC_MARKER)
    assert nested[start:end] == nested
    assert nested[end - len("</nav>") : end] == "</nav>"


def test_a_missing_marker_in_the_source_is_fatal():
    """The source is the freshly built newest page: a failure means every copy would be wrong."""
    with pytest.raises(SourceRegionError):
        splice_releases("<html>no regions</html>", page("x", "y"))


def test_a_missing_marker_in_the_destination_is_recoverable():
    """An old version folder may have been built by a theme that named the regions differently."""
    with pytest.raises(DestinationRegionError):
        splice_releases(page("x", "y"), "<html>no regions</html>")


def test_a_destination_without_a_toc_is_recoverable():
    source = page("x", "y")
    destination = page("a", "b", tocs=0)
    with pytest.raises(DestinationRegionError, match="Table of contents"):
        splice_releases(source, destination)


@pytest.mark.parametrize("link", ['href="../3.4/docs/"', 'src="images/x.png"', 'href="releases/"'])
def test_rejects_a_relocatable_link_in_the_source(link):
    """Relative links resolve against the folder the page lives in, so they would break."""
    source = f"{TOC_MARKER}</nav>{ARTICLE_MARKER}<a {link}>x</a></article>"
    with pytest.raises(SourceRegionError, match="relative to the version folder"):
        splice_releases(source, page("a", "b"))


@pytest.mark.parametrize(
    "link",
    ['href="https://openvidu.io/3.4/docs/"', 'href="#3-4-0"', 'href="mailto:a@b.c"'],
)
def test_accepts_absolute_anchor_and_mailto_links(link):
    source = f"{TOC_MARKER}</nav>{ARTICLE_MARKER}<a {link}>x</a></article>"
    assert splice_releases(source, page("a", "b")).tocs_replaced == 2


def test_reports_the_spliced_size():
    source = page("3.9.0 notes", "3.9.0")
    result = splice_releases(source, page("old", "old", chrome="3.4"))
    assert result.article_bytes > len(ARTICLE_MARKER)
