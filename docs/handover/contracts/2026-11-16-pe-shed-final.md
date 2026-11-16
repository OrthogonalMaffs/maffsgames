TOOL: Claude Code (home lane). SIZE: small-medium (one optional generator field, one room config, one teacher-page sync, final build). Recommended: Opus, medium effort.
MERGE TIMING: one merge heading for main at a time; nothing else is in a Gate now.

TASK: Make The P.E. Store Rebellion's print pack final: print who is speaking above the start read-out, mark the wording approved, and bring the live teacher page's variant-0 example in line with the fixed variant 0.

ROOT CAUSE:
1. The pack's start read-out (page 1, "Read this at the start", from room.hook via build_pack.py's read-out function near line 1777) is the PE teacher's speech, but nothing says so until the italic paragraph after it; a teacher reading it aloud from paper does not know whose voice it is or why (Jon, 16 Nov 21:12: "if the teacher is talking as the PE teacher, they need to know who he is and why they're saying it"). The generator has no way to print a speaker line.
2. PE-SHED-PACK (#801) changed variant 0's sprinkler to 9 m and 27π (was 12 m and 48π), but escape-rooms/pe-shed-rebellion/teacher.html still quotes the old example: line 41 "the 48&pi; limit", line 42 "the 12 m reach", line 48 notes "48&pi; over 144&pi; cancels to a third ... 150.796&hellip; over 452.389&hellip;".
3. config.json still has "wording_approved": null; Jon approved the rest of the pack's wording on 16 Nov 21:13 ("the rest I'm happy with").

CLASS CHECK: 1 is a generator gap shared by every pack (any room whose hook is spoken in a character's voice has the same problem), so it is fixed in build_pack.py as an optional, validated per-room config field, default absent, so the eight packs already built (and those on Tes) stay byte-identical. 2 is local to this room's teacher page (it holds variant 0's own example). 3 is this room's config.

EXACT CHANGE:
First commit: PE-SHED-PACK's close-out (AGENTS.md rule): #801 merged as 6f9498b via merge-pr.py, last line "main 6f9498b run 43942870305: GREEN", exit 0; check-site 43942870305 success, phone-fit-full 43942870330 success, push-triggered. Update its home handover entry (it says "MERGED: pending") and move its contract to docs/history/contracts/. Save this contract verbatim at docs/handover/contracts/2026-11-16-pe-shed-final.md.
1. build_pack.py: optional config field "readout_voice" (non-empty plain string, no {{token}}, no digit-bearing figure that fails the figure-binding check). When present, the start read-out prints it as its first line, in italics, before the hook. Validated in load_config(); documented in the module docstring and README.md beside "printed"/"caption"/"answer_units"/"lock_words". Every existing wording check (sentence, figure binding, fixed-penalty) applies to it. scripts/test-pack-generator.py: plants that must be caught: readout_voice empty; containing {{token}}; a non-string. Control: a valid readout_voice prints on page 1 above the hook.
2. tools/pack-generator/rooms/pe-shed-rebellion/config.json: "readout_voice": "Read this as the PE teacher, standing in the store doorway. It's four degrees and raining, and he's sending the class out on a six-kilometre cross-country run." (Use the generator's own apostrophe handling, as the room's text does.) "wording_approved": {"by": "Jon", "date": "2026-11-16"}.
3. escape-rooms/pe-shed-rebellion/teacher.html: lines 41, 42 and 48 to match variant 0 as it now is in escape-rooms/variants.json (27π limit, 9 m reach, 27π over 81π cancels to a third, and the two decimals recomputed from 27π and 81π to the same 3 places, 84.823… and 254.469…; verify both). Nothing else on the page.
4. docs/todo.md: close PE-SHED-PACK-APPROVE. Add one row PACK-READOUT-VOICE: check the other eight rooms' start read-outs for an unnamed speaker; any fix needs Jon's go-ahead because those packs are on Tes and are not to be republished without it. Home handover entry.

Run only the checks this contract names and the Gate: the pack build (draft and --final), test-pack-generator.py with self-test, check-escape-rooms.py, and the teacher-page check(s) that already cover teacher.html. No optional all-game local runs.

DO NOT TOUCH: the live room's room.js (hook, brief, hints, variants); the other eight rooms' configs or output; the art; any game; Gate files; the cloud handover; scripts/audit-answers.py.

SUCCESS CONDITION:
- `python -X utf8 tools/pack-generator/build_pack.py pe-shed-rebellion --final` builds 36 pages, 6 sets, no DRAFT badge, with the readout_voice line in italics above the start read-out on page 1; set answers and final padlocks unchanged from #801 (A 7455, B 4251, C 730, D 6248, E 760, F 23616).
- The other eight packs built before and after are byte-identical (HTML and build logs); say how compared.
- teacher.html's variant-0 lines match variants.json; its existing checks pass.
- test-pack-generator.py: every plant caught, every control passes.
- PR merged on green via `python -X utf8 scripts/merge-pr.py <n>`; report its last line and exit status and main's check-site and phone-fit-full run IDs on the merge commit. Home handover documented.

STOP IF:
- Any set's answers or padlock target change.
- Any other pack changes by one byte.
- The readout_voice text fails a wording check as written: report the message; do not reword Jon's text.
- The teacher page's example is generated from variants.json elsewhere and editing lines 41-48 by hand would be overwritten (report where it comes from).
- merge-pr.py reports it cannot reach GitHub (a 5xx during the Gate wait may be retried once with the same script).
