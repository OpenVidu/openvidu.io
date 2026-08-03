"""Load and validate ovweb.yaml into a :class:`~ovweb.model.SiteConfig`.

Pure apart from the single file read in :func:`load_site_config`, and deliberately light on
imports — only stdlib plus PyYAML. The MkDocs hook (publish-tool/mkdocs_hook.py) goes
through this module during a site build, where typer and Jinja2 are not necessarily
installed.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from .model import (
    VERSION_ROOT,
    MirrorRule,
    PatternRule,
    RedirectDefaults,
    RedirectOverride,
    RedirectRule,
    SiteConfig,
    SiteLayout,
)

#: Environment variable holding an absolute path to the config to use. `ovweb` sets it when
#: it invokes mike, so the site build and the post-processing can never disagree about the
#: layout — even though the build reads the file from the working tree and the
#: post-processing reads it from the installed package.
CONFIG_ENV_VAR = "OVWEB_SITE_CONFIG"

SCHEMA_VERSION = 1

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

    In order: an explicit path, then ``$OVWEB_SITE_CONFIG``, then the copy inside the
    installed package, then the copy next to this source tree (an uninstalled checkout).
    """
    candidates: list[Path] = []

    if explicit is not None:
        path = Path(explicit).expanduser()
        if not path.is_file():
            raise ConfigError(f"config not found: {path}")
        return path

    from_env = os.environ.get(CONFIG_ENV_VAR)
    if from_env:
        path = Path(from_env).expanduser()
        if not path.is_file():
            raise ConfigError(f"{CONFIG_ENV_VAR} points at a missing file: {path}")
        return path

    # Installed package: ovweb.yaml is force-included as ovweb/data/ovweb.yaml.
    candidates.append(Path(__file__).resolve().parent / "data" / "ovweb.yaml")
    # Uninstalled checkout: src/ovweb/config.py -> publish-tool/ovweb.yaml.
    candidates.append(Path(__file__).resolve().parents[2] / "ovweb.yaml")

    for candidate in candidates:
        if candidate.is_file():
            return candidate

    raise ConfigError(
        "could not locate ovweb.yaml. Looked at "
        + ", ".join(str(c) for c in candidates)
        + f". Set {CONFIG_ENV_VAR} to point at it explicitly."
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

    unknown_redirects = set(redirects) - {"defaults", "files", "patterns", "mirror"}
    if unknown_redirects:
        raise ConfigError(
            f"{source}: unknown 'redirects' keys: {', '.join(sorted(unknown_redirects))}"
        )

    defaults = _parse_defaults(redirects.get("defaults") or {}, source=source)
    mirror = _parse_mirror(redirects.get("mirror"), source=source, layout=layout)
    file_rules = tuple(
        _parse_file_rule(entry, source=source, index=index)
        for index, entry in enumerate(redirects.get("files") or [])
    )
    pattern_rules = tuple(
        _parse_pattern_rule(entry, source=source, index=index, layout=layout)
        for index, entry in enumerate(redirects.get("patterns") or [])
    )

    _check_unique_ids([rule.id for rule in file_rules], what="redirects.files", source=source)
    _check_unique_ids([rule.id for rule in pattern_rules], what="redirects.patterns", source=source)

    return SiteConfig(
        layout=layout,
        defaults=defaults,
        file_rules=file_rules,
        pattern_rules=pattern_rules,
        mirror=mirror,
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


def _parse_mirror(raw: Any, *, source: str, layout: SiteLayout) -> MirrorRule | None:
    if raw is None:
        return None
    where = f"{source}: redirects.mirror"
    if not isinstance(raw, dict):
        raise ConfigError(f"{where} must be a mapping")
    unknown = set(raw) - {"for_each", "body", "enabled", "description"}
    if unknown:
        raise ConfigError(f"{where} has unknown keys: {', '.join(sorted(unknown))}")

    for_each = raw.get("for_each")
    if not isinstance(for_each, str) or not hasattr(layout, for_each):
        raise ConfigError(f"{where}: for_each must name a layout list, got {for_each!r}")
    if not isinstance(raw.get("body"), str) or not raw["body"]:
        raise ConfigError(f"{where} needs a non-empty string 'body'")

    return MirrorRule(
        for_each=for_each,
        body=raw["body"],
        enabled=bool(raw.get("enabled", True)),
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


def _parse_pattern_rule(raw: Any, *, source: str, index: int, layout: SiteLayout) -> PatternRule:
    where = f"{source}: redirects.patterns[{index}]"
    if not isinstance(raw, dict):
        raise ConfigError(f"{where} must be a mapping")
    unknown = set(raw) - {"id", "match", "to", "for_each", "description"}
    if unknown:
        raise ConfigError(f"{where} has unknown keys: {', '.join(sorted(unknown))}")
    for key in ("id", "match", "to"):
        if not isinstance(raw.get(key), str) or not raw[key]:
            raise ConfigError(f"{where} needs a non-empty string '{key}'")

    for_each = raw.get("for_each")
    if for_each is not None and not hasattr(layout, str(for_each)):
        raise ConfigError(f"{where}: for_each must name a layout list, got {for_each!r}")

    return PatternRule(
        id=raw["id"],
        match=raw["match"],
        to=raw["to"],
        for_each=for_each,
        description=(raw.get("description") or "").strip(),
    )


def _check_unique_ids(ids: list[str], *, what: str, source: str) -> None:
    duplicates = sorted({name for name in ids if ids.count(name) > 1})
    if duplicates:
        raise ConfigError(f"{source}: duplicate {what} ids: {', '.join(duplicates)}")
