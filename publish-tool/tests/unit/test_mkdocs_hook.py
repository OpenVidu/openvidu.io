"""The `on_page_content` half of the MkDocs hook: llms.txt descriptions from the frontmatter.

The hook reaches into `llmstxt`'s private `_sections`, which is the one thing here that a
plugin upgrade could break. These tests pin the three outcomes that matter: the description is
copied across, a listed page without one fails the build, and a plugin that no longer exposes
`_sections` fails the build too instead of quietly publishing an llms.txt with no descriptions.
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from mkdocs.exceptions import PluginError

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from mkdocs_hook import on_page_content


def page(src_uri: str, description: str | None = None):
    meta = {} if description is None else {"description": description}
    return SimpleNamespace(file=SimpleNamespace(src_uri=src_uri), meta=meta)


def config(sections: object, *, plugin: bool = True):
    llmstxt = SimpleNamespace(_sections=sections) if plugin else None
    return {"plugins": {"llmstxt": llmstxt} if plugin else {}}


def test_the_description_replaces_whatever_the_config_said():
    sections = {"Platform": {"docs/index.md": "stale copy from mkdocs.yml"}}
    said = "What the page says about itself."
    on_page_content("<p/>", page("docs/index.md", said), config(sections))
    assert sections["Platform"]["docs/index.md"] == said


def test_a_glob_gives_each_matched_page_its_own_description():
    """The whole point: one config entry, one description per page."""
    sections = {"Deployment": {"a/install.md": "", "b/install.md": ""}}
    for uri, description in (("a/install.md", "Install on A."), ("b/install.md", "Install on B.")):
        on_page_content("<p/>", page(uri, description), config(sections))
    assert sections["Deployment"] == {
        "a/install.md": "Install on A.",
        "b/install.md": "Install on B.",
    }


def test_a_multiline_description_becomes_one_line():
    """A YAML block scalar would otherwise break the one-entry-per-line llms.txt format."""
    sections = {"Platform": {"docs/index.md": ""}}
    on_page_content("<p/>", page("docs/index.md", "First line\nand  second.\n"), config(sections))
    assert sections["Platform"]["docs/index.md"] == "First line and second."


def test_a_page_that_is_not_listed_is_left_alone():
    sections = {"Platform": {"docs/index.md": "kept"}}
    on_page_content("<p/>", page("blog/index.md", "not exported"), config(sections))
    assert sections == {"Platform": {"docs/index.md": "kept"}}


def test_a_listed_page_without_a_description_fails_the_build():
    sections = {"Platform": {"docs/index.md": ""}}
    with pytest.raises(PluginError, match="no `description`"):
        on_page_content("<p/>", page("docs/index.md"), config(sections))


@pytest.mark.parametrize("blank", ["", "   ", "\n"])
def test_a_blank_description_counts_as_missing(blank):
    sections = {"Platform": {"docs/index.md": ""}}
    with pytest.raises(PluginError, match="no `description`"):
        on_page_content("<p/>", page("docs/index.md", blank), config(sections))


def test_a_plugin_without_sections_fails_loudly():
    with pytest.raises(PluginError, match="no longer exposes"):
        on_page_content("<p/>", page("docs/index.md", "x"), config(None))


def test_no_llmstxt_plugin_is_not_an_error():
    """`mkdocs serve` in a checkout with the plugin disabled must still work."""
    assert on_page_content("<p/>", page("docs/index.md", "x"), config(None, plugin=False)) is None
