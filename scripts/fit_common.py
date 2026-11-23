#!/usr/bin/env python3
# ci-line: Fold sweep helper (scripts/fit_common.py: one fold measurement and an every-item sweep for the game verifiers; a fixture whose Next sits 20 px below the fold on one item only is caught, the rest pass) | --selftest
"""The fold check the game verifiers share (contract PRIMARY-FIT-SWEEP, 23 Nov 2026).

Sums in Disguise and Some Thingies each carried a copy of FIT_JS and fit(), and called fit() only on the first two items
of a shuffled run with a random right-answer line, so each CI run measured a different sample. Main's first run on
661f822 found a real overflow (a Stage 5 kids-look Next at 616 px against a 600 px fold) and the re-run drew other items
and passed. This module is the one copy, and it measures every item, not a sample.

  MEASURE_JS   the page-side measurement for a selector: the fold (window.innerHeight less a fixed .site-footer's height),
               the lowest bottom of the visible elements the selector matches (page coordinates, scrolled to the top),
               sideways scroll, and optionally a picture wider than its card (null-safe where the page has neither).
  fit()        one measurement, its failures appended to `out` (the verifiers' existing call shape).
  open_phone() a page as a phone shows it: 360 x 640 by default, touch, the real fonts (scripts/fonts/, the pinned copies
               bank_common serves), a mocked speechSynthesis with one LOCAL voice so a read-aloud speaker shows, reduced
               motion (every animation lands at once, so the settled layout is what is measured), the lock's fresh window
               and MaffsNext's floor at 0, mfg() and submitScore recorded, never sent.
  sweep()      every item, every variant: the verifier hands it item ids and a JS stepper,
                   { variants(id) -> [v, ...], run(id, v, m) }   (run may be async)
               where run() puts the item on screen (the game's preview hook), walks it step by step and calls
               m(selector, what) at every control it must see above the fold. Every m() call is measured; the sweep fails
               an item with no measurement, a selector with nothing on screen, a control below the fold, sideways scroll
               and (with pic) a picture wider than its card. It returns its counts, so a verifier can say what it covered.
               Every measurement first runs MaffsFold.decide() (fold.js lays options two to a row a frame later; this is
               the same call, made now); one variant in 20 is measured again after two frames, and a layout that moved
               in between fails, so a measurement can never pass on a frame no student sees.

    python scripts/fit_common.py --selftest    # the fixture: Next 20 px below the fold on one item only is caught
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

PHONE = (360, 640)

# One function, used by fit() (one call) and by sweep() (inside the page, at every step).
MEASURE_JS = r"""function (sel, pic) {
  // MaffsFold (schools/assets/fold.js) lays answer options two to a row one frame after they appear; its decide() is the
  // same call, made now, so what is measured is the settled layout a student sees, not the frame before it.
  if (window.MaffsFold && MaffsFold.decide) document.querySelectorAll('.maffs-options').forEach(b => MaffsFold.decide(b));
  window.scrollTo(0, 0);
  const f = document.querySelector('.site-footer');
  const fixed = !!f && getComputedStyle(f).position === 'fixed';
  const fold = window.innerHeight - (fixed ? f.getBoundingClientRect().height : 0);
  const els = [...document.querySelectorAll(sel)].filter(e => e.getBoundingClientRect().height > 0);
  const bottom = els.length ? Math.max(...els.map(e => e.getBoundingClientRect().bottom + window.scrollY)) : null;
  let picOut = false;
  if (pic) {
    const p = document.querySelector(pic[0]), c = document.querySelector(pic[1]);
    if (p && c) {
      const a = p.getBoundingClientRect(), b = c.getBoundingClientRect();
      picOut = a.width > 0 && (a.right > b.right + 0.5 || a.left < b.left - 0.5);
    }
  }
  return { n: els.length, bottom: bottom, fold: fold, sw: document.documentElement.scrollWidth, vw: window.innerWidth, picOut: picOut };
}"""
FIT_JS = '(a) => (%s)(a.sel, a.pic)' % MEASURE_JS


def faults(f, sel, what, pic=None):
    """The failures in one measurement."""
    out = []
    if not f['n']:
        out.append('%s: nothing on screen for %s' % (what, sel))
    elif f['bottom'] > f['fold'] + 0.5:
        out.append('%s: %s ends at %.0f px, below the fold at %.0f px' % (what, sel, f['bottom'], f['fold']))
    if f['sw'] > f['vw']:
        out.append('%s: the page scrolls sideways (%d > %d)' % (what, f['sw'], f['vw']))
    if pic and f.get('picOut'):
        out.append('%s: the picture is wider than the card' % what)
    return out


def fit(page, sel, what, out, pic=None):
    """Measure `sel` on the page as it is now; append any failure to `out`. pic: (picture, card) selectors, or None."""
    out.extend(faults(page.evaluate(FIT_JS, {'sel': sel, 'pic': list(pic) if pic else None}), sel, what, pic))


# A speechSynthesis with one local voice, there from the first script: a read-aloud speaker shows, as on a phone with an
# on-device voice. Nothing is spoken (speak() records only).
LOCAL_VOICE_INIT = r"""(() => {
  const voices = [{ name: 'Device GB', lang: 'en-GB', localService: true, default: true, voiceURI: 'device-gb' }];
  window.__spokenFit = [];
  const synth = { getVoices() { return voices.slice(); }, speak(u) { window.__spokenFit.push(u && u.text); },
    cancel() {}, pause() {}, resume() {}, speaking: false, pending: false, paused: false,
    addEventListener() {}, removeEventListener() {}, onvoiceschanged: null };
  Object.defineProperty(window, 'speechSynthesis', { value: synth, configurable: true });
  window.SpeechSynthesisUtterance = function (t) { this.text = t; this.voice = null; this.lang = ''; };
})();"""

RECORD_INIT = r"""(() => { window.__ev = [];
  Object.defineProperty(window, 'mfg', { configurable: true,
    get() { return function (n, p) { window.__ev.push([n, JSON.parse(JSON.stringify(p || {}))]); }; }, set(v) {} }); })();"""


def open_phone(pw, base, html, slug, ready, frag='', size=PHONE, voice=True, query='?cb=fit'):
    """(browser, page, errors) for the game page `html` served at /games/<slug>/ as a phone shows it (see the docstring).
    ready: a JS expression true once the game's hooks are there."""
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    ctx.add_init_script(RECORD_INIT)
    if voice:
        ctx.add_init_script(LOCAL_VOICE_INIT)
    bc.offline(ctx, base)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % re.escape(slug))
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    ctx.route(lambda url: bc.is_font_cdn(url), bc.serve_real_font)
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/%s%s' % (slug, query, frag), wait_until='load', timeout=30000)
    page.wait_for_function(ready, timeout=15000)
    page.emulate_media(reduced_motion='reduce')
    page.evaluate("""() => { window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = () => Promise.resolve(); }""")
    return br, page, errors


SWEEP_JS = r"""async ({ ids, pic, stepper, every }) => {
  const measure = (%s);
  const S = (0, eval)('(' + stepper + ')');
  const frames = () => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
  const rows = [];
  let n = 0;
  for (const id of ids) {
    let vs;
    try { vs = S.variants(id); } catch (e) { rows.push({ id: id, v: null, pts: [], err: 'variants: ' + e }); continue; }
    for (const v of vs) {
      const pts = [];
      let err = null;
      try { await S.run(id, v, (sel, what) => { pts.push(Object.assign({ sel: sel, what: what }, measure(sel, pic))); }); }
      catch (e) { err = String(e && e.stack || e).split('\n')[0]; }
      // One variant in `every`: the last control measured again after two frames, so a layout the page changes later
      // (a frame callback, an observer) than the measurement shows up as a difference, never as a pass.
      let late = null;
      if (!err && pts.length && every && n %% every === 0) {
        await frames();
        const last = pts[pts.length - 1], again = measure(last.sel, pic);
        if (Math.abs((again.bottom || 0) - (last.bottom || 0)) > 0.5) late = { was: last.bottom, now: again.bottom, what: last.what };
      }
      n++;
      rows.push({ id: id, v: v, pts: pts, err: err, late: late });
    }
  }
  return rows;
}""" % MEASURE_JS


def sweep(page, ids, stepper, out, tag, pic=None, chunk=25, warm=None, every=20):
    """Every item in `ids`, every variant the stepper gives, measured at every step it marks. Failures go to `out`,
    each led by `tag`, the item id and the variant. Returns {'items', 'variants', 'measures', 'worst'}: worst is the
    largest bottom less fold seen (negative: everything above the fold)."""
    ids = list(ids)
    arg = {'pic': list(pic) if pic else None, 'stepper': stepper, 'every': 0}
    # The faces the sweep draws in (text, KaTeX), loaded before anything is measured.
    page.evaluate(SWEEP_JS, dict(arg, ids=list(warm if warm is not None else ids[::max(1, len(ids) // 12)])))
    bc.wait_settled(page)
    stats = {'items': 0, 'variants': 0, 'measures': 0, 'worst': None}
    seen = set()
    for i in range(0, len(ids), chunk):
        for r in page.evaluate(SWEEP_JS, dict(arg, ids=ids[i:i + chunk], every=every)):
            lab = '%s %s%s' % (tag, r['id'], '' if r['v'] is None else ' [%s]' % (r['v'] if isinstance(r['v'], str) else json.dumps(r['v'])))
            stats['variants'] += 1
            if r['err']:
                out.append('%s: the sweep threw: %s' % (lab, r['err'][:200]))
            if r.get('late'):
                out.append('%s (%s): the layout moved after it was measured (%.0f px, then %.0f px two frames later)'
                           % (lab, r['late']['what'], r['late']['was'] or 0, r['late']['now'] or 0))
            if not r['pts']:
                out.append('%s: nothing was measured' % lab)
                continue
            seen.add(r['id'])
            for p in r['pts']:
                stats['measures'] += 1
                if p['n'] and p['bottom'] is not None:
                    d = p['bottom'] - p['fold']
                    stats['worst'] = d if stats['worst'] is None else max(stats['worst'], d)
                out.extend(faults(p, p['sel'], '%s (%s)' % (lab, p['what']), pic))
    stats['items'] = len(seen)
    missing = [x for x in ids if x not in seen]
    if missing:
        out.append('%s: %d item(s) never measured: %s' % (tag, len(missing), ', '.join(map(str, missing[:8]))))
    return stats


# ---------------------------------------------------------------- self-test: a fixture page
FIXTURE = r"""<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;font:16px sans-serif}.site-footer{position:fixed;left:0;right:0;bottom:0;height:40px;background:#eee}
#card{padding:8px}#pad{background:#ddd}#opts{height:22px;overflow:hidden}#next{display:block;height:44px;width:120px;margin:0;padding:0;box-sizing:border-box}</style></head>
<body><div id="card"><div id="pad"></div><div id="opts"><button class="opt">1</button></div><button id="next">Next</button></div>
<footer class="site-footer">footer</footer>
<script>
  // Items a to e. With the plant, item c's feedback is tall enough that Next ends 20 px below the 600 px fold, and only
  // after a wrong answer: the sampled check this module replaces would miss it on most runs.
  window.FX = { plant: false, late: false, show: function (id, v) {
    var next = document.getElementById('next'), pad = document.getElementById('pad');
    next.hidden = v === 'ask';
    pad.style.height = '200px';
    if (v !== 'ask') {
      var h = 600 - 8 - 22 - 44 - 30;                     // Next ends 30 px above the fold
      if (FX.plant && id === 'c' && v === 'wrong') h += 50; // ... or 20 px below it
      pad.style.height = h + 'px';
      // The late plant: on item e the layout grows a frame after it is drawn (as a frame callback in a page would).
      if (FX.late && id === 'e' && v === 'right') requestAnimationFrame(function () { pad.style.height = (h + 10) + 'px'; });
    }
  } };
</script></body></html>"""
FIXTURE_STEPPER = r"""{
  variants: (id) => ['right', 'wrong'],
  run: async (id, v, m) => { FX.show(id, 'ask'); m('#opts .opt', 'the options'); FX.show(id, v); m('#next', 'Next'); }
}"""


def selftest():
    from playwright.sync_api import sync_playwright
    fails = []
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        try:
            page = br.new_page(viewport={'width': PHONE[0], 'height': PHONE[1]})
            page.set_content(FIXTURE)
            for plant in (False, True):
                page.evaluate('(p) => { FX.plant = p; }', plant)
                got = []
                st = sweep(page, list('abcde'), FIXTURE_STEPPER, got, 'fixture')
                if st['items'] != 5 or st['variants'] != 10 or st['measures'] != 20:
                    fails.append('fixture%s: the sweep covered %s, expected 5 items, 10 variants, 20 measures' % (' (planted)' if plant else '', st))
                if not plant and got:
                    fails.append('fixture: a clean page failed: %s' % got[0])
                if plant:
                    hit = [g for g in got if re.search(r'^fixture c \[wrong\] \(Next\): #next ends at 620 px, below the fold at 600 px$', g)]
                    if len(got) != 1 or not hit:
                        fails.append('fixture (planted, Next 20 px below the fold on item c after a wrong answer only): got %s' % (got or 'nothing'))
                    else:
                        print('  self-test %-58s caught: %s' % ('Next 20 px below the fold on one item only', hit[0]))
            # fit() itself: the same plant in one call, and a page with no picture is null-safe with pic given.
            page.evaluate("() => { FX.plant = true; FX.show('c', 'wrong'); }")
            one = []
            fit(page, '#next', 'fixture fit()', one, pic=('#pic', '#qcard'))
            if one != ['fixture fit(): #next ends at 620 px, below the fold at 600 px']:
                fails.append('fit(): got %s' % one)
            none = []
            fit(page, '#nothing', 'fixture fit()', none)
            if none != ['fixture fit(): nothing on screen for #nothing']:
                fails.append('fit() with nothing on screen: got %s' % none)
            # A layout that moves a frame after it was measured is failed, never passed (every variant re-measured here).
            page.evaluate("() => { FX.plant = false; FX.late = true; }")
            late = []
            sweep(page, list('abcde'), FIXTURE_STEPPER, late, 'fixture', every=1)
            if len(late) != 1 or 'fixture e [right] (Next): the layout moved after it was measured (570 px, then 580 px two frames later)' not in late[0]:
                fails.append('a layout that moved after measuring: got %s' % (late or 'nothing'))
            else:
                print('  self-test %-58s caught: %s' % ('the layout moving a frame after it is measured', late[0]))
            page.evaluate("() => { FX.late = false; }")
            # A stepper that measures nothing for an item fails that item.
            empty = []
            sweep(page, ['a', 'b'], "{ variants: (id) => ['x'], run: (id, v, m) => { if (id === 'a') m('#next', 'Next'); } }", empty, 'fixture')
            if not any('fixture b [x]: nothing was measured' in g for g in empty):
                fails.append('an item with no measurement was not failed: %s' % empty)
        finally:
            br.close()
    for f in fails:
        print('FAIL  ' + f)
    print('FAILED' if fails else 'PASS')
    return 1 if fails else 0


if __name__ == '__main__':
    if sys.argv[1:] != ['--selftest']:
        sys.exit('usage: python scripts/fit_common.py --selftest')
    sys.exit(selftest())
