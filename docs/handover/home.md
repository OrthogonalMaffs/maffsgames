# Handover: home lane

**Queue (cross-lane facts; never archived)**

- CHRISTMAS-PACK (Shared, Codex): in progress on `codex/christmas-pack`, `/home/maffs/mg-christmas-pack`; contract and Amendments 1-4: `docs/handover/contracts/2026-11-06-christmas-pack.md`. Room art/config, independent recompute and generic pack fixes are isolated there. Cloud's WHOSE-SIDE-FIT/BIOS and Claude Code's PHONE-FIT-ASIDE files are untouched. Review holds at green Gate for Project Claude's proof PNG review and Jon's "merge".

- WHOSE-SIDE: DONE and live, unlisted. #674 merged as 257e883; fixes #676 merged as f1acc1f (it contains #675, closed unmerged); main green. Merged on Jon's word before review; Project Claude reviewed #674 and #676 on 6 Nov and passed them (side roles in both θ positions, FN, Stage 4's key, all 12 triples, uniform scaling). Worktrees and claude/whose-side-fixes deleted on Jon's call, 6 Nov. Art done (#684). timer-policy.md's line waits for WHOSE-SIDE-FIT to merge; the cloud lane owns the game until stage 5, which follows WHOSE-SIDE-BIOS. Contracts: docs/history/contracts/2026-11-05-whose-side*.md.

- CHRISTMAS-ROOM: DONE. #667 merged as 9cbedee; close-out #668 merged as e32608f. Contract: docs/history/contracts/2026-11-04-christmas-room.md.

- Cloud lane: one session at a time from 6 Nov (Jon, 5 Nov). #669 and #671 are merged; no overlapping cloud sessions remain authorised.

- DONE queue: docs/history/handover-home-archive.md

- how-many-parts to move next (cloud lane, HOW-MANY-PARTS-FRACTION)

- Cloud owns Gate files and docs/handover/cloud.md; home does not edit them. GATE-FIX #634 merged as 16c40530; incorporated here by merge dd370c69. GATE-RESUME #630–#632 and root-image removal #633 are merged.

- FRACTION-WHOLE: merged #662, b38ce399; Shared review passed and Jon authorised merge, 4 Nov. Contract: docs/history/contracts/2026-11-04-fraction-whole.md. Main run and cleanup recorded below.

## 2026-11-06 (home): CHRISTMAS-PACK

Agent Codex. Worktree `/home/maffs/mg-christmas-pack`, branch `codex/christmas-pack`, from origin/main 3d67615e after ROOM-ORDER-HERRINGS merged. Last commit pending; next: commit, PR and Gate. Shared review and Jon's "merge" hold. Coordination respected: cloud's WHOSE-SIDE game/verifier and Claude Code's PHONE-FIT-ASIDE files not touched.

The six clue markup pairs are the only room.js changes. The room check stayed at 98 VALID of 900 with the same TRUE-MINUS result. Four end-to-end win/loss browser plays passed at 390 and 1100 px; each clue rendered bold printed words with filled tokens. All 11 PNGs on `art/christmas-pack` scanned clean, then converted without resize to WebP under 250 KB. The pack has six fair sets; all 29 variant records independently recompute. The Christmas PDF stays ignored in `dist-packs/`; six 100 dpi Christmas proof PNGs and three Kiln before/after page pairs are prepared for review. Generic fixes count only cover/evidence/locks in each set's range, fill Set A misconception figures in the key, and flex locks-page work boxes with a 25 mm minimum. Christmas boxes measure 28.8 mm in every set; Kiln's measure 35.5 mm after, 34.5 mm before. Christmas page 1 is 150 words; Kiln's is 147 after the three approved trims. Selftest: 20/20 plants caught across both rooms. Build checks pass; no warning beyond the known room's variant-0 draw being INVALID and never served. `check-changed.py`: all 51 selected checks passed (404s), seven heavy checks deferred to CI. Gate pending.

## 2026-11-06 (home): WHOSE-SIDE handover

Agent Claude Code, Windows, worktree E:/jon/mg-whose-rec, branch claude/whose-side-review-record, which carries this entry and the queue line above. Its local checks were running when this was written; it merges through merge-pr.py on a green Gate (Small, docs).

Done: stages 1-4 live and unlisted (#674 257e883; fixes #676 f1acc1f, containing #675, closed unmerged; close-out #677). Project Claude passed #674 and #676 on 6 Nov. Art: #684 (e42aa76, cloud). Deleted on Jon's call, after confirming #675's changes are on main: E:/jon/mg-whose-fix, its local branch, remote claude/whose-side-fixes, and local claude/whose-side-are-you-on. E:/jon/mg-whose-side is also gone: no retry needed. Windows refused it because one of the verifier's serve-stubbed.py processes had outlived its run in that folder (PID 32912); stopping it let the folder go. Look for that before calling a folder undeletable.

Open: (1) .claude/rules/timer-policy.md: add the game's line from the code (counts up, no lives, faster right answer scores more), docs only, after WHOSE-SIDE-FIT merges; Project Claude reviews. No WHOSE-SIDE-FIT PR found at 16:19 on 6 Nov. (2) After this branch merges: end-task for claude/whose-side-review-record. (3) Stage 5 follows WHOSE-SIDE-BIOS; the cloud lane owns games/whose-side-are-you-on/ until then, so home does not edit it.

## 2026-11-05 (home): WHOSE-SIDE-FIXES

Jon's play-test. Stage 2 gets slots and Check; each side one hit line, nothing painted takes a tap; verifier clicks the dash and dot gaps at every size; 18 plants caught. No click on a side missed in reproduction; the clicks that did nothing came during MaffsLock's 300 ms window, and no bands exist during the 800 ms Right flash. Merged in #676 with Jon's second play-test (double clicks; the 0.8 s hold proven). Record: agent Claude Code; wall in the PR's report; review cycles 0; amendments 0; usage n/a.

## 2026-11-05 (home): WHOSE-SIDE

New unlisted game, stages 1–4; stage 5 and the art are later. Amendment 1: light theme, games.json and precedent checker lines, side-word text bold 19 px. Amendment 2: side colours on sides and side words only; ✓/✗ and a word for right and wrong. Rulings 19:45: grey sides until answered (1, 2, 4), stage 3 coloured with coloured numbers; 16-30-34 for 9-40-41. Added beyond the contract: question_id = item id (check-question-id.py requires it of new games). Verifier: all 10,368 items recomputed from geometry; 13 plants caught. Merged #674. Record: agent Claude Code; wall in the PR's report; review cycles 0; amendments 2; usage n/a.

## 2026-11-05 (home): MERGE-669-671

DONE: #669 EQUATLE-320 merged by merge-pr.py as d6e1ec5; main run 42082117555 GREEN. #671 TRUE-MINUS merged next by merge-pr.py as 3604b7f; main run 42087251109 GREEN. Each PR was rebased after a cloud.md conflict; main's CHRISTMAS-ROOM completion and every main entry were kept, and each PR's new entry was added. CLAUDE.md matched main. No exception to the merge guard was used. Cloud lane returns to one session at a time from 6 Nov.

Record: agent Codex; wall n/a; review cycles 0; amendments 1 (Jon's 5 Nov handover ruling); usage n/a.

## 2026-11-04 (home): CHRISTMAS-ROOM

Final state: DONE. #667 merged as 9cbedee; close-out #668 merged as e32608f. The contract is in docs/history/contracts/2026-11-04-christmas-room.md. Earlier notes below record the implementation and review handoffs.

AMENDMENTS 3 and 4 (Jon, 5 Nov), saved verbatim. The 4 Nov Gate stop (run 41922457161, teacher page's table.tt overflow, todo §1.37) is resolved by Amendment 3's tier1_phone_overflow entry, width 541 as issued; it measures 535 locally since the regeneration. Amendment 4: cr's given ratios in simplest form, in the generator and escape_set_checks; only cr's library changed (47 locks compared). VALID now 103 of 1000, was 32; floor 20. Reachable sets ct 8, sc 10, cr 8 of 10. Check-escape-rooms, the four test-escape scripts, the play-through (159 checks) and the independent recompute (30 sets; 232 of 232 corrupted sets rejected) rerun clean. Jon's rulings: Set A stays (warning only); minus signs, canon room count and the unreachable sets are follow-ups, not this PR. Not changed: docs/lock-bank-batch13.txt's cr NOTE does not state the new rule (flagged in the PR). No merge authority.

TAKEOVER (Jon's written task, 4 Nov 21:30): Claude Code takes over from Codex on the Windows machine. Primary E:/jon/maffsgames-new-clone fast-forwarded to 10a8b261. New worktree E:/jon/mg-christmas-room from origin/codex/christmas-room (Jon's instruction; the rulebook's same-worktree rule cannot apply across machines), branch keeps its prefix. Status clean and git log origin/main..HEAD matched the record below (head 0647f999). Identity: local user.name is "Jon", email matches; commits pass user.name=Vector52F per command, config unchanged. All Codex's checks treated as not run. Next: run the SUCCESS CONDITION, PR, stop at green Gate. No merge authority.

PAUSED for context handover at Jon's request, 4 Nov. Implementation checkpoint: 563b14a9; branch codex/christmas-room, worktree /home/maffs/mg-christmas-room, base 10a8b261. Resume the SAME branch/worktree; check clean status and git log origin/main..HEAD against this record. No push, PR, Gate or merge yet. Amendment 2 resolves the bank/findings scope STOP below and is saved verbatim with Amendment 1 and the full contract/draft. Registered preview server on 8874 stopped through end-task.py's stop_registered(); generator already exited. No running check queue remains. Do not restart until Jon resumes.

Implemented: approved room prose, eight objects/two blanks, three instruments/grades, Amendment 1 feedback tokens, scaffolds/teacher mapping, three bank entries and SR-30 findings file (no audit verdict; Project Claude review pending). Generator and shared per-set module add only the three Christmas locks. Ten sets per lock; ct includes rate/rise/abs/short, sc tree/total/ccm, cr reduced ratio/parts/each. Shared check independently recomputes domain, misconception and working tokens from clue parameters; grid solvers use the warming equation, ceiling-height balance and raw ratio proportions. Fixed freezer/door decoys retained and response 18 excluded. Other room.js files unchanged; JSON comparison proves every old variant library unchanged. Added one Core card to each listing, one sitemap URL and Jon's exact updates sentence; current count-bearing hub/front strings changed 13 to 14 (front metadata has no room count). Engine/assets, other rooms, cloud handover and pack generator untouched.

Art: all three source JPGs from origin/art/christmas-tree-fiasco, extracted to /tmp/christmas-tree-fiasco-{scene,win,fail}.jpg; existing strip-gen-watermark.py reports no mark on each, frames each to 1600x873 and writes q80 WebP. Source and output images visually inspected: no people, lettering or visible watermark. Art branch untouched. Local tool prerequisites numpy/Pillow were missing; installed into existing /home/maffs/.venvs/maffs with uv pip, no repo dependency change. First conversion attempts failed on missing imports; final conversions exit 0.

RAN: generator exit 0, log .claude/bg-1793826500110.log (GENERATOR_EXIT_STATUS=0). check-escape-rooms.py exit 0 after the room-specific shared checks were added: 30 verified sets, 32 VALID of 1000, all tokens resolve, all art present, rating Core; existing plants caught. Set A as a JOINT draw is INVALID (ct/cr share clue magnitudes 4/8 etc.; cr answer 6 is another lock's clue). Checker warns and engine never serves that combination; individual Set A locks retained exactly as approved, 32 other joint draws are served. No floor STOP hit. Audit-register --check exit 0. Bank checker 3/3 usable exit 0, with a float-equality note on ct; VERIFY then changed to the equivalent integer balance, NOT re-run yet. UTF-8 character reads and git diff --check pass. check-changed.py --list exit 0: 62 selected; plan /tmp/christmas-check-plan.txt, standard seven CI deferrals. This was planning only, not a test run.

VALIDATED on Windows (Claude Code, 4 Nov), every check rerun, Python 3.14 locally: generator deterministic (no diff); check-escape-rooms.py exit 0, VALID 32 of 1000, rating Core; test-escape-dial/keypad/setcodes/rating exit 0; check-lock-bank.py batch13 3/3; audit-register --check OK; check-changed.py 62/62, 731s, exit 0, standard seven CI deferrals. Scratch only, not committed: all 30 sets recomputed independently and 69 strings matched to the draft (0 fails); 213/213 mutations caught; play at 390x844 touch and desktop, win and timeout, 159 checks, 0 fails. Set A joint draw fails only on rule (a): 4 is in ct and cr (corrects the note above: cr's answer 6 is not a ct clue). Only 6 of 10 ct sets and 6 of 10 cr sets are reachable; neither lock's Set A. OPEN for review, in the PR: Set A / §5c step 6, ASCII -4 beside the draft's −18, canon's two 'thirteen' counts (out of scope), teacher page overflows a phone on every room. Next: PR Gate, then stop for Project Claude's Shared review and Jon's play-test and merge. No merge authority.

Agent: Codex. Worktree: /home/maffs/mg-christmas-room. Branch: codex/christmas-room. Base: 10a8b261. First commit 0b260bb5 saves the full approved draft/contract and Amendment 1 verbatim, plus Queue claim. Primary fast-forwarded; clean takeover and expected git identity confirmed. Root cause: approved new seasonal content on the existing engine; no bug class or engine change. Amendment 1 resolves the initial fixed-number feedback contradiction. Art branch exists; all three source JPGs visually inspected: no people, lettering or visible watermark. No artwork transformation or production changes yet.

STOP at contract/code check: scripts/check-escape-rooms.py:209 rejects every lock missing from docs/lock-bank-batch*.txt; no Christmas entries exist. EXACT CHANGE/lane exception omits that bank, so the required checker cannot pass within the named files. SR-30 also requires a new room's findings file, omitted from scope. Need a numbered amendment authorising the new room's bank entries and docs/audits/findings/christmas-tree-fiasco.yml; retain checker and engine unchanged. No implementation or tests claimed, no push/PR. Next: resume this clean branch after amendment, then build, validate, Gate and Shared review/Jon play-test hold. No SR exception applied; SR-30 requirement flagged.

Record: agent Codex; wall n/a (initial contract receipt timestamp unavailable); review cycles 0; amendments 2; usage n/a.

Record: agent Claude Code (takeover); wall in PR #667's report; review cycles 0; amendments 4; usage n/a.

