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
| `NON_VERSIONED_PAGES` | `account`, `pricing`, `support`, `openvidu-meet-vs-openvidu-platform`, `openvidu-vs-livekit`, `openvidu-vs-mediasoup`, `conditions`, `blog`, `about-us`, `research`, `acknowledgments` | Global pages shared across all versions. Served **once** at the site root (e.g. `/pricing/`).                     |
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

We want every version to serve the **full, most-recent** release notes, **without** dragging
the rest of the latest page along with them. This is achieved in two complementary parts:

1. **Copy the content at publish time (this folder).** On every publish, the **content** of
   the latest releases pages — the release notes body and the table of contents, nothing
   else — is spliced into the releases page of **every other version folder**, so each
   `/X.Y/…/releases/` lists the same complete changelog as `/latest/…/releases/`. See
   [`copyReleasesToAllOtherVersions` / `copyReleasesFromTo`](#the-releases-page-copy-helpers).

2. **Jump to the viewed version (front-end).** Because the notes are now identical across
   versions, a small client-side script scrolls the visitor to the section matching the
   version they are browsing — e.g. opening `/3.5/meet/releases/` jumps to the `## 3.5.0`
   section (anchor `#350`). The script lives outside this folder in
   [`docs/javascripts/releases-scroll-to-version.js`](../docs/javascripts/releases-scroll-to-version.js)
   and is loaded only on the releases pages, via the `scrolltoversion` tag in their front
   matter (wired in [`docs/overrides/main.html`](../docs/overrides/main.html)). It is a
   no-op when the URL already has an anchor (so cross-page `#380` links are respected) or
   when there is no matching section (the `latest` alias stays at the top, newest first).

Four consequences worth keeping in mind:

- **Only the content travels; the page stays version-local.** Header, tabs, navigation menu,
  footer, `<link rel="canonical">`, asset URLs and Material's runtime config are left exactly
  as the destination version built them, so a visitor who opens `/3.4/docs/releases/` keeps
  browsing the **3.4** documentation instead of being sent to `/latest/` by every link around
  the notes. Nothing in the spliced fragments needs rewriting: the release notes' own links
  are authored as absolute, version-pinned URLs, and the table of contents only holds
  `#anchor` links. Both are verified before splicing, so a page that breaks the convention is
  reported instead of published with links resolving against the wrong version folder.
- **The outdated-version banner shows up there like anywhere else.** The destination page is
  the destination version's own page, so Material flags it as outdated and the banner from
  `{% block outdated %}` appears — which is what tells the visitor that the documentation
  around the notes is old, even though the notes themselves are complete.
- **The canonical tag is the destination's own.** Every versioned page already has its
  canonical rewritten to `/latest/…` by
  [`changeVersionedPagesLinks`](#the-link-rewriting-helpers), so all releases pages
  consolidate onto `/latest/<vp>/releases/` for SEO — a target that no longer changes with
  every release.
- **The LLM Markdown companion does not travel.** Pages listed in the `mkdocs-llmstxt`
  plugin's `sections` also get an `index.md` next to their `index.html`, but old version
  folders have no `llms.txt` at all (the `UPDATE_LATEST=false` path removes it, since those
  branches predate the plugin), so nothing there ever links to that companion. Only
  `/latest/<vp>/releases/index.md`, the one `llms.txt` references, matters — and it is built,
  not copied.

---

## Files in this folder

| File                                                                                             | Purpose                                                                                                                    |
| ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| [`push-new-version.sh`](push-new-version.sh)                                                     | The workhorse. Deploys a version with `mike` and does all the post-processing. The other two scripts delegate to it.       |
| [`overwrite-latest-version.sh`](overwrite-latest-version.sh)                                     | Deletes and re-publishes the current latest version, refreshing the root pages, then syncs the version branch with `main`. |
| [`overwrite-past-version.sh`](overwrite-past-version.sh)                                         | Deletes and re-publishes a specific older version **without** touching the root pages.                                     |
| [`copy-releases-content.py`](copy-releases-content.py)                                           | Splices the release notes body and table of contents of one built releases page into another version's, leaving that version's navigation, canonical and assets alone. Called by `push-new-version.sh`. |
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

Fails early if the `mike` binary is not on `PATH` (`pip install mike`), or if `python3` is
missing (needed by [`copy-releases-content.py`](copy-releases-content.py)).

### `stageReleasesContentHelper`

Copies [`copy-releases-content.py`](copy-releases-content.py) to a temporary file (removed by
an `EXIT` trap) **before** any branch switching. `updateWebsite` runs with `gh-pages` checked
out, where this folder does not exist, so by then the script would be gone from the working
tree — `push-new-version.sh` itself only survives because bash keeps its file descriptor open.
Restoring it into the `gh-pages` working tree instead is not an option: `updateWebsite` runs
`git add .` and would publish it as part of the website.

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
    - **Raw-HTML asset references** (`src|href="/assets/…"`, `/javascripts/…`, `/stylesheets/…`)
      → version-pinned `src|href="/$VERSION/assets/…"`, etc. Authors write asset paths in **raw
      HTML blocks** (`<img src="/assets/…">`, glightbox `<a href="/assets/…">`) as root-absolute,
      because MkDocs does **not** process raw HTML — a relative path would need a fragile per-page
      depth relative to the _built_ folder and could never be correct inside a shared snippet
      included at different levels. At runtime the root `/assets/` folder always holds the
      **latest** publish's assets (they are promoted to the root by `copyFilesFromVersionToRoot`),
      so a versioned page must reference its **own** `/$VERSION/assets/…` instead: its assets may
      change or disappear in later releases, which would silently break the older page. Markdown
      asset links (and Markdown links in general) need **no** pinning — MkDocs already rewrites
      them into version-local relative URLs at build time. `/search/` is not pinned here (the
      search index is handled by `changeSearchIndexLinks`).
    - Links pointing at a non-versioned page (`href="(../)*NVP/"`) → absolute `href="/NVP/"`.
    - Links to the home page (`href="(../)*.."`) → `href="/"`.
    - The cookie-consent base URL `URL("(../)*..",location)` → `URL("/",location)`, so the
      cookie consent is not re-requested on every version.
    - Rewrites each versioned page's self-referencing SEO URLs — `<link rel="canonical">`
      and `og:url` — from `/$VERSION/…` to `/latest/…`, so ranking signals consolidate on
      one evergreen URL instead of churning every release (issue #1). JSON-LD needs no
      rewriting here: the only JSON-LD emitted on a versioned page (`docs/index.md`,
      `meet/index.md`) already hardcodes `/latest/…` (see `docs/overrides/partials/json-ld.html`);
      no other versioned page emits JSON-LD at all. Only these two tags are touched — the
      `/$VERSION/assets/…` pins above and any author-pinned `/X.Y/…` links elsewhere on the
      page are left alone.
- **`changeNonVersionedPagesLinks`** — operates on the version's non-versioned pages and
  `index.html`:
    - Fixes `404.html`: strips `/$VERSION/`, and rewrites links to versioned pages to
      `/latest/VP/`.
    - Rewrites links from global pages to versioned pages → `/latest/VP/`.
    - Removes the version prefix from each page's self-referencing URLs (`<link rel="canonical">`,
      `og:url`, JSON-LD `@id`/`url`/`mainEntityOfPage`), since these pages are served from the
      root. Author-written version-pinned links to versioned pages (`/X.Y/docs/`, `/X.Y/meet/`,
      e.g. release-notes links in blog posts) are shielded and preserved.
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

- **`copyReleasesFromTo SRC DST`** — copies the releases pages' **content** from a source
  version folder into a destination version folder. For each versioned page (`docs`, `meet`):
    - Skips it if either side lacks that built releases page (e.g. Meet did not exist before
      `3.4.0`), and never copies a version onto itself.
    - Runs [`copy-releases-content.py`](copy-releases-content.py) on
      `SRC/<vp>/releases/index.html` → `DST/<vp>/releases/index.html`, which replaces only two
      regions of the destination page and leaves the file otherwise byte-identical:

      | Region | Marker | Occurrences |
      | --- | --- | --- |
      | Release notes body | `<article class="md-content__inner md-typeset">` | 1 |
      | Table of contents | `<nav class="md-nav md-nav--secondary" aria-label="Table of contents">` | 2, identical |

      There are two tables of contents because Material renders one in the right-hand
      secondary sidebar and embeds another under the active item of the primary navigation
      (used by the mobile drawer); both are replaced, or the sidebar would keep listing the
      destination version's own, shorter set of releases. Regions are closed by **tag-depth
      counting**, not by searching for the first closing tag — the table of contents nests one
      `<nav>` per heading level, which is why this step is a Python script and not `sed`.

      No link rewriting is applied, and none is needed: every link inside a release-notes
      section is authored as an absolute, version-pinned URL, and the table of contents only
      holds `#anchor` links. The script **verifies** this before splicing and fails rather
      than publishing a fragment whose links would resolve against the wrong version folder.

      Everything else stays the destination's own: `<head>`, `<link rel="canonical">`, the OG
      tags, `<script id="__config">` (Material's `base`, search-index path and version data),
      header, tabs, primary navigation, footer and every asset URL.
    - Exit-code handling: `2` means the destination page did not expose those regions (an old
      folder built by a different theme version) — a `WARNING` is printed and that page is left
      as built, rather than aborting a publish that has already pushed a `mike` commit. Any
      other non-zero exit points at the freshly built **source** page and aborts the publish.
    - The LLM Markdown companion (`index.md`) is **not** copied: old version folders have no
      `llms.txt`, so nothing there links to it. See
      [Keeping the releases pages always up to date](#keeping-the-releases-pages-always-up-to-date).
- **`copyReleasesToAllOtherVersions`** — reads the version list from `versions.json` and
  calls `copyReleasesFromTo "$VERSION" <each other version>`. Used on the latest-publish
  path, where `"$VERSION"` is the freshly built latest.

On the past-version path (`UPDATE_LATEST=false`), the direction is reversed: the script
resolves the current latest via the `latest` symlink (`readlink latest`) and calls
`copyReleasesFromTo "$LATEST_VERSION" "$VERSION"`, so a rebuilt old version does not revert
to its stale, version-local notes.

Note that a destination page must have been **rebuilt since this content-only scheme was
introduced** for its navigation to be its own: folders last published under the old
whole-page copy still carry the latest version's chrome until
`overwrite-past-version.sh X.Y` rebuilds them.

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
| Versioned page → asset (raw HTML)   | `src="/assets/…"`  | `src="/3.0/assets/…"` (version-pinned) |
| Versioned page → asset (Markdown)   | `../../assets/…`   | _(left relative by mike; stays version-local)_ |
| Versioned page → non-versioned page | `../../pricing/`   | `/pricing/`                       |
| Versioned page → home               | `../..`            | `/`                               |
| Non-versioned page → versioned page | `../docs/`         | `/latest/docs/`                   |
| `404.html` → versioned page         | `/docs/`           | `/latest/docs/`                   |
| Canonical tag on non-versioned page | `…/3.0/…`        | `…/…` (version removed)           |
| Search index → versioned page       | `docs/`            | `/3.0/docs/` (explicit version) |
| Search index → non-versioned page   | `pricing/`         | `/pricing/`                       |
| Root sitemap → versioned page       | `/3.0/docs/`     | `/latest/docs/`                   |
| Root sitemap → non-versioned page   | `/3.0/pricing/`  | `/pricing/`                       |
| Canonical/`og:url` on versioned page | `…/3.0/docs/…`   | `…/latest/docs/…`                 |

The releases pages are **not** in this table any more: only their content is copied into other
version folders, so every link on the page — navigation, assets, canonical — is the one the
destination version built for itself and follows the rows above. Nothing inside the copied
content is rewritten either, because those links are authored absolute and version-pinned.

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
- **The releases-content splice is coupled to two Material markup strings.** A theme upgrade
  that renames the `md-content__inner` article or the `md-nav--secondary` table-of-contents
  `aria-label` breaks the splice. It fails loudly rather than silently (non-zero exit from
  [`copy-releases-content.py`](copy-releases-content.py); the source-side failure aborts the
  publish), so treat a `WARNING: could not splice the releases content` line in a publish log
  as something to fix, not noise.
- **Per-version search index is not updated by the copy.** The splice rewrites the rendered
  `index.html`, but each version's `search/search_index.json` still holds that version's
  original releases text. The page a visitor sees is current; in-version search results for
  the releases page may lag until that version is rebuilt.
- **Old branches do not generate `llms.txt` or the RSS feeds.** Their `mkdocs.yml`
  predates those plugins. The `UPDATE_LATEST=false` cleanup is therefore tolerant
  (`|| true`) of every root file it removes from the version folder — do not turn those
  into hard failures.
