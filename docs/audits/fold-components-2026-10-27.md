# Fold components: the three groups, before and after (contract FOLD-COMPONENTS, 27 Oct 2026)

Jon's contract of 26-27 Oct 2026 (`docs/handover/contracts/2026-10-27-fold-components.md`), run by the cloud lane under a lane
exception for this contract only. The groups are those of `docs/audits/below-fold-2026-10-26.md` as corrected by #560. Every
number is from `scripts/measure-phone-fit.py` (the first question at the default level; one sample, as the gate).

## Item 1: the games in the three groups

Resit suite first, then the lowest tier served (roster). **On theme.css**: whether the page loads `schools/assets/theme.css`
today. 18 of the 19 do not, so a game adopts the shared components through their own stylesheet, never the whole theme
(adopting theme.css would change a game's fonts and page colours: a STOP IF). **Fails** is each game's entry on the lists in
`scripts/phone-fit-state.json` after PR 1 (phone sizes by width; laptop `1366` is 1366 x 768, `1280` is 1280 x 720, by control).

### Group A: reference panel (8)

| # | Game | Lowest tier | Resit suite | On theme.css | Fails: normal | Aa | Laptop | Sideways (normal; Aa) |
|---|---|---|---|---|---|---|---|---|
| 1 | `constructions-lab` | KS3 |  | no | 320, 375 | 320, 375, 390 | 1366 option, 1280 option | –; – |
| 2 | `index-laws` | GCSE |  | no | 320, 375, 390 | 320, 375, 390 | 1366 next, 1280 next | –; – |
| 3 | `trig-worms` | GCSE |  | no | 320, 375 | 320, 375 | 1366 option, 1280 option | –; – |
| 4 | `tax-theft` | Core |  | no | 320, 375, 390 | 320, 375, 390 | 1366 option, 1280 option | 320, 375, 390; 320, 375, 390 |
| 5 | `differentiation-duel` | A-Level |  | no | 320, 375, 390 | 320, 375, 390 | 1366 next, 1366 option, 1280 next, 1280 option | –; 320, 375, 390 |
| 6 | `log-laws` | A-Level |  | no | 320, 375, 390 | 320, 375, 390 | 1366 next, 1280 next, 1280 option | –; – |
| 7 | `integration-duel` | A-Level |  | no | 320, 375, 390 | 320, 375, 390 | 1366 next, 1280 next, 1280 option | –; 320 |
| 8 | `suvat` | A-Level |  | no | 320, 375 | 320, 375, 390 | 1280 option | –; – |

### Group F: four full-width options (2)

| # | Game | Lowest tier | Resit suite | On theme.css | Fails: normal | Aa | Laptop | Sideways (normal; Aa) |
|---|---|---|---|---|---|---|---|---|
| 1 | `partial-fractions-duel` | A-Level |  | no | 320, 375 | 375 | – | –; – |
| 2 | `boolean-blitz` | L4 |  | no | 320 | – | 1280 next | –; – |

### Group D: figure above the options (9)

| # | Game | Lowest tier | Resit suite | On theme.css | Fails: normal | Aa | Laptop | Sideways (normal; Aa) |
|---|---|---|---|---|---|---|---|---|
| 1 | `percentage-flip` | Year 6 | yes | no | 320, 375 | 320, 375 | 1366 next, 1280 next, 1280 option | –; – |
| 2 | `prime-factorisation` | Year 6 | yes | no | 320 | 375 | – | –; – |
| 3 | `correlation-or-coincidence` | GCSE | yes | yes | – | 375 | – | –; – |
| 4 | `higher-power` | KS3 |  | no | 320 | 320, 375 | – | –; – |
| 5 | `circle-theorem-spotter` | GCSE |  | no | 320, 375 | 320, 375 | 1366 next, 1280 next, 1280 option | –; – |
| 6 | `modular-battle` | GCSE |  | no | 320 | 320 | – | –; – |
| 7 | `coordinate-geometry-dash` | GCSE |  | no | 320 | 375 | 1366 next, 1366 option, 1280 next, 1280 option | –; – |
| 8 | `curling-friction` | A-Level |  | no | 320 | 320, 375 | 1366 next, 1280 next | –; – |
| 9 | `complex-converter` | Further |  | no | 320, 375, 390 | 320, 375, 390 | – | –; – |

**Work order:** one PR per group, reference panels (A), then four full-width options (F), then figures (D); resit-suite games
first within a group. Group A has none; group D has three (`percentage-flip`, `prime-factorisation`, `correlation-or-coincidence`).

## PR 1: the gate (item 4)

`measure-phone-fit.py` gained three checks, each with its own list and selftest plants:

- **Laptop and projector sizes (R2):** `--laptop` judges 1366 x 768 and 1280 x 720 in normal mode: the last answer option and
  Next after a wrong answer both end above the fold. Seeded from a fresh run that matches the 26 Oct laptop run
  (`docs/audits/phone-fit-runs-2026-10-26/laptop.json`) exactly, plus the three canvas games it can now measure: 37 games.
- **Sideways scroll:** any measured screen (the asking screen, or after a wrong answer) that scrolls sideways fails, in every
  mode, against the `sideways` list: 9 games in normal mode, 26 in Aa, none on a laptop. The games outside the three groups stay
  on the list (Jon, 27 Oct 2026: listed, not fixed in this contract).
- **Canvas questions:** with no option group, input or submit, the canvas's own box and the buttons that start at or below its
  top are the answer area (one rule in the shared page script, no per-game code). `bearing-blitz`, `four-quadrant-explorer`,
  `gradient-hunter` and `shape-shifter` leave the unmeasurable list (14 -> 7 -> 3: `glorious-gantt`, `just-pythag-it-bruv`,
  `spot-the-error`); `bearing-blitz` (normal 320) and `shape-shifter` (normal 320 and 375, Aa 375) join known failures.

## PR 2: group A, reference panels

**The components (canon §7.5.7):** `schools/assets/fold.css` holds the reference card (`.maffs-ref`, moved from `theme.css`
unchanged in behaviour, with neutral fallbacks for a page without the theme's tokens), options two to a row (`.maffs-options`,
decided by `schools/assets/fold.js` by measuring the rendered options, ruling R3) and the compact header
(`.maffs-compact-header`, `.maffs-compact-bar`, phones only). `theme.css` imports it; the seven games below link it alone,
after their own `<style>`. Each panel's collapsed label is its own existing title, so no wording changed; Log Laws' title
keeps "log means log₁₀" on its play screen (SR-17; `verify-log-laws.py` now reads the collapsed card's label). After a wrong
answer the card opens where it fits: screens at least 601 px wide and at least the measured height (Next with the card open,
+40 px footer, +60 px for a longer explanation than the one measured): index-laws 860, differentiation-duel 960,
integration-duel 890, log-laws 900. Measured on one question per game (the gate's sample), not every item.

Each game claimed on `cloud-remaining` in a commit of its own before it was edited; all released in this PR.

| Game | Lowest tier | Components | Before (normal; Aa; laptop) | After (normal; Aa; laptop) | Sideways after (normal; Aa) |
|---|---|---|---|---|---|
| `index-laws` | GCSE | card, two-up | 320, 375, 390; 320, 375, 390; 1366 next, 1280 next | passes everywhere | –; – |
| `trig-worms` | GCSE | card, compact header | 320, 375; 320, 375; 1366 option, 1280 option | –; –; 1366 option (729 / 728), 1280 option (729 / 680) | –; – |
| `tax-theft` | Core | card | 320, 375, 390; 320, 375, 390; 1366 option, 1280 option | passes the gate everywhere | 320, 375, 390; 320, 375, 390 |
| `differentiation-duel` | A-Level | card, two-up, compact header | 320, 375, 390; 320, 375, 390; all four | passes everywhere | –; 320 (was 320, 375, 390) |
| `log-laws` | A-Level | card, two-up | 320, 375, 390; 320, 375, 390; 1366 next, 1280 next, 1280 option | passes everywhere | –; – |
| `integration-duel` | A-Level | card, two-up, compact header | 320, 375, 390; 320, 375, 390; 1366 next, 1280 next, 1280 option | passes everywhere | –; – (was Aa 320) |
| `suvat` | A-Level | card, compact header | 320, 375; 320, 375, 390; 1280 option | 320 (588 / 528); 320, 375; – | –; – |
| `constructions-lab` | KS3 | none (below) | 320, 375; 320, 375, 390; 1366 option, 1280 option | unchanged | –; – |

**Known failures:** normal 48 -> 42, Aa 48 -> 42, laptop 37 -> 31. Six games come off the known-failures lists in every mode
(index-laws, differentiation-duel, integration-duel, log-laws, tax-theft, and trig-worms on phones). Sideways, Aa: 26 -> 25.

**Not fixed by the group's component (3; the STOP IF threshold is more than 3), with the measured reason:**
- `constructions-lab`: its panel is the task itself, not a reference: the construction's name and the steps to follow, above
  a 700 x 600 drawing canvas whose tool buttons are the answer controls. Collapsing it hides the question, or needs a new label
  the game has never shown. Not claimed, not edited.
- `trig-worms` (laptop only): with the card collapsed and the compact header it fits every phone size; at 1366 x 768 and
  1280 x 720 its canvas (318 px tall at desktop width) keeps the last option 1 px and 49 px below the fold. The cause is a
  figure, group D's: the figure component is the fix to try in the group D PR.
- `suvat` (normal 320, Aa 320 and 375): with the equations panel collapsed and the compact header, what remains above the
  options is the question itself, the scenario box with its known-value chips (about 290 px).
- **Sideways (not this group's cause):** `tax-theft` scrolls sideways on every phone in both modes because its layout grid's
  track and its £ answer row are wider than a phone, not because of the panel; `differentiation-duel` in Aa at 320 because
  its title, level badge and Aa toggle do not fit on one line (canon §7.6.1 keeps the title and toggle on one line). Both
  stay on the sideways list.
- **Next after a wrong answer at 320 x 568** (reported, not gated on a phone) is still below the fold in the four duel games
  (index-laws 655, differentiation-duel 625, integration-duel 610, log-laws 631, against 528).
- Log Laws at 320 x 568: the collapsed card, which carries "log means log₁₀", sits just below the fold on the asking screen;
  before, the open panel was at the top.

## PR 3: group F, four full-width options

Both games already set their options two to a row on desktop and forced one to a row on phones (500 px and narrower). Each
now carries `.maffs-options` and links `fold.css` and `fold.js`, so on a phone the options go two to a row only when every
option fits on one line at half width with 44 px tap targets (R3), decided by measuring them. Each claimed on `cloud-remaining`
in its own commit first; both released in this PR.

| Game | Lowest tier | Before (normal; Aa; laptop) | After (normal; Aa; laptop) |
|---|---|---|---|
| `partial-fractions-duel` | A-Level | 320, 375; 375; – | passes everywhere |
| `boolean-blitz` | L4 | 320; –; 1280 next | –; –; 1280 next (Next 720 / 680) |

**Known failures:** normal 42 -> 40, Aa 42 -> 41, laptop unchanged at 31. **Not fixed by the group's component (1):**
`boolean-blitz` at 1280 x 720, Next 40 px below the fold after a wrong answer: on a laptop its options are already two to a row,
so the overflow is the header, question card, options and feedback together, not four stacked options. In Aa its Next is below
the fold on a phone (reported, not gated).

## PR 4: group D, figures above the options; the label floor

**The label floor (Jon, 27 Oct 2026, with contract SHARD's rulings):** "12 px minimum for any text in a figure, in every mode, Aa
included. A figure that can't fit with 12 px labels goes on the known-failures list with its reason; it isn't shrunk further.
Add it as a check in the gate." `measure-phone-fit.py` now measures the smallest text in a figure as drawn, on the asking
screen and after a wrong answer: SVG text by its font size times its on-screen scale, canvas text by recording every
`fillText` / `strokeText` (font size times the context's scale, times the bitmap's scale on screen, the smaller of width and
height, so a canvas held to a lower height is measured at the size it is drawn), and `.maffs-figure` blocks by computed size.
Under 12 px is a gate in every mode against its own list, `small-labels`, seeded from fresh runs of all 103 roster games
(KaTeX served locally): **normal 8, Aa 8, laptop 4.** The same eight games on phones in both modes (SVG and canvas text does
not take the Aa font): `circle-theorem-spotter` (320 only, 10.3 px), `complex-converter` (6.4 / 7.7 / 8.1 px at 320 / 375 /
390), `coordinate-geometry-dash` (4.3 / 5.1 / 5.3), `correlation-or-coincidence` (6.6 / 9.4 / 11.9), `given-that` (5.7 / 6.9
/ 7.3), `growth-and-decay` (8.5 / 10 / 10), `normal-navigator` (4.6 / 5.6 / 5.8), `trig-worms` (5.8 / 6.9 / 7.2); on laptops
`complex-converter` 9.0, `coordinate-geometry-dash` 10.9, `given-that` 11.0, `growth-and-decay` 10.0. Not seen: text a game
draws on a canvas outside the page and copies in (`drawImage`), and a canvas game's text before the first question.

**The components:** `.maffs-figure` (screens 900 px tall or less: the game's `--maffs-figure-max`; a canvas or image keeps its
proportions with `object-fit: contain`; a block's contents keep their size), `.maffs-figure-card` (a padded card figure's
padding drops to 10 px on screens 600 px tall or less) and the compact bar's pairs wrap rather than run off the screen. Each
game claimed on `cloud-remaining` in its own commit first; all released in this PR.

| Game | Components | Before (normal; Aa; laptop) | After (normal; Aa; laptop) | Smallest figure text after |
|---|---|---|---|---|
| `percentage-flip` | figure (the card, 22vh), compact header and bar | 320, 375; 320, 375; 1366 next, 1280 next, 1280 option | passes everywhere | 12 px ("TAP TO REVEAL", raised from 10) |
| `prime-factorisation` | figure card, compact bar | 320; 375; – | passes everywhere | none |
| `correlation-or-coincidence` | its own graph caps moved onto the figure variable, unchanged; compact bar | –; 375; – | –; 375 (661 / 627); – | 6.6 / 9.4 / 11.9 px (listed) |
| `modular-battle` | compact bar | 320; 320; – | –; 320 (options start 572 / 528); – | none |
| `curling-friction` | figure (the rink, 64 px), compact bar | 320; 320, 375; 1366 next, 1280 next | 320 (541 / 528); –; 1366 next (729 / 728), 1280 next (729 / 680) | none ("SWEEP!" raised to 12 px) |
| `trig-worms` (group A's laptop remainder) | figure (the battlefield, 265 px) | –; –; 1366 option, 1280 option | –; –; – (phones: small labels, listed) | laptop at 12 px or more |
| `coordinate-geometry-dash` | none | 320; 375; all four | unchanged | 4.3-10.9 px (listed) |
| `circle-theorem-spotter` | none | 320, 375; 320, 375; 1366 next, 1280 next, 1280 option | unchanged | 10.3 px at 320 (listed) |
| `complex-converter` | none | 320, 375, 390 in both modes; – | unchanged | 6.4-9.0 px (listed) |
| `higher-power` | none | 320; 320, 375; – | unchanged | none |

**Known failures:** normal 40 -> 37, Aa 41 -> 38, laptop 31 -> 29 (sideways unchanged: 9, 25, 0).

**Left on the lists, with the measured reason (Jon's rulings of 27 Oct: the label floor, and his ruling 4):**
- `correlation-or-coincidence` (Aa 375), `coordinate-geometry-dash` (everywhere): their labels are already under 12 px at
  full size, so the floor forbids any shrink. PR 4's work-in-progress had added a 130 px Aa cap to Correlation's graph; it is
  removed.
- `circle-theorem-spotter`: at 320 its labels are 10.3 px (Jon's ruling 4); at 375 they are 12.7 px, so the diagram can
  shrink by at most 5.5% (about 18 px) and it needs 67; on a laptop (14.7 px, about 61 px of room) Next needs 127.
- `complex-converter` (Jon's ruling 4): 329 px over at 320 by estimate, and its Argand labels are 6.4-9.0 px.
- `higher-power` (Jon's ruling 4): flip cards whose faces are absolutely placed in a `min-height` box, which `max-height`
  cannot cap. Its values spilling out of the cards on phones is a separate bug (cloud queue item 4).
- `curling-friction` at 320 (13 px) and Next on a laptop (1 px at 1366, 49 at 1280): the rink is at the house's height, the
  smallest it goes without resizing what is in it; the rest is the question card.
- `modular-battle` in Aa at 320: options start 44 px below the fold; the dots are not shrunk (canon §7.6.1: every dot drawn).

**Found, outside the groups:** `take-a-walk`'s last option at 320 x 568 measured 486, 511 and 537 px against a 528 px fold in
four identical runs (normal mode): the driver flips between pass and fail on it. Either its layout settles after the driver
measures, or it varies between loads; not investigated here.
