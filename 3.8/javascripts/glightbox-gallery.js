// Owns the page's GLightbox instance.
//
// It is the only instance on the page: the plugin hands its mkdocs.yml configuration over as
// `glightboxOptions` instead of building an instance of its own (see mkdocs_hook.py), and this
// script adds the video player options that configuration cannot express.
//
// It also merges the galleries. `auto_themed` puts every themed image in a `dark` or a
// `light` gallery, so a page mixing themed and plain assets ends up with several disjoint
// ones — and the plain gallery leaks the hidden variant, because GLightbox skips gallery
// filtering altogether for an element without `data-gallery`. Here every asset joins one
// gallery per page — once, however many times the page repeats it — and the variant the current
// palette hides is kept out of the instance, so the lightbox holds exactly what the page shows.
// Rebuilt on a palette change.
document.addEventListener("DOMContentLoaded", () => {
  if (typeof GLightbox === "undefined") return;

  // Video slides only: image slides carry their size per anchor from the plugin config, but
  // the player and the wider video frame have no equivalent in mkdocs.yml. GLightbox merges
  // `plyr` deeply, so its own defaults (the Plyr asset URLs, the 16:9 ratio) survive.
  const videoOptions = {
    videosWidth: "1400px",
    plyr: {
      config: {
        controls: ["play", "play-large", "progress", "fullscreen"],
        settings: [],
        autoplay: true,
        playsinline: true,
        muted: true,
        volume: 0,
        seekTime: 1,
        hideControls: true,
        loop: { active: true },
        clickToPlay: true,
        disableContextMenu: true,
        resetOnEnd: true,
        keyboard: { focused: false, global: false },
        displayDuration: false,
      },
    },
  };

  // What the mkdocs-glightbox plugin computed from the `glightbox:` block in mkdocs.yml, handed
  // over by the hook (publish-tool/mkdocs_hook.py) in place of the instance it would build itself.
  const pluginOptions = typeof glightboxOptions === "undefined" ? {} : glightboxOptions;

  // The URL identifies the picture: the same asset used twice on a page, and the slides Splide
  // clones to loop a carousel, are the same picture and belong in the gallery once.
  const assetOf = (anchor) => {
    const media = anchor.querySelector("img, video");
    return media ? media.src : anchor.href;
  };

  const themeVariantOf = (anchor) => {
    const gallery = anchor.getAttribute("data-gallery");
    if (gallery === "dark" || gallery === "light") return gallery;
    const media = anchor.querySelector("img, video");
    const source = (media && media.getAttribute("src")) || anchor.getAttribute("href") || "";
    if (source.includes("#only-dark")) return "dark";
    if (source.includes("#only-light")) return "light";
    return "any";
  };

  const primaries = new Map();
  document.querySelectorAll("a.glightbox").forEach((anchor) => {
    anchor.dataset.themeVariant = themeVariantOf(anchor);
    anchor.setAttribute("data-gallery", "page");
    const primary = primaries.get(assetOf(anchor));
    if (!primary) {
      primaries.set(assetOf(anchor), anchor);
      return;
    }
    // A repeat stays out of the gallery and hands its clicks to the copy that is in it, which
    // shows the same picture. Both copies of a themed pair keep their own entry: their URLs
    // differ by the `#only-*` suffix.
    anchor.dataset.galleryRepeat = "";
    anchor.addEventListener("click", (event) => {
      event.preventDefault();
      primary.click();
    });
  });

  let instance = null;
  let rebuildWhenClosed = false;

  const build = () => {
    const hidden = document.body.dataset.mdColorScheme === "slate" ? "light" : "dark";
    if (instance) instance.destroy();
    instance = GLightbox({
      ...pluginOptions,
      ...videoOptions,
      selector: `a.glightbox:not([data-theme-variant="${hidden}"]):not([data-gallery-repeat])`,
    });
    instance.on("close", () => {
      if (!rebuildWhenClosed) return;
      rebuildWhenClosed = false;
      setTimeout(build);
    });
  };

  build();

  new MutationObserver(() => {
    if (instance && instance.lightboxOpen) rebuildWhenClosed = true;
    else build();
  }).observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });
});
