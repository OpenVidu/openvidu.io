# CLAUDE.md

Source of https://openvidu.io — MkDocs Material (pinned 9.7.6) + mike, published to `gh-pages`.
Two versioned products: **OpenVidu Meet** (`docs/meet/`, served at `/{version}/meet/`) and
**OpenVidu Platform** (`docs/docs/`, served at `/{version}/docs/`), plus non-versioned root pages
(landing, pricing, support, blog, …). **Merging to `main` publishes nothing** — the live site only
changes when the manual [Publish Web workflow](.github/workflows/publish-web.yaml) runs.

Authoritative references — read the relevant one before working:

- [`README.md`](README.md) — development, page-writing guidelines, link rules, assets, tag
  system, versioning.
- [`publish-tool/README.md`](publish-tool/README.md) — the `ovweb` CLI, redirects, what a
  publish does.
- [`shared/README.md`](shared/README.md) — snippet folder layout.
- Skills: blog work → `blog-plan`/`blog-write`/`blog-review`; page edits → `edit-website`;
  release-day publishing → `release-version`. Commands: `/check-web`, `/publish-post`, `/serve`.

## Branches

- `next` — docs for the version in development (merged to `main` on release).
- `main` — fixes to published content and non-versioned pages.
- `X.Y` — past versions; fixes to an old minor are committed there, never to `main`.

## The build rule

`mkdocs build --strict` must pass with **zero WARNINGs** (CI enforces it on every PR). Anchor
`INFO` lines include ~110 false positives from `pymdownx.tabbed` tab anchors — expected; do not
try to fix them and do not raise `validation.links.anchors` above `info`.

## Link rules (wrong form = broken page or failed publish)

| Context | Form | Example |
|---|---|---|
| Regular pages (Markdown) | relative, with `.md` | `[x](../../pricing.md)` |
| `shared/` snippets + blog posts (Markdown) | root-absolute, with `.md` | `[x](/docs/self-hosting/local.md)` |
| Raw HTML (`href`/`src`) | absolute URL form — **MkDocs never validates HTML; check targets by hand** | `href="/pricing/"`, `src="/assets/images/x.png"` |
| Releases pages + `Release` blog posts | full-domain, version-pinned, never `latest` | `https://openvidu.io/3.8/docs/...` |

Never hardcode a version (`/3.8/...`) outside the releases pages and Release blog posts. Full
rationale: README "Link rules".

## Frontmatter

Every page requires `title` (≤57 chars — Material appends `" - OpenVidu"`) and `description`
(100–160 chars, ending in a full stop), both unique site-wide. The build fails on any
llmstxt-selected page missing either (`publish-tool/mkdocs_hook.py`), and the globs select
nearly every page.

## Structural invariants

- `nav` in `mkdocs.yml` is a literal tree: every new page goes in `nav` or in `not_in_nav`.
- Renaming, moving or deleting a published page requires a redirect rule in
  `publish-tool/ovweb.yaml` (`redirects:`). Never retire a URL silently.
- A new top-level content area must be registered in `ovweb.yaml` `layout`
  (`versioned_pages`/`non_versioned_pages`).
- `shared/` snippets render inside many pages — grep for the snippet's `--8<--` usages before
  editing one.
- The `tags:` frontmatter loads per-page JS/CSS (README "Mkdocs Material tag system"). Copying a
  visual pattern from another page → copy its tags too.
- The mkdocs-material pin is named in three places (`publish-tool/pyproject.toml`, `Dockerfile`,
  `Dockerfile.mike`) and must agree — `ovweb doctor --pins` checks it.

## Versioning

Versions are grouped by minor (`X.Y`): one git branch, one gh-pages folder, one selector entry,
each serving its newest patch. "OpenVidu Platform" as a product name exists only from 3.4 — do
not use it in copy targeting older versions.

## Commands

| Task | Command |
|---|---|
| Build the dev image (once) | `docker build --pull --no-cache --rm=true -t squidfunk/mkdocs-material .` |
| Serve with live reload | `docker run --name=mkdocs --rm -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material` |
| Strict build (what CI runs) | `CI=false GOOGLE_ANALYTICS_KEY=G-XXXXXXXX mkdocs build --strict -d /tmp/site` (needs `pip install "./publish-tool[validate]"`) |
| publish-tool tests | `cd publish-tool && pytest && ruff check . && ruff format --check .` |
| Environment/pins check | `ovweb doctor` (`--pins` for the pin agreement only) |
| Convention lint (what `--strict` can't see: raw-HTML links, link form, version pins, SEO budgets) | `ovweb lint` — or the `/check-web` command |
| Redirect rules check | `ovweb redirects check` |
| Published-tree invariants | `ovweb verify` |
| Versioned-layout preview | `mike serve` — see README "Testing versioning locally" |

Non-interactive runs: drop `-it` from docker commands. The dev server serves an unversioned site
at the root with local canonicals — both expected; version handling happens at publish time.
