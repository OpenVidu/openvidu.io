"""Turn a version's sitemap into the site-root sitemap.

The root sitemap is the only one published: `robots.txt` names it, and it is a plain `urlset`
rather than a sitemap index, so it has to list every URL itself. A version's own copy is
advertised to nobody, and the publish deletes it — see `pipeline/postprocess.py`.
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
