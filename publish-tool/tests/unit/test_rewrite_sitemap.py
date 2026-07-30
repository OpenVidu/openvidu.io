"""The two sitemaps a publish produces: the root one, and the version's own pruned copy."""

from __future__ import annotations

from ovweb.rewrite.sitemap import promote_root_sitemap, prune_version_sitemap

VERSION = "3.8"

# The indentation is the one MkDocs actually emits (4 spaces for <url>, 9 for its children).
# It is asserted byte for byte, because the parity gate compares the sitemap as bytes.
SITEMAP = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
         <loc>https://openvidu.io/3.8/</loc>
         <lastmod>2026-07-16</lastmod>
    </url>
    <url>
         <loc>https://openvidu.io/3.8/docs/</loc>
         <lastmod>2026-07-16</lastmod>
    </url>
    <url>
         <loc>https://openvidu.io/3.8/pricing/</loc>
         <lastmod>2026-07-16</lastmod>
    </url>
    <url>
         <loc>https://openvidu.io/3.8/blog/a-post/</loc>
         <lastmod>2026-07-16</lastmod>
    </url>
</urlset>
"""


def locations(text):
    import re

    return re.findall(r"<loc>([^<]+)</loc>", text)


# -- promotion ---------------------------------------------------------------------------


def test_promotion_maps_all_three_url_shapes(layout):
    promoted = promote_root_sitemap(SITEMAP, version=VERSION, layout=layout)
    assert locations(promoted) == [
        "https://openvidu.io/",
        "https://openvidu.io/latest/docs/",
        "https://openvidu.io/pricing/",
        "https://openvidu.io/blog/a-post/",
    ]


def test_promotion_preserves_everything_else_byte_for_byte(layout):
    promoted = promote_root_sitemap(SITEMAP, version=VERSION, layout=layout)
    assert promoted.count("         <lastmod>2026-07-16</lastmod>\n") == 4
    assert promoted.endswith("</urlset>\n")


# -- pruning the version's own copy ------------------------------------------------------
#
# This file is fetched at runtime by the theme's version selector, which is what keeps a reader
# on the same page when they switch version. Two of these assertions are the feature itself:
# without the version-root entry, or with the root-served pages left in, the selector either
# resolves nothing or resolves to a 404. See ovweb/rewrite/sitemap.py.


def test_pruning_drops_the_root_served_pages(layout):
    pruned = prune_version_sitemap(SITEMAP, version=VERSION, layout=layout)
    assert locations(pruned) == [
        "https://openvidu.io/3.8/",
        "https://openvidu.io/3.8/docs/",
    ]


def test_pruning_keeps_the_version_root_entry(layout):
    """The selector takes the longest common prefix of every URL and requires it to be an entry.

    Drop this one line and the prefix is still `https://openvidu.io/3.8/` but is no longer in the
    file, so every version switch falls back to the version root — the whole feature off.
    """
    pruned = prune_version_sitemap(SITEMAP, version=VERSION, layout=layout)
    assert "<loc>https://openvidu.io/3.8/</loc>" in pruned


def test_pruning_preserves_indentation_byte_for_byte(layout):
    """The parity gate compares this file as bytes, so rejoining must not reflow anything."""
    pruned = prune_version_sitemap(SITEMAP, version=VERSION, layout=layout)
    assert pruned == (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "    <url>\n"
        "         <loc>https://openvidu.io/3.8/</loc>\n"
        "         <lastmod>2026-07-16</lastmod>\n"
        "    </url>\n"
        "    <url>\n"
        "         <loc>https://openvidu.io/3.8/docs/</loc>\n"
        "         <lastmod>2026-07-16</lastmod>\n"
        "    </url>\n"
        "</urlset>\n"
    )


def test_pruning_handles_a_url_entry_spanning_lines_unusually(layout):
    """The entries are matched as blocks rather than lines, so layout cannot fool it."""
    text = (
        "<urlset>\n"
        "  <url><loc>https://openvidu.io/3.8/docs/</loc></url>\n"
        "  <url>\n    <loc>https://openvidu.io/3.8/pricing/</loc>\n  </url>\n"
        "</urlset>\n"
    )
    assert locations(prune_version_sitemap(text, version=VERSION, layout=layout)) == [
        "https://openvidu.io/3.8/docs/"
    ]


def test_pruning_leaves_another_versions_urls_alone(layout):
    text = "<urlset>\n    <url><loc>https://openvidu.io/3.7/pricing/</loc></url>\n</urlset>\n"
    assert prune_version_sitemap(text, version=VERSION, layout=layout) == text
