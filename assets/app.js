/* Trade Charts – all tools. No dependencies, no network except same-origin JSON. */
(function () {
  'use strict';
  var BASE = document.body.getAttribute('data-base') || '';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var ATM = 14.6959, KPA = 6.894757, INHG = 2.03602;
  var cache = {};
  function getJSON(name) {
    if (!cache[name]) cache[name] = fetch(BASE + '/assets/' + name).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
    return cache[name];
  }
  function num(el) { var v = parseFloat(String(el.value).replace(',', '.')); return isFinite(v) ? v : NaN; }
  function f1(x, d) { return (Math.round(x * Math.pow(10, d)) / Math.pow(10, d)).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d }); }
  function store(k, v) { try { if (v === undefined) return localStorage.getItem('tc.' + k); localStorage.setItem('tc.' + k, v); } catch (e) { return null; } }
  function out(el, html, cls) { el.innerHTML = html; el.className = 'res' + (cls ? ' ' + cls : ''); }
  var QP = new URLSearchParams(location.search);
  function qsel(el, k) { var v = QP.get(k); if (el && v !== null && el.querySelector('option[value="' + v.replace(/"/g, '') + '"]')) el.value = v; }
  function qnum(el, k) { var v = QP.get(k); if (el && v !== null && isFinite(parseFloat(v))) el.value = String(parseFloat(v)); }

  /* ---------- nav ---------- */
  var nb = $('.navbtn');
  if (nb) nb.addEventListener('click', function () { var o = nb.getAttribute('aria-expanded') === 'true'; nb.setAttribute('aria-expanded', String(!o)); document.body.classList.toggle('navopen', !o); });
  $$('[data-print]').forEach(function (b) { b.addEventListener('click', function () { window.print(); }); });

  /* ---------- refrigerant math ---------- */
  function pAt(r, F, q) {
    var arr = q === 0 ? r.b : r.d, i = Math.floor(F - r.t0);
    if (F < r.t0 || i > arr.length - 1 || (i === arr.length - 1 && F > r.t0 + i)) return null;
    if (i === arr.length - 1) return arr[i];
    return arr[i] + (arr[i + 1] - arr[i]) * (F - r.t0 - i);
  }
  function tAt(r, P, q) {
    var arr = q === 0 ? r.b : r.d;
    for (var i = 0; i < arr.length - 1; i++) if (arr[i] <= P && P <= arr[i + 1]) return r.t0 + i + (P - arr[i]) / (arr[i + 1] - arr[i]);
    return null;
  }
  function toPsig(v, u) { return u === 'kpa' ? (v + 101.325) / KPA - ATM : u === 'bar' ? (v * 100 + 101.325) / KPA - ATM : v; }
  function fromPsig(p, u) { return u === 'kpa' ? (p + ATM) * KPA - 101.325 : u === 'bar' ? ((p + ATM) * KPA - 101.325) / 100 : p; }
  function pStr(p, u) {
    if (p === null) return '—';
    if (u === 'psig' && p < 0) return f1(-p * INHG, 1) + ' inHg vac';
    var v = fromPsig(p, u);
    return f1(v, u === 'bar' ? 2 : u === 'kpa' ? 0 : 1) + ' ' + (u === 'psig' ? 'psig' : u === 'kpa' ? 'kPa(g)' : 'bar(g)');
  }
  function tStr(F, u) { return F === null ? '—' : (u === 'C' ? f1((F - 32) / 1.8, 1) + ' °C' : f1(F, 1) + ' °F'); }

  function ptTool(root, getRef) {
    var mode = 't2p', inp = $('[data-in]', root), tu = $('[data-tu]', root), pu = $('[data-pu]', root), o = $('[data-out]', root);
    var lt = $('.u-t', root), lp = $('.u-p', root);
    if (store('tu')) tu.value = store('tu');
    if (store('pu')) pu.value = store('pu');
    qsel(tu, 'tu'); qsel(pu, 'pu');
    if (QP.get('m') === 'p2t') { mode = 'p2t'; $$('[data-mode]', root).forEach(function (x) { x.setAttribute('aria-pressed', String(x.getAttribute('data-mode') === 'p2t')); }); }
    qnum(inp, 'v');
    root._state = function () { return { m: mode, v: inp.value, tu: tu.value, pu: pu.value }; };
    function run() {
      var r = getRef(); if (!r) { out(o, 'Loading…'); return; }
      var v = num(inp); if (isNaN(v)) { out(o, 'Enter a number.'); return; }
      var h;
      if (mode === 't2p') {
        var F = tu.value === 'C' ? v * 1.8 + 32 : v;
        var b = pAt(r, F, 0), d = pAt(r, F, 1);
        if (b === null) { out(o, 'Outside chart range for ' + r.n + '.', 'warn'); return; }
        h = r.bl ? '<span class="k">Dew (vapor)</span><b>' + pStr(d, pu.value) + '</b><span class="k">Bubble (liquid)</span><b>' + pStr(b, pu.value) + '</b>'
                 : '<span class="k">Saturation pressure</span><b>' + pStr(b, pu.value) + '</b>';
        h = '<span class="q">' + r.n + ' at ' + tStr(F, tu.value) + '</span>' + h;
      } else {
        var P = toPsig(v, pu.value), tb = tAt(r, P, 0), td = tAt(r, P, 1);
        if (tb === null && td === null) { out(o, 'Outside chart range for ' + r.n + '.', 'warn'); return; }
        h = r.bl ? '<span class="k">Dew temp (superheat)</span><b>' + tStr(td, tu.value) + '</b><span class="k">Bubble temp (subcooling)</span><b>' + tStr(tb, tu.value) + '</b>'
                 : '<span class="k">Saturation temperature</span><b>' + tStr(tb, tu.value) + '</b>';
        h = '<span class="q">' + r.n + ' at ' + pStr(P, pu.value) + '</span>' + h;
      }
      out(o, h, 'ok');
    }
    $$('[data-mode]', root).forEach(function (b) {
      b.addEventListener('click', function () {
        mode = b.getAttribute('data-mode');
        $$('[data-mode]', root).forEach(function (x) { x.setAttribute('aria-pressed', String(x === b)); });
        lt.hidden = false; lp.hidden = false;
        if (mode === 't2p') { inp.value = tu.value === 'C' ? '4' : '40'; } else { inp.value = pu.value === 'psig' ? '120' : pu.value === 'kpa' ? '830' : '8.3'; }
        run();
      });
    });
    lp.hidden = false;
    [inp, tu, pu].forEach(function (e) { e.addEventListener('input', run); e.addEventListener('change', function () { store('tu', tu.value); store('pu', pu.value); run(); }); });
    root._run = run; run();
  }
  $$('[data-tool="pt"]').forEach(function (root) {
    var r = JSON.parse($('.ptdata', root).textContent);
    ptTool(root, function () { return r; });
  });
  function withAll(root, cb) {
    var sel = $('[data-ref]', root), all = null;
    if (store('ref') && sel.querySelector('option[value="' + store('ref') + '"]') && root.getAttribute('data-tool') !== 'pt-any') sel.value = store('ref');
    qsel(sel, 'ref'); root._refSel = sel;
    var get = function () { return all ? all[sel.value] : null; };
    cb(get, sel);
    getJSON('pt-all.json').then(function (j) { all = j; if (root._run) root._run(); }).catch(function () { out($('[data-out]', root), 'Could not load refrigerant data.', 'warn'); });
    sel.addEventListener('change', function () { store('ref', sel.value); if (root._run) root._run(); });
  }
  $$('[data-tool="pt-any"]').forEach(function (root) { withAll(root, function (get) { ptTool(root, get); }); });

  function shsc(root, kind) {
    withAll(root, function (get) {
      var p = $('[data-p]', root), t = $('[data-t]', root), pu = $('[data-pu]', root), tu = $('[data-tu]', root), o = $('[data-out]', root);
      qsel(pu, 'pu'); qsel(tu, 'tu'); qnum(p, 'p'); qnum(t, 't');
      root._state = function () { return { p: p.value, t: t.value, pu: pu.value, tu: tu.value }; };
      function run() {
        var r = get(); if (!r) { out(o, 'Loading…'); return; }
        var P = toPsig(num(p), pu.value), T = num(t); if (isNaN(P) || isNaN(T)) { out(o, 'Enter pressure and temperature.'); return; }
        var TF = tu.value === 'C' ? T * 1.8 + 32 : T;
        var sat = tAt(r, P, kind === 'sh' ? 1 : 0);
        if (sat === null) { out(o, 'Pressure outside chart range for ' + r.n + '.', 'warn'); return; }
        var v = kind === 'sh' ? TF - sat : sat - TF, vd = tu.value === 'C' ? v / 1.8 : v, unit = tu.value === 'C' ? ' K' : ' °F';
        var lab = kind === 'sh' ? 'Superheat' : 'Subcooling';
        var warn = v < 0 ? (kind === 'sh' ? ' Negative superheat: the line is colder than saturation – check readings or liquid floodback.' : ' Negative subcooling: the liquid line is warmer than saturation – flash gas or a measurement error.') : '';
        out(o, '<span class="q">' + r.n + ': saturated ' + (r.bl ? (kind === 'sh' ? 'dew ' : 'bubble ') : '') + 'temp ' + tStr(sat, tu.value) + '</span><span class="k">' + lab + '</span><b>' + f1(vd, 1) + unit + '</b>' + (warn ? '<span class="w">' + warn + '</span>' : ''), v < 0 ? 'warn' : 'ok');
      }
      root._run = run;
      [p, t, pu, tu].forEach(function (e) { e.addEventListener('input', run); e.addEventListener('change', run); });
      run();
    });
  }
  $$('[data-tool="sh"]').forEach(function (r) { shsc(r, 'sh'); });
  $$('[data-tool="sc"]').forEach(function (r) { shsc(r, 'sc'); });

  $$('[data-tool="tsh"]').forEach(function (root) {
    var wb = $('[data-wb]', root), db = $('[data-db]', root), sh = $('[data-sh]', root), o = $('[data-out]', root);
    function run() {
      var w = num(wb), d = num(db); if (isNaN(w) || isNaN(d)) { out(o, 'Enter wet bulb and dry bulb.'); return; }
      var t = (3 * w - 80 - d) / 2;
      if (w < 50 || w > 76 || d < 55 || d > 115) { out(o, 'Outside the usual range of charging tables (WB 50–76 °F, DB 55–115 °F). Use the manufacturer chart.', 'warn'); return; }
      if (t < 5) { out(o, '<span class="k">Target superheat</span><b>below 5 °F</b><span class="w">Do not charge by superheat at these conditions; verify airflow and follow the manufacturer procedure.</span>', 'warn'); return; }
      var h = '<span class="k">Target superheat</span><b>' + f1(t, 0) + ' °F</b>', m = num(sh);
      if (!isNaN(m)) { var diff = m - t; h += '<span class="w">Measured ' + f1(m, 0) + ' °F is ' + f1(Math.abs(diff), 0) + ' °F ' + (diff > 0 ? 'above target: possible undercharge (add refrigerant slowly, re-check).' : diff < 0 ? 'below target: possible overcharge (recover slowly, re-check).' : 'on target.') + ' Allow ±3 °F (±5 °F per many manufacturers).</span>'; }
      out(o, h, 'ok');
    }
    root._run = run; [wb, db, sh].forEach(function (e) { e.addEventListener('input', run); }); run();
  });

  /* ---------- electrical ---------- */
  var AWG = ['14', '12', '10', '8', '6', '4', '3', '2', '1', '1/0', '2/0', '3/0', '4/0', '250', '300', '350', '400', '500', '600', '700', '750', '1000'];
  function awgL(s) { return /^\d+$/.test(s) && +s >= 250 ? s + ' kcmil' : s + ' AWG'; }
  function maxfill(area, w) { if (w > 0.53 * area) return 0; var n40 = 0.4 * area / w, n = Math.floor(n40); if (n40 - n >= 0.8) n++; if (n >= 3) return n; if (2 * w <= 0.31 * area) return 2; return 1; }
  $$('[data-tool="fill"]').forEach(function (root) {
    var ct = $('[data-ct]', root), cs = $('[data-cs]', root), box = $('[data-wires]', root), o = $('[data-out]', root), E = null;
    function addRow(type, size, n) {
      var d = document.createElement('div'); d.className = 'row wire';
      d.innerHTML = '<label>Count <input type="number" min="0" inputmode="numeric" value="' + n + '" data-n></label><label>Size <select data-s>' + AWG.map(function (s) { return '<option value="' + s + '"' + (s === size ? ' selected' : '') + '>' + awgL(s) + '</option>'; }).join('') + '</select></label><label>Insulation <select data-i><option value="THHN"' + (type === 'THHN' ? ' selected' : '') + '>THHN / THWN-2</option><option value="XHHW"' + (type === 'XHHW' ? ' selected' : '') + '>XHHW-2</option></select></label><button type="button" class="x" aria-label="Remove">×</button>';
      box.appendChild(d);
      $('.x', d).addEventListener('click', function () { d.remove(); run(); });
      $$('input,select', d).forEach(function (e) { e.addEventListener('input', run); e.addEventListener('change', run); });
    }
    function sizes() {
      var c = E.conduit[ct.value], keep = cs.value || '3/4';
      cs.innerHTML = Object.keys(c).map(function (s) { return '<option value="' + s + '">' + s + '"</option>'; }).join('');
      cs.value = c[keep] ? keep : Object.keys(c)[1];
    }
    function run() {
      if (!E) return;
      var c = E.conduit[ct.value], area = c[cs.value].area, tot = 0, n = 0, same = null, mixed = false;
      $$('.wire', box).forEach(function (w) {
        var k = Math.max(0, Math.floor(num($('[data-n]', w)) || 0)), s = $('[data-s]', w).value, t = $('[data-i]', w).value, a = E.wire_area[t][s];
        if (!a || !k) return; tot += k * a; n += k; var key = t + s; if (same === null) same = key; else if (same !== key) mixed = true;
      });
      if (!n) { out(o, 'Add at least one conductor.'); return; }
      var lim = n === 1 ? 0.53 : n === 2 ? 0.31 : 0.40, pct = 100 * tot / area, ok = tot <= lim * area;
      var smallest = null;
      Object.keys(c).some(function (s) { if (tot <= lim * c[s].area) { smallest = s; return true; } return false; });
      var h = '<span class="q">' + n + ' conductor' + (n > 1 ? 's' : '') + ', ' + f1(tot, 4) + ' in² in ' + cs.value + '" ' + ct.options[ct.selectedIndex].text + ' (' + f1(area, 3) + ' in²)</span>' +
        '<span class="k">Fill</span><b>' + f1(pct, 1) + '% of ' + f1(lim * 100, 0) + '% allowed – ' + (ok ? 'OK' : 'TOO FULL') + '</b>' +
        '<span class="w">Smallest ' + ct.options[ct.selectedIndex].text + ' that fits: ' + (smallest ? smallest + '"' : 'none in this table') + '.' + (!mixed && n >= 3 ? ' Same-size max (Note 7 round-up): ' + maxfill(area, tot / n) + '.' : '') + '</span>';
      out(o, h, ok ? 'ok' : 'bad');
    }
    root._run = run;
    root._reset = function () { if (!E) return; box.innerHTML = ''; cs.value = '3/4'; sizes(); addRow('THHN', '12', 3); addRow('THHN', '12', 1); run(); };
    getJSON('electrical.json').then(function (j) { E = j; sizes(); addRow('THHN', '12', 3); addRow('THHN', '12', 1); run(); });
    ct.addEventListener('change', function () { sizes(); run(); });
    cs.addEventListener('change', run);
    $('[data-add]', root).addEventListener('click', function () { addRow('THHN', '12', 1); run(); });
  });
  $$('[data-tool="amp"]').forEach(function (root) {
    var s = $('[data-s]', root), m = $('[data-m]', root), c = $('[data-c]', root), o = $('[data-out]', root);
    getJSON('electrical.json').then(function (E) {
      function run() {
        var a = E.ampacity[s.value], row = a[m.value];
        if (!row) { out(o, 'Aluminum is not listed for ' + awgL(s.value) + ' in Table 310.16.', 'warn'); return; }
        var lim = { '14': 15, '12': 20, '10': 30 }[s.value];
        out(o, '<span class="k">' + awgL(s.value) + ' ' + (m.value === 'cu' ? 'copper' : 'aluminum') + ' at ' + ['60', '75', '90'][+c.value] + ' °C</span><b>' + row[+c.value] + ' A</b>' + (lim && m.value === 'cu' ? '<span class="w">Overcurrent protection limited to ' + lim + ' A by NEC 240.4(D).</span>' : '') + '<span class="w">Base value: ≤3 current-carrying conductors, 30 °C ambient.</span>', 'ok');
      }
      root._run = run; [s, m, c].forEach(function (e) { e.addEventListener('change', run); }); run();
    });
  });
  $$('[data-tool="vd"]').forEach(function (root) {
    var m = $('[data-m]', root), s = $('[data-s]', root), ph = $('[data-ph]', root), L = $('[data-l]', root), I = $('[data-i]', root), V = $('[data-v]', root), o = $('[data-out]', root);
    getJSON('electrical.json').then(function (E) {
      function vd(size) { var r = E.t8[size][m.value]; if (!r) return null; return (ph.value === '3' ? 1.732 : 2) * num(L) * r * num(I) / 1000; }
      function run() {
        var d = vd(s.value), v = num(V);
        if (d === null) { out(o, 'No aluminum resistance for this size.', 'warn'); return; }
        if (isNaN(d) || !v) { out(o, 'Enter length, current and voltage.'); return; }
        var pct = 100 * d / v, best = null;
        Object.keys(E.t8).some(function (k) { if (k === '18' || k === '16') return false; var x = vd(k); if (x !== null && 100 * x / v <= 3) { best = k; return true; } return false; });
        out(o, '<span class="k">Voltage drop</span><b>' + f1(d, 2) + ' V (' + f1(pct, 2) + '%)</b><span class="w">Voltage at load ≈ ' + f1(v - d, 1) + ' V. ' + (pct <= 3 ? 'Within the 3% recommendation.' : 'Over 3%.') + ' Smallest ' + (m.value === 'cu' ? 'copper' : 'aluminum') + ' size under 3%: ' + (best ? awgL(best) : 'none up to 1000 kcmil') + '. Check ampacity separately.</span>', pct <= 3 ? 'ok' : 'warn');
      }
      root._run = run; [m, s, ph, L, I, V].forEach(function (e) { e.addEventListener('input', run); e.addEventListener('change', run); }); run();
    });
  });
  $$('[data-tool="off"]').forEach(function (root) {
    var a = $('[data-a]', root), d = $('[data-o]', root), o = $('[data-out]', root);
    function frac(x) { var w = Math.floor(x), s = Math.round((x - w) * 16); if (s === 16) { w++; s = 0; } var n = s, den = 16; while (n && n % 2 === 0) { n /= 2; den /= 2; } return w + (n ? '-' + n + '/' + den : '') + ' in'; }
    function run() {
      var ang = parseFloat(a.value) * Math.PI / 180, x = num(d); if (isNaN(x)) { out(o, 'Enter offset depth.'); return; }
      var dist = x / Math.sin(ang), sh = x * Math.tan(ang / 2);
      out(o, '<span class="k">Distance between bends</span><b>' + f1(dist, 2) + ' in (≈ ' + frac(dist) + ')</b><span class="k">Shrink</span><b>' + f1(sh, 2) + ' in (≈ ' + frac(sh) + ')</b><span class="w">Multiplier ' + f1(1 / Math.sin(ang), 3) + '; adds ' + (2 * parseFloat(a.value)) + '° toward the 360° limit between pull points.</span>', 'ok');
    }
    root._run = run; [a, d].forEach(function (e) { e.addEventListener('input', run); e.addEventListener('change', run); }); run();
  });
  $$('[data-tool="box"]').forEach(function (root) {
    var b = $('[data-b]', root), v = $('[data-v]', root), o = $('[data-out]', root);
    var AL = { '14': 2, '12': 2.25, '10': 2.5, '8': 3, '6': 5 };
    b.value = '21'; if (b.value !== '21') b.selectedIndex = 4;
    b.addEventListener('change', function () { if (b.value !== 'custom') v.value = parseFloat(b.value).toFixed(1); run(); });
    function g(k) { var x = num($('[data-' + k + ']', root)); return isNaN(x) || x < 0 ? 0 : Math.floor(x); }
    function run() {
      var vol = num(v); if (isNaN(vol)) { out(o, 'Enter box volume.'); return; }
      var tot = 0, largest = null, cnt = 0;
      ['14', '12', '10', '8', '6'].forEach(function (s) { var n = g('w' + s); if (n) { tot += n * AL[s]; cnt += n; largest = s; } });
      if (!largest) { out(o, 'Enter conductors.'); return; }
      var big = AL[largest], dev = g('dev'), egc = g('eg'), parts = [];
      parts.push(cnt + ' conductors = ' + f1(tot, 2));
      if (dev) { tot += dev * 2 * big; parts.push(dev + ' device(s) × 2 = ' + f1(dev * 2 * big, 2)); }
      if ($('[data-cl]', root).value === '1') { tot += big; parts.push('clamps = ' + f1(big, 2)); }
      if (egc) { var eg = big * (1 + Math.max(0, egc - 4) * 0.25); tot += eg; parts.push('grounds = ' + f1(eg, 2)); }
      var st = g('st'); if (st) { tot += st * big; parts.push('studs/hickeys = ' + f1(st * big, 2)); }
      var ok = tot <= vol;
      out(o, '<span class="k">Required volume</span><b>' + f1(tot, 2) + ' in³ of ' + f1(vol, 1) + ' in³ – ' + (ok ? 'OK' : 'TOO SMALL') + '</b><span class="w">' + parts.join('; ') + ' (allowances at ' + largest + ' AWG, the largest conductor; grounds use the largest ground in the box – the calculator assumes it is the same size).</span>', ok ? 'ok' : 'bad');
    }
    root._run = run; root._after = function () { b.value = '21'; if (b.value !== '21') b.selectedIndex = 4; };
    $$('input,select', root).forEach(function (e) { e.addEventListener('input', run); e.addEventListener('change', run); }); run();
  });

  /* ---------- gas ---------- */
  $$('[data-tool="gas"]').forEach(function (root) {
    var tb = $('[data-tb]', root), btu = $('[data-btu]', root), len = $('[data-len]', root), hv = $('[data-hv]', root), o = $('[data-out]', root);
    getJSON('gas.json').then(function (G) {
      function run() {
        var t = G.tables.filter(function (x) { return String(x.table) === tb.value; })[0], lp = /Propane/.test(t.gas), csst = /CSST/.test(t.material);
        $('.hv', root).hidden = lp;
        var load = num(btu), L = num(len); if (isNaN(load) || isNaN(L)) { out(o, 'Enter load and length.'); return; }
        var need = lp ? load / 1000 : load / (num(hv) || 1000);
        var lens = Object.keys(t.rows).map(Number).sort(function (a, b) { return a - b; }), row = null;
        for (var i = 0; i < lens.length; i++) if (lens[i] >= L) { row = lens[i]; break; }
        if (row === null) { out(o, 'Length is beyond this table (' + lens[lens.length - 1] + ' ft max).', 'warn'); return; }
        var vals = t.rows[String(row)], pick = null;
        for (var j = 0; j < vals.length; j++) if (vals[j] !== null && vals[j] >= need) { pick = j; break; }
        var unit = lp ? 'MBH' : 'CFH';
        if (pick === null) { out(o, 'Load of ' + f1(need, 0) + ' ' + unit + ' exceeds the largest size in this table at ' + row + ' ft.', 'warn'); return; }
        out(o, '<span class="q">' + f1(need, 0) + ' ' + unit + ' at ' + row + ' ft row (IFGC Table 402.4(' + t.table + '))</span><span class="k">Minimum size</span><b>' + (csst ? 'EHD ' + t.sizes[pick] : t.sizes[pick] + '"') + '</b><span class="w">Capacity ' + vals[pick].toLocaleString('en-US') + ' ' + unit + '. Size each branch with the same ' + row + ' ft row and its own load.</span>', 'ok');
      }
      root._run = run; [tb, btu, len, hv].forEach(function (e) { e.addEventListener('input', run); e.addEventListener('change', run); }); run();
    });
  });

  /* ---------- age by serial ---------- */
  var MON = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  var BWY = 'ABCDEFGHJKLMNPSTWXYZ', BWM = 'ABCDEFGHJKLM';
  function wk(y, w) { var d = new Date(Date.UTC(y, 0, 1 + (w - 1) * 7)); return 'week ' + w + ' of ' + y + ' (around ' + MON[d.getUTCMonth()] + ')'; }
  function yy(n) { var now = new Date().getFullYear() % 100; return n <= now ? 2000 + n : 1900 + n; }
  var AGE = {
    bw: function (s) { var y = BWY.indexOf(s[0]), m = BWM.indexOf(s[1]); if (y < 0 || m < 0) return null; var a = 1984 + y, b = 2004 + y, now = new Date().getFullYear(); return MON[m] + ' ' + (b <= now ? b + ' (or ' + a + ')' : a); },
    mmyy: function (s) { var m = /^(\d\d)(\d\d)/.exec(s); if (!m || +m[1] < 1 || +m[1] > 12) return null; return MON[+m[1] - 1] + ' ' + yy(+m[2]); },
    yyww: function (s) {
      var m = /^(\d\d)(\d\d)/.exec(s); if (m && +m[2] >= 1 && +m[2] <= 53) return wk(yy(+m[1]), +m[2]);
      var o = /^[A-Z0-9]([A-M])(\d\d)/.exec(s); if (o && o[1] !== 'I') return MON['ABCDEFGHJKLM'.indexOf(o[1])] + ' ' + yy(+o[2]) + ' (older month-letter format)';
      var st = /^([A-M])(\d\d)/.exec(s); if (st && st[1] !== 'I') return MON['ABCDEFGHJKLM'.indexOf(st[1])] + ' ' + yy(+st[2]) + ' (older State format)';
      return null;
    },
    wwyy: function (s) { var m = /^(\d\d)(\d\d)/.exec(s); if (!m || +m[1] < 1 || +m[1] > 53) return null; return wk(yy(+m[2]), +m[1]); },
    yymm: function (s) { var m = /^(\d\d)(\d\d)/.exec(s); if (!m || +m[2] < 1 || +m[2] > 12) return null; return MON[+m[2] - 1] + ' ' + yy(+m[1]); },
    lennox: function (s) { var m = /^(\d\d)(\d\d)([A-M])/.exec(s); if (!m || m[3] === 'I') return null; return MON['ABCDEFGHJKLM'.indexOf(m[3])] + ' ' + yy(+m[2]) + ' (plant ' + m[1] + ')'; },
    trane: function (s) { var m; if (s.length >= 10 && (m = /^(\d\d)(\d\d)/.exec(s)) && +m[1] >= 10 && +m[2] >= 1 && +m[2] <= 53) return wk(2000 + +m[1], +m[2]); if (s.length === 9 && (m = /^([2-9])(\d\d)/.exec(s)) && +m[2] >= 1 && +m[2] <= 53) return wk(2000 + +m[1], +m[2]); return null; },
    rheemhvac: function (s) { var m = /^[A-Z](\d\d)(\d\d)/.exec(s); if (!m || +m[1] < 1 || +m[1] > 53) return null; return wk(yy(+m[2]), +m[1]); }
  };
  $$('[data-tool="age"]').forEach(function (root) {
    var k = root.getAttribute('data-kind'), sn = $('[data-sn]', root), o = $('[data-out]', root);
    function run() {
      var s = sn.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
      if (s.length < 4) { out(o, 'Type the full serial number from the rating plate.'); return; }
      var r = AGE[k](s);
      if (!r) { out(o, 'This serial does not match the documented format. Check for a printed date on the label or use the manufacturer’s warranty lookup.', 'warn'); return; }
      var y = (/(\d{4})/.exec(r) || [])[1], age = y ? new Date().getFullYear() - +y : null;
      out(o, '<span class="k">Manufactured</span><b>' + r + '</b>' + (age !== null && age >= 0 ? '<span class="w">About ' + age + ' year' + (age === 1 ? '' : 's') + ' old.</span>' : ''), 'ok');
    }
    root._run = run; sn.addEventListener('input', run); run();
  });

  /* ---------- welding ---------- */
  $$('[data-tool="mig"]').forEach(function (root) {
    var th = $('[data-th]', root), w = $('[data-w]', root), o = $('[data-out]', root);
    var W = { '.023': [3.5, 30, 130], '.030': [2, 40, 145], '.035': [1.6, 50, 180], '.045': [1, 75, 250] };
    function run() {
      var t = num(th); if (isNaN(t) || t <= 0) { out(o, 'Enter thickness in inches (e.g. 0.125).'); return; }
      var amps = Math.round(t * 1000), x = W[w.value], fit = amps >= x[1] && amps <= x[2];
      var sug = Object.keys(W).filter(function (k) { return amps >= W[k][1] && amps <= W[k][2]; });
      out(o, '<span class="k">Starting amperage</span><b>≈ ' + amps + ' A</b><span class="k">Wire feed speed (' + w.value + ')</span><b>≈ ' + Math.round(amps * x[0]) + ' ipm</b><span class="w">' + (fit ? w.value + ' wire covers ' + x[1] + '–' + x[2] + ' A.' : w.value + ' wire is rated ' + x[1] + '–' + x[2] + ' A; consider ' + (sug.join(' or ') || 'multiple passes') + '.') + (amps > 250 ? ' Over 1/4 in: plan multiple passes or spray transfer.' : '') + ' Set voltage from your door chart, then tune on scrap.</span>', fit ? 'ok' : 'warn');
    }
    root._run = run; [th, w].forEach(function (e) { e.addEventListener('input', run); e.addEventListener('change', run); }); run();
  });

  /* ---------- light / dark toggle (choice saved in localStorage "tc.theme"; default follows the OS) ---------- */
  (function () {
    var btn = $('.theme-toggle'), html = document.documentElement, mq = window.matchMedia ? matchMedia('(prefers-color-scheme: dark)') : null;
    function cur() { return html.getAttribute('data-theme') || (mq && mq.matches ? 'dark' : 'light'); }
    function sync() { if (!btn) return; var d = cur() === 'dark'; btn.setAttribute('aria-pressed', String(d)); btn.setAttribute('aria-label', d ? 'Light mode' : 'Dark mode'); }
    if (btn) btn.addEventListener('click', function () { var t = cur() === 'dark' ? 'light' : 'dark'; html.setAttribute('data-theme', t); store('theme', t); sync(); });
    if (mq && mq.addEventListener) mq.addEventListener('change', sync);
    sync();
  })();

  /* ---------- Calculate / Enter, Copy result, Reset, Share (every tool) ---------- */
  function resText(o) {
    var lines = [], kid = o.children, i;
    if (!kid.length) return o.textContent.trim();
    for (i = 0; i < kid.length; i++) {
      var e = kid[i];
      if (e.classList.contains('k') && kid[i + 1] && kid[i + 1].tagName === 'B') { lines.push(e.textContent.trim() + ': ' + kid[i + 1].textContent.trim()); i++; }
      else lines.push(e.textContent.trim());
    }
    return lines.filter(Boolean).join('\n');
  }
  function copyText(t) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(t);
    return new Promise(function (ok, no) {
      var ta = document.createElement('textarea'); ta.value = t; ta.className = 'sr'; ta.setAttribute('readonly', ''); document.body.appendChild(ta); ta.select();
      var r = false; try { r = document.execCommand('copy'); } catch (e) {} ta.remove(); r ? ok() : no();
    });
  }
  function showInView(o, bar) {
    var hd = $('.top'), h = hd ? hd.getBoundingClientRect().height : 0;
    var top = o.getBoundingClientRect().top, bot = (bar && !bar.hidden ? bar : o).getBoundingClientRect().bottom, vh = window.visualViewport ? visualViewport.height : innerHeight;
    if (top < h + 8) window.scrollBy({ top: top - h - 8, behavior: 'smooth' });
    else if (bot > vh - 8) window.scrollBy({ top: Math.min(bot - vh + 12, top - h - 8), behavior: 'smooth' });
  }
  $$('[data-tool]').forEach(function (root) {
    var o = $('[data-out]', root); if (!o) return;
    var calcbar = $('.calcbar', root), bar = $('.tbar', root), msg = bar && $('.tmsg', bar), kind = root.getAttribute('data-tool'), tm;
    if (!calcbar || !bar) return;
    calcbar.hidden = false; bar.hidden = false;
    function say(t) { if (!msg) return; msg.textContent = t; clearTimeout(tm); tm = setTimeout(function () { msg.textContent = ''; }, 2500); }
    function calc() {
      if (root._run) root._run();
      var a = document.activeElement; if (a && root.contains(a) && a.blur && /INPUT|SELECT/.test(a.tagName)) a.blur();
      requestAnimationFrame(function () { showInView(o, bar); }); setTimeout(function () { showInView(o, bar); }, 350);
    }
    $('[data-calc]', calcbar).addEventListener('click', calc);
    root.addEventListener('keydown', function (e) { if (e.key === 'Enter' && e.target.tagName === 'INPUT') { e.preventDefault(); calc(); } });
    $$('input[type=number],input[data-sn]', root).forEach(function (i) { i.setAttribute('enterkeyhint', 'go'); });
    function shareUrl() {
      var st = root._state ? root._state() : {}, q = new URLSearchParams();
      if (root._refSel) q.set('ref', root._refSel.value);
      Object.keys(st).forEach(function (k) { if (st[k] !== '' && st[k] != null) q.set(k, st[k]); });
      return location.origin + location.pathname + '?' + q.toString();
    }
    var shareable = /^(pt|pt-any|sh|sc)$/.test(kind);
    $('[data-copy]', bar).addEventListener('click', function () {
      var t = resText(o); if (!t) return;
      copyText(t + '\n' + (shareable ? shareUrl() : location.origin + location.pathname)).then(function () { say('Copied'); }, function () { say('Copy failed – select the result and copy it'); });
    });
    $('[data-reset]', bar).addEventListener('click', function () {
      if (root._reset) { $$('select', root).forEach(function (s) { if (!s.closest('.wire') && !s.hasAttribute('data-cs')) { var d = $$('option', s).filter(function (x) { return x.defaultSelected; })[0]; s.selectedIndex = d ? d.index : 0; } }); root._reset(); say('Reset'); return; }
      $$('input', root).forEach(function (i) { i.value = i.defaultValue; });
      $$('select', root).forEach(function (s) { var d = $$('option', s).filter(function (x) { return x.defaultSelected; })[0]; s.selectedIndex = d ? d.index : 0; });
      if (root._after) root._after();
      var t2p = $('[data-mode="t2p"]', root);
      $$('select', root).forEach(function (s) { s.dispatchEvent(new Event('change', { bubbles: true })); });
      if (t2p) t2p.click(); else if (root._run) root._run();
      say('Reset');
    });
    var sb = $('[data-share]', bar);
    if (shareable) {
      sb.hidden = false;
      sb.addEventListener('click', function () {
        var u = shareUrl(), t = resText(o);
        if (navigator.share) { navigator.share({ title: document.title, text: t, url: u }).catch(function () {}); return; }
        copyText(u).then(function () { say('Link copied'); }, function () { say('Could not copy the link'); });
      });
    }
  });

  /* ---------- search ---------- */
  function searchIdx() { return getJSON('search.json'); }
  function score(p, q) {
    var t = (p.t + ' ' + p.d).toLowerCase().replace(/-/g, ''), terms = q.toLowerCase().replace(/-/g, '').split(/\s+/).filter(Boolean), s = 0;
    for (var i = 0; i < terms.length; i++) { var x = terms[i]; if (t.indexOf(x) < 0) return 0; s += p.t.toLowerCase().replace(/-/g, '').indexOf(x) >= 0 ? 3 : 1; }
    return s;
  }
  function find(idx, q) { return idx.map(function (p) { return [score(p, q), p]; }).filter(function (x) { return x[0] > 0; }).sort(function (a, b) { return b[0] - a[0]; }).slice(0, 12).map(function (x) { return x[1]; }); }
  var sf = $('.search'), si = $('#q'), sr = $('.sres');
  if (si) {
    si.addEventListener('input', function () {
      var q = si.value.trim(); if (q.length < 2) { sr.hidden = true; return; }
      searchIdx().then(function (idx) {
        var r = find(idx, q).slice(0, 8);
        sr.innerHTML = r.length ? r.map(function (p) { return '<a href="' + BASE + p.u + '">' + p.t.replace(/</g, '&lt;') + '</a>'; }).join('') : '<span>No match. Press Enter for full search.</span>';
        sr.hidden = false;
      });
    });
    document.addEventListener('click', function (e) { if (!sf.contains(e.target)) sr.hidden = true; });
  }
  $$('[data-tool="search"]').forEach(function (root) {
    var q = $('[data-q]', root), ol = $('[data-r]', root);
    var init = new URLSearchParams(location.search).get('q') || ''; q.value = init;
    function run() { searchIdx().then(function (idx) { var r = q.value.trim() ? find(idx, q.value.trim()) : []; ol.innerHTML = r.map(function (p) { return '<li><a href="' + BASE + p.u + '">' + p.t.replace(/</g, '&lt;') + '</a><p>' + p.d.replace(/</g, '&lt;') + '</p></li>'; }).join('') || (q.value ? '<li>No results.</li>' : ''); }); }
    q.addEventListener('input', run); run();
  });
})();
