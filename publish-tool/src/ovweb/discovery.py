"""Work out which versions exist, from the repository rather than from a hardcoded list."""

from __future__ import annotations

import re

from .gitrepo import Git, GitError
from .versions import MINOR_VERSION, read_versions_json, sort_descending

REMOTE_BRANCH = re.compile(r"^[0-9a-f]{40}\s+refs/heads/(.+)$", re.MULTILINE)


def published_versions(repo: Git, *, gh_branch: str = "gh-pages") -> list[str]:
    """Versions listed in versions.json on the published branch, newest first."""
    try:
        text = repo.show(gh_branch, "versions.json")
    except GitError:
        return []
    entries = read_versions_json(text)
    return sort_descending([entry.version for entry in entries])


def version_branches(repo: Git) -> list[str]:
    """Every `X.Y` branch, local or on the remote, newest first.

    A version branch can exist before the version is published (a new minor is branched
    first), so this is a superset of :func:`published_versions` and the right input for
    validating that the redirect rules cover everything.
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
