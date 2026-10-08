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
3. **CHANGED-UTF8: DONE, #178 merged 8 Oct (d73d3b6).**
4. **GA4-COUNTRY-CANON: DONE, #179 merged 8 Oct (3c3217c).**
4a. **VOCAB-SHOWTHAT: DONE, #180 merged 8 Oct (47ee9b9)** (Jon, 8 Oct, sent later: run after GA4-COUNTRY-CANON, before F1 batch 7). The "show
   that" tooltip in `schools/assets/exam-vocab.js`; closes factor-theorem-t5-009 unless the cloud lane holds that game.
5. **F1 batch 7, then F1 batch 8**, exactly as the standing F1 item below states (8 per batch, Year 6/KS3/GCSE/
   Core first; read `cloud-remaining:` in `docs/handover/cloud.md` on main before building each batch and drop
   every game on it).
6. **CHECKPOINT after batch 8 merges with main green:** update this file and stop. Do not start batch 9 in that session.
7. **DOCS-SMALL: first item NEXT session, after the batch 8 checkpoint** (Jon, 8 Oct). Verbatim below. (a) Roster
   convention: a generated game's row says "N per session, generated", a bank game's gives its bank size;
   just-pythag-it-bruv's row "20 per session, generated (round 1 from 15 triples and their sizes; rounds 2 and 3
   generated)"; list other generator rows noticed. (b) /updates/ 8 Oct, Updated badge: "Correlation or Coincidence:
   now 84 questions, twice as many as before." STOP IF its bank on main is not 84, or the roster parser reads the count.
- **F1 batch 7: in progress, draft #182, branch `claude/f1-batch7`, worktree E:/jon/mg-b7.**
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

<details><summary>Queue item 7 (DOCS-SMALL), verbatim (Jon, 8 Oct)</summary>

> TASK (home lane, DOCS-SMALL; first item next session, after the batch 8 checkpoint): Two docs fixes from 8 Oct 2026,
> in one docs PR.
> ROOT CAUSE: (a) The roster row for just-pythag-it-bruv says "20 questions in three rounds". Project Claude read that
> as a 20-item bank and wrongly told Jon the game was below the 40-50 minimum. The game generates every question each
> session (15 triples with sizes, orientation and side varied in round 1; fresh non-square lengths in round 2; five
> contexts with large number pools in round 3), so 20 is the session length, not the bank. (b) correlation-or-
> coincidence's bank went from 42 to 84 items on 8 Oct (cloud lane, Jon's contract), with no /updates/ entry. Twice
> the questions is a change a returning student notices in what they meet, so it earns the Updated badge under canon
> §3.4.
> CLASS CHECK: (a) is an instance of a pattern: a roster count that does not say whether it is a bank or a session.
> Fix it at the roster's convention. Canon or the roster's header states that a generated game's row says "N per
> session, generated", and a bank game's row gives its bank size. Apply that to just-pythag-it-bruv, and to any other
> generator rows you find while editing. Do not audit every row in this PR; list any you notice. (b) is local: one
> missing entry.
> EXACT CHANGE: 1. .claude/rules/game-roster.md: add the convention line to the roster's header notes.
> just-pythag-it-bruv's row says "20 per session, generated (round 1 from 15 triples and their sizes; rounds 2 and 3
> generated)". Keep the rest of the row. 2. /updates/, a new entry dated 8 Oct, Updated badge: "Correlation or
> Coincidence: now 84 questions, twice as many as before." If an 8 Oct entry already exists, add the line to it.
> 3. docs/handover/home.md updated.
> DO NOT TOUCH: any game page; other roster rows' content, beyond rows you confirm are generators (list them in the
> PR; only change those if the change is just the count wording); canon §3.4.
> SUCCESS CONDITION: the roster checks pass; /updates/ shows the line with the badge; merged on a green Gate; main
> green; handover current.
> STOP IF: correlation-or-coincidence's bank on main is not 84 (report the count, and don't write the line); the
> roster parser reads the count field so that new wording breaks it.

</details>

**Jon's rulings, 7 Oct:** eigenvector-engine-f0-005 is not a judgement call (SR-17: a scalar multiple of an
eigenvector is never a wrong option, whatever the prompt says about "simplest"): `jc: false` (in #108). The
verifier-lines-in-the-workflow question is answered by contract V: neither lane edits the workflow for a verifier.

## 2026-10-08 (home): VOCAB-SHOWTHAT (#180, branch `claude/vocab-showthat`)

- `schools/assets/exam-vocab.js`: two strings only, "show that" (Jon's exact text) and "hence show" ("prove" -> "reach").
  Only factor-theorem loads the file (STOP IF clear); its "show that" questions are all numerical (f(a) = 0).
- Proof: on the stub server in Chromium, factor-theorem practice Q3's tooltip reads the new text.
- factor-theorem-t5-009 closed here (`status: fixed`, `pr: 180`, `ruling:` Jon's 8 Oct ruling): nothing claimed on
  `cloud-remaining:`, no open PR touched factor-theorem or exam-vocab.js. The cloud lane's factor-theorem queue already
  left t5-009 out.

## 2026-10-08 (home): GA4-COUNTRY-CANON (#179, merged 3c3217c)

- Canon §1.2.1 "GA4 country tabs" added after §1.2 (the analytics section), in #153's proposed text, plus "Live only once
  Jon has installed it" from the contract's fallback line. The contract's anchor, a "'Users' are not people here" note,
  does not exist in canon; #153's own reading bullet says it, so that bullet now opens "'users' are not people here".
- STOP IF checked: #153's description and `docs/ga4-country-setup.md` agree on what is collected (aggregates GA4
  already holds; nothing new; site, analytics.js, endpoint and privacy page unchanged).

## 2026-10-08 (home): CHANGED-UTF8 (#178, merged d73d3b6)

- `check-changed.py` reconfigures its own stdout and stderr to UTF-8 (errors="replace") at the top of `main()`. Python
  here 3.14.6, CI 3.12: `reconfigure` exists on both. **Proof:** with a planted failing check printing "£5 → ✓",
  `python scripts/check-changed.py > out.txt` on main crashes (`UnicodeEncodeError` on "→"); this version completes,
  writes the failing check's tail and the summary. The `PYTHONIOENCODING` follow-up note is removed. **Still true for
  the verifiers themselves:** a verifier run on its own with output redirected can crash the same way (seen on
  verify-truth-buster and verify-just-pythag-it-bruv, 8 Oct); run those with `PYTHONIOENCODING=utf-8`.
- **Windows-only false failure seen:** verify-negative-number-line fails locally on main too (320x568: Confirm 536, fold
  528) while CI is green. Not a regression; ignore it in local check-changed runs.

