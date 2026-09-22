// Plays .lazy-video videos only while on screen. Videos use preload="none",
// so nothing downloads until shortly before the video scrolls into view;
// display:none theme variants never intersect and never download.
document.addEventListener("DOMContentLoaded", () => {
  const videos = document.querySelectorAll("video.lazy-video");
  if (videos.length === 0) return;
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const video = entry.target;
        if (entry.isIntersecting) {
          video.play().catch(() => {});
        } else if (!video.paused) {
          video.pause();
        }
      });
    },
    // Start loading half a viewport before the video becomes visible
    { rootMargin: "50% 0px" }
  );
  videos.forEach((video) => observer.observe(video));
});
