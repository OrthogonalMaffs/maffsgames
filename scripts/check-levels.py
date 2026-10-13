#!/usr/bin/env python3
# ci-line: Level resolver (MaffsLevel declarations equal the roster; every internal ?level= link and portal card names a level its game serves; no migrated game reads ?level itself; three planted faults) | --selftest && --check
# ci-deps: index.html sitemap.xml .claude/rules/game-roster.md scripts/roster-levels.json schools/assets/level.js games/ essentials/ resit/ op/ spec-map/ parents/ leaderboards/ escape-rooms/ year6/ 6-7/ about/ updates/
"""Does every game read ?level= through MaffsLevel, and does every link and listing agree with the game?
(contract LEVEL-RESOLVER, Jon, 12 Oct 2026; canon section 4.5; exit-bar point 3, "level resolver").

    python scripts/check-levels.py --check       # the site (CI, every PR)
    python scripts/check-levels.py --selftest    # three planted faults are caught
    python scripts/check-levels.py --report      # also print the NOT_YET list

A game MIGRATED to schools/assets/level.js calls `MaffsLevel.resolve({slug, levels, fallback[, boards]})` with
string literals. For every migrated game this check requires:
  a. the declared levels equal the roster's levels for the game, mapped through scripts/roster-levels.json (the
     one table; read, never copied), the slug is the folder's, and the fallback is one of the levels;
  b. every key the page submits to MaffsLeaderboard.submitScore as a string literal is a declared level or board;
  c. the page loads level.js, and does not read `?level` with its own code (`.get('level')`, `level=` in a
     query string it parses): the one reader is MaffsLevel.

Site-wide, for every game migrated or not (an unmigrated game serves the roster's levels):
  d. every internal link `games/<slug>/?level=<key>` (and a game page's `../<slug>/?level=<key>`) on every
     published page, and in sitemap.xml, names a level its target serves;
  e. every portal card (`<a href="games/<slug>/..." class="game-card" data-levels="...">`) lists only levels its
     game serves, and its link's level is one of them. "A level that serves another level's items is not listed
     as that level" (SR-16 to SR-20): a wrong listing is corrected to match the game, never made true by adding
     content.

NOT_YET (built the way check-answer-lock.py's is, canon 7.6.0): the games not yet migrated. Reported, never
failed, and it may only shrink: it is NOT_YET_AT_START minus MIGRATED, so a game that is not in
NOT_YET_AT_START must be migrated from the start. A game that calls MaffsLevel.resolve must be in MIGRATED, and
a game in MIGRATED must still call it (a migration cannot be undone silently). The migration batches move games
from NOT_YET_AT_START to MIGRATED; the last batch empties NOT_YET and sets 'level resolver' in
scripts/audit-register.py's SHARED_CHECKS_GREEN.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

SKIP_DIRS = {'.git', 'node_modules', 'docs', 'scripts', '.github', '.claude', 'firebase', 'data'}

# The games when contract LEVEL-RESOLVER began (12 Oct 2026). NOT_YET may only shrink: a new game is migrated
# from the start. Games leave this set (and join MIGRATED) in the batch that migrates them.
NOT_YET_AT_START = frozenset('''
52dle angle-ace bearing-blitz better-value binomial-blaster boolean-blitz characteristic-quest
chart-interrogator circle-theorem-spotter complex-converter component-crusher constructions-lab
coordinate-geometry-dash core-maths-paper1 core-maths-paper2a core-maths-paper2b core-maths-paper2c
correlation-or-coincidence curling-friction decimal-detective differentiation-duel dimension-checker
distinctly-average eigenvalue-extractor eigenvector-engine equation-builder equatle estimation-engine
estimation-golf expectation-station expected-damage factor-race factor-theorem fermi-lab force-resolver
formula-forge formula-plug-in formula-unlocked four-quadrant-explorer fraction-equivalence free-daily-pizza
given-that glorious-gantt gradient-hunter graph-sketcher graph-transformer growth-and-decay higher-power
index-laws integration-duel just-pythag-it-bruv like-terms-collector linear-equation-solver log-laws
maths-court matrix-crunch modular-battle moments-master negative-number-line new-shapes normal-navigator
partial-fractions-duel percentage-flip prime-factorisation prime-or-composite prisoners-dilemma
probability-paradox probability-pioneer proof-builder proportion-blaster quadratic-factoriser
regression-rumble scale-factor-scaling screening-room sequence-solver seven-bridges shape-shifter
simultaneous-solver six-sevens-bruv split-it spot-the-error spot-the-muppet standard-form-blitz stat-attack
surd-simplifier suvat tax-theft terrible-advice test-the-claim the-perfect-prank think-of-a-number
trig-identity-duel trig-wars trig-worms truth-buster truth-will-set-you-free unit-converter
word-problem-decoder wrong-on-the-internet
'''.split())
MIGRATED = frozenset('''
52dle angle-ace binomial-blaster complex-converter constructions-lab curling-friction decimal-detective
differentiation-duel distinctly-average equation-builder equatle expected-damage fermi-lab force-resolver
formula-plug-in four-quadrant-explorer fraction-equivalence higher-power integration-duel just-pythag-it-bruv
like-terms-collector maths-court matrix-crunch moments-master negative-number-line new-shapes percentage-flip
prime-factorisation prime-or-composite prisoners-dilemma probability-pioneer proof-builder sequence-solver
seven-bridges shape-shifter six-sevens-bruv split-it spot-the-error spot-the-muppet suvat terrible-advice
think-of-a-number truth-buster word-problem-decoder wrong-on-the-internet
'''.split())

# The portal has no Year 6 filter button, so a game that serves only Year 6 is reachable under the KS3 filter and its
# card lists 'ks3' as well (index.html, since the fresh repository of 2 Oct 2026). Every other token must be a level
# the game serves. A filter alias is a portal bucket, not a claim that the game serves that level; the game's own
# levels stay the roster's.
FILTER_ALIAS = {'year6': {'ks3'}}

RESOLVE = re.compile(r'MaffsLevel\.resolve\s*\(\s*\{(.*?)\}\s*\)', re.S)
OWN_READ = re.compile(r'''\.get\(\s*['"]level['"]\s*\)|[?&]level=|\blevel\s*=\s*([a-z]+)\.get\b''')
SUBMIT = re.compile(r'''MaffsLeaderboard\.submitScore\(\s*[^,]+,\s*(['"])([^'"]+)\1\s*,''')
LINK = re.compile(r'''(?:games/|\.\./)([a-z0-9][a-z0-9-]*)/(?:index\.html)?\?(?:[^"'\s<>#]*&(?:amp;)?)?level=([A-Za-z0-9_-]*)''')
CARD = re.compile(r'''<a\s+[^>]*href="([^"]*)"[^>]*class="game-card"[^>]*data-levels="([^"]*)"''')


def read_files(root):
    """{relpath: text} for every published page, the sitemap and every game page (docs and scripts are not published)."""
    out = {}
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if not (d in SKIP_DIRS and os.path.dirname(os.path.join(dp, d)) == root)]
        for fn in fns:
            if fn.endswith('.html') or fn == 'sitemap.xml':
                p = os.path.join(dp, fn)
                with open(p, encoding='utf-8', errors='replace', newline='') as f:
                    out[os.path.relpath(p, root).replace(os.sep, '/')] = f.read()
    for name in ('schools/assets/level.js',):
        p = os.path.join(root, name)
        if os.path.isfile(p):
            with open(p, encoding='utf-8', newline='') as f:
                out[name] = f.read()
    return out


def label_to_key():
    """The one table, for a portal card's data-levels tokens: a roster label (l4) or a key (alevel) -> the key."""
    with open(os.path.join(HERE, 'roster-levels.json'), encoding='utf-8') as f:
        labels = json.load(f)['labels']
    m = {k.replace('-', '').replace(' ', ''): v for k, v in labels.items()}
    m.update({v: v for v in labels.values()})
    return m


def parse_decl(text):
    """The first MaffsLevel.resolve({...}) declaration as {slug, levels, fallback, boards} (string literals), or None."""
    m = RESOLVE.search(text)
    if not m:
        return None
    body = m.group(1)

    def lit(name):
        mm = re.search(r'\b' + name + r'\s*:\s*([\'"])([^\'"]*)\1', body)
        return mm.group(2) if mm else None

    def arr(name):
        mm = re.search(r'\b' + name + r'\s*:\s*\[([^\]]*)\]', body)
        return re.findall(r'[\'"]([^\'"]*)[\'"]', mm.group(1)) if mm else None
    return {'slug': lit('slug'), 'levels': arr('levels'), 'fallback': lit('fallback'), 'boards': arr('boards') or []}


def analyse(files, roster, games, migrated, at_start):
    """(errors, not_yet). Pure: the selftest plants faults in `files`."""
    errors = []
    to_key = label_to_key()
    served = {}
    decls = {}
    for slug in games:
        text = files.get('games/%s/index.html' % slug, '')
        d = parse_decl(text)
        has_call = 'MaffsLevel.resolve' in text
        if has_call and slug not in migrated:
            errors.append('%s calls MaffsLevel.resolve but is not in MIGRATED: move it there and off NOT_YET_AT_START' % slug)
        if slug in migrated and not has_call:
            errors.append('%s is in MIGRATED but its page no longer calls MaffsLevel.resolve' % slug)
        if slug not in migrated and slug not in at_start:
            errors.append('%s is not in NOT_YET_AT_START, so it must be migrated from the start (canon 4.5)' % slug)
        if slug in migrated and has_call:
            if d is None or d['levels'] is None or d['fallback'] is None or d['slug'] is None:
                errors.append('%s: MaffsLevel.resolve must declare slug, levels and fallback as string literals' % slug)
                served[slug] = set(roster.get(slug, []))
                continue
            decls[slug] = d
            served[slug] = set(d['levels'])
            want = set(roster.get(slug, []))
            if d['slug'] != slug:
                errors.append('%s: declares slug %r' % (slug, d['slug']))
            if set(d['levels']) != want:
                errors.append('%s: declares levels %s but the roster lists %s (scripts/roster-levels.json)'
                              % (slug, sorted(d['levels']), sorted(want)))
            if d['fallback'] not in d['levels']:
                errors.append('%s: fallback %r is not one of its levels' % (slug, d['fallback']))
            if 'schools/assets/level.js' not in text:
                errors.append('%s: migrated, but the page does not load schools/assets/level.js' % slug)
            if OWN_READ.search(RESOLVE.sub('', text)):
                errors.append('%s: migrated, but the page still reads ?level with its own code: MaffsLevel is the one reader' % slug)
            for _, key in SUBMIT.findall(text):
                if key not in d['levels'] and key not in d['boards']:
                    errors.append('%s: submits under %r, which it declares neither as a level nor as a board' % (slug, key))
        else:
            served[slug] = set(roster.get(slug, []))

    def check_link(where, slug, key):
        if slug not in served:
            return                                  # not a game folder (a different ../<x>/ link)
        if key not in served[slug]:
            errors.append('%s: links %s/?level=%s, but %s serves %s' % (where, slug, key, slug, sorted(served[slug])))

    for path, text in sorted(files.items()):
        if path.endswith('.js'):
            continue
        for m in LINK.finditer(text):
            if path.startswith('games/') and m.group(0).startswith('games/'):
                continue
            check_link(path, m.group(1), m.group(2))
        for m in CARD.finditer(text):
            href, dl = m.group(1), m.group(2)
            lm = LINK.search(href)
            if not lm:
                continue
            slug = lm.group(1)
            if slug not in served:
                continue
            for tok in dl.split():
                key = to_key.get(tok.replace('-', ''))
                if key is None:
                    errors.append('%s: card %s lists an unknown level %r' % (path, slug, tok))
                elif key not in served[slug] and not any(key in FILTER_ALIAS.get(k, ()) for k in served[slug]):
                    errors.append('%s: card %s lists %r (%s), but the game serves %s' % (path, slug, tok, key, sorted(served[slug])))
    not_yet = sorted(set(at_start) - set(migrated))
    return errors, not_yet


def load(root):
    roster, _ = bc.roster_levels()
    games = sorted(d for d in os.listdir(os.path.join(root, 'games'))
                   if os.path.isfile(os.path.join(root, 'games', d, 'index.html')))
    return read_files(root), roster, games


def selftest(root):
    files, roster, games = load(root)
    ok = True
    base, _ = analyse(files, roster, games, MIGRATED, NOT_YET_AT_START)
    if base:
        print('self-test: the tree fails before any fault is planted: %s' % base[0])
        return False
    slug = next(g for g in games if roster.get(g) == ['gcse'])    # a game that does not serve alevel
    page = 'games/%s/index.html' % slug
    good = "<script src=\"../../schools/assets/level.js\"></script><script>var level=MaffsLevel.resolve({slug:'%s',levels:%s,fallback:'%s'});</script>"
    levels = roster[slug]
    plants = [
        ('a declaration that differs from the roster',
         {page: files[page] + good % (slug, json.dumps(levels + ['alevel']).replace('"', "'"), levels[0])},
         'but the roster lists'),
        ('a link to a key the game does not serve',
         {'index.html': files['index.html'] + '<a href="games/%s/?level=alevel">x</a>' % slug}, 'but %s serves' % slug),
        ('a migrated game that reads ?level itself',
         {page: files[page] + good % (slug, json.dumps(levels).replace('"', "'"), levels[0])
          + "<script>var l=new URLSearchParams(location.search).get('level');</script>"}, 'reads ?level with its own code'),
    ]
    for name, patch, want in plants:
        f2 = dict(files)
        f2.update(patch)
        errs, _ = analyse(f2, roster, games, MIGRATED | {slug}, NOT_YET_AT_START)
        caught = any(want in e for e in errs)
        print('  self-test %-44s %s' % (name, 'caught' if caught else '*** MISSED ***'))
        ok = ok and caught
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--report', action='store_true')
    args = ap.parse_args()
    ok = True
    if args.selftest:
        ok = selftest(ROOT)
    if args.check or args.report or not args.selftest:
        files, roster, games = load(ROOT)
        errors, not_yet = analyse(files, roster, games, MIGRATED, NOT_YET_AT_START)
        for e in errors:
            print('FAIL  ' + e)
        print('%d games, %d migrated, %d on NOT_YET (reported, never failed; it may only shrink)'
              % (len(games), len(MIGRATED), len(not_yet)))
        if args.report and not_yet:
            print('NOT_YET: ' + ' '.join(not_yet))
        ok = ok and not errors
    print('OK' if ok else 'FAILED')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
