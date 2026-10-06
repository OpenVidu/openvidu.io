# Link rules

There is **one convention for Markdown links** (with one exception for shared snippets) and a
separate one for raw HTML. The goal is a **clean strict build**: every Markdown link is validated
by Zensical, and `zensical build --strict` (run in CI) fails the build on any broken link.

## 1. Markdown links and images in regular pages and blog posts → relative, including the `.md` extension

Write internal links and images as paths relative to the current file:

```markdown
[Local deployment](../../self-hosting/local.md)
[Anchor on another page](../rooms/access.md#predefined-roles)
[Pricing](../../pricing.md)          <!-- non-versioned page: also relative .md, NOT /pricing/ -->
![Diagram](../../assets/images/platform/self-hosting/diagram.png#only-dark)
```

Relative `.md`/asset links are validated by Zensical, **navigable in the editor** (Ctrl+click /
preview works, which root-absolute forms break, since editors resolve `/` against the repo root
instead of `docs/`), and version-safe: the built URLs stay inside the version folder, and the
publish rewrites the built relative links that point to non-versioned pages into absolute URLs
(`/pricing/`) at publish time.

> [!NOTE]
> Non-versioned pages are linked **relatively too** (`../../pricing.md`). The bare-URL form
> (`/pricing/`) isn't validated — don't use it in Markdown.

**Blog posts link relatively too**, from their own folder: `../../../../docs/self-hosting/local.md`,
`../../../../assets/images/blog/YYYY/MM/<slug>/cover.png`. Every post sits four folders deep
(`blog/posts/YYYY/MM/`), the draft placeholders included, so the move at publish keeps every
relative link valid. Zensical validates a post's links from its source file, where a root-absolute
path resolves to nothing and fails the strict build — `ovweb lint` reports one as an error
(`md-root-absolute-in-post`).

## 2. Markdown links and images in shared snippets → root-absolute, resolved against `docs/`

A snippet is embedded in pages at different hierarchy levels, so relative paths would break.
Write them as an absolute path from the `docs/` root:

```markdown
[Deployment guide](/docs/self-hosting/deployment-types.md)
![Diagram](/assets/images/platform/self-hosting/diagram.png#only-dark)
```

Zensical leaves a root-absolute path untouched, so
[`ovweb.mdx.root_links`](../publish-tool/src/ovweb/mdx/root_links.py), a Markdown extension the
build loads, rewrites them into the equivalent **relative** link for each including page before
Zensical resolves, validates and rewrites it — so they end up identical to hand-written relative
links (validated, version-safe), just hierarchy-independent. (MkDocs 1.6 did the same with
`validation.links.absolute_links: relative_to_docs`.) The trade-off is that they are not
editor-navigable, which is why they are reserved for snippets.

**Exception — deployment-type-parametric snippets.** A few `shared/self-hosting/**` snippets are
included in **parallel deployment-type trees** (e.g. the same snippet is used in both
`single-node/oracle/` and `elastic/oracle/`) and link to a *sibling* page that must
differ per tree, such as `[Admin](../on-premises/admin.md)` or `[Admin](./admin.md)`. These are
intentionally **relative** so they resolve to the correct deployment type at each inclusion
point — keep them relative. Only links to *fixed* targets (anything under
`self-hosting/configuration/`, `self-hosting/how-to-guides/`, `ai/`, `tutorials/`, etc.) become
absolute.

**One exception inside a blog post: the excerpt** (everything before `<!-- more -->`). The blog
listing pages copy the excerpt, so in the excerpt internal links must be raw HTML in URL form
(`<a href="/meet/">…</a>`); `ovweb lint` enforces this (`md-link-in-excerpt`). The full blog
conventions — naming, draft lifecycle, frontmatter, publishing — live in
[`.claude/skills/blog-write/references/conventions.md`](../.claude/skills/blog-write/references/conventions.md).

## 3. Raw HTML links and images (inside HTML blocks) → absolute URL form

Zensical does **not** validate links inside raw HTML (`<a href>`, `<img src>`), and it rewrites a
*relative* one exactly like a Markdown link — from the source file, with a `../` prefix on every
page that is not an `index.md` — so a relative path in HTML is easy to get wrong and impossible
to get right in a shared snippet. Use absolute URLs:

```html
<a href="/pricing/">Pricing</a>                      <!-- non-versioned page: trailing-slash URL -->
<img src="/assets/images/home/feature.svg#only-dark" />
<a class="glightbox" href="/assets/images/foo.png">...</a>
```

**Assets referenced this way stay version-correct thanks to the publishing tool**: `ovweb`
rewrites `src|href="/assets/`, `/javascripts/`, `/stylesheets/` into `"/X.Y/assets/`... in every
**versioned** page at publish time, so each version keeps referencing its own assets even after
later versions change them. Non-versioned pages keep the root form (root assets are always the
latest publish's — correct for them). Locally the dev server serves assets at the root, so
`/assets/...` just works. `ovweb lint` resolves every raw-HTML target against the source tree —
see [checks.md](checks.md).

Links from HTML to **versioned** pages depend on where the linking page is served from:

- **From another versioned page**, write the path **relative to the source file, in directory
  form**: from `meet/embedded/intro.md`, the sibling page is `href="step-by-step-guide/"` and the
  folder below it `href="tutorials/"`; Zensical adds the `../` a non-index page needs. This works
  only **within one version**, where source and target share the version folder.
- **From a page served from the root** (`non_versioned_pages` — the landing, pricing, the
  comparisons, and every blog page including a post's excerpt), use the root-absolute form
  `/docs/…`, `/meet/…`. No relative path is right for a blog excerpt, which is copied verbatim
  into the post page, the listings and the archive, each at its own depth; and `/docs/…` is the
  only form that resolves on the dev server, where nothing is versioned. **`ovweb` repoints these
  at `/latest/` at publish time** (`point_root_absolute_links_at_latest`), in the HTML and in the
  Markdown export alike, so never write `/latest/` by hand: it resolves neither locally nor in
  `ovweb lint`, which checks raw-HTML targets against the source tree.

> [!NOTE]
> The unversioned URL is not broken without that rewrite — the `unversioned-mirror` rule in
> `ovweb.yaml` answers every `/docs/…` and `/meet/…` with a redirect stub to `/latest/…`. The
> rewrite is what keeps our own pages from taking that hop, and hands the link's ranking signal
> straight to the target. The stub stays for URLs typed or shared from outside.

> [!WARNING]
> **A link to `/latest/…` must be absolute — never relative, never `{{ base_url }}`-based.**
> `latest` is a sibling of the version folders, not a page inside one, so no relative path from a
> versioned page reaches it: MkDocs computes the depth without knowing the version segment mike
> adds later, and nothing rewrites it at publish time (`_absolutise_non_versioned_links` only
> covers `non_versioned_pages`). `{{ base_url }}/latest/meet/` renders as
> `../../latest/meet/`, which on `/3.8/docs/x/` resolves to the 404 `/3.8/latest/meet/`. The
> theme footer's two product links are the site-wide instance of this.

## 4. Releases pages are the one exception

In `docs/meet/releases.md` and `docs/docs/releases.md`, every link inside a version's
release-notes section must be an **absolute, version-pinned** URL to that same version (e.g.
`/3.4/docs/...`). **Never hardcode a version anywhere else** (`Release` blog posts follow the
same pinned form — see the blog conventions). The full releases-pages contract is in
[versioning.md](versioning.md).

## External links and new tabs

- **New tab**: the one canonical spelling is `{:target="_blank"}` (`ovweb lint` warns on
  variants). Never add `rel="noopener"` — modern browsers imply it for `target="_blank"`, and
  the privacy plugin adds it to published pages anyway.
- **Every external link opens in a new tab**, and **every link that opens a new tab carries the
  external-link icon** (`:fontawesome-solid-external-link:{.external-link-icon}`, appended inside
  the label). That includes internal links given `target="_blank"` so the reader keeps their
  place: on this site the icon means "this opens elsewhere", not "this is a third party".
  `ovweb lint` enforces both — a same-tab external link is an error, a missing icon a warning.
- **Exempt from the icon**, because it would be noise or impossible: a label that is already an
  image or a single icon shortcode (`:simple-github:`, the `:octicons-link-24:` cells in the
  releases tables), an `md-button` CTA (a button is its own affordance), and `mailto:` (no tab
  opens). Same for the source links in a code block's `title=` caption: the shortcode is not
  processed inside a fence attribute, and a filename chip is already its own affordance.
- **Illustrative URLs are code, not links**: `openvidu.example.io`, the
  `xxx-yyy-zzz-www.openvidu-local.dev` placeholder host — nothing resolves, so write
  `` `https://openvidu.example.io/dashboard` ``. A `localhost:PORT` URL that really answers while
  the tutorial runs stays a link, in a new tab, without the icon: it is the reader's own machine,
  not another site.
- **Watch the underscore in `_blank`.** If the same source line later contains `_..._` emphasis,
  the two underscores pair, the attr block is swallowed, and the link silently loses its
  `target` while `{:target="` shows up as text on the page. Use `*emphasis*` on such a line.
  `ovweb lint --site` catches the leak (`attr-block-leak`).
- Inside a blog excerpt the link must stay raw HTML (see rule 3), but the icon shortcode still
  renders inside inline raw HTML, so it goes in the anchor's text as usual.

## Anchors and warnings

> [!IMPORTANT]
> **Anchors:** links to a `pymdownx.tabbed` tab label (`=== "Run OpenVidu locally"` →
> `#run-openvidu-locally`) work at runtime, but Zensical's anchor validator can't see
> tab-generated ids and would report every one of them (~110 false positives). Anchor validation
> is therefore **off** in `mkdocs.yml` (`invalid_link_anchors: false`). The authoritative anchor
> check with no false positives is `ovweb lint --site` over a built tree — see
> [checks.md](checks.md).

> [!NOTE]
> When serving/building the site locally the build must end with **"No issues found"**: any
> warning fails `zensical build --strict`. Zensical does not check the nav for omitted pages, so a
> page meant to be reached by direct link only needs no registration — the list of such pages is
> kept as a comment above `nav` in `mkdocs.yml`.
