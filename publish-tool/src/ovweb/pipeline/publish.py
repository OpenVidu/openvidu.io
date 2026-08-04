"""Drive a full publish: prepare branches, build with mike, post-process, push.

**Nothing reaches the remote until the published tree is correct.** Every step up to and including
the gh-pages commit is local, the push happens once at the end, and a failure rolls the local
branch back to where it started — so there is nothing to restore from and no backup branch to
keep.
"""

from __future__ import annotations

from contextlib import contextmanager

from ..config import SiteConfig
from ..gitrepo import Git, GitError
from ..mikewrap import Mike
from ..model import PublishPlan
from ..report import Reporter
from .postprocess import postprocess

GH_BRANCH = "gh-pages"
LATEST_ALIAS = "latest"


class PublishError(Exception):
    """The publish cannot proceed."""


def publish(
    *,
    repo: Git,
    config: SiteConfig,
    plan: PublishPlan,
    report: Reporter,
    gh_branch: str = GH_BRANCH,
    keep_worktree: bool = False,
    commit: bool = True,
    force: bool = False,
) -> None:
    """Publish `plan.version`."""
    # Under --dry-run these are reported rather than raised: inspecting a plan is the moment when
    # the build toolchain may not be installed, or the tree may still be dirty.
    if repo.dry_run:
        if not Mike.is_available():
            report.warn("mike is not installed, so this plan could not actually be run.")
    else:
        Mike.require()
    _require_clean(repo, report=report)

    started_on = repo.current_branch()
    report.heading(
        f"Publishing {plan.version}"
        + (" and moving `latest` onto it" if plan.update_latest else " (root pages untouched)")
    )

    mike = Mike(repo.root, dry_run=repo.dry_run, log=report)

    try:
        created_branch = _prepare_branches(repo, plan=plan, gh_branch=gh_branch, report=report)

        # Everything from here to the gh-pages push is local and reversible.
        with _rollback_on_failure(repo, branch=gh_branch, report=report):
            if plan.delete_first:
                report.step("mike-delete", f"Remove the published {plan.version} before rebuilding")
                mike.delete(plan.version)

            report.step("mike-deploy", f"Build {plan.version} with mike")
            mike.deploy(plan.version, alias=LATEST_ALIAS if plan.update_latest else None)

            published = _post_process_gh_pages(
                repo,
                config=config,
                plan=plan,
                report=report,
                gh_branch=gh_branch,
                keep_worktree=keep_worktree,
                commit=commit,
                force=force,
            )

            if published and plan.push:
                report.step("push", f"Push {gh_branch}")
                repo.push(gh_branch)
            elif published:
                report.info(f"{gh_branch} committed locally; not pushed (--no-push).")

        # Past this point the site is published. What remains is branch bookkeeping: a
        # failure there is reported, but gh-pages is left alone.
        _finish_branches(repo, plan=plan, report=report, created_branch=created_branch)
    finally:
        if repo.current_branch() != started_on:
            repo.switch(started_on)

    if repo.dry_run:
        report.success(
            f"Dry run complete. Nothing was built, written or pushed for {plan.version}."
        )
    else:
        report.success(f"Published {plan.version}.")


@contextmanager
def _rollback_on_failure(repo: Git, *, branch: str, report: Reporter):
    """Restore `branch` to where it started if the body raises.

    mike commits locally and so does the pipeline, so a failure leaves the local branch carrying a
    half-finished publish; resetting it means a retry starts clean rather than stacking on top.

    `BaseException` rather than `Exception`, so a Ctrl-C mid-publish rolls back too.
    """
    if repo.dry_run:
        yield
        return

    before = repo.branch_sha(branch)
    try:
        yield
    except BaseException as error:
        report.warn(f"{type(error).__name__} during publish — rolling back '{branch}'.")
        try:
            # A worktree may still hold the branch if the failure escaped its cleanup.
            repo.prune_worktrees()
            if before is None:
                repo.delete_local_branch(branch)
                report.info(f"Deleted local '{branch}' (it did not exist before this run).")
            else:
                repo.set_branch(branch, before)
                report.info(f"Reset local '{branch}' to {before[:9]}.")
            report.info("Nothing was pushed, so the published site is unchanged.")
        except GitError as cleanup_error:
            report.error(
                f"could not roll back '{branch}': {cleanup_error}\n"
                f"Reset it by hand with: git update-ref refs/heads/{branch} "
                f"{before or '<previous sha>'}"
            )
        raise


def _require_clean(repo: Git, *, report: Reporter) -> None:
    """mike builds from the working tree, so uncommitted work would be published silently."""
    dirty = repo.status_porcelain()
    if not dirty:
        return
    message = (
        "the working tree has uncommitted changes. mike builds the site from the working "
        "tree, so publishing now would ship them:\n" + dirty
    )
    if repo.dry_run:
        report.warn(message)
        return
    raise PublishError(message)


def _prepare_branches(repo: Git, *, plan: PublishPlan, gh_branch: str, report: Reporter) -> bool:
    """Bring the local branches in line with the remote and check out the build source.

    Returns whether the version branch had to be created. Creating it is local only; pushing it
    happens after the site is published, so a failed publish leaves no new branch on the remote.
    """
    report.step("prepare-branches", "Synchronise the branches this publish reads")

    if repo.remote_branch_exists(gh_branch):
        _fast_forward_local(repo, gh_branch, report=report)
    else:
        report.info(f"'{gh_branch}' does not exist on {repo.remote} yet — first deployment.")

    version_branch = plan.version
    created = False
    if repo.remote_branch_exists(version_branch):
        _fast_forward_local(repo, version_branch, report=report)
    elif plan.create_branch:
        report.info(f"Creating branch '{version_branch}' from '{plan.source_branch}'.")
        _switch_to(repo, plan.source_branch)
        repo.create_branch(version_branch)
        created = True
    else:
        raise PublishError(
            f"branch '{version_branch}' does not exist on {repo.remote}. Updating a version "
            "requires its branch, because that branch — not main — is the source of truth for "
            "its content. Publish it as a new version first if that is what you meant."
        )

    # mike builds from the working tree, so the checked-out branch decides the content.
    _switch_to(repo, plan.source_branch)
    return created


def _finish_branches(
    repo: Git, *, plan: PublishPlan, report: Reporter, created_branch: bool
) -> None:
    """Push the version branch and, for a latest publish, rebase it onto the source.

    After the gh-pages push, because these steps only record *which source* produced the published
    site: a failure here leaves the site live and correct, so each one reports how to retry rather
    than aborting.
    """
    if created_branch and plan.push:
        report.step("push-version-branch", f"Push the new branch '{plan.version}'")
        try:
            repo.push(plan.version, set_upstream=True)
        except GitError as error:
            report.error(
                f"the site is published, but pushing branch '{plan.version}' failed: {error}\n"
                f"Retry with: git push --set-upstream {repo.remote} {plan.version}"
            )

    if plan.sync_branch:
        try:
            _sync_version_branch(repo, plan=plan, report=report)
        except GitError as error:
            report.error(
                f"the site is published, but syncing branch '{plan.version}' failed: {error}\n"
                f"Retry by rebasing '{plan.version}' onto '{plan.source_branch}' and pushing it."
            )


def _fast_forward_local(repo: Git, branch: str, *, report: Reporter) -> None:
    """Update the local branch from the remote without checking it out.

    A refspec fetch updates the ref in place, and fails rather than merging when the branches have
    diverged.
    """
    try:
        repo.do("fetch", repo.remote, f"{branch}:{branch}")
    except GitError as error:
        if repo.current_branch() == branch:
            repo.pull_ff_only(branch)
            return
        raise PublishError(
            f"cannot fast-forward local '{branch}' to {repo.remote}/{branch}:\n{error}\n"
            "The local branch has commits the remote does not. That usually means an earlier "
            "publish failed after committing but before pushing. Inspect it and reconcile by "
            "hand."
        ) from error
    report.detail(f"Local '{branch}' fast-forwarded to {repo.remote}/{branch}.")


def _switch_to(repo: Git, branch: str) -> None:
    if repo.current_branch() != branch:
        repo.switch(branch)


def _post_process_gh_pages(
    repo: Git,
    *,
    config: SiteConfig,
    plan: PublishPlan,
    report: Reporter,
    gh_branch: str,
    keep_worktree: bool,
    commit: bool,
    force: bool,
) -> bool:
    """Post-process and commit gh-pages in a throwaway worktree.

    Returns whether a commit was created and is therefore worth pushing.
    """
    if repo.dry_run:
        report.step("postprocess", f"Post-process {gh_branch} (skipped: --dry-run)")
        for step in plan.steps:
            report.info(f"{step.name}: {step.title}")
        return False

    with repo.worktree(gh_branch, keep=keep_worktree) as tree:
        report.detail(f"Worktree for '{gh_branch}' at {tree}")
        result = postprocess(
            tree,
            config=config,
            version=plan.version,
            update_latest=plan.update_latest,
            report=report,
            force=force,
        )

        for warning in result.warnings:
            report.warn(warning)

        if not commit:
            report.info("Left uncommitted (--no-commit).")
            report.info(f"Worktree: {tree}")
            return False

        report.step("commit", f"Commit {gh_branch}")
        repo.add_all(cwd=tree)
        suffix = "updated" if plan.update_latest else "untouched"
        created = repo.commit(
            f"Version {plan.version} updated. Non-versioned pages {suffix}", cwd=tree
        )
        if not created:
            report.info("Nothing changed on gh-pages; no commit created.")
        return created


def _sync_version_branch(repo: Git, *, plan: PublishPlan, report: Reporter) -> None:
    """Rebase the version branch onto main so it carries what was just published.

    Only meaningful when re-publishing the newest version, whose content comes from main. Done in a
    worktree so the main working tree never moves.
    """
    report.step("sync-branch", f"Rebase '{plan.version}' onto '{plan.source_branch}'")
    if repo.dry_run:
        report.info(f"Would rebase '{plan.version}' onto '{plan.source_branch}' and force-push.")
        return
    with repo.worktree(plan.version) as tree:
        repo.rebase(plan.source_branch, cwd=tree)
        if plan.push:
            repo.push_force_with_lease(plan.version, cwd=tree)
        else:
            report.info("Rebased locally; not pushed (--no-push).")
