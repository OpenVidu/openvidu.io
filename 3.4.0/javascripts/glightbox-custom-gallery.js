const COLOR_SCHEM_ATTR = "data-md-color-scheme";
let GLOBAL_GLIGHTBOX;

const resetGlightbox = () => {
  if (GLOBAL_GLIGHTBOX) {
    GLOBAL_GLIGHTBOX.destroy();
    console.debug("GLightbox reset");
  } else {
    console.debug("GLightbox initialized");
  }
  GLOBAL_GLIGHTBOX = GLightbox({
    touchNavigation: true,
    loop: false,
    autoplayVideos: true,
    zoomable: false,
    draggable: true,
    preload: true,
    videosWidth: "1400px",
    height: "auto",
    closeEffect: "fade",
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
  });
};

const clearSlides = () => {
  const body = document.querySelector("body");
  const colorScheme = body.getAttribute(COLOR_SCHEM_ATTR);
  const lightboxElements = GLOBAL_GLIGHTBOX.elements;
  // Iterate backwards to avoid index shifting issues when removing elements
  for (let i = lightboxElements.length - 1; i >= 0; i--) {
    const element = lightboxElements[i];
    const mediaElementSrc = element.node.firstChild.src;
    if (
      !mediaElementSrc ||
      (!mediaElementSrc.includes("#only-dark") &&
        !mediaElementSrc.includes("#only-light"))
    ) {
      continue;
    } else {
      if (
        (colorScheme === "slate" && mediaElementSrc.includes("#only-light")) ||
        (colorScheme !== "slate" && mediaElementSrc.includes("#only-dark"))
      ) {
        // Remove the slide
        const slideIndex = Number(element.index);
        console.debug(
          `Removing slide ${slideIndex} with src ${mediaElementSrc} because it does not match the current color scheme (${colorScheme})`
        );
        GLOBAL_GLIGHTBOX.removeSlide(slideIndex);
      }
    }
  }
};

// Use MutationObserver API to detect changes in the attribute COLOR_SCHEM_ATTR of the DOM body
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (
      mutation.type === "attributes" &&
      mutation.attributeName === COLOR_SCHEM_ATTR
    ) {
      const newColorScheme = mutation.target.getAttribute(COLOR_SCHEM_ATTR);
      console.debug(`Color scheme changed to ${newColorScheme}`);
      resetGlightbox();
      clearSlides();
    }
  });
});
const body = document.querySelector("body");
observer.observe(body, {
  attributes: true,
  attributeFilter: [COLOR_SCHEM_ATTR],
});

console.debug("Gallery setup");
