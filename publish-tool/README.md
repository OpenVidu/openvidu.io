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

### Minor-grouped versioning (`X.Y`)

Documentation versions are grouped by **minor** release and named `X.Y` (e.g. `3.8`): one git
branch, one `gh-pages` folder and one version-selector entry per minor. The content of each
`X.Y` version always reflects the **newest patch** of that minor — patch releases do **not**
create new documentation versions:

| Event                                      | Command                    | Root pages | Version branch                            |
| ------------------------------------------ | -------------------------- | ---------- | ----------------------------------------- |
| New minor release (e.g. `3.9.0`)           | `ovweb publish new 3.9`    | Refreshed  | Created from `main`                       |
| Patch for the current minor (e.g. `3.8.1`) | `ovweb publish latest 3.8` | Refreshed  | Rebased onto `main`                       |
| Patch for an old minor (e.g. `3.7.2`)      | `ovweb publish past 3.7`   | Untouched  | Must already exist; edits committed there |

For a patch of the current minor, merge the docs to `main` first and add the patch's section to
the releases pages. For a patch of an old minor, commit to that version's branch first — the
branch, not `main`, is the source of truth for a past version.

---

## Table of contents

- [Background concepts](#background-concepts)
- [The core problem this tool solves](#the-core-problem-this-tool-solves)
- [Keeping the releases pages always up to date](#keeping-the-releases-pages-always-up-to-date)
- [Redirects](#redirects)
- [Commands](#commands)
- [What a publish does](#what-a-publish-does)
- [How the code is organised](#how-the-code-is-organised)
- [Link-rewriting reference](#link-rewriting-reference)
- [Testing](#testing)
- [How it runs in CI](#how-it-runs-in-ci)
- [Caveats and observations](#caveats-and-observations)

---

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
├── latest/         # alias → 3.9  (a real symlink, see "Redirects")
├── versions.json   # mike's version index (drives the version selector)
└── ...
```

`mike` commits to `gh-pages` using git plumbing and never checks that branch out. `ovweb` relies
on that: it does the post-processing in a throwaway `git worktree`, so the main working tree
never leaves `main`.

### Versioned vs. non-versioned pages

Every page belongs to one of two groups, declared in [`ovweb.yaml`](ovweb.yaml):

| Key                   | Value                                                                                                                                 | Meaning                                                                                                       |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `versioned_pages`     | `docs`, `meet`                                                                                                                        | Documentation tied to a release. Served under `/latest/docs/`, `/latest/meet/`, and `/X.Y/docs/`, etc.         |
| `non_versioned_pages` | `account`, `pricing`, `support`, `openvidu-meet-vs-openvidu-platform`, `conditions`, `blog`, `about-us`, `research`, `acknowledgments` | Global pages shared across all versions. Served **once** at the site root (e.g. `/pricing/`).                 |
| `assets`              | `assets`, `javascripts`, `stylesheets`, `search`                                                                                       | Static asset folders that also live at the root.                                                              |
| `pinned_assets`       | `assets`, `javascripts`, `stylesheets`                                                                                                 | Of those, the ones whose root-absolute references inside versioned pages get pinned to the version folder.     |
| `root_files`          | `index.html`, `index.md`, `404.html`, `robots.txt`, `llms.txt`, the RSS/JSON feeds, `rss.xsl`                          | Individual files promoted to the root. `sitemap.xml` is absent on purpose: it is copied and rewritten, not moved. |

`ovweb.yaml` is the single source of truth for publishing: the layout above, and every redirect
on the site.

**Adding a page.** If a new page starts a new non-versioned area, add its folder to
`non_versioned_pages`; if it starts a new versioned section, add it to `versioned_pages`.
Otherwise its links will not be rewritten and it will not be relocated correctly.

---

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
- Write the [generated redirects](#redirects), so `/X.Y/` and `/latest/` land on the docs.

---

## Keeping the releases pages always up to date

There are two releases pages — OpenVidu Meet (`meet/releases/`) and OpenVidu Platform
(`docs/releases/`) — and both are **versioned** pages. Left untouched, an old version's releases
page would only list the notes up to that version: a visitor browsing `3.5.0` would never see
the notes for `3.6.0`, `3.7.0`, … even though release notes are inherently global information.

Every version should serve the **full, most-recent** release notes, **without** dragging the
rest of the newest page along with them. Two complementary parts achieve that:

1. **Copy the content at publish time.** On every publish the **content** of the newest releases
   pages — the release notes body and the table of contents, nothing else — is spliced into the
   releases page of **every other version folder**, so each `/X.Y/…/releases/` lists the same
   complete changelog as `/latest/…/releases/`. Publishing the newest version pushes its notes
   outwards; re-publishing an older one pulls the current newest notes back in, so a rebuild
   does not regress it. See [`releases.py`](src/ovweb/releases.py).

2. **Jump to the viewed version (front-end).** Because the notes are now identical across
   versions, a small client-side script scrolls the visitor to the section matching the version
   they are browsing — opening `/3.5/meet/releases/` jumps to the `## 3.5.0` section (anchor
   `#350`). It lives in
   [`docs/javascripts/releases-scroll-to-version.js`](../docs/javascripts/releases-scroll-to-version.js)
   and is loaded only on the releases pages, via the `scrolltoversion` tag in their front matter
   (wired in [`docs/overrides/main.html`](../docs/overrides/main.html)). It is a no-op when the
   URL already has an anchor (so cross-page `#380` links are respected) or when there is no
   matching section (the `latest` alias stays at the top, newest first).

Four consequences worth keeping in mind:

- **Only the content travels; the page stays version-local.** Header, tabs, navigation menu,
  footer, asset URLs and Material's runtime config are left exactly as the destination version
  built them, so a visitor who opens `/3.4/docs/releases/` keeps browsing the **3.4**
  documentation instead of being sent to `/latest/` by every link around the notes. Nothing in
  the spliced fragments needs rewriting: the release notes' own links are authored as absolute,
  version-pinned URLs, and the table of contents only holds `#anchor` links. Both are verified
  before splicing, so a page that breaks the convention is reported instead of published with
  links resolving against the wrong version folder.
- **The outdated-version banner shows up there like anywhere else.** The destination page is the
  destination version's own, so Material flags it as outdated and the banner from
  `{% block outdated %}` appears — which is what tells the visitor that the documentation
  *around* the notes is old, even though the notes themselves are complete.
- **The canonical tag belongs to whichever publish last rewrote it.** Post-processing only
  touches the version being published, so a version's canonical is rewritten to `/latest/…` when
  that version is (re)published, not when another one is. An older folder keeps whatever its last
  publish produced until it is rebuilt.
- **The Markdown export does not travel.** The releases pages have an `index.md` beside them like
  any other page in the plugin's `sections`, but only the content of the HTML is spliced. The
  export a reader actually reaches is `/latest/<vp>/releases/index.md` — the one `llms.txt`
  references, and the newest version's own, so it is built rather than copied. An
  old version folder's export keeps that version's notes; nothing links to it.

---

## Redirects

GitHub Pages has no server-side redirects, and it serves `404.html` with a **404 status** — the
thing a crawler acts on before it runs any JavaScript. So every redirect on this site is a real,
generated HTML page answering 200 with a zero-delay meta refresh, declared as data in
[`ovweb.yaml`](ovweb.yaml). There is no client-side router.

Two families of rules exist, separated by what has to be written by hand:

- **`redirects.files`** — one rule, one page: a known path and where it goes.
- **`redirects.expand`** — one rule, many pages, enumerated from the published tree.

### `redirects.files` — a known path

A rule says where the page goes (`at`) and where it sends the visitor (`to`):

```yaml
- id: version-root
  at: version-root              # the named location for "<X.Y>/index.html"
  to: "docs/"
  canonical: "{site_url}/latest/docs/"
  body: "Redirecting to the OpenVidu Platform documentation…"
  when:
    # Versions 3.0–3.3 predate the /docs/ landing page: back then the getting started guide
    # *was* the Platform documentation index.
    - versions: "<3.4"
      to: "docs/getting-started/"
      body: "Redirecting to the OpenVidu getting started guide…"
```

`to` may carry a fragment (`../how-to-guides/#backup-and-restore`), which is how several pages
converging into one land on the section that absorbed them. The `canonical` should not repeat
the fragment: search engines normalise it away.

`versions` (and `when[].versions`) are [PEP 440](https://peps.python.org/pep-0440/) specifiers
evaluated with `packaging`, so `3.10` correctly sorts above `3.9` and legacy folders like
`3.0.0-beta1` fall in the range written for them. **At most one `when` entry may match a given
version** — an overlap is an error, not a silent first-match-wins, because that would make the
published redirect depend on the order of the file.

**A rule's `versions` gate must not be wider than its target's.** Gate a rule at the first version
that stopped shipping the old page, then check that the *successor* exists in every version from
there on — those are not always the same release. When they differ, the older band needs a `when`
override pointing at a page that version really has; without one the stub redirects into a 404,
which is worse than the 404 it replaced. `ovweb verify` rejects that — see the redirect-target
check below.

**Not every dead URL earns a redirect.** A page that was never part of a release should not have
its URL preserved, and neither should a generated API page for a class that has been deleted. The
exclusions are pinned in [`test_redirects.py`](tests/unit/test_redirects.py) as
`DELIBERATELY_UNCOVERED`, which fails both ways — if a listed URL gains a rule, and if an
unlisted dead URL loses one.

### `redirects.expand` — one rule, many pages

Every kind enumerates its pages from the **published tree** rather than from a list, under three
filters that make a bulk expansion safe to materialise as files:

- **Never shadow a real page.** A candidate path already holding a page ovweb did not generate is
  skipped, so an expansion cannot overwrite content — `ha/on-premises/` survives the
  provider-index rule with no exclusion list to maintain.
- **Never redirect into a 404.** A candidate whose target does not exist in that tree is skipped.
- **Never chain.** A target that is itself a generated redirect is followed to its final
  destination, so every stub answers in one hop.

Four kinds ship:

**`kind: cross-product`** — many single-page moves that differ only by path segments. `at`, `to`,
`canonical` and `body` may use `{version}` and any `values` key; one candidate per combination:

```yaml
- id: removed-provider-index
  kind: cross-product
  at: "{version}/docs/self-hosting/{edition}/{provider}/index.html"
  to: "install/"
  canonical: "{site_url}/latest/docs/self-hosting/{edition}/{provider}/install/"
  versions: ">=3.8"           # the release the consolidation belongs to
  values:
    edition:  [single-node, single-node-pro, elastic, ha]
    provider: [on-premises, aws, azure, gcp, digitalocean, oracle]
```

Gate it at the release the change belongs to — the filters keep the rule honest *inside* the
gate, they do not replace it.

**`kind: tree-rename`** — a directory moved. The pages are enumerated from the tree under `to`,
so every stub has a live target by construction; a page removed in the same release as the rename
gets no stub and needs its own `files` rule, which is right — its successor is a judgement call,
not a path substitution:

```yaml
- id: self-hosting-becomes-deployment
  kind: tree-rename
  from: "{version}/docs/self-hosting"
  to: "{version}/docs/deployment"
  versions: ">=3.9"
```

**`kind: version-alias`** — a retired version folder rebuilt as a full mirror of its minor.
`3.4.1/docs/x/` answers with a redirect to `/3.4/docs/x/`, one stub per page of the minor's tree,
targets absolute and version-pinned (the folder is not behind the `latest` symlink, and the
reader asked for that version). A folder is rebuilt whenever its minor is published; creating the
folders in the first place is `ovweb redirects apply`'s job, since no publish creates them from
nothing.

**`kind: unversioned-mirror`** — every page of the newest version answering at its unversioned
URL: `/docs/ai/live-captions/` → `/latest/docs/ai/live-captions/`. Enumerated from the newest
version's section folders, so it covers the exported `reference-docs/*.html` file URLs too, and a
versioned page that is itself a redirect is mirrored as its final destination.

### Ownership, and why the bulk scopes are wiped

Everything an expansion writes is **ovweb-owned**: the root section mirrors (`/docs/`, `/meet/`)
and the alias folders are deleted outright and rebuilt on every publish that touches them, never
reconciled page by page — a renamed or removed page would otherwise leave a stub redirecting into
a 404, and rebuilding makes that state unrepresentable. The wipe refuses to delete any file that
does not carry the generated marker, so it can never reach content. Inside version folders, where
stubs live next to real pages, `redirects apply` reconciles instead: it deletes generated stubs
no rule produces any more and rewrites the rest.

`ovweb verify` asserts the wholly-owned scopes as **set equality** against the same functions
that generate them: a missing stub means a URL 404s for crawlers again, an extra one means it may
redirect into a 404.

### Why a `files` target is relative

`latest` is a **symlink** to the newest version folder, so one file answers at both `/3.9/` and
`/latest/`. An absolute target would have to name a version, and would leak `/3.9/` to visitors
of the stable `/latest/` URL. A relative target is resolved by the browser against the document
URL, so the same bytes send `/latest/` to `/latest/docs/` and `/3.9/` to `/3.9/docs/` — with no
JavaScript involved. `ovweb` rejects an absolute target on a rule marked `relative` (the
default), and `ovweb verify` asserts it on the published bytes. The mirror and alias stubs are
the exception: each is served from exactly one URL, so their targets are absolute.

### What the generated page contains

Every element earns its place; see
[`redirect.html.j2`](src/ovweb/data/templates/redirect.html.j2).

| Element                                         | Why                                                                                                                                                 |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<meta http-equiv="refresh" content="0; url=…">` | The no-JavaScript path. Search engines treat a zero-delay meta refresh as a redirect and pass ranking signals through.                              |
| `<meta name="robots" content="noindex, follow">` | Keeps the stub out of search results while still letting link equity flow to the target.                                                             |
| `<link rel="canonical" href="…">`                | Consolidates every version's copy on one evergreen URL. Belt and braces — a `noindex` page's canonical is ignored — so `canonical: null` omits it.  |
| `location.replace(…)` forwarding query and hash  | No history entry, so Back still works, and `?a=1#b` survives the redirect.                                                                          |
| A real `<a>` in the body                         | Works when the refresh is blocked, and gives crawlers an edge to follow.                                                                            |

### Inspecting and applying them

```bash
ovweb redirects render 3.2      # print the `files` pages that would be installed for a version
ovweb redirects check           # every version resolves every rule to exactly one target
ovweb redirects apply --tree T  # reconcile EVERY generated redirect in a tree with the config
```

`redirects apply` is the maintenance entry point: it writes the `files` and expansion stubs of
every version folder (deleting stubs no rule produces any more), rebuilds the unversioned mirror
and the alias folders, and is how a rule reaches versions that are not being republished. With
the global `--dry-run` it reports what would change and writes nothing.

---

## Commands

```
ovweb publish new    X.Y   Publish a brand-new minor and move `latest` onto it
ovweb publish latest X.Y   Re-publish the newest version in place, from main
ovweb publish past   X.Y   Re-publish an older minor, leaving the site root alone
ovweb deploy         X.Y   The primitive the three presets configure

ovweb postprocess    X.Y   Run ONLY the gh-pages post-processing, on a tree
ovweb redirects render|check|apply
ovweb verify               Assert the invariants of a published tree
ovweb versions list        What is published, and which version branches exist
ovweb doctor [--pins]      Dependencies, pins, configuration and git state
```

Useful flags. `--dry-run`, `--verbose`/`-v`, `--json`, `--color`/`--no-color`, `--repo`, `--layout`
and `--remote` are **global** — click requires a group's options before the subcommand, so
`ovweb --dry-run --verbose publish latest 3.8` is the canonical form. Writing them after the
subcommand works too: `ovweb` moves them to the front rather than failing with a parse error that
is neither obvious nor useful. Everything else in the table below belongs to a specific command.

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

---

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
| `promote-search-index` | latest | Point the root index's versioned hits at `/latest/`. The version's own index keeps its version — see below.            |
| `repair-export-links`  | always | Point a link at the HTML page wherever the Markdown export it names does not exist. Checked against the finished tree, not the MkDocs config. |
| `strip-non-versioned`  | past   | Delete the root-served pages from the version folder instead. Tolerant: an old version may never have built some.     |
| `install-redirects`    | always | Write the generated redirect pages: the `files` rules plus the tree-resolved expansions, never shadowing a real page. |
| `mirror-unversioned`   | latest | Delete `/docs/` and `/meet/` and rebuild them as one redirect page per page of the newest version.                     |
| `alias-versions`       | always | Rebuild the legacy patch-version folders that alias the published minor as mirrors of its tree.                        |
| `prune-version-sitemap`| always | Drop the root-served pages from this version's sitemap and regenerate its `.gz`. The theme's version selector fetches this file — see below. |
| `sync-releases`        | always | Splice the newest release notes across versions.                                                                       |
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

---

## How the code is organised

The split is between **pure** modules — they take and return strings and dataclasses and touch
nothing else — and **impure** ones that own the filesystem, git and mike. Every behavioural risk
lives in the pure layer, which is why that is where the tests are.

| Module                                                     | Pure? | Responsibility                                                                    |
| ---------------------------------------------------------- | ----- | --------------------------------------------------------------------------------- |
| [`cli.py`](src/ovweb/cli.py)                               | –     | Parse flags, build a plan, hand off. No decisions.                                |
| [`model.py`](src/ovweb/model.py)                           | ✔     | Frozen value objects.                                                             |
| [`config.py`](src/ovweb/config.py)                         | ✔     | Load and validate `ovweb.yaml`.                                                   |
| [`versions.py`](src/ovweb/versions.py)                     | ✔     | `X.Y` names, ordering, specifier matching, `versions.json`.                       |
| [`sources.py`](src/ovweb/sources.py)                       | ✔     | What a page is made of, for the sitemap's `<lastmod>`.                             |
| [`rewrite/versioned.py`](src/ovweb/rewrite/versioned.py)   | ✔     | Asset pinning, root links, cookie base URL, `canonical`/`og:url` → `/latest/`.     |
| [`rewrite/nonversioned.py`](src/ovweb/rewrite/nonversioned.py) | ✔ | Version stripping with the shield, `404.html`, the feeds.                         |
| [`rewrite/markdown.py`](src/ovweb/rewrite/markdown.py)     | ✔     | The same rules for the Markdown exports and `llms.txt`.                            |
| [`rewrite/search_index.py`](src/ovweb/rewrite/search_index.py) | ✔ | Absolutise search locations.                                                     |
| [`rewrite/sitemap.py`](src/ovweb/rewrite/sitemap.py)       | ✔     | Root promotion and `<url>` block pruning.                                         |
| [`releases.py`](src/ovweb/releases.py)                     | ✔     | Splice release notes between versions.                                            |
| [`redirects.py`](src/ovweb/redirects.py)                   | ✔     | Resolve the `files` rules and render any redirect page.                            |
| [`expand.py`](src/ovweb/expand.py)                         | –     | Enumerate the expansion kinds from the published tree, under the three filters.    |
| [`plan.py`](src/ovweb/plan.py)                             | ✔     | The ordered publish description `--dry-run` prints.                               |
| [`fsops.py`](src/ovweb/fsops.py)                           | –     | File walking, byte-preserving rewrites, deterministic gzip, moves and copies.     |
| [`gitrepo.py`](src/ovweb/gitrepo.py)                       | –     | The git facade, including the worktree context manager.                           |
| [`mikewrap.py`](src/ovweb/mikewrap.py)                     | –     | `mike deploy` / `mike delete`.                                                    |
| [`discovery.py`](src/ovweb/discovery.py)                   | –     | Which versions exist, from the repository or from a published tree.                |
| [`pipeline/postprocess.py`](src/ovweb/pipeline/postprocess.py) | – | The step table above.                                                             |
| [`pipeline/publish.py`](src/ovweb/pipeline/publish.py)     | –     | Branch preparation, mike, worktree, commit, branch sync.                          |
| [`verify.py`](src/ovweb/verify.py)                         | –     | Invariants of a published tree.                                                   |
| [`doctor.py`](src/ovweb/doctor.py)                         | –     | Preflight checks, including the pin agreement.                                    |
| [`mkdocs_hook.py`](mkdocs_hook.py)                         | –     | Set each page's `<lastmod>` from git; feed llms.txt the pages' own frontmatter.    |

---

## Link-rewriting reference

The final link conventions, for version `3.9`:

| Context                              | From (mike output) | To (final)                                     |
| ------------------------------------ | ------------------ | ---------------------------------------------- |
| Versioned page → asset (raw HTML)    | `src="/assets/…"`  | `src="/3.9/assets/…"` (version-pinned)         |
| Versioned page → asset (Markdown)    | `../../assets/…`   | _(left relative by mike; stays version-local)_ |
| Versioned page → non-versioned page  | `../../pricing/`   | `/pricing/`                                    |
| Versioned page → home                | `../..`            | `/`                                            |
| Canonical / `og:url` on versioned page | `…/3.9/docs/…`   | `…/latest/docs/…`                              |
| Non-versioned page → versioned page  | `../docs/`         | `/latest/docs/`                                |
| Canonical / `og:url` / JSON-LD on non-versioned page | `…/3.9/…` | `…/…` (version removed)                 |
| `404.html` → versioned page          | `/docs/`           | `/latest/docs/`                                |
| Versioned page → root file (RSS feed) | `../../feed_rss_created.xml` | `/feed_rss_created.xml`               |
| Version search index → versioned page | `docs/`           | `/3.9/docs/` (explicit version)                |
| Root search index → versioned page    | `docs/`           | `/latest/docs/`                                |
| Search index → non-versioned page    | `pricing/`         | `/pricing/`                                    |
| Root sitemap → versioned page        | `/3.9/docs/`       | `/latest/docs/`                                |
| Root sitemap → non-versioned page    | `/3.9/pricing/`    | `/pricing/`                                    |

And the same rules again for the Markdown exports, whose links are absolute rather than relative:

| Reference | mike writes | The publish makes it |
| --- | --- | --- |
| Versioned export → versioned page      | `…/3.9/docs/…`    | `…/3.9/docs/…` (kept, as above) |
| Versioned export → non-versioned page  | `…/3.9/pricing/`  | `…/pricing/`                    |
| Versioned export → home (`index.md`)   | `…/3.9/index.md`  | `…/index.md`                    |
| Promoted export → versioned page       | `…/3.9/docs/…`    | `…/latest/docs/…`               |
| Promoted export → non-versioned page   | `…/3.9/pricing/`  | `…/pricing/`                    |
| `llms.txt`                             | as promoted       | as promoted                     |
| Any export → a root-relative target    | `](/pricing/)`    | `](https://openvidu.io/pricing/)` |
| Any export → an export that does not exist | `](…/account/index.md)` | `](…/account/)`            |

### The Markdown exports and `llms.txt`

Every page listed in the `mkdocs-llmstxt` plugin's `sections` is published twice: as
`index.html`, and as an `index.md` beside it. `llms.txt` indexes those exports, and together they
are the site's AI-facing channel.

Neither half of an `llms.txt` entry comes from `mkdocs.yml`. The `on_page_content` half of
[`mkdocs_hook.py`](mkdocs_hook.py) replaces both with the page's own frontmatter:

* the **description**, which the plugin would otherwise take from the value beside the path in
  `mkdocs.yml`. That is what lets a `sections` entry be a glob — the plugin's own behaviour is to
  give every page a glob matches the *same* description.
* the **link text**, which the plugin takes from `page.title`. MkDocs resolves that to the *nav
  label* when the nav entry has one, so most entries would render as `[Install]`, `[Overview]` or
  `[Releases]` — fine beside a parent in a sidebar, useless in a flat list.

A listed page missing either one fails the build.

They need their own rewrites for one reason: **the plugin makes every link absolute**, resolved
against the build's `site_url` — which mike makes versioned. So an export comes out of the build
with every internal link pinned to the version that produced it, and the HTML patterns cannot
reach any of them, because they match `href="…"` and Markdown has no `href`.

Which rule applies depends on where the export is served from, exactly as it does for HTML — and
so the version-vs-`latest` asymmetry is the same one the two search indexes have, for the same
reason.

There is deliberately **no `llms-full.txt`**. The plugin can concatenate every export into one
file, and once `sections` covered every page that reached 2.8 MB — roughly 700k tokens, which
nothing can load, duplicating content the individual exports already serve. `llms.txt` as an index
plus on-demand page fetches is the spec's model and the one that works at this size.

Then two rules apply to *every* export, because they are about the form of a link rather than
its target — and both exist because the plugin is inconsistent in ways only the publish can settle:

- **Root-relative targets are made absolute.** The plugin absolutises a *relative* link but
  returns a root-relative one untouched, so which form an export handed out came down to how the
  author happened to write it. This cannot be fixed in the build: the plugin resolves against
  `site_url`, which mike makes versioned, so absolutising there yields `/3.8/pricing/` — a page
  served only from the root, and therefore a 404.
- **A link naming an export that does not exist is pointed at the page instead.** The plugin
  appends `index.md` to every directory link *without checking the target has an export*, and only
  pages in its `sections` list get one. Listing more pages shrinks the problem but cannot close
  it: `docs/reference-docs/` is vendored TypeDoc output with no Markdown source, and a JavaScript
  shell like `/account/` would export as a bare heading. The repair reads the real set of exports
  off the tree, so it needs no list to keep in step.

And one deliberate difference from the HTML:

- **A promoted export does not shield an author's pin to the version being published.** The HTML
  does (below), but in Markdown a hand-written pin and the plugin's absolutised link are the same
  bytes, and the plugin wrote almost all of them. A pin to a *different* version — the form a
  deliberately archival link takes, as when release notes link back to the release before — is
  untouched either way.

### The two sitemaps, and the version selector

There are two, and only one of them is for search engines.

| Sitemap | Read by | Contains |
| --- | --- | --- |
| `sitemap.xml` | crawlers — `robots.txt` names it, and it is a plain `urlset`, not an index | every URL the site serves, versioned pages as `/latest/…` |
| `<X.Y>/sitemap.xml` | **the theme's version selector, at runtime** | that version's own pages, plus its version root; *not* the root-served pages |

The per-version copy is what makes "switch version and keep reading the same page" work. When a
reader picks another version, Material's `setupVersionSelector` fetches `sitemap.xml` under the
selected version, strips the current version prefix off the path they are on, and looks the
remainder up. Found → they land on the same page in the new version. Not found, or the fetch
failed → they are dropped on the version root, which our generated redirect then sends to the docs
index.

Two properties of that file are therefore load-bearing, and **both fail silently**:

- **The version-root entry must be present.** The selector takes the longest common prefix of
  every URL in the sitemap and requires that prefix to itself be an entry before it resolves
  anything. With only page entries left, the prefix is still `https://openvidu.io/<X.Y>/` but is
  no longer in the file, and every switch falls back to the version root.
- **The root-served pages must be pruned.** mike builds the whole site into the version folder, so
  the sitemap it writes lists `<X.Y>/pricing/` and friends — URLs that never resolve, because
  those pages are moved to the root. The selector is shown on root pages too, so a reader on
  `/pricing/` picking 3.6 would be sent to `/3.6/pricing/`, a 404. Pruned, they fall back to the
  version root, which is right: that page has no per-version counterpart.

Nothing in the built site *links* to this file — the only reference is that `fetch()` in the
theme's JavaScript, which no link checking or grepping finds. `ovweb verify` asserts all three
conditions and [`tests/unit/test_rewrite_sitemap.py`](tests/unit/test_rewrite_sitemap.py) pins
them.

#### Where `<lastmod>` comes from

MkDocs initialises `Page.update_date` to the build date for every page and its sitemap template
emits exactly that, so the field would claim that every URL on the site changed on every publish —
no per-page signal, and false often enough to teach a crawler to ignore the field entirely.

The `on_env` half of [`mkdocs_hook.py`](mkdocs_hook.py) sets `update_date` from git instead, using
[`sources.py`](src/ovweb/sources.py): one `git log --name-only` pass gives the last commit date of
every file, and a page's date is the **newest across the page and the transitive closure of the
`--8<--` snippets it includes**. Most pages assemble their content from `shared/`, so without the
closure a rewritten shared install step would move no date at all on the pages that display it.

`on_env` is the only hook that can do this: MkDocs renders the theme's static templates —
`sitemap.xml` among them — *before* it renders the pages, so `on_page_content` runs too late.
Nothing in the post-processing needs to know: `promote_root_sitemap` only rewrites URL substrings,
so the values flow into the root sitemap untouched.

Two deliberate behaviours:

- **A generated page carries no `<lastmod>` at all.** The blog's archive, category and pagination
  views have no source file, so inventing a date for them would be the same lie in miniature; the
  spec makes the field optional per URL. They do, however, get a **title and description** from the
  same hook, since having no frontmatter left them serving `site_description` and a paginated view
  sharing a byte-identical `<title>` with the view it pages. Both are derived from the view itself
  (its own heading, the number of posts it lists, its page number), so a month or category that
  does not exist yet is described correctly the first time it appears.
- **Anything that stops git answering falls back to the build date, at INFO level.** A shallow
  clone is the important one — `git log` still succeeds there but reports the fetched commit for
  every path, which is silently wrong rather than absent, so it is detected and skipped.
  `validate-web.yaml` checks out shallow; `publish-web.yaml` sets `fetch-depth: 0`. It must stay
  INFO because `mkdocs build --strict` fails on a warning.

### The two search indexes

There are two, and they say different things, because **a page loads the index that sits beside
it**: Material records the folder to resolve against in its runtime config (`"base": "../.."`),
which the publish deliberately leaves relative.

| Index | Loaded by | A hit on versioned docs points at |
| --- | --- | --- |
| `<X.Y>/search/search_index.json` | pages under `/X.Y/docs/`, `/X.Y/meet/` | `/X.Y/docs/…` — the same version |
| `search/search_index.json` | the pages served from the site root | `/latest/docs/…` |

The version's own index has to keep its version, or searching inside the 3.4 documentation would
return 3.8 pages. The root index is a *copy* of the newest version's, so it inherits that
version — and it must not keep it: it is served on the evergreen root pages, `/latest/…` is the
canonical URL of the page being linked, and a pinned URL goes stale at the next release. Every
other root-to-versioned reference (page links, the sitemap, `llms.txt`, the canonicals) already
uses `/latest/`.

Author-written, version-pinned links to versioned pages (`/3.4/docs/…`, used by the
release-notes links in blog posts) are **shielded** while the version is stripped from a promoted
page, and restored afterwards. Getting that wrong would silently send every historical release
note to the newest documentation, which is why it has its own tests.

The releases pages are not in this table: only their content is copied between version folders,
so every link on the page follows the rows above for the version it lives in, and nothing inside
the copied content is rewritten because those links are authored absolute and version-pinned.

---

## Testing

```bash
pip install -e "./publish-tool[dev]"
cd publish-tool
pytest
ruff check . && ruff format --check .
```

The tests concentrate on the pure layer, with hand-written minimal fixtures rather than captured
pages: a real built page is ~100 KB of theme chrome, and the substitutions only ever look at a
few characters around a link.

Three of them are worth knowing about, because they are what keeps the rest honest:

- **The synthetic tree is derived from the configuration, not listed.**
  [`test_postprocess.py`](tests/unit/test_postprocess.py) builds it from the real `ovweb.yaml`
  layout and materialises every redirect rule's target from the rules themselves, so a page or a
  rule added to the config is covered without touching the fixture.
- **A tree that has just been post-processed must `verify` clean**
  ([`test_verify.py`](tests/unit/test_verify.py)). That makes `verify` a real post-publish signal:
  anything it reports right after a publish is something the pipeline failed to do.
- **The printed plan must match the steps that run.** `--dry-run` is only useful if it is the
  truth, so the pipeline is run against a recording reporter and compared to `plan.py`, in order.

### The export preprocessor

[`llmstxt_preprocess.py`](llmstxt_preprocess.py) replaces the `mkdocs-llmstxt` plugin's own
`autoclean`, which `mkdocs.yml` turns off. It has to be a replacement rather than an addition,
because the plugin runs `autoclean` **before** the `preprocess` hook and `autoclean` deletes every
`<img>` and `<svg>` — so by the time a hook sees the page, the alt text, the comparison-table icons
and the tab labels are already gone.

Everything `autoclean` did is reimplemented, and four things deliberately differ. They share one
premise: an assistant cannot see an image or watch a video, so the asset URL is worthless to it
while the words describing the asset are not.

| Deviation | Why |
| --- | --- |
| An `<img>` becomes its `alt` text | Most of the site's images carry informative alt text, all of which `autoclean` discards. Images with no usable alt are still removed, and only one of a Material light/dark pair contributes, or the text appears twice. |
| A comparison-table icon becomes `Yes` / `No` / `In progress` | The markup already says which — `class="twemoji compare-table-icon-yes"` — so the table exports as data with no change to the content. |
| A link whose only content is an image or video becomes that asset's alt text, unlinked | `autoclean` removes an `<a>` around an `<img>` but not around a `<video>`, so markdownify writes an empty link. |
| Tab labels are kept, as a bold line before each tab's block | Without them a tabbed block is a run of code blocks with nothing saying which is Linux, Windows or macOS — silently ambiguous rather than visibly missing. |

Two layers of checking, because "identical to `autoclean` except on purpose" is the whole promise:

- [`tests/unit/test_llmstxt_preprocess.py`](tests/unit/test_llmstxt_preprocess.py) runs the module
  and the plugin's real `autoclean` over the same markup and requires **byte-identical** output for
  every rule that is not a deviation, individually and all at once.
- A **differential build** proves it over the real site. Build once as configured, once with
  `autoclean: true` and the `preprocess` line removed, then diff the exports: every difference must
  be one of the four above.

  ```bash
  mkdocs build --strict -d /tmp/withhook
  # then flip autoclean to true, drop the preprocess line, and:
  mkdocs build --strict -d /tmp/baseline
  diff -r /tmp/baseline /tmp/withhook
  ```

  Run this after a plugin upgrade, or after changing any rule in the module.

### `verify`

`ovweb verify` asserts the invariants of a published tree: every version folder has a redirect at
its root with a relative target, no promoted page claims a versioned URL as its own, every version
folder carries a correctly pruned sitemap, every search location is absolute, nothing served from
the root pins the version `latest` points at, no versioned export links to a root-served page
under its version, no export links to another export that does not exist, every `<lastmod>` in the
root sitemap is a real date that is not in the future, the unversioned mirror and every alias
folder are exactly the sets their rules generate, no generated redirect points at a page that does
not exist or at another redirect, and `versions.json` agrees with the folders on disk.

The redirect-target check earns its place: a redirect into a 404 costs the visitor a second hop to
reach nothing and tells a crawler the content moved somewhere it did not. The chain half matters
because the expansions collapse chains at generation time, so one surviving to a published tree
means a `files` rule was pointed at another rule's stub.

The sitemap check is the one worth understanding, because it guards a feature that fails silently.
It asserts three things about `<X.Y>/sitemap.xml` — that it exists, that it has the version-root
entry, and that it lists no root-served page — each of which turns the version selector's
"keep the reader on the same page" behaviour off on its own. `rewrite/sitemap.py` explains why.
A publish only fixes its own version, so the findings for the others are the to-do list; the fix
is to publish each version, or to restore the sitemaps from history if they were lost without a
content change.

---

## How it runs in CI

[`.github/workflows/publish-web.yaml`](../.github/workflows/publish-web.yaml) is a manual
`workflow_dispatch` with three inputs: `command` (`new` / `latest` / `past`), `version`, and
`dry_run`. It installs the tool **non-editable** — publishing a past version checks out that
version's branch, where the package does not exist, so it has to live in `site-packages` —
publishes, and then runs `ovweb verify`.

There is no backup-branch step and no force-push recovery path, because a failed publish never
reaches the remote (see [Nothing is pushed until the tree is
correct](#nothing-is-pushed-until-the-tree-is-correct)).

[`.github/workflows/validate-web.yaml`](../.github/workflows/validate-web.yaml) runs on every PR:
`ovweb doctor --pins`, `ovweb redirects check`, and `mkdocs build --strict`.
[`.github/workflows/test-tools.yaml`](../.github/workflows/test-tools.yaml) runs `pytest` and
`ruff` when anything in this folder changes.

### Dependency pins

[`pyproject.toml`](pyproject.toml) is the single place the publishing dependencies are declared,
with two extras: `build` (the real publish, including `mkdocs-material[imaging]`) and `validate`
(the same minus the imaging stack). `mkdocs-material` is also named as the base-image tag of
[`Dockerfile`](../Dockerfile) and [`Dockerfile.mike`](../Dockerfile.mike), and `ovweb doctor
--pins` fails when the three disagree. A different theme version builds different markup, and the
release-notes splice matches on that markup.

---

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
