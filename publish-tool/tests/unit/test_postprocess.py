"""The post-processing pipeline over a synthetic built tree.

Covers the wiring the unit tests cannot: step order, what moves versus what is copied, and
the difference between publishing the newest version and re-publishing an older one.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import pytest

from ovweb.pipeline.postprocess import PostprocessError, postprocess
from ovweb.releases import ARTICLE_MARKER, TOC_MARKER
from ovweb.report import Reporter

VERSION = "3.9"
OLD_VERSION = "3.2"


def releases_page(notes: str, chrome: str) -> str:
    toc = f'{TOC_MARKER}<a href="#n">{notes}</a></nav>' * 2
    return (
        f'<html><head><link rel="canonical" href="https://openvidu.io/{chrome}/docs/releases/">'
        f"</head><body>{toc}{ARTICLE_MARKER}<h2>{notes}</h2></article>"
        f'<a class="chrome" href="/{chrome}/assets/logo.png">{chrome}</a></body></html>'
    )


def build_tree(root: Path, layout, *, version: str, modern: bool = True) -> None:
    """Write a folder shaped like raw `mike` output for one version.

    Driven by the real layout so the fixture cannot drift from the configuration: adding a
    page to ovweb.yaml automatically gets one here too.
    """
    base = root / version
    (base / "docs" / "releases").mkdir(parents=True)
    (base / "overrides").mkdir()
    for asset in layout.assets:
        (base / asset).mkdir()
    for page in layout.non_versioned_pages:
        (base / page).mkdir()
        # Every promoted page carries its own canonical URL and a link into the docs, which is
        # what the promotion rewrite has to fix.
        (base / page / "index.html").write_text(
            f'<link rel="canonical" href="https://openvidu.io/{version}/{page}/">'
            f'<a href="../docs/">Docs</a>',
            encoding="utf-8",
        )
        # ...and the Markdown export the llmstxt plugin writes beside it, where the same two
        # links are already absolute — and therefore version-pinned by the build.
        (base / page / "index.md").write_text(
            f"[Docs](https://openvidu.io/{version}/docs/index.md)\n"
            f"[Support](https://openvidu.io/{version}/support/index.md)\n",
            encoding="utf-8",
        )

    (base / "overrides" / "main.html").write_text("theme source", encoding="utf-8")
    (base / "assets" / "logo.png").write_bytes(b"\x89PNG\x00binary")
    (base / "javascripts" / "app.js").write_text('fetch("/assets/x.json")', encoding="utf-8")
    (base / "stylesheets" / "extra.css").write_text("body{}", encoding="utf-8")

    (base / "docs" / "index.html").write_text(
        f'<link rel="canonical" href="https://openvidu.io/{version}/docs/">'
        f'<img src="/assets/logo.png">'
        f'<a href="../pricing/">Pricing</a>'
        f'<a href="..">Home</a>'
        f'<link rel="alternate" type="application/rss+xml" href="../feed_rss_created.xml">'
        f'<script>new URL("../..",location)</script>',
        encoding="utf-8",
    )
    # The export beside the page above. Its links are absolute where the HTML's are relative,
    # so the HTML patterns cannot reach them: a link into its own version stays pinned, a link
    # to a page served only from the root must lose the version.
    (base / "docs" / "index.md").write_text(
        f"[Self-hosting](https://openvidu.io/{version}/docs/self-hosting/index.md)\n"
        f"[Pricing](https://openvidu.io/{version}/pricing/index.md)\n"
        f"[Home](https://openvidu.io/{version}/index.md)\n",
        encoding="utf-8",
    )
    (base / "docs" / "releases" / "index.html").write_text(
        releases_page(f"{version}.0 notes", version), encoding="utf-8"
    )
    (base / "index.html").write_text(
        f'<link rel="canonical" href="https://openvidu.io/{version}/"><a href="docs/">Docs</a>',
        encoding="utf-8",
    )
    (base / "index.md").write_text(
        f"# Home\n[Docs](https://openvidu.io/{version}/docs/index.md)\n"
        f"[Pricing](https://openvidu.io/{version}/pricing/index.md)\n",
        encoding="utf-8",
    )
    (base / "404.html").write_text(
        f'<a href="/{version}/pricing/">p</a><a href="/{version}/docs/">d</a>'
        f'<a href="/{version}">h</a>',
        encoding="utf-8",
    )
    (base / "robots.txt").write_text("Allow: /\n", encoding="utf-8")
    # The blog additionally holds an author-pinned release-notes link, which must survive the
    # version strip applied to the rest of the page.
    (base / "blog" / "index.html").write_text(
        f'<link rel="canonical" href="https://openvidu.io/{version}/blog/">'
        f'<a href="https://openvidu.io/3.4/docs/releases/">3.4 notes</a>',
        encoding="utf-8",
    )
    (base / "search" / "search_index.json").write_text(
        json.dumps(
            {"docs": [{"location": ""}, {"location": "docs/"}, {"location": "pricing/"}]},
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )
    (base / "sitemap.xml").write_text(
        "<urlset>\n"
        f"    <url>\n         <loc>https://openvidu.io/{version}/</loc>\n    </url>\n"
        f"    <url>\n         <loc>https://openvidu.io/{version}/docs/</loc>\n    </url>\n"
        f"    <url>\n         <loc>https://openvidu.io/{version}/pricing/</loc>\n    </url>\n"
        "</urlset>\n",
        encoding="utf-8",
    )

    if modern:
        (base / "llms.txt").write_text(
            f"- [Docs](https://openvidu.io/{version}/docs/): d\n"
            f"- [Getting started](https://openvidu.io/{version}/docs/getting-started/): gs\n"
            f"- [Pricing](https://openvidu.io/{version}/pricing/): p\n",
            encoding="utf-8",
        )
        # The concatenation of every export above. Same links, plus the root-relative ones that
        # only resolve while the file is read at a URL — which this one never is.
        (base / "llms-full.txt").write_text(
            f"# Docs\n[Self-hosting](https://openvidu.io/{version}/docs/self-hosting/index.md)\n"
            f"[Pricing](https://openvidu.io/{version}/pricing/index.md)\n"
            "[PRO](/pricing/#openvidu-pro)\n",
            encoding="utf-8",
        )
        for feed in (
            "feed_rss_created.xml",
            "feed_rss_updated.xml",
            "feed_json_created.json",
            "feed_json_updated.json",
        ):
            (base / feed).write_text(f"https://openvidu.io/{version}/blog/x/", encoding="utf-8")
        (base / "rss.xsl").write_text("<xsl/>", encoding="utf-8")


@pytest.fixture
def report():
    return Reporter(verbosity=0, color=False)


@pytest.fixture
def latest_tree(tmp_path, layout):
    build_tree(tmp_path, layout, version=VERSION)
    (tmp_path / "versions.json").write_text(
        json.dumps([{"version": VERSION, "aliases": ["latest"]}]), encoding="utf-8"
    )
    return tmp_path


# -- publishing the newest version -------------------------------------------------------


def test_promotes_pages_and_files_to_the_root(latest_tree, config, report):
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    assert (latest_tree / "pricing" / "index.html").is_file()
    assert (latest_tree / "blog" / "index.html").is_file()
    assert (latest_tree / "robots.txt").is_file()
    assert (latest_tree / "llms.txt").is_file()
    # Moved, so gone from the version folder.
    assert not (latest_tree / VERSION / "pricing").exists()
    assert not (latest_tree / VERSION / "robots.txt").exists()


def test_copies_assets_but_keeps_the_version_copy(latest_tree, config, report):
    """The version folder must keep its assets — that is what the pinning points at."""
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    assert (latest_tree / "assets" / "logo.png").is_file()
    assert (latest_tree / VERSION / "assets" / "logo.png").is_file()


def test_removes_the_theme_override_folder(latest_tree, config, report):
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)
    assert not (latest_tree / VERSION / "overrides").exists()


def test_rewrites_the_versioned_pages(latest_tree, config, report):
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    page = (latest_tree / VERSION / "docs" / "index.html").read_text()
    assert f'src="/{VERSION}/assets/logo.png"' in page
    assert 'href="/pricing/"' in page
    assert 'href="/"' in page
    assert 'new URL("/",location)' in page
    assert 'href="https://openvidu.io/latest/docs/"' in page
    # The feeds are promoted to the root, so a version-relative link would 404.
    assert 'href="/feed_rss_created.xml"' in page


def test_does_not_corrupt_a_binary_asset(latest_tree, config, report):
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)
    assert (latest_tree / VERSION / "assets" / "logo.png").read_bytes() == b"\x89PNG\x00binary"


def test_installs_the_version_root_redirect_after_promotion(latest_tree, config, report):
    """The built home page is promoted to the root first; the redirect then takes its place."""
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    root_home = (latest_tree / "index.html").read_text()
    version_root = (latest_tree / VERSION / "index.html").read_text()

    assert "Generated by ovweb" not in root_home
    assert 'href="/latest/docs/"' in root_home
    assert "Generated by ovweb" in version_root
    assert '<meta http-equiv="refresh" content="0; url=docs/">' in version_root


def test_installs_the_getting_started_redirect(latest_tree, config, report):
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    page = latest_tree / VERSION / "docs" / "getting-started" / "index.html"
    assert '<meta http-equiv="refresh" content="0; url=../">' in page.read_text()


def test_shields_an_author_pinned_link_in_the_blog(latest_tree, config, report):
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    blog = (latest_tree / "blog" / "index.html").read_text()
    assert 'href="https://openvidu.io/3.4/docs/releases/"' in blog
    assert 'href="https://openvidu.io/blog/"' in blog


def test_rewrites_the_404_page(latest_tree, config, report):
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    page = (latest_tree / "404.html").read_text()
    assert 'href="/pricing/"' in page
    assert 'href="/latest/docs/"' in page
    assert 'href="/"' in page
    assert VERSION not in page


def test_rewrites_llms_txt_three_ways(latest_tree, config, report):
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    llms = (latest_tree / "llms.txt").read_text()
    assert "/latest/docs/" in llms
    assert "/pricing/" in llms
    assert f"/{VERSION}/" not in llms


def test_rewrites_llms_full_txt_too(latest_tree, config, report):
    """It was promoted to the root untouched, which is how 764 version-pinned links reached it —
    including 21 for pages that are served only from the root and so never had a versioned URL."""
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    llms = (latest_tree / "llms-full.txt").read_text()
    assert "https://openvidu.io/latest/docs/self-hosting/index.md" in llms
    assert "https://openvidu.io/pricing/index.md" in llms
    assert f"/{VERSION}/" not in llms
    # Read detached from the site, so a root-relative target has nothing left to resolve against.
    assert "[PRO](https://openvidu.io/pricing/#openvidu-pro)" in llms


def test_rewrites_the_home_page_markdown_export(latest_tree, config, report):
    """`index.md` is a root file, so the walk over the promoted page folders misses it."""
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    home = (latest_tree / "index.md").read_text()
    assert "https://openvidu.io/latest/docs/index.md" in home
    assert "https://openvidu.io/pricing/index.md" in home
    assert f"/{VERSION}/" not in home


def test_rewrites_the_exports_of_promoted_pages(latest_tree, config, report):
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    export = (latest_tree / "pricing" / "index.md").read_text()
    assert "https://openvidu.io/latest/docs/index.md" in export
    assert "https://openvidu.io/support/index.md" in export
    assert f"/{VERSION}/" not in export


def test_versioned_export_keeps_its_version_but_not_for_root_pages(latest_tree, config, report):
    """The same asymmetry as the search index: an in-version reader keeps reading that version,
    while a link to a root-served page has no versioned URL to keep."""
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    export = (latest_tree / VERSION / "docs" / "index.md").read_text()
    assert f"https://openvidu.io/{VERSION}/docs/self-hosting/index.md" in export
    assert "https://openvidu.io/pricing/index.md" in export
    assert "https://openvidu.io/index.md" in export


def test_promotes_the_root_sitemap(latest_tree, config, report):
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    root = (latest_tree / "sitemap.xml").read_text()
    assert "https://openvidu.io/latest/docs/" in root
    assert "https://openvidu.io/pricing/" in root
    assert f"/{VERSION}/" not in root


def test_removes_the_per_version_sitemap(latest_tree, config, report):
    """Nothing references them: robots.txt names only the root sitemap, which is a plain
    urlset rather than an index."""
    assert (latest_tree / VERSION / "sitemap.xml").exists()

    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    assert not (latest_tree / VERSION / "sitemap.xml").exists()
    assert not (latest_tree / VERSION / "sitemap.xml.gz").exists()


def test_gzips_the_root_sitemap_from_its_final_content(latest_tree, config, report):
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    path = latest_tree / "sitemap.xml"
    assert gzip.decompress(path.with_suffix(".xml.gz").read_bytes()) == path.read_bytes()


def test_root_search_index_points_at_latest_but_the_version_keeps_its_version(
    latest_tree, config, report
):
    """A versioned page loads the index beside it, so in-version search must stay in the version;
    the root copy is served on the evergreen root pages and should not pin one."""
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    root = json.loads((latest_tree / "search" / "search_index.json").read_text())
    version = json.loads((latest_tree / VERSION / "search" / "search_index.json").read_text())

    assert [entry["location"] for entry in root["docs"]] == ["/", "/latest/docs/", "/pricing/"]
    assert [entry["location"] for entry in version["docs"]] == [
        "/",
        f"/{VERSION}/docs/",
        "/pricing/",
    ]


# -- re-publishing an older version ------------------------------------------------------


@pytest.fixture
def mixed_tree(tmp_path, layout):
    """The newest version plus an older one built by an older configuration."""
    build_tree(tmp_path, layout, version=VERSION)
    build_tree(tmp_path, layout, version=OLD_VERSION, modern=False)
    (tmp_path / "versions.json").write_text(
        json.dumps(
            [{"version": VERSION, "aliases": ["latest"]}, {"version": OLD_VERSION, "aliases": []}]
        ),
        encoding="utf-8",
    )
    (tmp_path / "latest").symlink_to(VERSION)
    return tmp_path


def test_past_version_leaves_the_root_alone(mixed_tree, config, report):
    (mixed_tree / "pricing").mkdir()
    (mixed_tree / "pricing" / "index.html").write_text("root pricing", encoding="utf-8")

    postprocess(mixed_tree, config=config, version=OLD_VERSION, update_latest=False, report=report)

    assert (mixed_tree / "pricing" / "index.html").read_text() == "root pricing"
    assert not (mixed_tree / "sitemap.xml").exists()


def test_past_version_strips_its_root_served_pages(mixed_tree, config, report):
    postprocess(mixed_tree, config=config, version=OLD_VERSION, update_latest=False, report=report)

    assert not (mixed_tree / OLD_VERSION / "pricing").exists()
    assert not (mixed_tree / OLD_VERSION / "robots.txt").exists()
    assert not (mixed_tree / OLD_VERSION / "index.md").exists()


def test_past_version_tolerates_files_it_never_built(mixed_tree, config, report):
    """An old branch's mkdocs.yml had no llms.txt or RSS plugins, so those files never existed."""
    assert not (mixed_tree / OLD_VERSION / "llms.txt").exists()
    postprocess(mixed_tree, config=config, version=OLD_VERSION, update_latest=False, report=report)
    assert not (mixed_tree / OLD_VERSION / "llms.txt").exists()


def test_past_version_gets_the_old_band_redirect(mixed_tree, config, report):
    """3.0–3.3 had no /docs/ landing page, so the version root goes to getting started."""
    postprocess(mixed_tree, config=config, version=OLD_VERSION, update_latest=False, report=report)

    root = (mixed_tree / OLD_VERSION / "index.html").read_text()
    assert '<meta http-equiv="refresh" content="0; url=docs/getting-started/">' in root

    docs_index = mixed_tree / OLD_VERSION / "docs" / "index.html"
    assert '<meta http-equiv="refresh" content="0; url=getting-started/">' in docs_index.read_text()
    assert not (mixed_tree / OLD_VERSION / "docs" / "getting-started").exists()


def test_past_version_pulls_the_newest_release_notes_in(mixed_tree, config, report):
    """Rebuilding an old version must not regress its notes to what it shipped with."""
    postprocess(mixed_tree, config=config, version=OLD_VERSION, update_latest=False, report=report)

    page = (mixed_tree / OLD_VERSION / "docs" / "releases" / "index.html").read_text()
    assert f"{VERSION}.0 notes" in page
    assert f"{OLD_VERSION}.0 notes" not in page
    # ...while its chrome keeps pointing inside its own version, which is what keeps a visitor
    # who opens /3.2/docs/releases/ browsing the 3.2 documentation.
    assert f'<a class="chrome" href="/{OLD_VERSION}/assets/logo.png">{OLD_VERSION}</a>' in page


def test_latest_version_pushes_its_release_notes_out(mixed_tree, config, report):
    postprocess(mixed_tree, config=config, version=VERSION, update_latest=True, report=report)

    page = (mixed_tree / OLD_VERSION / "docs" / "releases" / "index.html").read_text()
    assert f"{VERSION}.0 notes" in page
    assert f'<a class="chrome" href="/{OLD_VERSION}/assets/logo.png">{OLD_VERSION}</a>' in page


def test_removes_only_the_published_version_sitemap(mixed_tree, config, report):
    """A publish's blast radius stays its own folder: other versions keep their sitemap until
    they are next published."""
    postprocess(mixed_tree, config=config, version=OLD_VERSION, update_latest=False, report=report)

    assert not (mixed_tree / OLD_VERSION / "sitemap.xml").exists()
    assert not (mixed_tree / OLD_VERSION / "sitemap.xml.gz").exists()
    assert (mixed_tree / VERSION / "sitemap.xml").exists()


def test_only_the_published_version_gets_its_links_rewritten(mixed_tree, config, report):
    """Post-processing touches the version being published and nothing else.

    Publishing 3.9 rewrites 3.9's canonical to /latest/, and reaches into 3.2 only to splice
    the release notes — 3.2's own canonical, assets and navigation are whatever its last
    publish produced. That is what makes a publish's blast radius predictable, and it is why
    an older version has to be re-published for a rewrite change to reach it.
    """
    postprocess(mixed_tree, config=config, version=VERSION, update_latest=True, report=report)

    published = (mixed_tree / VERSION / "docs" / "releases" / "index.html").read_text()
    untouched = (mixed_tree / OLD_VERSION / "docs" / "releases" / "index.html").read_text()

    assert 'rel="canonical" href="https://openvidu.io/latest/docs/releases/"' in published
    assert f'rel="canonical" href="https://openvidu.io/{OLD_VERSION}/docs/releases/"' in untouched
    # ...but the notes themselves did travel.
    assert f"{VERSION}.0 notes" in untouched


# -- guards ------------------------------------------------------------------------------


def test_refuses_to_run_twice(latest_tree, config, report):
    """A second pass would strip the version out of author-pinned links and fail on the
    already-moved directories. The shell had no guard for this at all."""
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    with pytest.raises(PostprocessError, match="already a generated redirect"):
        postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)


def test_force_overrides_the_guard(latest_tree, config, report):
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)
    postprocess(
        latest_tree,
        config=config,
        version=VERSION,
        update_latest=False,
        report=report,
        force=True,
    )


def test_refuses_a_tree_without_the_version(tmp_path, config, report):
    with pytest.raises(PostprocessError, match="does not exist"):
        postprocess(tmp_path, config=config, version="9.9", update_latest=True, report=report)


def test_a_layout_naming_an_unbuilt_page_fails_with_the_config_key(latest_tree, config, report):
    """The likely cause is a typo in ovweb.yaml, so the message names the key, not the syscall."""
    from dataclasses import replace

    broken = replace(
        config,
        layout=replace(
            config.layout,
            non_versioned_pages=(*config.layout.non_versioned_pages, "no-such-page"),
        ),
    )
    with pytest.raises(PostprocessError, match=r"layout\.non_versioned_pages"):
        postprocess(latest_tree, config=broken, version=VERSION, update_latest=True, report=report)
