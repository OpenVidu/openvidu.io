# Custom versioning scripts

This folder contains the scripts and helper files used to publish and maintain the
different versions of the [openvidu.io](https://openvidu.io) documentation website.

The site is built with **MkDocs Material** and versioned with
[**mike**](https://github.com/jimporter/mike), which hosts every version in the
`gh-pages` branch of the repository (served through GitHub Pages). These scripts wrap
`mike` to solve a problem that `mike` alone does not: keeping a set of **global,
non‑versioned pages** (pricing, blog, support…) served once at the site root while the
**versioned documentation** lives under version‑aliased paths.

### Minor-grouped versioning (`X.Y`)

Documentation versions are grouped by **minor** release and named `X.Y` (e.g. `3.8`):
one git branch, one `gh-pages` folder and one version-selector entry per minor. The
content of each `X.Y` version always reflects the **newest patch** of that minor —
patch releases do **not** create new documentation versions:

| Event                                     | Action                                                                                                    |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| New minor release (e.g. `3.9.0`)          | `push-new-version.sh 3.9` — creates branch `3.9` from `main`, deploys, moves `latest`                     |
| Patch for the current minor (e.g. `3.8.1`) | Merge docs to `main` → `overwrite-latest-version.sh 3.8`. Add the patch's section to the releases pages   |
| Patch for an old minor (e.g. `3.7.2`)     | Commit to branch `3.7` → `overwrite-past-version.sh 3.7`                                                  |

Two supporting behaviors:

- **Tolerant `mike delete`**: the overwrite scripts do not fail when the version does
  not exist on `gh-pages` yet (first publish under a new name).
- **Legacy URL redirects**: exact-patch URLs from the old scheme (`/3.4.1/…`,
  `/3.0.0-beta2/…`) are redirected to their minor folder (`/3.4/…`, `/3.0/…`) by the
  404 page (`docs/overrides/404.html`) — GitHub Pages has no server-side redirects.

---

## Table of contents

- [Background concepts](#background-concepts)
- [The core problem these scripts solve](#the-core-problem-these-scripts-solve)
- [Keeping the releases pages always up to date](#keeping-the-releases-pages-always-up-to-date)
- [Files in this folder](#files-in-this-folder)
- [`push-new-version.sh` — the core script](#push-new-versionsh--the-core-script)
- [`overwrite-latest-version.sh`](#overwrite-latest-versionsh)
- [`overwrite-past-version.sh`](#overwrite-past-versionsh)
- [`redirect-from-version-to-getting-started.html`](#redirect-from-version-to-getting-startedhtml)
- [Link-rewriting reference](#link-rewriting-reference)
- [How the scripts are run in CI](#how-the-scripts-are-run-in-ci)
- [Caveats and observations](#caveats-and-observations)

---

## Background concepts

### `mike` and the `gh-pages` branch

`mike` builds each documentation version into its own subfolder of the `gh-pages`
branch, named after the version, and maintains **aliases** (friendly names that point
to a version). This project uses a single alias, `latest`, configured as the default in
`mkdocs.yml`:

```yaml
extra:
    version:
        provider: mike
        default: latest
        alias: true
```

So after publishing version `3.0` as `latest`, `gh-pages` contains something like:

```
gh-pages/
├── 3.0/            # the built site for version 3.0
├── latest/         # alias → 3.0
├── versions.json   # mike's version index (drives the version selector)
└── ...
```

### Versioned vs. non-versioned pages

The scripts classify every page into one of two groups, declared as arrays at the top of
[`push-new-version.sh`](push-new-version.sh):

| Group                 | Value                                                                                                                                  | Meaning                                                                                                           |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `VERSIONED_PAGES`     | `docs`, `meet`                                                                                                                         | Documentation tied to a specific release. Served under `/latest/docs/`, `/latest/meet/`, and `/X.Y/docs/`, etc. |
| `NON_VERSIONED_PAGES` | `account`, `pricing`, `support`, `openvidu-meet-vs-openvidu-platform`, `conditions`, `blog`, `about-us`, `research`, `acknowledgments` | Global pages shared across all versions. Served **once** at the site root (e.g. `/pricing/`).                     |
| `ASSETS`              | `assets`, `javascripts`, `stylesheets`, `search`                                                                                       | Static asset folders that also live at the root.                                                                  |

In addition to the non-versioned page folders, several **root files** are treated as
non-versioned: `index.html`, `index.md`, `404.html`, `robots.txt`, `llms.txt`,
`llms-full.txt`, the RSS/JSON feeds (`feed_rss_created.xml`, `feed_rss_updated.xml`,
`feed_json_created.json`, `feed_json_updated.json`, `rss.xsl`) and `sitemap.xml`.

---

## The core problem these scripts solve

`mike` builds the **entire** MkDocs site — versioned _and_ non-versioned pages — into
each version folder (`3.0/`). Two things follow from that:

1. **Duplication.** The pricing page, blog, etc. would be published once per version.
   We instead want a single canonical copy served at the root (`/pricing/`), always
   reflecting the most recent release.
2. **Broken links.** MkDocs Material emits **relative** links (e.g. `../../pricing/`).
   Once files are relocated (non-versioned pages moved to the root, versioned docs left
   under `/latest/`), those relative links no longer resolve.

The scripts therefore **post-process mike's output** on the `gh-pages` branch to:

- Rewrite relative links into **absolute** paths that match the final layout.
- Move the non-versioned pages and root files out of the version folder and into the
  root.
- Fix auxiliary files: the search index, `sitemap.xml`, `llms.txt`, RSS feeds and the
  `404.html`.
- Drop a small redirect page at each version root so `/X.Y/` and `/latest/` land on
  the docs.

---

## Keeping the releases pages always up to date

There are two releases pages — OpenVidu Meet (`meet/releases/`) and OpenVidu Platform
(`docs/releases/`) — and both are **versioned** pages. Left untouched, an old version's
releases page would only list the notes up to that version: a visitor browsing `3.5.0`
would never see the notes for `3.6.0`, `3.7.0`, … even though release notes are inherently
global information.

We want every version to serve the **full, most-recent** release notes. This is achieved
in two complementary parts:

1. **Copy at publish time (this folder).** On every publish, the latest releases pages are
   copied into **every other version folder**, so each `/X.Y/…/releases/` serves the same
   complete changelog as `/latest/…/releases/`. See
   [`copyReleasesToAllOtherVersions` / `copyReleasesFromTo`](#the-releases-page-copy-helpers).

2. **Jump to the viewed version (front-end).** Because the page is now identical across
   versions, a small client-side script scrolls the visitor to the section matching the
   version they are browsing — e.g. opening `/3.5.0/meet/releases/` jumps to the `## 3.5.0`
   section (anchor `#350`). The script lives outside this folder in
   [`docs/javascripts/releases-scroll-to-version.js`](../docs/javascripts/releases-scroll-to-version.js)
   and is loaded only on the releases pages, via the `scrolltoversion` tag in their front
   matter (wired in [`docs/overrides/main.html`](../docs/overrides/main.html)). It is a
   no-op when the URL already has an anchor (so cross-page `#380` links are respected) or
   when there is no matching section (the `latest` alias stays at the top, newest first).

Two consequences worth keeping in mind:

- **Theme links are rewritten to `/latest/`.** The release notes' own links are authored as
  absolute, version-pinned URLs, so they need no rewriting. What stays relative in the built
  page is theme-generated chrome — the navigation menu and the hashed CSS/JS/image assets.
  Those would break inside an older version folder (asset hashes differ across builds, and
  the latest nav points at pages the older folder never had), so they are rewritten to
  absolute `/latest/…` links. See the [link-rewriting reference](#link-rewriting-reference).
- **The canonical tag is left untouched.** Each copy already declares the latest version as
  its `<link rel="canonical">`, so all copies consolidate onto a single URL for SEO — no
  duplicate-content penalty.
- **The LLM Markdown companion travels too.** Pages listed in the `mkdocs-llmstxt` plugin's
  `sections` also get an `index.md` next to their `index.html` (both releases pages are
  listed). The copy step propagates it as well, so `/X.Y/<vp>/releases/index.md` stays in
  sync. Unlike the HTML, its links are already absolute, so it is copied verbatim.

---

## Files in this folder

| File                                                                                             | Purpose                                                                                                                    |
| ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| [`push-new-version.sh`](push-new-version.sh)                                                     | The workhorse. Deploys a version with `mike` and does all the post-processing. The other two scripts delegate to it.       |
| [`overwrite-latest-version.sh`](overwrite-latest-version.sh)                                     | Deletes and re-publishes the current latest version, refreshing the root pages, then syncs the version branch with `main`. |
| [`overwrite-past-version.sh`](overwrite-past-version.sh)                                         | Deletes and re-publishes a specific older version **without** touching the root pages.                                     |
| [`redirect-from-version-to-getting-started.html`](redirect-from-version-to-getting-started.html) | A tiny client-side redirect used as each version's `index.html`.                                                           |

---

## `push-new-version.sh` — the core script

```bash
./push-new-version.sh X.Y [update_latest]
```

- **`X.Y`** (required): the version to publish.
- **`update_latest`** (optional, default `true`):
    - `true` → publish the version, point the `latest` alias at it, **and** refresh all
      the root non-versioned pages from this version.
    - `false` → publish/overwrite only that version's folder; leave the root pages
      untouched.

The script is organized as a series of functions orchestrated by `main`. Execution flow:

```
main
 ├── validateArgs        # parse VERSION and UPDATE_LATEST
 ├── checkDependencies   # ensure `mike` is installed
 ├── cd <repo root>
 ├── checkGitStatus      # refuse to run with a dirty working tree
 ├── prepareGitBranches  # sync gh-pages + create/sync the version branch
 ├── deployVersion       # `mike deploy` the version
 └── updateWebsite       # the heavy post-processing on gh-pages
```

### `validateArgs`

Requires at least one argument (the version). Reads the optional second argument into
`UPDATE_LATEST` (default `true`).

### `checkDependencies`

Fails early if the `mike` binary is not on `PATH` (`pip install mike`).

### `checkGitStatus`

Aborts if `git status --porcelain` reports anything — the script switches branches and
moves files around, so it needs a clean working tree.

### `prepareGitBranches`

Prepares two branches:

- **`gh-pages`**: if it exists on the remote, it is checked out and pulled so the local
  copy is up to date, then control returns to `main`. If it does not exist, this is
  treated as the very first deployment.
- **The version branch** (named exactly after the version, e.g. `3.0`):
    - If it exists remotely, it is checked out and pulled. When `UPDATE_LATEST=true`,
      control returns to `main`.
    - If it does **not** exist:
        - With `UPDATE_LATEST=false` the script errors out — you cannot update a past
          version whose branch was never created.
        - With `UPDATE_LATEST=true` the branch is created from the current branch (`main`)
          and pushed. This per-version branch is what makes it possible to go back and edit
          an old version later.

The branch you end up on determines what `mike` builds next: `main` for a new/latest
release, or the version branch when overwriting a past version.

### `deployVersion`

Runs `mike`:

- `UPDATE_LATEST=true` → `mike deploy --push --update-aliases "$VERSION" latest`
  (builds the version, moves the `latest` alias to it, and pushes to `gh-pages`).
- `UPDATE_LATEST=false` → `mike deploy --push "$VERSION"` (builds the version, no alias
  change).

After this step, `gh-pages` holds a freshly built `"$VERSION"/` folder that still
contains everything (versioned + non-versioned pages) with relative links.

### `updateWebsite`

The post-processing stage, run on the `gh-pages` branch:

1. Check out and pull `gh-pages`; delete the stray `site/` build folder and the
   version's `overrides/` theme folder (not meant to be published).
2. Restore the redirect file
   [`redirect-from-version-to-getting-started.html`](redirect-from-version-to-getting-started.html)
   from the appropriate source branch (`main` for latest, the version branch otherwise).
3. Run `changeVersionedPagesLinks` and `changeSearchIndexLinks` (always).
4. Branch on `UPDATE_LATEST`:
    - **`false`** — remove the non-versioned pages, root files and feeds from the version
      folder (they must not appear inside `/X.Y/`), install the redirect as
      `"$VERSION"/index.html`, prune the version sitemap (`updateVersionSitemap`), copy the
      **current latest** releases pages into this version so it does not revert to stale
      notes (`copyReleasesFromTo` via the `latest` symlink), and commit with _"Non-versioned
      pages untouched"_.
    - **`true`** — run `changeNonVersionedPagesLinks`, then `copyFilesFromVersionToRoot`
      to promote the version's global pages/assets to the root, install the redirect as
      `"$VERSION"/index.html`, update both the root sitemap (`updateSitemap`) and the
      version sitemap (`updateVersionSitemap`), copy the **new latest** releases pages into
      every other version (`copyReleasesToAllOtherVersions`), and commit with _"Non-versioned
      pages updated"_.
5. Push `gh-pages` and check out `main`.

### The link-rewriting helpers

These functions are the heart of the post-processing. They use `grep -Erl … | xargs
sed -i …` to rewrite links in place.

- **`changeVersionedPagesLinks`** — operates on `"$VERSION"/docs` and `"$VERSION"/meet`:
    - Links pointing at a non-versioned page (`href="(../)*NVP/"`) → absolute `href="/NVP/"`.
    - Links to the home page (`href="(../)*.."`) → `href="/"`.
    - The cookie-consent base URL `URL("(../)*..",location)` → `URL("/",location)`, so the
      cookie consent is not re-requested on every version.
- **`changeNonVersionedPagesLinks`** — operates on the version's non-versioned pages and
  `index.html`:
    - Fixes `404.html`: strips `/$VERSION/`, and rewrites links to versioned pages to
      `/latest/VP/`.
    - Rewrites links from global pages to versioned pages → `/latest/VP/`.
    - Removes the version from the `<link rel="canonical">` tags.
    - Updates `llms.txt` (versioned → `/latest/…`, non-versioned → `/…`, root index).
    - Removes the version prefix from the RSS/JSON feeds.
- **`changeSearchIndexLinks`** — rewrites `"$VERSION"/search/search_index.json`:
    - Versioned locations → `/$VERSION/VP/` (search results stay **within** the version).
    - Non-versioned locations → `/NVP/`.
    - The empty root location → `/`.

> Note the asymmetry: the search index keeps the explicit version for versioned pages
> (so searching inside `3.0` links to `3.0` docs), while page links use the
> `latest` alias.

### The sitemap helpers

- **`updateSitemap`** (latest only) — copies the version's `sitemap.xml` to the root,
  rewrites versioned URLs to `/latest/…`, strips the version from non-versioned URLs and
  the root URL, and regenerates `sitemap.xml.gz`.
- **`updateVersionSitemap`** (always) — deletes the `<url>…</url>` blocks that reference
  non-versioned pages from the version's own `sitemap.xml` (using a `sed` range loop),
  then regenerates its `.gz`.

### `copyFilesFromVersionToRoot` (latest only)

Promotes the newly built version's global content to the site root:

- For each asset folder (`assets`, `javascripts`, `stylesheets`, `search`): delete the
  old root copy and copy the new one.
- Move the root files (`index.html`, `index.md`, `404.html`, `robots.txt`, `llms.txt`,
  `llms-full.txt`, the feeds and `rss.xsl`) to the root.
- For each non-versioned page: delete the old root copy and move the new one into place.

This is what keeps `/pricing/`, `/blog/`, etc. always in sync with the most recent
release.

### The releases-page copy helpers

These implement the [always-up-to-date releases pages](#keeping-the-releases-pages-always-up-to-date).
They run inside `updateWebsite`, on the `gh-pages` branch, just before the commit.

- **`copyReleasesFromTo SRC DST`** — copies the releases pages from a source version folder
  into a destination version folder. For each versioned page (`docs`, `meet`):
    - Skips it if either side lacks that releases page (e.g. Meet did not exist before
      `3.4.0`), and never copies a version onto itself.
    - Copies `SRC/<vp>/releases/index.html` over `DST/<vp>/releases/index.html` and rewrites
      the remaining relative `href`/`src` links to absolute `/latest/…` links. The release
      notes' own links are authored as absolute version-pinned URLs, so what gets rewritten
      is only theme chrome (the navigation menu and hashed CSS/JS/image assets). The page
      sits two levels deep (`<vp>/releases/`), so `../../` (version root) → `/latest/` and
      `../` (the `<vp>` root) → `/latest/<vp>/`. This keeps the copy loading the latest
      assets (hashes differ per build) and its nav from 404-ing against pages an older folder
      never had. Only `href`/`src` attributes are touched, so Material's runtime JS (its
      `base` and search-index paths) keeps working per version folder; `<link rel="canonical">`
      is left as-is.
    - Also copies the LLM Markdown companion `SRC/<vp>/releases/index.md` **when it exists**.
      The [`mkdocs-llmstxt`](https://github.com/pawamoy/mkdocs-llmstxt) plugin generates this
      `.md` for pages listed in its `sections` in `mkdocs.yml`; **both** releases pages
      (`meet/releases.md` and `docs/releases.md`) are listed. The existence check still
      matters for versions built before a page was added there. Its internal links are
      already **absolute** URLs emitted by the plugin (e.g. `https://openvidu.io/3.7.0/docs/…`),
      so it is copied **verbatim**, with no rewriting.
- **`copyReleasesToAllOtherVersions`** — reads the version list from `versions.json` and
  calls `copyReleasesFromTo "$VERSION" <each other version>`. Used on the latest-publish
  path, where `"$VERSION"` is the freshly built latest.

On the past-version path (`UPDATE_LATEST=false`), the direction is reversed: the script
resolves the current latest via the `latest` symlink (`readlink latest`) and calls
`copyReleasesFromTo "$LATEST_VERSION" "$VERSION"`, so a rebuilt old version does not revert
to its stale, version-local notes.

---

## `overwrite-latest-version.sh`

```bash
./overwrite-latest-version.sh X.Y
```

Completely rebuilds the **current latest** version, including the root pages. Steps:

1. Check `mike` is installed and that exactly one argument (the version) was given.
2. `cd` to the repo root.
3. `git fetch origin gh-pages` and `git fetch origin "$VERSION"` so `mike` and the
   branch operations work.
4. `mike delete --push "$VERSION"` — remove the existing version from `gh-pages` so it
   can be rebuilt cleanly. **Tolerant of a missing version**: on the first publish of a
   version under a new name there is nothing to delete, and the script continues.
5. `source ./push-new-version.sh "$VERSION"` — re-run the core script with the default
   `UPDATE_LATEST=true`, republishing the version and refreshing the root pages.
6. Rebase the version branch onto `main` and force-push it, so the version branch stays
   in sync with the latest `main`; then switch back to `main`.

Use this after committing documentation changes to `main` that should replace the
current release in place (same version number).

---

## `overwrite-past-version.sh`

```bash
./overwrite-past-version.sh X.Y
```

Rebuilds a **specific older** version **without** touching the root pages. Steps 1–4 are
identical to `overwrite-latest-version.sh`, then:

5. `source ./push-new-version.sh "$VERSION" false` — re-run the core script with
   `UPDATE_LATEST=false`, so only that version's folder is republished and the global
   root pages are left alone.

Because the root pages are not rebuilt, there is **no rebase step**: the fixes for an old
version must already be committed to that version's branch before running the script
(the branch is the source of truth for a past version).

---

## `redirect-from-version-to-getting-started.html`

A minimal HTML page whose only job is a client-side redirect:

```js
const version = window.location.pathname.split('/')[1];
window.location.href = `/${version}/docs/`;
```

It reads the first path segment (the version or alias, e.g. `3.0` or `latest`) and
redirects to that version's docs landing page. `push-new-version.sh` installs it as each
version's `index.html`, so visiting `/latest/` or `/3.0/` sends the user straight to
`/latest/docs/` or `/3.0/docs/`.

---

## Link-rewriting reference

Summary of the final link conventions produced by the scripts:

| Context                             | From (mike output) | To (final)                        |
| ----------------------------------- | ------------------ | --------------------------------- |
| Versioned page → non-versioned page | `../../pricing/`   | `/pricing/`                       |
| Versioned page → home               | `../..`            | `/`                               |
| Non-versioned page → versioned page | `../docs/`         | `/latest/docs/`                   |
| `404.html` → versioned page         | `/docs/`           | `/latest/docs/`                   |
| Canonical tag on non-versioned page | `…/3.0/…`        | `…/…` (version removed)           |
| Search index → versioned page       | `docs/`            | `/3.0/docs/` (explicit version) |
| Search index → non-versioned page   | `pricing/`         | `/pricing/`                       |
| Root sitemap → versioned page       | `/3.0/docs/`     | `/latest/docs/`                   |
| Root sitemap → non-versioned page   | `/3.0/pricing/`  | `/pricing/`                       |
| Copied releases page nav → other docs | `../../docs/`    | `/latest/docs/`                   |
| Copied releases page nav → `<vp>` page | `../features/`  | `/latest/meet/features/`          |
| Copied releases page → assets       | `../../assets/`    | `/latest/assets/`                 |
| Copied releases page content links  | _(authored absolute)_ | _(left as-is, not rewritten)_  |
| Canonical on copied releases page   | `…/3.7.0/…`        | `…/3.7.0/…` (unchanged)           |

---

## How the scripts are run in CI

The GitHub Actions workflow
[`.github/workflows/publish-web.yaml`](../.github/workflows/publish-web.yaml) exposes a
manual `workflow_dispatch` with two inputs:

- **`script`**: one of `push-new-version`, `overwrite-latest-version`,
  `overwrite-past-version`.
- **`version`**: the version string, e.g. `3.0`.

The job checks out the repo with full history (`fetch-depth: 0`), installs Python plus
`mike` and the MkDocs plugins (`mkdocs-material[imaging]`, `mkdocs-glightbox`,
`mkdocs-llmstxt`, `mkdocs-rss-plugin`, and a pinned `pygments`), configures a
`github-actions[bot]` git identity, and finally runs the selected script from within
`custom-versioning/`:

```bash
./${{ github.event.inputs.script }}.sh ${{ github.event.inputs.version }}
```

The scripts can also be run locally after `pip install mike mkdocs-material
mkdocs-glightbox` (see the repository [`README.md`](../README.md) for the full local
workflow).

### Which script do I run?

| Goal                                                          | Script                            | Root pages updated? | Version branch                            |
| ------------------------------------------------------------- | --------------------------------- | ------------------- | ----------------------------------------- |
| Publish a brand-new **minor** release and make it `latest`    | `push-new-version.sh X.Y`         | Yes                 | Created from `main`                       |
| Update the latest version (content fix or **patch release**)  | `overwrite-latest-version.sh X.Y` | Yes                 | Rebased onto `main`                       |
| Update an old minor (content fix or **patch release**)        | `overwrite-past-version.sh X.Y`   | No                  | Must already exist; edits committed there |

---

## Caveats and observations

- **Clean working tree required.** `push-new-version.sh` refuses to run with uncommitted
  changes, since it switches branches and relocates files.
- **Branch hopping.** The scripts move between `main`, the version branch and
  `gh-pages`. They end on `main`. If a script fails midway, you may be left on
  `gh-pages` or a version branch — check `git status`/`git branch` before retrying.
- **`overwrite-*` scripts use `source`.** They run `push-new-version.sh` in the same
  shell rather than as a subprocess, so its variables and `set -e` apply to the caller.
- **Adding new pages.** If you add a new non-versioned page, add its folder to
  `NON_VERSIONED_PAGES`; if you add a new versioned section, add it to `VERSIONED_PAGES`
  in [`push-new-version.sh`](push-new-version.sh). Otherwise its links will not be
  rewritten and it will not be relocated correctly.
- **Releases-page canonical tracks the latest version.** Because the copied releases pages
  inherit the source's canonical, the single consolidated URL follows the newest version
  number (`…/3.7.0/…` → `…/3.8.0/…` on the next release). This is valid — search engines
  simply re-consolidate — but the canonical URL is not stable across releases. If a stable
  target is preferred, rewrite the canonical to `/latest/…/releases/` in both the copies
  and the source page.
- **Per-version search index is not updated by the copy.** The copy overwrites the rendered
  `index.html`, but each version's `search/search_index.json` still holds that version's
  original releases text. The page a visitor sees is current; in-version search results for
  the releases page may lag until that version is rebuilt.
- **Old branches do not generate `llms.txt` or the RSS feeds.** Their `mkdocs.yml`
  predates those plugins. The `UPDATE_LATEST=false` cleanup is therefore tolerant
  (`|| true`) of every root file it removes from the version folder — do not turn those
  into hard failures.
