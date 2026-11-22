# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-22 (home): WHEN-WILL-I-USE-THIS (the "When will I use this?" section: 14 real jobs across ratio, percentages, area and averages, from one data file)

Claude Code (home lane), worktree `~/mg-uses`, branch `claude/when-will-i-use-this`; contract `docs/handover/contracts/2026-11-22-when-will-i-use-this.md` (verbatim, with Jon's HUBS ruling below it). The first commit carries GIVEN-THAT-POLISH's close-out (#881, 7660e2f).

- One source: `data/uses.json` (4 topics, the 15 Skills England routes, 14 scenarios verbatim, 18 sources). `scripts/build-uses.py` writes 11 committed pages (hub, 4 topics, 6 routes with scenarios) and sitemap.xml's block. Heads come from games.json "pages" via check-meta's render(); the footer is check-footer's CANONICAL. Maths is set in KaTeX at display only.
- `scripts/check-uses.py` (CI line, `--selftest && --check`): (a) to (f) as the contract lists, plus a guard that the build's own pages are whole. 27 steps with "=": 26 signs recomputed, 2 labels, and 5 steps marked noCheck ("% of" three times, a ratio, a unit change). Self-test: 41 of 41 caught. Chromium: 11 pages x 320/390 x normal/Aa, no sideways scroll.
- Outside EXACT CHANGE, needed by site-wide checks: `check-publish-scope.py` SITE gains `when-will-i-use-this/`; site-nav.js HUBS gains the 4 topic pages (Jon's ruling, 18:05). Hub has no back link: "Back to games" scrolled 4 px at 320 in Aa. parents/index.html has that same 4 px scroll on main (reported, not fixed: DO NOT TOUCH).
- Footer: defined once (check-footer.py `_LINKS`) but written into 159 pages on main (170 with these 11) by apply-footer.py, every game among them: not changed (DO NOT TOUCH any game).
- `check-uses-links.py --live` (not CI): on the first run 17 of 18 answered 200 and RCN's dosage page was 404; Project Claude's review moved it to RCN Learn, also 404 (the course is withdrawn); ruling (Project Claude with Jon): the source is now Gloucestershire Hospitals NHS FT's IV drug calculation practice formulae (PDF).
- Readings for review: ratio's parent guide is `parents/ratio-proportion/` (no `parents/ratio/`); percentages has none; "(sports turf)" sits in the groundsperson's job name; the Met Office source line is split into its two URLs; "(example figure/s)" stays in the wording, so the page marks which figures are examples, and the flag adds a note.
- Next: Gate green, then wait for Project Claude's review and Jon's look and "merge".

## 2026-11-22 (home): GIVEN-THAT-POLISH (a first-try hint, full-size fractions, slip lines that say what was computed, KaTeX in every worked answer, every fade stored)

Claude Code (home lane), worktree `~/mg-gtp`, branch `claude/given-that-polish`; contract `docs/handover/contracts/2026-11-22-given-that-polish.md` (verbatim). The first commit carries GIVEN-THAT-VENN-FADE's close-out (#879, 873befe).

- STOP checks: no STOP. Every SPEC condition other than the 27 Bayes trees is a Venn set, a table column or row, or a tree branch. The 25 stored GCSE greyOuts agree with SPEC on main (as #879 proved).
- Hint: a first wrong Phase 2 pick shows the slip's sentence, or "Not quite.", then "One more try, for 1 point." (71 named, 4 "Not quite."). Scoring, tries and analytics are unchanged.
- Fractions: `big()` sets every stored \tfrac as \dfrac at display, in options and feedback. Stored strings and dataset.latex are unchanged. The picked and correct options are no longer dimmed once spent.
- Worked answers: one renderer, `work()`, typesets P(...), a/b, = ≈ ≠ + in both phases' explanations (the Why card and the Worked Answer panel). The verifier reads each one back from its KaTeX: it must be the stored text, with no a/b left.
- Slip lines: the conditional families (Phase 1 "cond", Phase 2 "reversed") now start "That's X among Y only, P(X | Y).", in the item's labels. This is only where one group is pinned down, and not where a label is a bare Yes/No (it names nothing without its header). 24 GCSE options and 355 typed wrong ratios.
- Fade: phase2.greyOut is stored on all 90 items ("none" on the 27 Bayes trees); inferGreyOut is deleted. Tables carry data-row and data-col on every cell, so rows fade. Totals rule, from SPEC: the reduced sample space is the condition's group and its own total. For a column condition, the other columns, the Total column and the grand total fade, and the condition column's total stays. For a row condition, the same with rows. A Venn's "Total" and a tree's root fade too.
- The open Why card's thresholds were re-measured for the taller card. Needs: 827 at 320 wide, 1183 for 601 to 899, 854 at 900, 797 from 1200. New thresholds: 860, 1220, 890, 830. It is collapsed at all five fit sizes, which fit. Reported (not gated) Next below the fold on phones rose from 592 to 916 entries, all in Aa.
- Verifier: 13 plants, all caught. The 3 new: core_01 stored "none"; inferGreyOut restored with core_09's greyOut removed; the stored fade inside the condition (gcse_03's Bus, from #879).
- MERGED 22 Nov as 7660e2f (#881) via merge-pr.py, exit 0, last line "main 7660e2f run 45050898255: GREEN". Main on the merge commit: check-site 45050898255 success, phone-fit-full 45050898282 success, pages build 45050898271 success. The PR's own phone-fit runs measured given-that only: 45047801409 (head f312901) and 45049760979 (head 294beba), both success. Cleaned up by end-task. Contract moved to `docs/history/contracts/2026-11-22-given-that-polish.md` (closed out by WHEN-WILL-I-USE-THIS's first commit).

## 2026-11-22 (home): GIVEN-THAT-VENN-FADE and DOCS-TRUTH (Given That's Phase 2 fade made real and proved; two stale doc lines)

Claude Code (home lane), worktree `~/mg-gtv`, branch `claude/given-that-venn-fade`; contract `docs/handover/contracts/2026-11-22-given-that-venn-fade.md` (verbatim, with the ruling on the STOP below it). The first commit carries COMPLEX-CONVERTER-WHY's MERGED line (#874, 842aa2e).

- STOPPED at STOP IF before any change: 41 of the 90 items fade nothing in Phase 2. No item fades a region inside its condition. Ruling (Project Claude with Jon, 22 Nov): option (a). The 49 that fade are judged against SPEC; the 41 are the verifier's NO_FADE, reported, not failed. They are 7 column-condition tables inferGreyOut cannot read (core_01, core_09, core_15, core_17, l4_14, l4_16, l4_20), 4 row-condition tables (alevel_11, alevel_14, alevel_16, alevel_24), 3 branch-condition trees (core_20, l4_09, l4_17), and 27 Bayes trees, by design. The 14 and the table's never-fading Total column go to a later contract. There are 14 Venns (gcse 8, alevel 6), not 25; the ruling says 15 because the home lane's STOP report miscounted the A-Level Venns as 7. On main the fade unit fails on all 14 without reduced motion (with it, the inline opacity already faded them).
- Fix (`games/given-that/index.html` CSS only): `.venn-label.greyed,.venn-set-label.greyed{opacity:0.2}`, with the 0.6s transition the labels already had; the dead `.venn-region` rules removed (nothing used them). The verifier also found the table headers snapping to 0.2 with no transition (only td had one): `th.greyed` now has the same 0.6s, and th joins the reduced-motion list.
- `scripts/verify-given-that.py`, a `fade` unit: every item into Phase 2 at 390x844 and 1366x768 (both drawings), with and without reduced motion. Every greyed element is at most 0.3 opacity with a 0.6s transition (none with reduced motion), and every count is faded exactly when SPEC's Phase 2 denominator puts it outside the condition. A Total column, grand total and tree root are not judged. 2 new plants (the Venn rule removed: gcse_06; gcse_03's greyOut fading Bus, its own condition), 11 in all.
- canon.md "How it is checked" now says what measure-phone-fit gates: the asking-screen rule in every mode, sideways scroll in every mode (bar the `sideways` list), Next below the fold on laptop (R2), reported on phones. Snag 1 is under Fixed: 71fd49c8 (7 Oct) made the "simplifies to" line depend on a stored simplified form; e628fa18 (same day) added the identity condition.
- MERGED 22 Nov as 873befe (#879) via merge-pr.py, exit 0, last line "main 873befe run 45034467271: GREEN". Main on the merge commit: check-site 45034467271 success, phone-fit-full 45034467272 success, pages build 45034467062 success. The PR's own phone-fit run 45032986865 (head 0cdb088) measured given-that only (normal, aa, laptop), success, 14:28:19 to 14:29:49 UTC. Cleaned up by end-task. Contract moved to `docs/history/contracts/2026-11-22-given-that-venn-fade.md` (closed out by GIVEN-THAT-POLISH's first commit).

## 2026-11-22 (home): COMPLEX-CONVERTER-WHY (a Why card after a wrong answer in Form Roulette; the back link off the titles)

Claude Code (home lane), worktree `~/mg-cc-why`, branch `claude/complex-converter-why`; contract `docs/handover/contracts/2026-11-22-complex-converter-why.md` (verbatim). The first commit carries CLASS-PAGE's close-out (#872, 10ab776).

- STOP check redone on main 67ade5e: all 55 items agree with their own re, im, r, argDeg and argRad (to the bank's rounding: q5/q6's given 0.927 and q18's 2.828 are rounded), every key's angle is principal, correct === correctLatex, no distractor equals its key. No STOP.
- Why card (`games/complex-converter/index.html`, `WHY` and `showWhy`): canon 7.6.2's two copies in a `.maffs-ref-row` holding the Next mount; the page now links `fold.css`. Built at run time from the item's fields and its given and keyed TeX, through K() (j at Level 4, i at Further). The open copy shows only at `max-width:768px and min-height:1450px` or `min-width:769px and min-height:885px` (measured: worst need 1414 and 853, plus 30); every phone and both laptops get the collapsed copy beside Next, which adds no height.
- Slips named by computation (165 distractors): sign flipped (conjugate) 12, cos/sin swapped 20, degrees in the exponent 4, radians left in polar 2, r one part 15, r both parts wrong (sum or no root) 2, quadrant step missing 12, quadrant step not needed 5, r and θ swapped 3, wrong signs 23, upside-down arctan 6; 61 unnamed (no one slip, or two at once). The three r slips share one lesson; two other families at once name nothing.
- Back link: in the page's flow above every screen (it was `position:fixed` over each mode's title), not in each header: a hub label such as "← Back to OP for Secondary" cannot share a 320px header with the title and score. It costs 31px on every screen: laptop Next 498/680 (was 467); the phones were already a listed known failure (last option 857/528 on main, now 888/528).
- `scripts/verify-complex-converter.py` extended (it already existed; the contract said new): every card recomputed and every slip re-derived in Python, q16 live in j and i, the back link against every header at 320x568, 390x844 and 1366x768; 3 new plants (arctan(Re / Im), a slip for an option it does not give, the fixed back link), 11 in all, all caught.
- Found and fixed while building: the signs line read q.argRad (3 d.p.), so cos(-1.571) came out negative on the axis items; it reads argDeg now. check-site tier 2 flagged whyLine's while loop as a possible rejection-sampling loop; it is a split now.
- MERGED 22 Nov as 842aa2e (#874) via merge-pr.py, exit 0, last line "main 842aa2e run 45002104858: GREEN". Main on the merge commit: check-site 45002104858 success, phone-fit-full 45002104942 success, pages build 45002104429 success. Cleaned up by end-task. Contract moved to `docs/history/contracts/2026-11-22-complex-converter-why.md` by the cloud lane's CC-TRIG-SLIP (#876); this MERGED line closed out by GIVEN-THAT-VENN-FADE's first commit.

## 2026-11-21 (home): CLASS-PAGE (one hidden /class/ page for every child-look game; MaffsKids shared)

Claude Code (home lane), worktree `~/mg-class-page`, branch `claude/class-page`; contract `docs/handover/contracts/2026-11-21-class-page.md` (stored verbatim but for one teacher's first name, written "[a teacher's]"). The first commit carries SOME-THINGIES-TURN-LABELS' close-out (#870, 7d827fa).

- The two games' fragment rules were identical (no STOP). `schools/assets/kids-look.js` (MaffsKids: `read(hash)`, `read(hash, 'bare')`, `greeting()`, `gameLink()`, `classLink()`) is now the one copy. Each game passes its own `location.hash` once and keeps `LOOK`, `CLASS_NAME` and `greeting()`, so both verifiers pass unchanged with every plant caught.
- `/class/`: noindex, no menu, search or sitemap entry. Cards come from `"kids": true` in `data/games.json`, written in by `scripts/apply-class-page.py` (data/ is never published, so a fetch could not work). It loads analytics.js (the loader rule holds noindex pages to it); GA4's default page view leaves the fragment out.
- site-nav: `/class/` in HUBS ("the class page"); a game opened from `/class/#<Name>` goes back to `/class/#<Name>`, the name read from its own hash through MaffsKids; only the hub's path is in sessionStorage. Both games show stage-exit's short form, "← the class page" (STAGE-EXIT-LABEL).
- Checks: `scripts/test-kids-look.py` (Node vm, selective; 10 plants); check-site-nav's `class` unit and plant; check-site's site-wide class-name rule (Maple, plus `MAFFS_CLASS_NAMES`). For cloud: ci-deps' KNOWN_TOP lacks `class` (like printables, ugh-stats, core-maths), so a `class/` change counts as shared.
- MERGED 21 Nov as 10ab776 (#872) via merge-pr.py (the Gate's 101 runs green). Main on the merge commit: check-site 44956845120 success, phone-fit-full 44956845115 success, pages build 44956845097 success. Cleaned up by end-task. Contract moved to `docs/history/contracts/2026-11-21-class-page.md` (closed out by COMPLEX-CONVERTER-WHY's first commit).

## 2026-11-21 (home): SOME-THINGIES-TURN-LABELS (Stage 3's turn: labels gone first, thingies eyes up)

Claude Code (home lane), worktree `~/mg-stl`, branch `claude/some-thingies-turn-labels`; contract `docs/handover/contracts/2026-11-21-some-thingies-turn-labels.md` (the 20:09 reissue with amendment 1, which arrived after I'd started; I carried on). The first commit carries SOME-THINGIES-PERSONALITY's close-out (#868, 8bf4b4e; its entry below).

- `turnArray()`: the labels fade (120 ms) and are cleared, then the array turns on `MaffsLock.timer`. The turned array is redrawn with empty labels. With reduced motion it is drawn at once.
- Amendment 1: `.arr.turning .th{transform:rotate(-90deg)}`, centred on each thingy, with the array's 0.6 s ease, so every thingy stays eyes up. Measured mid-turn in Chromium: net 0° within 3°.
- Next is there at once after marking; marking and the lock are untouched.
- The verifier's new `turn` unit (laptop and phone at full motion, phone with reduced motion) and two plants (labels left visible, no counter-rotation), both caught; 15 plants in all.
- MERGED 21 Nov as 7d827fa (#870) via merge-pr.py, exit 0, last line "main 7d827fa run 44946545379: GREEN". Main on the merge commit: check-site 44946545379 success, pages build 44946545012 success, phone-fit-full 44946545381 success with its matrix skipped (a game-only change selects no shared path), so some-thingies was measured locally on main 4ac9b3af: PASS in normal, aa and laptop modes. Cleaned up by end-task. Contract moved to `docs/history/contracts/2026-11-21-some-thingies-turn-labels.md` (closed out by CLASS-PAGE's first commit).

