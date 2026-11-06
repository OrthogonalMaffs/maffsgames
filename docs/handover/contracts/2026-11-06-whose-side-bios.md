# WHOSE-SIDE-BIOS (Jon, via Project Claude, 6 Nov 2026, consolidated), verbatim

Saved on 6 Nov 2026 by the WHOSE-SIDE-BIOS session. This text consolidates the 6 Nov version, its Amendment 1 and Amendment 2, and replaces the earlier saved text (in git history). Jon's two answers to the implementer's questions follow it.

LANE: cloud (fresh session) · TIER: Shared · after WHOSE-SIDE-FIT (#688) merges, from current main

FIRST: overwrite docs/handover/contracts/2026-11-06-whose-side-bios.md with this text verbatim (it consolidates the 6 Nov version, its Amendment 1 and Amendment 2), and update its queue pointer in docs/handover/cloud.md.

COORDINATION: Codex owns tools/pack-generator/ and may add <b> markup to escape-rooms/christmas-tree-fiasco/room.js (CHRISTMAS-PACK). Claude Code (home) owns data/games.json, scripts/check-meta.py, scripts/apply-meta.py and escape-room page heads (ROOM-META). Touch none of those. Record in docs/handover/cloud.md.

TASK: Introduce HYP, OPP and ADJ on the start screen of "Whose Side Are You On?": tap a side of Jon's ramp, or its key row, to light it and read its bio. Fix the key's wording, take every character line out of the game, and show the rule as a stacked fraction on right and wrong answers alike.

ROOT CAUSE: (1) The character lines (#682) arrive in play from characters the student has never met. Jon, 6 Nov: "just randomly saying 'Marvellous, After you' means nothing, the characters have not been introduced". They also crowd the feedback panel, whose job is the verdict and the rule. (2) The ramp (#684) already carries the game's colours: slope red-orange = HYP, upright blue = OPP, base green = ADJ, with θ at the tip. (3) The panel's closing line "Move θ, and the polite two swap. HYP doesn't flinch." refers to the polite characters, who leave the game. (4) Jon, 6 Nov: show the rule as an actual fraction, "another vector for remembering it"; it is also the form Stage 5 and exams use (sin θ = O/H).

CLASS CHECK: Local. One game's start-screen panel, its feedback text and its verifier; no shared code.

EXACT CHANGE:
1. Start screen, inside .panel.menu-info: change ONLY the opening <p>, the .key list and the closing line after the key. The Stages heading, #stageList, the scoring line ("Ten quick questions a stage. No lives: ...") and everything else in the panel stay exactly as they are.
2. The key stays visible, with its swatches (colour, line style, letter). Definitions become:
   HYP, the longest side, across from the right angle.
   OPP, across from θ: the only side that doesn't touch it.
   ADJ, next to θ, and not the hypotenuse.
   The .say lines in the key are removed. Each key row becomes a button (aria-pressed) for its side. Below the key, one bio area shows the chosen side's bio; default text: "Tap a side of the ramp, or its name, to meet it." The opening <p> keeps its first sentence ("Every side gets its name from the marked angle.") and drops the rest. The closing line becomes, verbatim (θ in KaTeX): "Put θ in the other corner and OPP and ADJ swap. HYP stays put."
3. The ramp: three tap regions over the slope, upright and base strips, measured from the WebP's own pixels (as the tip was in WHOSE-SIDE-ART), each at least 44 px deep at 320 wide. Tapping a strip or its key row: that strip is outlined in the side's game line style (HYP solid, OPP dashed, ADJ dotted) in var(--text), the row is pressed, and its bio shows. Choosing another side switches. Keyboard: the key rows are the controls; the regions are pointer-only and aria-hidden. θ and the arc are unchanged.
4. Bios, verbatim (θ in KaTeX; Location, then Length, then Favourite number, each with that field label):
   HYP · Location: Opposite the right angle. That's my spot, I earned it, and I'm not moving. · Length: Bigger than the other two. Always. · Favourite number: The biggest one.
   OPP · Location: The only side that doesn't touch θ. I'm shy. · Length: Ask my friend Pythagoras, he always knows. · Favourite number: 6. I'm opposite 1 on a dice.
   ADJ · Location: Right next to θ, and I'm not the hypotenuse. Personal space is overrated. · Length: Always positive; other than that, I'm flexible. I can do a handstand, don't you know. · Favourite number: 52!
5. Play: remove every line spoken by HYP, OPP, ADJ or θ (right-answer lines, streak lines, results lines, Stage 1 speaker). Plain non-character text (streak count, score) stays. The verdict stays ("✓ Right" / "✗ Not quite").
6. The rule, Stages 2-4, on right AND wrong answers: an equation, not a sentence: sin θ = OPP/HYP, cos θ = ADJ/HYP, tan θ = OPP/ADJ, the fraction stacked (KaTeX \dfrac), each side's word in its side colour, at the size of the existing fraction line; the same equation in both panels for the same item. Stage 1 keeps a sentence rule (e.g. "That's OPP: the only side that doesn't touch θ.").
7. Archive every removed line (the key's .say lines and all in-play lines) verbatim in docs/whose-side-lines.md with the date and Jon's reason. Delete the dead code (LINE, SAYS, .say and their callers) rather than leaving it switched off.
8. Verifier: the three key definitions, the closing line and the three bios compared with this contract's text; the Stages heading, stage list and scoring line present and unchanged; each strip's role recomputed from the picture's geometry, not the page's labels (HYP = the strip opposite the right angle, OPP = the strip not touching the tip, ADJ = the other), and tapping it or its key row shows that role's bio; tap regions 44 px deep at 320 and 390; keyboard reaches all three rows; no character line anywhere on the start screen (the subtitle, #subtitle, exempt: Jon has not decided) or in play across all four stages; right and wrong panels both carry the item's equation, numerator and denominator words and colours recomputed from FN; first stage button against the fold reported, not judged. Plants, each caught: OPP's and ADJ's bios swapped; ADJ's definition reverted to "next to θ."; the old closing line restored; a strip mapped to the wrong role; the scoring line removed; a character line left in the right-answer panel; the rule missing on a right answer; numerator and denominator swapped; the equation shown as a sentence again.
9. Retire the #682 verifier checks for the removed lines. Keep the HOLD_MS 2.0 s check and every WHOSE-SIDE-FIT check.

DO NOT TOUCH: the Stages heading, #stageList and the scoring line; the subtitle; the WebP; θ, the arc and the tip; the triangle fit and grid rows (WHOSE-SIDE-FIT); colours and line styles; HOLD_MS; question generation and the verdict wording; any other game; shared assets; the files under COORDINATION.

SUCCESS CONDITION: The key always shows correct definitions; a student can tap each side of the ramp or its key row and read its bio, on phone and desktop, by touch and keyboard; bios, definitions and closing line match verbatim; no character speaks anywhere except the bios; right and wrong answers both show the stacked, coloured equation (Stages 2-4); the stages and scoring line are untouched; all plants caught; phone-fit passes; full verifier 0 failures. Report the start screen's height and the first stage button against the fold at 320x568, 375x667 and 390x844, before and after. Committed, PR open, Gate green, entry in docs/handover/cloud.md; stop for Project Claude's review and Jon's "merge".

STOP IF: WHOSE-SIDE-FIT has not merged; a strip cannot be given a 44 px tap region at 320 without overlapping another; the stacked equation pushes Next below the fold at any phone size where it is above on main (report the numbers); any change outside the opening <p>, the .key list and the closing line seems necessary in .panel.menu-info.

## Jon's answers to the implementer's questions (6 Nov 2026, in the session), verbatim choices

The implementer asked before building, because item 7 names `LINE` as dead code, but `LINE` holds the four misconception lines Jon approved in the original WHOSE-SIDE contract (`docs/history/contracts/2026-11-05-whose-side.md`, "Misconception feedback"), not character lines.

1. Misconception lines: **"Keep them (Recommended)"**. Wrong answers keep the named-misconception line under the rule. Stage 1: "That's X: <definition>." on right and wrong, plus the misconception line on wrong. Stage 4 wrong: the equation, then "Use both…". LINE stays; only SAYS and .say are deleted.
2. Stage 2's wrong panel: **"Equation + numbers (Recommended)"**. The equation, then the existing numbers sentence under it, on wrong answers only. Right answers show only the equation, since the fraction line already shows the correct 5/13.
