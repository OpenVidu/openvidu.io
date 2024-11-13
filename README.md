# openvidu-docs

This documentation is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

1. Create custom Docker image with necessary extra plugins:

```bash
docker build --pull --no-cache --rm=true -t squidfunk/mkdocs-material .
```

2. Serve:

```bash
docker run --name=mkdocs --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
```

3. Build:

```bash
docker run --rm -it -v ${PWD}:/docs -e GOOGLE_ANALYTICS_KEY=G-XXXXXXXX squidfunk/mkdocs-material build
```

Parameters:

-   `GOOGLE_ANALYTICS_KEY`: Google Analytics key to track page views. This is the **MEASUREMENT ID** of the web stream details.

## Versioning

MkDocs Material uses the [mike](https://github.com/jimporter/mike) tool for versioning. mike uses GitHub pages to host the documentation, and builds each version on branch `gh-pages`.

The repository must be using MkDocs Material and must be properly setup like explained [here](https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/). This proper setup includes the following points:

-   Adding `extra.version.provider: mike` to mkdocs.yml.
-   Properly configuring the default alias like `extra.version.default: latest` in mkdocs.yml.
-   Adding `extra.version.alias: true` to mkdocs.yml (just to show the default alias tag next to the version selector).
-   Properly configuring `site_url` in mkdocs.yml to the actual domain name in which the docs will be served (this allows staying on the same path when switching versions).

These configurations get the repository ready for versioning.

## Versioning with GitHub Actions

Run action [Publish Web](https://github.com/OpenVidu/livekit-tutorials-docs/actions/workflows/publish-web.yaml):

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
2. Update the non-versioned HTML files (home, support, pricing...) accessible from "/" to the state of the new version. This keeps the global pages served on "/ always updated to the latest published version.
3. Rewrite the versioned HTML files (docs) accessible from "/" to redirect to their versioned counterparts served in "/latest/". For example, this allows redirecting from `https://openvidu.io/docs/getting-started` to `https://openvidu.io/latest/docs/getting-started`.
4. Rewrite the non-versioned HTML files (home, support, pricing...) accessible from "/X.Y.Z/" to redirect to their non-versioned counterparts served in "/". For example, this allows redirecting from `https://openvidu.io/3.0.0/pricing` to `https://openvidu.io/pricing`.

> The overwriting of the non-versioned files located at root of `gh-pages` branch (points 2 and 3 above) is done by default. To avoid overriding these files, call the script adding `false` as second argument: `./push-new-version.sh 3.0.0 false`. Script `overwrite-past-version.sh` does this to only overwrite the files of that specific past version without affecting the root non-versioned files.

## Testing versioning locally

This will serve the content of gh-pages branch locally:

```bash
mike serve
```

To build a new version without pushing to GitHub:

```bash
mike deploy 3.0.0
```

## Updating tutorials

Whenever any changes are made to the tutorials documentation, theses changes must be also reflected in repository [livekit-tutorials-docs](https://github.com/OpenVidu/livekit-tutorials-docs) so they end up available in [livekit-tutorials.openvidu.io](https://livekit-tutorials.openvidu.io/).

To apply changes in the web *livekit-tutorials.openvidu.io*:

- In this repository, push the changes to tutorials documentation to the `main` branch and run GitHub Action to [overwrite the latest version](#overwriting-the-latest-version).
- In repository [livekit-tutorials-docs](https://github.com/OpenVidu/livekit-tutorials-docs), push the changes to the `main` branch, go to `Actions` and run the workflow named "Publish Web" selecting the `main` branch.
