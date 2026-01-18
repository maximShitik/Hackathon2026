const path = document.getElementById("routePath");
const flow = document.getElementById("routeFlow");
const outline = document.getElementById("routeOutline");


function setRouteD(d) {
  outline.setAttribute("d", d);
  main.setAttribute("d", d);
  flow.setAttribute("d", d);
}


function preparePath() {
  const length = main.getTotalLength();
  [outline, main, flow].forEach((p) => {
    p.style.strokeDasharray = length;
    p.style.strokeDashoffset = length;
    p.style.transition = "none";
  });
}

function play(durationMs = 1300) {
   requestAnimationFrame(() => {
    [outline, main, flow].forEach((p) => {
      p.style.transition = `stroke-dashoffset ${durationMs}ms ease-in-out`;
      p.style.strokeDashoffset = "0";
    });
  });
}

preparePath();
play(1400);
