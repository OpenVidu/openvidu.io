---
name: edit-website
description: Modify the openvidu.io website (this repo, served from gh-pages at https://openvidu.io/) — landing, pricing, docs for OpenVidu Meet and OpenVidu Platform, research, support and other pages. Explains how pages are composed with MkDocs Material (nav, frontmatter, theme overrides/partials, shared snippets, tag system), the strict link rules, how the two products' docs are versioned with mike, and how to test locally with Docker. Use for any change to page content, structure, styling, templates, structured data, or navigation. Trigger phrases like "edit the website", "change the landing page", "update the pricing page", "add a docs page", "modify a section of openvidu.io".
---

# OpenVidu Website Editor

This repo is the source of https://openvidu.io/, built with **MkDocs Material** and deployed to the `gh-pages` branch. All pages are Markdown under `docs/`. The repo's [`README.md`](../../../README.md) is the authoritative reference for development, page-writing guidelines and versioning — this skill summarizes it plus repo conventions; when in doubt, re-read the README section in question.

## Branch to work on

- Documentation for the **current version in development** goes to the **`next` branch** (merged to `main` by an OpenVidu developer on release).
- Fixes to already-published content and non-versioned pages go to `main` (published via the "overwrite latest" flow below).

## Repo map

| Path | Purpose |
|---|---|
| `mkdocs.yml` | Site config: `nav`, theme, plugins (blog, rss, llmstxt, privacy, glightbox), markdown extensions |
| `docs/` | Content root. Non-versioned pages: `index.md` (landing), `blog/`, `pricing.md`, `support.md`, `about-us.md`, `research.md`, `openvidu-meet-vs-openvidu-platform.md`, `account.md`, `conditions/`, `acknowledgments.md` |
| `docs/meet/` | **OpenVidu Meet** docs (versioned, served at `/{version}/meet/`) |
| `docs/docs/` | **OpenVidu Platform** docs (versioned, served at `/{version}/docs/`) |
| `docs/overrides/` | Material theme customization (`custom_dir`): `main.html`, `home.html`, `404.html`, `partials/` |
| `shared/` | Reusable Markdown snippets, included via `--8<-- "shared/<file>.md"` (path relative to **repo root**). Organized by consuming docs area — `meet/`, `self-hosting/` (one folder per cloud provider + `common/`), `tutorials/` — see `shared/README.md` |
| `docs/assets/`, `docs/stylesheets/`, `docs/javascripts/` | Images, CSS, JS. Images/videos are organized by consuming page — versioned docs mirror the docs tree under `images/meet/**` and `images/platform/**` (for `docs/docs/**`), root pages get a top-level folder (`home/`, `pricing/`, ...), cross-cutting assets go in `logos/` (brand library), `og/`, `sponsors/`. No files directly at the `images/`/`videos/` root — see README "Organizing assets" |
| `publish-tool/` | `ovweb`, the publishing CLI, plus `ovweb.yaml` (site layout + redirect rules). Read its `README.md` before touching anything URL- or version-related |
| `.claude/skills/blog-*` | Use those skills for blog posts, not this one |

## Adding a new page (README: "Adding a new page")

1. Create the `.md` file under the right `docs/` folder, with frontmatter: `description` (unique, max 160 chars) and `title` (only required if the `nav` title is missing or not unique).
2. In `mkdocs.yml`: add it to `nav`, **and** to the `llmstxt` plugin `sections` (under `OpenVidu` for non-versioned pages, `OpenVidu Meet`/`OpenVidu Platform` for versioned ones), copying the page description.
3. If the page starts a new non-versioned or versioned area, add it to `non_versioned_pages` or `versioned_pages` in `publish-tool/ovweb.yaml`.

## Link rules (strict — the build is zero-warning and CI runs `mkdocs build --strict`)

One convention for Markdown, a separate one for raw HTML. Full detail in the README "Link rules" section.

- **Markdown links & images in regular pages → relative, including the `.md` extension**: `[x](../../self-hosting/local.md)`, `![x](../assets/images/foo.png#only-dark)`. Validated by MkDocs, navigable in the editor (root-absolute forms are not — editors resolve `/` against the repo root, not `docs/`), and version-safe. **Non-versioned pages are linked relatively too** (`[Pricing](../../pricing.md)`, **not** `/pricing/` — the bare-URL form was a pre-1.6 workaround that produced a build warning; the deploy script converts the built relative links to `/pricing/` at publish).
- **Markdown links & images in shared snippets and blog posts → root-absolute against `docs/`**: `[x](/docs/self-hosting/deployment-types.md)`, `![x](/assets/images/foo.png)`. Snippets render at different depths, so relative would break; `validation.links.absolute_links: relative_to_docs` validates these and rewrites them to relative at build time (same output as hand-written relative). Blog posts use the same form because a post's source file and asset folder move on publish (draft in literal `blog/posts/YYYY/MM/` + `assets/images/blog/YYYY/MM/<slug>/` placeholder folders → the real `<year>/<month>` folders) — see the `blog-*` skills. **One exception:** snippets included in **parallel deployment-type trees** (`single-node/oracle/` *and* `single-node-pro/oracle/`, etc.) that link a *sibling* page differing per tree (`../on-premises/admin.md`, `./admin.md`) stay **relative** on purpose. Only their *fixed*-target links are absolute.
- **Raw HTML links & images** (inside HTML blocks): MkDocs does **not** validate or rewrite these. Use the **absolute URL** form: `href="/pricing/"` for non-versioned pages, `src="/assets/images/foo.png"` for assets (also in snippets). Versioned pages stay version-correct because `ovweb` rewrites `src|href="/assets/`, `/javascripts/`, `/stylesheets/` → `"/X.Y/...` in versioned pages at publish time; non-versioned pages keep the root form. HTML links to versioned pages (rare) use relative-to-built-folder: `performance.md` builds to `performance/index.html`, so add one extra `../` vs the Markdown path (unless linking *from* an `index.md`).
- **Anchors:** `pymdownx.tabbed` tab labels (`=== "Foo"` → `#foo`) work at runtime but MkDocs's validator can't see the generated ids, so it logs a **false-positive `INFO` "no such anchor"**. Expected. `validation.links.anchors` is kept at `info` (not `warn`) so it never fails `--strict`; real broken anchors still show as `INFO`.
- **Never hardcode a pinned version** (`/3.8.0/...`) anywhere. From non-versioned/marketing content, versioned docs are reached as `/latest/meet/` or `/latest/docs/` (`ovweb` rewrites source-relative links this way; absolute URLs you emit yourself, e.g. in templates or structured data, must already use `latest` — see `overrides/partials/json-ld.html`).
- **The releases pages are the one exception.** In `docs/meet/releases.md` and `docs/docs/releases.md`, every link inside a version's release-notes section must be an **absolute, version-pinned** URL to **that same version** (links in the `3.4.0`/`3.4.x` sections → `/3.4/docs/...`). The *content* of these pages is copied into every version folder on publish, so relative or `/latest/` links would be wrong for most copies — `ovweb` **fails the publish** if it finds one. Version-pinning keeps each note pointing at the docs it describes, and the outdated-version banner explains the version jump. `ovweb` shields these `/X.Y/docs/`, `/X.Y/meet/` links from the version-stripping applied to other non-versioned pages.
- **Intentionally-non-nav pages** must be listed in `not_in_nav` in `mkdocs.yml`, or the build warns.

## How pages are composed

1. **Frontmatter drives behavior**:
   - `title`, `description` — SEO (see above).
   - `template: home.html` — the landing page uses a custom template.
   - `hide:` — `navigation`, `toc`, `footer`, `search-bar`, `version-selector`, `footer-prev`, `footer-next` (the non-standard ones are implemented in `overrides/main.html`).
   - **Tag system** (README: "Mkdocs Material tag system") — tags load the JS/CSS a page needs, and each expects a specific HTML structure: `setupwowjs` (wow.js animations, elements with class `wow`), `setupcardglow` (`.feature-cards > .grid.cards`), `setupcarousel` (Flickity, `.carousel > .carousel-cell`), `setupcustomgallery` (GLightbox for **HTML** `<a class="glightbox">` images/videos — NOT needed for plain Markdown images), `copyclipboard`; `Meet`/`Platform` tags load `meet.css`/`platform.css`. If you copy a visual pattern from another page, copy its tags too.
   - **Structured data lives in frontmatter**: `publications:` (research.md) and `faq:` (pricing.md) feed the JSON-LD emitted by `overrides/partials/json-ld.html`. When editing those page sections, update the matching frontmatter entry (anchors must equal heading ids; answers/abstracts must match visible content).
2. **Theme overrides** (`docs/overrides/`): `main.html` extends the Material base template with Jinja blocks (`extrahead`, `scripts`, `styles`, `outdated`...); `home.html` extends `main.html`; `partials/` adds/overrides partials (`header.html`, `footer.html`, `tabs.html`, `json-ld.html`). Site-wide changes go here — follow the "before/after" comment markers inside the blocks.
3. **Shared snippets**: grep for a snippet's usages before editing it — it may render on several pages (e.g. `shared/meet/meet-vs-platform-table.md` is on the landing page). New snippets: create under `shared/` in the folder matching the consuming docs area/provider (conventions in `shared/README.md`) and include with `--8<-- "shared/<folder>/<file>.md"`.
4. **HTML-in-Markdown**: pages mix raw HTML and Markdown via `md_in_html` (`<div markdown>`). Layout uses unsemantic-grid classes (`grid-50`, `grid-90`, `tablet-grid-...`). Material features in use: admonitions, `???` collapsible details, content tabs, attr_list (`{ .class }`, `{:target="_blank"}`).
5. **Theme-dependent images/videos**: Markdown images use the `#only-dark`/`#only-light` suffixes. For custom GLightbox HTML: the suffix goes in the `<img>`/`<video>` `src`, **not** in the parent `<a href>`, each `<a>` element must be a one-liner, and the page needs the `setupcustomgallery` tag.

## Versioning with mike — the part that bites

The two products' docs are **versioned**; everything else is not. URL scheme is version-first: `https://openvidu.io/{version}/meet/...` and `/{version}/docs/...`, with `latest` aliasing the newest release. Non-versioned pages live at the root (`/pricing/`, `/blog/`, ...).

**Versions are grouped by minor release and named `X.Y`** (e.g. `3.8`): one git branch, one `gh-pages` folder, one version-selector entry per minor. Each `X.Y` version's content reflects the **newest patch** of that minor — patch releases do not create new documentation versions (they update the existing `X.Y` in place, adding their section to the releases pages). Legacy exact-patch URLs (`/3.4.1/...`) redirect to the minor folder (`/3.4/...`) via the 404 page, whose rules are generated from `publish-tool/ovweb.yaml`.

The source tree has no version in paths: `mike` builds the site into a version folder on `gh-pages`, then `ovweb` rewrites links/canonicals/`sitemap.xml`/search index, does the same for the Markdown exports and `llms.txt` (whose links the plugin makes absolute against a versioned `site_url`, so they need their own patterns), moves the non-versioned pages to root, and writes the generated redirect pages (step table in `publish-tool/README.md`, "What a publish does").

**Publishing is done via the [Publish Web GitHub Action](https://github.com/OpenVidu/openvidu.io/actions/workflows/publish-web.yaml)** (or locally after `pip install "./publish-tool[build]"` — see README):

- `ovweb publish new X.Y` — new **minor** release: deploys the version, points `latest` at it, refreshes root non-versioned pages, and creates an `X.Y` git branch for future fixes to that version.
- `ovweb publish latest X.Y` — re-publish current `main` over the latest version (also rebases the version branch). This is how content fixes **and patch releases of the current minor** go live.
- `ovweb publish past X.Y` — fix an old minor (content fix or patch release): commit changes to the `X.Y` branch first; root pages are untouched.

Add `--dry-run` to any of them to print the resolved plan without building or pushing. Redirects are **not** hand-written HTML: declare them in `publish-tool/ovweb.yaml` (`redirects.files` for a known path, `redirects.patterns` for a shape of path) and the tool generates the page or the 404 rule.

Consequences when editing: changes to `docs/meet/` and `docs/docs/` are **not live until one of these runs**; past versions are edited on their `X.Y` branches, not `main`.

**Releases pages** (`docs/meet/releases.md`, `docs/docs/releases.md`) have their own conventions: each minor gets a top-level `## X.Y.0` section, and later patches of that minor go in a subsection beneath it (under `### Patch releases`, as `#### X.Y.Z`) — never a new top-level section. The `scrolltoversion` frontmatter tag auto-jumps to the viewed minor's `## X.Y.0` heading. Their links must be absolute and version-pinned (see Link rules). On publish, only the **content** of the latest page (notes + table of contents) is spliced into every version folder's releases page — the surrounding page stays that version's own, so `/3.4/docs/releases/` keeps 3.4's navigation and shows the outdated-version banner.

**Reachability caveat**: since each `X.Y` folder always serves its **newest patch**, older patches' docs are never published and are unreachable. If you remove or rename a page or anchor that an older patch's release notes link to, that link breaks with nothing to fall back to — prefer additive changes, and fix affected release-notes links when a target moves.

## Sync with livekit-tutorials.openvidu.io

Any change to the **tutorials documentation** must also be reflected in the [livekit-tutorials-docs](https://github.com/OpenVidu/livekit-tutorials-docs) repo (published at livekit-tutorials.openvidu.io via its own Publish Web action). Flag this to the user whenever you touch tutorial pages.

## Local testing

The dev image is a custom build of `squidfunk/mkdocs-material` with the repo's extra plugins (tagged over the upstream name). Build it once, then serve with live reload:

```bash
docker build --pull --no-cache --rm=true -t squidfunk/mkdocs-material .
docker run --name=mkdocs-old --rm -it -p 9000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
```

Then open http://localhost:9000. To produce a full build instead: `docker run --rm -it -v ${PWD}:/docs -e GOOGLE_ANALYTICS_KEY=G-XXXXXXXX squidfunk/mkdocs-material build`.

Notes:

- Run from the repo root. When running non-interactively (scripts, agents), drop `-it`.
- If host port 9000 is taken (it often is on dev machines), map another one, e.g. `-p 9100:8000` — do not stop whatever holds 9000.
- Watch the console: the build must be **zero `WARNING`s**. Broken links appear as warnings (and CI's `mkdocs build --strict` turns them into hard failures). `INFO` messages about anchors are expected — most are `pymdownx.tabbed` tab-anchor false positives (see Link rules); still scan them for a genuinely renamed/removed heading when you touch headings.
- The dev server serves a **single unversioned site at the root** (`/meet/`, not `/latest/meet/`) and overrides `site_url`, so canonicals and JSON-LD show `http://0.0.0.0:8000/...` locally. Both are expected; version handling happens at deploy time. To preview the real versioned layout, use `mike serve` against `gh-pages` (see README "Testing versioning locally").

## Checklist before finishing

1. Working on the right branch (`next` for in-development docs, `main` for fixes to published content).
2. Page renders correctly locally (both light and dark themes if you touched styling or theme-dependent images).
3. **Zero `WARNING`s** in the mkdocs console (`mkdocs build --strict` must pass — CI enforces it). Anchor `INFO`s are expected (tab-anchor false positives).
4. New pages: `nav` + `llmstxt` sections updated; `publish-tool/ovweb.yaml` updated if a new area was created; intentionally-non-nav pages added to `not_in_nav`.
5. Links follow the rules above (Markdown in pages → relative `.md`/asset paths; Markdown in snippets and blog posts → root-absolute; raw HTML → absolute URL (`/pricing/`, `/assets/…`), built-folder-relative only for HTML→versioned-page links; no pinned versions outside releases pages).
6. If you touched a section backed by frontmatter data (`faq`, `publications`) or a shared snippet, its counterparts are updated too.
7. Tutorials touched? Remind the user to sync livekit-tutorials-docs.
