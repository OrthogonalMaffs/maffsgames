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
2. **RELIST-3: DONE, #176 merged 8 Oct (c0c825b).** (Jon, 8 Oct, sent after the queue.) It
   supersedes RELIST-ES-TB, sent minutes earlier: same relists, plus listing Just Pythag It, Bruv (Jon approved it).
3. **CHANGED-UTF8: DONE in this PR** (branch `claude/changed-utf8`, worktree E:/jon/mg-cu).
4. **GA4-COUNTRY-CANON.**
4a. **VOCAB-SHOWTHAT** (Jon, 8 Oct, sent later: run after GA4-COUNTRY-CANON, before F1 batch 7). The "show
   that" tooltip in `schools/assets/exam-vocab.js`; closes factor-theorem-t5-009 unless the cloud lane holds that game.
5. **F1 batch 7, then F1 batch 8**, exactly as the standing F1 item below states (8 per batch, Year 6/KS3/GCSE/
   Core first; read `cloud-remaining:` in `docs/handover/cloud.md` on main before building each batch and drop
   every game on it).
6. **CHECKPOINT after batch 8 merges with main green:** update this file and stop. Do not start batch 9 in that session.
- **Answer-lock L1 flake:** act only if it recurs (the follow-up below stands).
- **Standing F1 item:** the remaining listed games, Year 6/KS3/GCSE/Core first, 8 per batch, until NOT_YET is empty
  (NOT_YET: 40). **Before building each batch** (contract CLAIM, canon §7.8.2): read `cloud-remaining:` in
  `docs/handover/cloud.md` on main and drop every game on it from the batch. Never claim or edit a game on that
  line. For a listed game the claim is a process lock only: check-answer-lock.py still judges it as unclaimed.
- **Follow-up (home lane, CI): Answer lock L1 failed on main once (b66ccde, run 37776985917)** with five games at
  once (binomial-blaster, curling-friction, differentiation-duel by touch at 390px; force-resolver, moments-master
  UNPLAYABLE after Start). The same slice passed 20/20 locally on that commit, the parallel run (3878582) was green, and
  a rerun of the failed job passed. Canon 7.6.0 says a verdict never depends on timing: if it recurs, find what the
  driver waits on that a slow runner breaks (start(), the touch path), and fix it there, not with retries.

<details><summary>Queue items 4 and 4a, verbatim (2 and 3 moved to the archive when done) (Jon, 8 Oct)</summary>

> TASK (home lane, VOCAB-SHOWTHAT; run after GA4-COUNTRY-CANON, before F1 batch 7): Correct the "show that" tooltip
> in the shared exam vocabulary file.
> ROOT CAUSE: schools/assets/exam-vocab.js gives "show that" the definition "Prove this is true. Show every step of
> your working — you can't just verify it with numbers, you must derive it algebraically." That merges two different
> command words. "Show that" means the result is given and the student shows the working that reaches it. The
> working is often numerical: f(2) = 0 to show (x − 2) is a factor; a change of sign to show a root lies in an
> interval; "show that 3/4 of 60 is 45" at Foundation. "Prove" is the general argument. The rule the tooltip
> half-remembers is narrower: do not start from the given answer and work backwards. Found as factor-theorem-t5-009
> (shows on Q3, Q4, T1a, T3b, T7a, T10a, where the expected method is numerical). Ruled by Jon, 8 Oct 2026.
> CLASS CHECK: Shared infrastructure. The definition lives in a shared asset that any game can load, so it is fixed
> once, there, and every current and future user is corrected. Today only factor-theorem loads it; the fix is still
> made in the shared file, never as an override in the game.
> EXACT CHANGE: 1. schools/assets/exam-vocab.js, the 'show that' entry's plain text, exactly: "The answer is given
> to you. Write out every step that gets there. Working with numbers is fine when that is the method, such as
> showing f(2) = 0. You must not start from the given answer and work backwards." 2. Check the 'hence show' entry
> ("Use your previous answer to prove this result — show every step.") and change "prove" to "reach": "Use your
> previous answer to reach this result — show every step." The 'prove that', 'prove', 'verify that' and 'verify'
> entries stay as they are. 3. Close factor-theorem-t5-009 in docs/audits/findings/factor-theorem.yml in this PR,
> with a resolution line citing Jon's ruling. This is the one cloud-lane findings file the home lane edits here;
> check cloud-remaining: and the open PRs first, and if factor-theorem is claimed or has an open PR, leave the
> findings file to that PR and say so in the handover. 4. docs/handover/home.md updated.
> DO NOT TOUCH: every other entry in exam-vocab.js; the tooltip mechanism (wrapExamVocab's re-wrapping bug, t5-008,
> is in the cloud lane's factor-theorem contract); any game page.
> SUCCESS CONDITION: the 'show that' tooltip on factor-theorem Q3 shows the new text in Chromium; no other tooltip
> text changes (diff shows two strings); t5-009 closed (or handed to the cloud PR as above); merged on a green Gate;
> main green; handover current.
> STOP IF: exam-vocab.js is loaded by more pages than factor-theorem and any of them uses "show that" for a genuine
> proof (quote the question and ask Jon); the factor-theorem cloud PR has changed how the tooltip text is read so
> that this edit does not show.

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

## 2026-10-08 (home): CHANGED-UTF8 (branch `claude/changed-utf8`)

- `check-changed.py` reconfigures its own stdout and stderr to UTF-8 (errors="replace") at the top of `main()`. Python
  here 3.14.6, CI 3.12: `reconfigure` exists on both. **Proof:** with a planted failing check printing "£5 → ✓",
  `python scripts/check-changed.py > out.txt` on main crashes (`UnicodeEncodeError` on "→"); this version completes,
  writes the failing check's tail and the summary. The `PYTHONIOENCODING` follow-up note is removed. **Still true for
  the verifiers themselves:** a verifier run on its own with output redirected can crash the same way (seen on
  verify-truth-buster and verify-just-pythag-it-bruv, 8 Oct); run those with `PYTHONIOENCODING=utf-8`.
- **Windows-only false failure seen:** verify-negative-number-line fails locally on main too (320x568: Confirm 536, fold
  528) while CI is green. Not a regression; ignore it in local check-changed runs.

## 2026-10-08 (home): RELIST-3 (#176, merged c0c825b)

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

