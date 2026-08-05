"""Link checks over the source tree.

MkDocs validates Markdown link targets, so those resolution checks are not repeated here. What
it never sees: anything inside raw HTML, the *form* conventions (a relative link in a file that
moves at publish, a version-pinned URL outside the releases pages), and content hidden in HTML
comments.
"""

from __future__ import annotations

import re

from ..model import SiteLayout
from .corpus import Corpus, Source
from .findings import ERROR, INFO, WARN, Finding

HREF_SRC = re.compile(r"""(?:href|src)\s*=\s*(?:"([^"]*)"|'([^']*)')""")
MD_TARGET = re.compile(r"\]\(\s*(<[^>]*>|[^)\s]+)")
VERSION_PIN = re.compile(
    r"https://openvidu\.io/(\d+\.\d+)/|\]\(/(\d+\.\d+)/|(?:href|src)=\"/(\d+\.\d+)/"
)
LATEST_LINK = re.compile(r"https://openvidu\.io/latest/|\]\(/latest/|(?:href|src)=\"/latest/")
MORE_MARKER = re.compile(r"<!--\s*more\s*-->")
MINOR = re.compile(r"\d+\.\d+")

SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:", "//")


def _html_targets(text: str):
    """(offset, target) for every href/src value in `text`."""
    for match in HREF_SRC.finditer(text):
        target = match.group(1) if match.group(1) is not None else match.group(2)
        yield match.start(), target


def _md_targets(text: str):
    for match in MD_TARGET.finditer(text):
        yield match.start(), match.group(1).strip("<>")


def resolves(target: str, corpus: Corpus, layout: SiteLayout) -> bool:
    """Whether a root-absolute URL path is served by a file in the source tree."""
    path = target.partition("#")[0].partition("?")[0].lstrip("/")
    if path.startswith("latest/"):
        path = path[len("latest/") :]
    if path == "":
        return corpus.is_file("docs/index.md")
    first = path.split("/", 1)[0]
    if first in layout.assets:
        return not path.endswith("/") and corpus.is_file(f"docs/{path}")
    stem = path.rstrip("/")
    if stem.endswith((".html", ".md")):
        return corpus.is_file(f"docs/{stem}")
    return corpus.is_file(f"docs/{stem}.md") or corpus.is_file(f"docs/{stem}/index.md")


def _documented_relative_exception(path: str, target: str) -> bool:
    """The relative snippet links README "Link rules" documents as deliberate.

    Snippets in the parallel deployment-type trees keep sibling links relative so each host
    tree resolves its own copy, and links into `reference-docs/` resolve inside whichever
    version folder includes them.
    """
    if path.startswith("shared/self-hosting/"):
        return True
    return "reference-docs/" in target


def _checkable_html_target(target: str) -> bool:
    if not target.startswith("/") or target.startswith("//"):
        return False
    # Jinja expressions and template placeholders cannot be resolved from the source tree.
    if "{{" in target or "{%" in target:
        return False
    # A leading X.Y segment belongs to the version-pin check, not to resolution.
    return not MINOR.fullmatch(target.lstrip("/").split("/", 1)[0])


def check_html_targets(corpus: Corpus, layout: SiteLayout) -> list[Finding]:
    """Raw-HTML links and images: MkDocs never validates these."""
    findings = []
    sources: list[tuple[str, str, Source | None]] = [
        (source.path, source.visible, source)
        for collection in (corpus.docs, corpus.snippets)
        for source in collection.values()
    ]
    sources += [(path, text, None) for path, text in corpus.overrides.items()]

    for path, text, source in sources:
        for offset, target in _html_targets(text):
            line = source.line_of(offset) if source else text.count("\n", 0, offset) + 1
            if target.startswith("/") and target.partition("#")[0].endswith(".md"):
                findings.append(
                    Finding(
                        "html-md-form",
                        ERROR,
                        path,
                        line,
                        f'raw HTML must use the URL form, not a source path: "{target}"',
                        "the .md form is for Markdown links; in HTML write the served URL",
                    )
                )
                continue
            if not _checkable_html_target(target):
                continue
            if not resolves(target, corpus, layout):
                findings.append(
                    Finding(
                        "html-target",
                        ERROR,
                        path,
                        line,
                        f'raw HTML references "{target}", which no source file serves',
                        "MkDocs does not validate HTML; fix the path or restore the target",
                    )
                )
    return findings


def check_markdown_form(corpus: Corpus) -> list[Finding]:
    """Link form in the files that move at publish, and the stray-slash anchor defect."""
    findings = []
    movable = [
        (source, ERROR, "a blog post moves at publish; a relative link breaks then")
        for path, source in corpus.docs.items()
        if path.startswith("docs/blog/posts/")
    ]
    movable += [
        (
            source,
            WARN,
            "snippets render at many depths; only the documented sibling links stay relative",
        )
        for source in corpus.snippets.values()
    ]

    for source, severity, hint in movable:
        for offset, target in _md_targets(source.visible):
            if target.startswith(("/", "#", *SKIP_SCHEMES)):
                continue
            if _documented_relative_exception(source.path, target):
                continue
            findings.append(
                Finding(
                    "md-relative-in-movable",
                    severity,
                    source.path,
                    source.line_of(offset),
                    f'relative link "{target}" in a file whose rendered location varies',
                    hint,
                )
            )

    for collection in (corpus.docs, corpus.snippets):
        for source in collection.values():
            for offset, target in _md_targets(source.visible):
                if ".md/#" in target:
                    findings.append(
                        Finding(
                            "stray-slash-anchor",
                            ERROR,
                            source.path,
                            source.line_of(offset),
                            f'stray "/" before the anchor in "{target}"',
                            'write "page.md#anchor", not "page.md/#anchor"',
                        )
                    )

    # The blog plugin copies the excerpt (everything before <!-- more -->) onto the listing
    # pages WITHOUT rewriting resolved Markdown links, so a `.md` target that renders fine on
    # the post page leaks as a literal dead `/x.md` href on /blog/ and every category page.
    for path, source in corpus.docs.items():
        if not path.startswith("docs/blog/posts/"):
            continue
        marker = MORE_MARKER.search(source.commented)
        if marker is None:
            continue
        for offset, target in _md_targets(source.visible):
            if offset < marker.start() and target.partition("#")[0].endswith(".md"):
                findings.append(
                    Finding(
                        "md-link-in-excerpt",
                        ERROR,
                        source.path,
                        source.line_of(offset),
                        f'Markdown link "{target}" in the excerpt (before <!-- more -->)',
                        "the blog listing pages copy the excerpt without rewriting it; use "
                        'the raw-HTML URL form there: <a href="/x/">…</a>',
                    )
                )
    return findings


def _release_files(layout: SiteLayout) -> set[str]:
    return {f"docs/{section}/releases.md" for section in layout.versioned_pages}


def _is_release_post(source: Source) -> bool:
    categories = source.meta.get("categories") or []
    return isinstance(categories, list) and "Release" in categories


def check_version_pins(corpus: Corpus, layout: SiteLayout) -> list[Finding]:
    """Version-pinned links live only on the releases pages and in Release blog posts."""
    findings = []
    releases = _release_files(layout)
    for collection in (corpus.docs, corpus.snippets):
        for source in collection.values():
            if source.path in releases or _is_release_post(source):
                continue
            for match in VERSION_PIN.finditer(source.visible):
                version = next(group for group in match.groups() if group)
                findings.append(
                    Finding(
                        "version-pinned-link",
                        ERROR,
                        source.path,
                        source.line_of(match.start()),
                        f"link pinned to version {version} outside the releases pages",
                        "pin versions only on the releases pages and in Release blog posts",
                    )
                )

    # The inverse rule: the releases pages must never point at `latest` — the publish fails on it.
    for path in releases:
        source = corpus.docs.get(path)
        if source is None:
            continue
        for match in LATEST_LINK.finditer(source.visible):
            findings.append(
                Finding(
                    "latest-in-releases",
                    ERROR,
                    source.path,
                    source.line_of(match.start()),
                    "release notes link to `latest`, which the publish refuses",
                    "release-notes links must be absolute and pinned to the version they describe",
                )
            )
    return findings


def check_commented_links(corpus: Corpus, layout: SiteLayout) -> list[Finding]:
    """Root-absolute links inside HTML comments that nothing serves: janitorial."""
    findings = []
    for collection in (corpus.docs, corpus.snippets):
        for source in collection.values():
            targets = [*_html_targets(source.commented), *_md_targets(source.commented)]
            for offset, target in targets:
                if not _checkable_html_target(target):
                    continue
                if not resolves(target, corpus, layout):
                    findings.append(
                        Finding(
                            "commented-dead-link",
                            INFO,
                            source.path,
                            source.commented.count("\n", 0, offset) + 1,
                            f'commented-out content links to "{target}", which nothing serves',
                            "janitorial: delete the stale block or fix it before reviving it",
                        )
                    )
    return findings
