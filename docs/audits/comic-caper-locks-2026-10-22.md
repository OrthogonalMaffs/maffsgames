# Comic Caper: does every lock open on the answer worked from its clues? (22 Oct 2026)

Report only (contract COMIC-CAPER-LOCKS, cloud lane). Nothing in the room, the engine, variants or any check was changed.

## Result

**Every lock opens on the answer worked from its on-screen clues, for every set in its library, by every input
route, at desktop and phone sizes.** No set's clue disagrees with its checked answer. The live 0/31 is not a
clue/answer mismatch in the page as it stands on main (`e6606a0`, which GitHub Pages serves).

## Why look

Jon's daily report, 22 Oct (last 7 days): `escape-comic-caper` 31 lock attempts, 0 correct (lock 1 0/14, lock 3
0/15). Every other room logs some correct answers.

## Method

- The page was served by `scripts/serve-stubbed.py` (analytics stubbed; nothing reached the live sheet), in
  Chromium (Playwright 1.56.0). `mfg` was wrapped only to record what fired. "Opened" was read from the page
  (the lock button's open state and its "Open." panel), never from the wrapped `mfg`.
- **Clues were read from the rendered notebook** (`innerText`, after searching all eight objects), never from
  room.js or `answerOf`. Each answer was computed independently in Python: the number of divisors of the asset
  number (lock 1), the number of primes from 1 to the last volume (lock 2), `gcd` of the two book counts (lock 3).
- **Input routes:** the typed fallback box; the range slider by keyboard (Home, then ArrowRight to the value);
  the dial needle by pointer (locks 1 and 2). Each value was read back from the readout before Set.
- **A control on every lock:** answer + 1 typed and set first. It never opened and always logged `correct: false`,
  so "opened" really tells a right answer from a wrong one.
- **Phase A, fresh starts (the real draw):** `Math.random` (called once, by the draw) was pinned to each of 400
  evenly spaced values with localStorage cleared. That found **184 distinct VALID draws**. All 184 were played to
  the end; every lock opened and every play reached the win screen. Every set of every lock appears in at least
  one draw (counts in the tables).
- **Phase B, each set forced:** each set of each lock was put into a saved state and loaded with Resume, then
  solved by each route, at 1280x900 and at 390x844 (mobile, touch): 118 entries.
- **Phase C, saved states from older pages:** below.

## Results by lock and set

### Lock 1, dial on the hinge side (factor count)

| Set | Clue as rendered | Worked | Answer | Desktop: typed / slider / dial | Phone: typed / slider / dial | Fresh draws: opened / played |
|---|---|---|---|---|---|---|
| 1 | ASSET No. 24 | number of factors of 24 | 8 | opened / opened / opened | opened / opened / opened* | 44 / 44 |
| 2 | ASSET No. 72 | number of factors of 72 | 12 | opened / opened / opened | opened / opened / opened* | 39 / 39 |
| 3 | ASSET No. 76 | number of factors of 76 | 6 | opened / opened / opened | opened / opened / opened* | 62 / 62 |
| 4 | ASSET No. 80 | number of factors of 80 | 10 | opened / opened / opened | opened / opened / opened* | 39 / 39 |

### Lock 2, dial on the lock plate (primes)

| Set | Clue as rendered | Worked | Answer | Desktop: typed / slider / dial | Phone: typed / slider / dial | Fresh draws: opened / played |
|---|---|---|---|---|---|---|
| 1 | VOLUMES 1–30 | primes from 1 to 30 | 10 | opened / opened / opened | opened / opened / opened | 12 / 12 |
| 2 | VOLUMES 1–55 | primes from 1 to 55 | 16 | opened / opened / opened | opened / opened / opened | 30 / 30 |
| 3 | VOLUMES 1–20 | primes from 1 to 20 | 8 | opened / opened / opened | opened / opened / opened | 10 / 10 |
| 4 | VOLUMES 1–50 | primes from 1 to 50 | 15 | opened / opened / opened | opened / opened / opened | 26 / 26 |
| 5 | VOLUMES 1–60 | primes from 1 to 60 | 17 | opened / opened / opened | opened / opened / opened | 32 / 32 |
| 6 | VOLUMES 1–35 | primes from 1 to 35 | 11 | opened / opened / opened | opened / opened / opened | 16 / 16 |
| 7 | VOLUMES 1–45 | primes from 1 to 45 | 14 | opened / opened / opened | opened / opened / opened | 20 / 20 |
| 8 | VOLUMES 1–25 | primes from 1 to 25 | 9 | opened / opened / opened | opened / opened / opened | 19 / 19 |
| 9 | VOLUMES 1–40 | primes from 1 to 40 | 12 | opened / opened / opened | opened / opened / opened | 19 / 19 |

### Lock 3, slider across the handle (HCF)

| Set | Clue as rendered | Worked | Answer | Desktop: typed / slider / dial | Phone: typed / slider / dial | Fresh draws: opened / played |
|---|---|---|---|---|---|---|
| 1 | GRAMMAR BOOKS: 18; DICTIONARIES: 45 | HCF(18, 45) | 9 | opened / opened / n/a | opened / opened / n/a | 20 / 20 |
| 2 | GRAMMAR BOOKS: 18; DICTIONARIES: 24 | HCF(18, 24) | 6 | opened / opened / n/a | opened / opened / n/a | 12 / 12 |
| 3 | GRAMMAR BOOKS: 20; DICTIONARIES: 50 | HCF(20, 50) | 10 | opened / opened / n/a | opened / opened / n/a | 10 / 10 |
| 4 | GRAMMAR BOOKS: 15; DICTIONARIES: 20 | HCF(15, 20) | 5 | opened / opened / n/a | opened / opened / n/a | 23 / 23 |
| 5 | GRAMMAR BOOKS: 22; DICTIONARIES: 33 | HCF(22, 33) | 11 | opened / opened / n/a | opened / opened / n/a | 24 / 24 |
| 6 | GRAMMAR BOOKS: 24; DICTIONARIES: 36 | HCF(24, 36) | 12 | opened / opened / n/a | opened / opened / n/a | 11 / 11 |
| 7 | GRAMMAR BOOKS: 14; DICTIONARIES: 35 | HCF(14, 35) | 7 | opened / opened / n/a | opened / opened / n/a | 22 / 22 |
| 8 | GRAMMAR BOOKS: 16; DICTIONARIES: 24 | HCF(16, 24) | 8 | opened / opened / n/a | opened / opened / n/a | 11 / 11 |
| 9 | GRAMMAR BOOKS: 28; DICTIONARIES: 42 | HCF(28, 42) | 14 | opened / opened / n/a | opened / opened / n/a | 25 / 25 |
| 10 | GRAMMAR BOOKS: 26; DICTIONARIES: 39 | HCF(26, 39) | 13 | opened / opened / n/a | opened / opened / n/a | 26 / 26 |

\* Lock 1's phone dial: the first Phase B run reported "not opened" for all four sets because the readout still
showed 0, so 0 was what was set. At 390x844 the dial's top edge is at y = 838 of an 844 px screen, and the driver
clicked off-screen. With the dial scrolled into view, a mouse click, a touch tap and a touch drag each set the
answer (8 for set 1), and the lock opened. Lock 2's dial gave the same result (10). The instrument works; the
driver's first click missed it.

## What fires (stubbed analytics)

Every correct setting fires one `question_answered` event: `{game_slug: 'escape-comic-caper', level: 'gcse',
correct: true, question_index: <1|2|3>, detail: <lock id>}`. Every wrong one fires the same with `correct: false`.
A full escape fires `game_completed`. Logging a correct answer works in this room exactly as in the others, by
the same code.

## Can a saved state from an older page show one set's clues and check another's answer?

**No.** On reading, the engine saves only each lock's set *index* (`st.vars`). The clue text (`fill()`) and the
checked answer (`answerOf()`) both go through the same `variantOf(l)` at the moment they are drawn or checked.
So whatever index a save holds, the clues on screen and the answer checked come from the same set. Tested:

| Saved state | Clues shown | Locks opened on the worked answers |
|---|---|---|
| No `vars` (pre-variant engine) | Set 1 of each (24; 1&ndash;30; 18, 45) | 3 of 3 |
| Indices past the end of each library (7, 15, 99) | Set 1 of each | 3 of 3 |
| Indices saved as strings ("3", "8", "9") | Sets 4, 9, 10 (80; 1&ndash;40; 26, 39) | 3 of 3 |
| Mid-game save, all four clue objects already searched | That save's sets (76; 1&ndash;60; 14, 35), shown at once on Resume | 3 of 3 |
| Two tabs: B starts while A plays on, A not refreshed | A's own sets | 3 of 3 |
| Two tabs: D starts, C refreshed and resumed | D's sets (C showed 76; 1&ndash;25; 28, 42 before the refresh) | 3 of 3 |

Two version facts: room.js's three libraries are unchanged since the repository began (2 Oct 2026; the only
later edits add `grade` and `credit`), and engine.js has had no change to `pickVariants`, `variantOf`,
`answerOf`, save/load or `SAVE_V` since then. History before 2 Oct is not in this repository.

**The one way the numbers can disagree is off the page.** In the last case, a group that copied C's figures to
paper, then refreshed after another tab on the same device had started a game, now faces D's numbers. The page
is consistent with itself; the paper is not. The teacher page has the same property: with no game running on
its own device it shows set 1 as an example and says so in its banner. A teacher reading answers from a
projected teacher page gives every group set 1's answers (8, 10, 9), which open only for a group that drew
those sets.

## Observations for Jon (not faults found by this contract; nothing changed)

1. **31 attempts means at least two plays.** A wrong setting costs 45 s of a 900 s clock, so one play holds at
   most 20 wrong settings.
2. **Lock 3's brief can be read two ways.** "Every bundle has the same number of grammar books and dictionaries"
   is meant as "every bundle is identical". It also reads as "each bundle holds as many grammar books as
   dictionaries", which no set satisfies with every book used. That reading leads nowhere, which is consistent
   with, but does not prove, lock 3's 0/15.
3. **The dial's marks are not its values.** The dial draws its ticks at 36 even positions round the full circle (engine.js `dialSVG`), but its values
   sweep 270&deg; (0 to 20 on lock 1, 0 to 30 on lock 2), so a tick does not mark a whole number. Lock 1's brief
   says "numbered all the way round"; the dial shows no numbers. The readout and the typed box are exact, so
   this does not stop a correct entry.
4. **On a phone the lock-1 instrument opens below the fold:** at 390x844 the dial starts at the screen's last
   6 px. A student must scroll to see it.
5. **Class question (the contract's CLASS CHECK):** CI's per-set check (`scripts/escape_set_checks.py`)
   recomputes each answer from the variant's data fields (`N`, `V`, `a`, `b`), not from the text a student
   sees. This report closes that gap for this room only: here the rendered text and the data agree for every
   set. Whether to add a rendered-text check across all rooms is for Jon; this contract makes no change.

## Not covered

Real devices and browsers other than Chromium (no iOS Safari); the live site itself (the same bytes were
served locally). A real touch drag is simulated through CDP touch events, not by a hand.

## Test scripts

Test-only, kept out of the repository: a Playwright driver for phases A-C and a phone-dial diagnostic, run
against `serve-stubbed.py`. Raw results: 184 fresh draws (Phase A), 118 forced entries (Phase B), 6 saved-state
cases (Phase C).
