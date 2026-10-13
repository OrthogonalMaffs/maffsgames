#!/usr/bin/env python3
# ci-line: Level logged (every mfg event carries the level the game resolved through MaffsLevel, never a string literal; 'all' only where the declaration lists it in boards; one plant) | --selftest && --check
# ci-deps: games/ escape-rooms/ schools/assets/level.js
"""Does every analytics event log the level the game actually resolved?
(contract LEVEL-LOGGED, Jon, 13 Oct 2026; triage rule R10; SWEEP-1 findings eigenvector-engine-s1-004,
normal-navigator-s1-007).

    python scripts/check-level-logged.py --check       # the site (CI, every PR)
    python scripts/check-level-logged.py --selftest    # planted faults are caught
    python scripts/check-level-logged.py --report      # also print the NOT_YET list

The faults it stops: a game that serves two levels (or three) and writes `level: 'further'` into every mfg(...)
call logs a Level 4 or Core play as the other level, and every level-based GA4 report is wrong.

Rule. In every mfg(...) call under games/ and escape-rooms/ (pages and their local scripts), the value of the
`level` key is never a string literal (nor an expression containing one). It is the variable that holds
MaffsLevel.resolve's result. One literal is allowed: 'all', and only where the page's MaffsLevel.resolve
declaration lists 'all' in boards (the game keeps one combined board and logs it as such, SR-29 style).

This reads mfg calls only. A literal level given to MaffsLeaderboard.submitScore or MaffsScoreHistory.record is
the leaderboard's own key (SR-29 keeps it) and is not this check's business.

NOT_YET (built the way check-levels.py's is): games reported, never failed, that still log a literal. It may only
shrink: a game on it that no longer has a literal fails ("remove it from NOT_YET"), and a game not on it with a
literal fails.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# characteristic-quest: the cloud lane fixes it in its SWEEP-1-RULINGS PR for that game (with R7) after #359 and
# removes it from this list in that PR (Jon, 13 Oct 2026).
NOT_YET = {'characteristic-quest'}

DECL = re.compile(r'MaffsLevel\.resolve\s*\(\s*\{(.*?)\}\s*\)', re.S)
BOARDS = re.compile(r'boards\s*:\s*\[([^\]]*)\]')
LEVEL_KEY = re.compile(r'''[{,]\s*['"]?level['"]?\s*:\s*([^,}]+)''')


def strip_comments(s):
    """Blank // and /* */ comments (length kept, so line numbers hold). A // after a colon is a URL, not a comment."""
    out = []
    i = 0
    n = len(s)
    q = None
    while i < n:
        c = s[i]
        if q:
            out.append(c)
            if c == '\\' and i + 1 < n:
                out.append(s[i + 1])
                i += 2
                continue
            if c == q:
                q = None
            i += 1
        elif c in '\'"`':
            q = c
            out.append(c)
            i += 1
        elif c == '/' and s[i + 1:i + 2] == '/' and s[i - 1:i] != ':':
            while i < n and s[i] != '\n':
                out.append(' ')
                i += 1
        elif c == '/' and s[i + 1:i + 2] == '*':
            j = s.find('*/', i + 2)
            j = n if j < 0 else j + 2
            out.append(''.join(ch if ch == '\n' else ' ' for ch in s[i:j]))
            i = j
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def mfg_levels(src):
    """[(line, value)] for the `level` key of every mfg(...) call."""
    code = strip_comments(src)
    found = []
    for m in re.finditer(r'(?<![\w$.])mfg\s*\(', code):
        i = m.end()
        depth = 1
        j = i
        q = None
        while j < len(code) and depth:
            c = code[j]
            if q:
                if c == '\\':
                    j += 1
                elif c == q:
                    q = None
            elif c in '\'"`':
                q = c
            elif c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            j += 1
        lm = LEVEL_KEY.search(code[i:j - 1])
        if lm:
            found.append((code.count('\n', 0, m.start()) + 1, lm.group(1).strip()))
    return found


def declared_boards(src):
    d = DECL.search(strip_comments(src))
    if not d:
        return set()
    b = BOARDS.search(d.group(1))
    return set(re.findall(r'''['"]([^'"]+)['"]''', b.group(1))) if b else set()


def literal_faults(src):
    """[(line, value, why)] for the mfg level values on a page that are not allowed."""
    boards = declared_boards(src)
    faults = []
    for line, v in mfg_levels(src):
        if not re.search(r'''['"`]''', v):
            continue
        if re.fullmatch(r'''(['"])all\1''', v) and 'all' in boards:
            continue
        faults.append((line, v))
    return faults


def pages(root):
    for area in ('games', 'escape-rooms'):
        base = os.path.join(root, area)
        for dp, dn, fn in os.walk(base):
            dn[:] = [d for d in dn if d not in ('node_modules', '.git')]
            for f in fn:
                if f.endswith(('.html', '.js')):
                    p = os.path.join(dp, f)
                    yield os.path.relpath(p, root).replace(os.sep, '/'), p


def slug_of(rel):
    parts = rel.split('/')
    return parts[1] if len(parts) > 1 else rel


def scan(root, not_yet):
    errors, reported = [], []
    bad = {}
    for rel, p in pages(root):
        with open(p, encoding='utf-8', errors='replace') as fh:
            src = fh.read()
        if 'mfg' not in src:
            continue
        for line, v in literal_faults(src):
            bad.setdefault(slug_of(rel), []).append('%s:%d level: %s' % (rel, line, v))
    for slug, hits in sorted(bad.items()):
        if slug in not_yet:
            reported.append('%s: %d literal level(s), reported (NOT_YET): %s' % (slug, len(hits), hits[0]))
        else:
            errors.append('%s: %d mfg call(s) log a literal level, e.g. %s. Log the variable that holds '
                          "MaffsLevel.resolve's result (R10)." % (slug, len(hits), hits[0]))
    for slug in sorted(not_yet):
        if slug not in bad:
            errors.append('%s is on NOT_YET but no longer logs a literal level: remove it from NOT_YET' % slug)
    return errors, reported


def selftest():
    import tempfile
    ok = True

    def case(name, files, not_yet, expect_err):
        nonlocal ok
        with tempfile.TemporaryDirectory() as d:
            for rel, text in files.items():
                p = os.path.join(d, rel)
                os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, 'w', encoding='utf-8') as fh:
                    fh.write(text)
            errs, _ = scan(d, not_yet)
        got = bool(errs)
        print('  %-52s %s' % (name, 'ok' if got == expect_err else 'WRONG (%s)' % errs))
        ok = ok and got == expect_err

    decl = "<script>var resolvedLevel=MaffsLevel.resolve({slug:'g',levels:['a','b'],fallback:'a'%s});</script>"
    good = decl % '' + "<script>mfg('game_started',{game_slug:'g',level:resolvedLevel});</script>"
    case('PLANT: a literal level in an mfg call', {'games/g/index.html': decl % '' +
         "<script>mfg('game_started',{game_slug:'g',level:'a'});</script>"}, set(), True)
    case('a resolved variable passes', {'games/g/index.html': good}, set(), False)
    case("'all' without boards fails", {'games/g/index.html': decl % '' +
         "<script>mfg('x',{level:'all'});</script>"}, set(), True)
    case("'all' with boards:['all'] passes", {'games/g/index.html': decl % ",boards:['all']" +
         "<script>mfg('x',{level:'all'});</script>"}, set(), False)
    case('a literal in a comment is ignored', {'games/g/index.html': good +
         "<script>// mfg('x',{level:'gcse'})\n</script>"}, set(), False)
    case('a literal on NOT_YET is reported, not failed', {'games/g/index.html': decl % '' +
         "<script>mfg('x',{level:'a'});</script>"}, {'g'}, False)
    case('a NOT_YET game with no literal fails (stale)', {'games/g/index.html': good}, {'g'}, True)
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--report', action='store_true')
    a = ap.parse_args()
    if not (a.check or a.selftest or a.report):
        a.check = True
    status = 0
    if a.selftest:
        print('self-test:')
        if not selftest():
            print('FAIL: a planted fault was not caught')
            return 1
        print('PASS: planted faults caught')
    if a.check or a.report:
        errors, reported = scan(ROOT, NOT_YET)
        if a.report or reported:
            for r in reported:
                print('NOT_YET:', r)
        if errors:
            for e in errors:
                print('FAIL:', e)
            status = 1
        else:
            print('PASS: no mfg call logs a literal level (NOT_YET: %s)' % (', '.join(sorted(NOT_YET)) or 'empty'))
    return status


if __name__ == '__main__':
    sys.exit(main())
