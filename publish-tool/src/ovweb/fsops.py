"""Filesystem primitives used by the post-processing pipeline.

Thin and generic on purpose: the decisions live in the pure modules, this file only carries
them out. The two subtleties worth knowing about are documented on
:func:`iter_rewritable_files` and :func:`write_gzip`.
"""

from __future__ import annotations

import gzip
import shutil
from collections.abc import Callable, Iterable, Iterator
from functools import partial
from pathlib import Path

#: Files above this size are not candidates for link rewriting. The largest text file the
#: site builds is the search index (~3 MB), so this only ever excludes bundled media that
#: happens to be UTF-8 decodable.
MAX_REWRITE_BYTES = 64 * 1024 * 1024


def iter_rewritable_files(root: Path) -> Iterator[Path]:
    """Yield every file under `root` that link rewriting may touch.

    Deliberately no extension allow-list: the built tree mixes .html, .js, .json, .xml, .txt,
    .md and .css, and an allow-list would silently stop rewriting a new kind of file. Instead a
    file holding a NUL byte is skipped, so a substitution can never corrupt a font or an image.
    """
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        if path.stat().st_size > MAX_REWRITE_BYTES:
            continue
        yield path


def rewrite_file(path: Path, transform: Callable[[str], str]) -> bool:
    """Apply `transform` to one file's text. Returns whether anything changed.

    Reads and writes bytes around a UTF-8 decode so a file that needs no change is not
    rewritten at all, which also means a file with no trailing newline keeps not having one.

    Returns `False` for a file that is not UTF-8 text, or that holds a NUL byte.
    """
    original = path.read_bytes()
    if b"\x00" in original:
        return False
    try:
        text = original.decode("utf-8")
    except UnicodeDecodeError:
        return False

    updated = transform(text)
    if updated == text:
        return False

    path.write_bytes(updated.encode("utf-8"))
    return True


def rewrite_tree(root: Path, transform: Callable[[str], str]) -> int:
    """Apply `transform` to every rewritable file under `root`. Returns the change count."""
    return rewrite_tree_per_file(root, lambda _path, text: transform(text))


def rewrite_tree_per_file(root: Path, transform: Callable[[Path, str], str]) -> int:
    """Like :func:`rewrite_tree`, but `transform` also receives each file's path.

    For rewrites that depend on the file's *format* rather than its location. The built tree
    publishes each page twice — as HTML and as the Markdown export the llmstxt plugin writes
    beside it — and the same rule needs a different pattern in each, so the transform has to know
    which one it is looking at.
    """
    if not root.exists():
        return 0
    return sum(rewrite_file(path, partial(transform, path)) for path in iter_rewritable_files(root))


def rewrite_single(path: Path, transform: Callable[[str], str], *, required: bool = True) -> bool:
    """Apply `transform` to one known file.

    With `required=False` a missing file is not an error — old version branches never built
    some of these (llms.txt and the RSS feeds need plugins their mkdocs.yml did not have).
    """
    if not path.is_file():
        if required:
            raise FileNotFoundError(path)
        return False
    return rewrite_file(path, transform)


def write_text(path: Path, text: str) -> None:
    """Write text as UTF-8, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def write_gzip(path: Path) -> Path:
    """Write `path.gz` beside `path`, deterministically.

    gzip stores the source filename and modification time in its header, which would make the
    output differ on every publish even when the sitemap had not changed. Zeroing the mtime
    makes it a pure function of the input, so an unchanged sitemap stops churning the history.
    """
    target = path.with_suffix(path.suffix + ".gz")
    data = path.read_bytes()
    with (
        open(target, "wb") as handle,
        gzip.GzipFile(
            filename=path.name, mode="wb", fileobj=handle, mtime=0, compresslevel=9
        ) as compressor,
    ):
        compressor.write(data)
    return target


def remove(path: Path, *, required: bool = True) -> bool:
    """Delete a file or directory tree. Returns whether anything was removed."""
    if path.is_symlink() or path.is_file():
        path.unlink()
        return True
    if path.is_dir():
        shutil.rmtree(path)
        return True
    if required:
        raise FileNotFoundError(path)
    return False


def remove_all(paths: Iterable[Path], *, required: bool = True) -> int:
    return sum(remove(path, required=required) for path in paths)


def move(source: Path, destination: Path) -> None:
    """Move a file or directory, replacing whatever is already at the destination."""
    remove(destination, required=False)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))


def copy_tree(source: Path, destination: Path) -> None:
    """Copy a directory, replacing whatever is already at the destination."""
    remove(destination, required=False)
    shutil.copytree(source, destination, symlinks=True)


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8")
