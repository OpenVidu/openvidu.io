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

## Deploying a new version using `mike`

MkDocs Material uses the [mike](https://github.com/jimporter/mike) tool for versioning. mike uses GitHub pages to host the documentation, and builds each version on branh `gh-pages`.

To upload a new version:

> Remove `--push` to test locally without pushing to GitHub

```bash
mike deploy --push VERSION 3.0.0
```

```bash
mike deploy --push VERSION latest
```

```bash
mike set-default --push latest
```

To test locally the versioning:

> This only works if `mike deploy VERSION X.Y.Z` has been called first

```bash
mike serve
```
