---
description: Start the local Zensical dev server with live reload (Docker)
---

Serve the website locally with live reload. Run from the repo root, in the background:

```bash
docker run --name=zensical --rm -p 8000:8000 -v ${PWD}:/docs openvidu-io
```

- If the image is missing, build it first (takes a few minutes):
  `docker build --pull --no-cache --rm=true -t openvidu-io .`
- If host port 8000 is taken, map another one (`-p 9100:8000`) — do not stop whatever holds it.
- Report the URL (http://localhost:8000 or the port used) and watch the startup log: the build
  must finish with **no issues** — a warning is a failure to fix.

Known local-server behaviour, all expected — do not "fix" any of it:

- It serves a **single unversioned site at the root** (`/meet/`, not `/latest/meet/`); version
  handling happens at publish time. To preview the real versioned layout, see
  `contributing/local-testing.md` (`mike serve`).
- Canonicals and JSON-LD show the production URLs (`https://openvidu.io/...`): Zensical keeps
  `site_url` while serving.
- Builds are incremental and cached in `.cache/` (gitignored); after upgrading Zensical or on
  stale output, restart with `zensical build --clean` or delete `.cache/`.

Stop it afterwards with `docker stop zensical`.
