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
| `shared/` | Reusable Markdown snippets, included via `--8<-- "shared/<file>.md"` (path relative to **repo root**) |
| `docs/assets/`, `docs/stylesheets/`, `docs/javascripts/` | Images, CSS, JS |
| `custom-versioning/` | Versioning/deploy scripts — read `push-new-version.sh` before touching anything URL- or version-related |
| `.claude/skills/blog-*` | Use those skills for blog posts, not this one |

## Adding a new page (README: "Adding a new page")

1. Create the `.md` file under the right `docs/` folder, with frontmatter: `description` (unique, max 160 chars) and `title` (only required if the `nav` title is missing or not unique).
2. In `mkdocs.yml`: add it to `nav`, **and** to the `llmstxt` plugin `sections` (under `OpenVidu` for non-versioned pages, `OpenVidu Meet`/`OpenVidu Platform` for versioned ones), copying the page description.
3. If the page starts a new non-versioned or versioned area, add it to the `NON_VERSIONED_PAGES` or `VERSIONED_PAGES` array in `custom-versioning/push-new-version.sh`.

## Link rules (strict — deploy scripts depend on them)

- **Markdown links**: relative paths to the target **`.md` file including the extension** (e.g. `[link](../dir2/bar.md)`). Since MkDocs 1.6 an absolute form relative to `docs/` also works (`[link](/dir2/bar.md)`) — this is the way to link from **shared snippets**, which are embedded in pages at different hierarchy levels.
- **HTML links** (inside raw HTML blocks): relative paths to the **built folder**. `performance.md` builds to `performance/index.html`, so add one extra `../` compared to the markdown path — unless linking *from* an `index.md`.
- **Links to non-versioned pages must be absolute** (e.g. `/pricing/`). The local server will warn about these — that's the only acceptable warning category.
- **Never hardcode a pinned version** (`/3.8.0/...`) anywhere. From non-versioned/marketing content, versioned docs are reached as `/latest/meet/` or `/latest/docs/` (the deploy script rewrites source-relative links this way; absolute URLs you emit yourself, e.g. in templates or structured data, must already use `latest` — see `overrides/partials/json-ld.html`).

## How pages are composed

1. **Frontmatter drives behavior**:
   - `title`, `description` — SEO (see above).
   - `template: home.html` — the landing page uses a custom template.
   - `hide:` — `navigation`, `toc`, `footer`, `search-bar`, `version-selector`, `footer-prev`, `footer-next` (the non-standard ones are implemented in `overrides/main.html`).
   - **Tag system** (README: "Mkdocs Material tag system") — tags load the JS/CSS a page needs, and each expects a specific HTML structure: `setupwowjs` (wow.js animations, elements with class `wow`), `setupcardglow` (`.feature-cards > .grid.cards`), `setupcarousel` (Flickity, `.carousel > .carousel-cell`), `setupcustomgallery` (GLightbox for **HTML** `<a class="glightbox">` images/videos — NOT needed for plain Markdown images), `copyclipboard`; `Meet`/`Platform` tags load `meet.css`/`platform.css`. If you copy a visual pattern from another page, copy its tags too.
   - **Structured data lives in frontmatter**: `publications:` (research.md) and `faq:` (pricing.md) feed the JSON-LD emitted by `overrides/partials/json-ld.html`. When editing those page sections, update the matching frontmatter entry (anchors must equal heading ids; answers/abstracts must match visible content).
2. **Theme overrides** (`docs/overrides/`): `main.html` extends the Material base template with Jinja blocks (`extrahead`, `scripts`, `styles`, `outdated`...); `home.html` extends `main.html`; `partials/` adds/overrides partials (`header.html`, `footer.html`, `tabs.html`, `json-ld.html`). Site-wide changes go here — follow the "before/after" comment markers inside the blocks.
3. **Shared snippets**: grep for a snippet's usages before editing it — it may render on several pages (e.g. `shared/meet/meet-vs-platform-table.md` is on the landing page). New snippets: create under `shared/` and include with `--8<-- "shared/<file>.md"`.
4. **HTML-in-Markdown**: pages mix raw HTML and Markdown via `md_in_html` (`<div markdown>`). Layout uses unsemantic-grid classes (`grid-50`, `grid-90`, `tablet-grid-...`). Material features in use: admonitions, `???` collapsible details, content tabs, attr_list (`{ .class }`, `{:target="_blank"}`).
5. **Theme-dependent images/videos**: Markdown images use the `#only-dark`/`#only-light` suffixes. For custom GLightbox HTML: the suffix goes in the `<img>`/`<video>` `src`, **not** in the parent `<a href>`, each `<a>` element must be a one-liner, and the page needs the `setupcustomgallery` tag.

## Versioning with mike — the part that bites

The two products' docs are **versioned**; everything else is not. URL scheme is version-first: `https://openvidu.io/{version}/meet/...` and `/{version}/docs/...`, with `latest` aliasing the newest release. Non-versioned pages live at the root (`/pricing/`, `/blog/`, ...).

The source tree has no version in paths: `mike` builds the site into a version folder on `gh-pages`, then `custom-versioning/push-new-version.sh` rewrites links/canonicals/`llms.txt`/`sitemap.xml` and moves the non-versioned pages to root (the README's "Understanding the versioning script" section details all 8 steps).

**Publishing is done via the [Publish Web GitHub Action](https://github.com/OpenVidu/openvidu.io/actions/workflows/publish-web.yaml)** (or locally with `mike` + the scripts — see README):

- `push-new-version.sh X.Y.Z` — new release: deploys the version, points `latest` at it, refreshes root non-versioned pages, and creates an `X.Y.Z` git branch for future fixes to that version.
- `overwrite-latest-version.sh X.Y.Z` — re-publish current `main` over the latest version (also rebases the version branch). This is how content fixes go live.
- `overwrite-past-version.sh X.Y.Z` — fix an old version: commit changes to the `X.Y.Z` branch first; root pages are untouched.

Consequences when editing: changes to `docs/meet/` and `docs/docs/` are **not live until one of these runs**; past versions are edited on their `X.Y.Z` branches, not `main`.

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
- Watch the console: broken links appear as **warnings**, not failures. The only acceptable link warnings are absolute paths to non-versioned pages (`/pricing/` etc.).
- The dev server serves a **single unversioned site at the root** (`/meet/`, not `/latest/meet/`) and overrides `site_url`, so canonicals and JSON-LD show `http://0.0.0.0:8000/...` locally. Both are expected; version handling happens at deploy time. To preview the real versioned layout, use `mike serve` against `gh-pages` (see README "Testing versioning locally").

## Checklist before finishing

1. Working on the right branch (`next` for in-development docs, `main` for fixes to published content).
2. Page renders correctly locally (both light and dark themes if you touched styling or theme-dependent images).
3. No new warnings in the mkdocs console beyond absolute-path-to-non-versioned-page warnings.
4. New pages: `nav` + `llmstxt` sections updated; `NON_VERSIONED_PAGES`/`VERSIONED_PAGES` arrays updated if a new area was created.
5. Links follow the rules above (markdown → `.md` relative; HTML → built-folder relative; non-versioned → absolute; no pinned versions).
6. If you touched a section backed by frontmatter data (`faq`, `publications`) or a shared snippet, its counterparts are updated too.
7. Tutorials touched? Remind the user to sync livekit-tutorials-docs.
