# Handover: home lane

The home lane's running handover (canon §7.8.2). Only home-lane sessions edit this file; the cloud lane's is
`docs/handover/cloud.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**STANDING RULE (Jon, 7 Oct 2026):** when a contract finishes and the next queued contract's start condition is
met, start it without asking. Stop only for a STOP IF, a decision no standing ruling covers, or an empty queue.

**Home lane owns:** shared code, shared assets, CI and canon (contract F's shared fixes, then contract C), and every
docs PR: `docs/todo.md`, the roster's listed section, relisting fixed games (batched).

**QUEUE (home lane), Jon, 8 Oct 2026 (night)**, replacing the checkpoint's "ask Jon for that queue" note. Run in
order; the standing rule applies (start the next item when one finishes; stop only for a STOP IF, an unruled
decision, or a checkpoint). Each contract's verbatim text is below the list; move it to the archive when it merges.
1. **ESSENTIALS-WORDING: DONE, #172 merged 8 Oct (c1fc37a).** Its verbatim text was in Jon's queue message only.
2. **RELIST-3: in progress, branch `claude/relist-3`, worktree E:/jon/mg-r3** (Jon, 8 Oct, sent after the queue). It
   supersedes RELIST-ES-TB, sent minutes earlier: same relists, plus listing Just Pythag It, Bruv (Jon approved it).
3. **CHANGED-UTF8.**
4. **GA4-COUNTRY-CANON.**
5. **F1 batch 7, then F1 batch 8**, exactly as the standing F1 item below states (8 per batch, Year 6/KS3/GCSE/
   Core first; read `cloud-remaining:` in `docs/handover/cloud.md` on main before building each batch and drop
   every game on it).
6. **CHECKPOINT after batch 8 merges with main green:** update this file and stop. Do not start batch 9 in that session.
- **Answer-lock L1 flake:** act only if it recurs (the follow-up below stands).
- **Standing F1 item:** the remaining listed games, Year 6/KS3/GCSE/Core first, 8 per batch, until NOT_YET is empty
  (NOT_YET: 40). **Before building each batch** (contract CLAIM, canon §7.8.2): read `cloud-remaining:` in
  `docs/handover/cloud.md` on main and drop every game on it from the batch. Never claim or edit a game on that
  line. For a listed game the claim is a process lock only: check-answer-lock.py still judges it as unclaimed.
- **Follow-up (home lane, small):** `check-changed.py` crashes (`UnicodeEncodeError`, cp1252) printing a failure when
  its output is redirected to a file on Windows. Until fixed: `PYTHONIOENCODING=utf-8 python scripts/check-changed.py`.
  (Queue item 3 fixes it; remove this note when it merges.)
- **Follow-up (home lane, CI): Answer lock L1 failed on main once (b66ccde, run 37776985917)** with five games at
  once (binomial-blaster, curling-friction, differentiation-duel by touch at 390px; force-resolver, moments-master
  UNPLAYABLE after Start). The same slice passed 20/20 locally on that commit, the parallel run (3878582) was green, and
  a rerun of the failed job passed. Canon 7.6.0 says a verdict never depends on timing: if it recurs, find what the
  driver waits on that a slow runner breaks (start(), the touch path), and fix it there, not with retries.

<details><summary>Queue items 2 (RELIST-3), 3 and 4, verbatim (Jon, 8 Oct)</summary>

> TASK (home lane, RELIST-3; run after ESSENTIALS-WORDING, before CHANGED-UTF8): List Just Pythag It, Bruv (Jon's
> approval) and relist Expectation Station and Truth Buster (canon SR-21), in one batched docs PR.
> ROOT CAUSE: just-pythag-it-bruv was merged unlisted on 4 Oct 2026 for Jon to play first. Jon played it and approved
> it, but the approval was never recorded, so it is still noindex and off every listing surface (Jon, 8 Oct 2026: "I
> approved it days ago"). expectation-station and truth-buster were unlisted on 6 Oct (SR-20) and now meet SR-21:
> verifier in CI with ci-line headers, and no open CRITICAL or HIGH in docs/audits/findings/<slug>.yml (checked on
> main c8e1b91: expectation-station none open; truth-buster t3-014 MEDIUM, t3-015 LOW, t3-016 MEDIUM). The roster's
> Unlisted section is stale on expectation-station: it says pc-001 awaits Jon's A/B ruling, but Jon ruled B, and the
> fix and the 40/40/40 bank are merged.
> CLASS CHECK: Not a bug in code: it is the existing listing and SR-21 processes, batched through the home lane as
> canon says. The approval going unrecorded is a process gap, not code. Record it in the handover and to-do as a Jon
> ruling with its date, so no later session asks again. No shared code changes.
> EXACT CHANGE:
> 1. Re-run all three verifiers and confirm each register state on main at the time of the PR.
> 2. just-pythag-it-bruv, as docs/todo.md's listing item states (the "Jon to play /games/just-pythag-it-bruv/; on
>    approval" item, about line 545), reading /resit/ as /essentials/:
>    - remove the noindex line, and update the page's head comment to say it is listed;
>    - portal; /essentials/ (Geometry and measures; Choose: Foundation; Calculator required); spec map G20; sitemap;
>    - leaderboard hub row, with its NOT_ON_HUB entry dropped (check-leaderboard-coverage.js);
>    - add it to SUITE in check-resit-page.py;
>    - move the roster row to its listed section;
>    - update canon §4.2 and canon §1's game total.
>    The /updates/ entry, under 8 Oct, New badge, in exactly these words (Jon's approved line):
>    "Just Pythag It, Bruv: Pythagoras' theorem in three rounds, starting with whole-number triangles. In the
>    Essentials section."
> 3. expectation-station and truth-buster: relist on every surface SR-21 and the to-do relist checklists name
>    (expectation-station: todo §1.55; truth-buster: its row in §1.58-§1.75). That covers the roster rows, back in
>    their listed sections at their old numbers (#59, #17); the portal; the sitemap; the spec map; and the
>    leaderboard hub (remove each from NOT_ON_HUB). Add either to /essentials/ only if it was there before unlisting.
> 4. Roster descriptions current: Expectation Station "120 questions (40 per level); Stage 1 states a relation, so
>    every table has one completion"; Truth Buster's count as its bank now stands.
> 5. /updates/, same 8 Oct entry as step 2. Expectation Station gets the Updated badge (canon §3.4: three times the
>    questions, and Stage 1 now always has one right answer, which changes what a student meets and how they are
>    marked). Suggested line: "Expectation Station: now 40 questions at each level, and every probability table has
>    exactly one right completion." Truth Buster gets a badge and a line only if its changes since unlisting meet
>    §3.4. Wording honest, no alarming numbers; name the maths, never the student.
> 6. docs/todo.md: close the listing item and the two relist rows, and record "Jon approved Just Pythag It, Bruv
>    after playing it (recorded 8 Oct 2026)". Keep the real-iPhone check open as a separate follow-up; it does not
>    block listing. Handover updated.
> DO NOT TOUCH: any game's page or bank, apart from the noindex line and head comment of just-pythag-it-bruv; the
> findings files (MEDIUM and LOW entries stay open, cloud lane's); screening-room, factor-theorem, glorious-gantt; any
> game on cloud-remaining:.
> SUCCESS CONDITION: all three are on the portal and the sitemap; just-pythag-it-bruv is on /essentials/ and has no
> noindex; the roster lists three unlisted games (screening-room, glorious-gantt, factor-theorem); the roster,
> coverage, theme, meta, label and essentials-page checks pass; merged on a green Gate; main green; handover current.
> STOP IF: any of the three verifiers fails on main; expectation-station or truth-buster has an open CRITICAL or HIGH
> by the time you start; a listing surface named here no longer exists; Truth Buster's §3.4 call is unclear (quote
> the change and ask Jon).

> TASK (CHANGED-UTF8): Stop scripts/check-changed.py crashing on Windows when its output is redirected.
> ROOT CAUSE: check-changed.py already runs each check with PYTHONIOENCODING=utf-8 and decodes its output as UTF-8,
> but it prints the failing check's last 15 lines to its own stdout. On Windows with output redirected to a file,
> that stream is cp1252, so a non-ASCII character (£, →, ✓) raises UnicodeEncodeError and the summary is lost.
> CLASS CHECK: Local. check-changed.py is the one Windows entry point that wraps the other checks, and it already
> sets the child encoding; the gap is its own stdout only. Eight scripts already reconfigure stdout the same way;
> CI (Linux, UTF-8) is unaffected.
> EXACT CHANGE: scripts/check-changed.py: at start-up, sys.stdout.reconfigure(encoding="utf-8", errors="replace")
> and the same for sys.stderr. Remove the PYTHONIOENCODING workaround note from home.md's follow-ups once merged.
> DO NOT TOUCH: the other scripts; the check selection logic; CI.
> SUCCESS CONDITION: on Windows, `python scripts/check-changed.py > out.txt` with a failing check whose output
> contains £ completes and writes the summary; merged on a green Gate; handover current.
> STOP IF: reconfigure is unavailable on the Python version CI or Jon's machine runs (report the version).

> TASK (GA4-COUNTRY-CANON): Record the GA4 country figures in canon.
> ROOT CAUSE: #153 merged the Apps Script and setup steps (docs/ga4-country-setup.md), but canon's analytics
> section does not say the events Sheet now gains country tabs from GA4's Data API, so the next reader of canon
> cannot tell where those figures come from.
> CLASS CHECK: Local: one missing canon line for one merged feature.
> EXACT CHANGE: docs/canon.md, the analytics section beside the "'Users' are not people here" note: add the line
> proposed in #153's PR description (read it with gh); if it proposed none, write: "Country figures (Jon, 8 Oct
> 2026): two tabs in the events Sheet, copied daily from GA4's Data API by docs/apps-script-ga4-country.js (setup:
> docs/ga4-country-setup.md). Aggregates only: nothing new is collected, and the site, analytics.js, the events
> endpoint and the privacy page are unchanged. Live only once Jon has installed it." Handover updated.
> DO NOT TOUCH: the script, its test, the setup doc, the privacy page.
> SUCCESS CONDITION: canon carries the line; merged on a green Gate.
> STOP IF: #153's description says anything that contradicts the setup doc on what is collected (quote both).

</details>

**Jon's rulings, 7 Oct:** eigenvector-engine-f0-005 is not a judgement call (SR-17: a scalar multiple of an
eigenvector is never a wrong option, whatever the prompt says about "simplest"): `jc: false` (in #108). The
verifier-lines-in-the-workflow question is answered by contract V: neither lane edits the workflow for a verifier.

## 2026-10-08 (home): RELIST-3 (branch `claude/relist-3`, worktree E:/jon/mg-r3)

- **Start state, main c8e1b91 (neither game nor its findings file changed by c1fc37a):** verify-expectation-station and verify-truth-buster pass; findings:
  expectation-station none open, truth-buster t3-014 MEDIUM, t3-015 LOW, t3-016 MEDIUM (stay open, SR-21).
  Neither is on `cloud-remaining:` (terrible-advice only). On Windows a verifier run redirected to a file crashes on
  cp1252 (same as CHANGED-UTF8): run with `PYTHONIOENCODING=utf-8`.
- **Done:** Pythag listed (noindex off, head comment, portal KS3 card with New badge, /essentials/ Geometry, spec map
  G20 as its own row, sitemap, hub row, NOT_ON_HUB dropped, SUITE, roster KS3 #98, canon §1 and §4.2); ES and TB
  relisted from their unlisting commits (059b2ec, e419439): portal cards (ES Updated badge, both its cards), sitemap,
  spec map (ES §3.9 rows), hub rows, NOT_ON_HUB, TB's spec-mapping EXCEPTIONS entry back; roster #59 (GCSE), #17 (KS3).
  /updates/: Jon's Pythag line under October New; his suggested ES line under October Improved. TB: no badge, no line
  (its changes since unlisting are SR-18 rewording, corrected figures, the lock, phone fit and a test-only lock-hint
  declaration: none meets §3.4). todo: listing item closed with Jon's approval recorded; iPhone check a separate
  open follow-up; §1.55 and §1.75 closed.
- **Deviation, for Jon:** the /essentials/ card says "One level", not "Choose: Foundation": the game has one level and no
  picker and reads no `?level=`, so a Choose card fails check-resit-page.py (and would promise a choice that isn't there).

## 2026-10-08 (home): ESSENTIALS-WORDING, "resit" off every public page (#172, merged c1fc37a)

- /updates/ (four lines) and /essentials/ (description, og:description, teacher line, intro) no longer say resit or
  post-16; games.json's /essentials/ description matches. The /updates/ link now goes to /essentials/.
- `check-student-labels.py` now scans essentials/index.html and updates/index.html (PORTALS); /essentials/ is no
  longer exempt; the self-test plants a label on each and requires it caught. Against main's copies the widened check
  finds 10 labels (5 per page). Canon §7.5.3 records Jon's rule.
- Remaining site-wide hits (all exempt): the two rooms' teacher.html notes (teacher surface); given-that (KNOWN); code
  and HTML comments in room.js, schools/assets, games and the /essentials/ head comment (history of /resit/ and the
  script name check-resit-page.py).

## 2026-10-08 (home): F1 batch 6 (#165, branch `claude/f1-batch6`, worktree E:/jon/mg-b6)

- **On MaffsLock, each with its declaration, seeds 1-3 and its own verifier passing:** sequence-solver, bearing-blitz,
  expected-damage, maths-court, equation-builder, fermi-lab, better-value, chart-interrogator. terrible-advice (the cloud
  lane's #160) also to MIGRATED. **NOT_YET: 40.** Chosen off the cloud lane's listed-games order; opened as a draft PR
  at the start so the cloud lane could see it.
- **Faults fixed beyond the swap:** sequence-solver and bearing-blitz wait on Next after a wrong answer (bearing-blitz's
  Fire was "disabled" by a CSS class only; the last life's miss waits too); expected-damage, maths-court and fermi-lab
  keep their own Next, which now acts only on an answered question (a double-click skipped one); maths-court's two
  attempts survive a double-click and a tapped card cannot re-mark; equation-builder's double Check no longer spends the
  retry and the shown key waits on Next; fermi-lab's Calculate Estimate marked and scored twice on a double-click, and a
  step could count twice; chart-interrogator (logs right answers only, so `mark_any`) marked a right answer twice on a
  second Enter inside its 600 ms advance, and a double Submit Comparison finished the game twice.
- **Declarations:** bearing-blitz and fermi-lab declare `start_sel` (no Start button), so the double-click on Start is
  real; equation-builder fills its slots from data and checks twice to spend the retry, stopping if the question moved on.
- **Verifiers:** sequence-solver and fermi-lab get `bc.NO_LOCK_FRESH_INIT` (they answer as soon as a question renders).
  better-value's page-load KaTeX poll keeps a raw timer, marked `// lock-ok:`.

