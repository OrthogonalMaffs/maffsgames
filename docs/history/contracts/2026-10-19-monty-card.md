CONTRACT: MONTY-CARD (Project Claude for Jon, 19 Oct 2026, 13:45). CLOUD LANE.
Save verbatim under docs/handover/contracts/ in the first commit.

TASK: Rewrite the "100 Doors Makes Monty Hall Obvious" Misunderstood
Maths card so it states the puzzle's setup and the condition that makes
switching win, and report any other card that assumes setup it never
states.

ROOT CAUSE: The card says "Monty opens 98 goat doors" without saying
that a car is behind one door, goats are behind the rest, or that the
host knows where the car is and opens only goat doors. The last point is
what makes switching win 99 in 100: if the host opened doors at random,
it would be 50/50. A reader who has not met the puzzle gets jargon. The
condition the misconception depends on is missing, on a card whose
purpose is to correct misconceptions.

CLASS CHECK: Not yet determinable. Locally, it is one card's wording.
The same habit (a famous puzzle's setup taken as known) may run through
other Misunderstood Maths cards; step 3 reports, it does not fix. If the
cards are hand-written into markup in more than one place, see STOP IF.

EXACT CHANGE:
1. Find the card's source (data file or markup) and every place its text
   appears. Report them in the PR.
2. Replace the card's text, keeping its title, category label, button
   ("Test your probability intuition →", same link) and Share:
   Summary: "100 doors: a car behind one, goats behind the other 99.
   You pick one. The host, who knows where the car is, opens 98 of the
   others, all goats. Should you switch? Switching wins 99 times in
   100."
   Expanded: "Your door was a 1-in-100 guess, and nothing the host does
   changes that. The other 99 doors held the car 99 times in 100. The
   host has to avoid the car, so all of that chance ends up on the one
   door he leaves shut. The catch: he must know where the car is. If he
   opened doors at random and just happened to show goats, it would be
   50/50. The 3-door version works the same way (switching wins 2/3,
   staying 1/3); it just doesn't feel as dramatic."
3. Read every other Misunderstood Maths card. In the handover entry,
   list each one that relies on setup, terms or conditions it never
   states, quoting the phrase and saying what is missing. Change none
   of them.
4. Verifier: the card shows both texts exactly as in step 2, in summary
   and expanded states, at 320, 390 and 1280 px, with no overflow and
   the button and Share still present. Main's copy must fail.
5. python scripts/check-changed.py before opening the PR; report
   container-caused failures as before, with main failing them
   identically. Merge on green with main green; watch main's run.
6. Handover entry in docs/handover/cloud.md, including step 3's list.

DO NOT TOUCH: any other card's text; the card's title, category,
button, link or Share; the Misunderstood Maths filter or layout;
probability-paradox or any game; ROOM-CREDIT v2's files beyond this
card's own text.

SUCCESS CONDITION: The card reads exactly as in step 2 everywhere it
appears. The verifier passes and main's copy fails it. The handover
lists every other card with unstated setup, or says there are none.
CI green; merged; main green.

STOP IF: The card's text is hand-written in more than one place with no
shared source: report each place and wait. The card is also used
somewhere other than the homepage (a share image, social metadata, a
parents page) whose text would then differ. Main's latest full run is
red. ROOM-CREDIT v2 is open and both PRs edit index.html: finish and
merge ROOM-CREDIT v2 first, then start this.

---

Jon's ruling, 19 Oct 2026 (asked during the build): on phones (600 px and below) the front page's compact mode
hides every fact card's summary, with no way to open it, so phone readers never see the new setup sentence. The
layout is DO NOT TOUCH. Ruling: ship the text as specified and test truthfully: the verifier requires the summary
shown at 1280 px, the summary's text exact at every width (Share copies it), and the expanded text, button and
Share shown and exact everywhere; at 600 px and below it records that the summary is hidden. The phone gap is
reported for a later layout contract.
