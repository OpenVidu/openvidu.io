"""Turn a version's sitemap into the site-root sitemap.

Port of `updateSitemap` from push-new-version.sh. Its companion `updateVersionSitemap`, which
pruned the root-served pages out of each version's own sitemap, has no successor here: the
per-version sitemaps are not published at all any more. Nothing referenced them — `robots.txt`
names only the root sitemap, and that is a plain `urlset` rather than a sitemap index — so the
publish deletes them outright instead of maintaining them. See `pipeline/postprocess.py`.
"""

from __future__ import annotations

from ..model import SiteLayout


def promote_root_sitemap(text: str, *, version: str, layout: SiteLayout) -> str:
    """Turn a version's sitemap into the site-root sitemap.

    Versioned pages become `/latest/…` so the sitemap keeps naming one evergreen URL per page
    across releases; the promoted pages and the home page lose the version.
    """
    for page in layout.versioned_pages:
        text = text.replace(f"/{version}/{page}/", f"/latest/{page}/")
    for page in layout.non_versioned_pages:
        text = text.replace(f"/{version}/{page}/", f"/{page}/")
    return text.replace(f"/{version}/</loc>", "/</loc>")
