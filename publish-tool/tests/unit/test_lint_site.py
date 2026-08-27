"""The built-site tier: link resolution and anchor validation over mkdocs output."""

from __future__ import annotations

from ovweb.lint.site import check_site


def write(root, relpath, text=""):
    path = root / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def findings_of(site, check):
    return [f for f in check_site(site) if f.check == check]


PAGE = '<h1 id="top">T</h1><h2 id="section-one">S</h2>'


def test_a_missing_internal_target_is_an_error(tmp_path):
    write(tmp_path, "docs/index.html", '<a href="../gone/">x</a>')

    (finding,) = findings_of(tmp_path, "site-target")
    assert finding.severity == "error"
    assert finding.file == "docs/index.html"
    assert "/gone" in finding.message


def test_relative_root_absolute_and_asset_targets_resolve(tmp_path):
    write(tmp_path, "index.html", PAGE)
    write(tmp_path, "pricing/index.html", PAGE)
    write(tmp_path, "assets/logo.png")
    write(
        tmp_path,
        "docs/index.html",
        '<a href="../pricing/">a</a> <a href="/pricing/">b</a> '
        '<img src="/assets/logo.png"> <a href="/">home</a>',
    )

    assert findings_of(tmp_path, "site-target") == []


def test_a_broken_anchor_is_an_error_and_a_real_one_is_not(tmp_path):
    write(tmp_path, "pricing/index.html", PAGE)
    write(
        tmp_path,
        "docs/index.html",
        '<a href="/pricing/#section-one">ok</a> <a href="/pricing/#renamed">broken</a>',
    )

    (finding,) = findings_of(tmp_path, "site-anchor")
    assert "#renamed" in finding.message


def test_a_tab_style_generated_id_counts_as_a_real_anchor(tmp_path):
    """The whole point of checking the built HTML: generated ids exist here."""
    write(tmp_path, "guide/index.html", '<div id="__tabbed_1_2">tab</div>')
    write(tmp_path, "docs/index.html", '<a href="/guide/#__tabbed_1_2">x</a>')

    assert findings_of(tmp_path, "site-anchor") == []


def test_a_same_page_fragment_resolves_against_its_own_ids(tmp_path):
    write(tmp_path, "docs/index.html", f'{PAGE}<a href="#section-one">ok</a><a href="#nope">x</a>')

    (finding,) = findings_of(tmp_path, "site-anchor")
    assert "#nope" in finding.message


def test_spa_routing_fragments_are_skipped(tmp_path):
    write(tmp_path, "api.html", "<p>openapi viewer</p>")
    write(tmp_path, "docs/index.html", '<a href="/api.html#/operations/getRoom">x</a>')

    assert findings_of(tmp_path, "site-anchor") == []


def test_full_domain_internal_urls_resolve_and_version_pins_are_skipped(tmp_path):
    write(tmp_path, "pricing/index.html", PAGE)
    write(
        tmp_path,
        "docs/index.html",
        '<a href="https://openvidu.io/pricing/">ok</a> '
        '<a href="https://openvidu.io/latest/docs/">latest</a> '
        '<a href="https://openvidu.io/3.4/docs/">pinned</a> '
        '<a href="https://example.com/x">external</a>',
    )
    write(tmp_path, "docs/index2.html", '<a href="https://openvidu.io/gone/">broken</a>')

    findings = findings_of(tmp_path, "site-target")
    # /latest/ maps to the site root; the unversioned build serves docs/ itself.
    assert [f.file for f in findings] == ["docs/index2.html"]


def test_srcset_entries_are_checked(tmp_path):
    write(tmp_path, "docs/index.html", '<img srcset="/assets/a.png 1x, /assets/b.png 2x">')

    findings = findings_of(tmp_path, "site-target")
    assert len(findings) == 2


def test_generated_trees_and_copied_templates_are_not_walked(tmp_path):
    write(tmp_path, "docs/reference-docs/api/index.html", '<a href="./missing/">x</a>')
    write(tmp_path, "overrides/main.html", '<a href="{{ base_url }}/x/">jinja</a>')

    assert check_site(tmp_path) == []


def test_a_reference_docs_page_still_resolves_as_a_target(tmp_path):
    write(tmp_path, "docs/reference-docs/api/index.html", "<p>generated</p>")
    write(tmp_path, "docs/index.html", '<a href="reference-docs/api/index.html">x</a>')

    assert findings_of(tmp_path, "site-target") == []


def test_an_attr_block_that_reached_the_page_as_text_is_an_error(tmp_path):
    write(
        tmp_path,
        "docs/index.html",
        '<p>Go to <a href="../a/">X</a>{:target="_blank"}, then click <em>View</em>.</p>',
    )
    write(tmp_path, "docs/a/index.html", "<p>ok</p>")

    (finding,) = findings_of(tmp_path, "attr-block-leak")
    assert finding.severity == "error"
    assert 'target="_blank"' in finding.message


def test_an_attr_block_inside_an_html_comment_is_left_alone(tmp_path):
    write(
        tmp_path,
        "docs/index.html",
        '<!-- [X](https://e.com){:target="_blank"} commented out -->\n<p>ok</p>',
    )

    assert findings_of(tmp_path, "attr-block-leak") == []
