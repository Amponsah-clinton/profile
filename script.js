(function () {
  "use strict";

  var MOBILE_BREAKPOINT = "(max-width: 800px)";
  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Footer date — month and year */
  var lastUpdated = document.getElementById("last-updated");
  if (lastUpdated) {
    var now = new Date();
    lastUpdated.dateTime = now.toISOString().slice(0, 7);
    lastUpdated.textContent = now.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long"
    });
  }

  /* Portrait fallback */
  var portrait = document.getElementById("portrait");
  if (portrait) {
    var img = portrait.querySelector("img");
    var showPlaceholder = function () {
      portrait.classList.add("portrait--placeholder");
    };

    if (!img) {
      showPlaceholder();
    } else {
      img.addEventListener("error", showPlaceholder);
      if (img.complete && img.naturalWidth === 0) {
        showPlaceholder();
      }
    }
  }

  /* Mobile sidebar toggle */
  var navToggle = document.querySelector(".nav-toggle");
  var sectionNav = document.getElementById("section-nav");
  var navLinks = document.querySelectorAll(".section-nav a");

  function closeMobileNav() {
    if (window.matchMedia(MOBILE_BREAKPOINT).matches && sectionNav) {
      sectionNav.classList.remove("is-open");
      if (navToggle) {
        navToggle.setAttribute("aria-expanded", "false");
      }
    }
  }

  navLinks.forEach(function (link) {
    link.addEventListener("click", closeMobileNav);
  });

  if (navToggle && sectionNav) {
    navToggle.addEventListener("click", function () {
      var expanded = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!expanded));
      sectionNav.classList.toggle("is-open", !expanded);
    });
  }

  if (prefersReducedMotion) {
    document.documentElement.style.scrollBehavior = "auto";
  }
})();
