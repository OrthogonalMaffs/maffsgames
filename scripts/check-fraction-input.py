#!/usr/bin/env python3
# ci-line: Fraction input (a typed fraction is the shared stacked MaffsFractionInput, never a page's own boxes; shrink-only warn list; planted faults) | --selftest && --check
# ci-deps: games/ the-6-ps/ schools/assets/fraction-input.js scripts/fraction-input-warn.json
"""FRACTION-STACK (contract, 3 Nov 2026; canon 7.6.1): every fraction on screen is stacked, never 1/3, and a typed fraction answer
is the shared stacked input, MaffsFractionInput (schools/assets/fraction-input.js), never boxes a page builds for itself.

For every page under games/ and the-6-ps/ this check reads the page's own source (no browser) and fails a page that:
  - builds fraction boxes of its own: it has inputs, and either a label of its own naming a part of the fraction (a quoted string
    that STARTS "Top number", "Bottom number", "Top of the fraction", "Bottom of the fraction", "Numerator" or "Denominator", the
    way such boxes are labelled), or a separator element ("/", the fraction slash or a division sign) between two inputs; or
  - calls MaffsFractionInput without loading fraction-input.js.
The shared input's own labels live in fraction-input.js, so a page that uses it carries none of them. Prose is not read as a
label: a sentence that only mentions a numerator does not start with the word, and a stage name such as "Stage 1 · Same bottom
number" does not start with it either.

Warn first (canon 7.8.4): scripts/fraction-input-warn.json lists the pages not yet moved, each with its reason. A listed page
that still builds its own boxes WARNS; the list is shrink-only against the pull request's own base (adding a page fails), and an
entry whose page no longer fails is stale and fails, so the list cannot outlive the move. Seeded 3 Nov 2026 with the two pages
that need a whole-number box (mixed numbers) the shared input does not have yet: the-6-ps and how-many-parts.

  python scripts/check-fraction-input.py --check      the pages
  python scripts/check-fraction-input.py --selftest   planted faults: own side-by-side boxes fail; a warn-listed page warns;
                                                      adding to the warn list fails; and the cases around them
"""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import plant_common as pc

ROOT = Path(__file__).resolve().parent.parent
WARN = 'scripts/fraction-input-warn.json'
SCOPES = ('games', 'the-6-ps')
INITIAL_WARN = {'the-6-ps/index.html', 'games/how-many-parts/index.html'}

INPUT = re.compile(r"""<input\b|createElement\(\s*['"]input['"]\s*\)""", re.I)
# A label of the page's own for a part of a fraction: a quoted string that starts with the part's name.
LABEL = re.compile(r"""(['"])\s*((?:top|bottom)\s+(?:number|of\s+the\s+fraction)\b|numerator\b|denominator\b)[^'"\n]{0,60}\1""", re.I)
# JavaScript that builds markup in pieces ('...<input>' + '<span>/</span>...') is read joined.
JOIN = re.compile(r"""['"]\s*\+\s*['"]""")
SEP = re.compile(r"""<input\b[^>]*>(?:\s*</[a-z]+>)*\s*<(span|div|b|i|em|strong)\b[^>]*>\s*(?:/|&#47;|&#x2f;|&frasl;|⁄|÷|&divide;)\s*</\1>"""
                 r"""(?:\s*<[a-z]+\b[^>]*>)*\s*<input\b""", re.I)
LOADS = re.compile(r"""<script\b[^>]*\bsrc=["'][^"']*fraction-input\.js["']""", re.I)


def own_boxes(src):
    """What marks the page as building its own fraction boxes: (labels, separators). Both empty when it does not."""
    if not INPUT.search(src):
        return [], 0
    flat = JOIN.sub('', src)
    labels = sorted({m.group(0)[1:-1].strip() for m in LABEL.finditer(flat)})
    return labels, len(SEP.findall(flat))


def analyse(pages, listed_warn, base_warn):
    """pages: {path: source}. Returns (errors, warnings, pages using the shared input)."""
    errors, warnings, shared = [], [], 0
    warn = set(listed_warn)
    if len(warn) != len(listed_warn):
        errors.append('duplicate warn-list entries')
    for path in sorted(warn - set(base_warn)):
        errors.append('%s: adding to the warn list fails; it is shrink-only' % path)
    for path in sorted(warn - set(pages)):
        errors.append('%s: no such page; remove its stale warn-list entry' % path)
    for path in sorted(pages):
        src = pages[path]
        labels, seps = own_boxes(src)
        uses = 'MaffsFractionInput' in src
        if uses:
            shared += 1
            if not LOADS.search(src):
                errors.append('%s: calls MaffsFractionInput but does not load fraction-input.js' % path)
        if labels or seps:
            what = '; '.join(filter(None, ['its own labels %s' % labels if labels else '',
                                           '%d separator(s) between two inputs' % seps if seps else '']))
            msg = '%s: builds its own fraction boxes (%s): use MaffsFractionInput (schools/assets/fraction-input.js)' % (path, what)
            if path in warn:
                warnings.append(msg + ' [warn-listed]')
            else:
                errors.append(msg)
        elif path in warn:
            errors.append('%s: no longer builds its own fraction boxes; remove its stale warn-list entry' % path)
    return errors, warnings, shared


def pages(root=ROOT):
    out = {}
    for scope in SCOPES:
        for p in sorted((root / scope).rglob('*.html')):
            out[p.relative_to(root).as_posix()] = p.read_text(encoding='utf-8', errors='replace')
    return out


def read_warn(text):
    data = json.loads(text)
    if not isinstance(data, dict) or not isinstance(data.get('pages'), dict) or any(not isinstance(k, str) for k in data['pages']):
        raise ValueError('%s must be {"pages": {"<path>": "<reason>", ...}}' % WARN)
    return list(data['pages'])


def base_warn(root=ROOT, env=None):
    """The warn list on the pull request's own base (fail closed); outside a pull request, on the merge base with main.
    Before the list existed on the base: the seed."""
    env = os.environ if env is None else env
    if env.get('GITHUB_EVENT_NAME') == 'pull_request':
        event = json.loads(Path(env['GITHUB_EVENT_PATH']).read_text(encoding='utf-8'))
        base = event['pull_request']['base']['sha']
    else:
        base = subprocess.run(['git', 'merge-base', 'origin/main', 'HEAD'], cwd=root,
                              capture_output=True, text=True, check=True).stdout.strip()
    if subprocess.run(['git', 'cat-file', '-e', '%s^{commit}' % base], cwd=root, capture_output=True).returncode:
        subprocess.run(['git', 'fetch', '--no-tags', '--depth=1', 'origin', base], cwd=root,
                       capture_output=True, text=True, check=True)
    if not subprocess.run(['git', 'ls-tree', '--name-only', base, '--', WARN], cwd=root,
                          capture_output=True, text=True, check=True).stdout.strip():
        return sorted(INITIAL_WARN)
    return read_warn(subprocess.run(['git', 'show', '%s:%s' % (base, WARN)], cwd=root, capture_output=True, text=True,
                                    encoding='utf-8', check=True).stdout)


# ---------------------------------------------------------------- self-test
SHARED = ('<script src="../../schools/assets/fraction-input.js"></script>\n<div id="answer"></div>\n<script>\n'
          "  var a = document.getElementById('answer');\n"
          "  a.innerHTML = '<div class=\"ans-row\"><span id=\"fracHost\"></span>' + CHECK + '</div>';\n"
          "  var fi = MaffsFractionInput.mount(document.getElementById('fracHost'), { label: 'Your answer as a fraction' });\n"
          "  var stage = 'Stage 1 · Same bottom number', tip = 'The numerator is the top number.', why = 'Cancel the top and the bottom number.';\n"
          '</script>\n<p>The bottom number, the denominator, says how many parts.</p><input type="text" aria-label="Your answer">\n')
OWN = ("  a.innerHTML = '<div class=\"ans-row\"><span id=\"fracHost\"></span>' + CHECK + '</div>';\n"
       "  var fi = MaffsFractionInput.mount(document.getElementById('fracHost'), { label: 'Your answer as a fraction' });\n")
SIDE = ("  a.innerHTML = '<div class=\"ans-row\"><span class=\"nb\"><input type=\"text\" aria-label=\"Top number\"></span>' +\n"
        "    '<span class=\"slash\" aria-hidden=\"true\">/</span><span class=\"nb\"><input type=\"text\" aria-label=\"Bottom number\"></span>' + CHECK + '</div>';\n")
SLASH_ONLY = ("  a.innerHTML = '<div class=\"ans-row\"><span class=\"nb\"><input type=\"text\" aria-label=\"First\"></span>' +\n"
              "    '<span class=\"slash\">/</span><span class=\"nb\"><input type=\"text\" aria-label=\"Second\"></span>' + CHECK + '</div>';\n")
HELPER = ("  function box(k, label) { var el = document.createElement('input'); el.setAttribute('aria-label', label); return el; }\n"
          "  var top = box('num', 'Top of the fraction (numerator)'), bot = box('den', 'Bottom of the fraction (denominator)');\n")


def selftest():
    side = pc.apply_plant(SHARED, OWN, SIDE, name='own side-by-side boxes')
    slash_only = pc.apply_plant(SHARED, OWN, SLASH_ONLY, name='a separator between two inputs, unlabelled')
    helper = pc.apply_plant(SHARED, OWN, HELPER, name="own boxes built by a helper (The 6 P's shape)")
    unloaded = pc.apply_plant(SHARED, '<script src="../../schools/assets/fraction-input.js"></script>\n', '', name='script not loaded')
    G, W = 'games/test-game/index.html', 'games/listed-game/index.html'
    cases = [  # (name, pages, warn, base warn, expected error text or None, want a warning)
        ('the shared input passes (prose and stage names that mention a part are not labels)', {G: SHARED}, [], [], None, False),
        ('PLANT: a page with its own side-by-side boxes fails', {G: side}, [], [], 'builds its own fraction boxes', False),
        ('PLANT: a warn-listed page warns', {W: side}, [W], [W], None, True),
        ('PLANT: adding to the warn list fails', {G: side}, [G], [], 'shrink-only', True),
        ('a separator between two unlabelled inputs fails', {G: slash_only}, [], [], 'separator', False),
        ("boxes built by a helper with the parts' labels fail", {G: helper}, [], [], 'its own labels', False),
        ('MaffsFractionInput without its script fails', {G: unloaded}, [], [], 'does not load', False),
        ('a stale warn entry (the page moved) fails', {W: SHARED}, [W], [W], 'stale', False),
        ('a warn entry for a page that does not exist fails', {G: SHARED}, [W], [W], 'no such page', False),
        ('restoring a removed warn entry fails', {W: side}, [W], [], 'shrink-only', True),
    ]
    failed = 0
    for name, pg, warn, base, expected, want_warning in cases:
        errors, warnings, _ = analyse(pg, warn, base)
        ok = pc.is_caught([e for e in errors if expected in e]) if expected else not errors
        ok = ok and bool(warnings) == want_warning
        print('%s: %s%s' % ('PASS' if ok else 'FAIL', name, '' if ok else ' (errors %s, warnings %s)' % (errors, warnings)))
        failed += not ok
    print('Fraction input selftest: %d/%d passed' % (len(cases) - failed, len(cases)))
    return bool(failed)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    if args.selftest:
        return selftest()
    try:
        warn = read_warn((ROOT / WARN).read_text(encoding='utf-8'))
        pg = pages()
        errors, warnings, shared = analyse(pg, warn, base_warn())
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print('FAIL: cannot check the fraction inputs: %s' % exc)
        return 1
    for w in warnings:
        print('WARN: %s' % w)
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            print('::warning title=Fraction input::%s' % w)
    for e in errors:
        print('FAIL: %s' % e)
    print('Fraction input: %d pages read, %d use MaffsFractionInput, %d warnings, %d failures'
          % (len(pg), shared, len(warnings), len(errors)))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
