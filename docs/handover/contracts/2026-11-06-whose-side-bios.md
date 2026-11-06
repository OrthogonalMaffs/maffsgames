# WHOSE-SIDE-BIOS (Jon, via Project Claude, 6 Nov 2026), verbatim

Queued on 6 Nov 2026 by the WHOSE-SIDE-ART session (PR #684) for a fresh cloud session. The contract carried no name; the cloud lane calls it WHOSE-SIDE-BIOS. Start it only after WHOSE-SIDE-FIT merges, from current main. WHOSE-SIDE-FIT was queued later the same day (`2026-11-06-whose-side-fit.md`), and its contract calls this one WHOSE-SIDE-INTRO.

LANE: cloud (fresh session) · TIER: Shared · after WHOSE-SIDE-FIT merges, from current main

COORDINATION: the home lane may have codex/escape-herrings open (escape-room engine). Do not touch escape-rooms/, tools/pack-generator/ or docs/handover/home.md. Record in docs/handover/cloud.md.

TASK: Introduce HYP, OPP and ADJ on the start screen of "Whose Side Are You On?" through Jon's ramp: tap a side to light it and read its bio. Take every character line out of play, and give right answers the same rule sentence wrong answers get.

ROOT CAUSE: The character lines (#682) arrive in play from characters the student has never met. Jon, 6 Nov: "just randomly saying 'Marvellous, After you' means nothing, the characters have not been introduced". They also crowd the feedback panel, whose job is the verdict and the rule. The ramp (#684) already carries the game's colours: slope red-orange = HYP, upright blue = OPP, base green = ADJ, with θ at the tip.

CLASS CHECK: Local. One game's start screen and its feedback text; no shared code.

EXACT CHANGE:
1. Start screen: the existing key panel (.panel.menu-info, its <p> and .key list) is replaced by a bios panel of the same role. It has three buttons, one per side, each showing that side's existing swatch (colour, line style, letter), plus one bio area showing one bio at a time. Default: no side chosen; the area reads "Tap a side of the ramp to meet it."
2. The ramp: three tap regions over the slope, upright and base strips, measured from the WebP's own pixels (as the tip was in WHOSE-SIDE-ART). Each is at least 44 px deep at 320 wide. Tapping a strip or its button: that strip is outlined in the side's game line style (HYP solid, OPP dashed, ADJ dotted) in var(--text), its button is pressed (aria-pressed), and its bio shows. Tapping again or choosing another switches. Keyboard: the buttons are the controls; the regions are pointer-only and aria-hidden. θ and the arc are unchanged.
3. Bios, verbatim (θ in KaTeX; Location first, then Length, then Favourite number, each with that field label):
   HYP · Location: Opposite the right angle. That's my spot, I earned it, and I'm not moving. · Length: Bigger than the other two. Always. · Favourite number: The biggest one.
   OPP · Location: The only side that doesn't touch θ. I'm shy. · Length: Ask my friend Pythagoras, he always knows. · Favourite number: 6. I'm opposite 1 on a dice.
   ADJ · Location: Right next to θ, and I'm not the hypotenuse. Personal space is overrated. · Length: Always positive; other than that, I'm flexible. I can do a handstand, don't you know. · Favourite number: 52!
4. Play: remove every line spoken by HYP, OPP, ADJ or θ (right-answer lines, streak lines, results lines, Stage 1 speaker). Plain non-character text (streak count, score) stays. On a right answer the panel shows "✓ Right" and the same rule sentence the wrong-answer panel shows for that item (e.g. "tan θ is OPP over ADJ."), from the existing feedback table, coloured as it is there.
5. Archive the removed lines verbatim in docs/whose-side-lines.md with the date and Jon's reason. Delete the dead code (LINE, SAYS and their callers) rather than leaving it switched off.
6. Verifier: the three bios compared with the contract's text; each strip's role recomputed from the picture's geometry, not the page's labels (HYP = the strip opposite the right angle, OPP = the strip not touching the tip, ADJ = the other), and tapping it or its button shows that role's bio; tap regions 44 px deep at 320 and 390; keyboard reaches all three buttons; no character line anywhere in play across all four stages; right and wrong panels both carry the item's rule sentence, recomputed from FN; first stage button against the fold reported, not judged. Plants: OPP's and ADJ's bios swapped; a strip mapped to the wrong role; a character line left in the right-answer panel; the rule sentence missing on a right answer. Each must be caught.
7. Retire the #682 verifier checks for the removed lines. Keep the HOLD_MS 2.0 s check.

DO NOT TOUCH: the subtitle (Jon has not decided); the WebP; θ, the arc and the tip; the triangle fit (WHOSE-SIDE-FIT); colours and line styles; HOLD_MS; question generation and the feedback table's wording; any other game; shared assets; the files under COORDINATION.

SUCCESS CONDITION: A student can tap each side of the ramp and read its bio, on phone and desktop, by touch and keyboard; the bios match verbatim; no character speaks in play; right and wrong answers both show the rule; all plants caught; phone-fit passes; full verifier 0 failures. Committed, PR open, Gate green, entry in docs/handover/cloud.md; stop for Project Claude's review and Jon's "merge".

STOP IF: a strip cannot be given a 44 px tap region at 320 without overlapping another; a stage's wrong-answer panel has no rule sentence to reuse (report which, do not invent one); the bios panel is taller than the key panel it replaces by more than 40 px at 390x844 (report the numbers).
