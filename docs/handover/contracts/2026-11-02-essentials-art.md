CONTRACT: ESSENTIALS-ART
Tier: Medium · Lane: cloud · Implementer: Claude Code (cloud)
EXCEPTION (Jon, 2 Nov 2026, 20:37): one PR for all eight games, art only, instead of one game per PR.

START
Work on the existing branch art/essentials-batch-1 (Jon's images in art-inbox/). Merge origin/main into it first.
Claim all eight games (all listed) on scripts/answer-lock-state.json in ONE commit of its own; remove the claims in
the fix PR.

TASK
Put each game's new illustration on its start screen, converted to the house frame, and leave no source images
behind.

ROOT CAUSE
Jon commissioned start-screen illustrations to give these games character. The source files are full-size PNGs/JPGs
in art-inbox/ on this branch and one on main (games/factor-race/Gemini_Generated_Image_r5ueyyr5ueyyr5ue.jpg, a direct
upload, be4fc751); none is in the house format or wired into a page.

CLASS CHECK
Local: eight games each gaining one image in the same established pattern (I Found a Mark's assets/ precedent). No
shared code changes. Do not build a shared art component for this.

EXACT CHANGE
1. Convert with Pillow, exactly, for each source: open, convert("RGB"); w, h = size; new_h = max(873, round(h * 1600 / w));
   resize((1600, new_h), LANCZOS); crop centred vertically to (1600, 873); save WEBP quality=80 method=6 (no metadata).
   free-daily-pizza.webp is already 1600×873: copy it byte-identical.
   | Game (slug)            | Source                                                   | Destination                          |
   |------------------------|----------------------------------------------------------|--------------------------------------|
   | squared-squirrel       | art-inbox/squared-squirrel.png                           | games/squared-squirrel/assets/start.webp |
   | take-a-walk            | art-inbox/take-a-walk.png                                | games/take-a-walk/assets/start.webp  |
   | estimation-golf        | art-inbox/estimation-golf.png                            | games/estimation-golf/assets/start.webp |
   | formula-forge          | art-inbox/formula-forge.png                              | games/formula-forge/assets/start.webp |
   | just-pythag-it-bruv    | art-inbox/just-pythag-it-bruv.png                        | games/just-pythag-it-bruv/assets/start.webp |
   | factor-race            | games/factor-race/Gemini_Generated_Image_r5ueyyr5ueyyr5ue.jpg (on main) | games/factor-race/assets/start.webp |
   | free-daily-pizza       | art-inbox/free-daily-pizza.webp                          | games/free-daily-pizza/assets/start.webp |
   | i-found-a-mark         | art-inbox/i-found-a-mark.png                             | games/i-found-a-mark/assets/scene.webp |
2. Each start screen (not I Found a Mark): add <img src="assets/start.webp" width="1600" height="873" alt="..."> at the
   top of the start screen's content, full width of its card, rounded corners matching the card, height:auto. Keep
   every existing element; do not remove an existing SVG or text. Alt text, exactly:
   - squared-squirrel: "Football pitches across a valley, with a wooden squirrel statue in a small square garden"
   - take-a-walk: "A cricket ground with a mower striping the grass and a line marker painting the boundary"
   - estimation-golf: "A driving range at sunset with flags at 100, 200 and about 300 yards"
   - formula-forge: "A blacksmith's forge with maths symbols hanging on the wall above an anvil"
   - just-pythag-it-bruv: "A building site with scaffolding, a ladder against a wall and set squares on a workbench"
   - factor-race: "Two racing cars numbered 24 and 12 passing a scoreboard with 8 lights for 24 and 6 for 12"
   - free-daily-pizza: "A pizza cut into ten slices on a board, with two slices gone and one half eaten"
3. I Found a Mark: replace the start screen's sofa image with assets/scene.webp (same width/height attributes; alt
   "A living room with a green sofa and a gold coin on the floor beneath it"), and remove the start screen's
   gap-coin overlay (<img class="gap-coin">) and its .gap-coin CSS, since the scene draws its own coin. Keep
   assets/coin.webp (the marks bar uses it). Delete assets/sofa.webp only if nothing references it afterwards;
   update the CSS comment that names it.
4. Remove all source images: git rm -r art-inbox/ (all ten files, including the rejected and held ones) and
   git rm games/factor-race/Gemini_Generated_Image_r5ueyyr5ueyyr5ue.jpg. The PR diff must contain no PNG/JPG.
5. Phone fit, measured by a one-off script (not added to the repo), table in the PR: for each game at 320×568,
   375×667 and 390×844, the start screen's Start control is above the fold. Desktop 1280×720 screenshot not needed.

DO NOT TOUCH
- Game logic, questions, banks, scoring, themes and palettes; base tokens; shared assets; games.json, homepage,
  Essentials, /updates/.
- Any game not in the table; docs/art/.
- AGENTS.md, CLAUDE.md, docs/agent-workflow.md, docs/rules/, canon (RULEBOOK may still be open).

SUCCESS CONDITION
Eight start screens show their image; I Found a Mark's start screen shows the scene with no overlay coin; every
image 1600×873 WebP under 450 KB; no PNG/JPG in the diff; art-inbox/ and the main-branch JPG gone; claims added in
one commit and removed in the fix PR; phone-fit table all above the fold (or STOP below); Gate green (standing
ruling: no local check-changed.py; run each touched game's own verifier if it exists); handover current; stop at
Gate green for Project Claude review and Jon's "merge".

STOP IF
- A source file is missing or not the size recorded: squared-squirrel 1698×926, take-a-walk 1688×932,
  estimation-golf 1698×926, formula-forge 1698×926, just-pythag-it-bruv 1699×926, i-found-a-mark 1698×926,
  free-daily-pizza 1600×873 WebP, factor-race 2784×1536 JPG.
- A game's Start control cannot stay above the fold at 320×568 with the image: leave that game's image out, list it,
  and carry on with the rest.
- A game's existing verifier fails because of the image (report; do not edit verifiers beyond a selector fix).
- Any change is needed outside the eight games' folders, the claim file and the handover.
