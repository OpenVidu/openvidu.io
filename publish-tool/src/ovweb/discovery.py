"""Which versions exist — from the repository, or from a published tree on disk."""

from __future__ import annotations

import re
from pathlib import Path

from . import fsops
from .gitrepo import Git, GitError
from .versions import MINOR_VERSION, alias_target, read_versions_json, sort_descending

REMOTE_BRANCH = re.compile(r"^[0-9a-f]{40}\s+refs/heads/(.+)$", re.MULTILINE)

#: A version folder in a published tree. Legacy exact-patch folders (`3.0.0-beta1`) are not
#: matched: they are only ever read, never published or post-processed.
VERSION_FOLDER = re.compile(r"\d+\.\d+")

VERSIONS_JSON = "versions.json"
LATEST_ALIAS = "latest"


# -- from the repository ---------------------------------------------------------------------


def published_versions(repo: Git, *, gh_branch: str = "gh-pages") -> list[str]:
    """Versions listed in versions.json on the published branch, newest first."""
    try:
        text = repo.show(gh_branch, VERSIONS_JSON)
    except GitError:
        return []
    entries = read_versions_json(text)
    return sort_descending([entry.version for entry in entries])


def version_branches(repo: Git) -> list[str]:
    """Every `X.Y` branch, local or on the remote, newest first.

    A version branch can exist before the version is published — a new minor is branched
    first — so this is a superset of :func:`published_versions`.
    """
    names = {name for name in repo.local_branches() if MINOR_VERSION.match(name)}
    try:
        listing = repo.read("ls-remote", "--heads", repo.remote)
    except GitError:
        listing = ""
    names |= {
        match.group(1)
        for match in REMOTE_BRANCH.finditer(listing)
        if MINOR_VERSION.match(match.group(1))
    }
    return sort_descending(sorted(names))


def known_versions(repo: Git, *, gh_branch: str = "gh-pages") -> list[str]:
    """Everything a redirect rule might have to resolve for, newest first."""
    combined = set(published_versions(repo, gh_branch=gh_branch)) | set(version_branches(repo))
    return sort_descending(sorted(combined))


# -- from a published tree -------------------------------------------------------------------


def version_folders(tree: Path) -> list[str]:
    """Every `X.Y` folder in a published tree, in name order."""
    return sorted(
        entry.name
        for entry in tree.iterdir()
        if entry.is_dir() and VERSION_FOLDER.fullmatch(entry.name)
    )


def versions_in_tree(tree: Path) -> list[str]:
    """The versions a published tree serves, from versions.json, falling back to the folders."""
    path = tree / VERSIONS_JSON
    if not path.is_file():
        return version_folders(tree)
    return [entry.version for entry in read_versions_json(fsops.read_text(path))]


def latest_in_tree(tree: Path, *, alias: str = LATEST_ALIAS) -> str | None:
    """Which version `alias` points at in a published tree, or `None` if it cannot be resolved.

    mike materialises an alias as a symlink to the version folder, so the symlink is the
    authority; versions.json is the fallback for a tree where the alias is a real directory.
    """
    link = tree / alias
    if link.is_symlink():
        return Path(link.readlink()).name

    path = tree / VERSIONS_JSON
    if path.is_file():
        return alias_target(read_versions_json(fsops.read_text(path)), alias)
    return None
