// Open external http(s) links in a new tab.
function setExternalLinkTargets(root) {
  const scope = root || document;
  for (const link of scope.querySelectorAll("a[href]")) {
    if (!link.href || link.hasAttribute("data-external-link-processed")) {
      continue;
    }

    try {
      const url = new URL(link.href, location.href);
      if (url.protocol !== "http:" && url.protocol !== "https:") {
        continue;
      }
      if (url.host === location.host) {
        continue;
      }

      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.setAttribute("data-external-link-processed", "");
    } catch (_) {
      // Ignore invalid URLs.
    }
  }
}

if (typeof document$ !== "undefined") {
  document$.subscribe(() => setExternalLinkTargets(document));
} else {
  document.addEventListener("DOMContentLoaded", () =>
    setExternalLinkTargets(document)
  );
}
