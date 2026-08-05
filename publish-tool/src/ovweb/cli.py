"""The `ovweb` command line.

Thin by design: parse flags, build a plan, hand off. Anything that decides something belongs in
:mod:`ovweb.plan`, :mod:`ovweb.redirects` or :mod:`ovweb.pipeline`.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import typer

from . import __version__, fsops
from .config import ConfigError, SiteConfig, load_site_config
from .discovery import (
    known_versions,
    latest_in_tree,
    published_versions,
    version_branches,
    version_folders,
)
from .doctor import run_checks
from .expand import (
    alias_redirects,
    expand_candidate_paths,
    mirror_redirects,
    mirror_rule,
    scan_tree,
    version_redirects,
    wipe_owned,
)
from .gitrepo import Git, GitError, open_repository
from .lint import ERROR, WARN, run_lint
from .mikewrap import MikeError
from .model import (
    CrossProductRule,
    SectionFallbackRule,
    TreeRenameRule,
    UnversionedMirrorRule,
    VersionAliasRule,
)
from .pipeline.postprocess import PostprocessError, postprocess
from .pipeline.publish import PublishError, publish
from .plan import build_plan
from .redirects import RedirectError, render_redirect, resolve_file_redirects
from .releases import RegionError
from .report import Reporter
from .rewrite import RewriteError, sync_version_sitemap
from .verify import verify
from .versions import VersionError, validate_minor

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="Build, version and publish the openvidu.io website.",
)
publish_app = typer.Typer(no_args_is_help=True, help="Publish a documentation version.")
redirects_app = typer.Typer(no_args_is_help=True, help="Inspect the redirect configuration.")
versions_app = typer.Typer(no_args_is_help=True, help="Inspect the published versions.")
app.add_typer(publish_app, name="publish")
app.add_typer(redirects_app, name="redirects")
app.add_typer(versions_app, name="versions")

# Errors that are the user's problem, not a bug: report the message, not a traceback.
EXPECTED_ERRORS = (
    ConfigError,
    GitError,
    MikeError,
    PostprocessError,
    PublishError,
    RedirectError,
    RegionError,
    RewriteError,
    VersionError,
)

VersionArgument = Annotated[str, typer.Argument(help="Minor version to publish, e.g. 3.9.")]


# -- shared option handling -----------------------------------------------------------------


class Context:
    """Everything the commands share, resolved once."""

    def __init__(
        self,
        *,
        repo_path: Path | None,
        layout: Path | None,
        remote: str,
        dry_run: bool,
        verbosity: int,
        as_json: bool,
        color: bool,
    ) -> None:
        self.report = Reporter(verbosity=verbosity, as_json=as_json, color=color)
        self.dry_run = dry_run
        self._layout = layout
        self._config: SiteConfig | None = None
        self._repo: Git | None = None
        self._repo_path = repo_path
        self._remote = remote

    @property
    def config(self) -> SiteConfig:
        if self._config is None:
            self._config = load_site_config(self._layout)
        return self._config

    @property
    def repo(self) -> Git:
        if self._repo is None:
            self._repo = open_repository(
                self._repo_path, remote=self._remote, dry_run=self.dry_run, log=self.report
            )
        return self._repo


@app.callback(invoke_without_command=True)
def main_callback(
    context: typer.Context,
    repo: Annotated[
        Path | None, typer.Option(help="Repository to work on. Defaults to the current one.")
    ] = None,
    layout: Annotated[
        Path | None, typer.Option(help="Use this ovweb.yaml instead of the installed one.")
    ] = None,
    remote: Annotated[str, typer.Option(help="Git remote to publish to.")] = "origin",
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Resolve and print the plan without building, writing or pushing anything.",
        ),
    ] = False,
    verbose: Annotated[
        int,
        typer.Option("--verbose", "-v", count=True, help="Repeat for the argv of every command."),
    ] = 0,
    as_json: Annotated[
        bool, typer.Option("--json", help="Emit one JSON object per step instead of prose.")
    ] = False,
    color: Annotated[bool, typer.Option("--color/--no-color", help="Colourise the output.")] = True,
    show_version: Annotated[
        bool, typer.Option("--version", help="Print the ovweb version and exit.")
    ] = False,
) -> None:
    if show_version:
        typer.echo(__version__)
        raise typer.Exit
    context.obj = Context(
        repo_path=repo,
        layout=layout,
        remote=remote,
        dry_run=dry_run,
        verbosity=verbose,
        as_json=as_json,
        color=color,
    )
    # The group is invokable without a subcommand so `--version` works on its own. A bare `ovweb`
    # is handled by no_args_is_help, so this only catches options given with no command.
    if context.invoked_subcommand is None:
        typer.echo(context.get_help())
        raise typer.Exit


# -- publish ---------------------------------------------------------------------------------


def _run_publish(
    context: Context,
    *,
    version: str,
    update_latest: bool,
    delete_first: bool,
    create_branch: bool,
    sync_branch: bool,
    push: bool,
    keep_worktree: bool,
    commit: bool,
    force: bool,
) -> None:
    validate_minor(version)
    plan = build_plan(
        context.config,
        version=version,
        update_latest=update_latest,
        delete_first=delete_first,
        create_branch=create_branch,
        sync_branch=sync_branch,
        push=push,
    )
    if context.dry_run:
        _print_plan(context, plan)
    publish(
        repo=context.repo,
        config=context.config,
        plan=plan,
        report=context.report,
        keep_worktree=keep_worktree,
        commit=commit,
        force=force,
    )


def _print_plan(context: Context, plan) -> None:
    report = context.report
    report.heading(f"Plan for {plan.version}")
    report.info(f"build source branch: {plan.source_branch}")
    report.info(f"move `latest`:       {'yes' if plan.update_latest else 'no'}")
    report.info(f"delete first:        {'yes' if plan.delete_first else 'no'}")
    report.info(f"create branch:       {'yes' if plan.create_branch else 'no'}")
    report.info(f"rebase branch:       {'yes' if plan.sync_branch else 'no'}")
    report.info(f"push:                {'yes' if plan.push else 'no'}")

    report.heading("Post-processing steps")
    for step in plan.steps:
        report.info(f"{step.name:24} {step.title}")
        if step.detail:
            report.detail(f"{'':24} {step.detail}")

    report.heading("Redirects to install")
    if not plan.redirects:
        report.info("(none)")
    for redirect in plan.redirects:
        report.info(f"{redirect.path}  ->  {redirect.to}   [{redirect.rule_id}]")

    report.heading("Notes")
    for note in plan.notes:
        report.info(f"- {note}")


_KEEP = typer.Option("--keep-worktree", help="Leave the gh-pages worktree behind for inspection.")
_NO_PUSH = typer.Option("--push/--no-push", help="Push to the remote, or keep everything local.")
_FORCE = typer.Option("--force", help="Post-process a tree that has already been post-processed.")


@publish_app.command("new")
def publish_new(
    context: typer.Context,
    version: VersionArgument,
    push: Annotated[bool, _NO_PUSH] = True,
    keep_worktree: Annotated[bool, _KEEP] = False,
    force: Annotated[bool, _FORCE] = False,
) -> None:
    """Publish a brand-new minor version and move `latest` onto it.

    Creates the `X.Y` branch from main so the version can be fixed later, refreshes the pages
    served from the site root, and copies the new release notes into every other version.
    """
    _run_publish(
        context.obj,
        version=version,
        update_latest=True,
        delete_first=False,
        create_branch=True,
        sync_branch=False,
        push=push,
        keep_worktree=keep_worktree,
        commit=True,
        force=force,
    )


@publish_app.command("latest")
def publish_latest(
    context: typer.Context,
    version: VersionArgument,
    push: Annotated[bool, _NO_PUSH] = True,
    keep_worktree: Annotated[bool, _KEEP] = False,
    force: Annotated[bool, _FORCE] = False,
) -> None:
    """Re-publish the newest version in place, from main.

    This is how a content fix and a patch release of the current minor go live. The version is
    removed and rebuilt, the root pages are refreshed, and the `X.Y` branch is rebased onto
    main so it keeps carrying what is published.
    """
    _run_publish(
        context.obj,
        version=version,
        update_latest=True,
        delete_first=True,
        create_branch=False,
        sync_branch=True,
        push=push,
        keep_worktree=keep_worktree,
        commit=True,
        force=force,
    )


@publish_app.command("past")
def publish_past(
    context: typer.Context,
    version: VersionArgument,
    push: Annotated[bool, _NO_PUSH] = True,
    keep_worktree: Annotated[bool, _KEEP] = False,
    force: Annotated[bool, _FORCE] = False,
) -> None:
    """Re-publish an older minor version, leaving the site root untouched.

    The content comes from the `X.Y` branch, which must already hold the changes. `latest` does
    not move, and the version's releases pages are refreshed from the current newest ones.
    """
    _run_publish(
        context.obj,
        version=version,
        update_latest=False,
        delete_first=True,
        create_branch=False,
        sync_branch=False,
        push=push,
        keep_worktree=keep_worktree,
        commit=True,
        force=force,
    )


@app.command()
def deploy(
    context: typer.Context,
    version: VersionArgument,
    update_latest: Annotated[
        bool, typer.Option("--update-latest/--no-update-latest", help="Move `latest` onto it.")
    ] = True,
    delete_first: Annotated[
        bool,
        typer.Option("--delete-first/--no-delete-first", help="`mike delete` before building."),
    ] = False,
    create_branch: Annotated[
        bool, typer.Option("--create-branch/--require-branch", help="Create the X.Y branch.")
    ] = False,
    sync_branch: Annotated[
        bool, typer.Option("--sync-branch/--no-sync-branch", help="Rebase X.Y onto main after.")
    ] = False,
    push: Annotated[bool, _NO_PUSH] = True,
    keep_worktree: Annotated[bool, _KEEP] = False,
    commit: Annotated[
        bool, typer.Option("--commit/--no-commit", help="Commit the post-processed gh-pages tree.")
    ] = True,
    force: Annotated[bool, _FORCE] = False,
) -> None:
    """The primitive the three `publish` presets configure. Use those unless you need this."""
    _run_publish(
        context.obj,
        version=version,
        update_latest=update_latest,
        delete_first=delete_first,
        create_branch=create_branch,
        sync_branch=sync_branch,
        push=push,
        keep_worktree=keep_worktree,
        commit=commit,
        force=force,
    )


# -- postprocess -----------------------------------------------------------------------------


@app.command("postprocess")
def postprocess_command(
    context: typer.Context,
    version: VersionArgument,
    tree: Annotated[Path, typer.Option("--tree", help="Directory holding a built gh-pages tree.")],
    update_latest: Annotated[
        bool, typer.Option("--update-latest/--no-update-latest", help="Refresh the root pages.")
    ] = True,
    force: Annotated[bool, _FORCE] = False,
) -> None:
    """Run only the gh-pages post-processing, on a tree, touching no git and no remote."""
    ctx: Context = context.obj
    validate_minor(version)
    result = postprocess(
        tree.resolve(),
        config=ctx.config,
        version=version,
        update_latest=update_latest,
        report=ctx.report,
        force=force,
    )
    ctx.report.success(
        f"Post-processed {version} in {tree}"
        + (f" with {len(result.warnings)} warning(s)" if result.warnings else "")
    )


# -- redirects -------------------------------------------------------------------------------


@redirects_app.command("render")
def redirects_render(
    context: typer.Context,
    version: VersionArgument,
    rule: Annotated[str | None, typer.Option("--rule", help="Render only this rule id.")] = None,
) -> None:
    """Print the `files` redirect pages that would be installed for a version.

    The `expand` rules resolve against a published tree, so they cannot be rendered from the
    configuration alone; `redirects apply --tree <copy> --dry-run` shows their outcome.
    """
    ctx: Context = context.obj
    resolved = resolve_file_redirects(ctx.config, version)
    if rule is not None:
        resolved = tuple(item for item in resolved if item.rule_id == rule)
        if not resolved:
            raise typer.BadParameter(f"no rule {rule!r} applies to version {version}")
    if not resolved:
        ctx.report.info(f"No redirect rule applies to version {version}.")
        return
    for redirect in resolved:
        typer.echo(f"===== {redirect.path}   [{redirect.rule_id}]")
        typer.echo(render_redirect(redirect), nl=False)


def _expand_summary(rule) -> str:
    if isinstance(rule, CrossProductRule):
        combos = 1
        for _, options in rule.values:
            combos *= len(options)
        gate = f", versions {rule.versions}" if rule.versions else ""
        return f"cross-product: {combos} candidate(s) per version{gate}"
    if isinstance(rule, TreeRenameRule):
        gate = f", versions {rule.versions}" if rule.versions else ""
        return f"tree-rename: {rule.from_path} -> {rule.to_path}{gate}"
    if isinstance(rule, SectionFallbackRule):
        return f"section-fallback: {rule.dir} -> {rule.to}, versions {rule.versions}"
    if isinstance(rule, VersionAliasRule):
        return f"version-alias: {len(rule.folders)} folder(s)"
    if isinstance(rule, UnversionedMirrorRule):
        return f"unversioned-mirror of {rule.for_each}"
    return "?"


@redirects_app.command("check")
def redirects_check(context: typer.Context) -> None:
    """Validate every redirect rule against every version that exists.

    Fails when a rule is ambiguous for some version, when a target is absolute where it must
    be relative, when a canonical URL is not absolute, or when a `files` rule and an expansion
    could claim the same path.
    """
    ctx: Context = context.obj
    config = ctx.config
    try:
        versions = known_versions(ctx.repo)
    except GitError:
        versions = []

    ctx.report.heading(f"Checking {config.source}")
    if not versions:
        ctx.report.warn("no versions discovered — checking the rules in isolation only")

    problems = 0
    for version in versions:
        try:
            resolved = resolve_file_redirects(config, version)
        except RedirectError as error:
            ctx.report.error(f"{version}: {error}")
            problems += 1
            continue
        rendered = [f"{item.rule_id} -> {item.to}" for item in resolved]
        ctx.report.info(f"{version:8} {', '.join(rendered) if rendered else '(no redirects)'}")

        candidates = expand_candidate_paths(config, version)
        for redirect in resolved:
            claimed = candidates.get(redirect.path)
            if claimed:
                ctx.report.error(
                    f"{version}: {redirect.path} is claimed by both {redirect.rule_id!r} "
                    f"and {claimed!r}"
                )
                problems += 1

    ctx.report.heading("Expansion rules")
    if not config.expand_rules:
        ctx.report.info("(none)")
    for rule in config.expand_rules:
        ctx.report.info(f"{rule.id:38} {_expand_summary(rule)}")

    if problems:
        ctx.report.error(f"{problems} version(s) failed to resolve.")
        raise typer.Exit(1)
    ctx.report.success("All redirect rules resolve.")


@redirects_app.command("apply")
def redirects_apply(
    context: typer.Context,
    tree: Annotated[Path, typer.Option("--tree", help="Directory holding a gh-pages tree.")],
    only: Annotated[
        str | None, typer.Option("--version", help="Apply to this version only.")
    ] = None,
) -> None:
    """Reconcile every generated redirect in a tree with the configuration.

    Writes the `files` and expansion stubs of every version folder, deleting generated stubs no
    rule produces any more; lists the stubs in each version's sitemap for the version selector;
    rebuilds the unversioned mirror and the legacy patch-version folders. This is how a rule
    reaches versions that are not being rebuilt, and how the alias folders come to exist at
    all — no publish creates them from nothing.

    With the global `--dry-run`, reports what would change and writes nothing.
    """
    ctx: Context = context.obj
    root = tree.resolve()
    dry = ctx.dry_run
    versions = [only] if only else version_folders(root)
    written = removed = 0

    for version in versions:
        redirects = version_redirects(root, ctx.config, version)
        resolved_paths = {redirect.path for redirect in redirects}
        # Reconcile: a generated stub in the folder that no rule produces any more is stale.
        index = scan_tree(root, (version,))
        for stale in sorted(set(index.stub_targets) - resolved_paths):
            ctx.report.info(f"delete {stale} (no rule generates it)")
            if not dry:
                fsops.remove(root / stale)
            removed += 1
        for redirect in redirects:
            ctx.report.detail(f"{redirect.path}  ->  {redirect.to}   [{redirect.rule_id}]")
            if not dry:
                fsops.write_text(root / redirect.path, render_redirect(redirect))
            written += 1
        # The version selector resolves a moved page by looking its URL up in this file, so
        # the stubs just reconciled have to be listed there.
        sitemap = root / version / "sitemap.xml"
        if sitemap.is_file():
            text = fsops.read_text(sitemap)
            synced = sync_version_sitemap(
                text, base_url=ctx.config.layout.base_url, stubs=resolved_paths
            )
            if synced != text:
                ctx.report.info(f"sync {version}/sitemap.xml ({len(resolved_paths)} stub entries)")
                if not dry:
                    fsops.write_text(sitemap, synced)
                    fsops.write_gzip(sitemap)

    latest = latest_in_tree(root)
    if mirror_rule(ctx.config) is not None and latest is not None and (only in (None, latest)):
        redirects = mirror_redirects(root, ctx.config, latest=latest)
        if not dry:
            for section in getattr(ctx.config.layout, mirror_rule(ctx.config).for_each):
                removed += int(wipe_owned(root / section))
            for redirect in redirects:
                fsops.write_text(root / redirect.path, render_redirect(redirect))
        written += len(redirects)
        ctx.report.info(f"mirror: {len(redirects)} page(s) of {latest} answer unversioned")

    minors = {only} if only else None
    for folder, redirects in alias_redirects(root, ctx.config, minors=minors):
        if not dry:
            wipe_owned(root / folder)
            for redirect in redirects:
                fsops.write_text(root / redirect.path, render_redirect(redirect))
        written += len(redirects)
        ctx.report.info(f"alias: {folder}/ mirrors {len(redirects)} page(s)")

    outcome = "Would write" if dry else "Wrote"
    ctx.report.success(
        f"{outcome} {written} redirect page(s) across {len(versions)} version(s), "
        f"removing {removed} stale one(s)."
    )


# -- versions --------------------------------------------------------------------------------


@versions_app.command("list")
def versions_list(context: typer.Context) -> None:
    """Show what is published and which version branches exist."""
    ctx: Context = context.obj
    repo = ctx.repo
    published = published_versions(repo)
    branches = version_branches(repo)

    ctx.report.heading("Published (versions.json on gh-pages)")
    ctx.report.info(", ".join(published) if published else "(none)")
    ctx.report.heading("Version branches")
    ctx.report.info(", ".join(branches) if branches else "(none)")

    orphans = sorted(set(published) - set(branches))
    if orphans:
        ctx.report.warn(
            f"published without a branch: {', '.join(orphans)} — they cannot be re-published"
        )


# -- verify ----------------------------------------------------------------------------------


@app.command("verify")
def verify_command(
    context: typer.Context,
    tree: Annotated[
        Path | None,
        typer.Option("--tree", help="Directory holding a gh-pages tree. Defaults to a worktree."),
    ] = None,
    gh_branch: Annotated[
        str, typer.Option(help="Branch to check out when --tree is absent.")
    ] = "gh-pages",
) -> None:
    """Assert the invariants of a published tree."""
    ctx: Context = context.obj
    if tree is not None:
        findings = verify(tree.resolve(), config=ctx.config)
    else:
        with ctx.repo.worktree(gh_branch) as worktree:
            findings = verify(worktree, config=ctx.config)

    if not findings:
        ctx.report.success("All invariants hold.")
        return
    for finding in findings:
        ctx.report.error(f"[{finding.check}] {finding.where}: {finding.detail}")
    ctx.report.error(f"{len(findings)} invariant violation(s).")
    raise typer.Exit(1)


# -- lint ------------------------------------------------------------------------------------


@app.command("lint")
def lint_command(
    context: typer.Context,
    paths: Annotated[
        list[Path] | None,
        typer.Argument(help="Report only findings in these files (repo-relative)."),
    ] = None,
) -> None:
    """Check the authoring conventions `mkdocs build --strict` cannot see.

    Covers raw-HTML links and images, link form in the files that move at publish,
    version-pin discipline, SEO field lengths and uniqueness, admonition syntax, the
    functional `tags:` contract, and asset placement — over the source tree, in seconds,
    with no build.

    Exit codes: 0 clean, 1 error-severity findings, 2 tool failure.
    """
    ctx: Context = context.obj
    root = ctx.repo.root
    only = [path.as_posix() for path in paths] if paths else None
    findings = run_lint(root, layout=ctx.config.layout, paths=only)

    emit = {ERROR: ctx.report.error, WARN: ctx.report.warn}
    counts = {ERROR: 0, WARN: 0, "info": 0}
    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1
        suffix = f" — {finding.hint}" if finding.hint else ""
        emit.get(finding.severity, ctx.report.info)(
            f"[{finding.check}] {finding.file}:{finding.line}: {finding.message}{suffix}"
        )

    if counts[ERROR]:
        ctx.report.error(
            f"{counts[ERROR]} error(s), {counts[WARN]} warning(s), {counts['info']} info."
        )
        raise typer.Exit(1)
    ctx.report.success(
        f"No errors ({counts[WARN]} warning(s), {counts['info']} info) across "
        f"{len(findings)} finding(s)."
    )


# -- doctor ----------------------------------------------------------------------------------


@app.command()
def doctor(
    context: typer.Context,
    pins: Annotated[
        bool, typer.Option("--pins", help="Only check that the pinned versions agree.")
    ] = False,
) -> None:
    """Check dependencies, pins, configuration and git state before publishing."""
    ctx: Context = context.obj
    try:
        repo = ctx.repo
        repo_root = repo.root
    except GitError:
        repo = None
        repo_root = None

    checks = run_checks(repo=repo, repo_root=repo_root, pins_only=pins)
    failed = 0
    for check in checks:
        if check.ok:
            ctx.report.info(f"ok      {check.name:16} {check.detail}")
        elif check.fatal:
            ctx.report.error(f"{check.name}: {check.detail}")
            failed += 1
        else:
            ctx.report.warn(f"{check.name}: {check.detail}")

    if failed:
        raise typer.Exit(1)
    ctx.report.success("Ready to publish.")


# -- entry point -----------------------------------------------------------------------------

#: Options declared on the app callback rather than on a command. click only accepts a group's
#: options *before* the subcommand, so `ovweb publish latest 3.8 --verbose` is a parse error;
#: :func:`hoist_global_options` moves them to the front instead of failing.
#:
#: `tests/unit/test_cli.py` asserts these two sets stay in step with the app, and that no command
#: ever declares a name listed here — which is what makes the rewriting safe.
GLOBAL_SWITCHES = frozenset({"--dry-run", "--json", "--color", "--no-color", "--verbose", "-v"})
GLOBAL_OPTIONS_WITH_VALUE = frozenset({"--repo", "--layout", "--remote"})


def hoist_global_options(argv: list[str]) -> list[str]:
    """Move global options ahead of the subcommand so they may be written anywhere.

    Everything after a bare `--` is left alone, and an option already in front simply stays
    there, so this is idempotent.
    """
    leading: list[str] = []
    rest: list[str] = []
    index = 0

    while index < len(argv):
        token = argv[index]
        if token == "--":
            rest.extend(argv[index:])
            break
        name = token.split("=", 1)[0]
        if name in GLOBAL_SWITCHES:
            leading.append(token)
        elif name in GLOBAL_OPTIONS_WITH_VALUE:
            leading.append(token)
            # `--repo=x` carries its value; `--repo x` needs the next token too.
            if "=" not in token and index + 1 < len(argv):
                index += 1
                leading.append(argv[index])
        else:
            rest.append(token)
        index += 1

    return leading + rest


def main() -> None:
    try:
        app(args=hoist_global_options(sys.argv[1:]))
    except EXPECTED_ERRORS as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == "__main__":  # pragma: no cover
    main()
