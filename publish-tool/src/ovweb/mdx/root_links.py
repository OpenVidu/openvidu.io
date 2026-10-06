"""Root-absolute links resolved against `docs/`, as MkDocs 1.6's `absolute_links:
relative_to_docs` did.

A shared snippet renders inside pages at different depths and a blog post moves at publish, so
both write their internal links from the `docs/` root (contributing/link-rules.md, rule 2):

    [Deployment guide](/docs/self-hosting/deployment-types.md)
    ![Diagram](/assets/images/platform/self-hosting/diagram.png#only-dark)

Zensical leaves a link that starts with `/` untouched, so the page would ship
`href="/docs/self-hosting/deployment-types.md"`. This treeprocessor rewrites every such link
into the equivalent link relative to the page's source file, and Zensical then resolves,
validates and rewrites it exactly like a hand-written relative link — a missing target is still
a build warning, which `--strict` turns into a failure.

It runs after `inline` (priority 20, where links and images are created) and before Zensical's
own rewriting (`zrelpath`, priority 0). Raw HTML is left alone on purpose: links inside HTML
blocks use the URL form (`href="/pricing/"`), never a source path (link-rules.md, rule 3).

The page's source path comes from the rendering context Zensical registers on the Markdown
instance; without one (plain Python-Markdown, the tests) the extension is a no-op.
"""

from __future__ import annotations

import posixpath
from typing import Any
from urllib.parse import urlsplit, urlunsplit
from xml.etree.ElementTree import Element

from markdown import Extension, Markdown
from markdown.treeprocessors import Treeprocessor

#: Which attribute carries the link, per element — the two MkDocs resolves too.
_LINK_ATTRIBUTES = {"a": "href", "img": "src"}


def relative_to_page(target: str, page_path: str) -> str:
    """`/docs/x.md` as seen from the source file `page_path` (both relative to docs/).

    >>> relative_to_page("/docs/self-hosting/local.md", "blog/posts/2026/04/post.md")
    '../../../../docs/self-hosting/local.md'
    >>> relative_to_page("/assets/images/a.png#only-dark", "meet/index.md")
    '../assets/images/a.png#only-dark'
    >>> relative_to_page("/index.md", "pricing.md")
    'index.md'
    """
    parts = urlsplit(target)
    path = posixpath.relpath(parts.path.lstrip("/") or ".", posixpath.dirname(page_path) or ".")
    if parts.path.endswith("/") and not path.endswith("/"):
        path += "/"  # a directory link stays one (`/support/` → `../support/`)
    return urlunsplit(parts._replace(path=path))


def _is_root_absolute(value: str) -> bool:
    """A site path from the docs root: `/x`, but not `//host`, `http:`, `mailto:` or `#anchor`."""
    if not value.startswith("/") or value.startswith("//"):
        return False
    parts = urlsplit(value)
    return not (parts.scheme or parts.netloc)


class RootLinksTreeprocessor(Treeprocessor):
    name = "ovweb_root_links"

    def run(self, root: Element) -> None:
        page_path = _page_path(self.md)
        if page_path is None:
            return
        for element in root.iter():
            key = _LINK_ATTRIBUTES.get(element.tag)
            if key is None:
                continue
            value = element.get(key)
            if value and _is_root_absolute(value):
                element.set(key, relative_to_page(value, page_path))


def _page_path(md: Markdown) -> str | None:
    """The source path of the page being rendered, from Zensical's rendering context."""
    try:
        from zensical.extensions.context import ContextPreprocessor
    except ImportError:  # not a Zensical build
        return None
    context = ContextPreprocessor.from_markdown(md)
    if context is None:
        return None
    return getattr(context.page, "path", None) or None


class RootLinksExtension(Extension):
    name = "ovweb.mdx.root_links"

    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        # After `inline` (20) and the glightbox wrapper (7); before Zensical's `zrelpath` (0).
        md.treeprocessors.register(RootLinksTreeprocessor(md), RootLinksTreeprocessor.name, 1)


def makeExtension(**kwargs: Any) -> RootLinksExtension:
    return RootLinksExtension(**kwargs)
