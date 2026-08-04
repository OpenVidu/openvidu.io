"""The publish plan — the contract `--dry-run` prints.

`test_postprocess.py` asserts that these names and their order match the steps the pipeline really
runs, which is what stops the printed plan drifting from the work.
"""

from __future__ import annotations

from ovweb.plan import build_plan

LATEST_STEPS = [
    "remove-overrides",
    "rewrite-versioned",
    "rewrite-search-index",
    "rewrite-non-versioned",
    "promote-to-root",
    "promote-sitemap",
    "promote-search-index",
    "repair-export-links",
    "install-redirects",
    "mirror-unversioned",
    "prune-version-sitemap",
    "sync-releases",
    "commit",
]

PAST_STEPS = [
    "remove-overrides",
    "rewrite-versioned",
    "rewrite-search-index",
    "strip-non-versioned",
    "repair-export-links",
    "install-redirects",
    "prune-version-sitemap",
    "sync-releases",
    "commit",
]


def test_latest_step_order(config):
    """Locked down because the order is behaviour: promotion moves index.html out of the version
    folder, so the redirect must be written after it, and the mirror reads the promoted sitemap."""
    plan = build_plan(config, version="3.9", update_latest=True)
    assert [step.name for step in plan.steps] == LATEST_STEPS


def test_the_mirror_is_only_planned_for_the_newest_version(config):
    """Its stubs point at `/latest/`, so a publish that does not move `latest` must not touch it."""
    past = {step.name for step in build_plan(config, version="3.7", update_latest=False).steps}
    assert "mirror-unversioned" not in past


def test_past_step_order(config):
    plan = build_plan(config, version="3.7", update_latest=False)
    assert [step.name for step in plan.steps] == PAST_STEPS


def test_the_root_pages_are_only_touched_for_the_newest_version(config):
    past = {step.name for step in build_plan(config, version="3.7", update_latest=False).steps}
    assert "promote-to-root" not in past
    assert "promote-sitemap" not in past
    assert "rewrite-non-versioned" not in past


def test_build_source_branch(config):
    """mike builds from the working tree, so this decides what gets published."""
    assert build_plan(config, version="3.9", update_latest=True).source_branch == "main"
    assert build_plan(config, version="3.7", update_latest=False).source_branch == "3.7"


def test_plan_carries_the_resolved_redirects(config):
    plan = build_plan(config, version="3.2", update_latest=False)
    targets = {redirect.rule_id: redirect.to for redirect in plan.redirects}
    assert targets["version-root"] == "docs/getting-started/"


def test_plan_notes_explain_the_root_page_behaviour(config):
    latest = build_plan(config, version="3.9", update_latest=True)
    past = build_plan(config, version="3.7", update_latest=False)
    assert any("root" in note for note in latest.notes)
    assert any("not be touched" in note for note in past.notes)
