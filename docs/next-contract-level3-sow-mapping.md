# NEXT SESSION, TASK #1 — Level 3 SOW mapping

Handed over on 2026-09-17 because the session ran out of credits. **Start here before anything else.**
Nothing in the repo is half-built — this contract has not been started.

**The scheme of work is a local `.docx`** (its path is in `CLAUDE.local.md`) — Jon supplied the path on
2026-09-17, and it was confirmed present and readable the same evening (1.8 MB, about 31,000 characters of
text). It is **EAL Level 3 Engineering, AME3-004 Engineering Mathematics** (= AMEDK3-003 under EAL's newer
standard), Tuesday/Wednesday/Thursday classes on a Level 3 engineering course. It is not in this repo, so do not expect to find it
by searching. **It is a .docx, so read it without Word:** it is a zip, and `word/document.xml` inside it
gives the text once the tags are stripped — that is how it was verified. If the file has moved, the first
STOP IF applies: ask Jon rather than guessing at a substitute.

Jon's own teaching folders (`E:\jon\_ocsw_sow`, the AME3-004 build) are not MaffsGames and are not part of
this task; use them only if Jon points at them.

The contract, as given:

---

TASK: Map Jon's Level 3 apprentice maths scheme of work against the
existing MaffsGames roster and report coverage and gaps. Read-only.

ROOT CAUSE: Jon teaches a Level 3 engineering apprentice maths scheme of
work (one- and two-step equations first, then indices). Nobody has checked
which of its topics the 93 live games and 8 escape rooms already cover, so
any new build risks duplicating something that exists.

CLASS CHECK: Not a bug. A one-off analysis task, no code changes.

EXACT CHANGE: None to the repo except the report file.
1. Read the scheme of work Jon provides, .claude/rules/game-roster.md and
   the escape-room list in docs/canon.md §11.1.
2. For each SOW topic, in SOW order, give one verdict:
   - Covered: game or room slug(s), and which level tier fits
   - Partial: it exists but lacks the right level, context or content —
     say exactly what is missing
   - Gap: nothing covers it
3. For "one-step and two-step linear equations", open
   games/equation-builder/ and every other equations game on the roster,
   and state from the files what question types and levels they actually
   contain — not what the roster says.
4. For indices, do the same for games/index-laws/.
5. Note where an escape room covers a SOW topic: comic-caper covers
   factors, primes and HCF; kiln-disaster covers multiples, LCM and order
   of operations.
6. Save as docs/level3-sow-mapping.md.
7. End the report with the gaps only, listed shortest-build-first, with a
   one-line note on whether each looks like a new game, a new level tier
   on an existing game, or a content top-up.

DO NOT TOUCH:
- Any file under games/, escape-rooms/, schools/ or the portal index.html
- The roster, canon, CLAUDE.md or any other doc except the new report
- Do not build, stub, spec or scope any new game
- Do not add level tiers, a Level 3 filter, or any portal change

SUCCESS CONDITION:
- docs/level3-sow-mapping.md exists, lists every SOW topic once with a
  verdict and named games or rooms.
- Equation Builder and Index Laws are described from the actual files.
- The gap list at the end is ordered and annotated as in step 7.

STOP IF:
- The scheme of work is missing, unreadable, or has no topic list.
- The roster disagrees with games/ (a listed game has no folder, or a
  folder is not listed). Report the mismatch; do not fix it.
- A SOW topic is too vague to judge coverage. List it as "unclear" with
  the wording, and carry on.
- Credits or context run low: save the report with the topics done so far,
  mark where it stopped, and say so. A partial mapping is useful; an
  abandoned one is not.

---

**Note for whoever picks this up:** there is an existing, separate open item in `docs/todo.md` about the
spec map ("store spec references as data and generate the page, and who maps the 24 missing games").
This contract is not that job and must not turn into it — the output is one report file.
