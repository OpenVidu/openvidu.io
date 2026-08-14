---
description: Start the local MkDocs dev server with live reload (Docker)
---

Serve the website locally with live reload. Run from the repo root, in the background:

```bash
docker run --name=mkdocs --rm -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
```

- If the image is missing, build it first (takes a few minutes):
  `docker build --pull --no-cache --rm=true -t squidfunk/mkdocs-material .`
- If host port 8000 is taken, map another one (`-p 9100:8000`) — do not stop whatever holds it.
- Report the URL (http://localhost:8000 or the port used) and watch the startup log: the build
  must reach "Serving on" with **zero WARNINGs**. Anchor `INFO` lines are expected
  (pymdownx.tabbed false positives).

Known local-server behaviour, all expected — do not "fix" any of it:

- It serves a **single unversioned site at the root** (`/meet/`, not `/latest/meet/`); version
  handling happens at publish time. To preview the real versioned layout, see
  `contributing/local-testing.md` (`mike serve`).
- Canonicals and JSON-LD show `http://0.0.0.0:8000/...`.
- `--dirty` is on (fast, rebuilds only the edited page): after editing a shared snippet or an
  override, touch the including page (or restart) to see the change everywhere. For a
  full-fidelity serve, override the CMD to drop it:
  `docker run --name=mkdocs --rm -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material serve --dev-addr=0.0.0.0:8000 --livereload`

Stop it afterwards with `docker stop mkdocs`.
