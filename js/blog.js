/* Serenia blog: reading progress, table of contents, share, search and filters */
document.addEventListener('DOMContentLoaded', function () {
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Mobile menu */
  var tg = $('#navToggle'), mn = $('#mainNav');
  if (tg && mn) {
    tg.addEventListener('click', function () { tg.setAttribute('aria-expanded', mn.classList.toggle('open') ? 'true' : 'false'); });
  }

  /* Reading progress + back to top */
  var rp = $('#rp'), top = $('#toTop');
  function onScroll() {
    var h = document.documentElement.scrollHeight - window.innerHeight;
    if (rp) rp.style.width = (h > 0 ? Math.min(100, window.scrollY / h * 100) : 0) + '%';
    if (top) top.classList.toggle('show', window.scrollY > 700);
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  if (top) top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); });

  /* Toast + copy link */
  var toast = $('#toast'), tt;
  function say(msg) {
    if (!toast) return;
    toast.textContent = msg; toast.classList.add('show'); clearTimeout(tt);
    tt = setTimeout(function () { toast.classList.remove('show'); }, 2200);
  }
  $$('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var url = window.location.href.split('#')[0];
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(function () { say('Link copied'); }, function () { say('Copy failed'); });
      } else {
        var t = document.createElement('input'); t.value = url; document.body.appendChild(t); t.select();
        try { document.execCommand('copy'); say('Link copied'); } catch (e) { say('Copy failed'); }
        document.body.removeChild(t);
      }
    });
  });

  /* Table of contents: open on desktop, highlight the section being read */
  var toc = $('.toc');
  if (toc && window.innerWidth > 960) toc.setAttribute('open', '');
  var links = $$('.toc a');
  if (links.length && 'IntersectionObserver' in window) {
    var map = {};
    links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) {
          links.forEach(function (a) { a.classList.remove('on'); });
          var a = map[e.target.id]; if (a) a.classList.add('on');
        }
      });
    }, { rootMargin: '-90px 0px -65% 0px' });
    $$('.post-body h2[id]').forEach(function (h) { io.observe(h); });
  }

  /* Was this helpful? (stored only in this browser) */
  var hp = $('.helpful');
  if (hp) {
    var key = 'serenia_helpful_' + location.pathname;
    try { if (localStorage.getItem(key)) hp.classList.add('done'); } catch (e) {}
    $$('button', hp).forEach(function (b) {
      b.addEventListener('click', function () {
        try { localStorage.setItem(key, b.getAttribute('data-v')); } catch (e) {}
        hp.classList.add('done');
      });
    });
  }

  /* Hub: search + topic filter */
  var q = $('#q'), cards = $$('.gcard[data-title]'), chips = $$('.chips2 button'), empty = $('.empty'), count = $('.count');
  if (cards.length) {
    var tag = 'all';
    var apply = function () {
      var term = q ? q.value.trim().toLowerCase() : '', n = 0;
      cards.forEach(function (c) {
        var ok = (tag === 'all' || (c.getAttribute('data-tags') || '').split(',').indexOf(tag) > -1) &&
                 (!term || c.getAttribute('data-title').toLowerCase().indexOf(term) > -1);
        c.classList.toggle('hide', !ok); if (ok) n++;
      });
      if (empty) empty.classList.toggle('show', n === 0);
      if (count) count.textContent = n + (n === 1 ? ' guide' : ' guides');
    };
    if (q) q.addEventListener('input', apply);
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        chips.forEach(function (x) { x.classList.remove('on'); }); c.classList.add('on');
        tag = c.getAttribute('data-tag'); apply();
      });
    });
    apply();
  }

  /* Reveal on scroll */
  var rv = $$('.rv');
  if ('IntersectionObserver' in window && !reduce) {
    var ro = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); ro.unobserve(e.target); } });
    }, { threshold: .1 });
    rv.forEach(function (el) { ro.observe(el); });
  } else { rv.forEach(function (el) { el.classList.add('in'); }); }
});

/* Enquiry popup on blog pages (same behaviour as the landing page) */
document.addEventListener('DOMContentLoaded', function () {
  var overlay = document.getElementById('modalOverlay'), form = document.getElementById('modalForm');
  if (!overlay || !form) return;
  var cfg = window.SITE_CONFIG || {}, PHONE = cfg.PHONE_WHATSAPP || '917415322403', pendingWa = null;
  [['project', cfg.PROJECT_NAME], ['developer', cfg.DEFAULT_DEVELOPER_NAME], ['manager_name', cfg.DEFAULT_MANAGER_NAME], ['manager_email', cfg.DEFAULT_MANAGER_EMAIL]]
    .forEach(function (p) { if (p[1]) document.querySelectorAll('[name="' + p[0] + '"]').forEach(function (el) { el.defaultValue = el.value = p[1]; }); });
  var interest = document.getElementById('modal-interest');
  function openModal(plan, intent) {
    overlay.dataset.intent = intent || 'enquire';
    form.dispatchEvent(new CustomEvent('formreset-ui'));
    if (plan && interest) { interest.value = plan; interest.dispatchEvent(new Event('change', { bubbles: true })); }
    document.getElementById('modalTitle').textContent = intent === 'whatsapp' ? 'Chat with us on WhatsApp' : 'Get Price & Brochure';
    var ms = document.getElementById('modalSub'); if (ms) ms.textContent = intent === 'whatsapp' ? 'Share your details and we will open WhatsApp for you.' : 'Our relationship manager will call you back.';
    var sb = form.querySelector('button[type="submit"]'); if (sb) sb.textContent = intent === 'whatsapp' ? 'Continue to WhatsApp' : 'Request Callback';
    overlay.classList.add('open'); document.body.style.overflow = 'hidden';
    setTimeout(function () { var n = document.getElementById('modal-name'); if (n) n.focus(); }, 100);
  }
  function closeModal() { overlay.classList.remove('open'); document.body.style.overflow = ''; }
  document.getElementById('modalClose').addEventListener('click', closeModal);
  overlay.addEventListener('click', function (e) { if (e.target === overlay) closeModal(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeModal(); });
  Array.prototype.forEach.call(document.querySelectorAll('[data-open-modal]'), function (el) {
    el.addEventListener('click', function () { openModal(el.getAttribute('data-plan'), el.getAttribute('data-intent')); });
  });
  form.addEventListener('submit', function () { if (overlay.dataset.intent === 'whatsapp') pendingWa = window.open('', '_blank'); });
  form.addEventListener('enquirySubmitted', function (e) {
    var d = e.detail || {};
    if (overlay.dataset.intent === 'whatsapp') {
      var url = 'https://wa.me/' + PHONE + '?text=' + encodeURIComponent("Hi, I'm " + (d.name || '') + ". I'm interested in " + (d.interest || 'a home') + ' at ' + (d.project || 'Serenia by House of Jets') + '. My number is ' + (d.phone || '') + '. Please share details.');
      if (pendingWa && !pendingWa.closed) pendingWa.location.href = url; else window.open(url, '_blank');
      pendingWa = null;
    }
  });
});
