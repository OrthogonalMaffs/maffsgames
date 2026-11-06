# WHOSE-SIDE-BIOS (Jon, via Project Claude, 6 Nov 2026, second version), verbatim

Saved on 6 Nov 2026 by the WHOSE-SIDE-ART session (PR #684) for a fresh cloud session; it replaces the first version saved on #684's branch earlier the same day (in git history, commit e7a86fea). WHOSE-SIDE-FIT's contract calls this one WHOSE-SIDE-INTRO.

LANE: cloud (fresh session) · TIER: Shared · after WHOSE-SIDE-FIT merges, from current main

FIRST: replace docs/handover/contracts/2026-11-06-whose-side-bios.md with this text verbatim (it supersedes the version saved on #684's branch) and update the queue pointer in docs/handover/cloud.md.

COORDINATION: the home lane may have codex/escape-herrings open (escape-room engine). Do not touch escape-rooms/, tools/pack-generator/ or docs/handover/home.md. Record in docs/handover/cloud.md.

TASK: Introduce HYP, OPP and ADJ on the start screen of "Whose Side Are You On?": tap a side of Jon's ramp, or its key row, to light it and read its bio. Fix the key's ADJ definition, take every character line out of the game, and give right answers the same rule sentence wrong answers get.

ROOT CAUSE: (1) The character lines (#682) arrive in play from characters the student has never met. Jon, 6 Nov: "just randomly saying 'Marvellous, After you' means nothing, the characters have not been introduced". They also crowd the feedback panel, whose job is the verdict and the rule. (2) The key's ADJ definition, "next to θ", also describes the hypotenuse, since two sides touch θ: it teaches the commonest ADJ mistake. (3) The ramp (#684) already carries the game's colours: slope red-orange = HYP, upright blue = OPP, base green = ADJ, with θ at the tip.

CLASS CHECK: Local. One game's start-screen key, its feedback text and its verifier; no shared code.

EXACT CHANGE:
1. Start screen, inside .panel.menu-info: change ONLY the opening <p> and the .key list. The Stages heading, #stageList, the scoring line ("Ten quick questions a stage. No lives: ...") and everything else in the panel stay exactly as they are.
2. The key stays visible, with its swatches (colour, line style, letter). Definitions become:
   HYP, the longest side, across from the right angle.
   OPP, across from θ: the only side that doesn't touch it.
   ADJ, next to θ, and not the hypotenuse.
   The .say lines in the key are removed. Each key row becomes a button (aria-pressed) for its side. Below the key, one bio area shows the chosen side's bio; default text: "Tap a side of the ramp, or its name, to meet it." The opening <p> keeps its first sentence ("Every side gets its name from the marked angle.") and drops the rest.
3. The ramp: three tap regions over the slope, upright and base strips, measured from the WebP's own pixels (as the tip was in WHOSE-SIDE-ART), each at least 44 px deep at 320 wide. Tapping a strip or its key row: that strip is outlined in the side's game line style (HYP solid, OPP dashed, ADJ dotted) in var(--text), the row is pressed, and its bio shows. Choosing another side switches. Keyboard: the key rows are the controls; the regions are pointer-only and aria-hidden. θ and the arc are unchanged.
4. Bios, verbatim (θ in KaTeX; Location, then Length, then Favourite number, each with that field label):
   HYP · Location: Opposite the right angle. That's my spot, I earned it, and I'm not moving. · Length: Bigger than the other two. Always. · Favourite number: The biggest one.
   OPP · Location: The only side that doesn't touch θ. I'm shy. · Length: Ask my friend Pythagoras, he always knows. · Favourite number: 6. I'm opposite 1 on a dice.
   ADJ · Location: Right next to θ, and I'm not the hypotenuse. Personal space is overrated. · Length: Always positive; other than that, I'm flexible. I can do a handstand, don't you know. · Favourite number: 52!
5. Play: remove every line spoken by HYP, OPP, ADJ or θ (right-answer lines, streak lines, results lines, Stage 1 speaker). Plain non-character text (streak count, score) stays. On a right answer the panel shows "✓ Right" and the same rule sentence the wrong-answer panel shows for that item (e.g. "tan θ is OPP over ADJ."), from the existing feedback table, coloured as it is there.
6. Archive every removed line (the key's .say lines and all in-play lines) verbatim in docs/whose-side-lines.md with the date and Jon's reason. Delete the dead code (LINE, SAYS, .say and their callers) rather than leaving it switched off.
7. Verifier: the three key definitions and three bios compared with this contract's text; the Stages heading, stage list and scoring line still present and unchanged; each strip's role recomputed from the picture's geometry, not the page's labels (HYP = the strip opposite the right angle, OPP = the strip not touching the tip, ADJ = the other), and tapping it or its key row shows that role's bio; tap regions 44 px deep at 320 and 390; keyboard reaches all three rows; no character line anywhere on the start screen or in play across all four stages; right and wrong panels both carry the item's rule sentence, recomputed from FN; first stage button against the fold reported, not judged. Plants: OPP's and ADJ's bios swapped; ADJ's definition reverted to "next to θ."; a strip mapped to the wrong role; the scoring line removed; a character line left in the right-answer panel; the rule sentence missing on a right answer. Each must be caught.
8. Retire the #682 verifier checks for the removed lines. Keep the HOLD_MS 2.0 s check.

DO NOT TOUCH: the Stages heading, #stageList and the scoring line; the subtitle (Jon has not decided); the WebP; θ, the arc and the tip; the triangle fit and grid rows (WHOSE-SIDE-FIT); colours and line styles; HOLD_MS; question generation and the feedback table's wording; any other game; shared assets; the files under COORDINATION.

SUCCESS CONDITION: The key always shows correct definitions; a student can tap each side of the ramp or its key row and read its bio, on phone and desktop, by touch and keyboard; the bios and definitions match verbatim; no character speaks anywhere except the bios; right and wrong answers both show the rule; the stages and scoring line are untouched; all plants caught; phone-fit passes; full verifier 0 failures. Report the start screen's height and the first stage button against the fold at 320x568, 375x667 and 390x844, before and after. Committed, PR open, Gate green, entry in docs/handover/cloud.md; stop for Project Claude's review and Jon's "merge".

STOP IF: WHOSE-SIDE-FIT has not merged; a strip cannot be given a 44 px tap region at 320 without overlapping another; a stage's wrong-answer panel has no rule sentence to reuse (report which, do not invent one); any change outside the opening <p> and the .key list seems necessary in .panel.menu-info.
