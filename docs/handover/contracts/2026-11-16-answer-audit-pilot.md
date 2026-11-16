TOOL: Claude Code (cloud lane; same session that stopped). SIZE: medium (one new script with a field map for 21 games, its self-test, one todo row; no game changes). Recommended: Opus, high effort.
MERGE TIMING: one merge heading for main at a time; if PE-SHED-PACK (#801, home lane) is in its Gate wait when yours is green, wait for it to merge, rebase, then merge.
REISSUE: replaces ANSWER-AUDIT-SCRIPT in full. Jon, 16 Nov 19:52: "yes please. these credits are to play with, if we can get some tangible benefit so much the better" (to: pilot on the clean games, field map in the script, diagram questions excluded, Sonnet first pass with Opus re-solving only disagreements).

TASK: Write scripts/audit-answers.py, a pilot independent answer audit of the 21 games whose extracted banks hold a clean question and answer: Claude solves each question without seeing the key, and every disagreement is reported for Project Claude and Jon to triage. Jon runs it on his own PC with his monthly API credit ($100, expires 6 Dec 2026); it never runs in CI.

ROOT CAUSE: Correctness on live games is priority 1 (canon §0.2), but each game's answers are checked only by its own verifier, written alongside the bank. Your STOP (19:51) established that scripts/extract-banks.py writes each game's source data, not the student's screen: of 109 files and 12,517 questions, only 21 games (3,073 questions) carry both a question-text field and an answer field; field names differ per game; many banks carry answer-revealing fields (steps, working, worked, sol, explanation, misconception, revealText, hint); and some questions depend on a figure the model would not see. A library-wide generic script is therefore not possible without per-game knowledge, and a full Opus run (~$200) exceeds the credit.

CLASS CHECK: Not a bug fix; a one-off measuring tool, piloted. The per-game knowledge lives in ONE place, a declared FIELD_MAP inside the script, one entry per game, so nothing about the audit is scattered through game pages. If the pilot finds real errors, a later contract (Jon's decision) moves the declarations into the games themselves and widens coverage. No game, shared asset or verifier changes now.

EXACT CHANGE:
First commit: BEARING-BLITZ-GOAT's close-out: #800 merged as 5a82f36 via merge-pr.py, last line "main 5a82f36 run 43938279199: GREEN", exit 0; check-site 43938279199 success; phone-fit-full 43938279490 success. Move its contract to docs/history/contracts/. Save this contract verbatim at docs/handover/contracts/2026-11-16-answer-audit-pilot.md.

1. scripts/audit-answers.py:
   - FIELD_MAP: for each of the 21 clean games you classified, the fields that make the question text as the student reads it (e.g. q + ask, stem + stemAfterTable), the options field if MC, the answer field (correct / answer / acceptedAnswer), and the fields to STRIP because they reveal the answer. A game not in FIELD_MAP is never sent. List the 21 slugs and their question counts in the docstring.
   - Figures: any question that carries a figure/diagram field (fig, svg, curve, chart, image or similar per FIELD_MAP) is EXCLUDED and listed in the report as "not audited: needs its figure", never sent.
   - Input: data/banks/<slug>.json from extract-banks.py (run it first if missing; say so). --game <slug> (repeatable) limits the run.
   - Prompt: question text, options if MC, level; never the key or a stripped field. Ask for the final answer in a fixed, machine-readable form with brief working.
   - Pass 1: every question, model claude-sonnet-5-5, via the Message Batches API (custom_id "<slug>|<level>|<index>"); poll, download; --batch-id resumes.
   - Compare with the key: exact for MC by option value; numeric within the question's stated precision; otherwise normalised string. Unclear → UNCLEAR, never agreement.
   - Pass 2: only DISAGREE and UNCLEAR items from pass 1, re-solved by claude-opus-5-5 in a second batch. Final status per item: AGREE (pass 1 agreed), RESOLVED (Opus agrees with the key), DISAGREE (Opus also disagrees), UNCLEAR.
   - Budget: --dry-run builds every request, prints per-game counts and an estimated cost for pass 1 plus a worst-case pass 2, sends nothing. A real run refuses to start if the estimate exceeds --max-usd (default 50).
   - API key: read ONLY from --key-file (default ~/.config/maffs/anthropic-audit-key), refuse unless mode 600. Never read ANTHROPIC_API_KEY, never print, log or write the key.
   - Output: docs/audits/answer-audit-<date>.md (not committed by this task): per game, counts (sent, excluded for figure, agree, resolved, disagree, unclear, error) and a table of every DISAGREE and UNCLEAR with slug, level, index, question text, game key, both models' answers and Opus's working; plus actual tokens and cost per pass from the API's usage figures. Raw results to data/audit/ (add to .gitignore).
2. --selftest, no network: planted cases: correct item (agree); wrong key (disagree); numeric equal within precision (agree); precision mismatch (disagree); unparseable reply (unclear); a figure question (excluded, never sent); a request containing the key or a stripped field (self-test must fail it); an unmapped game (never sent); loose key-file permissions (refused); an estimate over --max-usd (refused); dry-run sends nothing.
3. Docstring: how to run (dry-run, then one game, then all 21), cost, and that disagreements are leads for review, not verdicts.
4. docs/todo.md: row ANSWER-AUDIT-RUN (Jon/home: create the API key and key file, dry-run, pilot one game, run all 21; Project Claude triages; then Jon decides whether to widen via per-game declarations). Cloud handover.

Run only the checks this contract names and the Gate: --selftest and a --dry-run on all 21 games in your session (no key there, so no real call). No optional all-game local runs.

DO NOT TOUCH: any game page, bank, verifier or shared asset; scripts/extract-banks.py and bank_common (use as they are); CI workflow and Gate files (never wired into CI); tools/pack-generator/; games/bearing-blitz/; the home handover.

SUCCESS CONDITION:
- --selftest passes with every planted case as stated.
- --dry-run over the 21 games prints per-game counts, the number excluded for figures, and an estimated cost under $50, sending nothing.
- No code path reads ANTHROPIC_API_KEY or prints the key (state how checked).
- PR merged on green via `python -X utf8 scripts/merge-pr.py <n>`; report its last line and exit status, main's check-site and phone-fit-full run IDs on the merge commit, and the dry-run's totals. Cloud handover documented.

STOP IF:
- The dry-run estimate for the 21 games exceeds $50 even on Sonnet (report the figure and per-game breakdown).
- claude-sonnet-5-5 or claude-opus-5-5 or the Batch API is not available as described (report the error text).
- A clean game's question cannot be sent without an answer-revealing field even after stripping (drop it from FIELD_MAP and list it; stop only if more than 5 drop).
- merge-pr.py reports it cannot reach GitHub (a 5xx during the Gate wait may be retried once with the same script).
