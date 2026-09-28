"""HTML pre-processing for the Markdown exports, hooked into `mkdocs-llmstxt`.

The plugin converts each page's rendered HTML to Markdown, running its own `autoclean` first unless
it is turned off — which `mkdocs.yml` does, because the plugin runs `autoclean` **before** the
`preprocess` hook:

    if should_autoclean: autoclean(soup)
    if preprocess:       _preprocess(soup, preprocess, path)

`autoclean` deletes every `twemoji` and the tab label bar outright, so by the time a hook sees the
soup the comparison-table icons and the tab labels are already gone. This module therefore
reimplements everything `autoclean` does, and deviates in the places listed below.
`tests/unit/test_llmstxt_preprocess.py` runs both over the same markup and requires identical
output everywhere else.

Every deviation serves one reader, an assistant that cannot see the page: what it gets must read as
the page does — a table as data, a tabbed block with its labels, a callout with its edges — and
nothing it cannot use may pass for prose.

1. A comparison-table icon becomes "Yes" / "No" / "In progress". The markup already says which —
   `<span class="twemoji compare-table-icon-yes">` — so the table exports as data instead of empty
   cells. The product logos heading such a table become their `alt` text for the same reason, one
   of each light/dark pair. Every other `twemoji` and image is removed, as `autoclean` does: a
   caption-length alt on a line of its own reads as a sentence of the page, not as a picture.

2. A link whose only content is an image or a video is dropped whole. `autoclean` removes an `<a>`
   wrapping an `<img>` but not one wrapping a `<video>`, so markdownify turns the anchor into an
   empty `[](…mp4)` link. A link with words of its own beside the image keeps them and its URL,
   where `autoclean` drops the whole link.

3. Tab labels are kept, as a bold line before each tab's content. Without them a tabbed block is a
   run of consecutive code blocks with nothing saying which is Linux, Windows or macOS — silently
   ambiguous rather than visibly missing.

4. A code block keeps its linked filename. Pygments 2.20.0 escapes the `<a>` our fences put in
   `title=`, so the soup holds it as text and the export would print raw HTML
   (`pygments_fence_title_hook.py` restores the same link in the page's HTML, which the plugin has
   converted by the time any hook runs). A line-numbered block's filename header is kept too,
   where `autoclean` drops it along with the numbers.

5. An admonition or a collapsible block becomes a blockquote, its title a bold first line. As the
   plain paragraphs markdownify would make of the `<div>`, the title reads as a stray word and
   nothing marks where the callout ends and the page resumes.

This file is copied verbatim onto the `X.Y` version branches from 3.4 and into
livekit-tutorials-docs (`hooks/`): the plugin loads it by path from the checked-out branch. Edit it
here, then re-copy it; `ovweb doctor` reports a copy that differs.
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

#: The class the theme puts on a product logo heading a comparison table.
COMPARISON_LOGO = "compare-table-logo"

#: Material renders a light/dark image pair as two `<img>` with the same `alt` and a `#only-…`
#: fragment. Only one logo of the pair may contribute its text, or the header names each product
#: twice.
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
    #   * a media link is dropped before its own `<img>` is removed, or the anchor would be left
    #     empty and become an empty Markdown link.
    _label_tabbed_blocks(soup)
    _replace_comparison_icons(soup)
    _drop_media_links(soup)
    _remove_images(soup)
    _remove_decoration(soup)
    _quote_callouts(soup)
    _unwrap_mkdocstrings(soup)
    _restore_fence_title_links(soup)
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


def _drop_media_links(soup: BeautifulSoup) -> None:
    """An anchor whose only content is an image or a video goes, URL and all.

    Kept, it would become an empty Markdown link. An anchor with words of its own keeps them.
    """
    for anchor in soup.find_all("a"):
        if anchor.find(["img", "video"]) is not None and not anchor.get_text().strip():
            anchor.decompose()


def _remove_images(soup: BeautifulSoup) -> None:
    """Every `<img>` goes, except a comparison-table logo, which becomes its alt text."""
    for image in soup.find_all("img"):
        if COMPARISON_LOGO in (image.get("class") or ()):
            image.replace_with(*_alt_text(image))
        else:
            image.decompose()


def _alt_text(media: Tag) -> list[NavigableString]:
    """The words a logo stands for: its `alt`, or nothing.

    A list, so a caller can splice it in with `replace_with(*…)` — which removes the node when the
    list is empty.
    """
    alt = (media.get("alt") or "").strip()
    if not alt or DUPLICATE_VARIANT in (media.get("src") or ""):
        return []
    return [NavigableString(alt)]


def _restore_fence_title_links(soup: BeautifulSoup) -> None:
    """`<span class="filename">&lt;a href='…'&gt;app.js&lt;/a&gt;</span>` -> a real `<a>`."""
    for span in soup.find_all("span", attrs={"class": "filename"}):
        text = span.get_text().strip()
        if span.find("a") is None and text.startswith("<a ") and text.endswith("</a>"):
            span.clear()
            span.extend(list(BeautifulSoup(text, "html.parser").contents))


def _quote_callouts(soup: BeautifulSoup) -> None:
    """`div.admonition` and `<details>` -> `<blockquote>`, led by the title (or summary) in bold.

    Document order, so a nested callout is quoted inside its parent's quote.
    """
    for box in soup.find_all(["div", "details"]):
        if box.name == "div" and "admonition" not in (box.get("class") or ()):
            continue
        title = (
            box.find("summary", recursive=False)
            if box.name == "details"
            else box.find("p", attrs={"class": "admonition-title"}, recursive=False)
        )
        quote = soup.new_tag("blockquote")
        if title is not None:
            heading = soup.new_tag("p")
            strong = soup.new_tag("strong")
            strong.string = title.get_text().strip()
            heading.append(strong)
            title.decompose()
            quote.append(heading)
        for child in list(box.children):
            quote.append(child.extract())
        box.replace_with(quote)


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
    """A line-numbered code block is a table; keep the filename and the code, drop the numbers."""
    for table in soup.find_all("table", attrs={"class": "highlighttable"}):
        code = table.find("code")
        if code is None:  # pragma: no cover - not a shape MkDocs produces
            continue
        pre = BeautifulSoup(f"<pre>{html.escape(code.get_text())}</pre>", "html.parser")
        filename = table.find("span", attrs={"class": "filename"})
        table.replace_with(*([filename.extract()] if filename else []), pre)
