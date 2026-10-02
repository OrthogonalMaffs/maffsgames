# NEXT CONTRACT (held) — Optional scoring modes for the leaderboard system

**Status: NOT STARTED. Held at Jon's request, 22 Sep 2026.** Jon pasted this mid-session and asked
for it to be parked until there is time. Do not begin it without Jon saying so — there is other work
ahead of it (see `docs/todo.md`).

**Sequencing.** Jon's stated order on 22 Sep: (1) the SUVAT / Trig Worms / Modular Battle fix list,
(2) the next level of the checker (tiers 3–4), (3) "other things", of which this is one.

---

## TASK

Add optional scoring modes to the leaderboard system, and adopt them in `higher-power` as the proof
case.

## ROOT CAUSE

`leaderboards/{slug}_{level}` has no mode dimension. A game with two scoring modes writes both to one
key (`higher-power`: streak, higher-is-better, and Pairs, lower-is-better — canon §8.2b, currently
excluded from hub ranking). Jon's 2026-09-22 policy (Practice by default, Speed Run opt-in) makes
multi-mode scoring platform-wide.

## CLASS CHECK

Yes — shared infrastructure (`firebase-leaderboard.js`, `score-history.js`, the hub, the ticker) used
by 91 games. Fixed once at that layer; games opt in by passing a mode.

## EXACT CHANGE

1. **`firebase-leaderboard.js`**: `submitScore(slug, level, score, questionsAnswered, mode)` — `mode`
   optional. Absent → the existing key `leaderboards/{slug}_{level}`, unchanged (the "legacy mode").
   Present → `leaderboards/{slug}_{level}__{mode}`. Add `mode` to each `recent_scores` entry
   (absent = legacy).
2. **`score-history.js`**: include `mode` in the local key when present; legacy keys unchanged.
3. **Leaderboard hub registry**: per game, a list of modes, each with a label, its key suffix (none
   for legacy) and a sort order (`'desc' | 'asc'`). Where a game has more than one mode, the card
   gets a mode switcher next to the level switcher.
4. **Ticker**: show the mode label beside the game name when the mode isn't legacy.
5. **`higher-power`**: streak mode stays legacy; Pairs submits mode `'pairs'`, registered `'asc'`.
   Re-enable `higher-power` in hub ranking for new data. Its legacy key holds mixed historical data:
   rank it as streak only if Pairs entries are distinguishable in it; otherwise show the legacy
   history unranked with a note (report which).

## DO NOT TOUCH

Any game other than `higher-power`; existing leaderboard data (no deletion, no migration);
`MIN_QUESTIONS_FOR_LEADERBOARD`; certificate thresholds.

## SUCCESS CONDITION

Every existing `submitScore()` call produces byte-identical writes (proved by stubbing `db.ref`
in-page and asserting paths and payloads for a sample of games); a mode call writes to the
`__{mode}` key; the hub shows the mode switcher for `higher-power` and sorts Pairs ascending, using
injected fixture data (no live Firebase writes — the `check-site.py` guard stays on); the ticker
renders mode labels from fixture entries; `check-site.py` passes; 0 guard escapes; pushed;
`--live` PASS.

## STOP IF

- The RTDB security rules restrict key names or the `recent_scores` schema, so this needs a rules
  deploy (report — Jon's call).
- Any existing call's write would change.
- The hub's hardcoded registry can't carry modes without restructuring it.

---

## Notes for whoever picks this up

- Read `docs/canon.md` §8.2b for the `higher-power` exclusion this contract lifts.
- The `check-site.py` network guard aborts Firebase over HTTP **and** WebSocket. That guard must stay
  on for the whole of this work — the success condition is explicit that verification uses injected
  fixtures, never live writes. Checking a page must never write a score into the live leaderboard.
- "Byte-identical writes for existing calls" is the load-bearing requirement: 91 games call
  `submitScore()` and none of them will be touched, so the no-mode path has to be provably unchanged
  rather than just look unchanged.

---

## Added scope — leaderboard wording not backed by the shared system (found 26 Sep 2026)

Found while verifying the `estimation-golf` / `equatle` holds before deploying them. **Neither
item below is a defect in what this contract will change, and neither blocked that deploy** —
Jon ruled on 26 Sep that they are pre-existing and unchanged by it. They belong here because
they are the same subject, and because the holds make the wording read differently than it did
before.

**1. `equatle` has a second leaderboard that this contract does not know about.**
`games/equatle/index.html:256`–`:873`. It is entirely device-local — `llb()` / `slb()` read and
write `localStorage` (`:556`–`:557`) and it never touches `MaffsLeaderboard` or Firebase. It is
also **correctly sorted for a lower-is-better game**: `(a,b) => a.g-b.g || a.t-b.t`, guesses
ascending. Nothing about it is broken.

What it does do is present itself to the student as a leaderboard:

| | |
|---|---|
| `:256` | a panel headed **"Daily Leaderboard"** |
| `:258` | a name prompt, `<input id="lbname" placeholder="Your name…">` |
| `:861` | a button reading **"Submit Score to Leaderboard"** |
| `:871` | a confirmation toast, **"Score submitted!"** |
| `:873` | the button then reads **"Submitted ✓"** |

None of it is behind `LEADERBOARD_MODE_READY`; only the Firebase call at `:668` is. So a student
finishing equatle today types a name, presses "Submit Score to Leaderboard" and is told "Score
submitted!" — for a `localStorage` write, while the game is held off the real boards.

**2. `estimation-golf:589` shows a "🏆 Global leaderboard" link inside its end-of-round summary
card** — at the exact moment a round has *not* reached the global leaderboard. Ungated. The
footer link on both games is site chrome and is not part of this.

**Scope item for this contract.** Before deciding either case, **scan all 94 roster games for
hand-rolled local leaderboards, name or initials prompts, and any "submitted" / "leaderboard"
wording that is not backed by `MaffsLeaderboard` or `MaffsScoreHistory`, and list what is
found.** Two games surfaced from looking at two games, so the real number is unknown and a list
is worth more than a fix. Grep is a starting point, not the answer — equatle's board uses none
of the shared names.

**How each one is then resolved — relabel, gate behind the mode flag, or migrate onto
`MaffsScoreHistory` — is Jon's call when this contract is scoped.** Do not pre-empt it, and do
not edit a game on the strength of this section alone.
