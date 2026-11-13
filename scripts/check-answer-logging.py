#!/usr/bin/env python3
# ci-line: Answer logging (no roster game logs only right answers: a page whose every question_answered call passes a literal correct:true fails; escape rooms out of scope; four plants caught and five controls pass) | --selftest && --check
# ci-deps: games/ .claude/rules/game-roster.md scripts/bank_common.py scripts/check-level-logged.py
"""Does every game that logs question_answered also log its wrong answers?
(contract ANSWER-LOGGING-WRONG, Jon's ruling 13 Nov 2026 19:29.)

    python scripts/check-answer-logging.py --check       # the site (CI, every PR)
    python scripts/check-answer-logging.py --selftest    # planted faults are caught

The fault it stops: a retry-until-right game that sends question_answered only on the right answer, always with
`correct: true`. Wrong answers never reach GA4 or the Sheet, the game's accuracy reads 100%, the Dashboard's
Hardest Questions cannot see its misconceptions, and a game that ends on lives logs no answer at all for the
question it ended on. Prime Sprint and Chart Interrogator both did this until this contract; two games make a class,
so the class is closed here rather than in the Sheet.

Rule. For every live game page (games/<slug>/index.html for each numbered row of .claude/rules/game-roster.md,
listed and unlisted alike), find each mfg('question_answered', {...}) call (or a call of the page's own wrapper round mfg, such as the resit
strand's ev('question_answered', {...}): any call whose first argument is that literal), comments ignored, and read the value its
object passes for `correct`. A page fails when at least one call passes a literal true (`true`, or the minified
`!0`) and no call passes anything else for `correct`: every answer it logs is logged right. One call that can say
false (a variable, an expression, a literal false) passes the page; a call with no `correct` key says neither and is
not counted either way. A retry game logs one question_answered per question with correct = right first time and
attempts = tries (Jon's ruling (a), 13 Nov 2026).

Out of scope: escape rooms (escape-rooms/), which log per lock attempt (one event for every try at a lock, right or
wrong) and are not roster games; shared assets (schools/assets/), which pass `correct` through from their caller;
pages that are not a roster game's index.html (a withdrawn holding page, a kept original). The check reads source,
never plays a game: whether a game's variable is ever false at run time is its own verifier's business.
"""
import argparse
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402


def _load_strip_comments():
    """check-level-logged.py's comment blanker (length kept, a // after a colon kept as a URL): one copy, not two."""
    spec = importlib.util.spec_from_file_location('check_level_logged', os.path.join(HERE, 'check-level-logged.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.strip_comments


strip_comments = _load_strip_comments()

# mfg itself, or a page's own wrapper round it (the resit strand's ev(name, params)): any call whose first argument is
# the literal 'question_answered'. Reading mfg( alone missed 15 roster games.
CALL = re.compile(r'''(?<![\w$])[A-Za-z_$][\w$]*(?:\.[A-Za-z_$][\w$]*)*\s*\(\s*(['"])question_answered\1\s*,''')
LITERAL_TRUE = {'true', '!0'}


def _span(code, i, close):
    """Index just past the bracket that closes the one opened before code[i] (strings skipped)."""
    pairs = {'(': ')', '[': ']', '{': '}'}
    stack = [close]
    q = None
    j = i
    while j < len(code) and stack:
        c = code[j]
        if q:
            if c == '\\':
                j += 1
            elif c == q:
                q = None
        elif c in '\'"`':
            q = c
        elif c in pairs:
            stack.append(pairs[c])
        elif c in ')]}':
            stack.pop()
        j += 1
    return j


def _top_level_parts(body):
    """The comma-separated parts of an object literal's body, split at depth 0 only."""
    parts, depth, q, start = [], 0, None, 0
    j = 0
    while j < len(body):
        c = body[j]
        if q:
            if c == '\\':
                j += 1
            elif c == q:
                q = None
        elif c in '\'"`':
            q = c
        elif c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
        elif c == ',' and depth == 0:
            parts.append(body[start:j])
            start = j + 1
        j += 1
    parts.append(body[start:])
    return parts


KEY = re.compile(r'''^\s*(['"]?)correct\1\s*:(.*)$''', re.S)


def answer_calls(src):
    """[(line, correct)] for every mfg('question_answered', ...) call on a page (or a local wrapper's). correct is the value's source text,
    stripped (ES shorthand `correct` reads as the variable correct); None when the call's second argument is not an object literal (unknown: not counted as literal true)
    or the object has no `correct` key."""
    code = strip_comments(src)
    out = []
    for m in CALL.finditer(code):
        line = code.count('\n', 0, m.start()) + 1
        k = m.end()
        while k < len(code) and code[k].isspace():
            k += 1
        value = None
        if code[k:k + 1] == '{':
            end = _span(code, k + 1, '}')
            for part in _top_level_parts(code[k + 1:end - 1]):
                km = KEY.match(part)
                if km:
                    value = km.group(2).strip()
                elif part.strip() == 'correct':   # ES shorthand { correct }: the variable named correct
                    value = 'correct'
        out.append((line, value))
    return out


def page_fault(src):
    """None, or why the page logs only right answers."""
    calls = answer_calls(src)
    trues = [ln for ln, v in calls if v in LITERAL_TRUE]
    others = [ln for ln, v in calls if v is not None and v not in LITERAL_TRUE]
    if trues and not others:
        return ('%d question_answered call(s), every one correct:true (line %s): wrong answers are never logged. '
                'Log one event per question with correct = right first time and attempts = tries (Jon, 13 Nov 2026)'
                % (len(trues), ', '.join(str(x) for x in trues)))
    return None


def roster_pages(root):
    """[(slug, path)] for every roster game's index.html that exists under root."""
    _, order = bc.roster_levels()
    out = []
    for slug in order:
        p = os.path.join(root, 'games', slug, 'index.html')
        if os.path.exists(p):
            out.append((slug, p))
    return out


def scan(pages):
    """(errors, n pages that log question_answered) for [(slug, path)]."""
    errors, n = [], 0
    for slug, p in pages:
        with open(p, encoding='utf-8', errors='replace') as fh:
            src = fh.read()
        if not answer_calls(src):
            continue
        n += 1
        why = page_fault(src)
        if why:
            errors.append('%s: %s' % (slug, why))
    return errors, n


def selftest():
    import tempfile
    ok = True

    def page(script):
        return '<!doctype html><html><body><script>\n%s\n</script></body></html>' % script

    def case(name, src, expect_err):
        nonlocal ok
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, 'index.html')
            with open(p, 'w', encoding='utf-8', newline='') as fh:
                fh.write(src)
            errs, n = scan([('g', p)])
        good = n == 1 and bool(errs) == expect_err
        print('  %-62s %s' % (name, 'ok' if good else 'WRONG (pages %d, %s)' % (n, errs)))
        ok = ok and good

    one = "mfg('question_answered',{game_slug:'g',level:lv,correct:true,question_index:i+1});"
    two_a = "mfg('question_answered',{game_slug:'g',level:lv,correct:true,question_index:i+1});"
    two_b = 'mfg("question_answered", { game_slug: "g", level: lv, correct: true, question_index: i + 1 });'
    case('PLANT: the only call is correct:true', page(one), True)
    case('PLANT: two calls, both correct:true (either spacing)', page(two_a + '\n' + two_b), True)
    case("PLANT: correct:!0 (minified true)", page(one.replace('correct:true', 'correct:!0')), True)
    case('CONTROL: correct:ok passes', page(one.replace('correct:true', 'correct:ok')), False)
    case('a true call beside a variable one passes', page(one + '\n' + one.replace('correct:true', 'correct:c')),
         False)
    case('shorthand { correct, attempts } passes',
         page("mfg('question_answered', { game_slug: 'g', level: lv, correct, attempts });"), False)
    case("PLANT: a page's own wrapper, ev('question_answered', {correct:true})",
         page(one.replace("mfg('question_answered'", "ev('question_answered'")), True)
    case('a commented-out false call does not rescue the page',
         page(one + '\n// ' + one.replace('correct:true', 'correct:ok')), True)
    case('a nested correct:false is not the call\'s own key',
         page(one.replace('correct:true', "extra:{correct:false},correct:true")), True)
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if not (a.check or a.selftest):
        a.check = True
    status = 0
    if a.selftest:
        print('self-test:')
        if not selftest():
            print('FAIL: a planted fault was not caught, or a control failed')
            return 1
        print('PASS: planted faults caught, controls pass')
    if a.check:
        pages = roster_pages(ROOT)
        errors, n = scan(pages)
        for e in errors:
            print('FAIL:', e)
        if errors:
            status = 1
        else:
            print('PASS: %d roster pages log question_answered; none logs only correct:true (%d roster pages read)'
                  % (n, len(pages)))
    return status


if __name__ == '__main__':
    sys.exit(main())
