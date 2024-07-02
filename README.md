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

- `GOOGLE_ANALYTICS_KEY`: Google Analytics key to track page views. This is the **MEASUREMENT ID** of the web stream details.

## Publishing a new version of the documentation

MkDocs Material uses the [mike](https://github.com/jimporter/mike) tool for versioning. mike uses GitHub pages to host the documentation, and builds each version on branch `gh-pages`. Install it with `pip install mike`.

The repository must be using MkDocs Material and must be properly setup like explained [here](https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/). This proper setup includes the following points:

- Adding `extra.version.provider: mike` to mkdocs.yml.
- Properly configuring the default alias like `extra.version.default: latest` in mkdocs.yml.
- Adding `extra.version.alias: true` to mkdocs.yml (just to show the default alias tag next to the version selector).
- Properly configuring `site_url` in mkdocs.yml to the actual domain name in which the docs will be served (this allows staying on the same path when switching versions).

Once the MkDocs Material project is properly setup and our documentation completed, all we have to do is run this script:

```bash
cd custom-versioning
./push.sh 3.0.0
```

### Understanding the versioning script

Script `push.sh` performs the following steps:

- Deploy a new version of the documentation with `mike`.
- Update the non-versioned HTML files (home, support, pricing...) accessible from "/" to the state of the new version. This keeps the global pages served on "/ always updated to the latest published version.
- Rewrite the non-versioned HTML files (home, support, pricing...) accessible from "/X.Y.Z/" to redirect to their non-versioned counterparts served in "/". For example, this allows redirecting from `https://openvidu.io/3.0.0/pricing` to `https://openvidu.io/pricing`.
- Rewrite the versioned HTML files (docs) accessible from "/" to redirect to their versioned counterparts served in "/latest/". For example, this allows redirecting from `https://openvidu.io/docs/getting-started` to `https://openvidu.io/latest/docs/getting-started`.

## Testing versioning locally

Build the documentation version locally:

```bash
mike deploy 3.0.0
```

Serve:

```bash
mike serve
```
