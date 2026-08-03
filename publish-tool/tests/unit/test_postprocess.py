"""The post-processing pipeline over a synthetic built tree.

Covers the wiring the unit tests cannot: step order, what moves versus what is copied, and
the difference between publishing the newest version and re-publishing an older one.
"""

from __future__ import annotations

import gzip
import json
import posixpath
from pathlib import Path

import pytest

from ovweb.pipeline.postprocess import PostprocessError, postprocess
from ovweb.redirects import MIRROR_RULE_ID, resolve_file_redirects
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


def build_redirect_targets(root: Path, config, version: str) -> None:
    """Give every redirect rule that applies to `version` a page to point at.

    Derived from the rules rather than listed, for the same reason the rest of the fixture is
    derived from the layout: a rule added to ovweb.yaml gets its target here automatically, and
    `ovweb verify` asserts that no generated redirect points at a missing page. Existing files
    are left alone — several rules target pages this fixture writes properly, and the version
    root targets `docs/`, whose real content other tests assert on.
    """
    for redirect in resolve_file_redirects(config, version):
        if redirect.to.startswith("/"):
            target = root / redirect.to.lstrip("/")
        else:
            base = posixpath.dirname(redirect.path)
            target = root / posixpath.normpath(posixpath.join(base, redirect.to))
        page = target / "index.html" if redirect.to.endswith("/") else target
        if page.exists():
            continue
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(f"<html><body>target of {redirect.rule_id}</body></html>", encoding="utf-8")


def build_tree(root: Path, layout, *, version: str, modern: bool = True, config=None) -> None:
    """Write a folder shaped like raw `mike` output for one version.

    Driven by the real layout so the fixture cannot drift from the configuration: adding a
    page to ovweb.yaml automatically gets one here too. Pass `config` to also materialise the
    redirect rules' targets, which a tree has to have for `ovweb verify` to pass on it.
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
            f"[Support](https://openvidu.io/{version}/support/index.md)\n"
            f"[Self-hosting](https://openvidu.io/{version}/docs/self-hosting/index.md)\n",
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
    # to a page served only from the root must lose the version. `releases` is a page this tree
    # really exports; `self-hosting` deliberately is not, so the repair step has something to fix.
    (base / "docs" / "index.md").write_text(
        f"[Releases](https://openvidu.io/{version}/docs/releases/index.md)\n"
        f"[Self-hosting](https://openvidu.io/{version}/docs/self-hosting/index.md)\n"
        f"[Pricing](https://openvidu.io/{version}/pricing/index.md)\n"
        f"[Home](https://openvidu.io/{version}/index.md)\n"
        "[PRO](/pricing/#openvidu-pro)\n",
        encoding="utf-8",
    )
    (base / "docs" / "releases" / "index.md").write_text("# Releases\n", encoding="utf-8")
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
    # Both versioned sections and a page below the top of one, so the unversioned mirror has
    # something to nest, plus a root-served page it must leave alone.
    (base / "sitemap.xml").write_text(
        "<urlset>\n"
        f"    <url>\n         <loc>https://openvidu.io/{version}/</loc>\n    </url>\n"
        f"    <url>\n         <loc>https://openvidu.io/{version}/docs/</loc>\n    </url>\n"
        f"    <url>\n         <loc>https://openvidu.io/{version}/docs/releases/</loc>\n    </url>\n"
        f"    <url>\n         <loc>https://openvidu.io/{version}/meet/</loc>\n    </url>\n"
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
        for feed in (
            "feed_rss_created.xml",
            "feed_rss_updated.xml",
            "feed_json_created.json",
            "feed_json_updated.json",
        ):
            (base / feed).write_text(f"https://openvidu.io/{version}/blog/x/", encoding="utf-8")
        (base / "rss.xsl").write_text("<xsl/>", encoding="utf-8")

    if config is not None:
        build_redirect_targets(root, config, version)


@pytest.fixture
def report():
    return Reporter(verbosity=0, color=False)


@pytest.fixture
def latest_tree(tmp_path, layout, config):
    build_tree(tmp_path, layout, version=VERSION, config=config)
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
    # No llms-full.txt: a single concatenation of every export reached 2.8 MB, which no model
    # can load, and duplicated content the exports already serve.
    assert not (latest_tree / "llms-full.txt").exists()
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
    assert f"https://openvidu.io/{VERSION}/docs/releases/index.md" in export
    assert "https://openvidu.io/pricing/index.md" in export
    assert "https://openvidu.io/index.md" in export
    # Root-relative targets are made absolute in every export, not just the llms files.
    assert "[PRO](https://openvidu.io/pricing/#openvidu-pro)" in export


def test_repairs_links_to_exports_that_do_not_exist(latest_tree, config, report):
    """The plugin appends `index.md` to every directory link without checking it exists, so a page
    outside its `sections` list is advertised at a URL that 404s. Not all of them can be fixed by
    listing more pages — vendored HTML and JavaScript shells can never have an export — so the
    link is repaired against the tree instead."""
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    export = (latest_tree / VERSION / "docs" / "index.md").read_text()
    # This tree exports no docs/self-hosting page, so the link goes to the page itself.
    assert f"https://openvidu.io/{VERSION}/docs/self-hosting/)" in export
    assert "self-hosting/index.md" not in export
    # ...while an export that does exist is left alone.
    assert f"https://openvidu.io/{VERSION}/docs/releases/index.md" in export


def test_repair_reaches_the_promoted_exports_too(latest_tree, config, report):
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    export = (latest_tree / "pricing" / "index.md").read_text()
    # Points into the docs, so it went to /latest/ first and was then repaired there.
    assert "https://openvidu.io/latest/docs/self-hosting/)" in export
    assert "self-hosting/index.md" not in export
    # A sibling root page's export does exist in this tree, so it keeps its .md link.
    assert "https://openvidu.io/support/index.md" in export


def test_promotes_the_root_sitemap(latest_tree, config, report):
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    root = (latest_tree / "sitemap.xml").read_text()
    assert "https://openvidu.io/latest/docs/" in root
    assert "https://openvidu.io/pricing/" in root
    assert f"/{VERSION}/" not in root


def test_prunes_the_per_version_sitemap(latest_tree, config, report):
    """It stays, because the version selector fetches it to keep a reader on the same page across
    a version switch — but the pages that moved to the root have to go."""
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    sitemap = (latest_tree / VERSION / "sitemap.xml").read_text()
    assert f"<loc>https://openvidu.io/{VERSION}/</loc>" in sitemap
    assert f"/{VERSION}/docs/" in sitemap
    assert "/pricing/" not in sitemap
    # The .gz is regenerated from the pruned content, not left stale.
    gz = (latest_tree / VERSION / "sitemap.xml.gz").read_bytes()
    assert gzip.decompress(gz).decode() == sitemap


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
def mixed_tree(tmp_path, layout, config):
    """The newest version plus an older one built by an older configuration."""
    build_tree(tmp_path, layout, version=VERSION, config=config)
    build_tree(tmp_path, layout, version=OLD_VERSION, modern=False, config=config)
    (tmp_path / "versions.json").write_text(
        json.dumps(
            [{"version": VERSION, "aliases": ["latest"]}, {"version": OLD_VERSION, "aliases": []}]
        ),
        encoding="utf-8",
    )
    (tmp_path / "latest").symlink_to(VERSION)
    return tmp_path


# -- the unversioned mirror --------------------------------------------------------------


def mirror_stub(target: str) -> str:
    """A stub shaped like one this step wrote on an earlier publish."""
    return (
        f'<!-- Generated by ovweb from the "{MIRROR_RULE_ID}" rule -->'
        f'<meta http-equiv="refresh" content="0; url={target}">'
    )


def test_mirrors_every_advertised_page_at_its_unversioned_url(latest_tree, config, report):
    """The point of the step: /docs/releases/ answers instead of dead-ending on the 404 page."""
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    page = (latest_tree / "docs" / "releases" / "index.html").read_text()
    assert 'content="0; url=/latest/docs/releases/"' in page
    assert '<link rel="canonical" href="https://openvidu.io/latest/docs/releases/">' in page
    assert 'content="noindex, follow"' in page
    assert MIRROR_RULE_ID in page
    # Both sections, and the section roots themselves — the two URLs issue 22 was raised for.
    assert (latest_tree / "docs" / "index.html").is_file()
    assert (latest_tree / "meet" / "index.html").is_file()


def test_the_mirror_leaves_the_root_served_pages_out(latest_tree, config, report):
    """`/pricing/` is served from the root already, so a stub there would shadow the real page."""
    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    assert "Generated by ovweb" not in (latest_tree / "pricing" / "index.html").read_text()


def test_the_mirror_is_rebuilt_rather_than_reconciled(latest_tree, config, report):
    """A page that has since been renamed must not leave a stub redirecting into a 404."""
    (latest_tree / "docs" / "gone").mkdir(parents=True)
    (latest_tree / "docs" / "gone" / "index.html").write_text(
        mirror_stub("/latest/docs/gone/"), encoding="utf-8"
    )

    postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)

    assert not (latest_tree / "docs" / "gone").exists()
    assert (latest_tree / "docs" / "releases" / "index.html").is_file()


def test_refuses_to_delete_content_it_did_not_write(latest_tree, config, report):
    """The step wipes /docs/ outright, so it first proves that everything there is its own."""
    (latest_tree / "docs").mkdir()
    (latest_tree / "docs" / "index.html").write_text("a real page", encoding="utf-8")

    with pytest.raises(PostprocessError, match="not a generated redirect"):
        postprocess(latest_tree, config=config, version=VERSION, update_latest=True, report=report)


def test_an_empty_mirror_is_a_failure_not_a_silent_skip(latest_tree, config, report):
    """A sitemap that names no versioned page means the promotion changed shape. Reinstating the
    404s quietly is the one outcome worse than stopping."""
    from dataclasses import replace

    renamed = replace(config, layout=replace(config.layout, site_url="https://example.invalid"))
    with pytest.raises(PostprocessError, match="unversioned mirror would be empty"):
        postprocess(latest_tree, config=renamed, version=VERSION, update_latest=True, report=report)


def test_past_version_leaves_the_mirror_alone(mixed_tree, config, report):
    """The stubs point at `/latest/`, so a publish that does not move `latest` has no say in
    them."""
    stub = mirror_stub("/latest/docs/")
    (mixed_tree / "docs").mkdir()
    (mixed_tree / "docs" / "index.html").write_text(stub, encoding="utf-8")

    postprocess(mixed_tree, config=config, version=OLD_VERSION, update_latest=False, report=report)

    assert (mixed_tree / "docs" / "index.html").read_text() == stub


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
    # And it lands somewhere: the fixture materialises every rule's target, because a redirect
    # into a 404 is worse than the 404 it replaced and `ovweb verify` now rejects one.
    assert (mixed_tree / OLD_VERSION / "docs" / "getting-started" / "index.html").is_file()


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


def test_prunes_only_the_published_version_sitemap(mixed_tree, config, report):
    """A publish's blast radius stays its own folder: another version's sitemap is left as its
    own last publish produced it."""
    postprocess(mixed_tree, config=config, version=OLD_VERSION, update_latest=False, report=report)

    assert "/pricing/" not in (mixed_tree / OLD_VERSION / "sitemap.xml").read_text()
    assert f"/{VERSION}/pricing/" in (mixed_tree / VERSION / "sitemap.xml").read_text()


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
