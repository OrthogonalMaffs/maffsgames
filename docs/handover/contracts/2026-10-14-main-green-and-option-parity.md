# Contract MAIN-GREEN-AND-OPTION-PARITY (cloud lane; 14 Oct 2026, Jon), verbatim

The home lane is unavailable until this evening. This contract needs nothing
from it, unless a STOP IF hands work over.

TASK: (1) Bring main back to green by fixing verify-probability-paradox.py's
run time, then merge #374. (2) Rewrite the options in the games where the key
gives itself away by its length, so every option has the same form and
comparable length, with the working moved to an explanation shown after the
answer.

ROOT CAUSE:
(1) Main's run 1042 (from #373) is red in one job, "CI timings and pack (main
    only)". Content verifiers 20 is estimated at 222 s, 82% of its 270 s
    budget (limit 80%). verify-probability-paradox.py takes 203 s of that.
    Suspected but unmeasured cause: the fixed-simulation path added in #371.
    #374 (boolean-blitz probe-fault note, Gate green, head ccdf64a) is waiting
    unmerged because main is red.
(2) Measured 14 Oct over the extracted banks: the share of items where the key
    is strictly the longest option, against chance, is:
    - spot-the-muppet 100% (25%), wrong-on-the-internet 100% (33%),
      stat-attack interpretations 100% (25%), terrible-advice 98% (25%);
    - gradient-hunter 89% (30%), better-value 81%, growth-and-decay 78%,
      graph-sketcher 65%, component-crusher 58%, expectation-station 51%
      (each 25%);
    - glorious-gantt 55% (unlisted; out of scope).
    The key carries its working ("Beverley is wrong — 30% of 80 means multiply
    by 0.30: 0.30 × 80 = 24") and the distractors do not ("Beverley is correct
    — 2.67"), so a student can answer without doing any maths.
    spot-the-muppet and terrible-advice have no explanation field: after a
    wrong answer they only highlight the key, so the key is the only place
    their working appears.

CLASS CHECK:
(1) If #371 introduced an inefficiency (for example, simulating where a closed
    form or a single seeded run would do), the bug is local: fix the
    inefficiency, not the budget. Only if the run time is genuine work, use the
    repo's documented remedy (--part / --shard), as other slow verifiers do.
(2) Is a class: the same option-form fault in 10 listed games. The shared
    layer, a CI check (check-option-parity.py) and canon SR-34, is the home
    lane's tonight. This lane does the per-game rewrites under the rule below.
    spot-the-muppet, terrible-advice and wrong-on-the-internet share
    hand-copied items: fix each shared item in every copy, the same way.

EXACT CHANGE:
Part 1: main green
1. Time verify-probability-paradox.py at main and at the commit before #371.
   Record both times.
2. If #371 caused the increase, make that path efficient without dropping any
   check. Otherwise, split the verifier with --part.
3. Its own PR. Merge on a green Gate: this is the red-main fix, so the
   red-main rule does not block it. Watch main's full run.
4. When main is green: merge #374, then run scripts/end-task.py for
   claude/boolean-blitz-recheck. If gh is unavailable, leave it, record it in
   the handover, and delete nothing by hand.

Part 2: option parity (start only when main is green)
5. The rule (SR-34, Jon, 14 Oct 2026): every option in a multiple-choice item
   has the same form and comparable length. The key never carries working the
   distractors lack; working belongs in the explanation shown after the
   answer.
6. The measure: an uncommitted scratch script.
   - Run extract-banks.py first.
   - Count every multiple-choice item with exactly one key, using displayed
     length with TeX commands and braces stripped.
   - A game with 10 or more such items fails if the key is strictly the longest
     on more than 40% of its items, or strictly the shortest on more than 40%.
   - Record each game's before and after rates in docs/handover/cloud.md.
7. Order, by audience, one PR per game:
   - spot-the-muppet, terrible-advice, wrong-on-the-internet, better-value,
     stat-attack;
   - then gradient-hunter, expectation-station;
   - then growth-and-decay, graph-sketcher, component-crusher.
8. Verdict-style games (spot-the-muppet, terrible-advice,
   wrong-on-the-internet):
   - Every option becomes a verdict plus a result, in one parallel form, for
     example "Beverley is wrong — it's 24" or "Beverley is wrong — it's 2.4".
   - spot-the-muppet and terrible-advice: add an explanation field to every
     item, holding the working removed from the key. Show it after the answer
     is marked, right or wrong, the way wrong-on-the-internet already shows
     its explanation.
9. Interpretation and conclusion options (all the others):
   - Prefer lengthening the distractors to full, parallel sentences, each
     stating one named misconception (SR-4), over cutting the key down.
   - Shorten the key only where it carries working, moving that working into
     the item's existing explanation.
10. Never change which option is correct, or what any option means
    mathematically. A distractor stays false; a key stays true.
11. Update each game's verifier wherever it pins option text. For the two games
    that gain the field, add a verifier rule that every item has an
    explanation.
12. Before each push: extract-banks.py, check-banks.py --ci, and the scratch
    measure. The game must pass both 40% limits.
13. In docs/handover/cloud.md, per game: the before and after rates, and three
    before-and-after examples, marked as your drafting under SR-34, which Jon
    may overrule.

DO NOT TOUCH:
- ci-groups.py, the workflow, schools/assets/, canon, and any shared module in
  scripts/ (home lane).
- Do not create check-option-parity.py or any KNOWN list (home lane, tonight).
- Which option is the key, any item's maths, any stem.
- glorious-gantt. Games not in the list.
- The verifier budgets.

SUCCESS CONDITION:
- Part 1: main's full run is green, including "CI timings and pack". #374 is
  merged. Both timings are recorded.
- Part 2: every listed game passes both 40% limits on the scratch measure.
  Every spot-the-muppet and terrible-advice item shows its working after the
  answer. Main is green after each merge.
- docs/handover/cloud.md lists, for the home lane tonight, each game's final
  rates and any game still failing, so check-option-parity.py can start with
  KNOWN holding only those.

STOP IF:
- Part 1 needs ci-groups.py or the workflow changed: record it for the home
  lane tonight, and do not start part 2 while main is red.
- Main goes red for any other reason.
- A parallel form would make a distractor true or a key false.
- A game cannot show an explanation without changing shared code
  (schools/assets/).
- An item cannot reach parity without changing its stem or its key: list it
  for Jon and carry on with the rest.
