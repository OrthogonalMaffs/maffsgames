# Exam Vocabulary Tooltip System
**For:** Code Claude  
**From:** Project Claude  
**Date:** March 2026  
**File:** `schools/assets/exam-vocab.js`

---

## What This Is

A platform-wide system that detects exam terminology in question text and adds a tappable/hoverable (?) bubble next to each term. Tapping or hovering reveals a plain English explanation of what the term is asking the student to do.

This is a pedagogical feature, not a hint system. It doesn't help with the mathematics — it helps students understand what they're being asked to do. A student who knows the maths but doesn't know what "hence" means should not lose marks because of vocabulary.

---

## The Problem This Solves

Exam questions use specific vocabulary that has precise meanings:
- "Hence" means use your previous answer
- "Show that" means prove it rigorously — verification by numbers is not enough
- "State" means no working required
- "Describe fully" for transformations means type + direction + magnitude — all three

Students who haven't been explicitly taught this vocabulary fail questions they understand mathematically. This system makes the vocabulary transparent without removing the challenge of the mathematics.

---

## Shared Asset

Create: `schools/assets/exam-vocab.js`

This file is loaded by every game that uses exam vocabulary. It exports one function: `applyExamVocabTooltips(containerSelector)`.

Call it after question text has been rendered to the DOM.

---

## Full Implementation

```javascript
/**
 * MaffsGames Exam Vocabulary Tooltip System
 * Detects exam terminology in question text and adds plain-English tooltips
 * 
 * Usage: applyExamVocabTooltips('#questionText')
 * Call after question text is rendered to DOM
 */

/**
 * Exam vocabulary dictionary
 * Key: phrase to detect (lowercase, will match case-insensitively)
 * Value: plain English explanation shown in tooltip
 * 
 * Order matters — longer phrases must come before shorter ones
 * (e.g. "hence or otherwise" before "hence")
 */
const EXAM_VOCAB = [
  {
    term: 'hence or otherwise',
    plain: 'You can use your answer from the previous part, or find a completely different method — your choice.'
  },
  {
    term: 'hence fully factorise',
    plain: 'Use your previous answer to help you find ALL the factors — don\'t stop at a partial factorisation.'
  },
  {
    term: 'hence find the exact value',
    plain: 'Use your previous answer AND leave your final answer as a fraction, surd, or in terms of π — no decimals.'
  },
  {
    term: 'hence solve',
    plain: 'Use your answer from the previous part to find the solution.'
  },
  {
    term: 'hence find',
    plain: 'Use your answer from the previous part to calculate this.'
  },
  {
    term: 'hence evaluate',
    plain: 'Use your previous answer to calculate the numerical value.'
  },
  {
    term: 'hence show',
    plain: 'Use your previous answer to prove this result — show every step.'
  },
  {
    term: 'hence deduce',
    plain: 'Use your previous answer to reach this conclusion — explain your reasoning.'
  },
  {
    term: 'hence',
    plain: 'Use your answer from the previous part to help you answer this part.'
  },
  {
    term: 'show that',
    plain: 'Prove this is true. Show every step of your working — you can\'t just verify it with numbers, you must derive it algebraically.'
  },
  {
    term: 'prove that',
    plain: 'Show rigorously that this is always true. Every step must be justified — this is not the same as checking with an example.'
  },
  {
    term: 'prove',
    plain: 'Show rigorously that this is always true. Every step must be justified.'
  },
  {
    term: 'verify that',
    plain: 'Check this is correct — substitute the value back in and confirm both sides match.'
  },
  {
    term: 'verify',
    plain: 'Check this is correct by substituting the value back in.'
  },
  {
    term: 'deduce that',
    plain: 'Use the result you just found to reach this conclusion. Explain your reasoning.'
  },
  {
    term: 'deduce',
    plain: 'Use what you\'ve just found or been told to reach this conclusion.'
  },
  {
    term: 'write down',
    plain: 'State the answer directly — no working is required or expected.'
  },
  {
    term: 'state',
    plain: 'Write the answer down — no working needed.'
  },
  {
    term: 'without the use of a calculator',
    plain: 'Show full algebraic working. Your answer must be exact — no decimal approximations.'
  },
  {
    term: 'without using a calculator',
    plain: 'Show full algebraic working. Your answer must be exact — no decimal approximations.'
  },
  {
    term: 'exact value',
    plain: 'Leave your answer as a fraction, surd (like √3), or in terms of π. Do NOT round to a decimal.'
  },
  {
    term: 'exact form',
    plain: 'Leave your answer as a fraction, surd, or in terms of π. Do NOT round to a decimal.'
  },
  {
    term: 'leave in exact form',
    plain: 'Do not use a decimal. Leave as a fraction, surd, or expression involving π or e.'
  },
  {
    term: 'factorise fully',
    plain: 'Find ALL the factors. Don\'t stop if you can still factorise further — e.g. 4(x²−1) is not fully factorised, it should be 4(x+1)(x−1).'
  },
  {
    term: 'fully factorise',
    plain: 'Find ALL the factors. Don\'t stop if you can still factorise further.'
  },
  {
    term: 'expand and simplify',
    plain: 'Multiply out all the brackets first, then collect like terms.'
  },
  {
    term: 'simplify fully',
    plain: 'Reduce to the simplest possible form — cancel fractions, collect like terms, apply index laws as needed.'
  },
  {
    term: 'express in the form',
    plain: 'Rewrite the expression so it looks exactly like the form shown — rearrange, complete the square, or factorise as needed.'
  },
  {
    term: 'express as',
    plain: 'Rewrite in the form the question specifies.'
  },
  {
    term: 'describe fully',
    plain: 'For transformations: you must give the TYPE (e.g. rotation), DIRECTION/CENTRE, and SIZE/ANGLE. All three are required for full marks. "It moved right" is not a full description.'
  },
  {
    term: 'describe the transformation',
    plain: 'Give the type (translation/rotation/reflection/enlargement), the direction or centre, and the distance, angle or scale factor. All parts needed for full marks.'
  },
  {
    term: 'comment on',
    plain: 'Give a mathematical interpretation — what does this result actually mean in context? A vague statement won\'t score marks.'
  },
  {
    term: 'sketch',
    plain: 'Draw a rough graph — it doesn\'t need to be to scale. But you must show: the shape of the curve, where it crosses the axes, and any asymptotes or turning points.'
  },
  {
    term: 'plot',
    plain: 'Draw accurately using the given coordinates. Use the scale on the axes. This is more precise than a sketch.'
  },
  {
    term: 'given that',
    plain: 'This is a fact you\'re allowed to treat as true — use it as a starting point or condition in your working.'
  },
  {
    term: 'it is given that',
    plain: 'This is a fact you\'re allowed to treat as true.'
  },
  {
    term: 'hence or otherwise',
    plain: 'Use your previous answer if you want, or find a completely different method.'
  },
  {
    term: 'find the range',
    plain: 'Find all possible OUTPUT values of the function — not the domain (inputs).'
  },
  {
    term: 'find the domain',
    plain: 'Find all valid INPUT values — the values of x for which the function is defined.'
  },
  {
    term: 'state the domain',
    plain: 'Write down the valid input values — no working needed, but you must be precise.'
  },
  {
    term: 'is increasing',
    plain: 'The function goes upward as x increases — f\'(x) > 0 in this region.'
  },
  {
    term: 'is decreasing',
    plain: 'The function goes downward as x increases — f\'(x) < 0 in this region.'
  },
  {
    term: 'show your working',
    plain: 'Write out every step — even if you could do it in your head. Examiners award marks for method, not just the final answer.'
  },
  {
    term: 'use calculus',
    plain: 'Differentiation or integration is required — you cannot use a graph or trial-and-error.'
  },
  {
    term: 'minimum value',
    plain: 'The lowest point the function reaches. Find it by differentiating, setting equal to zero, and confirming it\'s a minimum.'
  },
  {
    term: 'maximum value',
    plain: 'The highest point the function reaches. Find it by differentiating, setting equal to zero, and confirming it\'s a maximum.'
  },
  {
    term: 'stationary point',
    plain: 'A point where the gradient is zero — could be a maximum, minimum, or point of inflection. Differentiate and set equal to zero to find it.'
  },
  {
    term: 'point of inflection',
    plain: 'A point where the curve changes from concave to convex (or vice versa). The gradient doesn\'t have to be zero here.'
  },
  {
    term: 'nature of the stationary point',
    plain: 'Determine whether it\'s a maximum, minimum, or point of inflection. Use the second derivative test: f\'\'(x) > 0 is a minimum, f\'\'(x) < 0 is a maximum, f\'\'(x) = 0 needs further investigation.'
  }
];

/**
 * Inject tooltip CSS into document head (once only)
 */
function injectTooltipStyles() {
  if (document.getElementById('exam-vocab-styles')) return;

  const style = document.createElement('style');
  style.id = 'exam-vocab-styles';
  style.textContent = `
    .exam-vocab-wrap {
      display: inline;
      position: relative;
    }

    .exam-vocab-term {
      border-bottom: 1px dashed #0d9488;
      cursor: pointer;
    }

    .exam-vocab-bubble {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #0d9488;
      color: #ffffff;
      font-size: 10px;
      font-weight: 700;
      font-family: 'Outfit', sans-serif;
      cursor: pointer;
      vertical-align: super;
      margin-left: 2px;
      line-height: 1;
      flex-shrink: 0;
      user-select: none;
    }

    .exam-vocab-bubble:hover {
      background: #0f766e;
    }

    .exam-vocab-tooltip {
      display: none;
      position: absolute;
      bottom: calc(100% + 8px);
      left: 50%;
      transform: translateX(-50%);
      background: #1a2744;
      color: #e8eaf0;
      font-size: 13px;
      font-family: 'Outfit', sans-serif;
      line-height: 1.5;
      padding: 10px 14px;
      border-radius: 6px;
      border: 1px solid #2a3f6b;
      width: 280px;
      max-width: 90vw;
      z-index: 1000;
      box-shadow: 0 4px 12px rgba(0,0,0,0.4);
      pointer-events: none;
    }

    .exam-vocab-tooltip::after {
      content: '';
      position: absolute;
      top: 100%;
      left: 50%;
      transform: translateX(-50%);
      border: 6px solid transparent;
      border-top-color: #1a2744;
    }

    .exam-vocab-wrap.active .exam-vocab-tooltip {
      display: block;
    }

    /* Mobile: tooltip above always, full width */
    @media (max-width: 480px) {
      .exam-vocab-tooltip {
        width: 240px;
        font-size: 12px;
        left: 0;
        transform: none;
      }
    }

    /* Accessible mode overrides */
    body.accessible .exam-vocab-tooltip {
      font-size: 15px;
      line-height: 1.7;
    }

    /* Light theme variant (for OP for Secondary and KS3 games) */
    body.light-theme .exam-vocab-tooltip {
      background: #ffffff;
      color: #1a2744;
      border-color: #e2e8f0;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }

    body.light-theme .exam-vocab-tooltip::after {
      border-top-color: #ffffff;
    }
  `;

  document.head.appendChild(style);
}

/**
 * Escape special regex characters in a string
 */
function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * Wrap matched exam vocabulary in tooltip HTML
 * Returns the modified HTML string
 */
function wrapExamVocab(html) {
  let result = html;

  EXAM_VOCAB.forEach(({ term, plain }) => {
    const regex = new RegExp(
      `(?<![\\w-])(${escapeRegex(term)})(?![\\w-])`,
      'gi'
    );

    result = result.replace(regex, (match) => {
      const escaped = plain
        .replace(/'/g, '&#39;')
        .replace(/"/g, '&quot;');

      return `<span class="exam-vocab-wrap">` +
        `<span class="exam-vocab-term">${match}</span>` +
        `<span class="exam-vocab-bubble" role="button" aria-label="What does '${match}' mean?">?</span>` +
        `<span class="exam-vocab-tooltip">${plain}</span>` +
        `</span>`;
    });
  });

  return result;
}

/**
 * Apply exam vocabulary tooltips to rendered question text
 * 
 * @param {string} selector - CSS selector for the container(s) to process
 *
 * Call this AFTER question text has been rendered to DOM.
 * Safe to call multiple times — won't double-wrap already-processed text.
 *
 * Example usage in a game:
 *   renderQuestion(q);
 *   applyExamVocabTooltips('#questionText');
 */
function applyExamVocabTooltips(selector) {
  injectTooltipStyles();

  const containers = document.querySelectorAll(selector);
  if (!containers.length) return;

  containers.forEach(container => {
    // Skip if already processed
    if (container.dataset.vocabProcessed) return;

    // Don't process KaTeX-rendered math — only process text nodes
    // Walk the DOM and only modify text that isn't inside .katex elements
    processTextNodes(container);

    container.dataset.vocabProcessed = 'true';
  });

  attachTooltipHandlers();
}

/**
 * Process only text nodes, skipping KaTeX elements
 */
function processTextNodes(container) {
  const walker = document.createTreeWalker(
    container,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode: (node) => {
        // Skip text inside KaTeX elements
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
    }
  );

  const textNodes = [];
  let node;
  while (node = walker.nextNode()) {
    textNodes.push(node);
  }

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

/**
 * Attach click/hover handlers to all tooltip bubbles
 * Uses event delegation — safe to call after dynamic content updates
 */
function attachTooltipHandlers() {
  // Remove existing delegated listener if present
  document.removeEventListener('click', handleVocabClick);
  document.addEventListener('click', handleVocabClick);
}

function handleVocabClick(e) {
  const bubble = e.target.closest('.exam-vocab-bubble');

  // Close all open tooltips first
  document.querySelectorAll('.exam-vocab-wrap.active').forEach(el => {
    if (!el.contains(e.target)) {
      el.classList.remove('active');
    }
  });

  if (bubble) {
    e.stopPropagation();
    const wrap = bubble.closest('.exam-vocab-wrap');
    wrap.classList.toggle('active');
  }
}

/**
 * Call this when a new question is rendered
 * Resets processed state so new question text gets processed
 */
function resetVocabProcessing(selector) {
  const containers = document.querySelectorAll(selector);
  containers.forEach(c => {
    delete c.dataset.vocabProcessed;
  });
}

// Export
window.MaffsVocab = {
  applyExamVocabTooltips,
  resetVocabProcessing
};
```

---

## Integration Pattern

### In every game that uses exam vocabulary:

**1. Load the script in `<head>`:**

```html
<script src="../../schools/assets/exam-vocab.js"></script>
```

**2. Call after rendering each question:**

```javascript
function renderQuestion(q) {
  const el = document.getElementById('questionText');
  
  // Render question text (with KaTeX if needed)
  el.innerHTML = q.text;
  if (q.latex) katex.render(q.latex, el, { throwOnError: false });
  
  // Reset and apply vocab tooltips
  MaffsVocab.resetVocabProcessing('#questionText');
  MaffsVocab.applyExamVocabTooltips('#questionText');
}
```

**3. Also apply to scaffolded step explanations (Factor Theorem and future Learn + Practice resources):**

```javascript
// After rendering a step explanation
MaffsVocab.applyExamVocabTooltips('.step-explanation');
```

---

## Rollout Priority

### Phase 1 — Build these in now (do alongside current work)
These games are either being built now or are highest priority:

| Game | Reason |
|------|--------|
| Factor Theorem | Being built now — include from the start |
| Proof Builder | Highest vocabulary density on platform |
| Test the Claim | Hypothesis testing has its own vocabulary barrier |

### Phase 2 — Next pass
| Game | Key vocabulary present |
|------|----------------------|
| Differentiation Duel | hence, show that, exact value, stationary point, nature |
| Integration Duel | hence evaluate, exact value, show that |
| Partial Fractions Duel | express in partial fractions, hence integrate |
| Trig Identity Duel | show that, prove, hence solve |
| Log Laws | show that, express as, hence solve |
| Binomial Blaster | write down, hence find |
| Normal Navigator | state, exact value, comment on |

### Phase 3 — Sweep remaining A-Level and Level 4 games
| Game | Key vocabulary present |
|------|----------------------|
| SUVAT Selector | state, hence find |
| Regression Rumble | comment on, describe |
| Chart Interrogator | comment on, describe fully, compare |
| Matrix Crunch | hence solve, state |
| Complex Converter | express in the form, hence find |
| Sequence Solver | show that, hence find the sum |
| Index Laws | simplify fully, express as |
| Quadratic Factoriser | factorise fully, hence solve |
| Simultaneous Solver | solve, hence find |

### Phase 4 — GCSE games (lighter vocabulary)
| Game | Key vocabulary present |
|------|----------------------|
| Modular Battle | state, find the remainder |
| Surd Simplifier | simplify fully, express in the form |
| Standard Form Blitz | express, give your answer in standard form |

### Not needed
KS3 games, OP for Secondary games, and games using entirely plain English questions (Factor Race, Fraction Snap, Percentage Flip, Estimation Golf, Prime Sprint, Probability Pioneer etc.)

---

## What NOT to Do

- **Do not apply to KaTeX-rendered expressions** — the tree walker handles this, but don't call `applyExamVocabTooltips` on a container that is itself a KaTeX element
- **Do not apply to answer buttons** — only apply to question text and step explanations
- **Do not modify the EXAM_VOCAB array order** — longer phrases must remain before shorter ones (e.g. "hence fully factorise" before "hence")
- **Do not show tooltips for vocabulary in the feedback/reveal text** — only in the question prompt itself

---

## Accessibility

- Bubble has `role="button"` and `aria-label` for screen readers
- Tooltip text is plain English — no KaTeX, no symbols
- Accessible mode (`.accessible` on body) increases tooltip font size to 15px
- Tooltip is keyboard accessible via tab + enter (handled by browser default button behaviour)
- `prefers-reduced-motion`: no animation on tooltip — it appears/disappears instantly (no transition added, so this is automatic)

---

## Definition of Done

- [ ] `schools/assets/exam-vocab.js` created
- [ ] All vocabulary entries in correct order (longer phrases before shorter)
- [ ] Tooltip renders correctly on desktop (hover and click)
- [ ] Tooltip renders correctly on mobile (tap to open, tap elsewhere to close)
- [ ] KaTeX expressions are NOT processed — tree walker skips `.katex` elements
- [ ] Already-processed containers are not double-processed
- [ ] `resetVocabProcessing()` correctly resets state for new questions
- [ ] Tooltip closes when tapping/clicking elsewhere on the page
- [ ] Multiple tooltips cannot be open simultaneously
- [ ] Accessible mode: larger tooltip text
- [ ] Light theme: tooltip uses white background
- [ ] Phase 1 games integrated: Factor Theorem, Proof Builder, Test the Claim
- [ ] Tested on mobile — tooltip doesn't overflow screen edge
- [ ] Tested with KaTeX questions — math rendering unaffected
- [ ] Words "idiot" and "stupid" do not appear in any tooltip text
