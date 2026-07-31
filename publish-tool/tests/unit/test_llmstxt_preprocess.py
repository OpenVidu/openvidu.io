"""The `mkdocs-llmstxt` preprocess hook, checked against the `autoclean` it replaces.

Two halves, and the split is the point. The first half runs the module and the plugin's own
`autoclean` over the same markup and requires **identical** output — that is the promise that
turning `autoclean: false` changed nothing except on purpose. The second half covers the four
deviations, each of which the first half deliberately excludes.

The end-to-end proof over the real site is the differential build described in the README
("Testing and parity").
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from mkdocs_llmstxt._internal.preprocess import autoclean

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from llmstxt_preprocess import preprocess

#: Markup where the module must agree with `autoclean` exactly. Anything involving an image, a
#: comparison icon, a tab label or a media link belongs in the deviation tests instead.
AGREES = {
    "svg": '<p>text <svg viewBox="0 0 1 1"><path d="M0 0"></path></svg> more</p>',
    "permalink": '<h2>Title<a class="headerlink" href="#title" title="Permanent link">¶</a></h2>',
    "twemoji": '<p>ok <span class="twemoji"><svg><path d="M0"></path></svg></span></p>',
    "twemoji-with-other-classes": '<p><span class="twemoji icon lg-icon">x</span>y</p>',
    "doc-labels": '<p>sig<span class="doc-labels"><small>async</small></span></p>',
    "autoref": '<p>see <autoref identifier="x">Thing</autoref> here</p>',
    "doc-md-description": '<div class="doc-md-description">\n  A summary.\n</div>',
    "line-numbered-code": (
        '<table class="highlighttable"><tbody><tr>'
        '<td class="linenos"><div class="linenodiv"><pre>1\n2</pre></div></td>'
        '<td class="code"><div class="highlight"><pre><code>print("hi")\nexit()\n'
        "</code></pre></div></td></tr></tbody></table>"
    ),
    "plain-prose": "<p>Nothing to clean here at all.</p>",
    "table": "<table><thead><tr><th>A</th></tr></thead><tbody><tr><td>1</td></tr></tbody></table>",
    "code-fence": '<div class="highlight"><pre><code>docker run x</code></pre></div>',
    "anchor-with-text": '<p><a href="/pricing/">Pricing</a></p>',
    "nested-lists": "<ul><li>one<ul><li>two</li></ul></li></ul>",
}


def clean(markup: str, *, with_autoclean: bool) -> str:
    soup = BeautifulSoup(markup, "html.parser")
    if with_autoclean:
        autoclean(soup)
    else:
        preprocess(soup, "out.md")
    return str(soup)


# -- half one: identical to autoclean wherever we do not deviate -------------------------


@pytest.mark.parametrize("name", sorted(AGREES))
def test_matches_autoclean(name):
    """If this fails, `autoclean: false` changed something nobody chose to change."""
    markup = AGREES[name]
    assert clean(markup, with_autoclean=False) == clean(markup, with_autoclean=True)


def test_matches_autoclean_on_all_of_them_at_once():
    """Separately each rule agrees; together they must not interact into a difference."""
    markup = "<article>" + "".join(AGREES.values()) + "</article>"
    assert clean(markup, with_autoclean=False) == clean(markup, with_autoclean=True)


def test_an_image_without_alt_text_is_removed_exactly_as_autoclean_would():
    """The deviation is about *keeping the words*, so an image with no words is not a deviation."""
    for markup in ('<p>a<img src="x.png">b</p>', '<p>a<img src="x.png" alt="">b</p>'):
        assert clean(markup, with_autoclean=False) == clean(markup, with_autoclean=True)


# -- half two: the four deviations, each one deliberate ----------------------------------


def test_an_image_becomes_its_alt_text():
    markup = '<p><img alt="A room with three participants" src="/assets/x.png"></p>'
    assert "A room with three participants" in clean(markup, with_autoclean=False)
    assert "A room with three participants" not in clean(markup, with_autoclean=True)


def test_only_one_of_a_light_dark_pair_contributes_its_text():
    """Material renders the pair as two images with the same alt; both would read as a stutter."""
    markup = (
        '<p><img alt="The dashboard" src="/a.png#only-light">'
        '<img alt="The dashboard" src="/a.png#only-dark"></p>'
    )
    assert clean(markup, with_autoclean=False).count("The dashboard") == 1


@pytest.mark.parametrize(
    ("css_class", "expected"),
    [
        ("compare-table-icon-yes", "Yes"),
        ("compare-table-icon-no", "No"),
        ("compare-table-icon-progress", "In progress"),
    ],
)
def test_a_comparison_icon_becomes_text(css_class, expected):
    markup = f'<td><span class="twemoji {css_class}"><svg><path d="M0"></path></svg></span></td>'
    assert clean(markup, with_autoclean=False) == f"<td>{expected}</td>"


def test_the_comparison_table_header_recovers_the_product_names():
    """The header row is product logos, which is why the table exported with no header at all."""
    markup = '<tr><th></th><th><img alt="OpenVidu Meet" class="compare-table-logo"></th></tr>'
    assert clean(markup, with_autoclean=False) == "<tr><th></th><th>OpenVidu Meet</th></tr>"


def test_a_link_wrapping_a_video_becomes_its_alt_text_not_an_empty_link():
    """autoclean left this anchor alone, so markdownify wrote `[](…mp4)` — the \\[[](…)\\] noise."""
    markup = (
        '<p><a class="glightbox" href="/assets/videos/demo.mp4">'
        '<video src="/assets/videos/demo-preview.mp4" poster="/p.jpg"></video></a></p>'
    )
    cleaned = clean(markup, with_autoclean=False)
    assert "demo.mp4" not in cleaned
    assert "<a" not in cleaned


def test_a_link_wrapping_an_image_keeps_the_words_and_drops_the_url():
    markup = '<p><a href="/full.png"><img alt="Room settings dialog" src="/thumb.png"></a></p>'
    cleaned = clean(markup, with_autoclean=False)
    assert "Room settings dialog" in cleaned
    assert "full.png" not in cleaned


def test_a_media_link_with_nothing_to_say_is_dropped_entirely():
    markup = '<p><a href="/v.mp4"><video src="/v.mp4"></video></a></p>'
    assert clean(markup, with_autoclean=False) == "<p></p>"


def test_a_link_that_has_real_text_as_well_as_an_image_survives():
    """Only *purely* decorative anchors lose their URL."""
    markup = '<p><a href="/docs/"><img alt="icon" src="/i.png">Read the docs</a></p>'
    cleaned = clean(markup, with_autoclean=False)
    assert 'href="/docs/"' in cleaned
    assert "Read the docs" in cleaned


def test_tab_labels_are_kept_against_their_own_block():
    markup = (
        '<div class="tabbed-set"><input id="a" type="radio"><input id="b" type="radio">'
        '<div class="tabbed-labels">'
        '<label for="a"><span class="twemoji"><svg></svg></span> Linux</label>'
        '<label for="b">Windows</label></div>'
        '<div class="tabbed-content">'
        '<div class="tabbed-block"><pre><code>apt install</code></pre></div>'
        '<div class="tabbed-block"><pre><code>choco install</code></pre></div>'
        "</div></div>"
    )
    cleaned = clean(markup, with_autoclean=False)
    assert cleaned.index("Linux") < cleaned.index("apt install") < cleaned.index("Windows")
    assert cleaned.index("Windows") < cleaned.index("choco install")
    # autoclean dropped both, leaving two code blocks nobody could attribute.
    assert "Linux" not in clean(markup, with_autoclean=True)


def test_the_label_bar_itself_does_not_survive():
    """Otherwise every tab label would appear twice, once as a bar and once per block."""
    markup = (
        '<div class="tabbed-set"><div class="tabbed-labels"><label for="a">Go</label></div>'
        '<div class="tabbed-content"><div class="tabbed-block"><p>x</p></div></div></div>'
    )
    cleaned = clean(markup, with_autoclean=False)
    assert "tabbed-labels" not in cleaned
    assert cleaned.count("Go") == 1


def test_more_labels_than_blocks_does_not_raise():
    markup = (
        '<div class="tabbed-set"><div class="tabbed-labels">'
        '<label for="a">A</label><label for="b">B</label></div>'
        '<div class="tabbed-content"><div class="tabbed-block"><p>only one</p></div></div></div>'
    )
    assert "A" in clean(markup, with_autoclean=False)


def test_a_label_bar_with_no_content_sibling_does_not_raise():
    markup = '<div class="tabbed-labels"><label for="a">Orphan</label></div>'
    assert clean(markup, with_autoclean=False) == ""
