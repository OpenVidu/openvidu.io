"""The `mkdocs-llmstxt` preprocess hook, checked against the `autoclean` it replaces.

Two halves, and the split is the point. The first runs the module and the plugin's own `autoclean`
over the same markup and requires **identical** output, which is the promise that turning
`autoclean: false` changed nothing except on purpose. The second covers the deviations, each of
which the first half excludes.

The README describes the differential build that proves the same thing over the real site.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from mkdocs_llmstxt._internal.preprocess import autoclean

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from llmstxt_preprocess import preprocess

#: Markup where the module must agree with `autoclean` exactly. Anything involving a comparison
#: icon or logo, a tab label, a media link, a code block's filename or a callout belongs in the
#: deviation tests instead.
AGREES = {
    "svg": '<p>text <svg viewBox="0 0 1 1"><path d="M0 0"></path></svg> more</p>',
    "image": '<p>a<img alt="A room with three participants" src="/assets/x.png">b</p>',
    "image-without-alt": '<p>a<img src="x.png">b</p>',
    "image-with-empty-alt": '<p>a<img src="x.png" alt="">b</p>',
    "light-dark-pair": (
        '<p><img alt="The dashboard" src="/a.png#only-light">'
        '<img alt="The dashboard" src="/a.png#only-dark"></p>'
    ),
    "image-link": (
        '<p><a href="/full.png"><img alt="Room settings dialog" src="/thumb.png"></a></p>'
    ),
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
    "plain-filename": (
        '<div class="highlight"><span class="filename">app.js</span><pre><code>x</code></pre></div>'
    ),
    "anchor-with-text": '<p><a href="/pricing/">Pricing</a></p>',
    "plain-div": '<div class="grid cards"><p>Not a callout.</p></div>',
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


# -- half two: the deviations, each one deliberate ---------------------------------------


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
    assert clean(markup, with_autoclean=True) == "<tr><th></th><th></th></tr>"


def test_only_one_logo_of_a_light_dark_pair_names_the_product():
    markup = (
        '<th><img alt="OpenVidu Meet" class="compare-table-logo" src="/m.png#only-dark">'
        '<img alt="OpenVidu Meet" class="compare-table-logo" src="/m.png#only-light"></th>'
    )
    assert clean(markup, with_autoclean=False) == "<th>OpenVidu Meet</th>"


def test_a_link_wrapping_a_video_is_dropped_rather_than_left_as_an_empty_link():
    """`autoclean` leaves this anchor alone, so markdownify writes an empty `[](…mp4)` link."""
    markup = (
        '<p><a class="glightbox" href="/assets/videos/demo.mp4">'
        '<video src="/assets/videos/demo-preview.mp4" poster="/p.jpg"></video></a></p>'
    )
    assert clean(markup, with_autoclean=False) == "<p></p>"
    assert "demo.mp4" in clean(markup, with_autoclean=True)


def test_a_link_that_has_real_text_as_well_as_an_image_survives():
    """Only *purely* decorative anchors go; `autoclean` would drop this one whole."""
    markup = '<p><a href="/docs/"><img alt="icon" src="/i.png">Read the docs</a></p>'
    assert clean(markup, with_autoclean=False) == '<p><a href="/docs/">Read the docs</a></p>'
    assert "Read the docs" not in clean(markup, with_autoclean=True)


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


# -- a code block's linked filename -------------------------------------------------------

#: What Pygments 2.20.0 makes of `title="<a href='…' target='_blank'>app.js</a>"`.
ESCAPED_TITLE = (
    "&lt;a href='https://github.com/x/y/blob/main/app.js#L1-L9' target='_blank'&gt;app.js&lt;/a&gt;"
)
RESTORED_TITLE = (
    '<a href="https://github.com/x/y/blob/main/app.js#L1-L9" target="_blank">app.js</a>'
)


def test_an_escaped_filename_link_becomes_a_real_link():
    markup = (
        f'<div class="highlight"><span class="filename">{ESCAPED_TITLE}</span>'
        "<pre><code>x</code></pre></div>"
    )
    cleaned = clean(markup, with_autoclean=False)
    assert RESTORED_TITLE in cleaned
    assert "&lt;a" not in cleaned
    # autoclean leaves the text alone, and markdownify prints it as raw HTML.
    assert "&lt;a" in clean(markup, with_autoclean=True)


def test_a_filename_link_pygments_did_not_escape_is_left_alone():
    markup = (
        f'<div class="highlight"><span class="filename">{RESTORED_TITLE}</span>'
        "<pre><code>x</code></pre></div>"
    )
    assert clean(markup, with_autoclean=False) == markup


def test_a_line_numbered_block_keeps_its_filename_where_autoclean_drops_it():
    markup = (
        '<div class="language-js highlight"><table class="highlighttable"><tbody>'
        '<tr><th class="filename" colspan="2">'
        f'<span class="filename">{ESCAPED_TITLE}</span></th></tr>'
        '<tr><td class="linenos"><div class="linenodiv"><pre>1</pre></div></td>'
        '<td class="code"><div class="highlight"><pre><code>x = 1\n</code></pre></div></td></tr>'
        "</tbody></table></div>"
    )
    assert clean(markup, with_autoclean=False) == (
        f'<div class="language-js highlight"><span class="filename">{RESTORED_TITLE}</span>'
        "<pre>x = 1\n</pre></div>"
    )
    assert "app.js" not in clean(markup, with_autoclean=True)


# -- admonitions and collapsible blocks ---------------------------------------------------


def test_an_admonition_becomes_a_blockquote_led_by_its_bold_title():
    markup = (
        '<div class="admonition warning"><p class="admonition-title">Warning</p>'
        "<p>Back up first.</p><ul><li>one</li></ul></div>"
    )
    assert clean(markup, with_autoclean=False) == (
        "<blockquote><p><strong>Warning</strong></p>"
        "<p>Back up first.</p><ul><li>one</li></ul></blockquote>"
    )
    # autoclean keeps the div, and markdownify prints its title as a stray paragraph.
    assert clean(markup, with_autoclean=True) == markup


def test_an_admonition_without_a_title_is_still_quoted():
    markup = '<div class="admonition note"><p>Just this.</p></div>'
    assert clean(markup, with_autoclean=False) == "<blockquote><p>Just this.</p></blockquote>"


def test_a_collapsible_block_is_quoted_with_its_summary_as_the_title():
    markup = (
        '<details class="question"><summary>Nothing appears?</summary>'
        "<p>Check the console.</p></details>"
    )
    assert clean(markup, with_autoclean=False) == (
        "<blockquote><p><strong>Nothing appears?</strong></p><p>Check the console.</p></blockquote>"
    )


def test_a_nested_admonition_is_quoted_inside_its_parent():
    markup = (
        '<div class="admonition info"><p class="admonition-title">Info</p>'
        '<div class="admonition tip"><p class="admonition-title">Tip</p><p>x</p></div></div>'
    )
    assert clean(markup, with_autoclean=False) == (
        "<blockquote><p><strong>Info</strong></p>"
        "<blockquote><p><strong>Tip</strong></p><p>x</p></blockquote></blockquote>"
    )
