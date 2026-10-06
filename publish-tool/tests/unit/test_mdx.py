"""The Markdown extensions that replace the MkDocs hooks under Zensical."""

from __future__ import annotations

import markdown
import pytest

from ovweb.mdx import fence_title, root_links


@pytest.mark.parametrize(
    ("target", "page", "expected"),
    [
        (
            "/docs/self-hosting/local.md",
            "blog/posts/2026/04/post.md",
            "../../../../docs/self-hosting/local.md",
        ),
        ("/assets/images/a.png#only-dark", "meet/index.md", "../assets/images/a.png#only-dark"),
        ("/index.md", "pricing.md", "index.md"),
        (
            "/meet/embedded/intro.md#anchor",
            "meet/embedded/tutorials/index.md",
            "../intro.md#anchor",
        ),
        ("/support/", "docs/reference/egress.md", "../../support/"),
        ("/docs/releases.md?x=1#380", "docs/releases.md", "releases.md?x=1#380"),
    ],
)
def test_relative_to_page(target, page, expected):
    assert root_links.relative_to_page(target, page) == expected


@pytest.mark.parametrize(
    ("value", "root_absolute"),
    [
        ("/docs/x.md", True),
        ("/assets/a.png", True),
        ("//cdn.example.com/x.js", False),
        ("https://openvidu.io/pricing/", False),
        ("mailto:x@example.com", False),
        ("#anchor", False),
        ("../x.md", False),
    ],
)
def test_is_root_absolute(value, root_absolute):
    assert root_links._is_root_absolute(value) is root_absolute


def _render(text: str, page_path: str | None, monkeypatch) -> str:
    monkeypatch.setattr(root_links, "_page_path", lambda md: page_path)
    return markdown.markdown(text, extensions=[root_links.makeExtension()])


def test_rewrites_links_and_images_against_the_page(monkeypatch):
    html = _render(
        "[Local](/docs/self-hosting/local.md#step) ![d](/assets/images/x.png#only-dark)",
        "blog/posts/2026/04/post.md",
        monkeypatch,
    )
    assert 'href="../../../../docs/self-hosting/local.md#step"' in html
    assert 'src="../../../../assets/images/x.png#only-dark"' in html


def test_leaves_relative_external_and_anchor_links_alone(monkeypatch):
    text = "[a](../x.md) [b](https://example.com/y.md) [c](#top) [d](//cdn/x)"
    html = _render(text, "docs/index.md", monkeypatch)
    for href in ("../x.md", "https://example.com/y.md", "#top", "//cdn/x"):
        assert f'href="{href}"' in html


def test_is_a_no_op_without_a_rendering_context(monkeypatch):
    html = _render("[x](/docs/x.md)", None, monkeypatch)
    assert 'href="/docs/x.md"' in html


def test_raw_html_is_left_alone(monkeypatch):
    html = _render('<a href="/pricing/">Pricing</a>\n\ntext', "docs/index.md", monkeypatch)
    assert 'href="/pricing/"' in html


ESCAPED = (
    "<span class=\"filename\">&lt;a href='https://github.com/x/app.js' target='_blank'&gt;"
    "app.js&lt;/a&gt;</span>"
)


def test_fence_title_restores_the_link():
    assert fence_title.restore_filename_links(ESCAPED) == (
        '<span class="filename"><a href="https://github.com/x/app.js" target="_blank" '
        'rel="noopener">app.js</a></span>'
    )


def test_fence_title_restores_the_tab_nested_form():
    nested = ESCAPED.replace("'", "&#x27;")
    assert "<a href=" in fence_title.restore_filename_links(nested)


def test_fence_title_runs_as_a_postprocessor():
    md = markdown.Markdown(extensions=[fence_title.makeExtension()])
    md.postprocessors.register(_Escaper(md), "escaper", 6)
    assert "<a href=" in md.convert("x")


class _Escaper(markdown.postprocessors.Postprocessor):
    """Stand-in for the fence whose title Pygments escaped."""

    def run(self, text: str) -> str:
        return ESCAPED
