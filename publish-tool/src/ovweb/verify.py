"""Assert the invariants of a published gh-pages tree.

Deliberately written so it passes on the *live* site as it stands today: that makes it the
cheapest available check that the tool's understanding of the published layout is right, and
it turns "the publish worked" into something a machine can answer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from . import fsops
from .config import SiteConfig
from .pipeline.postprocess import GENERATED_MARKER
from .versions import read_versions_json

SELF_URL_TAGS = re.compile(r'(?:rel="canonical" href|property="og:url" content)="([^"]+)"')
RELATIVE_PARENT_HREF = re.compile(r'href="((?:\.\./)+[^"]*)"')


@dataclass
class Finding:
    check: str
    where: str
    detail: str


def verify(
    tree: Path, *, config: SiteConfig, versions: tuple[str, ...] | None = None
) -> list[Finding]:
    """Return every invariant violation found in `tree`. An empty list means it is sound."""
    findings: list[Finding] = []

    published = list(versions) if versions else _published_versions(tree)

    findings += _check_versions_json(tree, published)
    for version in published:
        version_dir = tree / version
        if not version_dir.is_dir():
            continue
        findings += _check_version_root_is_redirect(version_dir, version)
        findings += _check_version_sitemap(tree, version, config)
    findings += _check_root_pages_have_no_version(tree, config, published)
    findings += _check_search_index_absolute(tree, config)
    return findings


def _published_versions(tree: Path) -> list[str]:
    path = tree / "versions.json"
    if not path.is_file():
        return [
            entry.name
            for entry in sorted(tree.iterdir())
            if entry.is_dir() and re.fullmatch(r"\d+\.\d+", entry.name)
        ]
    return [entry.version for entry in read_versions_json(fsops.read_text(path))]


def _check_versions_json(tree: Path, published: list[str]) -> list[Finding]:
    """Every version in versions.json has a folder, and every version folder is listed."""
    findings = []
    for version in published:
        if not (tree / version).is_dir():
            findings.append(
                Finding("versions-json", "versions.json", f"{version} has no folder in the tree")
            )

    on_disk = {
        entry.name
        for entry in tree.iterdir()
        if entry.is_dir() and re.fullmatch(r"\d+\.\d+", entry.name)
    }
    for orphan in sorted(on_disk - set(published)):
        findings.append(
            Finding(
                "versions-json",
                orphan,
                "folder is published but missing from versions.json, so the version selector "
                "will not offer it",
            )
        )
    return findings


def _check_version_root_is_redirect(version_dir: Path, version: str) -> list[Finding]:
    """A bare version root must send the visitor into the documentation.

    Two shapes are accepted, so this check is meaningful both before and after the migration:
    a page ovweb generated, and the hand-written JavaScript-only stub that predates it. The
    stricter assertions — a meta refresh for crawlers without JavaScript, and a relative
    target — apply only to the generated form, which is the only one ovweb is responsible
    for.
    """
    where = f"{version}/index.html"
    index = version_dir / "index.html"
    if not index.is_file():
        return [Finding("version-root", where, "missing")]

    text = fsops.read_text(index)
    generated = GENERATED_MARKER in text
    redirects = (
        'http-equiv="refresh"' in text or "location.replace" in text or "location.href" in text
    )
    if not redirects:
        return [
            Finding(
                "version-root",
                where,
                "does not redirect anywhere — a bare version root must lead into the documentation",
            )
        ]
    if not generated:
        return []

    findings = []
    if 'http-equiv="refresh"' not in text:
        findings.append(
            Finding(
                "version-root",
                where,
                "has no meta refresh, so it does not redirect without JavaScript",
            )
        )
    absolute = re.search(r'(?:content="0; url=|<a href=")(/[^"\s>]*)', text)
    if absolute:
        findings.append(
            Finding(
                "version-root",
                where,
                f"redirect target {absolute.group(1)!r} is site-absolute. `latest` is a symlink "
                "to this folder, so an absolute target would leak the version number to "
                "visitors of /latest/",
            )
        )
    return findings


def _check_version_sitemap(tree: Path, version: str, config: SiteConfig) -> list[Finding]:
    """A version folder must not carry a sitemap.

    Only the root sitemap is published — `robots.txt` names it, and it is a plain `urlset`
    rather than an index. A per-version copy is advertised to nobody, so the publish deletes
    it. Until every version has been through a publish once, this reports the leftovers.
    """
    del config
    findings = []
    for name in ("sitemap.xml", "sitemap.xml.gz"):
        if (tree / version / name).exists():
            findings.append(
                Finding(
                    "version-sitemap",
                    f"{version}/{name}",
                    "per-version sitemaps are no longer published; publish this version to "
                    "remove it",
                )
            )
    return findings


def _check_root_pages_have_no_version(
    tree: Path, config: SiteConfig, published: list[str]
) -> list[Finding]:
    """A page served from the root must not claim a versioned URL as its own."""
    findings = []
    pattern = re.compile(r"^/(\d+\.\d+)/")
    for page in config.layout.non_versioned_pages:
        root = tree / page
        if not root.is_dir():
            continue
        for path in root.rglob("*.html"):
            for match in SELF_URL_TAGS.finditer(fsops.read_text(path)):
                url = match.group(1)
                relative = url.split("openvidu.io", 1)[-1]
                found = pattern.match(relative)
                if found and found.group(1) in published:
                    findings.append(
                        Finding(
                            "root-self-url",
                            str(path.relative_to(tree)),
                            f"self-referencing URL {url} still carries a version",
                        )
                    )
    return findings


def _check_search_index_absolute(tree: Path, config: SiteConfig) -> list[Finding]:
    path = tree / "search" / "search_index.json"
    if not path.is_file():
        return [Finding("search-index", "search/search_index.json", "missing")]
    text = fsops.read_text(path)
    findings = []
    for page in (*config.layout.versioned_pages, *config.layout.non_versioned_pages):
        needle = f'"location":"{page}/'
        if needle in text:
            findings.append(
                Finding(
                    "search-index",
                    "search/search_index.json",
                    f"holds the relative location {needle!r}; the root index is served from / so "
                    "every location must be absolute",
                )
            )
    return findings
