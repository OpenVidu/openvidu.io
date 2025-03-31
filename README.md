

# openvidu-docs

- [openvidu-docs](#openvidu-docs)
  - [Development](#development)
  - [Docs writing guidelines](#docs-writing-guidelines)
    - [Adding a new page](#adding-a-new-page)
    - [Adding a new shared snippet](#adding-a-new-shared-snippet)
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

If you are creating documentation for the current version in development, push commits to the `next` branch.

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
   Add the new page to the `nav` section in [`mkdocs.yml`](mkdocs.yml) (if you want to include it in the navigation) and set the title.

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
> If the new snippet contains links to other pages, the same rules as for pages apply. However, keep in mind that links will be relative to the page where the snippet is included. Therefore, ensure all referencing files are at the same level in the hierarchy.

## Versioning

MkDocs Material uses the [mike](https://github.com/jimporter/mike) tool for versioning. mike uses GitHub pages to host the documentation, and builds each version on branch `gh-pages`.

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
- **Version to publish**: `3.0.0`

### Overwriting the latest version

- **Select the script to execute**: `overwrite-latest-version.sh`
- **Version to publish**: `3.0.0`

### Overwriting a past version

- **Select the script to execute**: `overwrite-past-version.sh`
- **Version to publish**: `3.0.0`

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

It also creates a new branch from main named after the version (e.g. `3.0.0`) and pushes it to the repository. This allows modifying past versions if required later.

```bash
cd custom-versioning
./push-new-version.sh 3.0.0
```

### Overwriting the latest version

This script overwrites the content of the latest published version, also updating the non-versioned files at root.

It also updates the version branch with any new commits available in main branch (with a `git rebase`). This keeps the latest version branch up to date with the latest changes in main.

```bash
cd custom-versioning
./overwrite-latest-version.sh 3.0.0
```

### Overwriting a past version

This script overwrites the content of a specific past version without touching the non-versioned files at root.

In this case, all the changes to be published must be already commited into the version branch before calling this script.

```bash
cd custom-versioning
./overwrite-past-version.sh 3.0.0
```

### Understanding the versioning script

Script `push-new-version.sh` performs the following steps:

1. Deploy a new version of the documentation with `mike`.
2. Change links in versioned HTML files (docs) from new version that point to non-versioned files (home, support, pricing...) accessible from "/" to use absolute paths (e.g. `/pricing/`).
3. Change links in non-versioned HTML files from new version that point to versioned files to use absolute paths to the latest version (e.g. `/latest/docs/`).
4. Remove version from links that point to non-versioned files in the new version.
5. Remove non-versioned pages from the sitemap.xml file of the new version.
6. Update the sitemap_index.xml file to include the new version sitemap.
7. Regenerate the root sitemap.xml file that includes non-versioned pages.
8. Move non-versioned files from the new version to root. This keeps the global pages served on "/" always updated to the latest published version.
9. Add a redirection HTML file to the root of the new version to redirect to the getting started page (`docs/getting-started/`).

> [!NOTE]
> The overwriting of the non-versioned files located at root of `gh-pages` branch (points 3, 4, 7 and 8) is done by default. To avoid overriding these files, call the script adding `false` as second argument: `./push-new-version.sh 3.0.0 false`. Script `overwrite-past-version.sh` does this to only overwrite the files of that specific past version without affecting the root non-versioned files.

## Testing versioning locally

This will serve the content of gh-pages branch locally:

```bash
mike serve
```

To build a new version without pushing to GitHub:

```bash
mike deploy 3.0.0
```

## Sync changes between _openvidu.io_ and _livekit-tutorials.openvidu.io_

Whenever any changes are made to the tutorials documentation, theses changes must be also reflected in repository [livekit-tutorials-docs](https://github.com/OpenVidu/livekit-tutorials-docs) so they end up available in [livekit-tutorials.openvidu.io](https://livekit-tutorials.openvidu.io/).

To apply changes in the web _livekit-tutorials.openvidu.io_:

- In this repository, push the changes to tutorials documentation to the `main` branch and run GitHub Action to [overwrite the latest version](#overwriting-the-latest-version).
- In repository [livekit-tutorials-docs](https://github.com/OpenVidu/livekit-tutorials-docs), push the changes to the `main` branch and run action [Publish Web](https://github.com/OpenVidu/livekit-tutorials-docs/actions/workflows/publish-web.yaml) selecting the `main` branch.
