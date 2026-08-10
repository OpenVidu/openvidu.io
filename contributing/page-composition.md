# How pages are composed

## Frontmatter drives behavior

- `title`, `description` — required SEO fields; budgets and uniqueness in
  [authoring.md](authoring.md).
- `template: home.html` — the landing page uses a custom template.
- `hide:` — `navigation`, `toc`, `footer`, `search-bar`, `version-selector`, `footer-prev`,
  `footer-next`. The non-standard ones (`search-bar`, `version-selector`, `footer-prev`,
  `footer-next`) are implemented in [`docs/overrides/main.html`](../docs/overrides/main.html).
- **Structured data lives in frontmatter**: `publications:` (`research.md`) and `faq:`
  (`pricing.md`) feed the JSON-LD emitted by
  [`docs/overrides/partials/json-ld.html`](../docs/overrides/partials/json-ld.html). When editing
  those page sections, update the matching frontmatter entry (anchors must equal heading ids;
  answers/abstracts must match visible content).
- `tags:` — the tag system below.

## Mkdocs Material tag system

Frontmatter `tags:` determine which JS/CSS gets included and run for each page (wired in
[`docs/overrides/main.html`](../docs/overrides/main.html)):

```yaml
---
title: "My page"
tags:
  - tag1
  - tag2
---
```

Each tag expects a specific HTML structure. **If you copy a visual pattern from another page,
copy its tags too.** These are the tags currently used:

- `setupwowjs`: the page has [wow.js](https://wowjs.uk/) animations (elements with class `wow`):

  ```html
  <div class="wow animated animatedFadeInUp fadeInUp">
    ...
  </div>
  ```

- `setupcardglow`: the page has cards with glow effect. The HTML structure must comply with:

  ```html
  <div class="feature-cards">
    <div class="grid cards">
      ...
    </div>
  </div>
  ```

- `setupcarousel`: the page has [Flickity carousels](https://flickity.metafizzy.co/):

  ```html
  <div class="carousel">
    <div class="carousel-cell">
      ...
    </div>
    ...
  </div>
  ```

- `setupcustomgallery`: the page has custom [GLightbox](https://biati-digital.github.io/glightbox/)
  elements. A page with only Markdown images (`![x](image.jpg)`) does **not** need it (the
  mkdocs-glightbox plugin handles those automatically); a page with HTML images or videos marked
  with the `glightbox` class **does**:

  ```html
  <a class="glightbox" href="image.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="image.png" loading="lazy" class="control-height" alt="Image description"/></a>
  ```

  ```html
  <a class="glightbox" href="video.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="video.mp4" loading="lazy" defer muted playsinline autoplay loop async></video></a>
  ```

- `copyclipboard`: the page has inline copy-to-clipboard elements (a `.copy-inline` wrapper whose
  `.copy-btn` copies its `data-copy` value). Loads
  [`copy-clipboard.js`](../docs/javascripts/copy-clipboard.js).

- `scrolltoversion`: releases pages only — auto-scrolls to the `## X.Y.0` heading of the version
  being viewed. Loads
  [`releases-scroll-to-version.js`](../docs/javascripts/releases-scroll-to-version.js).

- `openviduregister`: the page embeds the `<openvidu-register>` Amplify sign-in web component
  (only [`account.md`](../docs/account.md)). Loads the ~4.4 MB `openvidu-register.js` bundle plus
  `openvidu-register.css` and `amplify.css` — never load these site-wide; every other page gets
  its Sign In/Sign Out header button from a small inline script in
  [`partials/header.html`](../docs/overrides/partials/header.html) that reads the Cognito session
  from `localStorage`.

- `dropdown`: groups the page's top-level nav tab into a dropdown menu; read by
  [`docs/overrides/partials/tabs.html`](../docs/overrides/partials/tabs.html) from the nav item's
  page (or the first child of a nav group).

- `Meet` / `Platform`: load [`meet.css`](../docs/stylesheets/meet.css) /
  [`platform.css`](../docs/stylesheets/platform.css) for product-specific styling. These are
  **not written per page**: they come from folder-level metadata —
  [`docs/meet/.meta.yml`](../docs/meet/.meta.yml) and [`docs/docs/.meta.yml`](../docs/docs/.meta.yml)
  each declare `tags:` that the `meta` plugin (enabled in `mkdocs.yml`) merges into every page of
  the folder. A new page under `docs/meet/` or `docs/docs/` gets its product tag automatically.

The `tags:`↔HTML contract is checked by `ovweb lint` (a page whose content carries
glightbox/feature-cards/carousel markup must declare the matching tag) — see
[checks.md](checks.md).

### Theme-dependent images/videos

For images using the default Mkdocs Material syntax (the `#only-dark` and `#only-light`
suffixes):

```markdown
![Image description](image-dark.png#only-dark)
![Image description](image-light.png#only-light)
```

For images/videos using the custom GLightbox syntax, apart from having tag `setupcustomgallery`
in its page, this must be the HTML structure:

```html
<a class="glightbox" href="image-dark.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="image-dark.png#only-dark" loading="lazy" class="round-corners" alt="Image description"/></a>
<a class="glightbox" href="image-light.png" data-type="image" data-desc-position="bottom" data-gallery="gallery1"><img src="image-light.png#only-light" loading="lazy" class="round-corners" alt="Image description"/></a>
```

> - The `#only-dark` and `#only-light` suffixes must be present in the `src` attribute of the
>   `<img>` or `<video>` elements, but **NOT** in the `href` attribute of the `<a>` parent
>   element.
> - It is important that each HTML `<a>` element is a **one-liner**. There are some strange
>   behaviors when they are not.

## Theme overrides

Material theme customization lives in [`docs/overrides/`](../docs/overrides) (`custom_dir`):

- `main.html` extends the Material base template with Jinja blocks (`extrahead`, `scripts`,
  `styles`, `outdated`...).
- `home.html` extends `main.html` (the landing page template).
- `partials/` adds or overrides partials: `header.html`, `footer.html`, `tabs.html`,
  `json-ld.html`, `og.html`.

Site-wide changes go here — follow the "before/after" comment markers inside the blocks.

## HTML-in-Markdown

Pages mix raw HTML and Markdown via `md_in_html` (`<div markdown>`). Layout uses unsemantic-grid
classes (`grid-50`, `grid-90`, `tablet-grid-...`). Material features in use: admonitions, `???`
collapsible details, content tabs, attr_list (`{ .class }`, `{:target="_blank"}`). Links inside
raw HTML follow their own rule — see [link rules](link-rules.md), rule 3.
