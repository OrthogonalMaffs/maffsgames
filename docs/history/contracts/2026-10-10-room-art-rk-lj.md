MODEL: sonnet · effort: medium · LANE: home

TASK: File The Rightful King's and The Library Jam's pictures (three each) and wire them into both rooms, keeping both rooms unreleased.

ROOT CAUSE: Both rooms were built before their art (ART-PENDING, #244). Jon generated and approved all six pictures on 10 Oct (22:20-22:42); neither room.js has `art` yet, and some alts no longer match the pictures.

CLASS CHECK: Local. Two rooms' assets and their own room.js files; the art pipeline and engine already exist and were used for Car Trap v2 (#246). Nothing shared changes.

EXACT CHANGE:
1. Take Jon's six images from [Jon: folder, or attached]: rightful-king-{scene,fail,win}, library-jam-{scene,fail,win}. Convert each to docs/art/<name>.webp at 1600x873, WebP q80 (canon §11.2), cropping, never stretching. The Library Jam's fail and win are about 1024 px wide: upscale them to 1600x873 and report how they compare with the scene. Check all six for a watermark, readable text or a brand mark.
2. library-jam-scene, -fail, -win: blank the squiggle "writing" on the papers pinned on the right-hand wall (as Car Trap's badges were blanked). Nothing else is retouched.
3. rightful-king/room.js: `art: 'rightful-king'`; remove the "ART: none yet" note.
   - sceneAlt: add "a yellow sticky note on the edge of the teacher's monitor, and a small printer with paper in its tray" to the desk sentence.
   - failAlt -> 'The same IT suite at night, lit only by the big display. The crown is lowered and glowing, the spotlight full on, sparkles frozen mid-fall. The server cupboard is shut.'
   - winAlt: unchanged.
4. library-jam/room.js: `art: 'library-jam'`; remove the "ART: none yet" note.
   - sceneAlt: unchanged unless a detail is plainly wrong against the picture (report any change).
   - failAlt -> 'The same backroom at the end of the day, nearly dark, the high window a dull orange. The belt is still, the arm frozen with its book, and the wire bin is empty. The screen on the desk glows red.'
   - winAlt -> 'The same backroom. The wire bin is piled high with books and the arm is raised, its claw open and empty. The screen on the desk glows green.'
5. Keep both RULE comments: no `missArt` on any lock in either room.
6. Handover entry in docs/handover/home.md: art filed; Jon can play-test both rooms with pictures at /escape-rooms/rightful-king/play.html and /escape-rooms/library-jam/play.html.

DO NOT TOUCH: Either room's index.html (holding pages stay: no release, hub card, stars chip, sitemap entry or counts); any other room's pictures or room.js; engine.js, teacher.js, engine.css; the it-vengeance art (history); the cloud lane's handover.

SUCCESS CONDITION: Six WebP files at 1600x873 in docs/art/. Each play.html shows its scene on start, its win picture on a win and its fail picture at time-out, in Chromium at 1280 and 320 px. check-escape-rooms and the escape-room art test pass. CI green. Handover documented. Merged.

STOP IF: Any image carries a watermark, readable text or brand mark that cropping or the wall-paper blanking cannot remove. The 1600x873 crop would cut off a story object (the crown, the server cupboard, the teacher's desk; the gripper arm, the bin, the drop-box, the desk screen). The upscaled Library Jam pictures are visibly soft beside the scene (show Jon before merging). Any check expects a released room's fields before release.
