# openvidu.io

Source of [https://openvidu.io](https://openvidu.io) — an MkDocs Material site versioned with
[mike](https://github.com/jimporter/mike) and published to the `gh-pages` branch by `ovweb`, the
CLI in [`publish-tool/`](publish-tool/). `docs/` is **site content**; the contributor
documentation lives in [`contributing/`](contributing/). **Merging to `main` publishes
nothing** — the live site only changes when the manual
[Publish Web workflow](https://github.com/OpenVidu/openvidu.io/actions/workflows/publish-web.yaml)
runs.

## Working with AI (the recommended daily workflow)

This repo is tooled for [Claude Code](https://claude.com/claude-code): [`CLAUDE.md`](CLAUDE.md)
is loaded automatically and routes to everything below, so for most tasks you just say what you
want.

| I want to… | Use |
|---|---|
| Edit a page, template, nav entry or style | Just ask — the `edit-website` skill triggers |
| Plan / write / review a blog post | The `blog-plan` / `blog-write` / `blog-review` skills |
| Publish a draft blog post | `/publish-post <slug>` |
| Serve the site locally | `/serve` |
| Validate my changes the way CI will | `/check-web` (add `full` for the strict build) |
| Do the release-day docs work and publish | The `release-version` skill |
| Review a content PR against the conventions | The `pr-reviewer` agent ("review PR 105") |
| Record an embedded-meeting demo video | The `video-recording` skill |

Two safety nets back this up: a hook lints every AI edit to `docs/`, `shared/` or the theme
overrides the moment it happens (errors bounce straight back to the agent), and every PR runs
the **Validate Web** gate — pins, redirect rules, convention lint, strict build, built-site
link+anchor lint. Details: [`contributing/checks.md`](contributing/checks.md).

## Quickstart (manual)

```bash
# Once: build the dev image (mkdocs-material + this repo's extra plugins)
docker build --pull --no-cache --rm=true -t squidfunk/mkdocs-material .

# Serve with live reload at http://localhost:8000
docker run --name=mkdocs --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
```

Everything else — full builds, validating like CI, previewing the versioned layout — is in
[`contributing/local-testing.md`](contributing/local-testing.md).

## Repository map

| Path | Purpose |
|---|---|
| [`mkdocs.yml`](mkdocs.yml) | Site config: `nav`, theme, plugins, markdown extensions |
| [`docs/`](docs/) | Content root. Non-versioned pages at the top level (landing, pricing, blog, …) |
| [`docs/meet/`](docs/meet/) | **OpenVidu Meet** docs (versioned, served at `/{version}/meet/`) |
| [`docs/docs/`](docs/docs/) | **OpenVidu Platform** docs (versioned, served at `/{version}/docs/`) |
| [`overrides/`](overrides/) | Material theme customization (`main.html`, `home.html`, `partials/`) |
| [`shared/`](shared/) | Reusable Markdown snippets, included with `--8<--` |
| `docs/assets/`, `docs/stylesheets/`, `docs/javascripts/` | Images/videos (organized by consuming page), CSS, JS |
| [`publish-tool/`](publish-tool/) | `ovweb`, the publishing CLI, plus `ovweb.yaml` (site layout + every redirect) |
| [`contributing/`](contributing/) | The contributor documentation (index below) |
| [`.claude/`](.claude/) | The AI tooling: skills, commands, agents, hooks, permissions |
| [`.github/workflows/`](.github/workflows/) | CI: PR validation, manual publish, weekly link check, tool tests |

## Documentation index

| Read when… | File |
|---|---|
| Adding a page, a shared snippet or an asset | [`contributing/authoring.md`](contributing/authoring.md) |
| Writing any internal link or image reference | [`contributing/link-rules.md`](contributing/link-rules.md) |
| Using HTML blocks, tags, theme overrides, light/dark images, JSON-LD | [`contributing/page-composition.md`](contributing/page-composition.md) |
| Anything about versions, branches, releases pages or publishing | [`contributing/versioning.md`](contributing/versioning.md) |
| Serving/building locally | [`contributing/local-testing.md`](contributing/local-testing.md) |
| Understanding the checks: `ovweb lint`, the hook, the CI workflows | [`contributing/checks.md`](contributing/checks.md) |
| Placing a snippet in the right `shared/` folder | [`shared/README.md`](shared/README.md) |
| Blog conventions (naming, drafts, frontmatter, publishing) | [`.claude/skills/blog-write/references/conventions.md`](.claude/skills/blog-write/references/conventions.md) |
| Using `ovweb` (commands, what a publish does) | [`publish-tool/README.md`](publish-tool/README.md) |
| The publishing design internals (redirects, rewriting, sitemaps, splice, verify) | [`publish-tool/docs/`](publish-tool/docs/) — indexed in the tool README |
| The always-on invariants an AI session starts from | [`CLAUDE.md`](CLAUDE.md) |

## Branches & publishing

`next` holds the docs for the version in development, `main` the published content, and each
`X.Y` branch a past version. Merging publishes nothing: run the
[Publish Web action](https://github.com/OpenVidu/openvidu.io/actions/workflows/publish-web.yaml)
when a change must go live. The whole model — and the strict releases-pages contract — is in
[`contributing/versioning.md`](contributing/versioning.md).

## Sync with livekit-tutorials.openvidu.io

Changes to the tutorials documentation must be mirrored to
[livekit-tutorials-docs](https://github.com/OpenVidu/livekit-tutorials-docs) — the procedure is
at the end of [`contributing/authoring.md`](contributing/authoring.md).
