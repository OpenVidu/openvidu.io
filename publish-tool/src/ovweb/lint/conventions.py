"""Page-composition conventions: admonitions, the `tags:` contract, assets and snippets.

The `tags:` contract is include-aware: a page's snippets are inlined before checking, because
the HTML that requires a tag usually lives in a snippet while the tag must sit on the page.
"""

from __future__ import annotations

import re

from ..sources import sources_of
from .corpus import Corpus, Source
from .findings import ERROR, WARN, Finding

ADMONITION = re.compile(r"^[ \t]*(!!!|\?\?\?\+?)(?=[A-Za-z])", re.MULTILINE)
BLOG_ASSET = re.compile(r"/assets/images/blog/([^/\s\"')]+/[^/\s\"')]+/[^/\s\"')]+)/")

#: HTML markers that only work when the page carries the matching functional tag, which loads
#: the JS behind them (see README "Mkdocs Material tag system").
TAG_CONTRACT = (
    ('class="glightbox"', "setupcustomgallery"),
    ("feature-cards", "setupcardglow"),
    ("carousel-cell", "setupcarousel"),
)


def check_admonitions(corpus: Corpus) -> list[Finding]:
    findings = []
    for collection in (corpus.docs, corpus.snippets):
        for source in collection.values():
            for match in ADMONITION.finditer(source.visible):
                findings.append(
                    Finding(
                        "admonition-spacing",
                        ERROR,
                        source.path,
                        source.line_of(match.start()),
                        f'"{match.group(1)}" needs a space before the type',
                        'write `!!! warning "Title"`, not `!!!warning`',
                    )
                )
    return findings


def _effective_text(page: Source, corpus: Corpus) -> str:
    """The page's visible text plus every snippet it pulls in, at any depth."""
    parts = []
    for path in sources_of(page.path, corpus.read_visible):
        text = corpus.read_visible(path)
        if text is not None:
            parts.append(text)
    return "\n".join(parts)


def check_tag_contract(corpus: Corpus) -> list[Finding]:
    findings = []
    for path, page in corpus.docs.items():
        tags = page.meta.get("tags") or []
        if not isinstance(tags, list):
            tags = []
        effective = _effective_text(page, corpus)
        for marker, tag in TAG_CONTRACT:
            if marker in effective and tag not in tags:
                findings.append(
                    Finding(
                        "tag-contract",
                        WARN,
                        path,
                        1,
                        f"page renders `{marker}` content but lacks `tags: [{tag}]`",
                        "the tag loads the JS behind that markup (possibly pulled in by a "
                        "snippet); without it the element falls back to default behaviour "
                        "or renders inert",
                    )
                )
    return findings


def check_asset_placement(corpus: Corpus) -> list[Finding]:
    """No files directly at the images/ or videos/ root — every asset lives in a page folder."""
    findings = []
    for folder in ("docs/assets/images", "docs/assets/videos"):
        base = corpus.root / folder
        if not base.is_dir():
            continue
        for entry in sorted(base.iterdir()):
            if entry.is_file():
                findings.append(
                    Finding(
                        "asset-placement",
                        WARN,
                        f"{folder}/{entry.name}",
                        1,
                        f"file sits directly at {folder}/",
                        "assets live in a folder named after the consuming page; see README "
                        "'Organizing assets'",
                    )
                )
    return findings


def check_light_dark_pairs(corpus: Corpus) -> list[Finding]:
    """`#only-light` and `#only-dark` are authored in pairs; an odd count means a theme gap."""
    findings = []
    for path, page in corpus.docs.items():
        effective = _effective_text(page, corpus)
        light = effective.count("#only-light")
        dark = effective.count("#only-dark")
        if light != dark:
            findings.append(
                Finding(
                    "light-dark-pair",
                    WARN,
                    path,
                    1,
                    f"{light} #only-light vs {dark} #only-dark references (snippets included)",
                    "one theme is missing an image the other has",
                )
            )
    return findings


def check_snippet_names(corpus: Corpus) -> list[Finding]:
    """A snippet's filename must not repeat its folder name (`aws/troubleshooting.md`)."""
    findings = []
    for path in corpus.snippets:
        parts = path.split("/")
        stem = parts[-1].removesuffix(".md")
        folder = parts[-2] if len(parts) > 1 else ""
        if folder and folder != "shared" and (stem == folder or stem.startswith(f"{folder}-")):
            findings.append(
                Finding(
                    "snippet-name",
                    WARN,
                    path,
                    1,
                    f'filename repeats the folder name "{folder}"',
                    "see shared/README.md naming conventions",
                )
            )
    return findings


def check_blog_asset_mirroring(corpus: Corpus) -> list[Finding]:
    """A post's assets live in the folder mirroring the post's own path."""
    findings = []
    for path, page in corpus.docs.items():
        if not path.startswith("docs/blog/posts/"):
            continue
        expected = "/".join(path.removesuffix(".md").split("/")[-3:])
        for match in BLOG_ASSET.finditer(page.visible):
            if match.group(1) != expected:
                findings.append(
                    Finding(
                        "blog-asset-mirror",
                        WARN,
                        path,
                        page.line_of(match.start()),
                        f"references assets of {match.group(1)}, but this post's folder "
                        f"is {expected}",
                        "a post's assets mirror its own year/month/slug path",
                    )
                )
    return findings
