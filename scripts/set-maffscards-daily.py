#!/usr/bin/env python3
# ci-line: MaffsCards daily result (scripts/set-maffscards-daily.py: the date, result, rounds and line Jon's Creator sheet sends are validated before games/maffscards/daily.json is written; every planted bad input refused; the committed file is all nulls or a valid result) | --selftest && --check
# ci-deps: scripts/set-maffscards-daily.py games/maffscards/daily.json
r"""Write Jon's result for today's MaffsCards deal (contract DAILY-DEAL, 25 Nov 2026).

.github/workflows/maffscards-daily.yml runs this with the four fields Jon typed into his Creator sheet
(docs/apps-script-creator.md) or into the workflow's own Run workflow form. It validates them and writes
games/maffscards/daily.json, which the workflow then commits to main; the page (games/maffscards/index.html) reads
the file and shows the result only on the file's own UK date.

    python scripts/set-maffscards-daily.py --date 2026-11-26 --result won --rounds 14 --line="..."
    python scripts/set-maffscards-daily.py --selftest      # planted bad inputs refused, good inputs written
    python scripts/set-maffscards-daily.py --check         # the committed daily.json is all nulls or a valid result

REFUSED (nothing is written, exit 1):
  date     not YYYY-MM-DD, not a real date, or neither today nor yesterday in the UK (Europe/London);
  result   not "won" or "lost" (any case);
  rounds   not a whole number, or outside 10 to 100 for a win, 10 to 200 for a loss.

THE LINE is optional and is never a reason to refuse: it is written as null (so the page shows a line from its own
pool) when it is empty, longer than 240 characters, holds "<" or ">", or holds contact details. Line breaks and runs
of spaces become one space first.

Contact details: the repository has no personal-details check to call (the list the lanes scan with is private and
is kept outside this public repository on purpose), so the line is checked here for what can be recognised without
one: an e-mail address, a web address, an @name, or a run of seven or more digits (a phone number).

The UK date is worked out here, with no time zone database: British Summer Time runs from 01:00 UTC on the last
Sunday of March to 01:00 UTC on the last Sunday of October.
"""
import argparse
import contextlib
import datetime as dt
import io
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'games', 'maffscards', 'daily.json')
LINE_MAX = 240
ROUNDS = {'won': (10, 100), 'lost': (10, 200)}
EMPTY = {'date': None, 'result': None, 'rounds': None, 'line': None}
CONTACT = [
    ('an e-mail address', re.compile(r'[^\s@]+@[^\s@]+\.[^\s@]+')),
    ('a web address', re.compile(r'(?i)\b(?:https?://|www\.)\S+|\b[\w-]+\.(?:co\.uk|org\.uk|ac\.uk|sch\.uk|com|org|net|io|uk)\b')),
    ('an @name', re.compile(r'(?<!\w)@\w{2,}')),
    ('a phone number', re.compile(r'(?:\d[\s().+-]{0,2}){7,}')),
]


class Refused(Exception):
    pass


def last_sunday(year, month):
    d = dt.date(year, month, 31)                    # March and October both have 31 days
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def uk_date(now):
    """The calendar date in the UK at `now` (an aware datetime)."""
    now = now.astimezone(dt.timezone.utc)
    on = dt.datetime.combine(last_sunday(now.year, 3), dt.time(1), dt.timezone.utc)
    off = dt.datetime.combine(last_sunday(now.year, 10), dt.time(1), dt.timezone.utc)
    return (now + dt.timedelta(hours=1 if on <= now < off else 0)).date()


def clean_line(text):
    """(the line to write or None, why it was dropped or None)."""
    line = re.sub(r'\s+', ' ', text or '').strip()
    if not line:
        return None, None
    if '<' in line or '>' in line:
        return None, 'it holds "<" or ">"'
    if len(line) > LINE_MAX:
        return None, 'it is %d characters, more than %d' % (len(line), LINE_MAX)
    for what, rx in CONTACT:
        if rx.search(line):
            return None, 'it holds %s' % what
    return line, None


def validate(date, result, rounds, line, now):
    """The record to write and a note about the line. Raises Refused with the reason."""
    date = (date or '').strip()
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
        raise Refused('date %r is not YYYY-MM-DD' % date)
    try:
        day = dt.date.fromisoformat(date)
    except ValueError:
        raise Refused('date %r is not a real date' % date)
    today = uk_date(now)
    if day not in (today, today - dt.timedelta(days=1)):
        raise Refused('date %s is neither today (%s) nor yesterday in the UK' % (date, today.isoformat()))
    result = (result or '').strip().lower()
    if result not in ROUNDS:
        raise Refused('result %r is not "won" or "lost"' % result)
    rounds = (rounds or '').strip()
    if not re.fullmatch(r'\d{1,4}', rounds):
        raise Refused('rounds %r is not a whole number' % rounds)
    n = int(rounds)
    lo, hi = ROUNDS[result]
    if not lo <= n <= hi:
        raise Refused('rounds %d is outside %d to %d for a game Jon %s' % (n, lo, hi, result))
    text, why = clean_line(line)
    return {'date': date, 'result': result, 'rounds': n, 'line': text}, why


def write(record, path):
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def check_file(path):
    """Why the file is not all nulls or a valid result; [] if it is."""
    try:
        with open(path, encoding='utf-8') as f:
            d = json.load(f)
    except (OSError, ValueError) as e:
        return ['%s does not read as JSON: %s' % (os.path.basename(path), e)]
    if not isinstance(d, dict) or sorted(d) != sorted(EMPTY):
        return ['daily.json does not hold exactly date, result, rounds and line']
    if d == EMPTY:
        return []
    bad = []
    try:
        ok_date = isinstance(d['date'], str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', d['date']) and dt.date.fromisoformat(d['date'])
    except ValueError:
        ok_date = False
    if not ok_date:
        bad.append('date %r is not a real YYYY-MM-DD date' % (d['date'],))
    if d['result'] not in ROUNDS:
        bad.append('result %r is not "won" or "lost"' % (d['result'],))
    elif type(d['rounds']) is not int or not ROUNDS[d['result']][0] <= d['rounds'] <= ROUNDS[d['result']][1]:
        bad.append('rounds %r is not a whole number in range for a game Jon %s' % (d['rounds'], d['result']))
    if d['line'] is not None and (not isinstance(d['line'], str) or clean_line(d['line']) != (d['line'], None)):
        bad.append('line %r is not null or a plain line this script would write' % (d['line'],))
    return bad


def selftest():
    utc = dt.timezone.utc
    ok = True

    def expect(what, cond):
        nonlocal ok
        print('  self-test %-58s %s' % (what, 'ok' if cond else '*** FAILED ***'))
        ok = ok and cond

    # the UK date across both clock changes (2027: BST from 28 March to 31 October)
    for stamp, want in (((2026, 11, 25, 23, 59), '2026-11-25'), ((2026, 11, 26, 0, 0), '2026-11-26'),
                        ((2027, 3, 28, 0, 59), '2027-03-28'), ((2027, 3, 28, 23, 30), '2027-03-29'),
                        ((2027, 6, 1, 22, 59), '2027-06-01'), ((2027, 6, 1, 23, 0), '2027-06-02'),
                        ((2027, 10, 30, 23, 30), '2027-10-31'), ((2027, 10, 31, 23, 30), '2027-10-31'),
                        ((2026, 3, 29, 23, 30), '2026-03-30'), ((2026, 10, 25, 23, 30), '2026-10-25')):
        got = uk_date(dt.datetime(*stamp, tzinfo=utc)).isoformat()
        expect('UK date at %04d-%02d-%02d %02d:%02d UTC is %s' % (stamp + (want,)), got == want)
    expect('last Sundays of March and October 2027', (last_sunday(2027, 3), last_sunday(2027, 10)) == (dt.date(2027, 3, 28), dt.date(2027, 10, 31)))

    now = dt.datetime(2026, 11, 26, 7, 30, tzinfo=utc)
    good = [
        (('2026-11-26', 'won', '14', ''), {'date': '2026-11-26', 'result': 'won', 'rounds': 14, 'line': None}),
        (('2026-11-25', 'lost', '31', ''), {'date': '2026-11-25', 'result': 'lost', 'rounds': 31, 'line': None}),
        ((' 2026-11-26 ', ' WON ', ' 10 ', None), {'date': '2026-11-26', 'result': 'won', 'rounds': 10, 'line': None}),
        (('2026-11-26', 'Won', '100', '  Beat that,\n Marvin.  '), {'date': '2026-11-26', 'result': 'won', 'rounds': 100, 'line': 'Beat that, Marvin.'}),
        (('2026-11-26', 'lost', '200', 'x' * 240), {'date': '2026-11-26', 'result': 'lost', 'rounds': 200, 'line': 'x' * 240}),
        (('2026-11-26', 'won', '12', "Jon took {N} rounds. Marvin isn't speaking to him."),
         {'date': '2026-11-26', 'result': 'won', 'rounds': 12, 'line': "Jon took {N} rounds. Marvin isn't speaking to him."}),
        (('2026-11-26', 'won', '12', 'Marvin recited the first 1,000 digits of pi. All 96 factors of nothing.'),
         {'date': '2026-11-26', 'result': 'won', 'rounds': 12, 'line': 'Marvin recited the first 1,000 digits of pi. All 96 factors of nothing.'}),
    ]
    for args, want in good:
        try:
            got = validate(*args, now=now)[0]
        except Refused as e:
            got = 'refused: %s' % e
        expect('good input %r' % (args[:3],), got == want)
    bad = [
        ('a date two days old', ('2026-11-24', 'won', '14', '')), ("tomorrow's date", ('2026-11-27', 'won', '14', '')),
        ('a date written day first', ('26-11-2026', 'won', '14', '')), ('a date that does not exist', ('2026-11-31', 'won', '14', '')),
        ('no date', ('', 'won', '14', '')), ('a date with more after it', ('2026-11-26x', 'won', '14', '')),
        ('a result that is neither', ('2026-11-26', 'draw', '14', '')), ('no result', ('2026-11-26', '', '14', '')),
        ('rounds not a number', ('2026-11-26', 'won', 'ten', '')), ('rounds with a decimal', ('2026-11-26', 'won', '14.5', '')),
        ('negative rounds', ('2026-11-26', 'won', '-14', '')), ('no rounds', ('2026-11-26', 'won', '', '')),
        ('a win in 9 rounds', ('2026-11-26', 'won', '9', '')), ('a win in 101 rounds', ('2026-11-26', 'won', '101', '')),
        ('a loss in 9 rounds', ('2026-11-26', 'lost', '9', '')), ('a loss in 201 rounds', ('2026-11-26', 'lost', '201', '')),
    ]
    for what, args in bad:
        try:
            validate(*args, now=now)
            refused = False
        except Refused:
            refused = True
        expect('refused: %s' % what, refused)
    # just after UK midnight in summer, yesterday is still accepted and the day before is not
    summer = dt.datetime(2027, 6, 1, 23, 5, tzinfo=utc)       # 00:05 on 2 June in the UK
    for date, want in (('2027-06-02', True), ('2027-06-01', True), ('2027-05-31', False), ('2027-06-03', False)):
        try:
            validate(date, 'won', '14', '', now=summer)
            got = True
        except Refused:
            got = False
        expect('at 23:05 UTC on 1 June 2027, %s is %s' % (date, 'accepted' if want else 'refused'), got == want)
    lines = [
        ('a tag', 'Marvin <b>lost</b>.'), ('a lone "<"', '9 < 10, Marvin.'), ('a lone ">"', '10 > 9, Marvin.'),
        ('241 characters', 'x' * 241), ('an e-mail address', 'Tell marvin@example.com he lost.'),
        ('a web address', 'See https://example.com/marvin'), ('a bare web address', 'See example.co.uk for more.'),
        ('an @name', 'Follow @marvin for excuses.'), ('a phone number', 'Call Marvin on 07700 900123.'),
    ]
    for what, text in lines:
        try:
            rec, why = validate('2026-11-26', 'won', '14', text, now=now)
        except Refused:
            rec, why = {'line': 'refused'}, None
        expect('line dropped, the result still written: %s' % what, rec['line'] is None and bool(why) and rec.get('rounds') == 14)
    for text in ('', '   ', '\n'):
        expect('an empty line (%r) is null with no complaint' % text, clean_line(text) == (None, None))

    # the file: written, read back, and judged by --check; a refusal leaves the file as it was
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'daily.json')
        write(EMPTY, path)
        expect('the all-null file passes --check', check_file(path) == [])
        before = open(path, encoding='utf-8').read()
        quiet = io.StringIO()                       # the two runs' own lines are not part of the self-test's report
        with contextlib.redirect_stdout(quiet):
            status = main(['--date', '2026-11-24', '--result', 'won', '--rounds', '14', '--out', path, '--now', '2026-11-26T07:30:00+00:00'])
        expect('a refused run exits 1 and leaves the file untouched', status == 1 and open(path, encoding='utf-8').read() == before)
        with contextlib.redirect_stdout(quiet):
            status = main(['--date', '2026-11-26', '--result', 'won', '--rounds', '14', '--line=Beat {N}, Marvin says.', '--out', path,
                           '--now', '2026-11-26T07:30:00+00:00'])
        got = json.load(open(path, encoding='utf-8'))
        expect('a good run exits 0 and writes the result', status == 0 and got == {'date': '2026-11-26', 'result': 'won', 'rounds': 14, 'line': 'Beat {N}, Marvin says.'})
        expect('the written file passes --check', check_file(path) == [])
        raw = open(path, 'rb').read()
        expect('the written file is one line ending in a line feed', raw.endswith(b'\n') and raw.count(b'\n') == 1 and b'\r' not in raw)
        for what, body in (('not JSON', '{'), ('a missing key', '{"date": null, "result": null, "rounds": null}'),
                           ('a result with no date', '{"date": null, "result": "won", "rounds": 14, "line": null}'),
                           ('rounds as text', '{"date": "2026-11-26", "result": "won", "rounds": "14", "line": null}'),
                           ('a win in 9 rounds', '{"date": "2026-11-26", "result": "won", "rounds": 9, "line": null}'),
                           ('a line with a tag', '{"date": "2026-11-26", "result": "won", "rounds": 14, "line": "<b>x</b>"}'),
                           ('a 241-character line', '{"date": "2026-11-26", "result": "won", "rounds": 14, "line": "%s"}' % ('x' * 241))):
            with open(path, 'w', encoding='utf-8', newline='') as f:
                f.write(body)
            expect('--check refuses a file with %s' % what, bool(check_file(path)))
    print('self-test: %s' % ('PASS' if ok else 'FAILED'))
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--date', default='')
    ap.add_argument('--result', default='')
    ap.add_argument('--rounds', default='')
    ap.add_argument('--line', default='')
    ap.add_argument('--out', default=OUT, help='the file to write (default: games/maffscards/daily.json)')
    ap.add_argument('--now', help='an ISO date and time to use as now (tests only)')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--check', action='store_true', help='judge the committed daily.json; write nothing')
    args = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError, io.UnsupportedOperation):
        pass
    if args.selftest:
        return selftest()
    if args.check:
        bad = check_file(args.out)
        for b in bad:
            print('FAIL  ' + b)
        print('FAILED' if bad else 'OK: games/maffscards/daily.json is all nulls or a valid result')
        return 1 if bad else 0
    now = dt.datetime.fromisoformat(args.now) if args.now else dt.datetime.now(dt.timezone.utc)
    try:
        record, why = validate(args.date, args.result, args.rounds, args.line, now)
    except Refused as e:
        print('FAIL  refused, nothing written: %s' % e)
        return 1
    write(record, args.out)
    print('written: Jon %s on %s in %d rounds; %s' % (record['result'], record['date'], record['rounds'],
          'with his line (%d characters)' % len(record['line']) if record['line'] else 'no line, so the page uses its own'))
    if why:
        print('NOTE  the line was not used (the page shows one of its own): %s' % why)
    return 0


if __name__ == '__main__':
    sys.exit(main())
