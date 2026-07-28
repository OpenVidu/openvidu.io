"""Version parsing, ordering and specifier matching."""

from __future__ import annotations

import json

import pytest

from ovweb.versions import (
    VersionError,
    alias_target,
    matches,
    read_versions_json,
    sort_descending,
    validate_minor,
)


@pytest.mark.parametrize("name", ["3.0", "3.8", "3.10", "10.0"])
def test_accepts_minor_names(name):
    assert validate_minor(name) == name


@pytest.mark.parametrize("name", ["3", "3.8.1", "3.0.0-beta1", "v3.8", "latest", "3.8/"])
def test_rejects_anything_that_is_not_a_minor_name(name):
    with pytest.raises(VersionError, match="minor version"):
        validate_minor(name)


def test_orders_by_version_not_by_string():
    """ "3.10" sorts before "3.4" as a string, which would put the wrong version first."""
    assert sort_descending(["3.4", "3.10", "3.9", "3.2"]) == ["3.10", "3.9", "3.4", "3.2"]


@pytest.mark.parametrize(
    ("specifier", "version", "expected"),
    [
        ("<3.4", "3.0", True),
        ("<3.4", "3.3", True),
        ("<3.4", "3.4", False),
        ("<3.4", "3.8", False),
        ("<3.4", "3.10", False),
        (">=3.4", "3.4", True),
        (">=3.4,<3.9", "3.8", True),
        (">=3.4,<3.9", "3.9", False),
    ],
)
def test_specifier_matching(specifier, version, expected):
    assert matches(specifier, version) is expected


@pytest.mark.parametrize("version", ["3.0.0-beta1", "3.0.0b1", "3.0.0-rc1"])
def test_prereleases_are_matched(version):
    """A specifier set excludes pre-releases by default, so the legacy folders would miss the
    band that was written for them."""
    assert matches("<3.4", version) is True


def test_an_invalid_specifier_is_reported_clearly():
    with pytest.raises(VersionError, match="invalid version specifier"):
        matches("~~3.4", "3.8")


def test_reads_versions_json():
    text = json.dumps(
        [
            {"version": "3.8", "title": "3.8", "aliases": ["latest"]},
            {"version": "3.6", "title": "3.6", "aliases": []},
        ]
    )
    entries = read_versions_json(text)
    assert [entry.version for entry in entries] == ["3.8", "3.6"]
    assert entries[0].aliases == ("latest",)


def test_resolves_an_alias_from_versions_json():
    entries = read_versions_json(
        json.dumps([{"version": "3.8", "aliases": ["latest"]}, {"version": "3.6"}])
    )
    assert alias_target(entries, "latest") == "3.8"
    assert alias_target(entries, "stable") is None


def test_malformed_versions_json_is_reported():
    with pytest.raises(VersionError):
        read_versions_json("not json")
    with pytest.raises(VersionError, match="list"):
        read_versions_json('{"version": "3.8"}')
