# Jon's Play-Test Log — August 2026

**Source:** Jon, playing the games directly. Started 2026-08-26, random sample across the roster.

Kept separate from `idea-backlog-2026-08.md` on purpose. That file is **Gemini's suggestions**,
logged unagreed. This file is **first-hand evidence from actually playing the game** — a different
and much stronger class of finding. Where the two touch the same game, the cross-ref says so.

Findings are recorded as observed, with verification added underneath. Verification is analysis,
not part of the original observation.

---

## 1. Circle Theorem Spotter — no diagrams at all

**Jon, 2026-08-26:** Too dry. It needs images. Asking the student to visualise the scenario
is not going to work for the majority of students.

**Verified — confirmed, and the problem is bigger than "dry".** Three separate faults:

**a. There is not one diagram in the file.** Zero `<canvas>`, zero `<svg>`, zero `<img>` across
all 23KB. Every question is plain text in a `.q-card`, answered by four text buttons. For a topic
where **every exam question ships with a figure**, this is the wrong modality — students are being
asked to do in their heads the exact step the exam board hands them on paper.

**b. The first 8 questions are not geometry — they are vocabulary matching.** The `ctx` field
*states the theorem in words* and `ask` is "Name this theorem":

> ctx: "A tangent to a circle is perpendicular to the radius at the point of contact."
> ask: "Name this theorem"
> correct: "Tangent is perpendicular to the radius"

The distractors are the same seven theorem names shuffled, so this is answerable by phrase-matching
with no spatial understanding whatsoever. A student can clear a third of the bank without once
picturing a circle. That is very likely why it reads as dry: for the first 8 questions it genuinely
is a definitions quiz wearing a geometry game's name.

**c. The meta description already promises diagrams that don't exist.** Line 7 and line 10 both
ship: *"55 GCSE questions with clear diagrams and instant marking."* That is live on the site and
in the OG card. Whatever else happens, that copy is currently false.

**Cross-ref — this supersedes Gemini's A3.** A3 proposed *interactive drag-to-verify* (drag points
around the circumference, watch angles update live). The backlog cross-ref rated it build-heavy —
a live geometry engine — for a game with no demonstrated demand (1 start, 0 completions).

That assessment stands for A3, but it does **not** apply here. **Static per-question SVG is a much
cheaper fix and solves the actual problem.** Seven theorems, each a circle with a handful of points,
chords, radii and a labelled angle. No engine, no interaction, no drag maths — just a diagram that
shows what the words are describing. Do the static diagrams first; A3's interactivity is a separate
question that only becomes worth asking once the game has figures at all.

**Suggested shape if picked up:** one small SVG per question, generated from a shared helper
(circle + labelled points on the circumference at given angles + chords/tangents/radii + an arc
marker for the angle in question). Rewrite the 8 "name this theorem" items to show a figure and
ask which theorem applies to *it* — that converts the site's dryest stretch into the exact skill
the game claims to teach. Fix the meta description at the same time.

---

## 2. Graph Transformer — the equation bar was showing raw LaTeX

**Found 2026-08-26** while implementing the backlog's A2 (ghost trails), not by playing.

`buildEquation()` returns LaTeX, but both equation slots were filled with `.textContent`:

```js
document.getElementById('eqTarget').textContent = buildEquation(...)   // leaks markup
```

KaTeX was already loaded in the head and never used. **23 of the 50 puzzles** use `sin x`, `1/x`
or `√x` as their base, all of which emit `\sin`, `\dfrac` or `\sqrt`. Those students were reading

> `y = \sqrt{(x-2)}+3`

off the target bar and being asked to match it.

**This is very likely the real cause of the 14% accuracy**, not the order-of-operations confusion
the backlog assumed. You cannot match a target you cannot read. Fixed by rendering through KaTeX,
with a plain-text fallback (`√`, `½`, superscripts) in case the deferred KaTeX script has not
landed yet.

**Lesson for the audits:** the help audit rated this game as adequately explained, and it was —
the guidance was fine, the *rendering* was broken. Neither the help audit nor the analytics could
have caught this. Only looking at the screen catches it, which is exactly what Jon's sampling does.

---

## 3. "Global leaderboard coming soon" — 78 games, all of them wrong

**Found 2026-08-26** while fixing Like Terms Collector.

**78 game files** displayed *"Global leaderboard coming soon"*. **All 78** call
`MaffsLeaderboard.submitScore`. The July retrofit (`5cc95e6`) shipped the feature to every game
but never removed the placeholder copy written before it.

So the site was telling students the leaderboard did not exist yet, while submitting their scores
to it — actively undermining the feature and any reason to replay for a better score. Trig Wars
additionally had the emoji corrupted to a mojibake `ð`.

All 78 replaced with a working link to `/leaderboards/`. The fix only touches files that actually
submit, so nothing claims a leaderboard it does not have.

---

## 4. Circle Theorem Spotter — Q48 is mathematically broken

**Found 2026-08-26** while building the diagrams for §1 — the figure could not be drawn
consistently, which is what exposed it.

> "Angle at centre = 2x. Angle at circumference = x + 15." — **Find x**, marked answer **15**.

The theorem says centre = 2 x circumference, so 2x = 2(x + 15), i.e. 2x = 2x + 30. **No solution.**
The marked answer of 15 only follows from `x + 15 = 2x`, which sets the two angles *equal* — the
exact misconception the game is meant to correct.

Left as-is rather than silently rewritten, because picking the replacement numbers is a teaching
decision. Two clean options:

- keep the answer 15: **centre = 4x, circumference = x + 15** &rarr; 4x = 2(x+15) &rarr; x = 15
- keep the expressions: **centre = 2x, circumference = x &minus; 15** &rarr; 2x = 2(x&minus;15) is still
  degenerate, so this one needs the centre changed too

The first is the smaller edit. The diagram currently shows a consistent 120&deg; construction with
the labels `2x` and `x + 15` exactly as the bank states them, so it will match whichever fix is
chosen once the numbers are sound.

---

## Running list — add findings here as the sample continues

Jon is sampling games at random through the day. Add each finding as a numbered section above
this line, in the same shape: **what he observed, verbatim**, then **verification** underneath
(confirmed / partly / not reproducible, plus whatever the code actually shows), then a
**cross-ref** if `idea-backlog-2026-08.md` already has an entry for that game.

To look at a game safely:

```
python scripts/serve-stubbed.py
# then http://127.0.0.1:8765/games/<slug>/
```

Never open a game against the live endpoint — it writes into the production Events sheet.

### Status of findings so far

| # | Game | Finding | Status |
|---|------|---------|--------|
| 1 | Circle Theorem Spotter | No diagrams anywhere; first 8 questions are vocabulary matching; meta description already claims "clear diagrams" | **Fixed** 2026-08-26 — all 55 have SVG figures, Q1-8 rewritten |
| 2 | Graph Transformer | Equation bar rendered raw LaTeX in 23 of 50 puzzles | **Fixed** 2026-08-26 (`02f41a5`) |
| 3 | Site-wide | 78 games said "leaderboard coming soon" while submitting to the live one | **Fixed** 2026-08-26 (`02f41a5`) |
| 4 | Circle Theorem Spotter | Q48 has no solution as written; marked answer encodes the misconception | **Open** — needs Jon's call on the numbers |

---

## Snagging

Reported findings that have **not** been reproduced against the code as it stands. They are kept
here rather than in the numbered sections above, because a numbered section is a confirmed
finding and these are not yet. Each needs one replay by Jon to either become a numbered finding
or be closed.

| # | Game | Reported | Verification |
|---|------|----------|--------------|
| S1 | Truth Will Set You Free | A "can be simplified" claim shown against `A · B` | **Unconfirmed — does not reproduce against current code (`bbLink` null on A·B); Jon to replay** |

**S1, what the code shows.** The "simplifies to …" sentence is written only on the `q.bbLink`
branch (`:856`). Where `bbLink` is `null` the `else` branch runs and the panel reads the neutral
*"To practise your Boolean algebra skills, try Boolean Blitz."* — it makes no claim about the
expression at all. Every `A · B`-shaped question in the bank has `bbLink: null`, so there is no
question that can produce the reported wording. Either the game has changed since the sample, or
the observation was of a different question. **Jon to replay it once and then either close this
row or give the exact wording seen and the question it was on.**
