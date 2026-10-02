# Audit: how the site loads OpenDyslexic, and the fix

Contract: *Make Aa mode actually load the OpenDyslexic font*, 28 September 2026. Inventory taken against `main` at `8b193c8` before any edit; the fix is on branch `claude/opendyslexic-self-host`.

## What was wrong

92 game pages declared the Aa font with two `@font-face` rules pointing at jsDelivr's npm mirror (host `cdn.jsdelivr.net`, path `/npm/` + `opendyslexic@latest/fonts/…`). No npm package of that name exists, and jsDelivr answers "Failed to fetch version info for opendyslexic" (confirmed by Jon). So the font never loaded, and Aa mode has been applying its spacing over a fallback sans-serif, site-wide and silently. Nothing checked that a declared font actually arrives.

## Inventory (before the edit)

- **650 mentions of OpenDyslexic in 95 files**: 94 game pages and `privacy/index.html`. 648 are in CSS and 2 are visible text. None is in JavaScript, a `<link>` or an `@import`.
- **One loading pattern, in 92 files:** the Regular (400) and Bold (700) `@font-face` rules inside the page's `<style>`, both on the dead mirror, `format('opentype')`. It comes in three layouts:
  - **A. Minified, one rule per line (49):** `52dle`, `better-value`, `chart-interrogator`, `complex-converter`, `constructions-lab`, `core-maths-paper1`, `core-maths-paper2a`, `core-maths-paper2b`, `core-maths-paper2c`, `correlation-or-coincidence`, `decimal-detective`, `equation-builder`, `equatle`, `estimation-engine`, `expectation-station`, `expected-damage`, `factor-theorem`, `fermi-lab`, `formula-plug-in`, `four-quadrant-explorer`, `given-that`, `glorious-gantt`, `gradient-hunter`, `graph-sketcher`, `graph-transformer`, `growth-and-decay`, `higher-power`, `like-terms-collector`, `maths-court`, `negative-number-line`, `new-shapes`, `prime-or-composite`, `prisoners-dilemma`, `probability-pioneer`, `regression-rumble`, `screening-room`, `seven-bridges`, `shape-shifter`, `spot-the-error`, `spot-the-muppet`, `standard-form-blitz`, `stat-attack`, `tax-theft`, `terrible-advice`, `test-the-claim`, `think-of-a-number`, `truth-buster`, `word-problem-decoder`, `wrong-on-the-internet`
  - **B. Minified, both rules on one line shared with the Aa rules (33):** `angle-ace`, `bearing-blitz`, `binomial-blaster`, `characteristic-quest`, `circle-theorem-spotter`, `component-crusher`, `coordinate-geometry-dash`, `curling-friction`, `dimension-checker`, `eigenvalue-extractor`, `eigenvector-engine`, `estimation-golf`, `factor-race`, `force-resolver`, `formula-forge`, `formula-unlocked`, `fraction-equivalence`, `linear-equation-solver`, `matrix-crunch`, `modular-battle`, `moments-master`, `normal-navigator`, `partial-fractions-duel`, `percentage-flip`, `prime-factorisation`, `probability-paradox`, `proof-builder`, `scale-factor-scaling`, `simultaneous-solver`, `split-it`, `trig-wars`, `trig-worms`, `unit-converter`
  - **C. Spaced, one rule per line (10):** `differentiation-duel`, `index-laws`, `integration-duel`, `log-laws`, `proportion-blaster`, `quadratic-factoriser`, `sequence-solver`, `surd-simplifier`, `suvat`, `trig-identity-duel`
- **`font-family: 'OpenDyslexic'` with nothing loading it (2):** `boolean-blitz`, `truth-will-set-you-free` (class `accessible-mode`).
- **`privacy/index.html:186`:** text only, the stored Aa preference. It stays accurate.

| Aa toggle | OpenDyslexic reference | Files |
|---|---|---|
| yes | the dead `@font-face` pair | 91 games |
| yes | `font-family` only | 2: `boolean-blitz`, `truth-will-set-you-free` |
| **no** | the dead `@font-face` pair | 1: `complex-converter` (snag 5, its missing toggle) |
| yes | none; Aa uses **Outfit/Verdana**, not OpenDyslexic | the escape rooms (`escape-rooms/assets/engine.css:13`) and `the-perfect-prank` (its line 31) |

**The escape rooms and `the-perfect-prank` never used OpenDyslexic.** Their Aa mode keeps Outfit, falls back to Verdana, and adds spacing. By Jon's ruling this is recorded, not changed.

## Jon's rulings (28 Sep 2026)

1. **Size:** ship Regular, Bold and Italic as WOFF2, about 320 KB. Italic is needed because 26 of the 95 game folders style text italic.
2. **Diff rule:** per file, the only changes allowed are the two `@font-face` rules removed (or the one line edited to remove them) and one `<link>` to `schools/assets/opendyslexic.css` added. Verify mechanically for all files and report any exception.
3. **Escape rooms:** drop them from the 5(b) sample; record that they use Outfit/Verdana; do not change them.
4. **`boolean-blitz` and `truth-will-set-you-free`:** include them, one added `<link>` each.

## The fix

- **`schools/assets/fonts/opendyslexic/`** holds `OpenDyslexic-Regular.woff2` (103,336 bytes), `OpenDyslexic-Bold.woff2` (108,068) and `OpenDyslexic-Italic.woff2` (107,968), 319,372 bytes in all, plus `OFL.txt`.
  - **Source:** `antijingoist/opendyslexic`, `compiled/`, commit `1824da5` (11 Aug 2025), copied byte for byte.
  - **Licence:** SIL Open Font License 1.1, with Reserved Font Name OpenDyslexic. The files are unmodified, so the name may stand.
- **`schools/assets/opendyslexic.css`** holds only the three `@font-face` declarations (400 normal, 700 normal, 400 italic), with relative URLs. It is the one place the font is declared.
- **94 game pages** now carry `<link rel="stylesheet" href="../../schools/assets/opendyslexic.css">` on the line before the `<style>` element that held the rules. That is the 92 with the dead rules plus the two `font-family`-only games; `complex-converter` is linked too, although it still has no toggle. Font-family stacks, Aa spacing rules, the toggle and `mfg_accessible` are untouched.

## Verification

- **Diff rule, checked mechanically on all 94 files against `main`: 0 exceptions.** The checker does not reuse the edit script's logic.
  - **59 files:** 1 `<link>` added and 2 rule lines removed.
  - **33 files:** 1 `<link>` added and 1 line edited. The edited line equals the original with exactly the two rules cut out.
  - **2 files:** 1 `<link>` added only.
- **The dead mirror URL** is no longer present in any file in the repository.
- **Tier 4 ledger:** `data/check-ledger.json`'s one B8 entry, test-the-claim's duplicate `crBoundaryUpper` key (todo §1.14), is identified by line number. Removing two font lines above that object moved it from line 527 to 526, so CI saw one "new" and one "stale" entry for the same unchanged defect. By Jon's ruling the entry is moved to `line526` in this commit, and identifying violations by content rather than line is queued as its own fix.
- **Checkers:** `check-site.py` tier 2 passes (138 files); `check-canonical-links.py` and `check-escape-rooms.py` pass.
- **Tier 1** runs in CI on this branch's push: the session's egress policy refuses `www.gstatic.com` and `cdn.jsdelivr.net`. The result is recorded on the pull request.
- **5(b), in Chromium through `serve-stubbed.py`, cache-busted, with Aa switched on by each game's own toggle.** Every font file requested returned 200, and `document.fonts.check('16px OpenDyslexic')` went from **false** to **true**. KaTeX was served from its npm package, test-only, because the CDN is blocked here. Firebase, gtag and Apps Script were blocked.

| Game | Row | Edit shape | Font files (all 200) | fonts.check |
|---|---|---|---|---|
| `index-laws` | dark | two lines removed (spaced) | Regular, Bold | false → true |
| `matrix-crunch` | dark | one line edited | Regular, Bold | false → true |
| `boolean-blitz` | dark | link added only | Regular, Bold, Italic | false → true |
| `spot-the-muppet` | light | two lines removed | Regular, Bold, Italic | false → true |
| `terrible-advice` | light | two lines removed | Regular, Bold, Italic | false → true |
| `like-terms-collector` | light | two lines removed | Regular, Bold | false → true |

Eight more games were tested the same way and all passed: `surd-simplifier`, `sequence-solver`, `truth-will-set-you-free`, `angle-ace`, `fraction-equivalence`, `prime-or-composite`, `factor-race` and `new-shapes`. Italic loads only where italic text is on screen, which is how a browser fetches font files.
`document.fonts.check` is sound on the games, returning false on the broken pages. On a page that never declares the font it returns true, which is why the escape rooms could not be tested this way.

## Found along the way — not fixed

1. **The Aa toggle is hidden until a game starts** in `spot-the-muppet`, `terrible-advice`, `like-terms-collector` and `new-shapes`. It sits in the in-game header, so a student cannot switch Aa on for the start screen.
2. **Answer buttons stay in Outfit in Aa mode** in `spot-the-muppet` and `terrible-advice` (seen in screenshots). The buttons set their own font, so `body.accessible` does not reach them. Other games not checked.
3. **Rows do not always match canon §7.5.1.** `prime-or-composite`, `fraction-equivalence`, `sequence-solver` and `angle-ace` serve KS3 or Year 6 but render on a dark background. The light sample therefore uses the roster's light-theme games.
4. **`complex-converter` still has no Aa toggle** (snag 5). It now links the stylesheet, so a toggle added later will work.
