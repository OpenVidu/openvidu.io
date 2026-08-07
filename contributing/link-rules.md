# Link rules

There is **one convention for Markdown links** and a separate one for raw HTML. The goal is a
**zero-warning build**: every link is validated by MkDocs, and `mkdocs build --strict` (run in CI)
fails the build on any broken link.

## 1. Markdown links and images in regular pages → relative, including the `.md` extension

Write internal links and images as paths relative to the current file:

```markdown
[Local deployment](../../self-hosting/local.md)
[Anchor on another page](../rooms/access.md#predefined-roles)
[Pricing](../../pricing.md)          <!-- non-versioned page: also relative .md, NOT /pricing/ -->
![Diagram](../../assets/images/platform/self-hosting/diagram.png#only-dark)
```

Relative `.md`/asset links are validated by MkDocs, **navigable in the editor** (Ctrl+click /
preview works, which root-absolute forms break, since editors resolve `/` against the repo root
instead of `docs/`), and version-safe: the built URLs stay inside the version folder, and the
publish rewrites the built relative links that point to non-versioned pages into absolute URLs
(`/pricing/`) at publish time.

> [!NOTE]
> Non-versioned pages are linked **relatively too** (`../../pricing.md`). The old bare-URL form
> (`/pricing/`) was a pre-MkDocs-1.6 workaround: it isn't validated and used to produce a build
> warning — don't use it in Markdown anymore.

## 2. Markdown links and images in shared snippets and blog posts → root-absolute, resolved against `docs/`

A snippet is embedded in pages at different hierarchy levels, so relative paths would break.
Write them as an absolute path from the `docs/` root:

```markdown
[Deployment guide](/docs/self-hosting/deployment-types.md)
![Diagram](/assets/images/platform/self-hosting/diagram.png#only-dark)
```

MkDocs resolves and validates these against `docs/` thanks to
`validation.links.absolute_links: relative_to_docs` in `mkdocs.yml`, and rewrites them into
correct **relative** URLs at build time — so they end up identical to hand-written relative links
(validated, version-safe), just hierarchy-independent. The trade-off is that they are not
editor-navigable, which is why they are reserved for snippets and blog posts.

**Exception — deployment-type-parametric snippets.** A few `shared/self-hosting/**` snippets are
included in **parallel deployment-type trees** (e.g. the same snippet is used in both
`single-node/oracle/` and `single-node-pro/oracle/`) and link to a *sibling* page that must
differ per tree, such as `[Admin](../on-premises/admin.md)` or `[Admin](./admin.md)`. These are
intentionally **relative** so they resolve to the correct deployment type at each inclusion
point — keep them relative. Only links to *fixed* targets (anything under
`self-hosting/configuration/`, `self-hosting/how-to-guides/`, `ai/`, `tutorials/`, etc.) become
absolute.

**Blog posts use the same root-absolute form** because a post's source file and asset folder move
at publish time (the draft `YYYY/MM` placeholder folders become the real date folders) —
hierarchy-independent links are what let a post move without touching its content. **One
exception inside a post: the excerpt** (everything before `<!-- more -->`). The blog listing
pages copy the excerpt **without rewriting resolved Markdown links**, so in the excerpt internal
links must be raw HTML in URL form (`<a href="/meet/">…</a>`); `ovweb lint` enforces this
(`md-link-in-excerpt`). The full blog conventions — naming, draft lifecycle, frontmatter,
publishing — live in
[`.claude/skills/blog-write/references/conventions.md`](../.claude/skills/blog-write/references/conventions.md).

## 3. Raw HTML links and images (inside HTML blocks) → absolute URL form

MkDocs does **not** process links inside raw HTML (`<a href>`, `<img src>`), so they are neither
validated nor rewritten at build time. Relative paths would need a fragile per-page `../` depth
(relative to the **built** folder, not the source file) and are impossible to get right in shared
snippets — so use absolute URLs:

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

Links from HTML to **versioned** pages (rare) still use relative-to-built-folder paths: a page
`performance.md` builds to `performance/index.html`, so add one extra `../` compared to the
Markdown path (unless linking from an `index.md`).

## 4. Releases pages are the one exception

In `docs/meet/releases.md` and `docs/docs/releases.md`, every link inside a version's
release-notes section must be an **absolute, version-pinned** URL to that same version (e.g.
`/3.4/docs/...`). **Never hardcode a version anywhere else** (`Release` blog posts follow the
same pinned form — see the blog conventions). The full releases-pages contract is in
[versioning.md](versioning.md).

## Anchors and warnings

> [!IMPORTANT]
> **Anchors:** links to a `pymdownx.tabbed` tab label (`=== "Run OpenVidu locally"` →
> `#run-openvidu-locally`) work at runtime but MkDocs's anchor validator can't see tab-generated
> ids, so it logs a **false-positive `INFO` "no such anchor"**. This is expected. Anchor
> validation is therefore kept at `info` (not `warn`) in `mkdocs.yml`, so it never fails
> `--strict`. The authoritative anchor check with no false positives is `ovweb lint --site` over
> a built tree — see [checks.md](checks.md).

> [!NOTE]
> When serving/building the site locally there should be **no `WARNING` messages at all**. `INFO`
> messages about anchors are expected (see above). If you add a page that is intentionally not in
> the nav, add it to `not_in_nav` in `mkdocs.yml` so it doesn't warn.
