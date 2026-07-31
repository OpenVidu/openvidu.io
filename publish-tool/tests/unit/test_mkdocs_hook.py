"""The `on_page_content` half of the MkDocs hook: llms.txt entries from the frontmatter.

The hook reaches into two private attributes of `llmstxt` — `_sections` for the description and
`_md_pages` for the title — which is the one thing here a plugin upgrade could break. These
tests pin what matters: both values are taken from the page, a listed page missing either fails
the build, and a plugin that no longer exposes those attributes fails the build too instead of
quietly publishing an llms.txt full of nav labels and no descriptions.

`_MDPageInfo` is imported from the plugin rather than restated, so the fixture cannot drift from
the record the plugin actually writes.
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from mkdocs.exceptions import PluginError
from mkdocs_llmstxt._internal.plugin import _MDPageInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from mkdocs_hook import on_page_content

NAV_LABEL = "Install"


def page(src_uri: str, *, title: str | None = "A page title", description: str | None = "A page."):
    meta = {}
    if title is not None:
        meta["title"] = title
    if description is not None:
        meta["description"] = description
    return SimpleNamespace(file=SimpleNamespace(src_uri=src_uri), meta=meta)


def exported(*src_uris: str) -> dict[str, _MDPageInfo]:
    """What the plugin records for each page it selected — the title is the nav label."""
    return {
        uri: _MDPageInfo(title=NAV_LABEL, path_md=Path(uri), md_url=f"https://x/{uri}", content="")
        for uri in src_uris
    }


def config(sections, md_pages=None, *, plugin: bool = True):
    if not plugin:
        return {"plugins": {}}
    llmstxt = SimpleNamespace(_sections=sections, _md_pages={} if md_pages is None else md_pages)
    return {"plugins": {"llmstxt": llmstxt}}


# -- the description ---------------------------------------------------------------------


def test_the_description_replaces_whatever_the_config_said():
    sections = {"Platform": {"docs/index.md": "stale copy from mkdocs.yml"}}
    said = "What the page says about itself."
    cfg = config(sections, exported("docs/index.md"))
    on_page_content("<p/>", page("docs/index.md", description=said), cfg)
    assert sections["Platform"]["docs/index.md"] == said


def test_a_glob_gives_each_matched_page_its_own_description():
    """The whole point: one config entry, one description per page."""
    sections = {"Deployment": {"a/install.md": "", "b/install.md": ""}}
    cfg = config(sections, exported("a/install.md", "b/install.md"))
    for uri, description in (("a/install.md", "Install on A."), ("b/install.md", "Install on B.")):
        on_page_content("<p/>", page(uri, description=description), cfg)
    assert sections["Deployment"] == {
        "a/install.md": "Install on A.",
        "b/install.md": "Install on B.",
    }


# -- the title ---------------------------------------------------------------------------


def test_the_title_replaces_the_nav_label():
    """`page.title` is the nav label when the nav entry has one, which is not the page's name."""
    uri = "docs/self-hosting/single-node/aws/install.md"
    md_pages = exported(uri)
    on_page_content(
        "<p/>",
        page(uri, title="Install OpenVidu Single Node on AWS"),
        config({"Guides": {uri: ""}}, md_pages),
    )
    assert md_pages[uri].title == "Install OpenVidu Single Node on AWS"


def test_replacing_the_title_keeps_the_rest_of_the_record():
    """`_replace` on the NamedTuple, so the export path, URL and content survive untouched."""
    md_pages = exported("docs/index.md")
    before = md_pages["docs/index.md"]
    cfg = config({"S": {"docs/index.md": ""}}, md_pages)
    on_page_content("<p/>", page("docs/index.md", title="Real name"), cfg)
    after = md_pages["docs/index.md"]
    assert (after.path_md, after.md_url) == (before.path_md, before.md_url)
    assert after.content == before.content


def test_a_multiline_value_becomes_one_line():
    """A YAML block scalar would otherwise break the one-entry-per-line llms.txt format."""
    sections = {"Platform": {"docs/index.md": ""}}
    md_pages = exported("docs/index.md")
    on_page_content(
        "<p/>",
        page("docs/index.md", title="First\nsecond", description="First line\nand  second.\n"),
        config(sections, md_pages),
    )
    assert sections["Platform"]["docs/index.md"] == "First line and second."
    assert md_pages["docs/index.md"].title == "First second"


# -- pages the hook must not touch, and failures it must raise ----------------------------


def test_a_page_that_is_not_listed_is_left_alone():
    sections = {"Platform": {"docs/index.md": "kept"}}
    md_pages = exported("docs/index.md")
    on_page_content("<p/>", page("blog/index.md"), config(sections, md_pages))
    assert sections == {"Platform": {"docs/index.md": "kept"}}
    assert md_pages["docs/index.md"].title == NAV_LABEL


@pytest.mark.parametrize("missing", ["title", "description"])
@pytest.mark.parametrize("blank", [None, "", "   ", "\n"])
def test_a_listed_page_missing_either_value_fails_the_build(missing, blank):
    md_pages = exported("docs/index.md")
    with pytest.raises(PluginError, match=f"no `{missing}`"):
        on_page_content(
            "<p/>",
            page("docs/index.md", **{missing: blank}),
            config({"Platform": {"docs/index.md": ""}}, md_pages),
        )


@pytest.mark.parametrize("renamed", ["_sections", "_md_pages"])
def test_a_plugin_that_changed_shape_fails_loudly(renamed):
    attrs = {"_sections": {}, "_md_pages": {}}
    attrs[renamed] = None  # as if the upgrade renamed it away
    cfg = {"plugins": {"llmstxt": SimpleNamespace(**attrs)}}
    with pytest.raises(PluginError, match="no longer exposes"):
        on_page_content("<p/>", page("docs/index.md"), cfg)


def test_no_llmstxt_plugin_is_not_an_error():
    """`mkdocs serve` in a checkout with the plugin disabled must still work."""
    assert on_page_content("<p/>", page("docs/index.md"), config(None, plugin=False)) is None
