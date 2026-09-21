"""MkDocs hook that restores the linked filename above a code block.

Pygments 2.20.0 (the CVE-2026-73295 / ReDoS hardening) started HTML-escaping the superfences
`title=` option, which this repository's tutorials use to link a code block's filename to its
GitHub source: `title="<a href='…' target='_blank'>app.js</a>"`. Escaping an arbitrary title is
the right fix, so it stays on; this restores just the one first-party shape our own fences emit.

A hook's `on_page_content` runs after the plugins', so this fixes the page's HTML but not its
Markdown export: `mkdocs-llmstxt` has converted the page by then. That half is in
`llmstxt_preprocess.py`.

This file is copied verbatim onto every `X.Y` version branch and into livekit-tutorials-docs
(`hooks/`), because MkDocs loads a hook by path from the checked-out branch. Edit it here, then
re-copy it; `ovweb doctor` reports a branch whose copy differs. Delete every copy, and the
`hooks:` entries naming it, when the fences stop carrying HTML in `title=`.
"""

import re

#: The quote is a literal `'` for a top-level fence but `&#x27;` for one nested in a content tab
#: (`pymdownx.tabbed` re-escapes it first), so both are matched.
_ESCAPED_FILENAME_LINK = re.compile(
    r"""class="filename">&lt;a href=(?:'|&\#x27;)([^'&]+)(?:'|&\#x27;) """
    r"""target=(?:'|&\#x27;)_blank(?:'|&\#x27;)&gt;([^<]+)&lt;/a&gt;"""
)


def on_page_content(html, page, config, **kwargs):
    return _ESCAPED_FILENAME_LINK.sub(
        r'class="filename"><a href="\1" target="_blank" rel="noopener">\2</a>', html
    )
