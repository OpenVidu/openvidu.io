# Blog conventions — the single source for blog-plan, blog-write and blog-review

Facts every blog skill relies on. Skills point here instead of carrying copies, so a change to a
convention is edited once.

## Naming — file, assets and frontmatter must agree

- **Published post:** `docs/blog/posts/<year>/<month>/<slug>.md`. The `<year>/<month>` folders
  MUST match the frontmatter `date` (the publish date) and the filename MUST be exactly
  `<slug>.md`, equal to the frontmatter `slug`. The rendered URL (`/blog/YYYY/MM/DD/<slug>/`)
  comes from `date` + `slug`, never from the file path.
- **Asset folder:** `docs/assets/images/blog/<year>/<month>/<slug>/` — mirrors the post's own
  location. All of the post's images live there, referenced root-absolute:
  `/assets/images/blog/<year>/<month>/<slug>/<file>`. The `og:image`/JSON-LD partials resolve a
  bare `cover_image` filename against this mirrored path. A post's videos mirror the same
  `<year>/<month>/<slug>` path under `docs/assets/videos/blog/`.
- **Draft (not yet published):** identical layout, with the **literal placeholder `YYYY/MM`** as
  the year/month segments — backed by real directories named `YYYY/MM` — so draft branches build
  zero-warning. `date:` holds a **temporary real date** (the draft's creation day); a literal
  placeholder there aborts the build. There is no build guard against publishing a draft early:
  each draft lives on its own branch, merged to `main` only when ready.
- Old convention to reject: date-prefixed filenames. Also reject a draft mixing placeholder and
  real year/month paths.

## Publishing a draft (`/publish-post` runs this)

1. Set the frontmatter `date` to the actual publish date.
2. Replace the string `YYYY/MM/` with the real `<year>/<month>/` everywhere it appears in the
   post body's asset references — a pure string replacement by design.
3. `git mv` the post to `docs/blog/posts/<year>/<month>/<slug>.md` and the asset folder to
   `docs/assets/images/blog/<year>/<month>/<slug>/` — plus
   `docs/assets/videos/blog/<year>/<month>/<slug>/` when the post embeds a video.

Nothing else inside the post changes. Merging to `main` publishes nothing; the post goes live
with the next Publish Web workflow run.

## Frontmatter (all required unless noted)

```yaml
---
title: Your post title      # REQUIRED — the build fails without it; usually the same as the H1
draft: false
date: 2026-07-04            # publish date; a temporary real date while a draft
slug: your-post-slug
description: One-sentence SEO summary. REQUIRED. Phrase it to avoid a ": " (colon-space) so it stays valid as unquoted YAML.
cover_image: poster.jpg     # recommended; raster only (png/jpg/webp, NOT svg), inside this post's asset folder. Omit to fall back to the site-wide branded card.
categories:
    - OpenVidu Meet         # 1-2 values, MUST be in categories_allowed — read the list from mkdocs.yml (plugins.blog.categories_allowed); an unlisted value breaks the build
tags:
    - WebRTC                # free-form, 4-8 technical tags — taxonomy only, NEVER a page_features key
authors:
    - carlosRuiz            # keys must exist in docs/blog/.authors.yml
page_features:
    - lazyvideo             # only when the post embeds a video — see Media below. Omit otherwise
---
```

Do **not** add a `hide:` block: posts inherit the whole of `hide: [path, feedback, navigation,
search-bar, version-selector]` from `docs/blog/posts/.meta.yml`. Repeating any of it in a post
is dead frontmatter.

Tag rules:

- **Reuse an existing spelling before inventing one** — grep other posts first. Canonical
  spellings for the recurring ones: `WebRTC`, `Self-hosted`, `AI agents`, `LiveKit`.
- **New multi-word tags are sentence case** (`Voice agents`, not `Voice Agents`). Older posts
  still carry Title-Case tags; their normalization is a pending follow-up, not license to add
  more.
- **Don't repeat a category as a tag** (e.g. a post in the `Release` or `OpenVidu Meet`
  category doesn't also tag it) — the category page already collects those posts.

`<!-- more -->` on its own line right after the intro is **mandatory** (`post_excerpt:
required` — a missing tag breaks the build). Exactly one.

## Media — images and videos

Posts follow the site-wide rules in `contributing/page-composition.md` ("Images", "Videos", "The
lightbox") with no exceptions. The parts a post always touches:

### Images

Plain Markdown, **never** a hand-written `<a class="glightbox">` wrapper — the mkdocs-glightbox
plugin adds the lightbox anchor, and `auto_themed` assigns the dark/light gallery from the
`#only-*` suffix.

```markdown
![Alt text](/assets/images/blog/YYYY/MM/<slug>/screenshot.png){ .round-corners loading=lazy }
```

- **`.round-corners`** on every screen capture, photo, poster and GIF — the one rounding class.
  Logos, icons, transparent art and SVG diagrams stay square: a transparent image has no corner
  to round.
- **`loading=lazy`** on every image below the first viewport — in a post that is everything
  except the poster right after the H1.
- **`.skip-gallery`** on logos, product marks and inline icons: nothing to enlarge.
- Theme variants always come **in pairs**, `#only-light` / `#only-dark` on the path.

### Videos

One canonical pattern for a post: a lazy `<video>` wrapped in a **glightbox anchor**, so the
video joins the page gallery like every other page on the site. A bare `<video>` is a bug — it
renders but never opens. One `<a>` per line (there are strange behaviors when it is not), no
`width`, no inline `style`.

```html
<a class="glightbox" href="/assets/videos/blog/YYYY/MM/<slug>/demo.mp4" data-type="video"><video class="round-corners lazy-video" src="/assets/videos/blog/YYYY/MM/<slug>/demo.mp4" preload="none" muted playsinline loop></video></a>
```

- Video assets live in `docs/assets/videos/blog/<year>/<month>/<slug>/`, mirroring the image
  folder, and `/publish-post` rewrites their `YYYY/MM` like any other asset path.
- `lazy-video` **requires `page_features: [lazyvideo]`** in the frontmatter — `ovweb lint` fails
  the post without it.
- A themed pair carries the `#only-dark` / `#only-light` suffix in the `<video src>`, **never**
  in the `<a href>`, plus `data-gallery="dark"` / `data-gallery="light"`. A single video needs
  neither.
- No `autoplay` in a post (that pattern is for above-the-fold showcase heroes only), and
  `<video>` never takes `defer`, `async` or `loading` — those attributes do not exist for
  videos and silently do nothing.

## Link rules

- **Internal links → root-absolute including the `.md` extension**: `[x](/meet/index.md)`,
  `[x](/pricing.md)`. Validated and rewritten at build time
  (`validation.links.absolute_links: relative_to_docs`). Never relative (the post moves at
  publish) and never a bare pretty-URL in Markdown (`/meet/` — MkDocs can't validate it).
- **Excerpt exception (before `<!-- more -->`): no `.md` Markdown links.** The blog listing
  pages (`/blog/`, categories, archive) copy the excerpt **without rewriting resolved links**,
  so a `.md` target that renders fine on the post page leaks as a literal dead `/x.md` href on
  every listing. In the excerpt, write internal links as raw HTML with the URL form:
  `<a href="/meet/embedded/intro/">OpenVidu Meet</a>`. `ovweb lint` enforces this
  (`md-link-in-excerpt`).
- **Cross-post links** → `/blog/posts/YYYY/MM/<slug>.md` (the published location of the target).
- **Assets** → root-absolute, in Markdown and in raw-HTML `src`/`href` alike. `YYYY/MM` stays
  literal on drafts.
- **External links** → append `{:target="_blank"}`.
- **Release posts** (`Release` category) are the exception for versioned docs: absolute,
  version-pinned, domain-qualified URLs (`https://openvidu.io/X.Y/docs/...`) for the announced
  version — never `latest`, never root-absolute `.md`. A release note keeps pointing at that
  release's docs forever.

## Registration

**No `mkdocs.yml` change is needed for a new post.** The llmstxt `Blog:` section is the glob
`blog/posts/*/*/*.md`, matching published and draft paths alike; the entry's link text and
description come from the post's own `title` and `description` — the build fails if either is
missing. A post outside the conventional layout falls out of `llms.txt`; the fix is moving the
file, never editing the glob.
