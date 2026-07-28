"""Version arithmetic: parsing X.Y names, matching specifiers, reading versions.json.

Pure. The one deliberate dependency is `packaging`, which mkdocs already installs.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version

#: Documentation versions are grouped by minor release and named X.Y. Anything else is
#: either a legacy exact-patch folder (only ever read, never published) or a mistake.
MINOR_VERSION = re.compile(r"^\d+\.\d+$")


class VersionError(Exception):
    """A version name or specifier is not usable."""


@dataclass(frozen=True)
class VersionEntry:
    """One entry of mike's versions.json."""

    version: str
    title: str
    aliases: tuple[str, ...]


def validate_minor(version: str) -> str:
    """Return `version` if it is a publishable `X.Y` name, else raise."""
    if not MINOR_VERSION.match(version):
        raise VersionError(
            f"{version!r} is not a minor version name. Documentation versions are grouped "
            "by minor release and named X.Y (for example 3.8) — patch releases update their "
            "minor's version in place rather than creating a new one."
        )
    return version


def parse(version: str) -> Version:
    """Parse any published version name, including legacy ones like `3.0.0-beta1`."""
    try:
        return Version(version)
    except InvalidVersion as error:
        raise VersionError(f"cannot parse version {version!r}: {error}") from error


def matches(specifier: str, version: str) -> bool:
    """Whether `version` satisfies `specifier` (a PEP 440 specifier set, e.g. `"<3.4"`).

    `prereleases=True` is not optional: legacy version folders such as `3.0.0-beta1`
    normalise to `3.0.0b1`, and a specifier set excludes pre-releases by default, so
    `"<3.4"` would silently fail to match them.
    """
    try:
        parsed = SpecifierSet(specifier, prereleases=True)
    except InvalidSpecifier as error:
        raise VersionError(f"invalid version specifier {specifier!r}: {error}") from error
    return parsed.contains(parse(version))


def sort_descending(versions: list[str]) -> list[str]:
    """Newest first, by version order rather than string order (so 3.10 > 3.9)."""
    return sorted(versions, key=parse, reverse=True)


def read_versions_json(text: str) -> tuple[VersionEntry, ...]:
    """Parse mike's versions.json.

    The bash implementation scraped this with `grep -oE '"version"…' | sed` to avoid a jq
    dependency; here it is simply JSON.
    """
    try:
        raw = json.loads(text)
    except json.JSONDecodeError as error:
        raise VersionError(f"versions.json is not valid JSON: {error}") from error
    if not isinstance(raw, list):
        raise VersionError("versions.json must hold a list of version entries")

    entries = []
    for item in raw:
        if not isinstance(item, dict) or "version" not in item:
            raise VersionError(f"malformed versions.json entry: {item!r}")
        entries.append(
            VersionEntry(
                version=str(item["version"]),
                title=str(item.get("title", item["version"])),
                aliases=tuple(str(alias) for alias in item.get("aliases", ())),
            )
        )
    return tuple(entries)


def alias_target(entries: tuple[VersionEntry, ...], alias: str) -> str | None:
    """The version an alias points at according to versions.json, if any."""
    for entry in entries:
        if alias in entry.aliases:
            return entry.version
    return None
