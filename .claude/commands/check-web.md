---
description: Validate the website sources the way CI will — convention lint plus the strict build
---

Validate the current state of the website sources. Argument: `$ARGUMENTS` (empty for the fast
check, `full` to add the strict build).

## Fast check (always)

Run from the repo root:

```bash
ovweb lint
```

(If `ovweb` is not installed: `pip install -e "./publish-tool[validate]"` first.)

It reports `[check] file:line: message — hint` lines at three severities. Act on them:

- **error** — CI fails on these. Fix every error in files this session touched; for errors in
  files you did not touch, fix them if the fix is unambiguous, otherwise list them for the user.
- **warn** — convention violations that do not block CI. Fix the ones caused by this session's
  edits; report pre-existing ones without fixing (they may be deliberate).
- **info** — janitorial; mention only if the user asked for a cleanup.

Never silence a finding by weakening the checker (`publish-tool/src/ovweb/lint/`) — the checker
changes only when a convention itself changes, with the user's agreement.

## Full check (`full` argument)

After the fast check passes, also run what CI runs:

```bash
CI=false GOOGLE_ANALYTICS_KEY=G-XXXXXXXX mkdocs build --strict --site-dir /tmp/mkdocs-strict-validation
```

- The build must end with **zero WARNINGs** — any WARNING is a failure to fix.
- Anchor `INFO` lines are expected noise (~110 `pymdownx.tabbed` false positives). Only scan
  them for a heading you renamed or removed in this session.
- If `mkdocs` is not installed locally, use the Docker image instead:
  `docker run --rm -v ${PWD}:/docs -e GOOGLE_ANALYTICS_KEY=G-XXXXXXXX squidfunk/mkdocs-material build --strict -d /tmp/site`.

If redirect rules or `publish-tool/ovweb.yaml` were touched this session, also run
`ovweb redirects check`.

## Report

End with a short summary: errors fixed, warnings fixed vs pre-existing, and whether the strict
build passed (when run).
