"""Build the ordered description of what a publish will do.

Pure: :func:`build_plan` decides everything up front, so `--dry-run` can print the exact
sequence without touching git, mike or the filesystem. The post-processing pipeline walks the
same step list, which keeps the printed plan honest.
"""

from __future__ import annotations

from .config import SiteConfig
from .model import PublishPlan, ResolvedRedirect, Step
from .redirects import resolve_file_redirects

# The post-processing steps, in execution order. `scope` says
# whether a step runs always, only when the root pages are refreshed ("latest"), or only when
# they are left alone ("past").
POSTPROCESS_STEPS: tuple[tuple[str, str, str, str], ...] = (
    ("remove-overrides", "always", "Remove the theme override folder", "<version>/overrides/"),
    (
        "rewrite-versioned",
        "always",
        "Rewrite links in versioned pages",
        "pin assets to the version, absolutise root links, point canonical/og:url at /latest/",
    ),
    ("rewrite-search-index", "always", "Absolutise the search index locations", ""),
    (
        "rewrite-non-versioned",
        "latest",
        "Rewrite links in pages promoted to the root",
        "point versioned links at /latest/, strip the version from self URLs",
    ),
    (
        "promote-to-root",
        "latest",
        "Promote assets, root files and non-versioned pages",
        "assets are copied, everything else is moved",
    ),
    ("promote-sitemap", "latest", "Copy the version sitemap to the root and rewrite it", ""),
    (
        "promote-search-index",
        "latest",
        "Point the root search index at /latest/",
        "the version's own index keeps its version, so in-version search stays in the version",
    ),
    (
        "strip-non-versioned",
        "past",
        "Delete the promoted pages from the version folder",
        "tolerant: an old version may never have built some of them",
    ),
    ("install-redirects", "always", "Write the generated redirect pages", ""),
    (
        "remove-version-sitemap",
        "always",
        "Remove this version's sitemap",
        "nothing references it; only the root sitemap is published",
    ),
    ("sync-releases", "always", "Splice the newest release notes across versions", ""),
    (
        "commit",
        "always",
        "Commit the gh-pages branch",
        "locally; the push happens afterwards, once the tree is known to be correct",
    ),
)


def build_plan(
    config: SiteConfig,
    *,
    version: str,
    update_latest: bool,
    delete_first: bool = False,
    create_branch: bool = False,
    sync_branch: bool = False,
    push: bool = True,
) -> PublishPlan:
    """Resolve the full publish description for one invocation."""
    redirects = resolve_file_redirects(config, version)
    scope_now = "latest" if update_latest else "past"

    steps = tuple(
        Step(name=name, title=title, detail=detail)
        for name, scope, title, detail in POSTPROCESS_STEPS
        if scope in ("always", scope_now)
    )

    return PublishPlan(
        version=version,
        update_latest=update_latest,
        # mike builds the site from the working tree, so the branch checked out at build
        # time decides the content: main for the newest version, the version's own branch
        # for a past one.
        source_branch="main" if update_latest else version,
        delete_first=delete_first,
        create_branch=create_branch,
        sync_branch=sync_branch,
        push=push,
        steps=steps,
        redirects=redirects,
        notes=_notes(redirects, version=version, update_latest=update_latest),
    )


def _notes(
    redirects: tuple[ResolvedRedirect, ...], *, version: str, update_latest: bool
) -> tuple[str, ...]:
    notes = []
    if update_latest:
        notes.append(
            f"`latest` will point at {version}, and the pages served from the site root "
            "will be replaced by this version's build."
        )
        notes.append("The newest release notes will be spliced into every other version folder.")
    else:
        notes.append(
            "The pages served from the site root will not be touched, and `latest` will not move."
        )
        notes.append(
            "This version's releases pages will be overwritten with the current newest ones."
        )
    if not redirects:
        notes.append(f"No redirect rule applies to version {version}.")
    return tuple(notes)
