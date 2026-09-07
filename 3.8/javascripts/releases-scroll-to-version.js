/**
 * On a versioned Releases page (/<version>/meet/releases/ or /<version>/docs/releases/),
 * jump to the release-notes section of the documentation version being viewed.
 *
 * Documentation versions are grouped by MINOR release (folders like "3.4"), while the
 * Releases page keeps one section per patch release ("## 3.4.0", "## 3.5.0", ...). The full
 * page is copied into every version folder, so a user browsing e.g. /3.4/meet/releases/ is
 * taken to that minor's initial ".0" section ("## 3.4.0", heading id "340") instead of
 * landing at the top of the whole list.
 *
 * No-ops when:
 *  - the URL already has an explicit anchor (respect deep links and cross-page links such
 *    as the Meet <-> Platform "#380" references),
 *  - the page has no section for that version (e.g. the "latest" alias) -> stays at the
 *    top, showing the newest notes first.
 */
function scrollToViewedVersionReleaseNotes() {
  // Respect an anchor already present in the URL
  if (window.location.hash) {
    return;
  }

  // Match "/<version>/<meet|docs>/releases/" and capture the version segment
  const match = window.location.pathname.match(
    /^\/([^/]+)\/(?:meet|docs)\/releases\/?$/
  );
  if (!match) {
    return;
  }

  // Target the ".0" patch of the viewed minor version. The heading id mirrors the toc
  // slugify (non-word characters stripped, lowercased): "3.4" -> "## 3.4.0" -> id "340".
  const anchorId = (match[1] + ".0").replace(/[^\w-]/g, "").toLowerCase();

  // Only jump when the page actually contains that section (e.g. the "latest" alias has
  // none, so it keeps the newest notes at the top).
  if (!document.getElementById(anchorId)) {
    return;
  }

  // Use native anchor navigation so the sticky-header offset matches a toc-link click
  window.location.hash = anchorId;
}

// Check if DOM is already loaded
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", scrollToViewedVersionReleaseNotes);
} else {
  scrollToViewedVersionReleaseNotes();
}
