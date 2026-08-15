# Versioning and publishing

The two products' docs are **versioned**; everything else is not. The URL scheme is
version-first: `https://openvidu.io/{version}/meet/...` and `/{version}/docs/...`, with `latest`
aliasing the newest release. Non-versioned pages live at the root (`/pricing/`, `/blog/`, ...).
MkDocs Material versioning uses [mike](https://github.com/jimporter/mike), which hosts every
version in the `gh-pages` branch; publishing is done by **`ovweb`**, the CLI in
[`publish-tool/`](../publish-tool). Its [README](../publish-tool/README.md) is the authoritative
reference for what a publish does step by step and how redirects are configured.

## Branches

- `next` — docs for the version in development (merged to `main` on release).
- `main` — fixes to published content and non-versioned pages.
- `X.Y` — past versions; fixes to an old minor are committed there, never to `main`.

## Minor-grouped versioning (`X.Y`)

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

Two URL facts that follow from this model:

- Legacy exact-patch URLs (`/3.4.1/...`) redirect to their minor folder (`/3.4/...`) through
  generated redirect pages, like every other redirect on the site — all of them declared in
  [`publish-tool/ovweb.yaml`](../publish-tool/ovweb.yaml). There is no client-side 404 router.
  **Renaming, moving or deleting a published page requires a redirect rule — never retire a URL
  silently** (`ovweb lint --against` guards this on every PR, see [checks.md](checks.md)).
- Every documentation page also answers at its **unversioned** URL: `/docs/self-hosting/` and
  `/meet/` redirect to the current version. Those are real redirect pages generated on publish,
  so an unversioned URL is safe to write in a blog post, a config comment or a support answer.
  Prefer a normal relative link inside the docs; this is for links written **outside** this
  repository.

> [!NOTE]
> "OpenVidu Platform" as a product name exists only from 3.4 — do not use it in copy targeting
> older versions.

## Releases pages

`docs/meet/releases.md` and `docs/docs/releases.md` follow two conventions, because the same
release notes are served across **every** documentation version (on publish, the *content* of the
latest page — the notes and their table of contents, nothing else — is spliced into every version
folder's releases page, so any version shows the full, most-recent notes while keeping its own
navigation, links and outdated-version banner):

- **Patch notes go in a subsection under their minor's first-patch section.** Each minor has a
  top-level `## X.Y.0` section (e.g. `## 3.4.0`); the notes for later patches of that minor go
  **below it**, under a `### Patch releases` heading as `#### 3.4.1`, `#### 3.4.2`, ... — never
  in a new top-level section. The auto-scroll (`releases-scroll-to-version.js`, enabled by the
  `scrolltoversion` frontmatter tag) jumps to the `## X.Y.0` heading, so viewing
  `/3.4/docs/releases/` lands on the 3.4 notes with every 3.4.x patch below.
- **Links are always absolute and pinned to their own version.** Every link inside a
  release-notes section must be an absolute URL pointing to **the version that section
  documents** (links in the `3.4.0`/`3.4.x` sections point to `/3.4/docs/...`, never `/latest/...`
  nor relative). A link followed from an old release note then lands on the matching version of
  that page, and the outdated-version banner explains the jump. This is the one place where
  hardcoding a version in a link is required — and it is what makes the content-only splice safe:
  a relative link would resolve against whichever version folder the notes were copied into. The
  publish step **verifies** this and fails rather than publishing a broken link.

> [!WARNING]
> Each `X.Y` version always serves the docs of its **newest patch**, so the documentation of
> **older patches is not reachable** — only the latest patch of every minor is ever published. Be
> careful with changes: if a page or anchor that an older patch's release notes link to is
> removed or renamed in a later patch, that link breaks with no older-patch page to fall back to.
> Prefer additive changes, and when a linked page must move, update the affected release-notes
> links too.

## Publishing with GitHub Actions

> [!IMPORTANT]
> **Merging to `main` does not put anything on the live site.** The site is served from the
> `gh-pages` branch, which only changes when a publish runs, and publishing is deliberately
> manual — `publish-web.yaml` is `workflow_dispatch` only. Treat the publish run as the last step
> of any change that is meant to be visible, and check the change against production rather than
> trusting merge status.

Run action [Publish Web](https://github.com/OpenVidu/openvidu.io/actions/workflows/publish-web.yaml)
and pick the **command** that matches what you are doing, per the table above (`new` / `latest` /
`past`, plus the `version`). Tick **dry_run** to see the plan first: it resolves everything,
prints the ordered steps and the redirects it would install, and touches nothing.

**A failed publish cannot break the live site.** `ovweb` builds, post-processes and commits
`gh-pages` entirely locally, and pushes only once the published tree is correct; a failure
anywhere before that rolls the local branch back and leaves the remote untouched. So there is no
backup branch and no force-push recovery path to remember. The workflow runs `ovweb verify`
afterwards to assert the published layout.

The release-day sequence (releases pages, Release blog post, dispatch, verification) is packaged
in the `release-version` skill — see the [README](../README.md).

## Publishing locally

Install the tool and everything needed to build the site:

```bash
pip install "./publish-tool[build]"
```

Install it **non-editable**, as above. Publishing a past version checks out that version's
branch, which does not contain the tool — from `site-packages` it survives the switch. Run
`ovweb doctor` to check the dependencies, the version pins, the configuration and the git state
before publishing.

```bash
ovweb publish new    3.9   # new minor: deploys 3.9, moves `latest`, refreshes the root pages,
                           # and creates the 3.9 branch so the version can be fixed later
ovweb publish latest 3.8   # rebuild the newest version from main in place, refresh the root
                           # pages, and rebase the 3.8 branch onto main
ovweb publish past   3.7   # rebuild an older minor from its own branch; the site root and
                           # `latest` are left alone
```

Add `--dry-run` to print the plan without building or pushing, or `--no-push` to do everything
locally and inspect the result before it goes out. The step-by-step description of what a publish
does is in [`publish-tool/README.md`](../publish-tool/README.md#what-a-publish-does); how to
preview the versioned layout locally is in [local-testing.md](local-testing.md).
