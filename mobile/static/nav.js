const path = document.getElementById("routePath");

function preparePath() {
  const length = path.getTotalLength();
  path.style.strokeDasharray = length;
  path.style.strokeDashoffset = length;
  path.style.transition = "none";
}

function play(durationMs = 1300) {
  path.style.transition = `stroke-dashoffset ${durationMs}ms ease-in-out`;
  requestAnimationFrame(() => {
    path.style.strokeDashoffset = "0";
  });
}

preparePath();
play(1400);
