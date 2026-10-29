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
DONE: 2026-10-27-build-found-a-mark-batch2.md   (merged: PR #585, squash 18454dc, 27 Oct 2026; main runs 40580295716 and 40580295599 green)
DONE: 2026-10-27-build-possibly-maybe.md   (merged: PR #594, squash 6512151, 27 Oct 2026; main runs 40596794906 and 40596796589 green)
DONE: 2026-10-28-build-pictogram-drawing.md   (merged: PR #599, squash 96489d2, 28 Oct 2026; main runs 40711007380 and 40711006678 green)
DONE: 2026-10-28-build-calc-flag.md   (merged: PR #603, squash 356529c, 28 Oct 2026; main runs 40729110379 and 40729109349 green)
DONE: 2026-10-28-build-feedback-teaches.md   (merged in three parts: #600 8c3e722, #602 1fdc20e main runs 40720476561 and 40720477747, #604 ed24ff6 main runs 40735921237 and 40735922595; part 1 main runs 40713063586 and 40713061487; all green)
DONE: 2026-10-28-build-friendly-loosen.md   (merged: PR #606, squash 66ea1ff, 28 Oct 2026; main runs 40741437285 and 40741437725 green)
DONE: 2026-10-28-build-stage-exit.md   (merged: PR #608, squash ed9b737, 28 Oct 2026; main runs 40784995918 and 40784996276 green; Who Ate All the Pies? DEFERRED)
DONE: 2026-10-28-build-essentials-filter.md   (merged in three parts: PHASE A PR #611, squash 51e5c1b, 29 Oct 2026, main runs 40804757443 and 40804756870 green; PHASE B part 1 PR #612, squash 7230c8c, main run 40817370804 green; PHASE B part 2 (chips) PR #614, squash <SHA-614-PLACEHOLDER>, main runs <RUNS-614-PLACEHOLDER>)

## Queue
1. **found-a-mark**: MERGED (#569) + art swap MERGED (#573, aaef265, main run 40514401072 green). Report still owed to Jon: its "Decided for you" list and screenshots.
2. **hc-factor**: MERGED (#571).
3. **y-so-steep**: MERGED (#574). Unmerged side branch: the "/" key for MaffsKeypad on `claude/keypad-fraction-key` (799dbfd9, worktree `E:/jon/mg-keypad-slash`), NOT a PR. Home lane/Jon to rule on merging it; then set `FRACTIONS = true` in `games/y-so-steep/index.html` to bring in Stage 3 and the fractional items.

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

## found-a-mark batch 2: state (27 Oct 2026, PR #585, MERGED 18454dc)
Five new types in the game's own bank (angles, mean from a frequency table, the ladder, coffee and tea, conditional probability from a two-way table). It was parked at the Plan job (new lines counted 120 s + 107 s setup), released after SHARD (#578) landed. Verifier converted to SHARD work units: one `# ci-shards` header, 32 units (engine, 10 sessions, 22 plants, all caught); no --part lines. Engine extended once for all types. Main green. Footer: if claude/footer-unpin lands, run scripts/apply-footer.py on games/i-found-a-mark/.

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

## Lessons (SHARD / flakes, 27 Oct 2026)
- Standing rule (Jon): any lane may re-run a failed main run once with `gh run rerun <id> --failed`; if it passes, log it in the shared lanes notes file under "Flakes for the cloud lane's step-4 audit"; if it fails again it is real, tell the home lane.
- After SHARD (#578), a verifier with `--part` lines conflicts on merge with main's `# ci-shards` version: take main's and re-apply as work units. A new content line used to count 120 s + setup median; SHARD fixed the setup-time cause.

## Open contracts (29 Oct 2026; Jon: stop after this docs PR)
- essentials-filter (contract 10): DONE, see Done. Nothing open on it.
- stage-exit follow-up: add the shell to Who Ate All the Pies? after the 2 Nov shared-infra freeze (docs/todo.md has the root cause: the shared HUD row has no phone-width space allocation). The 6 P's page header has "Back to games"; not checked in play.

Earlier queue finished 27 Oct 2026 (to #594); not empty now, see Open contracts above. Open follow-ups for others: as-you-can-see verifier to # ci-shards; footer apply (scripts/apply-footer.py) on as-you-can-see, i-found-a-mark and possibly-maybe if claude/footer-unpin lands; keypad "/" key branch (claude/keypad-fraction-key) awaiting a ruling; shared Stage 6 board label and a shared tolerance helper for MaffsAnswer (candidates); switch The 6 P's to the shared fraction input (see the lanes' notes file).

## possibly-maybe: state (27 Oct 2026, PR #594, 6512151)
Five stages on the probability bank (schools/assets/probability-generator.js, 60 questions, fixed seed 20261028, 12 a stage, answers computed; imported by schools/assets/probability-game.js). Stages: the scale; not and the missing one (x and 2x); listing outcomes (dice, spinners, coin and dice, menus); expected and relative frequency (is the dice fair, gambler's fallacy); tree diagrams (independent, no without-replacement). Worked example then 10 questions easiest first; boards stage-1..stage-5; roster #108, Unlisted (8). Fractions TYPED in two boxes (Jon's amendment) via the NEW shared file schools/assets/fraction-input.js (MaffsFractionInput), extracted from The 6 P's page, which is unchanged; matched by value, 2/4 = 1/2, lowest terms enforced only where asked (format result, never marked). Verifier scripts/verify-possibly-maybe.py: # ci-shards, 32 units, 13 planted faults caught, about 3m50s locally.
Notes for next week (in the lanes' notes file): switch The 6 P's to the shared fraction input (it also has a whole-number box the shared file lacks); The 6 P's basic-probability questions are in its own JSON, not importable, so the new bank overlaps it.

## Decided for you (possibly-maybe)
- Light palette, levels ks3 and gcse, no picker.
- Fractions in stems and keys are often not in lowest terms; typed answers accepted unsimplified unless the question says "in its simplest form" (only stage 1's decimal-to-fraction question does).
- Tall grids (two dice) use smaller cells on phones under 700 px high; text stays 12 px.
- The shared keypad's "." key shows for fractions and is ignored there; keypad not edited.
- "You can't tell" is not a general option: right only in stage 4's "is the dice fair?" when the dice is thrown just 12 times. Fair rule: every face within 45% of expected; the verifier uses it independently.
- Minimum registrations only; nothing listed. `PM.ui.preview(stage, slot, seed)` read-only test hook.
- Not wired into gen-six-ps.py (shared); phone fit covered by the verifier, not measure-phone-fit.py.

## Lessons (possibly-maybe)
- A verifier "wrong answer" generator must be proven different from the key (14/22 = 7/11).
- A plant caught only by a random session is flaky in CI: catch it with a deterministic view.
- Playwright route handlers must take exactly one argument.

## pictogram-drawing: state (28 Oct 2026, PR #599, 96489d2)
Cause: in games/as-you-can-see/index.html `symbol()`, the clip-path sat on the translated and scaled path, so the cut rectangle landed off the symbol and half and quarter symbols were in the DOM with the right data but never painted. The contract named reading-charts-generator.js; the renderer is in the page. Fixed with a clipped wrapper group (`data-cut`). Worked-step counts agree in number (`sym()` in the generator); key text reads "= 4 lunches". New scripts/verify-chart-drawings.py (# ci-shards, 14 units) hit-tests what is painted for pictograms, bars, line and scatter points, pie slices, spinner wedges and counters, plus a symbol-count wording check; 10 planted faults caught including the original bug. No mismatches in the pie-chart or probability banks. verify-as-you-can-see.py updated for the new key text.

## Decided for you (pictogram-drawing)
- Renderer fixed in the page (a drawing function, no layout change), not in the generator.
- New verifier file; the older verifier stays a plain ci-line.
- Pie angles measured at 85% of the radius, tolerance from the stroke width (about 3-4 degrees); stage 3 pies measured after a right answer (drawn from typed angles).
- Stem wording left alone.

## Lessons (pictogram-drawing)
- A verifier that reads attributes and path geometry cannot see a drawing that is in the DOM but not painted: hit-test with elementFromPoint over a grid inside isPointInFill.
- A clip-path is read in the user space of the element carrying it: never put it on an element with its own transform.
- Pie boundaries have stroke width: tolerance from the stroke; sample at 0.85 r (labels sit at 0.62 r; spinner letters up to 0.72 r).
- Probability grids, tables and trees are covered by their own verifier's read-back only (no visibility test).

## stage-exit: state (28 Oct 2026, PR #608, ed9b737)
Seven stage games (its-on-sale, as-you-can-see, possibly-maybe, hc-factor, y-so-steep, i-found-a-mark, free-daily-pizza) now have a "Stages" button ("Rounds" in hc-factor, "Menu" in i-found-a-mark and free-daily-pizza) and the standard "Back to Games" link on every question and worked example, from NEW shared files schools/assets/stage-exit.js and .css (new files only; each page got one stylesheet link and one script tag; the `body.playing a.back-link{display:none}` rule was removed). On a question the controls sit at the two ends of the game's HUD row (no added height); on the worked example they share one header row. The button clicks the page's own "All stages" button: no game_completed, no board submission, no score; a pending Next control is cleared first.
Who Ate All the Pies? is exactly as on main (hide rule kept, no stylesheet or script), exempt BY NAME in scripts/verify-stage-exit.py (Jon, option 4, "revisit after the 2 Nov shared-infra freeze"); the verifier fails if Pies ever carries the shell. Root cause is in docs/todo.md: Pies' HUD holds the calculator toggle (127 px) and at 320 and 360 px the toggle plus stage items plus exit controls overflow (answer controls end at 551 vs a 528 fold at 320x568). No fold rule or threshold was loosened.
Verifier scripts/verify-stage-exit.py: # ci-shards, 21 units (exempt check, 7 games exited to the picker and the portal, 5 fit sizes, 7 plants), all plants caught.
Lessons: the exit control must cost no layout height (use an existing row); Playwright route handlers receive (route, request), so use a factory; a new shell touching a page row must be re-run against every game's own phone-fit verifier; check-changed took about two hours and was reaped once for memory, rerun with --workers 2.

## calc-flag, feedback-teaches, friendly-loosen (28 Oct 2026)
- calc-flag (#603): per-stage tag kept; `optional` loads the shared calculator behind a closed toggle with a "Calculator optional" badge; check-calculator.py and canon 4.4 updated; `friendly` is hint-only; gen-six-ps.py unfrozen for that change only; As You Can See and Possibly, Maybe retagged `not allowed` (Jon, 28 Oct).
- feedback-teaches (#600, #602, #604): why lines on the pie, money and reading-charts banks, with verify-feedback-teaches*.py (planted faults raise if the plant does not apply); coffee/tea distractor feedback exactly "That's true, but it doesn't get rid of a letter, so there's no mark for it yet."
- friendly-loosen (#606): Jon accepted 56 of 60 (pie-charts) and 38 of 60 (percentages-money); hint "Try it with pen and paper" as a constant per bank. "Consolidate hint wording" for The 6 P's is logged in lanes/notes.md.

## Stale-plant audit (28 Oct 2026; report only, owners unclear)
Verifiers that can count a stale plant (target missing or unchanged) as caught: verify-correlation-or-coincidence.py:396-405, verify-just-pythag-it-bruv.py:1799-1808, test-ga4-summary.py:444, check-escape-rooms.py:494-532. Model to copy: verify-free-daily-pizza.py:1343-1385 (raises if the plant does not apply). Not fixed by the build lane.

## essentials-filter (29 Oct 2026; PRs #611, #612, #614)
PHASE A (#611): shared MaffsCardFilter (NEW schools/assets/card-filter.js and card-filter.css) on /essentials/: topic chips (All + six), search over card text, sticky bar under the featured card, empty message with Clear filters, URL state ?topic=&q= (read on load, replaceState on change; unknown values and ?calc= ignored). Every card carries data-topic (its section id). Events: filter_applied (per chip tap, and once after typing stops) and game_card_clicked, with filter_value "v1|page=essentials;topic=..;su=..;sl=..;q=..;n=.." and page=essentials as a GA4 parameter. The Sheet has no page column, so page rides in filter_value: the endpoint is unchanged. Only essentials/index.html was edited; index.html, portal filter, featured.js, game pages, data/games.json untouched. Verifier scripts/verify-card-filter.py: # ci-shards, 22 units, 11 planted faults caught.
PHASE B part 1 (#612): Jon's ruling 29 Oct: the roster Calculator tag is exam guidance ("likely"), not enforcement; levels differ: tag by the GCSE/Foundation bank. All 28 tags written (21 not allowed, 5 optional, 1 required, 1 scientific; reasons in docs/handover/essentials-calc-tags.md). Seven games got what check-calculator.py needs (scroll.js, keypad.js, calculator.js, badge, shared calculator behind a toggle): better-value (required), stat-attack (scientific), split-it, expected-damage, distinctly-average, sequence-solver, proportion-blaster (optional). No shared file changed except the check-calculator.py self-test below.
PHASE B part 2 (#614): data-calc on all 36 cards (23 non-calc, 6 calc, 7 both); chips "Likely non-calculator" (non-calc + both) and "Likely calculator" (calc + both); ?calc=non-calculator and ?calc=calculator; filter_value gains calc=; verify-card-filter.py strict (every card's data-calc equals the roster, chips alone and with a topic, 15 planted faults caught, Verdana injected); bar 145 px at 375x667 and 320x568, first card at about 841 px (held for Jon's look before merge).
Decided: check-calculator.py self-test now picks an UNTAGGED game for its "value outside the four" case (CONFIRMED by Jon, 29 Oct); badges keep the check's exact wording, "likely" is on the chips only (badge wording change logged for after 2 Nov); Distinctly Average's toggle sits inside a MaffsLock.fresh() window; results scroll uses window.scroll, not scrollTo (check-scroll-reveal.py bans scrollTo for feedback/Next).
Lessons: a sticky bar sticks only inside its parent (mount wrapper needs display:contents; assert bar-top = 0); a plant that cannot change behaviour is a MISSED plant; a page that loads keypad.js must load scroll.js; check-changed does not run Answer lock for touched pages, CI does: run check-answer-lock.py --game <slug> locally; a roster edit selects about 147 checks (about 20 min); the CI Plan job built the AST map twice and hit its 5-minute limit on five attempts: the home lane raised it to 10 minutes as a stopgap (#618, Jon's freeze exception; revert is PLAN-MAP-ONCE in docs/todo.md).
Not ours: the ticker pause and announcement strip (#616, #617) are home-lane work.
Parked (not blocking): keypad "/" key (claude/keypad-fraction-key) stays parked until after 2 Nov; Pies stage-exit after the freeze; footer apply (scripts/apply-footer.py) if claude/footer-unpin lands; verify-as-you-can-see.py to # ci-shards; stale-plant fixes (report only); consolidate hint wording; separate exam-guidance label from on-screen calculator after 2 Nov (docs/todo.md; Jon to confirm the withheld list).
