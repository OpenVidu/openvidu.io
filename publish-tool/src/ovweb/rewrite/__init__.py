"""Pure link rewriting over the built site.

Every function here takes the text of one built file and returns the rewritten text. This is
where the behavioural risk of publishing lives — a wrong substitution silently breaks links on
every page — which is why it is kept free of I/O and covered by tests/unit/test_rewrite_*.py.

A substitution may be applied unconditionally to every in-scope file: none of them matches
anything it should not, so there is no need to select files first.
"""

from __future__ import annotations

from .nonversioned import (
    RewriteError,
    rewrite_404,
    rewrite_feed,
    rewrite_llms_txt,
    rewrite_non_versioned_file,
)
from .search_index import promote_search_index, rewrite_search_index
from .sitemap import promote_root_sitemap
from .versioned import rewrite_versioned_file

__all__ = [
    "RewriteError",
    "promote_root_sitemap",
    "promote_search_index",
    "rewrite_404",
    "rewrite_feed",
    "rewrite_llms_txt",
    "rewrite_non_versioned_file",
    "rewrite_search_index",
    "rewrite_versioned_file",
]
