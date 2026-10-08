#!/usr/bin/env python3
# ci-line: B3 | Shared exam vocabulary tooltips (schools/assets/exam-vocab.js: idempotent on every Factor Theorem string, no markup in an attribute, the old function planted and caught) |
"""Test for the shared exam vocabulary tooltips, schools/assets/exam-vocab.js (factor-theorem-t5-008).

    python scripts/test-exam-vocab.py                  # the repo's helper, then the planted old one
    python scripts/test-exam-vocab.py --helper FILE    # judge another copy (main's, to see it fail)

The old wrapExamVocab wrapped the terms one after another on its own growing output, so a later term matched
inside markup an earlier one wrote: "Verify that" wrote aria-label="What does 'Verify that' mean?" and "verify"
then wrapped the word inside that attribute (Q10; "hence find" then "hence" on Q13, T1b, T8b, T10b).

Loads Factor Theorem (the only page that loads the helper) in headless Chromium with the helper under test, and
for every string in its CONTENT (prompts, step labels, test parts, hints, explanations):
  idempotent   wrapExamVocab(wrapExamVocab(x)) === wrapExamVocab(x)
  attributes   no attribute of the wrapped markup holds '<' or 'exam-vocab'
  nesting      no exam-vocab-wrap inside another, and every term span holds exactly one vocabulary term
  page         rendered as the game renders a prompt (its PQ, KaTeX), with the tooltips applied twice (the
               game's reset then apply): the same markup both times, every aria-label clean, and the visible
               text, bubbles and tooltips aside, the same as with no tooltips at all
Q10 and Q13 are named in the output. Then the old function is planted (the helper with the old wrapExamVocab
pasted in) and the run must FAIL, naming Q10.

Exits non-zero on any failure.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_common as bc  # noqa: E402

DEFAULT_HELPER = os.path.join(ROOT, 'schools', 'assets', 'exam-vocab.js')
SLUG = 'factor-theorem'

# The function as it was before VOCAB-IDEMPOTENT, word for word.
OLD_WRAP = r"""function wrapExamVocab(html) {
  let result = html;
  EXAM_VOCAB.forEach(({ term, plain }) => {
    const regex = new RegExp(`(?<![\\w-])(${escapeRegex(term)})(?![\\w-])`, 'gi');
    result = result.replace(regex, (match) => {
      return `<span class="exam-vocab-wrap">` +
        `<span class="exam-vocab-term">${match}</span>` +
        `<span class="exam-vocab-bubble" role="button" aria-label="What does '${match}' mean?">?</span>` +
        `<span class="exam-vocab-tooltip">${plain}</span>` +
        `</span>`;
    });
  });
  return result;
}"""

CHECK_JS = r"""() => {
  const strings = [];
  (function walk(v, path) {
    if (typeof v === 'string') { if (v.trim()) strings.push([path, v]); }
    else if (Array.isArray(v)) v.forEach((x, i) => walk(x, path + '[' + i + ']'));
    else if (v && typeof v === 'object') Object.keys(v).forEach(k => walk(v[k], path + '.' + k));
  })(CONTENT, 'CONTENT');
  const name = (path) => {
    const m = /^CONTENT\.practice\.questions\[(\d+)\]/.exec(path);
    if (m) return 'Q' + CONTENT.practice.questions[+m[1]].id + path.slice(m[0].length);
    return path.replace(/^CONTENT\./, '');
  };
  const terms = new Set(EXAM_VOCAB.map(v => v.term.toLowerCase()));
  const parse = (html) => { const t = document.createElement('template'); t.innerHTML = html; return t.content; };
  const attrFaults = (root) => {
    const bad = [];
    root.querySelectorAll('*').forEach(el => [...el.attributes].forEach(a => {
      if (/<|exam-vocab/.test(a.value) && a.name !== 'class') bad.push(a.name + '="' + a.value + '"');
    }));
    return bad;
  };
  const visible = (el) => {
    const c = el.cloneNode(true);
    c.querySelectorAll('.exam-vocab-bubble, .exam-vocab-tooltip, .katex-mathml').forEach(n => n.remove());
    return c.textContent;
  };
  const fails = [], seen = { strings: strings.length, wrapped: 0, q10: null, q13: null };
  const stage = document.createElement('div');
  document.body.appendChild(stage);
  strings.forEach(([path, x]) => {
    const where = name(path);
    const w1 = wrapExamVocab(x), w2 = wrapExamVocab(w1);
    if (w1 !== x) seen.wrapped++;
    if (w2 !== w1) fails.push(['idempotent', where, w1.slice(0, 160) + ' || twice: ' + w2.slice(0, 160)]);
    const frag = parse(w1);
    const bad = attrFaults(frag);
    if (bad.length) fails.push(['attributes', where, bad[0].slice(0, 200)]);
    if (frag.querySelector('.exam-vocab-wrap .exam-vocab-wrap'))
      fails.push(['nesting', where, 'an exam-vocab-wrap inside another']);
    frag.querySelectorAll('.exam-vocab-term').forEach(t => {
      if (!terms.has(t.textContent.toLowerCase())) fails.push(['nesting', where, 'term span holds ' + JSON.stringify(t.textContent)]);
    });
    // As the game renders it.
    const plain = document.createElement('div');
    plain.innerHTML = PQ(x);
    const box = document.createElement('div');
    box.className = 'vocab-probe';
    box.innerHTML = PQ(x);
    stage.innerHTML = '';
    stage.appendChild(box);
    MaffsVocab.resetVocabProcessing('.vocab-probe');
    MaffsVocab.applyExamVocabTooltips('.vocab-probe');
    const once = box.innerHTML;
    MaffsVocab.resetVocabProcessing('.vocab-probe');
    MaffsVocab.applyExamVocabTooltips('.vocab-probe');
    if (box.innerHTML !== once) fails.push(['page', where, 'applying the tooltips twice changed the markup']);
    const labels = [...box.querySelectorAll('[aria-label]')].map(e => e.getAttribute('aria-label'));
    labels.forEach(l => { if (/<|exam-vocab/.test(l)) fails.push(['page', where, 'aria-label: ' + l.slice(0, 160)]); });
    if (visible(box) !== visible(plain))
      fails.push(['page', where, 'shows ' + JSON.stringify(visible(box).slice(0, 160)) + ', not ' + JSON.stringify(visible(plain).slice(0, 160))]);
    const q = /^Q(10|13)\.prompt$/.exec(where);
    if (q) seen['q' + q[1]] = { text: visible(box), labels };
  });
  stage.remove();
  return { fails, seen };
}"""


def run(helper_js):
    from playwright.sync_api import sync_playwright
    proc, base = bc.start_stub_server()
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            ctx = browser.new_context(viewport={'width': 390, 'height': 844})
            ctx.route(lambda url: not url.startswith(base) and '/katex@' not in url, lambda route: route.abort())
            ctx.route(lambda url: url.split('?')[0].endswith('/schools/assets/exam-vocab.js'),
                      lambda route: route.fulfill(status=200, content_type='application/javascript', body=helper_js))
            page = ctx.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base + '/games/%s/?cb=vocab' % SLUG, wait_until='load', timeout=20000)
            page.wait_for_function('typeof CONTENT !== "undefined" && typeof katex !== "undefined" '
                                   '&& typeof MaffsVocab !== "undefined"', timeout=15000)
            out = page.evaluate(CHECK_JS)
            browser.close()
    finally:
        proc.terminate()
    if errors:
        out['fails'].insert(0, ['page', 'load', errors[0][:200]])
    return out


def report(label, out):
    fails, seen = out['fails'], out['seen']
    print('%s: %d strings, %d with a term' % (label, seen['strings'], seen['wrapped']))
    for q in ('q10', 'q13'):
        s = seen.get(q)
        if s:
            print('  %s shows %s' % (q.upper(), s['text'][:110]))
            print('  %s aria-labels %s' % (q.upper(), s['labels']))
    for kind, where, detail in fails[:40]:
        print('  FAIL  %-10s %-28s %s' % (kind, where, detail))
    if len(fails) > 40:
        print('  ... and %d more' % (len(fails) - 40))
    return fails


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser()
    ap.add_argument('--helper', default=DEFAULT_HELPER, help='the exam-vocab.js to judge')
    ap.add_argument('--no-selftest', action='store_true')
    args = ap.parse_args()
    with open(args.helper, encoding='utf-8') as f:
        helper = f.read()

    fails = report('helper', run(helper))
    ok = not fails
    print('PASS' if ok else 'FAIL: %d' % len(fails))

    if not args.no_selftest:
        start = helper.find('function wrapExamVocab(html) {')
        end = helper.find('\n}\n', start)
        if start < 0 or end < 0:
            print('SELFTEST FAIL: cannot find wrapExamVocab to replace')
            return 1
        planted = helper[:start] + OLD_WRAP + helper[end + 2:]
        pf = report('planted (old wrapExamVocab)', run(planted))
        caught = any(where.startswith('Q10') for _, where, _ in pf)
        print('SELFTEST %s: the old function %s' % ('PASS' if caught else 'FAIL',
                                                   'fails, naming Q10' if caught else 'was not caught on Q10'))
        ok = ok and caught
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
