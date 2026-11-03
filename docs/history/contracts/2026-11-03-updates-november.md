CONTRACT: UPDATES-NOVEMBER
Tier: Small · Lane: home · Implementer: Codex (WSL)

START
git -C ~/maffsgames pull --ff-only, then a worktree codex/updates-november from origin/main.

TASK
Add a November 2026 section to the What's changed page (/updates/) with Jon's approved wording, give The 6 P's its
"new" badge so it appears in the homepage's New and updated section, and make every future student- or
teacher-visible PR add its own line, so the page never goes quiet again.

ROOT CAUSE
/updates/ ends at October 2026 although eight user-visible changes went live between 1 and 3 Nov (Jon, 3 Nov 2026).
Nothing adds an entry when work merges: the page depends on someone remembering. The 6 P's (listed 27 Oct 2026,
#597) has no data-badge on its homepage card, so the New and updated section (#648) cannot show it.

CLASS CHECK
Yes for the updates page: every user-visible PR in both lanes, so fix the rule (AGENTS.md, one line) as well as adding
this month's entries. The 6 P's badge is local: one card's metadata.

EXACT CHANGE
1. updates/index.html: a "November 2026" section above October, in the page's existing markup and classes, with
   exactly this content (game names link to their game pages as October's entries do):
   - Theme line (bold) and paragraph: "The small stuff that trips students up." / "Most of this month's work is the
     kind nobody notices until it goes wrong: a dash that looks like a minus sign, a question with no way out, a
     fraction typed sideways. We've been hunting those down."
   - "No more dashes pretending to be minus signs." / "An answer option reading “Victor is wrong — x = 625” looks a
     lot like “−x = 625”, and the students most likely to be caught out are the ones we built this site for. We've
     changed 206 of them across 31 games and escape rooms, and a check now stops new ones sneaking in."
     (The quoted dash example is deliberate: list it as the documented exception if check-dash-minus.py flags it, by
     the check's own exception mechanism, not by weakening the check. If it has none, STOP.)
   - Under "New", newest first:
     3 Nov 2026: "“New and updated” on the home page" now shows the newest games first, and keeps itself up to date.
     3 Nov 2026: "A way out of every question." Who Ate All the Pies? now has "← Stages" and "Back to Games" on every
       question and worked example, like the other stage games. Escaping a pie chart should never need the browser's
       Back button.
     3 Nov 2026: "Fractions, typed the way you write them." In Who Ate All the Pies? you now type a fraction with the
       top number over the bottom one, not sideways with a slash. More games will follow.
     3 Nov 2026: "Pictures on the start screens" of Football Pitches per Squared Squirrel, Take a Walk, Formula Forge,
       Just Pythag It, Bruv, Factor Race and Free Daily Pizza, and a new scene for I Found a Mark.
     2 Nov 2026: "Who Ate All the Pies? gets its matchday look:" a pie stall, in red and white.
     1 Nov 2026: "Graph Transformer explains itself." After each graph, or if you skip one, it names each
       transformation in exam language, shows the equation before and after, and says why the curve moves the way it
       does.
2. index.html: The 6 P's card (href="the-6-ps/") gains data-badge="new" data-badge-date="2026-10-27", per canon §3.4
   (a genuinely new item, listed 27 Oct 2026, #597). No other card changes.
3. AGENTS.md, one line within the 300-byte rule: "A PR that changes what a student or teacher sees adds its dated
   line to /updates/ in the same PR, in plain words; internal work does not." Reason to canon §12 (Jon, 3 Nov 2026).

DO NOT TOUCH
October and earlier entries; any game file; any other homepage card or the section's code; other AGENTS.md rules.

SUCCESS CONDITION
/updates/ shows November above October with the text above, links working; the homepage's New and updated section
shows The 6 P's third (after I Found a Mark and Who Ate All the Pies?), with verify-new-and-updated.py passing;
check-dash-minus.py and every page check pass; the AGENTS.md line present; check-changed.py green; merge on green with
merge-pr.py <n> --watch --wait 3600; Record line.

STOP IF
Another open PR touches updates/index.html, index.html or AGENTS.md; the page's markup cannot take a month section
without a layout change; check-dash-minus.py would need weakening to allow the quoted example; The 6 P's card already
carries a different badge.

Amendment 1 (Jon, 3 Nov), UPDATES-NOVEMBER: check-dash-minus.py's scope does not include updates/, so the quoted
"Victor is wrong — x = 625" example needs no exception and the check is not changed. The STOP IF on the exception
mechanism is resolved. Proceed with the contract as written.
