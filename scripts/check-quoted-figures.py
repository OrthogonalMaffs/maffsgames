#!/usr/bin/env python3
"""No real-world figure the quoted-statistics audit found CONTRADICTED is still on its page.

The audit (docs/audits/quoted-statistics-2026-10.md, PR #68) checked every real-world figure a student is marked
against, and Screening Room's and Core Maths Paper 1's stated rates, against a source; its ledger
(docs/audits/quoted-statistics-2026-10-ledger.md) records each figure, one line each. Figures had been typed in
by hand with no source, so a wrong one could come back the same way. Each ledger line whose status says
CONTRADICTED carries a check annotation naming the old value as it was written in the page source and where:

    ... | CONTRADICTED (...) | check: `8 litres per 100 km` in games/fermi-lab/index.html#eq_school_trip

  - `#<item id>` limits the search to that item's line (the line holding id:"<item id>"); without it the whole
    page is searched. Several checks are separated by " ; ".
  - A literal is matched exactly, as written in the page source (\\u escapes and all).

Fails if: a CONTRADICTED line has no check; a check names a page or an item that does not exist (a check that
cannot find its target proves nothing); or an old value is still in its page or item. The corrected figures
themselves are each game's own verifier's job (verify-fermi-lab.py, verify-screening-room.py,
verify-core-maths-paper1.py).

    python scripts/check-quoted-figures.py [--selftest]

--selftest plants an old value back into a copy of a page (Fermi Lab's 8 litres per 100 km) and an unannotated
CONTRADICTED line, and requires both to fail.
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = 'docs/audits/quoted-statistics-2026-10-ledger.md'
CHECK = re.compile(r'\|\s*check:\s*(.+)$')
ONE = re.compile(r'^`([^`]+)`\s+in\s+([\w./-]+?)(?:#([\w-]+))?$')


def read(path, overrides):
    if path in overrides:
        return overrides[path]
    full = os.path.join(ROOT, path)
    if not os.path.isfile(full):
        return None
    return open(full, encoding='utf-8').read()


def item_line(text, iid):
    m = re.search(r'^.*\bid:\s*["\']' + re.escape(iid) + r'["\'].*$', text, re.M)
    return m.group(0) if m else None


def run(ledger_text, overrides=None):
    overrides = overrides or {}
    fails, checked = [], 0
    for n, line in enumerate(ledger_text.splitlines(), 1):
        if not line.startswith('- ') or 'CONTRADICTED' not in line:
            continue
        what = line[2:].split(' | ', 1)[0]
        m = CHECK.search(line)
        if not m:
            fails.append(f'ledger line {n} ({what}): CONTRADICTED with no check annotation')
            continue
        for spec in [s.strip() for s in m.group(1).split(' ; ')]:
            s = ONE.match(spec)
            if not s:
                fails.append(f'ledger line {n} ({what}): unreadable check {spec!r}')
                continue
            old, path, iid = s.groups()
            text = read(path, overrides)
            if text is None:
                fails.append(f'ledger line {n} ({what}): {path} does not exist')
                continue
            scope = text
            if iid:
                scope = item_line(text, iid)
                if scope is None:
                    fails.append(f'ledger line {n} ({what}): no item {iid} in {path}')
                    continue
            checked += 1
            if old in scope:
                fails.append(f'ledger line {n} ({what}): the old value `{old}` is still in {path}' + (f' ({iid})' if iid else ''))
    return fails, checked


def selftest():
    ledger = open(os.path.join(ROOT, LEDGER), encoding='utf-8').read()
    page = 'games/fermi-lab/index.html'
    src = open(os.path.join(ROOT, page), encoding='utf-8').read()
    planted = re.sub(r'(\{id:"eq_school_trip",question:")', r'\1A coach uses about 8 litres per 100 km. ', src, count=1)
    cases = [
        ("Fermi Lab's 8 litres per 100 km planted back", ledger, {page: planted}, 'eq_school_trip'),
        ('a CONTRADICTED ledger line with no check', ledger + '\n- planted.s1 | 1 | 2 | https://example.org | CONTRADICTED (planted)\n', {}, 'planted.s1'),
    ]
    bad = 0
    for label, led, ov, want in cases:
        fails, _ = run(led, ov)
        hit = any(want in f for f in fails)
        print(f'  {"caught" if hit else "MISSED"}: {label}')
        bad += not hit
    print(f'self-test: {len(cases) - bad}/{len(cases)} planted faults caught')
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    fails, checked = run(open(os.path.join(ROOT, LEDGER), encoding='utf-8').read())
    for f in fails:
        print('FAIL ' + f)
    print(f'{"PASS" if not fails else "FAILED"}: {checked} old values checked absent; {len(fails)} problem(s)')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
