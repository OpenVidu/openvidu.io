"""Tree-dependent redirect expansion: one rule in ovweb.yaml, many generated pages.

Every kind here enumerates its stubs from the published tree rather than from a list, under
three filters that make an expansion safe to materialise as files:

* **Never shadow a real page.** A candidate path already holding a page ovweb did not generate
  is skipped, so an expansion cannot overwrite content.
* **Never redirect into a 404.** A candidate whose target does not exist in the tree is
  skipped, so a stub cannot be worse than the 404 it replaces.
* **Never chain.** A target that is itself a generated redirect is followed to its final
  destination, so every stub answers in one hop.

:func:`scan_tree` and the `*_redirects` orchestrators at the bottom are the impure entry
points; everything that takes a :class:`TreeIndex` is pure.
"""

from __future__ import annotations

import posixpath
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from itertools import product
from pathlib import Path

from . import fsops
from .discovery import version_folders
from .model import (
    CrossProductRule,
    ExpandFields,
    ResolvedRedirect,
    SectionFallbackRule,
    SiteConfig,
    TreeRenameRule,
    UnversionedMirrorRule,
    VersionAliasRule,
)
from .redirects import (
    ALIAS,
    REFRESH_TARGET,
    RedirectError,
    is_generated_redirect,
    resolve_file_redirects,
)
from .versions import matches, minor_of

PLACEHOLDER = re.compile(r"\{(\w+)\}")

#: How many generated redirects a chain may pass through before it is declared a cycle.
COLLAPSE_LIMIT = 10


@dataclass(frozen=True)
class TreeIndex:
    """Every page one scan of a published tree found, and where its generated redirects point.

    Paths are tree-relative POSIX paths of `.html` files. `stub_targets` maps a generated
    redirect's file path to its resolved target — a tree-relative URL path (trailing slash for
    a directory URL), with any fragment attached.
    """

    pages: frozenset[str]
    stub_targets: Mapping[str, str]


# -- reading the tree ------------------------------------------------------------------------


def scan_tree(root: Path, within: Iterable[str]) -> TreeIndex:
    """Index every `.html` file under the given tree-relative directories.

    Symlinks are skipped on both sides — `latest` aliases a version folder that is scanned
    under its own name.
    """
    pages: set[str] = set()
    stubs: dict[str, str] = {}
    for prefix in within:
        base = root / prefix if prefix else root
        if not base.is_dir() or base.is_symlink():
            continue
        for path in sorted(base.rglob("*.html")):
            if path.is_symlink() or not path.is_file():
                continue
            page = path.relative_to(root).as_posix()
            pages.add(page)
            if is_generated_redirect(path):
                match = REFRESH_TARGET.search(path.read_text(encoding="utf-8"))
                if match is None:
                    continue
                target = _resolve_raw_target(page, match.group(1))
                if target is not None:
                    stubs[page] = target
    return TreeIndex(pages=frozenset(pages), stub_targets=stubs)


def with_stubs(index: TreeIndex, redirects: Iterable[ResolvedRedirect]) -> TreeIndex:
    """`index` as it will look once `redirects` are written.

    Lets an expansion collapse through redirects that are resolved but not yet on disk — the
    `files` rules of the same publish.
    """
    pages = set(index.pages)
    stubs = dict(index.stub_targets)
    for redirect in redirects:
        pages.add(redirect.path)
        target = _resolve_raw_target(redirect.path, redirect.to)
        if target is not None:
            stubs[redirect.path] = target
    return TreeIndex(pages=frozenset(pages), stub_targets=stubs)


# -- path arithmetic -------------------------------------------------------------------------


def _split_fragment(target: str) -> tuple[str, str]:
    path, _, fragment = target.partition("#")
    return path, fragment


def _served_file(urlpath: str) -> str:
    """The file GitHub serves for a URL path: `x/` -> `x/index.html`, `y.html` -> itself."""
    return f"{urlpath}index.html" if urlpath.endswith("/") or urlpath == "" else urlpath


def _url_of(page: str) -> str:
    """A page's URL path: `x/index.html` -> `x/`, `y.html` -> `y.html`."""
    return page[: -len("index.html")] if page.endswith("index.html") else page


def _resolve_raw_target(stub_path: str, raw: str) -> str | None:
    """A stub's refresh target as a tree-relative URL path, or None if it leaves the tree."""
    path, fragment = _split_fragment(raw)
    if path.startswith("/"):
        resolved = path.lstrip("/")
    else:
        joined = posixpath.normpath(posixpath.join(posixpath.dirname(stub_path), path))
        if joined.startswith(".."):
            return None
        resolved = "" if joined == "." else joined
        if path.endswith("/") or path == "":
            resolved = f"{resolved}/" if resolved else ""
    return f"{resolved}#{fragment}" if fragment else resolved


def collapse(index: TreeIndex, target: str) -> str:
    """Follow `target` through any generated redirects to its final destination.

    A hop that carries its own fragment replaces the incoming one, matching what the rendered
    JavaScript does. A cycle returns the current position; verify reports the chain.
    """
    path, fragment = _split_fragment(target)
    for _ in range(COLLAPSE_LIMIT):
        forwarded = index.stub_targets.get(_served_file(path))
        if forwarded is None:
            break
        path, next_fragment = _split_fragment(forwarded)
        fragment = next_fragment or fragment
    return f"{path}#{fragment}" if fragment else path


def _exists(index: TreeIndex, urlpath: str) -> bool:
    return _served_file(urlpath) in index.pages


def _relative_target(at: str, urlpath: str, fragment: str) -> str:
    """`urlpath` expressed relative to the directory the stub at `at` lives in."""
    origin = posixpath.dirname(at)
    if urlpath.endswith("/"):
        relative = posixpath.relpath(urlpath.rstrip("/"), origin)
        relative = "./" if relative == "." else f"{relative}/"
    else:
        relative = posixpath.relpath(urlpath, origin)
    return f"{relative}#{fragment}" if fragment else relative


def _fill(template: str, mapping: Mapping[str, str]) -> str:
    return PLACEHOLDER.sub(lambda m: mapping.get(m.group(1), m.group(0)), template)


# -- the kinds -------------------------------------------------------------------------------


def _page_fields(fields: ExpandFields, config: SiteConfig) -> dict:
    defaults = config.defaults
    preserve = fields.preserve_query_and_hash
    return {
        "title": fields.title if fields.title is not None else defaults.title,
        "body": fields.body if fields.body is not None else defaults.body,
        "robots": fields.robots if fields.robots is not None else defaults.robots,
        "lang": fields.lang if fields.lang is not None else defaults.lang,
        "preserve_query_and_hash": (
            preserve if preserve is not None else defaults.preserve_query_and_hash
        ),
    }


def expand_for_version(
    config: SiteConfig,
    version: str,
    index: TreeIndex,
    *,
    fallback_sources: Mapping[str, Iterable[str]] | None = None,
) -> tuple[ResolvedRedirect, ...]:
    """Every stub the in-version expansion kinds produce for `version` against `index`.

    `fallback_sources` carries the section-fallback rules' donor URLs, keyed by rule id — see
    :func:`section_sources`, which enumerates them from the tree.
    """
    sources = fallback_sources or {}
    resolved: list[ResolvedRedirect] = []
    for rule in config.expand_rules:
        if isinstance(rule, CrossProductRule):
            resolved.extend(_cross_product(rule, version, index, config))
        elif isinstance(rule, TreeRenameRule):
            resolved.extend(_tree_rename(rule, version, index, config))
        elif isinstance(rule, SectionFallbackRule):
            resolved.extend(
                _section_fallback(rule, version, index, config, sources.get(rule.id, ()))
            )
    return tuple(resolved)


def _applies(rule, version: str) -> bool:
    return rule.enabled and (rule.versions is None or matches(rule.versions, version))


def _cross_product(
    rule: CrossProductRule, version: str, index: TreeIndex, config: SiteConfig
) -> list[ResolvedRedirect]:
    if not _applies(rule, version):
        return []

    keys = [key for key, _ in rule.values]
    combos = product(*(options for _, options in rule.values))
    resolved = []
    for combo in combos:
        mapping = dict(zip(keys, combo, strict=True), version=version)
        at = _fill(rule.at, mapping)
        outcome = _place(index, at, _fill(rule.to, mapping))
        if outcome is None:
            continue
        urlpath, fragment = outcome
        fields = _page_fields(rule.fields, config)
        if fields["body"]:
            fields["body"] = _fill(fields["body"], mapping)
        canonical = (
            _fill(rule.canonical, {**mapping, "site_url": config.layout.base_url})
            if rule.canonical
            else None
        )
        resolved.append(
            ResolvedRedirect(
                rule_id=rule.id,
                path=at,
                to=_relative_target(at, urlpath, fragment),
                canonical=canonical,
                relative=True,
                **fields,
            )
        )
    return resolved


def _tree_rename(
    rule: TreeRenameRule, version: str, index: TreeIndex, config: SiteConfig
) -> list[ResolvedRedirect]:
    if not _applies(rule, version):
        return []

    mapping = {"version": version}
    from_root = _fill(rule.from_path, mapping)
    to_root = _fill(rule.to_path, mapping)
    fields = _page_fields(rule.fields, config)

    resolved = []
    for page in sorted(index.pages):
        if not page.startswith(f"{to_root}/"):
            continue
        at = f"{from_root}/{page[len(to_root) + 1 :]}"
        outcome = _place(index, at, f"/{_url_of(page)}")
        if outcome is None:
            continue
        urlpath, fragment = outcome
        # The renamed page's evergreen URL, matching the canonical the page itself carries.
        prefix = f"{version}/"
        canonical = (
            f"{config.layout.base_url}/{ALIAS}/{urlpath[len(prefix) :]}"
            if urlpath.startswith(prefix)
            else f"{config.layout.base_url}/{urlpath}"
        )
        resolved.append(
            ResolvedRedirect(
                rule_id=rule.id,
                path=at,
                to=_relative_target(at, urlpath, fragment),
                canonical=canonical,
                relative=True,
                **fields,
            )
        )
    return resolved


def _section_fallback(
    rule: SectionFallbackRule,
    version: str,
    index: TreeIndex,
    config: SiteConfig,
    sources: Iterable[str],
) -> list[ResolvedRedirect]:
    if not _applies(rule, version):
        return []

    mapping = {"version": version}
    dir_root = _fill(rule.dir, mapping)
    raw_target = f"/{_fill(rule.to, mapping)}"
    fields = _page_fields(rule.fields, config)

    resolved = []
    for source in sorted(sources):
        at = f"{dir_root}/{source}"
        outcome = _place(index, at, raw_target)
        if outcome is None:
            continue
        urlpath, fragment = outcome
        resolved.append(
            ResolvedRedirect(
                rule_id=rule.id,
                path=at,
                to=_relative_target(at, urlpath, fragment),
                # Version-pinned: the target has no counterpart under `latest` — that absence
                # is why the rule exists.
                canonical=f"{config.layout.base_url}/{urlpath}",
                relative=True,
                **fields,
            )
        )
    return resolved


def section_sources(tree: Path, config: SiteConfig, version: str) -> dict[str, frozenset[str]]:
    """Each section-fallback rule's donor URLs for `version`: dir-relative page paths.

    Donors are the version folders outside the rule's gate — the ones that have the section —
    and only their real pages donate: a stub is a page no reader can be on, so it needs no
    fallback.
    """
    out: dict[str, frozenset[str]] = {}
    for rule in config.expand_rules:
        if not isinstance(rule, SectionFallbackRule) or not _applies(rule, version):
            continue
        paths: set[str] = set()
        for donor in version_folders(tree):
            if donor == version or _applies(rule, donor):
                continue
            section = _fill(rule.dir, {"version": donor})
            donor_index = scan_tree(tree, (section,))
            paths.update(
                page[len(section) + 1 :]
                for page in donor_index.pages - set(donor_index.stub_targets)
            )
        out[rule.id] = frozenset(paths)
    return out


def _place(index: TreeIndex, at: str, raw_target: str) -> tuple[str, str] | None:
    """Where a stub at `at` should point, after the three filters, or None for no stub.

    `raw_target` is relative to the stub's own directory (or tree-absolute with a leading
    slash); the result is the collapsed tree-relative URL path plus fragment.
    """
    # F1: never shadow a page this tool did not generate.
    if at in index.pages and at not in index.stub_targets:
        return None
    target = _resolve_raw_target(at, raw_target)
    if target is None:
        return None
    # F3 before F2, so a target that is a redirect is judged by where it finally lands.
    urlpath, fragment = _split_fragment(collapse(index, target))
    if not _exists(index, urlpath) or _served_file(urlpath) == at:
        return None
    return urlpath, fragment


def expand_candidate_paths(config: SiteConfig, version: str) -> dict[str, str]:
    """Every path a cross-product rule could claim for `version`, as `{path: rule id}`.

    The tree filters decide which candidates become stubs, but a collision with a `files` rule
    is knowable from the configuration alone, so `redirects check` catches it without a tree.
    """
    candidates: dict[str, str] = {}
    for rule in config.expand_rules:
        if not isinstance(rule, CrossProductRule) or not _applies(rule, version):
            continue
        keys = [key for key, _ in rule.values]
        for combo in product(*(options for _, options in rule.values)):
            mapping = dict(zip(keys, combo, strict=True), version=version)
            candidates[_fill(rule.at, mapping)] = rule.id
    return candidates


def mirror_rule(config: SiteConfig) -> UnversionedMirrorRule | None:
    for rule in config.expand_rules:
        if isinstance(rule, UnversionedMirrorRule) and rule.enabled:
            return rule
    return None


def expand_mirror(
    config: SiteConfig, latest: str, index: TreeIndex
) -> tuple[ResolvedRedirect, ...]:
    """One stub per page of the newest version's mirrored sections, at its unversioned path."""
    rule = mirror_rule(config)
    if rule is None:
        return ()
    fields = _page_fields(rule.fields, config)
    prefix = f"{latest}/"

    resolved = []
    for page in sorted(index.pages):
        urlpath, fragment = _split_fragment(collapse(index, _url_of(page)))
        if not urlpath.startswith(prefix) or not _exists(index, urlpath):
            continue
        evergreen = f"{ALIAS}/{urlpath[len(prefix) :]}"
        suffix = f"#{fragment}" if fragment else ""
        resolved.append(
            ResolvedRedirect(
                rule_id=rule.id,
                path=page[len(prefix) :],
                to=f"/{evergreen}{suffix}",
                canonical=f"{config.layout.base_url}/{evergreen}",
                relative=False,
                **fields,
            )
        )
    return tuple(resolved)


def alias_entries(config: SiteConfig) -> tuple[tuple[VersionAliasRule, str, str], ...]:
    """Every `(rule, folder, minor)` the version-alias rules declare."""
    entries = []
    for rule in config.expand_rules:
        if isinstance(rule, VersionAliasRule) and rule.enabled:
            entries.extend((rule, folder, minor_of(folder)) for folder in rule.folders)
    return tuple(entries)


def expand_alias(
    config: SiteConfig, rule: VersionAliasRule, folder: str, minor: str, index: TreeIndex
) -> tuple[ResolvedRedirect, ...]:
    """One stub per page of `minor`, inside `folder`, pointing at the minor's copy.

    Targets are absolute and version-pinned: the folder is not behind the `latest` symlink, and
    the reader asked for a specific old version. The canonical names the target itself — the
    page the alias URL may not exist under `latest`.
    """
    fields = _page_fields(rule.fields, config)
    prefix = f"{minor}/"

    resolved = []
    for page in sorted(index.pages):
        if not page.startswith(prefix):
            continue
        urlpath, fragment = _split_fragment(collapse(index, _url_of(page)))
        if not urlpath.startswith(prefix) or not _exists(index, urlpath):
            continue
        suffix = f"#{fragment}" if fragment else ""
        resolved.append(
            ResolvedRedirect(
                rule_id=rule.id,
                path=f"{folder}/{page[len(prefix) :]}",
                to=f"/{urlpath}{suffix}",
                canonical=f"{config.layout.base_url}/{urlpath}",
                relative=False,
                **fields,
            )
        )
    return tuple(resolved)


# -- orchestration over a real tree ----------------------------------------------------------


def version_redirects(tree: Path, config: SiteConfig, version: str) -> tuple[ResolvedRedirect, ...]:
    """Everything to install inside one version folder: the `files` rules plus the expansions.

    The expansions collapse through the `files` stubs of the same resolution, so a rule whose
    target is about to become a redirect points past it. Two rules claiming one path is an
    error: which one wins would otherwise depend on write order.
    """
    files = resolve_file_redirects(config, version)
    index = with_stubs(scan_tree(tree, (version,)), files)
    expanded = expand_for_version(
        config, version, index, fallback_sources=section_sources(tree, config, version)
    )

    owners: dict[str, str] = {}
    for redirect in (*files, *expanded):
        other = owners.setdefault(redirect.path, redirect.rule_id)
        if other != redirect.rule_id:
            raise RedirectError(
                f"rules {other!r} and {redirect.rule_id!r} both generate {redirect.path}"
            )
    return (*files, *expanded)


def mirror_redirects(
    tree: Path, config: SiteConfig, *, latest: str
) -> tuple[ResolvedRedirect, ...]:
    """The unversioned mirror of `latest`, scanned from its section folders.

    An empty scan is an error, not a silent skip: it would quietly reinstate the 404s the
    mirror exists to prevent.
    """
    rule = mirror_rule(config)
    if rule is None:
        return ()
    sections = getattr(config.layout, rule.for_each)
    index = scan_tree(tree, tuple(f"{latest}/{section}" for section in sections))
    if not index.pages:
        raise RedirectError(
            f"no pages found under {latest}/{{{','.join(sections)}}}, so the unversioned "
            "mirror would be empty. Check that the version folder is built and that "
            f"layout.{rule.for_each} names its sections."
        )
    return expand_mirror(config, latest, index)


def alias_redirects(
    tree: Path, config: SiteConfig, *, minors: set[str] | None = None
) -> list[tuple[str, tuple[ResolvedRedirect, ...]]]:
    """`(folder, stubs)` for every alias folder whose minor exists in the tree.

    A folder whose minor is not published is skipped rather than failed: the alias mirrors what
    the tree serves, and a partial tree — a test fixture, a first deployment — serves less.
    """
    folders = []
    for rule, folder, minor in alias_entries(config):
        if minors is not None and minor not in minors:
            continue
        if not (tree / minor).is_dir():
            continue
        index = scan_tree(tree, (minor,))
        folders.append((folder, expand_alias(config, rule, folder, minor, index)))
    return folders


def wipe_owned(path: Path) -> bool:
    """Delete a directory this tool owns outright. Returns whether anything was removed.

    Refuses if any file inside was not generated by ovweb: the wholly-owned scopes — the root
    section mirrors and the alias folders — must never hold content, so finding some means the
    wipe would destroy something a publish cannot regenerate.
    """
    if not path.is_dir():
        return False
    for file in sorted(path.rglob("*")):
        if file.is_dir():
            continue
        if not is_generated_redirect(file):
            raise RedirectError(
                f"{file} was not generated by ovweb, so {path.name}/ holds content this tool "
                "does not own and must not delete. Remove it by hand, or take the folder out "
                "of the redirect rules."
            )
    return fsops.remove(path)
