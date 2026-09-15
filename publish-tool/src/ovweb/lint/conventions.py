"""Page-composition conventions: admonitions, the `page_features:` contract, assets and snippets.

The `page_features:` contract is include-aware: a page's snippets are inlined before
checking, because the HTML that requires a feature key usually lives in a snippet while
the key must sit on the page.
"""

from __future__ import annotations

import re

from ..sources import sources_of
from .corpus import Corpus, Source
from .findings import ERROR, WARN, Finding

ADMONITION = re.compile(r"^[ \t]*(!!!|\?\?\?\+?)(?=[A-Za-z])", re.MULTILINE)
BLOG_ASSET = re.compile(r"/assets/images/blog/([^/\s\"')]+/[^/\s\"')]+/[^/\s\"')]+)/")


def _class_token(token: str) -> re.Pattern[str]:
    """A class attribute containing `token` as a whole class name.

    Token matching, not substring: `ov-meet-commercial-feature-cards` is a custom class that
    happens to contain "feature-cards" and must not trip the contract.
    """
    return re.compile(rf'class="(?:[^"]* )?{re.escape(token)}( [^"]*)?"')


#: HTML class names that only work when the page carries the matching functional tag, which
#: loads the JS behind them (see contributing/page-composition.md).
TAG_CONTRACT = (
    (_class_token("feature-cards"), 'class="feature-cards"', "setupcardglow"),
    (_class_token("splide"), 'class="splide"', "setupcarousel"),
    (_class_token("lazy-video"), 'class="lazy-video"', "lazyvideo"),
    (_class_token("lead-form"), 'class="lead-form"', "leadform"),
    (re.compile(r'\bdata-sal="'), 'data-sal="..."', "revealonscroll"),
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
        features = page.meta.get("page_features") or []
        if not isinstance(features, list):
            features = []
        effective = _effective_text(page, corpus)
        for pattern, token, feature in TAG_CONTRACT:
            if pattern.search(effective) and feature not in features:
                findings.append(
                    Finding(
                        "tag-contract",
                        ERROR,
                        path,
                        1,
                        f"page renders `{token}` content but lacks `page_features: [{feature}]`",
                        "the feature key loads the JS behind that markup (possibly pulled in "
                        "by a snippet); without it the element falls back to default "
                        "behaviour or renders inert",
                    )
                )
    return findings


#: The site's font stylesheet and the preload hints that go with it (overrides/main.html).
FONT_LINK = re.compile(r"<link\b[^>]*fonts\.googleapis\.com/css2\?[^>]*>", re.DOTALL)
FONT_PRELOAD = re.compile(
    r"\{#\s*(?P<family>Tomorrow|Roboto Mono)(?:\s+(?P<weight>\d{3}))?\s*#\}\s*"
    r"<link\b(?P<attrs>[^>]*)>",
    re.DOTALL,
)
FONT_FAMILY_AXES = re.compile(r"family=([^:&]+):ital,wght@([^&]+)")


def _attr(tag: str, name: str) -> str:
    match = re.search(rf'\b{name}="([^"]*)"', tag)
    return match.group(1) if match else ""


def _requested_weights(url: str) -> dict[str, set[str]]:
    """Family -> upright weights a Google Fonts css2 URL requests."""
    families: dict[str, set[str]] = {}
    for family, axes in FONT_FAMILY_AXES.findall(url):
        pairs = (pair.split(",") for pair in axes.split(";"))
        families[family.replace("+", " ")] = {w for ital, w in pairs if ital == "0"}
    return families


def check_font_loading(corpus: Corpus) -> list[Finding]:
    """The font stylesheet keeps the no-flicker contract its comment in main.html describes.

    A render-blocking `rel="stylesheet"` with `display=block`, and every `{# Family NNN #}`
    preload hint names a weight the URL requests and carries `crossorigin`.
    """
    path = "overrides/main.html"
    text = corpus.overrides.get(path)
    if text is None:
        return []
    findings = []
    requested: dict[str, set[str]] = {}
    for match in FONT_LINK.finditer(text):
        tag = match.group(0)
        href = _attr(tag, "href")
        # Icon font of the register page: no text to flicker.
        if "Material+Symbols" in href:
            continue
        line = text.count("\n", 0, match.start()) + 1
        rel = _attr(tag, "rel")
        if rel != "stylesheet":
            findings.append(
                Finding(
                    "font-loading",
                    ERROR,
                    path,
                    line,
                    f'font stylesheet loaded with rel="{rel}"',
                    'load it with rel="stylesheet": the preload-as-style trick paints the page '
                    "before the @font-face rules exist",
                )
            )
        if "display=block" not in href:
            findings.append(
                Finding(
                    "font-loading",
                    ERROR,
                    path,
                    line,
                    "font stylesheet URL without display=block",
                    "display=swap paints the fallback font first, which is the flicker",
                )
            )
        requested.update(_requested_weights(href))
    for match in FONT_PRELOAD.finditer(text):
        attrs = match.group("attrs")
        if 'as="font"' not in attrs:
            continue
        family, weight = match.group("family"), match.group("weight")
        line = text.count("\n", 0, match.start()) + 1
        if weight and weight not in requested.get(family, set()):
            findings.append(
                Finding(
                    "font-loading",
                    ERROR,
                    path,
                    line,
                    f"preloads {family} {weight}, which the stylesheet URL does not request",
                    "a hint for a face the CSS never asks for is a wasted download: add the "
                    "weight to the URL or drop the preload",
                )
            )
        if "crossorigin" not in attrs:
            findings.append(
                Finding(
                    "font-loading",
                    ERROR,
                    path,
                    line,
                    f"{family} preload without crossorigin",
                    "fonts are fetched in CORS mode; a hint without crossorigin does not match "
                    "the request and the file downloads twice",
                )
            )
    return findings


IMG_TAG = re.compile(r"<img\b[^>]*>")

#: The canonical spelling is `{:target="_blank"}`. The escaped underscore and the unquoted or
#: colon-less variants render identically, but one spelling keeps greps and reviews sane.
TARGET_BLANK_FORM = re.compile(r"\\_blank|\{target=|target=_blank")


def check_image_alt(corpus: Corpus) -> list[Finding]:
    """Every raw-HTML image carries an `alt` attribute.

    Markdown images always have one (the bracket text); HTML ones are where it gets forgotten.
    A screenshot gets a descriptive alt; a purely decorative image gets an explicit `alt=""`.
    """
    findings = []
    sources = [
        (source.path, source.visible, source)
        for collection in (corpus.docs, corpus.snippets)
        for source in collection.values()
    ]
    sources += [(path, text, None) for path, text in corpus.overrides.items()]

    for path, text, source in sources:
        for match in IMG_TAG.finditer(text):
            if "alt=" in match.group(0):
                continue
            offset = match.start()
            line = source.line_of(offset) if source else text.count("\n", 0, offset) + 1
            findings.append(
                Finding(
                    "img-alt",
                    ERROR,
                    path,
                    line,
                    "HTML image without an alt attribute",
                    'screenshots get a descriptive alt; purely decorative images get alt=""',
                )
            )
    return findings


def check_target_blank_form(corpus: Corpus) -> list[Finding]:
    findings = []
    for collection in (corpus.docs, corpus.snippets):
        for source in collection.values():
            for match in TARGET_BLANK_FORM.finditer(source.visible):
                findings.append(
                    Finding(
                        "target-blank-form",
                        WARN,
                        source.path,
                        source.line_of(match.start()),
                        f'non-canonical target="_blank" spelling ("{match.group(0)}…")',
                        'write {:target="_blank"}',
                    )
                )
    return findings


#: A Markdown inline link with its optional attr_list block.
MD_LINK = re.compile(
    r"(?<!!)\[((?:[^\[\]]|\[[^\]]*\])*)\]\(<?([^)\s]+?)>?(?:\s+[\"'][^\"']*[\"'])?\)(\{[^}]*\})?"
)
EXTERNAL_ICON = re.compile(r":fontawesome-solid-external-link:\{\s*\.external-link-icon\s*\}")
#: Hosts that only look external: the reader's own deployment, or an illustrative domain.
LOCAL_HOSTS = (
    "localhost",
    "127.0.0.1",
    "openvidu-local.dev",
    "openvidu.example.io",
    "your-domain.com",
    "example.com",
)
ICON_ONLY_LABEL = re.compile(r"\s*:[a-z0-9-]+:\s*(\{[^}]*\})?\s*")


def _link_kind(url: str) -> str:
    if not url.startswith(("http://", "https://")):
        return "internal" if not url.startswith(("#", "mailto:", "tel:")) else ""
    host = url.split("//", 1)[1].split("/", 1)[0].lower()
    if any(h in host for h in LOCAL_HOSTS):
        return "local"
    if host in ("openvidu.io", "www.openvidu.io"):
        return "own"
    return "external"


def check_external_link_icon(corpus: Corpus) -> list[Finding]:
    """A link that leaves the page says so: `target="_blank"` plus the external-link icon.

    Exempt, because the marker would be noise or impossible: a label that is itself an image or
    a single icon shortcode, an `md-button` CTA (already its own affordance), `mailto:`, and the
    hosts in :data:`LOCAL_HOSTS` — the reader's own deployment is not another site.
    """
    findings = []
    for collection in (corpus.docs, corpus.snippets):
        for source in collection.values():
            for match in MD_LINK.finditer(source.visible):
                label, url, attrs = match.group(1), match.group(2), match.group(3) or ""
                kind = _link_kind(url)
                if kind in ("", "own", "local"):
                    continue
                if label.lstrip().startswith("!") or ICON_ONLY_LABEL.fullmatch(label):
                    continue
                if "md-button" in attrs:
                    continue
                line = source.line_of(match.start())
                if kind == "external" and "_blank" not in attrs:
                    findings.append(
                        Finding(
                            "external-link-target",
                            ERROR,
                            source.path,
                            line,
                            f'external link to "{url}" opens in the same tab',
                            'add {:target="_blank"} — leaving the site should not cost the '
                            "reader their place",
                        )
                    )
                if "_blank" in attrs and not EXTERNAL_ICON.search(label):
                    findings.append(
                        Finding(
                            "external-link-icon",
                            WARN,
                            source.path,
                            line,
                            f'link to "{url}" opens a new tab without the external-link icon',
                            "append :fontawesome-solid-external-link:{.external-link-icon} to "
                            "the label",
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
                        "assets live in a folder named after the consuming page; see "
                        "contributing/authoring.md 'Organizing assets'",
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
