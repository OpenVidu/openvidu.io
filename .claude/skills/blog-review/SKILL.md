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

The conventions themselves live in
[`../blog-write/references/conventions.md`](../blog-write/references/conventions.md) — read it,
then verify the draft against each and run **`ovweb lint <post path>`** (it mechanically checks
the link forms, the excerpt rule, and the asset mirroring; trust its errors). Severities:

- **File, naming & assets agree** (per the naming invariant) → any mismatch is High severity.
  Do NOT flag the `YYYY/MM` placeholder folders or the temporary date on a **draft** — that is
  the documented draft mechanism. DO flag: a published post whose `date` doesn't match its
  folders, a draft mixing placeholder and real year/month paths, a date-prefixed filename (old
  convention), or a literal `date: YYYY-MM-DD` string (aborts the build).
- **Frontmatter complete** (all keys of the template). `title` and `description` missing →
  High (build failure). `cover_image` recommended: raster (not svg) and actually present in the
  post's asset folder — flag a missing or broken value.
- **Covered by `llmstxt`** — a post at the conventional path needs **no `mkdocs.yml` change; do
  not ask for one**. A post outside that layout falls out of `llms.txt` → High; the fix is
  moving the file, never editing the glob.
- **Categories** in `categories_allowed` (read the list from `mkdocs.yml`) — unlisted breaks
  the build → High. **Authors** exist in `docs/blog/.authors.yml`.
- **`<!-- more -->`** — exactly one, right after the intro; missing breaks the build → High.
- **Poster image** follows the H1; `#only-light`/`#only-dark` paired if used. Every referenced
  image exists on disk.
- **Links** follow the conventions' link rules — including the **excerpt exception** (no `.md`
  Markdown links before `<!-- more -->`; raw-HTML URL form there) and the **Release-post
  exception** (version-pinned domain-qualified URLs, flag `latest` or `.md` links there).
- **Admonition syntax** — `!!! tip "..."` with a space and 4-space-indented bodies.

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
