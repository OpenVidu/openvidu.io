---
name: edit-website
description: Modify the openvidu.io website (this repo) — landing, pricing, docs for OpenVidu Meet and OpenVidu Platform, blog-adjacent pages, templates, navigation, styling. Routes each task to the canonical doc in contributing/. Trigger phrases like "edit the website", "change the landing page", "update the pricing page", "add a docs page", "modify a section of openvidu.io".
---

# OpenVidu Website Editor

This repo is the source of https://openvidu.io/ (MkDocs Material → `gh-pages`; content under
`docs/`). `CLAUDE.md` carries the always-on invariants; this skill is the workflow. The
knowledge lives in [`contributing/`](../../../contributing/) — read the file that matches the
task before editing.

## Branch to work on

`next` for the version in development, `main` for fixes to published content, `X.Y` for past
versions — details in [`contributing/versioning.md`](../../../contributing/versioning.md).

## Read the doc that matches the task

| Task touches… | Read first |
|---|---|
| Any internal link or image reference | [`contributing/link-rules.md`](../../../contributing/link-rules.md) |
| A new page, snippet or asset (placement, frontmatter, nav, llmstxt, layout) | [`contributing/authoring.md`](../../../contributing/authoring.md) + [`shared/README.md`](../../../shared/README.md) |
| HTML blocks, `page_features:`, theme overrides/partials, JSON-LD frontmatter, light/dark images | [`contributing/page-composition.md`](../../../contributing/page-composition.md) |
| URLs, versions, redirects, the releases pages | [`contributing/versioning.md`](../../../contributing/versioning.md) (+ [`publish-tool/README.md`](../../../publish-tool/README.md)) |
| Blog posts | The `blog-plan`/`blog-write`/`blog-review` skills, not this one |

## The facts that bite most often

- **Copy a visual pattern → copy its `page_features:` too** — the feature keys load the JS/CSS
  the pattern needs.
- **GLightbox HTML**: the `#only-dark`/`#only-light` suffix goes in the `<img>`/`<video>` `src`,
  never in the parent `<a href>`, and each `<a>` must be a one-liner.
- **`shared/` snippets render on many pages** — grep the snippet's `--8<--` usages before
  editing one.
- **Touched a tutorial page?** Flag the livekit-tutorials-docs sync to the user (procedure at
  the end of `contributing/authoring.md`).

## Local testing

`/serve` starts the dev server; `/check-web` validates like CI. Expected local behaviors
(unversioned root, local canonicals) and the versioned-layout preview are in
[`contributing/local-testing.md`](../../../contributing/local-testing.md).

## Checklist before finishing

0. `ovweb lint` reports no errors (or run `/check-web full` for link-heavy work). CI runs it on
   every PR.
1. Working on the right branch (`next` for in-development docs, `main` for fixes to published
   content).
2. Page renders correctly locally (both light and dark themes if you touched styling or
   theme-dependent images).
3. **Zero `WARNING`s** in the mkdocs console (`mkdocs build --strict` must pass — CI enforces
   it). Anchor `INFO`s are expected (tab-anchor false positives).
4. New pages: `nav` updated, `title` + `description` frontmatter present and within budget,
   `llmstxt` section line only if no glob covers the folder, `publish-tool/ovweb.yaml` updated
   if a new area was created, intentionally-non-nav pages in `not_in_nav`.
5. Links follow [`contributing/link-rules.md`](../../../contributing/link-rules.md); no pinned
   versions outside the releases pages.
6. If you touched a section backed by frontmatter data (`faq`, `publications`) or a shared
   snippet, its counterparts are updated too.
7. Renamed, moved or deleted a published page? It needs a redirect rule in
   `publish-tool/ovweb.yaml` — never retire a URL silently.
8. Tutorials touched? Remind the user to sync livekit-tutorials-docs.
