# Keeping the releases pages always up to date

There are two releases pages — OpenVidu Meet (`meet/releases/`) and OpenVidu Platform
(`docs/releases/`) — and both are **versioned** pages. Left untouched, an old version's releases
page would only list the notes up to that version: a visitor browsing `3.5.0` would never see
the notes for `3.6.0`, `3.7.0`, … even though release notes are inherently global information.

Every version should serve the **full, most-recent** release notes, **without** dragging the
rest of the newest page along with them. Two complementary parts achieve that:

1. **Copy the content at publish time.** On every publish the **content** of the newest releases
   pages — the release notes body and the table of contents, nothing else — is spliced into the
   releases page of **every other version folder**, so each `/X.Y/…/releases/` lists the same
   complete changelog as `/latest/…/releases/`. Publishing the newest version pushes its notes
   outwards; re-publishing an older one pulls the current newest notes back in, so a rebuild
   does not regress it. See [`releases.py`](../src/ovweb/releases.py).

2. **Jump to the viewed version (front-end).** Because the notes are now identical across
   versions, a small client-side script scrolls the visitor to the section matching the version
   they are browsing — opening `/3.5/meet/releases/` jumps to the `## 3.5.0` section (anchor
   `#350`). It lives in
   [`docs/javascripts/releases-scroll-to-version.js`](../../docs/javascripts/releases-scroll-to-version.js)
   and is loaded only on the releases pages, via the `scrolltoversion` tag in their front matter
   (wired in [`overrides/main.html`](../../overrides/main.html)). It is a no-op when the
   URL already has an anchor (so cross-page `#380` links are respected) or when there is no
   matching section (the `latest` alias stays at the top, newest first).

Four consequences worth keeping in mind:

- **Only the content travels; the page stays version-local.** Header, tabs, navigation menu,
  footer, asset URLs and Material's runtime config are left exactly as the destination version
  built them, so a visitor who opens `/3.4/docs/releases/` keeps browsing the **3.4**
  documentation instead of being sent to `/latest/` by every link around the notes. Nothing in
  the spliced fragments needs rewriting: the release notes' own links are authored as absolute,
  version-pinned URLs, and the table of contents only holds `#anchor` links. Both are verified
  before splicing, so a page that breaks the convention is reported instead of published with
  links resolving against the wrong version folder.
- **The outdated-version banner shows up there like anywhere else.** The destination page is the
  destination version's own, so Material flags it as outdated and the banner from
  `{% block outdated %}` appears — which is what tells the visitor that the documentation
  *around* the notes is old, even though the notes themselves are complete.
- **The canonical tag belongs to whichever publish last rewrote it.** Post-processing only
  touches the version being published, so a version's canonical is rewritten to `/latest/…` when
  that version is (re)published, not when another one is. An older folder keeps whatever its last
  publish produced until it is rebuilt.
- **The Markdown export does not travel.** The releases pages have an `index.md` beside them like
  any other page in the plugin's `sections`, but only the content of the HTML is spliced. The
  export a reader actually reaches is `/latest/<vp>/releases/index.md` — the one `llms.txt`
  references, and the newest version's own, so it is built rather than copied. An
  old version folder's export keeps that version's notes; nothing links to it.
