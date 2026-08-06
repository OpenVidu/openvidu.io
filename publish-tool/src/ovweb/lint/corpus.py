"""One pass over the authoring sources: docs pages, shared snippets, theme overrides.

Each Markdown source is kept in two same-length views so regex offsets map to real line
numbers: `visible` is what a reader sees (frontmatter, HTML comments, and code fences/spans
blanked out), `commented` is only what HTML comments hide. Checks that assert what the site
serves read `visible`; the janitorial commented-content check reads `commented`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
FENCE = re.compile(
    r"^(?P<indent>[ \t]*)(?P<fence>```+|~~~+).*?\n.*?^(?P=indent)(?P=fence)`*[ \t]*$",
    re.DOTALL | re.MULTILINE,
)
INLINE_CODE = re.compile(r"`[^`\n]+`")


@dataclass(frozen=True)
class Source:
    """A Markdown source file, parsed once."""

    path: str
    meta: dict
    visible: str
    commented: str

    def line_of(self, offset: int) -> int:
        return self.visible.count("\n", 0, offset) + 1


@dataclass(frozen=True)
class Corpus:
    root: Path
    docs: dict[str, Source]
    snippets: dict[str, Source]
    overrides: dict[str, str]

    def is_file(self, relpath: str) -> bool:
        return (self.root / relpath).is_file()

    def read_visible(self, relpath: str) -> str | None:
        """The visible text of a page or snippet, for snippet-closure walks."""
        source = self.docs.get(relpath) or self.snippets.get(relpath)
        return source.visible if source else None


def _blank(segment: str) -> str:
    """The segment with every character but newlines replaced, preserving offsets."""
    return "".join(char if char == "\n" else " " for char in segment)


def _mask(text: str, pattern: re.Pattern[str]) -> str:
    return pattern.sub(lambda match: _blank(match.group(0)), text)


def parse_source(path: str, text: str) -> Source:
    meta: dict = {}
    match = FRONTMATTER.match(text)
    body = text
    if match:
        try:
            loaded = yaml.safe_load(match.group(0).strip("-\n "))
            if isinstance(loaded, dict):
                meta = loaded
        except yaml.YAMLError:
            pass
        body = _blank(match.group(0)) + text[match.end() :]

    commented = "".join(
        segment if inside else _blank(segment) for segment, inside in _comment_segments(body)
    )
    visible = _mask(_mask(_mask(body, COMMENT), FENCE), INLINE_CODE)
    return Source(path=path, meta=meta, visible=visible, commented=commented)


def _comment_segments(text: str):
    """(segment, is_inside_comment) pairs covering the whole text."""
    position = 0
    for match in COMMENT.finditer(text):
        yield text[position : match.start()], False
        yield match.group(0), True
        position = match.end()
    yield text[position:], False


def load_corpus(root: Path) -> Corpus:
    docs: dict[str, Source] = {}
    snippets: dict[str, Source] = {}
    overrides: dict[str, str] = {}

    for base, target in (("docs", docs), ("shared", snippets)):
        folder = root / base
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob("*.md")):
            if path.is_symlink() or not path.is_file():
                continue
            relpath = path.relative_to(root).as_posix()
            # shared/README.md documents the snippets; it is not one.
            if relpath == "shared/README.md":
                continue
            target[relpath] = parse_source(relpath, path.read_text(encoding="utf-8"))

    overrides_dir = root / "docs" / "overrides"
    if overrides_dir.is_dir():
        for path in sorted(overrides_dir.rglob("*.html")):
            if path.is_file() and not path.is_symlink():
                relpath = path.relative_to(root).as_posix()
                overrides[relpath] = path.read_text(encoding="utf-8")

    return Corpus(root=root, docs=docs, snippets=snippets, overrides=overrides)
