---
name: blog-write
description: Write an OpenVidu technical blog post in English from a structured outline — full post or a single section — following the repo's conversational style, MkDocs frontmatter, intro hook + `<!-- more -->` tag, scannable formatting, and copy-pasteable commands. Use after an outline exists (from blog-plan) and it's time to draft. Trigger phrases like "write the post", "draft this blog", "write section X", "turn this outline into a post".
---

# OpenVidu Content Writer

Write a high-quality technical blog post from a provided outline. Draft in the outline's order, in one of two modes:

- **Full-post mode** — produce the entire draft in one response.
- **Section mode** — produce only the requested section(s), preserving continuity with surrounding context.

If no outline exists yet, use the `blog-plan` skill first.

## Conventions (read first)

**Read [`references/conventions.md`](references/conventions.md) before drafting** — it is the
single source for the naming invariant (file ↔ asset folder ↔ frontmatter agreement, the
`YYYY/MM` draft mechanism), the full frontmatter template, the link rules (including the
excerpt exception), registration, and the publish procedure. The allowed `categories` are read
from `categories_allowed` in `mkdocs.yml`; author keys from `docs/blog/.authors.yml`.

**Also read one or two recent posts** in `docs/blog/posts/` to match voice, depth, and
formatting.

## Post body structure

1. **H1 title** (`# ...`) — matches the outline's title.
2. **Poster image** immediately after the H1, using **root-absolute** asset paths (`YYYY/MM` stays literal while the post is a draft). Use light/dark variants when available:
   ```markdown
   ![Descriptive alt text](/assets/images/blog/YYYY/MM/<slug>/poster-light.webp#only-light "title")
   ![Descriptive alt text](/assets/images/blog/YYYY/MM/<slug>/poster-dark.webp#only-dark "title")
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

**Links** (the build runs `mkdocs build --strict`, and `ovweb lint` checks the form — a bad
link fails CI): follow the link rules in
[`references/conventions.md`](references/conventions.md). The two most-missed ones: internal
links are root-absolute **with the `.md` extension**, and in the **excerpt** (before
`<!-- more -->`) internal links must instead be raw HTML in URL form
(`<a href="/meet/">…</a>`), because the blog listing pages copy the excerpt without rewriting
Markdown links.

**Technical content**
- Every command must be **copy-pasteable** and correct.
- Fenced code blocks with a language tag (```bash, ```yaml, ```javascript).
- Use placeholders like `<your-subdomain>` and explain them.
- Explicitly mark where **screenshots, diagrams, or graphics** should go, with alt text and a placement note, even if the image file doesn't exist yet.

**Length**
- Target **2000–2500 words** for a complete post. Track cumulative word count in full-post mode.

## Output

In **full-post mode**, write the complete `.md` file content (frontmatter + body) ready to drop into `docs/blog/posts/`. If the user wants it saved, write it as a draft to the literal path `docs/blog/posts/YYYY/MM/<slug>.md` (temporary creation date in `date:`), or to the real `docs/blog/posts/<year>/<month>/<slug>.md` when it publishes immediately.

In **section mode**, write only the requested section(s).

Then add a short **Final checks** note confirming:
- English only.
- Estimated word count (full post) or section length.
- Intro hook + `<!-- more -->` present (when the intro is included).
- Active/conversational voice held throughout.
- All commands copy-pasteable; all image placements annotated.
- Frontmatter has a `title` and a `description` (both required — the build fails without them); `cover_image` set when a raster poster exists in the asset folder.
- Naming agrees: filename is `<slug>.md` (= frontmatter `slug`); asset folder is `docs/assets/images/blog/YYYY/MM/<slug>/` mirroring the post location; published posts sit in `posts/<year>/<month>/` matching the frontmatter `date`, drafts sit in the literal `posts/YYYY/MM/` placeholder folders with a temporary creation date.
- Links follow the rules above (root-absolute internal/assets with the `.md`/file extension; `{:target="_blank"}` external; absolute version-pinned for release posts).
