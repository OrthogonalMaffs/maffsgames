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
