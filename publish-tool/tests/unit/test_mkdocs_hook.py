"""The MkDocs hook's two jobs: the sitemap's `<lastmod>`, and what the glightbox plugin appends
to every page.

`on_env` sets `page.update_date`, which MkDocs' sitemap template publishes as `<lastmod>`. What is
pinned is what has to hold on a real build: a generated page gets no date at all, and anything that
stops git answering leaves MkDocs' build date in place rather than failing.

`on_post_page` rewrites the glightbox plugin's own output, so its tests pin the two edits and the
loud failure that a plugin upgrade changing that output must produce.
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from mkdocs.exceptions import PluginError

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import mkdocs_hook
from mkdocs_hook import on_env, on_post_page

BUILD_DATE = "2026-07-31"


def page(src_uri: str):
    return SimpleNamespace(file=SimpleNamespace(src_uri=src_uri), meta={})


# -- on_env: the sitemap's <lastmod> ------------------------------------------------------


def doc_file(src_uri: str, *, generated: bool = False):
    """A `File` as `files.documentation_pages()` yields it, with a Page carrying the build date."""
    return SimpleNamespace(
        src_uri=src_uri,
        generated_by="material/blog" if generated else None,
        page=SimpleNamespace(update_date=BUILD_DATE),
    )


def env_call(tmp_path: Path, monkeypatch, files, dates):
    """Run `on_env` over `files` with `dates` standing in for the git log."""
    monkeypatch.setattr(mkdocs_hook, "_source_dates", lambda root, trees: dates)
    cfg = {"docs_dir": str(tmp_path / "docs"), "plugins": {}}
    return on_env("env", cfg, SimpleNamespace(documentation_pages=lambda: files))


def test_a_page_is_dated_from_its_last_commit(tmp_path, monkeypatch):
    page = doc_file("pricing.md")
    env_call(tmp_path, monkeypatch, [page], {"docs/pricing.md": "2026-07-22"})
    assert page.page.update_date == "2026-07-22"


def test_a_generated_page_gets_no_date_at_all(tmp_path, monkeypatch):
    """The blog's archive, category and pagination views have no source file to date."""
    view = doc_file("blog/archive/2026/07.md", generated=True)
    env_call(tmp_path, monkeypatch, [view], {"docs/blog/archive/2026/07.md": "2026-07-22"})
    assert view.page.update_date == ""


def test_a_page_git_has_never_seen_keeps_the_build_date(tmp_path, monkeypatch):
    page = doc_file("brand-new.md")
    env_call(tmp_path, monkeypatch, [page], {"docs/pricing.md": "2026-07-22"})
    assert page.page.update_date == BUILD_DATE


def test_git_being_unable_to_answer_leaves_every_date_alone(tmp_path, monkeypatch):
    """A shallow clone, no git binary, or a repository git refuses to touch."""
    page, view = doc_file("pricing.md"), doc_file("blog/page/2.md", generated=True)
    env_call(tmp_path, monkeypatch, [page, view], None)
    assert page.page.update_date == BUILD_DATE
    assert view.page.update_date == "", "a generated page has no date whether git answers or not"


def test_an_included_snippet_is_read_from_disk_and_can_move_the_date(tmp_path, monkeypatch):
    (tmp_path / "docs").mkdir()
    (tmp_path / "shared").mkdir()
    (tmp_path / "docs" / "install.md").write_text('--8<-- "version.md"', encoding="utf8")
    (tmp_path / "shared" / "version.md").write_text("3.8.0", encoding="utf8")
    page = doc_file("install.md")
    env_call(
        tmp_path,
        monkeypatch,
        [page],
        {"docs/install.md": "2026-06-25", "shared/version.md": "2026-07-22"},
    )
    assert page.page.update_date == "2026-07-22"


def test_on_env_returns_the_env_it_was_given(tmp_path, monkeypatch):
    assert env_call(tmp_path, monkeypatch, [], {}) == "env"


# -- on_env: metadata for the blog views the plugin generates ------------------------------

SHAPES = {
    "blog": "blog",
    "archive": "archive/{date}",
    "category": "category/{slug}",
    "pagination": "page/{page}",
}


def view(src_uri: str, *, title: str, posts: int = 0, meta_title: str | None = None):
    page = doc_file(src_uri, generated=True).page
    page.title = title
    page.posts = [object()] * posts
    page.meta = {"title": meta_title} if meta_title else {}
    return SimpleNamespace(src_uri=src_uri, generated_by="material/blog", page=page)


def described(item) -> dict:
    return mkdocs_hook._view_metadata(item.page, item.src_uri, SHAPES)


def test_an_archive_view_is_described_by_its_month_and_post_count():
    got = described(view("blog/archive/2026/07.md", title="July 2026", posts=5))
    expected = "Every OpenVidu Blog article published in July 2026: 5 posts"
    assert got["description"].startswith(expected)
    assert "title" not in got, "the month is already the nav label and the <title>"


def test_a_category_view_is_described_by_its_name_and_post_count():
    got = described(view("blog/category/ai.md", title="AI", posts=2))
    assert got["description"].startswith("Every OpenVidu Blog article filed under AI: 2 posts")


def test_a_single_post_is_not_pluralised():
    got = described(view("blog/category/release.md", title="Release", posts=1))
    assert "1 post," in got["description"]


def test_a_paginated_copy_of_the_blog_index_gets_its_own_title_and_description():
    """Otherwise it is a byte-identical <title> to /blog/, the site's only duplicate."""
    got = described(view("blog/page/2.md", title="Blog", meta_title="OpenVidu Blog"))
    assert got["title"] == "OpenVidu Blog — page 2"
    assert got["description"] == (
        "Page 2 of the OpenVidu Blog: more articles on "
        "self-hosted video conferencing and WebRTC engineering."
    )


def test_a_paginated_category_carries_the_page_number_in_both():
    """Categories paginate at 10 posts, so this arrives on its own as the blog grows."""
    got = described(view("blog/category/technology/page/2.md", title="Technology", posts=12))
    assert ", page 2: 12 posts," in got["description"]
    assert got["title"] == "Technology — page 2"


def test_a_view_shape_the_hook_does_not_know_is_left_alone():
    """An author profile, say: better untouched than described wrongly."""
    assert described(view("blog/author/someone.md", title="Someone")) == {}


def test_the_url_shapes_come_from_the_plugins_own_configuration():
    """Read from the public config, so renaming `category/` in mkdocs.yml keeps working."""

    class Options(dict):
        """Stands in for a mkdocs plugin config: dict access plus attributes."""

        archive_url_format = "by-month/{date}"

    options = Options(
        blog_dir="weblog",
        archive_url_format="by-month/{date}",
        categories_url_format="topic/{slug}",
        pagination_url_format="p/{page}",
    )
    cfg = {"plugins": {"blog": SimpleNamespace(config=options)}}
    assert mkdocs_hook._blog_url_shapes(cfg) == {
        "blog": "weblog",
        "archive": "by-month/{date}",
        "category": "topic/{slug}",
        "pagination": "p/{page}",
    }


def test_no_blog_plugin_means_no_view_metadata(tmp_path, monkeypatch):
    """`_blog_url_shapes` returns None and `on_env` must not try to describe anything."""
    item = doc_file("blog/archive/2026/07.md", generated=True)
    monkeypatch.setattr(mkdocs_hook, "_source_dates", lambda root, trees: {})
    on_env(
        "env",
        {"docs_dir": str(tmp_path / "docs"), "plugins": {}},
        SimpleNamespace(documentation_pages=lambda: [item]),
    )
    assert item.page.update_date == "", "still no lastmod, which does not depend on the blog plugin"


# -- on_post_page: the glightbox plugin's output -------------------------------------------

GLIGHTBOX_LIBRARY = '<script src="../assets/javascripts/glightbox.min.js"></script>'
GLIGHTBOX_INIT = (
    '<script id="init-glightbox">const lightbox = GLightbox({"touchNavigation": true, '
    '"zoomable": true, "openEffect": "zoom"});\n'
    "document$.subscribe(()=>{ lightbox.reload(); });\n</script>"
)


def rendered(init: str = GLIGHTBOX_INIT, *, library: bool = True) -> str:
    """A page the way the glightbox plugin leaves it: library in <head>, init at the end."""
    head = f"<head>{GLIGHTBOX_LIBRARY if library else ''}<title>x</title></head>"
    return f"<html>{head}<body><p>x</p>{init}</body></html>"


def test_the_library_moves_from_the_head_to_just_before_its_init_script():
    output = on_post_page(rendered(), page("docs/x.md"), {})

    assert "<head>" in output and GLIGHTBOX_LIBRARY not in output.split("<body>")[0]
    assert output.index(GLIGHTBOX_LIBRARY) < output.index('<script id="init-glightbox">')


def test_the_plugins_instance_becomes_the_configuration_our_script_reads():
    output = on_post_page(rendered(), page("docs/x.md"), {})

    assert (
        '<script id="init-glightbox">const glightboxOptions = {"touchNavigation": true, '
        '"zoomable": true, "openEffect": "zoom"};\n</script>' in output
    )
    assert "GLightbox(" not in output, "no second instance is built"
    assert "lightbox.reload" not in output, "nothing revives it either"


def test_a_page_without_lightbox_content_is_left_alone():
    assert on_post_page("<html><body><p>x</p></body></html>", page("docs/x.md"), {}) is None


def test_an_init_script_that_changed_shape_fails_the_build():
    init = '<script id="init-glightbox">const box = new GLightbox({"loop": false});</script>'

    with pytest.raises(PluginError, match="no longer builds its instance"):
        on_post_page(rendered(init), page("docs/x.md"), {})
