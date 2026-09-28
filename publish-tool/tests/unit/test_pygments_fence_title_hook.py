"""The fence-title hook restores the `<a>` that Pygments 2.20.0 HTML-escapes out of a superfences
`title=`, in either quoting shape our own fences produce, and leaves anything else alone.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pygments_fence_title_hook import on_page_content


def restore(html: str) -> str:
    return on_page_content(html, page=None, config=None)


def test_a_top_level_fences_escaped_link_is_restored():
    """The quote survives as a literal `'` for a fence that is not inside a content tab."""
    escaped = (
        "class=\"filename\">&lt;a href='https://github.com/x/y/blob/main/z.yaml' "
        "target='_blank'&gt;z.yaml&lt;/a&gt;</span>"
    )
    assert restore(escaped) == (
        'class="filename"><a href="https://github.com/x/y/blob/main/z.yaml" '
        'target="_blank" rel="noopener">z.yaml</a></span>'
    )


def test_a_tabbed_fences_escaped_link_is_restored():
    """`pymdownx.tabbed` re-escapes the quote to `&#x27;` for a fence nested in a content tab."""
    escaped = (
        'class="filename">&lt;a href=&#x27;#&#x27; target=&#x27;_blank&#x27;&gt;'
        "main.ts&lt;/a&gt;</span>"
    )
    assert restore(escaped) == (
        'class="filename"><a href="#" target="_blank" rel="noopener">main.ts</a></span>'
    )


def test_html_with_no_escaped_filename_link_is_left_alone():
    html = '<p>Nothing to see here.</p><span class="filename">plain.txt</span>'
    assert restore(html) == html


def test_a_filename_link_pygments_did_not_escape_is_left_alone():
    """Self-neutralising: once the title renders unescaped again, there is nothing to do."""
    html = 'class="filename"><a href="https://x/y" target="_blank">y</a></span>'
    assert restore(html) == html
