# The IT room: rewrite brief (from Jon's interview, 9 Oct 2026)

Status: DRAFT for Jon's review. Canon §11.5 applies: the premise and character come from
Jon; a lane writes the prose from this brief; Jon reviews the draft before any file is
touched. **This replaces the room's premise entirely.** The old gym-hall vengeance room,
its vault and mat locks, and its six pictures are retired. Slug `it-vengeance` is kept
for now; a title and slug change is an open item below.

## The premise
A few days before the prom (the same school year as Prom Budget, earlier in the week; no
conflict, as Prom Budget never mentions a vote, a king or IT). The year group has voted
for prom king online. The system was built by **Mr Brian Narry**, the IT teacher.

Narry asked an AI to build the voting screen with this prompt, quoted verbatim in the room:

> "Make sure the voting screen looks amazing, like a proper pop-concert stage with neon and
> sparkles, concentrate on aesthetics over all other considerations."

(Jon's original named a film franchise; replaced on brand/IP grounds per canon §11.1. Jon
accepted the generic wording.)

**The AI did exactly what it was asked.** Security was not a consideration, so the ballot
is not secret: anyone who knows where to look can see who voted for whom. A bully in the
year (never named, never on stage) knew where to look. People voted for him out of fear,
and he is about to be announced prom king. The kindest boy in the year would have won a
free vote.

## The students' job (the ethical line, settled in interview)
The students **do not change any votes.** They close the leak, prove the ballot is secret
again, and get a fresh vote opened before the result is announced. The kind boy wins
because people are free to vote for him. Every vote counted at the end is genuine.
(Jon proposed moving the votes across; Project Claude argued that is overriding everyone's
choice, including genuine voters', and teaches "if the result is wrong, change it"; Jon
accepted the secret-ballot version.)

## Mr Brian Narry (character sheet)
- **Ally, not antagonist.** He loves his job and the students. He has realised his mistake
  and asks the players to help him put it right before it is too late.
- **The flaw:** he lets AI do his thinking instead of using it as a tool. Vague prompts,
  proud of them. The room's lesson: AI as a tool for education, not a replacement for
  your own brain doing some work. **The joke lands on the woolly prompt, never on AI
  itself** — this site is built with AI.
- **His opening line (Jon's, verbatim):** "You have to help me, my coding had a bug, and
  it's about to be unrecoverable."
  It is wrong twice, deliberately (Jon confirmed): it was not his coding, and it was not a
  bug. The code did what the prompt said.
- **The arc:** he comes in saying "my coding had a bug"; by the win he says "my prompt".
  That turn is the room's moral and the win slot is written around it.
- **Wrong-entry lines** are his reactions: he reaches to ask the AI, then stops himself.
  Escalating; never mocking the students. (Extrapolated by Project Claude; Jon to strike
  if unwanted.)
- **No picture of him.** House rule: pictures are empty of people. Kindly in prose only.
  The existing `cast-it-teacher.webp` (smug, arms folded) is not used.

## Present and beatable (canon's rule)
No antagonist on stage, by design: Narry is an ally and the bully is offstage. The
pressure is the **countdown to the announcement**, as in Kiln Disaster (precedent, voice
rewrite §5i). It reaches the students during play.

## The three locks (target ★★★ Challenge, grades 6–9; Jon ruled it stays ★★★)
Maths verified by Project Claude; the generator must enforce every constraint listed.

1. **The passcode (product rule, grade 6–7). PENDING JON'S RULING.** The current lock
   (arrangements with repeated letters, n! ÷ a!b!) is **not on the GCSE specifications**
   — AQA/Edexcel/OCR Higher cover listing and the product rule, not permutations of
   repeated objects — and has only two variants. Proposed rebuild: Narry's admin passcode
   is L different keys from a pad of k keys, **no key used twice**. The brute-force guard
   opens only when told exactly how many passcodes it would have to try.
   - Answer k × (k−1) × … (L factors). Misconception: repeats allowed, k^L.
   - Variants, e.g. k=5, L=3 → 60 (miss 125); k=6, L=3 → 120 (miss 216); k=4, L=3 → 24
     (miss 64); k=7, L=2 → 42 (miss 49).
   - Instrument: **keypad** (three digits), not a 1–100 dial — the dial is what stranded a
     Rugby Mud group.
2. **The overwrite (exponential decay by iteration, grade 7). Jon approved.** "About to be
   unrecoverable": the vote log is being overwritten, r% of the remaining original records
   each minute. How many whole minutes until fewer than half (or a quarter) survive? After
   that, the genuine votes cannot be recovered for the audit.
   - Answer: smallest n with (1 − r/100)^n < f. Misconception (named): linear,
     ⌈(1 − f) × 100 ÷ r⌉.
   - Verified sets (r, f → answer, miss): 20, ½ → 4, 3; 10, ½ → 7, 5; 15, ½ → 5, 4;
     25, ½ → 3, 2; 20, ¼ → 7, 4; 15, ¼ → 9, 5; 25, ¼ → 5, 3; 30, ¼ → 4, 3.
   - **Generator must reject** answer = miss (r ≥ 30 with f = ½ all collide), any r, f
     where (1 − r/100)^n equals f exactly, and answers of 2 or less.
   - Instrument: dial with a short travel (1–20) or a keypad.
3. **The audit (Venn diagram and conditional probability, grade 7–8). Jon approved.** The
   re-vote opens only once the audit shows the leak changed the result. From the clues: N
   voters, V voted for the bully, S saw the leak page, and some number voted for him
   without ever seeing it (or "neither"). Find P(voted for him | saw the leak) as a
   percentage.
   - B = V + S − (N − neither); answer = 100B ÷ S. Misconception (named): the wrong
     denominator, 100B ÷ N.
   - Verified sets (N, V, S, neither → both, answer, miss): 120, 50, 40, 60 → 30, 75, 25;
     200, 90, 60, 80 → 30, 50, 15; 150, 70, 50, 60 → 30, 60, 20.
   - **Generator must require** integer answer and integer misconception (160, 60, 40, 80
     gives a 12.5 misconception: reject).
   - Instrument: two-digit keypad (Kiln Disaster has the precedent).
   - Why this lock: it asks who was actually frightened, which is the question the
     students were tempted to skip. The maths is the ethics.

## Stakes, win and fail
- **Fail (time runs out):** the announcement goes out and the bully is crowned on a
  frightened vote. The failure picture shows the result, with no people and no lettering
  (draft for the lane; Jon to review).
- **Win:** the ballot is secret again, the re-vote runs, and the kind boy wins on genuine
  votes. Narry's last line owns it: "my prompt", not "my bug".

## For the build
- **Art:** all three pictures new (scene, fail, win), on the three-picture model, empty of
  people and lettering. Suggested scene: the IT suite or server cupboard, the voting
  screen glowing in neon and sparkles. Jon runs the prompts.
- **Retire** the six old pictures from the room (keep the files; canon decides deletion).
- **Teacher page:** add a note that the room is about using AI as a tool, for lecturers
  who want to discuss it.
- Same school (St Martha's), no year, no brands, British English.

## Open for Jon
1. Passcode rebuild on the product rule: yes or no.
2. Title and slug: "The IT Teacher's Vengeance" no longer describes the room. A new title
   (and whether to change the slug, which breaks any shared link to the withdrawn room —
   it is noindex, so the cost is small).
3. The fail picture's content.
