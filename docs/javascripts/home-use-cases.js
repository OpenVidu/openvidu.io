/* Landing page, "What are you building?": each pill selects the answer panel with the same
   index. Without JS the first panel is visible and the others carry `hidden` in the HTML. */
(function () {
  var root = document.querySelector(".ov-cases");
  if (!root) return;
  var buttons = Array.prototype.slice.call(root.querySelectorAll(".ov-case"));
  var panels = Array.prototype.slice.call(root.querySelectorAll(".ov-pick"));

  function select(index) {
    buttons.forEach(function (button, i) {
      button.setAttribute("aria-pressed", i === index ? "true" : "false");
    });
    panels.forEach(function (panel, i) {
      panel.hidden = i !== index;
    });
  }

  buttons.forEach(function (button, i) {
    button.addEventListener("click", function () {
      select(i);
    });
  });
  select(0);
})();
