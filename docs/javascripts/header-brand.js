(function () {
  function relativeSiteRoot() {
    var parts = location.pathname.split("/").filter(function (x) {
      return x && x !== "index.html";
    });
    return parts.length ? "../".repeat(parts.length) : "./";
  }

  function run() {
    var home = relativeSiteRoot();
    var logos = document.querySelectorAll('a[data-md-component="logo"]');
    var first = logos[0];
    if (first) {
      var h = first.getAttribute("href");
      if (!h || h === "" || h === "#") {
        logos.forEach(function (logo) {
          logo.setAttribute("href", home);
        });
      } else {
        home = first.getAttribute("href");
      }
    }

    var topic = document.querySelector(
      ".md-header__title .md-header__ellipsis > .md-header__topic:first-child .md-ellipsis"
    );
    if (!topic || topic.querySelector("a.pr-header-brand")) return;
    var name = topic.textContent.trim();
    if (!name) return;
    topic.innerHTML =
      '<a href="' +
      home +
      '" class="pr-header-brand" title="Home" aria-label="Home">' +
      name +
      "</a>";
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", run);
  } else {
    run();
  }
})();
