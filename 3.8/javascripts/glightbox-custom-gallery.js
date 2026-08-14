// Re-initializes GLightbox with the video player options (autoplaying plyr
// slides), which the mkdocs-glightbox plugin cannot express in its config.
// Runs at DOMContentLoaded, after the plugin's #init-glightbox script, and
// replaces the instance it created so each thumbnail keeps a single binding.
document.addEventListener("DOMContentLoaded", () => {
  if (typeof lightbox !== "undefined") {
    lightbox.destroy();
  }
  GLightbox({
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
});
