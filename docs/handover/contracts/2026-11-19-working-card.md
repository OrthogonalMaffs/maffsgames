WORKING-CARD, one part.
LANE: cloud. Send now. TIER: Small. MODEL: Claude Code, Opus 5.5, medium effort (layout measured over 100 items).

TASK: Surd Simplifier's "How to get there" moves above Next as a reference card (canon 7.6.2): open where it fits, one tap away where it would push Next below the fold.

ROOT CAUSE: On main ed8590b (re-checked), #838 put the working (#working, games/surd-simplifier/index.html:137) below Next's mount (#nextMount, :136), because the longest workings, open above Next, push Next past the fold at 1280x720. Canon 7.6.1 and 7.6.2: feedback goes above Next, never below. Below it, a student sees Next first, taps it, and skips the working, which is the teaching.

CLASS CHECK: A class: three games get a wrong-answer working box (Surd now; Circle Theorem Spotter and Standard Form Blitz are queued). The shared pattern already exists: .maffs-ref in schools/assets/fold.css, two copies swapped by the page's media query (7.6.2; games/log-laws/index.html:602 loads it, :669-676 uses it). Canon 7.6.2 still names theme.css: stale, corrected here. Surd adopts it here, and the two queued contracts use it from the start. schools/assets/ is unchanged.

EXACT CHANGE:
1. First commit: close out CORE-PAPERS-SHUFFLE (#840, merge 8f5f32f, run 44597230571: read main's runs on its merge commit from the API, record them in its cloud.md entry, move its contract to docs/history/contracts/). Save this contract verbatim as docs/handover/contracts/2026-11-19-working-card.md.
2. Load /schools/assets/fold.css as log-laws does. Replace #working with a .maffs-ref-row holding two <details class="maffs-ref">, .maffs-ref-fits (open) and .maffs-ref-phone (collapsed), each with the summary "How to get there" and the working lines as its body, followed by #nextMount. The working then sits between the options and Next. showWorking() fills both copies. Tint with --ref-bg and --ref-edge only; keep the current line styles, scoped inside the card.
3. The swap is the page's own media query on viewport height, within width bands. Set the thresholds by measuring the open card for all 100 items, in normal and Aa mode, at the canon phone sizes and 1280x720. The card is open where every item's Next stays above the fold, and collapsed everywhere else. No script decides.
4. Pass keep: the shown card to MaffsNext.wrong(), so its top stays on screen.
5. canon 7.6.2: "schools/assets/theme.css" becomes "schools/assets/fold.css"; and one sentence (Jon, 19 Nov 2026): "A worked solution after a wrong answer is a reference card too: above Next, open where it fits, collapsed wherever it would push Next below the fold, the 1280 x 720 laptop included."
6. scripts/verify-surd-simplifier.py: in Chromium, on every wrong answer the working comes before Next in document order. At each measured size, Next's bottom in page coordinates (rect.bottom + scrollY) is within the fold for every item, with the card open or collapsed as the media query says. Opening the collapsed card shows every line. Plants that must FAIL: the card moved below Next; a threshold loosened so that the open card shows where it pushes Next past the fold. The SymPy checks stay unchanged.
7. measure-phone-fit.py in normal, Aa and laptop mode: no worse than main for this game. cloud.md entry. No /updates/ line.
8. PR, Gate and phone-fit-full green, then merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line. No draft PR.

DO NOT TOUCH: the 100 workings' text; every item's question, options and key; marking and scoring; schools/assets/; any other game; docs/handover/home.md.

SUCCESS CONDITION: the working sits above Next on every wrong answer, open where it fits and collapsed elsewhere, with Next inside the fold for every item at every measured size; the verifier's new checks pass and both plants fail; phone fit no worse; canon sentence in; CORE-PAPERS-SHUFFLE closed out; merged by merge-pr.py with a GREEN last line; cloud.md records it all.

STOP IF: with the card collapsed, Next is still below the fold at a size where the game fits now (report the sizes and items); .maffs-ref needs a change in fold.css to work here (report it; schools/assets/ is the home lane's); merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
END OF CONTRACT
