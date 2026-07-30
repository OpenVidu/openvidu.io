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
from .pipeline.postprocess import GENERATED_MARKER, LLMS_FILES
from .rewrite.markdown import SUFFIX as MARKDOWN
from .versions import alias_target, read_versions_json

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
    latest = _latest_version(tree)

    findings += _check_versions_json(tree, published)
    for version in published:
        version_dir = tree / version
        if not version_dir.is_dir():
            continue
        findings += _check_version_root_is_redirect(version_dir, version)
        findings += _check_version_sitemap(tree, version, config)
        findings += _check_versioned_pages_reach_root_files(tree, version, config)
        findings += _check_exports_reach_root_pages(tree, version, config)
    findings += _check_root_pages_have_no_version(tree, config, published)
    findings += _check_search_index_absolute(tree, config)
    findings += _check_root_search_index_uses_latest(tree, config, published)
    findings += _check_root_exports_use_latest(tree, config, latest)
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


def _latest_version(tree: Path) -> str | None:
    """Which version `latest` points at. mike materialises the alias as a symlink."""
    alias = tree / "latest"
    if alias.is_symlink():
        return Path(alias.readlink()).name
    versions = tree / "versions.json"
    if versions.is_file():
        return alias_target(read_versions_json(fsops.read_text(versions)), "latest")
    return None


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
    """A bare version root must redirect into the documentation.

    The stricter assertions are the interesting ones: a meta refresh, so it works for a client
    that does not run JavaScript, and a relative target, because `latest` is a symlink to a
    version folder and the same file answers at both URLs — an absolute target would leak a
    version number to visitors of the stable one.
    """
    where = f"{version}/index.html"
    index = version_dir / "index.html"
    if not index.is_file():
        return [Finding("version-root", where, "missing")]

    text = fsops.read_text(index)
    if GENERATED_MARKER not in text:
        return [
            Finding(
                "version-root",
                where,
                "is not a generated redirect; publish this version, or run `ovweb redirects "
                "apply`, so a bare version root leads into the documentation",
            )
        ]

    findings = []
    if 'http-equiv="refresh"' not in text:
        findings.append(
            Finding("version-root", where, "has no meta refresh, so it needs JavaScript to work")
        )
    absolute = re.search(r'(?:content="0; url=|<a href=")(/[^"\s>]*)', text)
    if absolute:
        findings.append(
            Finding(
                "version-root",
                where,
                f"redirect target {absolute.group(1)!r} is site-absolute, which would leak the "
                "version number to visitors of /latest/",
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


def _check_versioned_pages_reach_root_files(
    tree: Path, version: str, config: SiteConfig
) -> list[Finding]:
    """A versioned page must not link to a root file relative to its own version folder.

    The RSS feeds, `robots.txt` and friends are served from the site root; a version folder does
    not keep a copy. The theme emits two `<link rel="alternate">` feed references on every page,
    which resolve inside the version folder unless they are made root-absolute.
    """
    names = [name for name in config.layout.root_files if not name.startswith("index.")]
    if not names:
        return []
    pattern = re.compile(r'href="(?:\.\./)*(' + "|".join(re.escape(name) for name in names) + r')"')

    findings = []
    for page in config.layout.versioned_pages:
        root = tree / version / page
        if not root.is_dir():
            continue
        for path in root.rglob("*.html"):
            match = pattern.search(fsops.read_text(path))
            if match:
                findings.append(
                    Finding(
                        "versioned-root-file-link",
                        str(path.relative_to(tree)),
                        f"links to {match.group(1)} relative to the version folder, where it is "
                        "not published",
                    )
                )
                break  # one report per versioned section is enough to act on
    return findings


def _check_exports_reach_root_pages(tree: Path, version: str, config: SiteConfig) -> list[Finding]:
    """A version's Markdown exports must not link to a root page under the version.

    The llmstxt plugin absolutises every link against the build's `site_url`, which mike makes
    versioned, so a link to a page that is only ever served from the site root comes out as a URL
    that has never existed. Unlike the stale-version problem this is a hard 404, and it is
    invisible to a link checker that reads the HTML only.
    """
    findings = []
    for page in config.layout.versioned_pages:
        root = tree / version / page
        if not root.is_dir():
            continue
        for path in sorted(root.rglob(f"*{MARKDOWN}")):
            text = fsops.read_text(path)
            dead = next(
                (
                    f"/{version}/{name}/"
                    for name in config.layout.non_versioned_pages
                    if f"/{version}/{name}/" in text
                ),
                None,
            )
            if dead:
                findings.append(
                    Finding(
                        "export-root-page-link",
                        str(path.relative_to(tree)),
                        f"links to {dead}, but that page is served only from the site root, so "
                        "the versioned URL is a 404",
                    )
                )
                break  # one report per versioned section is enough to act on
    return findings


def _check_root_exports_use_latest(
    tree: Path, config: SiteConfig, latest: str | None
) -> list[Finding]:
    """No file served from the root may pin the version `latest` currently points at.

    Covers the site's AI-facing channel: `llms.txt`, the `llms-full.txt` concatenation, and the
    `index.md` export published beside every root page. They are rebuilt from the newest version
    on every publish, so a URL naming that version is stale the moment the next one ships — and
    for a page served only from the root, it never resolved at all.

    A pin to some *other* version is left alone: that is how a release-notes page links back to
    the release before it, and the point of publishing versioned documentation.
    """
    if latest is None:
        return []

    candidates = [tree / name for name in LLMS_FILES]
    candidates.append(tree / f"index{MARKDOWN}")
    for page in config.layout.non_versioned_pages:
        root = tree / page
        if root.is_dir():
            candidates += sorted(root.rglob(f"*{MARKDOWN}"))

    needle = f"/{latest}/"
    findings = []
    for path in candidates:
        if not path.is_file():
            continue
        if needle in fsops.read_text(path):
            findings.append(
                Finding(
                    "root-export-version-pin",
                    str(path.relative_to(tree)),
                    f"holds {needle!r}; a file served from the root reaches versioned "
                    "documentation at /latest/, and a root page at its own unversioned URL",
                )
            )
    return findings


def _check_root_search_index_uses_latest(
    tree: Path, config: SiteConfig, published: list[str]
) -> list[Finding]:
    """The root index must not send a searcher to a version-pinned URL.

    It is a copy of the newest version's index, so its versioned hits name that version unless
    they are repointed. Each version's own index keeps its version on purpose, so that searching
    inside a version returns that version's pages — only the root copy is checked here.
    """
    path = tree / "search" / "search_index.json"
    if not path.is_file():
        return []
    text = fsops.read_text(path)
    findings = []
    for page in config.layout.versioned_pages:
        for version in published:
            needle = f'"location":"/{version}/{page}/'
            if needle in text:
                findings.append(
                    Finding(
                        "root-search-index",
                        "search/search_index.json",
                        f"holds {needle!r}; a hit on versioned documentation should point at "
                        "/latest/, which is the canonical URL and does not go stale",
                    )
                )
                break
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
