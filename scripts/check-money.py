#!/usr/bin/env python3
"""SR-33 R4 (Jon, 13 Oct 2026): money is shown to the penny, from the unrounded value.

    python scripts/check-money.py              # CI: the source rule and the generated-output rule
    python scripts/check-money.py --selftest   # a planted fault in each must fail; the tree as it is must pass
    python scripts/check-money.py --root <copy of the repo>

A displayed money amount (£ or €) is a whole number or has exactly two decimals. "€66.6" (a value
printed as a JS number) and "£190.40" for a true £190.42 (a 3 s.f. key padded with a zero) are the same
class: the string was built from a rounded or unformatted value. Two parts:

  1. SOURCE. Every games/**/*.html and *.js and escape-rooms/**/*.html and *.js (the extracted banks and
     every literal in a page): a £/€ amount with a decimal part must have exactly two decimals.
     KNOWN lists the amounts that are not money to the penny (a growth factor, a figure in trillions, a
     comment); a new hit fails, and so does a KNOWN entry the file no longer has (the list stays true).
  2. GENERATED OUTPUT. A string built at run time cannot be read from the source (`€${ans}` is a bare
     variable), so split-it's generators are run on the page, both levels, every mode, 300 questions each
     (seeded), and the prompt, working, hint and every other string of every question are read for the same rule.

The recomputation of a pence figure against its data (stat-attack's closing lines) is that game's verifier's
job (scripts/verify-stat-attack.py): it holds every printed decimal to the UNROUNDED mean and SD.
Adding a game that builds money at run time: add it to GENERATED below.
"""
import argparse, glob, os, pathlib, re, sys, tempfile

BASE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / 'scripts'))

GLOBS = ('games/**/*.html', 'games/**/*.js', 'escape-rooms/**/*.html', 'escape-rooms/**/*.js')
MONEY = re.compile(r'[£€]\s?\d[\d,]*\.(\d+)')

# (file, matched text) -> count. Not money to the penny; each says why.
KNOWN = {
    ('games/standard-form-blitz/index.html', '£2.5'): 1,   # £2.5 x 10^12: a figure in trillions, in KaTeX
    ('games/growth-and-decay/index.html', '£1.045'): 1,    # a wrong option: the growth FACTOR written as an amount
    ('games/estimation-engine/index.html', '£20.0'): 1,    # a code comment quoting the wrong form
}

# Generators run on the page: slug -> (generators object, modes, levels).
GENERATED = {
    'split-it': ('generators', ['simplify', 'equivalent', 'divide', 'fractions', 'scale', 'unitary'], ['ks3', 'gcse']),
}

SEEDED = """(seed) => {
  let a = seed >>> 0;
  Math.random = function () {
    a = (a + 0x6D2B79F5) >>> 0; let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}"""
GENERATE = """([obj, mode, level, n, seed]) => {
  (%s)(seed);
  const out = [];
  for (let i = 0; i < n; i++) {
    const q = window[obj] ? window[obj][mode](level) : eval(obj)[mode](level);
    const strings = [];
    (function walk(v, d) {
      if (typeof v === 'string') strings.push(v);
      else if (Array.isArray(v) && d < 4) v.forEach(x => walk(x, d + 1));
      else if (v && typeof v === 'object' && d < 4) Object.values(v).forEach(x => walk(x, d + 1));
    })(q, 0);
    out.push(strings);
  }
  return out;
}""" % SEEDED


def bad(text):
    """Money tokens in text whose decimal part is not exactly two digits."""
    return [m.group(0) for m in MONEY.finditer(text) if len(m.group(1)) != 2]


def source_hits(root):
    hits = {}
    for pat in GLOBS:
        for f in glob.glob(str(root / pat), recursive=True):
            rel = os.path.relpath(f, root).replace(os.sep, '/')
            try:
                text = open(f, encoding='utf-8').read()
            except (OSError, UnicodeDecodeError):
                continue
            for tok in bad(text):
                hits[(rel, tok)] = hits.get((rel, tok), 0) + 1
    return hits


def check_source(root):
    fails = []
    hits = source_hits(root)
    for key, n in sorted(hits.items()):
        if n > KNOWN.get(key, 0):
            fails.append('%s: %r is a money amount without exactly two decimals (%d x; KNOWN allows %d)'
                         % (key[0], key[1], n, KNOWN.get(key, 0)))
    for key, n in sorted(KNOWN.items()):
        if hits.get(key, 0) < n:
            fails.append('%s: KNOWN lists %r x%d but the file has %d: lower or remove the entry'
                         % (key[0], key[1], n, hits.get(key, 0)))
    return fails


def check_generated(root, per=300):
    from playwright.sync_api import sync_playwright
    import bank_common as bc
    fails = []
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for slug, (obj, modes, levels) in GENERATED.items():
                page = browser.new_page()
                errors = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                if root != BASE:   # a planted copy is served in place of the real page
                    page.route(re.compile(r'^https?://(?!127\.0\.0\.1)'), lambda route: route.abort())
                    body = (root / 'games' / slug / 'index.html').read_text(encoding='utf-8')
                    page.route('**/games/%s/' % slug, lambda route: route.fulfill(
                        status=200, content_type='text/html; charset=utf-8', body=body))
                page.goto('%s/games/%s/' % (base.rstrip('/'), slug), wait_until='domcontentloaded')
                page.evaluate('() => { window.setTimeout = function () { return 0; }; }')
                seen = set()
                for mi, mode in enumerate(modes):
                    for li, level in enumerate(levels):
                        for strings in page.evaluate(GENERATE, [obj, mode, level, per, 4000 + 17 * mi + li]):
                            for s in strings:
                                for tok in bad(s):
                                    k = (slug, mode, level, tok)
                                    if k not in seen:
                                        seen.add(k)
                                        fails.append('%s %s/%s generated %r in %r: a money amount must have exactly two decimals'
                                                     % (slug, mode, level, tok, re.sub(r'<[^>]+>', '', s)[:100]))
                for e in errors:
                    fails.append('%s: page error %s' % (slug, e))
                page.close()
            browser.close()
    finally:
        proc.terminate()
        proc.wait()
    return fails


def check(root):
    return check_source(root) + check_generated(root)


def selftest():
    """The tree passes; a planted fault in each part must fail."""
    ok = True
    fails = check(BASE)
    print('tree as it is: %s' % ('PASS' if not fails else 'FAIL'))
    for f in fails[:10]:
        print('  ' + f)
    ok = ok and not fails

    def plant(name, rel, old, new, part):
        nonlocal ok
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            for pat in GLOBS:
                for f in glob.glob(str(BASE / pat), recursive=True):
                    dst = root / os.path.relpath(f, BASE)
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    dst.write_bytes(open(f, 'rb').read())
            target = root / rel
            text = target.read_text(encoding='utf-8')
            if old not in text:
                print('self-test %-34s *** CANNOT PLANT: %r not in %s ***' % (name, old, rel))
                ok = False
                return
            target.write_text(text.replace(old, new, 1), encoding='utf-8')
            got = part(root)
        print('self-test %-34s %s' % (name, ('caught: ' + got[0][:110]) if got else '*** MISSED ***'))
        ok = ok and bool(got)

    # the old split-it line: a rate and an answer printed as JS numbers ("€66.6")
    plant('split-it working unformatted', 'games/split-it/index.html',
          '£${amt} × ${rate.toFixed(2)} = €${(amt*rate).toFixed(2)}', '£${amt} × ${rate} = €${ans}', check_generated)
    plant('source: a price to one decimal', 'games/stat-attack/index.html',
          '£10.79', '£10.8', check_source)
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--root', default=str(BASE))
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    fails = check(pathlib.Path(a.root))
    for f in fails:
        print('FAIL ' + f)
    print('PASS' if not fails else 'FAILED: %d' % len(fails))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
