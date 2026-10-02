# Learn + Practice — Reusable Template Spec
## First implementation: Factor Theorem, Algebraic Division & Remainder Theorem
**For:** Code Claude  
**From:** Project Claude  
**Date:** March 2026  
**Slug:** `factor-theorem`  
**Path:** `games/factor-theorem/index.html`

---

## What This Is

A new resource type for MaffsGames. Not a game — a pedagogical resource with three sections:

1. **Learn** — stepped worked examples, self-paced, fully explained
2. **Practice** — scaffolded questions, hints available, immediate feedback
3. **Test Yourself** — exam-style questions, no scaffolding, no hints

This template is designed to be reused for any topic that requires teaching before practice. Factor Theorem is the first implementation. Future topics using the same template: Integration by Parts, Completing the Square, Partial Fractions, Implicit Differentiation, Hypothesis Testing, Matrix Inverse.

**The template handles:** layout, navigation, progress tracking, responsive behaviour, KaTeX rendering, analytics.  
**The content file handles:** worked examples, practice questions, test questions, explanations.

---

## Responsive Layout — Critical

### Desktop (≥ 768px): Split screen
- Left panel (45%): worked example — current step shown, previous steps visible above in a lighter style
- Right panel (55%): interactive element — current step to complete, or practice question
- Panels scroll independently
- Divider: 1px `#2a2f45`, subtle

### Mobile (< 768px): Reveal-based tabs
- Single column
- Tab bar at top: "Example" | "Your Turn"
- Example tab: stepped reveal — student taps "Next Step" to reveal each step
- Your Turn tab: the interactive question
- No split — full width on each tab

### Implementation

```javascript
const isMobile = () => window.innerWidth < 768;

function initLayout() {
  if (isMobile()) {
    document.body.classList.add('mobile-layout');
    initTabLayout();
  } else {
    document.body.classList.add('desktop-layout');
    initSplitLayout();
  }
}

window.addEventListener('resize', debounce(() => {
  document.body.classList.remove('mobile-layout', 'desktop-layout');
  initLayout();
}, 300));
```

---

## Three-Section Structure

### Section 1 — Learn

Sequence of worked examples. Each example has numbered steps. Steps reveal one at a time (desktop: right panel updates; mobile: tap Next Step).

Every step has:
- The mathematical working (KaTeX)
- A brief explanation in plain English (1–2 sentences)
- Optionally: a "Why?" tooltip that gives deeper reasoning

Student controls: **Next Step** / **Previous Step** / **See Full Example** (reveals all steps at once)

Progress: small dots at top showing which step they're on within the current example. Separate progress showing which example they're on.

### Section 2 — Practice

Scaffolded questions. Scaffolding reduces as questions progress:

| Question tier | Scaffolding level |
|---------------|------------------|
| Questions 1–5 | Every step prompted — student fills one value per step |
| Questions 6–10 | Key steps prompted — student fills multiple values per step |
| Questions 11–20 | Structure shown, student fills working |
| Questions 21–30 | Answer only, with "Show working" hint available |
| Questions 31–40 | Answer only, no hints |

**Hint system:** Every question has up to 3 hints, revealed one at a time. Requesting a hint reduces the question score but never prevents completion.

**Scoring:** 
- Full marks: correct, no hints
- 2/3 marks: correct, 1 hint used
- 1/3 marks: correct, 2+ hints used
- 0: incorrect after all attempts

Running score shown as fraction.

### Section 3 — Test Yourself

Exam-style questions. No scaffolding. No hints. No worked examples visible.

Each question is a full multi-part problem (part a, b, c) as it would appear in an A-Level paper.

Results screen shows: score, time taken, and a specific link back to the relevant Learn section for any question answered incorrectly.

---

## Navigation

```
[Learn] [Practice] [Test Yourself]
```

Tab bar at top. Student can navigate freely between sections — no forced linear progression. Progress in each section is saved in `localStorage`.

Section state persists: if a student returns, they resume where they left off within each section.

---

## Visual Design

**Theme:** Dark, focused. Matches the existing A-Level game aesthetic.

**Palette:**
- Background: `#0f1117`
- Left panel (desktop): `#1a1d27`
- Right panel (desktop): `#0f1117`
- Mobile tab bar: `#1a1d27`
- Active tab: `#0d9488` teal underline
- Step card (revealed): `#1e2235`, `#2a2f45` border
- Step card (current): `#1e2235`, `#0d9488` left border
- Step card (future, dimmed): `#141620`, text `#374151`
- Explanation text: `#94a3b8` — distinct from working
- "Why?" tooltip: `#1a2744` navy background
- Hint button: `#f59e0b` amber
- Correct: `#22c55e` + ✓
- Incorrect: `#ef4444` + ✗

**Typography:**
- Mathematical working: KaTeX
- Explanation text: Outfit, `#94a3b8`, slightly smaller than working
- Section labels: Outfit bold, teal
- Step numbers: JetBrains Mono, small, teal

**Section badge:** Each resource type shows a badge instead of a level pill:

```
📖 Learn + Practice  |  A-Level  |  Level 4
```

---

## Analytics

`game_slug = 'factor-theorem'`

```javascript
mfg('game_started', {
  game_slug: 'factor-theorem',
  level: currentLevel,
  mode: currentSection  // 'learn' | 'practice' | 'test'
});

mfg('question_answered', {
  game_slug: 'factor-theorem',
  level: currentLevel,
  question_index: qIndex,
  correct: isCorrect,
  attempts: attemptCount,
  hints_used: hintsUsed,
  mode: currentSection
});

mfg('game_completed', {
  game_slug: 'factor-theorem',
  level: currentLevel,
  score: totalScore,
  questions_answered: total,
  questions_correct: correct,
  mode: 'test'  // completion only tracked for Test Yourself
});

// Section navigation
mfg('mode_selected', {
  game_slug: 'factor-theorem',
  mode: selectedSection
});
```

---

## SEO / Head

```html
<title>Factor Theorem — Learn + Practice — MaffsGames</title>
<meta name="description" content="Learn the Factor Theorem, Remainder Theorem and algebraic long division step by step. Worked examples, scaffolded practice and exam questions. Free A-Level maths resource.">
<link rel="canonical" href="https://maffsgames.co.uk/games/factor-theorem/">
```

---

# Factor Theorem Content

## Topic Overview

Three connected topics taught in sequence:

1. **Remainder Theorem** — f(x) ÷ (x − a) leaves remainder f(a)
2. **Factor Theorem** — if f(a) = 0 then (x − a) is a factor
3. **Algebraic Long Division** — dividing a polynomial by a linear factor
4. **Putting it together** — fully factorising a cubic

---

## Section 1 — Learn Content

### Example 1: The Remainder Theorem

**Setup text (shown before steps begin):**
> "When you divide a polynomial f(x) by (x − a), you don't always get zero remainder. The Remainder Theorem tells you exactly what that remainder will be — without doing the full division."

**Step 1:**
Working: `f(x) = 2x^3 - 3x^2 + x - 5`
Explanation: "Here's our polynomial. We want to find the remainder when we divide by (x − 2). The Remainder Theorem says the remainder equals f(2) — whatever you get when you substitute x = 2."

**Step 2:**
Working: `f(2) = 2(2)^3 - 3(2)^2 + (2) - 5`
Explanation: "Substitute x = 2 into every term. Replace every x with 2."

**Step 3:**
Working: `= 2(8) - 3(4) + 2 - 5`
Explanation: "Work out each power first: 2³ = 8, 2² = 4."

**Step 4:**
Working: `= 16 - 12 + 2 - 5`
Explanation: "Now multiply each term out."

**Step 5:**
Working: `= 1`
Explanation: "The remainder when f(x) is divided by (x − 2) is 1. We didn't need to do any long division to find this."

Why? tooltip: "The Remainder Theorem is provable by writing f(x) = (x − a)q(x) + r, where q(x) is the quotient and r is the remainder. Substituting x = a gives f(a) = 0 + r, so r = f(a)."

---

### Example 2: The Factor Theorem

**Setup text:**
> "The Factor Theorem is a special case of the Remainder Theorem. If the remainder is zero, then (x − a) divides exactly — making it a factor."

**Step 1:**
Working: `f(x) = x^3 - 7x - 6`
Explanation: "We want to find a factor of this cubic. The Factor Theorem says: try substituting values. If f(a) = 0, then (x − a) is a factor."

**Step 2:**
Working: `\text{Try } x = 3: \quad f(3) = (3)^3 - 7(3) - 6`
Explanation: "Which values should we try? Always start with the factors of the constant term (−6): try ±1, ±2, ±3, ±6. Start with small positive values."

**Step 3:**
Working: `= 27 - 21 - 6 = 0 \checkmark`
Explanation: "f(3) = 0, so by the Factor Theorem, (x − 3) is a factor of f(x)."

**Step 4:**
Working: `\therefore (x - 3) \text{ is a factor of } f(x)`
Explanation: "We've found one factor. Now we need to find the others — that's where algebraic long division comes in."

Why? tooltip: "The values to try are always ±(factors of the constant term) ÷ (factors of the leading coefficient). For a monic cubic (leading coefficient 1), it's simply ±(factors of the constant)."

---

### Example 3: Algebraic Long Division

**Setup text:**
> "We know (x − 3) is a factor of x³ − 7x − 6. Now we divide to find what's left. This is exactly like numerical long division — same process, just with algebra."

**Step 1:**
Working: `x^3 - 7x - 6 \div (x - 3)`
Explanation: "Set up the division. Important: our cubic has no x² term. Write it as x³ + 0x² − 7x − 6. The zero placeholder keeps your columns aligned."

**Step 2:**
Working: `x^3 \div x = x^2`
Explanation: "Divide the leading term of the dividend (x³) by the leading term of the divisor (x). This gives the first term of the quotient: x²."

**Step 3:**
Working: `x^2 \times (x - 3) = x^3 - 3x^2`
Explanation: "Multiply x² by the whole divisor (x − 3). Write the result below."

**Step 4:**
Working: `(x^3 + 0x^2 - 7x - 6) - (x^3 - 3x^2) = 3x^2 - 7x - 6`
Explanation: "Subtract. Be careful — you're subtracting the whole expression, so signs flip: −(x³ − 3x²) becomes −x³ + 3x². The x³ terms cancel, leaving 3x²."

**Step 5:**
Working: `3x^2 \div x = 3x`
Explanation: "Bring down and repeat. Divide the new leading term (3x²) by x to get 3x."

**Step 6:**
Working: `3x \times (x - 3) = 3x^2 - 9x`
Explanation: "Multiply 3x by the divisor."

**Step 7:**
Working: `(3x^2 - 7x - 6) - (3x^2 - 9x) = 2x - 6`
Explanation: "Subtract again. −(3x² − 9x) = −3x² + 9x. The 3x² cancels, leaving 2x − 6."

**Step 8:**
Working: `2x \div x = 2`
Explanation: "One more time. 2x ÷ x = 2."

**Step 9:**
Working: `2 \times (x - 3) = 2x - 6`
Explanation: "Multiply 2 by the divisor."

**Step 10:**
Working: `(2x - 6) - (2x - 6) = 0`
Explanation: "Subtract. Zero remainder — exactly what we expected since (x − 3) is a factor."

**Step 11:**
Working: `x^3 - 7x - 6 = (x - 3)(x^2 + 3x + 2)`
Explanation: "The quotient was x² + 3x + 2. So the cubic factorises as (x − 3)(x² + 3x + 2)."

**Step 12:**
Working: `x^2 + 3x + 2 = (x + 1)(x + 2)`
Explanation: "The quadratic factorises easily. Final answer: (x − 3)(x + 1)(x + 2)."

Why? tooltip: "The zero placeholder in step 1 is the single most common source of errors in algebraic long division. A missing term doesn't mean skip the column — write 0x² explicitly."

---

### Example 4: Putting It All Together

**Setup text:**
> "Here's the full process from start to finish — find a factor, divide, factorise the quadratic."

**Step 1:**
Working: `f(x) = 2x^3 + x^2 - 13x + 6`
Explanation: "A cubic with leading coefficient 2. Values to try: ±1, ±2, ±3, ±6, ±½, ±3/2."

**Step 2:**
Working: `f(2) = 2(8) + (4) - 13(2) + 6 = 16 + 4 - 26 + 6 = 0 \checkmark`
Explanation: "x = 2 gives zero, so (x − 2) is a factor."

**Step 3:**
Working: `2x^3 + x^2 - 13x + 6 \div (x - 2)`
Explanation: "Perform algebraic long division. All terms present, no zero placeholder needed this time."

**Step 4:**
Working: `2x^3 \div x = 2x^2`
Explanation: "First term of quotient: 2x²."

**Step 5:**
Working: `2x^2(x-2) = 2x^3 - 4x^2`
Explanation: "Multiply and subtract."

**Step 6:**
Working: `(2x^3 + x^2 - 13x + 6) - (2x^3 - 4x^2) = 5x^2 - 13x + 6`
Explanation: "5x² − 13x + 6 is the new dividend."

**Step 7:**
Working: `5x^2 \div x = 5x`
Explanation: "Next term: 5x."

**Step 8:**
Working: `5x(x-2) = 5x^2 - 10x`
Explanation: "Multiply and subtract: (5x² − 13x + 6) − (5x² − 10x) = −3x + 6."

**Step 9:**
Working: `-3x \div x = -3`
Explanation: "Last term: −3."

**Step 10:**
Working: `-3(x-2) = -3x + 6`
Explanation: "Multiply and subtract: (−3x + 6) − (−3x + 6) = 0. ✓"

**Step 11:**
Working: `2x^3 + x^2 - 13x + 6 = (x-2)(2x^2 + 5x - 3)`
Explanation: "Quotient is 2x² + 5x − 3."

**Step 12:**
Working: `2x^2 + 5x - 3 = (2x - 1)(x + 3)`
Explanation: "Factorise the quadratic. Check: (2x − 1)(x + 3) = 2x² + 6x − x − 3 = 2x² + 5x − 3 ✓"

**Step 13:**
Working: `\therefore 2x^3 + x^2 - 13x + 6 = (x-2)(2x-1)(x+3)`
Explanation: "Fully factorised. Three linear factors, three roots: x = 2, x = ½, x = −3."

---

## Section 2 — Practice Questions (40 questions)

### Scaffolding Tier 1 — Every step prompted (Q1–Q5)

```
Q1 | Remainder Theorem | A-Level
f(x) = x³ + 2x² − 5x + 1. Find the remainder when f(x) is divided by (x − 2).

Scaffolded steps:
  Step 1: "The remainder = f(___)" → student fills: 2
  Step 2: "f(2) = (2)³ + 2(2)² − 5(___) + 1" → student fills: 2
  Step 3: "= ___ + 8 − 10 + 1" → student fills: 8
  Step 4: "= ___" → student fills: 7
Answer: 7

Q2 | Remainder Theorem | A-Level
f(x) = 2x³ − x² + 3x − 4. Find the remainder when divided by (x + 1).
[Note: (x + 1) = (x − (−1)), so substitute x = −1]

Scaffolded steps:
  Step 1: "(x + 1) means substitute x = ___" → student fills: −1
  Step 2: "f(−1) = 2(−1)³ − (−1)² + 3(−1) − 4"
  Step 3: "= 2(___) − 1 − 3 − 4" → student fills: −1 [i.e. (−1)³]
  Step 4: "= ___ − 1 − 3 − 4" → student fills: −2
  Step 5: "= ___" → student fills: −10
Answer: −10

Q3 | Factor Theorem | A-Level
Show that (x − 1) is a factor of f(x) = x³ − 4x² + x + 6.

Scaffolded steps:
  Step 1: "To show (x − 1) is a factor, calculate f(___)" → student fills: 1
  Step 2: "f(1) = (1)³ − 4(1)² + (1) + 6"
  Step 3: "= 1 − ___ + 1 + 6" → student fills: 4
  Step 4: "= ___" → student fills: 4... wait, 1−4+1+6 = 4. But we need 0.
```

*(CC note: Q3 above has an error — x³ − 4x² + x + 6 evaluated at x=1 gives 1−4+1+6 = 4, not 0. (x−1) is NOT a factor of this polynomial. Replace Q3 with a corrected question where (x−1) IS a factor. Suggested: f(x) = x³ − 6x² + 11x − 6, f(1) = 1 − 6 + 11 − 6 = 0 ✓. Update steps accordingly.)*

```
Q4 | Factor Theorem | A-Level
f(x) = x³ + x² − 4x − 4. Show that (x + 2) is a factor and find all three factors.

Scaffolded steps:
  Step 1: "(x + 2) means test x = ___" → student fills: −2
  Step 2: "f(−2) = (−2)³ + (−2)² − 4(−2) − 4"
  Step 3: "= −8 + ___ + 8 − 4" → student fills: 4
  Step 4: "= ___" → student fills: 0
  Step 5: "Since f(−2) = 0, (x + 2) is a ___" → student fills: factor
  Step 6: "Divide: x³ + x² − 4x − 4 ÷ (x + 2). First term: x³ ÷ x = ___" → student fills: x²
  Step 7: "Quotient so far: x². Multiply: x²(x + 2) = x³ + ___" → student fills: 2x²
  Step 8: "Subtract: (x³ + x² − 4x − 4) − (x³ + 2x²) = ___x² − 4x − 4" → student fills: −1
  Step 9: "Next term: −x² ÷ x = ___" → student fills: −x
  Step 10: "Multiply: −x(x + 2) = −x² ___" → student fills: − 2x
  Step 11: "Subtract: (−x² − 4x − 4) − (−x² − 2x) = ___x − 4" → student fills: −2
  Step 12: "Last term: −2x ÷ x = ___" → student fills: −2
  Step 13: "Quotient = x² − x − 2 = (x − ___)(x + ___)" → student fills: 2 and 1
  Step 14: "Full factorisation: (x + 2)(x − 2)(x + 1)"
Answer: (x + 2)(x − 2)(x + 1)

Q5 | Remainder Theorem application | A-Level
f(x) = x³ + ax² − 3x + 2. When divided by (x − 1), the remainder is 5. Find a.

Scaffolded steps:
  Step 1: "Remainder when dividing by (x − 1) = f(___)" → student fills: 1
  Step 2: "f(1) = 1 + a − 3 + 2 = ___" → student fills: a (simplified: a + 0 = a... wait: 1 + a − 3 + 2 = a + 0 = a)
  Step 3: "So f(1) = a. We're told f(1) = ___" → student fills: 5
  Step 4: "Therefore a = ___" → student fills: 5
Answer: a = 5
```

### Scaffolding Tier 2 — Key steps prompted (Q6–Q10)

```
Q6 | A-Level
f(x) = x³ − 2x² − 5x + 6. Find a linear factor and fully factorise.
[Scaffolding: student told which value to try first, fills in f(a), confirms factor, then completes division with column headings provided]
Answer: (x − 1)(x + 2)(x − 3)

Q7 | A-Level
f(x) = 2x³ + 7x² + 2x − 3. Show (x + 3) is a factor and find the other factors.
[Scaffolding: substitution step prompted, division structure shown with first term filled]
Answer: (x + 3)(2x − 1)(x + 1)

Q8 | A-Level — Remainder with unknown
f(x) = x³ + bx + 4. When f(x) is divided by (x − 2) the remainder is 12. Find b.
[Scaffolding: f(2) = ___ equation prompted, student solves for b]
Answer: b = 0 (check: 8 + 2b + 4 = 12 → 2b = 0 → b = 0)

Q9 | A-Level
f(x) = x³ − 19x − 30. Fully factorise.
[Scaffolding: list of values to try given, student identifies correct one, completes division]
Answer: (x + 2)(x − 5)(x + 3)

Q10 | Level 4 framing
A beam deflection is modelled by d(x) = x³ − 6x² + 11x − 6, where x is the distance along the beam in metres. An engineer suspects there is zero deflection at x = 1, x = 2 and x = 3. Use the Factor Theorem to verify all three are roots.
[Scaffolding: first substitution prompted, remaining two guided briefly]
Answer: d(1) = 0, d(2) = 0, d(3) = 0. d(x) = (x−1)(x−2)(x−3) ✓
```

### Scaffolding Tier 3 — Structure shown, student fills working (Q11–Q20)

```
Q11 | A-Level
f(x) = x³ + 3x² − 4. Find all factors.
[Division structure shown as a template, student fills each term of quotient]
Answer: (x − 1)(x + 2)²

Q12 | A-Level
f(x) = 3x³ − 2x² − 7x − 2. Fully factorise.
Answer: (x − 2)(3x + 1)(x + 1)

Q13 | A-Level — Remainder
f(x) = x³ + cx² + 3x − 4. f(2) = 10. Find c and hence find the remainder when f(x) is divided by (x + 1).
Answer: c = 1. f(−1) = −1 + 1 − 3 − 4 = −7. Remainder = −7.

Q14 | Level 4 framing
A signal filter transfer function is H(s) = s³ + 2s² − s − 2. An engineer needs to find the poles (values of s where H(s) = 0). Fully factorise H(s).
Answer: (s − 1)(s + 1)(s + 2). Poles at s = 1, −1, −2.

Q15 | A-Level
f(x) = 2x³ − 3x² − 11x + 6. Fully factorise and solve f(x) = 0.
Answer: (x − 3)(2x + 1)(x − 2) = 0. x = 3, x = −½, x = 2.

Q16 | A-Level
f(x) = x³ + ax² + bx − 6. (x − 1) and (x + 2) are both factors. Find a and b.
Answer: Two equations from f(1)=0 and f(−2)=0: a + b = 5 and 4 − 2a − 2b = −12... 
*(CC note: verify this — set up f(1) = 1 + a + b − 6 = 0 → a + b = 5. f(−2) = −8 + 4a − 2b − 6 = 0 → 4a − 2b = 14 → 2a − b = 7. Solve: 3a = 12, a = 4, b = 1. Answer: a = 4, b = 1.)*

Q17–Q20: [4 further questions at this scaffolding level — mix of A-Level and Level 4 framing, including one with a repeated root and one requiring the student to find an unknown coefficient given two conditions]
```

### Scaffolding Tier 4 — Answer only, hint available (Q21–Q30)

```
Q21 | A-Level
Fully factorise f(x) = x³ − x² − 14x + 24.
Hint 1: Try x = 2.
Hint 2: After dividing by (x − 2), you get x² + x − 12.
Answer: (x − 2)(x + 4)(x − 3)

Q22 | A-Level  
f(x) = 6x³ + x² − 5x − 2. Fully factorise.
Hint 1: Try x = −½ (a non-integer root is possible when leading coefficient ≠ 1).
Hint 2: After dividing by (2x + 1), you get 3x² − x − 2.
Answer: (2x + 1)(3x + 2)(x − 1) ... 
*(CC note: verify: 6x³+x²−5x−2. Try x=−½: 6(−⅛)+¼+5/2−2 = −¾+¼+5/2−2 = −½+5/2−2 = 0 ✓. Division by (2x+1): quotient 3x²−x−2=(3x+2)(x−1). Full: (2x+1)(3x+2)(x−1). Verify by expansion.)*

Q23 | Level 4
The impedance of a circuit is modelled by Z(ω) = ω³ − 6ω² + 11ω − 6. Find all values of ω for which Z = 0.
Answer: ω = 1, 2, 3

Q24 | A-Level
f(x) = x³ + 2x² − x − 2. Factorise and hence sketch the curve y = f(x), marking all intercepts.
Answer: (x − 1)(x + 1)(x + 2). Roots at x = 1, −1, −2. y-intercept at (0, −2).

Q25–Q30: [6 further questions, hint available, covering: cubic with one repeated root, finding unknown constants using two remainder conditions, cubic where all three roots are negative, Level 4 engineering context with cubic model, proving a given factorisation is correct by expansion, finding a cubic given its three roots]
```

### Scaffolding Tier 5 — No hints (Q31–Q40)

```
Q31 | A-Level
Fully factorise 2x³ − x² − 18x + 9.
Answer: (x − 3)(x + 3)(2x − 1)

Q32 | A-Level
f(x) = x³ + px² + qx + 6. The curve passes through (1, 0) and (−1, 8). Find p and q, and hence fully factorise f(x).
Answer: f(1) = 0 → p + q = −7. f(−1) = 8 → −p + q = 13. Solving: q = 3, p = −10. f(x) = x³ − 10x² + 3x + 6... 
*(CC note: this needs verification — recheck the arithmetic and ensure a clean factorisation exists. If not, adjust the passing-through values to guarantee integer solutions.)*

Q33 | A-Level
Prove that (x − 2) is a factor of xⁿ − 2ⁿ for all positive integers n.
Answer: f(2) = 2ⁿ − 2ⁿ = 0 for all n. Therefore (x − 2) is a factor by the Factor Theorem. ✓

Q34 | Level 4
A cubic polynomial models the torque T(θ) = 4θ³ − 8θ² − θ + 2 in an engine component. Find all values of θ where torque is zero.
Answer: T(2) = 32−32−2+2 = 0. Divide by (θ−2): quotient 4θ²−1 = (2θ−1)(2θ+1). Roots: θ = 2, ½, −½.

Q35–Q40: [6 further exam-style questions with no scaffolding — including: a question requiring the student to prove a polynomial has no real roots after factoring out one linear factor, a question where the cubic has a repeated root, a question using the Factor Theorem to find two unknowns simultaneously, a Level 4 engineering context requiring roots to be interpreted physically, a question proving divisibility for all integers, and a final question combining remainder theorem, factor theorem and long division in a single multi-part problem]
```

*(CC note: for Q35–Q40, generate 6 questions following the established style. Every answer must be verified arithmetically before building. For the multi-part final question, structure as parts (a), (b), (c) to mirror A-Level paper format.)*

---

## Section 3 — Test Yourself (10 questions, exam style)

Each question is a full exam-style problem. No hints. No scaffolding. Time tracked.

```
T1 | 4 marks
f(x) = x³ − 3x − 2.
(a) Show that (x + 1) is a factor of f(x).     [1]
(b) Hence fully factorise f(x).                 [2]
(c) Solve f(x) = 0.                             [1]
Answer: (a) f(−1) = −1+3−2 = 0 ✓. (b) (x+1)²(x−2). (c) x = −1 (repeated), x = 2.

T2 | 3 marks
f(x) = 2x³ + ax² − 5x + 3. Given that (x − 1) is a factor, find a.    [2]
Hence find the remainder when f(x) is divided by (x + 2).              [1]
Answer: f(1) = 2 + a − 5 + 3 = 0 → a = 0. f(x) = 2x³ − 5x + 3. f(−2) = −16+10+3 = −3. Remainder = −3.

T3 | 5 marks
f(x) = 6x³ − 7x² − x + 2.
(a) Show that (x − 1) is not a factor.         [1]
(b) Show that (2x − 1) is a factor.            [1]
(c) Fully factorise f(x).                      [2]
(d) Hence solve 6x³ − 7x² − x + 2 = 0.       [1]
Answer: (a) f(1) = 6−7−1+2 = 0... wait, that IS zero. Rechoose polynomial.
*(CC note: T3 polynomial needs correcting — f(1) = 0 contradicts part (a). Replace with f(x) = 6x³ + x² − 5x − 2. Verify: f(1) = 6+1−5−2 = 0... still zero. Try f(x) = 6x³ − 11x² + 6x − 1. f(1) = 6−11+6−1 = 0... Try f(x) = 6x³ + 5x² − 3x − 2. f(1) = 6+5−3−2 = 6 ≠ 0 ✓. f(½) = 6(⅛)+5(¼)−3(½)−2 = ¾+5/4−3/2−2 = 3/4+5/4−6/4−8/4 = −6/4 ≠ 0. Try (3x+2): f(−⅔) = 6(−8/27)+5(4/9)−3(−2/3)−2 = −16/9+20/9+2−2 = 4/9 ≠ 0. CC should construct a valid T3 question from scratch with a polynomial that has one non-integer root and two integer roots, and where f(1) ≠ 0.)*

T4 | 4 marks
The polynomial p(x) = x³ + ax + b has a factor (x − 3) and leaves remainder 20 when divided by (x − 1).
Find a and b, and hence fully factorise p(x).
Answer: p(3) = 0: 27 + 3a + b = 0 → 3a + b = −27. p(1) = 20: 1 + a + b = 20 → a + b = 19. Subtract: 2a = −46 → a = −23, b = 42. p(x) = x³ − 23x + 42. Known factor (x−3). Divide: quotient x² + 3x − 14 = (x+7)(x−2). Full: (x−3)(x+7)(x−2).

T5 | 3 marks
Level 4: The characteristic equation of a matrix is λ³ − 6λ² + 11λ − 6 = 0. Find all eigenvalues.
Answer: Try λ=1: 1−6+11−6=0 ✓. Divide by (λ−1): λ²−5λ+6 = (λ−2)(λ−3). Eigenvalues: λ = 1, 2, 3.

T6–T10: [5 further exam-style questions following the same format. CC to generate, following the style of T1–T5. Must include: one question using remainder theorem only, one fully unsupported factorisation of a cubic with non-integer roots, one Level 4 engineering context, one question requiring proof, one multi-part question worth 6+ marks. All arithmetic must be verified before building.]*

---

## Portal Card

```
Name: Factor Theorem
Slug: factor-theorem
Type: Learn + Practice (not a game)
Levels: A-Level, Level 4
Topics: Algebra
Description: Learn the Remainder Theorem, Factor Theorem and algebraic long division from scratch — then practise with scaffolded questions and exam problems.
Timer: None
Badge: 📖 Learn + Practice
```

Add to portal in **A-Level section**. Display the "Learn + Practice" badge instead of a standard game card style — this is a resource, not a game, and should be visually distinct.

---

## Template Reuse Instructions for Future Topics

To create a new Learn + Practice resource using this template:

1. Copy `games/factor-theorem/index.html`
2. Replace the `CONTENT` object at the top of the script with the new topic's content
3. Update `game_slug`, title, meta description, canonical URL
4. The layout, navigation, responsive behaviour, scaffolding system, hint system, analytics, and KaTeX rendering are all inherited automatically

The `CONTENT` object structure:

```javascript
const CONTENT = {
  slug: 'factor-theorem',
  title: 'Factor Theorem',
  subtitle: 'Remainder Theorem, Factor Theorem & Algebraic Division',
  levels: ['alevel', 'level4'],
  sections: {
    learn: {
      examples: [ /* array of Example objects */ ]
    },
    practice: {
      questions: [ /* array of PracticeQuestion objects */ ]
    },
    test: {
      questions: [ /* array of TestQuestion objects */ ]
    }
  }
};
```

Future topics ready for this template:
- Integration by Parts (`integration-by-parts`)
- Completing the Square (`completing-the-square`)
- Partial Fractions (`partial-fractions-learn`)
- Implicit Differentiation (`implicit-differentiation`)
- Hypothesis Testing (`hypothesis-testing-learn`)
- Matrix Inverse (`matrix-inverse-learn`)

---

## Definition of Done

- [ ] Responsive layout: split screen ≥768px, reveal-based tabs <768px
- [ ] Resize handler switches layout without page reload
- [ ] Learn section: 4 worked examples, all steps correct mathematically
- [ ] Each step shows KaTeX working + plain English explanation
- [ ] "Why?" tooltips present on Steps 5 (Example 1), 4 (Example 2), 12 (Example 3), 13 (Example 4)
- [ ] Next/Previous/See All controls working
- [ ] Step progress dots update correctly
- [ ] Practice section: 40 questions loaded
- [ ] Scaffolding reduces correctly across tiers 1–5
- [ ] Hint system: up to 3 hints, score reduced per hint
- [ ] Test section: 10 exam-style questions, no hints, time tracked
- [ ] Results screen: per-question link back to relevant Learn step for incorrect answers
- [ ] Section tabs navigate freely, progress persists in localStorage
- [ ] All mathematical content verified arithmetically — especially Q3 (corrected), Q32, T3, T6–T10
- [ ] "Learn + Practice" badge shown on portal card instead of standard game style
- [ ] `mfg()` analytics events firing with correct mode field
- [ ] GA4 snippet `G-992JLHLP2D`
- [ ] KaTeX renders all expressions correctly
- [ ] Mobile tested: tabs work, KaTeX readable, step-by-step reveal smooth
- [ ] Words "idiot" and "stupid" do not appear
- [ ] Template `CONTENT` object is cleanly separated from template logic — future topics require only content replacement
