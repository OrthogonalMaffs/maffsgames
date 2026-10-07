# Handover: cloud lane

The cloud lane's running handover (canon §7.8.2). Only cloud-lane sessions edit this file; the home lane's is
`docs/handover/home.md`. Newest first. Keep it current on the branch as you go (CLAUDE.md, checkpoint discipline).

**Cloud lane owns:** per-game fixes in games that are currently unlisted, one game per PR, each with its verifier,
closing its entries in its own `docs/audits/findings/<slug>.yml`. It never edits `schools/assets/`, the shared
modules in `scripts/`, the workflow, canon, the roster's listed section, `docs/todo.md` or
`docs/audits/REGISTER.md` (CI regenerates that on main). Relisting a fixed game is the home lane's docs PR.

**Standing rule (Jon, 7 Oct 2026):** after each game's PR merges and main's full run is green, start the
next game on the contract's list without asking. Stop only for a STOP IF or an empty list.

**Every PR:** `python scripts/check-changed.py` before the first push; merge only on a green Gate, and never while
main's last full run is red; watch main's run after merging.

## 2026-10-07 (cloud): game 10 Integration Duel (PR #107); #106 Differentiation Duel merged; NEXT = Curling Friction

- **Differentiation Duel (PR #106) merged** on a green Gate; main's full run after it green.
- **Integration Duel (PR #107):** `scripts/verify-integration-duel.py` (B4): antiderivatives checked by differentiating, c held as a symbol, ln x + c sampled where it is right. Missing + c named in feedback (Jon may rule it right). B11 (5) cleared. Open: t5-010 in part (class 4).
- **Like Terms Collector's verifier flaked once on #106** (group E; item 1 typed 8.9/6.5, `MARK()` null, empty feedback;
  it passed 5 of 5 locally and on the one re-run). Same item and shape as #88's first-run flake. Home lane: after
  `page.fill`, wait for the boxes to read the typed values and for the feedback panel's class before reading the mark.
- **#103 split content group B into B1-B4**; the cloud lane's verifiers go at the end of B4, where #103 put them.
  A branch prepared before a ledger change on main conflicts on `data/check-ledger.json`: take main's ledger and
  replace only that game's record (the scratch helper did this per commit).
- **Next:** Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 9 Differentiation Duel (PR #106); #105 Partial Fractions Duel merged; NEXT = Integration Duel

- **Partial Fractions Duel (PR #105) merged** on a green Gate; main's full run after it green.
- **Differentiation Duel (PR #106):** `scripts/verify-differentiation-duel.py` (B4): implicit items compared on the curve; explanations must state the answer. B11 (9, five of them added by #99) and B7 (1) ledger entries cleared; t5-013/014 filed and fixed. Open: t5-010, t5-011 (class 4).
- **Next:** Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 8 Partial Fractions Duel (PR #105); #104 Binomial Blaster merged; NEXT = Differentiation Duel

- **Binomial Blaster (PR #104) merged** on a green Gate; main's full run after it green.
- **Partial Fractions Duel (PR #105):** `scripts/verify-partial-fractions-duel.py` (B4): every Find solved from its stated form; valid equivalent forms removed. Open: t5-007 (class 1), t5-009 (class 4). New B3 ledger entry: the Find B / Find C pair for 1/(x(x+1)(x-1)) now share stem, options and key (needs a new item).
- **The tier 4 crash recorded under game 6 has a known cause (home lane: shared code).** `_SiteEval.regex()` in
  `bank_common.py` returns `(pattern, glob)`, and the `.test` branch of `_SiteEval.call()` calls `.search` on that
  tuple, so any `/re/.test(x)` the evaluator reaches raises. Taking the pattern from the tuple fixes it. Also: a
  guard written as a page helper (`isTeX(v)`) is never decided, so both branches count; until the evaluator can
  look inside, the cloud lane writes such guards as `includes()` at the call site.
- **Next:** Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 7 Binomial Blaster (PR #104); #102 Trig Identity Duel merged; NEXT = Partial Fractions Duel

- **Trig Identity Duel (PR #102) merged** on a green Gate; main's full run after it green.
- **Binomial Blaster (PR #104):** `scripts/verify-binomial-blaster.py` (B4): three-term estimates as the ask states, rounding-ambiguity check, MaffsOptions. Open: t5-017 (class 1), t5-018 (class 4), t5-022 in part (portal card: home lane). One B3 duplicate (needs a new item).
- **Next:** Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 6 Trig Identity Duel (PR #102); #101 Component Crusher merged; NEXT = Binomial Blaster

- **Component Crusher (PR #101) merged** on a green Gate; main's full run after it green.
- **Trig Identity Duel (PR #102):** `scripts/verify-trig-identity-duel.py` (B2): every option read into SymPy. Compound-angle keys, 85.9°, identical options fixed; t2-011 filed and fixed. Open: t2-007 (class 1), t2-010 (timer: Jon's decision). gcse[16] duplicates gcse[12] (B3; needs a new item).
- **For the home lane (shared code, not edited here):** `bank_common.py`'s render-site analysis crashes
  (`AttributeError: 'tuple' object has no attribute 'search'`, in `call`) on a regex literal's `.test()` in some
  positions: inside a template-literal expression (Component Crusher's first CI run) and `/[\\^_{}]/.test(...)`
  (Proof Builder, found locally). Extraction then fails and every ledger entry reads as stale. The cloud lane works
  round it in each game (a named function, or string methods); the parser fix is the home lane's.
- **Local tier 4 in the cloud sandbox works:** serve KaTeX from the npm tarball (route the jsdelivr KaTeX URLs to
  `package/dist`), run `extract-banks.py`, then `check-banks.py --ci`; about 95 s with 4 workers.
- **Next:** Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 5 Component Crusher (PR #101); #100 Expectation Station merged; NEXT = Trig Identity Duel

- **Expectation Station (PR #100) merged** on a green Gate; main's full run after it green.
- **Component Crusher (PR #101):** `scripts/verify-component-crusher.py` (B2): keys from what is shown, diagrams measured from the canvas, marking through MaffsAnswer. Level 4 data shown; prompts' maths in `\( \)` (31 B7 ledger entries cleared). Open: t4-005 (class 1), t4-011 (class 5), t4-014 in part (class 4).
- **Next:** Trig Identity Duel, Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 4 Expectation Station (PR #100); #98 Trig Worms merged; NEXT = Component Crusher

- **Trig Worms (PR #98) merged** on a green Gate; main's full run after it green.
- **Expectation Station (PR #100):** `scripts/verify-expectation-station.py` (B1): all 180 Stage 3 cards reviewed with checks from the distribution ("most" = more than half); Stage 1 marked exactly. t2-001..016 fixed, t2-018/019 filed and fixed; open: t2-017 (class 1).
- **Next:** Component Crusher, Trig Identity Duel, Binomial Blaster, Partial Fractions Duel, Differentiation Duel, Integration Duel, Curling Friction, Dimension Checker, Proof Builder (prepared on local worktrees /home/user/*-work, not pushed).

## 2026-10-07 (cloud): game 3 Trig Worms (PR #98); #97 Truth Buster merged; NEXT = Expectation Station

- **Truth Buster (PR #97) merged** on a green Gate; main's full run after it green.
- **Trig Worms (PR #98):** `scripts/verify-trig-worms.py` (group B2, ~20 s). The generator is rebuilt from a
  `POOL` of servable outcomes (1,204; no retry); every outcome is recomputed with mpmath from the values shown,
  at the stated precision ("to the nearest degree", "to 1 decimal place"); every distractor is a named error and
  the feedback names it; only the two given sides are labelled and the triangle is drawn at one scale.
  t1-001..t1-004 fixed; nothing left open.
- **Next:** Expectation Station, then component-crusher, trig-identity-duel, binomial-blaster,
  partial-fractions-duel, differentiation-duel, integration-duel, curling-friction, dimension-checker,
  proof-builder (all prepared on local worktrees /home/user/*-work, not pushed; their PR texts and register
  specs are in this session's scratchpad).

## 2026-10-07 (cloud): game 2 Truth Buster (PR #97); #96 Spot the Error merged; NEXT = Trig Worms

- **Spot the Error (PR #96) merged** on a green Gate; main's full run after it green.
- **Truth Buster (PR #97):** `scripts/verify-truth-buster.py` (group B1). Keys are reviewed judgements, with the
  words a statement must contain for its key to hold (`needs`, SR-18) and SymPy where a key can be computed;
  every reveal figure is in `FIGURES` (an unlisted `=`, `<`, `>` fails); dates and counts in `SOURCED`.
  t3-001..012 fixed. Open: t3-013 (class 1), t3-014 (class 5/4), t3-015 in part: the 21 Learn More video IDs
  (YouTube is refused from the cloud sandbox: check them from home) and Next below the fold (shorter reveal
  text, Project Claude, or a layout ruling).
- **Next:** Trig Worms, then expectation-station, component-crusher, trig-identity-duel, binomial-blaster,
  partial-fractions-duel, differentiation-duel, integration-duel, curling-friction, dimension-checker (all
  prepared on local worktrees /home/user/*-work, not pushed), then proof-builder (in progress). A lost container
  loses them: redo from the register.
- **Gotchas:** a PR that clears a fixed B7/B11 finding also clears its entry in `data/check-ledger.json` (dump
  with `indent=1, ensure_ascii=False, sort_keys=True`, as `check-banks.py` does), or CI fails it as stale. With a
  workflow edit, `check-changed.py` selects every check (about 45 minutes here): run it in the background with a
  long timeout, never the default 30 minutes (the Truth Buster run was cut off there).

## 2026-10-07 (cloud): unlisted-games contract, game 1 Spot the Error (PR #96); NEXT = Truth Buster

Jon's contract of 7 Oct (cloud lane): fix the unlisted games one per PR, each under a new verifier, in this order:
spot-the-error, truth-buster, trig-worms, expectation-station, component-crusher, trig-identity-duel,
binomial-blaster, partial-fractions-duel, differentiation-duel, integration-duel, curling-friction,
dimension-checker, proof-builder. Shared classes stay open: 1 (answer lock, F1), 4 (?level resolver, F2),
5 (bank size), B11 parser gaps (F0). Skipped until Project Claude supplies data: moments-master, force-resolver,
suvat, factor-theorem, eigenvector-engine, truth-will-set-you-free. Other owners: linear-equation-solver,
screening-room, glorious-gantt.

- **Spot the Error (PR #96):** `scripts/verify-spot-the-error.py` (group B2, ~9 s). All 19 register entries
  fixed (t1-001..014 plus the re-audit's t1-015..019); nothing left open. 16 items reworded (listed in the PR
  for Project Claude). Model: the key is the first step that departs from correct working; later steps carry it.
- **Prepared on local branches, not pushed** (worktrees under /home/user/*-work, gone with this container): the
  next games are rebuilt from their audit entries in the same order. If this container is lost, redo from the
  register; the PR descriptions list the content choices.
- **Gotchas:**
  - A reviewed verdict (a step judged an error, a statement judged true) reads no text, so each verifier that
    holds verdicts pins each item's content hash (`REVIEWED`, `--print-pins`): any edit fails until re-reviewed.
  - The self-tests count a plant as caught only by a check other than that pin.
  - Locally, the KaTeX CDN is refused: KaTeX games' verifiers take `--katex-dir` (the npm tarball's dist/).
    `check-changed.py` here always fails seven checks for environment reasons (PR #96 lists them).
  - `extract-banks.py` through the sandbox wrapper reports component-crusher's 34 B7 entries stale even on main:
    do not trust a local tier 4 run for B7; read CI's.
  - A shared TeX-to-SymPy reader would serve several of these verifiers (each carries its own small one, since
    the cloud lane does not add shared modules): a home-lane candidate.

## 2026-10-07: the lane starts (written by the home lane, which set up the lanes)

- No cloud session has run since the lanes were split. The last cloud work was 6 Oct 2026 (#85 audit tranches 1-2
  and two games unlisted; #86 Core Maths Paper 1), recorded in CLAUDE.md's history.
- The unlisted games and their open findings: `docs/audits/REGISTER.md` ("By game", Listed = unlisted) and the
  roster's Unlisted section. Each has its relist checklist in `docs/todo.md` §1.53-§1.75.
- **Next:** Jon's first cloud-lane contract names the game.
