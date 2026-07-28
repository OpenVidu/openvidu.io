

# openvidu-docs

- [Development](#development)
- [Docs writing guidelines](#docs-writing-guidelines)
  - [Branches](#branches)
  - [Adding a new page](#adding-a-new-page)
  - [Adding a new shared snippet](#adding-a-new-shared-snippet)
  - [Mkdocs Material tag system](#mkdocs-material-tag-system)
    - [Theme-dependent images/videos](#theme-dependent-imagesvideos)
- [Versioning](#versioning)
- [Versioning with GitHub Actions](#versioning-with-github-actions)
  - [Publishing a new version](#publishing-a-new-version)
  - [Overwriting the latest version](#overwriting-the-latest-version)
  - [Overwriting a past version](#overwriting-a-past-version)
- [Versioning locally](#versioning-locally)
  - [Prerequisites](#prerequisites)
  - [Publishing a new version](#publishing-a-new-version-1)
  - [Overwriting the latest version](#overwriting-the-latest-version-1)
  - [Overwriting a past version](#overwriting-a-past-version-1)
  - [Understanding the versioning script](#understanding-the-versioning-script)
- [Testing versioning locally](#testing-versioning-locally)
- [Sync changes between _openvidu.io_ and _livekit-tutorials.openvidu.io_](#sync-changes-between-openviduio-and-livekit-tutorialsopenviduio)


## Development

This documentation is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

1. Create custom Docker image with necessary extra plugins:

```bash
docker build --pull --no-cache --rm=true -t squidfunk/mkdocs-material .
```

2. Serve the documentation:

```bash
docker run --name=mkdocs --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
```

3. Build the documentation:

```bash
docker run --rm -it -v ${PWD}:/docs -e GOOGLE_ANALYTICS_KEY=G-XXXXXXXX squidfunk/mkdocs-material build
```

Parameters:

- `GOOGLE_ANALYTICS_KEY`: Google Analytics key to track page views. This is the **MEASUREMENT ID** of the web stream details.

## Docs writing guidelines

### Branches

If you are writing documentation for the current version in development, push commits to the `next` branch. On new releases, this branch will be merged to `main` by an OpenVidu developer

### Adding a new page

When creating a new page, follow these steps:

1. **Create the Markdown file**:  
   Place a `.md` file in the appropriate folder under the [`docs`](docs) directory.

2. **Add metadata**:  
   Include the following metadata at the beginning of the file:

   ```yaml
   ---
   title: Example # Unique title (only required if the title in "mkdocs.yml" is not unique or missing)
   description: Some description # Unique description, max 160 characters
   ---
   ```

3. **Reference in `mkdocs.yml`**:  
   Two changes must be made:

   
   - Add the new page to the `nav` section in [`mkdocs.yml`](mkdocs.yml) (if you want to include it in the navigation) and set the title.

   - Include the page (relative to the docs folder) in mkdocs.yml in the mkdocs-llmstxt plugin configuration, under the corresponding section (OpenVidu for non-versioned generic pages, OpenVidu Meet or Platform for versioned pages specific to the corresponding technology):

      ```yaml
      plugins:
        - llmstxt:
            markdown_description: Self-hosted videoconference solution and SDK
            sections:
              OpenVidu Meet:
              - meet/newpage.md: Brief description # copy here the description from the metadata of the .md file.
      ```

4. **Update the site layout (if needed)**: if the new page starts a **new area**, add its folder to [`publish-tool/ovweb.yaml`](publish-tool/ovweb.yaml) — to `non_versioned_pages` if the page is not versioned, or to `versioned_pages` if it is part of a new set of versioned pages. Otherwise its links will not be rewritten and it will not be relocated correctly at publish time. A page inside an area that is already listed needs no change here.

If the new page contains links, follow the site-wide **link rules** below.

#### Link rules

There is **one convention for Markdown links** and a separate one for raw HTML. The goal is a **zero-warning build**: every link is validated by MkDocs, and `mkdocs build --strict` (run in CI) fails the build on any broken link.

**1. Markdown links and images (in regular pages) → relative, including the `.md` extension.**

Write internal links and images as paths relative to the current file:

```markdown
[Local deployment](../../self-hosting/local.md)
[Anchor on another page](../rooms/access.md#predefined-roles)
[Pricing](../../pricing.md)          <!-- non-versioned page: also relative .md, NOT /pricing/ -->
![Diagram](../../assets/images/platform/self-hosting/diagram.png#only-dark)
```

Relative `.md`/asset links are validated by MkDocs, **navigable in the editor** (Ctrl+click / preview works, which root-absolute forms break, since editors resolve `/` against the repo root instead of `docs/`), and version-safe: the built URLs stay inside the version folder, and the deploy script rewrites the built relative links that point to non-versioned pages into absolute URLs (`/pricing/`) at publish time.

> [!NOTE]
> Non-versioned pages are linked **relatively too** (`../../pricing.md`). The old bare-URL form (`/pricing/`) was a pre-MkDocs-1.6 workaround: it isn't validated and used to produce a build warning — don't use it in Markdown anymore.

**2. Markdown links and images in shared snippets and blog posts → root-absolute, resolved against `docs/`.**

A snippet is embedded in pages at different hierarchy levels, so relative paths would break. Write them as an absolute path from the `docs/` root:

```markdown
[Deployment guide](/docs/self-hosting/deployment-types.md)
![Diagram](/assets/images/platform/self-hosting/diagram.png#only-dark)
```

MkDocs resolves and validates these against `docs/` thanks to `validation.links.absolute_links: relative_to_docs` in `mkdocs.yml`, and rewrites them into correct **relative** URLs at build time — so they end up identical to hand-written relative links (validated, version-safe), just hierarchy-independent. The trade-off is that they are not editor-navigable, which is why they are reserved for snippets and blog posts. (See "Adding a new shared snippet" for the deployment-type-parametric exception where a snippet link must stay relative.)

**Blog posts use the same root-absolute form** because a post's source location changes during its lifecycle: a post lives at `docs/blog/posts/<year>/<month>/<slug>.md` (matching its frontmatter `date`) with its asset folder mirroring that location (`assets/images/blog/<year>/<month>/<slug>/`), and while it is a **draft** the year/month segments are the **literal placeholder `YYYY/MM`** — real directories with those names, in the post path, the asset paths and its `llmstxt` entry, plus a temporary creation date in the frontmatter. Everything resolves against the literal folders, so draft branches build with **zero warnings**; publishing replaces the `YYYY/MM/` string with the real `<year>/<month>/`, sets the real date and `git mv`s the post and asset folder. Hierarchy-independent links (including links to other posts, `[x](/blog/posts/<year>/<month>/<slug>.md)`, and to the post's assets, `![x](/assets/images/blog/YYYY/MM/<slug>/foo.png)`) are what let a post move without touching its content. Note there is no build-level guard against merging a draft early — drafts live on their own branch until ready. The full blog conventions live in the `.claude/skills/blog-*` skills.

**3. Raw HTML links and images (inside HTML blocks) → absolute URL form.**

MkDocs does **not** process links inside raw HTML (`<a href>`, `<img src>`), so they are neither validated nor rewritten at build time. Relative paths would need a fragile per-page `../` depth (relative to the **built** folder, not the source file) and are impossible to get right in shared snippets — so use absolute URLs:

```html
<a href="/pricing/">Pricing</a>                      <!-- non-versioned page: trailing-slash URL -->
<img src="/assets/images/home/feature.svg#only-dark" />
<a class="glightbox" href="/assets/images/foo.png">...</a>
```

**Assets referenced this way stay version-correct thanks to the publishing tool**: `ovweb` rewrites `src|href="/assets/`, `/javascripts/`, `/stylesheets/` into `"/X.Y/assets/`... in every **versioned** page at publish time, so each version keeps referencing its own assets even after later versions change them. Non-versioned pages keep the root form (root assets are always the latest publish's — correct for them). Locally the dev server serves assets at the root, so `/assets/...` just works.

Links from HTML to **versioned** pages (rare) still use relative-to-built-folder paths: a page `performance.md` builds to `performance/index.html`, so add one extra `../` compared to the Markdown path (unless linking from an `index.md`).

**4. Releases pages are the one exception.** In `docs/meet/releases.md` and `docs/docs/releases.md`, every link inside a version's release-notes section must be an **absolute, version-pinned** URL to that same version (e.g. `/3.4/docs/...`). See the [Versioning](#versioning) section.

> [!IMPORTANT]
> **Anchors:** links to a `pymdownx.tabbed` tab label (`=== "Run OpenVidu locally"` → `#run-openvidu-locally`) work at runtime but MkDocs's anchor validator can't see tab-generated ids, so it logs a **false-positive `INFO` "no such anchor"**. This is expected. Anchor validation is therefore kept at `info` (not `warn`) in `mkdocs.yml`, so it never fails `--strict`. Real broken anchors still appear in the log as `INFO` — scan for them when you touch headings.

> [!NOTE]
> When serving/building the site locally there should be **no `WARNING` messages at all**. `INFO` messages about anchors are expected (see above). If you add a page that is intentionally not in the nav, add it to `not_in_nav` in `mkdocs.yml` so it doesn't warn.

### Adding a new shared snippet

When creating a new shared snippet, follow these steps:

1. **Create the Markdown file**:  
   Place a `.md` file in the [`shared`](shared) directory, in the folder matching the docs area (and, for self-hosting, the cloud provider) it belongs to — see [`shared/README.md`](shared/README.md) for the folder conventions.

2. **Reference in a page**:
   Use the following syntax to include the snippet in other snippets or pages:

   ```markdown
   --8<-- "shared/snippet.md"
   ```

> [!NOTE]
> The path is relative to the root of the repository.

> [!IMPORTANT]
> **Links in shared snippets must be root-absolute** (Markdown `[x](/docs/.../bar.md)`, `![x](/assets/...)`; HTML `src="/assets/..."`). A snippet is embedded in pages at **different hierarchy levels**, so a relative path that is correct in one host page is broken in another. The root-absolute form resolves against `docs/` regardless of where the snippet is included (see [Link rules](#link-rules)). This is why every asset and internal link in `shared/` uses the absolute form.
>
> **Exception — deployment-type-parametric snippets.** A few `shared/self-hosting/**` snippets are included in **parallel deployment-type trees** (e.g. the same snippet is used in both `single-node/oracle/` and `single-node-pro/oracle/`) and link to a *sibling* page that must differ per tree, such as `[Admin](../on-premises/admin.md)` or `[Admin](./admin.md)`. These are intentionally **relative** so they resolve to the correct deployment type at each inclusion point — keep them relative. Only links to *fixed* targets (anything under `self-hosting/configuration/`, `self-hosting/how-to-guides/`, `ai/`, `tutorials/`, etc.) become absolute.

### Organizing assets

Images live in [`docs/assets/images`](docs/assets/images) and videos in [`docs/assets/videos`](docs/assets/videos), organized so an asset's folder tells you which page uses it. **Never leave files directly at the `images/` or `videos/` root** — place every new asset in the folder matching its page:

- **Versioned docs** mirror the docs tree under a product folder: an image for `docs/meet/meetings/live-captions.md` goes in `images/meet/meetings/live-captions/`, and one for `docs/docs/self-hosting/production-ready/performance.md` goes in `images/platform/self-hosting/production-ready/performance/` (`docs/docs/**` ↔ `images/platform/**`).
- **Non-versioned root pages** get a top-level folder named after the page: `images/home/` (landing), `images/about-us/`, `images/pricing/`, `images/research/`, `images/openvidu-meet-vs-openvidu-platform/`... Blog post assets follow the blog convention: `images/blog/YYYY/MM/<slug>/`, mirroring the post's own location (`blog/posts/YYYY/MM/<slug>.md`). Drafts use literal `YYYY/MM` placeholder directories, moved together with the post at publish time.
- **Cross-cutting assets**: `images/logos/` is the brand-asset library (OpenVidu, Meet and Platform logo variants and third-party logos — files here may be kept even while unreferenced), `images/og/` holds social cards and `images/sponsors/` sponsor/funding logos.
- An asset used by several pages lives in the folder of the page it primarily belongs to, and other pages reference it there (e.g. the deployment architecture diagrams in `images/platform/self-hosting/deployment-types/` are also referenced from OpenVidu Meet's advanced deployment page).
- **Images reused across deployment types** (referenced from `shared/self-hosting/**` snippets or from several `elastic`/`ha`/`single-node` pages) go in `images/platform/self-hosting/shared/`, in a subfolder per cloud provider (`aws/`, `azure/`, `digitalocean/`, `gcp/`, `oracle/`) mirroring the [`shared/self-hosting`](shared/self-hosting) snippet folders.

### Mkdocs Material tag system

We use a tag system to determine which JS scripts should be included and run for each page:

```markdown
---
title: My page
tags:
  - tag1
  - tag2
  - ...
---
```

These are the tags currently used:

- `setupwowjs`: add this tag to the page if there are [wow.js](https://wowjs.uk/) animations in it (elements with class `wow`):

  ```html
  <div class="wow animated animatedFadeInUp fadeInUp">
    ...
  </div>
  ```

- `setupcardglow`: add this tag to the page if there are cards with glow effect in it. The HTML structure of these cards must comply with:

  ```html
  <div class="feature-cards">
    <div class="grid cards">
      ...
    </div>
  </div>
  ```

- `setupcarousel`: add this tag to the page if there are [Flickity carousels](https://flickity.metafizzy.co/) in it. The HTML structure of these carousels must comply with:

  ```html
  <div class="carousel">
    <div class="carousel-cell">
      ...
    </div>
    ...
  </div>
  ```

- `setupcustomgallery`: add this tag to the page if there are custom [GLightbox](https://biati-digital.github.io/glightbox/) elements in it. This means that if a Markdown page only contains Markdown images (e.g. `![Image description](image-url.jpg)`), this tag is **not necessary** (the default behavior of the plugin mkdocs-glightbox will be used to automatically create the gallery). But if the page contains HTML images or videos marked with the glightbox class, this tag **is required**. The HTML structure of these elements is like this:

    For images:

    ```html
    <a class="glightbox" href="image.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="image.png" loading="lazy" class="control-height"/></a>
    ```

    For videos:

    ```html
    <a class="glightbox" href="video.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="video.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>
    ```

#### Theme-dependent images/videos

For images using the default Mkdocs Material syntax (using the `#only-dark` and `#only-light` suffixes):

```markdown
![Image description](image-dark.png#only-dark)
![Image description](image-light.png#only-light)
```

For images/videos using the custom GLightbox syntax, apart from having tag `setupcustomgallery` in its page, this must be the HTML structure:

```html
<a class="glightbox" href="image-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="image-dark.png#only-dark" loading="lazy" class="round-corners" alt="Image description"/></a>
<a class="glightbox" href="image-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="image-light.png#only-light" loading="lazy" class="round-corners" alt="Image description"/></a>
```

  > - The `#only-dark` and `#only-light` suffixes must be present in the `src` attribute of the `<img>` or `<video>` elements, but **NOT** in the `href` attribute of the `<a>` parent element.
  > - It is important that each HTML `<a>` element is a **one-liner**. There are some strange behaviors when they are not.

## Versioning

MkDocs Material uses the [mike](https://github.com/jimporter/mike) tool for versioning. mike uses GitHub pages to host the documentation, and builds each version on branch `gh-pages`.

> [!IMPORTANT]
> Documentation versions are grouped by **minor** release and named `X.Y` (e.g. `3.8`): one git branch, one `gh-pages` folder and one version-selector entry per minor version. The content of each `X.Y` version always reflects the **newest patch** of that minor. Patch releases do **not** create new documentation versions:
>
> - **New minor release** (e.g. `3.9.0`) → publish a new version `3.9` (`ovweb publish new 3.9`).
> - **Patch for the current minor** (e.g. `3.8.1`) → merge the docs to `main` and rebuild the latest version in place (`ovweb publish latest 3.8`). Add the patch's section to the releases pages; the version selector does not change.
> - **Patch for an old minor** (e.g. `3.7.2`) → commit to branch `3.7` and rebuild that past version (`ovweb publish past 3.7`).
>
> Legacy exact-patch URLs (`/3.4.1/...`) are redirected to their minor folder (`/3.4/...`) by the 404 page. That rule, and every other redirect on the site, is declared in [`publish-tool/ovweb.yaml`](publish-tool/ovweb.yaml).

> [!IMPORTANT]
> **Releases pages** (`docs/meet/releases.md` and `docs/docs/releases.md`) follow two conventions, because the same release notes are served across **every** documentation version (on publish, the *content* of the latest page — the notes and their table of contents, nothing else — is spliced into every version folder's releases page, so any version shows the full, most-recent notes while keeping its own navigation, links and outdated-version banner):
>
> - **Patch notes go in a subsection under their minor's first-patch section.** Each minor has a top-level `## X.Y.0` section (e.g. `## 3.4.0`); the notes for later patches of that minor go **below it**, under a `### Patch releases` heading as `#### 3.4.1`, `#### 3.4.2`, ... — never in a new top-level section. The auto-scroll (`releases-scroll-to-version.js`, enabled by the `scrolltoversion` frontmatter tag) jumps to the `## X.Y.0` heading, so viewing `/3.4/docs/releases/` lands on the 3.4 notes with every 3.4.x patch below.
> - **Links are always absolute and pinned to their own version.** Every link inside a release-notes section must be an absolute URL pointing to **the version that section documents** (links in the `3.4.0`/`3.4.x` sections point to `/3.4/docs/...`, never `/latest/...` nor relative). A link followed from an old release note then lands on the matching version of that page, and the outdated-version banner explains the jump. This is the one place where hardcoding a version in a link is required — and it is what makes the content-only splice safe: a relative link would resolve against whichever version folder the notes were copied into. The publish step **verifies** this and fails rather than publishing a broken link.

> [!WARNING]
> Each `X.Y` version always serves the docs of its **newest patch**, so the documentation of **older patches is not reachable** — only the latest patch of every minor is ever published. Be careful with changes: if a page or anchor that an older patch's release notes link to is removed or renamed in a later patch, that link breaks with no older-patch page to fall back to. Prefer additive changes, and when a linked page must move, update the affected release-notes links too.

The repository must be using MkDocs Material and must be properly setup like explained [here](https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/). This proper setup includes the following points:

- Adding `extra.version.provider: mike` to mkdocs.yml.
- Properly configuring the default alias like `extra.version.default: latest` in mkdocs.yml.
- Adding `extra.version.alias: true` to mkdocs.yml (just to show the default alias tag next to the version selector).
- Properly configuring `site_url` in mkdocs.yml to the actual domain name in which the docs will be served (this allows staying on the same path when switching versions).

These configurations get the repository ready for versioning.

Publishing is done by **`ovweb`**, the CLI in [`publish-tool/`](publish-tool/). Its
[README](publish-tool/README.md) is the authoritative reference: what a publish does step by
step, how the link rewriting works, how redirects are configured, and how the parity gate proves
a change to the rewriting logic is safe.

## Versioning with GitHub Actions

Run action [Publish Web](https://github.com/OpenVidu/openvidu.io/actions/workflows/publish-web.yaml)
and pick the command that matches what you are doing:

| What you are doing                                    | **command** | **version** |
| ----------------------------------------------------- | ----------- | ----------- |
| Publishing a brand-new minor release                  | `new`       | `3.9`       |
| A content fix, or a patch release of the current minor | `latest`    | `3.8`       |
| A fix or patch release for an older minor              | `past`      | `3.7`       |

Tick **dry_run** to see the plan first: it resolves everything, prints the ordered steps and the
redirects it would install, and touches nothing.

**A failed publish cannot break the live site.** `ovweb` builds, post-processes and commits
`gh-pages` entirely locally, and pushes only once the published tree is correct; a failure
anywhere before that rolls the local branch back and leaves the remote untouched. So there is no
backup branch and no force-push recovery path to remember. The workflow runs `ovweb verify`
afterwards to assert the published layout.

## Versioning locally

### Prerequisites

Install the tool and everything needed to build the site:

```bash
pip install "./publish-tool[build]"
```

Install it **non-editable**, as above. Publishing a past version checks out that version's
branch, which does not contain the tool — from `site-packages` it survives the switch. Run
`ovweb doctor` to check the dependencies, the version pins, the configuration and the git state
before publishing.

### Publishing

```bash
ovweb publish new    3.9   # new minor: deploys 3.9, moves `latest`, refreshes the root pages,
                           # and creates the 3.9 branch so the version can be fixed later
ovweb publish latest 3.8   # rebuild the newest version from main in place, refresh the root
                           # pages, and rebase the 3.8 branch onto main
ovweb publish past   3.7   # rebuild an older minor from its own branch; the site root and
                           # `latest` are left alone
```

Add `--dry-run` to print the plan without building or pushing, or `--no-push` to do everything
locally and inspect the result before it goes out.

### Understanding what a publish does

`mike` builds the **whole** site — versioned and non-versioned pages alike — into each version
folder, with relative links. `ovweb` then post-processes that output on `gh-pages`:

1. Deploy the version with `mike`.
2. In the **versioned** pages (docs and meet), rewrite links that point at pages served from the
   root (home, support, pricing…) into absolute paths (e.g. `/pricing/`), and **version-pin
   raw-HTML asset references** (`src`/`href` to `/assets/`, `/javascripts/`, `/stylesheets/`) to
   the version's own folder (e.g. `/3.9/assets/`), so each version keeps referencing its own
   assets even after later versions change them. Markdown asset links are already handled by
   MkDocs at build time and need no pinning. Point each page's `canonical` and `og:url` at
   `/latest/`, so ranking signals consolidate on one evergreen URL.
3. In the pages that will be served from the root, rewrite links to versioned pages into
   `/latest/docs/…`, and strip the version from each page's own URL — while shielding
   author-pinned `/X.Y/docs/…` links, which must survive.
4. Make every location in the search index absolute.
5. Update `llms.txt` and the RSS feeds.
6. Move the non-versioned pages and root files out to the site root, so the global pages served
   from `/` always reflect the newest release, and copy the asset folders there.
7. Copy the version's `sitemap.xml` to the root, rewrite it and regenerate its `.gz`. The root
   sitemap is the only one published — `robots.txt` names it, and it is a plain `urlset` rather
   than an index — so the per-version copies are deleted rather than maintained.
8. Write the [generated redirect pages](publish-tool/README.md#redirects), so `/X.Y/` and
   `/latest/` land on the documentation.
9. Splice the newest release notes into every other version folder, so any version shows the full
   changelog while keeping its own navigation.
10. Commit and push `gh-pages`.

> [!NOTE]
> Steps 3, 5, 6 and the root half of 7 only run when the version being published becomes
> `latest`. `ovweb publish past` skips them, so the pages served from the site root are left
> untouched.

## Testing versioning locally

Serve the content of the `gh-pages` branch:

```bash
mike serve
```

Build a version without pushing anything — `mike` commits to the local `gh-pages` only:

```bash
mike deploy 3.0
```

Or run a whole publish locally, post-processing included, and inspect the result:

```bash
ovweb publish latest 3.8 --no-push --keep-worktree
```

## Sync changes between _openvidu.io_ and _livekit-tutorials.openvidu.io_

Whenever any changes are made to the tutorials documentation, theses changes must be also reflected in repository [livekit-tutorials-docs](https://github.com/OpenVidu/livekit-tutorials-docs) so they end up available in [livekit-tutorials.openvidu.io](https://livekit-tutorials.openvidu.io/).

To apply changes in the web _livekit-tutorials.openvidu.io_:

- In this repository, push the changes to tutorials documentation to the `main` branch and run GitHub Action to [overwrite the latest version](#overwriting-the-latest-version).
- In repository [livekit-tutorials-docs](https://github.com/OpenVidu/livekit-tutorials-docs), push the changes to the `main` branch and run action [Publish Web](https://github.com/OpenVidu/livekit-tutorials-docs/actions/workflows/publish-web.yaml) selecting the `main` branch.
