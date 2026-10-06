# The move from MkDocs Material to Zensical

The site is built with [Zensical](https://zensical.org) 0.0.68, the successor of Material for
MkDocs by the same author, since October 2026. This page records what the migration changed,
what Zensical cannot do yet and how the repository works around it, and the Zensical bugs met on
the way — so the next Zensical upgrade knows what to re-check, and so anyone wondering why
something is done the way it is can find the reason here.

Zensical is pre-1.0 (`0.0.x`) and moves fast: the blog, RSS, llmstxt, meta and redirects
plugins all arrived between September 2 and 30, 2026. Expect every item below to deserve a
second look at each upgrade.

## What changed, in one table

| Area | Before (MkDocs Material 9.7.7) | Now (Zensical 0.0.68) |
| --- | --- | --- |
| Config file | `mkdocs.yml` | `mkdocs.yml`, read by Zensical. Not `zensical.toml`: only the YAML form carries the `!ENV` tags the analytics key and the RSS git flag need (Zensical has no environment mechanism for TOML yet). |
| Build / serve | `mkdocs build --strict`, `mkdocs serve` | `zensical build --strict`, `zensical serve`. No `--site-dir`: the output is `site/` (gitignored). Always from the repository root. |
| Dev image | custom build over `squidfunk/mkdocs-material` | custom build over the official `zensical/zensical` (`Dockerfile`, `Dockerfile.mike`) plus `ovweb` |
| Versioning | `mike` 2.2.0 | the [Zensical fork of mike](https://github.com/squidfunk/mike), pinned to a commit; same commands, builds with `zensical build` |
| Theme | Material 9.7.7 | Zensical's `classic` variant (Material's look); templates rendered by MiniJinja |
| Hooks | three MkDocs hooks | none. Two Markdown extensions in `ovweb` (`publish-tool/src/ovweb/mdx/`) run inside the build; two publish steps do the rest |
| Link validation | MkDocs, anchors at `info` | Zensical, anchors off (`ovweb lint --site` checks them) |
| Blog post links | root-absolute `.md` | relative `.md` (see below) |
| Lightbox | mkdocs-glightbox plugin + hook | Zensical's glightbox (build-time anchors) + the vendored library, owned by `glightbox-gallery.js` |
| Search index | `search/search_index.json` | `search.json` at the site root |
| Image optimisation, asset self-hosting | `optimize`, `privacy` plugins at publish | none (see limitations) |

## Limitations, and what the repository does about each

### No hooks

Zensical has no `hooks:`. The three MkDocs hooks (`publish-tool/mkdocs_hook.py`,
`llmstxt_entries_hook.py`, `pygments_fence_title_hook.py`) are gone from `main`; their jobs now
live in two places:

- **Inside the build**, as Python-Markdown extensions, which Zensical still runs:
  `ovweb.mdx.root_links` resolves root-absolute `.md` links against `docs/` (the MkDocs
  `absolute_links: relative_to_docs` behaviour Zensical lacks), and `ovweb.mdx.fence_title`
  restores the linked code-block filename Pygments 2.20+ escapes. `mkdocs.yml` lists both, so
  the `ovweb` package must be importable wherever the site is built (`pip install
  ./publish-tool`; the Docker image installs it and puts the mounted checkout first on
  `PYTHONPATH`).
- **At publish**, in `ovweb postprocess`: the sitemap's `<lastmod>` per page from git
  (`date-sitemap`), and every `llms.txt` entry's title and description from the page's own
  frontmatter (`publish-llms-txt`). A validation build or `zensical serve` has neither — the
  sitemap has no dates and `llms.txt` carries the nav labels — which only the published site
  needs.

What the hooks did that is **not** reproduced: the generated blog views (archive, category and
pagination pages) used to get a title and description of their own; under Zensical they carry the
blog's title and the site description, and a paginated view shares its `<title>` with the view it
pages. A publish-time rewrite of those pages would restore it.

### Links

- **Root-absolute links in blog posts fail the strict build.** Zensical validates a post's links
  against the post's source file, where `/docs/x.md` resolves to nothing — 143 warnings before
  the migration, which `--strict` turns into a failure. The build itself rendered them correctly
  (through `ovweb.mdx.root_links`), so this is a validation gap, not a rendering one. Every post
  sits four folders deep (`blog/posts/YYYY/MM/`, the draft placeholders included), so the 263
  links became relative and the convention changed with them (`contributing/link-rules.md`,
  the blog conventions, `ovweb lint`'s `md-root-absolute-in-post`). Shared snippets keep the
  root-absolute form, which the extension resolves; Zensical does not validate those, but
  `ovweb lint --site` does, over the built HTML.
- **Anchor validation is off** (`invalid_link_anchors: false`). Zensical reports every link to a
  `pymdownx.tabbed` tab label as "anchor does not exist" (~110 of them), although the built
  HTML carries the ids — see the bugs below. `ovweb lint --site` is the anchor check.
- **Raw-HTML relative links are rewritten like Markdown links**: from the source file, with a
  `../` prefix on every page that is not an `index.md`. MkDocs left raw HTML alone, so the two
  links written relative to the *built* folder (`docs/meet/embedded/intro.md`) resolved one
  level too high, and the six in `docs/pricing.md` only worked by URL normalisation — and broke
  in the page's Markdown export. Both pages now follow the rule in `link-rules.md`: the URL form
  for a root-served page, the source-relative directory form inside a version.
- **Markdown exports carry the page's raw HTML**, links included (Zensical converts less of the
  page than mkdocs-llmstxt's `autoclean` did), so `ovweb` applies its HTML rewrite rules to the
  exports as well as the Markdown ones. Zensical also writes every export link as `](<url>)`,
  which the rewrites normalise first.

### Plugins with no counterpart

- **`privacy`** (planned by Zensical): nothing self-hosts the Google Fonts stylesheet and font
  files, the `img.shields.io` badges on the landing page or any other external asset at publish
  any more — they load from their origins, as they already did in the validation build. The
  fonts could be vendored by hand if that matters.
- **`optimize`** (in progress at Zensical): nothing recompresses images at publish. Compress a
  screenshot before committing it; `contributing/page-composition.md` has the `pngquant` recipe.
- **`glightbox`** exists natively but as a build-time wrapper only: its UI bundle then loads the
  GLightbox library **from unpkg.com at runtime** and builds an instance of its own, and the
  `background`/`shadow` options of the MkDocs plugin are ignored. The library (3.6.1, the copy
  mkdocs-glightbox 0.5.2 shipped) and its stylesheet are vendored under `docs/javascripts/` and
  `docs/stylesheets/` and loaded before the bundle, so nothing is fetched from a CDN; the global
  `GLightboxOptions` points the bundle's instance at a selector nothing matches, and
  `glightbox-gallery.js` owns the only instance as before. The plugin's injected styles moved
  into `extra.css`.
- **`llmstxt`** exists natively but has no `preprocess` hook, so the site's own export cleaning
  (`publish-tool/llmstxt_preprocess.py`) no longer runs. Zensical's cleaning is a port of
  mkdocs-llmstxt's `autoclean`, with the consequences that module existed to avoid: **every link
  whose label carries an icon is dropped whole — text included** (the site puts the external-link
  icon on every external link, so every one of them vanishes from the exports), **tab labels are
  dropped** (a tabbed block exports as a run of unlabelled code blocks), and the comparison-table
  icons export as nothing. Admonitions do export as blockquotes, as before. `autoclean: false`
  is worse: the exports then carry the inline SVG of every icon and the permalink anchors. The
  module and its tests are kept on `main` as the reference for the follow-up: regenerating every
  export from the built page HTML at publish time (BeautifulSoup + `llmstxt_preprocess.preprocess`
  + markdownify, the same pipeline mkdocs-llmstxt ran), which would also serve Zensical's own
  "Copy as Markdown" button, since it reads the same files.
- **`not_in_nav`** is ignored: Zensical does not check the nav for omitted pages. The list is
  kept as a comment above `nav` in `mkdocs.yml`.
- **`!relative`** is not a tag Zensical knows; the snippets' `base_path` is now `shared`,
  relative to the working directory, so the site is always built from the repository root.

### Templates: MiniJinja, not Jinja2

The overrides render with MiniJinja. Everything that was Python in them had to go:
`.startswith()` (now the `is startingwith` test), `.strftime()` (dates arrive as ISO strings;
sliced), list concatenation (`namespace` counters instead), `page.file.src_uri` (gone; `page.url`,
and `page.edit_url` holds the source path), `build_date_utc` (gone; the footer year is set by a
line of JavaScript, with the publish year as the no-JavaScript fallback), printing an undefined
value (an error — guard it). `config.plugins["material/search"]` is `config.plugins["search"]`.
The `| e` filter escapes `/` as `&#x2f;`, which is why the Open Graph image URL is printed
unescaped. `contributing/page-composition.md` has the list.

### Publishing

- **A past version cannot be re-published from this toolchain.** Every `X.Y` branch from before
  the migration (3.0–3.9) carries a MkDocs configuration — `hooks:`, `!relative`, the MkDocs
  plugins, Jinja2 overrides — that the Zensical fork of `mike` cannot build. `ovweb publish past
  X.Y` therefore fails at the build until that branch is migrated the way `main` was (the
  commits of this migration are the recipe), or it is published with the previous toolchain:
  the MkDocs Material image and `mike` 2.2.0 at the last MkDocs commit of `main`.
  `ovweb doctor` no longer compares the branches' hook copies, since nothing on `main` is loaded
  by path from another branch.
- **The release-notes splice** (`ovweb`'s `sync-releases`) matches markup. Zensical labels the
  table of contents `On this page` where Material wrote `Table of contents`; the splice
  recognises both, so the newest, Zensical-built notes can still be spliced into the older,
  Material-built version folders.
- **The mike fork is a git dependency.** pip cannot hash a git checkout, so the hash-locked
  `requirements-publish.txt` leaves it out (`uv pip compile … --no-emit-package mike`) and the
  publish workflow installs it separately, pinned to the commit `pyproject.toml` names.
  `ovweb doctor --pins` checks that pin across the places that name it.
- **Zensical pins neither `markdown`, `pymdown-extensions` nor `pygments`** (`>=` ranges), and a
  different version of any of them renders different markup, so `pyproject.toml` pins all three
  and `ovweb doctor --pins` checks them with `zensical` itself.
- **The Docker image runs as root**: a `site/` or `.cache/` it writes into the mounted checkout
  is root-owned. Remove them through the image.

### Behaviour differences worth knowing

- The version switch, the search, the cookie consent, the analytics with its feedback widget,
  the blog (posts, categories, archive, pagination, authors, `draft_if_future_date`), the RSS
  and JSON feeds with their `date_from_meta` keys, the `.meta.yml` metadata (lists are
  concatenated, as before), the content tabs, the custom icons and the `page_features` system
  all behave as they did; the output file set is identical but for `search.json` and the
  missing `sitemap.xml.gz` (which `ovweb` writes itself).
- The search index has a different shape (`items` instead of `docs`, with `level` and `path`)
  and ~10% fewer entries (no entry for a page's own `h1`); `ovweb` rewrites its locations the
  same way.
- Zensical renders the `generator` meta tag as `zensical-0.0.68` and the `Made with` footer
  line stays off (`extra.generator: false`).
- Builds are incremental and cached in `.cache/`; a full build takes ~15 s where MkDocs took
  ~55 s.

## Bugs found in Zensical 0.0.68

Reported against the behaviour observed on this site; each is worth re-checking at the next
upgrade.

1. **A `watch:` entry naming the theme's `custom_dir` makes `zensical build` write no pages and
   exit 0.** With `watch: [overrides]` (the value `custom_dir` has) the build reports
   "Build finished in 0.07s" and writes only the feeds and `rss.xsl`: no HTML, no search index,
   no sitemap. Any other entry (`shared`, a file) is fine. Zensical already watches the theme
   directories, so the entry is redundant and was removed. Zensical's issue #655 ("Site doesn't
   build when `custom_dir` is in `watch`") is closed, so this looks like a regression of it; #934
   fixed the same symptom for the config file itself in 0.0.62.
2. **Anchor validation does not see the ids `pymdownx.tabbed` generates.** Every link to a tab
   label (`[Shutdown the cluster](#shutdown-the-cluster)`) is reported as "anchor does not exist",
   although the built HTML holds `<input id="shutdown-the-cluster" …>` and the link works. The
   anchors seem to be collected from the headings rather than from the rendered ids. ~110 false
   positives on this site; anchor validation is off because of it.
3. **Blog posts are validated from their source, not from what the build renders.** A link a
   Markdown extension rewrites (here, a root-absolute path resolved against `docs/`) is still
   reported as "page does not exist" in a post, while the same link in a regular page or a
   snippet is accepted once the extension has resolved it. (Consistent with the blog plugin
   validating the post's Markdown before rendering it.)
4. **Raw-HTML relative links get the Markdown treatment**: a `../` prefix is added on non-index
   pages. Documented as the 0.0.66 fix for `srcset`, but it changes the meaning of every
   hand-written relative `href` in HTML compared with MkDocs, silently. Arguably a design
   decision; it broke two pages here.
5. **The `llmstxt` exports drop a link's text when its label contains an icon**, and the tab
   labels — the mkdocs-llmstxt `autoclean` behaviour, reproduced faithfully. Not a crash, but
   the exports lose information the page shows, with no option to keep it.
6. **The UI bundle loads GLightbox from unpkg.com at runtime** when the `glightbox` plugin is
   enabled and `GLightbox` is not already defined — an external request on every page with an
   image, with nothing in the configuration to vendor it (the `privacy` plugin that would have
   is not implemented yet).
7. **`| e` escapes `/` as `&#x2f;`**, so an escaped URL in an attribute (`content="https:&#x2f;&#x2f;…"`)
   is valid HTML but unreadable to the naive scrapers social previews rely on. Zensical's own
   templates never escape URLs, which is the workaround.
8. **The `search` plugin's index moved** from `search/search_index.json` to `search.json` and
   changed shape, undocumented; anything post-processing it (as `ovweb` does) has to follow.
9. **`llmstxt` writes `](<url>)` link targets** in `llms.txt` and in every export, where
   mkdocs-llmstxt wrote `](url)`. Valid Markdown, but a change for anything parsing the files.
10. **The blog plugin panics when a post fails to render.** With a Markdown extension that
    cannot be imported (the upstream `zensical/zensical` image, which lacks `ovweb`), every
    page's render raises; the build reports the `ModuleNotFoundError` once, but first the blog
    plugin panics on its own assertion (`blog.rs:785: ordered posts have selected pages`)
    instead of reporting the render error for the posts. A Rust panic in a worker thread, not
    a diagnostic.

## Checking the next upgrade

After bumping `zensical` in `pyproject.toml` (and the lock, both Dockerfiles — `ovweb doctor
--pins`): `zensical build --strict` from the repository root, `ovweb lint --site site`, then
re-read the list above. If an item is fixed upstream, remove the workaround and the entry; the
ones to look for first are anchor validation (turn `invalid_link_anchors` back on), the
`privacy` plugin (drop the vendored GLightbox and the font notes), hooks or a module API (move
the `ovweb.mdx` extensions and the two publish steps back into the build), and a `preprocess`
hook for the exports (`llmstxt_preprocess.py` is ready for it).
