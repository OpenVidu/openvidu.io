"""Built-site link and anchor validation: `ovweb lint --site DIR`.

The built site is the truth the source tier approximates: it has the snippets inlined, the
templates composed, and — decisively — the anchor ids `pymdownx.tabbed` generates, which the
MkDocs validator cannot see (the reason `validation.links.anchors` sits at `info`, burying real
broken anchors under ~110 false positives). Resolving every fragment against the ids actually
present in the built HTML makes that false-positive class structurally impossible.

Scope: internal links only. Full-domain `https://openvidu.io/...` URLs resolve against the
site root too (minus version-pinned ones — those folders exist only in production and the
scheduled external-link job covers them). The generated `reference-docs/` API trees are not
walked as sources — their internal consistency belongs to the tool that generates them — but
they still resolve as targets.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

from .findings import ERROR, Finding

MINOR = re.compile(r"\d+\.\d+")
SITE_URL = re.compile(r"https://openvidu\.io(/|$)")

SKIP_SCHEMES = ("mailto:", "tel:", "data:", "javascript:", "about:")

#: Not walked as sources: generated API trees (their internal consistency belongs to the tool
#: that generates them) and the raw theme templates the build copies verbatim into the output.
SKIP_SOURCES = ("docs/reference-docs/", "overrides/")


class _PageParser(HTMLParser):
    """Collects every id and every href/src/srcset reference with its line number."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.refs: list[tuple[int, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line = self.getpos()[0]
        for name, value in attrs:
            if value is None:
                continue
            if name == "id" or (name == "name" and tag == "a"):
                self.ids.add(value)
            elif name in ("href", "src"):
                self.refs.append((line, value))
            elif name == "srcset":
                for entry in value.split(","):
                    candidate = entry.strip().split(" ")[0]
                    if candidate:
                        self.refs.append((line, candidate))

    handle_startendtag = handle_starttag


def _parse_page(path: Path) -> _PageParser:
    parser = _PageParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser


def _normalize(ref: str, page: str) -> str | None:
    """A reference as a site-relative path (with fragment), or None when out of scope."""
    if ref.startswith(SKIP_SCHEMES) or ref.startswith("//") or ref == "":
        return None
    if SITE_URL.match(ref):
        ref = "/" + ref.removeprefix("https://openvidu.io").lstrip("/")
    elif "://" in ref.partition("#")[0]:
        return None  # external: the scheduled link-check job's territory
    if ref.startswith("#"):
        return f"{page.rsplit('/', 1)[0] if '/' in page else ''}/{ref}".lstrip("/")

    path, _, fragment = ref.partition("#")
    path = path.partition("?")[0]
    if path.startswith("/"):
        resolved = path.lstrip("/")
    else:
        base = page.rsplit("/", 1)[0] if "/" in page else ""
        parts: list[str] = base.split("/") if base else []
        for segment in path.split("/"):
            if segment in ("", "."):
                continue
            if segment == "..":
                if not parts:
                    return None  # escapes the site: broken, but reported as unresolved below
                parts.pop()
            else:
                parts.append(segment)
        resolved = "/".join(parts) + ("/" if path.endswith("/") and parts else "")
    if resolved.startswith("latest/"):
        resolved = resolved.removeprefix("latest/")
    first = resolved.split("/", 1)[0]
    if MINOR.fullmatch(first):
        return None  # version-pinned: only production serves those folders
    return f"{resolved}#{fragment}" if fragment else resolved


def _served_file(site: Path, urlpath: str) -> Path | None:
    """The file the built site serves for a URL path, or None."""
    if urlpath in ("", "/"):
        candidate = site / "index.html"
        return candidate if candidate.is_file() else None
    candidate = site / urlpath.rstrip("/")
    if urlpath.endswith("/"):
        index = candidate / "index.html"
        return index if index.is_file() else None
    if candidate.is_file():
        return candidate
    index = candidate / "index.html"
    return index if index.is_file() else None


def check_site(site: Path) -> list[Finding]:
    """Every internal link and image resolves, and every fragment names a real id."""
    findings: list[Finding] = []
    ids_cache: dict[Path, set[str]] = {}

    pages = [
        path
        for path in sorted(site.rglob("*.html"))
        if path.is_file()
        and not any(path.relative_to(site).as_posix().startswith(prefix) for prefix in SKIP_SOURCES)
    ]

    for path in pages:
        page = path.relative_to(site).as_posix()
        parsed = _parse_page(path)
        ids_cache[path] = parsed.ids

        for line, ref in parsed.refs:
            normalized = _normalize(ref, page)
            if normalized is None:
                continue
            urlpath, _, fragment = normalized.partition("#")
            target = _served_file(site, urlpath)
            if target is None:
                findings.append(
                    Finding(
                        "site-target",
                        ERROR,
                        page,
                        line,
                        f'"{ref}" resolves to "/{urlpath}", which the built site does not serve',
                        "fix the reference or restore the target",
                    )
                )
                continue
            if not fragment or target.suffix != ".html":
                continue
            # "#/operations/..." style fragments are client-side routing (the OpenAPI
            # reference viewer), never HTML ids.
            if fragment.startswith("/"):
                continue
            if target not in ids_cache:
                ids_cache[target] = _parse_page(target).ids
            if fragment not in ids_cache[target]:
                findings.append(
                    Finding(
                        "site-anchor",
                        ERROR,
                        page,
                        line,
                        f'"{ref}" points at anchor "#{fragment}", which does not exist on the '
                        "target page",
                        "the heading was renamed or removed; fix the link or restore the anchor",
                    )
                )
    return findings
