"""Loading and validating ovweb.yaml."""

from __future__ import annotations

import pytest

from ovweb.config import CONFIG_ENV_VAR, ConfigError, find_site_config, parse_site_config

BASE_LAYOUT = {
    "site_url": "https://openvidu.io",
    "versioned_pages": ["docs"],
    "non_versioned_pages": ["pricing"],
    "assets": ["assets", "search"],
    "pinned_assets": ["assets"],
    "root_files": ["index.html", "llms.txt", "feed_rss_created.xml"],
    "feeds": ["feed_rss_created.xml"],
}


def build(layout_overrides=None, **top):
    layout = {**BASE_LAYOUT, **(layout_overrides or {})}
    return parse_site_config({"schema": 1, "layout": layout, **top}, source="<test>")


# -- the real file -----------------------------------------------------------------------


def test_the_real_config_loads(config):
    assert config.layout.versioned_pages == ("docs", "meet")
    assert "pricing" in config.layout.non_versioned_pages
    assert config.file_rules


def test_the_real_config_is_found_without_an_explicit_path(monkeypatch):
    monkeypatch.delenv(CONFIG_ENV_VAR, raising=False)
    assert find_site_config().name == "ovweb.yaml"


def test_the_env_var_wins(monkeypatch, tmp_path):
    elsewhere = tmp_path / "ovweb.yaml"
    elsewhere.write_text("schema: 1\n", encoding="utf-8")
    monkeypatch.setenv(CONFIG_ENV_VAR, str(elsewhere))
    assert find_site_config() == elsewhere


def test_a_missing_env_var_target_is_an_error(monkeypatch, tmp_path):
    monkeypatch.setenv(CONFIG_ENV_VAR, str(tmp_path / "nope.yaml"))
    with pytest.raises(ConfigError, match="missing file"):
        find_site_config()


# -- derived helpers ---------------------------------------------------------------------


def test_versioned_and_non_versioned_dirs(config):
    assert config.layout.versioned_dirs("3.8") == ("3.8/docs", "3.8/meet")
    assert "3.8/pricing" in config.layout.non_versioned_dirs("3.8")


def test_index_html_is_not_deleted_from_a_past_version(config):
    """It is overwritten by the generated redirect, not removed."""
    removed = config.layout.files_removed_from_past_version
    assert "index.html" not in removed
    assert "index.md" in removed
    assert "llms.txt" in removed


def test_base_url_has_no_trailing_slash():
    assert build({"site_url": "https://openvidu.io/"}).layout.base_url == "https://openvidu.io"


# -- validation --------------------------------------------------------------------------


def test_rejects_an_unknown_schema():
    with pytest.raises(ConfigError, match="unsupported schema"):
        parse_site_config({"schema": 99, "layout": BASE_LAYOUT}, source="<test>")


def test_rejects_a_missing_layout_key():
    layout = dict(BASE_LAYOUT)
    del layout["assets"]
    with pytest.raises(ConfigError, match="missing assets"):
        parse_site_config({"schema": 1, "layout": layout}, source="<test>")


def test_rejects_a_relative_site_url():
    with pytest.raises(ConfigError, match="absolute URL"):
        build({"site_url": "openvidu.io"})


@pytest.mark.parametrize("name", ["/docs", "docs/", ""])
def test_rejects_a_page_name_with_slashes(name):
    with pytest.raises(ConfigError, match="bare name"):
        build({"versioned_pages": [name]})


def test_rejects_a_page_listed_as_both_versioned_and_not():
    with pytest.raises(ConfigError, match="both versioned and non-versioned"):
        build({"versioned_pages": ["docs"], "non_versioned_pages": ["docs"]})


def test_rejects_a_pinned_asset_that_is_not_an_asset():
    with pytest.raises(ConfigError, match="pinned_assets entries not present"):
        build({"pinned_assets": ["nope"]})


def test_rejects_a_feed_that_is_not_a_root_file():
    with pytest.raises(ConfigError, match="feeds entries not present"):
        build({"feeds": ["nope.xml"]})


def test_requires_index_html_among_the_root_files():
    with pytest.raises(ConfigError, match=r"must include index\.html"):
        build({"root_files": ["robots.txt"], "feeds": []})


def test_rejects_an_unknown_rule_key():
    with pytest.raises(ConfigError, match="unknown keys"):
        build(redirects={"files": [{"id": "r", "at": "version-root", "to": "a/", "oops": 1}]})


def test_rejects_a_for_each_that_names_nothing():
    with pytest.raises(ConfigError, match="for_each must name a layout list"):
        build(
            redirects={"patterns": [{"id": "p", "match": "^/x$", "to": "/y", "for_each": "nope"}]}
        )


# -- the unversioned mirror --------------------------------------------------------------


def test_the_real_config_mirrors_the_versioned_sections(config):
    """Both halves of issue 22's fix: /docs/ and /meet/ answer, and nothing else is mirrored."""
    assert config.mirror is not None
    assert config.mirror.enabled
    assert config.mirror.for_each == "versioned_pages"


def test_a_mirror_is_optional():
    assert build(redirects={}).mirror is None


def test_rejects_a_mirror_for_each_that_names_nothing():
    with pytest.raises(ConfigError, match="for_each must name a layout list"):
        build(redirects={"mirror": {"for_each": "nope", "body": "x"}})


def test_rejects_a_mirror_without_a_body():
    """It is the sentence a visitor whose browser blocks the refresh is left looking at."""
    with pytest.raises(ConfigError, match="needs a non-empty string 'body'"):
        build(redirects={"mirror": {"for_each": "versioned_pages"}})


def test_rejects_an_unknown_mirror_key():
    with pytest.raises(ConfigError, match="unknown keys"):
        build(redirects={"mirror": {"for_each": "versioned_pages", "body": "x", "oops": 1}})


def test_rejects_an_unknown_redirects_key():
    """A misspelled section would otherwise be ignored in full: `mirrors:` instead of `mirror:`
    publishes a site with no mirror and no complaint."""
    with pytest.raises(ConfigError, match="unknown 'redirects' keys"):
        build(redirects={"mirrors": {"for_each": "versioned_pages", "body": "x"}})
