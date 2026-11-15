CONTENT-SAFETY-COVERAGE (Project Claude, Sat 14 Nov 2026 23:05; re-checked against main 7b00e6c at 20:30 on 15 Nov; Jon 22:46 "do them in numerical order please" (this is 3 of 3))
Recommended: Sonnet, effort medium: one check's file selection, inverted from a hand list to everything published, with a guard and plants.
LANE: cloud (todo row 52: "whichever lane next touches the content-safety check"; scripts/check-content-safety.py is not a Gate file). TIER: Medium (merge on green; Project Claude reviews after merge). START: now. This task's first commit is ESSENTIALS-PHONE-FIT-PAIR's close-out (the standing rule: PR 1 #788 6065fb6, check-site 43751842791 + phone-fit-full 43751842703; PR 2 #790 984851c, check-site 43755895132 + phone-fit-full 43755894977; all green; contract to history). One PR. Branch from current origin/main.
MERGE: on a green Gate, by merge-pr.py or, when gh auth fails, the 10 Nov 2026 GitHub-connection route; before merging, main's latest full run green with only bot commits after it.

JON'S RULING (verbatim in the PR body): 14 Nov 22:46: "do them in numerical order please" (item 3 of 3: the SR-14 scan reads the Ugh, stats pages).

TASK: Make the SR-14 content-safety scan read every published page, the six /ugh-stats/ pages included, so that a section added later cannot fall outside it.

ROOT CAUSE: scripts/check-content-safety.py reads only the folders in its hand-written GLOBS (:57-64). /ugh-stats/ (six pages, added 14 Nov) is not on it, so SR-14 has never been checked there (todo row 52, CONTENT-SAFETY-UGH-STATS). printables/ was added to the list by hand on 15 Nov, the same pattern. Project Claude ran the scan's own displayed() and hits_in() over the six /ugh-stats/ pages on 14 Nov 2026 (main c0cec86): no hits. schools/assets/ugh-stats.js is already read, via "schools/assets/*.js".

CLASS CHECK: A class within this check. The bug is not the missing folder; it is a hand list that every new section falls out of until someone notices (ugh-stats missed; printables added by hand). Adding "ugh-stats/**/*.html" would leave the next section exposed the same way. SR-14 is site-wide (the comment at :58-60, LISTINGS-AND-GATE part B, 13 Oct 2026), so the check selects every published page and excludes by name, and a guard fails on a folder it has not been told about. The other checks with folder lists (check-student-labels.py PORTALS and SURFACES; check-money.py GLOBS) are scoped by their own canon rules to games, rooms and portals, so they are not this bug, and they are not changed.

EXACT CHANGE:
1. Replace GLOBS with: every *.html and *.js under the repo root, minus a named EXCLUDE list of folders that hold no published page (start from docs/, scripts/, data/, tools/, firebase/, .github/, .claude/; add any other you find, each with a one-line reason). Games and escape rooms are still read first; each file is read once; displayed() and hits_in() are unchanged.
2. A guard: a top-level folder holding any .html that is neither read nor in EXCLUDE fails the check, naming the folder and saying to read it or exclude it with a reason.
3. --selftest plants: a tier (a) word in a planted /ugh-stats/ page is caught; a new top-level folder with an .html file, in neither list, fails the guard; the tree as it is passes.
4. Run the widened check on the tree and report how many files it reads before and after, and which folders are new to it.
5. todo row 52 closed; docs/handover/cloud.md entry; no /updates/ line (a check, not a feature).
DO NOT TOUCH: TIER_A, TIER_B, ALLOW, KNOWN, HUMOUR_KEYS, CODE_ATTRS and displayed(); the Ugh, stats pages and every other page's wording; the other checks; the workflow line for this check; Gate files.
SUCCESS CONDITION: ESSENTIALS-PHONE-FIT-PAIR's close-out is in the first commit; the check reads all six /ugh-stats/ pages and every other published page; the guard fails a planted unlisted folder; the selftest plants are caught and the tree passes; the file counts and the new folders are reported in the PR body; Gate green; merged; main's check-site and phone-fit-full green on the merge commit and reported; cloud.md and todo row 52 updated.
STOP IF: the wider read finds any hit, in /ugh-stats/ or in any page not read before (report each with its line for Jon's ruling; do not reword, allowlist or add to KNOWN); it is unclear whether a folder is published; the check's run time rises enough that the timing report warns on its group; the change would need the workflow or another Gate file edited.

---

AMENDMENT 1 (Project Claude, 15 Nov 2026 20:45; Jon's ruling, given in answer to the cloud lane's stop on PR #792's red Plan job):

CONTENT-SAFETY-COVERAGE: follow-up from Project Claude, 15 Nov 2026 20:45. Jon's ruling: yes to route 1 (fix ci-deps.py, the class fix), in this PR (#792). This lifts the STOP IF on editing a Gate file for scripts/ci-deps.py only; the workflow and every other Gate file stay untouched.

Why: the same bug shape as LINE-LIMIT-SCOPE (21 Oct 2026, ci-deps.py:17-19): an imported module's string literals become false dependencies of every verifier that loads it. Now: verify-correlation-or-coincidence.py imports check-content-safety.py, which imports check-publish-scope.py, whose SITE literals (docs/art/ among them) make a docs-only change select that verifier.

Do:
1. scripts/ci-deps.py: when following a verifier's local imports, a module that is a site-wide check (a scripts/check-*.py that is not itself a content verifier) contributes its own file, and the files of modules it imports, as dependencies, but NOT its string-literal paths, its game slugs or its fixtures. The verifier's own literals and its "# ci-deps:" header are unchanged. Update the docstring's dependency list to say so, citing this PR beside LINE-LIMIT-SCOPE.
2. --selftest proofs, all run on the real tree: (a) a docs-only change (e.g. docs/todo.md, docs/art/<any file>) selects no content verifier it did not select on main; (b) a change to scripts/check-content-safety.py selects verify-correlation-or-coincidence.py; (c) a change to scripts/check-publish-scope.py selects it too; (d) a change to games/correlation-or-coincidence/index.html selects it. Plant a fault (drop the new rule) and show (a) fails.
3. Run ci-deps.py --explain before and after; in the PR body, list every verifier whose dependency set changed and confirm each lost only literals of an imported site-wide check, never its own pages or its game.
Then: Gate green, merge as the contract says, report main's check-site and phone-fit-full on the merge commit, cloud.md updated (record the rule beside LINE-LIMIT-SCOPE).
STOP IF: any verifier loses a dependency on its own game folder, a page it tests or a shared asset that page loads; the rule cannot be stated without a hand list of module names; any other Gate file would need changing.
