"""The invariants `ovweb verify` asserts over a published tree.

The load-bearing test here is the first one: a tree that has just been post-processed must
verify clean. That makes `verify` a real post-publish signal rather than a formality — anything
it reports after a publish is something the pipeline failed to do — and it means each individual
check below is asserting against a tree the pipeline actually produces, not a hand-made one.
"""

from __future__ import annotations

import json

import pytest
from test_postprocess import OLD_VERSION, VERSION, build_tree

from ovweb.pipeline.postprocess import postprocess
from ovweb.report import Reporter
from ovweb.verify import verify


@pytest.fixture
def report():
    return Reporter(verbosity=0, color=False)


@pytest.fixture
def published(tmp_path, layout, config, report):
    """A tree that has been through a full `latest` publish."""
    build_tree(tmp_path, layout, version=VERSION, config=config)
    (tmp_path / "versions.json").write_text(
        json.dumps([{"version": VERSION, "aliases": ["latest"]}]), encoding="utf-8"
    )
    postprocess(tmp_path, config=config, version=VERSION, update_latest=True, report=report)
    (tmp_path / "latest").symlink_to(VERSION)
    return tmp_path


def findings_by_check(tree, config) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for finding in verify(tree, config=config):
        grouped.setdefault(finding.check, []).append(finding.where)
    return grouped


def test_a_freshly_published_tree_has_no_findings(published, config):
    assert verify(published, config=config) == []


# -- the AI-facing channel ---------------------------------------------------------------


@pytest.mark.parametrize("name", ["llms.txt", "index.md"])
def test_reports_a_root_file_that_pins_the_current_version(published, config, name):
    """The defect this check exists for: these were promoted to the root untouched, so every
    internal link named the version that produced them."""
    (published / name).write_text(
        f"[docs](https://openvidu.io/{VERSION}/docs/)\n", encoding="utf-8"
    )

    assert findings_by_check(published, config)["root-export-version-pin"] == [name]


def test_reports_a_promoted_export_that_pins_the_current_version(published, config):
    (published / "pricing" / "index.md").write_text(
        f"[docs](https://openvidu.io/{VERSION}/docs/)\n", encoding="utf-8"
    )

    assert findings_by_check(published, config)["root-export-version-pin"] == ["pricing/index.md"]


def test_a_root_file_may_pin_a_different_version(published, config):
    """That is how a release-notes page links back to the release before it."""
    (published / "llms.txt").write_text(
        f"[{OLD_VERSION} notes](https://openvidu.io/{OLD_VERSION}/docs/releases/)\n",
        encoding="utf-8",
    )

    assert "root-export-version-pin" not in findings_by_check(published, config)


def test_reports_a_versioned_export_linking_to_a_root_page_under_the_version(published, config):
    """A hard 404, not merely a stale URL: that page has no versioned URL at all."""
    (published / VERSION / "docs" / "index.md").write_text(
        f"[pricing](https://openvidu.io/{VERSION}/pricing/index.md)\n", encoding="utf-8"
    )

    grouped = findings_by_check(published, config)
    assert grouped["export-root-page-link"] == [f"{VERSION}/docs/index.md"]


def test_a_versioned_export_may_keep_its_own_version_for_versioned_pages(published, config):
    (published / VERSION / "docs" / "index.md").write_text(
        f"[self-hosting](https://openvidu.io/{VERSION}/docs/self-hosting/index.md)\n",
        encoding="utf-8",
    )

    assert "export-root-page-link" not in findings_by_check(published, config)


# -- the version folders themselves ------------------------------------------------------


def test_reports_a_version_root_that_is_not_a_generated_redirect(published, config):
    (published / VERSION / "index.html").write_text("<html>a real page</html>", encoding="utf-8")

    assert findings_by_check(published, config)["version-root"] == [f"{VERSION}/index.html"]


def test_reports_a_version_folder_missing_from_versions_json(published, config):
    """It is published but the version selector will not offer it."""
    (published / "3.5").mkdir()

    assert findings_by_check(published, config)["versions-json"] == ["3.5"]


def test_reports_a_version_in_versions_json_with_no_folder(published, config):
    (published / "versions.json").write_text(
        json.dumps([{"version": VERSION, "aliases": ["latest"]}, {"version": "3.4"}]),
        encoding="utf-8",
    )

    grouped = findings_by_check(published, config)
    assert grouped["versions-json"] == ["versions.json"]


def test_the_folders_stand_in_when_versions_json_is_absent(published, config):
    """A tree mid-publish has no versions.json yet, and must still be checkable."""
    (published / "versions.json").unlink()

    assert verify(published, config=config) == []


def test_reports_a_versioned_page_linking_to_a_root_file_under_its_version(published, config):
    """The feeds live at the site root; a version folder keeps no copy, so this is a 404."""
    (published / VERSION / "docs" / "index.html").write_text(
        '<link rel="alternate" href="../../feed_rss_created.xml">', encoding="utf-8"
    )

    grouped = findings_by_check(published, config)
    assert grouped["versioned-root-file-link"] == [f"{VERSION}/docs/index.html"]


def test_reports_a_promoted_page_still_claiming_a_versioned_url(published, config):
    (published / "pricing" / "index.html").write_text(
        f'<link rel="canonical" href="https://openvidu.io/{VERSION}/pricing/">', encoding="utf-8"
    )

    assert findings_by_check(published, config)["root-self-url"] == ["pricing/index.html"]


def test_reports_a_relative_location_in_the_root_search_index(published, config):
    """The root index is served from `/`, so a location relative to it resolves nowhere."""
    (published / "search" / "search_index.json").write_text(
        json.dumps({"docs": [{"location": "docs/"}]}, separators=(",", ":")), encoding="utf-8"
    )

    assert findings_by_check(published, config)["search-index"] == ["search/search_index.json"]


def test_reports_a_missing_root_search_index(published, config):
    (published / "search" / "search_index.json").unlink()

    assert findings_by_check(published, config)["search-index"] == ["search/search_index.json"]


# -- the sitemap's <lastmod> --------------------------------------------------------------


def lastmod_on_the_pricing_entry(tree, value: str) -> None:
    """Add a `<lastmod>` to a root page's entry, which the mirror check does not look at."""
    path = tree / "sitemap.xml"
    path.write_text(
        path.read_text().replace(
            "<loc>https://openvidu.io/pricing/</loc>",
            f"<loc>https://openvidu.io/pricing/</loc>\n         <lastmod>{value}</lastmod>",
        ),
        encoding="utf-8",
    )


def test_reports_a_lastmod_that_is_not_a_date(published, config):
    lastmod_on_the_pricing_entry(published, "last Tuesday")

    findings = [f for f in verify(published, config=config) if f.check == "sitemap-lastmod"]
    assert len(findings) == 1
    assert "not an ISO date" in findings[0].detail


def test_reports_a_lastmod_in_the_future(published, config):
    """A date nothing has happened on yet is a clock or timezone bug, not an edit."""
    lastmod_on_the_pricing_entry(published, "2999-01-01")

    findings = [f for f in verify(published, config=config) if f.check == "sitemap-lastmod"]
    assert len(findings) == 1
    assert "in the future" in findings[0].detail


def test_accepts_a_real_lastmod(published, config):
    lastmod_on_the_pricing_entry(published, "2026-07-22")

    assert verify(published, config=config) == []


def test_accepts_every_page_carrying_the_same_lastmod(published, config):
    """A commit that touches the whole site legitimately dates every page the same day."""
    path = published / "sitemap.xml"
    path.write_text(
        path.read_text().replace("</loc>", "</loc>\n         <lastmod>2026-07-31</lastmod>"),
        encoding="utf-8",
    )

    assert verify(published, config=config) == []


# -- the version selector ----------------------------------------------------------------
#
# Each of these silently turns off "switch version, keep reading the same page" and drops the
# reader on the version root instead.


def test_reports_a_missing_version_sitemap(published, config):
    (published / VERSION / "sitemap.xml").unlink()

    findings = [f for f in verify(published, config=config) if f.check == "version-sitemap"]
    assert [f.where for f in findings] == [f"{VERSION}/sitemap.xml"]
    assert "version selector" in findings[0].detail


def test_reports_a_version_sitemap_without_the_version_root_entry(published, config):
    """The selector needs it as the common prefix of every URL before it will resolve one."""
    (published / VERSION / "sitemap.xml").write_text(
        f"<urlset>\n  <url><loc>https://openvidu.io/{VERSION}/docs/</loc></url>\n</urlset>\n",
        encoding="utf-8",
    )

    findings = [f for f in verify(published, config=config) if f.check == "version-sitemap"]
    assert len(findings) == 1
    assert "common prefix" in findings[0].detail


def test_reports_a_version_sitemap_still_listing_a_root_served_page(published, config):
    (published / VERSION / "sitemap.xml").write_text(
        f"<urlset>\n  <url><loc>https://openvidu.io/{VERSION}/</loc></url>\n"
        f"  <url><loc>https://openvidu.io/{VERSION}/pricing/</loc></url>\n</urlset>\n",
        encoding="utf-8",
    )

    findings = [f for f in verify(published, config=config) if f.check == "version-sitemap"]
    assert len(findings) == 1
    assert "404" in findings[0].detail


def test_reports_a_root_search_index_that_pins_the_version(published, config):
    (published / "search" / "search_index.json").write_text(
        json.dumps({"docs": [{"location": f"/{VERSION}/docs/"}]}, separators=(",", ":")),
        encoding="utf-8",
    )

    assert findings_by_check(published, config)["root-search-index"] == ["search/search_index.json"]


def test_reports_a_link_to_an_export_that_does_not_exist(published, config):
    """The plugin writes these unconditionally; the publish repairs them. This is the assertion
    that it did."""
    (published / VERSION / "docs" / "index.md").write_text(
        "[gone](https://openvidu.io/latest/docs/no-such-page/index.md)\n", encoding="utf-8"
    )

    findings = [f for f in verify(published, config=config) if f.check == "export-link"]
    assert [f.where for f in findings] == [f"{VERSION}/docs/index.md"]
    assert "no-such-page" in findings[0].detail


# -- the unversioned mirror --------------------------------------------------------------


def test_reports_an_unversioned_url_with_no_redirect_page(published, config):
    """Without a stub, the URL a human types 404s for a crawler."""
    (published / "docs" / "releases" / "index.html").unlink()

    assert findings_by_check(published, config)["mirror"] == ["docs/releases/index.html"]


def test_reports_a_stale_redirect_page(published, config):
    """A page that has been renamed leaves a stub pointing into a 404 — worse than the 404 it
    replaced, and the reason the publish rebuilds the mirror instead of patching it."""
    stale = published / "docs" / "gone"
    stale.mkdir()
    (stale / "index.html").write_bytes((published / "docs" / "index.html").read_bytes())

    assert findings_by_check(published, config)["mirror"] == ["docs/gone/index.html"]


def test_reports_a_real_page_on_a_mirrored_path(published, config):
    """The next publish deletes everything under /docs/, so anything else there is a trap."""
    (published / "docs" / "notes.html").write_text("<h1>Notes</h1>", encoding="utf-8")

    assert findings_by_check(published, config)["mirror"] == ["docs/notes.html"]


def test_reports_a_redirect_that_points_at_a_missing_page(published, config):
    """A redirect into a 404 is worse than the 404 it replaced. This is the defect found in
    review of a rule gated `>=3.7` whose target page only arrived in 3.8."""
    stub = published / VERSION / "docs" / "moved" / "index.html"
    stub.parent.mkdir(parents=True)
    stub.write_text(
        '<!-- Generated by ovweb from the "x" rule -->'
        '<meta http-equiv="refresh" content="0; url=../not-a-page/">',
        encoding="utf-8",
    )

    assert findings_by_check(published, config)["redirect-target"] == [
        f"{VERSION}/docs/moved/index.html"
    ]


def test_a_redirect_to_a_page_that_exists_is_not_reported(published, config):
    stub = published / VERSION / "docs" / "moved" / "index.html"
    stub.parent.mkdir(parents=True)
    stub.write_text(
        '<!-- Generated by ovweb from the "x" rule -->'
        '<meta http-equiv="refresh" content="0; url=../releases/">',
        encoding="utf-8",
    )

    assert "redirect-target" not in findings_by_check(published, config)


def test_a_real_page_is_not_mistaken_for_a_redirect(published, config):
    """The marker decides, not the size: a small page with no marker is left alone."""
    page = published / VERSION / "docs" / "tiny" / "index.html"
    page.parent.mkdir(parents=True)
    page.write_text("<html><body>short but real</body></html>", encoding="utf-8")

    assert "redirect-target" not in findings_by_check(published, config)
