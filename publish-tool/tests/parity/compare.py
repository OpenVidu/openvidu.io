#!/usr/bin/env python3
"""Compare two post-processed trees and report every difference that is not expected.

Used instead of `diff -r` for three reasons: gzip members have to be compared decompressed —
the shell's `gzip -k -f` wrote the source mtime into the header, so every publish produced a
new blob even for an unchanged sitemap, and decompressing is what makes that churn invisible
here by construction — time-dependent fields have to be blanked when the two trees came from
separate builds, and the handful of intentional differences must be asserted individually
rather than filtered out of a text diff by eye.

Exit code 0 means the two trees agree everywhere except in the ways listed below.

Usage:
    compare.py OLD NEW VERSION
"""

from __future__ import annotations

import gzip
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Fields whose value is the time of the build. Only relevant to the end-to-end comparison,
# where the two trees are built separately; the stage-isolated run shares one build and these
# are already identical.
VOLATILE = (
    re.compile(rb"<lastmod>[^<]*</lastmod>"),
    re.compile(rb"<pubDate>[^<]*</pubDate>"),
    re.compile(rb"<lastBuildDate>[^<]*</lastBuildDate>"),
    re.compile(rb"<atom:updated>[^<]*</atom:updated>"),
    re.compile(rb'"date_published":"[^"]*"'),
    re.compile(rb'"date_modified":"[^"]*"'),
)


@dataclass
class Expected:
    """One intentional difference between the two implementations."""

    reason: str
    matches: object
    seen: list[str] = field(default_factory=list)


def expectations(version: str) -> list[Expected]:
    return [
        Expected(
            "the generated redirect pages replace the hand-written stub, and add two more "
            "redirects the shell had no way to express",
            lambda path: (
                path == f"{version}/index.html"
                or re.fullmatch(rf"{re.escape(version)}/docs(/getting-started)?/index\.html", path)
            ),
        ),
        Expected(
            "the build cache is not in a fresh worktree, so it can no longer be committed by "
            "accident",
            lambda path: path.startswith((".cache", "site/")),
        ),
        Expected(
            "the published version's sitemap is removed rather than pruned: nothing referenced it",
            lambda path: path in (f"{version}/sitemap.xml", f"{version}/sitemap.xml.gz"),
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

    def classify(path: str, problem: str) -> None:
        for rule in expected:
            if rule.matches(path):
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
            classify(path, f"content differs ({len(old_bytes)} vs {len(new_bytes)} bytes)")

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
