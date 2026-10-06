"""Preflight checks: dependencies, pins, git state and configuration. Read-only."""

from __future__ import annotations

import json
import re
import shutil
from collections.abc import Callable
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path

from .config import ConfigError, SiteConfig, load_site_config
from .discovery import known_versions, version_branches
from .expand import mirror_rule
from .gitrepo import Git, GitError
from .mikewrap import Mike
from .redirects import RedirectError, resolve_file_redirects
from .versions import parse

#: Every distribution that is a build input, pinned from the freeze of a known-good publish
#: run. Each is named in pyproject.toml, in the Dockerfiles (zensical as the base-image tag, the
#: rest in any pip install line) and in the lock compiled from pyproject.toml, so all the places
#: must agree. Zensical leaves the three packages that render the Markdown open, and a different
#: version of any of them builds different markup.
PINNED_DISTRIBUTIONS = (
    "zensical",
    "markdown",
    "pymdown-extensions",
    "pygments",
)

#: The Zensical fork of mike is installed from git, so its pin is a commit rather than a version:
#: `mike @ git+https://github.com/squidfunk/mike.git@<commit>` in pyproject.toml, the same URL in
#: Dockerfile.mike, and the commit pip recorded for the installed distribution. The lock leaves it
#: out: pip cannot hash a git checkout, so the publish workflow installs it separately.
MIKE_FORK = re.compile(r"squidfunk/mike(?:\.git)?@([0-9a-f]{7,40})")

#: Build inputs every past version branch carries as a verbatim copy of this checkout's, each with
#: the first version whose branch needs it. Empty since the move to Zensical: the past branches
#: still build with MkDocs and keep the hooks their own mkdocs.yml names, and nothing on main is
#: loaded by path from another branch any more.
BRANCH_FILES: tuple[tuple[str, str], ...] = ()

DOCKERFILES = ("Dockerfile", "Dockerfile.mike")
#: The hash-locked resolution of the `build` extra that the publish workflow installs from.
LOCKFILE = "publish-tool/requirements-publish.txt"
#: The tag may carry a digest (`0.0.68@sha256:…`); the version is the part before it.
DOCKER_TAG = re.compile(r"^FROM\s+zensical/zensical:([^@\s]+)", re.MULTILINE)


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    fatal: bool = True


def run_checks(
    *, repo: Git | None = None, repo_root: Path | None = None, pins_only: bool = False
) -> list[Check]:
    """Run the preflight checks and return them in reporting order."""
    checks: list[Check] = []

    if repo_root is None:
        # Every remaining check reads the checkout; without one there is nothing to certify.
        checks.append(
            Check(
                "repo", False, "not inside a git repository; run from the checkout or pass --repo"
            )
        )
        return checks

    checks += check_pins(repo_root)
    checks += check_mike_fork(repo_root)
    if pins_only:
        return checks

    checks += _check_dependencies()
    checks += _check_config(repo, repo_root=repo_root)
    if repo is not None:
        checks += _check_git(repo)
        checks += check_branch_files(repo, repo_root)
    return checks


def check_pins(
    repo_root: Path, *, installed_version: Callable[[str], str | None] | None = None
) -> list[Check]:
    """Assert that every place naming a pinned distribution names the same version.

    The pyproject pins, the Dockerfiles (base-image tag for zensical, pip install lines for
    anything else they name), the lock compiled from pyproject and the installed environment. A
    different theme or plugin version builds different markup — which the release-notes splice
    matches on — so drift is an error, not a warning. A lock that lags pyproject is the same
    drift one step later: the publish workflow installs from the lock, not from pyproject.
    """
    pyproject = repo_root / "publish-tool" / "pyproject.toml"
    pyproject_text = pyproject.read_text(encoding="utf-8") if pyproject.is_file() else ""
    lockfile = repo_root / LOCKFILE
    lock_text = lockfile.read_text(encoding="utf-8") if lockfile.is_file() else ""
    dockerfiles = {
        name: (repo_root / name).read_text(encoding="utf-8")
        for name in DOCKERFILES
        if (repo_root / name).is_file()
    }

    checks = []
    for distribution in PINNED_DISTRIBUTIONS:
        pin = re.compile(rf"\b{re.escape(distribution)}(?:\[[^\]]*\])?==([A-Za-z0-9._-]+)")
        found: dict[str, str] = {}

        declared = set(pin.findall(pyproject_text))
        if len(declared) > 1:
            checks.append(
                Check(
                    "pins",
                    False,
                    f"{distribution} is pinned to {len(declared)} different versions inside "
                    "publish-tool/pyproject.toml",
                )
            )
            continue
        if pyproject_text and not declared:
            # The pyproject pin is the source of truth; the other places agree *with it*.
            checks.append(
                Check("pins", False, f"{distribution} is not pinned in publish-tool/pyproject.toml")
            )
            continue
        if declared:
            found["publish-tool/pyproject.toml"] = declared.pop()

        for name, text in dockerfiles.items():
            match = DOCKER_TAG.search(text) if distribution == "zensical" else pin.search(text)
            if match:
                found[name] = match.group(1)

        if lock_text:
            match = pin.search(lock_text)
            if not match:
                checks.append(Check("pins", False, f"{distribution} is not in {LOCKFILE}"))
                continue
            found[LOCKFILE] = match.group(1)

        installed = (installed_version or _distribution_version)(distribution)
        if installed:
            found["installed"] = installed

        if not found:
            checks.append(Check("pins", False, f"no {distribution} version found anywhere"))
            continue
        unique = set(found.values())
        if len(unique) == 1:
            checks.append(Check("pins", True, f"{distribution} {unique.pop()} everywhere"))
            continue
        rendered = ", ".join(f"{where}={version}" for where, version in sorted(found.items()))
        checks.append(Check("pins", False, f"{distribution} versions disagree: {rendered}"))
    return checks


def check_mike_fork(
    repo_root: Path, *, installed_commit: Callable[[], str | None] | None = None
) -> list[Check]:
    """Every place naming the mike fork must name the same commit.

    pyproject.toml is the source of truth; Dockerfile.mike and the installed distribution agree
    with it. An environment without mike (the validation extra) is not compared.
    """
    pyproject = repo_root / "publish-tool" / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8") if pyproject.is_file() else ""
    declared = MIKE_FORK.search(text)
    if declared is None:
        return [
            Check(
                "pins",
                False,
                "mike is not pinned to a commit of the Zensical fork in "
                "publish-tool/pyproject.toml",
            )
        ]
    found = {"publish-tool/pyproject.toml": declared.group(1)}

    # Named only when the Dockerfile installs the fork directly; one that installs the `build`
    # extra takes the commit from pyproject and has nothing of its own to compare.
    dockerfile = repo_root / "Dockerfile.mike"
    if dockerfile.is_file():
        match = MIKE_FORK.search(dockerfile.read_text(encoding="utf-8"))
        if match:
            found["Dockerfile.mike"] = match.group(1)

    installed = (installed_commit or _installed_mike_commit)()
    if installed:
        found["installed"] = installed

    reference = found["publish-tool/pyproject.toml"]
    disagreeing = {
        where: commit
        for where, commit in found.items()
        if not (commit.startswith(reference) or reference.startswith(commit))
    }
    if disagreeing:
        rendered = ", ".join(f"{where}={commit}" for where, commit in sorted(found.items()))
        return [Check("pins", False, f"mike fork commits disagree: {rendered}")]
    return [Check("pins", True, f"mike fork at {reference[:12]} everywhere")]


def _installed_mike_commit() -> str | None:
    """The commit pip recorded for the installed mike, or None when it is not a git install."""
    try:
        recorded = metadata.distribution("mike").read_text("direct_url.json")
    except metadata.PackageNotFoundError:
        return None
    if not recorded:
        return None
    try:
        return json.loads(recorded).get("vcs_info", {}).get("commit_id")
    except (ValueError, AttributeError):
        return None


def check_branch_files(
    repo: Git, repo_root: Path, *, files: tuple[tuple[str, str], ...] = BRANCH_FILES
) -> list[Check]:
    """Every past version branch must hold the same copy of each file as this checkout.

    The newest version branch is skipped: `publish latest` builds it from `main` and rebases it
    onto `main`, so its copy is replaced on every publish. Every older branch is built from itself.
    """
    past = version_branches(repo)[1:]
    if not past:
        return [Check("branch-files", True, "no past version branches to compare", fatal=False)]

    checks = []
    for path, since in files:
        local = repo_root / path
        if not local.is_file():
            checks.append(Check("branch-files", False, f"{path} is missing from this checkout"))
            continue
        expected = repo.read("hash-object", str(local))

        same, differs, missing = [], [], []
        for version in past:
            if parse(version) < parse(since):
                continue
            blob = _branch_blob(repo, version, path)
            if blob is None:
                missing.append(version)
            elif blob == expected:
                same.append(version)
            else:
                differs.append(version)

        if differs or missing:
            problems = [f"differs on {', '.join(differs)}"] if differs else []
            problems += [f"missing on {', '.join(missing)}"] if missing else []
            checks.append(
                Check(
                    "branch-files",
                    False,
                    f"{path} {'; '.join(problems)} — copy this checkout's file onto each branch "
                    "(contributing/versioning.md, Branches)",
                )
            )
        elif same:
            checks.append(
                Check("branch-files", True, f"{path} matches this checkout on {', '.join(same)}")
            )
        else:
            checks.append(
                Check(
                    "branch-files",
                    True,
                    f"{path} is needed from {since}; no past branch that new to compare",
                    fatal=False,
                )
            )
    return checks


def _branch_blob(repo: Git, version: str, path: str) -> str | None:
    """The blob id of the file as the branch holds it: the remote-tracking ref when fetched, else
    the local one. Ids rather than text, so the comparison is byte for byte.
    """
    for ref in (f"{repo.remote}/{version}", version):
        try:
            return repo.read("rev-parse", "--verify", "--quiet", f"{ref}:{path}")
        except GitError:
            continue
    return None


def _distribution_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def _check_dependencies() -> list[Check]:
    missing_hint = 'not found — `pip install "./publish-tool[build]"`'
    mike_version = Mike.version()
    # The fork's version string carries its name (`2.2.0+zensical-0.1.0`); the original mike
    # would build with MkDocs, which is not installed any more.
    mike_ok = Mike.is_available() and "zensical" in (mike_version or "")
    return [
        Check(
            "mike",
            mike_ok,
            mike_version + (" — not the Zensical fork; " + missing_hint if not mike_ok else "")
            if mike_version
            else missing_hint,
        ),
        Check(
            "zensical",
            _distribution_version("zensical") is not None,
            _distribution_version("zensical") or missing_hint,
        ),
        Check(
            "git",
            shutil.which("git") is not None,
            shutil.which("git") or "not found",
        ),
    ]


def _check_config(repo: Git | None, *, repo_root: Path | None = None) -> list[Check]:
    try:
        config = load_site_config()
    except ConfigError as error:
        return [Check("config", False, str(error))]

    checks = [
        Check(
            "config",
            True,
            f"{config.source} — {len(config.file_rules)} file redirect(s), "
            f"{len(config.expand_rules)} expansion rule(s), "
            f"{_mirror_summary(config)}",
        )
    ]
    checks.append(_check_redirects_resolve(config, repo))
    site_url_check = _check_site_url_agreement(config, repo_root=repo_root)
    if site_url_check is not None:
        checks.append(site_url_check)
    return checks


def _check_site_url_agreement(config: SiteConfig, *, repo_root: Path | None = None) -> Check | None:
    """mkdocs.yml and ovweb.yaml both name the site URL; a drift breaks every rewrite.

    `mkdocs.yml` is looked up in the checkout, not next to the config file: the installed
    package ships its own copy of ovweb.yaml, so the config's location says nothing about
    where the site sources are.
    """
    if repo_root is not None:
        mkdocs_yml = repo_root / "mkdocs.yml"
    else:
        source = Path(config.source)
        if not source.is_file():  # config parsed from memory (tests)
            return None
        mkdocs_yml = source.resolve().parent.parent / "mkdocs.yml"
    if not mkdocs_yml.is_file():
        return Check("config", False, f"{mkdocs_yml} not found; cannot compare site_url")
    match = re.search(r"^site_url:\s*(\S+)", mkdocs_yml.read_text(encoding="utf-8"), re.MULTILINE)
    if match is None:
        return Check("config", False, "mkdocs.yml has no site_url")
    mkdocs_url = match.group(1).strip("\"'").rstrip("/")
    ovweb_url = config.layout.site_url.rstrip("/")
    if mkdocs_url != ovweb_url:
        return Check(
            "config",
            False,
            f"site_url disagrees: mkdocs.yml has {mkdocs_url}, {config.source} has {ovweb_url}",
        )
    return Check("config", True, f"site_url agrees across mkdocs.yml and ovweb.yaml ({ovweb_url})")


def _mirror_summary(config: SiteConfig) -> str:
    """Which sections the mirror covers.

    Not how many stubs it writes: that is only known at publish time, from the tree.
    """
    mirror = mirror_rule(config)
    if mirror is None:
        return "no unversioned mirror"
    sections = getattr(config.layout, mirror.for_each)
    return "unversioned mirror of " + ", ".join(f"/{section}/" for section in sections)


def _check_redirects_resolve(config: SiteConfig, repo: Git | None) -> Check:
    """Every version that could be published must resolve every rule unambiguously."""
    versions = known_versions(repo) if repo is not None else []
    if not versions:
        return Check("redirects", True, "no versions discovered to validate against", fatal=False)

    problems = []
    for version in versions:
        try:
            resolve_file_redirects(config, version)
        except RedirectError as error:
            problems.append(f"{version}: {error}")
    if problems:
        return Check("redirects", False, "; ".join(problems))
    return Check("redirects", True, f"resolve unambiguously for {', '.join(versions)}")


def _check_git(repo: Git) -> list[Check]:
    checks: list[Check] = []
    try:
        branch = repo.current_branch()
    except GitError as error:
        return [Check("git-branch", False, str(error))]
    checks.append(Check("git-branch", True, f"on '{branch}'", fatal=False))

    dirty = repo.status_porcelain()
    checks.append(
        Check(
            "git-clean",
            dirty == "",
            "clean"
            if dirty == ""
            else f"{len(dirty.splitlines())} uncommitted change(s) — mike builds from the "
            "working tree, so a publish would ship them",
        )
    )

    for name in ("main", "gh-pages"):
        exists = repo.remote_branch_exists(name)
        checks.append(
            Check(
                f"remote-{name}",
                exists,
                f"{repo.remote}/{name}" + ("" if exists else " missing"),
                fatal=name == "main",
            )
        )

    checks.append(_check_editable_install(repo))
    return checks


def _check_editable_install(repo: Git) -> Check:
    """Warn when ovweb is being imported from inside the repository it publishes.

    Publishing a past version checks out that version's branch, which does not contain this
    package, so an editable install or a PYTHONPATH checkout would disappear mid-run.
    """
    from . import __file__ as package_file

    location = Path(package_file).resolve().parent
    try:
        location.relative_to(repo.root.resolve())
    except ValueError:
        return Check("install", True, f"imported from outside the repository ({location})")
    return Check(
        "install",
        False,
        f"imported from inside the repository ({location}). Publishing a past version checks "
        "out that version's branch, where this package does not exist. Install it "
        'non-editable: `pip install "./publish-tool[build]"`.',
        fatal=False,
    )
