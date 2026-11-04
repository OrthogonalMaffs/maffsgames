PRE-STEP (Jon, 4 Nov): docs/handover/home.md is 20,427 of 20,480 bytes. Before anything else, move these finished
queue entries, word for word, into docs/history/ (the home lane's archive, under a dated heading "Queue DONE items
moved 4 Nov"), leaving one pointer line in the queue: CALC-DOCK-WIDE (#653), UPDATES-NOVEMBER (#651),
NEW-AND-UPDATED (#648), TODO-TRIM (#645), PIES-SIGNOFF-AND-PRIMARY-FF (#644), LOOK-STAGE (#638), RULEBOOK (#635).
Confirm each merged on main first. Keep the cross-lane line about cloud owning Gate files. The size check must pass
without its warning, now and after this contract's own entry.

CONTRACT: FRACTION-WHOLE
Tier: Shared · Lane: home · Implementer: Codex (WSL)

START
git -C ~/maffsgames pull --ff-only, then a worktree codex/fraction-whole from origin/main.

TASK
Give the shared stacked fraction input an optional whole-number box for mixed numbers, and move The 6 P's onto it.

ROOT CAUSE
FRACTION-STACK (#640) made typed fractions use MaffsFractionInput (canon §7.6.1: every fraction stacked), but the shared
input has no whole-number part, so the-6-ps (mixed-number answers) and how-many-parts (Stage 6) still build their own
boxes and sit on scripts/fraction-input-warn.json.

CLASS CHECK
Yes: shared component missing a capability two pages need. Fix in schools/assets/fraction-input.js; pages then use it.

EXACT CHANGE
1. fraction-input.js: mount(host, { whole: true }) adds a whole-number box to the left of the stacked fraction, same
   size rules (including the 700 px compact rule); raw() returns "2 3/4" form as MaffsAnswer.fractionForm reads it;
   value() includes `whole`. Without the option, behaviour is byte-for-byte unchanged (possibly-maybe, pies).
   Selftest/plants for the new mode.
2. the-6-ps/index.html: case 'fraction' uses MaffsFractionInput (whole: true where the answer has a whole part);
   remove its own boxes; marking rules unchanged. Remove the-6-ps from scripts/fraction-input-warn.json.
   The 6 P's verifier passes; phone fit at 320x568, 360x640, 375x667 recorded.
3. Cloud handover Queue line: how-many-parts to move next (cloud lane, HOW-MANY-PARTS-FRACTION).

DO NOT TOUCH
Marking rules; the 6 P's questions; any game folder; Gate files.

SUCCESS CONDITION
Both modes tested; the-6-ps off the warn list; possibly-maybe and pies verifiers unchanged and green; check-changed.py
green; Shared review; stop at Gate green for Jon's "merge"; Record line.

STOP IF
A 6 P's answer needs a form the input cannot represent (list them); The 6 P's phone rule fails at any size; the
pre-step cannot bring home.md under its limit without moving a live item.

## Pre-step extension — Jon, 4 Nov

Approved (Jon, 4 Nov), extending the pre-step: also move, word for word, every dated entry in docs/handover/home.md
whose work has merged on main (CALC-DOCK-WIDE #653 first, then any other finished entry, oldest first), into the
same dated archive heading. Confirm each merged before moving it. Never move a live or unmerged entry. Aim for at
least 3 KB below the warning threshold so FRACTION-WHOLE and the next contracts' entries fit. Then continue with
FRACTION-WHOLE. Thank you.
