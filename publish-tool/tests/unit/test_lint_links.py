"""The lint link checks: raw-HTML targets, link form, version pins, commented content."""

from __future__ import annotations

from ovweb.lint import run_lint
from ovweb.model import SiteLayout

LAYOUT = SiteLayout(
    site_url="https://openvidu.io",
    versioned_pages=("docs", "meet"),
    non_versioned_pages=("pricing", "blog"),
    assets=("assets", "javascripts", "stylesheets", "search"),
    pinned_assets=("assets",),
    root_files=("index.html",),
    feeds=(),
)


def write(root, relpath, text=""):
    path = root / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def findings_of(root, check, paths=None):
    return [f for f in run_lint(root, layout=LAYOUT, paths=paths) if f.check == check]


# -- raw-HTML targets ------------------------------------------------------------------------


def test_a_missing_html_asset_is_an_error(tmp_path):
    write(tmp_path, "docs/index.md", '<img src="/assets/images/missing.png">')

    (finding,) = findings_of(tmp_path, "html-target")
    assert finding.severity == "error"
    assert finding.file == "docs/index.md"
    assert "/assets/images/missing.png" in finding.message


def test_an_existing_html_asset_and_page_url_are_clean(tmp_path):
    write(tmp_path, "docs/assets/images/logo.png")
    write(tmp_path, "docs/pricing.md")
    write(
        tmp_path,
        "docs/index.md",
        '<img src="/assets/images/logo.png#only-light"> <a href="/pricing/">x</a>',
    )

    assert findings_of(tmp_path, "html-target") == []


def test_a_latest_prefixed_html_url_resolves_against_the_versioned_tree(tmp_path):
    write(tmp_path, "docs/docs/getting-started.md")
    write(tmp_path, "docs/index.md", '<a href="/latest/docs/getting-started/">x</a>')

    assert findings_of(tmp_path, "html-target") == []


def test_a_directory_page_url_resolves_via_its_index(tmp_path):
    write(tmp_path, "docs/meet/index.md")
    write(tmp_path, "docs/index.md", '<a href="/meet/">x</a>')

    assert findings_of(tmp_path, "html-target") == []


def test_a_source_path_in_html_is_an_error(tmp_path):
    write(tmp_path, "docs/pricing.md")
    write(tmp_path, "docs/index.md", '<a href="/pricing.md">x</a>')

    (finding,) = findings_of(tmp_path, "html-md-form")
    assert finding.severity == "error"


def test_jinja_and_external_targets_are_skipped(tmp_path):
    write(tmp_path, "docs/overrides/main.html", "<link href=\"{{ 'x.css' | url }}\">")
    write(tmp_path, "docs/index.md", '<a href="https://example.com/x">x</a>')

    assert findings_of(tmp_path, "html-target") == []


def test_html_inside_a_code_fence_is_not_checked(tmp_path):
    write(tmp_path, "docs/index.md", '```html\n<a href="/not-a-page/">example</a>\n```\n')

    assert findings_of(tmp_path, "html-target") == []


def test_a_snippet_html_reference_is_checked_too(tmp_path):
    write(tmp_path, "shared/common/step.md", '<img src="/assets/images/gone.png">')

    (finding,) = findings_of(tmp_path, "html-target")
    assert finding.file == "shared/common/step.md"


# -- Markdown link form ----------------------------------------------------------------------


def test_a_relative_link_in_a_blog_post_is_an_error(tmp_path):
    write(tmp_path, "docs/blog/posts/2026/08/post.md", "[guide](../../guide.md)")

    (finding,) = findings_of(tmp_path, "md-relative-in-movable")
    assert finding.severity == "error"


def test_a_relative_link_in_a_snippet_is_a_warning(tmp_path):
    write(tmp_path, "shared/tutorials/intro.md", "[guide](../guide.md)")

    (finding,) = findings_of(tmp_path, "md-relative-in-movable")
    assert finding.severity == "warn"


def test_the_documented_snippet_exceptions_stay_silent(tmp_path):
    write(tmp_path, "shared/self-hosting/oracle/single-node/app.md", "[admin](./admin.md)")
    write(
        tmp_path,
        "shared/tutorials/openvidu-components/files.md",
        "[docs](../../reference-docs/openvidu-components-angular/index.html)",
    )

    assert findings_of(tmp_path, "md-relative-in-movable") == []


def test_root_absolute_and_external_links_in_movable_files_are_fine(tmp_path):
    write(
        tmp_path,
        "docs/blog/posts/2026/08/post.md",
        "[a](/meet/index.md) [b](https://example.com) [c](#anchor)",
    )

    assert findings_of(tmp_path, "md-relative-in-movable") == []


def test_a_stray_slash_before_an_anchor_is_an_error(tmp_path):
    write(tmp_path, "docs/docs/install.md", "[certs](../install.md/#custom-certificates)")

    (finding,) = findings_of(tmp_path, "stray-slash-anchor")
    assert finding.severity == "error"


# -- version pins ----------------------------------------------------------------------------


def test_a_version_pinned_link_outside_the_releases_pages_is_an_error(tmp_path):
    write(tmp_path, "docs/docs/guide.md", "[x](https://openvidu.io/3.8/docs/guide/)")

    (finding,) = findings_of(tmp_path, "version-pinned-link")
    assert finding.severity == "error"
    assert "3.8" in finding.message


def test_the_releases_pages_and_release_posts_may_pin_versions(tmp_path):
    write(tmp_path, "docs/docs/releases.md", "[x](https://openvidu.io/3.8/docs/guide/)")
    write(tmp_path, "docs/meet/releases.md", '<a href="/3.8/meet/">x</a>')
    write(
        tmp_path,
        "docs/blog/posts/2026/07/release-380.md",
        "---\ncategories:\n  - Release\n---\n[x](https://openvidu.io/3.8/docs/)",
    )

    assert findings_of(tmp_path, "version-pinned-link") == []


def test_a_non_release_post_may_not_pin_versions(tmp_path):
    write(
        tmp_path,
        "docs/blog/posts/2026/07/howto.md",
        "---\ncategories:\n  - How-to\n---\n[x](https://openvidu.io/3.8/docs/)",
    )

    (finding,) = findings_of(tmp_path, "version-pinned-link")
    assert finding.severity == "error"


def test_a_latest_link_on_a_releases_page_is_an_error(tmp_path):
    write(tmp_path, "docs/docs/releases.md", "[x](https://openvidu.io/latest/docs/guide/)")

    (finding,) = findings_of(tmp_path, "latest-in-releases")
    assert finding.severity == "error"


# -- commented-out content -------------------------------------------------------------------


def test_a_dead_link_inside_a_comment_is_info_not_error(tmp_path):
    write(tmp_path, "docs/index.md", "<!-- [old](/deployment/gone/) -->")

    assert findings_of(tmp_path, "html-target") == []
    (finding,) = findings_of(tmp_path, "commented-dead-link")
    assert finding.severity == "info"


def test_a_live_link_inside_a_comment_is_silent(tmp_path):
    write(tmp_path, "docs/pricing.md")
    write(tmp_path, "docs/index.md", "<!-- [still fine](/pricing/) -->")

    assert findings_of(tmp_path, "commented-dead-link") == []


# -- the runner ------------------------------------------------------------------------------


def test_paths_filter_limits_the_report(tmp_path):
    write(tmp_path, "docs/a.md", '<img src="/assets/one.png">')
    write(tmp_path, "docs/b.md", '<img src="/assets/two.png">')

    findings = findings_of(tmp_path, "html-target", paths=["docs/b.md"])
    assert [finding.file for finding in findings] == ["docs/b.md"]


def test_findings_are_sorted_by_file_line_and_severity(tmp_path):
    write(tmp_path, "docs/a.md", '<img src="/assets/one.png">\n<img src="/assets/two.png">')

    findings = run_lint(tmp_path, layout=LAYOUT)
    assert [finding.line for finding in findings] == sorted(finding.line for finding in findings)
