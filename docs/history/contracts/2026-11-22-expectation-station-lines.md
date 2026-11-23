EXPECTATION-STATION-LINES. Cloud lane. Tier: Small (one game's Stage 2 layout and its verifier). From Project Claude; Jon, 22 Nov 2026, 19:28 (screenshot, es_core_012: read the line as a running total, "0.12 + (2x0.05) = 0.22 surely?") and 19:29 ("it should be separate lines please, as your suggested. they can then do some addition").
Recommended: Claude Code, Opus, medium effort. One render function rewritten to true equalities in KaTeX; the verifier proves it for every item.

TASK: In games/expectation-station/, Stage 2: show each product on its own line ("x × P(X = x) = [box]"), so every equals sign is true, in KaTeX; after Stage 2 is checked, show the sum line E(X) = ... = total.

ROOT CAUSE: renderStage2() (index.html:882-921) builds one line: "E(X) = (x1 × p1) = [slot] + (x2 × p2) = [slot] + ...", so each slot sits between two equals signs. As written it asserts (0 × 0.80) = 0 + (1 × 0.12) = 0.12 + (2 × 0.05) = ..., which is false. A student reading it literally adds as they go: Jon, on es_core_012, expected 0.22 in the third box, where the game wants 0.1 (that term alone). It happens on every item at every level. The line is plain text (× and = as characters, inline HTML), not KaTeX (canon §7.1.1), although the page loads KaTeX (:19-20).

CLASS CHECK: Local in its fix: one render function in one game. The shape (a fill-in box placed between chained "=" signs) could exist in other fill-the-box games. Grep games/*/index.html for builders that place a slot between two "=" in one line, and list them in the PR (report only, don't change them).

EXACT CHANGE:
1. First commit: the standing close-out for GIVEN-THAT-SET-LABELS (#884, merged as bc0496c; record main's run IDs from its merge and the PR's phone-fit run), per AGENTS.md, one line in cloud.md; its contract to docs/history/contracts/; given-that off the claim list. In the same commit, save this contract verbatim as docs/handover/contracts/2026-11-22-expectation-station-lines.md and claim expectation-station.
2. renderStage2(): one line per term, in KaTeX: x × P(X = x) = [slot], e.g. 2 × 0.05 = [box]. The slots, their ids, the tile bank, selectSlot, the marking and scoring stay the same; only the layout around them changes. Values shown as now (pDisplayHTML/renderValue), typeset in KaTeX where they are numbers or fractions.
3. After Stage 2 is checked (right, or as revealed after the last try), show one more line, not a slot and not scored: E(X) = Σ x P(x) = 0 + 0.12 + 0.1 + 0.09 = 0.31 (the item's own products and total, exact, in KaTeX, in the form the game's values use). Its total must equal the E(X) the game uses in Stage 3, by computation.
4. Fit: the new lines keep the phone and laptop rules this game is held to (it has entries on phone-fit's known-failures lists: they must not grow; take off any it now passes). Check Calculation stays reachable without hunting.
5. Verifier (scripts/verify-expectation-station.py): for every item at every level: each Stage 2 line's left side, computed, equals its slot's key; no rendered Stage 2 line contains two "=" with a slot between them (the plant: the old single-line layout restored, caught); the sum line's terms and total recompute and match Stage 3's E(X).
6. /updates/: one dated line, e.g. Expectation Station's working now puts each product on its own line, so every equals sign is true.
7. PR report: the other games whose builders chain "=" around a box (report only). Merge on green via scripts/merge-pr.py, then the standing close-out (cloud.md one line) and unclaim the game.

DO NOT TOUCH: Every item's data, probabilities and keys; the tile bank and its distractors; the marking and scoring of all three stages; Stage 1 and Stage 3; shared assets; Gate files; other games (report only); index.html (the portal), scripts/build-uses.py, /when-will-i-use-this/ and docs/handover/home.md (the home lane's WWIUT-STRIP is in flight).

SUCCESS CONDITION: On es_core_012, Stage 2 shows four lines (0 × 0.80 = [box], 1 × 0.12 = [box], 2 × 0.05 = [box], 3 × 0.03 = [box]) and, once checked, E(X) = 0 + 0.12 + 0.1 + 0.09 = 0.31. No line asserts a false equality, on any item. The verifier proves it for every item with the plant caught; fit doesn't get worse; CI is green and the PR is merged.

STOP IF: Any item's products or total disagree with its table, or with Stage 3's E(X) (a correctness bug: report the id first). The new layout pushes Check Calculation below the fold at a size where it was above it. The fix needs a shared asset. Main goes red for a reason outside this change (one rerun per AGENTS.md, then stop and report).
