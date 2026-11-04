# LOOK-REFRESH-1 (Jon, 4 Nov 2026), verbatim

```text
PRE-STEP (Jon, 4 Nov): in this contract's first commit, close out PACK-GENERATOR (merged #659, 713a1786): contract to
docs/history/contracts/, DONE in cloud.md's queue, correct its "Gate pending" line. Keep cloud.md's size check
passing without its warning (move DONE prose verbatim to the archive first if needed).

CONTRACT: LOOK-REFRESH-1
Tier: Small per game · Lane: cloud · Implementer: Claude Code (cloud)

TASK
Bring the three pixel-font games onto the shared adult theme, one game per PR, and produce a start-screen contact sheet
of every game not yet on it so Jon can name any others that still look childish.

ROOT CAUSE
Canon §7.5 (Jon, 2 Oct 2026): every game in one adult register. scripts/check-theme.py: 17 games MIGRATED, 91 NOT_YET.
Three still use the pixel font Press Start 2P with Nunito: prime-factorisation (Prime Sprint; Jon, 1 Nov: "still
childish"), percentage-flip and fraction-equivalence (Fraction Snap). Jon, 3 Nov: Percentage Flip gets the new font,
"plus any other games that still look childish need a refresh".

CLASS CHECK
Shared fix already exists: theme.css and check-theme.py's MIGRATED list. Migrate each game onto it (its existing
route); do not restyle by hand.

EXACT CHANGE
1. One PR each, in this order: prime-factorisation, percentage-flip, fraction-equivalence (standing rule: next game
   after each merge without asking). Each: load theme.css, data-theme by its roster levels, fonts from the theme
   (no Press Start 2P, no Nunito), hex colours to tokens, age-neutral static copy, no header emoji; move the game from
   NOT_YET to MIGRATED in check-theme.py (that list line only). Game behaviour unchanged; its verifier passes. Each PR
   adds its /updates/ line.
2. Research only, no code change: screenshots of the start screen of every remaining NOT_YET game at 375x667, one
   contact sheet image (or a few) saved under docs/audits/look-refresh-2026-11/ with a list naming each game and slug,
   plus check-theme.py --verbose's "age-specific wording" list (12 games). Put both in the PR or handover for Jon.

DO NOT TOUCH
Questions, answers, scoring; shared assets; the roster; check-theme.py beyond moving a slug between lists.

SUCCESS CONDITION
Three games MIGRATED and passing check-theme.py and their verifiers; contact sheet and wording list delivered; Gate
green per PR; merge on green (Small; Jon reviews by playing); Record lines; the work is committed and
docs/handover/cloud.md records the state.

STOP IF
A game's migration needs a change to theme.css; a game's layout breaks the phone rule after migration.
```

## Amendment 1 (Jon, 4 Nov 2026), verbatim

```text
Rulings on LOOK-REFRESH-1 (Jon, 4 Nov):
1. Hearts to three plain dots; sentence case for emphasis capitals: accepted.
2. scripts/phone-fit-state.json entries removed as the games now pass; images in docs/screenshots/look-refresh-2026-11/:
   accepted.
3. Change the two capital lines: Percentage Flip "WRONG — answer is N" becomes "Not quite: the answer is N", and Fraction
   Snap "CORRECT!" becomes "Correct!". Update each verifier's expected text in the same PR as the copy (a verifier
   checks behaviour, not shouting).
4. The colour-scheme finding (57 of 88 differ from the rule): no action in this contract; add one line under "For
   Project Claude to triage" in cloud.md.
Carry on with games 2 and 3 after #660 merges. Thank you.
```
