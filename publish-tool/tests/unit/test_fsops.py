"""Filesystem primitives — the parity-relevant behaviour is byte preservation."""

from __future__ import annotations

import gzip

from ovweb import fsops


def test_rewrite_file_preserves_a_missing_trailing_newline(tmp_path):
    """`sed -i` does not add one, so adding one here would diff every file."""
    path = tmp_path / "page.html"
    path.write_bytes(b"<a>old</a>")
    assert fsops.rewrite_file(path, lambda text: text.replace("old", "new"))
    assert path.read_bytes() == b"<a>new</a>"


def test_rewrite_file_leaves_an_unchanged_file_untouched(tmp_path):
    path = tmp_path / "page.html"
    path.write_bytes(b"<a>same</a>")
    before = path.stat().st_mtime_ns
    assert fsops.rewrite_file(path, lambda text: text) is False
    assert path.stat().st_mtime_ns == before


def test_rewrite_file_skips_a_file_holding_a_nul_byte(tmp_path):
    """The same test `grep` applies before deciding a file is binary."""
    path = tmp_path / "font.woff2"
    original = b"wOF2\x00\x00assets/x"
    path.write_bytes(original)
    assert fsops.rewrite_file(path, lambda text: text.replace("assets", "BROKEN")) is False
    assert path.read_bytes() == original


def test_rewrite_file_skips_undecodable_bytes(tmp_path):
    path = tmp_path / "image.png"
    original = b"\x89PNG\xff\xfe assets/x"
    path.write_bytes(original)
    assert fsops.rewrite_file(path, lambda text: text.upper()) is False
    assert path.read_bytes() == original


def test_rewrite_tree_walks_every_extension(tmp_path):
    for name in ("a.html", "b.js", "c.json", "d.xml", "e.txt", "f.md", "g.css"):
        (tmp_path / name).write_text("needle", encoding="utf-8")
    assert fsops.rewrite_tree(tmp_path, lambda text: text.replace("needle", "found")) == 7


def test_rewrite_tree_on_a_missing_directory_is_a_no_op(tmp_path):
    assert fsops.rewrite_tree(tmp_path / "nope", lambda text: text) == 0


def test_rewrite_single_can_tolerate_a_missing_file(tmp_path):
    assert fsops.rewrite_single(tmp_path / "llms.txt", lambda t: t, required=False) is False


def test_gzip_output_is_deterministic(tmp_path):
    """`gzip -k -f` embeds the mtime, so the shell churned a new blob on every publish."""
    path = tmp_path / "sitemap.xml"
    path.write_text("<urlset></urlset>\n", encoding="utf-8")

    first = fsops.write_gzip(path).read_bytes()
    path.touch()
    second = fsops.write_gzip(path).read_bytes()

    assert first == second
    assert gzip.decompress(first) == b"<urlset></urlset>\n"


def test_gzip_records_the_original_filename(tmp_path):
    path = tmp_path / "sitemap.xml"
    path.write_text("x", encoding="utf-8")
    data = fsops.write_gzip(path).read_bytes()
    assert b"sitemap.xml" in data


def test_remove_is_tolerant_when_asked(tmp_path):
    assert fsops.remove(tmp_path / "nope", required=False) is False


def test_move_replaces_the_destination(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "f").write_text("new", encoding="utf-8")
    (tmp_path / "dst").mkdir()
    (tmp_path / "dst" / "stale").write_text("old", encoding="utf-8")

    fsops.move(tmp_path / "src", tmp_path / "dst")

    assert (tmp_path / "dst" / "f").read_text() == "new"
    assert not (tmp_path / "dst" / "stale").exists()
    assert not (tmp_path / "src").exists()


def test_copy_tree_leaves_the_source_in_place(tmp_path):
    """Assets are copied, not moved: the version folder keeps its own copy for the pinning."""
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "f").write_text("x", encoding="utf-8")

    fsops.copy_tree(tmp_path / "src", tmp_path / "dst")

    assert (tmp_path / "src" / "f").exists()
    assert (tmp_path / "dst" / "f").exists()
