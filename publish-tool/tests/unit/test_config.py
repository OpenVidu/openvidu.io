"""Loading and validating ovweb.yaml."""

from __future__ import annotations

import pytest

from ovweb.config import ConfigError, find_site_config, load_site_config, parse_site_config
from ovweb.model import (
    CrossProductRule,
    SectionFallbackRule,
    TreeRenameRule,
    UnversionedMirrorRule,
    VersionAliasRule,
)

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
    return parse_site_config({"schema": 2, "layout": layout, **top}, source="<test>")


# -- the real file -----------------------------------------------------------------------


def test_the_real_config_loads(config):
    assert config.layout.versioned_pages == ("docs", "meet")
    assert "pricing" in config.layout.non_versioned_pages
    assert config.file_rules


def test_the_real_config_is_found_without_an_explicit_path():
    assert find_site_config().name == "ovweb.yaml"


def test_an_explicit_path_that_does_not_exist_is_an_error(tmp_path):
    with pytest.raises(ConfigError, match="config not found"):
        load_site_config(tmp_path / "ovweb.yaml")


def test_invalid_yaml_is_reported_as_such(tmp_path):
    path = tmp_path / "ovweb.yaml"
    path.write_text("schema: 1\nlayout: [unclosed\n", encoding="utf-8")
    with pytest.raises(ConfigError, match="cannot read"):
        load_site_config(path)


# -- derived helpers ---------------------------------------------------------------------


def test_index_html_is_not_deleted_from_a_past_version(config):
    """It is overwritten by the generated redirect, not removed."""
    removed = config.layout.files_removed_from_past_version
    assert "index.html" not in removed
    assert "index.md" in removed
    assert "llms.txt" in removed


def test_base_url_has_no_trailing_slash():
    assert build({"site_url": "https://openvidu.io/"}).layout.base_url == "https://openvidu.io"


# -- validation --------------------------------------------------------------------------


@pytest.mark.parametrize("schema", [1, 99, None])
def test_rejects_any_schema_but_the_current_one(schema):
    with pytest.raises(ConfigError, match="unsupported schema"):
        parse_site_config({"schema": schema, "layout": BASE_LAYOUT}, source="<test>")


@pytest.mark.parametrize("raw", ["just a string", ["a", "list"], None])
def test_rejects_a_top_level_that_is_not_a_mapping(raw):
    with pytest.raises(ConfigError, match="top level must be a mapping"):
        parse_site_config(raw, source="<test>")


@pytest.mark.parametrize("section", ["layout", "redirects"])
def test_rejects_a_section_that_is_not_a_mapping(section):
    with pytest.raises(ConfigError, match="must be a mapping"):
        parse_site_config({"schema": 2, "layout": BASE_LAYOUT, section: ["nope"]}, source="<test>")


def test_rejects_a_missing_layout_key():
    layout = dict(BASE_LAYOUT)
    del layout["assets"]
    with pytest.raises(ConfigError, match="missing assets"):
        parse_site_config({"schema": 2, "layout": layout}, source="<test>")


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


def test_rejects_an_unknown_defaults_key():
    with pytest.raises(ConfigError, match=r"unknown redirects\.defaults keys"):
        build(redirects={"defaults": {"tittle": "typo"}})


@pytest.mark.parametrize("key", ["id", "at", "to"])
def test_rejects_a_rule_missing_a_required_string(key):
    rule = {"id": "r", "at": "version-root", "to": "a/"}
    del rule[key]
    with pytest.raises(ConfigError, match=f"needs a non-empty string '{key}'"):
        build(redirects={"files": [rule]})


def test_rejects_an_absolute_at_path():
    with pytest.raises(ConfigError, match="must be relative to the site root"):
        build(redirects={"files": [{"id": "r", "at": "/x/index.html", "to": "a/"}]})


def test_rejects_an_unknown_when_key():
    with pytest.raises(ConfigError, match="unknown keys"):
        build(
            redirects={
                "files": [
                    {
                        "id": "r",
                        "at": "version-root",
                        "to": "a/",
                        "when": [{"versions": "<3.4", "at": "elsewhere"}],
                    }
                ]
            }
        )


def test_rejects_a_when_entry_without_a_version_range():
    with pytest.raises(ConfigError, match="needs a non-empty 'versions' specifier"):
        build(
            redirects={
                "files": [{"id": "r", "at": "version-root", "to": "a/", "when": [{"to": "b/"}]}]
            }
        )


def test_rejects_an_unknown_redirects_key():
    """A misspelled section would otherwise be ignored in full, publishing nothing of it."""
    with pytest.raises(ConfigError, match="unknown 'redirects' keys"):
        build(redirects={"expands": []})


@pytest.mark.parametrize(
    ("retired", "pointer"),
    [("patterns", "the 404 router is gone"), ("mirror", "unversioned-mirror")],
)
def test_the_retired_sections_name_their_replacement(retired, pointer):
    with pytest.raises(ConfigError, match=pointer):
        build(redirects={retired: []})


# -- expansion rules -----------------------------------------------------------------------

CROSS_PRODUCT = {
    "id": "moved",
    "kind": "cross-product",
    "at": "{version}/docs/{area}/{provider}/index.html",
    "to": "install/",
    "canonical": "{site_url}/latest/docs/{area}/{provider}/install/",
    "values": {"area": ["single-node", "elastic"], "provider": ["aws", "gcp"]},
}


def expand(*rules):
    return build(redirects={"expand": list(rules)}).expand_rules


def test_parses_a_cross_product_rule():
    (rule,) = expand(CROSS_PRODUCT)
    assert isinstance(rule, CrossProductRule)
    assert dict(rule.values) == {"area": ("single-node", "elastic"), "provider": ("aws", "gcp")}


def test_parses_the_other_three_kinds():
    rename, alias, mirror = expand(
        {"id": "rn", "kind": "tree-rename", "from": "{version}/docs/a", "to": "{version}/docs/b"},
        {"id": "va", "kind": "version-alias", "folders": ["3.4.1", "3.0.0-beta1"]},
        {"id": "um", "kind": "unversioned-mirror", "for_each": "versioned_pages"},
    )
    assert isinstance(rename, TreeRenameRule) and rename.from_path == "{version}/docs/a"
    assert isinstance(alias, VersionAliasRule) and alias.folders == ("3.4.1", "3.0.0-beta1")
    assert isinstance(mirror, UnversionedMirrorRule) and mirror.for_each == "versioned_pages"


SECTION_FALLBACK = {
    "id": "meet-fallback",
    "kind": "section-fallback",
    "dir": "{version}/meet",
    "to": "{version}/docs/call/",
    "versions": "<3.4",
}


def test_parses_a_section_fallback_rule():
    (rule,) = expand(SECTION_FALLBACK)
    assert isinstance(rule, SectionFallbackRule)
    assert rule.dir == "{version}/meet"
    assert rule.to == "{version}/docs/call/"
    assert rule.versions == "<3.4"


def test_a_section_fallback_requires_a_versions_gate():
    with pytest.raises(ConfigError, match="needs 'versions'"):
        expand({**SECTION_FALLBACK, "versions": None})


@pytest.mark.parametrize("key", ["dir", "to"])
def test_a_section_fallback_path_must_be_version_prefixed(key):
    with pytest.raises(ConfigError, match=r"must start with '\{version\}/'"):
        expand({**SECTION_FALLBACK, key: "meet"})


@pytest.mark.parametrize("to", ["{version}/meet/", "{version}/meet/docs/"])
def test_a_section_fallback_target_may_not_sit_inside_the_section(to):
    with pytest.raises(ConfigError, match="outside 'dir'"):
        expand({**SECTION_FALLBACK, "to": to})


def test_rejects_an_unknown_kind():
    with pytest.raises(ConfigError, match="'kind' must be one of"):
        expand({"id": "x", "kind": "wildcard", "at": "a", "to": "b"})


def test_rejects_a_key_belonging_to_another_kind():
    with pytest.raises(ConfigError, match="unknown keys: folders"):
        expand({**CROSS_PRODUCT, "folders": ["3.4.1"]})


def test_an_expansion_id_may_not_repeat_a_files_id():
    with pytest.raises(ConfigError, match="duplicate"):
        build(
            redirects={
                "files": [{"id": "moved", "at": "version-root", "to": "docs/"}],
                "expand": [CROSS_PRODUCT],
            }
        )


def test_cross_product_requires_a_versioned_at_naming_html():
    with pytest.raises(ConfigError, match=r"must start with '\{version\}/'"):
        expand({**CROSS_PRODUCT, "at": "docs/{area}/{provider}/index.html"})
    with pytest.raises(ConfigError, match="must name an HTML file"):
        expand({**CROSS_PRODUCT, "at": "{version}/docs/{area}/{provider}/"})


def test_cross_product_rejects_an_absolute_to():
    """The stub lives inside a version folder, which `latest` also serves."""
    with pytest.raises(ConfigError, match="'to' must be relative"):
        expand({**CROSS_PRODUCT, "to": "/latest/docs/install/"})


def test_cross_product_rejects_a_values_key_that_never_varies_the_path():
    """Every combination would claim the same page."""
    with pytest.raises(ConfigError, match="does not appear in 'at'"):
        expand({**CROSS_PRODUCT, "values": {**CROSS_PRODUCT["values"], "unused": ["x"]}})


def test_cross_product_rejects_an_undeclared_placeholder():
    with pytest.raises(ConfigError, match="undeclared placeholder"):
        expand({**CROSS_PRODUCT, "to": "{cloud}/install/"})


def test_cross_product_rejects_a_value_that_is_not_a_slug():
    """Values land in paths and URLs, so anything needing escaping is refused outright."""
    with pytest.raises(ConfigError, match="not a plain slug"):
        expand({**CROSS_PRODUCT, "values": {"area": ["a b"], "provider": ["aws"]}})


def test_tree_rename_rejects_nested_directories():
    with pytest.raises(ConfigError, match="must not nest"):
        expand(
            {
                "id": "rn",
                "kind": "tree-rename",
                "from": "{version}/docs/a",
                "to": "{version}/docs/a/b",
            }
        )


def test_version_alias_rejects_a_minor_folder():
    """A minor is a published folder, not an alias of one."""
    with pytest.raises(ConfigError, match="is a minor version name"):
        expand({"id": "va", "kind": "version-alias", "folders": ["3.4"]})


def test_version_alias_rejects_a_folder_claimed_twice():
    with pytest.raises(ConfigError, match="claimed by both"):
        expand(
            {"id": "a", "kind": "version-alias", "folders": ["3.4.1"]},
            {"id": "b", "kind": "version-alias", "folders": ["3.4.1"]},
        )


def test_only_one_unversioned_mirror_may_exist():
    with pytest.raises(ConfigError, match="only one unversioned-mirror"):
        expand(
            {"id": "a", "kind": "unversioned-mirror", "for_each": "versioned_pages"},
            {"id": "b", "kind": "unversioned-mirror", "for_each": "versioned_pages"},
        )


def test_mirror_for_each_must_name_a_layout_list():
    with pytest.raises(ConfigError, match="for_each must name a layout list"):
        expand({"id": "um", "kind": "unversioned-mirror", "for_each": "nope"})


@pytest.mark.parametrize("kind", ["version-alias", "unversioned-mirror"])
def test_the_unversioned_kinds_take_no_version_gate(kind):
    rule = {"id": "x", "kind": kind, "versions": ">=3.8"}
    rule |= {"folders": ["3.4.1"]} if kind == "version-alias" else {"for_each": "versioned_pages"}
    with pytest.raises(ConfigError, match="drop 'versions'"):
        expand(rule)


def test_the_real_config_declares_the_expansions(config):
    ids = [rule.id for rule in config.expand_rules]
    assert ids == [
        "removed-provider-index",
        "merged-single-node-upgrade",
        "split-single-node-upgrade",
        "single-node-pro-provider-pages-merged",
        "single-node-pro-provider-index-merged",
        "single-node-pro-provider-upgrade-merged",
        "meet-was-openvidu-call",
        "legacy-patch-folders",
        "unversioned-pages",
    ]
