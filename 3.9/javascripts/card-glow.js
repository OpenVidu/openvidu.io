// Card glow (page_features: setupcardglow). Each card of a `.feature-cards .grid.cards` grid
// tracks the pointer through the `--start` angle that home.css feeds its conic-gradient border.
function setupCardGlow() {
  const cards = document.querySelectorAll(".feature-cards .grid.cards > ul > li");
  cards.forEach((card) => {
    card.addEventListener("mousemove", (event) => {
      const rect = card.getBoundingClientRect();
      const x = event.clientX - rect.left - rect.width / 2;
      const y = event.clientY - rect.top - rect.height / 2;
      const angle = (Math.atan2(y, x) * (180 / Math.PI) + 360) % 360;
      card.style.setProperty("--start", angle + 60);
    });
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", setupCardGlow);
} else {
  setupCardGlow();
}
