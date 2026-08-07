---
name: release-version
description: Publish an OpenVidu documentation version end to end — update the releases pages with their strict heading and link contract, write the version-pinned Release blog post, choose and dispatch the right Publish Web command (new/latest/past), and interpret the post-publish verification. Use for any release-day docs work or when re-publishing a version. Trigger phrases like "publish version X.Y", "release 3.9 docs", "update the releases pages", "re-publish the site".
---

# Releasing a documentation version

The recurring sequence for release-day docs work. The mechanics live in
[`publish-tool/README.md`](../../../publish-tool/README.md) ("What a publish does"); this skill
is the order of operations and the contracts that make a publish fail.

## 1. Know which publish this is

| Situation | Command | Effect |
|---|---|---|
| New minor release (docs merged from `next`) | `ovweb publish new X.Y` | Deploys the version, points `latest` at it, refreshes the root pages, creates the `X.Y` branch |
| Content fix or patch release of the current minor | `ovweb publish latest X.Y` | Rebuilds the newest version from `main` in place; rebases the `X.Y` branch |
| Fix to an older minor | `ovweb publish past X.Y` | Commit to the `X.Y` branch first; root pages untouched |

Patch releases do **not** create a new documentation version: they update the existing `X.Y`
in place and add their notes under it.

## 2. Releases pages (`docs/meet/releases.md`, `docs/docs/releases.md`)

Strict contract — `ovweb` fails the publish on violations:

- Each minor gets one top-level `## X.Y.0` section. Later patches go **under it**, as
  `#### X.Y.Z` beneath a `### Patch releases` heading — never a new top-level section.
- Every link inside a version's notes is **absolute, domain-qualified and pinned to that same
  version** (`https://openvidu.io/X.Y/docs/...`) — never relative, never `latest`. The notes
  are spliced into every version folder on publish, so any other form is wrong for most
  copies. `ovweb lint` catches `latest` here at PR time.
- Prefer additive docs changes: each `X.Y` folder serves only its newest patch, so a page or
  anchor an older patch's notes link to has nothing to fall back to if removed. When a target
  must move, fix the affected release-notes links in the same change.

## 3. Version gates in `publish-tool/ovweb.yaml`

If pages moved or were removed in this release, add redirect rules gated to **the release the
change belongs to** (e.g. `versions: ">=3.9"`), never inferred from what a version folder
currently contains. Run `ovweb redirects check`. New legacy folders or rule changes for other
versions need `ovweb redirects apply` on gh-pages after the publish.

## 4. Release blog post

Use the `blog-write` skill with the `Release` category. Its exception applies: versioned-docs
links are version-pinned domain-qualified URLs to the announced version.

## 5. Dispatch and verify

- Publishing happens via the [Publish Web workflow](https://github.com/OpenVidu/openvidu.io/actions/workflows/publish-web.yaml)
  (`gh workflow run publish-web.yaml -f command=<new|latest|past> -f version=X.Y`), or locally
  after `pip install "./publish-tool[build]"`. Always available: `--dry-run` prints the full
  plan without building or pushing.
- A failed publish never reaches the remote — there is no recovery path to run, just fix and
  re-run.
- The workflow ends with `ovweb verify`. Findings name their remedy; in particular,
  `[version-alias]` findings after a `latest` publish mean alias folders of **other** minors
  need `ovweb redirects apply` on a gh-pages worktree — expected, not a rollback.
- After the publish, spot-check live: the new version in the selector, `/latest/` serving it,
  the releases page anchors, and the root sitemap.

## Naming rule

"OpenVidu Platform" as a product name exists only from 3.4 — never use it in copy that targets
older versions (release notes for 3.0–3.3, comparisons, redirect page bodies).
