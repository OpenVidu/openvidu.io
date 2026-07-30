"""Rewrites applied to the Markdown exports published beside every page.

The links these tests assert on are absolute, because that is the only form the exports use:
the llmstxt plugin resolves every link against the build's `site_url`, which mike makes
versioned. The HTML patterns match `href="…"`, so none of them reaches these files — which is
how 764 version-pinned links reached llms-full.txt while llms.txt held none.
"""

from __future__ import annotations

import pytest

from ovweb.rewrite.markdown import (
    repair_export_links,
    rewrite_promoted_markdown,
    rewrite_versioned_markdown,
)

VERSION = "3.8"


def versioned(text, layout):
    return rewrite_versioned_markdown(text, version=VERSION, layout=layout)


def promoted(text, layout):
    return rewrite_promoted_markdown(text, version=VERSION, layout=layout)


# llms.txt is a root-served Markdown file, so the promoted rules are exactly right for it.
llms = promoted


def repair(text, layout, exports=()):
    return repair_export_links(text, exports=frozenset(exports), layout=layout)


# -- the export of a versioned page ------------------------------------------------------


@pytest.mark.parametrize("page", ["docs", "meet"])
def test_versioned_export_keeps_links_inside_its_own_version(layout, page):
    """The mirror of the HTML rule: a reader who arrived at one version keeps reading it."""
    text = f"See [self-hosting](https://openvidu.io/3.8/{page}/self-hosting/index.md)."
    assert versioned(text, layout) == text


@pytest.mark.parametrize(
    "page", ["pricing", "support", "openvidu-meet-vs-openvidu-platform", "blog"]
)
def test_versioned_export_drops_the_version_from_a_root_page(layout, page):
    """These URLs are not merely stale — they have never existed, and return a hard 404."""
    text = f"See [it](https://openvidu.io/3.8/{page}/index.md)."
    assert versioned(text, layout) == f"See [it](https://openvidu.io/{page}/index.md)."


def test_versioned_export_drops_the_version_from_the_home_export(layout):
    text = "[OpenVidu](https://openvidu.io/3.8/index.md)"
    assert versioned(text, layout) == "[OpenVidu](https://openvidu.io/index.md)"


def test_versioned_export_leaves_another_version_alone(layout):
    """A release-notes page links back to the release before it, on purpose."""
    text = "[3.7 notes](https://openvidu.io/3.7/docs/releases/index.md)"
    assert versioned(text, layout) == text


def test_versioned_export_leaves_its_own_assets_pinned(layout):
    """Matching the HTML: the root /assets/ folder only ever holds the newest publish's copy."""
    text = "![diagram](https://openvidu.io/3.8/assets/images/x.png)"
    assert versioned(text, layout) == text


# -- the export of a page promoted to the root -------------------------------------------


@pytest.mark.parametrize("page", ["docs", "meet"])
def test_promoted_export_points_versioned_links_at_latest(layout, page):
    text = f"[docs](https://openvidu.io/3.8/{page}/self-hosting/index.md)"
    assert (
        promoted(text, layout) == f"[docs](https://openvidu.io/latest/{page}/self-hosting/index.md)"
    )


def test_promoted_export_drops_the_version_from_a_sibling_root_page(layout):
    text = "[pricing](https://openvidu.io/3.8/pricing/index.md)"
    assert promoted(text, layout) == "[pricing](https://openvidu.io/pricing/index.md)"


def test_promoted_export_leaves_another_version_alone(layout):
    """The one deliberate pin the rule must not touch: a link to a *previous* release."""
    text = "[3.7 notes](https://openvidu.io/3.7/docs/releases/index.md)"
    assert promoted(text, layout) == text


def test_promoted_export_does_not_shield_a_pin_to_the_published_version(layout):
    """Deliberately unlike the HTML, which does shield it.

    In Markdown an author's hand-written pin and the plugin's absolutised link are the same
    bytes, and the plugin wrote almost all of them, so they are treated as the plugin's. The
    HTML remains the place where author intent is preserved exactly.
    """
    text = "[observability](https://openvidu.io/3.8/docs/self-hosting/observability/)"
    assert promoted(text, layout) == (
        "[observability](https://openvidu.io/latest/docs/self-hosting/observability/)"
    )


# -- llms.txt and llms-full.txt ----------------------------------------------------------


def test_llms_file_three_way_mapping(layout):
    text = (
        "- [Self-hosting](https://openvidu.io/3.8/docs/self-hosting/): how to\n"
        "- [Pricing](https://openvidu.io/3.8/pricing/): plans\n"
        "- [Home](https://openvidu.io/3.8/index.md): landing\n"
    )
    assert llms(text, layout) == (
        "- [Self-hosting](https://openvidu.io/latest/docs/self-hosting/): how to\n"
        "- [Pricing](https://openvidu.io/pricing/): plans\n"
        "- [Home](https://openvidu.io/index.md): landing\n"
    )


def test_llms_file_absolutises_a_root_relative_target(layout):
    """These two files are read detached from the site, with no document URL left to resolve."""
    text = "See [PRO pricing](/pricing/#openvidu-pro) and ![clip](/assets/videos/x.mp4#only-light)."
    assert llms(text, layout) == (
        "See [PRO pricing](https://openvidu.io/pricing/#openvidu-pro) and "
        "![clip](https://openvidu.io/assets/videos/x.mp4#only-light)."
    )


def test_llms_file_leaves_a_protocol_relative_target_alone(layout):
    text = "[cdn](//cdn.example.com/x.js)"
    assert llms(text, layout) == text


def test_llms_file_leaves_a_root_relative_path_in_prose_alone(layout):
    """Anchored to Markdown link syntax, so a path quoted in prose or a code sample survives."""
    text = "Mount the config at `/etc/openvidu/config.yaml`, then read /var/log/openvidu."
    assert llms(text, layout) == text


def test_llms_file_leaves_an_external_link_alone(layout):
    text = "[LiveKit](https://docs.livekit.io/home/)"
    assert llms(text, layout) == text


def test_every_export_gets_root_relative_targets_absolutised(layout):
    """Not just the llms files: the plugin absolutises a *relative* link but returns a
    root-relative one untouched, so which form an export hands out came down to how the author
    happened to write it."""
    text = "[pricing](/pricing/#openvidu-pro)"
    want = "[pricing](https://openvidu.io/pricing/#openvidu-pro)"
    assert versioned(text, layout) == want
    assert promoted(text, layout) == want


# -- repairing links to exports that were never generated --------------------------------


def test_repair_points_a_missing_export_at_its_page(layout):
    """The plugin appends `index.md` to every directory link without checking it exists."""
    text = "[account](https://openvidu.io/account/index.md)"
    assert repair(text, layout) == "[account](https://openvidu.io/account/)"


def test_repair_leaves_an_export_that_exists_alone(layout):
    text = "[pricing](https://openvidu.io/pricing/index.md)"
    assert repair(text, layout, exports={"pricing/index.md"}) == text


def test_repair_keeps_the_fragment(layout):
    """The heading it pointed at exists on the HTML page too."""
    text = "[deep](https://openvidu.io/account/index.md#sign-up)"
    assert repair(text, layout) == "[deep](https://openvidu.io/account/#sign-up)"


def test_repair_handles_a_nested_path(layout):
    text = "[typedoc](https://openvidu.io/latest/docs/reference-docs/openvidu-components-angular/index.md)"
    assert repair(text, layout) == (
        "[typedoc](https://openvidu.io/latest/docs/reference-docs/openvidu-components-angular/)"
    )


def test_repair_resolves_latest_against_the_alias(layout):
    """A promoted export links to /latest/, never to the version, so the alias has to be in the
    set — the pipeline adds it from the symlink."""
    text = "[docs](https://openvidu.io/latest/docs/index.md)"
    assert repair(text, layout, exports={"latest/docs/index.md"}) == text


def test_repair_leaves_the_home_export_alone(layout):
    """`/index.md` is the home page's export and always exists."""
    text = "[home](https://openvidu.io/index.md)"
    assert repair(text, layout, exports={"index.md"}) == text


def test_repair_ignores_another_host(layout):
    text = "[external](https://docs.livekit.io/home/index.md)"
    assert repair(text, layout) == text


def test_repair_ignores_a_non_export_markdown_link(layout):
    """Only the `<directory>/index.md` shape the plugin emits is a candidate."""
    text = "[readme](https://openvidu.io/CONTRIBUTING.md)"
    assert repair(text, layout) == text
