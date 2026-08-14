# How pages are composed

## Frontmatter drives behavior

- `title`, `description` — required SEO fields; budgets and uniqueness in
  [authoring.md](authoring.md).
- `template: home.html` — the landing page uses a custom template.
- `hide:` — `navigation`, `toc`, `footer`, `search-bar`, `version-selector`. The non-standard
  ones (`search-bar`, `version-selector`) are implemented in
  [`docs/overrides/main.html`](../docs/overrides/main.html).
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

- `setupcarousel`: the page has [Splide carousels](https://splidejs.com/):

  ```html
  <div class="splide" markdown>
    <div class="splide__track" markdown>
      <ul class="splide__list" markdown>
        <li class="splide__slide" markdown>
          <div class="carousel-cell-content" markdown>
          ...
          </div>
        </li>
        ...
      </ul>
    </div>
  </div>
  ```

- `setupcustomgallery`: the page has **video** lightbox anchors (hand-written
  `<a class="glightbox" data-type="video">` — see the video patterns below). The script
  re-initializes [GLightbox](https://biati-digital.github.io/glightbox/) with the video player
  options (autoplaying plyr slides). Pages with only images never need it: Markdown images are
  wrapped by the mkdocs-glightbox plugin automatically.

- `lazyvideo`: the page has below-the-fold videos (`<video class="lazy-video">`, the default
  video pattern below). Loads [`lazy-video.js`](../docs/javascripts/lazy-video.js), which plays
  each video only while it is on screen and never downloads the hidden theme variant.

- `scrolltoversion`: releases pages only — auto-scrolls to the `## X.Y.0` heading of the version
  being viewed. Loads
  [`releases-scroll-to-version.js`](../docs/javascripts/releases-scroll-to-version.js).

- `openviduregister`: the page embeds the `<openvidu-register>` Amplify sign-in web component
  (only [`account.md`](../docs/account.md)). Loads the ~4.4 MB `openvidu-register.js` bundle plus
  `openvidu-register.css` and `amplify.css` — never load these site-wide. On every other page the
  header account button is a static "OpenVidu Pro account" link to `/account/`
  ([`partials/header.html`](../docs/overrides/partials/header.html)); only the account page
  itself, where the bundle runs, relabels it.

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

### Images

Write images as plain Markdown with a **relative** path — never hand-write
`<a class="glightbox">` wrappers around images (the mkdocs-glightbox plugin generates the
lightbox anchor, and `auto_themed` assigns the dark/light gallery from the `#only-*` suffix):

```markdown
![Image description](../assets/images/x.png){ .round-corners loading=lazy }
```

- Theme variants use the `#only-dark` / `#only-light` suffixes, always in pairs:

  ```markdown
  ![Image description](image-dark.png#only-dark){ .round-corners loading=lazy }
  ![Image description](image-light.png#only-light){ .round-corners loading=lazy }
  ```

- Every image below the first viewport takes `loading=lazy`.
- Resize sources to their rendered size **before** committing them — the `optimize` plugin
  recompresses but never resizes, so oversized sources ship oversized.
- To keep an image out of the lightbox, add the `skip-gallery` class.

### Videos

Two canonical patterns — nothing else. `<video>` never takes `defer`, `async` or `loading`
(those attributes do not exist for videos and silently do nothing).

**Below the fold (the default).** No `autoplay`; the video downloads and plays only when
scrolled into view. Requires the `lazyvideo` page tag:

```html
<a class="glightbox" href="/assets/videos/x-dark.mp4" data-type="video" data-desc-position="bottom" data-gallery="dark"><video class="round-corners lazy-video" src="/assets/videos/x-dark.mp4#only-dark" preload="none" muted playsinline loop></video></a>
<a class="glightbox" href="/assets/videos/x-light.mp4" data-type="video" data-desc-position="bottom" data-gallery="light"><video class="round-corners lazy-video" src="/assets/videos/x-light.mp4#only-light" preload="none" muted playsinline loop></video></a>
```

**Above the fold (showcase heroes only).** `autoplay` is allowed, but the inline `src` must be a
small downscaled `-preview.mp4` with a `poster`; the full-size file appears only in the lightbox
`href` (see `docs/meet/index.md` for the reference):

```html
<a class="glightbox" href="/assets/videos/full.mp4" data-type="video" data-desc-position="bottom" data-gallery="gallery1"><video class="round-corners" src="/assets/videos/full-preview.mp4" poster="/assets/videos/full-poster.jpg" muted playsinline autoplay loop></video></a>
```

Rules for both patterns:

> - Theme-variant videos carry the `#only-dark`/`#only-light` suffix in the `src` attribute (in
>   pairs), **never** in the `href` of the `<a>` parent, and declare `data-gallery="dark"` /
>   `data-gallery="light"` so each theme's lightbox gallery only contains its own variants.
>   Videos without theme variants share any per-page gallery name (e.g. `gallery1`).
> - Each HTML `<a>` element is a **one-liner**. There are some strange behaviors when it is not.
> - Video lightbox anchors need the `setupcustomgallery` page tag.

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
