# K() punctuation scan, 22 Oct 2026 (contract K-PUNCTUATION-SCAN, report only)

**Question.** Before #471, MaffsText could start a line with the punctuation straight after inline maths, or end one
on an orphaned opening bracket before it. The games that render KaTeX through their own code were never measured.
Do any of them show the same fault?

**Answer: 3 of the 38 games do, each in one place.**

| Game | Where | Width | Fault |
|---|---|---|---|
| expectation-station | Worked Example overlay | 320 px | "Prize (" ends a line, its maths on the next |
| growth-and-decay | Worked Example overlay | 390 px | "." starts a line after "when t = 0" |
| how-many-parts | wrong-answer line | 320 px | "(" ends a line, or ")" starts one |

None of them is a question stem or an option. 34 games show nothing, and 1 (glorious-gantt) could not be walked; it
calls KaTeX nowhere. With 3 affected, below the contract's 10, this stays a report rather than a migration contract.

**Every count here is from `scripts/scan-k-punctuation.py`** (not in CI): one full run on main at 0cf4494 with
the default settings (2 seeds per roster level, up to 40 questions a session), 27 minutes. `--selftest` plants the
fault (maths, then a separate full stop, in a column narrowed from 420 to 120 px). It is flagged at 62 of 301
widths, and at none once glued in one nowrap span as #471 does.

## Method

- **The set.** Every game page that calls `katex.renderToString` or `katex.render` itself and does not load
  `schools/assets/mathtext.js`: **38**, computed from the files on each run. The withdrawn holding page is left out.
  The home lane counted 36 on 21 Oct; the scan takes the set as the files define it today.
- **The walk.** Each game is played by `check-answer-lock.py`'s Driver: its seeded `Math.random`, its scaled
  timers and the page's own `maffs-lock-hint`. No game is changed or given an adapter. For every roster level and
  each seed, the scan measures:
  - the start screen;
  - the shared "Worked Example" overlay (`#methodOverlay`, opened as its button does, in the eight games that have
    one);
  - every question screen;
  - every screen after a mark. Answers rotate through the options, so both right and wrong feedback are seen.

  Each screen is measured at 320, 375 and 390 px.
- **The measure.** test-mathtext.py's line-box method, in Chromium with KaTeX's pinned fonts, never by reading
  markup. A punctuation mark counts as stranded when its line box is not on the same line as the maths it touches.
  The scan looks at:
  - the first text after each inline `.katex`, within the same block, starting with `. , ; : ! ? ) ]` or a
    closing quote;
  - the last text before it, ending with `(`, `[` or an opening quote.

  Because it walks the text nodes, the maths may sit inside a game's own wrapper span. A screen "with a candidate"
  has at least one such mark touching maths; only those screens can be affected.
- **The source.** The scan also lists every place where a KaTeX helper's output is joined straight to that
  punctuation (`k(x) + '.'`, `'(' + k(x)`, and the same inside template literals). In a game that builds its own
  maths HTML, these are the only shapes the fault can take, so a game with none cannot show it, whatever the walk
  reached. The one exception is prose a game parses itself, how-many-parts' `renderLine`, which only the walk can
  see.

## The three affected

1. **expectation-station, Worked Example overlay, 320 px.**
   - At `games/expectation-station/index.html:1513`, a table heading `'Prize ('+k('x')+')'` puts "(" before the
     maths and ")" after it as separate inline content. At 320 px the narrow column ends a line on "Prize (".
2. **growth-and-decay, Worked Example overlay, 390 px.**
   - "The 200 is the initial population when \(t = 0\)." The full stop starts the next line. It comes from one of
     the six method-block joins at :957-967, for example `k('t = 0')+'.'` at :958.
   - It breaks at 390 and not at 320 or 375: the fault depends on width, as #471 found for Paper 2C.
3. **how-many-parts, wrong-answer line, 320 px** (5 screens: 4 end on "(", 1 starts with ")").
   - "You added instead of taking away (\(\frac{17}{12}\)). The sign is −: take away." The brackets round the
     worked value are plain prose in the line `renderLine` (:1005) builds from text with maths between `§`
     marks.
   - No source join exists, because the brackets are data. This is the game's own redesign merged today (#479),
     still unlisted. The line is `H.example`'s template (name, then the worked value in brackets), rendered by
     `renderLine`.

## Every game

**Static** counts the joins in the source. **Screens** counts screens measured (each at three widths).
**Candidates** counts distinct screens with maths touching such punctuation. **Swap** answers the contract's
question: could its K() be swapped for `MaffsText.html` directly? The first five count columns are the script's.
The Swap column and its call-site counts come from reading each file (22 Oct), not from the script:
- **A:** one prose-with-delimiters function. No game is a clean A.
- **B:** a helper takes bare TeX, and callers concatenate prose round it.
- **C:** maths rendered into elements, with no prose.

| Game | Levels walked | Screens | Static | Candidates | Affected | Swap |
|---|---|---|---|---|---|---|
| better-value | gcse, core | 26 | 0 | 0 | 0 | No (B: method block, 4 sites) |
| binomial-blaster | alevel, alevel2 | 172 | 8 | 1 | 0 | No (C + B: rk 2; method block 15) |
| boolean-blitz | level4 | 162 | 0 | 0 | 0 | No (B, 5 sites; pure maths) |
| characteristic-quest | further, level4 | 128 | 0 | 1 | 0 | No (B + C: rkI 9, rk 1) |
| circle-theorem-spotter | gcse | 84 | 0 | 0 | 0 | Not needed (C, options only) |
| complex-converter | further, level4 | 20 | 0 | 0 | 0 | Not needed (pure maths into elements) |
| curling-friction | alevel, level4 | 168 | 0 | 0 | 0 | No (C + B: rkStr 3 with prose) |
| distinctly-average | ks3, gcse | 88 | 0 | 0 | 0 | Not needed (B, pure; MaffsText deliberately not used, :294) |
| eigenvalue-extractor | further, level4 | 128 | 0 | 0 | 0 | No (B + C: rkI 8, rk 1) |
| equation-builder | ks3, gcse, level4 | 252 | 0 | 0 | 0 | No (C-like: renderContent into tiles) |
| estimation-engine | gcse | 44 | 0 | 0 | 0 | No (C + B, plain-text fallbacks) |
| expectation-station | gcse, core, alevel | 492 | 3 | 5 | **1** (320) | No (C + B: method block 7) |
| expected-damage | ks3, gcse, core | 132 | 0 | 0 | 0 | Not needed (one pure formula) |
| force-resolver | alevel, level4 | 118 | 0 | 0 | 0 | Not needed (C) |
| formula-forge | gcse, alevel, level4 | 30 | 0 | 0 | 0 | No (C + B: rkStr "Hint 2:" + maths) |
| formula-plug-in | year6 | 50 | 0 | 0 | 0 | Not needed (C-like; steps pure TeX) |
| given-that | gcse, alevel, core, level4 | 268 | 0 | 0 | 0 | No (B: kx 9, feedback lines) |
| glorious-gantt | — | 8 | 0 | — | — | Not needed (KaTeX loaded, never called) |
| gradient-hunter | gcse, core, alevel | 258 | 2 | 1 | 0 | No (B: method block 7) |
| graph-sketcher | core, alevel, level4 | 52 | 7 | 1 | 0 | No (B: K 1; method block 16) |
| graph-transformer | gcse, alevel | 104 | 0 | 0 | 0 | Not needed (C) |
| growth-and-decay | core, alevel, level4 | 52 | 6 | 1 | **1** (390) | No (B: K 3; method block 15) |
| higher-power | ks3, gcse, alevel | 36 | 0 | 0 | 0 | Not needed (C) |
| how-many-parts | ks3, gcse | 184 | 0 | 62 | **5** (320) | Nearly: renderLine (:1005) is the one prose function, but its `§` lines would need converting to `\(...\)` first |
| index-laws | gcse, alevel | 104 | 0 | 0 | 0 | Not needed (B, pure maths) |
| integration-duel | alevel, level4 | 120 | 0 | 0 | 0 | Not needed (B, pure maths) |
| just-pythag-it-bruv | ks3 | 84 | 0 | 0 | 0 | No (B: `{tex, after}` line objects) |
| matrix-crunch | further, level4 | 168 | 0 | 0 | 0 | No (C + B: rkStr 1) |
| new-shapes | year6 | 50 | 0 | 0 | 0 | Not needed (C-like; steps pure TeX) |
| partial-fractions-duel | alevel, level4 | 168 | 0 | 0 | 0 | Not needed (C) |
| screening-room | gcse, alevel, core, level4 | 144 | 1 | 60 | 0 | No (B: kRender 2, one prose join at :897) |
| simultaneous-solver | gcse (alevel not walkable) | 46 | 18 | 20 | 0 | No (B, about 56 mathHtml sites; the biggest rewrite) |
| standard-form-blitz | gcse, alevel | 168 | 0 | 0 | 0 | Not needed (C) |
| stat-attack | gcse, core, level4 | 30 | 0 | 0 | 0 | No (B: K 4; method block 6) |
| surd-simplifier | gcse, alevel | 168 | 0 | 0 | 0 | Not needed (C) |
| suvat | level4 (its lock hint's level) | 36 | 0 | 15 | 0 | No (B: eqHTML; DOM text nodes round the maths at :949) |
| trig-identity-duel | gcse, alevel | 168 | 0 | 0 | 0 | Not needed (C; its `\csc` macro is not in MaffsText) |
| truth-will-set-you-free | level4 | 8 | 2 | 0 | 0 | No (B: K 4, prose round it) |

## Limits (what the walk did not reach)

- **glorious-gantt:** not playable by the driver at either level (no option group or input after Start). It never
  calls KaTeX, so it cannot show the fault.
- **simultaneous-solver at A-level:** not playable by the driver. Its Foundation walk reached 20 candidate screens
  and none broke; whether each of its 18 static joins (mathHtml, :962-1282) was among them is not recorded.
- **truth-will-set-you-free:** 8 screens; its 2 joins (`K(q.simplified) + ','` and `+ '.'`, :871 and :874) were
  not reached, so they are unmeasured.
- **The other method-block joins** (binomial-blaster, gradient-hunter, graph-sketcher) were all measured in the
  overlay at the three widths and held.
- Short sessions (better-value, complex-converter, formula-forge, stat-attack, 20 to 30 screens) end where the
  driver's session ends. All four have no static joins, so no shape exists there for the walk to have missed.

## What this means for the fix

- **No game's K() can be swapped for `MaffsText.html` directly.**
  - MaffsText takes prose with `\(...\)` maths. Every game here but one passes bare TeX to its helper and builds
    the prose round it.
  - The exception, how-many-parts, has one prose function, but it marks maths with `§`.
- **Pure-maths renders gain nothing from MaffsText.** These are the class C games and the "Not needed" rows: there
  is no prose for punctuation to break from.
- **The three faults are three local joins:**
  - two in the shared Worked Example method block, the IIFE `renderMethodRef` copied into eight games;
  - one in how-many-parts' line data.

  Applying the class check:
  - **The method block is the same code in eight games, so it is a class.** Its root fix is for that block to
    build its prose through MaffsText. That would cover all eight games and all of its sites, rather than
    patching the two that broke. By the classification above, that is about 70 helper calls in the seven games that use it.
  - **how-many-parts is local:** its own `§` format.
- **Which renderer would carry the method block** is a design decision for Jon: MaffsText for the overlay, or the
  block's own nowrap glue. So is whether to unlist anything. All three faults are in help or feedback, not in a
  stem or an option.
