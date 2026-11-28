# TODO-AUDIT: every item in docs/todo.md against main (28 Nov 2026)

Contract: `docs/handover/contracts/2026-11-28-todo-audit.md` (`docs/history/contracts/` once merged). Home lane, Claude Code. Checked on main abb9b605.

Each item has one verdict. DONE: on main, the whole item moved. PART DONE: the finished part moved where it could be cut word for word. DUPLICATE: the same owed work is in another item; moved. OWED: stays. STALE?: stays, listed for Jon below. "Bytes moved" also counts history clauses cut from items that stay. Everything moved is in `docs/history/todo-done.md` under "## Closed by TODO-AUDIT (28 Nov 2026)".

## Totals

`docs/todo.md`: 106,470 bytes before, 101,535 after (4,935 moved; TODO_LIMIT 107,520).

| Verdict | Items | Bytes moved |
|---|---|---|
| DONE | 5 | 3,283 |
| PART DONE | 4 | 302 |
| DUPLICATE | 2 | 439 |
| OWED | 213 | 911 |
| STALE? | 35 | 0 |
| **All** | **259** | **4,935** |

The bytes against OWED are history clauses (a past state, or where a row came from) cut from 10 rows that stay. Nothing was cut from a STALE? item.

## Every item

| Section | Item | Verdict | Evidence | Bytes moved |
|---|---|---|---|---|
| §1 | "Done rows moved word for word to docs/histor..." | DONE | An index of closed rows, not work (who moved what where): every heading it names is in `docs/history/todo-done.md` (`grep '^## '`), where the numbers resolve. | 1425 |
| §1 | 1.14 | OWED | `docs/test-the-claim-verification.md:172` still heads "For Jon's review"; no sign-off line in the file. |  |
| §1 | 1.26 | OWED | `games/regression-rumble/index.html` is still the holding page (:12); the game is in the roster's Withdrawn section. History clause moved: the three done games' verifiers each carry a ci header (`scripts/verify-normal-navigator.py`, `verify-core-maths-paper2a.py`, `verify-maths-court.py`). | 93 |
| §1 | 1.34 | OWED | `scripts/checker-allowlist.json` `tier1_phone_overflow` still holds spec-map (load, 540) and trig-wars (load and start, 711). |  |
| §1 | 1.36 | OWED | `scripts/check-banks.py` has no rule on money at 1 d.p. (its only money rule is the money-box one, :40-45). |  |
| §1 | 1.71 | OWED | Still unlisted on 28 Nov: no `glorious-gantt` in `index.html` or `sitemap.xml`; no `scripts/verify-glorious-gantt.py`; 13 findings open in `docs/audits/findings/glorious-gantt.yml`; roster Unlisted (`.claude/rules/game-roster.md:174`). The 8 Nov re-check sentence moved as a past state. | 322 |
| §1 | ANALYTICS-RETRY-RULE | OWED | `.claude/rules/analytics.md` has no retry or attempts rule (grep: none). |  |
| §1 | ANALYTICS-SILENT-QUESTIONS | OWED | No runtime audit in `docs/audits/`; `scripts/check-answer-logging.py` still reads calls only. |  |
| §1 | ANALYTICS-FIELDS | OWED | `.claude/rules/analytics.md:21` unchanged; no ruling recorded. |  |
| §1 | "regression-rumble never reports a wrong answ..." | OWED | The game is withdrawn and not rebuilt (1.26), so nothing has changed. |  |
| §2 | "The held contract docs/next-contract-leaderb..." | OWED | `docs/next-contract-leaderboard-modes.md` exists; not run. |  |
| §2 | "Sort direction per game/mode: higher-power..." | OWED | equatle and estimation-golf still gated (`LEADERBOARD_MODE_READY = false`, equatle:721, estimation-golf:957). Since written: `firebase-leaderboard.js` no longer has "HIGH SCORE" or `maxScore`, and carries a direction (#863), so the trophy fault may be gone; not shown. |  |
| §2 | "Scores that aren't scores:..." | OWED | Heading for the two lines below. |  |
| §2 | "trig-wars counts the opponent's hits, so a 0..." | OWED | `games/trig-wars/index.html:1016-1018` submits `_twHits[1]`; unchanged as far as read. |  |
| §2 | "chart-interrogator submits a constant 100 fo..." | STALE? | `games/chart-interrogator/index.html:1277` now computes `score=Math.max(1,Math.round(BASE*multiplier))`, so the score may no longer be a constant 100; the level key is still `l4` (:204). |  |
| §2 | "Local "leaderboard" wording not backed by th..." | OWED | Heading for the three lines below. |  |
| §2 | "equatle:256–:873 has an entirely device-loca..." | OWED | `games/equatle/index.html:915-925` still has "Submit Score to Leaderboard" and "Score submitted!". |  |
| §2 | "estimation-golf:589 shows a "🏆 Global leader..." | OWED | `games/estimation-golf/index.html:610` still shows the Global leaderboard link. |  |
| §2 | "Scan all 94 roster games for hand-rolled loc..." | OWED | No scan report in `docs/audits/`. |  |
| §2 | "like-terms-collector's banked runs (Stage..." | OWED | `games/like-terms-collector/index.html:618` still submits every run to `'year6'`. |  |
| §2 | "Housekeeping in the contract itself: remove..." | OWED | `MIN_QUESTIONS_FOR_LEADERBOARD` is still named in `docs/next-contract-leaderboard-modes.md`. |  |
| §2 | "Leave out: the roster-vs-code level mismatch..." | OWED | A scope note for the held contract, not work. |  |
| §2 | "Do not start without Jon's say-so — his stat..." | OWED | No say-so recorded. |  |
| §3 | 3.1 | OWED | None of the still-owed list is on main: no `data/spec-mapping.json`, no `docs/spec-mapping-review-2026-09.md`. `scripts/check-spec-mapping.py` exists but is the 3 Oct portal check (every live game is on the static spec map), not this row's. |  |
| §3 | 3.2 | OWED | `spec-map/index.html` is still static HTML (370 lines, no board selector). |  |
| §3 | 3.3 | OWED | Blocked on 3.1. |  |
| §3 | 3.5 | OWED | Rulings for games not built: no Don't Count the Zeroes or algebra-basics game in `games/`. |  |
| §3 | 3.8 | OWED | Follow-ups not shown done. History clause moved (the tidy was built 30 Sep). | 96 |
| §3 | 3.9 | OWED | `tier1_phone_overflow` still has 6 game entries tagged §3.9; `scripts/phone-fit-state.json` lists 31 games failing in normal mode. |  |
| §3 | 3.12 | OWED | `scripts/check-theme.py`: 85 games still NOT_YET. |  |
| §3 | 3.14 | OWED | No ruling recorded. |  |
| §3 | 3.15 | OWED | `levelLabel()` unchanged in `schools/assets/firebase-leaderboard.js:113`. |  |
| §3 | 3.16 | OWED | No ruling recorded. |  |
| §3 | 3.17 | OWED | `scripts/check-resit-page.py:67` still keeps prime-or-composite off the page. |  |
| §3 | 3.19 | OWED | `schools/assets/analytics.js:285` still counts with `sec.querySelectorAll('[data-mfg-item]')`. |  |
| §3 | 3.20 | STALE? | 117 game pages now load `site-nav.js`, which owns where a back link goes (canon §7.5.8, SITE-NAV, 21 Nov); 98 pages have `class="back-link"`, 16 `class="back"`. |  |
| §3 | 3.21 | PART DONE | 11 of the 22 listed games now load `schools/assets/keypad.js` (component-crusher, estimation-engine, graph-sketcher, growth-and-decay, just-pythag-it-bruv, log-laws, quadratic-factoriser, split-it, stat-attack, suvat, test-the-claim). Nothing moved: the list is a dated survey and cutting names would reword it. |  |
| §3 | SIX-PS-THREE-BANKS | OWED | No `venn-two-way`, `straight-line-graphs` or `constructions-loci` in `data/six-ps/authored.json` or the page. |  |
| §3 | SIX-PS-EXPAND-FACTORISE | OWED | No `expand-factorise` topic in `data/six-ps/`; no ruling recorded. |  |
| §3 | FOLD-COMPONENTS | STALE? | The four branches exist, each last committed 27 Oct 2026 (44a4ef8, 227c3d6, 4a526a6, ed00d80); main has had about 380 PRs since. |  |
| §3 | KEYPAD-FRACTION | OWED | `origin/claude/keypad-fraction` (fbf6c36, 27 Oct) is not merged; `games/y-so-steep/index.html:216` still has `FRACTIONS = false`. |  |
| §3 | COMIC-CAPER-PRIME-LOCK | OWED | `escape-rooms/comic-caper/room.js:140-165`: the lock still counts primes. |  |
| §3 | BETTER-VALUE-AA-SIDEWAYS | OWED | `scripts/phone-fit-state.json` sideways/aa still lists better-value. |  |
| §3 | HOW-MANY-PARTS-FRACTION | OWED | `scripts/fraction-input-warn.json` still lists how-many-parts. History clause moved (where the row came from). | 128 |
| §3 | CURLING-TEACH | STALE? | Held since 4 Nov; no contract or change since. |  |
| §3 | ABOUT-PAGE | STALE? | The row itself asks Jon to keep or drop a contract never sent (27 Oct); `about/index.html` is live. |  |
| §3 | LOOK-REFRESH-PALETTE | OWED | `check-theme.py` now has 85 NOT_YET (the row says 88); no triage recorded. |  |
| §3 | SPEC-MAP-SHORT-BANKS | OWED | No triage recorded. |  |
| §3 | PRIME-SPRINT-LOOK-REDS | STALE? | The reds were settled by #660; what is left is one Aa measurement the PR called "not a gate", and the row asks Jon to close it or contract it. |  |
| §3 | ESTIMATION-GOLF-ART | STALE? | Parked 3 Nov; `origin/art/estimation-golf` unchanged since 2 Nov (028cf683). |  |
| §3 | HIGHER-POWER-PHONE | STALE? | Parked 3 Nov, nothing since; the fault is still live (`scripts/phone-fit-state.json` known-failures: higher-power in normal and Aa). |  |
| §3 | SCREENING-ROOM-PANELS | STALE? | Parked 3 Nov; the row says no contract text exists in the repo. |  |
| §3 | ANSWER-CONTROL-TALL-INPUT | STALE? | Parked 3 Nov; since then ANSWER-BOX-TEXT (17 Nov) changed the answer boxes of 12 games (`scripts/check-answer-inputs.py`). |  |
| §3 | ICE-CREAM-LIST | OWED | Still in the roster's Unlisted section (`game-roster.md:164`). |  |
| §3 | ICE-CREAM-GCSE | OWED | No GCSE-only stages spec or build on main. |  |
| §3 | D-BY-DX | OWED | Unlisted (`game-roster.md:163`); Phase 2 has no spec. |  |
| §3 | PLOT-MIGRATE | OWED | Only `games/d-by-dx-why/` loads `plot.js`. |  |
| §3 | 3-GON-LINE-UP | OWED | Left as it is by contract: 3-GON-LINE-UP-BUILD is in flight (PR #943 open). |  |
| §3 | SEARCH-DEMAND | OWED | Added 28 Nov (#942); `index.html:3336` `#noResults` unchanged. |  |
| §3 | L3-FULL-RELEASE | OWED | Added 28 Nov (#942); waits for the gap games. |  |
| §3 | D-BY-DX-TYPED | OWED | No contract. |  |
| §3 | SUMS-IN-DISGUISE-LIST | OWED | Listed 24 Nov; Jon's LINES rewrite not recorded. |  |
| §3 | SOME-THINGIES-LIST | OWED | Listed 24 Nov; Jon's lines and the class teacher's answers not recorded. |  |
| §3 | BASE60-LIST | OWED | Jon's trims not recorded. History sentence moved (listed 26 Nov, #930). | 44 |
| §3 | BASE60-AA-FOLD | OWED | The known list is still in `scripts/verify-its-just-base-60-bruv.py:842`. |  |
| §3 | CLASS-PAGE-QR | OWED | `class/index.html` is live; no QR card. |  |
| §3 | COUNTING-PLAYERS-LIST | OWED | `core-maths/counting-players/` is not in `sitemap.xml`; second edition due after 30 Nov. |  |
| §3 | NUMBER-BONDS | OWED | No such game in `games/`; no spec. |  |
| §3 | BANK-LINT-GIVEN | OWED | `scripts/check-banks.py:379` `question_signature()` still reads prompt text plus answer. |  |
| §3 | SHAPE-SHIFTER-LISTING | OWED | No badge on the card (`index.html:1461`); the roster (:49) and `help-audit.md:45` still say four modes; `phone-fit-state.json` still lists shape-shifter. |  |
| §3 | TAKE-A-WALK-PHONE-LAYOUT | OWED | No design ruling recorded. |  |
| §3 | CGD-PHONE-LONG | OWED | `phone-fit-state.json` laptop still lists coordinate-geometry-dash; its prerequisite PHONE-FIT-ALL-ITEMS has no row (see "Found, not recorded"). |  |
| §3 | BOOLEAN-BLITZ-LENGTH | OWED | `games/boolean-blitz/index.html:783` still deals every question; no length choice. |  |
| §3 | CLAIM-WALKTHROUGH | OWED | No "Watch one first" in `games/test-the-claim/index.html`. |  |
| §3 | SCROLL-BOX-FOCUS | OWED | No `tabindex` on the `.tt-scroll` wrappers (`escape-rooms/assets/teacher.js:147, 168, 217`). |  |
| §3 | WHEN-WILL-I-USE-THIS | STALE? | The section is live: #883 (2710eedc, 22 Nov), #888, #891; `when-will-i-use-this/` and `data/uses.json`. The owner cell still says "pilot in build". |  |
| §3 | EVERYDAY-MAFFS | OWED | No scope from Jon; nothing built. |  |
| §3 | NNL-PHONE-NEXT | OWED | `phone-fit-state.json` aa still lists negative-number-line. |  |
| §3 | SIX-PS-SHORT-WRONG | OWED | `scripts/sweep-six-ps-wrong.py:28` `KNOWN_FAILURES` still holds the 14. |  |
| §3 | EXPECTATION-EXACT | OWED | `formatPNum` is still in `games/expectation-station/index.html` (5 matches). |  |
| §3 | KILN-FOLLOW-UPS | OWED | The name is still only in `escape-rooms/kiln-disaster/room.js:43`; no floor in `scripts/gen-escape-variants.py`. |  |
| §3 | MONEY-THOUSANDS | OWED | No ruling recorded. |  |
| §3 | GRAPH-SKETCHER-REDESIGN | OWED | Still unlisted (`game-roster.md:154`); no redesign spec. Its points (2) and (10) say the shared calculator has no x^y, e, sin or cos, but `schools/assets/calculator.js:38` has had them in scientific mode since SCI-CALC (ee64b6a5, 9 Oct): wording for Project Claude. |  |
| §3 | PACK-ART-EXTRAS | OWED | No new art recorded. |  |
| §3 | PI-FIGURE-BINDING | OWED | No π handling in `tools/pack-generator/build_pack.py` (grep: none). |  |
| §3 | PACKS-V2-UPLOAD | OWED | Jon's task on Tes; not recorded as done. |  |
| §3 | PACK-READOUT-VOICE | OWED | No list recorded. |  |
| §3 | ANSWER-AUDIT-RUN | OWED | No `docs/audits/answer-audit-*.md`. The row's credit expires 6 Dec 2026. |  |
| §3 | MODULAR-BATTLE-PRESS-ALL | OWED | `scripts/verify-modular-battle.py:184-188` unchanged. |  |
| §3 | IN-PLAY-EXIT-GAP | OWED | No prioritisation recorded; the audit file is unchanged. |  |
| §3 | PHONE-FIT-PAGE-COORDS | OWED | No shared helper in `scripts/bank_common.py`; 28 verifiers read innerHeight, 17 add scrollY. |  |
| §3 | WRONG-PAUSE-UNCHECKED | OWED | `scripts/check-answer-lock.py:1031` still lists the 6; `WRONG_PAUSE_KNOWN_FAIL` (:1047) is empty. History clause moved (52dle's removal). | 34 |
| §3 | CORE-PAPER-BANKS | OWED | Each paper is still 36 items (`data/check-ledger.json` B4). |  |
| §3 | CALC-CLEAR-ON-RIGHT | OWED | No `maffs:answered` in `schools/assets/`; no ruling recorded. |  |
| §3 | WRONG-PAUSE-REASONS | OWED | No queue recorded. |  |
| §3 | LARGE-SCREEN-LAYER | OWED | `scripts/check-large-screen.py:87` MIGRATED is the pilot only; canon has no large-screen section. |  |
| §3 | LARGE-SCREEN-ROLLOUT | OWED | Waits for the pilot's rulings. |  |
| §3 | LARGE-SCREEN-POINTER | OWED | No contract. |  |
| §3 | START-SIDEWAYS-GATE | OWED | `scripts/measure-phone-fit.py` has no start-screen sideways gate. |  |
| §3.9 order | "The rule for the order. First, the failing g..." | STALE? | The phone gate changed after this was written (canon 7.6.1, 26 Oct): `scripts/phone-fit-state.json` now lists each failing game and only shrinks. |  |
| §3.9 order | "Rulings on this list (Jon, 1 Oct 2026). (1)..." | PART DONE | (1) New Shapes' right-answer Next: `games/new-shapes/index.html` uses MaffsNext (batch 1, 1 Oct; record in todo-done under 3.9). (3) Wrong-answer timers: all nine games named now call `MaffsNext.wrong`, held by the pause check in `scripts/check-answer-lock.py:691` (#842, 8ab38d17; ci-shards "lock", self-test plants). | 277 |
| §3.9 order | "The order (batch 1, New Shapes, done 1 Oct 2..." | STALE? | Of the 56 games in batches 2-19, `phone-fit-state.json` lists 31 as failing in normal mode; the batches have not been followed since October. |  |
| §3.9 order | "Wherever a right answer waits, its Next has..." | OWED | A standing rule for each phone-fit fix; not shown enforced by a check. |  |
| §3.9 order | "Seen while reading, not part of this order:..." | DONE | All nine games call `MaffsNext.wrong` (e.g. `games/percentage-flip/index.html`, `games/suvat/index.html` 5 calls; complex-converter by #874, 842aa2e4), none is on an exempt or known-fail list, and the pause check holds it: `scripts/check-answer-lock.py:691` `wrong_pause` (#842, 8ab38d17; ci-shards "lock"; self-test plants). | 532 |
| §3.9 order | "Aa mode: one fix across three games (Jon, 1..." | STALE? | `phone-fit-state.json` aa known-failures lists none of six-sevens-bruv, free-daily-pizza or new-shapes; new-shapes is on sideways/aa at 320x568. The gate measures one seeded question each. |  |
| Game ideas | "Each idea is one line here and nowhere else..." | OWED | The section's rule, not work. |  |
| Game ideas | "It's Not a Diamond [PROPOSED]: shape vocabul..." | OWED | Not in `games/`. |  |
| Game ideas | "Small, or Far Away?: metric units, map scale..." | OWED | Not in `games/`. |  |
| Game ideas | "Letters? In Maffs? Y?!: algebra basics (A1.1..." | OWED | Not in `games/`. |  |
| Game ideas | "Bond. Number Bond. [PROPOSED]: number bonds..." | STALE? | Row NUMBER-BONDS (§3) asks for a number bonds to 10 and 20 fluency game "soon"; this idea is bonds to 10/100/1000 and decimals to 1. |  |
| Game ideas | "Maths Wizard [PROPOSED]: Jon's mental strate..." | OWED | Not in `games/`. |  |
| Game ideas | "Don't Count the Zeroes: standard form (STRET..." | OWED | Not in `games/`. |  |
| Game ideas | "Venn Diagrams AGAIN? (the next build after 3..." | OWED | Not in `games/`; next after 3-gon Line-up. |  |
| Game ideas | "Not in Pen: constructing charts (drag bars,..." | OWED | Not in `games/`. |  |
| Game ideas | "Use a Ruler, PLEASE [PROPOSED]: real-life gr..." | OWED | Not in `games/`. |  |
| Game ideas | "It's Not 50/50 [PROPOSED]: constructing Venn..." | OWED | Not in `games/`. |  |
| Game ideas | "Is That a Fake Bag?: asymptotes (Jon, 9 Nov..." | OWED | Not in `games/`. |  |
| Game ideas | "Plans and elevations [PROPOSED]: G13.2, a GA..." | OWED | Not in `games/`. |  |
| Game ideas | "Whack-a-mole [PROPOSED]: a fast-recall forma..." | OWED | Not in `games/`. |  |
| Game ideas | "8:53: grade 7–9 exam-prep game; deliberately..." | OWED | Not in `games/`; parked on purpose. |  |
| Game ideas | "Log Laws basic level: Log Laws is too hard f..." | OWED | `games/log-laws/` has had a Level 3 level since 13 Oct (a35cbd80), before this idea (10 Nov); no research recorded. |  |
| Game ideas | "IT Vengeance: rebuild (withdrawn, awaiting i..." | STALE? | Canon §11.1 (:2583): withdrawn, and its URL redirects to The Rightful King (live 10 Oct). |  |
| Game ideas | "Food Technology (bake-off) and Music (PA..." | OWED | No such rooms in `escape-rooms/`. |  |
| Game ideas | "Anime Society: Mrs Rogers's idea, credited...." | OWED | No such room. |  |
| Game ideas | "Environmental Club: Jon's; exponential growt..." | OWED | No such room. |  |
| Game ideas | "Pi Day: idea only...." | OWED | No such room. |  |
| Game ideas | "ESC-BAND-ROTATION (ESC-BAND-SLIM, 15 Nov 202..." | OWED | No research or contract recorded. |  |
| §4 | item 1 | OWED | `data/check-ledger.json`: every game's layer C is "none". |  |
| §4 | item 2 | DONE | All 11 games show the worked solution or misconception and then call `MaffsNext.wrong` (e.g. `games/angle-ace/index.html:824-827`, `games/characteristic-quest/index.html:157-159`; commits 0470870b, 0d665c31, 10e73ae6, 95f63221, 2427414d, 27d0a43d, 02b6cefa, ace43bd5). The floor exists platform-wide: `schools/assets/next-control.js:24` FLOOR_MS, 3 s. Enforced by the pause check, `scripts/check-answer-lock.py:691` (#842; ci-shards "lock"; self-test plants). | 939 |
| §4 | item 3 | OWED | The four class A games still load KaTeX and never call it. Counts are stale: scale-factor-scaling, estimation-engine and fraction-equivalence now render through KaTeX or MaffsText; not shown complete for any game. |  |
| §4 | item 4 | STALE? | Written 21 Sep. Since then the wrong-answer pause is checked on every game (`scripts/check-answer-lock.py`, #842) and all five games named have been reworked under MaffsLock and MaffsNext. |  |
| §4 | item 5 | STALE? | `tier3_exceptions` still has 7 entries, but tier 3 was re-surveyed and changed on 24 Nov (`docs/audits/tier3-coverage-2026-11.md`; TIER3-LOCK-FIX: 52 games now play fully). |  |
| §4 | item 9 | OWED | `PQ(s)` is still copied in component-crusher:568, factor-theorem:298 and test-the-claim:1257. |  |
| §4 | item 11 | OWED | `scripts/bank_common.py:377` `TEXT_KEYS` has no `post`; the B3 entries are unchanged. |  |
| §4 | item 12 | PART DONE | `scripts/check-site.py` loads every served page through `jekyll_serves()` (:1006) and has `--live` (:42, :3225); the DONE clause moved. The `--live` confirmation is not recorded. | 25 |
| §4 | item 13 | OWED | `scripts/check-banks.py` still lists runtime-only sites unchecked. |  |
| §4 | item 14 | STALE? | The gate now measures in Outfit from pinned fonts (`scripts/fonts/`, `scripts/check-site.py:1680`). The site still loads Outfit from Google (`index.html:19`). |  |
| §4 | item 15 | OWED | Not shown: tier 1's start driver (`check-site.py:1478`) was not traced for the four games. |  |
| §4 | item 17 | PART DONE | `scripts/check-escape-rooms.py` and `scripts/check-lock-bank.py` now carry ci-line headers and run in the Gate; `check-lock-uniqueness.py` and `check-feedback-options.py` have none, and `check-verifier-coverage.py:72-84` still polices only verify-/test-. Nothing moved: the two halves share sentences. |  |
| §4 | item 18 | STALE? | Windows-only local failures. The home lane works in WSL and neither lane runs check-changed before pushing (AGENTS.md:52, #787). Branch protection: the token cannot read it; 0 rulesets. |  |
| §4 | item 19 | STALE? | Seen once, on PR #36 (4 Oct). proportion-blaster's B4 passes in `data/check-ledger.json`; no recurrence recorded. |  |
| §4 | item 20 | OWED | Not shown: the stub server's default seed and a nightly random sweep were not found by grep. Part of the still-owed line has moved on: the driver now measures the wrong-answer screen (`scripts/measure-phone-fit.py:34`); later screens are still unmeasured. |  |
| §4 | item 21 | STALE? | The row says the warn list is empty and the move is insurance only; no decision from Jon recorded. |  |
| §4 | item 22 | OWED | `scripts/measure-phone-fit.py` has no `data-opt` handling; possibly-maybe is still unmeasurable in `phone-fit-state.json`. |  |
| §4 | item 23 | STALE? | Local failures in WSL; CI is the authority and local runs are optional (AGENTS.md:52). MONOTONIC-CLOCK fixed the shared assets' part. |  |
| §4 | item 24 | OWED | `games/distinctly-average/index.html:215` still sets Aa line-height 1.4. |  |
| §4 | item 25 | OWED | No such check. |  |
| §4 | item 26 | OWED | chart-interrogator still uses `l4` (:204). |  |
| §4 | item 27 | OWED | Not shown fixed; the row's own caveats stand. |  |
| §4 | item 28 | OWED | `scripts/merge-pr.py:308` still refuses with "start one by hand". |  |
| §4 | item 30 | OWED | No such failure mode in `tools/pack-generator/build_pack.py`. |  |
| §4 | item 31 | OWED | `python3 -W error` on `scripts/check-banks.py` still raises on `\(`. |  |
| §4 | item 32 | STALE? | Parked with the 27 Oct queue; Jon has since ruled on start screens in START-SIDEWAYS-GATE (ruling (b), 20 Nov). |  |
| §4 | item 33 | STALE? | Parked 3 Nov, nothing since; `/the-6-ps/` is not in `scripts/measure-phone-fit.py`. |  |
| §4 | item 34 | STALE? | Parked 3 Nov; the row says no contract text exists. |  |
| §4 | item 35 | STALE? | Parked 3 Nov; Jon's start-screen ruling of 20 Nov is row START-SIDEWAYS-GATE. |  |
| §4 | item 36 | OWED | `docs/apps-script-endpoint.js:15` still has the placeholder. |  |
| §4 | item 37 | OWED | `scripts/measure-phone-fit.py:343` `settle_point` still has a ceiling; one seeded question per game. |  |
| §4 | item 39 | OWED | 152 ledger entries still carry `line` (`scripts/check-banks.py:246`). |  |
| §4 | item 41 | OWED | `scripts/test-escape-rating.py:146` still hides `table.tt`. |  |
| §4 | item 42 | OWED | `scripts/check-look-signoff.py:55` skips a row without 9 cells; no cell-count check. |  |
| §4 | item 43 | OWED | `docs/apps-script-endpoint.js:21, :67` still read `previous_score`. |  |
| §4 | item 44 | OWED | No checkpoint in `verify-decimal-detective.py` or `verify-free-daily-pizza.py`. |  |
| §4 | item 45 | OWED | `.github/workflows/check-site.yml:70` is still `timeout-minutes: 10`. |  |
| §4 | item 46 | DONE | A CI check compares them, with plants: `scripts/check-escape-rooms.py:22-28` holds the front page's `data-room-count` and its number words to the live rooms and the hub's cards, seven faults planted on every run (ESC-BAND-SLIM, #786, d5381e86); it runs in the Gate (its `# ci-line: Escape rooms` header). | 236 |
| §4 | item 48 | OWED | No declaration requirement in `scripts/extract-banks.py` or `check-banks.py`; `docs/checker-tier4-design.md:139` still says awaiting. |  |
| §4 | item 49 | OWED | Not shown done: factor-race still shows only the factor counts (`games/factor-race/index.html:381`) and equation-builder is still listed "Answer shown, no reason" in row WRONG-PAUSE-REASONS. History note moved (where the row came from). | 59 |
| §4 | item 50 | STALE? | The same fault is §4 item 37(c); the three games still read only `mfg_dyslexia` and `measure-phone-fit.py:822` sets `mfg_accessible`. The two items name different owners (cloud lane here, home lane there). |  |
| §4 | item 53 | OWED | No follow-up recorded. |  |
| §4 | item 54 | OWED | No scope recorded. |  |
| Check-ledger debt | "One row per failing rule-and-game group in d..." | OWED | The section's rule, not work. |  |
| Check-ledger debt | LEDGER-B4-CHARACTERISTIC-QUEST | OWED | `data/check-ledger.json`: characteristic-quest B4 still fails at the same counts (further 26, level4 26; compared by script). |  |
| Check-ledger debt | LEDGER-B4-COMPONENT-CRUSHER | OWED | `data/check-ledger.json`: component-crusher B4 still fails at the same counts (alevel 15, gcse 15, level4 15; compared by script). |  |
| Check-ledger debt | LEDGER-B4-CONSTRUCTIONS-LAB | OWED | `data/check-ledger.json`: constructions-lab B4 still fails at the same counts (gcse 10, ks3 10; compared by script). |  |
| Check-ledger debt | LEDGER-B4-CORE-MATHS-PAPER1 | OWED | `data/check-ledger.json`: core-maths-paper1 B4 still fails at the same counts (core 36; compared by script). |  |
| Check-ledger debt | LEDGER-B4-CORE-MATHS-PAPER2A | OWED | `data/check-ledger.json`: core-maths-paper2a B4 still fails at the same counts (core 36; compared by script). |  |
| Check-ledger debt | LEDGER-B4-CORE-MATHS-PAPER2B | OWED | `data/check-ledger.json`: core-maths-paper2b B4 still fails at the same counts (core 36; compared by script). |  |
| Check-ledger debt | LEDGER-B4-CORE-MATHS-PAPER2C | OWED | `data/check-ledger.json`: core-maths-paper2c B4 still fails at the same counts (core 36; compared by script). |  |
| Check-ledger debt | LEDGER-B4-CURLING-FRICTION | OWED | `data/check-ledger.json`: curling-friction B4 still fails at the same counts (level4 20; compared by script). |  |
| Check-ledger debt | LEDGER-B4-DIMENSION-CHECKER | OWED | `data/check-ledger.json`: dimension-checker B4 still fails at the same counts (level4 28; compared by script). |  |
| Check-ledger debt | LEDGER-B4-EIGENVALUE-EXTRACTOR | OWED | `data/check-ledger.json`: eigenvalue-extractor B4 still fails at the same counts (further 25, level4 25; compared by script). |  |
| Check-ledger debt | LEDGER-B4-EIGENVECTOR-ENGINE | OWED | `data/check-ledger.json`: eigenvector-engine B4 still fails at the same counts (further 25, level4 25; compared by script). |  |
| Check-ledger debt | LEDGER-B4-ESTIMATION-GOLF | OWED | `data/check-ledger.json`: estimation-golf B4 still fails at the same counts (alevel 9, gcse 9, ks3 9, level4 9, year6 20; compared by script). |  |
| Check-ledger debt | LEDGER-B4-EXPECTED-DAMAGE | OWED | `data/check-ledger.json`: expected-damage B4 still fails at the same counts (core 15, gcse 20, ks3 15; compared by script). |  |
| Check-ledger debt | LEDGER-B4-FERMI-LAB | OWED | `data/check-ledger.json`: fermi-lab B4 still fails at the same counts (alevel 13, core 15, gcse 15, ks3 12, level4 10; compared by script). |  |
| Check-ledger debt | LEDGER-B4-FORCE-RESOLVER | OWED | `data/check-ledger.json`: force-resolver B4 still fails at the same counts (level4 20; compared by script). |  |
| Check-ledger debt | LEDGER-B4-FORMULA-FORGE | OWED | `data/check-ledger.json`: formula-forge B4 still fails at the same counts (level4 16; compared by script). |  |
| Check-ledger debt | BEST-KEY-PER-LEVEL | OWED | The fixed keys are still there (`pf_best`, `ps_best`, `il_best`, `ll_best`, `tw_best`); factor-race now also has `'fr_best_'+level`. |  |
| Check-ledger debt | LEDGER-B4-GIVEN-THAT | OWED | `data/check-ledger.json`: given-that B4 still fails at the same counts (alevel 25, core 20, gcse 25, level4 20; compared by script). |  |
| Check-ledger debt | LEDGER-B4-GLORIOUS-GANTT | OWED | `data/check-ledger.json`: glorious-gantt B4 still fails at the same counts (core 15, level4 15; compared by script). |  |
| Check-ledger debt | LEDGER-B4-GRADIENT-HUNTER | OWED | `data/check-ledger.json`: gradient-hunter B4 still fails at the same counts (alevel 10, core 20, gcse 15; compared by script). |  |
| Check-ledger debt | LEDGER-B4-GRAPH-SKETCHER | OWED | `data/check-ledger.json`: graph-sketcher B4 still fails at the same counts (alevel 15, core 15, level4 15; compared by script). |  |
| Check-ledger debt | LEDGER-B4-GROWTH-AND-DECAY | OWED | `data/check-ledger.json`: growth-and-decay B4 still fails at the same counts (alevel 15, core 15, level4 15; compared by script). |  |
| Check-ledger debt | LEDGER-B4-MATHS-COURT | OWED | `data/check-ledger.json`: maths-court B4 still fails at the same counts (core 10, gcse 20, ks3 15; compared by script). |  |
| Check-ledger debt | LEDGER-B4-MATRIX-CRUNCH | OWED | `data/check-ledger.json`: matrix-crunch B4 still fails at the same counts (further 35, level4 18; compared by script). |  |
| Check-ledger debt | LEDGER-B4-MOMENTS-MASTER | OWED | `data/check-ledger.json`: moments-master B4 still fails at the same counts (level4 20; compared by script). |  |
| Check-ledger debt | LEDGER-B4-NEGATIVE-NUMBER-LINE | OWED | `data/check-ledger.json`: negative-number-line B4 still fails at the same counts (year6 30; compared by script). |  |
| Check-ledger debt | LEDGER-B4-PRISONERS-DILEMMA | OWED | `data/check-ledger.json`: prisoners-dilemma B4 still fails at the same counts (alevel 9, core 9, gcse 9, ks3 9; compared by script). |  |
| Check-ledger debt | LEDGER-B4-PROBABILITY-PARADOX | OWED | `data/check-ledger.json`: probability-paradox B4 still fails at the same counts (core 38, gcse 38; compared by script). |  |
| Check-ledger debt | LEDGER-B4-PROOF-BUILDER | OWED | `data/check-ledger.json`: proof-builder B4 still fails at the same counts (alevel 33, further 10; compared by script). |  |
| Check-ledger debt | LEDGER-B4-REGRESSION-RUMBLE | OWED | `data/check-ledger.json`: regression-rumble B4 still fails at the same counts (alevel 14, core 12, level4 14; compared by script). |  |
| Check-ledger debt | LEDGER-B4-SCREENING-ROOM | OWED | `data/check-ledger.json`: screening-room B4 still fails at the same counts (alevel 20, core 15, gcse 20, level4 15; compared by script). |  |
| Check-ledger debt | LEDGER-B4-SEVEN-BRIDGES | OWED | `data/check-ledger.json`: seven-bridges B4 still fails at the same counts (alevel 25, gcse 25, ks3 25; compared by script). |  |
| Check-ledger debt | LEDGER-B4-STAT-ATTACK | OWED | `data/check-ledger.json`: stat-attack B4 still fails at the same counts (core 12, gcse 12, level4 12; compared by script). |  |
| Check-ledger debt | LEDGER-B4-TERRIBLE-ADVICE | OWED | `data/check-ledger.json`: terrible-advice B4 still fails at the same counts (core 12, gcse 20, ks3 18; compared by script). |  |
| Check-ledger debt | LEDGER-B4-TRUTH-WILL-SET-YOU-FREE | OWED | `data/check-ledger.json`: truth-will-set-you-free B4 still fails at the same counts (level4 32; compared by script). |  |
| Check-ledger debt | LEDGER-B4-WRONG-ON-THE-INTERNET | OWED | `data/check-ledger.json`: wrong-on-the-internet B4 still fails at the same counts (core 10, gcse 20, ks3 15; compared by script). |  |
| Check-ledger debt | LEDGER-B7-CHARACTERISTIC-QUEST | OWED | `data/check-ledger.json`: characteristic-quest B7 still has the same 7 entries (compared by script). |  |
| Check-ledger debt | LEDGER-B7-EIGENVALUE-EXTRACTOR | OWED | `data/check-ledger.json`: eigenvalue-extractor B7 still has the same 6 entries (compared by script). |  |
| Check-ledger debt | LEDGER-B7-EQUATION-BUILDER | OWED | `data/check-ledger.json`: equation-builder B7 still has the same 1 entries (compared by script). |  |
| Check-ledger debt | LEDGER-B7-MATRIX-CRUNCH | OWED | `data/check-ledger.json`: matrix-crunch B7 still has the same 30 entries (compared by script). |  |
| Check-ledger debt | LEDGER-B6 | OWED | `data/check-ledger.json`: B6 still has the same 18 entries in the same 6 games (compared by script). |  |
| Check-ledger debt | LEDGER-B3-ANGLE-ACE | OWED | `data/check-ledger.json`: angle-ace B3 still has the same 7 entries (compared by script). |  |
| Check-ledger debt | LEDGER-B3-MOMENTS-MASTER | OWED | `data/check-ledger.json`: moments-master B3 still has the same 1 entries (compared by script). |  |
| Check-ledger debt | EXTRACT-BANKS-MISREAD | OWED | `scripts/extract-banks.py` last changed by #892 (not this); the ledger still has negative-number-line year6 at 30. |  |
| Check-ledger debt | PHONE-FIT-NEXT-FOLD | OWED | `phone-fit-state.json` laptop still lists probability-paradox and trig-worms. |  |
| Check-ledger debt | ESCAPE-KEYPAD-FLAKY | OWED | `scripts/test-escape-keypad.py` unchanged since #434. |  |
| Check-ledger debt | CI-SPLIT-CANDIDATES | OWED | No policy recorded. |  |
| Check-ledger debt | CI-SHARD-FALLBACK | OWED | `scripts/ci-groups.py` `choose_parts()` still falls back to one part per unit. |  |
| §5 | "MaffsOptions.build() retrofit (~29 games han..." | OWED | Parked on purpose; not done. |  |
| §5 | "Matrix Crunch bank expansion to 50+50...." | STALE? | Row LEDGER-B4-MATRIX-CRUNCH holds the same bank to the 40 minimum (further 35, level4 18). |  |
| §5 | "Bank growth for 1.13's four over-promising g..." | DUPLICATE | Duplicate of rows LEDGER-B4-WRONG-ON-THE-INTERNET (ks3 15, gcse 20, core 10) and LEDGER-B4-EXPECTED-DAMAGE (ks3 15, gcse 20, core 15), which hold the same counts. The other two games are done: spot-the-muppet and better-value pass B4 in `data/check-ledger.json` (better-value by FOOTER-PHONE-FOUR). Nothing to add to the ledger rows. | 324 |
| §5 | "Escape rooms: the Car Trap voice rewrite (it..." | STALE? | Canon §11.1 (:2577): The Headteacher's Car Trap is live, "rewritten", since 10 Oct 2026. |  |
| §5 | "Certificates (Phase 1b), teacher portal (Pha..." | OWED | Parked on purpose; not built. |  |
| §6 | "Only what needs Jon: a ruling, a content rev..." | OWED | The section's rule, not work. |  |
| §6 | "Functional Skills Maths: no game maps to its..." | OWED | Added 28 Nov (#942); no ruling. |  |
| §6 | "Spot the Error banks (§1.23): KS3 35, Level..." | STALE? | spot-the-error passes B4 in `data/check-ledger.json`, so the counts (KS3 35, Level 4 30) are out of date. |  |
| §6 | "New Shapes banks (§1.27): 15 / 20 / 15...." | STALE? | new-shapes passes B4 in `data/check-ledger.json` (#731), so 15 / 20 / 15 is out of date. |  |
| §6 | "Regression Rumble (§1.26): Jon's look at the..." | OWED | The game is not rebuilt (1.26). |  |
| §6 | "Spec-map spot-check (blocks §3.1): 10 of the..." | DUPLICATE | Duplicate of row 3.1's "Blocked on" cell, which already reads "Jon: spot-check 10 of the 34 mixed statements in `data/dfe-gcse-parts.json` against the PDF". Nothing to add to 3.1. | 115 |
| §6 | "Analytics checkpoint (overdue): re-answer th..." | OWED | Jon's task; not recorded as done. |  |
| §6 | "DAILY-DEAL (MaffsCards' "Today's deal", 25 N..." | OWED | #919 merged; `games/maffscards/index.html:343` still has the placeholder words; the Creator sheet is not recorded as set up. |  |
| §7 | "Canon §4 still says 93 games; the roster (94..." | OWED | `docs/canon.md:515` still totals 93; `games/` has 118 folders. |  |
| §7 | "MAFFSGAMES_PROJECT_INSTRUCTIONS.md is not in..." | OWED | Not in the repo; the project's copy cannot be read from here. |  |
| §7 | "The project's own copies of canon.md and CLA..." | STALE? | Cannot be checked from the repo. The "temporary `plan` doc" and "the note at the top of this file" no longer exist in `docs/todo.md`. |  |
| §7 | "canon.md: game_restarted event not in canon'..." | OWED | `docs/canon.md` has no `game_restarted` (grep: none); `schools/assets/analytics.js:149` sends it. History note moved (where the line came from). | 41 |
| §7 | "CI maintenance:..." | OWED | Heading for the three lines below. |  |
| §7 | "serve-stubbed.py's port probe has no SO_REUS..." | OWED | No `SO_REUSEADDR` in `scripts/serve-stubbed.py`. |  |
| §7 | "Bump the runner pin deliberately after 19 Oc..." | OWED | Workflows still pin `ubuntu-24.04` (`check-site.yml:68`). |  |
| §7 | "Action versions: actions/checkout@v4 and act..." | OWED | Still `actions/checkout@v4` and `setup-python@v5` (`answer-counts.yml:49, :52`). |  |
| §7 | "HANDOVER-IN-TASK-PRS: BACKLOG-ONE's rule a:..." | STALE? | Every home contract since puts its handover entry in the task PR, and AGENTS.md still says to keep the branch handover current; no ruling from Project Claude recorded. |  |
| §7 | "CANON-SEARCH-RULE (SEARCH-KEYWORDS, 4 Nov):..." | OWED | `docs/canon.md` has no `MaffsSearch` (grep: none). |  |
| §7 | "CANON-ROOM-ESCAPED (ROOM-ESCAPED, 4 Nov): ca..." | OWED | `docs/canon.md:331` still says escaped (`game_completed`). |  |
| §7 | "CANON-MONEY-ANSWERS (MONEY-ANSWERS, 11 Nov 2..." | OWED | `docs/canon.md` §7.1.3 has the money box (:994) but not the widened rule (no `opts.currency`). |  |
| §7 | "ANSWER-BOX-CANON (ANSWER-BOX-TEXT, Jon 15 No..." | OWED | `docs/canon.md` does not name `check-answer-inputs.py` or the rule for every typed numeric answer. |  |
| §7 | "MAFFSANSWER-OWN-MARKING (ANSWER-BOX-TEXT, 17..." | OWED | `games/estimation-golf/index.html:825` still marks with `parseFloat`. |  |
| §7 | "WHOSE-SIDE-TIMER-LINE: .claude/rules/timer-..." | OWED | `.claude/rules/timer-policy.md` has no Whose Side line. History sentence moved (#688). | 46 |
| §7 | "ROOM-TIMES-READING: read the room-time data,..." | OWED | No reading recorded. |  |
| §7 | "TICKER-CLICKED-REVIEW (about 21 Nov): review..." | OWED | No review recorded; a week past its date. |  |
| §7 | "BURST-CLEANUP: remove schools/assets/burst...." | OWED | `schools/assets/burst.js` exists and 31 pages load it. The 6 P's has been listed since 27 Oct (`index.html:1743`), so the wait is over. |  |
| §7 | "CHECK-CHANGED-ONE-RUN (Jon, 29 Oct 2026): fu..." | STALE? | Neither lane runs check-changed before pushing since HOME-LEAN (#787, 15 Nov; AGENTS.md:52); local runs are optional. |  |
| §7 | "PORTAL-RESET-TRIGGER — trigger: 'reset':..." | OWED | `index.html` calls `reportFilter` with fresh, level, topic and search only (:3425-3557). |  |
| §7 | "ESCAPE-FEEDBACK-LINK — the escape-room feedb..." | OWED | `scripts/check-footer.py:64` still exempts `escape-rooms/`. History clause moved (the footer PR). | 48 |
| Parked, low priority | "check-lock-bank.py flags a computed n == len..." | OWED | `scripts/check-lock-bank.py:88` `is_tautological` unchanged; parked. |  |
| Parked, low priority | "Escape-room games saved before 0907f6e resum..." | OWED | No action planned by the line itself; nothing to show either way. |  |
| Parked, low priority | "serve-stubbed.py blocks every fetch, not jus..." | OWED | `scripts/serve-stubbed.py:164` sends `no-store` only on its stubbed and pinned replies, not on ordinary files. |  |
| Parked, low priority | "GA4 inline gtag page_view still fires on non..." | DONE | No page carries the inline snippet now: GA4 loads from `schools/assets/analytics.js` on the live host only (:31-37, `var LIVE = location.hostname === ...`; GA4-LIVE-ONLY, #311, 7c4c8115); `grep "gtag('config'" games/*/index.html index.html` finds nothing. | 151 |
| Parked, low priority | "DAILY-BOARD-GROWTH: Free Daily Pizza writes..." | OWED | No decision recorded. |  |
| Post-freeze | "Jon, 29 Oct 2026: the roster Calculator tag..." | OWED | `scripts/check-calculator.py` still ties loading the calculator to the roster tag; the list is not confirmed. |  |

## For Jon: STALE? items

Ruled by Jon, 28 Nov 2026; applied by TODO-RULINGS.

Nothing here was moved. Each line: what it is, why it may no longer matter, and the choice.

1. chart-interrogator "submits a constant 100" (§2): the page now multiplies its score (:1277), so the constant may be gone; the `l4` key is still there. Keep (and re-check the score), or close the constant-100 half.
2. 3.20, back links and headers on 40 games: site-nav.js now owns back links on 117 pages, so folding each game onto one pattern may no longer matter. Keep, or close.
3. FOLD-COMPONENTS PRs 3-6: four branches untouched since 27 Oct. Keep (rebase and finish), or close and delete the branches.
4. CURLING-TEACH, Curling Friction teaching at Level 4: low priority, held since 4 Nov, nothing since. Keep, or close.
5. ABOUT-PAGE: an About-page contract from 27 Oct that was never sent. Keep, or drop (the row's own question).
6. PRIME-SPRINT-LOOK-REDS: settled by #660; left is the Start button 30 px under the fold in Aa at 375x667. Close, or contract that fix (the row's own question).
7. ESTIMATION-GOLF-ART: parked 3 Nov, the game still has no start screen for the art. Keep (and rule placement), or close.
8. HIGHER-POWER-PHONE: parked 3 Nov; the gate still lists Higher Power as failing on phones. Keep (and unpark), or close.
9. SCREENING-ROOM-PANELS ("item E"): parked, and nobody has the contract text. Keep (Jon restates it), or close.
10. ANSWER-CONTROL-TALL-INPUT: parked 3 Nov; ANSWER-BOX-TEXT has since reworked answer boxes in 12 games, so the lists of 8 and 6 may be out of date. Keep (re-survey), or close.
11. WHEN-WILL-I-USE-THIS: the section is built and has grown to 47 jobs (#883, #888, #891). What the row still owes (more topics? nothing?) is not written. Keep (and say what is left), or close.
12. §3.9 "The rule for the order" (1 Oct): fixes now come game by game off the gate's known-failures list. Keep the 1 Oct order, or close it and work from the gate's list.
13. §3.9 "The order", batches 2 to 19: not followed since October; the gate's known-failures list (31 games in normal mode) is the live record. Keep, or close in favour of the gate's list.
14. §3.9 "Aa mode: one fix across three games": the gate now measures Aa and lists none of the three as failing the fold (New Shapes scrolls sideways at 320 in Aa). Keep, or close.
15. "Bond. Number Bond." (idea) and row NUMBER-BONDS: one game or two? Keep both, or close the idea into the row.
16. IT Vengeance "rebuild" (escape-room idea): its URL now redirects to The Rightful King. Keep the rebuild, or close.
17. §4 item 4, the 21 Sep timer audit of seven files: every game's wrong-answer pause is now checked in CI and the five games have been reworked. Keep (audit the rest of timer-policy), or close.
18. §4 item 5, "35 of 42 games still to read" for tier 3's UNSUPPORTED ledger: tier 3 was re-surveyed on 24 Nov and the numbers no longer hold. Keep (restated from the new report), or close.
19. §4 item 14, self-host Outfit: the gate half is done (it measures in Outfit from `scripts/fonts/`). Is serving Outfit and KaTeX to students from the repo still wanted? Keep that half, or close.
20. §4 item 18, CI Contract B parity: the listed failures are Windows-local, and local runs are no longer a merge condition. Keep (for the branch-protection step), or close.
21. §4 item 19, a one-off B4 flake on proportion-blaster (4 Oct): not seen since. Keep, or close.
22. §4 item 21, GATE-STEP-6 shard migration: "insurance only", waiting on Jon since October. Keep, or close.
23. §4 item 23, LOCAL-CHECKS (verifiers failing locally in WSL): CI is the authority and local runs are optional. Keep, or close.
24. §4 item 32, PHONE-FIT-DRIVER-RULINGS: Jon's 20 Nov start-screen ruling (row START-SIDEWAYS-GATE) may cover it. Keep (the 11-game exception), or close.
25. §4 item 33, SIX-PS-PHONE-FIT: parked 3 Nov, unchanged. Keep, or close.
26. §4 item 34, MODE-DIMENSION ("item D"): parked, no contract text anywhere. Keep (Jon restates it), or close.
27. §4 item 35, START-SCREEN-RULE: parked; START-SIDEWAYS-GATE now carries Jon's start-screen ruling. Keep, or close into that row.
28. §4 item 50, AA-KEY-MISMATCH: the same fault as item 37(c), with a different owner. Keep both, or close this one into item 37 (and say whose it is).
29. §5 "Matrix Crunch bank expansion to 50+50": the ledger row already asks for 40 per level. Keep 50+50 as the target, or close into the ledger row.
30. §5 "the Car Trap voice rewrite ... rooms A and B": Car Trap went live rewritten on 10 Oct. Keep (if rooms A and B are something else), or close.
31. §6 "Spot the Error banks (§1.23): KS3 35, Level 4 30" for Jon's review: every level now has 40 or more. Keep (review the new questions), or close.
32. §6 "New Shapes banks (§1.27): 15 / 20 / 15" for Jon's review: every bank now has 40 or more. Keep (review the new questions), or close.
33. §7 "The project's own copies of canon.md and CLAUDE.md lag the repo ... delete the temporary plan doc": the note it points to is gone. Keep (Jon checks the project's files), or close.
34. HANDOVER-IN-TASK-PRS (rule a: task PRs never edit the handover): practice and every contract since do the opposite. Keep (and rule), or close.
35. CHECK-CHANGED-ONE-RUN (write the one-run-at-a-time rule into the docs): check-changed is no longer run before pushing. Keep, or close.

## Found, not recorded

- **PHONE-FIT-ALL-ITEMS has no row.** Row CGD-PHONE-LONG waits for "the Gate measures every item (PHONE-FIT-ALL-ITEMS)", and no item carries that name. The nearest are §4 item 37(b) (one seeded question per game) and item 20's still-owed line (later screens unmeasured). Nothing added.

## Seen while auditing

- Counts and line numbers inside rows that stay have drifted (3.12 and LOOK-REFRESH-PALETTE: 85 NOT_YET, not 88; EXPECTATION-EXACT: 5 matches of `formatPNum`, not 3; 1.71's `NOT_ON_HUB` line; §2's line numbers). Not changed: correcting them would reword owed text.
- GRAPH-SKETCHER-REDESIGN points (2) and (10) say the shared calculator has no x^y, e, sin or cos. It has had them, in scientific mode, since SCI-CALC (ee64b6a5, 9 Oct 2026). Project Claude's to reword.
- §4 item 17 is half done (two of its four scripts now run in CI) and row 3.21 is half done (11 of 22 games on the keypad); in both the finished half cannot be cut without rewording, so nothing moved. Project Claude's to rewrite.
- §4 item 37(b), item 20's still-owed line and CGD-PHONE-LONG's PHONE-FIT-ALL-ITEMS describe overlapping work (the gate measures one screen of one seeded question). Not the same text, so not merged.
- The file's preamble ("This repository's PRs are #1-#31 so far") and the START OF NEXT SESSION block are outside the audit: not items, and the block's wording is not to be touched.
- ANSWER-AUDIT-RUN is time-limited: the row's API credit expires 6 Dec 2026.

## How it was checked

Each item was read against main: the files, checks and lists it names, `data/check-ledger.json`, `scripts/phone-fit-state.json`, `scripts/checker-allowlist.json`, the roster, canon, remote branches and merged PRs. The 43 LEDGER rows were compared with the ledger by script, entry for entry. Anything that could not be shown done is OWED or STALE?.
