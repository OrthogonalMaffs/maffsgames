# GATE-WARN-THEN-ENFORCE step 4: spec (from Mon 2 Nov 2026)

## Jon's ruling (27 Oct 2026, 20:14, relayed), verbatim

> Per Jon's 20:14 ruling (infrastructure freeze until Mon 2 Nov): merge steps 1 and 3 only. If step 2 or 5 is already merged, leave it; if not, park it on its branch. Do NOT start step 4 this week.
> Step 4 approach is approved for next week, with one addition: the gate uses a fixed default seed injected by the stub server, plus per-verifier fixed seed lists; a separate nightly, non-gating random sweep plays fresh seeds and reports any failing seed, which is then added to that verifier's fixed list. Random sampling lives only there, never in the gate. Take a Walk's Date.now seed is fixed with it.

## The approach (approved)

1. `scripts/serve-stubbed.py` (every verifier's pages come through `bc.start_stub_server`) injects a fixed default seed for
   `Math.random` into every HTML page it serves. A verifier that needs more than one session keeps a fixed list of seeds.
2. Take a Walk's session seed (`newSeed()`: `Math.random` XOR `Date.now`) is made fixed by the same change.
3. A nightly, non-gating workflow plays fresh seeds and reports each failing seed; the failing seed joins that verifier's
   fixed list. Random sampling lives only there.
4. Every listed page measurement calls `bc.wait_settled` (#583, home lane) before it reads layout.

## The audit (27 Oct 2026, main 2171fc0; 181 gating scripts read; spot-checked)

Source: read-only sweep of 181 gating scripts; spot-checked: bank_common.py has no settle helper; every browser verifier serves through bc.start_stub_server.
A = random draw decides the verdict; B = layout measured without fonts.ready / settle.
A+B (random session, then fold/sideways): hc-factor 568-584,648; its-on-sale 349-384; i-found-a-mark 436-466; y-so-steep 434-458,500; who-ate-all-the-pies 394-405,457; take-a-walk 675,739 (newSeed = Math.random ^ Date.now); squared-squirrel 683,486-488,549,598 (stage 2+); how-many-parts 1488-1501 (phone pass seeded mulberry32(1)); the-6-ps 1112-1127 (phone feedback; #588 fixed its driver bug).
A only: the-6-ps 427-466 (10,000 plans, 4.5-sigma), 500-515, 722-760/569-610/703-713 (session; play_bank_first retries 25), 946/1014; check-site 799-884,1171-1275 (tier 1 + level_controls on real Math.random; cache-buster randint harmless); modular-battle 40-46,170-178 (20,000 draws, negligible); estimation-engine 336-349; screening-room 446-466; free-daily-pizza 981-1014; unsure: matrix-crunch 94/110, bearing-blitz 107, new-shapes 244.
B only: the-6-ps 521-524,882-885; estimation-engine 396-399; screening-room 427-433; free-daily-pizza 1230-1273; check-answer-count 151-305; check-burst 166-168,238-243; check-keypad 58-69,167,217,236-239; test-calculator-js 142-146,434-440,491-495; test-escape-credit 46-52; test-escape-dial 63-86; test-escape-rating 43; test-fact-monty 62-70; test-next-control 168; verify-comic-caper 54-60; correlation-or-coincidence 234-240,302-308; decimal-detective 221-224,365,407; negative-number-line 241-244; force-resolver 446-514; moments-master 351-419; linear-equation-solver 593,607,706,846; eigenvector-engine 332-347; factor-theorem 1158-1252; truth-will-set-you-free 296; truth-buster 442,488; core-maths-paper1 681,778; probability-paradox 463; just-pythag-it-bruv 1282-1475 (partial).
Clean: seeded (check-answer-lock, check-money, trig-wars, split-it, expected-damage, test-the-claim, gen-six-ps, equation-builder, unit-converter); settled (simultaneous-solver, test-mathtext, test-real-fonts); static checks.
