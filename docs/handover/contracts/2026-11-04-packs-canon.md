# PACKS-CANON (received 4 Nov 2026, cloud lane, Claude Code)

Saved verbatim on receipt (canon §7.8.2, CONTRACTS-FOLDER), with Jon's pre-step from the same hand-off.

## Pre-step (verbatim)

PRE-STEP (Jon, 4 Nov): docs/handover/cloud.md is at 20,342 of 20,480 bytes. Before adding this contract's queue line,
move every DONE item's prose out of the queue section, verbatim, into docs/history/handover-cloud-archive.md under a
dated entry "Queue DONE items moved 4 Nov", leaving in the queue only one pointer line to that entry plus the live and
parked items. Then add the c351d90 close-out (SEARCH-KEYWORDS) and this contract's line. The size check must pass
without its warning.

## Contract (verbatim)

CONTRACT: PACKS-CANON (cloud lane, Small; Jon, 4 Nov 2026)
LANE EXCEPTION, THIS CONTRACT ONLY (Jon, 4 Nov): you may edit docs/canon.md (§7.1, the backlog and §12 only).
Save this contract verbatim as docs/handover/contracts/2026-11-04-packs-canon.md in the first commit, with one
line in docs/handover/cloud.md's queue. Moved from the home lane (Codex) to cloud; PACK-GENERATOR follows it in cloud.

TASK: Amend the free-forever principle in canon to permit paid offline teacher packs, keeping everything online free.

ROOT CAUSE: Jon has decided (5 Oct 2026; resumed 3 Nov 2026) to sell printable group-race packs of escape rooms through
a teacher resource marketplace (Tes first). Canon §7.1 says "Free forever — no subscription, no freemium, no ads"
(docs/canon.md:745 on 4 Nov), which as written forbids it.

CLASS CHECK: Not a bug class: one policy statement. Local edit, plus a search for every other place canon or a public
page states the same principle (reported, not edited).

EXACT CHANGE:
1. docs/canon.md §7.1: replace the free-forever line with, verbatim: "Everything a student plays is free, forever. No
   subscriptions, no ads, no sign-up. Teachers may buy offline convenience versions of free content (e.g. printable
   escape-room packs); the online version stays free and identical. Paid packs are sold through an external
   marketplace first; nothing paid is sold or linked from maffsgames.co.uk without Jon's approval."
2. Canon backlog: "Escape-room printable packs: pilot (The Kiln Disaster, 7 sets) on an external marketplace; review
   sales before offering via the site." Reason line in §12 (Jon, 5 Oct and 3 Nov 2026).
3. Report (do not edit) every other occurrence of free-forever or no-freemium wording in canon, AGENTS.md, CLAUDE.md
   and public pages (about, privacy, homepage), with file and line, in the PR body and in docs/handover/cloud.md.

DO NOT TOUCH: Any other canon section; any site page; AGENTS.md; CLAUDE.md; tools/; escape-rooms/; anything for
PACK-GENERATOR.

SUCCESS CONDITION: §7.1 carries the new wording verbatim; backlog and §12 lines present; the occurrence report in the
PR; the handover size check passes without its warning; main green; merge on green with merge-pr.py <n> --watch; the
work is committed and docs/handover/cloud.md records the state, including that PACK-GENERATOR is next in cloud.

STOP IF: Canon §0 or any public page states the principle in words the packs would contradict (report the wording;
Jon decides); the §7.1 line is no longer "Free forever — no subscription, no freemium, no ads"; the pre-step cannot
bring cloud.md under its limit without moving live or parked items.

## Found on receipt (4 Nov, Claude Code)

- Pre-step: done in 953a0ca (21 DONE items moved verbatim; no live or parked item moved; 17,224 bytes). STOP IF 3 clear.
- STOP IF 2 clear: docs/canon.md:745 reads "- Free forever — no subscription, no freemium, no ads".
- STOP IF 1 HIT (reported for Jon; the canon edit is made, the merge waits for his ruling): about/index.html:161,
  "Free forever &mdash; no subscriptions, no freemium, no ads". The new §7.1 wording drops "no freemium"; a paid
  printable version of free content can be read as a premium version, which the About page's "no freemium" rules out.
  Canon §0 does not state the principle.
