# The two sitemaps, the version selector, and the two search indexes

## The two sitemaps, and the version selector

There are two, and only one of them is for search engines.

| Sitemap | Read by | Contains |
| --- | --- | --- |
| `sitemap.xml` | crawlers — `robots.txt` names it, and it is a plain `urlset`, not an index | every URL the site serves, versioned pages as `/latest/…`; never a redirect stub |
| `<X.Y>/sitemap.xml` | **the theme's version selector, at runtime** | that version's own pages **and its redirect stubs**, plus its version root; *not* the root-served pages |

The per-version copy is what makes "switch version and keep reading the same page" work. When a
reader picks another version, Material's `setupVersionSelector` fetches `sitemap.xml` under the
selected version, strips the current version prefix off the path they are on, and looks the
remainder up — an **exact-match lookup, nothing else**. Found → they land on that URL in the new
version, hash and query carried over. Not found, or the fetch failed → they are dropped on the
version root, which our generated redirect then sends to the docs index.

That exact-match lookup is why the stubs are listed (`sync-version-sitemap`, and `redirects
apply` for the versions not being republished): a moved page's old URL is a stub, so listing it
makes the selector land the reader on the stub, which forwards them in one invisible hop —
`location.replace`, hash and query preserved. Unlisted, every switch onto a moved page falls
back to the version root. This is also how the cross-version fallbacks work in both directions:
a reader on 3.7's `…/aws/upgrade/` picking 3.8 resolves through the merged-upgrade stub, and a
reader on 3.8's `/meet/…` picking 3.2 resolves through the section-fallback stub onto the Call
docs. Stub entries carry an `<!-- ovweb:stub -->` marker, which is what lets a later sync drop
the ones whose stub is gone, and no `<lastmod>` — a redirect has no modification date.

Three properties of that file are therefore load-bearing, and **all fail silently**:

- **The version-root entry must be present.** The selector takes the longest common prefix of
  every URL in the sitemap and requires that prefix to itself be an entry before it resolves
  anything. With only page entries left, the prefix is still `https://openvidu.io/<X.Y>/` but is
  no longer in the file, and every switch falls back to the version root.
- **The root-served pages must be pruned.** mike builds the whole site into the version folder, so
  the sitemap it writes lists `<X.Y>/pricing/` and friends — URLs that never resolve, because
  those pages are moved to the root. The selector is shown on root pages too, so a reader on
  `/pricing/` picking 3.6 would be sent to `/3.6/pricing/`, a 404. Pruned, they fall back to the
  version root, which is right: that page has no per-version counterpart.
- **The generated redirects must be listed** — see above.

Nothing in the built site *links* to this file — the only reference is that `fetch()` in the
theme's JavaScript, which no link checking or grepping finds. `ovweb verify` asserts all of these
conditions and [`tests/unit/test_rewrite_sitemap.py`](../tests/unit/test_rewrite_sitemap.py) pins
them.

## Where `<lastmod>` comes from

MkDocs initialises `Page.update_date` to the build date for every page and its sitemap template
emits exactly that, so the field would claim that every URL on the site changed on every publish —
no per-page signal, and false often enough to teach a crawler to ignore the field entirely.

The `on_env` half of [`mkdocs_hook.py`](../mkdocs_hook.py) sets `update_date` from git instead,
using [`sources.py`](../src/ovweb/sources.py): one `git log --name-only` pass gives the last
commit date of every file, and a page's date is the **newest across the page and the transitive
closure of the `--8<--` snippets it includes**. Most pages assemble their content from `shared/`,
so without the closure a rewritten shared install step would move no date at all on the pages
that display it.

`on_env` is the only hook that can do this: MkDocs renders the theme's static templates —
`sitemap.xml` among them — *before* it renders the pages, so `on_page_content` runs too late.
Nothing in the post-processing needs to know: `promote_root_sitemap` only rewrites URL substrings,
so the values flow into the root sitemap untouched.

Two deliberate behaviours:

- **A generated page carries no `<lastmod>` at all.** The blog's archive, category and pagination
  views have no source file, so inventing a date for them would be the same lie in miniature; the
  spec makes the field optional per URL. They do, however, get a **title and description** from the
  same hook, since having no frontmatter left them serving `site_description` and a paginated view
  sharing a byte-identical `<title>` with the view it pages. Both are derived from the view itself
  (its own heading, the number of posts it lists, its page number), so a month or category that
  does not exist yet is described correctly the first time it appears.
- **Anything that stops git answering falls back to the build date, at INFO level.** A shallow
  clone is the important one — `git log` still succeeds there but reports the fetched commit for
  every path, which is silently wrong rather than absent, so it is detected and skipped.
  `validate-web.yaml` checks out shallow; `publish-web.yaml` sets `fetch-depth: 0`. It must stay
  INFO because `mkdocs build --strict` fails on a warning.

## The two search indexes

There are two, and they say different things, because **a page loads the index that sits beside
it**: Material records the folder to resolve against in its runtime config (`"base": "../.."`),
which the publish deliberately leaves relative.

| Index | Loaded by | A hit on versioned docs points at |
| --- | --- | --- |
| `<X.Y>/search/search_index.json` | pages under `/X.Y/docs/`, `/X.Y/meet/` | `/X.Y/docs/…` — the same version |
| `search/search_index.json` | the pages served from the site root | `/latest/docs/…` |

The version's own index has to keep its version, or searching inside the 3.4 documentation would
return 3.8 pages. The root index is a *copy* of the newest version's, so it inherits that
version — and it must not keep it: it is served on the evergreen root pages, `/latest/…` is the
canonical URL of the page being linked, and a pinned URL goes stale at the next release. Every
other root-to-versioned reference (page links, the sitemap, `llms.txt`, the canonicals) already
uses `/latest/`.

Author-written, version-pinned links to versioned pages (`/3.4/docs/…`, used by the
release-notes links in blog posts) are **shielded** while the version is stripped from a promoted
page, and restored afterwards. Getting that wrong would silently send every historical release
note to the newest documentation, which is why it has its own tests.

The releases pages are not in this table: only their content is copied between version folders,
so every link on the page follows the rows above for the version it lives in, and nothing inside
the copied content is rewritten because those links are authored absolute and version-pinned.
