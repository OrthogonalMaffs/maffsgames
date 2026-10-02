# Idea Backlog — August 2026

**Source:** Gemini, requested by Jon 2026-08-26. Logged for later work — **nothing here is agreed or scheduled.**

Ideas are recorded as supplied. Everything under **Cross-ref** is added at logging time by
checking each idea against `.claude/rules/game-roster.md` (93 games) and the live
"MaffsGames Events" Dashboard tab (rebuilt 2026-08-26 07:49). Keep the two separated —
the cross-refs are analysis, not part of the original suggestion.

## ⚠️ Read before picking anything up

**The supporting data is holiday data.** The 7-day window behind every cross-ref below is
~69 game starts during the summer break — tiny and self-selected. Re-pull the Dashboard in
late September before committing to any of this.

**The instrumentation has known faults** (blank-slug abandons, `game_started` firing on level
switch, out-of-order question events). Completion and accuracy figures quoted below inherit
those faults. Fixing analytics is the prerequisite for trusting any of it.

### Status — updated 2026-08-26

Some of this has now been actioned. **Check here before picking anything up.**

| Item | Status |
|---|---|
| **A9** Trig Wars | **Done, as the prerequisite not the proposal.** Full Mission Briefing shipped (`02f41a5`). The wind/elevation modifiers are still *not* agreed — re-measure in term time first. Note the "27% accuracy" quoted below is a **shot hit-rate**, not comprehension; missing then correcting is the intended artillery loop. |
| **A2** Graph Transformer | **Ghost trails shipped** (`02f41a5`) as "Show steps". But the 14% accuracy turned out to be **a rendering bug** — the equation bar was printing raw LaTeX in 23 of 50 puzzles. Fixed in the same commit. See `jon-playtest-2026-08.md` §2. |
| **A8** Like Terms Collector | **Done, the length fix, not the combo multiplier** — the cross-ref below called this right. Stage 3 split into 3 rounds of 10 with checkpoints (`02f41a5`). |
| **A3** Circle Theorem Spotter | **Superseded.** Jon play-tested it: there are no diagrams in the game *at all*. Static per-question SVG comes first and is far cheaper than the drag-to-verify engine proposed here. See `jon-playtest-2026-08.md` §1. |
| Everything else | Untouched. |

Also fixed alongside: **78 games displayed "Global leaderboard coming soon"** while all 78
submitted to the live leaderboard. Any completion figure quoted below predates that fix.

### Fast triage

| Verdict | Items |
|---|---|
| **Strong — data supports it** | Graph Transformer ghost trails |
| **Contradicted by data** | Trig Wars wind/elevation |
| **Real curriculum gap** | Bounds & Safe Cracker · Inequality Turf War · Capture-Recapture Safari · Histogram Architect |
| **Duplicates an existing game** | Standard Form Asteroids · Vector Voyage · Tangent Racer · Proof Chain · Tree Diagram Detective |
| **No data either way** | Bearing Blitz · Circle Theorem Spotter · Angle Ace · Surd Simplifier · Spot the Error/Muppet · Fraction Snap |

---

# Part A — 10 enhancements to existing games

## A1. Bearing Blitz — Radar Sweep & 3-Digit Protocol
Add a sweeping radar effect and strictly enforce 3-figure notation (reject `45°` in favour of
`045°`). Optional "protractor overlay" toggle in practice mode to scaffold KS3 learners before
testing them blind.

**Cross-ref:** No starts in the 7-day window — no evidence either way. The 3-figure enforcement
is a genuine exam-technique win regardless of engagement data; bearings are marked wrong without
it. The scaffold toggle fits the pattern that's currently missing across the site (see A9/A6).

## A2. Graph Transformer — Step-by-Step Ghost Trails
For combined transformations (`y = 2f(x − 3) + 1`), display intermediate "ghost" curves showing
translation and stretch sequentially, so pupils see the order of operations visually.

**Cross-ref: strongest item in Part A.** `graph-transformer` has the **worst accuracy on the
site — 14%** (1 correct of 7 answers). Order-of-operations confusion is the textbook cause, and
ghost trails are a scaffolding fix aimed squarely at it. Small sample, but the mechanism matches
the failure mode exactly. Prioritise.

## A3. Circle Theorem Spotter — Interactive Drag-to-Verify
Let students drag points around the circumference to watch angles change dynamically before
answering, reinforcing *why* the theorem holds (e.g. angles in the same segment staying equal).

**Cross-ref:** 1 start, 0 completions in window — no usable signal. Note this is a build-heavy
item (live geometry engine) for a game with no demonstrated demand. Re-check in term time first.

## A4. Angle Ace — Multi-Step Cascade Puzzles
Chain mode: finding one basic angle (e.g. vertically opposite) reveals the value needed to solve
alternate or co-interior angles across complex parallel-line diagrams.

**Cross-ref:** No starts in window. Angle Ace already has the strongest help section on the site
(2-para explanation + full 8-rule reason grid), so it can carry added difficulty better than most.
Reasonable candidate once demand is confirmed.

## A5. Estimation Golf — Wind & Hazard Penalties
Wind conditions and hazard zones narrow the margin of error. Tight estimates yield straight
drives; loose estimates slice or land in the rough.

**Cross-ref: blocked on instrumentation.** Shows 4 starts / 0 completions (0%), but the raw log
shows it firing `game_started` on every *level switch* — six starts in 35 seconds at
2026-03-25T18:19 with no answers between them. The 0% is probably a measurement artifact.
**Fix the analytics before designing anything for this game.**

## A6. Spot the Error / Spot the Muppet — "Red Pen" Precision
Require players to click the exact line or operator where the algebraic slip occurred (e.g. a
negative not distributed) rather than picking from multiple choice.

**Cross-ref:** No starts in window. Pedagogically the strongest idea in Part A after A2 —
it converts recognition into location, which is a genuinely harder and more useful skill.
Note it changes the answer model, so scoring and the leaderboard key need thought.

## A7. Surd Simplifier — Tile Merging Mechanic
2048-style merging: `√12` and `√27` become `2√3` and `3√3`, summing to `5√3` to clear the board.

**Cross-ref:** No starts in window. Biggest build in Part A by some distance — this is a new game
engine wearing an existing game's name, not an enhancement. If pursued, consider shipping it as a
separate game rather than replacing a working 100-question drill.

## A8. Like Terms Collector — Combo Multipliers for Sign Traps
Streak bonuses for quickly sorting negative terms (`−3x²` vs `3x`), penalising the common
misconception of dropping the negative when rearranging.

**Cross-ref: probably aimed at the wrong problem.** `like-terms-collector` is the 2nd
most-started game (11 starts) with **178 answers at 78% accuracy** — students are engaging
happily and mostly getting it right. But completion is **9%** (1 of 11). 178 answers across
11 starts ≈ 16 questions each against a 45-question bank, so they're quitting a third of the
way through. That reads as **too long**, not too error-prone. A length/checkpoint fix likely
beats a combo multiplier. Worth testing shorter rounds first.

## A9. Trig Wars — Wind & Elevation Modifiers
Upgrade 2-player mode with elevation deltas and crosswinds, requiring multi-step trig
(Pythagoras + SOH CAH TOA, or the Sine Rule) for line-of-sight firing solutions.

**Cross-ref: the data contradicts this one.** `trig-wars` is the **most-started game on the
site (13)** with **8% completion** and **27% accuracy** — and it is one of only **three games
with no help section at all**. The evidence says students already can't finish it. Adding
multi-step difficulty to the hardest, least-completed game would make the drop-off worse.

**Do the help section first**, re-measure, and only then consider modifiers — ideally as an
opt-in advanced mode rather than a change to the default experience.

## A10. Fraction Snap — Visual Bar Proofs on Misses
On an incorrect answer, briefly animate the two fraction bars side by side to show equivalence
or discrepancy instantly.

**Cross-ref:** `fraction-equivalence` is at **87% accuracy** (13 of 15) — one of the healthier
games. Low urgency, but it's a cheap, self-contained addition with no scoring implications.
Good candidate for a spare hour rather than a planned sprint.

---

# Part B — 10 new game concepts

## B1. Vector Voyage — KS3 / GCSE / Level 4
Navigate a ship using column vector addition and scalar multiples against ocean currents. Enter
vector components to reach waypoints while avoiding rocks.

**Cross-ref: overlaps `component-crusher`**, which already covers column notation, i/j/k,
magnitude, scalar product, angles and 3D at L4 across 45 scenarios. The *navigation* framing is
new and the KS3 entry point is lower than component-crusher offers, so there may be room — but
scope it as "KS3 on-ramp to component-crusher", not a standalone vectors game.

## B2. Bounds & Safe Cracker — GCSE / Core Maths
Crack a safe using error intervals. Clues give truncated or rounded measurements ("Length = 4.8 cm
to 1 d.p."); players enter exact bounds `4.75 ≤ x < 4.85` to open the lock.

**Cross-ref: genuine gap — nothing in the 93-game roster covers bounds or error intervals.**
Solid GCSE topic, notoriously badly examined, and the safe-cracking framing fits the strict
inequality notation naturally. **Strongest new-game candidate in Part B.**

## B3. Histogram Architect — GCSE / A-Level
Build accurate histograms with unequal class widths by calculating frequency density
(FD = frequency ÷ class width) rather than plotting raw frequency.

**Cross-ref: likely a real gap.** `stat-attack` covers grouped frequency tables (modal class,
median class, mean, SD) and `chart-interrogator` covers diagram reading, but **frequency density
and unequal class widths aren't covered by either**. Classic GCSE Higher trap. Verify against
stat-attack's bank before building.

## B4. Venn Venture / Set Master — KS3 / GCSE
Rapid-fire sorting into 2- and 3-set Venn diagrams, classifying numbers by set-notation prompts
(`A ∩ B`, `(A ∪ B)′`, prime/square conditions) under time pressure.

**Cross-ref: partial overlap with `given-that`**, which uses Venn diagrams but for *conditional
probability*, not set notation. Formal set notation and complements are a distinct KS3/GCSE skill
and aren't covered elsewhere. Worth doing, but coordinate with given-that so they don't look like
the same game.

## B5. Inequality Turf War — GCSE / A-Level
Territory capture on a coordinate grid: graph linear inequalities (`y ≥ 2x − 1`, `x + y < 6`) to
shade and claim regions against an AI opponent.

**Cross-ref: genuine gap — there is no inequalities game in the roster at all.** Shading regions
is a standard exam skill that's hard to practise on paper and suits an interactive grid well.
`coordinate-geometry-dash` has canvas plotting that might be reusable. **Second-strongest
candidate.**

## B6. Tree Diagram Detective — GCSE / Core Maths
Mystery scenarios using conditional probability without replacement; complete probability tree
branches to find compound outcomes.

**Cross-ref: overlaps `given-that`** (conditional probability with two-way tables, Venn diagrams
**and frequency trees**) and `screening-room` (false positives, base rates). Without-replacement
specifically may be thin in the existing banks — check before treating this as new. Possibly
better as an extra mode inside `given-that`.

## B7. Tangent Racer / Calculus Coaster — A-Level / Level 4
Keep a rollercoaster cart on track by differentiating `y = f(x)`, computing dy/dx at critical
points and placing matching tangent guide rails.

**Cross-ref: overlaps two games** — `differentiation-duel` (45+53 questions) for the calculus and
`gradient-hunter` (canvas graphs, click-to-find-gradient, Core Maths S3.11) for the visual
gradient work. The rollercoaster framing is fun but the underlying skill is well covered. Lowest
priority in Part B unless it's pitched as pure presentation.

## B8. Capture-Recapture Safari — GCSE / Core Maths
Field ecology simulator: tag a sample, release, resample, and set up `M/N = m/n` to estimate
population.

**Cross-ref: genuine gap — not in the roster.** On GCSE Higher and relevant to Core Maths
sampling. Self-contained, small bank, no new engine needed. **Good low-cost win.**

## B9. Standard Form Asteroids — KS3 / GCSE
Arcade shooter where asteroids are labelled with scientific notation; set blaster power to match
or order values (`3.2 × 10⁴` ↔ `32,000`).

**Cross-ref: duplicates `standard-form-blitz`**, which already does convert / multiply / divide
across 50+50 questions. This is a **reskin of an existing game, not a new one**. If the arcade
framing is wanted, apply it to standard-form-blitz rather than adding a 94th game competing for
the same slot.

## B10. Proof Chain: Domino Logic — GCSE Higher / A-Level
Drag and connect premise tiles ("alternate segment theorem", "base angles of isosceles triangle
are equal", "RHS congruence") in strict logical order to complete Q.E.D. objectives.

**Cross-ref: overlaps `proof-builder`** (A-Level/Further, three modes). The **GCSE Higher
geometric-proof** angle is arguably new — proof-builder is pitched at A-Level and above, and
congruence/circle-theorem proof chains are a distinct GCSE skill. Consider as a new mode or level
tier inside proof-builder rather than a separate game.

---

## Suggested sequencing if this gets picked up

1. **A9 (Trig Wars help section)** — not the enhancement as proposed, the *prerequisite* to it.
   Most-played game, 8% completion, no help. Highest-impact fix on the site.
2. **A2 (Graph Transformer ghost trails)** — worst accuracy on the site, and the fix matches the
   failure mode.
3. **B2 (Bounds & Safe Cracker)** and **B5 (Inequality Turf War)** — the two clearest curriculum
   gaps in a 93-game catalogue.
4. **B8 (Capture-Recapture Safari)** — cheapest genuine gap to close.
5. Everything else — revisit after the September data is in.

Skip or fold in: **B9** (duplicate), **B7** (covered twice over), **B6** and **B10** (better as
modes inside existing games).
