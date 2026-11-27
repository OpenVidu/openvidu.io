// Use-cases carousel (page_features: setupcarousel). Mounts a looping Splide on every `.splide`
// of the page; main.html loads splide.min.js before this file.
function setupCarousel() {
  document.querySelectorAll(".splide").forEach((element) => {
    new Splide(element, {
      type: "loop",
      autoWidth: true,
      autoHeight: true,
      focus: "center",
      gap: "4%",
    }).mount();
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", setupCarousel);
} else {
  setupCarousel();
}
