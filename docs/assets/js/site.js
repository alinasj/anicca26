// Home page logo: draw on load, replay the drawing when hovered or tapped.
(function () {
  var art = document.querySelector(".logo-art");
  var logo = art && art.querySelector(".logo-anim");
  if (!logo) return;
  var replaying = false;
  function play() {
    if (replaying) return;
    replaying = true;
    logo.classList.remove("play");
    void logo.getBoundingClientRect(); // restart the CSS animations
    logo.classList.add("play");
    setTimeout(function () { replaying = false; }, 3000);
  }
  logo.classList.add("play");
  art.addEventListener("mouseenter", play);
  art.addEventListener("click", play);
  art.setAttribute("role", "button");
  art.setAttribute("tabindex", "0");
  art.setAttribute("aria-label", "Replay the logo animation");
  art.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); play(); } });
})();
