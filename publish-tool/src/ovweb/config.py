"""Load and validate ovweb.yaml into a :class:`~ovweb.model.SiteConfig`.

Pure apart from the single file read in :func:`load_site_config`.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from .model import (
    VERSION_ROOT,
    CrossProductRule,
    ExpandFields,
    RedirectDefaults,
    RedirectOverride,
    RedirectRule,
    SiteConfig,
    SiteLayout,
    TreeRenameRule,
    UnversionedMirrorRule,
    VersionAliasRule,
)
from .versions import MINOR_VERSION, VersionError, minor_of

SCHEMA_VERSION = 2

_REQUIRED_LAYOUT_KEYS = (
    "site_url",
    "versioned_pages",
    "non_versioned_pages",
    "assets",
    "pinned_assets",
    "root_files",
    "feeds",
)


class ConfigError(Exception):
    """ovweb.yaml is missing, unreadable or invalid."""


def find_site_config(explicit: Path | str | None = None) -> Path:
    """Locate ovweb.yaml.

    In order: an explicit path, then the copy inside the installed package, then the copy next
    to this source tree (an uninstalled checkout).
    """
    candidates: list[Path] = []

    if explicit is not None:
        path = Path(explicit).expanduser()
        if not path.is_file():
            raise ConfigError(f"config not found: {path}")
        return path

    # Installed package: pyproject force-includes ovweb.yaml as ovweb/data/ovweb.yaml.
    candidates.append(Path(__file__).resolve().parent / "data" / "ovweb.yaml")
    # Uninstalled checkout: src/ovweb/config.py -> publish-tool/ovweb.yaml.
    candidates.append(Path(__file__).resolve().parents[2] / "ovweb.yaml")

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    raise ConfigError(
        "could not locate ovweb.yaml. Looked at "
        + ", ".join(str(c) for c in candidates)
        + ". Pass --layout to point at it explicitly."
    )


def load_site_config(explicit: Path | str | None = None) -> SiteConfig:
    """Read, validate and freeze ovweb.yaml."""
    path = find_site_config(explicit)
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise ConfigError(f"cannot read {path}: {error}") from error
    return parse_site_config(raw, source=str(path))


def parse_site_config(raw: Any, *, source: str = "<memory>") -> SiteConfig:
    """Validate an already-parsed ovweb.yaml mapping. Pure."""
    if not isinstance(raw, dict):
        raise ConfigError(f"{source}: top level must be a mapping")

    schema = raw.get("schema")
    if schema != SCHEMA_VERSION:
        raise ConfigError(
            f"{source}: unsupported schema {schema!r}, this ovweb understands {SCHEMA_VERSION}"
        )

    layout = _parse_layout(raw.get("layout"), source=source)
    redirects = raw.get("redirects") or {}
    if not isinstance(redirects, dict):
        raise ConfigError(f"{source}: 'redirects' must be a mapping")

    for retired, replacement in (
        ("patterns", "an `expand` rule — the 404 router is gone"),
        ("mirror", "an `expand` rule of kind `unversioned-mirror`"),
    ):
        if retired in redirects:
            raise ConfigError(
                f"{source}: 'redirects.{retired}' no longer exists; use {replacement}"
            )
    unknown_redirects = set(redirects) - {"defaults", "files", "expand"}
    if unknown_redirects:
        raise ConfigError(
            f"{source}: unknown 'redirects' keys: {', '.join(sorted(unknown_redirects))}"
        )

    defaults = _parse_defaults(redirects.get("defaults") or {}, source=source)
    file_rules = tuple(
        _parse_file_rule(entry, source=source, index=index)
        for index, entry in enumerate(redirects.get("files") or [])
    )
    expand_rules = tuple(
        _parse_expand_rule(entry, source=source, index=index, layout=layout)
        for index, entry in enumerate(redirects.get("expand") or [])
    )
    _validate_expand_rules(expand_rules, source=source)

    _check_unique_ids(
        [rule.id for rule in (*file_rules, *expand_rules)], what="redirect", source=source
    )

    return SiteConfig(
        layout=layout,
        defaults=defaults,
        file_rules=file_rules,
        expand_rules=expand_rules,
        source=source,
    )


def _parse_layout(raw: Any, *, source: str) -> SiteLayout:
    if not isinstance(raw, dict):
        raise ConfigError(f"{source}: 'layout' must be a mapping")

    missing = [key for key in _REQUIRED_LAYOUT_KEYS if key not in raw]
    if missing:
        raise ConfigError(f"{source}: layout is missing {', '.join(missing)}")

    site_url = raw["site_url"]
    if not isinstance(site_url, str) or not site_url.startswith(("http://", "https://")):
        raise ConfigError(f"{source}: layout.site_url must be an absolute URL")

    def names(key: str) -> tuple[str, ...]:
        value = raw[key]
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ConfigError(f"{source}: layout.{key} must be a list of strings")
        for item in value:
            if not item or item.startswith("/") or item.endswith("/"):
                raise ConfigError(
                    f"{source}: layout.{key} entry {item!r} must be a bare name "
                    "without leading or trailing slashes"
                )
        return tuple(value)

    layout = SiteLayout(
        site_url=site_url,
        versioned_pages=names("versioned_pages"),
        non_versioned_pages=names("non_versioned_pages"),
        assets=names("assets"),
        pinned_assets=names("pinned_assets"),
        root_files=names("root_files"),
        feeds=names("feeds"),
    )

    overlap = set(layout.versioned_pages) & set(layout.non_versioned_pages)
    if overlap:
        raise ConfigError(
            f"{source}: {', '.join(sorted(overlap))} listed as both versioned and non-versioned"
        )

    unknown_pinned = set(layout.pinned_assets) - set(layout.assets)
    if unknown_pinned:
        raise ConfigError(
            f"{source}: layout.pinned_assets entries not present in layout.assets: "
            f"{', '.join(sorted(unknown_pinned))}"
        )

    unknown_feeds = set(layout.feeds) - set(layout.root_files)
    if unknown_feeds:
        raise ConfigError(
            f"{source}: layout.feeds entries not present in layout.root_files: "
            f"{', '.join(sorted(unknown_feeds))}"
        )

    if "index.html" not in layout.root_files:
        raise ConfigError(f"{source}: layout.root_files must include index.html")

    return layout


def _parse_defaults(raw: Any, *, source: str) -> RedirectDefaults:
    if not isinstance(raw, dict):
        raise ConfigError(f"{source}: redirects.defaults must be a mapping")
    fallback = RedirectDefaults()
    unknown = set(raw) - {
        "lang",
        "title",
        "body",
        "robots",
        "relative",
        "preserve_query_and_hash",
    }
    if unknown:
        raise ConfigError(
            f"{source}: unknown redirects.defaults keys: {', '.join(sorted(unknown))}"
        )
    return RedirectDefaults(
        lang=raw.get("lang", fallback.lang),
        title=raw.get("title", fallback.title),
        body=raw.get("body", fallback.body),
        robots=raw.get("robots", fallback.robots),
        relative=bool(raw.get("relative", fallback.relative)),
        preserve_query_and_hash=bool(
            raw.get("preserve_query_and_hash", fallback.preserve_query_and_hash)
        ),
    )


#: Keys every expansion rule accepts, whatever its kind.
_EXPAND_COMMON_KEYS = {
    "id",
    "kind",
    "title",
    "body",
    "robots",
    "lang",
    "preserve_query_and_hash",
    "enabled",
    "versions",
    "description",
}

_EXPAND_KIND_KEYS = {
    "cross-product": {"at", "to", "canonical", "values"},
    "tree-rename": {"from", "to"},
    "version-alias": {"folders"},
    "unversioned-mirror": {"for_each"},
}

#: A cross-product value lands in a path and a URL; a slug is the only shape that is safe in
#: both without escaping.
_VALUE_SLUG = re.compile(r"^[A-Za-z0-9._-]+$")


def _parse_expand_rule(raw: Any, *, source: str, index: int, layout: SiteLayout):
    where = f"{source}: redirects.expand[{index}]"
    if not isinstance(raw, dict):
        raise ConfigError(f"{where} must be a mapping")

    kind = raw.get("kind")
    if kind not in _EXPAND_KIND_KEYS:
        raise ConfigError(
            f"{where}: 'kind' must be one of {', '.join(sorted(_EXPAND_KIND_KEYS))}, got {kind!r}"
        )
    if not isinstance(raw.get("id"), str) or not raw["id"]:
        raise ConfigError(f"{where} needs a non-empty string 'id'")
    where = f"{source}: redirects.expand[{raw['id']}]"

    unknown = set(raw) - _EXPAND_COMMON_KEYS - _EXPAND_KIND_KEYS[kind]
    if unknown:
        raise ConfigError(f"{where} has unknown keys: {', '.join(sorted(unknown))}")

    common = {
        "id": raw["id"],
        "fields": ExpandFields(
            title=raw.get("title"),
            body=raw.get("body"),
            robots=raw.get("robots"),
            lang=raw.get("lang"),
            preserve_query_and_hash=raw.get("preserve_query_and_hash"),
        ),
        "enabled": bool(raw.get("enabled", True)),
        "description": (raw.get("description") or "").strip(),
    }
    gated = {**common, "versions": raw.get("versions")}

    if kind == "cross-product":
        return _parse_cross_product(raw, where=where, common=gated)
    if kind == "tree-rename":
        return _parse_tree_rename(raw, where=where, common=gated)
    if kind == "version-alias":
        if raw.get("versions") is not None:
            raise ConfigError(f"{where}: a version-alias names its folders; drop 'versions'")
        return _parse_version_alias(raw, where=where, common=common)
    if raw.get("versions") is not None:
        raise ConfigError(f"{where}: the mirror always follows `latest`; drop 'versions'")
    return _parse_unversioned_mirror(raw, where=where, common=common, layout=layout)


def _placeholders(template: str) -> set[str]:
    return set(re.findall(r"\{(\w+)\}", template))


def _parse_cross_product(raw: dict, *, where: str, common: dict) -> CrossProductRule:
    for key in ("at", "to"):
        if not isinstance(raw.get(key), str) or not raw[key]:
            raise ConfigError(f"{where} needs a non-empty string '{key}'")
    at, to = raw["at"], raw["to"]
    if not at.startswith("{version}/"):
        raise ConfigError(f"{where}: 'at' must start with '{{version}}/', got {at!r}")
    if not at.endswith(".html"):
        raise ConfigError(f"{where}: 'at' must name an HTML file, got {at!r}")
    if to.startswith("/"):
        raise ConfigError(
            f"{where}: 'to' must be relative — the stub lives inside a version folder that "
            "`latest` also serves"
        )

    values = raw.get("values")
    if not isinstance(values, dict) or not values:
        raise ConfigError(f"{where} needs a non-empty 'values' mapping")
    parsed_values = []
    for key, options in values.items():
        if not isinstance(options, list) or not options:
            raise ConfigError(f"{where}: values.{key} must be a non-empty list")
        for option in options:
            if not isinstance(option, str) or not _VALUE_SLUG.match(option):
                raise ConfigError(f"{where}: values.{key} entry {option!r} is not a plain slug")
        if key not in _placeholders(at):
            raise ConfigError(
                f"{where}: values key {key!r} does not appear in 'at', so every combination "
                "would generate the same page"
            )
        parsed_values.append((key, tuple(options)))

    allowed = set(values) | {"version"}
    for name, template in (("at", at), ("to", to), ("body", raw.get("body") or "")):
        unknown = _placeholders(template) - allowed
        if unknown:
            raise ConfigError(
                f"{where}: '{name}' uses undeclared placeholder(s) {', '.join(sorted(unknown))}"
            )
    unknown = _placeholders(raw.get("canonical") or "") - allowed - {"site_url"}
    if unknown:
        raise ConfigError(
            f"{where}: 'canonical' uses undeclared placeholder(s) {', '.join(sorted(unknown))}"
        )

    return CrossProductRule(
        at=at, to=to, canonical=raw.get("canonical"), values=tuple(parsed_values), **common
    )


def _parse_tree_rename(raw: dict, *, where: str, common: dict) -> TreeRenameRule:
    for key in ("from", "to"):
        if not isinstance(raw.get(key), str) or not raw[key]:
            raise ConfigError(f"{where} needs a non-empty string '{key}'")
        if not raw[key].startswith("{version}/"):
            raise ConfigError(f"{where}: '{key}' must start with '{{version}}/', got {raw[key]!r}")
    from_path = raw["from"].rstrip("/")
    to_path = raw["to"].rstrip("/")
    if from_path == to_path:
        raise ConfigError(f"{where}: 'from' and 'to' are the same directory")
    if from_path.startswith(f"{to_path}/") or to_path.startswith(f"{from_path}/"):
        raise ConfigError(f"{where}: 'from' and 'to' must not nest inside each other")
    return TreeRenameRule(from_path=from_path, to_path=to_path, **common)


def _parse_version_alias(raw: dict, *, where: str, common: dict) -> VersionAliasRule:
    folders = raw.get("folders")
    if not isinstance(folders, list) or not folders:
        raise ConfigError(f"{where} needs a non-empty 'folders' list")
    for folder in folders:
        if not isinstance(folder, str) or "/" in folder:
            raise ConfigError(f"{where}: folder {folder!r} must be a bare directory name")
        if MINOR_VERSION.match(folder):
            raise ConfigError(
                f"{where}: {folder!r} is a minor version name, which is a published folder, "
                "not an alias"
            )
        try:
            minor_of(folder)
        except VersionError as error:
            raise ConfigError(f"{where}: {error}") from error
    duplicates = sorted({f for f in folders if folders.count(f) > 1})
    if duplicates:
        raise ConfigError(f"{where}: duplicate folders: {', '.join(duplicates)}")
    return VersionAliasRule(folders=tuple(folders), **common)


def _parse_unversioned_mirror(
    raw: dict, *, where: str, common: dict, layout: SiteLayout
) -> UnversionedMirrorRule:
    for_each = raw.get("for_each")
    if not isinstance(for_each, str) or not hasattr(layout, for_each):
        raise ConfigError(f"{where}: for_each must name a layout list, got {for_each!r}")
    return UnversionedMirrorRule(for_each=for_each, **common)


def _validate_expand_rules(rules: tuple, *, source: str) -> None:
    mirrors = [rule.id for rule in rules if isinstance(rule, UnversionedMirrorRule)]
    if len(mirrors) > 1:
        raise ConfigError(
            f"{source}: only one unversioned-mirror rule may exist, found: {', '.join(mirrors)}"
        )
    folders: dict[str, str] = {}
    for rule in rules:
        if isinstance(rule, VersionAliasRule):
            for folder in rule.folders:
                other = folders.setdefault(folder, rule.id)
                if other != rule.id:
                    raise ConfigError(
                        f"{source}: folder {folder!r} is claimed by both {other!r} and {rule.id!r}"
                    )


_FILE_RULE_KEYS = {
    "id",
    "at",
    "to",
    "canonical",
    "title",
    "body",
    "robots",
    "lang",
    "relative",
    "preserve_query_and_hash",
    "enabled",
    "versions",
    "when",
    "description",
}

_OVERRIDE_KEYS = (_FILE_RULE_KEYS - {"id", "at", "when", "description"}) | {"versions"}


def _parse_file_rule(raw: Any, *, source: str, index: int) -> RedirectRule:
    where = f"{source}: redirects.files[{index}]"
    if not isinstance(raw, dict):
        raise ConfigError(f"{where} must be a mapping")

    unknown = set(raw) - _FILE_RULE_KEYS
    if unknown:
        raise ConfigError(f"{where} has unknown keys: {', '.join(sorted(unknown))}")

    for key in ("id", "at", "to"):
        if not isinstance(raw.get(key), str) or not raw[key]:
            raise ConfigError(f"{where} needs a non-empty string '{key}'")

    at = raw["at"]
    if at != VERSION_ROOT:
        if at.startswith("/"):
            raise ConfigError(f"{where}: 'at' must be relative to the site root, got {at!r}")
        if not at.endswith(".html"):
            raise ConfigError(f"{where}: 'at' must name an HTML file, got {at!r}")

    overrides = tuple(
        _parse_override(entry, source=source, rule=raw["id"], index=position)
        for position, entry in enumerate(raw.get("when") or [])
    )

    return RedirectRule(
        id=raw["id"],
        at=at,
        to=raw["to"],
        canonical=raw.get("canonical"),
        title=raw.get("title"),
        body=raw.get("body"),
        robots=raw.get("robots"),
        lang=raw.get("lang"),
        relative=raw.get("relative"),
        preserve_query_and_hash=raw.get("preserve_query_and_hash"),
        enabled=bool(raw.get("enabled", True)),
        versions=raw.get("versions"),
        when=overrides,
        description=(raw.get("description") or "").strip(),
    )


def _parse_override(raw: Any, *, source: str, rule: str, index: int) -> RedirectOverride:
    where = f"{source}: redirects.files[{rule}].when[{index}]"
    if not isinstance(raw, dict):
        raise ConfigError(f"{where} must be a mapping")
    unknown = set(raw) - _OVERRIDE_KEYS
    if unknown:
        raise ConfigError(f"{where} has unknown keys: {', '.join(sorted(unknown))}")
    if not isinstance(raw.get("versions"), str) or not raw["versions"]:
        raise ConfigError(f"{where} needs a non-empty 'versions' specifier")
    return RedirectOverride(
        versions=raw["versions"],
        to=raw.get("to"),
        canonical=raw.get("canonical"),
        title=raw.get("title"),
        body=raw.get("body"),
        robots=raw.get("robots"),
        lang=raw.get("lang"),
        relative=raw.get("relative"),
        preserve_query_and_hash=raw.get("preserve_query_and_hash"),
        enabled=raw.get("enabled"),
    )


def _check_unique_ids(ids: list[str], *, what: str, source: str) -> None:
    duplicates = sorted({name for name in ids if ids.count(name) > 1})
    if duplicates:
        raise ConfigError(f"{source}: duplicate {what} ids: {', '.join(duplicates)}")
