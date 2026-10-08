#!/usr/bin/env python3
"""Name the maths, never the student (canon §7.5.3, Jon, 7 Oct 2026; contract ESSENTIALS).

    python scripts/check-student-labels.py              # CI
    python scripts/check-student-labels.py --selftest   # planted labels are caught; exempt places are not
    python scripts/check-student-labels.py --root <copy of the repo>

A link posted in Google Classroom or Teams shows its page's description and og/twitter tags to the whole
class. Until 8 Oct 2026 the two escape rooms built for a resit class opened "A GCSE resit escape room
on...", and the portal's cards said "for a GCSE resit class": a label on the student, typed by hand into
several pages, with nothing to stop it coming back. Student surfaces describe the topic and level only.

Student surfaces, scanned: every games/**/index.html, every escape-rooms/*/index.html, and the portal,
section and updates pages a student can reach (PORTALS: the home page, the escape-rooms and op portals,
/essentials/ and /updates/). In each: the visible text (text nodes outside script, style and
comments, plus alt, title, aria-label and placeholder), the strings in its scripts (questions and feedback
built in JavaScript are visible too; comments are not), and the description, og: and twitter: meta tags.
LABEL fails anywhere there.

Exempt: teacher surfaces, which may say resit or post-16 (each room's teacher.html, the parent and teacher
guides), docs, and code comments. Until 8 Oct 2026 /essentials/ was exempt too and /updates/ was not scanned,
so both still said resit; Jon, 8 Oct 2026: the section is "Essentials" everywhere public, and no public page
labels a student as a resitter (contract ESSENTIALS-WORDING).

Runs in CI's site-wide checks (.github/workflows/check-site.yml), not as a content line: a content line runs
on a pull request only when a page it names changes, and this check must see every page on every change.

Stdlib only.
"""
import argparse
import glob
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LABEL = re.compile(r'\b(re-?sits?|re-?takes?|post-?16)\b', re.I)
PORTALS = ['index.html', 'escape-rooms/index.html', 'op/index.html', 'essentials/index.html', 'updates/index.html']
SURFACES = ['games/**/index.html', 'escape-rooms/*/index.html']
META = re.compile(r'^(description|og:.*|twitter:.*)$', re.I)
SHOWN_ATTRS = ('alt', 'title', 'aria-label', 'placeholder')

# A page whose label is maths content, not a label on the student, with the reason. Reported, never failed;
# an entry whose page no longer has a label fails as stale, so the fixing PR removes it.
KNOWN = {
    'games/given-that/index.html': 'a tree-diagram question about 500 GCSE students, first attempt and re-sit '
                                   '(P(passes | re-sits)): a scenario, not the player. Game content is outside '
                                   'contract ESSENTIALS; whether it suits a resit class is for Jon (8 Oct 2026)',
}


def strip_js_comments(src):
    """The script with its comments removed and its strings kept: a small scanner that knows quotes and
    template literals, so a // inside a string (a URL) is not taken for a comment."""
    out, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c in '"\'`':
            j = i + 1
            while j < n and src[j] != c:
                if src[j] == '\\':
                    j += 1
                elif src[j] == '\n' and c != '`':
                    break
                j += 1
            out.append(src[i:j + 1])
            i = j + 1
        elif src.startswith('//', i):
            j = src.find('\n', i)
            i = n if j < 0 else j
        elif src.startswith('/*', i):
            j = src.find('*/', i + 2)
            i = n if j < 0 else j + 2
        else:
            out.append(c)
            i += 1
    return ''.join(out)


class Surface(HTMLParser):
    """[(where, text)] a student can see on one page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.found, self.skip, self.script = [], 0, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta':
            key = a.get('name') or a.get('property') or ''
            if META.match(key) and a.get('content'):
                self.found.append(('<meta %s>' % key, a['content']))
            return
        for k in SHOWN_ATTRS:
            if a.get(k):
                self.found.append(('%s="..." on <%s>' % (k, tag), a[k]))
        if tag == 'script':
            self.script = []
        elif tag in ('style', 'noscript', 'template'):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag == 'script' and self.script is not None:
            self.found.append(('a script string', strip_js_comments(''.join(self.script))))
            self.script = None
        elif tag in ('style', 'noscript', 'template') and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if self.script is not None:
            self.script.append(data)
        elif not self.skip and data.strip():
            self.found.append(('visible text', data))


def faults_in(path, html):
    p = Surface()
    p.feed(html)
    p.close()
    out = []
    for where, text in p.found:
        for m in LABEL.finditer(text):
            s = text[max(0, m.start() - 50):m.end() + 50].replace('\n', ' ').strip()
            out.append('%s: "%s" in %s: ...%s...' % (path, m.group(0), where, s))
    return out


def surfaces(root):
    paths = []
    for pat in SURFACES:
        paths += glob.glob(os.path.join(root, pat), recursive=True)
    paths += [os.path.join(root, p) for p in PORTALS if os.path.exists(os.path.join(root, p))]
    return sorted({os.path.relpath(p, root).replace(os.sep, '/') for p in paths})


def check(root):
    faults, pages = [], surfaces(root)
    for rel in pages:
        faults += faults_in(rel, open(os.path.join(root, rel), encoding='utf-8').read())
    return pages, faults


def selftest():
    """Each plant must be caught; each exempt place must not be."""
    errs = []
    room = 'escape-rooms/' + 'comic-caper' + '/index.html'
    html = open(os.path.join(ROOT, room), encoding='utf-8').read()
    good = 'A GCSE escape room on factors, primes and HCF.'
    if html.count(good) != 3:
        errs.append('%s no longer carries its description three times (description, og, twitter)' % room)
    plants = [
        ('the old comic-caper description', html.replace(good, 'A GCSE resit escape room on factors, primes and HCF.')),
        ('a label in visible text', html.replace('<body>', '<body><p>For post-16 students</p>', 1)),
        ('a label in a script string', html.replace('</body>', '<script>var t = "Retake ready";</script></body>', 1)),
        ('a label in an alt attribute', html.replace('<body>', '<body><img alt="resit class" src="x.png">', 1)),
    ]
    for name, page in plants:
        if not faults_in(room, page):
            errs.append('planted %s: NOT caught' % name)
        else:
            print('  self-test: planted %s: caught (%s)' % (name, faults_in(room, page)[0][:110]))
    exempt = [
        ('a label in a code comment', html.replace('</body>', '<script>// built for a resit class\n/* resit */ var x = "a//b";</script></body>', 1)),
        ('a label in an HTML comment', html.replace('<body>', '<body><!-- built for a resit class -->', 1)),
        ('a label in a style block', html.replace('</head>', '<style>/* resit */</style></head>', 1)),
    ]
    for name, page in exempt:
        if faults_in(room, page):
            errs.append('%s was flagged (comments are exempt): %s' % (name, faults_in(room, page)[0]))
    for page, needle in (('essentials/index.html', '<p class="teacher-line">'),
                         ('updates/index.html', '<ul>')):
        src = open(os.path.join(ROOT, page), encoding='utf-8').read()
        if needle not in src:
            errs.append('%s no longer contains %s to plant beside' % (page, needle))
            continue
        planted = src.replace(needle, needle + 'Built for GCSE resit students. ', 1)
        if not faults_in(page, planted):
            errs.append('planted a label on %s: NOT caught' % page)
        else:
            print('  self-test: planted a label on %s: caught (%s)' % (page, faults_in(page, planted)[0][:110]))
    pages = surfaces(ROOT)
    for must in ('index.html', room, 'escape-rooms/index.html', 'essentials/index.html', 'updates/index.html'):
        if must not in pages:
            errs.append('%s is not scanned' % must)
    for never in ('escape-rooms/comic-caper/teacher.html',):
        if never in pages:
            errs.append('%s is scanned (a teacher surface is exempt)' % never)
    if not any(p.startswith('games/') for p in pages):
        errs.append('no game page is scanned')
    for e in errs:
        print('FAIL  self-test: ' + e)
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=ROOT)
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    if args.selftest:
        errs = selftest()
        print('FAILED' if errs else 'PASS')
        return 1 if errs else 0
    pages, found = check(args.root)
    faults = [f for f in found if f.split(':')[0] not in KNOWN]
    for page, why in sorted(KNOWN.items()):
        hits = [f for f in found if f.split(':')[0] == page]
        if not hits:
            faults.append('%s: in KNOWN but has no label now (stale: remove its entry)' % page)
        else:
            print('  REPORTED %s (%d, KNOWN: %s)' % (page, len(hits), why))
    for f in faults:
        print('FAIL  ' + f)
    print('%s: %d student surfaces (%d game pages, %d escape-room pages, portals %s); %d label(s)' % (
        'FAILED' if faults else 'OK', len(pages), sum(p.startswith('games/') for p in pages),
        sum(p.startswith('escape-rooms/') and p.count('/') == 2 for p in pages),
        ', '.join(p for p in PORTALS if p in pages), len(faults)))
    return 1 if faults else 0


if __name__ == '__main__':
    sys.exit(main())
