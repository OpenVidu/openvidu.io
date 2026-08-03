"""Redirect rule resolution and rendering."""

from __future__ import annotations

import re

import pytest

from ovweb.config import ConfigError, parse_site_config
from ovweb.redirects import (
    MIRROR_RULE_ID,
    RedirectError,
    mirror_redirects,
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


def build(files=(), patterns=(), defaults=None, mirror=None):
    redirects = {
        "defaults": defaults or {},
        "files": list(files),
        "patterns": list(patterns),
    }
    if mirror is not None:
        redirects["mirror"] = mirror
    return parse_site_config(
        {"schema": 1, "layout": MINIMAL_LAYOUT, "redirects": redirects},
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


# -- the unversioned mirror --------------------------------------------------------------

MIRROR = {"for_each": "versioned_pages", "body": "Redirecting to the current version…"}


def sitemap(*urls: str) -> str:
    """A sitemap in MkDocs' own shape: the URL indented onto its own line."""
    entries = "".join(f"    <url>\n         <loc>{url}</loc>\n    </url>\n" for url in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset>\n{entries}</urlset>\n'


def mirrored(*urls: str, mirror=MIRROR) -> dict[str, str]:
    """`{stub path: target}` for a promoted root sitemap holding `urls`."""
    resolved = mirror_redirects(sitemap(*urls), config=build(mirror=mirror))
    return {redirect.path: redirect.to for redirect in resolved}


def test_a_page_is_mirrored_at_the_same_path_without_the_version():
    assert mirrored("https://openvidu.io/latest/docs/ai/live-captions/") == {
        "docs/ai/live-captions/index.html": "/latest/docs/ai/live-captions/"
    }


def test_a_section_root_is_mirrored_too():
    """`/docs/` and `/meet/` are the two URLs the audit raised: the ones a human types."""
    assert mirrored("https://openvidu.io/latest/docs/", "https://openvidu.io/latest/meet/") == {
        "docs/index.html": "/latest/docs/",
        "meet/index.html": "/latest/meet/",
    }


@pytest.mark.parametrize(
    "url",
    [
        # Served from the root already, so a stub would shadow the real page.
        "https://openvidu.io/pricing/",
        # The home page.
        "https://openvidu.io/",
        # A version-pinned URL. Only `latest` is mirrored: an unversioned URL means "the current
        # one", and pinning the mirror to 3.8 would send visitors to a stale page next release.
        "https://openvidu.io/3.8/docs/",
        # Another site.
        "https://example.com/latest/docs/",
        # A section this site does not have.
        "https://openvidu.io/latest/blog/",
    ],
)
def test_only_versioned_pages_under_latest_are_mirrored(url):
    assert mirrored(url) == {}


def test_a_url_naming_a_file_is_left_to_the_404_router():
    """The stub path is the URL plus `index.html`, which is wrong for a file URL. The exported
    reference-docs pages are the real case, and they are not in the sitemap."""
    assert mirrored("https://openvidu.io/latest/docs/reference/api.html") == {}


def test_the_order_follows_the_sitemap():
    urls = [f"https://openvidu.io/latest/docs/{name}/" for name in ("c", "a", "b")]
    resolved = mirror_redirects(sitemap(*urls), config=build(mirror=MIRROR))
    assert [redirect.path for redirect in resolved] == [
        "docs/c/index.html",
        "docs/a/index.html",
        "docs/b/index.html",
    ]


def test_a_repeated_url_yields_one_stub():
    url = "https://openvidu.io/latest/docs/"
    assert len(mirror_redirects(sitemap(url, url), config=build(mirror=MIRROR))) == 1


def test_the_stub_carries_the_seo_signals_that_make_it_a_redirect():
    redirect = mirror_redirects(
        sitemap("https://openvidu.io/latest/docs/"), config=build(mirror=MIRROR)
    )[0]

    assert redirect.rule_id == MIRROR_RULE_ID
    assert redirect.canonical == "https://openvidu.io/latest/docs/"
    assert redirect.robots == "noindex, follow"
    assert redirect.body == MIRROR["body"]
    # Absolute, because a root-level stub is served from exactly one URL — unlike the rules
    # installed inside a version folder, which `latest` makes answer at two.
    assert redirect.relative is False
    # The fragment is what the shipped agent-configuration link carries.
    assert redirect.preserve_query_and_hash is True


def test_the_rendered_stub_redirects_and_stays_out_of_the_index():
    redirect = mirror_redirects(
        sitemap("https://openvidu.io/latest/meet/embedded/"), config=build(mirror=MIRROR)
    )[0]
    page = render_redirect(redirect)

    assert '<meta http-equiv="refresh" content="0; url=/latest/meet/embedded/">' in page
    assert '<meta name="robots" content="noindex, follow">' in page
    assert '<a href="/latest/meet/embedded/">' in page


def test_no_mirror_is_configured_means_no_stubs():
    assert mirror_redirects(sitemap("https://openvidu.io/latest/docs/"), config=build()) == ()


def test_a_disabled_mirror_produces_no_stubs():
    assert mirrored("https://openvidu.io/latest/docs/", mirror={**MIRROR, "enabled": False}) == {}


def test_an_empty_sitemap_produces_no_stubs():
    assert mirrored() == {}


# -- version bands whose target arrived later --------------------------------------------


MEET_REORGANISATION_RULES = (
    "moved-meet-features-users",
    "moved-meet-features-rooms",
    "moved-meet-features-live-captions",
    "moved-meet-features-recordings",
)


def test_the_meet_reorganisation_rules_start_at_3_8_not_3_7(config):
    """The pages these rules replace are still published in a correct 3.7, so a stub installed
    there would overwrite a real page.

    For six weeks the 3.7 folder appeared not to have them, which is what made these gates look
    like 3.7 in the first place. One blog branch had been cut from `next` rather than `main`, so
    merging it (2481b7146) brought 14 of 3.8's documentation commits into `main`, and the next
    3.7 publish served them. The gate describes the release a change belongs to; the folder is
    only evidence of what was published.
    """
    for version in ("3.6", "3.7"):
        installed = {item.rule_id for item in resolve_file_redirects(config, version)}
        assert not installed & set(MEET_REORGANISATION_RULES), version

    installed = {item.rule_id for item in resolve_file_redirects(config, "3.8")}
    assert set(MEET_REORGANISATION_RULES) <= installed


def test_both_oracle_tutorial_rules_start_at_3_7(config):
    """The counter-examples, and why the gates were checked one by one rather than as a batch.

    Neither page comes back when 3.7 is rebuilt. The PRO one was removed before 3.7 shipped
    (2026-05-18) and its folder was correctly rebuilt without it. The community one was removed
    as *outdated* during 3.7's life — the deletion only reached `main` with the 3.8 batch, but
    resurrecting instructions the team had already found wrong is not what fixing 3.7 means, so
    the rebuild keeps it deleted and this rule covers the URL.
    """
    installed = {item.rule_id for item in resolve_file_redirects(config, "3.7")}
    assert "removed-oracle-install-tutorial-pro" in installed
    assert "removed-oracle-install-tutorial-community" in installed


#: Dead URLs left without a rule on purpose. The first five were never part of a release —
#: they reached the site only through the 3.7 folder while it served mis-branched 3.8
#: documentation, and 3.8 renamed them before shipping — so a redirect would preserve URLs that
#: should not have existed. The last is a generated API page for a deleted class, one release long.
DELIBERATELY_UNCOVERED = {
    "meet/embedded/tutorials/external-members/",
    "meet/embedded/tutorials/registered-members/",
    "meet/features/rooms/creation-management/",
    "meet/features/recordings/creation-management/",
    "meet/features/rooms/appearance/",
    "docs/reference-docs/openvidu-components-angular/injectables/E2eeService.html",
}


def test_every_dead_page_of_every_version_has_a_rule(config):
    """The rules were derived by scanning the version folders for pages 3.8 no longer has, so the
    newest publish must cover all of them bar the exclusions above. Restated here as the set the
    scan produced: a rule quietly dropped from ovweb.yaml would otherwise reinstate a 404 that
    used to rank, and an exclusion quietly gaining a rule would revive a URL we chose to retire."""
    dead = {
        # Found by a Search Console export (PR #108).
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
        # Found by scanning every version folder for what 3.8 does not serve.
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
