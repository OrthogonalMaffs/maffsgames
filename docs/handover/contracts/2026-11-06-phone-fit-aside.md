# PHONE-FIT-ASIDE (Jon, 6 Nov 2026), verbatim

Name given by the home lane (the contract has none).

LANE: home · TIER: Shared · from current main

COORDINATION: the cloud lane owns games/whose-side-are-you-on/ and scripts/verify-whose-side-are-you-on.py (WHOSE-SIDE-FIT, then WHOSE-SIDE-BIOS). Do not touch either. Record in docs/handover/home.md.

START: claim equatle, 52dle and prime-or-composite on scripts/answer-lock-state.json in one commit of its own; remove the claims in the fix PR.

TASK: Make scripts/measure-phone-fit.py ignore controls inside a declared non-answer region (a leaderboard), so games with leaderboards are measured by their real answer controls.

ROOT CAUSE: __pfAsking() treats as an answer control every visible text input on the page and every visible button whose text starts with a submit word (SUBMIT_RE: check|submit|answer|enter|...), anywhere in the document; __pfSubmit() clicks the first such button. A leaderboard's name box and "Submit Score" button match both rules. Equatle's leaderboard (.lbw: #lbname, #lbsbtn "Submit Score (finish puzzle first)") sits below the board, so its bottom is read as the answer controls' bottom and Equatle is mis-measured; it stays on known-failures for that reason (handover 6 Nov, queue item 1). 52dle and prime-or-composite carry the same pair (#name-input, "Submit Score") inside a modal that is hidden while asking, so they escape today only because the modal is hidden.

CLASS CHECK: Yes. The fault is in shared infrastructure (the one checker every game passes through), and the same shape (a name input plus "Submit Score") is in three games. The fix is in the checker: a declared region it never counts, one shared marker, not a per-game exception list and not a text denylist ("score" is a word a real answer button could carry).

EXACT CHANGE:
1. Convention: a container holding controls that are not part of answering the question carries data-mfg-aside="<what>" (e.g. data-mfg-aside="leaderboard"). Record it in docs/canon.md §7.6.1 in two sentences: what it means, and that it may never contain any part of the question's answer controls.
2. scripts/measure-phone-fit.py, in the injected page script: __pfAsking() and __pfSubmit() skip any element with el.closest('[data-mfg-aside]'). Guard: if any element of tier 3's option group (window.__mfgGroup) is inside a [data-mfg-aside] region, the game's row reports "answer control inside data-mfg-aside" and FAILS (never passes silently). The report lists, per game, each aside region's value and how many controls it skipped.
3. Tag the leaderboard containers: games/equatle/index.html .lbw; games/52dle/index.html #modal; games/prime-or-composite/index.html #modal. Attribute only; nothing else in those files changes.
4. selftest(): add cases: (a) an aside with a name input and "Submit Score" below the fold beside answer controls above it: passes, measured by the answer controls; (b) the same without the marker: fails as today; (c) the option group inside an aside: fails with the guard's message.
5. Re-measure equatle, 52dle and prime-or-composite in normal, aa and laptop modes. In scripts/phone-fit-state.json remove only the entries that now pass (the lists only shrink); report any that still fail, with the measured bottom, fold and the control that sets it.
6. Report: equatle's asking-screen bottom and fold at 320x568, 375x667 and 390x844, and laptop sizes, before and after.

DO NOT TOUCH: SUBMIT_RE, CONTINUE_RE and the canvas rule; the fold, settle and classify logic; the known-failures and sideways entries of any other game; any other game's files; the games' leaderboards' behaviour, styling or text; games/whose-side-are-you-on/ and its verifier; escape-rooms/ and tools/pack-generator/; docs/handover/cloud.md.

SUCCESS CONDITION: The checker ignores controls inside [data-mfg-aside] and fails loudly if an answer control is inside one; selftest passes with the three new cases; the three games are tagged; Equatle is measured by its board and keypad, and is off known-failures in every mode where it now passes; no other game's phone-fit result changes. Committed, PR open, Gate green, entry in docs/handover/home.md; stop for Project Claude's review and Jon's "merge".

STOP IF: Equatle still fails after the change for a reason other than the leaderboard (report it; do not fix the game here); any other game's phone-fit result changes; a game's answer controls turn out to live inside its leaderboard container; tier 3's probe (__mfgProbe) itself picks up the leaderboard (that is a different layer: report).
