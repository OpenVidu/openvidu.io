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
    build_tree(tmp_path, layout, version=VERSION)
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


@pytest.mark.parametrize("name", ["llms.txt", "llms-full.txt", "index.md"])
def test_reports_a_root_file_that_pins_the_current_version(published, config, name):
    """The defect this check exists for: `llms-full.txt` and `index.md` were promoted to the
    root untouched, so every internal link named the version that produced them."""
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
    (published / "llms-full.txt").write_text(
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


# -- the checks that predate the exports -------------------------------------------------


def test_reports_a_version_root_that_is_not_a_generated_redirect(published, config):
    (published / VERSION / "index.html").write_text("<html>a real page</html>", encoding="utf-8")

    assert findings_by_check(published, config)["version-root"] == [f"{VERSION}/index.html"]


# -- the version selector ----------------------------------------------------------------
#
# Each of these silently turns off "switch version, keep reading the same page" and drops the
# reader on the version root instead. The middle one is how the feature was lost once already.


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
