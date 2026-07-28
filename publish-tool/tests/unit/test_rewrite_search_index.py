"""Rewrites applied to `search/search_index.json`."""

from __future__ import annotations

import json

from ovweb.rewrite.search_index import rewrite_search_index

VERSION = "3.8"


def rewrite(text, layout):
    return rewrite_search_index(text, version=VERSION, layout=layout)


def test_versioned_hits_keep_the_explicit_version(layout):
    """Deliberate asymmetry with the page links, which use `/latest/`.

    A search hit describes the page that was indexed. `latest` moves at the next release, so
    pinning the version is what keeps an indexed hit pointing at what was indexed. Do not
    "fix" this to `/latest/` without also deciding what happens to the root index, which is
    a copy of the newest version's.
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
