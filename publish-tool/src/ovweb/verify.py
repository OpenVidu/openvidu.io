"""Assert the invariants of a published gh-pages tree.

Written so it passes on the live site as it stands, which makes it both a post-publish signal
and a check that the tool's model of the published layout is right.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import fsops
from .config import SiteConfig
from .discovery import latest_in_tree, version_folders, versions_in_tree
from .expand import alias_entries, expand_alias, mirror_redirects, mirror_rule, scan_tree
from .pipeline.postprocess import LLMS_TXT
from .redirects import (
    REDIRECT_MAX_BYTES,
    REFRESH_TARGET,
    RedirectError,
    is_generated_redirect,
)
from .rewrite.markdown import SUFFIX as MARKDOWN

SELF_URL_TAGS = re.compile(r'(?:rel="canonical" href|property="og:url" content)="([^"]+)"')
SITEMAP_LASTMOD = re.compile(r"<lastmod>([^<]*)</lastmod>")


@dataclass
class Finding:
    check: str
    where: str
    detail: str


def verify(tree: Path, *, config: SiteConfig) -> list[Finding]:
    """Return every invariant violation found in `tree`. An empty list means it is sound."""
    findings: list[Finding] = []

    published = versions_in_tree(tree)
    latest = latest_in_tree(tree)

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
    findings += _check_export_links_resolve(tree, config, latest)
    findings += _check_root_sitemap_lastmod(tree)
    findings += _check_unversioned_mirror(tree, config, latest)
    findings += _check_alias_folders(tree, config)
    findings += _check_redirect_targets_resolve(tree, config, published, latest)
    return findings


def _check_versions_json(tree: Path, published: list[str]) -> list[Finding]:
    """Every version in versions.json has a folder, and every version folder is listed."""
    findings = []
    for version in published:
        if not (tree / version).is_dir():
            findings.append(
                Finding("versions-json", "versions.json", f"{version} has no folder in the tree")
            )

    for orphan in sorted(set(version_folders(tree)) - set(published)):
        findings.append(
            Finding(
                "versions-json",
                orphan,
                "folder is published but missing from versions.json, so the version selector "
                "will not offer it",
            )
        )
    return findings


def _check_redirect_targets_resolve(
    tree: Path, config: SiteConfig, published: list[str], latest: str | None
) -> list[Finding]:
    """No generated redirect may point at a page that does not exist, or at another redirect.

    A redirect into a 404 is worse than the 404 it replaced: the visitor takes two hops to reach
    nothing, and a crawler is told the content moved somewhere it did not. This happens when a
    rule's `versions` gate is wider than its target's — a rule for a page renamed in 3.8, gated
    `>=3.7`, materialises in 3.7 too, where the successor does not exist yet. The fix is a `when`
    override for the older band rather than a wider gate.

    A redirect into another redirect is a chain: the expansions collapse them at generation
    time, so one surviving to a published tree means a `files` rule targets another rule's stub.
    """
    directories = [tree / version for version in published]
    directories += [tree / section for section in config.layout.versioned_pages]
    directories += [tree / folder for _, folder, _ in alias_entries(config)]
    findings = []

    for root in directories:
        if not root.is_dir() or root.is_symlink():
            continue
        for path in sorted(root.rglob("*.html")):
            if path.is_symlink() or path.stat().st_size > REDIRECT_MAX_BYTES:
                continue
            if not is_generated_redirect(path):
                continue
            text = fsops.read_text(path)
            match = REFRESH_TARGET.search(text)
            where = str(path.relative_to(tree))
            if match is None:
                findings.append(Finding("redirect-target", where, "has no meta refresh target"))
                continue
            # The fragment is the browser's business; existence is decided by the path.
            target = match.group(1).partition("#")[0]
            if not target:
                continue
            if target.startswith("/"):
                # Site-absolute, so resolved from the tree root. `latest` is a symlink, which
                # only resolves on a checkout that has it; name the version instead.
                relative = target.lstrip("/")
                if latest is not None:
                    relative = re.sub(r"^latest/", f"{latest}/", relative)
                resolved = tree / relative
            else:
                resolved = path.parent / target
            served = resolved / "index.html" if target.endswith("/") else resolved
            if not served.is_file():
                findings.append(
                    Finding(
                        "redirect-target",
                        where,
                        f"redirects to {target!r}, which does not exist in this tree "
                        f"({served.relative_to(tree)}); the rule's version gate is wider than "
                        "its target's, so it needs a `when` override for the older versions",
                    )
                )
            elif is_generated_redirect(served):
                findings.append(
                    Finding(
                        "redirect-target",
                        where,
                        f"redirects to {target!r}, which is itself a generated redirect; point "
                        "the rule at the final destination instead of chaining",
                    )
                )
    return findings


def _check_version_root_is_redirect(version_dir: Path, version: str) -> list[Finding]:
    """A bare version root must redirect into the documentation.

    Also asserts a meta refresh, so it works without JavaScript, and a relative target, because
    `latest` is a symlink to a version folder and the same file answers at both URLs.
    """
    where = f"{version}/index.html"
    index = version_dir / "index.html"
    if not index.is_file():
        return [Finding("version-root", where, "missing")]

    if not is_generated_redirect(index):
        return [
            Finding(
                "version-root",
                where,
                "is not a generated redirect; publish this version, or run `ovweb redirects "
                "apply`, so a bare version root leads into the documentation",
            )
        ]

    text = fsops.read_text(index)
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
    """A version folder must carry a correctly pruned sitemap.

    Not for crawlers, but because the theme's version selector fetches it to decide whether the
    page the reader is on exists in the version they picked. Each of the three assertions below
    silently turns that off on its own, leaving every switch on the version root:

    * the file is missing, so the fetch fails;
    * the version-root entry is absent, so the longest common prefix of the remaining URLs is not
      itself an entry, which the selector requires before it resolves anything;
    * a root-served page is still listed, so a reader on `/pricing/` is sent to
      `/<version>/pricing/`, which is a 404.
    """
    where = f"{version}/sitemap.xml"
    path = tree / version / "sitemap.xml"
    if not path.is_file():
        return [
            Finding(
                "version-sitemap",
                where,
                "missing, so the version selector cannot tell whether the reader's page exists "
                "in this version and will drop them on the version root; publish this version",
            )
        ]

    text = fsops.read_text(path)
    findings = []
    if f"<loc>{config.layout.base_url}/{version}/</loc>" not in text:
        findings.append(
            Finding(
                "version-sitemap",
                where,
                "has no entry for the version root, which the version selector needs as the "
                "common prefix of every URL before it will resolve one",
            )
        )
    for page in config.layout.non_versioned_pages:
        if f"/{version}/{page}/" in text:
            findings.append(
                Finding(
                    "version-sitemap",
                    where,
                    f"lists /{version}/{page}/, which is served only from the site root; the "
                    "version selector would send a reader there and get a 404",
                )
            )
    return findings


def _check_versioned_pages_reach_root_files(
    tree: Path, version: str, config: SiteConfig
) -> list[Finding]:
    """A versioned page must not link to a root file relative to its own version folder.

    The RSS feeds, `robots.txt` and friends are served from the site root and a version folder
    keeps no copy, so the two `<link rel="alternate">` feed references the theme emits on every
    page resolve nowhere unless they are made root-absolute.
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
    versioned, so a link to a page served only from the site root comes out as a URL that has
    never existed — a hard 404, and invisible to a link checker that reads the HTML only.
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

    Covers the site's AI-facing channel: `llms.txt` and the `index.md` export beside every root
    page. They are rebuilt from the newest version on every publish, so a URL naming that version
    is stale the moment the next one ships.

    A pin to some *other* version is left alone: that is how a release-notes page links back to
    the release before it.
    """
    if latest is None:
        return []

    candidates = [tree / LLMS_TXT]
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


def _check_root_sitemap_lastmod(tree: Path) -> list[Finding]:
    """Every `<lastmod>` in the root sitemap must be a real date, and not in the future.

    The values come from each page's last commit (see :mod:`ovweb.sources`). A malformed value
    invalidates the entry; a future one is the signature of a clock or timezone bug.

    Deliberately *not* asserted: that the values differ from each other. A commit that touches
    every page legitimately gives all of them the same date.
    """
    path = tree / "sitemap.xml"
    if not path.is_file():
        return []
    today = date.today().isoformat()
    findings: list[Finding] = []
    for value in SITEMAP_LASTMOD.findall(fsops.read_text(path) or ""):
        try:
            parsed = date.fromisoformat(value[:10]).isoformat()
        except ValueError:
            findings.append(
                Finding("sitemap-lastmod", "sitemap.xml", f"{value!r} is not an ISO date")
            )
            continue
        if parsed > today:
            findings.append(
                Finding(
                    "sitemap-lastmod",
                    "sitemap.xml",
                    f"{value!r} is in the future, so it describes an edit that has not happened",
                )
            )
    return findings


def _check_unversioned_mirror(tree: Path, config: SiteConfig, latest: str | None) -> list[Finding]:
    """The unversioned mirror must be exactly one stub per page of the newest version.

    Asserted as set equality against the same function the publish generates it with, which
    catches both failures: a **missing** stub means an unversioned URL 404s for crawlers again,
    an **extra** one means a renamed or removed page now redirects into a 404.
    """
    rule = mirror_rule(config)
    if rule is None or latest is None:
        return []

    try:
        expected = {redirect.path for redirect in mirror_redirects(tree, config, latest=latest)}
    except RedirectError as error:
        return [Finding("mirror", str(tree), str(error))]

    return _check_owned_scope(
        tree,
        roots=[tree / section for section in getattr(config.layout, rule.for_each)],
        expected=expected,
        check="mirror",
        rebuild="Publish latest, or run `ovweb redirects apply`, to rebuild the mirror",
    )


def _check_alias_folders(tree: Path, config: SiteConfig) -> list[Finding]:
    """Every legacy patch folder must be exactly one stub per page of the minor it aliases.

    A folder whose minor is not in the tree is skipped, matching how the folders are built.
    """
    findings: list[Finding] = []
    for rule, folder, minor in alias_entries(config):
        if not (tree / minor).is_dir():
            continue
        expected = {
            redirect.path
            for redirect in expand_alias(config, rule, folder, minor, scan_tree(tree, (minor,)))
        }
        if not (tree / folder).is_dir():
            findings.append(
                Finding(
                    "version-alias",
                    folder,
                    f"folder not built, so /{folder}/ URLs answer 404; run `ovweb redirects apply`",
                )
            )
            continue
        findings += _check_owned_scope(
            tree,
            roots=[tree / folder],
            expected=expected,
            check="version-alias",
            rebuild=f"Publish {minor}, or run `ovweb redirects apply`, to rebuild the folder",
        )
    return findings


def _check_owned_scope(
    tree: Path, *, roots: list[Path], expected: set[str], check: str, rebuild: str
) -> list[Finding]:
    """Set equality over a directory ovweb owns outright: every file a stub, no more, no less."""
    found: set[str] = set()
    findings: list[Finding] = []

    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_dir():
                continue
            where = path.relative_to(tree).as_posix()
            if is_generated_redirect(path):
                found.add(where)
                continue
            # Reported here rather than counted as stale below: the reason it does not belong
            # is different, it is not a redirect at all.
            findings.append(
                Finding(
                    check,
                    where,
                    "sits on a generated path but is not a generated redirect, so the next "
                    "rebuild would delete it",
                )
            )

    missing = sorted(expected - found)
    if missing:
        findings.append(
            Finding(
                check,
                missing[0],
                f"one of {len(missing)} URL(s) with no redirect page: they 404 for a crawler. "
                + rebuild,
            )
        )
    stale = sorted(found - expected)
    if stale:
        findings.append(
            Finding(
                check,
                stale[0],
                f"one of {len(stale)} redirect page(s) no current page justifies, so they may "
                "redirect into a 404. " + rebuild,
            )
        )
    return findings


def _check_export_links_resolve(
    tree: Path, config: SiteConfig, latest: str | None
) -> list[Finding]:
    """No Markdown export may link to another export that does not exist.

    The llmstxt plugin appends `index.md` to every relative directory link without checking that
    the page has an export, so any page outside its `sections` list is advertised at a URL that
    404s. The publish repairs those links against the tree.

    Only the newest version and the site root are checked: older folders keep whatever their own
    last publish produced, which only a publish of that version can change.
    """
    if latest is None:
        return []

    base = f"{config.layout.base_url}/"
    pattern = re.compile(re.escape(base) + r"(?P<page>(?:[^)\s#\"']*/)?)index\.md")

    def resolves(page: str) -> bool:
        if page.startswith("latest/"):
            page = f"{latest}/{page[len('latest/') :]}"
        return (tree / page / "index.md").is_file()

    candidates = [tree / f"index{MARKDOWN}", tree / LLMS_TXT]
    for page in (*config.layout.non_versioned_pages, latest):
        root = tree / page
        if root.is_dir():
            candidates += sorted(root.rglob(f"*{MARKDOWN}"))

    findings = []
    for path in candidates:
        if not path.is_file():
            continue
        dead = {m.group("page") for m in pattern.finditer(fsops.read_text(path))}
        broken = sorted(page for page in dead if not resolves(page))
        if broken:
            findings.append(
                Finding(
                    "export-link",
                    str(path.relative_to(tree)),
                    f"links to {len(broken)} Markdown export(s) that do not exist, starting with "
                    f"{base}{broken[0]}index.md; the link should point at the page instead",
                )
            )
    return findings


def _check_root_search_index_uses_latest(
    tree: Path, config: SiteConfig, published: list[str]
) -> list[Finding]:
    """The root index must not send a searcher to a version-pinned URL.

    It is a copy of the newest version's index, so its versioned hits name that version unless
    they are repointed. Each version's own index keeps its version on purpose, so only the root
    copy is checked here.
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
