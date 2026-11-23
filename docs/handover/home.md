# Handover: home lane

**Queue (cross-lane facts; never archived)**

- PHONE-SCROLL (Small; Project Claude, 10 Nov 05:55, Amendments 1-3): merged as a594c8f (#721) under Jon's one-off ruling of 10 Nov 07:05; main run 42772678182 GREEN (89/89 jobs; phone-fit-full 42772678203 green). Entry below.

- DOCS-BUNDLE (Docs; Project Claude, 9 Nov 19:10, Amendments 1-2): merged as 10d3167.

- WHOSE-SIDE: the cloud lane owns the game until stage 5; timer-policy.md's line is `docs/todo.md` row WHOSE-SIDE-TIMER-LINE. DONE lines moved to docs/history/handover-home-archive.md, 8 Nov.

- One lane at a time: AGENTS.md, Lane ownership (rule e, BACKLOG-ONE).

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts: `docs/todo.md` row HOW-MANY-PARTS-FRACTION (§3)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

## 2026-11-23 (home): WWIUT-BATCH-1-2 ("When will I use this?" grows to 40 jobs in 16 topics, with a tier on every job and the home strip's count written by the build)

Claude Code (home lane), worktree `~/mg-batch`, branch `claude/wwiut-batch-1-2`; contract `docs/handover/contracts/2026-11-22-wwiut-batch-1-2.md` (verbatim). The first commit carries WWIUT-STAND-OUT's close-out (#885, 66a29e7).

- Data: 26 of the 33 approved scenarios and 12 of the 13 topics, verbatim; every scenario has a tier (the 14 existing "F"). Step 5 took out 7 scenarios whose sources do not answer 200 (re-fetched as a browser too: 404, 410, 403, 522): football-analyst, bricklayer-corner, crime-scene-investigator, mammographer, football-recruitment-analyst, nuclear-medicine-technologist, chef. That passed the STOP IF of 4; by the standing rule the rest was finished and the list reported. Probability, left with no scenario, is left out too (decided for Jon). Each is listed in the PR with its source.
- check-uses.py's reader, in one place, also reads "1,000", "1/16", ½, √, superscript powers, sin, cos, tan and their inverses (degrees), "°", and an expression on the right; the 14 existing scenarios read exactly as before (all 48 results compared). 40 headlines and 83 "=" signs recomputed; 5 new noCheck steps, each with a reason (hours and minutes, minutes and seconds, "% of", "1 in 5"). Self-test 94 of 94.
- build-uses.py: a Higher or Level 4 tag on cards (measured 4.5:1 in Chromium); KaTeX for the new signs; index.html's "N real jobs" written between uses-count markers and checked. A topic heading ("Transformations:") scrolled 46 px at 320 in Aa: headings now wrap long words.
- index.html: #usesFlag and #parFlag lose data-cmp-hide, so both show on phones while current; expiry unchanged. 12 HUBS lines in site-nav.js under Jon's ruling (23 Nov), as #883's 4. 21 new data/games.json "pages" entries; 7 descriptions updated.
- Next: Gate green, then wait for Project Claude's review and Jon's "merge".
- Taken over and merged by the cloud lane (contract WWIUT-BATCH-MERGE, 23 Nov): see docs/handover/cloud.md.

## 2026-11-22 (home): WWIUT-STAND-OUT ("When will I use this?" gets its own navy strip on the home page; the section leads with coloured course tiles and a sum on every job card)

Claude Code (home lane), worktree `~/mg-wwiut`, branch `claude/wwiut-stand-out`; contract `docs/handover/contracts/2026-11-22-wwiut-stand-out.md` (verbatim). The first commit carries WHEN-WILL-I-USE-THIS's close-out (#883, 2710eed).

- Portal: a navy strip (`#usesStrip`, `.par-strip uses-strip cmp`) above the parents strip, with a New flag dated 2026-11-22 and the button "See the jobs" (`data-mfg-item="open-wwiut"`, section `when-will-i-use-this`). The parents strip has its one button again. `applyParFlag()` became `applyStripFlags()`: every `.par-flag[data-badge-date]` expires on BADGE_DAYS; game cards are untouched.
- `verify-new-and-updated.py` checks each strip flag on its last shown day and its first hidden day, read from the markup. A new plant (the expiry ignores the new flag) is caught: 4 of 4.
- Data: 15 route colours, white at 4.92:1 or better, the closest pair delta E 16.4, the nearest to teal delta E 33.5. The 14 headlines are as the contract gives them, and all recompute.
- Pages: the hub runs "Pick your course" tiles, then 14 job cards (each with its headline in KaTeX, linked to `<topic>/#<id>`), then "By maths topic", in a 1040 px container. Scenario cards get a route-colour top band, a route chip and the headline. Route headers are filled with their colour. The hub's foot line drops its self-link. The look is in `when-will-i-use-this/uses.css`, written by build-uses.py.
- check-uses.py: headlines, colours, anchors, no hub self-link, and Chromium contrast on tiles, chips and headers. Self-test 50 of 50. A route header scrolled 9 px at 320 in Aa ("environmental"); fixed with overflow-wrap and less phone padding.
- MERGED 22 Nov as 66a29e7 (#885) via merge-pr.py, exit 0, last line "main 66a29e7 run 45075943570: GREEN", on Jon's "merge", after a merge of main for #886's conflict on updates/index.html (both lines kept; head 662f42a, Gate check-site 45074183522 and phone-fit-full 45074183455, both success). Main on the merge commit: check-site 45075943570 success, phone-fit-full 45075943580 success, pages build 45075943027 success. Cleaned up by end-task. Contract moved to `docs/history/contracts/2026-11-22-wwiut-stand-out.md` (closed out by WWIUT-BATCH-1-2's first commit).

## 2026-11-22 (home): WHEN-WILL-I-USE-THIS (the "When will I use this?" section: 14 real jobs across ratio, percentages, area and averages, from one data file)

Claude Code (home lane), worktree `~/mg-uses`, branch `claude/when-will-i-use-this`; contract `docs/handover/contracts/2026-11-22-when-will-i-use-this.md` (verbatim, with Jon's HUBS ruling below it). The first commit carries GIVEN-THAT-POLISH's close-out (#881, 7660e2f).

- One source: `data/uses.json` (4 topics, the 15 Skills England routes, 14 scenarios verbatim, 18 sources). `scripts/build-uses.py` writes 11 committed pages (hub, 4 topics, 6 routes with scenarios) and sitemap.xml's block. Heads come from games.json "pages" via check-meta's render(); the footer is check-footer's CANONICAL. Maths is set in KaTeX at display only.
- `scripts/check-uses.py` (CI line, `--selftest && --check`): (a) to (f) as the contract lists, plus a guard that the build's own pages are whole. 27 steps with "=": 26 signs recomputed, 2 labels, and 5 steps marked noCheck ("% of" three times, a ratio, a unit change). Self-test: 41 of 41 caught. Chromium: 11 pages x 320/390 x normal/Aa, no sideways scroll.
- Outside EXACT CHANGE, needed by site-wide checks: `check-publish-scope.py` SITE gains `when-will-i-use-this/`; site-nav.js HUBS gains the 4 topic pages (Jon's ruling, 18:05). Hub has no back link: "Back to games" scrolled 4 px at 320 in Aa. parents/index.html has that same 4 px scroll on main (reported, not fixed: DO NOT TOUCH).
- Footer: defined once (check-footer.py `_LINKS`) but written into 159 pages on main (170 with these 11) by apply-footer.py, every game among them: not changed (DO NOT TOUCH any game).
- `check-uses-links.py --live` (not CI): on the first run 17 of 18 answered 200 and RCN's dosage page was 404; Project Claude's review moved it to RCN Learn, also 404 (the course is withdrawn); ruling (Project Claude with Jon): the source is now Gloucestershire Hospitals NHS FT's IV drug calculation practice formulae (PDF).
- Readings for review: ratio's parent guide is `parents/ratio-proportion/` (no `parents/ratio/`); percentages has none; "(sports turf)" sits in the groundsperson's job name; the Met Office source line is split into its two URLs; "(example figure/s)" stays in the wording, so the page marks which figures are examples, and the flag adds a note.
- Next: Gate green, then wait for Project Claude's review and Jon's look and "merge".
- MERGED 22 Nov as 2710eed (#883) via merge-pr.py, exit 0, last line "main 2710eed run 45061326436: GREEN", after Project Claude's review (the RCN source replaced, by ruling, with Gloucestershire Hospitals NHS FT's calculation formulae; 18 of 18 links 200) and a merge of main for #882's conflict. Main on the merge commit: check-site 45061326436 success, phone-fit-full 45061326451 success (every game), pages build 45061325860 success. The PR's last Gate: check-site 45059668766 and phone-fit-full 45059668793 (head d0c21e3), both success. Cleaned up by end-task. Contract moved to `docs/history/contracts/2026-11-22-when-will-i-use-this.md` (closed out by WWIUT-STAND-OUT's first commit).

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

