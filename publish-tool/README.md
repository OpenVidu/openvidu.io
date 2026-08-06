# `ovweb` — publishing openvidu.io

This folder holds **`ovweb`**, the command line tool that publishes and maintains the
versions of the [openvidu.io](https://openvidu.io) documentation website.

The site is built with **MkDocs Material** and versioned with
[**mike**](https://github.com/jimporter/mike), which hosts every version in the `gh-pages`
branch of the repository (served through GitHub Pages). `ovweb` wraps `mike` to solve a problem
`mike` alone does not: keeping a set of **global, non-versioned pages** (pricing, blog,
support…) served once at the site root while the **versioned documentation** lives under
version-aliased paths.

```bash
pip install "./publish-tool[build]"

ovweb publish new    3.9   # a brand-new minor release
ovweb publish latest 3.8   # rebuild the newest version in place
ovweb publish past   3.7   # rebuild an older minor, root pages untouched
```

Versions are grouped by **minor** release (`X.Y`): one git branch, one `gh-pages` folder, one
version-selector entry, each serving its newest patch. The versioning model, the branch policy
and the releases-pages contract live in
[`contributing/versioning.md`](../contributing/versioning.md); this README covers the tool.

## Table of contents

- [Background concepts](#background-concepts)
- [The core problem this tool solves](#the-core-problem-this-tool-solves)
- [Commands](#commands)
- [What a publish does](#what-a-publish-does)
- [Testing](#testing)
- [Dependency pins](#dependency-pins)
- [Caveats and observations](#caveats-and-observations)

Design documentation, in [`docs/`](docs):

| Read when… | File |
| --- | --- |
| Adding or changing a redirect rule | [`docs/redirects.md`](docs/redirects.md) — the `files`/`expand` rule kinds, ownership, the generated page |
| Wondering what happens to a link at publish | [`docs/link-rewriting.md`](docs/link-rewriting.md) — the rewrite tables, the Markdown exports and `llms.txt` |
| Touching sitemaps, the version selector or search | [`docs/sitemaps-and-search.md`](docs/sitemaps-and-search.md) — the two sitemaps, `<lastmod>`, the two search indexes |
| Touching the releases pages machinery | [`docs/releases-splice.md`](docs/releases-splice.md) — the cross-version notes splice |
| Working on the tool's code or tests | [`docs/architecture.md`](docs/architecture.md), [`docs/testing-and-verify.md`](docs/testing-and-verify.md) |

The authoring conventions `ovweb lint` enforces are documented for contributors in
[`contributing/checks.md`](../contributing/checks.md).

## Background concepts

### `mike` and the `gh-pages` branch

`mike` builds each documentation version into its own subfolder of the `gh-pages` branch, named
after the version, and maintains **aliases** (friendly names that point to a version). This
project uses a single alias, `latest`, configured as the default in `mkdocs.yml`:

```yaml
extra:
    version:
        provider: mike
        default: latest
        alias: true
```

So after publishing version `3.9` as `latest`, `gh-pages` contains something like:

```
gh-pages/
├── 3.9/            # the built site for version 3.9
├── latest/         # alias → 3.9  (a real symlink, see docs/redirects.md)
├── versions.json   # mike's version index (drives the version selector)
└── ...
```

`mike` commits to `gh-pages` using git plumbing and never checks that branch out. `ovweb` relies
on that: it does the post-processing in a throwaway `git worktree`, so the main working tree
never leaves `main`.

### Versioned vs. non-versioned pages

Every page belongs to one of two groups, declared under the `layout:` key of
[`ovweb.yaml`](ovweb.yaml):

| Key (under `layout:`)        | Value                                                                                                                                 | Meaning                                                                                                       |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `layout.site_url`            | `https://openvidu.io`                                                                                                                 | The production origin every absolute URL is built against.                                                    |
| `layout.versioned_pages`     | `docs`, `meet`                                                                                                                        | Documentation tied to a release. Served under `/latest/docs/`, `/latest/meet/`, and `/X.Y/docs/`, etc.         |
| `layout.non_versioned_pages` | `account`, `pricing`, `support`, `openvidu-meet-vs-openvidu-platform`, `conditions`, `blog`, `about-us`, `research`, `acknowledgments` | Global pages shared across all versions. Served **once** at the site root (e.g. `/pricing/`).                 |
| `layout.assets`              | `assets`, `javascripts`, `stylesheets`, `search`                                                                                       | Static asset folders that also live at the root.                                                              |
| `layout.pinned_assets`       | `assets`, `javascripts`, `stylesheets`                                                                                                 | Of those, the ones whose root-absolute references inside versioned pages get pinned to the version folder.     |
| `layout.root_files`          | `index.html`, `index.md`, `404.html`, `robots.txt`, `llms.txt`, the four RSS/JSON feeds, `rss.xsl`                                     | Individual files promoted to the root. `sitemap.xml` is absent on purpose: it is copied and rewritten, not moved. |
| `layout.feeds`               | the four RSS/JSON feed files                                                                                                          | Rewritten wholesale (every `/X.Y/` occurrence) when promoted to the root.                                     |

`ovweb.yaml` is the single source of truth for publishing: the layout above, and every redirect
on the site.

**Adding a page.** If a new page starts a new non-versioned area, add its folder to
`layout.non_versioned_pages`; if it starts a new versioned section, add it to
`layout.versioned_pages`. Otherwise its links will not be rewritten and it will not be relocated
correctly.

## The core problem this tool solves

`mike` builds the **entire** MkDocs site — versioned _and_ non-versioned pages — into each
version folder. Two things follow:

1. **Duplication.** The pricing page, blog, etc. would be published once per version. We want a
   single canonical copy served at the root (`/pricing/`), always reflecting the most recent
   release.
2. **Broken links.** MkDocs Material emits **relative** links (e.g. `../../pricing/`). Once
   files are relocated — non-versioned pages moved to the root, versioned docs left under
   `/latest/` — those relative links no longer resolve.

`ovweb` therefore **post-processes mike's output** on the `gh-pages` branch to:

- Rewrite relative links into **absolute** paths that match the final layout.
- Move the non-versioned pages and root files out of the version folder and into the root.
- Fix the auxiliary files: the search index, `sitemap.xml`, the RSS feeds, `404.html`, and the
  AI-facing channel — every page's Markdown export plus `llms.txt`.
- Write the [generated redirects](docs/redirects.md), so `/X.Y/` and `/latest/` land on the docs.

## Commands

```
ovweb publish new    X.Y   Publish a brand-new minor and move `latest` onto it
ovweb publish latest X.Y   Re-publish the newest version in place, from main
ovweb publish past   X.Y   Re-publish an older minor, leaving the site root alone
ovweb deploy         X.Y   The primitive the three presets configure

ovweb postprocess    X.Y   Run ONLY the gh-pages post-processing, on a tree
ovweb redirects render|check|apply
ovweb lint [PATHS...] [--site DIR] [--against REF]   Authoring conventions the strict build cannot see
ovweb verify               Assert the invariants of a published tree
ovweb versions list        What is published, and which version branches exist
ovweb doctor [--pins]      Dependencies, pins, configuration and git state
```

Useful flags. `--dry-run`, `--verbose`/`-v`, `--json`, `--color`/`--no-color`, `--repo`, `--layout`
and `--remote` are **global**, and their canonical position is before the subcommand:
`ovweb --dry-run --verbose publish latest 3.8`. Writing them after the subcommand works too:
`ovweb` moves them to the front rather than failing with a parse error that is neither obvious
nor useful. Everything else in the table below belongs to a specific command.

| Flag                        | Effect                                                                                                                                                     |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--dry-run`                 | Resolve and print the plan — ordered steps, the redirects that would be installed, the git operations — and touch nothing. Implies `--no-push`.             |
| `--no-push`                 | Build and commit locally, push nothing. The everyday "let me look at it first" mode.                                                                        |
| `--tree PATH`, `--no-commit` | `postprocess` and `verify` only: work on a directory instead of a worktree, and leave it dirty.                                                             |
| `--keep-worktree`           | Leave the gh-pages worktree behind for inspection.                                                                                                          |
| `--force`                   | Post-process a tree that has already been post-processed. See the idempotence note in [Caveats](#caveats-and-observations).                                  |
| `-v` / `-vv`                | `-vv` logs the argv of every git and mike call.                                                                                                              |
| `--json`                    | One JSON object per step, for machine consumption.                                                                                                           |
| `--layout FILE`             | Use a different `ovweb.yaml` — for local experiments only.                                                                                                   |

## What a publish does

```
publish
 ├── doctor-style preflight     # mike installed, working tree clean
 ├── prepare-branches           # fast-forward gh-pages and X.Y from the remote; check out the build source
 ├── mike delete                # `publish latest` / `publish past` only, tolerant of a missing version
 ├── mike deploy                # build the version and commit it to gh-pages
 ├── worktree gh-pages          # a throwaway checkout, outside the repository
 │    └── postprocess           # the steps below
 ├── commit + push
 └── sync-branch                # `publish latest` only: rebase X.Y onto main, push with --force-with-lease
```

The post-processing steps, in order. `--dry-run` prints exactly this list, and
[`test_postprocess.py`](tests/unit/test_postprocess.py) asserts that it does.

| Step                   | When   | What                                                                                                                  |
| ---------------------- | ------ | --------------------------------------------------------------------------------------------------------------------- |
| `remove-overrides`     | always | Delete the version's `overrides/` theme folder, which is source, not output.                                          |
| `rewrite-versioned`    | always | Pin assets to the version, absolutise root links, point `canonical`/`og:url` at `/latest/`. Also each page's Markdown export, whose links need different patterns. |
| `rewrite-search-index` | always | Make every search location absolute.                                                                                  |
| `rewrite-non-versioned`| latest | Point versioned links at `/latest/`, strip the version from the promoted pages' own URLs, fix `404.html`, the feeds, and the AI-facing channel: the Markdown exports and `llms.txt`. |
| `promote-to-root`      | latest | Copy the asset folders and move the root files and non-versioned pages out to the site root.                          |
| `promote-sitemap`      | latest | Copy the version's sitemap to the root and rewrite it for the root URL scheme.                                        |
| `promote-search-index` | latest | Point the root index's versioned hits at `/latest/`. The version's own index keeps its version — see [docs/sitemaps-and-search.md](docs/sitemaps-and-search.md). |
| `repair-export-links`  | always | Point a link at the HTML page wherever the Markdown export it names does not exist. Checked against the finished tree, not the MkDocs config. |
| `strip-non-versioned`  | past   | Delete the root-served pages from the version folder instead. Tolerant: an old version may never have built some.     |
| `install-redirects`    | always | Write the generated redirect pages: the `files` rules plus the tree-resolved expansions, never shadowing a real page. |
| `mirror-unversioned`   | latest | Delete `/docs/` and `/meet/` and rebuild them as one redirect page per page of the newest version.                     |
| `alias-versions`       | always | Rebuild the legacy patch-version folders that alias the published minor as mirrors of its tree.                        |
| `prune-version-sitemap`| always | Drop the root-served pages from this version's sitemap and regenerate its `.gz`. The theme's version selector fetches this file — see [docs/sitemaps-and-search.md](docs/sitemaps-and-search.md). |
| `sync-version-sitemap` | always | List the version's generated redirects in that same sitemap, so the selector resolves a moved page through its stub.   |
| `sync-releases`        | always | Splice the newest release notes across versions — see [docs/releases-splice.md](docs/releases-splice.md).              |
| `commit`               | always | `git add --all` and commit — **locally**. The push happens afterwards, once the tree is known to be correct. |

Everything before `commit` touches no git at all, which is what makes
`ovweb postprocess --tree <copy> --no-commit` a deterministic unit.

### Nothing is pushed until the tree is correct

`mike` output is only half a publish: the version folder still holds the pages that belong at the
site root, their relative links resolve nowhere, and there is no redirect at the version root. So
`ovweb` never passes `--push` to mike. Everything — the delete, the build, the post-processing and
the commit — happens on the local `gh-pages`, and a single push follows once the tree is right. If
anything fails first, the local branch is reset to where it started (or deleted, if this was the
first deployment) and the remote is never touched. There is nothing to restore from, and no backup
branch to maintain.

Two consequences worth knowing:

- **The version branch is pushed after the site, not before.** A failed publish therefore leaves
  no new branch on the remote either.
- **Steps after the push are bookkeeping.** Pushing the version branch and rebasing it onto main
  record *which source* produced the published site. If one fails, the site is already live and
  correct, so it is reported with the command to retry rather than aborting.

### Why a worktree

Post-processing needs the `gh-pages` content, and checking that branch out in the main working
tree has three problems:

- **The tool's own files vanish.** Its sources, config and templates are not on `gh-pages`, and
  for a past version they are not on that version's branch either.
- **`.gitignore` is a main-only file**, so `site/` and `.cache/` become untracked *and* unignored
  the moment `gh-pages` is checked out, and `git add .` publishes them.
- **A failure half-way strands you** on `gh-pages` mid-move.

A throwaway worktree avoids all three, and the main tree never leaves `main`.

## Testing

```bash
pip install -e "./publish-tool[dev]"
cd publish-tool
pytest
ruff check . && ruff format --check .
```

What the tests cover, the export preprocessor and its differential build, and everything
`ovweb verify` asserts: [`docs/testing-and-verify.md`](docs/testing-and-verify.md).

## How it runs in CI

The four workflows (the PR gate, the manual publish, the weekly external-link check and the tool
tests) are documented in [`contributing/checks.md`](../contributing/checks.md).

## Dependency pins

[`pyproject.toml`](pyproject.toml) is the single place the publishing dependencies are declared,
with two extras: `build` (the real publish, including `mkdocs-material[imaging]`) and `validate`
(the same minus the imaging stack). `mkdocs-material` is also named as the base-image tag of
[`Dockerfile`](../Dockerfile) and [`Dockerfile.mike`](../Dockerfile.mike), and `ovweb doctor
--pins` fails when the three disagree. A different theme version builds different markup, and the
release-notes splice matches on that markup.

## Caveats and observations

- **Clean working tree required.** `mike` builds the site from the working tree, so a publish
  with uncommitted changes would ship them. `ovweb` refuses.
- **Post-processing is not idempotent.** A second pass would strip the version out of
  author-pinned links (the shield is single-shot) and fail on the already-moved directories.
  `ovweb` refuses to run on a tree whose version root is already a generated redirect; `--force`
  overrides it.
- **A publish only touches the version being published.** The one exception is the release-notes
  splice, which reaches into every other version folder. So a change to the rewriting rules
  reaches an old version only when that version is re-published.
- **The releases-content splice is coupled to two Material markup strings.** A theme upgrade that
  renames the `md-content__inner` article or the `md-nav--secondary` table-of-contents
  `aria-label` breaks it. It fails loudly rather than silently — a source-side failure aborts the
  publish, a destination-side one warns and leaves that page as built — so treat a
  `could not splice release notes` line in a publish log as something to fix, not noise.
- **Per-version search indexes are not updated by the splice.** It rewrites the rendered
  `index.html`, but each version's `search/search_index.json` still holds that version's original
  releases text. The page a visitor sees is current; in-version search results for the releases
  page may lag until that version is rebuilt.
- **Old branches do not generate `llms.txt` or the RSS feeds.** Their `mkdocs.yml` predates those
  plugins, so the past-version cleanup is tolerant of every root file it removes.
- **A version can be published without a branch.** `ovweb versions list` flags it; such a version
  cannot be re-published, because the branch is the source of truth for its content.
