---
description: Move a draft blog post from the YYYY/MM placeholders to its real publish date
---

Publish the draft blog post whose slug is `$ARGUMENTS`. This is the mechanical draft→publish
transition defined in `.claude/skills/blog-write/references/conventions.md`.

1. Locate the draft at `docs/blog/posts/YYYY/MM/<slug>.md` (literal `YYYY/MM` directories). If
   it is not there, stop and tell the user — the post may already be published or the slug
   wrong.
2. Take today's date as the publish date (`<year>`, zero-padded `<month>`).
3. Set the frontmatter `date:` to the publish date.
4. In the post body, string-replace every `YYYY/MM/` with `<year>/<month>/` — this rewrites the
   asset references and nothing else, by design.
5. `git mv docs/blog/posts/YYYY/MM/<slug>.md docs/blog/posts/<year>/<month>/<slug>.md` and
   `git mv docs/assets/images/blog/YYYY/MM/<slug> docs/assets/images/blog/<year>/<month>/<slug>`
   (create the year/month directories if this is the first post of the month).
6. Verify nothing else remained in the placeholder folders; remove them if now empty.
7. Run `ovweb lint docs/blog/posts/<year>/<month>/<slug>.md` and fix any error it reports.
8. Remind the user: merging this to `main` does **not** put the post online — it goes live with
   the next Publish Web workflow run (`ovweb publish latest X.Y`).
