// Home page logo: the drawing plays once per visit via CSS (.logo-anim.play);
// after that only the dots keep pulsing. No replay on hover or scroll.

// Support page: hearts in the logo colors float up out of the
// coffee cup, sway and fade. Hovering the cup or the button sends up more.
(function () {
  var layer = document.getElementById("steam");
  if (!layer) return;
  var NS = "http://www.w3.org/2000/svg";
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  var colors = ["#F7A21B", "#E8661F", "#D4AF37", "#B8452A"];
  var HEART = "M0 3.2C-6 -1.6 -4 -7.4 0 -4.1C4 -7.4 6 -1.6 0 3.2Z";   // about 12 units wide
  var items = [];

  function spawn(age) {
    var heart = true;                              // hearts only for now
    var el = document.createElementNS(NS, heart ? "path" : "circle");
    if (heart) el.setAttribute("d", HEART); else el.setAttribute("r", "3");
    el.setAttribute("fill", colors[(Math.random() * colors.length) | 0]);
    layer.appendChild(el);
    items.push({
      el: el, heart: heart, age: age || 0,
      life: 2600 + Math.random() * 1600,
      x0: 78 + Math.random() * 48, y0: 70,
      rise: 44 + Math.random() * 16,
      sway: 4 + Math.random() * 7, freq: 1 + Math.random() * 1.5, phase: Math.random() * 6.3,
      s0: 0.5, s1: 1.2 + Math.random() * 0.6,
      tilt: (Math.random() - 0.5) * 30
    });
  }

  function draw(p) {
    var t = Math.min(p.age / p.life, 1);
    var ease = 1 - Math.pow(1 - t, 1.8);
    var x = p.x0 + Math.sin(p.phase + t * p.freq * 3.14) * p.sway;
    var y = p.y0 - p.rise * ease;
    var sc = p.s0 + (p.s1 - p.s0) * Math.min(t * 2.2, 1);
    var a = t < 0.12 ? t / 0.12 : t > 0.6 ? 1 - (t - 0.6) / 0.4 : 1;
    var rot = p.heart ? p.tilt * Math.sin(p.phase + t * 4) : 0;
    p.el.setAttribute("transform", "translate(" + x.toFixed(2) + " " + y.toFixed(2) + ") rotate(" + rot.toFixed(1) + ") scale(" + sc.toFixed(3) + ")");
    p.el.setAttribute("opacity", (a * 0.95).toFixed(3));
  }

  if (reduce) {                                   // a still handful of hearts above the cup
    for (var i = 0; i < 10; i++) { spawn(500 + i * 220); }
    items.forEach(draw);
    return;
  }

  var boost = false;
  [document.getElementById("coffee-btn"), layer.ownerSVGElement].forEach(function (el) {
    if (!el) return;
    el.addEventListener("mouseenter", function () { boost = true; });
    el.addEventListener("mouseleave", function () { boost = false; });
    el.addEventListener("touchstart", function () { boost = true; setTimeout(function () { boost = false; }, 1500); }, { passive: true });
  });

  for (var k = 0; k < 10; k++) spawn(k * 280);    // start mid-flow
  var last = performance.now(), since = 0;
  function tick(now) {
    var dt = Math.min(now - last, 60); last = now; since += dt;
    var every = boost ? 90 : 260;
    while (since > every) { since -= every; spawn(0); }
    for (var i = items.length - 1; i >= 0; i--) {
      var p = items[i]; p.age += dt;
      if (p.age >= p.life) { p.el.remove(); items.splice(i, 1); continue; }
      draw(p);
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
})();
