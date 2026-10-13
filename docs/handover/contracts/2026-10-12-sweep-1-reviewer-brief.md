<!-- SWEEP-1: the brief each per-game reviewer agent is given (read-only), kept so a new session can carry on. The scratch paths in it are one session's; a new session points them at its own scratchpad. -->

# SWEEP-1 reviewer brief (read-only)

You are reviewing ONE maths game in the repo at /home/user/maffsgames for MaffsGames' SWEEP-1, a reading sweep.
The audience is UK students who struggle with maths (grade 1-3, resitters). The maths must be right.
**Do not edit, create or delete any file in the repo. Do not run git commands that change anything.** You may write
scratch files only under /tmp/claude-0/-home-user-maffsgames/ee02da46-4701-5b9e-83ce-cb6641866247/scratchpad/<slug>/ (e.g. to
run node/python to draw from a generator). Node may not be installed; python3 is.

## Inputs for game <slug>
- The page: games/<slug>/index.html (and any other file in games/<slug>/). This is what is served.
- The extracted bank (what the live page held after its script ran): data/banks/<slug>.json. For a "generator"
  game it is empty: read the generator code instead and work out every template and enough draws to cover each one.
- The game's verifier: scripts/verify-<slug>.py. Skim it so you know what values it already recomputes. A value it
  already checks is not your concern; MEANING is.
- Existing findings: docs/audits/findings/<slug>.yml. Do not re-report an entry already there (open, fixed or
  ruled), but you may say "already recorded as <id>".

## What to read
Every item as a student sees it: stem, every option, the key, hints, worked steps / explanations, feedback text,
the start screen's instructions. For each item ask:
a. **True wrong option / second correct answer (SR-16, SR-24).** Is an option marked wrong actually a true statement,
   or a second correct answer to the question as written? (A worded option that is true; an equivalent form the stem
   does not exclude; a counterexample that refutes only a softer statement than the one written.)
b. **Unstated convention (SR-1, SR-17).** Does the key depend on a convention, precision, rounding, form or
   assumption that the question does not state? Examples: quartile method; rounding / number of d.p. or s.f. (SR-1:
   a non-exact typed answer must state its precision; multiple-choice answers state their precision too); range of an
   angle; g; "simplify" without naming the form; a positive square root taken silently; whether 1 is prime; whether 0
   counts; inclusive/exclusive boundaries; wheel type; which way a ratio is written. **Not a finding (SR-28):**
   algebraic terms divide as a whole (6x^7 ÷ 2x^2 divides by 2x^2).
c. **Words, figure and key agree (SR-6, SR-25)**, where the verifier does not already assert it. A drawn figure,
   grid, number line, label or diagram that disagrees with the text or the key.
d. **SR-14 sensitive content** in student-facing text: banned everywhere: death, fatal outcomes, suicide, self-harm,
   abuse, drowning, violence, family breakdown. Banned in jokes/humour: those plus illness and injury. Neutral
   exam-style medical contexts are fine. Idioms are fine.

Also note (briefly) any outright WRONG key or wrong explanation figure you happen to see.

**Two more things to report (Jon, 13 Oct 2026):**
e. **Verifier gap.** Does scripts/verify-<slug>.py recompute the game's worked steps, hints, explanations and feedback
   figures (not just the keys)? Name each student-facing explanation / hint / worked-step / feedback text the verifier
   does NOT check (file:line). If the game shows none, say so.
g. **"Estimate" stems (Jon, 13 Oct 2026).** A stem that says "Estimate X" must state an estimation method (SR-12) or
   say "use the model to estimate". A plain "Estimate X to n s.f." (or to n d.p.) with a calculator is a finding: list
   each (file:line, the stem). It is fixed by rewording to "Use the model to calculate X" (keys unchanged).
h. **Contexts make sense at their values.** Every scenario's context is physically possible at the values shown
   (no 240% efficiency, no negative mass, no probability above 1). List any that is not.
f. **Negative typed answers.** Any typed-answer box with inputmode="decimal" (iOS's decimal pad has no minus key):
   can any of its answers be negative? Count them (file:line, how many of how many).

## Standing rulings that already decide things (do not report these as open questions)
- SR-4: distractors come from nameable student errors; four distinct options; none equal in value to the key unless
  the ask names the form that tells them apart.
- SR-16: a true statement is never a wrong option; an option with the right value by a wrong method names the fault.
- SR-17: conventions and precision are stated in the question (list above).
- SR-18: Probability Paradox states assumptions; Word Problem Decoder accepts both categories where both fit; Spot the
  Error: a strategy choice is not an error; Truth Buster statements are worded so the key holds as written.
- SR-12: estimation questions are marked by the stated method.
- SR-13: move-based equation games accept any valid move.

## Severity
- HIGH: a student answering correctly is marked wrong, or a wrong answer is marked right.
- MEDIUM: an unstated convention, or a misleading option that does not change the marking.
- LOW: wording.
Be precise and honest. Do not pad. "No findings" is a perfectly good answer when it is true. False positives cost
time: before reporting, check the item really reads the way you claim as served (e.g. check that the stem really
lacks the precision statement — it may be in the start screen, a level banner, or a shared instruction line shown on
every question; if so it is stated, not a finding).

## Output (your final message)
1. One line: how many items/templates you read, per level.
2. A list of candidate findings, each with:
   - check (a/b/c/d), proposed severity, level, where (file:line and item id/index),
   - the stem, the options and the key QUOTED verbatim,
   - one-line why,
   - fix shape: (i) inside games/<slug>/ without changing the key or the stem — e.g. replace the true wrong option
     with a named error, or add a precision line the key already uses; or (ii) needs a new stem / context / a choice
     between conventions / a key change (Jon's call).
3. Any class-level observation (the same unstated convention throughout the game).
Keep it compact.
