---
name: blog-write
description: Write an OpenVidu technical blog post in English from a structured outline — full post or a single section — following the repo's conversational style, MkDocs frontmatter, intro hook + `<!-- more -->` tag, scannable formatting, and copy-pasteable commands. Use after an outline exists (from blog-plan) and it's time to draft. Trigger phrases like "write the post", "draft this blog", "write section X", "turn this outline into a post".
---

# OpenVidu Content Writer

Write a high-quality technical blog post from a provided outline. Draft in the outline's order, in one of two modes:

- **Full-post mode** — produce the entire draft in one response.
- **Section mode** — produce only the requested section(s), preserving continuity with surrounding context.

If no outline exists yet, use the `blog-plan` skill first.

## File, assets, and registration

**Naming — the filename, the asset folder, and the frontmatter `date`/`slug` must all agree:**

- **Post file:** `docs/blog/posts/YYYY-MM-DD-<slug>.md`. `YYYY-MM-DD` MUST equal the frontmatter `date` (the intended publish date) and `<slug>` MUST equal the frontmatter `slug`.
- **Asset folder:** `docs/assets/images/blog/YYYY-MM-DD-<slug>/` — its name MUST be **identical to the post's filename basename**. All of the post's images live here and are referenced with **relative** paths: `../../assets/images/blog/YYYY-MM-DD-<slug>/<file>`.

**Register the post in `mkdocs.yml`:** add one line for it to the `llmstxt` plugin's `sections`, under the `OpenVidu:` group, alongside the other `blog/posts/...` entries:

```yaml
- blog/posts/YYYY-MM-DD-<slug>.md: <one-line description of the post>
```

Every post is listed **individually** there (not via a glob), so a new post that isn't added won't get its own entry in `llms.txt`.

**Before drafting, read one or two recent posts** in `docs/blog/posts/` to match voice, depth, and formatting.

## Frontmatter (required, at the top of the file)

```yaml
---
draft: false
date: 2026-07-04
slug: your-post-slug
description: One-sentence SEO summary. REQUIRED on every post — feeds search snippets, og:description and JSON-LD. Phrase it to avoid a ": " (colon-space) so it stays valid as unquoted YAML.
cover_image: poster.jpg   # recommended; the social/link-preview image (og:image + JSON-LD). A raster file (png/jpg/webp — NOT svg) inside this post's image folder. Omit to fall back to the site-wide branded card.
categories:
    - OpenVidu Meet        # MUST be from categories_allowed in mkdocs.yml
tags:
    - WebRTC               # free-form, 4–8 technical tags
    - Security
authors:
    - carlosRuiz           # a key that exists in docs/blog/.authors.yml
hide:
    - navigation
    - search-bar
    - version-selector
---
```

- **`categories`** must come from `categories_allowed` in `mkdocs.yml`: `Comparison`, `How-to`, `Research`, `Livekit`, `Technology`, `Vertical`, `Success story`, `Implementation`, `OpenVidu How-to`, `OpenVidu Meet`, `Openvidu Implementation`, `OpenVidu`, `OpenVidu comparison`, `OpenVidu Platform`, `Release`, `AI`. An unlisted category breaks the build.
- **`authors`** keys must exist in `docs/blog/.authors.yml` (e.g. `pabloFuente`, `csantosm`, `carlosRuiz`, `juanCarlos`, `sergio`, `mica`, `patxi`).

## Post body structure

1. **H1 title** (`# ...`) — matches the outline's title.
2. **Poster image** immediately after the H1, using **relative** asset paths. Use light/dark variants when available:
   ```markdown
   ![Descriptive alt text](../../assets/images/blog/YYYY-MM-DD-<slug>/poster-light.webp#only-light "title")
   ![Descriptive alt text](../../assets/images/blog/YYYY-MM-DD-<slug>/poster-dark.webp#only-dark "title")
   ```
   A single image can use `{ align=right width=60% }` sizing attributes. Point `cover_image` at this poster too (a raster `-light` variant).
3. **Intro** — first paragraph opens with a **hook** (a question or a clear benefit). It may run a little longer than body paragraphs.
4. **`<!-- more -->`** on its own line immediately after the intro. This is **mandatory** — the blog plugin sets `post_excerpt: required`, so a missing tag breaks the build.
5. **H2/H3 sections** following the outline, fundamentals → advanced.
6. A closing "**What to do next / Need more than this?**" section linking to relevant OpenVidu docs and deployment types.

## Style rules

**Voice**
- Active voice, conversational and direct. English only.
- Address the reader naturally when it helps ("I know what you're thinking", "Imagine this", "you probably don't need convincing 😉").
- No passive/academic/corporate-vague tone. No fluff or filler transitions.

**Paragraphs**
- Under **5 lines** each; aim for 2–4 sentences. Short, clear sentences.
- Don't overuse single-sentence paragraphs.

**Formatting for scannability**
- **Bold** the key concept in a bullet (`- **Privacy and ownership.** ...`).
- Bullet lists for parallel points; numbered lists for sequences/procedures.
- Use MkDocs Material admonitions the way existing posts do:
  ```markdown
  !!! tip "Short title"
      Body text, indented 4 spaces.
  ```
  Common ones here: `!!! tip`, `!!! abstract "What you'll build"`, `!!! note`.

**Links** (the build runs `mkdocs build --strict` — a bad link fails CI)
- **Internal links → relative, including the `.md` extension**, e.g. `[OpenVidu Meet](../../meet/index.md)`, `[Pricing](../../pricing.md)`. Never root-absolute (`/meet/`) or a bare pretty-URL — MkDocs validates only the relative form, and the deploy script rewrites it to `/latest/...` at publish.
- **Images/assets → relative too**, e.g. `../../assets/images/blog/YYYY-MM-DD-<slug>/<file>`. Never root-absolute.
- **External links → append `{:target="_blank"}`**, e.g. `[DuckDNS](https://www.duckdns.org){:target="_blank"}`.
- **Release posts are the exception** (`Release` category — an `X.Y.Z` announcement): links to versioned docs must be **absolute, version-pinned URLs including the domain** — `https://openvidu.io/X.Y/docs/...` and `https://openvidu.io/X.Y/meet/...`, pinned to the version being announced (**not** `latest`). A release note should keep pointing at that release's docs forever.

**Technical content**
- Every command must be **copy-pasteable** and correct.
- Fenced code blocks with a language tag (```bash, ```yaml, ```javascript).
- Use placeholders like `<your-subdomain>` and explain them.
- Explicitly mark where **screenshots, diagrams, or graphics** should go, with alt text and a placement note, even if the image file doesn't exist yet.

**Length**
- Target **2000–2500 words** for a complete post. Track cumulative word count in full-post mode.

## Output

In **full-post mode**, write the complete `.md` file content (frontmatter + body) ready to drop into `docs/blog/posts/`. If the user wants it saved, write it to the correct `docs/blog/posts/YYYY-MM-DD-<slug>.md` path.

In **section mode**, write only the requested section(s).

Then add a short **Final checks** note confirming:
- English only.
- Estimated word count (full post) or section length.
- Intro hook + `<!-- more -->` present (when the intro is included).
- Active/conversational voice held throughout.
- All commands copy-pasteable; all image placements annotated.
- Frontmatter has a `description` (required); `cover_image` set when a raster poster exists in the asset folder.
- Filename, asset-folder name, and frontmatter `date`/`slug` all agree (`YYYY-MM-DD-<slug>`).
- Post added to the `llmstxt` `sections` in `mkdocs.yml`.
- Links follow the rules above (relative internal/assets; `{:target="_blank"}` external; absolute version-pinned for release posts).
