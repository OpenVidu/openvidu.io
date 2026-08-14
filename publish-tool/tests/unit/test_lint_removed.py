"""Removed pages must leave a redirect rule behind (`ovweb lint --against REF`)."""

from __future__ import annotations

from ovweb.config import parse_site_config
from ovweb.lint.removed import check_removed_pages

LAYOUT = {
    "site_url": "https://openvidu.io",
    "versioned_pages": ["docs", "meet"],
    "non_versioned_pages": ["pricing", "blog"],
    "assets": ["assets", "javascripts", "stylesheets", "search"],
    "pinned_assets": ["assets"],
    "root_files": ["index.html"],
    "feeds": [],
}


def build(files=(), expand=()):
    return parse_site_config(
        {
            "schema": 2,
            "layout": LAYOUT,
            "redirects": {"files": list(files), "expand": list(expand)},
        },
        source="<test>",
    )


def write(root, relpath):
    path = root / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x", encoding="utf-8")


def test_a_removed_versioned_page_without_a_rule_is_an_error(tmp_path):
    findings = check_removed_pages(
        ["docs/docs/self-hosting/local.md"], root=tmp_path, config=build()
    )

    (finding,) = findings
    assert finding.check == "removed-without-redirect"
    assert finding.severity == "error"
    assert finding.file == "docs/docs/self-hosting/local.md"


def test_a_page_still_present_is_fine(tmp_path):
    write(tmp_path, "docs/docs/self-hosting/local.md")

    assert (
        check_removed_pages(["docs/docs/self-hosting/local.md"], root=tmp_path, config=build())
        == []
    )


def test_a_files_rule_claiming_the_old_url_satisfies_the_check(tmp_path):
    config = build(
        files=[{"id": "moved", "at": "{version}/docs/self-hosting/local/index.html", "to": "../"}]
    )

    assert (
        check_removed_pages(["docs/docs/self-hosting/local.md"], root=tmp_path, config=config) == []
    )


def test_a_removed_non_versioned_page_maps_to_an_unversioned_stub(tmp_path):
    config = build(files=[{"id": "gone", "at": "pricing/index.html", "to": "/", "relative": False}])

    assert check_removed_pages(["docs/pricing.md"], root=tmp_path, config=config) == []
    (finding,) = check_removed_pages(["docs/support.md"], root=tmp_path, config=build())
    assert finding.file == "docs/support.md"


def test_an_index_page_maps_to_its_directory_url(tmp_path):
    config = build(files=[{"id": "gone", "at": "{version}/meet/embedded/index.html", "to": "../"}])

    assert check_removed_pages(["docs/meet/embedded/index.md"], root=tmp_path, config=config) == []


def test_expansion_rules_claim_their_paths(tmp_path):
    config = build(
        expand=[
            {
                "id": "provider-index",
                "kind": "cross-product",
                "at": "{version}/docs/self-hosting/{edition}/{provider}/index.html",
                "to": "install/",
                "values": {"edition": ["single-node"], "provider": ["aws"]},
            },
            {
                "id": "renamed",
                "kind": "tree-rename",
                "from": "{version}/docs/self-hosting",
                "to": "{version}/docs/deployment",
            },
            {
                "id": "fallback",
                "kind": "section-fallback",
                "dir": "{version}/meet",
                "to": "{version}/docs/call/",
                "versions": "<3.4",
            },
        ]
    )

    removed = [
        "docs/docs/self-hosting/single-node/aws/index.md",  # cross-product
        "docs/docs/self-hosting/elastic/upgrade.md",  # tree-rename prefix
        "docs/meet/embedded/intro.md",  # section-fallback prefix
    ]
    assert check_removed_pages(removed, root=tmp_path, config=config) == []

    (finding,) = check_removed_pages(["docs/docs/ai/overview.md"], root=tmp_path, config=config)
    assert finding.check == "removed-without-redirect"


def test_blog_posts_and_non_pages_are_exempt(tmp_path):
    removed = [
        "docs/blog/posts/2026/08/old-post.md",
        "overrides/partials/notes.md",
        "shared/self-hosting/common/step.md",
        "docs/assets/images/x.png",
    ]

    assert check_removed_pages(removed, root=tmp_path, config=build()) == []
