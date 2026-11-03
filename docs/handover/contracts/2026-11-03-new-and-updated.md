CONTRACT: NEW-AND-UPDATED
Tier: Shared · Lane: home · Implementer: Codex (WSL)

START
git -C ~/maffsgames pull --ff-only, then a worktree codex/new-and-updated from origin/main. Claim index.html.

TASK
Build the homepage's new-games section from the same dated badges as the "New & updated" filter: newest first, at
most 12 games, titled "New and updated", with wording that never goes out of date.

ROOT CAUSE
The section #cmpNew ("New for 2026/27") is a hand-placed list of 18 cards with no badge dates, written at the start
of the year and never maintained: it omits every game released since (Who Ate All the Pies?, I Found a Mark, How
Many Parts?), has no order, and its note ("New games arrived late last year") is stale. The filter beside it reads
dated metadata (data-badge, data-badge-date, applyBadges(), BADGE_DAYS = 56, canon §3.4) and is correct. Two
sources for one fact; the hand-kept one drifted (Jon, 3 Nov 2026).

CLASS CHECK
Yes: a hand-maintained copy of data that already exists as metadata, the same class as copied backlogs going stale.
Fix by deriving the section from the badge metadata in applyBadges()'s pass (one source), not by editing the
hand list.

EXACT CHANGE
1. index.html, #cmpNew: remove the 18 hand-placed cards. At load, in or beside applyBadges() (same mfgToday() and
   BADGE_DAYS), fill the section's grid with one card per game whose badge is live: a copy of that game's first
   card on the page, sorted by data-badge-date newest first (ties: New before Updated, then card title A-Z),
   at most 12 (const NEW_CAP = 12, commented with Jon's ruling). If no badge is live, hide the whole section.
   Each copied card keeps its href, badge ribbon and data attributes; no element id is duplicated.
2. Heading: "New and updated". Note (replace the stale one), exactly: "The newest games first, and games that have
   had real work done: new questions, new levels or new help. Each one is also in its level section below. Every
   game feeds the leaderboards and keeps a score history on your device." (keep the leaderboards link). The phone
   summary line keeps its live count ("<n> new and updated games").
3. Section label: data-mfg-section becomes "new-and-updated"; update canon's label list (line on portal labels,
   §2) and scripts/test-section-clicks.py to match. Canon §3.4: one line saying the section is built from the
   badges, newest first, capped at 12 (Jon, 3 Nov 2026); reason in §12.
4. Test (extend verify-card-filter.py or a new ci-line script with --selftest): with mfgToday() stubbed in the test
   only, assert newest-first order, the cap of 12 with more than 12 live, a game appearing once, the section hidden
   when none are live, Pies present on 3 Nov 2026, and the filter's results unchanged. Plants: order reversed, cap
   removed, a hand card left in the section; each CAUGHT.

DO NOT TOUCH
BADGE_DAYS and the badge rules (canon §3.4 definitions); the "New & updated" filter's behaviour; any badge date or
game card outside #cmpNew; the phone compact (.cmp) behaviour; other sections; game files; Gate files.

SUCCESS CONDITION
On the live portal on 3 Nov 2026 the section shows at most 12 games, newest first, including Who Ate All the Pies?
and I Found a Mark; the filter gives the same set as before; tests and plants pass; test-section-clicks.py passes;
phone fit unchanged at 320x568, 375x667, 390x844; check-changed.py green; Shared review by Project Claude; stop at
Gate green for Jon's "merge"; Record line.

STOP IF
index.html is claimed or touched by another open PR; a badge date on a live card is missing or malformed (list them,
do not guess dates); copying a card would duplicate an id or break the card's analytics events; the phone summary
cannot show a live count without changing .cmp behaviour.

Amendment 1 (Jon, 3 Nov 2026):
No concurrency exception (Jon, 3 Nov): #646 is merging now. Wait until git log origin/main shows DASH-MINUS
(#646) merged, pull, then start NEW-AND-UPDATED from a fresh worktree on that main. If it has not merged within
an hour, stop and report.

Amendment 1 (Jon, 3 Nov), NEW-AND-UPDATED: DO NOT TOUCH lifted for one line in
scripts/verify-circle-theorem-spotter.py check_copies(): the portal card count changes from exactly 2 to at least 1
(every card found must still read CARD exactly, and none may say "seven"). Reason in the PR: the second card was the
hand-placed copy in #cmpNew, which this contract removes; the section's cards are now built at load, so no static
count is stable. Its plants must still be caught. No other change to that verifier. Then finish the full checks, open
the PR, and stop at Gate green for review as the contract says.
