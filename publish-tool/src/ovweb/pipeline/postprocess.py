"""Turn mike's raw output for one version into the published site layout.

Takes the tree to work on as an argument and touches git only in the final step, which makes
`ovweb postprocess --tree <copy> --no-commit` a deterministic unit.

The steps fall into three groups, and the order matters:

1. Clean the version folder and rewrite everything that stays inside it.
2. Either build the site root from this version (when it becomes `latest`) or strip the
   root-served content out of the version folder (when it does not).
3. Write the redirects, including the mirror that answers the versioned pages' unversioned
   URLs; prune what is not published; sync the release notes.

Group 2 has to precede the redirects, because promoting moves the version's `index.html` out to
the root and the generated redirect then takes its place.

Every page is published twice — as HTML and as the Markdown export the llmstxt plugin writes
beside it — so the two rewriting steps dispatch on the file's suffix. See
:mod:`ovweb.rewrite.markdown`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .. import fsops
from ..config import SiteConfig
from ..discovery import latest_in_tree, versions_in_tree
from ..expand import (
    alias_redirects,
    mirror_redirects,
    mirror_rule,
    scan_tree,
    version_redirects,
    wipe_owned,
)
from ..redirects import is_generated_redirect, render_redirect
from ..releases import DestinationRegionError, splice_releases
from ..report import Reporter
from ..rewrite import (
    promote_root_sitemap,
    promote_search_index,
    prune_version_sitemap,
    repair_export_links,
    rewrite_404,
    rewrite_feed,
    rewrite_non_versioned_file,
    rewrite_promoted_markdown,
    rewrite_search_index,
    rewrite_versioned_file,
    rewrite_versioned_markdown,
    sync_version_sitemap,
)
from ..rewrite.markdown import SUFFIX as MARKDOWN

SITEMAP = "sitemap.xml"
SEARCH_INDEX = "search/search_index.json"

#: The index of every page's Markdown export. Served only from the site root, and a Markdown
#: file itself, so the promoted rules apply to it unchanged.
LLMS_TXT = "llms.txt"


class PostprocessError(Exception):
    """The tree cannot be post-processed."""


@dataclass
class PostprocessResult:
    version: str
    update_latest: bool
    counts: dict[str, int] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    redirects_written: list[str] = field(default_factory=list)


def postprocess(
    tree: Path,
    *,
    config: SiteConfig,
    version: str,
    update_latest: bool,
    report: Reporter,
    force: bool = False,
) -> PostprocessResult:
    """Turn mike's raw output for `version` into the published site layout."""
    layout = config.layout
    version_dir = tree / version
    if not version_dir.is_dir():
        raise PostprocessError(
            f"{version_dir} does not exist. mike should have created it — has the deploy run?"
        )

    result = PostprocessResult(version=version, update_latest=update_latest)

    _guard(version_dir, force=force)

    # 1. Drop what must never be published.
    report.step("remove-overrides", "Remove the theme override folder")
    removed = fsops.remove(version_dir / "overrides", required=False)
    # `site/` only exists when the tree came from a checkout rather than a fresh worktree.
    removed += fsops.remove(tree / "site", required=False)
    report.result("remove-overrides", removed=int(removed))

    # 2. Versioned pages: pin assets, absolutise root links, consolidate SEO URLs.
    report.step("rewrite-versioned", "Rewrite links in versioned pages")

    def versioned(path: Path, text: str) -> str:
        if path.suffix == MARKDOWN:
            return rewrite_versioned_markdown(text, version=version, layout=layout)
        return rewrite_versioned_file(text, version=version, layout=layout)

    changed = 0
    for directory in layout.versioned_pages:
        changed += fsops.rewrite_tree_per_file(version_dir / directory, versioned)
    result.counts["rewrite-versioned"] = changed
    report.result("rewrite-versioned", files_changed=changed)

    # 3. Search index: relative locations become absolute.
    report.step("rewrite-search-index", "Absolutise the search index locations")
    changed = int(
        fsops.rewrite_single(
            version_dir / SEARCH_INDEX,
            lambda text: rewrite_search_index(text, version=version, layout=layout),
        )
    )
    result.counts["rewrite-search-index"] = changed
    report.result("rewrite-search-index", files_changed=changed)

    # Group 2: build the site root from this version, or strip the root-served content out of it.
    if update_latest:
        _rewrite_promoted_pages(tree, version=version, config=config, report=report, result=result)
        _promote_to_root(tree, version=version, config=config, report=report, result=result)
        _promote_sitemap(tree, version=version, config=config, report=report, result=result)
        _promote_search_index(tree, version=version, config=config, report=report, result=result)
    else:
        _strip_promoted_pages(tree, version=version, config=config, report=report, result=result)

    # Last of the rewrites, because it checks links against the tree as finally laid out.
    _repair_export_links(tree, version=version, config=config, report=report, result=result)

    # Group 3. The redirects come after promotion, which moves this version's index.html to the
    # root and leaves the version root free for the generated page.
    report.step("install-redirects", "Write the generated redirect pages")
    for redirect in version_redirects(tree, config, version):
        fsops.write_text(tree / redirect.path, render_redirect(redirect))
        result.redirects_written.append(redirect.path)
        report.detail(f"{redirect.path} -> {redirect.to} [{redirect.rule_id}]")
    report.result("install-redirects", written=len(result.redirects_written))

    if update_latest:
        _mirror_unversioned_pages(
            tree, version=version, config=config, report=report, result=result
        )

    _alias_versions(tree, version=version, config=config, report=report, result=result)
    _prune_version_sitemap(tree, version=version, config=config, report=report, result=result)
    _sync_version_sitemap(tree, version=version, config=config, report=report, result=result)
    _sync_releases(tree, version=version, config=config, report=report, result=result)

    return result


def _guard(version_dir: Path, *, force: bool) -> None:
    """Refuse to post-process a tree that has already been post-processed.

    The pipeline is not idempotent, and a second run is silently destructive twice over: the
    sentinel that shields author-pinned `/X.Y/docs/` links is single-shot, so a re-run strips the
    version out of every release-notes link in the blog, and promotion moves directories, so it
    half-fails once they are gone.
    """
    index = version_dir / "index.html"
    if index.is_file() and is_generated_redirect(index) and not force:
        raise PostprocessError(
            f"{index} is already a generated redirect, so this tree has been post-processed "
            "before. Running the pipeline twice would strip the version out of author-pinned "
            "links and fail on the already-moved directories. Re-deploy the version with mike "
            "first, or pass --force if you know the tree is safe."
        )


def _rewrite_promoted_pages(
    tree: Path, *, version: str, config: SiteConfig, report: Reporter, result: PostprocessResult
) -> None:
    """Rewrite the pages that are about to be served from the site root."""
    layout = config.layout
    version_dir = tree / version
    report.step("rewrite-non-versioned", "Rewrite links in pages promoted to the root")

    changed = int(
        fsops.rewrite_single(
            version_dir / "404.html",
            lambda text: rewrite_404(text, version=version, layout=layout),
        )
    )

    def promote_html(text: str) -> str:
        return rewrite_non_versioned_file(text, version=version, layout=layout)

    def promote_markdown(text: str) -> str:
        return rewrite_promoted_markdown(text, version=version, layout=layout)

    def promote(path: Path, text: str) -> str:
        return promote_markdown(text) if path.suffix == MARKDOWN else promote_html(text)

    for directory in layout.non_versioned_pages:
        changed += fsops.rewrite_tree_per_file(version_dir / directory, promote)

    # The home page is a root file rather than a folder, so the walk above misses both halves
    # of it.
    changed += int(fsops.rewrite_single(version_dir / "index.html", promote_html))
    changed += int(fsops.rewrite_single(version_dir / "index.md", promote_markdown, required=False))

    # llms.txt is a root-served Markdown file, so the promoted rules are exactly right for it.
    changed += int(fsops.rewrite_single(version_dir / LLMS_TXT, promote_markdown, required=False))

    for feed in layout.feeds:
        changed += int(
            fsops.rewrite_single(
                version_dir / feed,
                lambda text: rewrite_feed(text, version=version),
                required=False,
            )
        )

    result.counts["rewrite-non-versioned"] = changed
    report.result("rewrite-non-versioned", files_changed=changed)


def _promote_to_root(
    tree: Path, *, version: str, config: SiteConfig, report: Reporter, result: PostprocessResult
) -> None:
    """Move this version's root-served content out to the site root.

    Assets are **copied**, not moved: the version folder keeps its own copy, which is what the
    `/X.Y/assets/` pinning applied earlier points at. Everything else is moved.
    """
    layout = config.layout
    version_dir = tree / version
    report.step("promote-to-root", "Promote assets, root files and non-versioned pages")

    for asset in layout.assets:
        _require_built(version_dir / asset, key="assets", name=asset, version=version)
        fsops.copy_tree(version_dir / asset, tree / asset)
    for name in layout.root_files:
        _require_built(version_dir / name, key="root_files", name=name, version=version)
        fsops.move(version_dir / name, tree / name)
    for page in layout.non_versioned_pages:
        _require_built(version_dir / page, key="non_versioned_pages", name=page, version=version)
        fsops.move(version_dir / page, tree / page)

    result.counts["promote-to-root"] = (
        len(layout.assets) + len(layout.root_files) + len(layout.non_versioned_pages)
    )
    report.result(
        "promote-to-root",
        assets_copied=len(layout.assets),
        files_moved=len(layout.root_files),
        pages_moved=len(layout.non_versioned_pages),
    )


def _require_built(path: Path, *, key: str, name: str, version: str) -> None:
    """Fail with the config key at fault rather than a bare FileNotFoundError.

    Promotion is strict — silently skipping a page the config asks for would publish a site
    missing it — and the likely cause is a name in ovweb.yaml matching nothing the site builds.
    """
    if path.exists():
        return
    raise PostprocessError(
        f"ovweb.yaml lists {name!r} under layout.{key}, but the build produced no "
        f"{version}/{name}. Either the name is wrong, or the page is not in the MkDocs nav."
    )


def _strip_promoted_pages(
    tree: Path, *, version: str, config: SiteConfig, report: Reporter, result: PostprocessResult
) -> None:
    """Delete the root-served content from a version folder without touching the root.

    Every removal is tolerant: an old version branch may never have built some of these files,
    because llms.txt and the RSS feeds need plugins its mkdocs.yml did not have. `index.html` is
    not removed — the generated redirect overwrites it.
    """
    layout = config.layout
    version_dir = tree / version
    report.step("strip-non-versioned", "Delete the promoted pages from the version folder")

    removed = fsops.remove_all(
        (version_dir / page for page in layout.non_versioned_pages), required=False
    )
    removed += fsops.remove_all(
        (version_dir / name for name in layout.files_removed_from_past_version), required=False
    )

    result.counts["strip-non-versioned"] = removed
    report.result("strip-non-versioned", removed=removed)


def _promote_sitemap(
    tree: Path,
    *,
    version: str,
    config: SiteConfig,
    report: Reporter,
    result: PostprocessResult,
) -> None:
    """Copy the version's sitemap to the root and rewrite it for the root URL scheme.

    This is the sitemap crawlers read: `robots.txt` names it, and it is a plain `urlset` rather
    than an index, so it has to list every URL itself.
    """
    report.step("promote-sitemap", "Copy the version sitemap to the root and rewrite it")

    source = tree / version / SITEMAP
    target = tree / SITEMAP
    text = promote_root_sitemap(fsops.read_text(source), version=version, layout=config.layout)
    fsops.write_text(target, text)
    fsops.write_gzip(target)

    result.counts["promote-sitemap"] = 1
    report.result("promote-sitemap", written=1)


def _promote_search_index(
    tree: Path, *, version: str, config: SiteConfig, report: Reporter, result: PostprocessResult
) -> None:
    """Point the root search index's versioned hits at `/latest/`.

    The root index is a copy of this version's, taken by the promotion above, so its versioned
    locations still name the version they were rewritten for. Every other root-to-versioned
    reference uses `/latest/`, which does not go stale at the next release. The version's own
    index keeps its version, so searching inside a version returns that version's pages.
    """
    report.step("promote-search-index", "Point the root search index at /latest/")

    changed = int(
        fsops.rewrite_single(
            tree / SEARCH_INDEX,
            lambda text: promote_search_index(text, version=version, layout=config.layout),
        )
    )

    result.counts["promote-search-index"] = changed
    report.result("promote-search-index", files_changed=changed)


def _mirror_unversioned_pages(
    tree: Path, *, version: str, config: SiteConfig, report: Reporter, result: PostprocessResult
) -> None:
    """Make every versioned page answer at its unversioned URL too, with a redirect page.

    Wiped and rebuilt in full rather than reconciled page by page: a renamed or removed page
    would otherwise leave a stub redirecting into a 404, which is worse than the 404 it
    replaced. Regenerating from this publish's tree makes that state unrepresentable.

    Runs after `install-redirects` so a versioned page that is itself a redirect is mirrored as
    its final destination, and only on a latest publish, since the stubs send visitors to
    `/latest/`.
    """
    rule = mirror_rule(config)
    if rule is None:
        return

    report.step("mirror-unversioned", "Answer the versioned pages' unversioned URLs")

    redirects = mirror_redirects(tree, config, latest=version)
    removed = sum(
        int(wipe_owned(tree / section)) for section in getattr(config.layout, rule.for_each)
    )
    for redirect in redirects:
        fsops.write_text(tree / redirect.path, render_redirect(redirect))

    result.counts["mirror-unversioned"] = len(redirects)
    report.result("mirror-unversioned", removed=removed, written=len(redirects))


def _alias_versions(
    tree: Path, *, version: str, config: SiteConfig, report: Reporter, result: PostprocessResult
) -> None:
    """Rebuild the legacy patch-version folders that alias the version being published.

    `3.4.0` and `3.4.1` mirror whatever `3.4` serves, so they are rebuilt whenever `3.4` is —
    wiped and regenerated like the unversioned mirror, and for the same reason. Folders aliasing
    other minors are left as their own publish produced them.
    """
    report.step("alias-versions", "Rebuild the legacy patch-version folders")

    written = 0
    rebuilt = []
    for folder, redirects in alias_redirects(tree, config, minors={version}):
        wipe_owned(tree / folder)
        for redirect in redirects:
            fsops.write_text(tree / redirect.path, render_redirect(redirect))
        written += len(redirects)
        rebuilt.append(folder)
        report.detail(f"{folder}/ -> {version}/ ({len(redirects)} pages)")

    result.counts["alias-versions"] = written
    report.result("alias-versions", folders=len(rebuilt), written=written)


def _repair_export_links(
    tree: Path, *, version: str, config: SiteConfig, report: Reporter, result: PostprocessResult
) -> None:
    """Point every link at a Markdown export that does not exist back at its HTML page.

    Runs after promotion so the tree is in its final shape, which is what makes the check
    trustworthy: the set of real exports is read off disk rather than inferred from the MkDocs
    configuration. See :func:`ovweb.rewrite.markdown.repair_export_links` for why the links need
    repairing at all.

    Scope follows the rest of the pipeline — this version's exports, plus the root's when the root
    is being rebuilt. Another version's folder is left as its own publish produced it.
    """
    report.step("repair-export-links", "Point links at the HTML page where no export exists")

    # On a latest publish `latest` is this version, whether or not mike has materialised the
    # symlink yet; otherwise the tree decides.
    alias = version if result.update_latest else latest_in_tree(tree)
    if alias is None:
        # Every promoted export links to `/latest/…`. Without knowing what that resolves to, those
        # links cannot be checked, and guessing would strip `index.md` from all of them at once.
        message = "could not resolve the 'latest' alias; export links were left as built"
        result.warnings.append(message)
        report.warn(message)
        result.counts["repair-export-links"] = 0
        return

    exports = _published_exports(tree, alias=alias)

    def repair(text: str) -> str:
        return repair_export_links(text, exports=exports, layout=config.layout)

    # Named explicitly rather than walking the tree root: a walk from there descends into every
    # other version folder, and repairing those would reach outside this publish.
    directories = [tree / version]
    files = []
    if result.update_latest:
        directories += [tree / page for page in config.layout.non_versioned_pages]
        files = [tree / f"index{MARKDOWN}", tree / LLMS_TXT]

    changed = 0
    for directory in directories:
        for path in directory.rglob(f"*{MARKDOWN}"):
            changed += int(fsops.rewrite_file(path, repair))
    for path in files:
        changed += int(fsops.rewrite_single(path, repair, required=False))

    result.counts["repair-export-links"] = changed
    report.result("repair-export-links", files_changed=changed, exports=len(exports))


def _published_exports(tree: Path, *, alias: str) -> frozenset[str]:
    """Every Markdown export in the tree, as a site-root-relative path.

    `latest` is a symlink to a version folder, so that folder's exports are reachable under both
    names and both have to be in the set: a promoted export links to `/latest/docs/…`.
    """
    paths = {
        path.relative_to(tree).as_posix()
        for path in tree.rglob(f"*{MARKDOWN}")
        if path.is_file() and not path.is_symlink()
    }
    return frozenset(
        paths | {f"latest/{p[len(alias) + 1 :]}" for p in paths if p.startswith(f"{alias}/")}
    )


def _prune_version_sitemap(
    tree: Path, *, version: str, config: SiteConfig, report: Reporter, result: PostprocessResult
) -> None:
    """Drop the root-served pages from this version's sitemap and regenerate its `.gz`.

    This file is what makes the version selector keep a reader on the same page across a version
    switch: the theme fetches it at runtime and resolves the current path against it. See
    :mod:`ovweb.rewrite.sitemap` for the properties that have to hold.
    """
    report.step("prune-version-sitemap", "Drop the root-served pages from this version's sitemap")

    target = tree / version / SITEMAP
    changed = int(
        fsops.rewrite_single(
            target,
            lambda text: prune_version_sitemap(text, version=version, layout=config.layout),
        )
    )
    fsops.write_gzip(target)

    result.counts["prune-version-sitemap"] = changed
    report.result("prune-version-sitemap", files_changed=changed)


def _sync_version_sitemap(
    tree: Path, *, version: str, config: SiteConfig, report: Reporter, result: PostprocessResult
) -> None:
    """List this version's generated redirects in its sitemap.

    The version selector resolves a reader's page by exact lookup in this file, so a moved
    page keeps working across a version switch only if its old URL — now a stub — is listed.
    Runs after the pruning, which this must not disturb, and after every step that writes or
    removes stubs in the version folder.
    """
    report.step("sync-version-sitemap", "List the generated redirects in the version sitemap")

    stubs = scan_tree(tree, (version,)).stub_targets
    target = tree / version / SITEMAP
    fsops.rewrite_single(
        target,
        lambda text: sync_version_sitemap(text, base_url=config.layout.base_url, stubs=stubs),
    )
    fsops.write_gzip(target)

    result.counts["sync-version-sitemap"] = len(stubs)
    report.result("sync-version-sitemap", listed=len(stubs))


def _sync_releases(
    tree: Path, *, version: str, config: SiteConfig, report: Reporter, result: PostprocessResult
) -> None:
    """Make every version's releases pages show the newest release notes.

    Publishing the newest version pushes its notes out to every other version folder;
    re-publishing an older version pulls the current newest notes back in, so a rebuild does
    not regress it to the notes that version shipped with.
    """
    report.step("sync-releases", "Splice the newest release notes across versions")

    if result.update_latest:
        pairs = [(version, other) for other in versions_in_tree(tree)]
    else:
        newest = latest_in_tree(tree)
        if newest is None:
            message = "could not resolve the 'latest' alias; the releases pages were left as built"
            result.warnings.append(message)
            report.warn(message)
        pairs = [] if newest is None else [(newest, version)]

    spliced = 0
    for source, destination in pairs:
        if source == destination:
            continue
        spliced += _splice_pair(
            tree,
            source=source,
            destination=destination,
            config=config,
            report=report,
            result=result,
        )

    result.counts["sync-releases"] = spliced
    report.result("sync-releases", pages_spliced=spliced)


def _splice_pair(
    tree: Path,
    *,
    source: str,
    destination: str,
    config: SiteConfig,
    report: Reporter,
    result: PostprocessResult,
) -> int:
    spliced = 0
    for page in config.layout.versioned_pages:
        source_file = tree / source / page / "releases" / "index.html"
        destination_file = tree / destination / page / "releases" / "index.html"
        # Only copy when both sides have this releases page: OpenVidu Meet's documentation
        # did not exist before 3.4.
        if not source_file.is_file() or not destination_file.is_file():
            continue
        try:
            outcome = splice_releases(
                fsops.read_text(source_file), fsops.read_text(destination_file)
            )
        except DestinationRegionError as error:
            # An old version folder may have been built by a theme version that named these
            # regions differently: warn rather than abort a publish that is already half done. A
            # problem in the *source* is fatal and propagates.
            message = f"could not splice release notes into {destination}/{page}: {error}"
            result.warnings.append(message)
            report.warn(f"{message} — left as built")
            continue
        fsops.write_text(destination_file, outcome.html)
        report.detail(
            f"{source}/{page} -> {destination}/{page}: "
            f"{outcome.article_bytes} bytes, {outcome.tocs_replaced} table(s) of contents"
        )
        spliced += 1
    return spliced
