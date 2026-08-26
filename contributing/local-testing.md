# Local testing

## Dev server (Docker)

The dev image is a custom build of `squidfunk/mkdocs-material` with the repo's extra plugins
(tagged over the upstream name). Build it once, then serve with live reload:

```bash
docker build --pull --no-cache --rm=true -t squidfunk/mkdocs-material .
docker run --name=mkdocs --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
```

The default serve runs in `--dirty` mode: fast, but only the edited page is re-rendered, so
nav changes and snippet edits show stale on other pages until they are touched or the server
restarts. For a full-fidelity serve (every change rebuilds the whole site), override the CMD:

```bash
docker run --name=mkdocs --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material serve --dev-addr=0.0.0.0:8000 --livereload
```

Then open http://localhost:8000. Notes:

- Run from the repo root. When running non-interactively (scripts, agents), drop `-it`.
- If host port 8000 is taken, map another one, e.g. `-p 9100:8000` — do not stop whatever holds
  it.
- Watch the console: the build must be **zero `WARNING`s**. Broken links appear as warnings (and
  CI's `mkdocs build --strict` turns them into hard failures). `INFO` messages about anchors are
  expected — most are `pymdownx.tabbed` tab-anchor false positives (see
  [link rules](link-rules.md)); still scan them for a genuinely renamed/removed heading when you
  touch headings.
- The dev server serves a **single unversioned site at the root** (`/meet/`, not
  `/latest/meet/`) and overrides `site_url`, so canonicals and JSON-LD show
  `http://0.0.0.0:8000/...` locally. Both are expected; version handling happens at publish time.
- Live reload rebuilds the whole site on each save; pages built from `shared/` snippets pick up
  snippet edits on rebuild too.

## Building and validating like CI

```bash
docker run --rm -it -v ${PWD}:/docs -e GOOGLE_ANALYTICS_KEY=G-XXXXXXXX squidfunk/mkdocs-material build
```

`GOOGLE_ANALYTICS_KEY` is the web stream's **MEASUREMENT ID**; any placeholder works locally.

What CI actually runs on every PR is the strict build plus the convention lint — reproduce it
with `ovweb lint` and `CI=false GOOGLE_ANALYTICS_KEY=G-XXXXXXXX mkdocs build --strict` (needs
`pip install "./publish-tool[validate]"`), or the `/check-web full` command. The full check
reference is [checks.md](checks.md).

## Testing versioning locally

The dev server is unversioned; the versioned layout only exists on `gh-pages`. To preview it,
serve the content of the `gh-pages` branch:

```bash
mike serve
```

Build a version without pushing anything — `mike` commits to the local `gh-pages` only:

```bash
mike deploy 3.9
```

Or run a whole publish locally, post-processing included, and inspect the result:

```bash
ovweb publish latest 3.8 --no-push --keep-worktree
```
