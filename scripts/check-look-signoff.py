#!/usr/bin/env python3
# ci-line: Look sign-off (listed games require Jon's approval; shrink-only warnings; planted faults) | --selftest && --check
# ci-deps: .claude/rules/game-roster.md scripts/look-signoff-warn.json
"""LOOK-STAGE, Jon, 2 Nov 2026: visual approval is recorded in the roster.

The initial warning seed is frozen. PRs also compare against their base, so an
exception cannot be restored after removal. No game files are read or changed.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import subprocess

import plant_common as pc

ROOT = Path(__file__).resolve().parent.parent
ROSTER = '.claude/rules/game-roster.md'
WARN = 'scripts/look-signoff-warn.json'
INITIAL_WARN = {'who-ate-all-the-pies'}
ROW = re.compile(r'^\|\s*\d+\s*\|[^|]*\|\s*`([a-z0-9-]+)`\s*\|')
SIGNOFF = re.compile(r'(?<!\S)Look signed off by Jon, (pre-2 Nov, grandfathered|\d{4}-\d{2}-\d{2})\.(?: |$)')


def analyse(roster, listed_warn, base_warn):
    errors, warnings = [], []
    warn = set(listed_warn)
    if len(warn) != len(listed_warn):
        errors.append('duplicate warn-list entries')
    for slug in sorted(warn - INITIAL_WARN | (warn - set(base_warn))):
        errors.append(f'{slug}: adding to the warn list fails; it is shrink-only')
    section = None
    listed, seen = set(), set()
    for line in roster.splitlines():
        if line.startswith('## '):
            section = line[3:]
        match = ROW.match(line)
        if not match:
            continue
        slug = match[1]
        if slug in seen:
            errors.append(f'{slug}: duplicate roster row')
        seen.add(slug)
        if section is None:
            errors.append(f'{slug}: game row outside a roster section')
            continue
        if section.startswith(('Unlisted', 'Withdrawn')):
            continue
        listed.add(slug)
        # Approval belongs to this game's description, never another row or cell.
        cells = line.split('|')
        approval = SIGNOFF.search(cells[6].strip()) if len(cells) == 9 else None
        if approval and approval[1] != 'pre-2 Nov, grandfathered':
            try:
                datetime.date.fromisoformat(approval[1])
            except ValueError:
                approval = None
        if approval:
            if slug in warn:
                errors.append(f'{slug}: signed off now; remove its stale warn-list entry')
        elif slug in warn:
            warnings.append(f'{slug}: missing look sign-off (warn-listed pending Jon; remove after approval)')
        else:
            errors.append(f'{slug}: listed without look sign-off by Jon')
    if not listed:
        errors.append('no listed game rows found; roster parsing is blind')
    for slug in sorted(warn - listed):
        errors.append(f'{slug}: no longer listed; remove its stale warn-list entry')
    return errors, warnings, len(listed)


def base_warn():
    """Read the PR base; fail closed on missing git/event data. Bootstrap once."""
    if os.environ.get('GITHUB_EVENT_NAME') == 'pull_request':
        event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text(encoding='utf-8'))
        base = event['pull_request']['base']['sha']
    else:
        base = subprocess.run(['git', 'merge-base', 'origin/main', 'HEAD'], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    files = subprocess.run(['git', 'ls-tree', '--name-only', base, '--', WARN], cwd=ROOT,
                           capture_output=True, text=True, check=True).stdout.strip()
    if not files:
        return INITIAL_WARN
    source = subprocess.run(['git', 'show', f'{base}:{WARN}'], cwd=ROOT,
                            capture_output=True, text=True, encoding='utf-8', check=True).stdout
    return json.loads(source)


def selftest():
    good = '## GCSE Games (1)\n| 1 | Test | `test-game` | GCSE | Algebra | Look signed off by Jon, 2026-11-02. | optional |\n'
    missing = pc.apply_plant(good, 'Look signed off by Jon, 2026-11-02.', 'Pending.', name='missing approval')
    pending = pc.apply_plant(missing, '`test-game`', '`who-ate-all-the-pies`', name='warn-listed game')
    cases = [
        ('signed-off game passes', good, [], [], None, False),
        ('listed game without sign-off fails', missing, [], [], 'listed without', False),
        ('warn-listed game warns', pending, ['who-ate-all-the-pies'], INITIAL_WARN, None, True),
        ('adding to warn list fails', missing, ['test-game'], [], 'shrink-only', True),
        ('restoring removed warning fails', pending, ['who-ate-all-the-pies'], [], 'shrink-only', True),
        ('stale warning fails', good.replace('`test-game`', '`who-ate-all-the-pies`'),
         ['who-ate-all-the-pies'], INITIAL_WARN, 'stale', False),
        ('unlisted game needs no sign-off', good + missing.replace('## GCSE Games (1)', '## Unlisted (1)').replace('`test-game`', '`unlisted-game`'),
         [], [], None, False),
    ]
    failed = 0
    for name, source, warn, base, expected, want_warning in cases:
        errors, warnings, _ = analyse(source, warn, base)
        ok = (pc.is_caught([e for e in errors if expected in e]) if expected else not errors)
        ok = ok and bool(warnings) == want_warning
        print(f'{"PASS" if ok else "FAIL"}: {name}')
        failed += not ok
    print(f'Look sign-off selftest: {len(cases) - failed}/{len(cases)} passed')
    return bool(failed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--selftest', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    try:
        warn = json.loads((ROOT / WARN).read_text(encoding='utf-8'))
        if not isinstance(warn, list) or any(not isinstance(s, str) for s in warn):
            raise ValueError('warn list must be an array of slugs')
        errors, warnings, count = analyse((ROOT / ROSTER).read_text(encoding='utf-8'), warn, base_warn())
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(f'FAIL: cannot check look sign-offs: {exc}')
        return 1
    for warning in warnings:
        print(f'WARN: {warning}')
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            print(f'::warning title=Look sign-off::{warning}')
    for error in errors:
        print(f'FAIL: {error}')
    print(f'Look sign-off: {count} listed games, {len(warnings)} warnings, {len(errors)} failures')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
