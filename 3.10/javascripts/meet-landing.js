(function () {
  var root = document.querySelector("[data-ovp-rotator]");
  if (!root) return;
  var points = Array.prototype.slice.call(root.querySelectorAll("[data-ovp-point]"));
  var slides = Array.prototype.slice.call(root.querySelectorAll("[data-ovp-slide]"));
  var still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var current = 0;
  var timer = null;
  function show(index) {
    current = index;
    points.forEach(function (point, i) {
      point.classList.toggle("is-active", i === index);
      point.querySelector("button").setAttribute("aria-pressed", i === index ? "true" : "false");
    });
    slides.forEach(function (slide, i) {
      slide.classList.toggle("is-active", i === index);
    });
  }
  function stop() {
    clearInterval(timer);
  }
  function start() {
    stop();
    if (still) return;
    timer = setInterval(function () {
      show((current + 1) % slides.length);
    }, 3000);
  }
  points.forEach(function (point, i) {
    point.querySelector("button").addEventListener("click", function () {
      show(i);
      start();
    });
  });
  var section = root.closest("section") || root;
  section.addEventListener("mouseenter", stop);
  section.addEventListener("mouseleave", start);
  show(0);
  start();
})();
