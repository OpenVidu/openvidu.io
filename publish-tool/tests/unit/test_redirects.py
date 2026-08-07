"""Redirect rule resolution and rendering."""

from __future__ import annotations

import re

import pytest

from ovweb.config import ConfigError, parse_site_config
from ovweb.redirects import RedirectError, render_redirect, resolve_file_redirects

MINIMAL_LAYOUT = {
    "site_url": "https://openvidu.io",
    "versioned_pages": ["docs", "meet"],
    "non_versioned_pages": ["pricing"],
    "assets": ["assets"],
    "pinned_assets": ["assets"],
    "root_files": ["index.html"],
    "feeds": [],
}


def build(files=(), defaults=None):
    return parse_site_config(
        {
            "schema": 2,
            "layout": MINIMAL_LAYOUT,
            "redirects": {"defaults": defaults or {}, "files": list(files)},
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


def test_an_at_path_without_the_placeholder_is_used_verbatim():
    """A rule can name one fixed location instead of one per version."""
    config = build([{"id": "r", "at": "docs/index.html", "to": "latest/docs/", "relative": False}])
    assert only(config, "3.8").path == "docs/index.html"
    assert only(config, "3.2").path == "docs/index.html"


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


def test_a_target_may_carry_a_fragment():
    """Converging pages land on the section that absorbed them, not just the page."""
    config = build([{"id": "r", "at": "{version}/docs/faq/index.html", "to": "../how-to/#backup"}])
    resolved = only(config, "3.8")
    assert resolved.to == "../how-to/#backup"

    page = render_redirect(resolved)
    assert '<meta http-equiv="refresh" content="0; url=../how-to/#backup">' in page
    assert '<a href="../how-to/#backup">' in page


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


# -- version bands whose target arrived later --------------------------------------------


MEET_REORGANISATION_RULES = (
    "moved-meet-features-users",
    "moved-meet-features-rooms",
    "moved-meet-features-live-captions",
    "moved-meet-features-recordings",
)


def test_the_meet_reorganisation_rules_start_at_3_8_not_3_7(config):
    """The reorganisation shipped in 3.8, and 3.7 still publishes the pages these rules replace,
    so a stub installed there would overwrite a real page.

    A rule's gate follows the release a change belongs to. What a version folder currently holds is
    evidence of what was published, which is not the same thing.
    """
    for version in ("3.6", "3.7"):
        installed = {item.rule_id for item in resolve_file_redirects(config, version)}
        assert not installed & set(MEET_REORGANISATION_RULES), version

    installed = {item.rule_id for item in resolve_file_redirects(config, "3.8")}
    assert set(MEET_REORGANISATION_RULES) <= installed


def test_both_oracle_tutorial_rules_start_at_3_7(config):
    """Neither Oracle install tutorial comes back when 3.7 is rebuilt, so both are redirected.

    The PRO one was removed before 3.7 shipped. The community one was removed *during* 3.7's life
    as outdated, and a rebuild keeps it deleted rather than resurrecting instructions the team had
    already found wrong — which is why the two gates were decided one at a time.
    """
    installed = {item.rule_id for item in resolve_file_redirects(config, "3.7")}
    assert "removed-oracle-install-tutorial-pro" in installed
    assert "removed-oracle-install-tutorial-community" in installed


#: Dead URLs left without a rule on purpose. The first five were never part of a release: they
#: reached the site only through a version folder that briefly served unreleased documentation, and
#: were renamed before shipping, so redirecting them would preserve URLs that should not have
#: existed. The last is a generated API page for a class that was deleted.
DELIBERATELY_UNCOVERED = {
    "meet/embedded/tutorials/external-members/",
    "meet/embedded/tutorials/registered-members/",
    "meet/features/rooms/creation-management/",
    "meet/features/recordings/creation-management/",
    "meet/features/rooms/appearance/",
    "docs/reference-docs/openvidu-components-angular/injectables/E2eeService.html",
}


def test_every_dead_page_of_every_version_has_a_rule(config):
    """Every URL a published version folder holds and the newest does not needs a rule, or the
    exclusion above.

    Fails both ways: a rule quietly dropped from ovweb.yaml reinstates a 404 that used to rank, and
    an exclusion quietly gaining one revives a URL that was retired on purpose.
    """
    dead = {
        # Found by checking a Search Console export against the live site.
        "docs/self-hosting/faq/",
        "docs/self-hosting/how-to-guides/force-443-tls/",
        "docs/self-hosting/single-node/oracle/install-tutorial/",
        "docs/self-hosting/single-node-pro/oracle/install-tutorial/",
        "meet/embedded/tutorials/direct-link/",
        "meet/embedded/tutorials/recordings/",
        "meet/embedded/tutorials/webcomponent/",
        "meet/embedded/tutorials/webcomponent-advanced/",
        "meet/embedded/tutorials/webhooks/",
        "meet/features/live-captions/",
        "meet/features/recordings/",
        "meet/features/rooms-and-meetings/",
        "meet/features/users-and-permissions/",
        # Found by scanning every version folder for what the newest does not serve.
        "docs/openvidu-call/",
        "docs/openvidu-call/docs/",
        "docs/tutorials/advanced-features/recording-advanced/",
        "docs/tutorials/advanced-features/recording-basic/",
        *DELIBERATELY_UNCOVERED,
    }
    installed = set()
    for item in resolve_file_redirects(config, "3.8"):
        path = item.path[len("3.8/") :]
        installed.add(path[: -len("index.html")] if path.endswith("/index.html") else path)

    assert not dead - installed - DELIBERATELY_UNCOVERED, (
        f"no rule covers {sorted(dead - installed - DELIBERATELY_UNCOVERED)}"
    )
    revived = installed & DELIBERATELY_UNCOVERED
    assert not revived, f"these were retired on purpose, not to be redirected: {sorted(revived)}"
