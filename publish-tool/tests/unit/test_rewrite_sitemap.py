"""Promotion of a version sitemap to the site root."""

from __future__ import annotations

from ovweb.rewrite.sitemap import promote_root_sitemap

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
