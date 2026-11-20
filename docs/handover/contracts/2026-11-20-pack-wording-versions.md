PACK-WORDING-VERSIONS, one part.
LANE: cloud. Send now. TIER: Small. MODEL: Claude Code, Sonnet 5.5, low effort.

TASK: The Christmas Tree Fiasco and Heatwave Mutiny printable packs get new version numbers, so the copies Jon rebuilds with ESCAPE-WORDING's clues (#845) never share a name or footer with the ones already on Tes.

ROOT CAUSE: On main cbad9b0. #845 changed three clue lines in the two rooms; the packs print them, but tools/pack-generator/rooms/christmas-tree-fiasco/config.json:3 is still "pack_version": "3" (on Tes as 13656567) and heatwave-mutiny/config.json:3 "2" (Tes 13669810). The README rule (Jon, 17 Nov 2026, FINAL-PADLOCK-FAIR): two versions of a pack never share a name.

CLASS CHECK: Local: two config values. The version rule and the build are sound.

EXACT CHANGE:
1. First commit: close out ESCAPE-WORDING (#845, merge e769730, run 44690793429: main's runs from the API into its cloud.md entry; contract to docs/history/contracts/). Save this contract verbatim as docs/handover/contracts/2026-11-20-pack-wording-versions.md.
2. christmas-tree-fiasco/config.json: "pack_version" "3" -> "4"; "wording_approved" date -> "2026-11-20" (Jon approved the new clipboard and leaflet lines today). heatwave-mutiny/config.json: "pack_version" "2" -> "3"; "wording_approved" date -> "2026-11-20".
3. Build both with --final here to prove they build (tools/pack-generator/build_pack.py <room> --final); report pages, size and any fit line for the clipboard, leaflet and Patrol brief. Do not commit, upload or attach the PDFs (README rule). Jon's copies are built separately.
4. Wherever the repo records the Tes listing versions (grep "13656567", "13669810", PACKS-V2-UPLOAD), note: Christmas v4 and Heatwave v3 replace v3 and v2 on Tes, uploaded by Jon. One todo row PACK-RELIST only if no such record exists. Add a §4 todo row ESCAPE-KEYPAD-FLAKY: test-escape-keypad failed once on kiln-disaster while 15 checks ran in parallel during #845, then passed four times alone. cloud.md entry. No /updates/ line.
5. PR, Gate green, merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line. No draft PR.

DO NOT TOUCH: any room's room.js, art or clue text; the build script; any other pack's config; schools/assets/; canon; docs/handover/home.md.

SUCCESS CONDITION: both configs carry the new versions and today's approval date; both packs build with --final; the Tes record notes the replacements; ESCAPE-KEYPAD-FLAKY row in; ESCAPE-WORDING closed out; merged GREEN; cloud.md records it.

STOP IF: either --final build fails (report the reason); a clue no longer fits its art; merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
END OF CONTRACT
