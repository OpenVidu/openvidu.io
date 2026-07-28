"""Redirect rule resolution and rendering."""

from __future__ import annotations

import re

import pytest

from ovweb.config import ConfigError, parse_site_config
from ovweb.redirects import (
    RedirectError,
    render_redirect,
    resolve_file_redirects,
    resolve_patterns,
)

MINIMAL_LAYOUT = {
    "site_url": "https://openvidu.io",
    "versioned_pages": ["docs", "meet"],
    "non_versioned_pages": ["pricing"],
    "assets": ["assets"],
    "pinned_assets": ["assets"],
    "root_files": ["index.html"],
    "feeds": [],
}


def build(files=(), patterns=(), defaults=None):
    return parse_site_config(
        {
            "schema": 1,
            "layout": MINIMAL_LAYOUT,
            "redirects": {
                "defaults": defaults or {},
                "files": list(files),
                "patterns": list(patterns),
            },
        },
        source="<test>",
    )


def only(config, version):
    resolved = resolve_file_redirects(config, version)
    assert len(resolved) == 1, resolved
    return resolved[0]


# -- the real configuration --------------------------------------------------------------


@pytest.mark.parametrize(
    ("version", "expected"),
    [
        ("3.0", "docs/getting-started/"),
        ("3.3", "docs/getting-started/"),
        ("3.4", "docs/"),
        ("3.8", "docs/"),
        # Version ordering, not string ordering: "3.10" < "3.4" as a string.
        ("3.10", "docs/"),
    ],
)
def test_version_root_target_per_band(config, version, expected):
    resolved = {item.rule_id: item for item in resolve_file_redirects(config, version)}
    assert resolved["version-root"].to == expected
    assert resolved["version-root"].path == f"{version}/index.html"


def test_legacy_prerelease_versions_fall_in_the_old_band(config):
    """`3.0.0-beta1` normalises to `3.0.0b1`, which a specifier set excludes unless
    pre-releases are allowed. Getting this wrong would silently send those folders to a
    /docs/ page that never existed."""
    resolved = {item.rule_id: item for item in resolve_file_redirects(config, "3.0.0-beta1")}
    assert resolved["version-root"].to == "docs/getting-started/"


def test_getting_started_redirect_only_exists_from_3_4(config):
    ids_new = {item.rule_id for item in resolve_file_redirects(config, "3.8")}
    ids_old = {item.rule_id for item in resolve_file_redirects(config, "3.2")}
    assert "platform-getting-started" in ids_new
    assert "platform-getting-started" not in ids_old
    assert "legacy-docs-index" in ids_old
    assert "legacy-docs-index" not in ids_new


def test_every_real_target_is_relative(config):
    for version in ("3.0", "3.2", "3.4", "3.8"):
        for redirect in resolve_file_redirects(config, version):
            assert not redirect.to.startswith("/"), (version, redirect.rule_id, redirect.to)


def test_every_real_canonical_is_absolute(config):
    for version in ("3.0", "3.8"):
        for redirect in resolve_file_redirects(config, version):
            assert redirect.canonical.startswith("https://openvidu.io/")


# -- resolution rules --------------------------------------------------------------------


def test_named_version_root_location():
    config = build([{"id": "r", "at": "version-root", "to": "docs/"}])
    assert only(config, "3.8").path == "3.8/index.html"


def test_path_template_interpolates_the_version():
    config = build([{"id": "r", "at": "{version}/docs/x/index.html", "to": "../"}])
    assert only(config, "3.8").path == "3.8/docs/x/index.html"


def test_canonical_interpolates_site_url_and_version():
    config = build(
        [{"id": "r", "at": "version-root", "to": "docs/", "canonical": "{site_url}/{version}/x/"}]
    )
    assert only(config, "3.8").canonical == "https://openvidu.io/3.8/x/"


def test_rule_level_version_gate():
    config = build([{"id": "r", "at": "version-root", "to": "docs/", "versions": "<3.4"}])
    assert resolve_file_redirects(config, "3.2")
    assert resolve_file_redirects(config, "3.8") == ()


def test_override_replaces_only_the_fields_it_names():
    config = build(
        [
            {
                "id": "r",
                "at": "version-root",
                "to": "docs/",
                "body": "new",
                "canonical": "{site_url}/latest/docs/",
                "when": [{"versions": "<3.4", "to": "docs/getting-started/", "body": "old"}],
            }
        ]
    )
    old = only(config, "3.2")
    new = only(config, "3.8")
    assert (old.to, old.body) == ("docs/getting-started/", "old")
    assert (new.to, new.body) == ("docs/", "new")
    # Not overridden, so inherited from the rule in both.
    assert old.canonical == new.canonical == "https://openvidu.io/latest/docs/"


def test_override_can_disable_the_rule_for_a_band():
    config = build(
        [
            {
                "id": "r",
                "at": "version-root",
                "to": "docs/",
                "when": [{"versions": "<3.4", "enabled": False}],
            }
        ]
    )
    assert resolve_file_redirects(config, "3.2") == ()
    assert resolve_file_redirects(config, "3.8")


def test_overlapping_bands_are_an_error_not_first_match_wins():
    """Silently taking the first match would make the published redirect depend on file order."""
    config = build(
        [
            {
                "id": "r",
                "at": "version-root",
                "to": "docs/",
                "when": [
                    {"versions": "<3.4", "to": "a/"},
                    {"versions": "<3.9", "to": "b/"},
                ],
            }
        ]
    )
    with pytest.raises(RedirectError, match="ambiguous"):
        resolve_file_redirects(config, "3.2")
    # Only one band matches 3.8, so it still resolves.
    assert only(config, "3.8").to == "b/"


def test_absolute_target_is_rejected_when_relative():
    """The /latest/ symlink is the reason: an absolute target leaks the version number."""
    config = build([{"id": "r", "at": "version-root", "to": "/3.8/docs/"}])
    with pytest.raises(RedirectError, match="relative"):
        resolve_file_redirects(config, "3.8")


def test_absolute_target_is_allowed_when_declared_not_relative():
    config = build([{"id": "r", "at": "version-root", "to": "/docs/", "relative": False}])
    assert only(config, "3.8").to == "/docs/"


def test_relative_canonical_is_rejected():
    config = build([{"id": "r", "at": "version-root", "to": "docs/", "canonical": "/docs/"}])
    with pytest.raises(RedirectError, match="absolute URL"):
        resolve_file_redirects(config, "3.8")


@pytest.mark.parametrize("target", ['a"b/', "a<b/", "a b/", "a'b/"])
def test_a_target_that_could_break_out_of_its_context_is_rejected(target):
    """The target lands in an attribute, a meta content value and a JavaScript string."""
    config = build([{"id": "r", "at": "version-root", "to": target}])
    with pytest.raises(RedirectError, match="must not contain"):
        resolve_file_redirects(config, "3.8")


def test_config_rejects_a_non_html_at_path():
    with pytest.raises(ConfigError, match="HTML file"):
        build([{"id": "r", "at": "{version}/docs/", "to": "../"}])


def test_config_rejects_duplicate_rule_ids():
    with pytest.raises(ConfigError, match="duplicate"):
        build(
            [
                {"id": "r", "at": "version-root", "to": "a/"},
                {"id": "r", "at": "{version}/x/index.html", "to": "b/"},
            ]
        )


# -- rendering ---------------------------------------------------------------------------


def test_rendered_page_has_everything_a_crawler_needs(config):
    html = render_redirect(only_version_root(config, "3.8"))
    assert '<meta http-equiv="refresh" content="0; url=docs/">' in html
    assert '<meta name="robots" content="noindex, follow">' in html
    assert '<link rel="canonical" href="https://openvidu.io/latest/docs/">' in html
    assert '<a href="docs/">' in html
    assert html.startswith("<!DOCTYPE html>")
    assert html.endswith("\n")


def test_rendered_javascript_is_not_html_escaped(config):
    """Inside <script> the content is raw text, so `&#34;` would be a syntax error."""
    html = render_redirect(only_version_root(config, "3.8"))
    script = html.split("<script>", 1)[1].split("</script>", 1)[0]
    assert 'new URL("docs/", location.href)' in script
    assert "&#34;" not in script
    assert "&amp;" not in script


def test_rendered_javascript_uses_replace_and_forwards_query_and_hash(config):
    script = render_redirect(only_version_root(config, "3.8")).split("<script>", 1)[1]
    assert "location.replace(" in script
    assert "location.href =" not in script
    assert "location.search" in script
    assert "location.hash" in script


def test_rendered_page_never_contains_an_absolute_target(config):
    """This is the /latest/ invariant, checked on the rendered bytes."""
    for version in ("3.0", "3.8"):
        for redirect in resolve_file_redirects(config, version):
            html = render_redirect(redirect)
            assert 'content="0; url=/' not in html
            assert not re.search(r'<a href="/', html)


def test_query_forwarding_can_be_switched_off():
    config = build(
        [{"id": "r", "at": "version-root", "to": "docs/", "preserve_query_and_hash": False}]
    )
    assert "location.search" not in render_redirect(only(config, "3.8"))


def test_canonical_can_be_omitted():
    config = build([{"id": "r", "at": "version-root", "to": "docs/"}])
    assert 'rel="canonical"' not in render_redirect(only(config, "3.8"))


def only_version_root(config, version):
    return next(
        item for item in resolve_file_redirects(config, version) if item.rule_id == "version-root"
    )


# -- 404 patterns ------------------------------------------------------------------------


def test_patterns_expand_per_versioned_page(config):
    ids = [pattern.id for pattern in resolve_patterns(config)]
    assert "unversioned-versioned-page:docs" in ids
    assert "unversioned-versioned-page:meet" in ids


def test_patterns_keep_config_order(config):
    """The router stops at the first match, so order is behaviour."""
    ids = [pattern.id for pattern in resolve_patterns(config)]
    assert ids.index("legacy-patch-version-root") < ids.index("unversioned-versioned-page:docs")


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/3.4.1", "/3.4/"),
        ("/3.4.1/", "/3.4/"),
        ("/3.4.1/docs/self-hosting/", "/3.4/docs/self-hosting/"),
        ("/3.0.0-beta2/docs/", "/3.0/docs/"),
        ("/docs/self-hosting/", "/latest/docs/self-hosting/"),
        ("/meet/", "/latest/meet/"),
    ],
)
def test_patterns_produce_the_documented_redirects(config, path, expected):
    """Evaluated with Python's regex engine, which agrees with JavaScript on these patterns.

    `/3.4.1` with no trailing path is the case the single-rule version got wrong: replacing an
    unmatched group yields "" in JavaScript, so it produced "/3.4" instead of "/3.4/".
    """
    for pattern in resolve_patterns(config):
        compiled = re.compile(pattern.match)
        if compiled.match(path):
            replacement = re.sub(r"\$(\d)", r"\\\1", pattern.to)
            assert compiled.sub(replacement, path) == expected
            return
    raise AssertionError(f"no pattern matched {path}")


@pytest.mark.parametrize("path", ["/", "/pricing/", "/latest/docs/", "/3.8/docs/", "/docs"])
def test_patterns_leave_valid_paths_alone(config, path):
    for pattern in resolve_patterns(config):
        assert not re.compile(pattern.match).match(path), (pattern.id, path)
