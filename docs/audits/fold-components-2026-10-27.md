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
