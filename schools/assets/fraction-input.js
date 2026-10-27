/* MaffsFractionInput: the two-box typed fraction (numerator over denominator), one copy for any game that asks for a fraction
 * (contract POSSIBLY-MAYBE, Jon's amendment, 27 Oct 2026). Extracted as a NEW shared file from the numerator/denominator input in
 * The 6 P's page (the-6-ps/index.html, case 'fraction'); that page is not changed and still carries its own copy until it is
 * switched over (listed in the lanes' notes for the week of 2 Nov).
 *
 *   var f = MaffsFractionInput.mount(host, { label: 'Your answer as a fraction' });
 *     host   an element to draw the two boxes into (its contents are replaced)
 *     f.inputs   [numeratorInput, denominatorInput]  (hand these to MaffsKeypad.mount as its targets)
 *     f.raw()    what was typed, as MaffsAnswer.fractionForm reads it: "3/8", "3/" never; '' when both are empty
 *     f.value()  { num, den } as whole numbers when both boxes hold digits and the denominator is not 0, else null
 *     f.filled() true when both boxes hold something
 *     f.clear()  empty both
 *     f.mark(state)  'right' | 'wrong' | '' puts a class on the boxes (never colour alone: the game also writes words)
 *
 * The boxes take digits only (a probability is never negative) and at most three of them. Enter in the numerator moves to the
 * denominator; Enter in the denominator fires the 'fraction-submit' event on host, which the game listens for.
 * Marking is not here: the game marks with MaffsAnswer (fraction() for the value, fractionForm() when lowest terms are asked).
 * Stdlib only, no hex colours: it takes its colours from the page's theme tokens.
 */
(function (root) {
  'use strict';

  var CSS = [
    '.mfi{display:inline-flex;flex-direction:column;align-items:center;gap:.2rem;vertical-align:middle}',
    '.mfi-in{width:4.2rem;height:44px;text-align:center;font:inherit;font-size:1.1rem;border:2px solid var(--border);border-radius:9px;background:var(--surface-alt);color:var(--text)}',
    '.mfi-in:focus{outline:3px solid var(--accent);outline-offset:1px}',
    '.mfi-in.maffs-keypad-selected{border-color:var(--text);outline-color:var(--text)}',
    '.mfi-bar{width:100%;height:2px;background:var(--text)}',
    '.mfi.right .mfi-in{border-color:var(--correct)}',
    '.mfi.wrong .mfi-in{border-color:var(--wrong)}',
    '@media (max-height:620px){.mfi-in{height:40px;width:3.8rem}.mfi{gap:.1rem}}'
  ].join('\n');

  function ensureCss() {
    if (document.getElementById('mfi-css')) return;
    var st = document.createElement('style');
    st.id = 'mfi-css'; st.textContent = CSS;
    document.head.appendChild(st);
  }

  function digits(v) { return String(v).replace(/[^0-9]/g, '').slice(0, 3); }

  function mount(host, opts) {
    opts = opts || {};
    ensureCss();
    host.textContent = '';
    var wrap = document.createElement('span');
    wrap.className = 'mfi'; wrap.setAttribute('role', 'group'); wrap.setAttribute('aria-label', opts.label || 'Your answer as a fraction');
    function box(label) {
      var el = document.createElement('input');
      el.type = 'text'; el.className = 'mfi-in'; el.setAttribute('inputmode', 'numeric');
      el.autocomplete = 'off'; el.spellcheck = false; el.setAttribute('maxlength', '3');
      el.setAttribute('aria-label', label);
      return el;
    }
    var top = box('Top of the fraction (numerator)'), bar = document.createElement('span'), bot = box('Bottom of the fraction (denominator)');
    bar.className = 'mfi-bar'; bar.setAttribute('aria-hidden', 'true');
    wrap.appendChild(top); wrap.appendChild(bar); wrap.appendChild(bot);
    host.appendChild(wrap);
    var inputs = [top, bot];
    inputs.forEach(function (el) { el.addEventListener('input', function () { var c = digits(el.value); if (c !== el.value) el.value = c; }); });
    top.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); try { bot.focus({ preventScroll: true }); } catch (x) {} } });
    bot.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); host.dispatchEvent(new Event('fraction-submit', { bubbles: true })); } });
    return {
      inputs: inputs,
      raw: function () { var n = top.value.trim(), d = bot.value.trim(); return n === '' && d === '' ? '' : n + '/' + d; },
      filled: function () { return top.value.trim() !== '' && bot.value.trim() !== ''; },
      value: function () {
        var n = top.value.trim(), d = bot.value.trim();
        if (!/^\d+$/.test(n) || !/^\d+$/.test(d)) return null;
        n = parseInt(n, 10); d = parseInt(d, 10);
        return d === 0 ? null : { num: n, den: d };
      },
      clear: function () { top.value = ''; bot.value = ''; },
      mark: function (state) { wrap.classList.toggle('right', state === 'right'); wrap.classList.toggle('wrong', state === 'wrong'); }
    };
  }

  root.MaffsFractionInput = { mount: mount };
})(typeof window !== 'undefined' ? window : globalThis);
