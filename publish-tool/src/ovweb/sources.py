"""What a page is made of, so `sitemap.xml` can carry a `<lastmod>` that is true.

MkDocs initialises `Page.update_date` to the build date for every page, and its sitemap template
emits exactly that. The field therefore claimed that all 261 URLs changed on every publish — no
per-page signal, and false often enough to teach a crawler to ignore it. The fix is to set
`update_date` from git before the sitemap is rendered; this module is the part of that with no I/O
in it.

A page's date is **not** just its own file's. 101 of the site's 248 pages assemble their content
from snippets under `shared/` with `--8<-- "path"`, 11 of those snippets include further snippets,
and the most-included one reaches 34 pages. Dating a page by its own file alone would leave all 34
untouched when the step they display is rewritten. So a page's date is the newest date across the
page and the transitive closure of what it includes.

Everything here takes the git output and a `read` callable and returns plain data, which is what
lets the rules be tested without a repository or a filesystem.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable

#: Prefix `LOG_ARGS` puts in front of each commit's date, so the walker can tell a date line
#: from a path line. `@@` cannot start a path in this repository, and `git log --name-only`
#: separates commits with a blank line either way.
MARKER = "@@"

#: The `git log` arguments this module parses. `--name-only` lists the paths each commit touched,
#: `%cs` is the committer date as `YYYY-MM-DD` — the format MkDocs already emits, and the date
#: that reflects when a change actually landed on the branch being published. `--no-renames`
#: reports a rename as an add plus a delete, so the new path is listed at the commit that created
#: it rather than being followed back to content that is no longer at that path.
LOG_ARGS = ("log", f"--format={MARKER}%cs", "--name-only", "--no-renames")

#: A `pymdownx.snippets` include. The marker has to open the line (indented is fine — many sit
#: inside admonitions), and this site uses only the quoted-path form: no `path:section`, no
#: `;optional` prefix and no URLs, across all 472 occurrences.
SNIPPET = re.compile(r'^[ \t]*--8<--[ \t]*"([^"]+)"[ \t]*$', re.MULTILINE)

#: Reads a repository-relative path, or returns None when there is nothing there. A miss is
#: normal rather than exceptional: `shared/README.md` documents the include syntax with a
#: placeholder path inside a code fence, and that is picked up by the regex like any other.
Reader = Callable[[str], "str | None"]


def parse_git_log(text: str) -> dict[str, str]:
    """Map every path in the log to the date of the most recent commit that touched it.

    `git log` walks newest-first, so the first date seen for a path is the answer and later ones
    are its history. Paths of files that have since been deleted come through too; they simply
    never get looked up.
    """
    dates: dict[str, str] = {}
    date = ""
    for line in text.splitlines():
        line = line.rstrip()
        if line.startswith(MARKER):
            date = line[len(MARKER) :]
        elif line and date:
            dates.setdefault(line, date)
    return dates


def sources_of(path: str, read: Reader) -> frozenset[str]:
    """The page plus every snippet it pulls in, at any depth.

    Iterative and set-guarded, so a snippet that includes itself — or two that include each
    other — terminates instead of recursing forever.
    """
    found: set[str] = set()
    pending = [path]
    while pending:
        current = pending.pop()
        if current in found:
            continue
        found.add(current)
        text = read(current)
        if text is not None:
            pending.extend(SNIPPET.findall(text))
    return frozenset(found)


def newest_dates(paths: Iterable[str], *, dates: dict[str, str], read: Reader) -> dict[str, str]:
    """The date to publish for each page: the newest across the page and what it includes.

    A page with no dated source at all — nothing in git yet — is left out of the result rather
    than given a made-up value, so the caller can omit the field for it.
    """
    cache: dict[str, str | None] = {}

    def cached(path: str) -> str | None:
        if path not in cache:
            cache[path] = read(path)
        return cache[path]

    resolved: dict[str, str] = {}
    for path in paths:
        found = [dates[source] for source in sources_of(path, cached) if source in dates]
        if found:
            resolved[path] = max(found)
    return resolved
