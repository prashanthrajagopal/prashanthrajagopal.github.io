(function () {
  function init() {
    var chips = document.querySelectorAll(".pr-filter-chip");
    var rows = document.querySelectorAll(".blog-post-row[data-tags]");
    if (!chips.length || !rows.length) return;

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        chips.forEach(function (c) {
          c.classList.remove("active");
        });
        chip.classList.add("active");
        var f = chip.getAttribute("data-filter") || "all";
        rows.forEach(function (row) {
          var tags = (row.getAttribute("data-tags") || "").toLowerCase();
          if (f === "all") {
            row.style.display = "";
          } else {
            row.style.display = tags.indexOf(f) !== -1 ? "" : "none";
          }
        });
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
