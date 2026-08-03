"""Assert the invariants of a published gh-pages tree.

Deliberately written so it passes on the *live* site as it stands today: that makes it the
cheapest available check that the tool's understanding of the published layout is right, and
it turns "the publish worked" into something a machine can answer.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import fsops
from .config import SiteConfig
from .pipeline.postprocess import GENERATED_MARKER, LLMS_TXT
from .redirects import MIRROR_RULE_ID, mirror_redirects
from .rewrite.markdown import SUFFIX as MARKDOWN
from .versions import alias_target, read_versions_json

SELF_URL_TAGS = re.compile(r'(?:rel="canonical" href|property="og:url" content)="([^"]+)"')
RELATIVE_PARENT_HREF = re.compile(r'href="((?:\.\./)+[^"]*)"')
SITEMAP_LASTMOD = re.compile(r"<lastmod>([^<]*)</lastmod>")
REFRESH_TARGET = re.compile(r'http-equiv="refresh" content="0; *url=([^"]+)"')

#: A generated redirect page is about 2 KB, while a real page carries the theme chrome and is
#: never close to this small. Only used to avoid reading every file in the tree before the
#: `GENERATED_MARKER` check decides what is actually a redirect.
REDIRECT_MAX_BYTES = 8192


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
    findings += _check_export_links_resolve(tree, config, latest)
    findings += _check_root_sitemap_lastmod(tree)
    findings += _check_unversioned_mirror(tree, config)
    findings += _check_redirect_targets_resolve(tree, config, published, latest)
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


def _check_redirect_targets_resolve(
    tree: Path, config: SiteConfig, published: list[str], latest: str | None
) -> list[Finding]:
    """No generated redirect may point at a page that does not exist.

    A redirect into a 404 is worse than the 404 it replaced: the visitor now takes two hops to
    reach nothing, and a crawler is told the content moved somewhere that is not there. The way
    this happens is a rule gated to a version range wider than its target's: a `files` rule for a
    page that was renamed in 3.8, gated `>=3.7`, materialises in 3.7 as well — where the
    successor page does not exist yet. That is a real defect this check was written for, caught in
    review of a rule aimed at `features/users/overview/`, which arrived one release after the
    page it replaced went away.

    Every rule is resolved per version, so the fix is a `when` override for the older band rather
    than a wider gate.
    """
    directories = [tree / version for version in published]
    directories += [tree / section for section in config.layout.versioned_pages]
    findings = []

    for root in directories:
        if not root.is_dir() or root.is_symlink():
            continue
        for path in sorted(root.rglob("*.html")):
            if path.is_symlink() or path.stat().st_size > REDIRECT_MAX_BYTES:
                continue
            text = fsops.read_text(path)
            if GENERATED_MARKER not in text:
                continue
            match = REFRESH_TARGET.search(text)
            where = str(path.relative_to(tree))
            if match is None:
                findings.append(Finding("redirect-target", where, "has no meta refresh target"))
                continue
            target = match.group(1)
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
    """A version folder must carry a correctly pruned sitemap.

    Not for crawlers — nothing links to it and `robots.txt` does not name it — but because the
    theme's version selector fetches it to decide whether the page the reader is on exists in the
    version they picked. All three assertions below are things that silently turn the feature off
    and leave every switch dropping the reader on the version root:

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

    Covers the site's AI-facing channel: `llms.txt` and the `index.md` export published beside
    every root page. They are rebuilt from the newest version
    on every publish, so a URL naming that version is stale the moment the next one ships — and
    for a page served only from the root, it never resolved at all.

    A pin to some *other* version is left alone: that is how a release-notes page links back to
    the release before it, and the point of publishing versioned documentation.
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

    The values come from each page's last commit (see `ovweb.sources`), which is only useful to a
    crawler while it stays credible: a malformed value invalidates the entry, and a future one is
    the signature of a clock or timezone bug rather than of an edit.

    Deliberately *not* asserted: that the values differ from each other. A commit that touches
    every page — a site-wide frontmatter pass, say — legitimately gives all of them the same date,
    and a check that failed on that would be a check that fails on the truth.
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


def _check_unversioned_mirror(tree: Path, config: SiteConfig) -> list[Finding]:
    """The unversioned mirror must be exactly the set of pages the sitemap advertises.

    Asserted as set equality against the same pure function the publish generates it with, which
    catches both halves of the only way this can go wrong. A **missing** stub means an
    unversioned URL 404s for crawlers again — the defect this mirror exists to fix. An **extra**
    stub means a page was renamed or removed and its redirect now points into a 404, which is
    worse than the plain 404 it replaced. The publish deletes and rebuilds the whole mirror to
    make the second case unreachable; this is the assertion that it did.
    """
    rule = config.mirror
    if rule is None or not rule.enabled:
        return []
    sitemap = tree / "sitemap.xml"
    if not sitemap.is_file():
        return []

    text = fsops.read_text(sitemap)
    expected = {redirect.path for redirect in mirror_redirects(text, config=config)}
    found: set[str] = set()
    findings: list[Finding] = []

    for section in getattr(config.layout, rule.for_each):
        root = tree / section
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_dir():
                continue
            where = path.relative_to(tree).as_posix()
            head = path.read_bytes()[:512].decode("utf-8", errors="replace")
            if path.name == "index.html" and GENERATED_MARKER in head and MIRROR_RULE_ID in head:
                found.add(where)
                continue
            # Reported here rather than counted as a stale stub below, because the reason it does
            # not belong is different: it is not a redirect at all.
            findings.append(
                Finding(
                    "mirror",
                    where,
                    "sits on a mirrored path but is not a generated mirror redirect, so the "
                    "next publish would delete it",
                )
            )

    missing = sorted(expected - found)
    if missing:
        findings.append(
            Finding(
                "mirror",
                missing[0],
                f"one of {len(missing)} unversioned URL(s) the sitemap advertises under /latest/ "
                "with no redirect page: they 404 for a crawler. Publish latest to rebuild the "
                "mirror",
            )
        )
    stale = sorted(found - expected)
    if stale:
        findings.append(
            Finding(
                "mirror",
                stale[0],
                f"one of {len(stale)} redirect page(s) pointing at a page the sitemap no longer "
                "lists, so they redirect into a 404. Publish latest to rebuild the mirror",
            )
        )
    return findings


def _check_export_links_resolve(
    tree: Path, config: SiteConfig, latest: str | None
) -> list[Finding]:
    """No Markdown export may link to another export that does not exist.

    The llmstxt plugin appends `index.md` to every relative directory link without checking that
    the page has an export, so any page outside its `sections` list is advertised at a URL that
    404s. The publish repairs those links against the tree; this is the assertion that it did.

    Only the newest version and the site root are checked. Older folders keep whatever their own
    last publish produced, so reporting them would be reporting work that a publish of that
    version — not this check — has to do.
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
