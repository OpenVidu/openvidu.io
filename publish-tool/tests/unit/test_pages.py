"""The checkout's pages, keyed by the URL each is served at."""

from __future__ import annotations

import datetime as dt

from ovweb.pages import page_dates, page_url, read_frontmatter, scan_pages


def test_an_index_collapses_to_its_folder_and_a_page_becomes_one():
    assert page_url("index.md", {}) == ""
    assert page_url("meet/index.md", {}) == "meet/"
    assert page_url("meet/getting-started.md", {}) == "meet/getting-started/"


def test_a_post_is_served_at_its_date_and_slug():
    meta = {"date": {"created": dt.date(2026, 4, 30)}, "slug": "Client-Networks"}

    assert page_url("blog/posts/2026/04/client-networks.md", meta) == (
        "blog/2026/04/30/client-networks/"
    )


def test_a_post_with_a_bare_date_and_no_slug_uses_its_file_name():
    meta = {"date": dt.date(2026, 7, 9)}

    assert page_url("blog/posts/2026/07/release-380.md", meta) == "blog/2026/07/09/release-380/"


def test_a_post_without_a_date_is_not_a_page():
    assert page_url("blog/posts/2026/07/draft.md", {"slug": "x"}) is None


def test_only_markdown_files_are_pages():
    assert page_url("blog/.authors.yml", {}) is None
    assert page_url("assets/images/x.png", {}) is None


def test_frontmatter_is_read_and_a_missing_block_is_empty():
    assert read_frontmatter('---\ntitle: "A"\n---\n# A\n') == {"title": "A"}
    assert read_frontmatter("# No frontmatter\n") == {}
    assert read_frontmatter("---\ntitle: [\n---\n") == {}


def test_scan_keys_every_page_by_url_and_keeps_its_path_and_meta(tmp_path):
    docs = tmp_path / "docs"
    (docs / "blog" / "posts" / "2026" / "04").mkdir(parents=True)
    (docs / "index.md").write_text('---\ntitle: "Home"\ndescription: "Start here."\n---\n')
    (docs / "pricing.md").write_text('---\ntitle: "Pricing"\n---\n')
    (docs / "blog" / "posts" / "2026" / "04" / "x.md").write_text(
        "---\ntitle: X\ndate:\n  created: 2026-04-30\nslug: x\n---\n"
    )

    pages = scan_pages(tmp_path)

    assert set(pages) == {"", "pricing/", "blog/2026/04/30/x/"}
    assert pages[""].path == "docs/index.md"
    assert pages[""].field("description") == "Start here."
    assert pages["pricing/"].field("description") is None
    assert pages["blog/2026/04/30/x/"].path == "docs/blog/posts/2026/04/x.md"


def test_a_field_is_one_line():
    from ovweb.pages import SourcePage

    page = SourcePage(url="", path="docs/index.md", meta={"description": "Two\n  lines. "})

    assert page.field("description") == "Two lines."


def test_page_dates_follow_the_snippets_and_are_keyed_by_url(tmp_path):
    from ovweb.pages import SourcePage

    pages = {
        "meet/": SourcePage(url="meet/", path="docs/meet/index.md", meta={}),
        "pricing/": SourcePage(url="pricing/", path="docs/pricing.md", meta={}),
    }
    files = {"docs/meet/index.md": '--8<-- "meet/intro.md"\n', "docs/pricing.md": "# Pricing"}
    dates = {"docs/meet/index.md": "2026-01-01", "shared/meet/intro.md": "2026-05-05"}

    resolved = page_dates(pages, dates=dates, read=files.get)

    assert resolved == {"meet/": "2026-05-05"}
