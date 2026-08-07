"""Filesystem primitives used by the post-processing pipeline.

Thin and generic: the decisions live in the pure modules, this file only carries them out.
"""

from __future__ import annotations

import gzip
import shutil
from collections.abc import Callable, Iterable, Iterator
from functools import partial
from pathlib import Path

#: Files above this size are not candidates for link rewriting. The largest text file the site
#: builds is the search index at a few MB, so this only excludes bundled media.
MAX_REWRITE_BYTES = 64 * 1024 * 1024


def iter_rewritable_files(root: Path) -> Iterator[Path]:
    """Yield every file under `root` that link rewriting may touch, in sorted order.

    No extension allow-list: the built tree mixes .html, .js, .json, .xml, .txt, .md and .css,
    and an allow-list would silently stop rewriting a new kind of file. Binary content is
    excluded by :func:`rewrite_file` instead.
    """
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        if path.stat().st_size > MAX_REWRITE_BYTES:
            continue
        yield path


def rewrite_file(path: Path, transform: Callable[[str], str]) -> bool:
    """Apply `transform` to one file's text. Returns whether anything changed.

    Reads and writes bytes around a UTF-8 decode, so a file that needs no change is not
    rewritten at all and a file with no trailing newline keeps not having one. Returns `False`
    for a file that holds a NUL byte or is not UTF-8 text, so a substitution can never corrupt
    a font or an image.
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


def rewrite_tree_per_file(root: Path, transform: Callable[[Path, str], str]) -> int:
    """Apply `transform` to every rewritable file under `root`. Returns the change count.

    `transform` receives each file's path as well as its text, because the built tree publishes
    every page twice — as HTML and as the Markdown export beside it — and the same rule needs a
    different pattern in each. A missing `root` is a no-op.
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

    gzip stores the source mtime in its header, which would make the output differ on every
    publish even when the content had not changed. Zeroing it makes the blob a pure function of
    the input, so an unchanged sitemap does not churn the history.
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
