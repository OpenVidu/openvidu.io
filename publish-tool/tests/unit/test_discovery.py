"""Reading a published tree: which versions it serves, and what `latest` points at.

The git-backed half of `discovery` is exercised through `ovweb versions list` and
`ovweb redirects check`; what is pinned here is the tree half, which the post-processing, `verify`
and `redirects apply` all depend on.
"""

from __future__ import annotations

import json

from ovweb.discovery import latest_in_tree, version_folders, versions_in_tree


def tree(tmp_path, *versions: str, published=None, alias: str | None = None):
    for version in versions:
        (tmp_path / version).mkdir()
    if published is not None:
        (tmp_path / "versions.json").write_text(
            json.dumps(
                [
                    {"version": name, "aliases": ["latest"] if name == alias else []}
                    for name in published
                ]
            ),
            encoding="utf-8",
        )
    return tmp_path


# -- the version folders -----------------------------------------------------------------


def test_finds_the_minor_version_folders(tmp_path):
    root = tree(tmp_path, "3.8", "3.2")
    (root / "pricing").mkdir()
    (root / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")

    assert version_folders(root) == ["3.2", "3.8"]


def test_a_legacy_exact_patch_folder_is_not_a_version_folder(tmp_path):
    """`/3.4.1/` is only ever read — the 404 router redirects it to the minor folder."""
    assert version_folders(tree(tmp_path, "3.4", "3.4.1", "3.0.0-beta1")) == ["3.4"]


# -- which versions the tree serves ------------------------------------------------------


def test_versions_json_is_the_authority(tmp_path):
    """It drives the version selector, so a folder it does not list is not served."""
    root = tree(tmp_path, "3.8", "3.7", published=["3.8"])
    assert versions_in_tree(root) == ["3.8"]


def test_the_folders_stand_in_when_versions_json_is_absent(tmp_path):
    assert versions_in_tree(tree(tmp_path, "3.8", "3.7")) == ["3.7", "3.8"]


# -- the alias ---------------------------------------------------------------------------


def test_the_symlink_is_the_authority(tmp_path):
    """mike materialises the alias as a symlink to the version folder."""
    root = tree(tmp_path, "3.8", published=["3.8", "3.7"], alias="3.7")
    (root / "latest").symlink_to("3.8")

    assert latest_in_tree(root) == "3.8"


def test_versions_json_resolves_the_alias_without_a_symlink(tmp_path):
    root = tree(tmp_path, "3.8", published=["3.8", "3.7"], alias="3.8")
    assert latest_in_tree(root) == "3.8"


def test_an_alias_no_one_claims_is_none(tmp_path):
    """Neither a symlink nor an entry naming it: the caller has to handle not knowing."""
    assert latest_in_tree(tree(tmp_path, "3.8")) is None
    assert latest_in_tree(tree(tmp_path, "3.7", published=["3.7"])) is None


def test_another_alias_can_be_asked_for(tmp_path):
    root = tree(tmp_path, "3.8")
    (root / "stable").symlink_to("3.8")

    assert latest_in_tree(root, alias="stable") == "3.8"
    assert latest_in_tree(root) is None
