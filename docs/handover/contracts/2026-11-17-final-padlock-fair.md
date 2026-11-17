TOOL: Claude Code (home lane). SIZE: large (shared final-padlock rules, every pack rebuilt, versioned file names). Recommended: Opus, high effort.
MERGE TIMING: merge only after MERGE-PR-ROBUST (#806, cloud lane) has merged and main is green; if it is still open when your Gate is green, wait, rebase, then merge. One merge heading for main at a time.

TASK: Make every pack's final padlock doable by hand under time pressure and equally hard for every team: cap any product at 10,000, make all sets in a pack the same difficulty, give Heatwave an add-and-subtract padlock, and put a version number in every pack's file name; rebuild all ten packs.

ROOT CAUSE: final.py's friendly() (tools/pack-generator/final.py:38) refuses a product only when no factor is a multiple of 5 or ≤ 12, or when two factors are ≥ 100; it never limits the product, and choose()/add_finals() (build_pack.py:850, :903) pick each set's target independently (random.Random(seed-letter).choice). So padlocks escalated as rooms' answers grew (Hamster 45 × 480 = 21,600; PE Shed 74 × 320 = 23,680; Heatwave Set C 31 × 3375 + 168 = 104,793) and sets within one pack differ widely (Car Trap 3 × 10 = 30 beside 9 × 245 = 2,205). Jon, 17 Nov 06:13-06:18: "these final locks are getting out of hand ... an insane calculation to ask a team to do under time pressure with no calculator"; "10,000 should be the ceiling, and all final locks on a room should be of a similar difficulty"; "yes" (rebuild the packs on Tes too); Heatwave "might need to avoid a multiplication". Separately, every PDF is written as dist-packs/<slug>-pack.pdf whatever its version, and Jon now holds several versions of some packs (06:17: "append them with a version number so no confusion exists").

CLASS CHECK: Architectural. The padlock rules and the file name live in the shared generator (final.py, build_pack.py) used by every pack, and the fault appears in several packs; so the rules are general, checked for every room, never per-room flags. Heatwave's shape is a per-room config choice using the existing "plus-and-minus" shape (final.py SHAPES).

EXACT CHANGE:
First commit: HEATWAVE-PACK's close-out (AGENTS.md rule): #804 merged as 61b2f9a via merge-pr.py (second call; last line "main 61b2f9a: NO RUN FOUND", exit 1, as it looked before main's runs registered); check-site 44028365136 success, phone-fit-full 44028365052 success. Fill in its home handover entry and move its contract to docs/history/contracts/. Save this contract verbatim at docs/handover/contracts/2026-11-17-final-padlock-fair.md.
1. final.py: friendly() also refuses any product above PRODUCT_MAX = 10000 (Jon, 17 Nov 2026), keeping its two existing rules.
2. Uniform difficulty across a pack's sets (build_pack.py choose()/add_finals(), with final.py helpers): every set's final padlock must share one difficulty class:
   - shapes with a multiplication: the same digit signature for the product's two factors (e.g. every set 1-digit × 3-digit), and the largest product at most 3 × the smallest;
   - the "plus-and-minus" shape: the largest term has the same number of digits in every set.
   Selection: search, in an order fixed by the seed, for a class and a set of N draws (VALID, every lock's answers distinct, no miss printed as the answer) that each have a candidate target in that class within the product window; then each set's target is drawn from its in-class candidates by the existing seeded choice. BuildError naming the best class found and its count if none reaches N. Document the rule in final.py's docstring and README.md.
3. tools/pack-generator/rooms/heatwave-mutiny/config.json: "final_shape": "plus-and-minus".
4. Versioned file names: the PDF is written as dist-packs/<slug>-pack-v<pack_version>.pdf (pack_version from the room's config, already printed in the footer as "pack v1"). Every room whose sets or targets change under 1-3 gets pack_version bumped by 1 (state each). The print-on-page footer and the PDF title carry the same version.
5. scripts/test-pack-generator.py: plants that must be caught: a product of 10,001 accepted; a pack whose sets mix digit signatures; a pack whose largest product is more than 3 × its smallest; a plus-and-minus pack whose largest terms differ in digit count; a PDF name without its version. Controls: a product of exactly 10,000 passes; a uniform pack passes. Every existing plant still caught.
6. Rebuild all ten packs (car-trap, christmas-tree-fiasco, comic-caper, kiln-disaster, library-jam, prom-budget, roll-for-initiative, hamster-heist, pe-shed-rebellion, heatwave-mutiny) with --final for every room whose config already has wording_approved (Heatwave stays DRAFT: Jon has not approved its wording). Expected, from Project Claude's own simulation of these rules on main (seed order may pick another class; any class meeting the rules is fine): car-trap 1×2-digit (products 90-270), christmas-tree-fiasco 2×3-digit (1,320-3,960), comic-caper 1×2-digit (30-90), kiln-disaster 2×2-digit (420-1,260, 7 sets), library-jam 1×2-digit (56-168), prom-budget 1×2-digit (42-126), roll-for-initiative 2×2-digit (500-1,500), hamster-heist 2×3-digit (2,295-6,885), pe-shed-rebellion 2×2-digit (690-2,070); heatwave-mutiny cannot meet the rules with a multiplication and passes as plus-and-minus (every largest term 4 digits, e.g. 1728 + 31 − 154).
7. docs/todo.md: a row PACKS-V2-UPLOAD (Jon: replace the Tes files for car-trap, roll-for-initiative, prom-budget and the Core bundle with the new versions; list hamster-heist and pe-shed-rebellion). HEATWAVE-PACK-APPROVE stays open. Home handover entry.

Run only the checks this contract names and the Gate: test-pack-generator.py with self-test, check-escape-rooms.py, and the ten builds. No optional all-game local runs. Roll for Initiative may not build on this machine (its locks pages overflow locally, as in #801/#803); if so, say so and rely on CI.

DO NOT TOUCH: any room's room.js, variants, hints or wording; any config field other than final_shape (Heatwave only) and pack_version; the art; the live site's games; scripts/merge-pr.py and Gate files (MERGE-PR-ROBUST is working there); scripts/audit-answers.py; the cloud handover.

SUCCESS CONDITION:
- Every pack builds (Heatwave DRAFT, the others --final) with every final product ≤ 10,000, one difficulty class per pack, and largest/smallest product ≤ 3 (or same-digit largest terms for plus-and-minus).
- Each PDF is named <slug>-pack-v<N>.pdf and its footer says pack v<N>.
- test-pack-generator.py catches every planted fault and passes every control.
- PR merged on green via `python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600` (after #806); report its last line and exit status, main's check-site and phone-fit-full run IDs and results on the merge commit (look them up if it prints NO RUN FOUND), and for every pack: its new version, its class, and every set's final padlock expression and target. Home handover documented.

STOP IF:
- Any pack cannot meet the rules (report the pack and the best class found; do not loosen the ceiling or the ratio).
- Any lock answer, hint, wording or variant would have to change to meet them.
- Meeting the rules needs a new final shape (report; separate contract).
- merge-pr.py reports it cannot reach GitHub (a 5xx during the Gate wait may be retried once with the same script).

## Amendment 1 (Jon, 17 Nov 06:31, via session: the final padlock should be optional for the teacher)

Follow-up to FINAL-PADLOCK-FAIR (Jon, 17 Nov 06:31: the final padlock should be optional for the teacher): in the same PR, in the generator so every pack gets it: (1) under the teacher run sheet’s step 5 add “Short of time, or a class that will struggle? Skip the final padlock: tell teams before you start, and note the time when Lock 3 is ticked instead.”; (2) the score sheet’s finish column reads “Finished (final padlock, or Lock 3 if skipped)”; (3) each student set’s heading “The final padlock” becomes “The final padlock (if your teacher says so)”. These count as a change for every pack’s version bump. All existing wording checks apply to the new lines.
