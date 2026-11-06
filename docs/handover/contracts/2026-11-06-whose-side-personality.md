# WHOSE-SIDE-PERSONALITY (6 Nov 2026), saved verbatim

LANE: cloud (one session) · TIER: Shared · from current main (after #680)

COORDINATION: the home lane has codex/escape-herrings open (escape-room engine). Do not touch escape-rooms/, tools/pack-generator/ or docs/handover/home.md. The LOGO-CENTRE close-out PR may be open and edit docs/handover/cloud.md: rebase on main before your PR, keep every cloud.md entry, STOP rather than drop one. Record in docs/handover/cloud.md.

TASK: Give "Whose Side Are You On?" its personality (Jon's characters and lines, verbatim) and make it fill a large screen or projector, without changing how it plays.

ROOT CAUSE: The game (games/whose-side-are-you-on/index.html, live and unlisted since #674/#676) was built in one evening for Jon's 6 Nov lesson. Students liked how it plays and wanted nothing changed there, but it has no voice (Jon: "looks very much like a template job, it has no personality") and it is laid out for a phone: on a 1920px screen the whole game sits in a column about 660px wide and the triangle uses about a third of the screen, too small for the back of a classroom on a projector.

CLASS CHECK: Local: one game's text and its own layout. No shared code. (Other games' large-screen sizing is not in scope.)

EXACT CHANGE (games/whose-side-are-you-on/index.html, plus its verifier and cloud.md):
1. Characters (Jon, 6 Nov): HYP is stoic and immovable; OPP and ADJ are an impeccably polite pair who swap places depending on where θ is; θ is the guest of honour. All text below is Jon's, verbatim (straight or curly quotes as the page already uses); HYP/OPP/ADJ keep their colours (Amendment 2: colours for the side words only).
2. Subtitle (replace the current one): "One side never moves. The other two can't stop being polite about it."
3. Start screen: keep the three legend rows (line sample, letter, coloured word) and add each character's line after its definition; then one closing line:
   - HYP row: "HYP, the longest side, across from the right angle." + "“I'm here. I'm always here.”"
   - OPP row: "OPP, across from θ." + "“Oh, I'm opposite today? Splendid.”"
   - ADJ row: "ADJ, next to θ." + "“Then I shall stand beside it. After you.”"
   - Closing line: "Move θ, and the polite two swap. HYP doesn't flinch."
   Keep "Ten quick questions a stage…" and the stage list.
4. Right answers: the hold after a right answer becomes 2.0 s (Jon, 6 Nov: 0.8 s is far too short to take in the lit side), clock still stopped and taps still ignored during it. During the hold, with "✓ Right", show one of these at random (never the same twice running): "HYP: “Correct. I remain unmoved.”" / "OPP: “Spot on. Do carry on.”" / "ADJ: “Marvellous. After you.”"
5. Wrong answers, Stage 1 only, one character line ABOVE the existing teaching line (the teaching line stays, unchanged):
   - asked HYP and tapped another side, or asked OPP/ADJ and tapped HYP: "HYP: “I have been the hypotenuse since before you were born.”"
   - asked OPP and tapped ADJ, or asked ADJ and tapped OPP: "OPP and ADJ: “Terribly sorry, I think you'll find we swapped.”"
6. Streak shout-outs, shown briefly when the streak reaches exactly that number (all stages): 3: "HYP nods, very slightly." · 5: "OPP and ADJ bow so politely they bump heads." · 10: "HYP shows emotion. Once. Never again."
7. Results screen, one line above the score: 8–10 right: "Sides labelled. HYP is quietly proud. He will never say so." · 0–5 right: "The polite two are still bowing at each other in the corridor. Shall we go again?" · 6–7: no character line.
8. Large screens: on viewports 1024px wide and above, the game column grows with the screen (up to about 1100px), the triangle is sized to fill the height available (so the question, triangle and answer controls all fit without scrolling), and text and buttons scale up in proportion (clamp()). Phones are unchanged: phone-fit at 320 and 390, normal and Aa, must still pass.
9. Verifier: the start-screen, subtitle, right, wrong, streak and results lines compared with this contract's text exactly; the right-answer line never repeats twice running; the right-answer hold is 2.0 s with the clock stopped; the Stage 1 wrong-line rule recomputed from the geometry (as the teaching line already is); at 1366x768 and 1920x1080 the triangle's drawn height is at least 50% of the viewport height and the answer controls are on screen without scrolling; plants: a wrong line, a missing streak shout-out at 5, a small triangle at 1920x1080.
10. /updates/: no line (the game is unlisted).

DO NOT TOUCH: how the game plays (stages, questions, generator, marking, scoring, timing apart from the hold now 2.0 s, tap bands, slots and Check); the teaching lines' wording; the colours and line styles; any other game; shared assets; data/games.json and listing (not in this contract); the files under COORDINATION.

SUCCESS CONDITION: Jon's lines appear exactly where listed; at 1920x1080 and 1366x768 the game fills the screen with the triangle at least half the screen's height and nothing needs scrolling; phones unchanged; the verifier (with its new checks and plants), the phone-fit checks and the theme check pass. Committed, PR open, Gate green, entry in docs/handover/cloud.md; stop for Project Claude's review and Jon's "merge".

STOP IF: any line would need rewording to fit (report it, don't edit Jon's text); the large-screen layout breaks phone-fit or the theme check; a change is needed outside the game's file, the verifier and cloud.md.
