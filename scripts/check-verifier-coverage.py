#!/usr/bin/env python3
"""Does CI run every verifier in the repo?

CI lists its checks by hand (.github/workflows/check-site.yml, one "label|command"
line per check), so a new verifier can land as a script and never run: until
2 Oct 2026, three of them in a single commit (stat-attack, graph-sketcher,
growth-and-decay), plus quadratic-factoriser and parent-guides from earlier.
A verifier that never runs passes every time.

Every scripts/verify-*.py and scripts/test-*.py must appear in the workflow as
"python scripts/<name>", or be declared in HELD below with the reason it is held.
Fails on:
  - a verifier the workflow does not run and HELD does not declare;
  - a HELD entry whose script is gone, or that the workflow now runs (stale).

Stdlib only; about a second. Run from anywhere: paths are relative to the repo.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW = os.path.join(ROOT, '.github', 'workflows', 'check-site.yml')
PATTERN = re.compile(r'^(verify|test)-.+\.py$')

# Verifiers deliberately NOT run in CI. Each needs its reason; remove the entry
# when the script is wired in (a stale entry fails this check).
HELD = {
    'verify-regression-rumble.py':
        'regression-rumble is withdrawn; 37 of 40 scenarios fail, held for the data ruling (todo 1.26)',
}


def main():
    with open(WORKFLOW, encoding='utf-8') as f:
        workflow = f.read()
    run = set(re.findall(r'python3? scripts/([A-Za-z0-9_.-]+\.py)', workflow))
    present = sorted(n for n in os.listdir(os.path.join(ROOT, 'scripts')) if PATTERN.match(n))

    problems = []
    for name in present:
        if name in run:
            print(f'ok      {name}')
        elif name in HELD:
            print(f'held    {name}: {HELD[name]}')
        else:
            problems.append(f'{name} is not run by CI: add it to a group in '
                            f'.github/workflows/check-site.yml, or declare it in HELD with a reason')
    for name in sorted(HELD):
        if name not in present:
            problems.append(f'HELD entry {name} has no script: remove it')
        elif name in run:
            problems.append(f'HELD entry {name} is now run by CI: remove it from HELD')

    if problems:
        for p in problems:
            print(f'FAIL    {p}')
        print(f'\nFAILED: {len(problems)} problem(s)')
        return 1
    print(f'\nPASS: {len(present)} verifiers, {len(present) - len(HELD)} run by CI, {len(HELD)} held')
    return 0


if __name__ == '__main__':
    sys.exit(main())
