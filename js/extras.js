/* Serenia: Simplex showcase interactions and the nearby places toggle */
document.addEventListener('DOMContentLoaded', function () {
  var fine = window.matchMedia && window.matchMedia('(pointer:fine)').matches;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Simplex cards: spotlight + gentle tilt, keyboard activation */
  Array.prototype.forEach.call(document.querySelectorAll('.sx-card'), function (card) {
    card.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); card.click(); }
    });
    if (!fine || reduce) return;
    card.addEventListener('pointermove', function (e) {
      var r = card.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      card.style.setProperty('--mx', (x * 100) + '%'); card.style.setProperty('--my', (y * 100) + '%');
      card.style.setProperty('--ry', ((x - .5) * 7) + 'deg'); card.style.setProperty('--rx', ((.5 - y) * 7) + 'deg');
    });
    card.addEventListener('pointerleave', function () { card.style.setProperty('--rx', '0deg'); card.style.setProperty('--ry', '0deg'); });
  });

  /* Nearby places: View more / View less */
  var near = document.querySelector('.near'), t = near && near.querySelector('.toggle');
  if (t) {
    t.addEventListener('click', function () {
      var open = near.classList.toggle('open');
      t.textContent = open ? 'View less' : 'View more';
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
});
