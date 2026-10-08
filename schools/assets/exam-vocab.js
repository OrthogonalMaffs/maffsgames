/**
 * MaffsGames Exam Vocabulary Tooltip System
 * Detects exam terminology in question text and adds plain-English tooltips
 *
 * Usage: MaffsVocab.applyExamVocabTooltips('#questionText')
 * Call after question text is rendered to DOM
 */

const EXAM_VOCAB = [
  { term: 'hence or otherwise', plain: 'You can use your answer from the previous part, or find a completely different method — your choice.' },
  { term: 'hence fully factorise', plain: 'Use your previous answer to help you find ALL the factors — don\'t stop at a partial factorisation.' },
  { term: 'hence find the exact value', plain: 'Use your previous answer AND leave your final answer as a fraction, surd, or in terms of \u03C0 — no decimals.' },
  { term: 'hence solve', plain: 'Use your answer from the previous part to find the solution.' },
  { term: 'hence find', plain: 'Use your answer from the previous part to calculate this.' },
  { term: 'hence evaluate', plain: 'Use your previous answer to calculate the numerical value.' },
  { term: 'hence show', plain: 'Use your previous answer to reach this result — show every step.' },
  { term: 'hence deduce', plain: 'Use your previous answer to reach this conclusion — explain your reasoning.' },
  { term: 'hence', plain: 'Use your answer from the previous part to help you answer this part.' },
  { term: 'show that', plain: 'The answer is given to you. Write out every step that gets there. Working with numbers is fine when that is the method, such as showing f(2) = 0. You must not start from the given answer and work backwards.' },
  { term: 'prove that', plain: 'Show rigorously that this is always true. Every step must be justified — this is not the same as checking with an example.' },
  { term: 'prove', plain: 'Show rigorously that this is always true. Every step must be justified.' },
  { term: 'verify that', plain: 'Check this is correct — substitute the value back in and confirm both sides match.' },
  { term: 'verify', plain: 'Check this is correct by substituting the value back in.' },
  { term: 'deduce that', plain: 'Use the result you just found to reach this conclusion. Explain your reasoning.' },
  { term: 'deduce', plain: 'Use what you\'ve just found or been told to reach this conclusion.' },
  { term: 'write down', plain: 'State the answer directly — no working is required or expected.' },
  { term: 'state', plain: 'Write the answer down — no working needed.' },
  { term: 'without the use of a calculator', plain: 'Show full algebraic working. Your answer must be exact — no decimal approximations.' },
  { term: 'without using a calculator', plain: 'Show full algebraic working. Your answer must be exact — no decimal approximations.' },
  { term: 'exact value', plain: 'Leave your answer as a fraction, surd (like \u221A3), or in terms of \u03C0. Do NOT round to a decimal.' },
  { term: 'exact form', plain: 'Leave your answer as a fraction, surd, or in terms of \u03C0. Do NOT round to a decimal.' },
  { term: 'leave in exact form', plain: 'Do not use a decimal. Leave as a fraction, surd, or expression involving \u03C0 or e.' },
  { term: 'factorise fully', plain: 'Find ALL the factors. Don\'t stop if you can still factorise further — e.g. 4(x\u00B2\u22121) is not fully factorised, it should be 4(x+1)(x\u22121).' },
  { term: 'fully factorise', plain: 'Find ALL the factors. Don\'t stop if you can still factorise further.' },
  { term: 'expand and simplify', plain: 'Multiply out all the brackets first, then collect like terms.' },
  { term: 'simplify fully', plain: 'Reduce to the simplest possible form — cancel fractions, collect like terms, apply index laws as needed.' },
  { term: 'express in the form', plain: 'Rewrite the expression so it looks exactly like the form shown — rearrange, complete the square, or factorise as needed.' },
  { term: 'express as', plain: 'Rewrite in the form the question specifies.' },
  { term: 'describe fully', plain: 'For transformations: you must give the TYPE (e.g. rotation), DIRECTION/CENTRE, and SIZE/ANGLE. All three are required for full marks. "It moved right" is not a full description.' },
  { term: 'describe the transformation', plain: 'Give the type (translation/rotation/reflection/enlargement), the direction or centre, and the distance, angle or scale factor. All parts needed for full marks.' },
  { term: 'comment on', plain: 'Give a mathematical interpretation — what does this result actually mean in context? A vague statement won\'t score marks.' },
  { term: 'sketch', plain: 'Draw a rough graph — it doesn\'t need to be to scale. But you must show: the shape of the curve, where it crosses the axes, and any asymptotes or turning points.' },
  { term: 'plot', plain: 'Draw accurately using the given coordinates. Use the scale on the axes. This is more precise than a sketch.' },
  { term: 'given that', plain: 'This is a fact you\'re allowed to treat as true — use it as a starting point or condition in your working.' },
  { term: 'it is given that', plain: 'This is a fact you\'re allowed to treat as true.' },
  { term: 'find the range', plain: 'Find all possible OUTPUT values of the function — not the domain (inputs).' },
  { term: 'find the domain', plain: 'Find all valid INPUT values — the values of x for which the function is defined.' },
  { term: 'state the domain', plain: 'Write down the valid input values — no working needed, but you must be precise.' },
  { term: 'is increasing', plain: 'The function goes upward as x increases — f\'(x) > 0 in this region.' },
  { term: 'is decreasing', plain: 'The function goes downward as x increases — f\'(x) < 0 in this region.' },
  { term: 'show your working', plain: 'Write out every step — even if you could do it in your head. Examiners award marks for method, not just the final answer.' },
  { term: 'use calculus', plain: 'Differentiation or integration is required — you cannot use a graph or trial-and-error.' },
  { term: 'minimum value', plain: 'The lowest point the function reaches. Find it by differentiating, setting equal to zero, and confirming it\'s a minimum.' },
  { term: 'maximum value', plain: 'The highest point the function reaches. Find it by differentiating, setting equal to zero, and confirming it\'s a maximum.' },
  { term: 'stationary point', plain: 'A point where the gradient is zero — could be a maximum, minimum, or point of inflection. Differentiate and set equal to zero to find it.' },
  { term: 'point of inflection', plain: 'A point where the curve changes from concave to convex (or vice versa). The gradient doesn\'t have to be zero here.' },
  { term: 'nature of the stationary point', plain: 'Determine whether it\'s a maximum, minimum, or point of inflection. Use the second derivative test: f\'\'(x) > 0 is a minimum, f\'\'(x) < 0 is a maximum, f\'\'(x) = 0 needs further investigation.' }
];

function injectTooltipStyles() {
  if (document.getElementById('exam-vocab-styles')) return;
  const style = document.createElement('style');
  style.id = 'exam-vocab-styles';
  style.textContent = `
    .exam-vocab-wrap { display: inline; position: relative; }
    .exam-vocab-term { border-bottom: 1px dashed #0d9488; cursor: pointer; }
    .exam-vocab-bubble {
      display: inline-flex; align-items: center; justify-content: center;
      width: 16px; height: 16px; border-radius: 50%;
      background: #0d9488; color: #ffffff;
      font-size: 10px; font-weight: 700; font-family: 'Outfit', sans-serif;
      cursor: pointer; vertical-align: super; margin-left: 2px;
      line-height: 1; flex-shrink: 0; user-select: none;
    }
    .exam-vocab-bubble:hover { background: #0f766e; }
    .exam-vocab-tooltip {
      display: none; position: absolute;
      bottom: calc(100% + 8px); left: 50%; transform: translateX(-50%);
      background: #1a2744; color: #e8eaf0;
      font-size: 13px; font-family: 'Outfit', sans-serif; line-height: 1.5;
      padding: 10px 14px; border-radius: 6px;
      border: 1px solid #2a3f6b; width: 280px; max-width: 90vw;
      z-index: 1000; box-shadow: 0 4px 12px rgba(0,0,0,0.4);
      pointer-events: none;
    }
    .exam-vocab-tooltip::after {
      content: ''; position: absolute; top: 100%; left: 50%;
      transform: translateX(-50%); border: 6px solid transparent;
      border-top-color: #1a2744;
    }
    .exam-vocab-wrap.active .exam-vocab-tooltip { display: block; }
    @media (max-width: 480px) {
      .exam-vocab-tooltip { width: 240px; font-size: 12px; left: 0; transform: none; }
    }
    body.accessible .exam-vocab-tooltip { font-size: 15px; line-height: 1.7; }
    body.light-theme .exam-vocab-tooltip {
      background: #ffffff; color: #1a2744;
      border-color: #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    body.light-theme .exam-vocab-tooltip::after { border-top-color: #ffffff; }
  `;
  document.head.appendChild(style);
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function vocabMarkup(match, plain) {
  return `<span class="exam-vocab-wrap">` +
    `<span class="exam-vocab-term">${match}</span>` +
    `<span class="exam-vocab-bubble" role="button" aria-label="What does '${match}' mean?">?</span>` +
    `<span class="exam-vocab-tooltip">${plain}</span>` +
    `</span>`;
}

// Wraps the terms in one run of text. Terms are tried in list order, as before, but every match is found in
// the original text and none may overlap an earlier one, so a later term never matches inside markup an
// earlier term wrote (factor-theorem-t5-008: "verify" inside the aria-label that "verify that" wrote).
function wrapVocabText(text) {
  const claims = [];
  EXAM_VOCAB.forEach(({ term, plain }) => {
    const regex = new RegExp(`(?<![\\w-])(${escapeRegex(term)})(?![\\w-])`, 'gi');
    let m;
    while ((m = regex.exec(text))) {
      const start = m.index, end = start + m[0].length;
      if (!claims.some(c => start < c.end && c.start < end)) claims.push({ start, end, plain });
    }
  });
  if (!claims.length) return text;
  claims.sort((a, b) => a.start - b.start);
  let out = '', at = 0;
  claims.forEach(c => {
    out += text.slice(at, c.start) + vocabMarkup(text.slice(c.start, c.end), c.plain);
    at = c.end;
  });
  return out + text.slice(at);
}

// Idempotent: only text outside tags is matched, never a tag or an attribute, and text already inside an
// exam-vocab-wrap span is left alone, so wrapExamVocab(wrapExamVocab(x)) === wrapExamVocab(x).
function wrapExamVocab(html) {
  const parts = html.split(/(<\/?[A-Za-z][^>]*>)/);
  const open = [];        // for each open span: is it an exam-vocab-wrap?
  let inWrap = 0;
  return parts.map((part, i) => {
    if (i % 2 === 0) return inWrap ? part : wrapVocabText(part);
    const tag = /^<(\/?)([A-Za-z][\w-]*)/.exec(part);
    if (tag[2].toLowerCase() === 'span') {
      if (tag[1]) {
        if (open.pop()) inWrap--;
      } else if (!/\/>$/.test(part)) {
        const isWrap = /\bclass\s*=\s*["'][^"']*\bexam-vocab-wrap\b/.test(part);
        open.push(isWrap);
        if (isWrap) inWrap++;
      }
    }
    return part;
  }).join('');
}

function processTextNodes(container) {
  const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, {
    acceptNode: (node) => {
      let parent = node.parentElement;
      while (parent && parent !== container) {
        if (parent.classList.contains('katex') ||
            parent.classList.contains('katex-html') ||
            parent.classList.contains('exam-vocab-wrap')) {
          return NodeFilter.FILTER_REJECT;
        }
        parent = parent.parentElement;
      }
      return NodeFilter.FILTER_ACCEPT;
    }
  });
  const textNodes = [];
  let node;
  while (node = walker.nextNode()) textNodes.push(node);
  textNodes.forEach(textNode => {
    const original = textNode.textContent;
    const wrapped = wrapExamVocab(original);
    if (wrapped !== original) {
      const span = document.createElement('span');
      span.innerHTML = wrapped;
      textNode.parentNode.replaceChild(span, textNode);
    }
  });
}

function handleVocabClick(e) {
  const bubble = e.target.closest('.exam-vocab-bubble');
  document.querySelectorAll('.exam-vocab-wrap.active').forEach(el => {
    if (!el.contains(e.target)) el.classList.remove('active');
  });
  if (bubble) {
    e.stopPropagation();
    bubble.closest('.exam-vocab-wrap').classList.toggle('active');
  }
}

function applyExamVocabTooltips(selector) {
  injectTooltipStyles();
  const containers = document.querySelectorAll(selector);
  if (!containers.length) return;
  containers.forEach(container => {
    if (container.dataset.vocabProcessed) return;
    processTextNodes(container);
    container.dataset.vocabProcessed = 'true';
  });
  document.removeEventListener('click', handleVocabClick);
  document.addEventListener('click', handleVocabClick);
}

function resetVocabProcessing(selector) {
  document.querySelectorAll(selector).forEach(c => { delete c.dataset.vocabProcessed; });
}

window.MaffsVocab = { applyExamVocabTooltips, resetVocabProcessing };
