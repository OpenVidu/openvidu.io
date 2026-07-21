---
name: blog-plan
description: Plan and outline an OpenVidu blog post. Use when turning a raw technical idea into a structured, SEO-optimized outline — title, article type, H1/H2/H3 structure with concrete talking points, and a buying-journey CTA — before any writing happens. Trigger phrases like "plan a blog post", "outline an article", "blog brief", "what should this post cover".
---

# OpenVidu Blog Planner

Convert a raw technical idea into a detailed, SEO-optimized blog post outline. You produce the **plan**, not the prose.

## Scope

- **DO** produce an SEO brief, an article type, one H1 title, an intro plan, a full H2/H3 outline with talking points, and one CTA.
- **DO NOT** write the full article. That is the `blog-write` skill's job.
- Hand off the finished outline to `blog-write`; the reviewer (`blog-review`) will audit the result.

## Gather inputs first

Extract these from the user's request. If any are missing, infer them and **state your assumption** rather than blocking:

- **Primary keyword** (the phrase the post should rank for)
- **Secondary keywords** (2–5 related phrases)
- **Search intent** (informational, comparison, how-to, decision)
- **Target audience** (almost always technical developers / DevOps / CTOs evaluating WebRTC)
- **Buying-journey stage**: Awareness, Consideration, or Decision

## Repo conventions this outline must respect

Posts live in `docs/blog/posts/` as `YYYY-MM-DD-<slug>.md`, with a matching asset folder `docs/assets/images/blog/YYYY-MM-DD-<slug>/` (**same name** as the post file). The outline should already choose:

- **A slug** (kebab-case, keyword-bearing, e.g. `secure-home-video-conferencing`) — it becomes both the filename slug and the asset-folder slug.
- **A `description`** — a one-sentence, keyword-bearing SEO summary. It is **required** on every post (search snippets, `og:description`, JSON-LD), so propose it here.
- **Categories** — MUST come from the allowed list in `mkdocs.yml` (`categories_allowed`): `Comparison`, `How-to`, `Research`, `Livekit`, `Technology`, `Vertical`, `Success story`, `Implementation`, `OpenVidu How-to`, `OpenVidu Meet`, `Openvidu Implementation`, `OpenVidu`, `OpenVidu comparison`, `OpenVidu Platform`, `Release`, `AI`. Pick 1–2.
- **Tags** — free-form, 4–8, technical (e.g. `WebRTC`, `self-hosted`, `Security`, `TURN`, `React`).

Read 1–2 existing posts in `docs/blog/posts/` to match tone and depth before finalizing.

## Title rules

- Keep it under **70 characters** and use the primary keyword naturally.
- Including a **number** (prefer odd) is a *recommendation*, not a requirement.
- Including the **current year (2026)** is a *recommendation*, not a requirement.
- A **question-style** title is allowed when it raises curiosity and fits intent.
- **Bracketed/parenthetical** supplemental context is allowed when useful.

Existing titles for calibration: *"5 React video call platforms in 2026: Is SaaS still the right choice?"*, *"Host Your Own Secure Video Calls at Home: A Private Server for Family and Friends"*, *"Connectivity Resilience and Security in WebRTC Deployments: Key Considerations on TURN"*.

## Article type rules

- Prefer one of: **List-based**, **How-to**, **Infographic**, **Checklist**, **Interview**.
- Other types are allowed when they fit intent better.
- Give a one-line reason why the type matches search intent.

## Structure rules

- One **H1**.
- An **intro plan**: hook angle, problem statement, promise of value. (The writer will place `<!-- more -->` right after the first paragraph — flag this so it isn't forgotten.)
- A logical sequence of **H2** sections, optionally with **H3** subsections, ordered fundamentals → advanced.
- Every H2 lists **3–5 concrete, non-generic talking points**. Same for each H3.
- End with a "next steps / go further" section that links to OpenVidu deployment or feature docs (this mirrors the house style — see how posts close with a "Need more than this?" section).

## CTA rule

- Define **one** specific CTA aligned to the buying-journey stage:
  - **Awareness** → learn more / read a related guide.
  - **Consideration** → try OpenVidu Meet, compare deployment types.
  - **Decision** → install, book a demo, deploy to production.
- Give explicit action text and say why it matches the stage.

## Output format

Return exactly these sections, in order:

1. **SEO Brief** — primary keyword, secondary keywords, search intent, target audience.
2. **Article Type** — selected type + why it fits.
3. **Title** — H1 (with char count), style used (standard/question/bracket), which optional recommendations were applied.
4. **Frontmatter proposal** — proposed `slug`, `description` (required, one sentence), `categories` (from the allowed list), `tags`, suggested `author` key.
5. **Intro Plan** — hook angle, problem statement, promise of value; note where `<!-- more -->` goes.
6. **Outline & Section Guide** — each H2 with its purpose + 3–5 talking points; H3s where useful; in logical order.
7. **CTA** — stage, goal, exact CTA text, why it matches.

## Quality bar

- Keep everything specific to a technical developer audience.
- Section flow should reduce friction from discovery to action.
- No generic filler talking points — each should tell the writer exactly what to cover.
