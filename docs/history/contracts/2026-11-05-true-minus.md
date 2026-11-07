CONTRACT: TRUE-MINUS (name given by the implementer; Jon's contract of 5 Nov 2026 carried no name)
Tier: Shared · Lane: cloud, lane exception (Jon's answers below) · Implementer: Claude Code (cloud)

TASK: Every negative number a room prints from a variant token shows a true minus sign (U+2212), in the room, the teacher page and the printable pack.

ROOT CAUSE: The room engine prints tokens with String(value), so {{ct.start}} = -4 prints "-4" (ASCII hyphen-minus) beside the authored "−18 °C" in the same clue. A hyphen reads as a dash, and this lock is the negative-numbers lock.

CLASS CHECK: Yes, a class. The same token-to-text step is written four times: escape-rooms/assets/engine.js fill() (~line 189), escape-rooms/assets/teacher.js fill() (~line 62), tools/pack-generator/build_pack.py filler() (~line 370), and scripts/check-escape-rooms.py's clue rendering (~line 115), which must see the text students see or its answer-in-clue check is checking the wrong string. The fix is one formatting rule per language, used by every renderer, with a test that keeps the two languages in step. Fixing only the room engine would leave the teacher page and the pack printing hyphens.

EXACT CHANGE:
1. JS: one function, formatToken(v): a number below zero, or a string matching ^-\d, becomes "−" + the rest; every other value is unchanged. Put it in one shared file under escape-rooms/assets/ that engine.js and teacher.js both load (or in engine.js, if teacher.html already loads engine.js); both fill() functions call it. No second copy.
2. Python: the same rule as format_token() in scripts/escape_set_checks.py; build_pack.py's filler() and check-escape-rooms.py's clue rendering both import it.
3. A parity test (a new scripts/test-escape-format.py with a ci-line header): a fixed table of values (-4, -0.5, "-4", 0, 4, "4-6", "−4", "x", null) gives identical output from the JS function (run in Node or Chromium) and the Python one.
4. A guard: render every variant of every room's clue, hint, solve and teacher strings through the shared rule, and fail any ASCII hyphen-minus directly before a digit. Add it to check-escape-rooms.py, with a planted fault in its self-test.
5. Values used for answer checking (answerOf, missOf, the keypad and dial) stay raw numbers: formatting is for display only.

BEFORE MERGE: #668 (CHRISTMAS-ROOM close-out) is green and waits for the home lane to merge it. Once it lands, rebase on main; if docs/handover/cloud.md or CLAUDE.md conflict, keep every entry intact and STOP rather than drop one.

DO NOT TOUCH: answer checking, variant libraries (escape-rooms/variants.json, every room.js's variant data), authored prose, gen-escape-variants.py's rules, check-dash-minus.py's rule (a different fault: a dash before a number), the Christmas pack art or config.

SUCCESS CONDITION: In the Christmas room, teacher page and a selftest pack, every negative token prints with U+2212. The parity test and the new guard pass, each with a planted fault caught. All existing escape-room tests, the play-through and check-changed.py pass. Committed, PR open, entry in docs/handover/cloud.md.

STOP IF: fill()'s output is ever parsed back or compared (for example a keypad display read as a number), or any room has a negative ANSWER (the keypad would need a minus key; report, don't build one); the shared JS file can't be loaded by teacher.html without changing how teacher pages load; any room's rendered text changes other than hyphen to minus.

JON'S ANSWERS (5 Nov 2026, to the implementer's questions before any edit), verbatim as chosen:
- Lane and tier: "Cloud, Shared, exception": cloud lane, Shared tier, with a lane exception for the four renderers, escape_set_checks.py, the new test and this contract's files; stop at a green Gate for Project Claude's review and Jon's "merge".
- Local suite: "CLOUD-LEAN: Gate only": the parity test, the new guard, the escape tests, the pack selftest, the play-through and any changed script's selftest by hand; the Gate covers the rest (check-changed.py is not run in the cloud lane).
- JS home: "rating.js (Recommended)": formatToken in escape-rooms/assets/rating.js (window.MaffsEscapeRating.formatToken), which every live room's index.html and teacher.html already load; no page's script tags change.
- Guard rule: "Literal rule + allowlist": fail every hyphen-minus before a digit, with a shrink-only allowlist holding the one entry (roll-for-initiative onOpen "R-1", authored prose), on canon §7.8.4's warn-first pattern.
