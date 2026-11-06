#!/usr/bin/env python3
# ci-line: Logo copies (every copy of the M+ mark, translated and scaled into the master's coordinates, has the master's M, plus and bars; bars #0d9488; no unregistered copy; planted faults caught) | --selftest && --check
# ci-deps: schools/assets/m_plus_logo.svg schools/assets/favicon.svg schools/assets/og-image.svg index.html about/index.html
"""LOGO-CENTRE, Jon, 6 Nov 2026: one master geometry for the logo, and every copy held to it.

The mark was hand-copied five times and the copies drifted three ways (bars 7.5 units off the right leg, an old
teal, bars 30 wide in one copy). schools/assets/m_plus_logo.svg is the master. For every copy this check:

  * finds the M path by its shape (its point list equals the master's after translating and uniformly scaling);
  * derives the copy -> master map from the M's bounding box (one scale, one offset);
  * maps the plus path and the two bar rectangles through it and requires them equal to the master's;
  * requires every bar's fill to be #0d9488 (the M and plus keep their own colours: the header is white on navy).

It also scans every .svg and .html file in the repo for the M's shape, so a new hand copy fails until it is added to
COPIES (and so matches). The PNG og-image.png cannot be read this way; it is regenerated from og-image.svg by hand.
"""
import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import plant_common as pc

ROOT = Path(__file__).resolve().parent.parent
MASTER = 'schools/assets/m_plus_logo.svg'
COPIES = [
    'schools/assets/favicon.svg',
    'schools/assets/og-image.svg',
    'index.html',
    'about/index.html',
]
TEAL = '#0d9488'
SCAN_SKIP = {'.git', 'node_modules'}
SVG_BLOCK = re.compile(r'<svg\b.*?</svg>', re.S | re.I)
NS = '{http://www.w3.org/2000/svg}'
EPS = 1e-6


def local(tag):
    return tag.rsplit('}', 1)[-1]


def parse_path(d):
    """Absolute M/L/Z polygon -> list of (x, y), or None for any other path."""
    tokens = re.findall(r'[A-Za-z]|-?\d*\.?\d+(?:[eE][-+]?\d+)?', d or '')
    pts, i, cmd = [], 0, None
    while i < len(tokens):
        t = tokens[i]
        if t.isalpha():
            if t not in 'MLZ':
                return None
            cmd = t
            i += 1
            continue
        if cmd not in ('M', 'L') or i + 1 >= len(tokens) or tokens[i + 1].isalpha():
            return None
        pts.append((float(t), float(tokens[i + 1])))
        i += 2
    return pts or None


def bbox(pts):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def same(a, b):
    return abs(a - b) < EPS


def shape_map(pts, ref):
    """(scale, dx, dy) taking pts onto ref point for point, or None if pts is not ref's shape."""
    if len(pts) != len(ref):
        return None
    ax0, ay0, ax1, ay1 = bbox(pts)
    rx0, ry0, rx1, ry1 = bbox(ref)
    if ax1 - ax0 <= 0 or ay1 - ay0 <= 0:
        return None
    s = (rx1 - rx0) / (ax1 - ax0)
    if not same(s * (ay1 - ay0), ry1 - ry0):
        return None
    dx, dy = rx0 - s * ax0, ry0 - s * ay0
    for (x, y), (u, v) in zip(pts, ref):
        if not (same(s * x + dx, u) and same(s * y + dy, v)):
            return None
    return s, dx, dy


def svg_blocks(name, text):
    """(parsed root or None, raw text) for each <svg> in the file. A file that is itself SVG is one block."""
    raw = [text] if name.endswith('.svg') else SVG_BLOCK.findall(text)
    out = []
    for block in raw:
        try:
            out.append((ET.fromstring(block.encode('utf-8')), block))
        except ET.ParseError:
            out.append((None, block))
    return out


PATH_D = re.compile(r'<path\b[^>]*?\sd="([^"]*)"', re.I)


def has_m(block, m_ref):
    """For an <svg> that does not parse: does any path in it have the M's shape?"""
    return any(shape_map(parse_path(d) or [], m_ref) for d in PATH_D.findall(block))


def walk(el, chain=()):
    """(element, the chain of ancestor transforms) for every descendant."""
    for child in el:
        tf = child.get('transform')
        here = chain + ((tf,) if tf else ())
        yield child, here
        yield from walk(child, here)


def extract(root):
    """The master-independent parts of one <svg>: paths and rects with their transform chains."""
    paths, rects = [], []
    for el, chain in walk(root):
        tag = local(el.tag)
        if tag == 'path':
            pts = parse_path(el.get('d'))
            if pts:
                paths.append((pts, el, chain))
        elif tag == 'rect':
            rects.append((el, chain))
    return paths, rects


def num(el, attr, default=0.0):
    v = el.get(attr)
    return float(v) if v is not None else default


def master_parts(text):
    roots = [root for root, _ in svg_blocks(MASTER, text)]
    if len(roots) != 1 or roots[0] is None:
        raise ValueError('%s: does not parse as one SVG' % MASTER)
    paths, rects = extract(roots[0])
    if len(paths) != 2:
        raise ValueError('%s: expected 2 paths (M, plus), found %d' % (MASTER, len(paths)))
    m = max(paths, key=lambda p: len(p[0]))[0]
    plus = min(paths, key=lambda p: len(p[0]))[0]
    x0, y0, x1, y1 = bbox(m)
    bars = [r for r, _ in rects if not (num(r, 'x') <= x0 and num(r, 'y') <= y0
                                         and num(r, 'x') + num(r, 'width') >= x1
                                         and num(r, 'y') + num(r, 'height') >= y1)]
    if len(bars) != 2:
        raise ValueError('%s: expected 2 bar rects, found %d' % (MASTER, len(bars)))
    bars = sorted(((num(b, 'x'), num(b, 'y'), num(b, 'width'), num(b, 'height'), num(b, 'rx')) for b in bars),
                  key=lambda b: (b[1], b[0]))  # top bar first
    return m, plus, bars, roots[0]


def check_logo(name, root, master, errors):
    """Compare one <svg> holding the M against the master. Returns True if it held the M at all."""
    m_ref, plus_ref, bars_ref, _ = master
    paths, rects = extract(root)
    found = [(p, el, chain, shape_map(p, m_ref)) for p, el, chain in paths]
    ms = [f for f in found if f[3]]
    if not ms:
        return False
    if len(ms) > 1:
        errors.append('%s: %d M paths in one <svg>' % (name, len(ms)))
        return True
    _, m_el, chain, (s, dx, dy) = ms[0]
    others = [f for f in found if f is not ms[0]]
    if len(others) != 1:
        errors.append('%s: expected one plus path beside the M, found %d' % (name, len(others)))
    else:
        pts, _, pchain, _ = others[0]
        mapped = [(s * x + dx, s * y + dy) for x, y in pts]
        if pchain != chain:
            errors.append('%s: the plus is under a different transform from the M' % name)
        elif len(mapped) != len(plus_ref) or not all(same(a, u) and same(b, v)
                                                     for (a, b), (u, v) in zip(mapped, plus_ref)):
            errors.append('%s: the plus path, in the master\'s coordinates, is %s; the master\'s is %s'
                          % (name, fmt_pts(mapped), fmt_pts(plus_ref)))
    x0, y0, x1, y1 = bbox(m_ref)
    bars = []
    for r, rchain in rects:
        if rchain != chain:
            continue
        rx, ry = s * num(r, 'x') + dx, s * num(r, 'y') + dy
        rw, rh = s * num(r, 'width'), s * num(r, 'height')
        if rx <= x0 + EPS and ry <= y0 + EPS and rx + rw >= x1 - EPS and ry + rh >= y1 - EPS:
            continue  # a background behind the whole mark
        bars.append(((rx, ry, rw, rh, s * num(r, 'rx')), r))
    if len(bars) != 2:
        errors.append('%s: expected 2 bar rects beside the M, found %d' % (name, len(bars)))
        return True
    got = sorted((b for b, _ in bars), key=lambda b: (b[1], b[0]))  # top bar first, as the master's
    for g, want in zip(got, bars_ref):
        if not all(same(a, b) for a, b in zip(g, want)):
            errors.append('%s: a bar, in the master\'s coordinates, is x %g y %g width %g height %g rx %g; '
                          'the master\'s is x %g y %g width %g height %g rx %g' % ((name,) + g + want))
    for _, r in bars:
        fill = (r.get('fill') or '').strip().lower()
        if fill != TEAL:
            errors.append('%s: a bar is filled %r, not %s' % (name, r.get('fill'), TEAL))
    return True


def fmt_pts(pts):
    return ' '.join('%g,%g' % p for p in pts)


def analyse(files):
    """files: {repo path: text}. Returns errors (empty = pass)."""
    errors = []
    try:
        master = master_parts(files[MASTER])
    except (KeyError, ValueError) as exc:
        return [str(exc)]
    held = {}
    for name in sorted(files):
        if not name.endswith(('.svg', '.html')):
            continue
        count = 0
        for root, block in svg_blocks(name, files[name]):
            if root is None:
                if has_m(block, master[0]):
                    errors.append('%s: an <svg> holding the logo does not parse as XML, so it cannot be checked'
                                  % name)
                    count += 1
            elif check_logo(name, root, master, errors):
                count += 1
        if count:
            held[name] = count
    for name in [MASTER] + COPIES:
        if held.get(name, 0) != 1:
            errors.append('%s: should hold the logo exactly once, holds it %d times' % (name, held.get(name, 0)))
    for name in sorted(set(held) - set(COPIES) - {MASTER}):
        errors.append('%s: an unregistered copy of the logo; add it to COPIES in scripts/check-logo.py '
                      '(or load the master instead of copying it)' % name)
    return errors


def repo_files():
    files = {}
    for p in ROOT.rglob('*'):
        if p.suffix not in ('.svg', '.html') or not p.is_file():
            continue
        rel = p.relative_to(ROOT)
        if SCAN_SKIP & set(rel.parts):
            continue
        files[rel.as_posix()] = p.read_text(encoding='utf-8', errors='replace')
    return files


def selftest():
    files = repo_files()
    base = analyse(files)
    if base:
        print('SELFTEST: the live tree must pass first:')
        for e in base:
            print('  ' + e)
        return 1
    # (label, file, old, new, replace every occurrence, the error text that must appear)
    plants = [
        ('an off-centre bar (the old x 215) in the favicon', 'schools/assets/favicon.svg',
         '<rect x="222.5" y="130"', '<rect x="215" y="130"', False, 'a bar, in the master'),
        ('the old teal #4CB5B0 in the homepage header', 'index.html',
         'height="12" rx="2" fill="#0d9488"/>', 'height="12" rx="2" fill="#4CB5B0"/>', True, 'not #0d9488'),
        ('og-image bars 30 wide, not 35', 'schools/assets/og-image.svg',
         '<rect x="82.5" y="30" width="35"', '<rect x="82.5" y="30" width="30"', False, 'a bar, in the master'),
        ('a moved plus on the about page', 'about/index.html',
         'M 155,140 L 155,130', 'M 156,140 L 155,130', False, 'the plus path'),
        ('the master moved alone (every copy now drifts)', MASTER,
         '<rect x="222.5" y="148"', '<rect x="215" y="148"', False, 'a bar, in the master'),
        ('a copy that does not parse as XML', 'about/index.html',
         'fill="#ffffff"/>\n      <rect x="222.5"', 'fill="#ffffff"/>&nbsp;\n      <rect x="222.5"', False,
         'does not parse'),
        ('an unregistered sixth copy (half size, moved)', 'games/planted-logo/index.html',
         None, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><path d="M 0,0 L 15,0 L 30,20 '
         'L 45,0 L 60,0 L 60,50 L 40,50 L 40,27.5 L 32.5,37.5 L 27.5,37.5 L 20,27.5 L 20,50 L 0,50 Z"/></svg>',
         False, 'unregistered copy'),
    ]
    failures = 0
    for label, path, old, new, every, expect in plants:
        planted = dict(files)
        if old is None:
            if path in files:
                print('STALE PLANT: %s: %s already exists' % (label, path))
                failures += 1
                continue
            planted[path] = new
        else:
            try:
                planted[path] = pc.apply_plant(files[path], old, new, name=label, allow_multiple=every)
            except pc.StalePlant as exc:
                print(exc)
                failures += 1
                continue
        try:
            errs, err = analyse(planted), None
        except Exception as exc:  # an error is never a catch
            errs, err = [], exc
        hit = [e for e in errs if expect in e]
        if pc.is_caught(hit, err):
            print('caught: %s -> %s' % (label, hit[0]))
        else:
            print('MISSED: %s (errors: %s; exception: %s)' % (label, errs, err))
            failures += 1
    print('SELFTEST %s: %d plants, %d missed or stale' % ('PASS' if not failures else 'FAIL', len(plants), failures))
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    args = ap.parse_args()
    if not (args.check or args.selftest):
        ap.error('give --check and/or --selftest')
    rc = 0
    if args.selftest:
        rc |= selftest()
    if args.check:
        errors = analyse(repo_files())
        for e in errors:
            print('FAIL: ' + e)
        if not errors:
            print('PASS: the master and %d copies match (%s)' % (len(COPIES), ', '.join(COPIES)))
        rc |= 1 if errors else 0
    return rc


if __name__ == '__main__':
    sys.exit(main())
