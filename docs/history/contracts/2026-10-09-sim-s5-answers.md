# Answers to the SIM-S5 STOP IF and the UC-FIX questions (verbatim)

From Project Claude for Jon, pasted by Jon, 9 Oct 2026, 08:10. Saved verbatim beside `2026-10-09-sim-s5.md` as they
ask; read with that contract when SIM-S5 starts; both move to `docs/history/contracts/` when SIM-S5 merges.

```text
Answers (Project Claude for Jon, 9 Oct 2026, 08:10). Save beside the
SIM-S5 contract in docs/handover/contracts/.

1. SIM-S5: option A, a Stage 5 tile builder inside Simultaneous Solver,
   marked as a non-zero multiple of a key equation. Jon approves.
   One condition: write the builder as a self-contained block
   (its own object with build, read and mark functions, no reach into
   Stages 1-4), so it can be lifted into a shared module if a second
   game ever needs it. Record that in the PR. Carry on with SIM-S5 now;
   FT-FIX follows it as planned.

2. FT-FIX: no switch. SIM-S5 first, then FT-FIX without asking.

3. From UC-FIX:
   a. Boards: Jon checks unit_converter_* in Firebase. Nothing for you.
   b. timer-policy.md: Unit Converter moves out of "Hidden count-up"
      to "No timer". If the file is a shared rules file outside your
      lane, put the change in the handover for the home lane instead.
   c. t4-007: the prompt becomes "Convert 60 mph to m/s
      (1 mile ≈ 1609 m). Give your answer to 3 significant figures."
      The key stays 26.8 m/s: with the exact 1609.344 m it is
      26.82 m/s, still 26.8 to 3 s.f. Do it as a small PR after
      SIM-S5, close t4-007, and have the verifier allow "≈" here,
      because 1609 is a rounded value, not a definition.

4. CI timing (a fifth B group): noted for the home lane this evening.
```
