# WHOSE-SIDE-ART (Jon, via Project Claude, 6 Nov 2026), verbatim

The contract carried no name; the cloud lane calls it WHOSE-SIDE-ART.

LANE: cloud (fresh session) · TIER: Shared · after #682 (WHOSE-SIDE-LOOK) merges, from current main

COORDINATION: the home lane has codex/escape-herrings open (escape-room engine). Do not touch escape-rooms/, tools/pack-generator/ or docs/handover/home.md. The #682 close-out PR may be open and edit docs/handover/cloud.md: rebase on main before your PR, keep every entry, STOP rather than drop one. Record in docs/handover/cloud.md.

TASK: Put Jon's skate-ramp illustration on the start screen of "Whose Side Are You On?", with θ drawn over the ramp's tip so the picture's colours are mathematically right.

ROOT CAUSE: The start screen has no image (Jon, 6 Nov: "it needs an image"). Jon's image is on branch art-inbox at whose-side-are-you-on.png (commit 9ed06af, 1698x926 PNG, 2,154,880 bytes): a wooden skate ramp seen side-on, slope red-orange, upright blue, base green, no lettering; Project Claude checked it at full size on 5 Nov (right angle true, no generator mark). Without θ the picture says "upright = opposite, bottom = adjacent", the exact misconception the game fights; with θ at the ramp's bottom-right tip, blue really is OPP and green really is ADJ.

CLASS CHECK: Local: one game gaining one image in the established pattern (ESSENTIALS-ART, I Found a Mark's assets/). No shared code.

EXACT CHANGE:
1. Convert with Pillow exactly as ESSENTIALS-ART did: open, convert("RGB"); new_h = max(873, round(h*1600/w)); resize((1600, new_h), LANCZOS); crop centred vertically to (1600, 873); save WEBP quality=80 method=6, no metadata, to games/whose-side-are-you-on/assets/start.webp.
2. Start screen: <img src="assets/start.webp" width="1600" height="873" alt="A wooden skate ramp seen side-on: its slope, upright and base form a right-angled triangle, with the angle θ marked at the bottom of the slope"> at the top of the start card, full card width, rounded corners matching the card, height:auto, inside a position:relative wrapper. On wide screens (#682's two-column layout) it sits at the top of the start screen, not squeezed into a column.
3. θ overlay (never baked into the image): an absolutely positioned element over the ramp's bottom-right tip, where the red slope meets the green base (about (1450, 790) in the source's 1698x926 coordinates: measure the exact point on the converted image and give it in percentages so it scales). It draws a small angle arc between the slope and the base, opening to the left inside the triangle, and a KaTeX θ just inside the arc, in the text colour, readable on the concrete and the wood at phone and desktop sizes.
4. The PR adds only the WebP: no PNG in the diff. Jon deletes the art-inbox branch after merge.
5. Verifier: the start screen shows assets/start.webp; θ is on screen over the image, within 6% of the measured tip at 320, 390 and 1920 widths; Start stays above the fold at 320x568, 375x667 and 390x844, normal and Aa; plant a wrong θ position and require it caught.
6. /updates/: no line (unlisted).

DO NOT TOUCH: the image's content (no edits beyond the house conversion); game play, text and Jon's lines; colours; #682's layout beyond placing the image; any other game; shared assets; the files under COORDINATION.

SUCCESS CONDITION: The start screen shows the ramp with θ at its tip on phone and desktop; the WebP is 1600x873 and under 450 KB; no PNG in the diff; the verifier's new checks pass with the plant caught; phone-fit passes. Committed, PR open, Gate green, entry in docs/handover/cloud.md; stop for Project Claude's review and Jon's "merge".

STOP IF: the art-inbox file is not a 1698x926 PNG of 2,154,880 bytes; Start cannot stay above the fold at 320x568 with the image (report; do not shrink the game); the θ overlay cannot sit cleanly on the tip at every size.
