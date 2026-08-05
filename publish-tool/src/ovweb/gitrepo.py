"""A small, explicit facade over the git commands the publish needs.

Every mutating operation goes through here so `--dry-run` has exactly one place to stop at,
and so the argv of every call can be logged with `-vv`.
"""

from __future__ import annotations

import subprocess
from collections.abc import Sequence
from contextlib import contextmanager
from pathlib import Path
from tempfile import mkdtemp

from .sources import LOG_ARGS as LOG_DATES_ARGS


class GitError(Exception):
    """A git command failed, or the repository is not in a usable state."""


class Git:
    """Runs git in one repository."""

    def __init__(
        self,
        root: Path,
        *,
        remote: str = "origin",
        dry_run: bool = False,
        log: object = None,
    ) -> None:
        self.root = root
        self.remote = remote
        self.dry_run = dry_run
        self._log = log

    # -- plumbing ---------------------------------------------------------------------

    def _run(
        self,
        args: Sequence[str],
        *,
        cwd: Path | None = None,
        check: bool = True,
        mutating: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        command = ["git", *args]
        where = cwd or self.root
        if self._log is not None:
            self._log.command(command, cwd=where, skipped=mutating and self.dry_run)  # type: ignore[attr-defined]
        if mutating and self.dry_run:
            return subprocess.CompletedProcess(command, 0, "", "")
        result = subprocess.run(command, cwd=where, capture_output=True, text=True, check=False)
        if check and result.returncode != 0:
            raise GitError(
                f"`{' '.join(command)}` failed with exit code {result.returncode}:\n"
                f"{result.stderr.strip() or result.stdout.strip()}"
            )
        return result

    def read(self, *args: str, cwd: Path | None = None) -> str:
        return self._run(args, cwd=cwd).stdout.strip()

    def do(self, *args: str, cwd: Path | None = None) -> None:
        self._run(args, cwd=cwd, mutating=True)

    # -- queries ----------------------------------------------------------------------

    def toplevel(self) -> Path:
        return Path(self.read("rev-parse", "--show-toplevel"))

    def current_branch(self) -> str:
        return self.read("rev-parse", "--abbrev-ref", "HEAD")

    def is_shallow(self) -> bool:
        """Whether the clone has a truncated history.

        Asked before reading dates out of the log: in a shallow clone `git log` succeeds but
        reports the one fetched commit for every path, which is wrong rather than absent.
        """
        return self.read("rev-parse", "--is-shallow-repository") == "true"

    def log_dates_for(self, *paths: str) -> str:
        """Raw `git log` output pairing each commit's date with the paths it touched.

        One pass covers every file under `paths`. :func:`ovweb.sources.parse_git_log` owns the
        format and the walking.
        """
        return self.read(*LOG_DATES_ARGS, "HEAD", "--", *paths)

    def status_porcelain(self, cwd: Path | None = None) -> str:
        return self._run(("status", "--porcelain"), cwd=cwd).stdout.strip()

    def remote_branch_exists(self, branch: str) -> bool:
        """Whether `branch` exists on the remote.

        Matches the full ref, so branch `3.0` is not reported as existing on the strength of
        `refs/heads/3.0.0-beta1`.
        """
        result = self._run(
            ("ls-remote", "--exit-code", "--heads", self.remote, f"refs/heads/{branch}"),
            check=False,
        )
        return result.returncode == 0

    def local_branches(self) -> list[str]:
        return self.read("for-each-ref", "--format=%(refname:short)", "refs/heads").splitlines()

    def branch_sha(self, branch: str) -> str | None:
        """The commit a local branch points at, or `None` if it does not exist."""
        result = self._run(("rev-parse", "--verify", f"refs/heads/{branch}"), check=False)
        return result.stdout.strip() if result.returncode == 0 else None

    # -- moving a branch without checking it out ----------------------------------------

    def set_branch(self, branch: str, sha: str) -> None:
        """Point a local branch at `sha`, whether or not it is checked out anywhere."""
        self.do("update-ref", f"refs/heads/{branch}", sha)

    def delete_local_branch(self, branch: str) -> None:
        self.do("update-ref", "-d", f"refs/heads/{branch}")

    def prune_worktrees(self) -> None:
        self._run(("worktree", "prune"), check=False, mutating=True)

    # -- branch and remote operations --------------------------------------------------

    def switch(self, branch: str) -> None:
        self.do("switch", branch)

    def create_branch(self, branch: str) -> None:
        self.do("switch", "--create", branch)

    def pull_ff_only(self, branch: str, *, cwd: Path | None = None) -> None:
        """Fast-forward `branch` from the remote, refusing to create a merge commit.

        Raises :class:`GitError` when the branches have diverged, rather than merging a tree
        nobody has reviewed into the publish.
        """
        result = self._run(
            ("pull", "--ff-only", self.remote, branch), cwd=cwd, check=False, mutating=True
        )
        if result.returncode != 0:
            raise GitError(
                f"cannot fast-forward '{branch}' from {self.remote}:\n"
                f"{result.stderr.strip() or result.stdout.strip()}\n"
                "The local and remote branches have diverged. Reconcile them by hand before "
                "publishing — merging them automatically would publish a tree nobody has "
                "reviewed."
            )

    def push(self, branch: str, *, set_upstream: bool = False, cwd: Path | None = None) -> None:
        args = ["push"]
        if set_upstream:
            args.append("--set-upstream")
        args += [self.remote, branch]
        self.do(*args, cwd=cwd)

    def push_force_with_lease(self, branch: str, *, cwd: Path | None = None) -> None:
        """Force-push, refusing to discard commits the local repository has not seen.

        A bare `--force` would silently drop a fix somebody else pushed to the version branch.
        """
        self.do("push", "--force-with-lease", self.remote, branch, cwd=cwd)

    def rebase(self, onto: str, *, cwd: Path | None = None) -> None:
        self.do("rebase", onto, cwd=cwd)

    # -- worktrees ---------------------------------------------------------------------

    @contextmanager
    def worktree(self, branch: str, *, keep: bool = False):
        """Check `branch` out into a throwaway worktree outside the repository.

        The publish reaches gh-pages this way rather than checking it out in the main working
        tree, which would take the tool's own sources, config and templates out of scope (they
        exist on neither gh-pages nor a version branch), unignore `site/` and `.cache/` for
        `git add --all` (`.gitignore` is a main-only file), and strand the caller mid-move on a
        failure.
        """
        path = Path(mkdtemp(prefix=f"ovweb-{branch.replace('/', '-')}-"))
        # mkdtemp already created the directory and `git worktree add` wants to create it.
        path.rmdir()
        self.do("worktree", "add", str(path), branch)
        try:
            yield path
        finally:
            if keep:
                if self._log is not None:
                    self._log.info(f"Worktree kept at {path}")  # type: ignore[attr-defined]
            else:
                self._run(("worktree", "remove", "--force", str(path)), check=False, mutating=True)
                self._run(("worktree", "prune"), check=False, mutating=True)

    # -- the index ---------------------------------------------------------------------

    def add_all(self, *, cwd: Path) -> None:
        self.do("add", "--all", cwd=cwd)

    def commit(self, message: str, *, cwd: Path) -> bool:
        """Commit the staged tree. Returns whether a commit was created."""
        if self.dry_run:
            self.do("commit", "--message", message, cwd=cwd)
            return False
        if not self.status_porcelain(cwd=cwd):
            return False
        self.do("commit", "--message", message, cwd=cwd)
        return True

    def show(self, ref: str, path: str) -> str:
        return self.read("show", f"{ref}:{path}")


def open_repository(start: Path | None = None, **kwargs) -> Git:
    """Open the repository containing `start` (the current directory by default)."""
    probe = Git(start or Path.cwd(), **kwargs)
    try:
        root = probe.toplevel()
    except GitError as error:
        raise GitError(f"not inside a git repository: {start or Path.cwd()}") from error
    return Git(root, **kwargs)
