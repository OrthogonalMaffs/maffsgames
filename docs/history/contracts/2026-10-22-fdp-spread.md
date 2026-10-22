# FDP-SPREAD (Jon's rulings, 22 Oct 2026, on FDP-KEY-COLLIDE), verbatim

Rulings (Jon, 22 Oct), FDP-KEY-COLLIDE:
(1) Option 2: fix FDP.spread first, in its own PR (FDP-SPREAD): a placement that always separates same-value questions when separation is possible; the verifier checks 10,000 seeds per practice mode, with the current spread as a plant; question content, daily pizza, scoring and boards unchanged. Claim free-daily-pizza for it as usual; merge through merge-pr.py when green.
(2) Then rebase claude/fdp-key-collide onto it, re-run, and merge after 23:00 UK, recording the first changed daily date in the handover.
(3) Changing the test seeds is ruled out, as you said.
Carry on with #479, then the K() scan, in your order.

## The finding that prompted it (cloud lane, 22 Oct)

FDP.spread makes one pass of swaps. Over 10,000 seeds on main, 245 mixed/20 practice sets and 4 mixed/40 sets kept two
neighbours about the same value although separation was possible (single-stage sets: 0). FDP-KEY-COLLIDE's filter
changed what seed 2026 draws, and the verifier's mixed/20 seed-2026 check failed on it: stage 1's five were
4/5, 1/100, 1/100, 1/8, 1/100 (separable as 1/100, 4/5, 1/100, 1/8, 1/100); spread left two 1/100 together.
