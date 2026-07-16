/**
 * On a versioned Releases page (/<version>/meet/releases/ or /<version>/docs/releases/),
 * jump to the release-notes section that matches the documentation version being viewed.
 *
 * Documentation versions are grouped by MINOR release (folders like "3.4"), while the
 * Releases page keeps one section per exact patch release ("## 3.4.0", "## 3.4.1", ...).
 * The page contains the notes for every version (the latest page is copied into every
 * version folder), so a user browsing e.g. /3.4/meet/releases/ lands directly on the
 * newest section of the 3.4 minor instead of at the top of the full list.
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
  const version = match[1];

  let anchorId = null;

  if (/^\d+\.\d+$/.test(version)) {
    // Minor-grouped version folder ("3.4"): scroll to the FIRST release-notes heading of
    // that minor in document order (the page lists newest first, so that is the newest
    // patch, e.g. "## 3.4.1"). Match against the headings' TEXT ("3.4."), not their
    // slugified ids: id prefixes are ambiguous ("31..." matches both 3.1.0 and a future
    // 3.10.0), while the dotted text prefix is not.
    const minorPrefix = version + ".";
    const headings = document.querySelectorAll("article h2[id]");
    for (const heading of headings) {
      if (heading.textContent.trim().indexOf(minorPrefix) === 0) {
        anchorId = heading.id;
        break;
      }
    }
  } else {
    // Exact version segment (defensive; no such folders remain after the minor-grouping
    // migration). Convert it into the heading anchor id, mirroring the toc slugify
    // (non-word characters are stripped, lowercased): "3.5.0" -> "350"
    const slug = version.replace(/[^\w-]/g, "").toLowerCase();
    if (slug && document.getElementById(slug)) {
      anchorId = slug;
    }
  }

  // Only jump when the page actually contains a matching section. The "latest" alias has
  // no matching section, so it keeps the newest notes at the top.
  if (!anchorId) {
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
