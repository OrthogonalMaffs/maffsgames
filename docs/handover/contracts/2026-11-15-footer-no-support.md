FOOTER-NO-SUPPORT (Project Claude, Sun 15 Nov 2026 18:22, re-checked against main 6065fb65 at 19:26)
Recommended: Sonnet, effort low: one entry out of the footer's canonical list, applied site-wide by the existing script.
LANE: home (scripts/check-footer.py, apply-footer.py, site-footer.css). TIER: Medium (merge on green; Project Claude reviews after merge; Jon checks the live footer on desktop and phone). START: now; this task's first commit fills in home.md's HOME-LEAN merge line (#787 merged as 4809d1a; main's check-site 43749922722 and phone-fit-full 43749922791 both success), the standing rule. Before UNLIST-GRAPH-SKETCHER. One PR. Branch from current origin/main.
MERGE: merge-pr.py on a green Gate. Pre-push by hand only (HOME-LEAN): personal-details scan, skip-CI word check, check-footer's own self-test.

JON'S RULING (verbatim in the PR body): 15 Nov 18:17: "the footer is now looking very crowded, can we remove the support maffsgames please, no one bloody uses it anyway. it's already in the about page I think, it's just taking up room at the bottom."

TASK: Remove the "Support MaffsGames" (Buy Me a Coffee) link from the site footer on every page; the About page keeps its own coffee button.

ROOT CAUSE: The footer is built from scripts/check-footer.py's CANONICAL, which appends _SUPPORT (:46-47, the buymeacoffee.com link with "&#9749; Support<span class="sf-long"> MaffsGames</span>") after the _LINKS (:33-44). With "Printable packs" added on 15 Nov the row is crowded. About already has the link as a button (about/index.html:195-197, .coffee-btn).

CLASS CHECK: Local to the shared footer's one source. The footer is never edited by hand: removing _SUPPORT from CANONICAL and running apply-footer.py changes every page identically.

EXACT CHANGE:
1. scripts/check-footer.py: remove _SUPPORT and its use in CANONICAL (:46-49), so the footer is the _LINKS joined by _SEP. Update any self-test plant or fixture expectation that includes the Support link.
2. Run scripts/apply-footer.py so every page carries the new footer; the test fixtures that hold a copy of the footer (scripts/fixtures/escape-format.html, scripts/fixtures/fraction-input.html) follow if a check requires them to match.
3. schools/assets/site-footer.css: remove the .sf-long rule (:61) and the header comment's line about it (:19), now unused; nothing else in the stylesheet changes. The row must still fit at 320 px without sideways scroll.
4. about/index.html keeps its coffee button unchanged; privacy/index.html's "Buy Me a Coffee" section (:192-193) stays, since the link is still on the site.
5. /updates/: no line (a footer tidy). home.md entry.
DO NOT TOUCH: the _LINKS and their order; the About page's button; the privacy page; every page's content except through apply-footer.py; Gate files.
SUCCESS CONDITION: no page's footer has the Support link; check-footer passes on every page with its self-test catching its plants; the footer fits at 320/375/390 px; About still shows its coffee button; Gate green; merged; main's check-site and phone-fit-full green on the merge commit and reported; home.md updated.
STOP IF: any check other than check-footer.py requires the Support link in the footer; apply-footer.py would change anything on a page other than its footer.
