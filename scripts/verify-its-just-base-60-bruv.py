#!/usr/bin/env python3
# ci-shards: It's Just Base 60, Bruv (the 192-item bank held to the contract's SHA-256 and counts; every answer, decoy and working line recomputed from the item's own fields, without the generator; every decoy's error allowed for its item type (ERR_TYPES) and no two options equal in value; one LINES line per error key, none unused; every stage played to the end, right and wrong marked, each wrong option showing its own line; every item's wrong-answer screen above the fold at 375x667, 390x844, 1280x720 and 1366x768; the start picture's tag, file size and that it shows on the start screen only; fault-injection self-test) | | 1
# ci-deps: games/its-just-base-60-bruv/ tools/its-just-base-60-bruv/
r"""Independent verification for It's Just Base 60, Bruv (games/its-just-base-60-bruv/), contract BASE-60 (Amendment 1),
24 Nov 2026. SR-30: checked from its first PR.

WHAT THIS DOES NOT TRUST
-------------------------------------------------------------------------------
The page holds a fixed bank of 192 items, the output of tools/its-just-base-60-bruv/bank.py embedded one item a line.
This script never runs or imports that generator. It reads the bank from the page and recomputes, with its own
arithmetic on whole minutes and exact fractions:

  Bank     the item lines hash to the contract's SHA-256; 192 items, 24 of each of the eight types, each in its stage;
           ids and prompts unique. Every answer from the item's own fields: minutes from h and m (and back from T), clock
           times from h, m and half (or H and m), durations from start and end, end times from start and the duration,
           decimal hours from h and m (and back from x). Every decoy from its err key and the same fields (the value, or
           one of the values, that named error gives). Every working line rebuilt from the same fields, and its sums true.
           Every prompt states the item's own values. Every decoy's err key is one ERR_TYPES allows for the item's type
           (ERR_TYPES is read from the generator's source as data, by ast, never by running it). Four options an item, no
           two equal in value: a duration against its minutes, a 12-hour against a 24-hour reading of one time, two
           decimals as numbers.
  Lines    LINES in the page has exactly the keys of ERR_TYPES; every key the bank uses has a line and no line is unused.
  Play     in Chromium at 375 x 667, each stage played to the end: ten different items of that stage, four options each,
           every button's dataset.val and text the bank's string; a right answer shows "Right: <answer>" and moves on by
           itself; a wrong answer marks the chosen option wrong and the answer right, shows exactly the LINES line for the
           chosen option's err key, "The answer is <answer>", every working line and Next; the score is the right answers;
           one game_completed and one leaderboard submission on the stage's board; no event but game_started,
           question_answered (with the item's id) and game_completed.
  Why 60?  the panel (details#why) is closed on load at 1280 x 720 and 375 x 667 (Jon, 24 Nov 2026; GAME-TITLE-IN-PLAY).
  Art      the start picture (contract BASE-60-LOOK, 24 Nov 2026): the img.start-art has src assets/start.webp, width 1600,
           height 873 and a non-empty alt; the file is a WebP 1600 x 873 (read from its own header); at 375 x 667 it is
           loaded and showing on the start screen, and not showing once a stage has started.
  Fit      at 375 x 667, 390 x 844, 1280 x 720 and 1366 x 768, for every item and each of its three wrong options: the
           line, the answer, the working and Next all end above the fold (the viewport less the 40 px footer, in page
           coordinates), the prompt and the two marked options are on screen above it, the line shown is that option's,
           and the page does not scroll sideways.

Work units: "bank" (no browser), "play 375x667", "why 1280x720", "why 375x667", "art 375x667", "fit <W>x<H>" (four) and
"plant: <what>" (one per planted fault).

    python scripts/verify-its-just-base-60-bruv.py              # every unit, then the self-test
    python scripts/verify-its-just-base-60-bruv.py --selftest   # the planted faults only
"""
import argparse
import ast
import contextlib
import hashlib
import json
import os
import re
import sys
from collections import Counter
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402
import plant_common as pc  # noqa: E402

SLUG = 'its-just-base-60-bruv'
GAME = os.path.join(ROOT, 'games', SLUG, 'index.html')
GENERATOR = os.path.join(ROOT, 'tools', SLUG, 'bank.py')
SHA256 = '59ed0cba9963c33b2e6a62e80b0e4f64808a3c48eaf30b38034912f140e0eb53'   # contract BASE-60, Amendment 1
MODES = ['stage-1', 'stage-2', 'stage-3', 'stage-4']
TYPES = {'min-to-hm': 1, 'hm-to-min': 1, '12-to-24': 2, '24-to-12': 2, 'duration': 3, 'end-time': 3, 'dec-to-hm': 4, 'hm-to-dec': 4}
STAGE_NAMES = ['Sixty, Not a Hundred', 'Twelve or Twenty-Four', 'How Long, Bruv?', 'The Calculator Lies']
PER = 10
FOOTER = 40
SIZES = [(375, 667), (390, 844), (1280, 720), (1366, 768)]
EVENTS = {'game_started', 'question_answered', 'game_completed'}
ART = os.path.join(ROOT, 'games', SLUG, 'assets', 'start.webp')
ART_TAG = {'src': 'assets/start.webp', 'width': '1600', 'height': '873'}


# ---------------------------------------------------------------- the page's bank and lines, read from its source
def bank_lines(html):
    """The raw item lines of the page's BANK, each as the generator wrote it (the joining comma removed)."""
    m = re.search(r'\n  var BANK = \[\n(.*?)\n  \];', html, re.S)
    if not m:
        raise ValueError('no BANK block in the page')
    lines = m.group(1).split('\n')
    return [ln[:-1] if ln.endswith(',') else ln for ln in lines]


def lines_of(html):
    """The page's LINES object: {err key: line}."""
    m = re.search(r'\n  var LINES = \{\n(.*?)\n  \};', html, re.S)
    if not m:
        raise ValueError('no LINES object in the page')
    out = {}
    for ln in m.group(1).split('\n'):
        k = re.match(r'^\s+([a-z0-9_]+): (".*"),?$', ln)
        if not k:
            raise ValueError('a LINES line this script cannot read: %r' % ln[:60])
        if k.group(1) in out:
            raise ValueError('LINES has %s twice' % k.group(1))
        out[k.group(1)] = json.loads(k.group(2))
    return out


def err_types():
    """ERR_TYPES from the generator's source, as data: the dict literal is read by ast, the file is never run."""
    tree = ast.parse(open(GENERATOR, encoding='utf-8').read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'ERR_TYPES' for t in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError('no ERR_TYPES in %s' % GENERATOR)


# ---------------------------------------------------------------- this script's own arithmetic and formats
def dur(mins_h, mins_m):
    if mins_h == 0:
        return '%d min' % mins_m
    if mins_m == 0:
        return '%d h' % mins_h
    return '%d h %d min' % (mins_h, mins_m)


def c24(h, m):
    return '%02d:%02d' % (h, m)


def c12(h, m, half):
    return '%d:%02d %s' % (h, m, half)


def dec(x):
    """A terminating fraction as its shortest decimal string."""
    x = Fraction(x)
    whole, rest, digits = x.numerator // x.denominator, x - x.numerator // x.denominator, ''
    for _ in range(8):
        if rest == 0:
            break
        rest *= 10
        d = rest.numerator // rest.denominator
        digits += str(d)
        rest -= d
    if rest != 0:
        raise ValueError('%s does not terminate' % x)
    return str(whole) + ('.' + digits if digits else '')


def hm(clock):
    return int(clock[:2]), int(clock[3:])


def whole(x):
    x = Fraction(x)
    return int(x) if x.denominator == 1 else None


def solve(q):
    """(answer, {err: set of the values that error gives}, working lines, strings the prompt must state), from the
    item's own fields only."""
    t = q['type']
    if t == 'min-to-hm':
        T = q['T']
        h, m = divmod(T, 60)
        part = Fraction(T, 60) - h
        errs = {'base100': {dur(T // 100, T % 100)}, 'rounded_hour': {dur(h + 1, m)}}
        if whole(part * 100) is not None:
            errs['decimal_read'] = {dur(h, whole(part * 100))}
        work = ['\\(%d \\div 60 = %d\\) remainder \\(%d\\)' % (T, h, m), '\\(%d\\) min \\(= %d\\) h \\(%d\\) min' % (T, h, m)]
        return dur(h, m), errs, work, ['%d minutes' % T]
    if t == 'hm-to-min':
        h, m = q['h'], q['m']
        T = 60 * h + m
        errs = {'base100': {str(100 * h + m)}, 'decimal_times60': {dec((h + Fraction(m, 100)) * 60)}, 'dropped_minutes': {str(60 * h)}}
        work = ['\\(%d \\times 60 + %d = %d\\)' % (h, m, T), '%s \\(= %d\\) min' % (dur(h, m), T)]
        return str(T), errs, work, [dur(h, m)]
    if t == '12-to-24':
        h, m, half = q['h'], q['m'], q['half']
        shown = c12(h, m, half)
        if half == 'pm' and h != 12:
            ans = c24(h + 12, m)
            errs = {'forgot_pm': {c24(h, m)}, 'added_10': {c24(h + 10, m)}, 'counted_short': {c24(h + 11, m)}}
            first = 'pm, so add 12: \\(%d + 12 = %d\\)' % (h, h + 12)
        elif half == 'pm':
            ans = c24(12, m)
            errs = {'noon_midnight': {c24(0, m)}, 'noon_changed': {c24(22, m), c24(2, m)}}
            first = '12 pm is the hour after midday, so it stays 12'
        elif h != 12:
            ans = c24(h, m)
            errs = {'added_to_morning': {c24(h + 12, m), c24(h + 10, m), c24(h + 11, m)}}
            first = 'am, before midday: the hour stays the same'
        else:
            raise ValueError('a time just after midnight: the contract has none')
        return ans, errs, [first, '%s \\(\\to\\) %s' % (shown, ans)], [shown, '24-hour clock']
    if t == '24-to-12':
        H, m = q['H'], q['m']
        shown = c24(H, m)
        if H > 12:
            ans = c12(H - 12, m, 'pm')
            errs = {'wrong_half': {c12(H - 12, m, 'am')}, 'took_10': {c12(H - 10, m, 'pm')}, 'took_11': {c12(H - 11, m, 'pm')}}
            first = 'After 12, so take off 12: \\(%d - 12 = %d\\), and it is pm' % (H, H - 12)
        elif H == 12:
            ans = c12(12, m, 'pm')
            errs = {'noon_midnight': {c12(12, m, 'am')}, 'noon_changed': {c12(2, m, 'pm'), c12(1, m, 'pm')}}
            first = '12:something is just after midday, so it is 12 pm'
        else:
            raise ValueError('a morning 24-hour time: the contract has none')
        return ans, errs, [first, '%s \\(\\to\\) %s' % (shown, ans)], [shown, '12-hour clock']
    if t == 'duration':
        (sh, sm), (eh, em) = hm(q['start']), hm(q['end'])
        d = (60 * eh + em) - (60 * sh + sm)
        ans = dur(d // 60, d % 60)
        as_numbers = (100 * eh + em) - (100 * sh + sm)
        errs = {'hhmm_subtract': {dur(as_numbers // 100, as_numbers % 100)}, 'no_borrow': {dur(eh - sh, abs(sm - em))},
                'hhmm_as_minutes': {dur(as_numbers // 60, as_numbers % 60)}, 'stopped_at_hour': {dur(0, 60 - sm)}}
        to_hour = 60 - sm
        rest = (60 * eh + em) - 60 * (sh + 1)
        if to_hour + rest != d or rest < 0:
            raise ValueError('%s: the working does not add up' % q['id'])
        nxt = c24(sh + 1, 0)
        work = ['%s to %s is \\(%d\\) min' % (q['start'], nxt, to_hour), '%s to %s is %s' % (nxt, q['end'], dur(rest // 60, rest % 60)),
                '\\(%d\\) min + %s = %s' % (to_hour, dur(rest // 60, rest % 60), ans)]
        return ans, errs, work, [q['start'], q['end']]
    if t == 'end-time':
        sh, sm = hm(q['start'])
        dh, dm = q['dh'], q['dm']
        end = 60 * sh + sm + 60 * dh + dm
        ans = c24(end // 60, end % 60)
        back = 60 * sh + sm - 60 * dh - dm
        errs = {'to_hour_then_all': {c24(sh + dh + 1, dm)}, 'forgot_hour': {c24(sh + dh, sm + dm - 60)},
                'carry_no_subtract': {'%02d:%02d' % (sh + dh + 1, sm + dm)}, 'subtracted': {c24(back // 60, back % 60)}}
        if not 60 <= sm + dm < 120 or (sh + dh + 1, sm + dm - 60) != (end // 60, end % 60):
            raise ValueError('%s: the working does not add up' % q['id'])
        work = ['\\(%d + %d = %d\\) min, which is 1 h \\(%d\\) min' % (sm, dm, sm + dm, sm + dm - 60),
                '\\(%d + %d + 1 = %d\\), so %s' % (sh, dh, sh + dh + 1, ans)]
        return ans, errs, work, [q['start'], dur(dh, dm)]
    if t == 'dec-to-hm':
        x = Fraction(q['x'])
        h = x.numerator // x.denominator
        part = x - h
        mins = whole(part * 60)
        if mins is None:
            raise ValueError('%s: not a whole number of minutes' % q['id'])
        T = 60 * h + mins
        hundredths = int(x * 100)
        errs = {'decimal_read': {dur(h, int(part * 100))}, 'base100': {dur(T // 100, T % 100)},
                'times100': {dur(hundredths // 60, hundredths % 60)}, 'rounded_hour': {dur(h + 1 if part >= Fraction(1, 2) else h, 0)}}
        if whole(part * 10) is not None:
            errs['tenths_read'] = {dur(h, whole(part * 10))}
        work = ['\\(%s \\times 60 = %d\\)' % (dec(part), mins), '%s hours \\(=\\) %s' % (q['x'], dur(h, mins))]
        return dur(h, mins), errs, work, ['%s hours' % q['x']]
    if t == 'hm-to-dec':
        h, m = q['h'], q['m']
        T = 60 * h + m
        ans = dec(Fraction(T, 60))
        errs = {'minutes_as_decimal': {dec(h + Fraction(m, 100))}, 'total_minutes': {str(T)}, 'minutes_over_100': {dec(Fraction(T, 100))}}
        work = ['\\(%d \\div 60 = %s\\)' % (m, dec(Fraction(m, 60))), '%s \\(= %s\\) hours' % (dur(h, m), ans)]
        return ans, errs, work, [dur(h, m)]
    raise ValueError('unknown type %r' % t)


def value(s):
    """What an option is worth, so equal options are caught whatever their form: a clock time as minutes past midnight
    (12-hour or 24-hour), a duration as minutes, anything else as an exact number."""
    m = re.fullmatch(r'(\d\d):(\d\d)', s)
    if m:
        return ('clock', (int(m.group(1)) * 60 + int(m.group(2))) % 1440)
    m = re.fullmatch(r'(\d{1,2}):(\d\d) (am|pm)', s)
    if m:
        return ('clock', ((int(m.group(1)) % 12 + (12 if m.group(3) == 'pm' else 0)) * 60 + int(m.group(2))) % 1440)
    m = re.fullmatch(r'(\d+) h(?: (\d+) min)?', s)
    if m:
        return ('minutes', int(m.group(1)) * 60 + int(m.group(2) or 0))
    m = re.fullmatch(r'(\d+) min', s)
    if m:
        return ('minutes', int(m.group(1)))
    return ('number', Fraction(s))


def worth(q, s):
    """An option's value in the item's own unit: for a question answered in minutes, a bare number is minutes too."""
    kind, v = value(s)
    return ('minutes', v) if kind == 'number' and q['type'] == 'hm-to-min' else (kind, v)


def check_bank(html, out, info):
    raw = bank_lines(html)
    blob = ''.join(ln + '\n' for ln in raw)
    got = hashlib.sha256(blob.encode('utf-8')).hexdigest()
    if got != SHA256:
        out.append('bank: the item lines hash to %s, not the contract\'s %s' % (got, SHA256))
    items = []
    for ln in raw:
        try:
            items.append(json.loads(ln))
        except ValueError:
            out.append('bank: a line is not JSON: %r' % ln[:60])
    if len(items) != 192:
        out.append('bank: %d items, not 192' % len(items))
    counts = Counter((q.get('stage'), q.get('type')) for q in items)
    for t, st in TYPES.items():
        if counts.get((st, t)) != 24:
            out.append('bank: %d %s items in stage %d, not 24' % (counts.get((st, t), 0), t, st))
    for key in counts:
        if TYPES.get(key[1]) != key[0]:
            out.append('bank: %d items of type %r in stage %r' % (counts[key], key[1], key[0]))
    for what in ('id', 'prompt'):
        for v, n in Counter(q.get(what) for q in items).items():
            if n > 1:
                out.append('bank: the %s %r is used %d times' % (what, v, n))
    types = err_types()
    lines = lines_of(html)
    used = set()
    for q in items:
        iid = q.get('id')
        try:
            ans, errs, work, states = solve(q)
        except Exception as e:  # noqa: BLE001
            out.append('%s: cannot be recomputed: %s' % (iid, str(e)[:120]))
            continue
        if q['answer'] != ans:
            out.append('%s: answer %r, recomputed %r' % (iid, q['answer'], ans))
        if q['working'] != work:
            out.append('%s: working %r, recomputed %r' % (iid, q['working'], work))
        for s in states:
            if s not in q['prompt']:
                out.append('%s: the prompt does not state %r' % (iid, s))
        if len(q['decoys']) != 3:
            out.append('%s: %d decoys, not 3' % (iid, len(q['decoys'])))
        for d in q['decoys']:
            err, val = d.get('err'), d.get('val')
            used.add(err)
            if err not in types:
                out.append('%s: decoy %r has the err key %r, which ERR_TYPES does not have' % (iid, val, err))
            elif q['type'] not in types[err]:
                out.append('%s: %s is not allowed on a %s item (ERR_TYPES: %s)' % (iid, err, q['type'], ', '.join(sorted(types[err]))))
            if err not in lines:
                out.append('%s: no LINES line for %s' % (iid, err))
            if val not in errs.get(err, set()):
                out.append('%s: decoy %r (%s), recomputed %s' % (iid, val, err, sorted(errs.get(err, [])) or 'no such error for this item'))
        opts = [q['answer']] + [d.get('val') for d in q['decoys']]
        try:
            worths = [worth(q, o) for o in opts]
        except Exception:  # noqa: BLE001
            out.append('%s: an option this script cannot read: %r' % (iid, opts))
            continue
        for i in range(len(opts)):
            for j in range(i + 1, len(opts)):
                if opts[i] == opts[j] or worths[i] == worths[j]:
                    out.append('%s: options %r and %r are equal in value' % (iid, opts[i], opts[j]))
    for k in sorted(set(types) - set(lines)):
        out.append('lines: no LINES line for %s' % k)
    for k in sorted(set(lines) - set(types)):
        out.append('lines: LINES has %s, which ERR_TYPES does not' % k)
    for k in sorted(set(lines) - used):
        out.append('lines: the LINES line for %s is never used by the bank' % k)
    for k, v in lines.items():
        if not v.strip():
            out.append('lines: the LINES line for %s is empty' % k)
    for n, name in enumerate(STAGE_NAMES, 1):
        if not re.search(r'data-mode="stage-%d"><span class="n">%d</span><span><span class="t">%s</span>' % (n, n, re.escape(name)), html):
            out.append('start: stage %d is not named %r' % (n, name))
    info['bank'] = len(items)
    return items


# ---------------------------------------------------------------- the start picture
def webp_size(path):
    """(width, height) from a WebP file's own header (VP8, VP8L or VP8X), or None if it is not one."""
    with open(path, 'rb') as f:
        b = f.read(40)
    if len(b) < 30 or b[:4] != b'RIFF' or b[8:12] != b'WEBP':
        return None
    kind = b[12:16]
    if kind == b'VP8 ' and b[23:26] == b'\x9d\x01\x2a':
        return int.from_bytes(b[26:28], 'little') & 0x3fff, int.from_bytes(b[28:30], 'little') & 0x3fff
    if kind == b'VP8L' and b[20] == 0x2f:
        v = int.from_bytes(b[21:25], 'little')
        return (v & 0x3fff) + 1, ((v >> 14) & 0x3fff) + 1
    if kind == b'VP8X':
        return int.from_bytes(b[24:27], 'little') + 1, int.from_bytes(b[27:30], 'little') + 1
    return None


def check_art_static(html, out):
    tags = re.findall(r'<img\b[^>]*\bclass="start-art"[^>]*>', html)
    if len(tags) != 1:
        out.append('art: %d img.start-art tags in the page, not 1' % len(tags))
        return
    attrs = dict(re.findall(r'\b([a-z-]+)="([^"]*)"', tags[0]))
    for k, v in ART_TAG.items():
        if attrs.get(k) != v:
            out.append('art: the start picture\'s %s is %r, not %r' % (k, attrs.get(k), v))
    if not attrs.get('alt', '').strip():
        out.append('art: the start picture has no alt text')
    size = webp_size(ART) if os.path.exists(ART) else None
    if size != (1600, 873):
        out.append('art: assets/start.webp is %s, not a 1600 x 873 WebP' % (size,))


ART_SHOWN_JS = """() => { const i = document.querySelector('img.start-art');
  return !!i && i.getClientRects().length > 0 && i.getBoundingClientRect().height > 0 && getComputedStyle(i).visibility !== 'hidden'; }"""


# ---------------------------------------------------------------- the page
def open_page(pw, base, html, size):
    br = pw.chromium.launch()
    touch = size[0] <= 600
    ctx = br.new_context(viewport={'width': size[0], 'height': size[1]}, has_touch=touch, is_mobile=touch)
    ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT)
    bc.offline(ctx, base)
    page_url = re.compile(r'/games/%s/(\?[^/]*)?$' % SLUG)
    ctx.route(lambda url: bool(page_url.search(url)), lambda route: route.fulfill(
        status=200, content_type='text/html; charset=utf-8', body=html))
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(base + '/games/%s/?cb=verify' % SLUG, wait_until='load', timeout=30000)
    page.wait_for_function('!!window.B60 && !!B60.ui', timeout=15000)
    page.evaluate("""async () => { window.__ev = []; window.__sub = [];
        window.mfg = (n, p) => { window.__ev.push([n, p]); };
        window.MaffsLeaderboard = window.MaffsLeaderboard || {};
        MaffsLeaderboard.submitScore = (g, l, s, n) => { window.__sub.push([g, l, s, n]); return Promise.resolve(); };
        if (document.fonts && document.fonts.ready) await document.fonts.ready; }""")
    return br, page, errors


# What is on screen: the options, and the feedback after an answer.
SCREEN_JS = r"""() => {
  const opts = [...document.querySelectorAll('#opts .opt')].map(b => ({ val: b.dataset.val, text: b.textContent, cls: b.className, off: b.disabled }));
  const fb = document.querySelector('#feedback .fb');
  const err = fb && fb.querySelector('.fb-err'), ans = fb && fb.querySelector('.fb-ans');
  return { state: B60.ui.state(), q: B60.ui.question(), score: B60.ui.score(), opts,
           why: fb ? fb.dataset.why : null, err: fb ? fb.dataset.err || null : null, errText: err ? err.textContent : null,
           head: fb && fb.querySelector('.fb-head') ? fb.querySelector('.fb-head').textContent : null,
           ansText: ans ? ans.textContent : null, worked: fb ? fb.querySelectorAll('.worked .w-line').length : 0,
           katex: fb ? fb.querySelectorAll('.worked .katex').length : 0,
           next: !!document.querySelector('#feedback .maffs-next') };
}"""
PRESS_JS = r"""(val) => { const b = [...document.querySelectorAll('#opts .opt')].find(x => x.dataset.val === val); if (!b) return false; b.click(); return true; }"""


def play(page, m, lines, out):
    st = int(m[-1])
    page.evaluate('() => { window.__ev = []; window.__sub = []; }')
    page.evaluate('(m) => B60.ui.start(m)', m)
    seen, right = [], 0
    for k in range(PER):
        s = page.evaluate(SCREEN_JS)
        q = s['q']
        tag = '%s question %d (%s)' % (m, k + 1, q and q['id'])
        if s['state'] != 'asking' or not q:
            out.append('%s: no question on screen (state %s)' % (tag, s['state']))
            return
        seen.append(q['id'])
        if q['stage'] != st:
            out.append('%s: a stage %d item' % (tag, q['stage']))
        want = sorted([q['answer']] + [d['val'] for d in q['decoys']])
        if sorted(o['val'] for o in s['opts']) != want or any(o['text'] != o['val'] for o in s['opts']):
            out.append('%s: options %s, should be %s, each button\'s dataset.val its text' % (tag, [(o['val'], o['text']) for o in s['opts']], want))
        if k % 2 == 0:
            page.evaluate(PRESS_JS, q['answer'])
            a = page.evaluate(SCREEN_JS)
            right += 1
            if a['why'] != 'right' or a['head'] != 'Right: ' + q['answer']:
                out.append('%s: the right answer shows %r (%s), not "Right: %s"' % (tag, a['head'], a['why'], q['answer']))
            if a['next']:
                out.append('%s: a right answer waits on Next' % tag)
            try:
                page.wait_for_function('(id) => B60.ui.state() === "over" || (B60.ui.state() === "asking" && B60.ui.question().id !== id)', arg=q['id'], timeout=4000)
            except Exception:  # noqa: BLE001
                out.append('%s: a right answer did not move on by itself' % tag)
                return
        else:
            d = q['decoys'][(k // 2) % 3]
            page.evaluate(PRESS_JS, d['val'])
            a = page.evaluate(SCREEN_JS)
            check_wrong(tag, q, d, a, lines, out)
            if a['score'] != right:
                out.append('%s: a wrong answer changed the score to %d' % (tag, a['score']))
            page.evaluate('B60.ui.next()')
    tag = m
    if page.evaluate('B60.ui.state()') != 'over':
        out.append('%s: the run did not finish after %d questions' % (tag, PER))
        return
    if len(set(seen)) != PER:
        out.append('%s: the run served %s, not %d different items' % (tag, seen, PER))
    ev = page.evaluate('window.__ev')
    sub = page.evaluate('window.__sub')
    done = [p for n, p in ev if n == 'game_completed']
    if len(done) != 1 or done[0].get('score') != right or done[0].get('mode') != m or done[0].get('level') != 'ks3':
        out.append('%s: game_completed %s, expected one with score %d, mode %s, level ks3' % (tag, done, right, m))
    if sub != [[SLUG, m, right, PER]]:
        out.append('%s: the leaderboard got %s, expected one submission on %s with %d of %d' % (tag, sub, m, right, PER))
    qa = [p for n, p in ev if n == 'question_answered']
    if [p.get('question_id') for p in qa] != seen or [p.get('correct') for p in qa] != [k % 2 == 0 for k in range(PER)]:
        out.append('%s: question_answered events %s do not match the run' % (tag, [(p.get('question_id'), p.get('correct')) for p in qa]))
    extra = sorted({n for n, _ in ev} - EVENTS)
    if extra:
        out.append('%s: events the contract does not allow: %s' % (tag, extra))
    shown = page.evaluate("() => ({ score: document.getElementById('resScore').textContent, of: document.getElementById('resOf').textContent, on: document.getElementById('results').classList.contains('active') })")
    if not shown['on'] or shown['score'] != str(right) or shown['of'] != 'out of %d' % PER:
        out.append('%s: the results screen shows %s, expected %d out of %d' % (tag, shown, right, PER))
    page.evaluate("document.getElementById('menuBtn').click()")


def check_wrong(tag, q, d, a, lines, out):
    """A wrong answer's screen: the chosen option's own line, the answer, the working, Next, and the two marks."""
    if a['why'] != 'wrong':
        out.append('%s: %r is marked %s, not wrong' % (tag, d['val'], a['why']))
        return
    if a['err'] != d['err'] or a['errText'] != lines.get(d['err']):
        out.append('%s: choosing %r (%s) shows the line %r, not the LINES line for %s' % (tag, d['val'], d['err'], a['errText'], d['err']))
    if a['ansText'] != 'The answer is ' + q['answer']:
        out.append('%s: a wrong answer shows %r, not "The answer is %s"' % (tag, a['ansText'], q['answer']))
    if a['worked'] != len(q['working']):
        out.append('%s: %d working lines shown, the item has %d' % (tag, a['worked'], len(q['working'])))
    if a['katex'] < 1:
        out.append('%s: the working shows no KaTeX' % tag)
    if not a['next']:
        out.append('%s: no Next after a wrong answer' % tag)
    marks = {o['val']: o['cls'] for o in a['opts']}
    if 'is-wrong' not in marks.get(d['val'], '') or 'is-right' not in marks.get(q['answer'], '') or not all(o['off'] for o in a['opts']):
        out.append('%s: the chosen option is not marked wrong, the answer right and every option locked (%s)' % (tag, marks))


# One item's wrong-answer screen for one wrong option, measured in page coordinates once the layout has settled.
FIT_JS = r"""async ([id, val]) => {
  B60.ui.preview(id);
  const frame = () => new Promise(r => requestAnimationFrame(() => r()));
  const b = [...document.querySelectorAll('#opts .opt')].find(x => x.dataset.val === val);
  if (!b) return null;
  b.click();
  await frame(); await frame();
  const y = window.scrollY, box = (el) => { if (!el) return null; const r = el.getBoundingClientRect(); return r.width && r.height ? [Math.round(r.top + y), Math.round(r.bottom + y)] : null; };
  const fb = document.querySelector('#feedback .fb');
  const marked = [...document.querySelectorAll('#opts .opt.is-wrong, #opts .opt.is-right')].map(box);
  return { fold: window.innerHeight - 40, wide: document.documentElement.scrollWidth, view: window.innerWidth,
           err: fb ? fb.dataset.err || null : null, errText: fb && fb.querySelector('.fb-err') ? fb.querySelector('.fb-err').textContent : null,
           parts: { 'the prompt': box(document.getElementById('ask')), 'the line': box(fb && fb.querySelector('.fb-err')),
                    'the answer': box(fb && fb.querySelector('.fb-ans')), 'the working': box(fb && fb.querySelector('.worked')),
                    'Next': box(document.querySelector('#feedback .maffs-next')) },
           marked };
}"""


def check_fit(page, items, size, lines, out, info):
    worst, n = None, 0
    for q in items:
        for d in q['decoys']:
            tag = '%s, choosing %r (%s), at %dx%d' % (q['id'], d['val'], d['err'], size[0], size[1])
            r = page.evaluate(FIT_JS, [q['id'], d['val']])
            n += 1
            if r is None:
                out.append('%s: that option is not on screen' % tag)
                continue
            if r['err'] != d['err'] or r['errText'] != lines.get(d['err']):
                out.append('%s: shows the line %r, not the LINES line for %s' % (tag, r['errText'], d['err']))
            if r['wide'] > r['view']:
                out.append('%s: the page scrolls sideways (%d px wide)' % (tag, r['wide']))
            for name, b in r['parts'].items():
                if b is None:
                    out.append('%s: %s is not on screen' % (tag, name))
                elif b[0] < 0 or b[1] > r['fold']:
                    out.append('%s: %s ends at %d px, below the fold at %d px' % (tag, name, b[1], r['fold']))
            if len(r['marked']) != 2 or any(b is None or b[0] < 0 or b[1] > r['fold'] for b in r['marked']):
                out.append('%s: the chosen option and the answer are not both on screen above the fold (%s)' % (tag, r['marked']))
            nb = r['parts'].get('Next')
            if nb and (worst is None or r['fold'] - nb[1] < worst[0]):
                worst = (r['fold'] - nb[1], q['id'], d['err'])
    info.setdefault('fit', []).append((size, n, worst))


def check(html, out, units, shard=None, sample=None):
    unit = shard.unit if shard is not None else (lambda uid: contextlib.nullcontext())
    info, items = {}, None
    if 'bank' in units:
        with unit('bank'):
            try:
                items = check_bank(html, out, info)
            except Exception as e:  # noqa: BLE001
                out.append('the bank checks threw: %s' % str(e).splitlines()[0][:200])
    browser = [u for u in units if u != 'bank']
    if not browser:
        return info
    try:
        items = [json.loads(ln) for ln in bank_lines(html)]
        lines = lines_of(html)
    except Exception as e:  # noqa: BLE001
        out.append('the page\'s bank or LINES cannot be read: %s' % str(e).splitlines()[0][:200])
        return info
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            for uid in browser:
                with unit(uid):
                    size = tuple(int(x) for x in uid.split(' ')[1].split('x'))
                    br, page, errs = open_page(pw, base, html, size)
                    try:
                        if uid.startswith('why'):
                            if page.evaluate("() => { const d = document.querySelector('details#why'); return !d || d.open; }"):
                                out.append('start: the "Why 60?" panel is missing or open on load at %dx%d (it starts closed)' % size)
                            info['why'] = info.get('why', 0) + 1
                        elif uid.startswith('art'):
                            check_art_static(html, out)
                            page.wait_for_function("() => { const i = document.querySelector('img.start-art'); return !i || i.complete; }", timeout=15000)
                            if not page.evaluate("() => { const i = document.querySelector('img.start-art'); return !!i && i.naturalWidth === 1600; }"):
                                out.append('art: the start picture did not load at %dx%d' % size)
                            if not page.evaluate(ART_SHOWN_JS):
                                out.append('art: the start picture is not showing on the start screen at %dx%d' % size)
                            for m in MODES:
                                page.evaluate('(m) => B60.ui.start(m)', m)
                                if page.evaluate(ART_SHOWN_JS):
                                    out.append('art: the start picture is shown during play (%s) at %dx%d' % ((m,) + size))
                            info['art'] = 1
                        elif uid.startswith('play'):
                            for m in MODES:
                                play(page, m, lines, out)
                            info['played'] = len(MODES)
                        else:
                            check_fit(page, items[:sample] if sample else items, size, lines, out, info)
                    except Exception as e:  # noqa: BLE001
                        out.append('%s threw: %s' % (uid, str(e).splitlines()[0][:220]))
                    out.extend('page error (%s): %s' % (uid, e) for e in errs if 'production host' not in e)
                    br.close()
    finally:
        proc.terminate()
    return info


PLANT_SAMPLE = 8
# The start picture's line in the page, as BASE-60-LOOK placed it (moved by a plant).
ART_LINE = ('    <img class="start-art" src="assets/start.webp" width="1600" height="873" alt="An old clock shop crammed with clocks'
            ' of every kind: grandfather clocks with brass pendulums, cuckoo clocks, a giant clock face on the back wall, pocket'
            ' watches in a glass counter, an hourglass, and a sundial by the window">\n')


# Each plant: (what, [(old, new)], the unit it needs, the pattern its finding must match). The six the contract names, and
# the panel opened on load (GAME-TITLE-IN-PLAY, 24 Nov 2026), and the two the start picture needs (BASE-60-LOOK, 24 Nov 2026).
PLANTS = [
    ('a wrong answer', [('"prompt":"A film lasts 135 minutes. How long is that in hours and minutes?","answer":"2 h 15 min"',
                         '"prompt":"A film lasts 135 minutes. How long is that in hours and minutes?","answer":"2 h 5 min"')],
     'bank', r"s1a-135: answer '2 h 5 min', recomputed '2 h 15 min'"),
    ('a decoy equal in value to its answer', [('arrives at 11:20. How long is the journey?","answer":"1 h 35 min","decoys":[{"val":"1 h 75 min","err":"hhmm_subtract"}',
                                               'arrives at 11:20. How long is the journey?","answer":"1 h 35 min","decoys":[{"val":"95 min","err":"hhmm_subtract"}')],
     'bank', r"s3a-0945-1120: options '1 h 35 min' and '95 min' are equal in value"),
    ('a missing LINES key', [('    took_11: "Take off 12, not 11. Count back again.",\n', '')],
     'bank', r'no LINES line for took_11'),
    ('the wrong line shown for a decoy', [("'<div class=\"fb-err\">' + esc(LINES[err]) + '</div>'", "'<div class=\"fb-err\">' + esc(LINES[Q.decoys[0].err]) + '</div>'")],
     'play 375x667', r'shows the line .*, not the LINES line for '),
    ('a decoy given an err key its type does not allow (took_10 on a 12-to-24 item)',
     [('"id":"s2a-115pm","stage":2,"type":"12-to-24","h":1,"m":15,"half":"pm","prompt":"Your train leaves at 1:15 pm. What is that on the 24-hour clock?","answer":"13:15","decoys":[{"val":"01:15","err":"forgot_pm"},{"val":"11:15","err":"added_10"}',
       '"id":"s2a-115pm","stage":2,"type":"12-to-24","h":1,"m":15,"half":"pm","prompt":"Your train leaves at 1:15 pm. What is that on the 24-hour clock?","answer":"13:15","decoys":[{"val":"01:15","err":"forgot_pm"},{"val":"11:15","err":"took_10"}')],
     'bank', r's2a-115pm: took_10 is not allowed on a 12-to-24 item'),
    ('the "Why 60?" panel opened on load', [('<details class="maffs-ref why" id="why">', '<details class="maffs-ref why" id="why" open>')],
     'why 1280x720', r'the "Why 60\?" panel is missing or open on load at 1280x720'),
    ('the start picture without its alt', [(' height="873" alt="An old clock shop', ' height="873" data-alt="An old clock shop')],
     'art 375x667', r'art: the start picture has no alt text'),
    ('the start picture shown on the play screen', [(ART_LINE, ''),
                                                    ('  <div id="game" class="screen">\n', '  <div id="game" class="screen">\n%s' % ART_LINE)],
     'art 375x667', r'art: the start picture is shown during play'),
    ('the working pushed below the fold', [('.worked{font-size:.94rem;line-height:1.5}', '.worked{font-size:.94rem;line-height:1.5;padding-top:420px}')],
     'fit 375x667', r'the working ends at \d+ px, below the fold at 627 px'),
]


def selftest(html, plants=None, shard=None):
    ok = True
    for what, edits, unit_id, want in (PLANTS if plants is None else plants):
        with (shard.unit('plant: ' + what) if shard is not None else contextlib.nullcontext()):
            try:
                src = html
                for old, new in edits:
                    src = pc.apply_plant(src, old, new, name=what)
            except pc.StalePlant as e:
                print('  self-test %-78s *** %s ***' % (what, e))
                ok = False
                continue
            got, err = [], None
            try:
                check(src, got, [unit_id], sample=PLANT_SAMPLE)   # a fit plant needs only the first items' screens
            except Exception as e:  # noqa: BLE001
                err = e
            hit = [g for g in got if re.search(want, g)]
            caught = pc.is_caught(hit, err)
            print('  self-test %-78s %s' % (what, ('caught: ' + hit[0][:100]) if caught else '*** MISSED ***' + (' (other: %s)' % got[0][:90] if got else '') + (' (error: %s)' % err if err else '')))
            ok = caught and ok
    return ok


def main():
    ap = argparse.ArgumentParser()
    bc.shard_args(ap)
    ap.add_argument('--selftest', action='store_true', help='the planted faults only')
    args = ap.parse_args()
    shard = bc.Shard(__file__, args)
    units = ['bank', 'play 375x667', 'why 1280x720', 'why 375x667', 'art 375x667'] + ['fit %dx%d' % s for s in SIZES]
    if args.selftest:
        units = []
    mine = shard.pick(units + ['plant: ' + p[0] for p in PLANTS])
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    html = open(GAME, encoding='utf-8').read()
    out = []
    run = [u for u in units if u in mine]
    info = check(html, out, run, shard) if run else {}
    if 'bank' in info:
        print('%s: %d items, the contract\'s hash and counts; every answer, decoy and working line recomputed from the item\'s own fields; ERR_TYPES, LINES and equal-value options checked' % (SLUG, info['bank']))
    if 'why' in info:
        print('%s: the "Why 60?" panel closed on load (%d size(s))' % (SLUG, info['why']))
    if 'art' in info:
        print('%s: the start picture (img.start-art, assets/start.webp 1600 x 873, alt present) on the start screen, not in play' % SLUG)
    if 'played' in info:
        print('%s: %d stages played to the end at 375x667 (right and wrong marked, each wrong option\'s own line)' % (SLUG, info['played']))
    for size, n, worst in info.get('fit', []):
        print('%s: %d wrong-answer screens at %dx%d; the least room under Next: %s' % (SLUG, n, size[0], size[1], ('%d px (%s, %s)' % worst) if worst else 'none measured'))
    ok = selftest(html, [p for p in PLANTS if 'plant: ' + p[0] in mine], shard)
    for f in out[:80]:
        print('FAIL  ' + f)
    if len(out) > 80:
        print('FAIL  ... and %d more' % (len(out) - 80))
    if not ok:
        print('FAIL  self-test: a planted fault was not caught')
    print('FAILED' if out or not ok else 'PASS')
    return 1 if out or not ok else 0


if __name__ == '__main__':
    sys.exit(main())
