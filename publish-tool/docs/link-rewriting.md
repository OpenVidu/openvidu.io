# Link-rewriting reference

The final link conventions, for version `3.9`:

| Context                              | From (mike output) | To (final)                                     |
| ------------------------------------ | ------------------ | ---------------------------------------------- |
| Versioned page → asset (raw HTML)    | `src="/assets/…"`  | `src="/3.9/assets/…"` (version-pinned)         |
| Versioned page → asset (Markdown)    | `../../assets/…`   | _(left relative by mike; stays version-local)_ |
| Versioned page → non-versioned page  | `../../pricing/`   | `/pricing/`                                    |
| Versioned page → home                | `../..`            | `/`                                            |
| Canonical / `og:url` on versioned page | `…/3.9/docs/…`   | `…/latest/docs/…`                              |
| Non-versioned page → versioned page  | `../docs/`         | `/latest/docs/`                                |
| Canonical / `og:url` / JSON-LD on non-versioned page | `…/3.9/…` | `…/…` (version removed)                 |
| `404.html` → versioned page          | `/docs/`           | `/latest/docs/`                                |
| Versioned page → root file (RSS feed) | `../../feed_rss_created.xml` | `/feed_rss_created.xml`               |
| Version search index → versioned page | `docs/`           | `/3.9/docs/` (explicit version)                |
| Root search index → versioned page    | `docs/`           | `/latest/docs/`                                |
| Search index → non-versioned page    | `pricing/`         | `/pricing/`                                    |
| Root sitemap → versioned page        | `/3.9/docs/`       | `/latest/docs/`                                |
| Root sitemap → non-versioned page    | `/3.9/pricing/`    | `/pricing/`                                    |

And the same rules again for the Markdown exports, whose links are absolute rather than relative:

| Reference | mike writes | The publish makes it |
| --- | --- | --- |
| Versioned export → versioned page      | `…/3.9/docs/…`    | `…/3.9/docs/…` (kept, as above) |
| Versioned export → non-versioned page  | `…/3.9/pricing/`  | `…/pricing/`                    |
| Versioned export → home (`index.md`)   | `…/3.9/index.md`  | `…/index.md`                    |
| Promoted export → versioned page       | `…/3.9/docs/…`    | `…/latest/docs/…`               |
| Promoted export → non-versioned page   | `…/3.9/pricing/`  | `…/pricing/`                    |
| `llms.txt`                             | as promoted       | as promoted                     |
| Any export → a root-relative target    | `](/pricing/)`    | `](https://openvidu.io/pricing/)` |
| Any export → an export that does not exist | `](…/account/index.md)` | `](…/account/)`            |

## The Markdown exports and `llms.txt`

Every page listed in the `mkdocs-llmstxt` plugin's `sections` is published twice: as
`index.html`, and as an `index.md` beside it. `llms.txt` indexes those exports, and together they
are the site's AI-facing channel.

Neither half of an `llms.txt` entry comes from `mkdocs.yml`. The `on_page_content` half of
[`mkdocs_hook.py`](../mkdocs_hook.py) replaces both with the page's own frontmatter:

* the **description**, which the plugin would otherwise take from the value beside the path in
  `mkdocs.yml`. That is what lets a `sections` entry be a glob — the plugin's own behaviour is to
  give every page a glob matches the *same* description.
* the **link text**, which the plugin takes from `page.title`. MkDocs resolves that to the *nav
  label* when the nav entry has one, so most entries would render as `[Install]`, `[Overview]` or
  `[Releases]` — fine beside a parent in a sidebar, useless in a flat list.

A listed page missing either one fails the build.

They need their own rewrites for one reason: **the plugin makes every link absolute**, resolved
against the build's `site_url` — which mike makes versioned. So an export comes out of the build
with every internal link pinned to the version that produced it, and the HTML patterns cannot
reach any of them, because they match `href="…"` and Markdown has no `href`.

Which rule applies depends on where the export is served from, exactly as it does for HTML — and
so the version-vs-`latest` asymmetry is the same one the two search indexes have (see
[sitemaps-and-search.md](sitemaps-and-search.md)), for the same reason.

There is deliberately **no `llms-full.txt`**. The plugin can concatenate every export into one
file, and once `sections` covered every page that reached 2.8 MB — roughly 700k tokens, which
nothing can load, duplicating content the individual exports already serve. `llms.txt` as an index
plus on-demand page fetches is the spec's model and the one that works at this size.

Then two rules apply to *every* export, because they are about the form of a link rather than
its target — and both exist because the plugin is inconsistent in ways only the publish can settle:

- **Root-relative targets are made absolute.** The plugin absolutises a *relative* link but
  returns a root-relative one untouched, so which form an export handed out came down to how the
  author happened to write it. This cannot be fixed in the build: the plugin resolves against
  `site_url`, which mike makes versioned, so absolutising there yields `/3.8/pricing/` — a page
  served only from the root, and therefore a 404.
- **A link naming an export that does not exist is pointed at the page instead.** The plugin
  appends `index.md` to every directory link *without checking the target has an export*, and only
  pages in its `sections` list get one. Listing more pages shrinks the problem but cannot close
  it: `docs/reference-docs/` is vendored TypeDoc output with no Markdown source, and a JavaScript
  shell like `/account/` would export as a bare heading. The repair reads the real set of exports
  off the tree, so it needs no list to keep in step.

And one deliberate difference from the HTML:

- **A promoted export does not shield an author's pin to the version being published.** The HTML
  does (see [sitemaps-and-search.md](sitemaps-and-search.md)), but in Markdown a hand-written pin
  and the plugin's absolutised link are the same bytes, and the plugin wrote almost all of them. A
  pin to a *different* version — the form a deliberately archival link takes, as when release
  notes link back to the release before — is untouched either way.
