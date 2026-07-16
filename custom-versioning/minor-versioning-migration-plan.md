# Migration plan: minor-grouped documentation versions (`3.Y`)

> **STATUS: EXECUTED on 2026-07-16.** All phases completed and verified except the manual
> external tasks in Phase 6 (Medium links, Search Console resubmit) and the post-soak
> deletion of the `gh-pages-backup-pre-minor` backup branch.

**Goal:** stop publishing one documentation version per patch release. Each **minor** release
gets a single documentation version named `3.Y` (branch + `gh-pages` folder + dropdown
entry), whose content always reflects the **newest patch** of that minor. The version
selector shows `3.8, 3.7, …` instead of `3.8.0, 3.7.0, 3.6.1, 3.6.0, …`.

**Status legend:** each step has a checkbox so the migration can be executed and tracked
incrementally. Order matters — phases are laid out in execution order.

---

## 0. Current state (verified 2026-07-16)

- **`gh-pages` folders / `versions.json`:** `3.0.0, 3.1.0, 3.2.0, 3.3.0, 3.4.0, 3.4.1,
  3.5.0, 3.6.0, 3.6.1, 3.7.0, 3.8.0` — `latest` → `3.8.0`.
- **Version branches:** one per folder above, plus `3.0.0-beta1/2/3` (never published as
  folders) and `next` (in-development docs).
- **Pinned `/3.Y.Z/` links in source (`main`):** only in `docs/meet/releases.md`,
  `docs/docs/releases.md`, `docs/blog/posts/2026-07-09-release-380.md` and
  `docs/docs/reference-docs/` (15 links across 14 compodoc HTML files). All other content
  uses relative links or `/latest/`.
- **Reference docs:** committed per branch under `docs/docs/reference-docs/`; each branch
  pins links to its own exact version (`3.4.1` branch → `openvidu.io/3.4.1/…`).
  `properties.html` shows the library version (`Version : 3.8.0`).
- **`llms.txt` / RSS feeds:** absent from every version folder on `gh-pages` (by design —
  moved to root on latest publish, removed on past publish). Old branches do not even
  generate them (their `mkdocs.yml` lacks the plugins), so the publish script must tolerate
  their absence (see 2.1).

### Naming-feasibility audit (`3.Y`, two segments)

Verified before adopting the two-segment naming — nothing in the pipeline assumes three
segments:

- All three shell scripts use `$VERSION` as an **opaque string** (no `cut`/`awk`/splitting;
  the only `X.Y.Z` occurrences are usage strings and comments).
- `mike` treats version names and aliases as opaque identifiers — `3.4` is a valid name.
- `3.4` is a valid git branch name, and `git ls-remote --heads origin "3.4"` matches only
  the exact ref — it returns nothing while `3.4.0`/`3.4.1` still exist, so
  `prepareGitBranches` correctly detects the new branch as "not yet existing" during the
  migration window.
- The client-side pieces (`releases-scroll-to-version.js`, the outdated-banner script,
  `redirect-from-version-to-getting-started.html`, `404.html`) all read the first path
  segment generically (`[^/]+` / `split('/')[1]`).
- Theme partials (`json-ld.html`, `og.html`) hardcode `/latest/` — no version parsing.
- The CI workflow takes the version as free text — no validation regex.
- No non-versioned page or asset folder can collide with a `\d+.\d+` name.
- A side benefit for the legacy redirect (3.3): old URLs always have a third version
  segment, new ones never do, so the `X.Y.Z → X.Y` rewrite cannot misfire on new URLs.

### Version mapping

| Old folders (gh-pages)  | Old branches       | New folder + branch | Built from (source branch) |
| ----------------------- | ------------------ | ------------------- | -------------------------- |
| `3.0.0`                 | `3.0.0` (+ betas)  | `3.0`               | `3.0.0`                    |
| `3.1.0`                 | `3.1.0`            | `3.1`               | `3.1.0`                    |
| `3.2.0`                 | `3.2.0`            | `3.2`               | `3.2.0`                    |
| `3.3.0`                 | `3.3.0`            | `3.3`               | `3.3.0`                    |
| `3.4.0`, `3.4.1`        | `3.4.0`, `3.4.1`   | `3.4`               | `3.4.1` (newest patch)     |
| `3.5.0`                 | `3.5.0`            | `3.5`               | `3.5.0`                    |
| `3.6.0`, `3.6.1`        | `3.6.0`, `3.6.1`   | `3.6`               | `3.6.1` (newest patch)     |
| `3.7.0`                 | `3.7.0`            | `3.7`               | `3.7.0`                    |
| `3.8.0` (latest)        | `3.8.0`            | `3.8` (latest)      | `main` (≡ `3.8.0`)         |

The beta branches (`3.0.0-beta1/2/3`) were never published as folders: nothing to migrate;
cleanup in Phase 8.

---

## 1. Phase 0 — pre-flight

- [ ] **Freeze publishing**: no `Publish Web` workflow runs during the migration except the
      ones in this plan.
- [ ] **Backup `gh-pages`**: `git branch gh-pages-backup-pre-minor origin/gh-pages &&
      git push origin gh-pages-backup-pre-minor`. Delete after a soak period (Phase 8).
- [ ] Save a copy of the current `versions.json` (for dropdown-order reference).

---

## 2. Phase 1 — script changes (on `main`)

### 2.1 `custom-versioning/push-new-version.sh`

- [ ] **Harden the `UPDATE_LATEST=false` cleanup** so it cannot fail on versions whose
      build does not generate `llms.txt`/RSS (old branches lack those plugins):
    - `rm "$VERSION/404.html"` → add `|| true` (defensive, same as its siblings).
    - Fix the five buggy lines `rm "$VERSION/feed_….xml" . || true` — the stray `.`
      argument makes every one of them attempt `rm .` (currently masked by `|| true`).
      They must be `rm "$VERSION/feed_….xml" || true`.
- [ ] No changes needed for naming: `mike deploy`, branch handling, `copyReleasesFromTo`,
      `copyReleasesToAllOtherVersions` (parses `versions.json`), `readlink latest`,
      `changeSearchIndexLinks` (uses `$VERSION` verbatim → `/3.4/docs/…`) are all
      name-agnostic (see the naming-feasibility audit above). Update only the usage
      examples in comments (`X.Y.Z` → `X.Y`).

### 2.2 `overwrite-past-version.sh` and `overwrite-latest-version.sh`

- [ ] Both scripts run `mike delete --push "$VERSION" || exit 1` before republishing. The
      **first** publish of each renamed version (`3.4` does not exist on `gh-pages` yet)
      would abort. Make the delete tolerant:

      ```bash
      mike delete --push "$VERSION" || echo "Version $VERSION not present yet; first deployment under this name"
      ```

      This is what lets us migrate **without manually renaming `gh-pages` folders**: old
      `X.Y.Z` folders are removed with explicit `mike delete` commands (Phase 5) and the
      new `3.Y` folder is created fresh by the overwrite scripts from the new branch.
      (Alternative considered: manually rename folders + edit `versions.json` on `gh-pages`
      first so the unmodified scripts work. Rejected: heavier, error-prone, and the folder
      is fully rebuilt right after anyway.)

- [ ] Update usage strings (`Usage: $0 X.Y.Z` → `Usage: $0 X.Y`).

### 2.3 `redirect-from-version-to-getting-started.html`

- [ ] **No functional change** — it reads the first path segment generically and works for
      `3.8`. Verify only.

---

## 3. Phase 2 — content changes (on `main`, mirrored to `next`)

### 3.1 Releases pages (`docs/meet/releases.md`, `docs/docs/releases.md`)

- [ ] **Keep the exact-patch section headers** (`## 3.8.0`, and future `## 3.8.1` sections
      get added to the same page). Rationale: release notes are a per-release historical
      record; anchors (`#380`) stay stable for existing blog/Medium/external deep links; a
      future patch simply adds a new section inside the same minor's page.
- [ ] **Remap all pinned links** from `/3.Y.Z/` to `/3.Y/`:
      `/3.8.0/` → `/3.8/`, `/3.7.0/` → `/3.7/`, … `/3.4.0/` → `/3.4/`,
      beta sections (currently pinned to `/3.0.0/`) → `/3.0/`.
      Cross-page anchors are untouched (`/3.4/docs/releases/#340` still resolves — the
      headers keep exact patch versions).

### 3.2 `docs/javascripts/releases-scroll-to-version.js`

- [ ] Update the anchor resolution for `3.Y` folders. Today it slugifies the URL version
      (`3.5.0` → `#350`) and no-ops when no element matches — `3.4` → `34` matches
      nothing. New behavior:
    1. If the version segment matches `^\d+\.\d+$`, append a dot to get the minor prefix
       (`3.4.`) and scroll to the **first** release-notes heading of that minor in
       document order (the page lists newest first, so that is the newest patch — e.g.
       `## 3.4.1` → `#341`). Match against the headings' text (`h2` starting with
       `3.4.`), not the slugified id (prefix-matching ids is ambiguous: `31…` matches
       both `3.1.0` and a future `3.10.0`; text-matching `3.1.` vs `3.10.` is not).
    2. Keep the exact-id path for three-segment folder names (defensive; none will remain
       after the migration) and all existing no-op guards (explicit hash present,
       `latest`, no match).
- [ ] Update the file's comments to describe the minor-grouped scheme.

### 3.3 `docs/overrides/404.html` — legacy URL redirects (SEO)

- [ ] Old deep links (`/3.4.1/docs/self-hosting/…`) will 404 once the `X.Y.Z` folders are
      deleted. GitHub Pages has no server redirects, so extend the 404 override script:
      if the first path segment matches `^(\d+\.\d+)\.` (i.e. it has a third segment —
      `3.4.1`, `3.0.0-beta2`), rewrite it to the captured minor (`3.4`, `3.0`) and
      `location.replace()` the same path under the new folder. New two-segment URLs have
      no third segment, so the rule cannot misfire on them. Keep the existing "versioned
      section without version" logic.
      The root `404.html` is refreshed by the Phase 4 latest publish, so this must be
      merged **before** that run.

### 3.4 Angular components reference docs (`docs/docs/reference-docs/`)

- [ ] On `main`: replace the 15 `openvidu.io/3.8.0/…` links (14 files) with
      `openvidu.io/3.8/…`. `sed` over the folder is fine — the pattern only appears in
      `href`s.
- [ ] **`properties.html` keeps the exact library version** (`Version : 3.8.0`) — it
      documents the npm package, not the docs folder. No change in this repo.
- [ ] **External task — generation script** (openvidu-components-angular repo): update the
      compodoc generation/post-processing so future outputs emit **both** cases: exact
      patch for the version property in `properties.html`, and `/3.Y/` for all hardcoded
      `openvidu.io` doc links.

### 3.5 Release blog post (`docs/blog/posts/2026-07-09-release-380.md`)

- [ ] Remap its 23 pinned links: `/3.8.0/` → `/3.8/`, and the one `/3.7.0/` link →
      `/3.7/`.
- [ ] Older release-notes blog posts: audit with
      `grep -rlE "openvidu\.io/3\.[0-9]+\.[0-9]+" docs/blog/posts/` (currently only the
      3.8.0 post matches; the rest already use `/latest/`).

### 3.6 Verified as no-change

- [ ] Outdated banner (`overrides/main.html`): displays the raw folder name → shows
      `3.4`; message reads naturally. No change.
- [ ] `mkdocs.yml` (nav, llmstxt sections, validation): version-agnostic. No change.
- [ ] Root `llms.txt` / sitemap / RSS: regenerated with `/latest/` links on the Phase 4
      publish. No manual change.
- [ ] **GitHub / installation-script / external links keep exact patch versions** — both
      in releases notes (external tags like `loki/v3.5.12` are not openvidu.io links) and
      in self-hosting install pages (each `3.Y` folder is built from the newest patch
      branch, so install commands naturally show the newest patch, e.g. `3.4.1`). No
      action needed.

### 3.7 Mirror to `next`

- [ ] Cherry-pick/merge 3.1–3.4 (releases links, scroll JS, 404 override, reference-docs
      links) into the `next` branch so the next release ships with the new scheme.

---

## 4. Phase 3 — create the `3.Y` branches

For each minor (see mapping table):

- [ ] Create the branch from the **newest patch** branch and push:

      ```bash
      for m in "3.0 origin/3.0.0" "3.1 origin/3.1.0" "3.2 origin/3.2.0" \
               "3.3 origin/3.3.0" "3.4 origin/3.4.1" "3.5 origin/3.5.0" \
               "3.6 origin/3.6.1" "3.7 origin/3.7.0" "3.8 origin/3.8.0"; do
        set -- $m; git branch "$1" "$2" && git push -u origin "$1"
      done
      ```

- [ ] On **each** new `3.Y` branch (except `3.8`, which is rebased onto `main` by the
      latest-overwrite anyway), commit the per-branch content fixes:
    - Reference-docs links: `openvidu.io/3.Y.Z/…` → `openvidu.io/3.Y/…` (each branch
      pins its own version — the whole point is **not** regenerating compodoc output for
      old versions).
    - That is the only strictly required per-branch change: the built releases pages get
      overwritten by the copy step, and the banner block is already propagated.
- [ ] Do **not** delete the old `X.Y.Z` branches yet (Phase 8).

---

## 5. Phase 4 — publish the new latest (`3.8`)

- [ ] Merge Phases 1–2 to `main`.
- [ ] Run CI `Publish Web` → `overwrite-latest-version` with version **`3.8`**. With the
      tolerant delete (2.2) this deploys `3.8` from `main`, points `latest` at it,
      refreshes all root pages (including the new `404.html`), fans the releases pages out
      to every folder listed in `versions.json`, and rebases branch `3.8` onto `main`.
- [ ] Delete the superseded folder (locally, with mike installed):

      ```bash
      git fetch origin gh-pages && mike delete --push 3.8.0
      ```

      Order matters: deploy `3.8` **first**, then delete `3.8.0` (never delete the
      version holding the `latest` alias before its replacement exists).
- [ ] Verify: `https://openvidu.io/` root pages, `/latest/` → `3.8`, dropdown shows
      `3.8`, `/3.8.0/…` deep links land on `/3.8/…` via the 404 redirect.

---

## 6. Phase 5 — migrate the old minors (ascending order)

For each minor, **oldest first** (`3.0` → `3.7`) so `versions.json` ends up newest-first
if mike prepends new entries (verify in the last step regardless):

- [ ] `3.0`: `mike delete --push 3.0.0` → CI `overwrite-past-version` `3.0`
- [ ] `3.1`: `mike delete --push 3.1.0` → CI `overwrite-past-version` `3.1`
- [ ] `3.2`: `mike delete --push 3.2.0` → CI `overwrite-past-version` `3.2`
- [ ] `3.3`: `mike delete --push 3.3.0` → CI `overwrite-past-version` `3.3`
- [ ] `3.4`: `mike delete --push 3.4.0 3.4.1` → CI `overwrite-past-version` `3.4`
- [ ] `3.5`: `mike delete --push 3.5.0` → CI `overwrite-past-version` `3.5`
- [ ] `3.6`: `mike delete --push 3.6.0 3.6.1` → CI `overwrite-past-version` `3.6`
- [ ] `3.7`: `mike delete --push 3.7.0` → CI `overwrite-past-version` `3.7`

Each `overwrite-past-version 3.Y` run builds from the `3.Y` branch, strips NVPs (tolerant
of missing `llms.txt`/RSS after 2.1), rewrites the search index to `/3.Y/…`, prunes the
version sitemap, copies the current latest releases pages in (from `readlink latest` =
`3.8`, whose links already use the `/3.Y/` scheme), and installs the version-root
redirect.

- [ ] **After all runs: verify `versions.json` order** (dropdown order). If mike did not
      keep newest-first ordering, fix with a single manual commit on `gh-pages` reordering
      the JSON array.
- [ ] Spot-verify per version: folder exists, old folders gone, `/3.4.1/…` deep link
      redirects to `/3.4/…`, releases page shows full notes and auto-scrolls to the
      newest 3.4 section, install pages show `3.4.1` commands, reference-docs links point
      to `/3.4/`.

---

## 7. Phase 6 — external / manual updates

- [ ] **Medium**: edit the release blog posts on Medium to replace `openvidu.io/3.Y.Z/…`
      links with `/3.Y/…` (at minimum the 3.8.0 release post — same 23 links as 3.5).
      Manual, via the Medium editor.
- [ ] **Google Search Console**: after Phase 5, resubmit `sitemap.xml` to accelerate
      re-crawling of the renamed URLs. Expect the old `X.Y.Z` URLs to drop out gradually
      (the 404-page JS redirect is weaker than a 301, but the canonical URLs in the new
      sitemaps and the `latest`-consolidated releases pages do the heavy lifting).
- [ ] Audit any external dashboards/tools that reference doc URLs with exact versions
      (support macros, README badges in other OpenVidu repos, etc.).

---

## 8. Phase 7 — documentation of the new model

- [ ] **`custom-versioning/README.md`**:
    - New naming convention (`3.Y`, one branch + folder per minor, content = newest
      patch).
    - New release flows:
        - **New minor release** → `push-new-version.sh 3.9` (creates branch `3.9` from
          `main`, deploys, moves `latest`).
        - **Patch for the current minor** (e.g. `3.8.1`) → merge docs to `main` →
          `overwrite-latest-version.sh 3.8`. Add the patch's section to the releases
          pages; the version dropdown does not change.
        - **Patch for an old minor** (e.g. `3.7.2`) → commit to branch `3.7` →
          `overwrite-past-version.sh 3.7`.
    - The tolerant `mike delete` behavior (first publish under a new name).
    - The legacy `X.Y.Z` → `X.Y` 404 redirect.
    - Update every `X.Y.Z` example (`3.0.0` → `3.0` etc.), including the
      "Which script do I run?" table.
- [ ] **Root `README.md`**: same naming/flow updates in its versioning sections.
- [ ] **`.claude/skills/edit-website/SKILL.md`**: update the versioning section (branch
      naming `3.Y`, the three publish flows with new examples, "past versions are edited
      on their `3.Y` branches", the no-pinned-version link rule stays as-is).

---

## 9. Phase 8 — cleanup

- [ ] Tag the old branches for history, then delete them:

      ```bash
      for b in 3.0.0 3.0.0-beta1 3.0.0-beta2 3.0.0-beta3 3.1.0 3.2.0 3.3.0 \
               3.4.0 3.4.1 3.5.0 3.6.0 3.6.1 3.7.0 3.8.0; do
        git tag "docs-$b" "origin/$b" && git push origin "docs-$b" ":$b"
      done
      ```

- [ ] After a soak period (suggested: 2–4 weeks with no issues), delete
      `gh-pages-backup-pre-minor`.
- [ ] Delete this plan file or mark it as completed.

---

## 10. Final verification checklist

- [ ] Dropdown lists exactly `3.8 [latest], 3.7, 3.6, 3.5, 3.4, 3.3, 3.2, 3.1, 3.0`,
      newest first.
- [ ] `/latest/…` and `/3.8/…` serve the same content; `latest` symlink → `3.8`.
- [ ] Every old URL form redirects: `/3.4.0/…`, `/3.4.1/…` → `/3.4/…`; `/3.8.0/…` →
      `/3.8/…`; `/docs/…` (versionless) → `/latest/docs/…`.
- [ ] Releases pages in every folder: identical full notes, links point to `/3.Y/`,
      auto-scroll works for `3.Y` folders (newest section of the minor), outdated banner
      hidden on them.
- [ ] In-version search on e.g. `3.4` returns `/3.4/…` results.
- [ ] Reference docs in every folder link to their own `/3.Y/`; `properties.html` shows
      the exact library patch version.
- [ ] Blog post + Medium links resolve.
- [ ] `mkdocs serve` on `main` shows no new warnings.

## 11. Known risks / open questions

- **mike vs. non-semver names**: `3.4` is a valid but two-segment name; mike treats it as
  an opaque identifier (fine) but its ordering behavior in `versions.json` must be
  verified after the first deploys (mitigation in Phase 5).
- **Old-branch builds under pinned CI deps**: CI installs `mkdocs-material==9.7.6` for
  every branch; old branches were authored against older versions. `overwrite-past-version`
  has been run before under the same conditions, but watch the first old-minor build
  (`3.0`) closely.
- **SEO transition**: JS-based 404 redirects are not 301s. Acceptable because the
  highest-value pages (releases) are canonicalized to `latest`, and version-pinned deep
  links are mostly reached from the releases pages themselves, which are being updated.
- **Dropdown label ambiguity**: `3.8` (folder/dropdown) vs `3.8.0` (release) — users see a
  minor version in the selector but exact patches in release notes and install commands.
  This is the intended model; if the team ever wants the dropdown to hint at grouping, mike
  supports separate titles (`mike deploy 3.8 --title "3.8.x"`) without changing URLs.
- **Release-notes section headers**: this plan keeps exact-patch headers (`## 3.8.0`). If
  the team prefers one section per minor instead, the scroll JS change in 3.2 becomes
  trivial (exact match again), but existing `#380`-style deep links from blog posts,
  Medium and `llms.txt` would break — not recommended.
