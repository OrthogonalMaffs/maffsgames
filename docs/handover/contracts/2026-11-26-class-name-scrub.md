CLASS-NAME-SCRUB (Project Claude, Thu 26 Nov 2026 14:48; checked against main 4b1d749)
Jon, 26 Nov 2026, 14:25: "a breach like that can and should be an exception to a rule. can we get the cloud lane to do it as a quick contract ?" (Project Claude found the real primary class's name and its class teacher's surname in the public repo.)
This contract deliberately never writes either name. Below, CLASS means the value of CLASS_NAME_EXAMPLE at scripts/check-site.py:3151 on main 4b1d749, and TEACHER means the surname of the teacher named in docs/todo.md:113 (row SOME-THINGIES-LIST). Never write either word in a commit message, PR title or description, handover, saved contract or report: write CLASS and TEACHER.
RECOMMENDED: Claude Code, Opus 5.5, effort medium. Mechanical, but every check that uses the example must still pass.
LANE: cloud, lane 3. SEND: now (#925 merged as 4b1d749). First commit carries SOME-THINGIES-FACTS's close-out (AGENTS.md:62): #925, 4b1d749, its PR runs, and main's three runs on 4b1d749, read from GitHub (the guard was still watching main's run at the merge report; if any is not success, stop and report before anything else). This jumps lane 3's queue (Jon's ruling above).
TIER: Medium (merge on green).

TASK: Remove the real primary class's name (CLASS) and its class teacher's surname (TEACHER) from every file on main, replacing them with invented examples, so the repo no longer identifies the pilot class.

ROOT CAUSE: The child look's privacy rule (contract CLASS-PAGE, 21 Nov 2026: "a real class's name never enters the repo") is defeated by its own example: the "documented example" class name, CLASS, is the real class's name. scripts/check-site.py:3148-3151 holds it as CLASS_NAME_EXAMPLE and lets it appear in comments, so the check passes the very name it exists to keep out. On main 4b1d749, CLASS appears 101 times in 16 files (class/index.html, schools/assets/kids-look.js, docs/canon.md, docs/todo.md, scripts/check-site.py, scripts/check-site-nav.py, scripts/test-kids-look.py, scripts/verify-some-thingies.py, scripts/verify-sums-in-disguise.py, scripts/ci-timings.json, and files under docs/history/). TEACHER appears in docs/todo.md:113, docs/handover/home.md:74, scripts/test-kids-look.py:106 (an apostrophe test case) and files under docs/history/. (docs/audits/served-2026-11.json holds a fictional question-bank character with the same surname: not this; leave it.)

CLASS CHECK: A class in shared infrastructure: the privacy check's own example is the leak, and every check and test that uses the example repeats it. So the fix is at the example (one invented name, used everywhere the example is used, and held by the check), not file by file.

EXACT CHANGE:
0. First commit: the close-out above. Save this contract verbatim as docs/handover/contracts/2026-11-26-class-name-scrub.md (it contains neither name).
1. Choose one invented example class name (a common UK class name, e.g. "[a tree name, removed by the implementer under Amendment 1]"; your choice, named in the report) and replace CLASS with it in every file on main, docs/history/ included, preserving meaning (the greeting "Welcome, <invented> Class!", "#kids/<invented>", "/class/#<invented>", plant names).
2. scripts/check-site.py: CLASS_NAME_EXAMPLE becomes the invented name; its comment (:3145-3150) says the example is invented, and that real names come only from MAFFS_CLASS_NAMES, which is never written in the repo.
3. Replace TEACHER: in docs/todo.md, docs/handover/home.md and docs/history/ files with "the class teacher"; in scripts/test-kids-look.py:106 the apostrophe test case uses an invented surname with an apostrophe (e.g. "D'Arcy"; your choice) so the apostrophe case is still tested.
4. scripts/ci-timings.json: let the bot's repack regenerate the plant names; hand-edit only the renamed keys and only if a check requires it.
5. After the change, git grep for CLASS as a whole word, and for TEACHER outside docs/audits/served-2026-11.json, both return nothing on the branch. Report the commands with the words replaced by CLASS and TEACHER, and their (empty) output.
6. docs/handover/cloud.md entry, written with CLASS and TEACHER. No /updates/ line.

DO NOT TOUCH:
- Git history: no rewrite, no force-push (the names remain in past commits; Jon has been told separately).
- Behaviour of the child look, the class page, MaffsKids, the greeting format, analytics, every game's bank and play.
- docs/audits/served-2026-11.json; every workflow; scripts/merge-pr.py.
- Any file not containing either name.

SUCCESS CONDITION:
- Both searches in step 5 return nothing on merged main.
- Every check and verifier that used the example passes with the invented name (check-site's class-name part, check-site-nav's class unit, test-kids-look, verify-some-thingies, verify-sums-in-disguise), and their plants still fail when planted.
- Neither name appears in the PR's title, description, commits, saved contract or cloud.md.
- Merged on green through merge-pr.py; main green after; last line and main's runs reported; cloud.md records it.

STOP IF:
- Any served page or script needs the name to work (not just a comment or test): report the file and line (writing CLASS or TEACHER) before changing it.
- A check's plant stops failing after the rename.
- main is red when you come to merge: report it; do not use --override.
- merge-pr.py cannot reach GitHub or refuses: report its output; do not merge another way.

---
Amendment 1 (Project Claude relaying Jon, 26 Nov 2026, 14:59; saved with the first invented name replaced by [NAME1], because it is the name this amendment removes): [NAME1] is also a real class name at the same school (its classes are all tree names), so it must not be used. Replace the invented class name [NAME1] with "Example" everywhere you used it (greetings read "Welcome, Example Class!", "#kids/Example", "/class/#Example", CLASS_NAME_EXAMPLE = "Example", plant names, ci-timings.json keys), and never use a tree name. Then re-run both step 5 searches plus a case-insensitive search for [NAME1], all returning nothing, and re-run test-kids-look.py. Keep "D'Arcy". Amend on the same branch; report the commit.

Amendment 2 (Jon, 26 Nov 2026, answering this lane's STOP on Amendment 1, which offered (a) keep "Example" and stop the class-name rule banning the invented example, its plant rebased on a MAFFS_CLASS_NAMES name, or (b) a made-up non-word): "you were correct to leave previous inventions, go with A"
