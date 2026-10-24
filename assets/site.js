// Theme toggle. The inline script in <head> applies a saved choice before paint;
// with no saved choice the site follows the system setting.
(function () {
  var button = document.querySelector(".theme-toggle");
  if (!button) return;

  var root = document.documentElement;
  var systemDark = window.matchMedia("(prefers-color-scheme: dark)");

  function current() {
    return root.getAttribute("data-theme") || (systemDark.matches ? "dark" : "light");
  }

  function updateLabel() {
    button.setAttribute(
      "aria-label",
      current() === "dark" ? "Switch to light theme" : "Switch to dark theme"
    );
  }

  button.addEventListener("click", function () {
    var next = current() === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try {
      localStorage.setItem("theme", next);
    } catch (e) {}
    updateLabel();
  });

  if (systemDark.addEventListener) systemDark.addEventListener("change", updateLabel);
  updateLabel();
})();
