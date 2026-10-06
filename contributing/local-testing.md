# Local testing

## Dev server (Docker)

The dev image is the official `zensical/zensical` image plus `ovweb`, whose Markdown extensions
the build loads. Build it once, then serve with live reload:

```bash
docker build --pull --no-cache --rm=true -t openvidu-io .
docker run --name=zensical --rm -it -p 8000:8000 -v ${PWD}:/docs openvidu-io
```

Then open http://localhost:8000. Notes:

- Run from the repo root. When running non-interactively (scripts, agents), drop `-it`.
- If host port 8000 is taken, map another one, e.g. `-p 9100:8000` — do not stop whatever holds
  it.
- Watch the console: the build must end with **"No issues found"**. Broken links appear as
  warnings (and CI's `zensical build --strict` turns them into hard failures).
- The dev server serves a **single unversioned site at the root** (`/meet/`, not
  `/latest/meet/`); version handling happens at publish time.
- Builds are incremental: Zensical caches in `.cache/` (gitignored) and rebuilds what changed,
  snippets included. After upgrading Zensical, or on stale output, run `zensical build --clean`
  or delete `.cache/`.
- The image installs `ovweb` but puts the mounted checkout first on `PYTHONPATH`, so an edit to
  [`publish-tool/src/ovweb/mdx/`](../publish-tool/src/ovweb/mdx) is live after a restart.

Without Docker, a virtualenv works too — `pip install -e "./publish-tool[validate]"` installs
Zensical, the pinned Markdown renderers and `ovweb`, and `zensical serve` from the repo root
serves the same site.

## Building and validating like CI

```bash
docker run --rm -it -v ${PWD}:/docs -e GOOGLE_ANALYTICS_KEY=G-XXXXXXXX openvidu-io build --strict
```

`GOOGLE_ANALYTICS_KEY` is the web stream's **MEASUREMENT ID**; any placeholder works locally. The
output goes to `site/` (gitignored): Zensical has no `--site-dir` option.

What CI actually runs on every PR is the strict build plus the convention lint — reproduce it
with `ovweb lint`, `CI=false GOOGLE_ANALYTICS_KEY=G-XXXXXXXX zensical build --strict` and
`ovweb lint --site site` (needs `pip install -e "./publish-tool[validate]"`), or the
`/check-web full` command. The full check reference is [checks.md](checks.md).

## Testing versioning locally

The dev server is unversioned; the versioned layout only exists on `gh-pages`. To preview it,
serve the content of the `gh-pages` branch with the Zensical fork of `mike` (installed by
`pip install "./publish-tool[build]"`, or in the image built from `Dockerfile.mike`):

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

To exercise only the post-processing on a build, without git: build as `mike` would
(`MIKE_DOCS_VERSION=3.9 zensical build`), copy `site/` to `<tree>/3.9/`, add a `versions.json`
(`[{"version": "3.9", "aliases": ["latest"]}]`), and run `ovweb postprocess 3.9 --tree <tree>`
followed by `ovweb verify --tree <tree>`.
