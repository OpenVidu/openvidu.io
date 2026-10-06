# CLAUDE.md

Source of https://openvidu.io — Zensical (pinned 0.0.68; Material for MkDocs' successor, configured
in `mkdocs.yml`) + the Zensical fork of mike, published to `gh-pages`.
Two versioned products: **OpenVidu Meet** (`docs/meet/`, served at `/{version}/meet/`) and
**OpenVidu Platform** (`docs/docs/`, served at `/{version}/docs/`), plus non-versioned root pages
(landing, pricing, support, blog, …). **Merging to `main` publishes nothing** — the live site only
changes when the manual [Publish Web workflow](.github/workflows/publish-web.yaml) runs, which
then redeploys the docs MCP server (`OpenVidu/openvidu-docs-mcp`) and waits for it.

Authoritative references — read the relevant one before working:

- [`contributing/`](contributing/) — the canonical contributor docs:
  [`authoring.md`](contributing/authoring.md) (pages, snippets, assets),
  [`link-rules.md`](contributing/link-rules.md),
  [`page-composition.md`](contributing/page-composition.md) (page features, overrides, HTML, light/dark),
  [`versioning.md`](contributing/versioning.md) (branches, releases pages, publishing),
  [`local-testing.md`](contributing/local-testing.md),
  [`checks.md`](contributing/checks.md) (lint, CI),
  [`zensical-migration.md`](contributing/zensical-migration.md) (what Zensical cannot do yet, the
  bugs found, what the publish does instead).
- [`publish-tool/README.md`](publish-tool/README.md) — the `ovweb` CLI and what a publish does;
  design internals in [`publish-tool/docs/`](publish-tool/docs/).
- [`shared/README.md`](shared/README.md) — snippet folder layout.
- [`README.md`](README.md) — the repo index (repository map + full documentation index).
- Skills: blog work → `blog-plan`/`blog-write`/`blog-review` (conventions in
  `.claude/skills/blog-write/references/conventions.md`); page edits → `edit-website`;
  release-day publishing → `release-version`; demo videos → `video-recording`. Commands:
  `/check-web`, `/publish-post`, `/serve`. Agents: PR review → `pr-reviewer`. A `PostToolUse`
  hook auto-lints every edit to `docs/`, `shared/` or the overrides — fix what it reports.

## Branches

- `next` — docs for the version in development (merged to `main` on release).
- `main` — fixes to published content and non-versioned pages.
- `X.Y` — past versions; fixes to an old minor are committed there, never to `main`.

## The build rule

`zensical build --strict` must pass with **no issues** (CI enforces it on every PR). Anchor
validation is off in `mkdocs.yml` (`invalid_link_anchors: false`): Zensical would report ~110
false positives from `pymdownx.tabbed` tab anchors; `ovweb lint --site` is the anchor check. Build
and serve from the repository root (the snippet path is relative to the working directory).

## Link rules (wrong form = broken page or failed publish)

| Context | Form | Example |
|---|---|---|
| Regular pages + blog posts (Markdown) | relative, with `.md` | `[x](../../pricing.md)`, in a post `[x](../../../../docs/x.md)` |
| `shared/` snippets (Markdown) | root-absolute, with `.md` | `[x](/docs/self-hosting/local.md)` |
| Raw HTML (`href`/`src`) | absolute URL form — **the build never validates HTML; check targets by hand**. A relative one is rewritten like Markdown (source-relative, `../` added on non-index pages) | `href="/pricing/"`, `src="/assets/images/x.png"` |
| Releases pages + `Release` blog posts | full-domain, version-pinned, never `latest` | `https://openvidu.io/3.8/docs/...` |

Never hardcode a version (`/3.8/...`) outside the releases pages and Release blog posts. Full
rationale: [`contributing/link-rules.md`](contributing/link-rules.md).

## Frontmatter

Every page requires `title` (≤57 chars — the theme appends `" - OpenVidu"`) and `description`
(100–160 chars, ending in a full stop), both unique site-wide. `ovweb lint` errors on a page
missing either: the publish reads both off the page for its `llms.txt` entry.

Blog posts date themselves with a `date:` mapping, `created` plus `updated`: **any edit to a
published post sets `date.updated` to the day it merges** — automated release-review PRs included.

## Structural invariants

- `nav` in `mkdocs.yml` is a literal tree: every new page goes in `nav`, or in the comment above
  it listing the pages reached by direct link only (Zensical has no `not_in_nav` check).
- Renaming, moving or deleting a published page requires a redirect rule in
  `publish-tool/ovweb.yaml` (`redirects:`). Never retire a URL silently.
- A new top-level content area must be registered in `ovweb.yaml` `layout`
  (`versioned_pages`/`non_versioned_pages`).
- `shared/` snippets render inside many pages — grep for the snippet's `--8<--` usages before
  editing one.
- The `page_features:` frontmatter loads per-page JS/CSS
  ([`contributing/page-composition.md`](contributing/page-composition.md)). Copying a visual
  pattern from another page → copy its feature keys too. `tags:` is blog taxonomy only.
- Tutorials are published twice: every edit under `docs/docs/tutorials/` or `shared/tutorials/`
  must be mirrored in `livekit-tutorials-docs` (LiveKit-first framing), whose
  `tools/sync-check.py` verifies the two stay in step —
  [`contributing/authoring.md`](contributing/authoring.md).
- The zensical pin is named in four places (`publish-tool/pyproject.toml`, `Dockerfile`,
  `Dockerfile.mike`, `publish-tool/requirements-publish.txt`) and must agree, as must the
  commit of the mike fork — `ovweb doctor --pins` checks it. After changing a pin, regenerate
  the lock ([`publish-tool/README.md`](publish-tool/README.md), "Dependency pins").
- Zensical has no hooks. What the MkDocs hooks did lives in `ovweb`: two Markdown extensions
  (`publish-tool/src/ovweb/mdx/`, listed in `mkdocs.yml`) and two publish steps (the sitemap
  `<lastmod>`, the `llms.txt` titles and descriptions). The past `X.Y` branches (3.0–3.9) still
  build with MkDocs and cannot be re-published by this toolchain until migrated
  ([`contributing/versioning.md`](contributing/versioning.md)).

## Versioning

Versions are grouped by minor (`X.Y`): one git branch, one gh-pages folder, one selector entry,
each serving its newest patch. "OpenVidu Platform" as a product name exists only from 3.4 — do
not use it in copy targeting older versions.

## Commands

| Task | Command |
|---|---|
| Build the dev image (once) | `docker build --pull --no-cache --rm=true -t openvidu-io .` |
| Serve with live reload | `docker run --name=zensical --rm -p 8000:8000 -v ${PWD}:/docs openvidu-io` |
| Strict build (what CI runs) | `CI=false GOOGLE_ANALYTICS_KEY=G-XXXXXXXX zensical build --strict` — output in `site/` (needs `pip install "./publish-tool[validate]"`) |
| publish-tool tests | `cd publish-tool && pytest && ruff check . && ruff format --check .` |
| Environment/pins check | `ovweb doctor` (`--pins` for the pin agreement only; needs a non-editable `pip install "./publish-tool[build]"` — the `[validate]` extra has no mike, so doctor reports it missing) |
| Convention lint (what `--strict` can't see: raw-HTML links, link form, version pins, SEO budgets) | `ovweb lint` — or the `/check-web` command |
| Redirect rules check | `ovweb redirects check` |
| Published-tree invariants | `ovweb verify` |
| Versioned-layout preview | `mike serve` — see [`contributing/local-testing.md`](contributing/local-testing.md) |

Non-interactive runs: drop `-it` from docker commands. The dev server serves an unversioned site
at the root — expected; version handling happens at publish time. The image runs as root, so a
`site/` or `.cache/` it writes into the checkout is root-owned: remove them through the image
(`docker run --rm -v ${PWD}:/docs --entrypoint sh openvidu-io -c 'rm -rf /docs/site /docs/.cache'`).
