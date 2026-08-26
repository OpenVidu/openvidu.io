# How pages are composed

## Frontmatter drives behavior

- `title`, `description` — required SEO fields; budgets and uniqueness in
  [authoring.md](authoring.md).
- `template: home.html` — the landing page uses a custom template.
- `hide:` — `navigation`, `toc`, `footer`, `path`, `feedback`, `search-bar`, `version-selector`.
  The non-standard ones (`search-bar`, `version-selector`) are implemented in
  [`overrides/main.html`](../overrides/main.html).
- `robots:` — the page's `robots` meta tag, emitted by
  [`overrides/main.html`](../overrides/main.html). Only
  [`support/thanks.md`](../docs/support/thanks.md) uses it (`noindex, follow`): the form
  confirmation is the signal that a lead arrived, so an organic visitor landing there would
  count as one. A `noindex` page also drops out of `sitemap.xml` on its own (see the overrides
  below); pair the key with `search: {exclude: true}` and leave the page out of the `llmstxt`
  sections.
- **Structured data lives in frontmatter**: `publications:` (`research.md`) and `faq:`
  (`pricing.md`) feed the JSON-LD emitted by
  [`overrides/partials/json-ld.html`](../overrides/partials/json-ld.html). When editing
  those page sections, update the matching frontmatter entry (anchors must equal heading ids;
  answers/abstracts must match visible content).
- `page_features:` — the feature-key system below.
- `tags:` — blog-post taxonomy only (exported to the RSS feed). Never put a feature key here.

## Page features (per-page JS/CSS)

Frontmatter `page_features:` determines which JS/CSS gets included and run for each page (wired
in [`overrides/main.html`](../overrides/main.html)):

```yaml
---
title: "My page"
page_features:
  - feature1
  - feature2
---
```

Each feature key expects a specific HTML structure. **If you copy a visual pattern from another
page, copy its feature keys too.** These are the keys currently used:

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
      <div class="splide__list" markdown>
        <div class="splide__slide" markdown>
          <div class="carousel-cell-content" markdown>
          ...
          </div>
        </div>
        ...
      </div>
    </div>
  </div>
  ```

- `lazyvideo`: the page has below-the-fold videos (`<video class="lazy-video">`, the default
  video pattern below). Loads [`lazy-video.js`](../docs/javascripts/lazy-video.js), which plays
  each video only while it is on screen and never downloads the hidden theme variant.

- `scrolltoversion`: releases pages only — auto-scrolls to the `## X.Y.0` heading of the version
  being viewed. Loads
  [`releases-scroll-to-version.js`](../docs/javascripts/releases-scroll-to-version.js).

- `leadform`: the page has the enterprise lead form (a `<form class="lead-form">`, only
  [`support/index.md`](../docs/support/index.md)). Loads
  [`lead-form.js`](../docs/javascripts/lead-form.js), which submits to the leads endpoint and
  redirects to `/support/thanks/`. The field names are the endpoint's contract — changing them
  requires changing the backend too (the `CreateLead` function in
  [openvidu-deployments-manager](https://github.com/OpenVidu/openvidu-deployments-manager)).

- `openviduregister`: the page embeds the `<openvidu-register>` Amplify sign-in web component
  (only [`account.md`](../docs/account.md)). Loads the ~4.4 MB `openvidu-register.js` bundle plus
  `openvidu-register.css` and `amplify.css` — never load these site-wide. On every other page the
  header account button is a static "OpenVidu Pro account" link to `/account/`
  ([`partials/header.html`](../overrides/partials/header.html)); only the account page
  itself, where the bundle runs, relabels it.

- `dropdown`: groups the page's top-level nav tab into a dropdown menu; read by
  [`overrides/partials/tabs.html`](../overrides/partials/tabs.html) from the nav item's
  page (or the first child of a nav group).

- `homestyles`: loads [`home.css`](../docs/stylesheets/home.css) (the landing and Meet landing
  pages only).

- `Meet` / `Platform`: load [`meet.css`](../docs/stylesheets/meet.css) /
  [`platform.css`](../docs/stylesheets/platform.css) (each on top of the shared
  [`product.css`](../docs/stylesheets/product.css) palette mapping) for product-specific styling. These are
  **not written per page**: they come from folder-level metadata —
  [`docs/meet/.meta.yml`](../docs/meet/.meta.yml) and [`docs/docs/.meta.yml`](../docs/docs/.meta.yml)
  each declare `page_features:` that the `meta` plugin (enabled in `mkdocs.yml`) merges into
  every page of the folder. A new page under `docs/meet/` or `docs/docs/` gets its product key
  automatically.

The `page_features:`↔HTML contract is checked by `ovweb lint` (a page whose content carries
glightbox/feature-cards/carousel/lazy-video markup must declare the matching feature key) — see
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
- **Leave a blank line before an image that follows text**, above all inside a numbered step:
  without it the image is a lazy continuation of that paragraph, and inside a list item it
  renders inline at the end of the sentence instead of as its own centred block.
- **`.round-corners`** on every screen capture, photo and video — the one rounding class.
  Logos, icons, transparent art and SVG diagrams stay square: a mark is not a picture, and a
  transparent image has no corner to round.
- **`.control-height`** caps an image at half the viewport. Use it when a capture is 4:3 or
  taller *and* wide enough to fill the reading column (~700px), which is when it would
  otherwise run most of a screen tall. A 16:9 capture never needs it — its width already
  governs its height. **Never give it `width=`/`height=`** — see the dimensions rule below.
- **`.skip-gallery`** keeps an image out of the lightbox: logos, product marks and inline
  icons, which have nothing to enlarge.
- **`width=`/`height=` are the source's real pixel dimensions**, and they reserve the image's
  box so text below does not reflow while it loads (measured: they take `/about-us/` from
  0.048 CLS to 0.010). They also make the width *definite*, so a CSS `max-height` on the same
  image clamps the two axes independently and **stretches** it — `height: auto` and
  `aspect-ratio` cannot undo that. Constrain such an image on the width axis instead (as
  `.md-typeset .about-us-img` does), or leave the attributes off.
- **Full-width screenshots are 1920px wide.** The widest a content image is ever displayed is
  ~1040 CSS px, so 1920 keeps it sharp on a 2x display; anything wider than 1920 is resized
  down to it. Images displayed small (portraits, device frames) are exported at twice their
  display size instead. Resize sources **before** committing them — the `optimize` plugin
  recompresses but never resizes, so oversized sources ship oversized.
- **Screenshots are PNG, and every image goes through the same pipeline.** No per-image
  formats, no `optimize_exclude` entries. The publish build reduces each PNG to a 256-colour
  palette with `pngquant` (`optimize_png_speed: 1`, its best search effort), which is a real
  loss on photographic content — measured 36–38 dB PSNR on the captures that contain video
  thumbnails, against 42–49 dB on flat UI, diagrams and charts. That is the accepted cost of
  one uniform pipeline; the palette is capped at 256 colours by the PNG format itself, so
  there is no setting that removes it.

### Icons

Material's bundled sets (`:material-…:`, `:simple-…:`, `:octicons-…:`, `:fontawesome-…:`) cover
most needs. Site-specific icons live in [`overrides/.icons/custom/`](../overrides/.icons/custom) and
are addressed by file name — `multiplatform.svg` → `:custom-multiplatform:`. Both kinds take
attr_list classes: `:custom-multiplatform:{ .feature-icon }`.

What a file in `.icons/custom/` must look like:

- One `<svg>` element and nothing else. The file is inlined **verbatim** into every page that uses
  it, so an XML declaration, a DOCTYPE or a draw.io `content=` blob would ship into the HTML.
- No `fill` on the paths — `.md-typeset .twemoji svg` sets `fill: currentcolor`, so the icon takes
  the surrounding text color in both palettes with no per-palette CSS.
- Nested `<svg>` children flattened into `<g transform="translate(…) scale(…)">`: the theme's
  `.md-typeset .twemoji svg` width rule matches nested viewports too and would resize each one.
- A non-square `viewBox` is fine — the glyph is letterboxed inside the square icon slot.

Never fake an icon with an `<img>`: an image cannot inherit `currentcolor` (it needs one `filter`
per palette to be recolored), and sizing it in `em` inside the icon span resolves `--md-icon-size`
against the image's own font size instead of the span's.

### Videos

Two canonical patterns — nothing else. `<video>` never takes `defer`, `async` or `loading`
(those attributes do not exist for videos and silently do nothing).

**Below the fold (the default).** No `autoplay`; the video downloads and plays only when
scrolled into view. Requires the `lazyvideo` page tag:

```html
<a class="glightbox" href="/assets/videos/x-dark.mp4" data-type="video" data-gallery="dark"><video class="round-corners lazy-video" src="/assets/videos/x-dark.mp4#only-dark" preload="none" muted playsinline loop></video></a>
<a class="glightbox" href="/assets/videos/x-light.mp4" data-type="video" data-gallery="light"><video class="round-corners lazy-video" src="/assets/videos/x-light.mp4#only-light" preload="none" muted playsinline loop></video></a>
```

**Above the fold (showcase heroes only).** `autoplay` is allowed, but the inline `src` must be a
small downscaled `-preview.mp4` with a `poster`; the full-size file appears only in the lightbox
`href` (see `docs/meet/index.md` for the reference). Encode the preview at **half to two-thirds
the original's width, 30 fps, ~0.8–1.2 Mbps, no audio track** — enough for UI text to stay
legible, an order of magnitude under the original:

```bash
ffmpeg -i full.mp4 -vf "scale=1280:720:flags=lanczos,setsar=1" -r 30 \
  -c:v libx264 -preset slower -profile:v high -pix_fmt yuv420p \
  -b:v 1000k -pass 1 -an -f mp4 /dev/null
ffmpeg -i full.mp4 -vf "scale=1280:720:flags=lanczos,setsar=1" -r 30 \
  -c:v libx264 -preset slower -profile:v high -pix_fmt yuv420p \
  -b:v 1000k -pass 2 -an -movflags +faststart full-preview.mp4
```

```html
<a class="glightbox" href="/assets/videos/full.mp4" data-type="video"><video class="round-corners" src="/assets/videos/full-preview.mp4" poster="/assets/videos/full-poster.jpg" muted playsinline autoplay loop></video></a>
```

Rules for both patterns:

> - Theme-variant videos carry the `#only-dark`/`#only-light` suffix in the `src` attribute (in
>   pairs), **never** in the `href` of the `<a>` parent, and declare `data-gallery="dark"` /
>   `data-gallery="light"` to mark which variant they are (see the lightbox below). A video
>   without theme variants needs no `data-gallery` at all.
> - Each HTML `<a>` element is a **one-liner**. There are some strange behaviors when it is not.

### The lightbox

Every image and video on a page shares **one** gallery, so the arrows walk the whole page.
[`glightbox-gallery.js`](../docs/javascripts/glightbox-gallery.js) is loaded site-wide and owns
the only [GLightbox](https://biati-digital.github.io/glightbox/) instance; nothing needs a page
feature key. What each side controls:

- **mkdocs.yml** (`glightbox:`) configures the image slides — width, effects, `zoomable`, the
  classes that opt out. The plugin computes it, the hook hands it over as `glightboxOptions`
  and the script builds its instance on top, so that block stays the one place to change them.
- **The script** adds what that configuration cannot express: the Plyr player options and the
  wider video frame.
- **The palette** decides membership. A themed pair contributes only the variant currently on
  screen, and the gallery is rebuilt when the palette changes — so `data-gallery="dark"` /
  `"light"` is a *marker*, not a gallery name (the `#only-*` suffix serves as a fallback).
  A per-page gallery name would only split the page in two; there is none.
- **Repeats collapse.** The same asset used more than once on a page — including the slides
  Splide clones to loop a carousel — is one entry, and a click on any copy opens it.
- **`skip-gallery`** on an image keeps it out of the lightbox altogether.

## Theme overrides

Material theme customization lives in [`overrides/`](../overrides) (`custom_dir`):

- `main.html` extends the Material base template with Jinja blocks (`extrahead`, `scripts`,
  `styles`, `outdated`...).
- `home.html` extends `main.html` (the landing page template).
- `partials/` adds or overrides partials: `header.html`, `footer.html`, `tabs.html`,
  `json-ld.html`, `og.html`.
- `sitemap.xml` is MkDocs' own template (Material ships none) with one added clause: a page
  declaring `robots: noindex` is left out, so the sitemap never submits a URL that then
  refuses indexing. Re-copy it from `mkdocs/templates/sitemap.xml` on a MkDocs bump.

Site-wide changes go here — follow the "before/after" comment markers inside the blocks.

## HTML-in-Markdown

Layout uses unsemantic-grid classes (`grid-50`, `grid-90`, `tablet-grid-...`). Material features in
use: admonitions, `???` collapsible details, content tabs, attr_list (`{ .class }`,
`{:target="_blank"}`). Links inside raw HTML follow their own rule — see
[link rules](link-rules.md), rule 3.

To put Markdown inside a styled element, pick the mechanism by **where the element sits**:

| Where | Write | Why |
|---|---|---|
| Top level of a page | `<div class="x" markdown>` | `md_in_html`, the usual case |
| Inside a content tab, an admonition or a list item — including a snippet that is *included* at an indent | `/// html \| div.x` | `md_in_html` only honours the attribute at the top level of a document (see below) |

**`md_in_html` does not work at depth.** Its preprocessor runs before the block parsers, so once
content sits inside a tab or an admonition the attribute is never read: it is passed through into
the page as a literal `markdown=""`, the element is treated as inline HTML, and the Markdown inside
loses its paragraph. `mkdocs build --strict` reports nothing. This bites snippets hardest, because
[`tutorials/application-client/tabs.md`](../shared/tutorials/application-client/tabs.md) includes
the client snippets indented inside tabs while the tutorial pages include the same files at the top
level — no attribute is right in both places, so those snippets use `/// html` blocks
(`pymdownx.blocks.html`), which the block parser handles at any depth.

**Block or span.** Both mechanisms default to block mode, which wraps loose text and images in a
`<p>`:

- **block** (`markdown`, or `/// html | div.x`) — the element holds paragraphs, lists, tables,
  headings or nested wrappers, or a standalone image that should sit in its own paragraph. If the
  element is styled as a flex/grid row, the CSS has to account for that `<p>` — as
  `.provider-chip p` does.
- **span** (`markdown="span"`) — the element is a layout row whose direct children must be the
  links or images themselves: `.md-social`, a `grid cards` row of links, an image cell that had no
  `<p>`. Block mode there inserts a paragraph and shifts the layout. A standalone image in such a
  cell is still centred: the centring rule in `extra.css` matches a grid cell whose own child is
  the image, not just a paragraph's.

Check the rendered HTML when in doubt: the mode is right when the element's children match what
they were before the conversion.
