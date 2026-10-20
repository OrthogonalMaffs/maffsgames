CONTRACT: MONTY-100-RETITLE (Jon, 20 Oct 2026; file name as the contract gives it). CLOUD LANE. Saved verbatim.

TASK: Retitle the front-page fact card "100 Doors Makes Monty Hall Obvious" to "Monty Hall, With 100 Doors" and replace its expanded text with Jon's approved wording (20 Oct 2026).
ROOT CAUSE: The title tells the reader the result is obvious, but the expanded text (x) repeats the 3-door probability argument with bigger numbers and never gives the picture that makes the 100-door version persuasive. A student who does not see it is told, in effect, that the problem is them. Jon's ruling, 20 Oct: remove "obvious" and use the new text.
CLASS CHECK: Local. The card is one entry in the FACTS array in index.html; loadFact() and Share have no fault. The wording is a content ruling for this card alone. Other cards' wording is not in scope.
EXACT CHANGE: index.html, the FACTS entry currently titled "100 Doors Makes Monty Hall Obvious":
  t -> "Monty Hall, With 100 Doors"
  x -> exactly: "You pick door 1. The host opens every other door except door 57. Why did he skip 57? Either your door hides the car, which happens 1 time in 100, or 57 does, which happens the other 99 times. Switching is the same as swapping your one door for all 99 others; the host has just opened the empty ones for you. The catch: he must know where the car is. If he opened doors at random and happened to show only goats, it would be 50/50. Three doors work the same way (switching wins 2 times in 3); it just doesn't feel as clear."
  h, g, gl unchanged.
scripts/verify-facts.py: re-key this card's pins to the new title; pin the new claims, each recomputed (1 in 100 stay, 99 in 100 switch, 50/50 for a random host by exact fractions, 2 in 3 for three doors).
scripts/test-fact-monty.py: TITLE and the expected x updated; the docstring names the new title and this contract. The test still holds both texts exactly, the button and Share shown, and no overflow at 320/390/1280.
Save this contract verbatim as docs/handover/contracts/2026-10-20-monty-100-retitle.md in the first commit; move it to docs/history/contracts/ when merged.
DO NOT TOUCH: h (the summary, written under MONTY-CARD); the "The Monty Hall Problem" card (card 2, its own contract); every other card; the phone compact mode; loadFact() and Share; docs/history/contracts/2026-10-19-monty-card.md (an archive, so its old title stays).
SUCCESS CONDITION: The new title and text render exactly. verify-facts.py and test-fact-monty.py pass, and fail when the old title or text is planted. No file outside index.html and the two scripts contains the old title, apart from history and contract archives. check-changed.py green; merged on a green Gate; main's run green after.
STOP IF: The card 2 PR is still open (wait for it to merge, then rebase; never edit FACTS in parallel); the new text overflows at any tested width; the old title is found in any other live page, share image, sitemap or metadata; or a check needs changing beyond these two scripts.
FINISH: Committed and merged; docs/handover/cloud.md updated with the entry, PR number and main run.
