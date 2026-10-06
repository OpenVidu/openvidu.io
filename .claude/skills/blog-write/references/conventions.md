# Blog conventions — the single source for blog-plan, blog-write and blog-review

Facts every blog skill relies on. Skills point here instead of carrying copies, so a change to a
convention is edited once.

## Naming — file, assets and frontmatter must agree

- **Published post:** `docs/blog/posts/<year>/<month>/<slug>.md`. The `<year>/<month>` folders
  MUST match the frontmatter `date.created` (the publish date) and the filename MUST be exactly
  `<slug>.md`, equal to the frontmatter `slug`. The rendered URL (`/blog/YYYY/MM/DD/<slug>/`)
  comes from `date.created` + `slug`, never from the file path.
- **Asset folder:** `docs/assets/images/blog/<year>/<month>/<slug>/` — mirrors the post's own
  location. All of the post's images live there, referenced relative to the post:
  `../../../../assets/images/blog/<year>/<month>/<slug>/<file>` (four `../`: every post sits in
  `blog/posts/<year>/<month>/`). The `og:image`/JSON-LD partials resolve a bare `cover_image`
  filename against this mirrored path. A post's videos mirror the same
  `<year>/<month>/<slug>` path under `docs/assets/videos/blog/`.
- **Draft (not yet published):** identical layout, with the **literal placeholder `YYYY/MM`** as
  the year/month segments — backed by real directories named `YYYY/MM` — so draft branches build
  zero-warning. `date.created` holds a **temporary real date** (the draft's creation day); a
  literal placeholder there aborts the build. There is no build guard against publishing a draft
  early: each draft lives on its own branch, merged to `main` only when ready.
- Old convention to reject: date-prefixed filenames. Also reject a draft mixing placeholder and
  real year/month paths.

## Publishing a draft (`/publish-post` runs this)

1. Set the frontmatter `date.created` to the actual publish date.
2. Replace the string `YYYY/MM/` with the real `<year>/<month>/` everywhere it appears in the
   post body's asset references — a pure string replacement by design.
3. `git mv` the post to `docs/blog/posts/<year>/<month>/<slug>.md` and the asset folder to
   `docs/assets/images/blog/<year>/<month>/<slug>/` — plus
   `docs/assets/videos/blog/<year>/<month>/<slug>/` when the post embeds a video.

Nothing else inside the post changes. Merging to `main` publishes nothing; the post goes live
with the next Publish Web workflow run.

## Editing a published post

Every change to the body of a published post — a corrected fact, a new version in a command, an
added note or link — sets `date.updated` to the day it merges to `main`, adding the key if the
post has none. It renders as the post's "updated" date, becomes the JSON-LD `dateModified` and
dates the post in the updated RSS feed. A pull request that waits is re-dated when it merges.
Drafts and newly published posts carry no `updated`.

## Frontmatter (all required unless noted)

```yaml
---
title: Your post title      # REQUIRED — the build fails without it; usually the same as the H1
draft: false
date:
  created: 2026-07-04       # publish date; a temporary real date while a draft
  updated: 2026-10-06       # only once published: the day an edit merged (see "Editing a published post")
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

`date` is always a mapping: the RSS feeds read `date.created` and `date.updated` by key, and
`ovweb lint` fails a post whose `date` is a bare date (`blog-date`).

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

Plain Markdown, **never** a hand-written `<a class="glightbox">` wrapper — Zensical's glightbox
support adds the lightbox anchor at build time, and `auto_themed` assigns the dark/light gallery
from the `#only-*` suffix.

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

- **Internal links → relative to the post, including the `.md` extension**:
  `[x](../../../../meet/index.md)`, `[x](../../../../pricing.md)` — always four `../`, because
  every post sits in `blog/posts/<year>/<month>/`, the draft placeholders included, so the move
  at publish keeps the links valid. Validated and rewritten at build time. Never root-absolute
  (`/meet/index.md` — Zensical validates a post from its source, where that resolves to nothing
  and fails the strict build; `ovweb lint` reports it as `md-root-absolute-in-post`) and never a
  bare pretty-URL in Markdown (`/meet/` — the build can't validate it).
- **Excerpt exception (before `<!-- more -->`): no `.md` Markdown links.** The blog listing
  pages (`/blog/`, categories, archive) copy the excerpt, so in the excerpt write internal links
  as raw HTML with the URL form: `<a href="/meet/embedded/intro/">OpenVidu Meet</a>`.
  `ovweb lint` enforces this (`md-link-in-excerpt`).
- **A versioned target in the excerpt still uses the unversioned form** — `/docs/…`, `/meet/…`,
  never `/latest/docs/…`. That is the form that resolves locally and the only one `ovweb lint`
  can check; the publish repoints it at `/latest/` in the HTML and in the Markdown export
  (`point_root_absolute_links_at_latest`). A hand-written `/latest/` would survive the rewrite
  and break the dev server.
- **Cross-post links** → `../../YYYY/MM/<slug>.md` (the published location of the target,
  relative to this post's folder).
- **Assets** → relative in Markdown (`../../../../assets/images/blog/YYYY/MM/<slug>/x.png`),
  root-absolute in raw-HTML `src`/`href` (`/assets/videos/blog/YYYY/MM/<slug>/demo.mp4`).
  `YYYY/MM` stays literal on drafts.
- **External links** → append `{:target="_blank"}`.
- **Release posts** (`Release` category) are the exception for versioned docs: absolute,
  version-pinned, domain-qualified URLs (`https://openvidu.io/X.Y/docs/...`) for the announced
  version — never `latest`, never a `.md` path. A release note keeps pointing at that
  release's docs forever.

## Registration

**No `mkdocs.yml` change is needed for a new post.** The llmstxt `Blog:` section is the glob
`blog/posts/*/*/*.md`, matching published and draft paths alike; the entry's link text and
description come from the post's own `title` and `description` — the build fails if either is
missing. A post outside the conventional layout falls out of `llms.txt`; the fix is moving the
file, never editing the glob.
