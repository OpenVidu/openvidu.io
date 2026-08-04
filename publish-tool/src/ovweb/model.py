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
class PatternRule:
    """A regex redirect compiled into the 404 router, before `for_each` expansion."""

    id: str
    match: str
    to: str
    for_each: str | None = None
    description: str = ""


@dataclass(frozen=True)
class ResolvedPattern:
    """A single regex redirect, ready to be emitted into the 404 router."""

    id: str
    match: str
    to: str


@dataclass(frozen=True)
class MirrorRule:
    """Answer a versioned section's URLs without their version prefix.

    One redirect page per published page of every section named by `for_each`, at the
    unversioned path. Documentation is served under `/latest/docs/`, so `/docs/self-hosting/`
    would otherwise be handled by the 404 router — which GitHub serves with a 404 status, the
    thing a crawler acts on before it runs any JavaScript.
    """

    for_each: str
    body: str
    enabled: bool = True


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
    pattern_rules: tuple[PatternRule, ...]
    mirror: MirrorRule | None = None
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
