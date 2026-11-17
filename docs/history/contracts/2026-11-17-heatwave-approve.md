LANE: cloud (Claude Code on the web). Send now: the cloud lane is free after #808.
RECOMMENDED: Sonnet 5.5, medium effort. It's a one-field config change plus docs.

TASK: HEATWAVE-APPROVE. Record Jon's approval of The Heatwave Mutiny print pack's wording, so it builds with --final and has no DRAFT marks.

ROOT CAUSE: tools/pack-generator/rooms/heatwave-mutiny/config.json line 8 is "wording_approved": null. Jon proofread the v2 PDF built from main 58e4ea7 and approved it on 17 Nov 2026 ("approved, please remove the draft markings").

CLASS CHECK: Local. Approval is one field per room, in that room's config, by design (tools/pack-generator/README.md "Approval and the DRAFT badge"). The generator already handles every room's DRAFT marks from that field, so no shared code changes.

EXACT CHANGE:
0. First commit: #808 PADLOCK-EASIEST-HINT close-out, per AGENTS.md's close-out rule. Merge commit 58e4ea7; main check-site 44052013877 and phone-fit-full 44052013837, both success. Move the contract to docs/history/contracts/ if it is not already there.
1. In tools/pack-generator/rooms/heatwave-mutiny/config.json, replace
   "wording_approved": null,
   with
   "wording_approved": {"by": "Jon", "date": "2026-11-17"},
2. Build python -X utf8 tools/pack-generator/build_pack.py heatwave-mutiny --final. It must succeed and write dist-packs/heatwave-mutiny-pack-v2.pdf, with no DRAFT text on any page. Do not commit the PDF.
3. In docs/todo.md:
   - Close the HEATWAVE-PACK-APPROVE row: approved by Jon on 17 Nov 2026, this PR.
   - In PACKS-V2-UPLOAD, remove "Waits for PADLOCK-EASIEST-HINT to merge" (it has merged, #808), and add: list heatwave-mutiny (v2) on Tes at £3.
4. docs/handover/cloud.md: record the state. The file is 20,169 bytes, past the warning size, so archive its older entries the way AGENTS.md says, keeping it well under the limit.
5. Merge with scripts/merge-pr.py when the Gate is green. That is the only merge route.

DO NOT TOUCH:
- Every other key in heatwave-mutiny/config.json, including pack_version (stays "2"), final_shape and every printed word.
- Every other room's config.
- build_pack.py, final.py, lockcheck.py and the tests.
- docs/canon.md and docs/handover/home.md (both home-lane files).
- Never commit or upload a PDF.
- No draft PR.

SUCCESS CONDITION:
- On main, heatwave-mutiny's wording_approved is {"by": "Jon", "date": "2026-11-17"}.
- The --final build succeeds with no DRAFT text, at 36 pages.
- #808's close-out is committed.
- The todo rows are updated as above.
- docs/handover/cloud.md is under the warning size.
- Merged by merge-pr.py, with its last line, the merge commit and main's check-site and phone-fit-full run IDs reported.

STOP IF:
- The --final build refuses or reports any check failure.
- Any pack_version or padlock target changes.
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.
