# Authoring pages, snippets and assets

## Adding a new page

1. **Create the Markdown file**:
   Place a `.md` file in the appropriate folder under the [`docs`](../docs) directory.

2. **Add metadata**:
   Include the following frontmatter at the beginning of the file:

   ```yaml
   ---
   title: "Example" # ≤57 characters (70 for blog posts) — Material appends " - OpenVidu"
   description: "Some description." # 100–160 characters, ending in a full stop
   ---
   ```

   Both keys are **required on every page** — the build fails on any llmstxt-selected page
   missing either ([`publish-tool/mkdocs_hook.py`](../publish-tool/mkdocs_hook.py)), and the
   globs select nearly every page. Both must be **unique site-wide**, and both are double-quoted.
   `ovweb lint` enforces the length budgets and the uniqueness — see [checks.md](checks.md).

3. **Reference in `mkdocs.yml`**:
   Two changes must be made:

   - Add the new page to the `nav` section in [`mkdocs.yml`](../mkdocs.yml) (if you want to
     include it in the navigation) and set the title. A page intentionally left out of the nav
     must be listed in `not_in_nav`, or the build warns.

   - Check the mkdocs-llmstxt plugin's `sections` in mkdocs.yml. **Most new pages need no change
     at all**: most sections are a glob over a folder, so a page added inside one is picked up
     automatically. Only add a line if the page's folder is listed page by page (the top-level
     product pages, the Meet embedding guides and the self-hosting entry pages) or if it starts a
     new folder.

     When you do add one, add **the path only.**
     [`publish-tool/mkdocs_hook.py`](../publish-tool/mkdocs_hook.py) fills each entry in from the
     page's own frontmatter — the `title` as the link text and the `description` after it — so
     both are written once; a listed page missing either fails the build, and a page in no
     section at all is missing from `llms.txt` *and* linked as a dead `.md`.

     ```yaml
     plugins:
       - llmstxt:
           sections:
             OpenVidu Meet features:
             - meet/features/*.md          # the whole subtree, subfolders included
     ```

     The plugin matches with `fnmatch`, where **`*` crosses `/`** — so `meet/features/*.md`
     covers the whole subtree, but `docs/*.md` would swallow every page under `docs/` rather than
     just the top-level ones. A literal segment is what fences a glob in: `single-node/*/*.md`
     takes the 24 provider guides but not `single-node/index.md`.

4. **Update the site layout (if needed)**: if the new page starts a **new area**, add its folder
   to the `layout` section of [`publish-tool/ovweb.yaml`](../publish-tool/ovweb.yaml) — to
   `non_versioned_pages` if the page is not versioned, or to `versioned_pages` if it is part of a
   new set of versioned pages. Otherwise its links will not be rewritten and it will not be
   relocated correctly at publish time. A page inside an area that is already listed needs no
   change here.

If the new page contains links, follow the site-wide [link rules](link-rules.md).

## Adding a new shared snippet

1. **Create the Markdown file**:
   Place a `.md` file in the [`shared`](../shared) directory, in the folder matching the docs
   area (and, for self-hosting, the cloud provider) it belongs to — see
   [`shared/README.md`](../shared/README.md) for the folder conventions.

2. **Reference in a page**:
   Use the following syntax to include the snippet in other snippets or pages:

   ```markdown
   --8<-- "area/snippet.md"
   ```

> [!NOTE]
> The include path is relative to [`shared`](../shared) itself — `pymdownx.snippets` is
> configured with `base_path: [!relative $config_dir/shared]`, so the `shared/` prefix must be
> left out. Links **inside** a snippet are root-absolute (with one documented exception) — see
> [link rules](link-rules.md), rule 2.

> [!IMPORTANT]
> A snippet renders inside every page that includes it. **Grep for its `--8<--` usages before
> editing one** (e.g. `shared/meet-vs-platform-table.md` is on the landing page), and check the
> consequences on each host page.

## Organizing assets

Images live in [`docs/assets/images`](../docs/assets/images) and videos in
[`docs/assets/videos`](../docs/assets/videos), organized so an asset's folder tells you which
page uses it. **Never leave files directly at the `images/` or `videos/` root** — place every new
asset in the folder matching its page:

- **Versioned docs** mirror the docs tree under a product folder: an image for
  `docs/meet/meetings/live-captions.md` goes in `images/meet/meetings/live-captions/`, and one
  for `docs/docs/self-hosting/production-ready/performance.md` goes in
  `images/platform/self-hosting/production-ready/performance/` (`docs/docs/**` ↔
  `images/platform/**`).
- **Non-versioned root pages** get a top-level folder named after the page: `images/home/`
  (landing), `images/about-us/`, `images/pricing/`, `images/research/`,
  `images/openvidu-meet-vs-openvidu-platform/`... Blog post assets follow the blog convention:
  `images/blog/YYYY/MM/<slug>/`, mirroring the post's own location
  (`blog/posts/YYYY/MM/<slug>.md`). Drafts use literal `YYYY/MM` placeholder directories, moved
  together with the post at publish time.
- **Cross-cutting assets**: `images/logos/` is the brand-asset library (OpenVidu, Meet and
  Platform logo variants and third-party logos — files here may be kept even while unreferenced),
  `images/og/` holds social cards and `images/sponsors/` sponsor/funding logos.
- An asset used by several pages lives in the folder of the page it primarily belongs to, and
  other pages reference it there (e.g. the deployment architecture diagrams in
  `images/platform/self-hosting/deployment-types/` are also referenced from OpenVidu Meet's
  advanced deployment page).
- **Images reused across deployment types** (referenced from `shared/self-hosting/**` snippets or
  from several `elastic`/`ha`/`single-node` pages) go in `images/platform/self-hosting/shared/`,
  in a subfolder per cloud provider (`aws/`, `azure/`, `digitalocean/`, `gcp/`, `oracle/`)
  mirroring the [`shared/self-hosting`](../shared/self-hosting) snippet folders.

## Sync changes between _openvidu.io_ and _livekit-tutorials.openvidu.io_

Whenever any changes are made to the tutorials documentation, these changes must also be
reflected in repository [livekit-tutorials-docs](https://github.com/OpenVidu/livekit-tutorials-docs)
so they end up available in [livekit-tutorials.openvidu.io](https://livekit-tutorials.openvidu.io/).

To apply changes in the web _livekit-tutorials.openvidu.io_:

- In this repository, push the changes to tutorials documentation to the `main` branch and run
  the [Publish Web action](versioning.md#publishing-with-github-actions) with command `latest`.
- In repository [livekit-tutorials-docs](https://github.com/OpenVidu/livekit-tutorials-docs),
  push the changes to the `main` branch and run action
  [Publish Web](https://github.com/OpenVidu/livekit-tutorials-docs/actions/workflows/publish-web.yaml)
  selecting the `main` branch.
