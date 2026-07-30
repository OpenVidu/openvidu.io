"""Rewrites applied to the Markdown exports published beside every page.

The links these tests assert on are absolute, because that is the only form the exports use:
the llmstxt plugin resolves every link against the build's `site_url`, which mike makes
versioned. The HTML patterns match `href="…"`, so none of them reaches these files — which is
how 764 version-pinned links reached llms-full.txt while llms.txt held none.
"""

from __future__ import annotations

import pytest

from ovweb.rewrite.markdown import (
    rewrite_llms_file,
    rewrite_promoted_markdown,
    rewrite_versioned_markdown,
)

VERSION = "3.8"


def versioned(text, layout):
    return rewrite_versioned_markdown(text, version=VERSION, layout=layout)


def promoted(text, layout):
    return rewrite_promoted_markdown(text, version=VERSION, layout=layout)


def llms(text, layout):
    return rewrite_llms_file(text, version=VERSION, layout=layout)


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


def test_llms_file_is_the_promoted_rules_plus_absolutising(layout):
    """Stated as a test so the two cannot drift: llms-full.txt is a root file like any other."""
    text = "[docs](https://openvidu.io/3.8/docs/) [pricing](/pricing/)"
    assert llms(text, layout) == (
        promoted("[docs](https://openvidu.io/3.8/docs/)", layout)
        + " [pricing](https://openvidu.io/pricing/)"
    )
