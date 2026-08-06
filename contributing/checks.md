# Checks and CI

Every convention in these docs is enforced by a tool, in four layers:

| Layer | When it runs | What |
|---|---|---|
| Edit-time hook | on every AI edit | [`.claude/hooks/lint-changed-file.sh`](../.claude/hooks/lint-changed-file.sh) runs `ovweb lint` on the changed file |
| `ovweb lint` | on demand, ~1 s, no build | authoring conventions the strict build cannot see |
| `mkdocs build --strict` | on demand + every PR | zero-WARNING build; broken Markdown links fail it |
| CI workflows | PRs, weekly, manual | the four workflows below |

`/check-web` runs the lint tier; `/check-web full` adds the strict build and the built-site lint —
the exact sequence CI runs.

## `ovweb lint`

Where `ovweb verify` asserts a *published* tree (see
[`publish-tool/README.md`](../publish-tool/README.md)), `ovweb lint` checks the *sources* — the
authoring conventions `mkdocs build --strict` cannot see, in about a second and with no build:

- **Raw-HTML links and images** (`href="/…"`, `src="/…"`): MkDocs never processes HTML, so a
  broken target there survives every build. Resolved against the source tree, `latest/`-prefixed
  URLs included; a `.md` path inside HTML is its own finding.
- **Link form in the files that move at publish**: a relative Markdown link in a blog post
  (error — it breaks when the post moves) or in a shared snippet (warn — only the sibling links
  [link-rules.md](link-rules.md) documents as deliberate stay relative, and those are
  recognized), and the `page.md/#anchor` stray-slash form.
- **Version-pin discipline**: `/X.Y/` links are allowed only on the two releases pages and in
  `Release` blog posts; the releases pages themselves must never link `latest` (the publish
  refuses it — lint catches it at PR time instead).
- **SEO budgets** (warn): `title` over 57 characters (70 for posts), `description` over 160 or
  not a sentence, duplicated titles/descriptions site-wide. Presence stays a build error in
  `mkdocs_hook.py` — a missing field must kill CI, but a long one must not kill `mkdocs serve`.
- **Page composition**: `!!!warning`-without-space admonitions; the functional `tags:` contract
  (a page whose content — snippets included — carries `glightbox`/`feature-cards`/`carousel`
  markup should declare the matching tag); `<img>` elements without `alt` text; files at the
  `assets/images|videos/` root; unpaired `#only-light`/`#only-dark`; blog posts referencing
  another post's asset folder; snippet filenames repeating their folder.
- **Commented-out dead links** (info): janitorial, since MkDocs skips comments too.

Findings live in code fences, inline code and HTML comments are excluded before matching, so a
documentation example never trips a check. Severity is decided in the checker, not by the
reader: `error` fails CI (exit 1), `warn` and `info` do not. **Never silence a finding by
weakening the checker** — fix the content, or discuss the rule. `ovweb lint PATH…` limits the
report to the given files.

### `ovweb lint --against REF`

Closes the gap none of the other checks can see: a *missing* redirect rule. Every page that
existed in `REF` (e.g. `origin/main`) and is gone from the working tree must be claimed by a rule
in `ovweb.yaml` — a `files` rule naming its URL or an expansion covering it — because retiring a
published URL silently is the 404 class that only surfaces months later in Search Console. Blog
posts are exempt (their URLs come from `date`+`slug`, and drafts move at publish by design).
Validate Web runs it on every PR against the PR's base branch.

### `ovweb lint --site DIR`

Adds the built-site tier over a `mkdocs build` output: every internal `href`/`src`/`srcset` —
full-domain `https://openvidu.io/…` and `/latest/…` forms included — must resolve within the
built tree, and every `#fragment` must name an id actually present on the target page. The built
HTML carries the `pymdownx.tabbed` ids the MkDocs validator cannot see, so this is the
authoritative anchor check with none of the ~110 INFO false positives. Version-pinned URLs (only
production serves those folders), external URLs (the scheduled link-check workflow's job),
SPA-style `#/…` routing fragments of the OpenAPI viewer, and the generated `reference-docs/`
trees as sources are all excluded by design.

## The edit-time hook

[`.claude/settings.json`](../.claude/settings.json) registers a `PostToolUse` hook: every
Edit/Write to `docs/**/*.md`, `shared/**/*.md` or `docs/overrides/**/*.html` is immediately
linted, and error-severity findings bounce back to the agent (exit 2), which self-corrects in the
same turn. It degrades silently when `ovweb` is not installed.

## CI workflows

| Workflow | Trigger | What it runs |
|---|---|---|
| [`validate-web.yaml`](../.github/workflows/validate-web.yaml) | every PR | `ovweb doctor --pins` → `ovweb redirects check` → `ovweb lint` (PRs also `--against` the base branch) → `mkdocs build --strict` → `ovweb lint --site` over that build |
| [`publish-web.yaml`](../.github/workflows/publish-web.yaml) | manual (`workflow_dispatch`) | the publish: `ovweb publish <command> <version>`, then `ovweb verify`. Inputs: `command` (`new`/`latest`/`past`), `version`, `dry_run` |
| [`check-external-links.yaml`](../.github/workflows/check-external-links.yaml) | weekly + manual | external URLs with lychee — never on PRs, since third-party outages must not block merges; reports through a single self-updating `broken-links` issue |
| [`test-tools.yaml`](../.github/workflows/test-tools.yaml) | changes under `publish-tool/` | `pytest` and `ruff` |

`publish-web.yaml` installs the tool **non-editable** — publishing a past version checks out that
version's branch, where the package does not exist, so it has to live in `site-packages`.
