# Handover: home lane

The home lane's running handover (canon §7.8.2). Only home-lane sessions edit this file; the cloud lane's is
`docs/handover/cloud.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**STANDING RULE (Jon, 7 Oct 2026):** when a contract finishes and the next queued contract's start condition is
met, start it without asking. Stop only for a STOP IF, a decision no standing ruling covers, or an empty queue.

**Home lane owns:** shared code, shared assets, CI and canon (contract F's shared fixes, then contract C), and every
docs PR: `docs/todo.md`, the roster's listed section, relisting fixed games (batched).

**QUEUE (home lane):** done 8 Oct: DET (#144), CLAIM (#145), ESSENTIALS (#150), UPDATES (#151). Their verbatim
contracts and notes moved to `docs/history/handover-home-archive.md` ("QUEUE as of 8 Oct") in contract CTX. Then:
1. **Contract CTX: PR on `claude/ctx` (8 Oct; see its entry below).** Merge on a green Gate once Jon has answered
   the PR's "For Jon" list (its STOP IF). Verbatim (Jon, 8 Oct):
   > TASK (home lane, after UPDATES merges and main is green): Cut what every Claude Code session loads before it
   > starts work: CLAUDE.md down to standing rules and pointers, each handover down to current state plus its last
   > three entries, history moved to archives nobody loads by default, and a CI size limit so it can't creep back.
   > ROOT CAUSE: Measured 8 Oct on main: CLAUDE.md is 159 KB and loads automatically into every session in both
   > lanes; most of it is dated "## Handover —" sections back to 3 Oct. docs/handover/cloud.md (56 KB) and
   > docs/handover/home.md (64 KB) are read first by instruction and hold every entry since 7 Oct.
   > .claude/rules/*.md add about 40 KB. A fresh cloud session starts at 16% context before reading its task,
   > which forces checkpoints after two or three games.
   > CLASS CHECK: Yes: shared infrastructure every session loads, and the absence of any limit on it. Fix at that
   > layer: restructure once, move history out of the load path, and add a CI check with a size limit. Not by
   > trimming individual pastes or by asking sessions to skim.
   > EXACT CHANGE: 1. Inventory first (in the PR description): every standing rule, ruling and lesson in
   > CLAUDE.md, each mapped to where it now lives: CLAUDE.md (still needed every session), canon (already there:
   > cite the section), or docs/history/claude-md-archive.md (history only). Nothing is deleted; everything is
   > moved or kept. 2. CLAUDE.md, target <= 15 KB: project overview (short); the standing rules sections that
   > apply every session (checkpoint discipline, check-changed before pushing, watch main after merging, two
   > lanes and who edits what, the cloud-claim rule, Jon never amends contracts: PC sends complete pastes);
   > pointers to canon, the handovers, the register, the roster, the archive. Every dated "## Handover —" section
   > moves verbatim to docs/history/claude-md-archive.md (newest first). 3. Handovers, target <= 15 KB each:
   > docs/handover/home.md keeps its header (rules, queue, standing rulings) and its newest three dated entries;
   > older entries move verbatim to docs/history/handover-home-archive.md. docs/handover/cloud.md: the same, to
   > docs/history/handover-cloud-archive.md, BUT only when the cloud lane has no open PR and its cloud-remaining
   > line is empty (it is at a checkpoint). If it isn't, skip cloud.md in this PR and leave a one-line note in
   > home.md to do it at the next cloud checkpoint. 4. Scripts that read CLAUDE.md (on main 8 Oct:
   > bank_common.py, check-theme.py, ci-deps.py, extract-banks.py, gen-simultaneous.py, verify-log-laws.py,
   > verify-quadratic-factoriser.py): find what each reads. If it needs content that moves, point it at the
   > content's new home (canon or the archive) in this PR; prove each still passes. 5.
   > scripts/check-context-size.py (CI, own ci-line header): fails if CLAUDE.md > 20 KB or either handover >
   > 20 KB (limits a little above the targets so a normal entry fits); prints each file's size. Self-test: a
   > planted 25 KB CLAUDE.md fails. 6. Roster header: .claude/rules/game-roster.md's title still says "74 games
   > on the portal, 23 unlisted" (91 and 6 after #142): a hand-typed count beside the data. Drop the counts from
   > the title or generate them; don't hand-type new ones. 7. Report in the PR: bytes before and after for
   > CLAUDE.md, both handovers and .claude/rules/ total.
   > DO NOT TOUCH: canon's content (cite it, don't move things into it unless the inventory shows a rule exists
   > nowhere else, and then list it); the roster's rows (the only copy); .claude/rules/ files other than the
   > roster title; any game; the workflow beyond what the new check's ci-line header gives; the meaning of any
   > rule (move text verbatim; reword nothing except pointers).
   > SUCCESS CONDITION: CLAUDE.md <= 15 KB with every every-session rule present; each handover <= 15 KB
   > (cloud.md may be deferred per step 3); archives hold the moved text verbatim; every script that read
   > CLAUDE.md passes; the size check passes and catches its planted file; the inventory and before/after sizes
   > are in the PR; merged on a green Gate; main green; home.md handover current.
   > STOP IF: a rule appears only in a dated handover section and it is unclear whether it still stands (list it
   > for Jon; don't guess); a script depends on CLAUDE.md content in a way that can't be repointed without
   > changing what it checks; the cloud lane has an open PR touching docs/handover/cloud.md (skip cloud.md, per
   > step 3).
2. **F1 batch 5: PARKED on `claude/f1-batch5` (worktree E:/jon/mg-b5), pushed, no PR.** Done and committed:
   angle-ace, word-problem-decoder, free-daily-pizza, split-it, six-sevens-bruv on MaffsLock (each passes
   check-answer-lock on seeds 1-3 and its own verifier), trig-wars (tap-through now also aims above 45 degrees;
   seeds 1-12 pass) and truth-buster added to MIGRATED. Still to do: 52dle, distinctly-average, seven-bridges.
   Then rebase on main, check-changed, PR. Lesson: a sweep that answers at once needs `bc.NO_LOCK_FRESH_INIT`;
   a top-level `const endGame` cannot be stubbed by `window.endGame =`: keep `function endGame(){finishGame()}`.
- **cloud.md not trimmed (contract CTX step 3):** the cloud lane had PR #154 open on it. Trim it to its header and
  newest three entries (to `docs/history/handover-cloud-archive.md`) at the next cloud checkpoint.
3. **Then** the remaining listed games, Year 6/KS3/GCSE/Core first, 8 per batch, until NOT_YET is empty.
   **Before building each batch** (contract CLAIM, canon §7.8.2): read `cloud-remaining:` in
   `docs/handover/cloud.md` on main and drop every game on it from the batch. Never claim or edit a game on that
   line. For a listed game the claim is a process lock only: check-answer-lock.py still judges it as unclaimed.
- **Checkpoint rule:** stop after every 2 batches merged (main green), or at the next batch boundary when Jon
  says "checkpoint". At each stop, update this file.

**Jon's rulings, 7 Oct:** eigenvector-engine-f0-005 is not a judgement call (SR-17: a scalar multiple of an
eigenvector is never a wrong option, whatever the prompt says about "simplest"): `jc: false` (in #108). The
verifier-lines-in-the-workflow question is answered by contract V: neither lane edits the workflow for a verifier.

## 2026-10-08 (home): contract CTX, what every session loads (branch `claude/ctx`, worktree E:/jon/mg-ctx)

- **Sizes (bytes, before -> after):** CLAUDE.md 159,172 -> 12,246; home.md 63,666 -> ~13,300;
  cloud.md 55,721 (deferred); .claude/rules/ 42,011 -> 41,960. Canon 148,526 -> 175,803 (§12).
- **CLAUDE.md** keeps the every-session rules, the cloud-claim rule (copied verbatim from canon §7.8.2), "Jon never
  amends contracts: PC sends complete pastes" (new: it existed nowhere; wording from the contract) and a "Where
  things live" pointer block. Every other section moved verbatim (proof: every non-blank old line is in the new
  file, the archive or canon §12, except the one reworded pointer sentence).
- **Canon §12 (new):** the sections that existed only in CLAUDE.md: check-site tiers 1-4, no rejection sampling,
  `MaffsOptions.build()`, generator ranges, scaffolds fade, accessibility, tiered banks, level colours, the Firebase
  leaderboard. Four canon pointers to "CLAUDE.md" now say §12.
- **Archives:** `docs/history/claude-md-archive.md` (dated handovers, state sections, and reference sections canon
  already holds, each headed with where it lives), `docs/history/handover-home-archive.md` (the done contracts'
  queue text and every entry before UPDATES). cloud.md deferred (cloud PR #154 open on it).
- **`scripts/check-context-size.py`** (site-wide ci-line): CLAUDE.md and both handovers <= 20 KB; self-test plants
  a 25 KB CLAUDE.md. Roster title no longer carries hand-typed counts.
- **STOP IF hit, answered (Jon, 8 Oct):** seven rules lived only in dated sections; all stand. Placed as he named:
  canon §3.4 (New & updated badges, his Updated definition verbatim), §3.5 (/updates/: describe a false claim, never
  quote it), SR-24 (counterexample refutes the statement as written), SR-25 (words, figure and key agree), §0.4 (register
  files edited by hand), §7.9 (verifiers read the page's feedback, not a wrapped mfg; pointer in CLAUDE.md), CLAUDE.md
  "Session practice" (`--against` scratch copy; never `| tail` under a timeout). Then merge on a green Gate.
## 2026-10-08 (home): contract UPDATES, the October quality entries on /updates/ (branch `claude/updates`)

- **STOP IF hit (item 5's fact check, before committing):** item 3's American-wheel example was not true on main.
  No game names the wheel; wrong-on-the-internet (listed) still keys roulette `P(black) = 18/38` with no wheel
  stated (audit tranche 2's open fix: "say 'American wheel', or key 18/37"). **Ruling (Project Claude, 8 Oct):**
  drop it; item 3 now ends "for example, which method to use for quartiles." Items 1, 2 and 4 unchanged.
  wrong-on-the-internet's roulette item is still an open SR-17 fix for a later batch.
- **Claims confirmed on main:** Linear Equation Solver marks `b` (every optimal move) full, `s` (valid but slower)
  half the points at stake with the quickest route shown, `e` named (154 one-side ÷ errors, "Whatever you do to
  one side, do to the other side too"). core-maths-paper1 (listed) states "Using the (n + 1)/4 method".
- **Page:** the "Every answer checked again" note after "Which tax year?", then first items under New, Clarified
  and Improved in the October section. No existing entry touched; the /resit/ history links stay (they redirect).
## 2026-10-08 (home): contract ESSENTIALS, BUILT on `claude/essentials` (worktree E:/jon/mg-ess), MERGED (#150, 69d05df)

**MERGED 8 Oct (#150, 69d05df) on a green Gate.** Locally, Test the Claim (`generateWrongContexts is not defined`
under Playwright's Node v24 `node -e`) and Negative Number Line (320x568 fold, 536 vs 528) fail on main too: local
environment only, CI green. Worth a look if a local run must be clean.
- **/resit/ -> /essentials/**: page moved (git mv), heading "Essentials" plus the teacher line, analytics section
  `essentials`; /resit/ is a meta-refresh stub (spec-map pattern, registered in check-footer.py). games.json key,
  apply-meta/check-meta, check-resit-page.py (PAGE; filename kept), check-canonical-links RESOLVE/LEVEL pages,
  publish scope, ci-deps KNOWN_TOP, sitemap, homepage badge ("Essentials", section `essentials-link`, item
  `open-essentials`), test-section-clicks, workflow labels all follow. Title: "Essentials: GCSE Foundation
  Maths Games | MaffsGames" (description kept: teacher metadata).
- **Not done on purpose:** /resit/ is NOT in check-canonical-links' REDIRECTS: that would fail the /updates/
  history links to /resit/, which contract UPDATES says stay as written (they redirect). Say so in the PR.
- **Student surfaces:** comic-caper and kiln-disaster description/og/twitter now "A GCSE escape room on ...";
  the four "for a GCSE resit class" card notes (homepage, /escape-rooms/) now "Built from a site user's
  request. Want something built?".
- **scripts/check-student-labels.py:** visible text, alt/title/aria-label/placeholder, script strings (comments
  stripped) and description/og/twitter meta of games/**/index.html, escape-rooms/*/index.html and the portals
  (index, escape-rooms, op). Self-test: the old comic-caper description and three more plants caught; comments
  not flagged. **In the workflow's site-wide list, NOT a ci-line** (a ci-line is selected per named page on PRs;
  this must see every page): a departure from the contract's wording, say so in the PR. **given-that** has a
  tree-diagram question about students re-sitting (6 hits): a KNOWN exception, reported not failed, flagged
  for Jon (game content is DO NOT TOUCH).
- **Homepage:** title "MaffsGames — Free Maths Games for KS3, GCSE, Core Maths and A-Level"; description (also
  og, new twitter tags) "Free maths games and 15-minute escape rooms for UK schools, KS3 to Further Maths,
  including GCSE Foundation and Core Maths. No sign-up, no personal data." No game count AND no room count
  ("eight" vs 8 cards / 11 room folders: same class); subtitle and JSON-LD now "KS3 to Further Maths". Draft
  wording for Project Claude to review in the PR. Choice recorded: the number is dropped, not generated.
- **Canon:** new §7.5.3 (the rule, the check, KNOWN, the teacher line, no hand-typed counts); analytics mapping
  (resit-link->essentials-link, open-resit->open-essentials, resit->essentials, page views) in §1.3; §2.1 and the
  CI tables follow the new address.
