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

    def rev_parse(self, ref: str) -> str:
        return self.read("rev-parse", ref)

    def is_clean(self, cwd: Path | None = None) -> bool:
        return self._run(("status", "--porcelain"), cwd=cwd).stdout.strip() == ""

    def status_porcelain(self, cwd: Path | None = None) -> str:
        return self._run(("status", "--porcelain"), cwd=cwd).stdout.strip()

    def remote_branch_exists(self, branch: str) -> bool:
        """Whether `branch` exists on the remote.

        Matches the full ref. The shell implementation used
        `git ls-remote --heads origin 3.0 | grep -q 3.0`, whose substring match is satisfied
        by `refs/heads/3.0.0-beta1` — so it could report that branch `3.0` exists when it
        does not, and then fail (or worse, silently use a stale local branch).
        """
        result = self._run(
            ("ls-remote", "--exit-code", "--heads", self.remote, f"refs/heads/{branch}"),
            check=False,
        )
        return result.returncode == 0

    def local_branch_exists(self, branch: str) -> bool:
        return (
            self._run(
                ("show-ref", "--verify", "--quiet", f"refs/heads/{branch}"), check=False
            ).returncode
            == 0
        )

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

    def fetch(self, branch: str) -> None:
        self.do("fetch", self.remote, branch)

    def switch(self, branch: str) -> None:
        self.do("switch", branch)

    def create_branch(self, branch: str) -> None:
        self.do("switch", "--create", branch)

    def pull_ff_only(self, branch: str, *, cwd: Path | None = None) -> None:
        """Fast-forward `branch` from the remote, refusing to create a merge commit.

        The shell used a plain `git pull`, which would silently merge a diverged branch into
        the publish. Diverging here is a real problem and should stop the publish.
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
        """Force-push, but refuse to discard commits the local repo has not seen.

        The shell used a bare `git push --force`, which would silently drop a fix someone
        else had pushed to the version branch.
        """
        self.do("push", "--force-with-lease", self.remote, branch, cwd=cwd)

    def rebase(self, onto: str, *, cwd: Path | None = None) -> None:
        self.do("rebase", onto, cwd=cwd)

    # -- worktrees ---------------------------------------------------------------------

    @contextmanager
    def worktree(self, branch: str, *, keep: bool = False):
        """Check `branch` out into a throwaway worktree outside the repository.

        This is how the publish reaches gh-pages, rather than checking it out in the main
        working tree, for three reasons:

        * The tool's own files would vanish. Its sources, config and templates are not on
          gh-pages, and for a past version they are not on that version's branch either.
        * `.gitignore` is a main-only file, so `site/` and `.cache/` would become untracked
          *and* unignored, and `git add --all` would publish them.
        * A failure half-way would strand the caller on gh-pages mid-move. Here the main tree
          never leaves the branch it started on.

        Created after mike has finished, so it sees mike's commit.
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

    def restore_from(self, branch: str, path: str, *, cwd: Path | None = None) -> None:
        self.do("restore", "--source", branch, "--", path, cwd=cwd)

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
