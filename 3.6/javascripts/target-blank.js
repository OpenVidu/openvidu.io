/**
 * Automatically add target="_blank" to external links
 * Finds all elements with class "external-link" and adds target="_blank" to their nearest <a> parent
 */
function addTargetBlankToExternalLinks() {
  // Find all elements with class "external-link"
  const externalLinkElements = document.querySelectorAll(".external-link");
  externalLinkElements.forEach(function (element) {
    // Find the nearest <a> parent
    const linkParent = element.closest("a");
    if (linkParent) {
      // Add target="_blank" attribute to open in new tab
      linkParent.setAttribute("target", "_blank");
    }
  });
}

// Check if DOM is already loaded
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", addTargetBlankToExternalLinks);
} else {
  addTargetBlankToExternalLinks();
}
