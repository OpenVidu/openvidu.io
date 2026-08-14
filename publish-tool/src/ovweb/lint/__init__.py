"""Authoring-convention checks that `mkdocs build --strict` cannot see.

MkDocs validates Markdown links, but never looks inside raw HTML, never compares a page against
the conventions (version-pin discipline, SEO field lengths, the `page_features:` contract),
and reports
broken anchors at INFO where ~110 `pymdownx.tabbed` false positives bury them. Each check here
covers one of those blind spots, over the *source* tree — no build needed, so the whole run
takes a second or two.

Severities: an `error` is a defect the tree must stay free of (CI fails on it); a `warn` is a
convention violation worth fixing but not worth blocking a merge; an `info` is janitorial.
"""

from __future__ import annotations

from pathlib import Path

from ..model import SiteLayout
from . import conventions, links, meta
from .corpus import load_corpus
from .findings import ERROR, INFO, SEVERITY_ORDER, WARN, Finding

__all__ = ["ERROR", "INFO", "WARN", "Finding", "run_lint"]


def run_lint(root: Path, *, layout: SiteLayout, paths: list[str] | None = None) -> list[Finding]:
    """Every finding in the tree at `root`, or only those in `paths` (repo-relative)."""
    corpus = load_corpus(root)
    findings = [
        *links.check_html_targets(corpus, layout),
        *links.check_markdown_form(corpus),
        *links.check_version_pins(corpus, layout),
        *links.check_commented_links(corpus, layout),
        *meta.check_seo_fields(corpus),
        *conventions.check_admonitions(corpus),
        *conventions.check_tag_contract(corpus),
        *conventions.check_image_alt(corpus),
        *conventions.check_target_blank_form(corpus),
        *conventions.check_asset_placement(corpus),
        *conventions.check_light_dark_pairs(corpus),
        *conventions.check_snippet_names(corpus),
        *conventions.check_blog_asset_mirroring(corpus),
    ]
    if paths is not None:
        wanted = {path.replace("\\", "/").lstrip("./") for path in paths}
        findings = [finding for finding in findings if finding.file in wanted]
    return sorted(findings, key=lambda f: (f.file, f.line, SEVERITY_ORDER[f.severity], f.check))
