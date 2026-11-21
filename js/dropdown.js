/* Serenia: styled dropdown for the "I'm interested in" field.
   Enhances every <select name="interest"> and keeps the native select
   (visually hidden) as the real value, so form.js works unchanged. */
document.addEventListener('DOMContentLoaded', function () {
  var CHEV = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>';
  var TICK = '<svg class="tk" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12l5 5 9-10"/></svg>';
  var all = [];

  function build(sel) {
    var wrap = document.createElement('div'); wrap.className = 'dd';
    var btn = document.createElement('button'); btn.type = 'button'; btn.className = 'dd-btn';
    btn.setAttribute('aria-haspopup', 'listbox'); btn.setAttribute('aria-expanded', 'false');
    var list = document.createElement('ul'); list.className = 'dd-list'; list.setAttribute('role', 'listbox'); list.id = sel.id + '-list';
    btn.setAttribute('aria-controls', list.id);
    var placeholder = '';
    var items = [];
    Array.prototype.forEach.call(sel.options, function (o) {
      if (!o.value) { placeholder = o.textContent; return; }
      var li = document.createElement('li'); li.setAttribute('role', 'option'); li.setAttribute('data-value', o.value);
      li.innerHTML = '<span class="m">' + o.textContent + '</span>' + (o.getAttribute('data-sub') ? '<span class="s">' + o.getAttribute('data-sub') + '</span>' : '') + TICK;
      list.appendChild(li); items.push(li);
    });
    wrap.appendChild(btn); wrap.appendChild(list);
    sel.classList.add('dd-native'); sel.tabIndex = -1; sel.setAttribute('aria-hidden', 'true');
    sel.parentNode.insertBefore(wrap, sel.nextSibling);
    var active = -1, isOpen = false;

    function refresh() {
      var o = sel.options[sel.selectedIndex];
      if (o && o.value) {
        btn.innerHTML = '<span class="v"><b>' + o.textContent + '</b>' + (o.getAttribute('data-sub') ? '<i>' + o.getAttribute('data-sub') + '</i>' : '') + '</span>' + CHEV;
        btn.classList.remove('ph');
      } else {
        btn.innerHTML = '<span class="v">' + (placeholder || 'Select') + '</span>' + CHEV; btn.classList.add('ph');
      }
      items.forEach(function (li) { var on = li.getAttribute('data-value') === sel.value; li.setAttribute('aria-selected', on ? 'true' : 'false'); li.classList.toggle('on', on); });
    }
    function setActive(i) {
      active = Math.max(0, Math.min(items.length - 1, i));
      items.forEach(function (li, k) { li.classList.toggle('act', k === active); });
      if (items[active]) items[active].scrollIntoView({ block: 'nearest' });
    }
    function open() {
      if (isOpen) return; isOpen = true;
      wrap.classList.remove('up');
      var r = btn.getBoundingClientRect();
      if (window.innerHeight - r.bottom < 250 && r.top > 250) wrap.classList.add('up');
      wrap.classList.add('open'); btn.setAttribute('aria-expanded', 'true');
      var i = items.findIndex(function (li) { return li.getAttribute('data-value') === sel.value; });
      setActive(i < 0 ? 0 : i);
    }
    function close() { isOpen = false; wrap.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
    function choose(i) {
      var li = items[i]; if (!li) return;
      sel.value = li.getAttribute('data-value');
      sel.dispatchEvent(new Event('change', { bubbles: true }));
      refresh(); close(); btn.focus();
    }
    btn.addEventListener('click', function () { isOpen ? close() : open(); });
    btn.addEventListener('keydown', function (e) {
      var k = e.key;
      if (k === 'Escape' && isOpen) { e.stopPropagation(); close(); return; }
      if (k === 'ArrowDown' || k === 'ArrowUp') { e.preventDefault(); if (!isOpen) open(); else setActive(active + (k === 'ArrowDown' ? 1 : -1)); }
      else if ((k === 'Enter' || k === ' ') && isOpen) { e.preventDefault(); choose(active); }
      else if ((k === 'Enter' || k === ' ') && !isOpen) { e.preventDefault(); open(); }
      else if (k === 'Tab') close();
    });
    list.addEventListener('click', function (e) { var li = e.target.closest('li'); if (li) choose(items.indexOf(li)); });
    list.addEventListener('mousemove', function (e) { var li = e.target.closest('li'); if (li) setActive(items.indexOf(li)); });
    document.addEventListener('click', function (e) { if (!wrap.contains(e.target)) close(); });
    sel.addEventListener('focus', function () { btn.focus(); });
    sel.addEventListener('change', refresh);
    if (sel.form) sel.form.addEventListener('reset', function () { setTimeout(refresh, 0); });
    refresh(); all.push(refresh);
  }
  Array.prototype.forEach.call(document.querySelectorAll('select[name="interest"]'), build);
});
