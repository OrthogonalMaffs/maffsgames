#!/usr/bin/env python3
# ci-line: Answer boxes are text boxes (no <input type="number"> in any game page or shared game script, in markup, in an HTML string a script builds, or set by .type / setAttribute; comments, CSS and prose are not inputs; planted faults caught: a box in markup, one in a script string, one after a URL on the same line, one set by .type, one by setAttribute, a stale exemption; controls pass) | --selftest && --check
# ci-deps: games/ schools/assets/
"""Is every typed answer box a text box, never type="number"? (contract ANSWER-BOX-TEXT, Jon 15 Nov 2026)

    python scripts/check-answer-inputs.py --check       # every file under games/ and schools/assets/
    python scripts/check-answer-inputs.py --selftest    # planted faults fail, controls pass (no files read)

THE RULE (Jon, 15 Nov 2026; canon §7.1.3 once the home lane records it, todo ANSWER-BOX-CANON): a typed answer box is
<input type="text">, never type="number", for two reasons. (1) A number box changes its value when its arrows are
clicked or the mouse wheel turns over it: Graph Sketcher's table marked each change, so a click on an arrow submitted
and wiped the answer ("click up or down and it auto deletes it. this is properly broken", Jon, 15 Nov). (2) A number
box silently empties on anything it cannot parse (a typed £, "1,000"), so MaffsAnswer, which reads the raw typed string
(schools/assets/answer.js), receives "" and can never give its 'format' message. On a phone a text box takes
inputmode="decimal"; where the answer can be negative it takes MaffsKeypad with {minus: true} instead, since the
iPhone's decimal keypad has no minus key.

WHAT IS AN INPUT HERE. A type="number" (any quoting, or none) in markup or in a string a script builds; `.type = 'number'`
on an element; setAttribute('type', 'number'). NOT an input: anything inside an HTML comment, a JavaScript comment or a
<style> block; an attribute selector such as input[type=number] (CSS, or a querySelector string); a data-type= or any
other attribute ending in "type"; a comparison such as q.type === 'number'. Scripts are read by a small lexer that knows
strings, template literals (with ${...}), regular-expression literals and comments, so a // inside a string (a URL) is
never taken for a comment and the rest of its line is still read. Known gap: an object literal passed to an element
builder ({type: 'number'}) is not matched, because games use type: 'number' as question data (chart-interrogator);
no page builds inputs that way.

SCOPE: games/ and schools/assets/ only (*.html, *.js). escape-rooms/assets/engine.js keeps a type="number" box on
purpose: the slider's typed fallback ("Or type the setting") sets an instrument and is never marked on change; it is
out of this check's scope by design (contract ANSWER-BOX-TEXT). schools/assets/answer.js mentions type="number" only
in a comment, which this check reads as prose.

EXEMPT lists a file by path with its reason. An exempt file's matches are reported, not failed; an EXEMPT entry whose
file has no match (or no longer exists) fails, so the list can only shrink.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCOPE = ('games', os.path.join('schools', 'assets'))

EXEMPT = {
    # Empty since PR 2 of ANSWER-BOX-TEXT (estimation-golf and glorious-gantt). An entry needs a path and its reason.
}

# type="number" as an attribute: not after [ (a selector), a word character, '.', '-' or ':' (another attribute or a property).
ATTR = re.compile(r'''(?<![\[\w.\-:$])type\s*=\s*\\?["'`]?\s*number\b''', re.I)
PROP = re.compile(r'''\.type\s*=(?!=)\s*["'`]number["'`]''', re.I)
SETA = re.compile(r'''setAttribute\(\s*["'`]type["'`]\s*,\s*["'`]number["'`]\s*\)''', re.I)
PATTERNS = (ATTR, PROP, SETA)

REGEX_BEFORE = set('(,=:[!&|?{};+-*%<>~^')


def blank(s):
    """The same text with every character but newlines made a space, so line numbers survive."""
    return re.sub(r'[^\n]', ' ', s)


def strip_js(src):
    """JavaScript with its comments blanked out; strings, templates and regex literals kept as they are."""
    out, i, n = [], 0, len(src)
    stack = ['code']          # 'code', or 'tpl' for the text of a template literal; braces in ${...} counted per frame
    depth = [0]
    prev = ''                 # the last significant character in code, to tell a regex literal from a division
    while i < n:
        c = src[i]
        mode = stack[-1]
        if mode == 'tpl':
            if c == '\\':
                out.append(src[i:i + 2]); i += 2; continue
            if c == '`':
                out.append(c); stack.pop(); depth.pop(); prev = '`'; i += 1; continue
            if c == '$' and src[i + 1:i + 2] == '{':
                out.append('${'); stack.append('code'); depth.append(0); prev = '{'; i += 2; continue
            out.append(c); i += 1; continue
        # code
        if c == '/' and src[i + 1:i + 2] == '/':
            j = src.find('\n', i)
            j = n if j < 0 else j
            out.append(blank(src[i:j])); i = j; continue
        if c == '/' and src[i + 1:i + 2] == '*':
            j = src.find('*/', i + 2)
            j = n if j < 0 else j + 2
            out.append(blank(src[i:j])); i = j; continue
        if c in '"\'':
            j = i + 1
            while j < n and src[j] != c and src[j] != '\n':
                j += 2 if src[j] == '\\' else 1
            out.append(src[i:j + 1]); i = j + 1; prev = c; continue
        if c == '`':
            out.append(c); stack.append('tpl'); depth.append(0); i += 1; continue
        if c == '/' and (prev == '' or prev in REGEX_BEFORE):
            j, cls = i + 1, False
            while j < n and src[j] != '\n':
                if src[j] == '\\':
                    j += 2; continue
                if src[j] == '[':
                    cls = True
                elif src[j] == ']':
                    cls = False
                elif src[j] == '/' and not cls:
                    break
                j += 1
            out.append(src[i:j + 1]); i = j + 1; prev = 'r'; continue
        if c == '{':
            depth[-1] += 1
        elif c == '}':
            if depth[-1] == 0 and len(stack) > 1:      # the end of a template's ${...}
                stack.pop(); depth.pop(); out.append(c); i += 1; continue
            depth[-1] -= 1
        if not c.isspace():
            prev = c if not (c.isalnum() or c in '_$') else 'w'
        out.append(c); i += 1
    return ''.join(out)


SCRIPT = re.compile(r'(<script\b[^>]*>)(.*?)(</script\s*>)', re.S | re.I)
STYLE = re.compile(r'(<style\b[^>]*>)(.*?)(</style\s*>)', re.S | re.I)
HTML_COMMENT = re.compile(r'<!--.*?-->', re.S)


def code_of(path, text):
    """What counts as code: comments and <style> blocks blanked, scripts lexed. Line numbers are kept."""
    if path.endswith('.js'):
        return strip_js(text)
    out, pos = [], 0
    for m in re.finditer(r'<!--.*?-->|<script\b[^>]*>.*?</script\s*>|<style\b[^>]*>.*?</style\s*>', text, re.S | re.I):
        out.append(text[pos:m.start()])
        chunk = m.group(0)
        if chunk.startswith('<!--'):
            out.append(blank(chunk))
        elif chunk[:6].lower() == '<style':
            s = STYLE.match(chunk)
            out.append(s.group(1) + blank(s.group(2)) + s.group(3))
        else:
            s = SCRIPT.match(chunk)
            out.append(s.group(1) + strip_js(s.group(2)) + s.group(3))
        pos = m.end()
    out.append(text[pos:])
    return ''.join(out)


def matches(path, text):
    code = code_of(path, text)
    lines = text.split('\n')
    hits = []
    for p in PATTERNS:
        for m in p.finditer(code):
            ln = code.count('\n', 0, m.start()) + 1
            hits.append((ln, lines[ln - 1].strip()[:140]))
    return sorted(set(hits))


def files():
    for top in SCOPE:
        for d, _, fs in os.walk(os.path.join(ROOT, top)):
            for f in fs:
                if f.endswith(('.html', '.js')):
                    yield os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, '/')


def judge(found, exempt):
    """(failures, notes) from {path: hits} and the exemption list."""
    fails, notes = [], []
    for path in sorted(found):
        for ln, s in found[path]:
            if path in exempt:
                notes.append('exempt  %s:%d  %s' % (path, ln, s))
            else:
                fails.append('%s:%d: a type="number" answer box: %s' % (path, ln, s))
    for path, why in sorted(exempt.items()):
        if not found.get(path):
            fails.append('EXEMPT lists %s (%s), but it has no type="number" box: remove the entry' % (path, why))
    return fails, notes


def check():
    found = {}
    for path in files():
        with open(os.path.join(ROOT, path), encoding='utf-8') as fh:
            h = matches(path, fh.read())
        if h:
            found[path] = h
    fails, notes = judge(found, EXEMPT)
    for n in notes:
        print(n)
    if fails:
        for f in fails:
            print('FAIL  ' + f)
        print('FAILED: %d answer box(es) are type="number"; make each type="text" (inputmode="decimal", or MaffsKeypad '
              'with {minus: true} where the answer can be negative)' % len(fails))
        return 1
    print('OK: no type="number" answer box in games/ or schools/assets/ (%d exempt match(es) in %d file(s), listed above)'
          % (len(notes), len([p for p in EXEMPT if found.get(p)])))
    return 0


PAGE = '<!DOCTYPE html><html><head><style>%s</style></head><body>%s<script>%s</script></body></html>'
CONTROLS = [
    ('a JavaScript line comment', PAGE % ('', '', '// Money is typed as text (a type="number" input empties).\nvar a = 1;')),
    ('a JavaScript block comment', PAGE % ('', '', '/* never <input type="number"> */ var a = 1;')),
    ('an HTML comment', PAGE % ('', '<!-- an old <input type="number"> box -->', '')),
    ('a CSS attribute selector', PAGE % ('input[type=number]{width:4rem}', '', '')),
    ('a querySelector string', PAGE % ('', '', "document.querySelectorAll('input[type=number]');")),
    ('question data compared', PAGE % ('', '', "if (q.type === 'number') go(); if(q.type==='number')go();")),
    ('a data-type attribute', PAGE % ('', '<div data-type="number"></div>', '')),
    ('a text box', PAGE % ('', '<input type="text" inputmode="decimal">', "inp.type = 'text';")),
    ('a regex literal with quotes', PAGE % ('', '', "var r = /['\"]/g; var s = 'type';")),
]
PLANTS = [
    ('a box in a game page', PAGE % ('', '<input type="number" id="a">', '')),
    ('a box built in a script string', PAGE % ('', '', "html += '<input type=\"number\" class=\"n\">';")),
    ('a box in a template literal', PAGE % ('', '', 'html += `<td><input class="mono" type="number" data-x="${k}"></td>`;')),
    ('a box after a URL on the same line', PAGE % ('', '', "var u = 'https://example.invalid/x'; html += '<input type=number>';")),
    ('a box set by .type', PAGE % ('', '', "const inp = document.createElement('input'); inp.type='number';")),
    ('a box set by setAttribute', PAGE % ('', '', "el.setAttribute('type', 'number');")),
    ('a box in a shared script', None),
]


def selftest():
    ok = True
    for what, page in CONTROLS:
        h = matches('games/x/index.html', page)
        print('  control %-40s %s' % (what, 'passes' if not h else '*** FLAGGED: %s ***' % h))
        ok = ok and not h
    for what, page in PLANTS:
        if page is None:
            h = matches('schools/assets/x.js', "/* a comment */ el.innerHTML = '<input type=\"number\">';")
        else:
            h = matches('games/x/index.html', page)
        print('  plant   %-40s %s' % (what, 'caught' if h else '*** MISSED ***'))
        ok = ok and bool(h)
    fails, _ = judge({}, {'games/x/index.html': 'a planted exemption'})
    stale = any('remove the entry' in f for f in fails)
    print('  plant   %-40s %s' % ('a stale EXEMPT entry', 'caught' if stale else '*** MISSED ***'))
    ok = ok and stale
    print('selftest: %s' % ('PASS' if ok else 'FAIL'))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='every file under games/ and schools/assets/')
    ap.add_argument('--selftest', action='store_true', help='planted faults fail, controls pass')
    a = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    rc = 0
    if a.selftest:
        rc |= selftest()
    if a.check or not a.selftest:
        rc |= check()
    return rc


if __name__ == '__main__':
    sys.exit(main())
