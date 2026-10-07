#!/usr/bin/env python3
"""The findings register: every audit finding, one file per game, tracked to its fix.

    python scripts/audit-register.py            # validate, regenerate docs/audits/REGISTER.md
    python scripts/audit-register.py --check    # CI on every PR: validate the per-game files only
    python scripts/audit-register.py --selftest # planted faults must fail (CI runs it with --check)

Each game audited has docs/audits/findings/<slug>.yml (Jon, 6 Oct 2026: one file per game, so
parallel fix PRs never edit the same file). The schema is the tranche 3-6 audits' own:

    game: <slug>
    audited: {tranche, head, date, served: {<level>: "<per session>/<distinct>"}}
             (a list of these when the game was audited more than once)
    findings:
      - id: <slug>-t<n>-NNN (tranche n), <slug>-r-NNN (resit audit)
        severity: CRITICAL | HIGH | MEDIUM | LOW
        jc: true | false            (judgement call)
        class: <n> | "NEW:<name>"   (the audits' bug classes)
        level, where, summary, evidence: text
        status: open | fixed | ruled
        pr: <n> or [<n>, ...]       (required when fixed: the PR that fixed it)
        ruling: <text>              (required when ruled: the SR or ruling that closed it)

A fix PR closes an entry in the same PR: status fixed and pr set, in its own game's file only (canon
§0.4). No PR edits REGISTER.md (7 Oct 2026, so two PRs never conflict on it): the workflow's
"Regenerate REGISTER.md" job runs this script on every push to main, after the Gate, and commits the
file if it changed.

Fails on: a file that does not parse or breaks the schema; a duplicate id; a fixed entry with no
PR; a ruled entry with no ruling; a file for a game with no games/<slug>/; and a roster
"Unlisted" game with no register file. The dashboard's exit-bar points 1, 2, 4 and 5 are computed (canon §0.2); 3 and 6
are stated in SHARED_CHECKS_GREEN and SWEEP_DONE below, changed by the PR that meets them.
"""
import argparse
import collections
import os
import re
import sys
import tempfile

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FINDINGS = os.path.join('docs', 'audits', 'findings')
REGISTER = os.path.join('docs', 'audits', 'REGISTER.md')
ROSTER = os.path.join('.claude', 'rules', 'game-roster.md')
WORKFLOW = os.path.join('.github', 'workflows', 'check-site.yml')

SEVERITIES = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
STATUSES = ['open', 'fixed', 'ruled']
FIELDS = ['id', 'severity', 'jc', 'class', 'level', 'where', 'summary', 'evidence', 'status']
OPTIONAL = {'pr', 'ruling'}

# Exit bar point 3 (canon §0.2): shared checks green site-wide. Set each True in the PR that makes it so.
SHARED_CHECKS_GREEN = {
    'answer lock': False,
    'level resolver': False,
    'served bank size': False,
    'SR-14 fields': False,
    'B11 parser': False,
}
# Exit bar point 6: one sweep of the already-verified games for true wrong options and unstated conventions.
SWEEP_DONE = False

# Roster-Unlisted games that no audit unlisted, so they need no register file: slug -> why.
UNLISTED_NOT_BY_AUDIT = {'just-pythag-it-bruv': 'new, unlisted until Jon has played and approved it (todo START)'}

# A verifier named for something other than its game, or one that covers only part of a game.
VERIFIER_GAME = {'verify-six-sevens.py': 'six-sevens-bruv'}
PARTIAL = {'verify-better-value-tax.py': 'better-value', 'verify-core-maths-paper1-tax.py': 'core-maths-paper1'}
NOT_A_GAME = {'verify-parent-guides.py'}

# Audience, for ordering open CRITICAL/HIGH: the roster's lowest level first (Year 6/KS3/GCSE/Core first).
LEVEL_RANK = [('year 6', 0), ('ks3', 1), ('gcse', 2), ('core', 3), ('a-level', 4), ('further', 5), ('l4', 6)]


def read(root, rel):
    with open(os.path.join(root, rel), encoding='utf-8') as f:
        return f.read()


def roster(root):
    """{slug: {'name', 'levels', 'section'}} for every numbered row, and the Unlisted slugs."""
    games, unlisted, section = {}, [], None
    for ln in read(root, ROSTER).split('\n'):
        if ln.startswith('## '):
            section = ln[3:].split(' (')[0]
        m = re.match(r'^\| (\d+) \| ([^|]+) \| `([a-z0-9-]+)` \| ([^|]+) \|', ln)
        if m:
            games[m.group(3)] = {'name': m.group(2).strip(), 'levels': m.group(4).strip(), 'section': section}
            if section == 'Unlisted':
                unlisted.append(m.group(3))
    return games, unlisted


def audience(levels):
    low = levels.lower()
    ranks = [r for k, r in LEVEL_RANK if k in low]
    return min(ranks) if ranks else 9


def load(root):
    """[(path, data)] for every register file, and the parse errors."""
    out, errors = [], []
    d = os.path.join(root, FINDINGS)
    for name in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if not name.endswith('.yml'):
            continue
        rel = os.path.join(FINDINGS, name)
        try:
            out.append((rel, yaml.safe_load(read(root, rel))))
        except yaml.YAMLError as e:
            errors.append('%s: does not parse: %s' % (rel, str(e).splitlines()[0]))
    return out, errors


def audits(data):
    a = data.get('audited')
    return a if isinstance(a, list) else [a]


def validate(files, games, unlisted, root):
    errors, seen = [], {}
    for rel, data in files:
        slug = os.path.basename(rel)[:-4]
        if not isinstance(data, dict):
            errors.append('%s: not a mapping' % rel)
            continue
        if data.get('game') != slug:
            errors.append('%s: game is %r, the file is named for %r' % (rel, data.get('game'), slug))
        if not os.path.isdir(os.path.join(root, 'games', slug)):
            errors.append('%s: there is no games/%s/' % (rel, slug))
        extra = set(data) - {'game', 'audited', 'findings'}
        if extra:
            errors.append('%s: unknown top-level keys %s' % (rel, sorted(extra)))
        for a in audits(data):
            if not isinstance(a, dict) or set(a) != {'tranche', 'head', 'date', 'served'}:
                errors.append('%s: audited entry %r needs exactly tranche, head, date, served' % (rel, a))
            elif not isinstance(a['served'], dict):
                errors.append('%s: audited served must map level to size' % rel)
        fs = data.get('findings')
        if not isinstance(fs, list):
            errors.append('%s: findings must be a list' % rel)
            continue
        for f in fs:
            fid = f.get('id', '?') if isinstance(f, dict) else '?'
            where = '%s %s' % (rel, fid)
            if not isinstance(f, dict):
                errors.append('%s: a finding is not a mapping' % rel)
                continue
            missing = [k for k in FIELDS if k not in f]
            if missing:
                errors.append('%s: missing %s' % (where, ', '.join(missing)))
            unknown = set(f) - set(FIELDS) - OPTIONAL
            if unknown:
                errors.append('%s: unknown fields %s' % (where, sorted(unknown)))
            if not str(fid).startswith(slug + '-'):
                errors.append('%s: id does not start with %s-' % (where, slug))
            if fid in seen:
                errors.append('%s: id also used in %s' % (where, seen[fid]))
            seen[fid] = rel
            if f.get('severity') not in SEVERITIES:
                errors.append('%s: severity %r' % (where, f.get('severity')))
            if not isinstance(f.get('jc'), bool):
                errors.append('%s: jc must be true or false' % where)
            if f.get('status') not in STATUSES:
                errors.append('%s: status %r (open, fixed or ruled)' % (where, f.get('status')))
            pr = f.get('pr')
            prs = pr if isinstance(pr, list) else [pr] if pr is not None else []
            if f.get('status') == 'fixed' and not prs:
                errors.append('%s: fixed, but names no PR' % where)
            if any(not isinstance(p, int) or p < 1 for p in prs):
                errors.append('%s: pr must be a PR number or a list of them, got %r' % (where, pr))
            if f.get('status') == 'ruled' and not f.get('ruling'):
                errors.append('%s: ruled, but names no ruling' % where)
    have = {os.path.basename(rel)[:-4] for rel, _ in files}
    for slug in unlisted:
        if slug not in have and slug not in UNLISTED_NOT_BY_AUDIT:
            errors.append('%s is in the roster\'s Unlisted section but has no register file (%s/%s.yml)'
                          % (slug, FINDINGS.replace(os.sep, '/'), slug))
    return errors


def verifiers(root):
    """{slug: script} for games with a whole-game verifier that CI runs; and the partial ones."""
    # What CI runs: the workflow's site-wide lines and every script's ci-line header (contract V), as
    # scripts/ci-groups.py in this tree reads them.
    import importlib.util
    spec = importlib.util.spec_from_file_location('ci_groups', os.path.join(root, 'scripts', 'ci-groups.py'))
    cg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cg)
    run = set(re.findall(r'python3? scripts/([A-Za-z0-9_.-]+\.py)', cg.ci_text()))
    full, partial = {}, {}
    for name in sorted(os.listdir(os.path.join(root, 'scripts'))):
        if not re.match(r'^verify-.+\.py$', name) or name not in run or name in NOT_A_GAME:
            continue
        if name in PARTIAL:
            partial.setdefault(PARTIAL[name], name)
        else:
            full[VERIFIER_GAME.get(name, name[len('verify-'):-3])] = name
    return full, partial


def distinct(size):
    """The distinct items a served-size string names ("10/1347" -> 1347, "45" -> 45), or None."""
    s = str(size)
    m = re.search(r'/\s*(\d[\d,]*)', s) or re.search(r'(\d[\d,]*)', s)
    return int(m.group(1).replace(',', '')) if m else None


def render(files, games, unlisted, root):
    every = [(data['game'], f) for _, data in files for f in data['findings']]
    by_game = {data['game']: data for _, data in files}
    open_ch = [(g, f) for g, f in every if f['status'] == 'open' and f['severity'] in ('CRITICAL', 'HIGH')]
    full, partial = verifiers(root)
    live = sorted(games)
    L = []
    L.append('# Findings register')
    L.append('')
    L.append('Generated by `scripts/audit-register.py` from `docs/audits/findings/<slug>.yml`; do not edit by hand. '
             'CI regenerates and commits it on main after every merge; no PR edits it. A fix PR closes its '
             "entries in its own game's file in the same PR (status `fixed`, `pr` set; canon §0.4).")
    L.append('')
    L.append('Sources: `docs/audit-resit-correctness-2026-10-04.md` (ids `-r-`), `docs/audits/audit-tranche1-2026-10-06.md` '
             'and `audit-tranche2-2026-10-06.md` (`-t1-`, `-t2-`; converted from the reports: every CRITICAL and HIGH, and '
             'every MEDIUM the report itemises with its severity), `docs/audits/tranche-3..6-2026-10-06.md` (`-t3-`..`-t6-`; '
             'each tranche file `findings/tranche-<n>.yml` from its audit branch, split one file per game, data unchanged).')
    L.append('')

    # ---- exit bar
    no_verifier = [s for s in live if s not in full]
    lv_under = []
    for g, data in sorted(by_game.items()):
        if g not in games:
            continue
        a = audits(data)[-1]
        for lvl, size in a['served'].items():
            n = distinct(size)
            if n is not None and n < 40:
                lv_under.append('%s %s (%s)' % (g, lvl, size))
    L.append('## Exit bar (canon §0.2)')
    L.append('')
    L.append('| # | Point | Status |')
    L.append('|---|---|---|')
    L.append('| 1 | Every live game has a verifier in CI | %s: %d of %d live games have none (computed from `games/` and the verifiers CI runs) |'
             % ('met' if not no_verifier else 'NOT MET', len(no_verifier), len(live)))
    L.append('| 2 | Every CRITICAL and HIGH in the register fixed | %s: %d open (%d CRITICAL, %d HIGH) |'
             % ('met' if not open_ch else 'NOT MET', len(open_ch),
                sum(1 for _, f in open_ch if f['severity'] == 'CRITICAL'), sum(1 for _, f in open_ch if f['severity'] == 'HIGH')))
    red = [k for k, v in SHARED_CHECKS_GREEN.items() if not v]
    L.append('| 3 | Shared checks green site-wide | %s (stated): %s |'
             % ('met' if not red else 'NOT MET', 'all green' if not red else 'not yet: ' + ', '.join(red)))
    L.append('| 4 | Every level serves 40+ | %s: %d audited levels serve under 40 (games no audit has covered are not measured) |'
             % ('met' if not lv_under else 'NOT MET', len(lv_under)))
    L.append('| 5 | Every unlisted game relisted or archived | %s: %d in the roster\'s Unlisted section |'
             % ('met' if not unlisted else 'NOT MET', len(unlisted)))
    L.append('| 6 | One sweep of the verified games for true wrong options and unstated conventions | %s (stated) |'
             % ('met' if SWEEP_DONE else 'NOT MET'))
    L.append('')

    # ---- counts
    L.append('## Counts')
    L.append('')
    L.append('%d findings in %d games.' % (len(every), len(by_game)))
    L.append('')
    L.append('| Severity | open | fixed | ruled | total |')
    L.append('|---|---|---|---|---|')
    for s in SEVERITIES:
        c = collections.Counter(f['status'] for _, f in every if f['severity'] == s)
        L.append('| %s | %d | %d | %d | %d |' % (s, c['open'], c['fixed'], c['ruled'], sum(c.values())))
    c = collections.Counter(f['status'] for _, f in every)
    L.append('| **All** | %d | %d | %d | %d |' % (c['open'], c['fixed'], c['ruled'], len(every)))
    L.append('')
    L.append('### By class')
    L.append('')
    L.append('| Class | open | total |')
    L.append('|---|---|---|')
    cls = collections.Counter(str(f['class']) for _, f in every)
    cls_open = collections.Counter(str(f['class']) for _, f in every if f['status'] == 'open')
    for k, n in sorted(cls.items(), key=lambda kv: (-kv[1], kv[0])):
        L.append('| %s | %d | %d |' % (k.replace('|', '/'), cls_open[k], n))
    L.append('')
    L.append('### By game')
    L.append('')
    L.append('| Game | Listed | Verifier | C | H | M | L | open | fixed | ruled |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for g in sorted(by_game):
        fs = by_game[g]['findings']
        sc = collections.Counter(f['severity'] for f in fs)
        st = collections.Counter(f['status'] for f in fs)
        L.append('| `%s` | %s | %s | %d | %d | %d | %d | %d | %d | %d |' % (
            g, 'unlisted' if g in unlisted else 'yes', full.get(g, 'partial: ' + partial[g] if g in partial else 'none'),
            sc['CRITICAL'], sc['HIGH'], sc['MEDIUM'], sc['LOW'], st['open'], st['fixed'], st['ruled']))
    L.append('')

    # ---- open CRITICAL/HIGH by audience
    L.append('## Open CRITICAL and HIGH, by game (Year 6, KS3, GCSE and Core first)')
    L.append('')
    per = collections.defaultdict(list)
    for g, f in open_ch:
        per[g].append(f)
    order = sorted(per, key=lambda g: (audience(games.get(g, {}).get('levels', '')), g))
    for g in order:
        info = games.get(g, {})
        L.append('### `%s` (%s%s)' % (g, info.get('levels', '?'), '; unlisted' if g in unlisted else ''))
        L.append('')
        for f in sorted(per[g], key=lambda f: (SEVERITIES.index(f['severity']), f['id'])):
            L.append('- **%s** %s%s, `%s`: %s' % (f['severity'], f['id'], ' (JC)' if f['jc'] else '',
                                                    str(f['where']).replace('`', "'"), one_line(f['summary'])))
        L.append('')
    if not order:
        L.append('None.')
        L.append('')

    # ---- unaudited
    L.append('## Live games no audit has covered')
    L.append('')
    un = [s for s in live if s not in by_game]
    L.append('%d of %d live games: %s' % (len(un), len(live), ', '.join('`%s`' % s for s in un) if un else 'none'))
    L.append('')
    L.append('## Exit bar detail')
    L.append('')
    L.append('**1. No verifier in CI (%d):** %s' % (len(no_verifier), ', '.join('`%s`%s' % (s, ' (partial: %s)' % partial[s] if s in partial else '') for s in no_verifier)))
    L.append('')
    L.append('**4. Audited levels serving under 40 (%d):** %s' % (len(lv_under), ', '.join(lv_under) or 'none'))
    L.append('')
    L.append('**5. Unlisted (%d):** %s' % (len(unlisted), ', '.join('`%s`' % s for s in unlisted)))
    L.append('')
    return '\n'.join(L)


def one_line(s):
    s = re.sub(r'\s+', ' ', str(s)).strip()
    return s if len(s) <= 220 else s[:217] + '...'


def run(root):
    """(errors, the rendered REGISTER.md or None). Validation reads the per-game files, the roster and
    games/; REGISTER.md itself is never read."""
    games, unlisted = roster(root)
    files, errors = load(root)
    errors += validate(files, games, unlisted, root)
    if errors:
        return errors, None
    return errors, render(files, games, unlisted, root)


def selftest(root):
    """A fixed entry with no PR, and an entry that breaks the schema, must each fail; the real tree must pass."""
    import shutil
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        for rel in (FINDINGS, os.path.dirname(ROSTER), os.path.dirname(WORKFLOW), 'scripts', 'games'):
            shutil.copytree(os.path.join(root, rel), os.path.join(tmp, rel), dirs_exist_ok=True)
        base, _ = run(tmp)
        if base:
            print('self-test: the tree fails before any fault is planted: %s' % base[0])
            return False
        # 1. a fixed entry with no PR
        name = sorted(n for n in os.listdir(os.path.join(tmp, FINDINGS)) if n.endswith('.yml'))[0]
        p = os.path.join(tmp, FINDINGS, name)
        src = open(p, encoding='utf-8').read()
        data = yaml.safe_load(src)
        data['findings'][0]['status'] = 'fixed'
        data['findings'][0].pop('pr', None)
        open(p, 'w', encoding='utf-8').write(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
        errs, _ = run(tmp)
        caught = any('names no PR' in e for e in errs)
        print('  self-test %-34s %s' % ('a fixed entry with no PR', 'caught' if caught else '*** MISSED ***'))
        ok = ok and caught
        open(p, 'w', encoding='utf-8').write(src)
        # 2. a schema fault: a severity the schema does not have, and a finding missing a field
        data = yaml.safe_load(src)
        data['findings'][0]['severity'] = 'SEVERE'
        data['findings'][-1].pop('evidence', None)
        open(p, 'w', encoding='utf-8').write(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
        errs, _ = run(tmp)
        caught = any("severity 'SEVERE'" in e for e in errs) and any('missing evidence' in e for e in errs)
        print('  self-test %-34s %s' % ('a schema fault (severity, field)', 'caught' if caught else '*** MISSED ***'))
        ok = ok and caught
        open(p, 'w', encoding='utf-8').write(src)
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true',
                    help='validate only; never reads or writes REGISTER.md (CI, every PR)')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()
    errors, text = run(ROOT)
    if text is not None and not args.check:
        with open(os.path.join(ROOT, REGISTER), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        print('wrote %s' % REGISTER)
    ok = not errors
    if args.selftest and ok:
        ok = selftest(ROOT)
    for e in errors:
        print('FAIL  ' + e)
    print('OK' if ok else 'FAILED')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
