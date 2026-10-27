#!/usr/bin/env python3
"""Every The 6 P's question in the wrong state on a phone: is the verdict, and Next, on the screen once the page has settled?
(Jon's class check, 27 Oct 2026, after main run 40529609805.) Not run in CI: a report, run by hand. It reuses
verify-the-6-ps.py's `phone_feedback_topic(only=<question id>)`, which serves five copies of one real question and answers it wrong.

    python scripts/sweep-six-ps-wrong.py                       # every question at 375 x 667, then the tallest 30% of each bank at the others
    python scripts/sweep-six-ps-wrong.py --sizes 375x667 --all # every question at the sizes named
    python scripts/sweep-six-ps-wrong.py --workers 4 --only fraction-percentage-of-amount

Prints one line per size and every finding; exit 1 if any.
"""
import argparse
import concurrent.futures as cf
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SIZES = [(375, 667), (320, 568), (390, 844), (414, 896)]


def load():
    sys.path.insert(0, HERE)
    spec = importlib.util.spec_from_file_location('v6', os.path.join(HERE, 'verify-the-6-ps.py'))
    v = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(v)
    return v


def weight(q):
    """How tall the wrong-state feedback is likely to be: the characters of the working, the slips and the stem."""
    return sum(len(w) for w in q['worked']) + sum(len(s['line']) for s in q['slip']) + len(q['stem'])


def worker(args):
    jobs, size = args
    v = load()
    from playwright.sync_api import sync_playwright
    import bank_common as bc
    html = open(os.path.join(ROOT, 'the-6-ps', 'index.html'), encoding='utf-8').read()
    data = v.load_data()
    by_topic = {t['id']: t for t in data['covered']}
    out = []
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            for tid, qid in jobs:
                try:
                    v.phone_feedback_topic(pw, base, html, data, by_topic[tid], out, only=qid, size=size)
                except Exception as exc:
                    out.append('%dx%d: %s %s: stopped: %s' % (size[0], size[1], tid, qid, str(exc).splitlines()[0][:100]))
    finally:
        proc.terminate()
    return len(jobs), out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--sizes', help='e.g. 375x667,320x568 (default: the four phone sizes)')
    ap.add_argument('--all', action='store_true', help='every question at every size named (default: every question at 375x667 only, the tallest 30%% elsewhere)')
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--only', help='one topic id')
    a = ap.parse_args()
    sizes = [tuple(int(x) for x in s.split('x')) for s in a.sizes.split(',')] if a.sizes else SIZES
    v = load()
    data = v.load_data()
    banks = {}
    for t in data['covered']:
        if a.only and t['id'] != a.only:
            continue
        banks[t['id']] = json.load(open(os.path.join(ROOT, 'schools', 'assets', 'six-ps', t['id'] + '.json'), encoding='utf-8'))['questions']
    bad = []
    for size in sizes:
        jobs = []
        for tid, qs in banks.items():
            pick = qs
            if size != (375, 667) and not a.all:
                keep = max(1, int(len(qs) * 0.3))
                pick = sorted(qs, key=weight, reverse=True)[:keep]
            jobs += [(tid, q['id']) for q in pick]
        chunks = [jobs[i::a.workers] for i in range(a.workers)]
        n = 0
        found = []
        with cf.ProcessPoolExecutor(a.workers) as ex:
            for done, out in ex.map(worker, [(c, size) for c in chunks if c]):
                n += done
                found += out
        print('%dx%d: %d questions in the wrong state, %d finding(s)' % (size[0], size[1], n, len(found)), flush=True)
        for f in found[:60]:
            print('  FAIL ' + f, flush=True)
        bad += found
    print('PASS' if not bad else 'FAILED: %d finding(s)' % len(bad))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
