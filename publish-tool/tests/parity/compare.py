#!/usr/bin/env python3
"""Compare two post-processed trees and report every difference that is not expected.

Used instead of `diff -r` for three reasons: gzip members have to be compared decompressed, since
gzip writes the source mtime into its header and an unchanged sitemap would otherwise look
changed; time-dependent fields have to be blanked when the two trees came from separate builds;
and each intentional difference must be asserted on its own rather than filtered out of a text
diff by eye.

Exit code 0 means the two trees agree everywhere except in the ways listed below.

Usage:
    compare.py OLD NEW VERSION [--blank-volatile]
"""

from __future__ import annotations

import gzip
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

# Fields whose value is the time of the build. Only relevant to the end-to-end comparison, where
# the two trees are built separately; a stage-isolated run shares one build and these already
# match.
VOLATILE = (
    re.compile(rb"<lastmod>[^<]*</lastmod>"),
    re.compile(rb"<pubDate>[^<]*</pubDate>"),
    re.compile(rb"<lastBuildDate>[^<]*</lastBuildDate>"),
    re.compile(rb"<atom:updated>[^<]*</atom:updated>"),
    re.compile(rb'"date_published":"[^"]*"'),
    re.compile(rb'"date_modified":"[^"]*"'),
)

#: Mirrors `layout.root_files` minus the `index.*` entries: the files a versioned page may link
#: relatively and that the publish makes root-absolute. If this drifts from ovweb.yaml the gate
#: reports the difference as unexpected rather than hiding it, which is the safe direction.
ROOT_FILES = (
    "404.html",
    "robots.txt",
    "llms.txt",
    "feed_rss_created.xml",
    "feed_rss_updated.xml",
    "feed_json_created.json",
    "feed_json_updated.json",
    "rss.xsl",
)
RELATIVE_ROOT_FILE = re.compile(
    rb'href="(?:\.\./)*(' + b"|".join(re.escape(name.encode()) for name in ROOT_FILES) + rb')"'
)

#: The rest of `layout`, restated here for the same reason as ROOT_FILES: the reconcilers below
#: have to say independently what the rewrite should do, or they only restate the code they check.
VERSIONED_PAGES = ("docs", "meet")
NON_VERSIONED_PAGES = (
    "account",
    "pricing",
    "support",
    "openvidu-meet-vs-openvidu-platform",
    "conditions",
    "blog",
    "about-us",
    "research",
    "acknowledgments",
)
PROMOTED_FILES = ("index.html", "index.md", *ROOT_FILES)

#: A path inside a version folder, e.g. "3.8/docs/index.md".
VERSION_FOLDER = re.compile(r"\d+\.\d+/")

#: A page of the unversioned mirror, e.g. "docs/ai/live-captions/index.html". Anchored outside any
#: version folder: `3.8/docs/…/index.html` is a real page in both trees.
MIRROR_PAGE = re.compile(r"(?:" + "|".join(VERSIONED_PAGES) + r")/(?:[^/]+/)*index\.html$")

#: Markdown link or image target that is root-relative, excluding protocol-relative URLs.
ROOT_RELATIVE_TARGET = re.compile(rb"\]\(/(?!/)")
BASE_URL = b"https://openvidu.io"


@dataclass
class Expected:
    """One intentional difference between the two implementations.

    `matches` selects by path. `reconciles`, when given, must additionally show that the *only*
    difference is the intended one: it transforms the old bytes the way the new implementation
    would and requires the result to be identical. An expectation selected by path alone waves
    through any other change to those files, so anything covering more than a handful of paths
    needs one.
    """

    reason: str
    matches: Callable[[str], bool]
    reconciles: Callable[[bytes, bytes], bool] | None = None
    seen: list[str] = field(default_factory=list)


def _root_file_links_reconcile(old: bytes, new: bytes) -> bool:
    """The difference is exactly `href="../../<root file>"` becoming `href="/<root file>"`."""
    return RELATIVE_ROOT_FILE.sub(rb'href="/\1"', old) == new


def _search_index_reconciles(version: str) -> Callable[[bytes, bytes], bool]:
    """The difference is exactly the versioned `"location"` values moving to `/latest/`."""

    def reconcile(old: bytes, new: bytes) -> bool:
        rewritten = old
        for page in (b"docs", b"meet"):
            rewritten = rewritten.replace(
                b'"location":"/' + version.encode() + b"/" + page + b"/",
                b'"location":"/latest/' + page + b"/",
            )
        return rewritten == new

    return reconcile


def _drop_version_from_root_urls(data: bytes, version: str) -> bytes:
    """Every URL for something served only from the site root loses the version segment."""
    pinned = version.encode()
    for page in NON_VERSIONED_PAGES:
        data = data.replace(
            b"/" + pinned + b"/" + page.encode() + b"/", b"/" + page.encode() + b"/"
        )
    for name in PROMOTED_FILES:
        data = data.replace(b"/" + pinned + b"/" + name.encode(), b"/" + name.encode())
    return data


def _point_versioned_urls_at_latest(data: bytes, version: str) -> bytes:
    for page in VERSIONED_PAGES:
        data = data.replace(
            b"/" + version.encode() + b"/" + page.encode() + b"/",
            b"/latest/" + page.encode() + b"/",
        )
    return data


def _absolutise(data: bytes) -> bytes:
    """Root-relative Markdown targets become absolute URLs."""
    return ROOT_RELATIVE_TARGET.sub(b"](" + BASE_URL + b"/", data)


def _forget_export_suffix(data: bytes) -> bytes:
    """Erase the distinction between `…/x/index.md` and `…/x/` on both sides of a comparison.

    The publish repairs a link naming a Markdown export that was never generated, which depends on
    what the build actually produced and so cannot be recomputed from the old bytes alone. Applying
    this to both sides leaves the reconciler proving the useful half: that *nothing else* changed.
    The repair's own correctness is pinned by tests/unit/test_rewrite_markdown.py, and by
    `ovweb verify`.
    """
    return data.replace(b"/index.md", b"/")


def _versioned_export_reconciles(version: str) -> Callable[[bytes, bytes], bool]:
    """The root-served URLs lose the version; root-relative targets become absolute.

    A link into the export's own version stays pinned, so that an in-version reader keeps
    reading that version — the same asymmetry the search index has.
    """

    def reconcile(old: bytes, new: bytes) -> bool:
        rewritten = _absolutise(_drop_version_from_root_urls(old, version))
        return _forget_export_suffix(rewritten) == _forget_export_suffix(new)

    return reconcile


def _promoted_export_reconciles(version: str) -> Callable[[bytes, bytes], bool]:
    """The same, plus the versioned URLs moving to `/latest/`.

    The export has no version of its own, so it reaches versioned documentation the same way
    every other root file does.
    """

    def reconcile(old: bytes, new: bytes) -> bool:
        rewritten = _point_versioned_urls_at_latest(old, version)
        rewritten = _absolutise(_drop_version_from_root_urls(rewritten, version))
        return _forget_export_suffix(rewritten) == _forget_export_suffix(new)

    return reconcile


#: `llms.txt` is a root-served Markdown file, so the promoted rules apply to it unchanged.
_llms_file_reconciles = _promoted_export_reconciles


def _redirect_paths(version: str) -> frozenset[str]:
    """Exactly the paths a redirect is installed at for this version.

    Which ones depends on the version band, so this cannot be a loose pattern: from 3.4 onwards
    `<version>/docs/index.html` is a real page, and treating it as a redirect would wave through
    any change to the Platform documentation landing page.
    """
    paths = {f"{version}/index.html"}
    major, _, minor = version.partition(".")
    if (int(major), int(minor)) >= (3, 4):
        paths.add(f"{version}/docs/getting-started/index.html")
    else:
        paths.add(f"{version}/docs/index.html")
    return frozenset(paths)


def expectations(version: str) -> list[Expected]:
    redirects = _redirect_paths(version)
    versioned_prefixes = tuple(f"{version}/{page}/" for page in ("docs", "meet"))
    return [
        Expected(
            "the generated redirect pages replace the hand-written stub, and add one the shell "
            "had no way to express",
            lambda path: path in redirects,
        ),
        Expected(
            "the build cache is not in a fresh worktree, so it can no longer be committed by "
            "accident",
            lambda path: path.startswith((".cache", "site/")),
        ),
        Expected(
            "every documentation page now answers at its unversioned URL as well, with a real "
            "redirect page. The shell had only the 404 router for those URLs, which GitHub serves "
            "with a 404 status — the thing a search engine acts on before it runs any JavaScript. "
            "No reconciler: these paths exist in ovweb's tree only, so there are no old bytes to "
            "transform. What they contain is asserted by `ovweb verify` and the unit tests",
            lambda path: MIRROR_PAGE.fullmatch(path) is not None,
        ),
        # No expectation for <X.Y>/sitemap.xml: the pruning is back, so it must match the shell's
        # output byte for byte. It was briefly deleted instead, which silently turned off the
        # version selector's "keep the reader on the same page" behaviour — the gate could not
        # catch that, because an expectation had been written for the deletion. Gzip members are
        # compared decompressed, so the deterministic .gz header is invisible here.
        Expected(
            "the root search index sends a hit on versioned documentation to /latest/ instead of "
            "pinning the version it was copied from",
            lambda path: path == "search/search_index.json",
            _search_index_reconciles(version),
        ),
        Expected(
            "versioned pages link to the root files — the RSS feeds above all — at the site root, "
            "where they are published, instead of relative to a version folder that keeps no copy",
            lambda path: path.startswith(versioned_prefixes) and path.endswith(".html"),
            _root_file_links_reconcile,
        ),
        Expected(
            "the Markdown export of a versioned page no longer links to a root-served page under "
            "the version, which was a hard 404: that page has no versioned URL at all",
            lambda path: path.startswith(versioned_prefixes) and path.endswith(".md"),
            _versioned_export_reconciles(version),
        ),
        Expected(
            "the Markdown export of a page promoted to the root reaches versioned documentation "
            "at /latest/, like every other root file, instead of pinning the published version",
            # Anchored to "outside any version folder", not merely "outside this one": a publish
            # must not touch another version's exports, and `not path.startswith(version)` would
            # have waved that through.
            lambda path: path.endswith(".md") and not VERSION_FOLDER.match(path),
            _promoted_export_reconciles(version),
        ),
        Expected(
            "llms.txt gets the root rewrites. llms-full.txt appears in neither tree: the build no "
            "longer generates it, because one concatenation of every export reached 2.8 MB — about "
            "700k tokens, which nothing can load — duplicating content the exports already serve",
            lambda path: path in ("llms.txt", "llms-full.txt"),
            _llms_file_reconciles(version),
        ),
    ]


def normalise(data: bytes, *, blank_volatile: bool) -> bytes:
    if not blank_volatile:
        return data
    for pattern in VOLATILE:
        data = pattern.sub(b"<VOLATILE/>", data)
    return data


def read(path: Path) -> bytes:
    data = path.read_bytes()
    if path.suffix == ".gz":
        try:
            return gzip.decompress(data)
        except OSError:
            return data
    return data


def walk(root: Path) -> dict[str, Path]:
    found = {}
    for path in root.rglob("*"):
        if path.is_dir() and not path.is_symlink():
            continue
        found[str(path.relative_to(root))] = path
    return found


def main(argv: list[str]) -> int:
    if len(argv) not in (4, 5):
        print(__doc__, file=sys.stderr)
        return 2

    old_root, new_root, version = Path(argv[1]), Path(argv[2]), argv[3]
    blank_volatile = "--blank-volatile" in argv

    old, new = walk(old_root), walk(new_root)
    expected = expectations(version)
    unexpected: list[str] = []

    def classify(
        path: str, problem: str, old_bytes: bytes | None = None, new_bytes: bytes | None = None
    ) -> None:
        for rule in expected:
            if not rule.matches(path):
                continue
            if rule.reconciles is not None:
                if old_bytes is None or new_bytes is None:
                    continue
                if not rule.reconciles(old_bytes, new_bytes):
                    continue
            rule.seen.append(f"{path}: {problem}")
            return
        unexpected.append(f"{path}: {problem}")

    for path in sorted(set(old) | set(new)):
        if path not in new:
            classify(path, "present in the shell's output, absent from ovweb's")
            continue
        if path not in old:
            classify(path, "present in ovweb's output, absent from the shell's")
            continue

        old_path, new_path = old[path], new[path]
        if old_path.is_symlink() or new_path.is_symlink():
            if old_path.is_symlink() != new_path.is_symlink():
                classify(path, "one side is a symlink and the other is not")
            elif old_path.readlink() != new_path.readlink():
                classify(path, f"symlink target {old_path.readlink()} vs {new_path.readlink()}")
            continue

        old_bytes = normalise(read(old_path), blank_volatile=blank_volatile)
        new_bytes = normalise(read(new_path), blank_volatile=blank_volatile)
        if old_bytes != new_bytes:
            classify(
                path,
                f"content differs ({len(old_bytes)} vs {len(new_bytes)} bytes)",
                old_bytes,
                new_bytes,
            )

    print(f"Compared {len(set(old) | set(new))} paths for version {version}.\n")

    for rule in expected:
        status = f"{len(rule.seen)} path(s)" if rule.seen else "none"
        print(f"expected: {rule.reason}\n          -> {status}")
        for line in rule.seen[:10]:
            print(f"             {line}")
        if len(rule.seen) > 10:
            print(f"             ... and {len(rule.seen) - 10} more")
        print()

    if unexpected:
        print(f"UNEXPECTED DIFFERENCES ({len(unexpected)}):")
        for line in unexpected[:200]:
            print(f"  {line}")
        if len(unexpected) > 200:
            print(f"  ... and {len(unexpected) - 200} more")
        return 1

    print("PARITY: no unexpected differences.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
