#!/usr/bin/env python3
# ci-line: Shared child-look fragment rule (schools/assets/kids-look.js, MaffsKids in Chromium: #kids and #kids/<Name> as both games read them before CLASS-PAGE, the bare #<Name> of the class page, the name rule, no second "Class", the links' fragments, nothing stored or sent; the class page greeting by textContent and its cards' links; four planted faults caught) | --selftest && --run
# ci-deps: schools/assets/kids-look.js class/index.html
"""Browser test for MaffsKids, schools/assets/kids-look.js (contract CLASS-PAGE, 21 Nov 2026; canon §7.5.9).

    python scripts/test-kids-look.py --run        # the cases below, in headless Chromium
    python scripts/test-kids-look.py --selftest   # the same cases against four planted faults: each must FAIL

  rule       MaffsKids.read(hash) on every case in CASES, and on 400 generated fragments, gives exactly what the two
             games' own copy of the rule gave before CLASS-PAGE (OLD_RULE below, verbatim from
             games/sums-in-disguise/index.html at 7d827fa; some-thingies' copy was byte-identical): the look, and the
             class name or none. CASES also states each expected answer, so the old rule is not the only judge.
  bare       MaffsKids.read(hash, {bare: true}): "#Maple" is the name Maple, never the child look; "#kids/Maple", "",
             "#<script>", a fragment that will not decode and a 21-letter name give no name.
  greeting   "Welcome, {name} Class!" with Maple, "Maple Class", "maple class" and "Classic": Class never twice.
  links      gameHash(name) is "#kids/<encoded>" or "#kids"; classHash(name) "#<encoded>" or "".
  private    with every storage, network and cookie route watched, nothing is written or sent by any call above;
             and the file's source names no storage, network, cookie, innerHTML or analytics call.
  page       /class/#Maple greets "Welcome, Maple Class!" (textContent: the paragraph holds no element), hides the
             teachers' line, and links each card to /games/<slug>/#kids/Maple; /class/ and /class/#<script> show no
             greeting, show the teachers' line and link with #kids; a hash change re-reads the name; nothing stored.

Exits non-zero on any failure.
"""
import argparse
import json
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

ASSET = os.path.join(ROOT, 'schools', 'assets', 'kids-look.js')

# The rule both games carried until CLASS-PAGE, verbatim (sums-in-disguise :363-381 at 7d827fa), wrapped as a function.
OLD_RULE = r"""
window.oldRule = function (hash) {
  var LOOK = 'grown', CLASS_NAME = null;
  try {
    var frag = String(hash || '').replace(/^#/, '');
    var low = frag.toLowerCase();
    if (low === 'kids') LOOK = 'kids';
    else if (low.indexOf('kids/') === 0) {
      LOOK = 'kids';
      var nm = decodeURIComponent(frag.slice(5)).trim();
      if (/^[\p{L}' ’-]{1,20}$/u.test(nm) && /\p{L}/u.test(nm)) CLASS_NAME = nm;
    }
  } catch (e) { CLASS_NAME = null; }
  return { kids: LOOK === 'kids', name: CLASS_NAME };
};
window.oldGreeting = function (template, CLASS_NAME) {
  var g = template.replace('{name}', CLASS_NAME);
  if (/class$/i.test(CLASS_NAME)) g = g.replace(/(class)\s+class\b/i, '$1');
  return g;
};
"""

# (fragment, kids, name): the games' rule, stated.
CASES = [
    ('', False, None), ('#', False, None), ('#kidsx', False, None), ('#kid', False, None), ('#Maple', False, None),
    ('#kids', True, None), ('#KIDS', True, None), ('#Kids', True, None), ('#kids/', True, None),
    ('#kids/Maple', True, 'Maple'), ('#KIDS/Maple', True, 'Maple'), ('#kids/Maple%20Class', True, 'Maple Class'),
    ('#kids/%20Maple%20', True, 'Maple'), ('#kids/%20%20', True, None), ('#kids/--', True, None),
    ("#kids/O'Neil", True, "O'Neil"), ('#kids/O%E2%80%99Neil', True, 'O’Neil'), ('#kids/Saint-Jean', True, 'Saint-Jean'),
    ('#kids/%C3%89lan', True, 'Élan'), ('#kids/Maple2', True, None), ('#kids/Maple.', True, None),
    ('#kids/' + 'a' * 20, True, 'a' * 20), ('#kids/' + 'a' * 21, True, None),
    ('#kids/<script>', True, None), ('#kids/%3Cscript%3Ealert(1)%3C%2Fscript%3E', True, None),
    ('#kids/%E0%A4%A', True, None), ('#kids/Maple/Oak', True, None), ('kids/Maple', True, 'Maple'),
]
BARE = [
    ('#Maple', 'Maple'), ('Maple', 'Maple'), ('#Maple%20Class', 'Maple Class'), ('#%20Maple', 'Maple'),
    ('#O%E2%80%99Neil', 'O’Neil'), ('', None), ('#', None), ('#kids/Maple', None), ('#kids', 'kids'),
    ('#<script>', None), ('#%3Cb%3E', None), ('#%E0%A4%A', None), ('#' + 'b' * 21, None), ('#--', None), ('#Maple1', None),
]
GREETINGS = [('Maple', 'Welcome, Maple Class!'), ('Maple Class', 'Welcome, Maple Class!'),
             ('maple class', 'Welcome, maple class!'), ('Classic', 'Welcome, Classic Class!'),
             ("O'Neil", "Welcome, O'Neil Class!")]
HASHES = [('Maple', '#kids/Maple', '#Maple'), ('Maple Class', '#kids/Maple%20Class', '#Maple%20Class'),
          ('O’Neil', '#kids/O%E2%80%99Neil', '#O%E2%80%99Neil'), (None, '#kids', ''), ('<b>', '#kids', ''),
          ('', '#kids', ''), ('a' * 21, '#kids', '')]
FORBIDDEN = re.compile(r'localStorage|sessionStorage|indexedDB|fetch\s*\(|XMLHttpRequest|sendBeacon|cookie|innerHTML|'
                       r'\bmfg\b|\bgtag\b|WebSocket|postMessage')

WATCH = r"""
window.__leaks = [];
(function () {
  var note = function (what) { return function () { window.__leaks.push(what + ' ' + [].slice.call(arguments).join(',')); }; };
  var S = Storage.prototype, si = S.setItem;
  S.setItem = function (k, v) { window.__leaks.push('storage ' + k + '=' + v); return si.apply(this, arguments); };
  var f = window.fetch; window.fetch = function (u) { window.__leaks.push('fetch ' + u); return f.apply(this, arguments); };
  var o = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (m, u) { window.__leaks.push('xhr ' + u); return o.apply(this, arguments); };
  if (navigator.sendBeacon) { var b = navigator.sendBeacon.bind(navigator); navigator.sendBeacon = function (u) { window.__leaks.push('beacon ' + u); return b.apply(null, arguments); }; }
  var d = Object.getOwnPropertyDescriptor(Document.prototype, 'cookie');
  Object.defineProperty(document, 'cookie', { get: function () { return d.get.call(document); }, set: function (v) { window.__leaks.push('cookie ' + v); d.set.call(document, v); } });
  window.mfg = note('mfg'); window.gtag = note('gtag');
})();
"""

# Planted faults for --selftest: (name, (old, new) in kids-look.js, the section that must fail).
PLANTS = [
    ('a name with no letter accepted', ("&& /\\p{L}/u.test(nm);", ";"), 'rule'),
    ('a second "Class" left in the greeting', ("    if (/class$/i.test(name)) g = g.replace(/(class)\\s+class\\b/i, '$1');\n", ''), 'greeting'),
    ('the name written to storage', ("        if (valid(nm)) out.name = nm;", "        if (valid(nm)) { out.name = nm; try { localStorage.setItem('kids-name', nm); } catch (e) {} }"), 'private'),
    ('the bare name read as the child look', ("    var out = { kids: false, name: null };", "    var out = { kids: !!(opts && opts.bare), name: null };"), 'bare'),
]


def fragments(n=400, seed=52):
    """Generated fragments around the rule's edges: prefixes, letters, digits, marks, encodings, lengths."""
    rnd = random.Random(seed)
    parts = ['a', 'Z', 'é', 'Ω', ' ', '-', "'", '’', '1', '.', '/', '<', '%20', '%E2%80%99', '%41', '%', '%zz', 'class', 'Class']
    out = []
    for _ in range(n):
        head = rnd.choice(['#kids/', '#KIDS/', '#kids', '#kid/', '#', '', 'kids/', '#Kids/'])
        out.append(head + ''.join(rnd.choice(parts) for _ in range(rnd.randint(0, 24))))
    return out


def run(js_text):
    """{section: [fault]} for kids-look.js given as text."""
    from playwright.sync_api import sync_playwright
    bad = {k: [] for k in ('rule', 'bare', 'greeting', 'links', 'private', 'page')}
    for m in FORBIDDEN.finditer(re.sub(r'/\*.*?\*/', '', js_text, flags=re.S)):
        bad['private'].append('kids-look.js names %r' % m.group(0))
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        page = br.new_page()
        page.set_content('<!doctype html><meta charset="utf-8"><body></body>')
        page.add_script_tag(content=WATCH)
        page.add_script_tag(content=OLD_RULE)
        page.add_script_tag(content=js_text)
        frs = [c[0] for c in CASES] + fragments()
        got = page.evaluate('(fs) => fs.map(f => [MaffsKids.read(f), oldRule(f)])', frs)
        stated = {c[0]: (c[1], c[2]) for c in CASES}
        for f, (new, old) in zip(frs, got):
            if new != old:
                bad['rule'].append('read(%r) is %s; the games read %s' % (f, json.dumps(new), json.dumps(old)))
            if f in stated and (new.get('kids'), new.get('name')) != stated[f]:
                bad['rule'].append('read(%r) is %s, expected kids %s name %r' % (f, json.dumps(new), stated[f][0], stated[f][1]))
        dflt = page.evaluate('() => { location.hash = "kids/Maple"; var r = MaffsKids.read(); location.hash = ""; return r; }')
        if dflt != {'kids': True, 'name': 'Maple'}:
            bad['rule'].append('read() with no argument does not read location.hash: %s' % dflt)
        for f, want in BARE:
            r = page.evaluate('(f) => MaffsKids.read(f, {bare: true})', f)
            if r != {'kids': False, 'name': want}:
                bad['bare'].append('read(%r, {bare}) is %s, expected name %r and never the child look' % (f, json.dumps(r), want))
        for name, want in GREETINGS:
            r = page.evaluate('([n]) => [MaffsKids.greeting("Welcome, {name} Class!", n), oldGreeting("Welcome, {name} Class!", n)]', [name])
            if r[0] != want or r[0] != r[1]:
                bad['greeting'].append('greeting(%r) is %r, expected %r (the games gave %r)' % (name, r[0], want, r[1]))
        for name, gh, ch in HASHES:
            r = page.evaluate('(n) => [MaffsKids.gameHash(n), MaffsKids.classHash(n)]', name)
            if r != [gh, ch]:
                bad['links'].append('gameHash/classHash(%r) are %s, expected %s' % (name, r, [gh, ch]))
        leaks = page.evaluate('() => window.__leaks')
        if leaks:
            bad['private'].append('stored or sent: %s' % leaks[:3])
        br.close()
        proc, base = bc.start_stub_server()
        try:
            br = pw.chromium.launch()
            ctx = br.new_context(viewport={'width': 390, 'height': 844})
            bc.offline(ctx, base)
            ctx.add_init_script(WATCH)
            ctx.route(base + '/schools/assets/kids-look.js',
                      lambda route: route.fulfill(status=200, content_type='application/javascript', body=js_text))
            STATE = ('() => [document.getElementById("welcome").textContent, document.getElementById("welcome").children.length,'
                     ' document.getElementById("teacherNote").hidden,'
                     ' [...document.querySelectorAll("a.kid-card")].map(a => [a.getAttribute("href"), a.dataset.slug]), window.__leaks,'
                     ' JSON.stringify(Object.assign({}, localStorage, sessionStorage))]')
            for frag, greet, note, tail in (('#Maple', 'Welcome, Maple Class!', True, '#kids/Maple'), ('', '', False, '#kids'),
                                            ('#%3Cscript%3E', '', False, '#kids'), ('#Maple%20Class', 'Welcome, Maple Class!', True, '#kids/Maple%20Class')):
                pg = ctx.new_page()
                pg.goto(base + '/class/' + frag, wait_until='load')
                text, kids_el, hidden, hrefs, leaks, stored = pg.evaluate(STATE)
                where = '/class/%s' % frag
                if text != greet or kids_el:
                    bad['page'].append('%s: the greeting reads %r (%d elements), expected %r as text' % (where, text, kids_el, greet))
                if hidden != note:
                    bad['page'].append('%s: the teachers\' line is %s' % (where, 'hidden' if hidden else 'shown'))
                if not hrefs or any(h != '/games/%s/%s' % (s, tail) for h, s in hrefs):
                    bad['page'].append('%s: the cards link to %s, expected /games/<slug>/%s' % (where, hrefs, tail))
                if leaks or 'Maple' in stored:
                    bad['page'].append('%s: stored or sent %s %s' % (where, leaks[:2], stored[:80]))
                if frag == '':
                    pg.evaluate('() => { location.hash = "Maple"; }')
                    pg.wait_for_timeout(100)
                    text, _, hidden, hrefs, _, _ = pg.evaluate(STATE)
                    if text != 'Welcome, Maple Class!' or not hidden or any(h != '/games/%s/#kids/Maple' % s for h, s in hrefs):
                        bad['page'].append('/class/ then #Maple typed in: greeting %r, links %s' % (text, hrefs))
                pg.close()
            br.close()
        finally:
            proc.terminate()
            proc.wait()
    return bad


def report(bad):
    n = 0
    for sec, faults in bad.items():
        print('  %-9s %s' % (sec, 'PASS' if not faults else 'FAIL (%d)' % len(faults)))
        for f in faults[:6]:
            print('      ' + f)
        n += len(faults)
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    js = open(ASSET, encoding='utf-8').read()
    rc = 0
    if args.selftest:
        missed = []
        for name, (old, new), section in PLANTS:
            if js.count(old) != 1:
                missed.append('%s: its text is not in kids-look.js once' % name)
                continue
            bad = run(js.replace(old, new))
            hit = bool(bad[section])
            print('  self-test %-40s %s' % (name, 'caught: ' + bad[section][0][:90] if hit else '*** MISSED ***'))
            if not hit:
                missed.append(name)
        for m in missed:
            print('FAIL  self-test: ' + m)
        print('self-test: %s' % ('FAILED' if missed else 'PASS'))
        rc = 1 if missed else 0
    if args.run or not args.selftest:
        print('MaffsKids (schools/assets/kids-look.js):')
        n = report(run(js))
        print('FAILED (%d)' % n if n else 'PASS')
        rc = rc or (1 if n else 0)
    return rc


if __name__ == '__main__':
    sys.exit(main())
