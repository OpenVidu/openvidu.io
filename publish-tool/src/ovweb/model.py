"""Frozen value objects shared across the tool. Pure: no I/O, no imports beyond stdlib."""

from __future__ import annotations

from dataclasses import dataclass, field

#: Shields author-pinned /X.Y/<versioned page>/ links from the blanket version strip applied to
#: pages promoted to the site root. See :mod:`ovweb.rewrite.nonversioned`.
KEEPVERSION_SENTINEL = "@@KEEPVERSION@@"

#: The named location a redirect rule may use instead of a path template.
VERSION_ROOT = "version-root"


@dataclass(frozen=True)
class SiteLayout:
    """Which parts of a built site are versioned, promoted to the root, or assets."""

    site_url: str
    versioned_pages: tuple[str, ...]
    non_versioned_pages: tuple[str, ...]
    assets: tuple[str, ...]
    pinned_assets: tuple[str, ...]
    root_files: tuple[str, ...]
    feeds: tuple[str, ...]

    @property
    def files_removed_from_past_version(self) -> tuple[str, ...]:
        """Root files deleted from a version folder when the site root is left untouched.

        Everything in :attr:`root_files` except ``index.html``, which is overwritten by the
        generated version-root redirect rather than deleted.
        """
        return tuple(name for name in self.root_files if name != "index.html")

    @property
    def base_url(self) -> str:
        """`site_url` without a trailing slash, for building absolute URLs."""
        return self.site_url.rstrip("/")


@dataclass(frozen=True)
class RedirectRule:
    """A redirect materialised as an HTML file, before version resolution."""

    id: str
    at: str
    to: str
    canonical: str | None = None
    title: str | None = None
    body: str | None = None
    robots: str | None = None
    lang: str | None = None
    relative: bool | None = None
    preserve_query_and_hash: bool | None = None
    enabled: bool = True
    versions: str | None = None
    when: tuple[RedirectOverride, ...] = ()
    description: str = ""


@dataclass(frozen=True)
class RedirectOverride:
    """Fields of a :class:`RedirectRule` that apply only to a version range."""

    versions: str
    to: str | None = None
    canonical: str | None = None
    title: str | None = None
    body: str | None = None
    robots: str | None = None
    lang: str | None = None
    relative: bool | None = None
    preserve_query_and_hash: bool | None = None
    enabled: bool | None = None


@dataclass(frozen=True)
class ResolvedRedirect:
    """A redirect rule with every field decided for one concrete version."""

    rule_id: str
    path: str
    to: str
    canonical: str | None
    title: str
    body: str
    robots: str
    lang: str
    relative: bool
    preserve_query_and_hash: bool


@dataclass(frozen=True)
class ExpandFields:
    """The page fields an expansion rule may override; unset ones fall back to the defaults."""

    title: str | None = None
    body: str | None = None
    robots: str | None = None
    lang: str | None = None
    preserve_query_and_hash: bool | None = None


@dataclass(frozen=True)
class CrossProductRule:
    """Many single-page moves that differ only by path segments: one stub per `values` combination.

    `at`, `to`, `canonical` and `body` may use `{version}` and any `values` key. Resolved
    against the published tree, so a combination whose old path is still a real page, or whose
    target does not exist, produces no stub.
    """

    id: str
    at: str
    to: str
    values: tuple[tuple[str, tuple[str, ...]], ...]
    canonical: str | None = None
    fields: ExpandFields = ExpandFields()
    enabled: bool = True
    versions: str | None = None
    description: str = ""


@dataclass(frozen=True)
class TreeRenameRule:
    """A directory moved: one stub per page under the new path, at its old path.

    The pages are enumerated from the tree under `to_path`, so every stub has a live target by
    construction and a page removed in the same release needs its own `files` rule.
    """

    id: str
    from_path: str
    to_path: str
    fields: ExpandFields = ExpandFields()
    enabled: bool = True
    versions: str | None = None
    description: str = ""


@dataclass(frozen=True)
class SectionFallbackRule:
    """A section absent from some versions: every URL it answers elsewhere redirects to `to`.

    Sources are enumerated from the versions outside the `versions` gate — the ones that have
    the section — so a reader switching into a gated version lands on `to` whatever page of the
    section they came from. `versions` is required: the gate is what separates the versions
    that lack the section from the ones that donate its URLs.
    """

    id: str
    dir: str
    to: str
    versions: str
    fields: ExpandFields = ExpandFields()
    enabled: bool = True
    description: str = ""


@dataclass(frozen=True)
class VersionAliasRule:
    """A retired version folder aliased to its minor: one stub per page of the minor.

    `folders` name folders that no longer exist as versions — the pre-regroup exact-patch
    releases. Each is rebuilt as a mirror of its minor's tree, so `/3.4.1/docs/x/` answers with
    a redirect to `/3.4/docs/x/`.
    """

    id: str
    folders: tuple[str, ...]
    fields: ExpandFields = ExpandFields()
    enabled: bool = True
    description: str = ""


@dataclass(frozen=True)
class UnversionedMirrorRule:
    """Every versioned page answering at its unversioned URL: `/docs/x/` -> `/latest/docs/x/`.

    Enumerated from the newest version's tree, one stub per page of every section named by
    `for_each`. GitHub Pages serves `404.html` with a 404 status — the thing a crawler acts on
    before it runs any JavaScript — so a real page with a meta refresh is the only redirect a
    crawler can be given for these URLs.
    """

    id: str
    for_each: str
    fields: ExpandFields = ExpandFields()
    enabled: bool = True
    description: str = ""


ExpandRule = (
    CrossProductRule
    | TreeRenameRule
    | SectionFallbackRule
    | VersionAliasRule
    | UnversionedMirrorRule
)


@dataclass(frozen=True)
class RedirectDefaults:
    """Field values inherited by every redirect rule that does not override them."""

    lang: str = "en"
    title: str = "Redirecting…"
    body: str = "Redirecting…"
    robots: str = "noindex, follow"
    relative: bool = True
    preserve_query_and_hash: bool = True


@dataclass(frozen=True)
class SiteConfig:
    """Everything ovweb.yaml declares."""

    layout: SiteLayout
    defaults: RedirectDefaults
    file_rules: tuple[RedirectRule, ...]
    expand_rules: tuple[ExpandRule, ...] = ()
    source: str = "<unknown>"


@dataclass(frozen=True)
class Step:
    """One post-processing step, as reported by `--dry-run` and the `--json` journal."""

    name: str
    title: str
    detail: str = ""


@dataclass(frozen=True)
class PublishPlan:
    """The ordered, fully resolved description of what a publish will do."""

    version: str
    update_latest: bool
    source_branch: str
    delete_first: bool
    create_branch: bool
    sync_branch: bool
    push: bool
    steps: tuple[Step, ...] = ()
    redirects: tuple[ResolvedRedirect, ...] = ()
    notes: tuple[str, ...] = field(default=())
