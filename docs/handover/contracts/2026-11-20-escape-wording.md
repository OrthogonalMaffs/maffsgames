ESCAPE-WORDING, one part.
LANE: cloud. Send now. TIER: Small. MODEL: Claude Code, Sonnet 5.5, medium effort.

TASK: Three lock clues in two escape rooms are reworded so a careful student can't read them a second way. No answer changes.

ROOT CAUSE: Project Claude read all 51 locks in the 16 rooms with every variant's numbers (20 Nov 2026), on main 527f8b8, unchanged on 3d6ce66:
- christmas-tree-fiasco/room.js:46, Eric's clipboard: "WARMS {{ct.g}} °C EVERY {{ct.h}} HOURS" can be read as a steady rate (the key, hints and solve) or as jumps of {{ct.g}} °C every {{ct.h}} hours. The two readings give different answers in 6 of the 10 sets (set 0: -4 °C to 16 °C, 8 °C every 2 hours: 5 hours steadily, 6 in jumps).
- christmas-tree-fiasco/room.js:48, the leaflet: "STAND ADDS {{sc.s}} cm" sits beside the leaflet's scaled height, so the stand can be read as a leaflet measurement to scale up.
- heatwave-mutiny/room.js:127-128, the patrol brief: "when it is safe to cross" never says the first such time (only the slider's range rules out later ones).

CLASS CHECK: Local: three authored strings, each a one-off wording choice in its own room. The engine, variant libraries and checks are sound.

EXACT CHANGE:
1. First commit: close out CORE-PAPERS-NO-LETTERS (#843, merge 64f56a6, run 44686407010: main's runs on its merge commit from the API, recorded in its cloud.md entry; contract to docs/history/contracts/). Save this contract verbatim as docs/handover/contracts/2026-11-20-escape-wording.md.
2. christmas-tree-fiasco/room.js:46: "WARMS {{ct.g}} °C EVERY {{ct.h}} HOURS ONCE UNLOADED" becomes "WARMS AT A CONSTANT RATE: {{ct.g}} °C EVERY {{ct.h}} HOURS ONCE UNLOADED" (Jon, 20 Nov 2026).
3. christmas-tree-fiasco/room.js:48: "STAND ADDS {{sc.s}} cm" becomes "THE REAL STAND ADDS {{sc.s}} cm" (Jon).
4. heatwave-mutiny/room.js:127-128: "Set it to the number of minutes after the Supervisors set off when it is safe to cross" becomes "Set it to the number of minutes after the Supervisors set off until the first time it is safe to cross: the first time all three are back together" (Jon), the rest of the sentence unchanged.
5. If either room's teacher page, art alt text, pack-generator config (tools/pack-generator/rooms/) or verifier quotes any of the three old strings, change it to match. Run scripts/check-escape-rooms.py and every escape-room and pack check; all pass.
6. cloud.md entry. No /updates/ line.
7. PR, Gate and phone-fit-full green, merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line. No draft PR.

DO NOT TOUCH: any variant library, answer, hint, solve, missSays or wrongLine; the numbers; any other room; schools/assets/; canon; docs/handover/home.md; any game.

SUCCESS CONDITION: the three strings read as above in the live rooms; no answer changed; every escape-room and pack check passes; #843 closed out; merged by merge-pr.py with a GREEN last line; cloud.md records it all.

STOP IF: a check forbids the new wording (e.g. a rule on words in prose): report it, change nothing; a printed pack already sold or listed carries the old wording (report which; don't rebuild it); merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
END OF CONTRACT
