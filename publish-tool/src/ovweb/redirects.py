"""Resolve redirect rules for a concrete version and render them to HTML.

Pure. Jinja2 is imported lazily inside :func:`render_redirect` so that the MkDocs hook,
which only needs the pattern rules, does not require it.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache

from .model import (
    VERSION_ROOT,
    PatternRule,
    RedirectOverride,
    RedirectRule,
    ResolvedPattern,
    ResolvedRedirect,
    SiteConfig,
)
from .versions import matches

TEMPLATE_NAME = "redirect.html.j2"

#: The alias the mirror sends visitors to. `latest` is the evergreen name for the newest
#: version folder, and the prefix `promote_root_sitemap` writes into every versioned URL.
ALIAS = "latest"

#: Every mirror stub is generated under this rule id, which is what the marker comment in the
#: rendered page names and what `ovweb verify` looks for.
MIRROR_RULE_ID = "unversioned-page-mirror"

#: One `<loc>` in a sitemap. Whitespace is tolerated inside the element: MkDocs' template
#: indents the URL onto its own line.
SITEMAP_LOC = re.compile(r"<loc>\s*([^<\s]+)\s*</loc>")

# A target ends up in an HTML attribute, in a `meta refresh` content value and in a
# JavaScript string. Rejecting these characters outright is simpler, and easier to reason
# about, than escaping the same value three different ways.
_FORBIDDEN_IN_TARGET = re.compile(r'["\'<>\s]')


class RedirectError(Exception):
    """A redirect rule cannot be resolved."""


def resolve_file_redirects(config: SiteConfig, version: str) -> tuple[ResolvedRedirect, ...]:
    """Every file redirect that applies to `version`, fully resolved."""
    resolved = []
    for rule in config.file_rules:
        outcome = resolve_rule(config, rule, version)
        if outcome is not None:
            resolved.append(outcome)
    return tuple(resolved)


def resolve_rule(config: SiteConfig, rule: RedirectRule, version: str) -> ResolvedRedirect | None:
    """Resolve one rule for one version, or `None` when it does not apply."""
    if rule.versions is not None and not matches(rule.versions, version):
        return None

    override = _matching_override(rule, version)

    def pick(name: str):
        if override is not None:
            value = getattr(override, name)
            if value is not None:
                return value
        value = getattr(rule, name)
        if value is not None:
            return value
        return getattr(config.defaults, name, None)

    if not bool(pick("enabled")):
        return None

    path = _resolve_path(rule, version)
    relative = bool(pick("relative"))
    target = _interpolate(str(pick("to")), version=version, layout_url=config.layout.base_url)
    canonical_raw = pick("canonical")
    canonical = (
        _interpolate(str(canonical_raw), version=version, layout_url=config.layout.base_url)
        if canonical_raw
        else None
    )

    _validate_target(rule.id, target, relative=relative)
    if canonical is not None and not canonical.startswith(("http://", "https://")):
        raise RedirectError(
            f"redirect {rule.id!r}: canonical must be an absolute URL, got {canonical!r}"
        )

    return ResolvedRedirect(
        rule_id=rule.id,
        path=path,
        to=target,
        canonical=canonical,
        title=str(pick("title")),
        body=str(pick("body")),
        robots=str(pick("robots")),
        lang=str(pick("lang")),
        relative=relative,
        preserve_query_and_hash=bool(pick("preserve_query_and_hash")),
    )


def _matching_override(rule: RedirectRule, version: str) -> RedirectOverride | None:
    hits = [entry for entry in rule.when if matches(entry.versions, version)]
    if len(hits) > 1:
        raise RedirectError(
            f"redirect {rule.id!r} is ambiguous for version {version}: "
            f"{len(hits)} 'when' entries match ({', '.join(hit.versions for hit in hits)}). "
            "Version ranges must not overlap — a first-match-wins rule would make the "
            "published redirect depend on the order of the config file."
        )
    return hits[0] if hits else None


def _resolve_path(rule: RedirectRule, version: str) -> str:
    if rule.at == VERSION_ROOT:
        return f"{version}/index.html"
    if "{version}" not in rule.at:
        return rule.at
    return rule.at.replace("{version}", version)


def _interpolate(value: str, *, version: str, layout_url: str) -> str:
    return value.replace("{version}", version).replace("{site_url}", layout_url)


def _validate_target(rule_id: str, target: str, *, relative: bool) -> None:
    if not target:
        raise RedirectError(f"redirect {rule_id!r}: 'to' must not be empty")
    if _FORBIDDEN_IN_TARGET.search(target):
        raise RedirectError(
            f"redirect {rule_id!r}: 'to' must not contain quotes, angle brackets or "
            f"whitespace, got {target!r}"
        )
    if relative and target.startswith("/"):
        raise RedirectError(
            f"redirect {rule_id!r}: 'to' is {target!r}, but the rule is relative. A redirect "
            "installed inside a version folder must use a relative target: `latest` is a "
            "symlink to the newest version folder, so the same file answers at /latest/ and "
            "at /X.Y/, and an absolute target would leak a version number to visitors of the "
            "stable /latest/ URL. Set `relative: false` if the target really is site-absolute."
        )


def resolve_patterns(config: SiteConfig) -> tuple[ResolvedPattern, ...]:
    """Expand the pattern rules into the flat, ordered list the 404 router emits.

    Order is significant: the router tries each pattern in turn and stops at the first
    match, exactly as the hand-written router did.
    """
    resolved: list[ResolvedPattern] = []
    for rule in config.pattern_rules:
        resolved.extend(_expand(rule, config))
    return tuple(resolved)


def _expand(rule: PatternRule, config: SiteConfig) -> list[ResolvedPattern]:
    if rule.for_each is None:
        return [ResolvedPattern(id=rule.id, match=rule.match, to=rule.to)]
    return [
        ResolvedPattern(
            id=f"{rule.id}:{item}",
            match=rule.match.replace("{item}", item),
            to=rule.to.replace("{item}", item),
        )
        for item in getattr(config.layout, rule.for_each)
    ]


def mirror_redirects(sitemap: str, *, config: SiteConfig) -> tuple[ResolvedRedirect, ...]:
    """One redirect page per published page of every mirrored section, at its unversioned path.

    `sitemap` is the **promoted root sitemap**, where versioned pages already read
    `https://openvidu.io/latest/docs/…`. Deriving the set from it rather than from the tree is
    what keeps the mirror honest in both directions: everything the site advertises gets a stub,
    and nothing else does. The three `3.8/docs/*/index.html` files that are not in the sitemap —
    the generated `getting-started` redirect and two typedoc index pages — are therefore skipped,
    which is right: mirroring a redirect would publish a chain, and the sitemap is the site's own
    statement of what a crawler should ask for.

    Order follows the sitemap, so the same input always produces the same files in the same
    order.
    """
    rule = config.mirror
    if rule is None or not rule.enabled:
        return ()

    sections = getattr(config.layout, rule.for_each)
    prefixes = [(f"{config.layout.base_url}/{ALIAS}/{section}/", section) for section in sections]

    resolved: dict[str, ResolvedRedirect] = {}
    for url in SITEMAP_LOC.findall(sitemap):
        for prefix, section in prefixes:
            if not url.startswith(prefix):
                continue
            # Every page URL this site publishes ends in a slash (`directory_urls`), and the
            # stub's own path is built by appending index.html — so a URL naming a file has no
            # correct mirror path and is left to the 404 router.
            if not url.endswith("/"):
                break
            page = f"{section}/{url[len(prefix) :]}"
            path = f"{page}index.html"
            target = f"/{ALIAS}/{page}"
            _validate_target(MIRROR_RULE_ID, target, relative=False)
            resolved.setdefault(
                path,
                ResolvedRedirect(
                    rule_id=MIRROR_RULE_ID,
                    path=path,
                    to=target,
                    canonical=url,
                    title=config.defaults.title,
                    body=rule.body,
                    robots=config.defaults.robots,
                    lang=config.defaults.lang,
                    # A root-level stub is served from exactly one URL, so there is no `latest`
                    # symlink to stay inside and nothing to gain from a relative target — an
                    # absolute one says where it goes without counting `../` segments.
                    relative=False,
                    preserve_query_and_hash=config.defaults.preserve_query_and_hash,
                ),
            )
            break
    return tuple(resolved.values())


def render_redirect(redirect: ResolvedRedirect) -> str:
    """Render the redirect page.

    Every element earns its place:

    * ``meta http-equiv="refresh"`` with a zero delay is the no-JS path, and on GitHub Pages the
      only redirect a search engine can be given at all: it treats a zero-delay meta refresh as
      a redirect and passes ranking signals to the target. The URL is **relative** for a rule
      installed inside a version folder, which is what lets one file serve both ``/3.8/`` and
      ``/latest/``, and site-absolute for the root-level mirror, which is served from one URL.
    * ``robots: noindex, follow`` keeps the stub out of search results while still letting
      link equity flow to the target.
    * An absolute ``canonical`` consolidates every version's copy of the redirect on one
      evergreen URL, matching what the publish does to every other versioned page. It is
      belt and braces, since a ``noindex`` page's canonical is ignored; set ``canonical:
      null`` on the rule to omit it.
    * ``location.replace`` (not an assignment to ``location.href``) does not add a history
      entry, so the back button still works, and the query string and fragment are forwarded
      explicitly instead of being dropped.
    * A real ``<a>`` in the body works when the refresh is blocked, and is crawlable.
    """
    template = _environment().get_template(TEMPLATE_NAME)
    rendered = template.render(
        lang=redirect.lang,
        robots=redirect.robots,
        title=redirect.title,
        body=redirect.body,
        to=redirect.to,
        to_js=json.dumps(redirect.to),
        relative=redirect.relative,
        canonical=redirect.canonical,
        preserve_query_and_hash=redirect.preserve_query_and_hash,
        rule_id=redirect.rule_id,
    )
    return rendered if rendered.endswith("\n") else rendered + "\n"


@lru_cache(maxsize=1)
def _environment():
    from jinja2 import Environment, PackageLoader, select_autoescape

    return Environment(
        loader=PackageLoader("ovweb", "data/templates"),
        autoescape=select_autoescape(default_for_string=True, default=True),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
