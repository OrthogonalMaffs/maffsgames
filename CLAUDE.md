# MaffsGames — CLAUDE.md

## Project Overview
Free curriculum-aligned maths games for UK schools. 96 games and eight escape rooms live (Regression Rumble withdrawn 30 Sep 2026 pending a data rebuild). Separate from MathsWins (mathswins.co.uk).

- **Repo:** https://github.com/OrthogonalMaffs/maffsgames
- **Live site:** maffsgames.co.uk (GitHub Pages)
- **maffsgames.com:** bought 24 Sep 2026, 301-redirects to maffsgames.co.uk at the Cloudflare edge
  and serves nothing of its own. See `docs/domain-maffsgames-com.md` — including why the .co.uk stays
  canonical, and the two IONOS prompts to ignore
- **Contact:** contact@maffsgames.co.uk
- **BMC:** buymeacoffee.com/maffsgames
- **Project brief:** `.claude/rules/project-claude.md` — the mission, the audience, the division of
  labour and the platform principles. Loaded at the start of every session; read it with the note
  under **Task Contract** at the end of this file.

## Handover — 2026-10-03: tax-theft fixed; the money-answer standard (canon §7.1.3)

- **PR #3 merged** (`9f9ce59`); the three games' live pages are byte-identical to the merge.
- **Tax-theft (todo START item 4) is fixed.** Income tax is charged on taxable income (20% on the first
  £37,700, 40% to £125,140, 45% above); the game had stretched the basic band to a gross £50,270,
  under-taxing every salary over £100,000 by £500 to £2,514. Medium's £105,000 and £118,000 (taper maths)
  are now £86,500 and £97,500. Every key comes from `computeKeys()`, in whole pence, from the payslip's
  figures. Hard's closing line names the reduced allowance below £125,140.
- **Money-answer standard, canon §7.1.3:** numeric match first; a right amount wrongly written (114.4,
  3050.0) gets the format message and a resubmit, never a mark. `moneyResult()` in tax-theft is the
  reference. `scripts/verify-tax-theft.py` (CI group B) plays all 20 salaries; 489 FAILs on the old game.
- **Next:** START item 5 (apply §7.1.3 to every money game; shared helper or not, Jon's call), item 6
  (other income-tax games: only `core-maths-paper1`, which also states NI at 12%, not 8%), then items 2–3.

## Handover — 2026-10-02 (late): wrong-keys batch 1 + verifier coverage (PR #3)

- **Wrong-keys batch 1 is reapplied** (patch 0001, old `2e1ffe5`): the keys in stat-attack,
  graph-sketcher and growth-and-decay are corrected, and each game has a `scripts/verify-<slug>.py` that
  recomputes every key from the question's own data. Each verifier failed on the uncorrected game
  (83, 34 and 17 FAILs) and passes on the corrected one.
- **CI now enforces verifier coverage.** `scripts/check-verifier-coverage.py` (Tiers 1 + 2, stdlib) fails
  if any `scripts/verify-*.py` or `scripts/test-*.py` is not run by `check-site.yml`, unless its `HELD`
  table declares it with a reason (only `verify-regression-rumble.py`). A new verifier must be added to
  a group, or the run fails. Five verifiers were not running before this: the three above, plus
  `verify-quadratic-factoriser.py` and `verify-parent-guides.py`. All five pass and are now in group B.
- **Tax-theft is NOT started**; patch 0001 never held tax-theft work. Its rulings, and a docs trace of
  the misread 'whole pounds' ruling, are to-do START items 4 and 5.

## Handover — 2026-10-02 (cutover): this repository started fresh

- **Started fresh on 2 Oct 2026**, public, from one commit (`ab701b4`, then `6c478cb` for `CNAME`).
  **Commit hashes and PR numbers in older notes, in this file, `docs/todo.md` and anywhere else, refer
  to `OrthogonalMaffs/maffsgames-archive`** (the old private repository, archived read-only).
- maffsgames.co.uk is served from this repository (Pages, legacy Jekyll build from `main` at `/`;
  `_config.yml` keeps INTERNAL files unpublished, canon §7.7). Cutover measured no downtime.
- The repository is public, so Actions minutes are no longer metered; the per-run cost notes below
  are history, not a constraint.

## Handover — 2026-10-02 (night)

- **Pages publish scope (canon §7.7).** `_config.yml` now excludes every INTERNAL path (`CLAUDE.md`,
  `docs/` except `docs/art/`, `scripts/`, `data/`, `firebase/`, package and requirements files), and
  `scripts/check-publish-scope.py` (CI, Tiers 1 + 2) fails on any published file outside the SITE
  list, any excluded SITE path, and any SITE page that references an unpublished file. A new
  top-level path must be classified in one of the two places. Jon's personal email address is out
  of the repo's current files (the Apps Script copy holds a placeholder; history is unchanged).
- **Public-visibility audit ran (2 Oct 2026, read-only, gitleaks 8.30.1 over all 72 refs and the full
  history, plus pattern sweeps, PR/issue text and repo settings). Verdict: safe to make public after
  the actions Jon was given in that session.** No findings are recorded here, on purpose.
- **Actions minutes (diagnosed, NOT yet fixed).** The growth is in both run count and run duration:
  `check-site` went from ~4 runs/day at 3 billed min (21-24 Sep) to ~85 runs/day at a median 18 billed
  min (2 Oct). Each PR commit runs twice (`push` on every branch + `pull_request`), and per-run cost
  grows with every verifier added to `check-site.yml`, which all check the whole library. Fix held
  until Jon decides on repo visibility (public repos get free Actions minutes).

## Current State — 2026-09-28

**`main` has moved well past `1a37ad7`.** Later the same day it took:
- Chart Interrogator Contract B;
- Log Laws Solve;
- the portal ticker's live standing;
- the Spot the Error audit and two fixes;
- PR #7, the parent guides audit;
- PR #8, `coordinate-geometry-dash:233` plus the value-equivalent options scan.

`docs/todo.md`'s START OF NEXT SESSION block has each one; it, not this line, is the handover.
Checker tier 4, layer A (bank extraction + lint) was built, verified and regression-proven on
26 Sep and committed on 27 Sep (`175fb64`): `scripts/bank_common.py`, `scripts/extract-banks.py`,
`scripts/check-banks.py`, `data/check-ledger.json` and `docs/checker-tier4-design.md`, with its step in
`.github/workflows/check-site.yml` running on every push. Start at `docs/todo.md` — its
**START OF NEXT SESSION** block is the running handover.

**Tiers 1–3 prove a page runs and can be played; nothing before today inspected the question
data itself.** `extract-banks.py` reads every game's bank back from the live page under
Playwright (so a runtime patch is included, not just the source literal); `check-banks.py` lints
it against eleven rules and tracks every known violation in `data/check-ledger.json`. All 97 games
are accounted for — 83 banks read live, 1 via a static fallback for a module-pattern IIFE
(`given-that`), 13 confirmed true generators with no static bank anywhere in source
(`distinctly-average` added 29 Sep 2026 — its window.DA_ITEMS pools are built by the same
kind of enumeration as `quadratic-factoriser`'s, not a hand-authored array; `six-sevens-bruv`
added 30 Sep 2026 — its 78 facts are enumerated, and `scripts/verify-six-sevens.py` checks them;
`free-daily-pizza` added 30 Sep 2026 — 518 items enumerated from parameter tables on `window.FDP`,
checked by `scripts/verify-free-daily-pizza.py`). CI
(`.github/workflows/check-site.yml`) runs it on every push and fails only on a violation not yet
in the ledger, or a ledger entry that no longer reproduces.

Two real, previously-unknown defects came out of the first run, on top of confirming three
already-known ones (matrix-crunch's dropped duplicate, formula-unlocked's `correct_override`
collision, and — while regression-testing the checker itself — a bug in the checker's own
`correct`/`correct_override` precedence that had been hiding the second): `test-the-claim:538`
sets `crBoundaryUpper` twice in one object literal (7, then 8), and the correct value is neither —
todo.md §1.14 has the full statistics; and `factor-theorem` and `test-the-claim` both
pass whole prose through KaTeX the same way `component-crusher` does (canon's §1.10), losing
their spaces on render. **B7's KaTeX check went through two wrong definitions on 27 Sep before
landing:** the shipped version kept its general-string half's 26-letter threshold, which
undercounted; dropping the threshold to "did any space get lost" overcounted instead, flagging
398 "hits" across 9 games, because LaTeX spacing is cosmetic and a space lost around `-1 + j` or
`(A + B) \cdot (C + D)` is correct rendering, not a defect. It is now defined on prose — two or
more adjacent real words surviving after every `\text{}`/`\mathrm{}`/`\operatorname{}` and bare
LaTeX command is stripped out, pinned by six fixture tests (`check-banks.py --selftest`). True
count: **3 games, 79 hits** (`component-crusher` 37, `factor-theorem` 39, `test-the-claim` 3) —
todo.md §1.10.

Layer A is one of five designed layers (A–E); only A is built. Layer C — recomputing an answer
from its own stored parameters, which is what would have caught Trig Worms, Modular Battle and
`es_gcse_005` on day one — is still not built. Full design, what each layer catches, what none of
them can (wording and pedagogy stay Jon's call), and a proposed new-game gate awaiting Jon's
ruling: **`docs/checker-tier4-design.md`**. Detail on the checker itself, including two rejected
designs for its KaTeX-rendering check and why they were rejected, is in the "Tier 4, layer A"
subsection below.

---

## Previous state — 2026-09-26

**Eight commits are unpushed and nothing is half-finished in the working tree.** Two pieces of
work landed since 25 Sep: the `.com` domain went live as a redirect, and both stray branches
were merged. A third, the spec mapping, is **deliberately part-way** — see below.

> ### `maffsgames.com` is live and redirects (24 Sep 2026)
>
> Bought 24 Sep, now a **301 to `maffsgames.co.uk` at the Cloudflare edge**, serving nothing of
> its own. Verified: apex, `www` and plain HTTP all 301, path and query preserved, one hop to a
> 200. **Nothing in this repo changed for it** — `CNAME`, the canonical tags (117 then, 139 now), `sitemap.xml`
> and `robots.txt` were already right for a `.co.uk`-canonical site, and all of them would have
> become wrong had the domains been flipped.
>
> The redirect is what protects the analytics: no page from this repo is ever returned on a
> `.com` URL, so the gtag snippet cannot run with a `.com` hostname. Confirmed against the live
> response — the body is Cloudflare's bare stub, no script tag, no `G-992JLHLP2D`.
>
> Full detail, the Cloudflare config, the rollback set and two traps worth knowing (the A
> records must stay **Proxied** or Redirect Rules never run; IONOS falsely claims the domain has
> no SSL and offers to sell one) are in **`docs/domain-maffsgames-com.md`**.

> ### Both stray branches are merged (24 Sep 2026)
>
> - **`cool-hawking`** — fast-forward, docs only. Added `.claude/rules/project-claude.md`, the
>   Project Claude brief, and took the task contract from six fields to seven (CLASS CHECK).
> - **`wizardly-gauss`** — `151baa4` leaderboard eligibility is completion, not a 10-question
>   count; `d3dc13a` Chart Interrogator spread grading. Only `docs/todo.md` conflicted, both
>   sides kept. Neither code file had been touched on `main` since the branch point.
>
> **What that merge exposed, and what was done about it:** removing the ten-question gate let
> thirteen games reach the boards for the first time. Eleven rank correctly. `estimation-golf`
> and `equatle` are **lower-is-better** and would have ranked backwards, so both are now gated
> off at the call site behind `LEADERBOARD_MODE_READY`. The call is left present and visible so
> the coverage check still sees it and lifting the gate is a one-word change. See to-do item 0.

**Spec mapping (Contract 1) is part-built and stops at a clean line.** `data/dfe-gcse-parts.json`
holds the DfE GCSE subject content as 97 statements split into 174 typed parts, derived
mechanically by `scripts/extract-dfe-tier.py` from the PDF vendored in `docs/sources/`. The
mapping itself — boards, crosswalks, the 95 games, the checker and the review doc — is **not
started**. To-do item 0c has the full state, including what is still owed and the one review step
Jon has outstanding.

The 23–25 September sessions were **prevention plus repair**: the checker learned to play the
games, the platform got the shared option-builder it never had, and six question-bank defects
were fixed. Detail in `docs/canon.md` §8.2c and the to-do.

- **Checker tier 3** (`scripts/check-site.py --tier 3`) plays every game. Baseline 190 PASS,
  0 FAIL, 6 WARN, 115 UNSUPPORTED over 311 runs, ~16 min. **Opt-in, not in CI.** Read the three
  load-bearing notes in the checker section below before touching it — especially that
  **UNSUPPORTED is not a failure**, which is what keeps the tier believable.
- **`MaffsOptions.build()`** (`schools/assets/options.js`) is the option-assembly helper the
  site never had. 32 games hand-roll `shuffle([correct, ...d])`; the Trig Worms rule had
  nowhere to live. Wired into 3 games only — **the retrofit of the other ~29 is parked**, see
  canon §8.2c.
- **Six bank repairs**, none of which tier 1 could ever have caught: `matrix-crunch:171` and
  `formula-unlocked:295` each rendered one option twice; `proof-builder:232` shipped the
  author's self-correction as a selectable option *and* had two distractors that were valid
  counterexamples; `normal-navigator:222` was unanswerable; `:241` accepted the wrong integer;
  and `normal-navigator` was **overwriting three of its own questions** with hand-written
  `QUESTIONS[n] =` patches aimed at the wrong indices.

**The lesson of the last session, and it is the cheap one to remember: patch the entry, not an
index.** A hand-written index is a guess that nothing was watching. It destroyed two good
questions, missed the broken one it was aimed at, and duplicated two others — and the repair
made the day before landed in a slot that was overwritten at load, so it reached nobody.

---

## Previous state — 2026-09-22

Tonight was a **content-quality** session, not an infrastructure one, and its main lesson is in the
two bugs it found. Both were live for months, both survived a full green checker run, and both were
caught only because Jon played the games and looked at the pictures.

- **Trig Worms** generated **impossible triangles**. `const angle=5*Math.floor(Math.random()*17)+15`
  yields 15,20..90,95; the comment claimed it avoided 90 and never had, and 95 was in there too.
  Neither can be the non-right angle of a right-angled triangle. At 95 degrees the adjacent goes
  negative, so the game asked for "the adjacent = -0.8" and marked **95 degrees** correct. That was
  2 of 17 angle values: **11.8% of every question, at every difficulty**. Its distractors could also
  collide (`asin` and `atan` of the same near-zero ratio both gave -5.1), shipping a question with
  the same option twice.
- **Modular Battle**'s dot grid **showed the wrong remainder**. It capped the drawing at 40 dots and
  scaled the counts, which cannot preserve a remainder: `46 mod 7` drew **3** red dots for an answer
  of **4**, and 3 was one of the four options. A student using exactly the strategy the picture
  invites was handed a wrong answer sitting on a button.

**This is the case for checker tier 4.** Tier 1 proves a page runs. It has nothing to say about
whether the maths is true, and neither of the above would ever fail it.

Three architectural rules landed in canon, each from an audit rather than a hunch:

- **§7.1.1 — KaTeX scope.** The rule covers *expressions*; a bare unit superscript (`cm²`, `m/s²`)
  may stay Unicode. The audit found raw Unicode notation in **17 games** in three sub-classes:
  loads KaTeX but never calls it; no KaTeX at all; KaTeX for the options but raw text for the
  explanation. Only `suvat` is fixed.
- **§7.5 — one register for every game** (superseding the 22 Sep lowest-tier rule, which moved
  `suvat`, `trig-worms` and `modular-battle` off KS3 styling). Since 2 Oct 2026: one shared
  stylesheet, a light/dark palette derived from the roster, checked by `scripts/check-theme.py`.
- **§7.6 — self-paced advance.** Games auto-advanced on a fixed timer, 800ms to 2400ms across
  **25 games**, and not one distinguished a right answer from a wrong one. A wrong answer now shows
  a `Next →` control and waits (`schools/assets/next-control.js`); a correct answer keeps its brisk
  delay; and **any pause must have something on screen worth reading**.

Eight games are on §7.6 so far: `suvat`, `trig-worms`, `modular-battle`, `differentiation-duel`,
`index-laws`, `integration-duel`, `log-laws`, `prime-or-composite`. `linear-equation-solver` and
`probability-pioneer` already implemented the pattern by hand and were left alone — and
probability-pioneer additionally enforces a **5s floor** before its button works, which is arguably
better than a bare button and is an open question for §7.6.

**The §7.6 rollout is blocked on content, not code.** Of the games still on a fixed timer, 11 have
authored explanation data (`mc`, `steps`, `hint`) that is **never displayed**, and 6 have none at
all. Adding a button to either group would ship a pause with a blank screen behind it. See the
todo's Group B and Group C.

---

## Previous state — 2026-09-21 (late session)

**The checker exists now: `scripts/check-site.py`, green in CI on every push.** It closes the
prevention gap the earlier 21 September session left open, and it justified itself immediately —
on its first run it found **two more games dead in production**, neither suspected:

- **Differentiation Duel** (`63c2478`) — `RULES` read `LEVEL` at `:626` while `const LEVEL` was
  declared at `:640`. Temporal dead zone, script halted on load, unplayable at every level. It came
  from sweep **`4b3d7d3`** (11 files, *"apply timer policy across platform"*), **whose other seven
  games are still unaudited** — see the todo's item 1.
- **Matrix Crunch** (`91bbd1b`) — bare `cos`/`sin` identifiers where their neighbours in the same
  array were quoted LaTeX strings. Introduced by `41d806b`, the commit that *added* the game on
  14 March, so **it never worked once, for anyone, in six months** — one of only five Further Maths
  games.

Also live from that session: **Factor Race** (`025ec00`) no longer rejection-samples; the
**newsletter and every MailerLite reference** are gone (`c0d07c3`) — the form id had shipped as the
literal placeholder `your-mailerlite-form-id`, so the signup 404'd for every visitor and no
newsletter was ever sent; and the portal now emits **`filter_applied` and `game_card_clicked`**
(`a476db7`). Site reports **344 pages, 0 fail, 0 warn**.

**What a green check does and does not mean.** Tier 1 proves every page loads and runs. It does not
prove a game is *correct*: the two games above were dead in a way a page load can see, whereas
`es_gcse_005` — a scenario no student could complete — had a clean console. Tiers 3 and 4 are the
ones that would catch that class, and neither is built. Green is a floor, not a warranty.

---

The earlier 21 September session, kept for the record — a game-integrity job, five commits:

- **Chart Interrogator** (`2ec80e0`) — the score bar had been broken since **22 March**. The
  leaderboard-teaser sweep `96381d74` inserted its `<div>` inside a single-quoted JS string, so the
  whole inline script failed to parse and no function was ever defined. Unplayable for six months.
- **Modular Battle** (`b685e44`) — **never once playable.** Two defects: the "Back to Games" sweep
  `76514c70` put an `<a>` between `setInterval(() =>` and its body (parse error), and behind it
  `generateChoices` rejection-sampled 4 distinct values from `0..mod-1` with `mod` as low as 2, so a
  quarter of questions froze the tab. The parse error had been masking the hang since 13 March.
- **Expectation Station**, three commits — `4917203` replaced a distractor loop that could not
  terminate on its own resources; `9b1c4e2` moved the game onto exact rationals, which fixed
  **`es_gcse_005`, an unwinnable scenario** (product 0.375 displayed as the tile "0.38", and Stage 2
  accepted only `|diff| < 0.005` against the 4dp product — the difference is exactly 0.005);
  `9e6d9e1` lets the two loss-modelling scenarios deal negative distractors.

See `docs/game-integrity-2026-09-21.md` for the full findings, the loop scan over all 95 games, and
what the console checker must catch. Its tiers 1 and 2 are now built as `scripts/check-site.py`;
**its tiers 3 and 4 — drive questions with a watchdog, and play the correct answer to assert it is
accepted — are still the outstanding prevention layer**, and tier 4 is the only one that would have
caught `es_gcse_005`.

The 17 September session shipped eleven commits, all live:

- **The Comic Caper** (`comic-caper`), a new GCSE resit room (factors, primes, HCF) built from a site
  user's request — room, pictures, wording fixes (`d2b27a2`, `9e0bf8a`, `f6c25da`). Its locks are
  bank batch 6.
- **Every room now draws its variants jointly** (`0907f6e`), so no two locks in a play can collide. See
  "Cross-lock collisions" below.
- **Teacher pages** only claim the failure picture shows mid-game when a lock sets `missArt` (`215b084`).
- **The Kiln Disaster** (`kiln-disaster`), an eighth room and the second GCSE resit one — multiples, LCM and
  order of operations, on bank batch 7. Its keypad is the site's **first two-digit keypad** (`digits: 2`).
  The fail picture shows the suppression system fired, so no lock may set `missArt`.
- **The hub quotes no sets/combinations figure** any more, by Jon's decision — do not put one back.

**Open, in order of urgency:** pe-shed-rebellion's variant-0 collision (needs its own contract);
IT Vengeance and Car Trap still withdrawn; three small Kiln follow-ups that are Jon's call, not defects
(teacher page never names Mr Mudge; it does not say that a group hitting only named misconceptions skips
some wrong-entry lines; the fail and win pictures have straps that read as fingers at thumbnail size).
`docs/todo.md` is the running list.

The Level 3 SOW mapping contract (`docs/next-contract-level3-sow-mapping.md`) was **done on 18/09**;
its report is `docs/level3-sow-mapping.md`.

**`games/` changes since 17/09:** `linear-equation-solver` added (94th game, 141 questions), and the
four games above repaired. `the-truth-will-set-you-free` still draws a random 10 from 32.

**The portal has a "New & updated" filter**, a teal toggle after Core Maths, driven entirely by
dated metadata on the cards — **not** a hand-maintained list any more (that was tried twice, 26
Aug and 27 Sep, and drifted both ways each time: `factor-theorem` kept a **New** ribbon for
~6 months with nothing to expire it, and a git-log audit on 27 Sep badged 28 games by treating bug
fixes as updates). Rebuilt 27 Sep 2026 at the mechanism layer instead:

- **NEW** = a genuinely new game, first added to the portal in the window. **UPDATED** = the
  question bank grew, or a level/tier was added. **Neither is earned by a bug fix, rendering fix,
  distractor/key correction, UI change (help screens, self-paced advance, session-length buttons)
  or reskin, on their own** — evidence has to be an actual before/after count (bank size or level
  count), not a commit message's own framing.
- Each qualifying card carries `data-badge="new"` or `data-badge="updated"` plus
  `data-badge-date="YYYY-MM-DD"` (the day the qualifying work went live), on **every** occurrence
  of that game's card — a game can repeat across several level-filtered sections, and the
  attribute has to be on all of them for the toggle to work regardless of which section is
  showing. There is no hand-placed ribbon in the HTML any more.
- One function, `applyBadges()` (top of the portal's `<script>`, run once via `applyBadges();`
  right before the first `filter('all')` — i.e. before `applyFilters()` ever runs), computes
  whether each badge is still live: `BADGE_DAYS = 56` (half a term) since `data-badge-date`. If
  live, it sets `card.dataset.fresh = '1'` (the flag `applyFilters()` already reads — that
  function itself was never touched) and renders the `.fresh-badge` / `.fresh-badge.updated`
  ribbon on that game's *first* card only. If nothing is live, it also hides `#freshBtn` entirely,
  so the toggle can never be clicked into an empty result — there is never a state where "New &
  updated" is selectable and shows nothing.
- "Today" is read through a single function, `mfgToday()`, purely so a test can temporarily
  replace its body to simulate a later date without touching the badge data — never committed.
- When a game next qualifies, add or refresh `data-badge`/`data-badge-date` on every occurrence of
  its card; nothing else to update, no list to keep in sync, nothing to remember to remove later.
- 27 Sep 2026 audit result under this rule: only two games had real evidence in the whole
  2 Aug–27 Sep window — `linear-equation-solver` (**New**, 2026-09-18, the 94th game, bank
  48→141 same day) and `quadratic-factoriser` (**Updated**, 2026-09-27, its three-phase rebuild,
  1 level→3). Every other game touched in that window — including the six previously badged
  **Updated** and `factor-theorem`'s stale **New** — turned out to be a bug/rendering/UI fix on
  the actual count, verified file-by-file rather than trusted from commit messages, and lost its
  ribbon.
- **When the single metadata source (`games.json`) is built, `data-badge`/`data-badge-date` move
  there** — this is still per-card HTML attributes only because that source doesn't exist yet.
- Separate from all of the above: the **"New for 2026/27"** section (the front-page band naming
  `core-maths-paper1/2a/2b/2c`, `boolean-blitz`, `higher-power`, `prisoners-dilemma`,
  `seven-bridges`, `given-that`, `screening-room`) has its own permanent, undated `.fresh-badge`
  ribbon that is **not** wired to `data-fresh`, the toggle, or `BADGE_DAYS` at all — it never
  expires and was untouched by this rebuild. Its membership is Jon's call, tracked separately.

**`/escape-rooms/` is LIVE and promoted, and as of 2026-09-08 it ships ROOM BY ROOM.** Eight
rooms are live — `hamster-heist`, `pe-shed-rebellion`, `prom-budget`, `canteen-hack`
(2026-09-12), `heatwave-mutiny` (2026-09-13), `rugby-mud` (2026-09-15) and the two new ones,
`comic-caper` and `kiln-disaster` (both 2026-09-17) — in the sitemap, on the hub, and in the **front page
feature band** above "New for 2026/27". The other two (`it-vengeance`, `car-trap`) are
built but **withdrawn behind `noindex` holding pages at their own URLs** until each one's voice rewrite is
done; nothing was deleted and no indexed path 404s. **The teacher pages keep `noindex` deliberately**
— they hold every answer, and a student who can Google them has no room left to solve.

**Releasing a room is part of finishing it**: its real `index.html` and `teacher.html`, its card on
the hub *and* the front-page band, its `<url>` in `sitemap.xml`, the room counts (grep the current count word — `eight` as of 2026-09-17; the front page has it twice in one repeated meta string). The hub quotes no
sets/combinations figure any more (Jon, 17/09), so there is nothing to recompute. See §5c of the voice-rewrite doc.

The band uses `esc-` classes, **not `.game-card`**, on purpose: `applyFilters()` counts and filters
every `.game-card` on the page, so reusing that class would have made the portal claim 101 games and
let a topic filter hide the rooms. As built, the count still reads 93 and the band is always
visible.

**Open decision, still Jon's:** the "New for 2026/27" portal section holds **18 cards (6 Updated,
12 New)**, which is a lot of page-top before KS3 starts. It shipped un-trimmed deliberately. The
6 Updated have real work behind them; the 12 New arrived Mar–Apr 2026 and are only "new since you
last looked" — that is the tail to cut. Deleting a card block is all it takes; those cards are
copies and the originals live in the level sections. The new filter is the lighter-weight answer to
the same problem and may make trimming the section easier to argue for.

## Escape Rooms — active project

Started 2026-08-26. Narrative maths escape rooms, reference point **Unlock!**.
**Multiple short rooms per level**, each **under 15 minutes** — designed to end a lesson, not fill
one.

> ### ⚠ The live work is the voice rewrite — start at `docs/escape-room-voice-rewrite.md`
>
> A teacher found `/escape-rooms/` on 2026-09-08 and said through the feedback form that the prose
> is visibly AI-written and the rooms are unusable in class. **They were right**, and the diagnosis
> is precise: the maths and the puzzles are sound, the prose has no author behind it. All eight
> rooms are being rewritten one at a time, each around a named antagonist drawn out of Jon in an
> interview rather than invented for him.
>
> **One room per session. Jon reviews before any file is touched.** The binding contract is
> `docs/escape-room-voice-contract.md`; the running state, per-room status and the gotchas are in
> `docs/escape-room-voice-rewrite.md`. **Six of eight are done** — `hamster-heist` (Mr Beaker,
> and still the reference implementation), The P.E. Store Rebellion (Lungey; fuller worked example in
> `docs/pe-store-rebellion-story.md`), The Prom Budget Embezzlement (Mr D Tension), The Canteen Menu
> Hack (Ms Cinnamon), The Heatwave Mutiny (Mr Robin Banks, energy contractor; full record in
> `docs/heatwave-mutiny-sanity-check.md`) and The Rugby Mud Bath (Mr Mower). A new room, The Comic Caper
> (Ms Fromage), is live too.
>
> **Neither of the two remaining rooms can be opened cold.** IT Vengeance and Car Trap each
> have a new scene image that does not match the room, so each needs a premise/image conversation with
> Jon **before** its session (§7 of the working doc) — and **Car Trap has lost its antagonist**,
> because the headteacher now speaks in `prom-budget` and a character speaks in only one room.
>
> **Heatwave added a step that worked:** before any file was touched, the full breakdown went to a
> second Claude for a sanity check, and it moved the premise and cut a failure mode. **Jon cannot run
> `serve-stubbed.py` himself** — start it in the background and open the room in his Chrome.
>
> Three things that will bite, all written up in that file: **`teacher.html` maps clues to locks by
> `room.js` object `id`** — change an object's visible text freely, never its id; **every PNG
> downloaded from Gemini since September 2026 carries a watermark**, removed by
> `scripts/strip-gen-watermark.py`, which must be run on every image before filing and **whose
> detector misses soft marks, so look at the corner yourself**; and **object and lock `name`/`where`
> go through `esc()`, so an HTML entity in one renders literally** — use real characters there.

Read in this order:

| Doc | What it is |
|---|---|
| `docs/escape-room-voice-rewrite.md` | **The live work.** Why the rewrite is happening, how a room gets done, per-room status, and the gotchas that have already cost time |
| `docs/escape-room-voice-contract.md` | The binding task contract for the rewrite |
| `escape-rooms/` | **The built rooms.** Read `assets/engine.js` and one `room.js` before changing anything |
| `docs/escape-rooms-concept.md` | The design position. §3 has the rule everything follows from; §9 records where it ended up |
| `docs/escape-puzzle-bank.md` | **Audited** lock bank, batches 1–6, plus how the variant libraries are held to the same rules |
| `docs/lock-bank-batch3.txt` to `-batch7.txt` | Repaired, room-grouped locks — 30 across ten rooms, all passing the checker. `check-escape-rooms.py` finds every `lock-bank-batch*.txt` by pattern, so a new batch needs no edit there |
| `docs/escape-rooms-scenarios.md` | The narratives these were built from. C–J built; A and B still need repairs. Its figures are only the first of several |
| `docs/escape-room-image-prompts.md` | The art record. **All eight live rooms are on the new three-picture model** (scene, fail, win, empty rooms, no lettering); the two withdrawn ones still carry their old six. Keeps the style line, the four rules, the alt text and what went wrong |
| `docs/gemini-lock-brief.md` | Paste-ready brief for generating more locks |
| `games/the-perfect-prank/` | The original prototype, unlisted. Built to the old 40-min spec, kept as the long-form example |

### Where this got to — 2026-09-17

**The rooms are being rewritten, one at a time, and the art is being redrawn with them.** See the
box above and `docs/escape-room-voice-rewrite.md`. **Six rooms of eight are finished and live, plus the new
Comic Caper; the other two are withdrawn** until their turn.

**A finished room is not a closed room.** `hamster-heist` was signed off, illustrated and pushed, and
then took **five more fixes plus a maths correction** in one sitting once Jon read it properly — §5d of
the voice-rewrite doc lists them. The maths one matters beyond this room: its bounds lock asked for the
**greatest** volume a rounded measurement could give, which is a supremum that is never attained
(exactly 9.5 rounds up to 10, so it could not have been recorded as 9). **Bounds locks ask for the
minimum** — now a standing rule in `docs/escape-puzzle-bank.md`. Fix maths through
`scripts/gen-escape-variants.py`, never by hand.

**`hamster-heist` is done.** Its premise was corrected as well as its prose — the first pass had
the students stealing an animal and fooling a technician with a toy, which made the heroes thieves
and hung the pressure on somebody who could not reach them during play. It is now a recovery: the
P.E. teacher confiscated Pythagoras at lunchtime and shut him in the old cage in the chemistry lab,
and the class have until the 3:30 bell to get him home. Mr Beaker sleeps through it in the store
room arguing the hull-first horizon proof with a colleague who retired in 1994. **Expect the
premise to move in every one of these sessions** — interviewing for voice is what exposes a premise
that does not hold up.

**The art model has changed to three pictures a room, not six:** scene, failure, victory. Jon has
redrawn all eight establishing shots by hand in a new style — visible ink linework, flat colour,
muted, and **empty of people and lettering**, which is where the old generation kept failing. The
instrument art is dropped; the engine draws the live control. **The failure picture stays** — it is
the time-out screen, and it also appears beside a misconception **only** on a lock with `missArt: true`
(today only `canteen-hack`). **`comic-caper` must never set `missArt`**: its failure picture shows the
cupboard already gone, which is only true at time-out.

**Nothing on the site carries a generator watermark**, but every PNG downloaded since the September
change does. `strip-gen-watermark.py` handles it and must be run on everything.

### How it got here — the art run, 2026-09-01

*Superseded by the September rewrite above, which redraws all of this. Kept because the prompt
lessons still hold.*

**The art is finished for rooms C to J.** All eight victory pictures were drawn and filed on
2026-09-01, so no room falls back to its establishing shot on a win any more. That fallback was the
bug Jon hit: you beat the P.E. room and got the picture of the shed in the rain, under prose about
a dodgeball arena that was now up indoors. The engine had always been right — it shows
`<room>-win.webp` only where `room.js` defines a `winAlt` — the pictures simply did not exist.

Each was filed at **1600x873 WebP q80** (the frame every other picture uses) with its `winAlt`
written at the same time, because the pairing is what switches the engine off the fallback and
`check-escape-rooms.py` enforces it. C and D were replaced the same day with better takes that put
both rooms in the same recognisable school hall.

**Two prose edits followed the pictures, not the other way round.** G's win line said the horse
"comes up to meet her at the top of her flight" and the vaulter came back male, so the pronoun now
follows the picture. C's says twenty-eight people and the picture has about twenty-four, which was
left alone.

**One known flaw, filed deliberately:** room I's victory queue is in polo shirts and shorts and
reads primary-age, where its failure picture puts the same queue in blazers and ties. No play shows
both endings, so it stands; the fix line is in the prompts doc if it is ever redone.

**Three prompt lessons, all now written into `docs/escape-room-image-prompts.md`:** repeat the
blank-labels rule inside the prompt (the four-checks list alone does not hold it); do not ask for a
state the generator cannot draw (folded wing mirrors — the replacement details gave a better picture
anyway); and attach the room's own scene, not just the style reference, wherever the victory shot
looks at the same place from the same angle.

### How it got here — 2026-08-26 to 08-31

**Eight rooms are built and playable at `/escape-rooms/`.** The engine exists, rooms C–J are on
it. It went live on 2026-09-01: indexable, in the sitemap, and led from the front page. Before
that it spent a week unlisted and `noindex` as a playtest build shared with colleagues.

**I and J went up on 2026-08-31 from six locks Jon wrote** (`lock-bank-batch5.txt`, 6 usable, 0
rejected): The Canteen Menu Hack (mean averages, simultaneous equations, fractions of an amount)
and The Headteacher's Car Trap (lower bounds, arc length, quadratics with a constraint). Both were
drawn the same day, so all eight rooms are illustrated. They were built and shared *before* their
art existed, which the engine now supports on purpose: a missing image falls back or takes its own
frame, and `check-escape-rooms.py` lists pending art rather than failing on it.

### State, at a glance — current

| | State |
|---|---|
| Engine | `escape-rooms/assets/` — `engine.js`, `engine.css`, `teacher.js`. Instruments, penalty clock, 3-step hints, save state, typed fallback on every instrument, Aa toggle |
| Rooms | Nine folders, each `index.html` (shell) + `room.js` (all the content) + `teacher.html`. **`teacher.html` maps clues to locks by `room.js` object `id`** — rewriting an object's visible text is safe, renaming its `id` silently breaks that page |
| Voice rewrite | **6 of 8 done and live**, plus the new `comic-caper`. IT Vengeance and Car Trap are withdrawn and need the §7 premise/image conversation first. `docs/escape-room-voice-rewrite.md` |
| Locks | 27 across nine rooms, all still agreeing with the audited bank — `scripts/check-escape-rooms.py` |
| Variants | **243 verified number sets**, 2–10 per lock, in `escape-rooms/variants.json` and injected into `room.js`. Generated by `scripts/gen-escape-variants.py` — never hand-edit a `variants:` block. **A lock never draws the set it gave last time**, and **the room is drawn jointly** so only VALID combinations are served (see "Cross-lock collisions") |
| Art | **The new model is three pictures a room** — scene, failure, victory — in Jon's redrawn hand-inked style, empty of people and lettering. Instrument art is dropped; the engine draws the live control. All eight live rooms have their three; `it-vengeance` and `car-trap` still carry the old six. Served straight from `docs/art/`, not copied; room pages reference `../../docs/art/`. A missing image falls back to the one named in `data-fallback`, or takes its frame with it — never a broken box. **Run `strip-gen-watermark.py` on every image before filing** |
| Wrong-entry | Rooms carry `wrongLines: [{head, body}, …]`, indexed by wrong-setting count, last one repeating. **Wired since 2026-09-08.** A misconception hit consumes an index without printing a line, by design |
| Rooms A and B | Still narratives only. Their locks were **rejected** in the batch-one audit and have never been repaired |

**How a room is put together.** `room.js` holds one `window.ROOM` object: the hook, the brief, the
stakes, eight searchable objects (usually six carrying a clue and two blank; `comic-caper` has four and
four; the checker requires at least two blanks), and three locks. Each lock names
its instrument (`dial`, `slider`, `keypad` or `pair`), the one misconception it is built around, a
three-step hint ladder and a one-line solve. `index.html` and `teacher.html` both read that same
file, so the answers on the teacher page cannot drift from the ones in the game.

**No number is written into the prose.** Every figure is a `{{key.token}}` filled at run time from
the lock's drawn variant, so the clue, the hints, the misconception response and the worked solution
all move together. To change the maths, edit `scripts/gen-escape-variants.py` and re-run it — it
rewrites `variants.json` and re-injects every `variants:` block. It only admits a set that has
exactly one settable answer on that instrument's own grid, a settable misconception that is not the
answer, an answer off the ends of the travel, and no clue number equal to the answer. **Variant 0 of
every lock is the audited bank lock and must stay that way**; `check-escape-rooms.py` enforces that,
that `room.js` has not drifted from `variants.json`, and that every token used resolves for every
variant.

**Cross-lock collisions — fixed 2026-09-17 (`0907f6e`).** Each lock's library is verified on its own, but
a room serves one variant per lock together, and independent draws collided (Jon saw ASSET No. 24 beside
DICTIONARIES: 24). `pickVariants()` in `engine.js` now draws the room as a whole. A draw is **VALID** when
(a) no clue figure appears in two locks' clues, (b) no answer appears in another lock's clues, (c) no
answer equals another lock's misconception, (d) no two locks share an answer. A clue figure is every
number the student reads in a clue — filled tokens *and* numerals typed into the clue string — and a clue
belongs to the lock whose tokens it uses. **(a) and (b) ignore figures of 2 or less; (c) and (d) apply at
every size.** Among VALID draws that repeat no lock's last set, one is chosen uniformly; if none exists the
no-repeat rule is relaxed for the fewest locks. `check-escape-rooms.py` applies the identical rules — **change
the two together**. **Games saved before `0907f6e` resume with their old draw**, collision and all; that
clears itself as they finish.

**The teacher page tracks the live draw.** The game mirrors its chosen variant indices into
`localStorage` under `mfg_escape_vars_<slug>`; the teacher page reads that and re-renders on the
`storage` event, so opening it in a second tab shows the numbers the class actually has, and
"play again" updates it.

**The two design rules are implemented, not just written down.** Clues are pooled and none of them
names its lock — deciding which note goes with which instrument is the first piece of thinking.
And entering a lock's named misconception gets a response that says what went wrong by name,
rather than a generic cross; in the room whose failure picture matches that specific mistake, the
picture appears with it.

**Next, in order:**

1. **Time a real room against a real class.** Every per-lock estimate is still the puzzle author's
   own. The only timing so far is Jon's solo run of `comic-caper` in 3:16 — the author, knowing the
   methods, so not a student baseline.
2. **Watch what the launch actually does.** GA4 has `page_view` on every room and teacher page, and
   the rooms fire the full game event set (`game_started`, `question_answered`, `hint_used`,
   `game_completed`, `game_abandoned`) exactly as the 96 games do, so completion rate, hints taken
   and wrong settings per lock are all queryable per room. Nothing has been indexed before, so the
   first Search Console impressions will take days to weeks — **request indexing for
   `/escape-rooms/` in Search Console** rather than waiting for a crawl. Holiday-quiet traffic is
   not evidence either way; the real read is late September.
3. **Rooms A and B, if they are wanted.** Everything else is drawn: fifty-three images across rooms
   C to J. The one thing to carry over is the style line — attaching `heatwave-mutiny-fail.webp` as
   a reference does **not** hold the rendering style. Room I's first three came back photoreal with
   it attached; with the style line in the prompt text and the photographic terms in the negative,
   every one of the ten that followed landed first time. Two more rules came out of the victory
   batch: **repeat the blank-labels rule inside the prompt** — the four-checks list alone does not
   hold it, and E came back with five invented plates on the gauge panel — and **do not ask for a
   state the generator cannot draw**; J's folded wing mirrors were unrenderable and unnecessary,
   and replacing them with things that do render (a bay visibly shorter than the car, tyre scuffs,
   a red light on the charger) gave a better picture than the original prompt would have.
4. **The maths pass A and B need first**: the laser mirror is incoherent as written and the lever
   has two answers. Neither is worth drawing until that is done.
5. **Watch the completion rate.** §8 of the concept doc sets the bar: the site's most-played games
   run at 8–9%. Rooms send the usual `game_started` / `game_completed` events, with wrongs and
   hints in the `detail` field.

**The four scripts, and when to run them:**

| Script | When |
|---|---|
| `scripts/gen-escape-variants.py` | Any change to a lock's maths. Rewrites `variants.json` and re-injects every `variants:` block in `room.js`. **The only way those blocks should ever change.** |
| `scripts/check-escape-rooms.py` | After any edit to `escape-rooms/`. Pins variant 0 to the bank, refuses drift from `variants.json`, fails on an unfillable `{{token}}`, and requires a `-win.webp` wherever `room.js` has a `winAlt`. **Reports every room's VALID draw count and fails any room under 20**; an invalid variant-0 draw is a warning only (withdrawn rooms only ever warn). Missing art is listed as pending and does **not** fail the run — a room may be built before it is drawn |
| `scripts/strip-gen-watermark.py` | **Every image, before filing.** Takes Gemini's four-pointed corner watermark off a PNG download and reframes to the house frame: `in.jpg docs/art/out.webp --frame 1600x873` (use `--frame` on every image — Gemini's aspect ratio varies). A no-op on a clean image, and it says so. Keys on the glyph's four-fold symmetry, not on brightness, so it does not flag scenery |
| `scripts/art-queue.py` | Regenerates the prompt file's status header from its own contents |
| `scripts/strip-dial-needle.py` | Takes a painted needle off a gauge, since instrument art must not contain the moving part. Only needed while instrument art exists — the new three-image model drops it |

**Four rules the art has to keep**, learned across 35 images and recorded in full in
`escape-room-image-prompts.md`:

- **Instrument art is the housing, never the moving part** — the bare track, the empty pivot boss.
  A painted needle at zero gives the student two needles the moment the live one moves. Name the
  moving part in the *negative* prompt or the model draws it anyway.
- **Nothing legible on a puzzle surface.** Clue text is HTML so the Aa toggle and screen readers
  can reach it. Sign-writing in a scene or failure is welcome — put what it says in the `alt`.
- **Count the controls against the lock's INSTRUMENT line.** A feeder came back with no slider at
  all; a keypad came back with four buttons when the code has four digits and needs ten.
- **Reroll compositions, inpaint words.** Flat lettering fixes in one pass, every time. Removing a
  *figure* failed five times out of five.

**The design rule:** the maths must be the *action*, not the toll gate. A door that pops a
question when you click it is a worksheet with a story stapled on. A dial you can only set
correctly by working out the bearing *is* the answer.

**The difficulty rule, learned the hard way:** difficulty comes from not knowing which clue
belongs to which lock, not from harder arithmetic. Jon solved the first prototype in six minutes
because every act announced what it wanted.

### Never build a lock without checking it

```
python scripts/check-lock-bank.py <bank file>
```

A lock with two answers is not a lock. Of the first twenty generated, three were unbuildable for
this reason. The checker catches multiple/zero solutions, VERIFY lines that merely restate their
own answer, and exact float equality. Locks answering a minimum or maximum use `VERIFY_MIN` /
`VERIFY_MAX`.

**A counting lock trips the tautology detector.** `n == len([...])` is flagged as a VERIFY that only
restates its answer, because the detector cannot tell a computed count from a typed number. Batch 6 writes
it as `len([...]) - n == 0`, which still fails when ANSWER is wrong (tested). Fixing the detector is
parked, not done.

**Prefer integer arithmetic in VERIFY.** `12*d == 8*(1200-d)`, not `d/8 == (1200-d)/12`. Binary
floats cannot hold a power of ten exactly, which is why `6e5 / 1.5e-4` is 4000000000.0000005.

**The checker cannot see the other way a lock breaks: an answer that is printed in its own clue.**
Batch 3 had two — a gauge whose answer was 30 psi with "30 m³" in the clue, and a Venn dial
answering 15 with "15 idle" in the clue. Both were sound maths and both opened to a guess. Read
every clue for its numbers before building it.

## Reference Files
- Full game roster (96 games, plus 1 withdrawn): see `.claude/rules/game-roster.md`
- Help/instructions audit: see `.claude/rules/help-audit.md`
- Timer policy (countdown/hidden/none): see `.claude/rules/timer-policy.md`
- Analytics events & dual logging: see `.claude/rules/analytics.md`
- Running to-do list: docs/todo.md

### Improvement ideas — two lists, deliberately separate
- `docs/idea-backlog-2026-08.md` — **Gemini's suggestions**, logged unagreed, each with a
  cross-ref against the roster and the Dashboard. Nothing in it is scheduled.
- `docs/jon-playtest-2026-08.md` — **Jon's own play-testing.** First-hand and much stronger
  evidence than the above. He samples games through the day; new findings go here, not in the
  Gemini file. Where they touch the same game, the entry says which supersedes which.

## Local render testing — ALWAYS use the stub server
```
python scripts/serve-stubbed.py        # http://127.0.0.1:8765/
```
Every page loads `schools/assets/analytics.js`, which posts to the live Apps Script endpoint and
into the production Events sheet. **Never open a real page against the live endpoint to check a
layout** — it writes junk rows into the data Jon makes decisions from (happened once, 2026-08-26).
The script swaps analytics.js for a no-op and leaves every other byte untouched. Node is not
installed on the Windows machine; Python is the way to serve this repo there.

Three things that cost time on 21/09, local or live:

- **Always cache-bust** — `?cb=<random>` on every page load and live fetch. Chrome will happily
  replay the previous build and hand you a clean pass that means nothing. It can fake a green as
  easily as a red, locally and on Pages.
- **The automation tab reports `document.hidden`**, so timers throttle to ~1.5/sec and any
  poll-based test driver stalls. To play a game end to end, capture the game's own `setTimeout`
  callbacks and drain them synchronously — every callback still runs, in order, without the waits.
  Test-only; never commit it.
- **`serve-stubbed.py` stubs `window.fetch` site-wide**, so an in-page `fetch` fails with
  `Error: stubbed`. Use `XMLHttpRequest` when a test needs to read a file.

## Does it actually run? — `scripts/check-site.py`

```
python scripts/check-site.py            # tiers 1 + 2, local stub server
python scripts/check-site.py --tier 2   # static scan only, no browser
python scripts/check-site.py --tier 3   # PLAY every game (opt-in, ~16 min)
python scripts/check-site.py --live     # tier 1 against maffsgames.co.uk
python scripts/check-site.py --only modular-battle
```
One-time setup: `pip install playwright && python -m playwright install chromium`.
**In a Claude Code cloud sandbox** the CDNs are unreachable and the installed Chromium is not the one pip's
Playwright expects, so tiers 1 and 3 fail there identically on `main`: follow `docs/sandbox-checks.md`.

`check-leaderboard-coverage.js` verifies that code **exists**. It cannot tell you whether that
code **runs** — `chart-interrogator` and `modular-battle` were dead for six months after the
2026-03-22 sweeps (`96381d74`, `76514c70`) and passed the coverage check every time. `check-site.py`
is the missing layer:

- **Tier 1** loads every game, room, teacher page and portal page in headless Chromium — bare and
  once per `?level=` the game declares in `.claude/rules/game-roster.md` (a roster label becomes a
  level key in `scripts/roster-levels.json`, the one table; an unlisted label is an error). FAIL on an uncaught
  exception, a `console.error`, a 404 on a local asset, or a main thread that stops answering
  (an infinite loop). External-CDN trouble is WARN, not FAIL. **Tier 1 also presses every level
  button** (30 Sep 2026): each game's every level control, in a fresh page, must reach
  `game_started` with no uncaught exception. Loading `?level=` URLs never presses a button, which is
  how `regression-rumble`'s Level 4 button sat dead: it set `l4`, a key its bank did not have.
  125 controls across 47 games; the method is commented in `check-site.py` at "Tier 1, level controls"
  (122 across 46 since `regression-rumble` was withdrawn).
- **Tier 1 loads every page the site serves** (2 Oct 2026, to-do §4 item 12), not only files named
  `index.html`. "Served" is GitHub Pages' Jekyll rule, encoded once in `jekyll_serves()`: there is no
  `.nojekyll`, so a file or folder whose name starts with `_`, `.`, `#` or `~` is not published, nor is
  anything in Jekyll's default exclude list; everything else is, `docs/` and `scripts/` included. So
  `games/sequence-solver/index-original.html` (a redirect stub) is loaded and
  `games/regression-rumble/_withdrawn.html` is not.
- **Tier 1 fails any page that scrolls sideways on a 320px phone** (2 Oct 2026, to-do §1.34). Every
  page is loaded again at 320×568, and every game is started through its first level control or Start
  button and measured again; `scrollWidth` 1px past the viewport is a FAIL naming the outermost
  elements past the edge. Measured with **Google's web fonts blocked**, so in the fallback font CI pins
  to DejaVu, the same every run (Jon's ruling: in Outfit 12 of the 44 overflows fit, and a gate must
  not depend on a third-party fetch; to-do §4 item 14 is self-hosting Outfit). No fixed pause: load
  event, KaTeX, `document.fonts.ready`, two animation frames. **Known overflows live in
  `scripts/checker-allowlist.json` under `tier1_phone_overflow`**, one entry per path and `at`
  (`load` or `start`) with its width and owning to-do item; CI fails on a new overflow and on a stale
  entry (one that now fits), so **the PR that fixes an overflow removes its entry**. Redirect stubs
  are not measured themselves; the check asserts each stub's target is. A game that starts at desktop
  size but not at 320×568 FAILs as "phone start unreachable". Four games start at neither by this
  method and are noted, not measured (`factor-theorem`, `six-sevens-bruv`, `trig-worms`,
  `test-the-claim`; reasons in the to-do's §1.34). Commented in `check-site.py` at "Tier 1, phone
  width".
- **Tier 2** scans every inline `<script>` and every `room.js` for the loop shape that froze
  modular-battle. Unlisted hits FAIL. Reviewed-safe loops live in `scripts/checker-allowlist.json`,
  keyed on **file + enclosing function name** (not line number), each with a written reason.
- **Tier 3 plays the games** — finds the options, clicks one, waits for the question to turn over,
  repeats. It is what tier 1 cannot be: modular-battle's freeze was on the *second* question, and a
  page load never gets there. Baseline 2026-09-23: **190 PASS, 0 FAIL, 6 WARN, 115 UNSUPPORTED**
  across 311 runs, 1544 questions played, ~16 min. Opt-in (`--tier 3`); `--tier all` is still 1+2.

**Three things about tier 3 that are load-bearing:**

- **UNSUPPORTED is not a failure, and the distinction is the whole point.** Tier 3 drives pick-one
  options and typed answers. A drag game, a canvas, a build-the-answer keypad or a second phase it
  cannot complete comes back UNSUPPORTED and never fails the run. The first draft called 118 of
  those FAIL — noise on that scale is how a checker gets ignored, and the one real failure inside it
  goes too. FAIL now means a crashed tab, a frozen main thread, a mid-play throw, or an option that
  cannot be clicked. The UNSUPPORTED list is the coverage ledger: record a game in
  `checker-allowlist.json` under `tier3_exceptions` **only once you have read it**, because what
  makes the ledger useful is that a game *newly* arriving on it is a change worth chasing.
- **Progress is read from the game, not the DOM.** 95 of 96 games fire `question_answered` with a
  `question_index` and 95 fire `game_completed`, so tier 3 hooks `window.mfg` through an accessor
  and counts events. Watching the options for a change instead is simply wrong for a binary game:
  `prime-or-composite` renders the same two buttons, PRIME and COMPOSITE, for every question it ever
  asks.
- **Options are found by behaviour, never by markup.** 27 games use `id="options"`, 8 use a class
  containing `option`, and **60 use neither**. Tier 3 takes every visible element carrying a click
  handler — as an `onclick` property (index-laws, suvat) or via `addEventListener` (angle-ace,
  matrix-crunch) — and groups by **parent alone**. Adding the class to that key splits
  prime-or-composite's `ans-prime`/`ans-composite` pair into two groups of one.

**Duplicate options are a WARN, deliberately.** A repeat in a pick-one group is a real defect —
Trig Worms shipped `-5.1` twice — but `expectation-station`'s stage 1 is a *tile bank* filling
several blanks, so `es_gcse_001`'s `['0.25','0.25','0.50','0.10']` is authored on purpose. Nothing
in the DOM tells the two apart, so the run reports it and a person judges.

**Timers are NOT throttled in headless Playwright.** `docs/game-integrity-2026-09-21.md` §5 says an
automation tab reports `document.hidden`, throttling timers to ~1.5/sec, and recommends draining
`setTimeout` callbacks by hand. That is true of the **Chrome-extension** tab and false here:
measured 2026-09-23, `document.hidden` is `false` and three chained 200ms timeouts finish in ~620ms.
Tier 3 waits on the game's real timers, so it sits through the delays a student sits through.

**When to run it:**

- **Before every commit touching `games/` or `escape-rooms/`.** No exceptions.
- **Any site-wide sweep runs it before committing** — a sweep is exactly what killed those two
  games, and the damage is invisible until someone opens the page.
- **Live verification uses `--live`, never a plain reload.** It cache-busts every page load.
  Chrome will happily replay the previous build and hand you a clean pass that means nothing.
- A **network guard is mandatory in every mode**, `--live` included: requests to the Apps Script
  endpoint, GA/gtag collect and Firebase are aborted over both HTTP and WebSocket, and the run
  fails if one completes. Checking a page must never write a row into the production Events
  sheet or a score into the live leaderboard.

`.github/workflows/check-site.yml` runs **tiers 1 and 2** on every push and PR. No secrets, free
runner. **Tier 3 is not in CI** — it takes ~16 minutes against ~85s for the other two, and it is new.
Putting it in CI is Jon's call once he has seen a few runs.

**Tier 3 is regression-proven, the same way tiers 1 and 2 were.** Restoring `1a407fe`'s
`while (choices.size < 4)` to modular-battle's `generateChoices` fails all three runs of
`--tier 3 --only modular-battle`; restoring the fixed version passes 24 questions. Note what that
proves and how: the loop does **not** hang politely enough for the watchdog — it allocates until
Chromium kills the tab, and Playwright reports "Target crashed". That is reported as *the page
crashed the browser tab*, not as a driver error, because blaming the checker for the one bug this
tier exists to find is how the tier stops being believed.

### Tier 4, layer A — bank extraction + lint (`scripts/extract-banks.py`, `scripts/check-banks.py`)

Tiers 1–3 prove a page runs and can be played. None of them inspects the *question
data* — matrix-crunch's duplicated determinant option, formula-unlocked's
`correct_override` collision, and normal-navigator's index patches all survived every
green checker run this repo has had, and were each found only by Jon playing the games.

Layer A closes that gap for **static data defects**: `extract-banks.py` reads every
game's question bank back from the live page under Playwright (post any runtime
patch), and `check-banks.py` lints it against eleven rules (B1–B11 — missing/duplicate
answers, duplicate questions, bank size, session-length overpromise, draft-prose
leaks, text that loses its spaces on render, duplicate object keys, hand-written index patches,
`correct_override` usage, options equal in value). **`data/check-ledger.json`** tracks every known violation
per game; CI (`.github/workflows/check-site.yml`) fails only on a violation not yet in
the ledger, or a ledger entry that no longer reproduces — a tracked, unfixed defect is
not a failure.

**B7, text that loses its spaces on render (rebuilt 2 Oct 2026, to-do §1.31).** Its KaTeX half used
to match two call shapes, `K(x.field)` and `katex.renderToString(x.field)`, and so never saw the 50
games that render through `rk`, `rkStr`, `tex`, `kx` and the rest (`docs/audit-katex-wrappers.md`).
Now, with no per-game list: **render sites are found by behaviour** (a function whose parameter, or
a local derived from it, reaches `katex.render`/`renderToString`/`MaffsText.html`, to a fixed point);
**what reaches each site is rebuilt per question** (locals, ternaries both ways, `||`, callbacks,
`shuffle`-like selectors), with **its guards evaluated per string**, so an option the game shows by
`textContent` is never counted; a game function on bank data is **computed in the page**, after
putting the page in the state that question sets where the function reads game state; and every
string is **rendered in the page through the site's own callee** (`extract-banks.py`), read as the
student sees it (`.katex-html`, a positive-width `.mspace` as a space). **The test**
(`bank_common.katex_lost_word_spaces`): a space the source has between two tokens is gone and one
of them is a word, 3+ letters or a 2-letter function word from a fixed list (`to of is as or an in
on at by if so no be do up it we he me my us am`), so maths products (`mg`, `bx`) never count and
units (`13 cm`) are out of scope. A site that cannot be rebuilt is listed by `--ci` as
`unresolved`, one fed only by a generator as `runtime-only` (log-laws Solve, free-daily-pizza,
graph-transformer, quadratic-factoriser; to-do §4 has the runtime-hook candidate), never a failure.
First run: 277 strings in 12 games, all of them in the audit's second count, 30 of 30 hand-read
hits genuine; the audit's other 246 strings were guarded (217), two-letter products (13) or other
(16). B7 alone has `RULE_MAX` 800. Fixtures: `check-banks.py --selftest`, and `--selftest-live`
renders them in a real page. Extraction takes about 40s longer for it.

**B11, options equal in value (2 Oct 2026, PR 51).** Two options that are different strings but
the same value (√50 beside 5√2) are invisible to B2 and to `MaffsOptions.build()`, which compare
strings. B11 parses every option with `bank_common.parse_value()`/`equal()` (SymPy; the one copy,
shared with `scripts/scan-value-equivalent-options.py`) and compares the distinct options within
each answer unit. An option it cannot read is never guessed at. A question whose ask names the form
("Write in standard form", "Simplify") is listed in `scripts/checker-allowlist.json` under
`b11_form_questions`, with a reason quoting the ask. **B11 findings are identified by content, not
position:** `bank_common.content_id()` is the SHA-1 of the whole question's canonical JSON, plus an
ordinal over exact copies, so inserting or reordering questions never turns a known pair into one
new + one stale entry. The whole question is hashed because a narrower hash (stem + ask + options)
gave one id to 74 groups of different questions in 21 games: simultaneous-solver's "Find x"
questions differ only in `sys`. The cost: editing any field of a question gives it a new id. `--ci` also fails in two cases beyond the
ledger diff: a bank the ledger knows as readable extracts as a generator (with the KaTeX CDN
unreachable, three games come back empty and every rule would pass them quietly), and a
`b11_form_questions` entry that matches nothing (the question changed; re-read it).

**Every finding is identified by content, not by bank index or line (to-do item 7, PR 52, 2 Oct
2026).** On 28 Sep the OpenDyslexic change moved `test-the-claim`'s known B8 entry from line 527 to
526, and CI failed on a defect it already tracked until the entry was moved by hand: a position-based
id turns any edit above a known defect into one new + one stale entry. B1, B2, B6, B7 and B10 now use
the question's `content_id()`. B3 is named after every copy in its group, sorted, so it survives
swaps too. B7's KaTeX and MaffsText halves, which carry no question, use the SHA-1 of the string plus
an ordinal. B8 uses the enclosing function (else top-level variable, else `(top level)`), the
duplicate keys and the SHA-1 of the object's text. B9 uses the target as written and the SHA-1 of
the right-hand side. B4, B5 and B11 are unchanged. The location goes in the detail and the line in
`line`. **Three things now change an id, all expected:** editing the content itself (a question's
fields, or a comment inside a B8 object), renaming a B8 object's enclosing function or variable, and
changing either syntax rewrite in `bank_common._shim_for_parser`, which B8 and B9 hash through and
which changes every B8/B9 id at once.

**`--write-ledger` merges; it never rebuilds (to-do §4 item 10, PR 53, 2 Oct 2026).** Only games this
run actually linted, or true generators the ledger already records as such, are replaced. Every other
game keeps its record byte for byte and is reported as carried, with its reason (withdrawn/off-roster,
not selected by `--only`, bank missing, bank not read) and entry count. So regression-rumble's three
B4 entries survive every write, and `--only=x --write-ledger` touches only `x`. **It refuses (exit 1,
nothing written)** when a bank the ledger knows as read (`generator: false`) came back missing or as a
generator, the KaTeX-CDN-unreachable case: a partial extraction is never the basis of a full ledger
write. A game new to the ledger that did not read is reported, not written; that includes a new
true generator, which has to be added deliberately.

Layer A is one of five designed layers, A–E; only A is built. **Full design, what each
layer catches, what none of them can (wording and pedagogy stay Jon's call), and the
proposed new-game gate: `docs/checker-tier4-design.md`.**

### No rejection sampling

**Build the candidate pool, dedupe on the same representation the answer check uses, shuffle,
slice.** Never draw at random and retry until the set happens to be big enough.

`while (choices.size < 4) { choices.add(randInt(0, mod - 1)) }` froze the tab on ~25% of
modular-battle's questions, because a modulus below 4 can never yield 4 distinct remainders.
Expectation Station had the same shape latent in its distractors. A loop that terminates only
when the dice cooperate is a hang waiting for the right question.

The test that separates a safe loop from a hanging one: **does a counter advance on every pass,
whatever the draw returns?** A Fisher-Yates shuffle reads `arr.length` and calls `Math.random`
just like the loop above, but its `i--` runs every time, so it is bounded. Rejection sampling
advances only when the draw happens to be new.

Constraints on distractors — sign, form, denominator — are **per-scenario properties, not global
rules**. Model them on the scenario that needs them rather than filtering a global pool until
what survives fits.

**Dedupe the distractors against each other, not just against the correct answer.** Trig Worms
filtered out candidates equal to the correct answer and nothing else, so when `asin` and `atan` of
the same near-zero ratio both returned -5.1 it shipped a question with **the same option twice**.
Where the candidate list can collide, top it up from a deterministic ladder (correct ±5, ±10, ±20,
clamped to the valid range) rather than redrawing. Finite list, no retry, always terminates.

### Assembling a question's options — `MaffsOptions.build()`

**Any new game assembles its options with `schools/assets/options.js`. Do not hand-roll it.**

```html
<script src="../../schools/assets/options.js"></script>
```
```js
const opts = MaffsOptions.build(q.correct, q.d);   // replaces shuffle([q.correct, ...q.d])
```

It guarantees the correct answer appears exactly once, that no two options share a key, and that
the order is shuffled by a bounded Fisher-Yates — never by retrying a draw. Options are compared on
`String(value)`, which is exactly what `dataset.val = v` stores and what the marking code compares
(canon §7.1). Deduping on any other representation would let through a pair the answer check cannot
tell apart, which is the whole failure being prevented.

**Why this exists rather than the rule above alone.** The Trig Worms lesson was written down as a
rule for authors and could not be applied platform-wide, because there was nowhere to apply it —
**32 games each hand-roll `shuffle([correct, ...d])` and not one checks for a collision.** Two more
shipped one, in shapes the Trig Worms rule does not describe:

- `matrix-crunch:171` **authored** it — `det([[6,2],[3,1]])` is 0 and `'0'` was listed in its own
  distractor array, so the question rendered **0, 0, 12, 6** with two buttons both marking correct.
- `formula-unlocked:295` **drifted** into it — a late `correct_override` was set to a string
  identical to the question's third distractor, so the override and that distractor became twins
  and the bank's real `correct` form never reached the screen at all.

**It cannot invent a replacement for what it drops.** A bank that authored a collision has one
fewer real option than its author intended, so those two questions now render **three** options,
honestly short — the same call modular-battle makes when a modulus of 2 has only 2 residues. It
warns to the console when it drops one (`console.warn`, never `console.error`, which would fail
tier 1). **Fixing the bank is still a teaching call**; this only guarantees the collision never
reaches a student.

**It cannot see two options that are equal in value.** To `String(value)`, √50 and 5√2 are different.
`coordinate-geometry-dash:233` shipped both, with only 5√2 marked right: a student who picked √50 was
marked wrong for a correct answer (fixed 28 Sep, to-do §1.24). A scan of every bank found the same
shape in 10 more games (`docs/scan-value-equivalent-options.md`). The guard belongs in the checker,
not here, because marking compares strings. Checker rule B11 (tier 4, layer A, 2 Oct 2026) now
fails CI on any new value-equal pair. **Never offer the answer in a second form unless the
question's ask names the form**; when it does, list the question in `checker-allowlist.json`'s
`b11_form_questions` with the ask quoted.

**Wired into `matrix-crunch`, `formula-unlocked` and `proof-builder` only.** The other ~28 games
hand-rolling this were deliberately left alone — that retrofit is a separate pass, and sweeps are
what killed `chart-interrogator` and `modular-battle` for six months.

### Check the generator's own range

Trig Worms picked its angle from `5*Math.floor(Math.random()*17)+15`, which is 15..**95**, with a
comment claiming it avoided 90. Neither 90 nor 95 can be the non-right angle of a right-angled
triangle; at 95 the adjacent goes negative and the game asked for a side of **-0.8**. It had been
doing that to 11.8% of questions, at every difficulty, since the game shipped.

**A comment saying a range is safe is not evidence that it is.** When a generator picks from a
range, enumerate the endpoints and ask what the game does at each one.

## Directory Structure
```
index.html                    # Main portal (all 96 live games)
op/index.html                 # OP for Secondary — Year 6 transition
leaderboards/index.html       # Leaderboard hub — rolling 7-day scores, all-time highs, your local history
about/index.html              # About page (bio, BMC) — canonical; schools/about/ is a redirect to it
feedback/index.html           # Feedback form (Formspree) — canonical; schools/feedback/ is a redirect to it
privacy/index.html            # Privacy policy — canonical; schools/privacy/ is a redirect to it
spec-map/index.html           # Specification mapping (AQA/Edexcel/BTEC/Core) — canonical; schools/spec-map/ is a redirect to it
schools/assets/               # Logo, favicon, OG image, analytics.js, firebase-leaderboard.js, score-history.js
games/                        # ALL 96 live games (single-file HTML each; regression-rumble is a holding page)
scripts/                      # Repo tooling (e.g. check-leaderboard-coverage.js, check-site.py)
```
Note: every `/schools/` page (`/schools/`, about, feedback, privacy, spec-map) is a redirect to its root canonical page. Link to the root path; `python scripts/check-canonical-links.py` fails on any link that resolves to a `/schools/` redirect.

## Tech Stack
- Single-file HTML games — no build step, no framework
- KaTeX via CDN for math rendering
- GitHub Pages hosting
- Firebase Realtime Database for leaderboard
- GA4 + Google Sheets dual analytics via `mfg()` wrapper

## Platform Principles
- Free forever — no subscription, no freemium, no ads
- No sign-up required — zero friction
- No personal data collected — cookieless analytics only
- Curriculum aligned — every game maps to AQA/Edexcel/BTEC spec
- Minimum 40-50 questions per game per tier

## Portal Features
- **Level filters:** All, KS3, GCSE, A-Level, Further, Level 4, Core Maths
- **Topic filters:** All, Number, Algebra, Geometry, Statistics, Applied
- **Search:** instant text filter
- **Banner badges:** clickable links to about/spec-map/privacy
- **Score ticker:** scrolling bar below header showing recent high scores from Firebase
- **Site footer:** one fixed 40px navy bar on every page except the escape rooms and the redirect stubs
  (each exemption, with its reason, in `scripts/check-footer.py`). Nine links: About ·
  Leaderboards · Spec Map · Parent guides · What's changed · Contact · Privacy · Feedback · ☕ Support
  MaffsGames. Its look lives only in `schools/assets/site-footer.css`; its markup lives only in
  `check-footer.py` (`CANONICAL`), written into every page by `scripts/apply-footer.py` (idempotent)
  and held there by `check-footer.py` in CI. **Never hand-copy it or its CSS into a page.** On a phone
  the links scroll sideways inside the bar, with a shading cue on the edge that has more. The bar stays
  exactly 40px, because every game's phone-fit fold subtracts it. Canon §7.5.2

## Level Colours
| Level | Colour | CSS Var |
|-------|--------|---------|
| Year 6 | Indigo | #6366f1 |
| KS3 | Green | #22c55e |
| GCSE | Blue | #3b82f6 |
| A-Level | Orange | #f97316 |
| Further | Purple | #8b5cf6 |
| Level 4 | Red | #ef4444 |
| Core Maths | Sky | #0ea5e9 |

## Theme
**Canon §7.5 is the rule; this is a pointer, not a copy.** One adult register for every game
(Jon's ruling, 2 Oct 2026): Outfit for text, JetBrains Mono for numbers, no emoji in the header,
age-neutral copy, each game its own `--accent`. The light or dark palette is derived from the
roster's Levels column (`palette()` in `scripts/check-theme.py`, the only copy of the rule), never
chosen per game. Tokens and fonts live only in `schools/assets/theme.css`; `check-theme.py` holds
every MIGRATED game to it in CI and reports the rest. Migration is per game, never by sweep (to-do
§3.12). The portal keeps its own look: Outfit, white surfaces, navy/teal. All games are single-file
HTML apart from the shared assets.

**The level colours above are portal chrome, not in-game chrome.** Each game picks its own accent;
none of the 20 senior games' accents tracks its level colour, and they are not meant to.

## Scaffolds fade, and never pre-announce the answer

Jon's rule, 22 Sep 2026. A visual aid earns its place by building the model, and then by getting
out of the way.

- **A scaffold is withdrawn once the student can work without it.** Modular Battle's dot grid now
  hides after 2 correct and returns after 2 wrong in a row. Showing it on every question turns
  "46 mod 7" into "count the red circles" — the student never divides. The picture teaches the
  model; **removing it is what embeds it.**
- **A visual aid must never give the answer away before the student has thought.** If it can only
  be made useful by pre-marking the answer, prefer showing it *after* they answer, as the reason.
- **If it cannot be drawn honestly, do not draw it.** Modular Battle scaled its dots to fit a
  40-dot cap, and scaling a count cannot preserve a remainder — it displayed 3 for an answer of 4.
  Draw it in full or omit it; never a lossy version of something that has to be exact.

## Advancing to the next question — canon §7.6
- **Correct answer:** keep whatever brisk delay the game already uses.
- **Wrong answer:** show a `Next →` control and wait for the student.
  `MaffsNext.wrong({mount, onAdvance})` from `schools/assets/next-control.js`. The 20s fallback is a
  safety net for a walked-away tab, never the mechanism.
  The control is disabled for a **3s floor** first (Jon, 29 Sep 2026), advances **once** however it is
  triggered, and `clear()` cancels its timers. A game that handles Enter itself routes it through the
  `advance()` that `wrong()` returns, never straight to its own next-question function (that skips the floor).
- **Any pause must have something on screen worth reading.** A pause with only "WRONG!" behind it is
  worse than no pause. Show the working, the step or the misconception *before* handing over.
- **The phone rule (canon §7.6.1, 30 Sep 2026):** on a narrow screen the reason and Next both sit
  above the fold. Hide controls that cannot be used during the feedback, collapse secondary panels,
  order fact → hint → picture → Next, and on a screen 600px tall or less move the picture (never the
  hint) below Next. Measure at 320×568, 375×667 and 390×844 over every question shape.
  `six-sevens-bruv` is the reference build.

Do not reintroduce a fixed wrong-answer timer, and do not hand-roll the control.

## Accessibility
- **Aa toggle** on every game — OpenDyslexic font, increased spacing
- State persists in localStorage (`mfg_accessible`)
- Colour feedback: tick/cross symbols alongside colour
- `prefers-reduced-motion` respected

## Tiered Question Banks
Games load level-keyed banks via URL param: `/games/{slug}/?level=level4`
```js
const QUESTIONS = { ks3: [...], gcse: [...], alevel: [...], further: [...], level4: [...], year6: [...] }
```

## Firebase Leaderboard (LIVE)
- A status that depends on other records is computed at display time, never stored — see `docs/canon.md` §9 "Architecture".
- Firebase Realtime Database (europe-west1, project `maffsgames-c1c9f`)
- Anonymous score submission — `MaffsLeaderboard.submitScore(slug, level, score, questionsAnswered)`
- 3-letter arcade initials (profanity filter, ~50 blocked combos, localStorage persistence)
- High score detection: gold trophy (all-time), blue star (weekly best)
- All-time best shown as target on each ticker entry
- `recent_scores` feed powers the portal ticker (reads the latest 20). The client no longer prunes it: the database rules in `firebase/database.rules.json` (source of truth, create-only; emulator tests in `firebase/rules.test.mjs`) refuse every delete and overwrite; **deployed and verified live 30 Sep 2026**, so a score can now only be deleted in the Firebase console. Deploy, verify, roll back and the manual prune: `docs/firebase-rules-deploy.md`
- **Eligibility is completion, not a question count** (23 Sep 2026). A run that reaches the game's own end ranks; `submitScore()` must only ever be called there. Every unsubmitted score is logged with its reason. The old 10-question gate silently kept 13 games (Prime Sprint, Estimation Golf, Equatle, Gantt, Chart Interrogator …) off the leaderboards since launch
- Wired into 94 of the 96 live games (`constructions-lab`, `given-that` excluded — non-scored; `regression-rumble` withdrawn 30 Sep 2026, declared `WITHDRAWN` in the coverage check, its boards kept); recounted from the repo 29 Sep 2026, plus `six-sevens-bruv` and `free-daily-pizza` on 30 Sep. Four of the 94 carry a call-site gate declared in `HELD`: `estimation-golf`, `equatle` and `distinctly-average` submit nothing today, `log-laws` submits its Laws drill only — so 90 submit unconditionally. `six-sevens-bruv` submits its 20- and 40-question sessions to levels `q20`/`q40` and its clear-the-grid sessions to no board. `free-daily-pizza` submits mixed-stage practice to `practice-q20`/`practice-q40` (single-stage practice ranks nowhere: history only, under `stage-s1-q20` etc.) and each UK day's pizza to `daily-YYYY-MM-DD`, a pattern declared off the hub in the coverage check's `OFF_HUB_LEVEL_PATTERNS`. Coverage enforced by `scripts/check-leaderboard-coverage.js`, which since 30 Sep 2026 also fails if a submitting game is missing from the hub registry (`leaderboards/index.html` `GAMES`) or listed with levels other than the ones it submits under (canon §9)
- Device-local score history alongside it: `schools/assets/score-history.js` (`MaffsScoreHistory`) — last 10 runs per game+level, `localStorage` only, no server call
- Public hub page: `/leaderboards/index.html` — rolling 7-day top scores + all-time-high per game, plus a "Your Scores" device-local section. See `docs/canon.md` §9 for full detail
- Certificates planned for Phase 1b (still not built)
- **Lesson from the retrofit:** the July rollout shipped the feature to every game but left the
  old *"Global leaderboard coming soon"* copy in place — 78 games told students the leaderboard
  did not exist while submitting their scores to it. Fixed 2026-08-26. When rolling a feature out
  site-wide, grep for the placeholder copy it is meant to replace.

## OP for Secondary
Year 6 → Year 7 transition section at /op/. 15 games (9 new + 6 with Year 6 banks).
Indigo accent (#6366f1). Summer banner: 1 July – 31 August only.

## SEO
- Sitemap: 133 URLs (96 games + 8 escape rooms + 8 pages + 21 parent-guide URLs — the pages count includes the `/escape-rooms/` hub; the parent-guide count is 20 guides plus the `/parents/` hub)
- All pages have: title, meta description, canonical, OG tags, twitter:card
- JSON-LD: WebSite + Organization schema on portal
- OG image: `schools/assets/og-image.png` (1200x630)

## Specification Coverage
- **AQA Core Maths (§3.1–§3.13):** All covered. 144 exam-style MC questions.
- **GCSE (AQA/Edexcel):** Full coverage
- **A-Level (AQA):** Full coverage including Factor Theorem
- **Further Maths:** Eigenvectors trilogy, Complex Numbers, Matrices
- **BTEC Level 4:** All 4 Learning Outcomes

## Roadmap
- [x] ~~Circle Theorem Spotter — add diagrams~~ **Done 2026-08-26.** All 55 questions now carry a
      generated SVG figure and Q1-8 were rewritten from "name this theorem" into figure
      recognition. See `docs/jon-playtest-2026-08.md` §1
- [ ] **Circle Theorem Spotter Q48 needs new numbers** — the question has no solution as written
      and its marked answer encodes the very misconception the game corrects. Needs a teaching
      call, see `docs/jon-playtest-2026-08.md` §4
- [ ] Matrix Crunch question bank expansion (35+18 → 50+50)
- [ ] GA4 spec pass — visibilitychange, attempts, game_replayed/level_selected
- [ ] L4 content review for Equation Builder and Spot the Error
- [ ] Phase 1b: Certificates (percentile ranking + downloadable)
- [ ] Phase 2: Teacher Portal (paid school model)

## Branding Assets
```
schools/assets/m_plus_logo.svg    # Full logo
schools/assets/favicon.svg        # Icon mark
schools/assets/og-image.png       # 1200×630 social image
```

## Relationship to Other Projects
- **mathswins.co.uk** — sister site, academy/commercial. Zero crossover in branding.
- **QF Network** — the blockchain. MaffsGames is part of the QF ecosystem.


## Task Contract

**Whose brief is which.** `.claude/rules/project-claude.md` loads alongside this file at the start of
every session. It is written to Project Claude, the planning role in Claude chat, so its **Your Role**
section — plan and advise, do not build unless asked — describes Project Claude, not you. In a Claude
Code session you are **Code Claude**, the implementation row of its Division of Labour table, and the
contract below is how work reaches you. Its mission, audience, platform principles and design rules
bind you exactly as they bind Project Claude.

All tasks arriving from Jon (relayed from Claude chat) will be structured as follows.
Do not begin work unless all seven fields are present:

TASK: [one sentence description]
ROOT CAUSE: [what is actually wrong]
CLASS CHECK: [is this finding an instance of a bug class (tests below)? If yes, EXACT CHANGE addresses the architectural layer. If no, state why the bug is local]
EXACT CHANGE: [file, function, what changes to what]
DO NOT TOUCH: [explicit exclusions]
SUCCESS CONDITION: [how to know the task is complete]
STOP IF: [conditions that require you to halt and report back to Jon]

**CLASS CHECK is answered before EXACT CHANGE, because its answer decides what EXACT CHANGE is.** A
finding is an instance of a bug class when any of these hold: the same bug shape appears in two or more
components; the bug is in shared infrastructure called by multiple components; or the bug is the absence
of safety in a function called from multiple paths. If it is, the fix addresses the architectural layer,
not the call site — the defensive-patch shape, a flag in one caller working round a bug in shared code,
is always the wrong answer. If it is not, say why the bug is local and fix it locally.

### Behaviour rules

- Before touching any file, state your understanding of the ROOT CAUSE in one sentence.
- If you hit something unexpected, do not improvise. Invoke STOP IF and report back.
- Do not refactor, rename, reformat, or tidy anything outside EXACT CHANGE.
- One pass. If it isn't right, stop and report — do not attempt iterative self-correction.
- If a task arrives without this structure, ask Jon for the missing fields before proceeding.
