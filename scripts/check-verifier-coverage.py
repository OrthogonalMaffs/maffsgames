#!/usr/bin/env python3
"""Does CI run every verifier in the repo?

A new verifier can land as a script and never run: until 2 Oct 2026, three of them in a single commit
(stat-attack, graph-sketcher, growth-and-decay), plus quadratic-factoriser and parent-guides from earlier.
A verifier that never runs passes every time.

Since contract V (7 Oct 2026, canon §7.8.2) a content verifier declares its own CI lines in its own file,
"# ci-line: <group> | <label> | <args>", and scripts/ci-groups.py builds the content groups from those
headers; the workflow lists only the site-wide jobs. Fails on:
  - a scripts/verify-*.py with no ci-line header and no "# ci-held: <reason>" header;
  - a scripts/test-*.py neither declared by a ci-line nor listed in the workflow's site-wide jobs;
  - a malformed header, a ci-line naming a group not in ci-groups.py's GROUPS, or ci-held beside a ci-line;
  - a script that declares a ci-line AND is listed in the workflow (it would run twice);
  - a scripts/verify-*.py listed in the workflow (verifiers declare their own lines; neither lane edits the
    workflow for one).
Reported, never failed: a content group whose lines took more than 4 minutes in all on main's last recorded
full run (scripts/ci-timings.json, written by `python scripts/ci-groups.py --record-timings <run id>`), and
the case where no timing file exists.

Stdlib only; about a second. Run from anywhere: paths are relative to the repo.
"""
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERN = re.compile(r'^(verify|test)-.+\.py$')
LIMIT = 240             # canon §7.8.1: no content job past 4 minutes

spec = importlib.util.spec_from_file_location('ci_groups', os.path.join(ROOT, 'scripts', 'ci-groups.py'))
cg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cg)


def timing_report(groups):
    path = os.path.join(ROOT, cg.TIMINGS)
    if not os.path.exists(path):
        print('timings: no %s yet (record one with ci-groups.py --record-timings <run id>)' % cg.TIMINGS)
        return
    with open(path, encoding='utf-8') as f:
        rec = json.load(f)
    secs = rec.get('lines', {})
    print('timings: main run %s (%s)' % (rec.get('run'), rec.get('date')))
    for g in groups:
        known = [secs[l] for l, _ in g['lines'] if l in secs]
        unknown = [l for l, _ in g['lines'] if l not in secs]
        total = sum(known)
        note = '' if not unknown else ' (+%d line(s) not in that run)' % len(unknown)
        print('%s%-4s %3ds of checks%s' % ('OVER    ' if total > LIMIT else 'timing  ', g['id'], total, note))
        if total > LIMIT:
            print('REPORT  group %s: its lines took %ds on main, past 4 minutes (canon §7.8.1): move a ci-line to '
                  'another group, or split the group' % (g['id'], total))


def main():
    hdrs = cg.headers()
    static = {}
    for job, _, cmd in cg.static_checks():
        for s in re.findall(r'python3? scripts/([A-Za-z0-9_.-]+\.py)', cmd):
            static.setdefault(s, job)
    declared = {name for name, info in hdrs.items() if info['lines']}
    held = {name: info['held'] for name, info in hdrs.items() if info['held']}
    present = sorted(n for n in os.listdir(os.path.join(ROOT, 'scripts')) if PATTERN.match(n))

    problems = list(cg.errors(hdrs))
    for name in present:
        if name in declared:
            print('ok      %s  (%s)' % (name, ', '.join(g for g, _, _ in hdrs[name]['lines'])))
        elif name in held:
            print('held    %s: %s' % (name, held[name]))
        elif name.startswith('test-') and name in static:
            print('ok      %s  (workflow: %s)' % (name, static[name]))
        elif name.startswith('verify-'):
            problems.append('%s declares no CI line: add "# ci-line: <group> | <label> | <args>" to its own file '
                            '(groups: %s), or "# ci-held: <reason>"' % (name, ', '.join(cg.GROUP_IDS)))
        else:
            problems.append('%s is not run by CI: add a ci-line header, or list it in a site-wide job' % name)
    for name in sorted(declared):
        if name in static:
            problems.append('%s declares a ci-line and is also listed in the workflow (%s): it would run twice'
                            % (name, static[name]))
    for name in sorted(static):
        if name.startswith('verify-') and name not in declared:
            problems.append('%s is listed in the workflow (%s): a verifier declares its own ci-line instead'
                            % (name, static[name]))

    timing_report(cg.groups(hdrs))
    if problems:
        for p in problems:
            print('FAIL    %s' % p)
        print('\nFAILED: %d problem(s)' % len(problems))
        return 1
    print('\nPASS: %d verifiers, %d run by CI, %d held' % (len(present), len(present) - len(held), len(held)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
