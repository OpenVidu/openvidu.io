"""The linked filename above a code block, restored from the escape Pygments applies.

Pygments 2.20.0 (the CVE-2026-73295 / ReDoS hardening) started HTML-escaping the superfences
`title=` option, which this repository's tutorials use to link a code block's filename to its
GitHub source: `title="<a href='…' target='_blank'>app.js</a>"`. Escaping an arbitrary title is
the right fix, so it stays on; this restores just the one first-party shape our own fences emit.

A postprocessor sees the page's final HTML, after the `raw_html` postprocessor has put the
stashed code blocks back, so it fixes the page and — because Zensical converts that same HTML
into the page's Markdown export — the llms.txt copy as well. It replaces the MkDocs hook
`publish-tool/pygments_fence_title_hook.py`, which the version branches still carry for their
MkDocs builds. Delete both when the fences stop carrying HTML in `title=`.
"""

from __future__ import annotations

import re
from typing import Any

from markdown import Extension, Markdown
from markdown.postprocessors import Postprocessor

#: The quote is a literal `'` for a top-level fence but `&#x27;` for one nested in a content tab
#: (`pymdownx.tabbed` re-escapes it first), so both are matched.
ESCAPED_FILENAME_LINK = re.compile(
    r"""class="filename">&lt;a href=(?:'|&\#x27;)([^'&]+)(?:'|&\#x27;) """
    r"""target=(?:'|&\#x27;)_blank(?:'|&\#x27;)&gt;([^<]+)&lt;/a&gt;"""
)


def restore_filename_links(html: str) -> str:
    return ESCAPED_FILENAME_LINK.sub(
        r'class="filename"><a href="\1" target="_blank" rel="noopener">\2</a>', html
    )


class FenceTitlePostprocessor(Postprocessor):
    name = "ovweb_fence_title"

    def run(self, text: str) -> str:
        return restore_filename_links(text)


class FenceTitleExtension(Extension):
    name = "ovweb.mdx.fence_title"

    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)
        # Below `raw_html` (30), which restores the stashed code blocks this looks into.
        md.postprocessors.register(FenceTitlePostprocessor(md), FenceTitlePostprocessor.name, 5)


def makeExtension(**kwargs: Any) -> FenceTitleExtension:
    return FenceTitleExtension(**kwargs)
