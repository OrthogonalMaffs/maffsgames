LANE: home (Codex) · TIER: Shared (new game) · after #669 and #671 merge

TASK: Build "Whose Side Are You On?" (games/whose-side-are-you-on/), stages 1–4 of the approved spec, live but UNLISTED by tonight so Jon can use it in class tomorrow.

ROOT CAUSE: Nothing on the site teaches labelling a right-angled triangle's sides (HYP/OPP/ADJ) from a marked angle, the step before SOHCAHTOA where Foundation students lose marks. Spec approved by Jon, 5 Nov: claude/trig-sides-spec-2026-11-05.md in the project (copied below in full in the PR body).

CLASS CHECK: Not a class: a new single-file game. It reuses the shared game scaffolding (theme, footer, analytics, keypad not needed) and adds nothing to shared code.

EXACT CHANGE:
1. games/whose-side-are-you-on/index.html, single file, KaTeX via CDN, dark theme (GCSE row, canon §7.5.1).
2. Colours fixed across every stage: HYP #D55E00 solid line, letter H; OPP #0072B2 dashed, letter O; ADJ #009E73 dotted, letter A. Colour never the only cue. HYP/OPP/ADJ words in text use the same colours.
3. Triangles generated: every rotation and reflection, tall/thin and short/wide, θ at either acute corner, right-angle square always drawn. Stages 2–4 use Pythagorean triples and multiples (3-4-5, 5-12-13, 8-15-17, 7-24-25, 20-21-29, 6-8-10 …).
4. Stage 1, Tap the side: "Tap the OPPOSITE" etc.; the student taps the side on the diagram (tap target ≥44px deep along each side). Right: the side lights in its colour with its letter. Wrong: the correct side lights, plus one feedback line from the spec. HYP questions first in each run.
5. Stage 2, Build the fraction: lengths shown; "OPP over HYP"; tap a side into the numerator, then the denominator.
6. Stage 3, Name it: coloured fraction → pick sin θ / cos θ / tan θ; then the reverse.
7. Stage 4, Which function?: one side known (length), one wanted ("?"), θ marked; pick sin/cos/tan. No calculation.
8. Streak, no lives; speed adds to score, never marks wrong. Answers matched by dataset.val. ≥50 distinct items per stage.
9. A verifier (scripts/verify-whose-side-are-you-on.py, ci-line header, following the existing verify-*.py pattern): for every stage and a large seeded sample, recompute which side is HYP/OPP/ADJ from the triangle's geometry (not from the game's labels), every fraction, every function choice; plant one wrong label and one wrong function and require both caught.
10. Unlisted: not in data/games.json, the portal, /essentials/ or the sitemap; noindex until listed. Roster: add it in the unlisted section only.

DO NOT TOUCH: stage 5 (calculations; a later contract); the portal, games.json, /essentials/, sitemap, /updates/; shared assets; any other game.

SUCCESS CONDITION: Stages 1–4 play end to end at 320px and desktop; the verifier passes and catches both plants; phone-fit passes; Gate green; Jon plays it on his phone and says "merge"; merged and live at maffsgames.co.uk/games/whose-side-are-you-on/. Entry in docs/handover/home.md.

STOP IF: not at a green Gate by 23:00 tonight (report how far it got, push the branch, stop); any stage needs a shared-code change; the geometry check and the game's labels disagree on any triangle.

==================== JON'S ANSWERS (5 Nov 18:30), verbatim ====================

Answers (Jon, 5 Nov 18:30), thank you:
1. Spec below, verbatim and approved; use its feedback wording exactly.
2. You build it, on claude/whose-side-are-you-on in your own worktree. Codex will not touch it: it is only merging #669/#671 tonight, then stops.
3. Start now; don't wait for #671. #671 was reviewed and passed by Project Claude at 17:45; its merge conflict is Codex's to resolve. Do not touch docs/handover/home.md, escape-room files or equatle until Codex reports done; rebase on main and add your home.md entry just before the PR.
Review: when your Gate is green, report and stop. Project Claude reviews tonight, then Jon plays it on his phone and says "merge". No /updates/ line (unlisted), as you said.

--- SPEC: claude/trig-sides-spec-2026-11-05.md ---
# Spec: trig side-labelling game, "Whose Side Are You On?" (slug `whose-side-are-you-on`) (5 Nov 2026)
Status: approved by Jon, 5 Nov 2026. Tonight's build: stages 1–4 only, unlisted.

## Purpose
Teach the skill that comes before SOHCAHTOA: labelling a right-angled triangle's sides from a marked angle, then linking those labels to sin, cos and tan, in small stages. Students working at grades 1–3 and post-16 resitters lose Foundation trig marks at the labelling step, before any calculation. Nothing on the site teaches it: Trig Wars, Trig Worms and Trig Identity Duel all assume it.
- Level: GCSE (Foundation content). Curriculum: DfE GCSE content G20 (trigonometric ratios in right-angled triangles); AQA 8300, Edexcel 1MA1, OCR J560.
- Feel: quick-fire, like Prime or Composite. Speed feeds the score and streak; it never marks an answer wrong. Streak, no lives.

## The colour system (fixed across every stage and every play)
| Side | Letter | Colour | Line |
| Hypotenuse | H | red-orange #D55E00 | solid |
| Opposite | O | blue #0072B2 | dashed |
| Adjacent | A | bluish green #009E73 | dotted |
Jon's rule: each side keeps the same colour every time, so repetition builds the habit. Colour-blind-safe palette; the letter and line style carry the meaning too, so colour is never the only cue. The same colours are used for the words HYP, OPP, ADJ wherever they appear in game text and fractions. Check contrast on the dark background.

## Triangles
- Generated, not hand-typed. Every orientation from stage 1: rotated through all four quadrants, reflected, tall and thin, short and wide. θ at either acute corner. No rule based on which side is "the bottom" or "the upright" works.
- Right angle always marked with the square symbol; the marked angle with θ (KaTeX).
- Stages 2 onward use whole-number triangles (Pythagorean triples and multiples: 3-4-5, 5-12-13, 8-15-17, 7-24-25, 20-21-29, 6-8-10 …) so every fraction is exact.
- At least 50 distinct items per stage, every answer recomputed by the verifier.

## Stages
1. Tap the side. "Tap the OPPOSITE." The student taps a side on the diagram. Right: it lights up in its colour with its letter. Wrong: the correct side lights up, and one line of feedback names the misconception (below). Hypotenuse questions come first in each run, because H anchors the other two.
2. Build the fraction. Sides carry lengths. "OPP over HYP." The student taps a side into the top of the fraction, then one into the bottom: 5/13. No sin, cos or tan yet.
3. Name it. A coloured fraction with θ marked: OPP/HYP, ADJ/HYP or OPP/ADJ. The student picks sin θ, cos θ or tan θ. Then the reverse: given sin θ, pick the fraction.
4. Which function? One side known (marked with its length), one side wanted (marked "?"), θ given. The student picks sin, cos or tan. No calculation; spotting only.
5. (NOT TONIGHT) Put it together: find a missing side, then a missing angle; calculator; 1 d.p.

## Misconception feedback (one line each)
- Picked the side that is vertical on screen as OPP: "Opposite means across from θ, not upright. Turn the triangle in your head."
- Called the hypotenuse ADJ because it touches θ: "Two sides touch θ. The longest one, across from the right angle, is always HYP."
- Labelled from the right angle: "Label from θ, not from the square corner."
- Stage 4, picked the function from the known side alone: "Use both: the side you know AND the side you want."

## Platform rules
Single-file HTML; KaTeX for θ and fractions; answers by dataset.val; dark theme (GCSE row, canon §7.5.1); phone-fit at 320px (each side's tap target at least 44px deep along its length); verifier in CI recomputing every answer from the geometry, every orientation, every fraction; analytics as standard.

==================== AMENDMENTS ====================

AMENDMENT 1 (Jon, 5 Nov): thank you, both clashes are the contract's error; the repo wins.
1. Theme: build to theme.css with the data-theme check-theme.py gives, straight into MIGRATED, as canon §7.5.1 says for a new game. Ignore "dark theme" in the contract and spec.
2. games.json and the checker files: do exactly what the existing unlisted-for-Jon-to-play games did (hc-factor, as-you-can-see): a games.json entry, the roster's Unlisted section, and whatever checker entries that precedent needed. "Unlisted" means not on the portal, /essentials/ or the sitemap; it does not mean absent from games.json.
3. Side colours on a light background: keep the three hues fixed (H #D55E00, O #0072B2, A #009E73). Lines and fills as given (they need 3:1, which they meet). Where HYP/OPP/ADJ appear as text, meet WCAG contrast: bold at 19px or larger (3:1), or a darker shade of the same hue for smaller text (4.5:1). Letters and line styles unchanged.
STOP IF any of these still fails a check after following the precedent.

AMENDMENT 2 (Jon, 5 Nov): the three side colours (H #D55E00, O #0072B2, A #009E73) are used for the sides and the HYP/OPP/ADJ words ONLY: never for buttons, headings, score, streak or right/wrong feedback. Right/wrong feedback must not use green or red at all, so it can never be read as ADJ or HYP: show it with a tick or cross symbol and a word ("Right" / "Not quite"), plus the side lighting up in its own colour. Everything else uses the theme's normal tokens. STOP IF the theme's feedback styles can't be used without green/red; report rather than override a base token.
