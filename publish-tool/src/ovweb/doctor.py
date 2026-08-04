"""Preflight checks: dependencies, pins, git state and configuration. Read-only."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path

from .config import ConfigError, SiteConfig, load_site_config
from .discovery import known_versions
from .gitrepo import Git, GitError
from .mikewrap import Mike
from .redirects import RedirectError, resolve_file_redirects, resolve_patterns

#: The distribution whose version must agree everywhere: the only pinned dependency that is also
#: named outside Python packaging, as a Docker base-image tag.
PINNED_DISTRIBUTION = "mkdocs-material"

DOCKERFILES = ("Dockerfile", "Dockerfile.mike")
DOCKER_TAG = re.compile(r"^FROM\s+squidfunk/mkdocs-material:(\S+)", re.MULTILINE)
PYPROJECT_PIN = re.compile(r"mkdocs-material(?:\[[^\]]*\])?==([^\"'\s]+)")


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

    if repo_root is not None:
        checks += check_pins(repo_root)
    if pins_only:
        return checks

    checks += _check_dependencies()
    checks += _check_config(repo)
    if repo is not None:
        checks += _check_git(repo)
    return checks


def check_pins(repo_root: Path) -> list[Check]:
    """Assert that every place naming a mkdocs-material version names the same one.

    The declared pin, the two Docker base-image tags and the installed distribution. A different
    theme version builds different markup, and the release-notes splice matches on that markup.
    """
    found: dict[str, str] = {}

    pyproject = repo_root / "publish-tool" / "pyproject.toml"
    if pyproject.is_file():
        match = PYPROJECT_PIN.search(pyproject.read_text(encoding="utf-8"))
        if match:
            found["publish-tool/pyproject.toml"] = match.group(1)

    for name in DOCKERFILES:
        path = repo_root / name
        if not path.is_file():
            continue
        match = DOCKER_TAG.search(path.read_text(encoding="utf-8"))
        if match:
            found[name] = match.group(1)

    installed = _distribution_version(PINNED_DISTRIBUTION)
    if installed:
        found["installed"] = installed

    if not found:
        return [Check("pins", False, f"no {PINNED_DISTRIBUTION} version found anywhere")]

    unique = set(found.values())
    if len(unique) == 1:
        return [Check("pins", True, f"{PINNED_DISTRIBUTION} {unique.pop()} everywhere")]

    rendered = ", ".join(f"{where}={version}" for where, version in sorted(found.items()))
    return [Check("pins", False, f"{PINNED_DISTRIBUTION} versions disagree: {rendered}")]


def _distribution_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


def _check_dependencies() -> list[Check]:
    missing_hint = 'not found — `pip install "./publish-tool[build]"`'
    return [
        Check("mike", Mike.is_available(), Mike.version() or missing_hint),
        Check(
            "mkdocs",
            _distribution_version("mkdocs") is not None,
            _distribution_version("mkdocs") or missing_hint,
        ),
        Check(
            "git",
            shutil.which("git") is not None,
            shutil.which("git") or "not found",
        ),
    ]


def _check_config(repo: Git | None) -> list[Check]:
    try:
        config = load_site_config()
    except ConfigError as error:
        return [Check("config", False, str(error))]

    checks = [
        Check(
            "config",
            True,
            f"{config.source} — {len(config.file_rules)} file redirect(s), "
            f"{len(resolve_patterns(config))} 404 pattern(s), "
            f"{_mirror_summary(config)}",
        )
    ]
    checks.append(_check_redirects_resolve(config, repo))
    return checks


def _mirror_summary(config: SiteConfig) -> str:
    """Which sections the mirror covers.

    Not how many stubs it writes: that is only known at publish time, from the sitemap.
    """
    mirror = config.mirror
    if mirror is None or not mirror.enabled:
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
