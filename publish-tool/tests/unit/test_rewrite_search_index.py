"""Rewrites applied to `search/search_index.json`."""

from __future__ import annotations

import json

from ovweb.rewrite.search_index import promote_search_index, rewrite_search_index

VERSION = "3.8"


def rewrite(text, layout):
    return rewrite_search_index(text, version=VERSION, layout=layout)


def test_versioned_hits_keep_the_explicit_version(layout):
    """A versioned page loads the index beside it, so a hit must stay inside that version.

    Material's runtime `base` is left relative by the publish, so a page under /3.4/docs/ fetches
    /3.4/search/search_index.json. Repointing these at /latest/ would make searching inside 3.4
    return 3.8 pages. The *root* copy is repointed instead — see promote_search_index.
    """
    assert rewrite('{"location":"docs/self-hosting/"}', layout) == (
        '{"location":"/3.8/docs/self-hosting/"}'
    )
    assert rewrite('{"location":"meet/"}', layout) == '{"location":"/3.8/meet/"}'


def test_root_page_hits_lose_the_version(layout):
    assert rewrite('{"location":"pricing/"}', layout) == '{"location":"/pricing/"}'


def test_the_home_page_hit_becomes_the_root(layout):
    assert rewrite('{"location":""}', layout) == '{"location":"/"}'


def test_leaves_a_bare_anchor_alone(layout):
    """A section hit on the home page is an anchor, not a path."""
    assert rewrite('{"location":"#get-started"}', layout) == '{"location":"#get-started"}'


def test_leaves_an_already_absolute_location_alone(layout):
    text = '{"location":"/about-us/#micael-gallego"}'
    assert rewrite(text, layout) == text


def test_rewrites_a_realistic_index_and_keeps_it_valid_json(layout):
    original = {
        "config": {"lang": ["en"]},
        "docs": [
            {"location": "", "title": "Home"},
            {"location": "#home", "title": "Home section"},
            {"location": "docs/", "title": "Platform"},
            {"location": "meet/releases/", "title": "Meet releases"},
            {"location": "pricing/", "title": "Pricing"},
            {"location": "blog/a-post/", "title": "A post"},
        ],
    }
    rewritten = json.loads(rewrite(json.dumps(original, separators=(",", ":")), layout))
    assert [entry["location"] for entry in rewritten["docs"]] == [
        "/",
        "#home",
        "/3.8/docs/",
        "/3.8/meet/releases/",
        "/pricing/",
        "/blog/a-post/",
    ]


# -- promotion to the root index ---------------------------------------------------------


def test_promotion_points_versioned_hits_at_latest(layout):
    """The root index is served on the evergreen root pages, so a hit should not name a version
    that goes stale at the next release."""
    text = '{"location":"/3.8/docs/self-hosting/"},{"location":"/3.8/meet/"}'
    assert promote_search_index(text, version=VERSION, layout=layout) == (
        '{"location":"/latest/docs/self-hosting/"},{"location":"/latest/meet/"}'
    )


def test_promotion_leaves_root_page_hits_alone(layout):
    text = '{"location":"/pricing/"},{"location":"/"}'
    assert promote_search_index(text, version=VERSION, layout=layout) == text


def test_promotion_does_not_touch_indexed_page_text(layout):
    """A version number in a command sample or a release note is content, not a location."""
    text = '{"location":"/3.8/docs/","text":"run openvidu 3.8 and see /3.8/docs/ for more"}'
    assert promote_search_index(text, version=VERSION, layout=layout) == (
        '{"location":"/latest/docs/","text":"run openvidu 3.8 and see /3.8/docs/ for more"}'
    )


def test_promotion_leaves_another_version_alone(layout):
    """Only the version being published is repointed."""
    text = '{"location":"/3.4/docs/"}'
    assert promote_search_index(text, version=VERSION, layout=layout) == text
