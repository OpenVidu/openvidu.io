# How the code is organised

The split is between **pure** modules — they take and return strings and dataclasses and touch
nothing else — and **impure** ones that own the filesystem, git and mike. Every behavioural risk
lives in the pure layer, which is why that is where the tests are.

| Module                                                     | Pure? | Responsibility                                                                    |
| ---------------------------------------------------------- | ----- | ---------------------------------------------------------------------------------- |
| [`cli.py`](../src/ovweb/cli.py)                               | –     | Parse flags, build a plan, hand off. No decisions.                                |
| [`model.py`](../src/ovweb/model.py)                           | ✔     | Frozen value objects.                                                             |
| [`config.py`](../src/ovweb/config.py)                         | ✔     | Load and validate `ovweb.yaml`.                                                   |
| [`versions.py`](../src/ovweb/versions.py)                     | ✔     | `X.Y` names, ordering, specifier matching, `versions.json`.                       |
| [`sources.py`](../src/ovweb/sources.py)                       | ✔     | What a page is made of, for the sitemap's `<lastmod>`.                             |
| [`rewrite/versioned.py`](../src/ovweb/rewrite/versioned.py)   | ✔     | Asset pinning, root links, cookie base URL, `canonical`/`og:url` → `/latest/`.     |
| [`rewrite/nonversioned.py`](../src/ovweb/rewrite/nonversioned.py) | ✔ | Version stripping with the shield, `404.html`, the feeds.                         |
| [`rewrite/markdown.py`](../src/ovweb/rewrite/markdown.py)     | ✔     | The same rules for the Markdown exports and `llms.txt`.                            |
| [`rewrite/search_index.py`](../src/ovweb/rewrite/search_index.py) | ✔ | Absolutise search locations.                                                     |
| [`rewrite/sitemap.py`](../src/ovweb/rewrite/sitemap.py)       | ✔     | Root promotion and `<url>` block pruning.                                         |
| [`releases.py`](../src/ovweb/releases.py)                     | ✔     | Splice release notes between versions.                                            |
| [`redirects.py`](../src/ovweb/redirects.py)                   | ✔     | Resolve the `files` rules and render any redirect page.                            |
| [`expand.py`](../src/ovweb/expand.py)                         | –     | Enumerate the expansion kinds from the published tree, under the three filters.    |
| [`plan.py`](../src/ovweb/plan.py)                             | ✔     | The ordered publish description `--dry-run` prints.                               |
| [`fsops.py`](../src/ovweb/fsops.py)                           | –     | File walking, byte-preserving rewrites, deterministic gzip, moves and copies.     |
| [`gitrepo.py`](../src/ovweb/gitrepo.py)                       | –     | The git facade, including the worktree context manager.                           |
| [`mikewrap.py`](../src/ovweb/mikewrap.py)                     | –     | `mike deploy` / `mike delete`.                                                    |
| [`discovery.py`](../src/ovweb/discovery.py)                   | –     | Which versions exist, from the repository or from a published tree.                |
| [`pipeline/postprocess.py`](../src/ovweb/pipeline/postprocess.py) | – | The post-processing step table.                                                   |
| [`pipeline/publish.py`](../src/ovweb/pipeline/publish.py)     | –     | Branch preparation, mike, worktree, commit, branch sync.                          |
| [`verify.py`](../src/ovweb/verify.py)                         | –     | Invariants of a published tree.                                                   |
| [`lint/`](../src/ovweb/lint)                                  | –     | Authoring conventions over the sources — see [`contributing/checks.md`](../../contributing/checks.md). |
| [`doctor.py`](../src/ovweb/doctor.py)                         | –     | Preflight checks, including the pin agreement.                                    |
| [`mkdocs_hook.py`](../mkdocs_hook.py)                         | –     | Set each page's `<lastmod>` from git; feed llms.txt the pages' own frontmatter.    |
