"""Pure link rewriting over the built site.

Every function here takes the text of one built file and returns the rewritten text. They
are the port of the `grep -Erl … | xargs sed -i` blocks that used to live in
`push-new-version.sh`, and they are where all the parity risk sits — hence
tests/unit/test_rewrite_*.py.

Two porting rules apply throughout:

* The `grep` in `grep … | xargs sed -i` was only a guard against `xargs` running `sed` with
  no arguments; it selected nothing that the substitution itself would not have skipped. So
  every function may be applied unconditionally to every in-scope file.
* The substitutions were BRE/ERE `sed` expressions with no `.` wildcards and no character
  classes able to cross a newline, so a whole-file `re.sub` is equivalent to `sed`'s
  line-by-line application.
"""

from __future__ import annotations

from .nonversioned import (
    RewriteError,
    rewrite_404,
    rewrite_feed,
    rewrite_llms_txt,
    rewrite_non_versioned_file,
)
from .search_index import rewrite_search_index
from .sitemap import promote_root_sitemap
from .versioned import rewrite_versioned_file

__all__ = [
    "RewriteError",
    "promote_root_sitemap",
    "rewrite_404",
    "rewrite_feed",
    "rewrite_llms_txt",
    "rewrite_non_versioned_file",
    "rewrite_search_index",
    "rewrite_versioned_file",
]
