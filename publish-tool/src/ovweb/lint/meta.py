"""SEO frontmatter checks: presence of `title` and `description`, field lengths, uniqueness.

Presence is an error: both fields are what an llms.txt entry is made of (the publish reads them
off the page), what the `<title>` and the search snippet show, and what the social cards carry.
Under MkDocs a missing one failed the build, through a hook Zensical has no equivalent of, so the
lint is where CI catches it now. Lengths and uniqueness are conventions: violating them costs
ranking, not the build, so they warn instead of failing CI.
"""

from __future__ import annotations

from collections import defaultdict

from .corpus import Corpus
from .findings import ERROR, WARN, Finding

#: Material appends " - OpenVidu" to the <title>, which is what the ~57-character budget is for.
TITLE_LIMIT = 57
#: Blog post titles follow the SEO guideline instead: under 70 characters total.
BLOG_TITLE_LIMIT = 70
DESCRIPTION_LIMIT = 160
SENTENCE_ENDINGS = (".", "!", "?", "…")


def check_seo_fields(corpus: Corpus) -> list[Finding]:
    findings = []
    by_title: dict[str, list[str]] = defaultdict(list)
    by_description: dict[str, list[str]] = defaultdict(list)

    for path, source in corpus.docs.items():
        title = source.meta.get("title")
        description = source.meta.get("description")
        is_post = path.startswith("docs/blog/posts/")

        for key, value in (("title", title), ("description", description)):
            if not isinstance(value, str) or not value.strip():
                findings.append(
                    Finding(
                        f"missing-{key}",
                        ERROR,
                        path,
                        1,
                        f"no `{key}` in the frontmatter",
                        "every page needs a title and a description: together they are its "
                        "llms.txt entry, its <title> and its search snippet",
                    )
                )

        if isinstance(title, str):
            by_title[title].append(path)
            limit = BLOG_TITLE_LIMIT if is_post else TITLE_LIMIT
            if len(title) > limit:
                findings.append(
                    Finding(
                        "title-length",
                        WARN,
                        path,
                        1,
                        f"title is {len(title)} characters (budget {limit})",
                        'Material appends " - OpenVidu"; long titles truncate in search results',
                    )
                )
        if isinstance(description, str):
            by_description[description].append(path)
            if len(description) > DESCRIPTION_LIMIT:
                findings.append(
                    Finding(
                        "description-length",
                        WARN,
                        path,
                        1,
                        f"description is {len(description)} characters "
                        f"(budget {DESCRIPTION_LIMIT})",
                        "search engines truncate longer snippets",
                    )
                )
            elif not description.rstrip().endswith(SENTENCE_ENDINGS):
                findings.append(
                    Finding(
                        "description-format",
                        WARN,
                        path,
                        1,
                        "description does not end in a full stop",
                        "descriptions are full sentences; see contributing/authoring.md",
                    )
                )

    for value, paths in by_title.items():
        if len(paths) > 1:
            for path in paths:
                others = ", ".join(other for other in paths if other != path)
                findings.append(
                    Finding(
                        "duplicate-title",
                        WARN,
                        path,
                        1,
                        f'title "{value}" is shared by {len(paths)} pages',
                        f"titles are unique site-wide; also on {others}",
                    )
                )
    for paths in by_description.values():
        if len(paths) > 1:
            for path in paths:
                others = ", ".join(other for other in paths if other != path)
                findings.append(
                    Finding(
                        "duplicate-description",
                        WARN,
                        path,
                        1,
                        f"description is shared by {len(paths)} pages",
                        f"descriptions are unique site-wide; also on {others}",
                    )
                )
    return findings
