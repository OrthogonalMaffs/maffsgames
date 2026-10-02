#!/usr/bin/env python3
"""
Derive DfE GCSE subject-content statements, and their PRINTED TYPE, from the
vendored source PDF.

Why this exists: the `tier` field in data/spec-mapping.json records what the DfE
document actually prints - standard, underlined or bold - and both Foundation gap
lists in the review doc are computed from it. That has to be re-derivable rather
than typed out by hand and trusted, so this script produces it mechanically and
asserts the source hash before reading a byte of content.

Printed type, per the document's own convention:
  standard    all students develop confidence and competence with this content
  underlined  all students are ASSESSED on standard + underlined content
  bold        only the more highly attaining students are assessed on this

A single numbered statement frequently mixes types - A25 is standard except for
the words "and quadratic", which are bold. Flattening that to one type per
statement would put Higher-only content into the Foundation gap list. So each
statement is split into contiguous typed PARTS (A25.1 standard, A25.2 bold), and
mappings and gap lists work on parts.

How the two markers are detected:
  bold       font flag 16 (Arial-BoldMT in this document)
  underline  a drawn horizontal rule under the span. NOT a font attribute in PDF.
             The rule's top sits 2.4-2.6pt ABOVE the span bbox bottom, inside the
             descender zone, so a test demanding it sit below the text matches
             nothing - which is how the first attempt found no underlines at all.

             Fraction bars are thin horizontal rules too. Width does not separate
             them: real underlines here run from under 50pt to 449pt, so any floor
             high enough to exclude a fraction bar also discards genuine partial
             underlines. What separates them is what sits BELOW. A denominator
             touches its bar - measured at dy 0.00 to 0.09 - while the nearest
             text under a true underline is at least 2.2pt away, usually a whole
             line at 19pt or more.

Four things the layout throws at this, each with a measured rule:
  page numbers    the only spans at y0 = 777.9; body text never passes y = 741.
                  Left in, they became parts of their own ("6", "8", "12") and
                  would have entered the Foundation gap list as unmapped content.
  sub-headings    ArialMT 12pt at x0 = 56.7, where body text sits at x0 = 92.
                  They are underlined in the document, so left in they attached
                  to the previous statement AS UNDERLINED CONTENT - inflating the
                  underlined count with things like "Vectors" and "Graphs".
  maths notation  even with fraction bars excluded, a maths run can flip type
                  mid-expression. A maths run therefore takes its MAJORITY type
                  and a type boundary is accepted only at the run's edge. Real
                  boundaries do sit at notation edges - G23.1 and A18.4 - so the
                  splitting is not suppressed, only prevented from happening
                  *inside* an expression. G20, the worst case, went from 15 parts
                  to 9, and all 9 are now real typography including the two bold
                  Higher-only clauses.
  lost spaces     adjacent spans are joined with a space when their x-gap says
                  there was one, otherwise "real roots" becomes "realroots".

Run: python scripts/extract-dfe-tier.py [--out data/dfe-gcse-parts.json]
"""
import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter

try:
    import pymupdf
except ImportError:
    sys.exit("pymupdf is required: pip install pymupdf")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PDF = os.path.join(ROOT, 'docs', 'sources', 'dfe-gcse-maths-subject-content.pdf')

SOURCE = {
    'id': 'dfe-gcse-subject-content',
    'title': 'Mathematics: GCSE subject content and assessment objectives',
    'publisher': 'Department for Education',
    'url': ('https://assets.publishing.service.gov.uk/media/5a7cb5b040f0b6629523b52c/'
            'GCSE_mathematics_subject_content_and_assessment_objectives.pdf'),
    'sha256': '647a751b51c71d9ced1c9356aa70b15ceb1a4acb2fd5bc9af49619ead06d0ee6',
    'retrieved': '2026-09-24',
    'licence': 'OGL v3.0, Crown copyright 2013',
    'vendored': 'docs/sources/dfe-gcse-maths-subject-content.pdf',
}

SECTIONS = ['Number', 'Algebra', 'Ratio, proportion and rates of change',
            'Geometry and measures', 'Probability', 'Statistics']
LETTER = {'Number': 'N', 'Algebra': 'A', 'Ratio, proportion and rates of change': 'R',
          'Geometry and measures': 'G', 'Probability': 'P', 'Statistics': 'S'}
FIRST_PAGE, LAST_PAGE = 3, 11

# Published reference ranges. Asserted, because a silent change here would mean
# the extractor had started reading something other than the content statements.
EXPECTED = {'N': 16, 'A': 25, 'R': 16, 'G': 25, 'P': 9, 'S': 6}

RULE_MIN_WIDTH = 10.0        # ignores notation noise; fraction bars handled below
FRACTION_DY = 1.0            # a denominator touches its bar (measured 0.00-0.09)
RULE_DY_MIN, RULE_DY_MAX = -3.2, 1.5
FOOTER_Y = 770.0             # page numbers sit at 777.9; body stops at 741
SUBHEAD_MAX_X = 60.0         # sub-headings at 56.7, body text at 92
SUBHEAD_SIZE = (11.5, 12.5)
SPACE_GAP = 1.0              # x-gap above which a space was really there
MATHS_FONTS = ('Times', 'Cambria', 'Symbol')
NUM_RE = re.compile(r'^\s*(\d{1,2})\.\s')

# --- Regression assertions -------------------------------------------------
# These encode the 24 Sep 2026 review checkpoint. The seven splits below were
# each checked against the PDF and are real Foundation/Higher boundaries; if a
# change to the segmentation rules moves or retypes any of them, that is a
# regression and this script must fail rather than quietly ship different data.
REQUIRED_PARTS = [
    ('N5.2', 'bold', 'product rule for counting'),
    ('N10.2', 'bold', 'recurring decimals'),
    ('A25.2', 'bold', 'and quadratic'),
    ('A18.4', 'bold', 'completing the square'),
    ('G23.1', 'bold', 'to calculate the area'),
    ('G25.2', 'bold', 'proofs'),
    ('S4.2', 'bold', 'box plots'),
]
# Defects found at the same checkpoint. None may reappear.
FORBIDDEN_SUBHEADINGS = [
    'Fractions, decimals and percentages', 'Measures and accuracy', 'Graphs',
    'Solving equations and inequalities', 'Sequences',
    'Mensuration and calculation', 'Vectors',
]
FORBIDDEN_JOINS = ['realroots', 'andfractional', 'andalgebraic',
                   'simplifyingexpressions', 'sinyx']
# G20 is the worst case in the document: a line mixing an underlined phrase, two
# displayed fractions and two bold Higher-only clauses. It was shattered into 15
# parts when fraction bars counted as underlines. The test is NOT a part count -
# its nine parts are all real typography - but that no boundary falls INSIDE a
# fraction, and that both genuine Higher boundaries survive.
G20_FRACTION_WORDS = {'opposite', 'hypotenuse', 'adjacent'}
G20_REQUIRED_BOLD = ['general triangles', 'three']


def assert_source():
    if not os.path.exists(PDF):
        sys.exit("missing vendored source: %s\nSee docs/sources/README.md" % PDF)
    got = hashlib.sha256(open(PDF, 'rb').read()).hexdigest()
    if got != SOURCE['sha256']:
        sys.exit("source PDF hash mismatch.\n  expected %s\n  got      %s\n"
                 "The vendored document changed. Do not just update the constant: "
                 "re-read the convention and re-check the tier data."
                 % (SOURCE['sha256'], got))
    return got


def raw_spans(page):
    out = []
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            for sp in line['spans']:
                if sp['text'].strip():
                    out.append(sp)
    return out


def underline_rules(page, spans):
    """Thin horizontal rules that underline text, with fraction bars removed.

    Width cannot separate the two: real underlines in this document run from
    under 50pt to 449pt, so any floor high enough to exclude a fraction bar also
    throws away genuine partial underlines. What separates them is what sits
    BELOW. A fraction's denominator touches the bar - measured at dy 0.00 to
    0.09 - while the nearest text under a true underline is at least 2.2pt away
    and usually a whole line, 19pt or more.
    """
    rules = []
    for drawing in page.get_drawings():
        r = drawing['rect']
        if r.height >= 2.5 or r.width <= RULE_MIN_WIDTH:
            continue
        denominator = any(
            -FRACTION_DY <= (sp['bbox'][1] - r.y1) <= FRACTION_DY
            and min(sp['bbox'][2], r.x1) - max(sp['bbox'][0], r.x0) > 0.3 * r.width
            for sp in spans)
        if not denominator:
            rules.append(r)
    return rules


def page_headings(page):
    out = set()
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            for sp in line['spans']:
                if sp['text'].strip() in SECTIONS and 13.0 < sp['size'] < 15.5:
                    out.add((round(sp['bbox'][1], 1), sp['text'].strip()))
    return out


def is_subheading(sp):
    x0, y0 = sp['bbox'][0], sp['bbox'][1]
    return (x0 < SUBHEAD_MAX_X
            and SUBHEAD_SIZE[0] <= sp['size'] <= SUBHEAD_SIZE[1]
            and not NUM_RE.match(sp['text'])
            and sp['text'].strip() != '')


def page_spans(page):
    spans = raw_spans(page)
    rules = underline_rules(page, spans)
    out = []
    if True:
        if True:
            for sp in spans:
                x0, y0, x1, y1 = sp['bbox']
                if y0 > FOOTER_Y:                       # page number
                    continue
                bold = bool(sp['flags'] & 16)
                und = any(RULE_DY_MIN <= (r.y0 - y1) <= RULE_DY_MAX
                          and min(x1, r.x1) - max(x0, r.x0) > 0.5 * (x1 - x0)
                          for r in rules)
                out.append({'text': sp['text'], 'bold': bold, 'underlined': und,
                            'maths': any(f in sp['font'] for f in MATHS_FONTS),
                            'sub': is_subheading(sp),
                            'x0': round(x0, 1), 'x1': round(x1, 1), 'y': round(y0, 1)})
    return out


def kind(run):
    # bold wins where a run carries both: bold is the assessment-boundary marker,
    # and it is the one that decides Foundation vs Higher.
    if run['bold']:
        return 'bold'
    return 'underlined' if run['underlined'] else 'standard'


def extract():
    doc = pymupdf.open(PDF)
    statements = []
    section = None
    cur = None
    for i in range(FIRST_PAGE, LAST_PAGE + 1):
        heads = page_headings(doc[i])
        for run in page_spans(doc[i]):
            hit = [h for (hy, h) in heads if abs(hy - run['y']) < 0.6]
            if hit:
                section, cur = hit[0], None
                continue
            if run['sub']:
                # A sub-heading ends the statement above it; it is not content.
                cur = None
                continue
            if section is None:
                continue
            match = NUM_RE.match(run['text'])
            if match and run['x0'] < 90:
                cur = {'section': section, 'n': int(match.group(1)), 'page': i, 'runs': []}
                statements.append(cur)
                run = dict(run, text=NUM_RE.sub('', run['text'], count=1))
                if not run['text'].strip():
                    continue
            if cur is not None:
                cur['runs'].append(run)
    return statements


def settle_maths_runs(runs):
    """Give each contiguous maths-font run a single, majority type.

    A fraction bar sits at underline height, so without this a maths expression
    flips type part-way through and creates boundaries that are notation, not
    typography. Boundaries at the EDGE of a maths run are left alone, because
    real ones live there - G23.1's area formula, A18.4's quadratic formula.
    """
    out = [dict(r, kind=kind(r)) for r in runs]
    i = 0
    while i < len(out):
        if not out[i]['maths']:
            i += 1
            continue
        j = i
        while j < len(out) and out[j]['maths']:
            j += 1
        group = out[i:j]
        weight = Counter()
        for r in group:
            weight[r['kind']] += max(len(r['text'].strip()), 1)
        majority = weight.most_common(1)[0][0]
        for r in group:
            r['kind'] = majority
        i = j
    return out


def join_text(prev, run):
    """Join spans, restoring the space the span split threw away."""
    if not prev:
        return run['text']
    gap = run['x0'] - prev['x1']
    sep = '' if (prev['text'].endswith(' ') or run['text'].startswith(' ')
                 or gap <= SPACE_GAP) else ' '
    return sep + run['text']


def to_parts(statements):
    out = []
    for st in statements:
        letter = LETTER[st['section']]
        ref = '%s%d' % (letter, st['n'])
        runs = settle_maths_runs(st['runs'])

        merged = []
        prev = None
        for run in runs:
            piece = join_text(prev, run)
            if merged and merged[-1]['tier'] == run['kind']:
                merged[-1]['text'] += piece
            else:
                merged.append({'tier': run['kind'], 'text': piece.lstrip()})
            prev = run

        parts = []
        for part in merged:
            text = re.sub(r'\s+', ' ', part['text']).strip()
            if text:
                parts.append({'tier': part['tier'], 'text': text})

        # A part of pure punctuation or a bare number carries no content; fold it
        # into its neighbour so the gap lists never point at a stray semicolon.
        cleaned = []
        for part in parts:
            if (not re.search(r'[A-Za-z]', part['text'])) and cleaned:
                cleaned[-1]['text'] += ' ' + part['text']
            else:
                cleaned.append(part)

        full = ''
        prev = None
        for run in runs:
            full += join_text(prev, run)
            prev = run
        full = re.sub(r'\s+', ' ', full).strip()

        out.append({
            'ref': ref,
            'section': st['section'],
            'letter': letter,
            'n': st['n'],
            'page': st['page'],
            'text': full,
            'tiers': sorted({p['tier'] for p in cleaned}),
            'parts': [{'ref': '%s.%d' % (ref, i + 1), 'tier': p['tier'], 'text': p['text']}
                      for i, p in enumerate(cleaned)],
        })
    return out


def check_regressions(rows):
    """Fail loudly if the 24 Sep review checkpoint has been broken."""
    index = {p['ref']: (p['tier'], p['text']) for r in rows for p in r['parts']}
    problems = []

    for ref, tier, needle in REQUIRED_PARTS:
        if ref not in index:
            problems.append('missing required part %s (%s "%s")' % (ref, tier, needle))
            continue
        got_tier, got_text = index[ref]
        if got_tier != tier:
            problems.append('%s should be %s, is %s' % (ref, tier, got_tier))
        if needle.lower() not in got_text.lower():
            problems.append('%s no longer contains "%s": %r' % (ref, needle, got_text[:70]))

    for ref, (tier, text) in index.items():
        if re.fullmatch(r'\d{1,2}', text):
            problems.append('%s is a bare page number: %r' % (ref, text))
        if text.strip() in FORBIDDEN_SUBHEADINGS:
            problems.append('%s is a sub-heading, not content: %r' % (ref, text))
        for bad in FORBIDDEN_JOINS:
            if bad in text.replace(' ', '') and bad in text:
                problems.append('%s has a lost space: %r' % (ref, bad))

    g20 = [r for r in rows if r['ref'] == 'G20']
    if g20:
        parts = g20[0]['parts']
        for p in parts:
            if p['text'].strip().lower().strip('.,;') in G20_FRACTION_WORDS:
                problems.append('%s is a bare fraction term (%r) - a part boundary '
                                'has fallen inside a fraction again' % (p['ref'], p['text']))
        bold_text = ' '.join(p['text'].lower() for p in parts if p['tier'] == 'bold')
        for needle in G20_REQUIRED_BOLD:
            if needle not in bold_text:
                problems.append('G20 has lost its bold Higher boundary %r' % needle)

    if problems:
        sys.exit('regression check failed:\n' + '\n'.join('  - ' + p for p in problems))


def main():
    parser = argparse.ArgumentParser(description='Extract DfE GCSE tier data.')
    parser.add_argument('--out', default=os.path.join(ROOT, 'data', 'dfe-gcse-parts.json'))
    args = parser.parse_args()

    sha = assert_source()
    rows = to_parts(extract())

    counts = {}
    for row in rows:
        counts[row['letter']] = counts.get(row['letter'], 0) + 1
    if counts != EXPECTED:
        sys.exit("statement counts do not match the published reference ranges.\n"
                 "  expected %s\n  got      %s" % (EXPECTED, counts))

    check_regressions(rows)

    payload = {
        'source': dict(SOURCE, sha256=sha),
        'convention': {
            'standard': 'all students develop confidence and competence with this content',
            'underlined': 'all students are assessed on standard and underlined content',
            'bold': 'only the more highly attaining students are assessed on this content',
        },
        'statements': rows,
    }

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w', encoding='utf-8') as fh:
        json.dump(payload, fh, indent=1, ensure_ascii=False)
        fh.write('\n')

    tiers = Counter(p['tier'] for r in rows for p in r['parts'])
    nparts = sum(len(r['parts']) for r in rows)
    mixed = sum(1 for r in rows if len(r['tiers']) > 1)
    print('source sha256 OK: %s' % sha[:16])
    print('regression check: PASS (%d required parts, %d defect rules)'
          % (len(REQUIRED_PARTS), len(FORBIDDEN_SUBHEADINGS) + len(FORBIDDEN_JOINS) + 4))
    print('statements: %d %s' % (len(rows), counts))
    print('parts:      %d (%d statements mix types)' % (nparts, mixed))
    print('part tiers: standard=%d bold=%d underlined=%d'
          % (tiers['standard'], tiers['bold'], tiers['underlined']))
    print('written:    %s' % os.path.relpath(args.out, ROOT))


if __name__ == '__main__':
    main()
