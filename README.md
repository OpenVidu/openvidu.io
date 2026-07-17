

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

4. **Update custom versioning scripts (if needed)**:
   - **Non-versioned pages**: If the new page is not versioned, add it to the `NON_VERSIONED_PAGES` array in the [`push-new-version.sh` script](custom-versioning/push-new-version.sh).
   - **Versioned pages**: If the new page is part of a new set of versioned pages, add it to the `VERSIONED_PAGES` array in the [`push-new-version.sh` script](custom-versioning/push-new-version.sh).

If the new page contains links to other pages, take into account the following:

- **Markdown links**: Use relative paths pointing to the Markdown file (including the `.md` extension).
- **HTML links**: Use relative paths pointing to the folder containing the HTML file. Keep in mind that, after building the documentation, the HTML files will be placed in a folder with the same name as the Markdown file (except `index.md` files, which will be placed in its parent folder as `index.html`). For example, if you have a Markdown file `performance.md`, it will be built to `performance/index.html`. Therefore, you must add an extra `../` to the path to point to the correct folder unless the markdown file from which you are linking is named `index.md`.

> [!IMPORTANT]
> Links to non-versioned pages must be absolute paths (e.g. `/pricing/`).

> [!NOTE]
> When serving the site locally using `mkdocs-material`, there should be no warnings about links except for using absolute paths to non-versioned pages. 

### Adding a new shared snippet

When creating a new shared snippet, follow these steps:

1. **Create the Markdown file**:  
   Place a `.md` file in the [`shared`](shared) directory.

2. **Reference in a page**:
   Use the following syntax to include the snippet in other snippets or pages:

   ```markdown
   --8<-- "shared/snippet.md"
   ```

> [!NOTE]
> The path is relative to the root of the repository.

> [!IMPORTANT]
> If the new snippet contains links to other pages, the same rules as for pages apply. Since the release of Mkdocs 1.6, it is possible to use absolute links to other pages, and Mkdocs will make them relative to the `docs_dir` root folder thanks to [this configuration options in `mkdocs.yml`](https://github.com/OpenVidu/openvidu.io/blob/e1d6bb08d7f6e222bf9a0c420bd79b552fb0a25c/mkdocs.yml#L194-L195). So, now any document (e.g. "dir1/foo.md") can link to the document "dir2/bar.md" as `[link](/dir2/bar.md)`, in addition to the previously only correct way `[link](../dir2/bar.md)`.
> 
> **This allows to use local links in shared snippets that are embedded in pages with different hierarchy!**.

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
> - **New minor release** (e.g. `3.9.0`) → publish a new version `3.9` (`push-new-version.sh 3.9`).
> - **Patch for the current minor** (e.g. `3.8.1`) → merge the docs to `main` and overwrite the latest version (`overwrite-latest-version.sh 3.8`). Add the patch's section to the releases pages; the version selector does not change.
> - **Patch for an old minor** (e.g. `3.7.2`) → commit to branch `3.7` and overwrite that past version (`overwrite-past-version.sh 3.7`).
>
> Legacy exact-patch URLs (`/3.4.1/...`) are redirected to their minor folder (`/3.4/...`) by the 404 page.

> [!IMPORTANT]
> **Releases pages** (`docs/meet/releases.md` and `docs/docs/releases.md`) follow two conventions, because a single copy of each is served across **every** documentation version (on publish, the latest page is copied into all version folders, so any version's releases page shows the full, most-recent notes):
>
> - **Patch notes go in a subsection under their minor's first-patch section.** Each minor has a top-level `## X.Y.0` section (e.g. `## 3.4.0`); the notes for later patches of that minor go **below it**, under a `### Patch releases` heading as `#### 3.4.1`, `#### 3.4.2`, ... — never in a new top-level section. The auto-scroll (`releases-scroll-to-version.js`, enabled by the `scrolltoversion` frontmatter tag) jumps to the `## X.Y.0` heading, so viewing `/3.4/docs/releases/` lands on the 3.4 notes with every 3.4.x patch below.
> - **Links are always absolute and pinned to their own version.** Every link inside a release-notes section must be an absolute URL pointing to **the version that section documents** (links in the `3.4.0`/`3.4.x` sections point to `/3.4/docs/...`, never `/latest/...` nor relative). A link followed from an old release note then lands on the matching version of that page, and the outdated-version banner explains the jump. This is the one place where hardcoding a version in a link is required.

> [!WARNING]
> Each `X.Y` version always serves the docs of its **newest patch**, so the documentation of **older patches is not reachable** — only the latest patch of every minor is ever published. Be careful with changes: if a page or anchor that an older patch's release notes link to is removed or renamed in a later patch, that link breaks with no older-patch page to fall back to. Prefer additive changes, and when a linked page must move, update the affected release-notes links too.

The repository must be using MkDocs Material and must be properly setup like explained [here](https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/). This proper setup includes the following points:

- Adding `extra.version.provider: mike` to mkdocs.yml.
- Properly configuring the default alias like `extra.version.default: latest` in mkdocs.yml.
- Adding `extra.version.alias: true` to mkdocs.yml (just to show the default alias tag next to the version selector).
- Properly configuring `site_url` in mkdocs.yml to the actual domain name in which the docs will be served (this allows staying on the same path when switching versions).

These configurations get the repository ready for versioning.

## Versioning with GitHub Actions

Run action [Publish Web](https://github.com/OpenVidu/openvidu.io/actions/workflows/publish-web.yaml):

### Publishing a new version

- **Select the script to execute**: `push-new-version.sh`
- **Version to publish**: `3.0`

### Overwriting the latest version

- **Select the script to execute**: `overwrite-latest-version.sh`
- **Version to publish**: `3.0`

### Overwriting a past version

- **Select the script to execute**: `overwrite-past-version.sh`
- **Version to publish**: `3.0`

## Versioning locally

### Prerequisites

- `mike`:

  ```bash
  pip install mike
  ```

- Packages `mkdocs-material` and `mkdocs-glightbox`:

  ```bash
  pip install mkdocs-material mkdocs-glightbox
  ```

### Publishing a new version

This script publishes a new version, updates alias "latest" to point to this new version, and updates the non-versioned files at root.

It also creates a new branch from main named after the minor version (e.g. `3.0`) and pushes it to the repository. This allows modifying past versions if required later.

```bash
cd custom-versioning
./push-new-version.sh 3.0
```

### Overwriting the latest version

This script overwrites the content of the latest published version, also updating the non-versioned files at root.

It also updates the version branch with any new commits available in main branch (with a `git rebase`). This keeps the latest version branch up to date with the latest changes in main.

```bash
cd custom-versioning
./overwrite-latest-version.sh 3.0
```

### Overwriting a past version

This script overwrites the content of a specific past version without touching the non-versioned files at root.

In this case, all the changes to be published must be already commited into the version branch before calling this script.

```bash
cd custom-versioning
./overwrite-past-version.sh 3.0
```

### Understanding the versioning script

Script `push-new-version.sh` performs the following steps:

1. Deploy a new version of the documentation with `mike`.
2. Change links in versioned HTML files (docs and meet) from new version that point to non-versioned files (home, support, pricing...) accessible from "/" to use absolute paths (e.g. `/pricing/`).
3. Change links in non-versioned HTML files from new version that point to versioned files to use absolute paths to the latest version (e.g. `/latest/docs/`).
4. Remove version from links that point to non-versioned files in the new version.
5. Update `llms.txt` file: replace version with 'latest' for versioned pages and remove version from non-versioned pages.
6. Move non-versioned files from the new version to root. This keeps the global pages served on "/" always updated to the latest published version.
7. Update `sitemap.xml`: copy it from the version folder to root, replace version with 'latest' for versioned pages, remove version from non-versioned pages, and generate the compressed `sitemap.xml.gz` file.
8. Add a redirection HTML file to the root of the new version to redirect to the docs index page (`docs/`).

> [!NOTE]
> The overwriting of the non-versioned files located at root of `gh-pages` branch (points 3, 4, 5, 6 and 7) is done by default. To avoid overriding these files, call the script adding `false` as second argument: `./push-new-version.sh 3.0 false`. Script `overwrite-past-version.sh` does this to only overwrite the files of that specific past version without affecting the root non-versioned files.

## Testing versioning locally

This will serve the content of gh-pages branch locally:

```bash
mike serve
```

To build a new version without pushing to GitHub:

```bash
mike deploy 3.0
```

## Sync changes between _openvidu.io_ and _livekit-tutorials.openvidu.io_

Whenever any changes are made to the tutorials documentation, theses changes must be also reflected in repository [livekit-tutorials-docs](https://github.com/OpenVidu/livekit-tutorials-docs) so they end up available in [livekit-tutorials.openvidu.io](https://livekit-tutorials.openvidu.io/).

To apply changes in the web _livekit-tutorials.openvidu.io_:

- In this repository, push the changes to tutorials documentation to the `main` branch and run GitHub Action to [overwrite the latest version](#overwriting-the-latest-version).
- In repository [livekit-tutorials-docs](https://github.com/OpenVidu/livekit-tutorials-docs), push the changes to the `main` branch and run action [Publish Web](https://github.com/OpenVidu/livekit-tutorials-docs/actions/workflows/publish-web.yaml) selecting the `main` branch.
