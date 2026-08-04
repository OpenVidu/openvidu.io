"""Wrapper around the `mike` CLI.

`mike` builds the site with MkDocs from the current working tree and commits the result into
the gh-pages branch using git plumbing — it never checks that branch out. That is what lets
the post-processing run in a separate worktree afterwards.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path

from .config import CONFIG_ENV_VAR


class MikeError(Exception):
    """A mike command failed, or mike is not installed."""


class Mike:
    def __init__(
        self,
        root: Path,
        *,
        config_path: Path | None = None,
        dry_run: bool = False,
        log: object = None,
    ) -> None:
        self.root = root
        self.config_path = config_path
        self.dry_run = dry_run
        self._log = log

    @staticmethod
    def is_available() -> bool:
        return shutil.which("mike") is not None

    @staticmethod
    def require() -> None:
        if not Mike.is_available():
            raise MikeError(
                "mike not found. Install the publishing dependencies with "
                '`pip install "./publish-tool[build]"`.'
            )

    def _environment(self) -> dict[str, str]:
        """The environment mike, and therefore MkDocs, builds under.

        `OVWEB_SITE_CONFIG` is pinned to an absolute path so the MkDocs hook reads the config this
        run is using, rather than whatever ovweb.yaml is in the checked-out tree — which for a
        past-version publish is that branch's stale copy.
        """
        environment = dict(os.environ)
        if self.config_path is not None:
            environment[CONFIG_ENV_VAR] = str(self.config_path.resolve())
        return environment

    def _run(self, args: Sequence[str]) -> None:
        command = ["mike", *args]
        if self._log is not None:
            self._log.command(command, cwd=self.root, skipped=self.dry_run)  # type: ignore[attr-defined]
        if self.dry_run:
            return
        result = subprocess.run(command, cwd=self.root, env=self._environment(), check=False)
        if result.returncode != 0:
            raise MikeError(f"`{' '.join(command)}` failed with exit code {result.returncode}")

    # Neither command below ever passes `--push`. mike's output is only half a publish — the
    # version folder still holds the pages that belong at the site root, their links resolve
    # nowhere, and there is no redirect at the version root — so pushing it would put that on the
    # live site. `pipeline/publish.py` pushes once the tree is correct, which also keeps rolling
    # back a failure a purely local operation.

    def deploy(self, version: str, *, alias: str | None = None) -> None:
        """Build `version` and commit it to the local gh-pages, optionally moving an alias."""
        args = ["deploy"]
        if alias:
            args.append("--update-aliases")
        args.append(version)
        if alias:
            args.append(alias)
        self._run(args)

    def delete(self, version: str) -> bool:
        """Remove `version` from the local gh-pages. Returns whether it was there.

        A missing version is tolerated: the first publish of a version under a new name has
        nothing to delete yet.
        """
        try:
            self._run(["delete", version])
            return True
        except MikeError:
            if self._log is not None:
                self._log.info(  # type: ignore[attr-defined]
                    f"Version {version} is not published yet; nothing to delete."
                )
            return False

    @staticmethod
    def version() -> str | None:
        if not Mike.is_available():
            return None
        result = subprocess.run(["mike", "--version"], capture_output=True, text=True, check=False)
        return result.stdout.strip() or result.stderr.strip() or None
