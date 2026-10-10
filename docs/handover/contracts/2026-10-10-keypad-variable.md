CONTRACT: KEYPAD-VARIABLE (Project Claude for Jon, 10 Oct 2026, 10:20). HOME LANE (engine.js).
Queue: after ART-PENDING. Save verbatim under docs/handover/contracts/ when it starts.

======================================================================
TASK (KEYPAD-VARIABLE): Give the escape-room keypad an optional
"up to N digits" mode, entered with a Set key, so a lock can take an
answer with fewer digits than the keypad's maximum without padding,
leaving every existing keypad lock exactly as it is.

ROOT CAUSE: the engine's keypad takes exactly its declared number of
digits (a three-digit keypad needs 060 for 60). Found in two drafts on
10 Oct (cloud lane): The Rightful King's passcode (answers 24 to 504)
and the Library's fines lock (answer up to £99, misconception up to
9900). A fixed four-digit keypad's four empty slots steer a student
towards the four-digit misconception; a fixed two-digit keypad turns
5400 into 54 and marks the misconception right.

CLASS CHECK: Yes, a class: a limit in shared code (engine.js keypad)
blocking locks in two rooms, and every future lock whose answers vary in
length. Fix it once in the engine as an opt-in instrument option. Do not
pad answers, split locks, or redesign the maths around the limit.

EXACT CHANGE:
1. escape-rooms/assets/engine.js: keypad instrument accepts
   `maxDigits: N` (instead of the fixed length). In that mode the display
   shows the digits typed so far with no empty placeholder slots, a
   delete key works as now, and a Set key submits whatever has been
   typed (1 to N digits; Set with nothing typed does nothing). Leading
   zeros are not accepted. A keypad without `maxDigits` behaves exactly
   as now, key for key.
2. The typed fallback (canon: every instrument has one) accepts 1 to N
   digits in maxDigits mode.
3. escape-rooms/assets/teacher.js: shows the answer as entered (no
   padding) for maxDigits locks.
4. scripts/check-escape-rooms.py and gen-escape-variants.py: in
   maxDigits mode an answer is settable if it has 1 to N digits and no
   leading zero; the misconception must also be settable (so a four-digit
   misconception needs maxDigits ≥ 4). Fixed-length behaviour unchanged.
5. A browser test on a fixture lock (not a live room): maxDigits 4,
   answer 54 — typing 5,4,Set opens; typing 5,4,0,0,Set triggers the
   named misconception response; the display never shows empty slots.
   Plant: the old fixed-length rule; the test must fail.
6. Handover and canon §11: document the option ("up to N digits, Set to
   submit"), and note the two drafts waiting on it.

DO NOT TOUCH: any live room's room.js or variants; fixed-length keypad
behaviour; the dial, slider and pair instruments; save state (no SAVE_V
bump unless the keypad state shape must change — then STOP).

SUCCESS CONDITION: every live room plays exactly as before (all eight
checked); check-escape-rooms passes; the fixture test passes and its
plant fails; merged on a green Gate; the Rightful King and Library
drafts can use maxDigits in phase 2.

STOP IF: the change needs a SAVE_V bump; a live room's keypad behaviour
changes in any way; the typed fallback cannot share the rule.
