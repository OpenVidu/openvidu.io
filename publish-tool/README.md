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
- [Testing and parity](#testing-and-parity)
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
| `root_files`          | `index.html`, `index.md`, `404.html`, `robots.txt`, `llms.txt`, `llms-full.txt`, the RSS/JSON feeds, `rss.xsl`                          | Individual files promoted to the root. `sitemap.xml` is absent on purpose: it is copied and rewritten, not moved. |

`ovweb.yaml` is the single source of truth for both halves of publishing. The MkDocs build reads
it too, through [`mkdocs_hook.py`](mkdocs_hook.py), so the 404 router compiles its patterns from
the same data rather than from a hardcoded list somebody has to remember to update.

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
- Fix the auxiliary files: the search index, `sitemap.xml`, `llms.txt`, the RSS feeds and
  `404.html`.
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
- **The LLM Markdown companion does not travel.** Pages listed in the `mkdocs-llmstxt` plugin's
  `sections` also get an `index.md` next to their `index.html`, but old version folders have no
  `llms.txt` at all (the past-version path removes it, since those branches predate the plugin),
  so nothing there ever links to that companion. Only `/latest/<vp>/releases/index.md`, the one
  `llms.txt` references, matters — and it is built, not copied.

---

## Redirects

GitHub Pages has no server-side redirects, so every redirect on the site is client-side. They
are declared in [`ovweb.yaml`](ovweb.yaml) as data — a `from` and a `to`, optionally scoped to a
range of versions — and split into two kinds by what they can be.

### `redirects.files` — a known path

Materialised as HTML pages in the published tree. A rule says where the page goes (`at`) and
where it sends the visitor (`to`):

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
      body: "Redirecting to the OpenVidu Platform getting started guide…"
```

`versions` (and `when[].versions`) are [PEP 440](https://peps.python.org/pep-0440/) specifiers
evaluated with `packaging`, so `3.10` correctly sorts above `3.9` and legacy folders like
`3.0.0-beta1` fall in the range written for them. **At most one `when` entry may match a given
version** — an overlap is an error, not a silent first-match-wins, because that would make the
published redirect depend on the order of the file.

Three rules ship today: the version root, `/X.Y/docs/getting-started/` → `/X.Y/docs/` for 3.4
and later, and `/X.Y/docs/` → `/X.Y/docs/getting-started/` for 3.0–3.3, which fixes a set of
URLs that used to be hard 404s.

### Why every target is relative

`latest` is a **symlink** to the newest version folder, so one file answers at both `/3.9/` and
`/latest/`. An absolute target would have to name a version, and would leak `/3.9/` to visitors
of the stable `/latest/` URL. A relative target is resolved by the browser against the document
URL, so the same bytes send `/latest/` to `/latest/docs/` and `/3.9/` to `/3.9/docs/` — with no
JavaScript involved. `ovweb` rejects an absolute target on a rule marked `relative` (the
default), and `ovweb verify` asserts it on the published bytes.

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

### `redirects.patterns` — a shape of path

A pattern cannot be a file, because there is no single path to put it at. These are compiled
into the 404 router ([`docs/overrides/404.html`](../docs/overrides/404.html)) through
[`mkdocs_hook.py`](mkdocs_hook.py), which is the page GitHub serves for any URL that matches no
file. Two families ship today:

- **Legacy exact-patch URLs.** Versions used to be published per patch release (`/3.4.1/…`,
  `/3.0.0-beta2/…`) and are now grouped by minor, so a first segment with a third component is a
  legacy URL and goes to the minor folder.
- **A versioned section without a version.** `/docs/self-hosting/` → `/latest/docs/self-hosting/`.

Patterns are tried in order and the first match wins, so the order in `ovweb.yaml` is behaviour.

### Inspecting them

```bash
ovweb redirects render 3.2      # print the pages that would be installed for a version
ovweb redirects check           # every version resolves every rule to exactly one target
ovweb redirects apply --tree T  # write the file redirects into every version folder of a tree
```

`redirects apply` exists so a rule can reach versions that are not being rebuilt — which is how
the `/3.0/docs/` dead end gets fixed without republishing 3.0 from its own branch.

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

Useful flags:

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

The post-processing steps, in order. `--dry-run` prints exactly this list.

| Step                   | When   | What                                                                                                                  |
| ---------------------- | ------ | --------------------------------------------------------------------------------------------------------------------- |
| `remove-overrides`     | always | Delete the version's `overrides/` theme folder, which is source, not output.                                          |
| `rewrite-versioned`    | always | Pin assets to the version, absolutise root links, point `canonical`/`og:url` at `/latest/`.                            |
| `rewrite-search-index` | always | Make every search location absolute.                                                                                  |
| `rewrite-non-versioned`| latest | Point versioned links at `/latest/`, strip the version from the promoted pages' own URLs, fix `404.html`, `llms.txt`, the feeds. |
| `promote-to-root`      | latest | Copy the asset folders and move the root files and non-versioned pages out to the site root.                          |
| `strip-non-versioned`  | past   | Delete the root-served pages from the version folder instead. Tolerant: an old version may never have built some.     |
| `install-redirects`    | always | Write the generated redirect pages.                                                                                   |
| `promote-sitemap`      | latest | Copy the version's sitemap to the root and rewrite it for the root URL scheme.                                        |
| `remove-version-sitemap`| always | Delete this version's sitemap. Nothing referenced it: only the root sitemap is published. |
| `sync-releases`        | always | Splice the newest release notes across versions.                                                                      |
| `commit`               | always | `git add --all` and commit — **locally**. The push happens afterwards, once the tree is known to be correct. |

Steps 1–10 touch no git at all. That is what makes `ovweb postprocess --tree <copy> --no-commit`
a deterministic unit, and it is what the [parity gate](#testing-and-parity) compares.

### Nothing is pushed until the tree is correct

`mike` output is only half a publish: the version folder still holds the pages that belong at the
site root, their relative links resolve nowhere, and there is no redirect at the version root. The
shell ran `mike deploy --push`, so **that** was what went live, and only then did the
post-processing start. A failure in between left the broken state published, and recovering meant
force-pushing a backup branch.

`ovweb` never passes `--push` to mike. Everything — the delete, the build, the post-processing and
the commit — happens on the local `gh-pages`, and a single push follows once the tree is right. If
anything fails first, the local branch is reset to where it started (or deleted, if this was the
first deployment) and the remote is never touched. So there is nothing to restore from, and no
backup branch to maintain.

Two consequences worth knowing:

- **The version branch is pushed after the site, not before.** A failed publish therefore leaves
  no new branch on the remote either.
- **Steps after the push are bookkeeping.** Pushing the version branch and rebasing it onto main
  record *which source* produced the published site. If one fails, the site is already live and
  correct, so it is reported with the command to retry rather than aborting.

### Why a worktree

Post-processing needs the `gh-pages` content, but checking that branch out in the main working
tree — what the shell implementation did — has three problems:

- **The tool's own files vanish.** Its sources, config and templates are not on `gh-pages`, and
  for a past version they are not on that version's branch either.
- **`.gitignore` is a main-only file**, so `site/` and `.cache/` become untracked *and* unignored
  the moment `gh-pages` is checked out, and `git add .` publishes them. That is how 729 files of
  build cache ended up committed on `gh-pages`.
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
| [`rewrite/versioned.py`](src/ovweb/rewrite/versioned.py)   | ✔     | Asset pinning, root links, cookie base URL, `canonical`/`og:url` → `/latest/`.     |
| [`rewrite/nonversioned.py`](src/ovweb/rewrite/nonversioned.py) | ✔ | Version stripping with the shield, `404.html`, `llms.txt`, the feeds.             |
| [`rewrite/search_index.py`](src/ovweb/rewrite/search_index.py) | ✔ | Absolutise search locations.                                                     |
| [`rewrite/sitemap.py`](src/ovweb/rewrite/sitemap.py)       | ✔     | Root promotion and `<url>` block pruning.                                         |
| [`releases.py`](src/ovweb/releases.py)                     | ✔     | Splice release notes between versions.                                            |
| [`redirects.py`](src/ovweb/redirects.py)                   | ✔     | Resolve rules for a version and render the pages.                                 |
| [`plan.py`](src/ovweb/plan.py)                             | ✔     | The ordered publish description `--dry-run` prints.                               |
| [`fsops.py`](src/ovweb/fsops.py)                           | –     | File walking, byte-preserving rewrites, deterministic gzip, moves and copies.     |
| [`gitrepo.py`](src/ovweb/gitrepo.py)                       | –     | The git facade, including the worktree context manager.                           |
| [`mikewrap.py`](src/ovweb/mikewrap.py)                     | –     | `mike deploy` / `mike delete`.                                                    |
| [`discovery.py`](src/ovweb/discovery.py)                   | –     | Which versions exist, from `versions.json` and the branches.                      |
| [`pipeline/postprocess.py`](src/ovweb/pipeline/postprocess.py) | – | The step table above.                                                             |
| [`pipeline/publish.py`](src/ovweb/pipeline/publish.py)     | –     | Branch preparation, mike, worktree, commit, branch sync.                          |
| [`verify.py`](src/ovweb/verify.py)                         | –     | Invariants of a published tree.                                                   |
| [`doctor.py`](src/ovweb/doctor.py)                         | –     | Preflight checks, including the pin agreement.                                    |
| [`mkdocs_hook.py`](mkdocs_hook.py)                         | –     | Expose `ovweb.yaml` to the MkDocs templates.                                      |

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
| Search index → versioned page        | `docs/`            | `/3.9/docs/` (explicit version)                |
| Search index → non-versioned page    | `pricing/`         | `/pricing/`                                    |
| Root sitemap → versioned page        | `/3.9/docs/`       | `/latest/docs/`                                |
| Root sitemap → non-versioned page    | `/3.9/pricing/`    | `/pricing/`                                    |

Note the asymmetry: the **search index keeps the explicit version** for versioned pages, so a
search inside `3.4` links to `3.4` docs, while page links use the `latest` alias.

Author-written, version-pinned links to versioned pages (`/3.4/docs/…`, used by the
release-notes links in blog posts) are **shielded** while the version is stripped from a promoted
page, and restored afterwards. Getting that wrong would silently send every historical release
note to the newest documentation, which is why it has its own tests.

The releases pages are not in this table: only their content is copied between version folders,
so every link on the page follows the rows above for the version it lives in, and nothing inside
the copied content is rewritten because those links are authored absolute and version-pinned.

---

## Testing and parity

```bash
pip install -e "./publish-tool[dev]"
cd publish-tool
pytest
ruff check . && ruff format --check .
```

The tests concentrate on the pure layer, with hand-written minimal fixtures rather than captured
pages: a real built page is ~100 KB of theme chrome, and the substitutions only ever look at a
few characters around a link. Realism is the parity gate's job.

### The parity gate

The check that `ovweb` turns a built tree into the same published tree the shell implementation
did. It runs **one** `mike` build and post-processes two copies of it, so nothing that varies
between builds — timestamps, privacy-plugin downloads, image optimisation — can enter the
comparison; what is left is purely the post-processing.

```bash
pip install "./publish-tool[build,dev]"

# LEGACY_REF is a commit from before the migration, where the shell scripts still exist.
export LEGACY_REF=<sha>
publish-tool/tests/parity/run_parity.sh 3.99 latest   # a new minor
publish-tool/tests/parity/run_parity.sh 3.8  latest   # the newest, rebuilt in place
publish-tool/tests/parity/run_parity.sh 3.2  past     # an old minor, older configuration
```

[`compare.py`](tests/parity/compare.py) compares the two trees and asserts each intentional
difference individually rather than filtering a text diff by eye. Gzip members are compared
decompressed — the shell's `gzip -k -f` wrote the source mtime into the header, so an unchanged
sitemap produced a new blob on every publish, and decompressing makes that churn invisible here
by construction. The expected differences are:

| Difference                                                    | Why                                                                                    |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `<X.Y>/index.html`, `<X.Y>/docs/index.html`, `<X.Y>/docs/getting-started/index.html` | The generated redirects replace the hand-written stub and add two the shell could not express. |
| `<X.Y>/sitemap.xml`, `<X.Y>/sitemap.xml.gz`                   | The published version's sitemap is removed rather than pruned.                           |
| `.cache/**`, `site/**`                                        | Not in a fresh worktree, so they can no longer be committed by accident.                |

Anything else is a bug. Run the gate before merging a change to the rewriting logic; it is not
in CI because it needs a full build (see
[`.github/workflows/test-tools.yaml`](../.github/workflows/test-tools.yaml)).

### `verify`

`ovweb verify` asserts the invariants of a published tree: every version folder has a redirect at
its root with a relative target, no promoted page claims a versioned URL as its own, no version
folder still carries a sitemap, every search location is absolute, and `versions.json` agrees
with the folders on disk.

The sitemap check reports any version folder that still carries a sitemap. A publish only removes
its own, so versions published before that change keep theirs until they are next published — the
findings are the to-do list. A one-off cleanup clears them all without rebuilding anything:

```bash
git worktree add /tmp/ghp gh-pages
find /tmp/ghp -maxdepth 2 -regextype posix-extended \
  -regex '.*/[0-9]+\.[0-9]+/sitemap\.xml(\.gz)?' -delete
git -C /tmp/ghp commit -am "Remove the per-version sitemaps" && git -C /tmp/ghp push origin gh-pages
git worktree remove /tmp/ghp
```

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
[`Dockerfile`](../Dockerfile) and [`Dockerfile.mike`](../Dockerfile.mike); those three had
drifted to three different values before `ovweb doctor --pins` started failing on disagreement.
A different theme version builds different markup, and the release-notes splice matches on that
markup.

---

## Caveats and observations

- **Clean working tree required.** `mike` builds the site from the working tree, so a publish
  with uncommitted changes would ship them. `ovweb` refuses.
- **Post-processing is not idempotent.** A second pass would strip the version out of
  author-pinned links (the shield is single-shot) and fail on the already-moved directories.
  `ovweb` refuses to run on a tree whose version root is already a generated redirect; `--force`
  overrides it. The shell had no guard at all.
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
- **The root search index names explicit versions.** It is a copy of the newest version's index,
  taken after the locations were pinned, so a versioned hit points at `/3.9/docs/…` rather than
  `/latest/docs/…`. Preserved deliberately from the shell implementation; revisiting it means
  deciding what a search hit should mean once `latest` moves.
- **Old branches do not generate `llms.txt` or the RSS feeds.** Their `mkdocs.yml` predates those
  plugins, so the past-version cleanup is tolerant of every root file it removes.
- **A version can be published without a branch.** `ovweb versions list` flags it; such a version
  cannot be re-published, because the branch is the source of truth for its content.
