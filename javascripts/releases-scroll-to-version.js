/**
 * On a versioned Releases page (/<version>/meet/releases/ or /<version>/docs/releases/),
 * jump to the release-notes section that matches the documentation version being viewed.
 *
 * The Releases page contains the notes for every version (the latest page is copied into
 * every version folder), so a user browsing an older version (e.g. 3.5.0) lands directly on
 * its "## 3.5.0" section (anchor "#350") instead of at the top of the full list.
 *
 * No-ops when:
 *  - the URL already has an explicit anchor (respect deep links and cross-page links such
 *    as the Meet <-> Platform "#380" references),
 *  - the version segment has no matching section (e.g. the "latest" alias) -> stays at the
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

  // Convert the version into the heading anchor id, mirroring the toc slugify
  // (non-word characters are stripped, lowercased): "3.5.0" -> "350"
  const anchorId = match[1].replace(/[^\w-]/g, "").toLowerCase();
  if (!anchorId) {
    return;
  }

  // Only jump when the page actually contains that version's section. The "latest" alias
  // has no matching section, so it keeps the newest notes at the top.
  if (!document.getElementById(anchorId)) {
    return;
  }

  // Use the native anchor navigation so the sticky-header offset matches what clicking a
  // table-of-contents link does
  window.location.hash = anchorId;
}

// Check if DOM is already loaded
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", scrollToViewedVersionReleaseNotes);
} else {
  scrollToViewedVersionReleaseNotes();
}
