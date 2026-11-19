# FRACTION-SNAP-REBUILD (Jon, 19 Nov 2026), verbatim, both parts

## Part 1 of 2

FRACTION-SNAP-REBUILD, part 1 of 2. Do not start until part 2 has arrived; it ends with "END OF CONTRACT".
LANE: cloud (this session). TIER: Medium. MODEL: Claude Code, Opus 5.5, high effort (a new bank, two generators, a verifier rewrite in Chromium).

TASK: Rebuild Fraction Snap (games/fraction-equivalence/index.html): a 46-pair Year 6 bank, different KS3 and GCSE generators, wrong pairs built from three misconceptions, a leaderboard per level, a best per level, fractions in KaTeX.

ROOT CAUSE: Checked on main 4df5235. Year 6 is a fixed bank of 20 (:212-235, with duplicate finding fraction-equivalence-v20-001), under the 40 minimum. KS3 and GCSE share one generator (:252-279) because gameLevel is 'all' for both (:238-239), so they are the same game. Every wrong pair is n1·m/(d1·m+1..3) (:272-276), which can be spotted without understanding equivalence. Answers are 60% YES (:261). One best key, fs_best (:379-380), serves all three levels. The fractions are drawn in CSS (:39-40, :168-176), not KaTeX (todo 1.48's open part).

CLASS CHECK: The bank, the generators and the wiring are local: no other game uses them. Two classes are touched. (1) A fixed best key in a multi-level game: eight other games use one fixed *_best key (modular-battle, percentage-flip, prime-factorisation, factor-race, index-laws, log-laws, quadratic-factoriser, trig-worms). Fix it here only, and add a todo row that checks each of them (report only). (2) CSS-drawn fractions: this game is 1.48's last open case, so the KaTeX change closes that row.

EXACT CHANGE:
1. First commit: close out #832 (TODO-135-CLOSE, 20b30ed): read main's runs on it from the API, record them in its cloud.md entry, and move its contract to docs/history/contracts/. Save this contract verbatim (both parts) as docs/handover/contracts/2026-11-19-fraction-snap-rebuild.md.
2. YEAR6_BANK becomes these 46 items, each {n1,d1,n2,d2,equiv,kind}. kind is yes, add (same number added to top and bottom), one (only one of top and bottom multiplied) or near (cross-products differ by 1). Denominators come only from {2,3,4,5,6,8,10,12}: update the bank's comment.
   yes (22): 1/2-2/4, 1/2-3/6, 1/2-5/10, 2/4-4/8, 3/6-6/12, 1/3-2/6, 1/3-4/12, 2/6-4/12, 2/3-4/6, 2/3-8/12, 4/6-8/12, 1/4-2/8, 1/4-3/12, 3/4-6/8, 3/4-9/12, 6/8-9/12, 1/5-2/10, 2/5-4/10, 3/5-6/10, 4/5-8/10, 1/6-2/12, 5/6-10/12
   add (8): 1/2-2/3, 1/3-2/4, 2/3-3/4, 1/4-2/5, 3/4-4/5, 1/2-3/4, 1/3-3/5, 1/4-3/6
   one (8): 1/2-1/4, 1/3-1/6, 3/4-3/8, 2/5-2/10, 1/4-2/4, 1/5-3/5, 1/6-1/12, 2/3-2/6
   near (8): 1/2-2/5, 1/3-3/8, 2/3-5/8, 3/5-5/8, 1/2-3/5, 2/5-3/8, 1/4-1/5, 2/5-5/12
   15 dealt per session, none twice (unchanged).
3. Generators. Half of all pairs are YES; the NOs are split equally between add, one and near. Each draw carries its kind.
   KS3: first p/q proper and in simplest form, q 2-12. yes: pm/qm, m 2-6. add: (p+k)/(q+k), k 1-5. one: p/(qm), or pm/q when pm < q, m 2-6. near: a proper c/d in simplest form with |pd - qc| = 1, d 2 to max(12, 2q), c/d != p/q.
   GCSE: base p/q as KS3; first pa/qa, a 2-6 (never simplest). yes: pb/qb, b 2-9, b != a. add: (pa+k)/(qa+k), k 1-9, with k chosen so the result is not in simplest form. one: pa/(qa·m), or pa·m/qa when proper, m 2-4. near: a neighbour c/d of the base (|pd - qc| = 1, d <= 12, c/d != p/q), shown as ce/de, e 2-6. Every number <= 60: redraw otherwise. Neither fraction is ever in simplest form.
   (Project Claude ran 20,000 draws of each kind at each level in Python: every key right, every rule held, at most 13 redraws.)

## Part 2 of 2

FRACTION-SNAP-REBUILD, part 2 of 2 (part 1 came first).

EXACT CHANGE (continued):
4. Levels: MaffsLevel.resolve({slug:'fraction-equivalence', levels:['year6','ks3','gcse'], fallback:'ks3'}), with no boards:['all']. gameLevel is the resolved level everywhere (events, submitScore, score history). leaderboards/index.html:187 becomes ['fraction-equivalence','Fraction Snap',['year6','ks3','gcse']]. Nothing is deleted in Firebase.
5. Personal best per level: key 'fs_best_' + gameLevel; the old fs_best is no longer read.
6. KaTeX: draw both fractions with KaTeX \dfrac, loaded as split-it does (games/split-it/index.html:21-22), at the size the CSS fractions have now. Remove .frac-num, .frac-line and .frac-den. The hint (:357-362) renders in KaTeX too, its content unchanged. Answers still compare cur.equiv, never rendered HTML.
7. scripts/verify-fraction-equivalence.py, rewritten to these rules:
   - Bank: every key by Fraction; every item's kind holds (add: the same k > 0 on both; one: exactly one of top and bottom multiplied by an integer >= 2; near: |ad - bc| = 1); denominators in the set; proper; no repeats in either order; >= 40 items; every NO kind present.
   - KS3 and GCSE: 20,000 draws each in Chromium. Every key; every rule in item 3, including KS3's first fraction always in simplest form, and GCSE never in simplest form with every number <= 60; YES share 45-55%; each NO kind 30-37% of the NOs.
   - Marking both ways, the hint's figures and verdict, and dealing, as today.
   - New plants that must FAIL: a wrong key in the bank; a GCSE draw in simplest form; the old +1..3-on-the-bottom NO rule restored; the best back to one shared key. Every existing plant that still applies is kept.
8. Docs: move LEDGER-B4-FRACTION-EQUIVALENCE to docs/history/todo-done.md with a done note; close fraction-equivalence-v20-001 in docs/audits/findings/fraction-equivalence.yml. Move 1.48 to todo-done (its last open case is fixed here). Rewrite 1.14's headline so it no longer says plain FIXED: keys fixed, Jon's review of the 24 explanations still owed. Drop "the --live check is owed" from its owner cell, because its body records the check as run on 8 Nov. Add row BEST-KEY-PER-LEVEL (§4): the eight games above, and which of them serve more than one level (report only). todo.md must end smaller than 151,168 bytes. One /updates/ line: "Fraction Snap: 46 Year 6 pairs, a harder GCSE level, and wrong pairs built from real misconceptions." cloud.md entry.
9. PR, Gate and phone-fit-full green, then merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line. No draft PR.

DO NOT TOUCH: schools/assets/; the 30 s timer, 15 questions a session, scoring, the YES/NO buttons, MaffsLock and MaffsNext use; question_answered's fields; the roster; canon; docs/handover/home.md; the eight other games; Firebase data.

SUCCESS CONDITION: the bank is the 46 items above; KS3 and GCSE play by item 3's rules; boards and events carry year6, ks3 or gcse; the hub lists all three; the best is per level; the fractions and hint are in KaTeX; the verifier passes with every new plant failing; the docs in item 8 are done and todo.md is smaller; #832 is closed out; merged by merge-pr.py with a GREEN last line; cloud.md records it all.

STOP IF: any line reference doesn't match main (report what is there); check-leaderboard-coverage.js disagrees with the new wiring; KaTeX fractions fail a phone-fit check that passed before (report sizes; don't redesign); a generator can't meet its rules without a dead end; merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
END OF CONTRACT
