# Build lane handover

Lane rules: new, fully specified games only; new files only; games stay unlisted; branches `claude/build-<slug>`; worktrees `E:/jon/mg-build-<slug>`.
Contracts are saved verbatim in `docs/handover/contracts/<date>-build-<slug>.md`.

## Standing rules (Jon, 27 Oct 2026; apply to every contract unless it says otherwise)
1. **Never sit idle.** Several contracts: save each verbatim to `docs/handover/contracts/<date>-build-<slug>.md`, work in order. A real STOP IF parks the contract: commit and push the branch, record the stop here with the exact question for Jon, start the next. While CI runs on one job, start the next in its own worktree. Main red from another lane: keep building, only the merge waits.
2. **Decide the small things and say so** (wording and copy: plain, adult, listed for Jon; layout inside theme.css and shared components; names and structure; example numbers; counts above the minimum), each as one line under "Decided for you" in the report. Real stops: a mathematically wrong answer that can't be resolved; a shared-file change; a design question with no reasonable default; any new data collection.
3. **Worktree `E:/jon/mg-build-<slug>`** (cloud: any worktree), never the main checkout.
4. **Context loss:** commit and push at each milestone; keep this file current enough for a fresh session. At about 60% context, checkpoint and say so.
5. **One short report per job:** what merged (PR, commit, main run); "Decided for you"; screenshots; anything parked with its question. End with "Ready for /clear".
6. Queue finished: write "Build queue empty" here and stop. Start nothing uncontracted.
7. **Subagents for large reads** (CI logs, full measurement runs, long files): only conclusions enter the main context.
8. **Done marker:** when a contract's job is merged (or parked with its question recorded), add a line `DONE: <contract file name>` under "Done" below; `E:/jon/tools/run-build-queue.ps1` skips contracts with such a line.

## Done
DONE: 2026-10-27-build-found-a-mark.md   (merged: PR #569, squash 6c5cc59, 27 Oct 2026; held up by CI timing blocks, fixed by #570, then one real 320 x 568 fault on CI's real fonts, fixed)

DONE: 2026-10-27-build-hc-factor.md   (merged: PR #571, squash f6eecad; main run 40510992524 green)
DONE: 2026-10-27-build-y-so-steep.md   (merged: PR #574, squash f8083cc, 27 Oct 2026; main run 40518636405 green)
DONE: 2026-10-27-build-who-ate-all-the-pies.md   (merged: PR #580, squash bc5c883, 27 Oct 2026; main run 40558247107 green; waited for main to go green after #576, no override)
DONE: 2026-10-27-build-its-on-sale.md   (merged: PR #579, squash 079ceaa, 27 Oct 2026; main run 40563459598 green)
DONE: 2026-10-27-build-as-you-can-see.md   (merged: PR #587, squash 24f641e, 27 Oct 2026; main runs 40576210979 and 40576211649 green)

## Queue
1. **found-a-mark**: MERGED (#569) + art swap MERGED (#573, aaef265, main run 40514401072 green). Report still owed to Jon: its "Decided for you" list and screenshots.
2. **hc-factor**: MERGED (#571).
3. **y-so-steep**: MERGED (#574). Unmerged side branch: the "/" key for MaffsKeypad on `claude/keypad-fraction-key` (799dbfd9, worktree `E:/jon/mg-keypad-slash`), NOT a PR. Home lane/Jon to rule on merging it; then set `FRACTIONS = true` in `games/y-so-steep/index.html` to bring in Stage 3 and the fractional items.
Build queue empty (27 Oct 2026, after #574). Nothing uncontracted is started.

## Standing notes (Jon, 27 Oct 2026)
- Roster numbers stay as they are (#102 found-a-mark, #103 hc-factor; next is #104). "The 100th" is the count of LISTED items on the portal, not a roster number. NEVER list anything: listing is the home lane's job and The 6 P's goes first.
- Roster rows for unlisted games go in the Unlisted section, numbered above #101.

## hc-factor: state (27 Oct 2026)
Design: `schools/assets/hc-factor-gen.js` (`MaffsHCFactor`: bank(stage) 40 a stage, session(stage, seed), mark(step, vals)); polynomial [c2,c1,c0]; box answers marked by value; Stage 3 `canon` vector gives the 'format' (not fully factorised) verdict; sign grid is its own step (marks: S1-S5 one a question, S6 two).
Verifier `scripts/verify-hc-factor.py` parses the printed stem with its own polynomial parser; part 2 plays all six stages at 375, 360, 320, 1280, 1366.
Lessons that cost a round each (new-game checklist): the Theme check bans hex colours outside :root (use tokens); Search titles needs the page meta description = data/games.json text; the lock check finds Next by its text ("See results →", not "See the result →"); check-start-mount needs a START_STEPS entry when the menu has no Start button; CI has real fonts so options wrap more than locally: test short phones with a wide font (inject `body{font-family:Verdana,"DejaVu Sans"}`); a PR that edits the site-wide check lists selects ~136 verifiers, so ANY near-limit verifier line (70% of 270 s) blocks it: check `PR budget` job text.

## Decided for you (hc-factor; found-a-mark's list is in its PR #569)
- Palette: LIGHT row, not dark: check-theme derives it from the roster levels (GCSE = light). The stage is dark panels inside it.
- "Round" in the UI for the contract's "stage"; "You're through to the next round!" when at least half the marks, never a block.
- Round 6 has no leaderboard (stage-6 needs a label in firebase-leaderboard.js, shared); rounds 1-5 use stage-1..stage-5.
- Round 6: 2 marks a question (signs, then numbers).
- Extra named slips: S3 divided the x term but not the number; S6 add to b but multiply to -c; S2 kx(x+a) lost the k on the second term.
- Unsigned boxes (no toggle) take 0 or more; a missing term is typed as 0.
- Short phones (height under 620 px): Next sits under the one-line reason, the worked answer after it.
- Rows: #103, Unlisted (3).

## y-so-steep: state (27 Oct 2026)
S1, S2, S4, S5, S6 shipped with whole-number items; S3 ("Rearrange it") and fractional items OFF. Generator `schools/assets/y-so-steep-gen.js` (whole-number and with-fractions banks, 48 items a stage; the 6 P's imports it later); verifier `scripts/verify-y-so-steep.py` (3 parts, about 22,000 probe answers marked both ways against an independent marker). Roster #104, Unlisted (4). Keypad: `MaffsKeypad.mount(..., {keys: {fraction: true}})` on the unmerged branch above; `MaffsAnswer.fraction()` already exists, so test-answer-js.py needed no new cases.
Decided for you: light palette; fractions off until the keypad branch merges; Stage 6 has no board (stage-6 needs a label in firebase-leaderboard.js, shared; stages 1-5 use stage-1..stage-5, stage-3's declared but unused); Stage 5 has two steps (the gradient is given) and about 92% of its given points are off the y-intercept (minimum 75%); Stage 2's line comes from the figure data (no equation in its stem); marking by value through MaffsAnswer.fraction(), no game parser; extra slips on Stage 1 (m and c swapped; sign of c); a slip equal to the right answer is dropped; "run over rise" only fires once fractions are on; marks a question 1/1/1/3/2/3 (S1..S6).
Lessons: merge-pr.py refuses while main's run is queued (other lanes push often): use `--wait 540`; end-task.py must be run from a CURRENT worktree (the primary checkout's scripts/ is stale), e.g. `python scripts/end-task.py <branch>` from any worktree.

## found-a-mark art (27 Oct 2026, merged as #573, aaef265; main run 40514401072 green)
Jon's sofa and coin illustrations replace the code-drawn ones in `games/i-found-a-mark/`.
- Sources: the contract's art folder (jon/art/i-found-a-mark/ on the external drive) did not exist; the two images Jon attached to his message were used from his Downloads folder (Gemini_Generated_Image_reshrereshreresh.jpg 2752x1536 = sofa; Gemini_Generated_Image_uftykiuftykiufty.jpg 2048x2048 = coin). Jon confirmed (27 Oct) these are the intended files.
- `assets/sofa.webp`: 1600x873, q80, 71,140 bytes. The source (2752 px) was ABOVE 1600 px wide, so it was downscaled, then cropped 10 px top and bottom to the house frame (never stretched).
- `assets/coin.webp`: 512x512 with alpha, q80, 15,214 bytes. Paper and grey drop shadow removed by growing the border-connected light-grey region (the closed ink outline stops it), shrinking the subject 1 px with a 0.8 px soft edge, premultiplied resize; checked on dark (#182033), light (#f8fafc) and green surfaces: no halo; the ink glint at the top left kept. Total added 86 KB. No Gemini sparkle in either bottom-right corner.
- Page: the start-screen SVG is now the sofa image with the coin image over the cushion gap (both eager, both visible there); `.slot.got` (found-mark coins in game and on results) uses the coin as its background, same size and drop animation. The marks bar stays CSS, retinted to the sofa green (#3f5953). Old drawing CSS and the unused tokens (--wall, --rug, --lamp, --coin-edge) deleted.

## Decided for you (found-a-mark; PR #569, art #573)
- Palette: LIGHT row with a warm-brown accent: check-theme derives it from the roster levels and GCSE is light. (Art swap: the marks bar takes the sofa's green.)
- One level (key `gcse`), one board: unaided method marks in a session. A step shown with help ("Show me a step") is never counted: not in the HUD, the leaderboard, game_completed or the personal best.
- Session: 5 questions, the four types (is it enough, ratio with a twist, interest and depreciation, the L-shaped garden) once each plus one more of a random type, in random order; every question is 3 method marks, with a dotted 4th "A" slot for the answer mark that is never asked for.
- Marking: any valid calculation scores once its inputs are found (a form may have alternatives); a wrong tap shows the one-line slip plus MaffsNext (3 s floor), then the options return with that one struck out; no penalty.
- "Bank it and move on" ends a question early and lists the steps still in the working.
- Sound is a small clink, OFF by default, switched on from the menu.
- Wording is plain and adult (no jokes; they are Jon's to add); the feedback line after a full question says the last mark is for the answer.
- Phone fit: short phones (under 620 px high, and again under 580) tighten the card, the options and the HUD; found when CI's real fonts made the garden question's options wrap more than they do locally (it failed at 320 x 568 on CI, not locally).
- Shared-file lines added (the minimum a new unlisted game folder needs, as #509): roster row #102 + Unlisted line, data/games.json entry, audit-register, check-answer-lock, check-leaderboard-coverage (NOT_ON_HUB), check-levels, check-start-mount, check-teacher-invite, check-theme, findings yml. Nothing listed.
- Screenshots: 375 x 667 and 1366 x 768, one per question type, in the earlier session's scratchpad (re-make by playing a session with the stub server).

## who-ate-all-the-pies: state (27 Oct 2026, PR #580, bc5c883)
Five stages on the pie-charts bank (schools/assets/pie-game.js imports it; no question copied). Worked example, then 10 questions easiest first. Boards stage-1..stage-5 (stage-5 label already exists). Roster #105, Unlisted (5). Verifier scripts/verify-who-ate-all-the-pies.py, 4 parts, 7 planted faults each caught; no bank answer was wrong. The bank has no "You can't tell" items in stages 2 and 5, so the game has none there; all are in stage 4. One screenshot per stage at 375 x 667 was made in the fork's scratchpad.

## Decided for you (who-ate-all-the-pies)
- Palette: light (GCSE/KS3 roster levels).
- "You can't tell" only appears where the bank supplies it (stage 4).
- Merge waited for main to go green (home lane's #581 fixed the red run); no override was used.

## its-on-sale: state (27 Oct 2026, PR #579, 079ceaa)
Five stages on the percentages-money bank (schools/assets/percentages-money-generator.js, imported, never copied); worked example (slot 0, fixed seed, logs nothing) then 10 questions (slots 1-11 minus one at random, easiest first; a repeated wording is drawn again); answer typed onto a price tag (GBP box to 2 d.p., % box in stage 3); marking by value via MaffsAnswer; bank slips as feedback; format answers never marked. Calculator "by stage": optional 1-4 with a "Try without a calculator" note on friendly items, required in 5. Boards stage-1..stage-5. Roster #106, Unlisted (6). Verifier scripts/verify-its-on-sale.py, 4 parts (3-39 s): params recomputed with Fractions, about 16,700 typed answers marked both ways, six sizes played, seven planted faults caught.

## Decided for you (its-on-sale)
- Palette: light, because GCSE is light.
- Stage 5 has a leaderboard: stage-5 already exists in firebase-leaderboard.js (Squared Squirrel's), verified, not assumed.
- Question selection: worked example is slot 0 with a fixed seed; the 10 questions are slots 1-11 minus one at random, in the bank's order.
- A session redraws a repeated wording (stage 5 slot pairs share a shape).
- Calculator badge and stage list are static HTML because the calculator check reads the page source.
- Unit boxes: GBP for money, % for percentage change, plain numbers via the keypad.
- Roster: held #105 briefly while #580 looked late, then moved to #106.

## Lessons (pies, sale; 27 Oct 2026)
- The calculator check reads page SOURCE: a "by stage" game's calc badge must be static HTML.
- Two bank slots of one shape can collide on wording; redraw repeated stems.
- The format-answer test needs a key whose pence are a multiple of 10.
- merge-pr.py refuses while main is red or its run is unfinished; use --wait 540. end-task.py needs a current worktree and a local branch equal to the PR head (reset a local merge-of-main first).
- Plan job: its-on-sale passed with four `--part` ci-lines on 27 Oct, but the home lane says new --part lines fail the Plan job; use the shard interface when it is on main.

## found-a-mark batch 2: state (27 Oct 2026, PR #585, PARKED)
Five new types in the game's own bank (angles, mean from a frequency table, the ladder, coffee and tea, conditional probability from a two-way table). Built; local checks green (51 checks; verifier parts 1-5 pass; 14 new planted faults caught, 6 old still caught). PARKED: main's median CI setup is 107 s, so a new or renamed content ci-line counts 120 s + 107 s = 227 s against the 216 s fail line and the Plan job fails. Not overridden, not hand-split (Jon). Release: the cloud lane's step 1 (new lines warn, not fail) is merged, then merge main in and merge. Converting the verifier to shard work units is a follow-up after #578 lands.

## Decided for you (found-a-mark batch 2; Jon's rulings marked)
- **Five types per session, 15 method marks (Jon agrees).** A session is five different types always worth 15 method marks (five 3-mark types, or the ladder 2 + coffee or two-way 4 + three 3-mark types), so the leaderboard stays fair. The menu says "15 method marks".
- **`?types=` preview (Jon agrees):** `?types=ladder,mean` plays those types in turn, submits no score and shows "not on the leaderboard".
- Ladder (Jon: correction stands): the "foot under a third of the ladder" clause was unsatisfiable (only 7-24-25 qualified, 3 questions); dropped, foot is the shorter leg of every triple; 14 scalings x 2 variants = 28 questions.
- Coffee and tea (Jon): "added when the signs match" stays as a distractor, with the feedback "That's true, but it doesn't get rid of a letter, so there's no mark for it yet."
- Engine extended once, for all types: `answers` answer marks (marks = slots + answers); forms/distractors can carry `tex` and a `fact`; expressions accept `sqrt`; `options()` takes a cap. Batch 1 templates and marking unchanged.
- Short screens: batch 2 questions show 4 to 6 options (never fewer than 4) so the last stays above the fold.
- Mean table: consecutive values from 0 or 1; the x x f column fills in when step A is found. Two-way: context in the corner cell; "Give your answer as a fraction" dropped; totals-row first and last cells show a dash.
- Extra distractors: x / f for the mean's step A; swapped coefficients for coffee and tea's first and second equations. Pens and pencils use p and q. No-KaTeX fallback shows the degree, angle and root signs.
- CI lines: parts 4 (module self-test, 17 plants) and 5 (page self-test, 5 plants) are new.

## as-you-can-see: state (27 Oct 2026, PR #587, 24f641e)
Bank schools/assets/reading-charts-generator.js (60 questions, fixed seed 20261027, 12 a stage, answers computed from chart data, accepted interval per number answer); schools/assets/reading-charts-game.js; games/as-you-can-see/index.html; scripts/verify-as-you-can-see.py (recomputes every answer, reads every chart back from its SVG, every kind of question at 6 sizes, 11 plants caught; one ci-line, no --part, written in units so converting to # ci-shards is a header change). Five stages, boards stage-1..stage-5. Plan job passed on the PR; no override, no hand split. Roster #107, Unlisted (7).
Candidate shared helper: value-with-tolerance match in MaffsAnswer (here an accepted interval stored in the bank question); a second graph-reading game would make it a class.
Follow-ups: convert verify-as-you-can-see.py to # ci-shards; if claude/footer-unpin lands, run scripts/apply-footer.py on games/as-you-can-see/; wire the bank into The 6 P's (home lane; not done here, gen-six-ps.py is shared).

## Decided for you (as-you-can-see)
- Setting and tone neutral (school and cafe), no jokes: the contract leaves both to Jon.
- Scale not stated in the stem; the worked answer teaches it, otherwise the wrong-gridline slip has no point.
- Tolerance: half a minor gridline for readings, exact for counts, totals and differences; interval stored per bank question.
- Slot 0 is the worked example; a session is 10 of slots 1-11, easiest first.
- Stage 2 scales 2s, 5s, 10s with a number every 10. Stage 4 correlation bands: |r| >= 0.8 strong, 0.45-0.78 weak, below 0.25 none (verifier enforces).
- "You can't tell" only in stages 3 and 4, right in some questions and a wrong option in others (stage 3: a time between measured points, an unmeasured value; stage 4: another group).
- Stage 5: six flaws (truncated axis, uneven scale, pictures scaled both ways, 3D bars, missing labels, or fair); two of 12 slots are fair charts.
- Levels ks3 and gcse, no picker; light theme; calculator optional.
- Minimum registrations only (data/games.json unlisted entry and roster row); nothing listed.
- Page title and description reworded to match what games.json generates (KS3/GCSE, description at most 155 characters).
- `ACS.ui.preview(stage, slot, seed)` read-only test hook.

