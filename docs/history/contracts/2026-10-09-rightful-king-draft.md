CONTRACT: RIGHTFUL-KING-DRAFT (Project Claude for Jon, 9 Oct 2026, 18:10). Phase 1 of the
replacement for the withdrawn it-vengeance room: draft only. Either lane may take it (it
touches no live file). Save verbatim under docs/handover/contracts/ when it starts.

======================================================================
TASK (RIGHTFUL-KING-DRAFT): Draft every piece of prose for the new
escape room "The Rightful King", which replaces it-vengeance, plus the
variant parameters for its three locks, into one review file for Jon.
Change no live file.

ROOT CAUSE: it-vengeance was withdrawn on 8 Sep 2026 awaiting its
voice rewrite (canon §11.5). Its premise (an IT teacher's revenge on
the gymnastics team) had no named character, its locks (vaulting
horse, mats) sat in a gym, and two of its three locks are being
replaced: the vault's peak heights (1.7–4.2 m) are not physical, and
the passcode lock (n! ÷ a!b!, arrangements with repeated letters) is
not on the GCSE specifications and has only two variants. Jon has given
a new premise and character in interview
(claude/it-room-brief-2026-10-09.md; summarised below). Canon §11.5:
Jon reviews the draft before any file is touched.

CLASS CHECK: Not a bug: content work under the existing voice-rewrite
process. The voice contract (docs/escape-room-voice-contract.md), the
working doc (docs/escape-room-voice-rewrite.md, read first), the
reference room (escape-rooms/hamster-heist/room.js) and, for a room
with an ally and a countdown instead of an antagonist,
escape-rooms/kiln-disaster/room.js (voice-rewrite §5i) govern it. No
shared code.

THE BRIEF (Jon, 9 Oct 2026):
- Title: "The Rightful King" (Jon, 18:06). New slug to be decided in
  phase 2; propose one (e.g. rightful-king) in the draft.
- Same school (St Martha's), a few days before the Prom Budget night.
  Read prom-budget/room.js first; nothing in it may be contradicted.
- The year group has voted online for prom king. The system was built
  by Mr Brian Narry, the IT teacher, with an AI and this prompt, quoted
  verbatim in the room: "Make sure the voting screen looks amazing,
  like a proper pop-concert stage with neon and sparkles, concentrate
  on aesthetics over all other considerations." No brand or franchise
  name anywhere.
- The AI did exactly what it was asked. Security was not a
  consideration, so the ballot is not secret: anyone who knows where to
  look can see who voted for whom. A bully in the year (never named,
  never on stage, never described in a way that identifies a real
  type of student for mockery) knew where to look. People voted for
  him out of fear. The kindest boy in the year would have won a free
  vote.
- The students NEVER change a vote. They close the leak, prove the
  ballot is secret again, and get a fresh vote opened before the
  result is announced. The kind boy wins because people are free to
  vote for him. (Jon's ruling after discussion; do not soften it into
  "fixing the count".)
- Mr Brian Narry is an ALLY. He loves his job and the students. He has
  realised his mistake and asks the players to help him put it right.
  His flaw: he lets AI do his thinking instead of using it as a tool.
  The joke lands on his woolly prompt, never on AI itself (this site is
  built with AI). The room's lesson: AI is a tool for learning, not a
  replacement for your own thinking.
- His opening line (Jon's, verbatim): "You have to help me, my coding
  had a bug, and it's about to be unrecoverable." It is deliberately
  wrong twice: it was not his coding, and it was not a bug. By the win
  he says "my prompt". Jon confirmed this arc; the win is written
  around it.
- Wrong-entry lines: Narry's reactions, escalating. He reaches to ask
  the AI, then stops himself. Never mocking the students.
- No picture of him; pictures are empty of people. Kindly in prose
  only.
- Pressure: the countdown to the announcement (Kiln Disaster
  precedent; no antagonist on stage).
- Fail: the announcement goes out and the bully is crowned on a
  frightened vote. Win: the ballot is secret, the fresh vote runs, the
  kind boy wins on genuine votes, and Narry owns it as his prompt.
- Rated ★★★ Challenge (grades 6–9).

EXACT CHANGE:
1. Write docs/escape-room-drafts/rightful-king-draft.md (a new file,
   not served) containing, in the order room.js uses them: title,
   hook, brief, stakes, win, fail; the wrongLines (four, escalating, in
   Narry's voice); eight objects (name, where, and clue or flavour: six
   clues and at least two blanks), each clue written with {{key.token}}
   placeholders, never figures; for each lock: name, brief, instrument
   label and verb, the three-step hint ladder, missTitle, missSays and
   solve text; the three picture alts (scene, fail, win: empty of
   people, no lettering); the hub card line and the meta description;
   one line for the teacher page saying the room is about using AI as
   a tool, for lecturers who want to discuss it.
2. Locks, with variant parameters proposed for gen-escape-variants.py
   (propose only; list every set in the draft):
   - Lock 1, the passcode (REBUILD, Jon approved 18:06): product rule
     for counting, no key used twice. Narry's admin passcode is L
     different keys from a pad of k keys; the brute-force guard opens
     only when told exactly how many passcodes it would have to try.
     Answer k × (k−1) × … (L factors). Misconception: repeats allowed,
     k^L. Example sets: k=5, L=3 → 60 (miss 125); k=6, L=3 → 120 (miss
     216); k=4, L=3 → 24 (miss 64); k=7, L=2 → 42 (miss 49).
     Instrument: keypad (three digits), not a 1–100 dial.
   - Lock 2, the overwrite (exponential decay by iteration, grade 7):
     the vote log is being overwritten, r% of the remaining original
     records each minute. How many whole minutes until fewer than a
     fraction f survive (½ or ¼)? Answer: smallest n with
     (1 − r/100)^n < f. Named misconception: linear,
     ⌈(1 − f) × 100 ÷ r⌉. Verified sets (r, f → answer, miss): 20, ½ →
     4, 3; 10, ½ → 7, 5; 15, ½ → 5, 4; 25, ½ → 3, 2; 20, ¼ → 7, 4; 15,
     ¼ → 9, 5; 25, ¼ → 5, 3; 30, ¼ → 4, 3. Reject answer = miss (r ≥ 30
     with f = ½ collide), any exact hit (1 − r/100)^n = f, and answers
     of 2 or less. Instrument: short dial (1–20) or keypad.
   - Lock 3, the audit (Venn diagram, conditional probability, grade
     7–8): N voters, V voted for the bully, S saw the leak page, and a
     number who did neither. Find P(voted for him | saw the leak) as a
     percentage. Both = V + S − (N − neither); answer = 100 × both ÷ S.
     Named misconception: dividing by everyone, 100 × both ÷ N.
     Verified sets (N, V, S, neither → both, answer, miss): 120, 50,
     40, 60 → 30, 75, 25; 200, 90, 60, 80 → 30, 50, 15; 150, 70, 50,
     60 → 30, 60, 20. Require whole-number answer AND misconception
     (reject e.g. 160, 60, 40, 80 → miss 12.5). Instrument: two-digit
     keypad (Kiln Disaster precedent).
   Check every proposed set against the joint-draw rules (canon §11.3:
   no shared clue figures, answers, or answer = another lock's
   misconception) and report the expected VALID count; the checker
   fails a room under 20.
3. Run the prose against the voice contract's checklist and the room
   rules in the working doc, and list each rule with pass/fail at the
   end of the draft.
4. Open a PR with the draft file only, and record it in the handover:
   "Rightful King draft for Jon's review". Merge it on a green Gate (it
   changes nothing served).

DO NOT TOUCH: escape-rooms/it-vengeance/ (room.js, index.html,
teacher.html); the hub; the front page; the sitemap; docs/art/ (all
three pictures are new and are made after the room is built — Jon,
18:06; write no art prompts now); gen-escape-variants.py (propose
parameters only); every other room.

SUCCESS CONDITION: the draft file exists, with every slot room.js
needs; no figure appears in the prose outside {{tokens}} (Narry's
quoted prompt contains none); the three locks' parameter sets are
listed and checked; the checklist is all pass, or each fail is
explained; Jon has it to review. Phase 2 (slug, build, variants,
teacher page, retiring the old six pictures, release) and phase 3
(art) are separate contracts after Jon approves the draft.

STOP IF: the brief contradicts the voice contract or a room rule in a
way the draft cannot resolve (quote both); any lock cannot be given
exactly one settable answer on its instrument; the joint draw gives
fewer than 20 VALID combinations; anything in prom-budget contradicts
the premise.
