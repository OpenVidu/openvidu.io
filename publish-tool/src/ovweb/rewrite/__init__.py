"""Pure link rewriting over the built site.

Every function here takes the text of one built file and returns the rewritten text. This is
where the behavioural risk of publishing lives — a wrong substitution silently breaks links on
every page — which is why it is kept free of I/O and covered by tests/unit/test_rewrite_*.py.

Within one format a substitution may be applied unconditionally to every in-scope file: none of
them matches anything it should not, so there is no need to select files first. Across formats it
cannot: the built tree publishes each page twice, as HTML and as the Markdown export the llmstxt
plugin writes beside it, and the two need different patterns to express the same rule. `markdown`
holds that second set, and the pipeline picks between them by suffix.
"""

from __future__ import annotations

from .markdown import (
    repair_export_links,
    rewrite_promoted_markdown,
    rewrite_versioned_markdown,
)
from .nonversioned import (
    RewriteError,
    rewrite_404,
    rewrite_feed,
    rewrite_non_versioned_file,
)
from .search_index import promote_search_index, rewrite_search_index
from .sitemap import promote_root_sitemap, prune_version_sitemap
from .versioned import rewrite_versioned_file

__all__ = [
    "RewriteError",
    "promote_root_sitemap",
    "promote_search_index",
    "prune_version_sitemap",
    "repair_export_links",
    "rewrite_404",
    "rewrite_feed",
    "rewrite_non_versioned_file",
    "rewrite_promoted_markdown",
    "rewrite_search_index",
    "rewrite_versioned_file",
    "rewrite_versioned_markdown",
]
