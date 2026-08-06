"""HTML pre-processing for the Markdown exports, hooked into `mkdocs-llmstxt`.

The plugin converts each page's rendered HTML to Markdown, running its own `autoclean` first unless
it is turned off — which `mkdocs.yml` does, because the plugin runs `autoclean` **before** the
`preprocess` hook:

    if should_autoclean: autoclean(soup)
    if preprocess:       _preprocess(soup, preprocess, path)

`autoclean` deletes every `<img>` and `<svg>` outright, so by the time a hook sees the soup the
alt text, comparison-table icons and tab labels are already gone. This module therefore
reimplements everything `autoclean` does, and deviates in four places.
`tests/unit/test_llmstxt_preprocess.py` runs both over the same markup and requires identical
output everywhere else.

The deviations share one premise: an assistant cannot see an image or watch a video, so the asset
URL is worthless to it while the words describing the asset are not.

1. An `<img>` becomes its `alt` text instead of vanishing. Images with no usable alt are still
   removed, and of a Material light/dark pair only one contributes, or the text appears twice.

2. A comparison-table icon becomes "Yes" / "No" / "In progress". The markup already says which —
   `<span class="twemoji compare-table-icon-yes">` — so the table exports as data instead of empty
   cells. Every other `twemoji` is still removed.

3. A link whose only content is an image or a video becomes that asset's alt text, unlinked, and is
   dropped when there is none. `autoclean` removes an `<a>` wrapping an `<img>` but not one wrapping
   a `<video>`, so markdownify turns the anchor into an empty `[](…mp4)` link.

4. Tab labels are kept, as a bold line before each tab's content. Without them a tabbed block is a
   run of consecutive code blocks with nothing saying which is Linux, Windows or macOS — silently
   ambiguous rather than visibly missing.
"""

from __future__ import annotations

import html
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup, NavigableString

if TYPE_CHECKING:
    from bs4 import Tag

#: Maps the class the theme puts on a comparison-table icon to the text it stands for.
COMPARISON_ICONS = {
    "compare-table-icon-yes": "Yes",
    "compare-table-icon-no": "No",
    "compare-table-icon-progress": "In progress",
}

#: Material renders a light/dark image pair as two `<img>` with the same `alt` and a `#only-…`
#: fragment. Only one may contribute its text, or every such caption is duplicated.
DUPLICATE_VARIANT = "#only-dark"


def preprocess(soup: BeautifulSoup, output: str) -> None:
    """Clean one page's HTML before it is converted to Markdown.

    The signature is fixed by the plugin: the soup to modify, and the path of the Markdown file
    being written. Mutates in place; the return value is ignored.
    """
    del output  # Every rule here is page-independent.

    # Order matters in three places, and only these three:
    #   * tab labels are read before the label bar is removed;
    #   * a comparison icon is recognised before the generic `twemoji` removal reaches it;
    #   * a media link is resolved before its own `<img>` is replaced, so the anchor is what gets
    #     replaced rather than being left holding loose text.
    _label_tabbed_blocks(soup)
    _replace_comparison_icons(soup)
    _replace_media_links(soup)
    _replace_images_with_alt(soup)
    _remove_decoration(soup)
    _unwrap_mkdocstrings(soup)
    _flatten_code_tables(soup)


# -- the deviations ----------------------------------------------------------------------


def _label_tabbed_blocks(soup: BeautifulSoup) -> None:
    """Prefix each tab's content with its label, then drop the label bar.

    Labels and blocks are two flat lists in the same order — `div.tabbed-labels > label` and
    `div.tabbed-content > div.tabbed-block` — so they pair by position.
    """
    for tabbed in soup.find_all("div", attrs={"class": "tabbed-labels"}):
        labels = [label.get_text().strip() for label in tabbed.find_all("label")]
        content = tabbed.find_next_sibling("div", attrs={"class": "tabbed-content"})
        blocks = (
            content.find_all("div", attrs={"class": "tabbed-block"}, recursive=False)
            if content
            else []
        )
        for label, block in zip(labels, blocks, strict=False):
            if not label:
                continue
            heading = soup.new_tag("p")
            strong = soup.new_tag("strong")
            strong.string = label
            heading.append(strong)
            block.insert(0, heading)
        tabbed.decompose()


def _replace_comparison_icons(soup: BeautifulSoup) -> None:
    """`<span class="twemoji compare-table-icon-yes">` -> `Yes`."""
    for span in soup.find_all("span", attrs={"class": "twemoji"}):
        classes = span.get("class") or ()
        for name, text in COMPARISON_ICONS.items():
            if name in classes:
                span.replace_with(NavigableString(text))
                break


def _replace_media_links(soup: BeautifulSoup) -> None:
    """An anchor whose only content is an image or a video becomes that asset's alt text.

    The URL is dropped: a reader of these files cannot open it, and keeping it yields an empty
    Markdown link. When the asset has no alt text there is nothing to say, so the anchor goes.
    """
    for anchor in soup.find_all("a"):
        media = anchor.find(["img", "video"])
        if media is None or anchor.get_text().strip():
            continue
        anchor.replace_with(*_alt_text(media))


def _replace_images_with_alt(soup: BeautifulSoup) -> None:
    """Every remaining `<img>` becomes its alt text, or is removed when it has none."""
    for image in soup.find_all("img"):
        image.replace_with(*_alt_text(image))


def _alt_text(media: Tag) -> list[NavigableString]:
    """The words an asset stands for: its `alt`, or nothing.

    A list, so a caller can splice it in with `replace_with(*…)` — which removes the node when the
    list is empty.
    """
    alt = (media.get("alt") or "").strip()
    if not alt or DUPLICATE_VARIANT in (media.get("src") or ""):
        return []
    return [NavigableString(alt)]


# -- everything below reproduces the plugin's own `autoclean` -----------------------------


def _remove_decoration(soup: BeautifulSoup) -> None:
    """Drop what carries no text: icons, permalinks, mkdocstrings labels, media elements.

    `<video>` is not in `autoclean`'s list, which is why an anchor around one survives to become an
    empty link. A bare `<video>` contributes nothing either way.
    """
    for element in soup.find_all(["svg", "video"]):
        element.decompose()
    for element in soup.find_all(attrs={"class": "twemoji"}):
        element.decompose()
    for element in soup.find_all("a", attrs={"class": "headerlink"}):
        element.decompose()
    for element in soup.find_all("span", attrs={"class": "doc-labels"}):
        element.decompose()


def _unwrap_mkdocstrings(soup: BeautifulSoup) -> None:
    """Flatten the two mkdocstrings wrappers to their text.

    This site does not use mkdocstrings; the rules are kept so that turning `autoclean` off would
    change nothing if it ever does.
    """
    for element in soup.find_all("autoref"):
        element.replace_with(NavigableString(element.get_text()))
    for element in soup.find_all("div", attrs={"class": "doc-md-description"}):
        element.replace_with(NavigableString(element.get_text().strip()))


def _flatten_code_tables(soup: BeautifulSoup) -> None:
    """A line-numbered code block is a table; keep the code and drop the numbers."""
    for table in soup.find_all("table", attrs={"class": "highlighttable"}):
        code = table.find("code")
        if code is None:  # pragma: no cover - not a shape MkDocs produces
            continue
        table.replace_with(
            BeautifulSoup(f"<pre>{html.escape(code.get_text())}</pre>", "html.parser")
        )
