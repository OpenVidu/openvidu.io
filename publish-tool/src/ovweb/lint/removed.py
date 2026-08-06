"""Removed pages must leave a redirect behind: `ovweb lint --against REF`.

`redirects check` validates the rules that exist; nothing else notices a rule that is
*missing*. A PR that renames or deletes a published page merges green today and only fails
months later as a 404 and lost ranking. Given the page list of a base revision, every page
that is gone from the working tree must be claimed by a redirect rule — a `files` rule naming
its URL, or an expansion (cross-product template, tree-rename or section-fallback prefix)
covering it.

Blog posts are exempt: their URLs derive from `date` + `slug`, not from the file path, and the
draft-publish transition moves the file by design.
"""

from __future__ import annotations

import re
from pathlib import Path

from ..model import (
    VERSION_ROOT,
    CrossProductRule,
    SectionFallbackRule,
    SiteConfig,
    TreeRenameRule,
)
from .findings import ERROR, Finding

PLACEHOLDER = re.compile(r"\{\w+\}")


def _stub_template(page: str, layout) -> str | None:
    """The redirect-page path a rule must claim for a removed source page, or None if exempt."""
    if not page.startswith("docs/") or not page.endswith(".md"):
        return None
    relative = page[len("docs/") :]
    if relative.startswith(("blog/", "overrides/")):
        return None
    if relative.endswith("/index.md"):
        url_file = relative[: -len("index.md")] + "index.html"
    elif relative == "index.md":
        url_file = "index.html"
    else:
        url_file = relative[: -len(".md")] + "/index.html"
    area = relative.split("/", 1)[0]
    if area in layout.versioned_pages:
        return f"{{version}}/{url_file}"
    return url_file


def _template_regex(template: str) -> re.Pattern[str]:
    """A rule's `at` template as a regex: each placeholder matches one path segment."""
    escaped = re.escape(PLACEHOLDER.sub("\x00", template))
    return re.compile("^" + escaped.replace("\x00", "[^/]+") + "$")


def _claimed(stub: str, config: SiteConfig) -> bool:
    for rule in config.file_rules:
        if rule.at != VERSION_ROOT and rule.at == stub:
            return True
    for rule in config.expand_rules:
        if isinstance(rule, CrossProductRule) and _template_regex(rule.at).match(stub):
            return True
        if isinstance(rule, TreeRenameRule) and stub.startswith(f"{rule.from_path}/"):
            return True
        if isinstance(rule, SectionFallbackRule) and stub.startswith(f"{rule.dir}/"):
            return True
    return False


def check_removed_pages(base_pages: list[str], *, root: Path, config: SiteConfig) -> list[Finding]:
    """Every page of the base revision that is gone must be claimed by a redirect rule."""
    findings = []
    for page in sorted(set(base_pages)):
        stub = _stub_template(page, config.layout)
        if stub is None or (root / page).is_file():
            continue
        if _claimed(stub, config):
            continue
        findings.append(
            Finding(
                "removed-without-redirect",
                ERROR,
                page,
                1,
                "page removed or renamed with no redirect rule claiming its old URL",
                "declare it in publish-tool/ovweb.yaml (redirects.files or an expand rule) — "
                "never retire a published URL silently",
            )
        )
    return findings
