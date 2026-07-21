---
name: blog-review
description: Review an OpenVidu blog draft (full post or a section) for readability, SEO, technical accuracy, CTA strength, structure, formatting, and repo-specific validity (frontmatter, categories, authors, the `<!-- more -->` tag, links, image assets). Returns a scorecard, findings by severity, and prioritized edits. Use when a draft exists and needs auditing before publish. Trigger phrases like "review this post", "is this blog ready to publish", "audit the draft", "check my article".
---

# OpenVidu Content Reviewer

Audit a written blog draft and return **actionable, evidence-based** improvements. Support two modes:

- **Full-post review** — evaluate the whole article end to end.
- **Section review** — evaluate only the requested section(s) plus continuity with surrounding context.

## Ground rules

- **DO NOT** rewrite the whole post unless explicitly asked.
- **DO NOT** invent technical facts, benchmark numbers, or product capabilities.
- **DO NOT** give vague feedback ("improve flow") without a concrete example and fix.
- Always account for target audience, primary keyword, and buying-journey stage. If not given, infer and **state the assumption**.

## Repo-specific validity checks (do these first — they block publish)

Verify against the actual repo conventions:

- **File, naming & assets** — post at `docs/blog/posts/YYYY-MM-DD-<slug>.md`, where `YYYY-MM-DD` equals the frontmatter `date` **and** `<slug>` equals the frontmatter `slug`. The asset folder `docs/assets/images/blog/YYYY-MM-DD-<slug>/` MUST have the **same name** as the post file. Any mismatch → High severity.
- **Frontmatter present and complete** — `draft`, `date`, `slug`, `description`, `categories`, `tags`, `authors`, and the `hide` block. `description` is **required** (feeds search snippets, `og:description` and JSON-LD) → its absence is High severity. `cover_image` is **recommended**: a raster image (png/jpg/webp, **not** svg) that actually exists inside this post's asset folder — flag a missing or broken value.
- **Registered in `llmstxt`** — the post has its own line in the `llmstxt` plugin `sections` in `mkdocs.yml` (`- blog/posts/YYYY-MM-DD-<slug>.md: <description>`). Posts are listed individually; a missing entry means no `llms.txt` entry → Medium severity.
- **Categories valid** — every category is in `categories_allowed` in `mkdocs.yml` (`Comparison`, `How-to`, `Research`, `Livekit`, `Technology`, `Vertical`, `Success story`, `Implementation`, `OpenVidu How-to`, `OpenVidu Meet`, `Openvidu Implementation`, `OpenVidu`, `OpenVidu comparison`, `OpenVidu Platform`, `Release`, `AI`). An unlisted category **breaks the build** → High severity.
- **Authors valid** — every author key exists in `docs/blog/.authors.yml`.
- **`<!-- more -->` present** — exactly one, right after the intro. `post_excerpt: required` means a missing tag **breaks the build** → High severity.
- **Poster image** — an image follows the H1; `#only-light`/`#only-dark` variants are paired if used.
- **Image assets** — every referenced image (`../../assets/images/blog/YYYY-MM-DD-<slug>/<file>`) actually exists in that post's asset folder under `docs/assets/images/blog/`; flag missing files.
- **Links** — internal links and image/asset references are **relative** (relative `.md` for pages, `../../assets/images/blog/...` for images); external links carry `{:target="_blank"}`. Flag root-absolute (`/meet/`) or bare pretty-URL internal links, and obviously broken relative paths. **Release posts** (`Release` category) are the exception: links to versioned docs must be **absolute, version-pinned URLs including the domain** (`https://openvidu.io/X.Y/docs/...`, `/X.Y/meet/...`) for the announced version — flag `latest` or relative links there.
- **Admonition syntax** — `!!! tip "..."` with 4-space-indented bodies.

## Editorial rubric

Score each 1–5 and justify briefly:

- **Readability** — active voice, conversational tone, paragraphs under 5 lines, short sentences, no fluff.
- **SEO** — primary keyword in title/intro/headings naturally; search-intent match; `description` present; title under 70 chars.
- **Technical Accuracy** — commands correct and copy-pasteable; no invented capabilities; placeholders explained.
- **CTA Strength** — one clear CTA matched to the buying-journey stage.
- **Structure** — logical H1 → H2/H3 hierarchy; strong hook; a closing "next steps" section.
- **Formatting** — bullets/numbered lists used well, key terms bolded, admonitions and code fences correct, scannable.

Score meaning: **1** not publishable · **2** major revision · **3** moderate revision · **4** minor revision · **5** publish-ready.

## Output format

Return exactly these sections:

1. **Review Context** — mode, audience, primary keyword, buying-journey stage, assumptions.
2. **Build/Validity Check** — pass/fail on each repo-specific item above; call out anything that would break the MkDocs build.
3. **Scorecard** — Readability, SEO, Technical Accuracy, CTA Strength, Structure, Formatting, each x/5, plus Overall x/5.
4. **Findings by Severity** — High / Medium / Low. Each finding: the issue (quote the offending text), why it matters, and a concrete recommended fix.
5. **SEO & CTA Audit** — search-intent match (Strong/Partial/Weak), title check, intro hook check, CTA stage alignment, suggested CTA improvement.
6. **Technical Audit** — correctness risks, command copy-pasteability, missing examples or visual aids, suggested screenshot/diagram placements.
7. **Prioritized Next Edits** — the top 3 edits that most improve publish readiness.
8. **Publish Readiness** — Not ready / Nearly ready / Ready, plus the minimum fixes required before publish.
