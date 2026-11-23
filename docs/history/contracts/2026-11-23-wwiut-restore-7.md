WWIUT-RESTORE-7. Home lane. Tier: Medium: merge on green with merge-pr.py (no hold). Send: now (23 Nov 2026, 16:30; home idle; cloud idle). Branch from origin/main (4d09d45 or later).
From Project Claude; Jon, 23 Nov 2026: 10:15 (mammographer and xG figures), 10:20 (Plus article address), 13:23 (card fields for the 7), 16:12 (mammographer asks and answers "25% is cancer"; nuclear headline gets "× 100"; GOV.UK's "people" wording; payroll keeps its sum and gains a note).
Recommended: Claude Code, Opus, medium effort. Data only, every value given below; the existing checks prove it.

TASK: Put back the 7 jobs #888 left out (their sources now answer), restore the Probability topic, and add Jon's payroll note, in "When will I use this?".

ROOT CAUSE: #888 left out 7 scenarios because their sources did not answer 200 (shown: #888's PR body). Project Claude found working sources and opened every one on 23 Nov (shown, 16:20): Skills England OCC0828 (Sport performance analyst, Health and science); Wonkee Donkee (the 3, 4, 5 rule); Plus at its new address (sin θ = b/a); GOV.UK "Your guide to NHS breast screening" ("For every 100 people who have breast screening, 4 will need further tests"; "Of those 4 people, 1 will be diagnosed with breast cancer"); The Analyst (xG on a scale between zero and one); UH Sussex ?p=5862 (technetium "has a half-life of six hours"); BNMS (the technologist's role); FSA hot holding (63°C or above; out more than two hours, thrown away); Bromley "High-risk foods" ("can double in number every 10 to 20 minutes"). Probability's two jobs were both among the 7, so its page was not built.

CLASS CHECK: Local: content in data/uses.json and the one page entry the build requires. The checks that guard it (check-uses.py's reader, headlines, sideways scroll, KaTeX, live-games-only Practise it; check-site-nav.py's HUBS) already exist and are not changed.

EXACT CHANGE:
1. First commit: save this contract verbatim as docs/handover/contracts/2026-11-23-wwiut-restore-7.md. No home-lane close-out is owed (#888's was recorded on main by 2e96b6f). #890's close-out belongs to the cloud lane: do not do it.
2. data/uses.json, keeping the file's existing formatting:
   a. Insert the APPENDIX "topic" into topics immediately after "trigonometry".
   b. Append the 7 APPENDIX "scenarios" to scenarios, verbatim, in the order given.
   c. In scenario "payroll-administrator", append to the end of its text exactly: " Real payslips use HMRC's tax tables, so they can differ by a few pence." (Jon, 16:12). Nothing else in any existing scenario changes.
3. data/games.json "pages": add the APPENDIX "page" entry (build-uses.py refuses without it: shown, Project Claude's trial).
4. schools/assets/site-nav.js: CONTRACT EXCEPTION, one line only: in HUBS, after the trigonometry line, add
       '/when-will-i-use-this/probability/': 'the topic page',
   (the page links games, so check-site-nav.py needs it; same form as #883's and #888's lines). Nothing else in schools/assets/ changes.
5. Run scripts/build-uses.py, then check-uses.py --selftest and --check. Expected (Project Claude's trial on 4d09d45, shown): self-test 98 of 98; "headlines: 47 sums recomputed"; "pages: 33 generated (17 topics, 15 routes with scenarios) ... 47 scenarios, 62 sources"; Probability's Practise it: expected-damage, probability-pioneer, probability-paradox, given-that, screening-room, core-maths-paper2b; "chromium: 33 pages x 2 sizes x normal and Aa: no sideways scroll, KaTeX rendered"; OK. The home strip then reads "47 real jobs" (written by the build).
6. Run scripts/check-uses-links.py --live and report the result. Every new source was opened by hand on 23 Nov.
7. /updates/: one dated line, e.g. "23 Nov 2026: When will I use this? now has 47 jobs, and a Probability page: breast screening call-backs and football's expected goals."
8. Merge with merge-pr.py when the Gate is green; record the merge commit and main's run IDs in docs/handover/home.md; run end-task.

DO NOT TOUCH: any other scenario or topic (except step 2c's one sentence); the 7 scenarios' wording (verbatim); check-uses.py, build-uses.py, check-uses-links.py; any file under games/; schools/assets/ except step 4's line; parents/; canon, AGENTS.md, the roster, docs/todo.md, docs/handover/cloud.md; .github/workflows/, scripts/ci-*, merge-pr.py; #890's close-out (cloud's).

SUCCESS CONDITION: data/uses.json has 17 topics and 47 scenarios; check-uses.py --selftest and --check pass with the figures in step 5; the Probability page exists and lists the two probability jobs; check-site-nav.py passes; the link check's result is in the PR; Gate green; merged; main green; home.md records it.

STOP IF: any of the 7 sources fails the live link check (report which; do not drop the job or guess a URL; Project Claude rules); check-uses.py reports any failure in the 7 or the payroll text; the figures in step 5 differ (report what you got); check-site-nav.py needs more than the one HUBS line; a check still fails after your second fix (standing rule); merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").

APPENDIX (verbatim):
{
 "topic": {
  "slug": "probability",
  "title": "Probability",
  "answer": "Whenever you need to know how likely something really is.",
  "keywords": [
   "probability",
   "conditional probability"
  ],
  "parentGuide": "probability"
 },
 "page": {
  "when-will-i-use-this/probability/index.html": {
   "title": "Probability: when will I use this? | MaffsGames",
   "description": "Real jobs that use probability: breast screening call-backs and football's expected goals, with worked examples and sources. Free, no sign-up."
  }
 },
 "scenarios": [
  {
   "id": "football-analyst",
   "topic": "percentages",
   "route": "health-and-science",
   "job": "Football performance analyst",
   "tier": "F",
   "headline": "408 ÷ 480 × 100 = 85%",
   "formula": "\\dfrac{\\text{completed}}{\\text{attempted}} \\times 100",
   "question": "Is this midfielder's passing any good?",
   "inside": "Percentages",
   "text": "Analysts turn a match into numbers the coach can use. A midfielder tried 480 passes over five games and 408 reached a teammate (example figures).",
   "steps": [
    "Pass completion: 408 ÷ 480 × 100 = 85%."
   ],
   "sources": [
    {
     "title": "Skills England, Sport performance analyst (OCC0828)",
     "url": "https://occupational-maps.skillsengland.education.gov.uk/maps/occupation/OCC0828",
     "type": "public"
    }
   ],
   "exampleFigures": true
  },
  {
   "id": "bricklayer-corner",
   "topic": "pythagoras",
   "route": "construction",
   "job": "Bricklayer",
   "tier": "F",
   "headline": "3² + 4² = 5²",
   "formula": "a^2 + b^2 = c^2",
   "question": "Is this corner really square?",
   "inside": "Pythagoras",
   "text": "To check a corner is square, mark 3 m along one wall and 4 m along the other: the diagonal must be exactly 5 m.",
   "steps": [
    "3² + 4² = 9 + 16 = 25 = 5², so the corner is 90°.",
    "A diagonal of 5.1 m means the corner is more than 90° and the walls aren't square."
   ],
   "sources": [
    {
     "title": "Wonkee Donkee Tools, \"How to lay the first three courses\"",
     "url": "https://www.wonkeedonkeetools.co.uk/builders-profiles/how-to-lay-the-first-three-courses",
     "type": "public"
    }
   ],
   "exampleFigures": false
  },
  {
   "id": "crime-scene-investigator",
   "topic": "trigonometry",
   "route": "protective-services",
   "job": "Crime scene investigator",
   "tier": "F",
   "headline": "sin⁻¹(2 ÷ 4) = 30°",
   "formula": "\\sin\\theta = \\dfrac{\\text{width}}{\\text{length}}",
   "question": "What angle did this blood drop hit at?",
   "inside": "Trigonometry",
   "text": "A blood drop that hits a surface at an angle leaves a stretched mark. The width ÷ the length is the sine of the angle it hit at. A mark 2 mm wide and 4 mm long (example figures):",
   "steps": [
    "sin θ = 2 ÷ 4 = 0.5, so θ = sin⁻¹(0.5) = 30°.",
    "A mark 1 mm by 4 mm: sin⁻¹(0.25) = 14.5°, a shallower hit."
   ],
   "sources": [
    {
     "title": "Plus Magazine (University of Cambridge), \"Solving crimes with maths: Bloodstain pattern analysis\"",
     "url": "https://plus.maths.org/solving-crimes-maths",
     "type": "public"
    },
    {
     "title": "National Careers Service, \"Scenes of crime officer\"",
     "url": "https://nationalcareers.service.gov.uk/job-profiles/scenes-of-crime-officer",
     "type": "public"
    }
   ],
   "exampleFigures": true
  },
  {
   "id": "mammographer",
   "topic": "probability",
   "route": "health-and-science",
   "job": "Mammographer (breast screening radiographer)",
   "tier": "F",
   "headline": "10 ÷ 40 × 100 = 25% of call-backs are cancer",
   "formula": "\\dfrac{\\text{cancer}}{\\text{called back}} \\times 100",
   "question": "If you're called back, how likely is it to be cancer?",
   "inside": "Probability",
   "text": "NHS breast screening calls about 4 in every 100 people back for more tests. Of those 4, about 1 is diagnosed with breast cancer. Out of 1,000 people screened:",
   "steps": [
    "Called back: 1000 × 4 ÷ 100 = 40.",
    "Diagnosed with breast cancer: 40 ÷ 4 = 10.",
    "Chance a call-back is cancer: 10 ÷ 40 × 100 = 25%. So 3 in 4 people called back are fine."
   ],
   "sources": [
    {
     "title": "GOV.UK, \"Your guide to NHS breast screening\"",
     "url": "https://www.gov.uk/government/publications/breast-screening-helping-women-decide/nhs-breast-screening-helping-you-decide",
     "type": "public"
    }
   ],
   "exampleFigures": false
  },
  {
   "id": "football-recruitment-analyst",
   "topic": "probability",
   "route": "health-and-science",
   "job": "Football recruitment analyst",
   "tier": "H",
   "headline": "1 − 0.0657 = 0.9343, the chance of at least one goal",
   "formula": "1 - (1 - p_1)(1 - p_2)(1 - p_3)",
   "formulaNote": "p is each shot's chance of scoring",
   "question": "Why can't one attack be worth 1.67 goals?",
   "inside": "Probability",
   "text": "Expected goals (xG) gives every shot a probability of being scored, from 0 to 1. Different models give slightly different values. One attack had three shots worth 0.41, 0.47 and 0.79 (example figures).",
   "steps": [
    "xG for the attack: 0.41 + 0.47 + 0.79 = 1.67.",
    "You can't score 1.67 goals from one attack. The chance of no goal is (1 − 0.41) × (1 − 0.47) × (1 − 0.79) = 0.0657, so the chance of at least one goal is 1 − 0.0657 = 0.9343."
   ],
   "sources": [
    {
     "title": "The Analyst (Opta), \"What Is Expected Goals (xG)?\"",
     "url": "https://theanalyst.com/articles/what-is-expected-goals-xg",
     "type": "public"
    }
   ],
   "exampleFigures": true
  },
  {
   "id": "nuclear-medicine-technologist",
   "topic": "exponential-change",
   "route": "health-and-science",
   "job": "Nuclear medicine technologist",
   "tier": "H",
   "headline": "(½)⁴ × 100 = 6.25% left after a day",
   "formula": "\\left(\\tfrac{1}{2}\\right)^n",
   "formulaNote": "n is the number of half-lives",
   "question": "How much tracer is left after a day?",
   "inside": "Powers",
   "text": "The tracer used in many scans halves every 6 hours (its half-life). After 24 hours:",
   "steps": [
    "Half-lives: 24 ÷ 6 = 4.",
    "Left: (½)⁴ = 1/16 = 0.0625, so 6.25%."
   ],
   "sources": [
    {
     "title": "University Hospitals Sussex NHS, \"What is nuclear medicine?\" (patient information)",
     "url": "https://uhsussex.nhs.uk/?p=5862",
     "type": "public"
    },
    {
     "title": "British Nuclear Medicine Society, \"What does a Nuclear Medicine Technologist do?\"",
     "url": "https://www.bnms.org.uk/page/WhatdoesaNuclearMedicineTechnologistdo",
     "type": "public"
    }
   ],
   "exampleFigures": false
  },
  {
   "id": "chef",
   "topic": "exponential-change",
   "route": "catering",
   "job": "Chef",
   "tier": "F",
   "headline": "100 × 2⁶ = 6,400 bacteria",
   "formula": "N = 100 \\times 2^n",
   "formulaNote": "n is the number of 20-minute doublings",
   "question": "Why is food left out for 2 hours thrown away?",
   "inside": "Powers",
   "text": "Hot food must be kept at 63°C or above. Below that, bacteria can double every 20 minutes in the right conditions, which is why food left out more than 2 hours is thrown away. Start with 100 bacteria, 2 hours at room temperature (example figure):",
   "steps": [
    "Doublings: 120 ÷ 20 = 6.",
    "Bacteria: 100 × 2⁶ = 100 × 64 = 6,400."
   ],
   "sources": [
    {
     "title": "Food Standards Agency, Safer Food Better Business, \"Hot holding\"",
     "url": "https://www.food.gov.uk/sites/default/files/media/document/sfbb-caterer-cooking-06-hot-holding_0.pdf",
     "type": "public"
    },
    {
     "title": "London Borough of Bromley, \"High-risk foods\"",
     "url": "https://www.bromley.gov.uk/leaflet/261300/12/799/d",
     "type": "public"
    }
   ],
   "exampleFigures": true
  }
 ]
}

END OF CONTRACT
