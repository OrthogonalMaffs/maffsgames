# D-BY-DX-BUILD (Jon, 26 Nov 2026), verbatim

```text
D-BY-DX-BUILD (26 Nov 2026). Cloud lane: the session that ran SOME-THINGIES-HOST, or a fresh cloud session. Tier: Medium (one shared file for a new game, by Jon's lane exception below): merge on green with merge-pr.py; the game merges UNLISTED. Send: now (the cloud lane is free: #931 merged at 20:06).
From Project Claude. Jon, 26 Nov 2026:
- 20:28: multiple choice for the first build; free typed answers later; differentiation only for now; build to his assessment paper.
- 20:38-20:39: a Pro mode that turns the cheat sheet off. It is a start-screen switch for every stage, with its own boards; in Pro a wrong answer shows the table row the student needed.
- 20:39: the five stages.
- 20:43: the cheat sheet is the derivative table printed on his paper.
- 20:44: build now; Jon writes the wrong-answer lines, tagline and look after playing it.
- 20:46: keep the constant terms.
- 20:48: lane exception for ONE line in schools/assets/firebase-leaderboard.js: the 'pro-stage-5' label.
Backlog row D-BY-DX; the spec is Project Claude's.
Recommended: Claude Code, Opus, high effort. A new five-stage game from a fixed 60-item bank, with a verifier and full integration, modelled on It's Just Base 60, Bruv.

TASK: Build "d by dx? Why?" at /games/d-by-dx-why/ for Jon's Level 3 class and merge it unlisted. It is differentiation: power terms, rewriting roots and fractions as powers, sin and cos, e and ln, and sums of terms. It has five stages of four-option questions from the fixed bank the generator below produces, and every wrong option is a named error with its own line. The derivative table is on screen, and a Pro switch hides it. Pro has its own boards.

ROOT CAUSE: New build, not a fault.
- Shown: backlog row D-BY-DX (docs/todo.md) asks for it. It is canon §0.2 priority 2, Jon's own class. His assessment is in January, and he wants it built and played before the Christmas break.
- Shown: the live calculus games are harder than his class needs.
  - Differentiation Duel is A-Level and L4 (.claude/rules/game-roster.md:110).
  - Y So Steep? is straight lines.
  - No live game asks for a derivative at Level 3, with the variable changing (x, r, t, z) or with the question's three wordings.

CLASS CHECK: New build; no bug class.
- Every shared behaviour comes from existing shared assets used exactly as games/its-just-base-60-bruv/index.html uses them: level resolve, stage boards, answer lock, MaffsNext, MaffsOptions.build and shuffle, MaffsText, stage-exit, teacher-invite, fold, site-nav, leaderboard, score history and analytics.
- The theme comes from games/cast-away/index.html, because both serve Level 3 only: data-theme="dark" by canon's palette rule.
- One shared-file change, Jon's lane exception (20:48): the label 'pro-stage-5' in schools/assets/firebase-leaderboard.js.
  - Every other board key this game uses already has a label: 'stage-1'..'stage-5' and 'pro-stage-1'..'pro-stage-4', lines 131-135.
  - firebase/database.rules.json accepts any levelKey of [a-z0-9-]{1,40}, so no rules change and no deploy.

EXACT CHANGE:
1. First commit: the standing close-outs, in your new entry in docs/handover/cloud.md.
   a. BASE-60-CUCKOO (#929, merge commit 54d13e6): merge-pr.py's last line, and main's check-site, phone-fit-full and pages run IDs and results for 54d13e6, read from the PR and GitHub Actions. Then git mv docs/handover/contracts/2026-11-26-base-60-cuckoo.md docs/history/contracts/.
   b. SOME-THINGIES-HOST (#931, merge commit 9f51bb8): the same records. Then git mv docs/handover/contracts/2026-11-26-some-thingies-host.md docs/history/contracts/.
   c. In the same commit, save this contract verbatim as docs/handover/contracts/2026-11-26-d-by-dx-build.md.

2. The bank.
   - Save the generator below verbatim as tools/d-by-dx-why/bank.py and run it: python -X utf8 -I tools/d-by-dx-why/bank.py --out <file>.
   - It must print "total 60" and sha256 a8ecdc0582e0f336832726f8f4bf9f8782ef9f944b2efe5148d864658428a14e. That is the hash of the item lines: json.dumps(item, separators=(",", ":"), ensure_ascii=False) + "\n", in generator order, UTF-8.
   - 12 items a stage. Embed its output in the page as a static array, one item a line, as Base 60 does. Never edit an item by hand.

3. The page: games/d-by-dx-why/index.html, one HTML page on shared assets.
   - Modelled on games/its-just-base-60-bruv/index.html for structure, stage choice, boards, start and results screens, MaffsNext, feedback and integration.
   - Theme as games/cast-away/index.html: data-theme="dark", Outfit and JetBrains Mono from theme.css. No decorative emoji.
   - Level: MaffsLevel.resolve({slug: 'd-by-dx-why', levels: ['level3'], fallback: 'level3', boards: [the ten keys in c]}). One level of content, no picker.
   - Do NOT load large-screen.js: the layer's rollout to new pages waits for Jon's look (todo LARGE-SCREEN-ROLLOUT).
   a. Title and badge.
      - Title "d by dx? Why?".
      - Sub-line, a placeholder until Jon writes his tagline: "Differentiation for Level 3 engineers: the power rule, roots and fractions, sin and cos, e and ln. The table is there; Pro takes it away."
      - Calculator badge: not allowed (Non-calculator).
   b. Start screen.
      - The five stages to choose from, with their names from the generator's STAGES:
        1 Power terms
        2 Rewrite first
        3 Sin and cos
        4 e and ln
        5 Sums of terms
      - Above them, the Pro switch: a button with aria-pressed, labelled "Pro: no table". It is off on every load, applies to whichever stage is chosen next, and is never stored.
   c. A run.
      - 8 items from the chosen stage's 12, no repeat within a run (MaffsOptions.shuffle). Score out of 8.
      - Boards: 'stage-1'..'stage-5', or with Pro on 'pro-stage-1'..'pro-stage-5'.
      - The score is submitted only at the run's end through MaffsLock.finishOnce, with MaffsScoreHistory, as Base 60 does.
   d. The derivative table ("the table").
      - Two columns. The headings are, in KaTeX: "\(y\) or \(f(x)\)" and "\(\dfrac{dy}{dx}\) or \(f'(x)\)".
      - The six rows, in this order, keyed for highlighting:
        x: \(x\) | \(1\)
        axn: \(ax^{n}\) | \(anx^{n-1}\)
        sin: \(\sin ax\) | \(a\cos ax\)
        cos: \(\cos ax\) | \(-a\sin ax\)
        exp: \(e^{ax}\) | \(ae^{ax}\)
        ln: \(\ln ax\) | \(\frac{1}{x}\)
      - It is written in x only, whatever the item's variable, as on Jon's paper.
      - With Pro off, it is on screen during every question: open from 1024 px, and a fold-away panel "Derivative table" on narrower screens (shared fold.js; closed on load there).
      - With Pro on, it is not in the page during a question.
   e. Each item.
      - Its prompt through MaffsText. The prompts carry their own \( \).
      - Then four options from MaffsOptions.build(answer.tex, the three decoys' tex). Each button's dataset.val is the tex string exactly as the bank has it, and its label is that tex rendered by KaTeX. Marking by dataset.val only.
   f. Feedback (canon §7.6).
      - A right answer shows "Right: " and the answer in KaTeX, and advances after 1000 ms.
      - A wrong answer shows, in order:
        1. the LINES line for the chosen option's err key;
        2. "The answer is " and the answer in KaTeX;
        3. the item's working lines, each through MaffsText;
        4. the table rows named in the item's "rows" (one or two), headed "From the table:", in both modes;
        5. MaffsNext.wrong.
      - With Pro off, the same rows are also highlighted in the open table until Next.
      - The options stay visible and locked, the chosen one marked wrong and the answer marked right.
      - On a screen where that cannot fit, hide the two options that are neither the chosen one nor the answer while the feedback shows (canon §7.6.1), and show them again with the next item.
      - The whole wrong-answer screen, Next included, must be above the fold at 375 × 667, 390 × 844, 1280 × 720 and 1366 × 768, in normal and Aa mode, for every item and both modes (step 6).
   g. LINES: one object, under the comment "Placeholders by Project Claude, 26 Nov 2026; Jon writes the real lines after playing." No line anywhere else. Verbatim, one per err key, exactly the keys of the generator's ERR_STAGES:
      power_kept: "You multiplied by the power, then forgot to take one off it."
      coeff_lost: "The number in front got lost. Multiply it by the power too."
      new_power_used: "Multiply by the power you started with, not the new one."
      kept_variable: "A letter on its own differentiates to 1, so it disappears and the number stays."
      treated_as_constant: "That's a letter times a number, not a constant. It differentiates to the number."
      sign_lost: "The power was negative, so bringing it down gives a minus."
      power_wrong_way: "Take one off the power, even when it's negative or a fraction: -2 goes to -3."
      bottom_differentiated: "Rewrite it as a power first. You can't differentiate the bottom on its own."
      root_upside_down: "A square root is the power 1/2: the root's number goes on the bottom of the power."
      a_forgotten: "The number in the angle or the power comes out to the front."
      sign_slip: "sin goes to cos, and cos goes to minus sin. Check the sign."
      a_dropped_from_angle: "The number comes out to the front, but it stays in the angle too."
      integrated_instead: "That's integrating: you divided by the number. Differentiating multiplies by it."
      power_rule_used: "e to a power isn't x to a power. The power stays the same."
      a_kept: "ln of ax goes to 1/x. The number cancels out."
      a_divided: "ln of ax goes to 1/x, not 1/(ax). The number cancels out."
      ln_flipped: "ln of ax differentiates to 1/x, not 1 over the ln."
      constant_kept: "A number on its own doesn't change, so it differentiates to 0."
   h. Analytics: game_started, question_answered (question_id = the item's id, correct true or false) and game_completed only. Level 'level3'; mode the run's board key. Nothing else.

4. The one shared line (Jon's lane exception, 20:48).
   - In schools/assets/firebase-leaderboard.js, add 'pro-stage-5':'Pro · Stage 5' to LEVEL_NAMES, beside 'stage-5' (line 135), with a comment: "// d by dx? Why? Pro mode, Stage 5 (contract D-BY-DX-BUILD; Jon's lane exception, 26 Nov 2026, 20:48)."
   - Nothing else in that file or any other shared asset.

5. Integration, each as Base 60 did it at its build (contract BASE-60, docs/history/contracts/):
   - stage-exit.js, teacher-invite.js, fold, site-nav.js (via scripts/apply-site-nav.py);
   - schools/assets/launch-dates.json "d-by-dx-why": the merge date;
   - .claude/rules/game-roster.md, a row under Unlisted, and its note:
     - levels L3; topic Calculus;
     - description: "Differentiation for Level 3 (EAL 004C): power terms, roots and fractions rewritten as powers, sin and cos, e and ln, sums of terms; the variable changes (x, r, t, z) and the question's three wordings. Five stages × 12 (60 questions), four options, every wrong option a named error with its own line. The derivative table on screen; Pro hides it, own boards (stage-N, pro-stage-N). One level of content (key level3).";
     - calculator not allowed;
   - a data/games.json entry (unlisted), then apply-meta.py and check-meta.py:
     - search phrase "Differentiation game: power rule, trig, e and ln";
     - keywords including "differentiation", "differentiate", "derivative", "dy/dx", "power rule", "calculus", "level 3", "engineering maths";
   - the findings file;
   - the MIGRATED and registration lists Base 60 is in: check-theme.py, check-levels.py, check-answer-lock.py, check-start-mount.py, check-teacher-invite.py, audit-register.py, verify-stage-exit.py;
   - check-leaderboard-coverage.js NOT_ON_HUB, with the note "new, unlisted until Jon has played and approved it; hub row added at listing".
   - No noindex. No /updates/ line while unlisted.

6. The verifier: scripts/verify-d-by-dx-why.py in CI, with the ci-shards header (as verify-its-just-base-60-bruv.py has, ci-deps games/d-by-dx-why/ tools/d-by-dx-why/) and --selftest.
   a. The bank (never runs or imports the generator):
      - the hash and counts;
      - ids and prompts unique;
      - each item's question rebuilt in sympy from its "q" terms and differentiated, and equal to its answer's terms;
      - every decoy's terms not equal to the answer or to another option;
      - every decoy recomputed independently from its err key and the item's question terms;
      - every tex string (qtex, answer and decoys) re-rendered from its terms by the verifier's own formatter and equal to the bank's;
      - every decoy's err key allowed for its stage by ERR_STAGES (read from the generator's source as data, by ast);
      - "rows" correct for the stage and kind;
      - every working line's sums true.
   b. Lines: LINES has exactly the keys of ERR_STAGES; every key the bank uses has a line, and no line is unused.
   c. In Chromium:
      - each stage is played to the end in both modes. Each run has eight different items of that stage with four options each, every button's dataset.val the bank's tex.
      - A right answer shows "Right:" and moves on by itself.
      - A wrong answer:
        - marks the chosen option wrong and the answer right;
        - shows exactly the LINES line for the chosen option's err key;
        - shows the answer, every working line, the item's table rows and Next.
      - The score is the right answers; there is one game_completed and one leaderboard submission on the run's board.
      - With Pro off, the table is open at 1280 × 720, closed but present at 375 × 667, and highlights the item's rows after a wrong answer. With Pro on, there is no table during a question.
      - No event but game_started, question_answered (with the item's id) and game_completed.
   d. For every item, in both modes: the wrong-answer screen (line, answer, working, rows, Next) is above the fold at 375 × 667, 390 × 844, 1280 × 720 and 1366 × 768, normal and Aa. Figures from CI, not a container (fonts differ).
   e. Plants, each caught:
      - a wrong answer;
      - a decoy equal in value to its answer;
      - a tex string that doesn't match its terms;
      - a missing LINES key;
      - the wrong line shown for a decoy;
      - a decoy err key its stage does not allow (sign_slip in Stage 1);
      - the table shown during a Pro question;
      - the working pushed below the fold.

7. Phone fit and contrast.
   - Measure the game in normal, Aa and laptop modes (scripts/measure-phone-fit.py), with Pro on and off. It must pass every size without any known-failure entry.
   - scripts/check-contrast.py passes, including the highlighted table row on the dark theme.

8. docs/todo.md.
   - Rewrite row D-BY-DX to what is still owed, under TODO-TRIM, with the built part moved word for word to docs/history/todo-done.md. Still owed:
     - Jon plays all five stages in both modes (/games/d-by-dx-why/);
     - he writes the LINES lines, the tagline and the look;
     - he rules on listing;
     - Phase 2, integration as reverse differentiation (his rulings of 26 Nov 14:11-14:14 stay in the row), needs Project Claude's spec.
   - Add one row, D-BY-DX-TYPED: "Free typed answers for d by dx? Why? (Jon, 26 Nov 2026: multiple choice first, typed responses as future development)."

9. Merge on green via scripts/merge-pr.py.
   - Record the merge commit, its last line and main's run IDs in your cloud.md entry, and run end-task.
   - Report for Jon: https://maffsgames.co.uk/games/d-by-dx-why/ (please play each stage with Pro off and on, and get some wrong).

DO NOT TOUCH:
- Every other game page.
- schools/assets/, except the one 'pro-stage-5' line in step 4.
- The bank's items: generator only.
- Firebase rules.
- scripts/check-site.py, scripts/measure-phone-fit.py and every other checker, except the registration and MIGRATED list lines in step 5.
- The hub, the Essentials page and the homepage: listing is Jon's later decision.
- Canon, AGENTS.md and docs/handover/home.md.
- Any other session's entries in cloud.md. If main gains cloud.md changes (the archive bot's included), merge main in and keep both sides.
- Never write any wording or number from Jon's assessment paper anywhere in the repo. Project Claude has checked that no bank item reproduces one of its items.

SUCCESS CONDITION:
- /games/d-by-dx-why/ plays all five stages, in both modes, from the exact bank (hash matches), on the dark theme.
- The table is laid out as given. Pro hides it and has its own five boards. 'pro-stage-5' has its label.
- Every answer is marked by dataset.val.
- Every wrong option shows its own LINES line, the answer, the working and its table rows, with Next above the fold at all four sizes, normal and Aa, for every item.
- The verifier passes with all eight plants caught.
- These pass: check-site, phone fit (normal, Aa, laptop, Pro on and off, no known failures), check-contrast, check-answer-lock, check-levels, check-theme, check-meta, check-site-nav, check-start-mount, check-teacher-invite and leaderboard coverage.
- The game is unlisted. The roster, games.json, launch date and both todo rows are in.
- Both close-outs are in the first commit.
- Merged with merge-pr.py, and cloud.md records it.

STOP IF:
- The generator's hash or counts differ from the above. Report both; never edit items.
- Any answer, decoy or tex string disagrees with your independent recomputation. Report the item; never edit it.
- Two options in an item are equal in value.
- An item's wrong-answer screen cannot fit above the fold at any of the four sizes, in either mode, without smaller text, removed content or keys under 44 px. Report the item and the figures.
- A KaTeX string in the bank fails to render.
- A shared check needs an exemption for this game.
- Any change to a shared asset beyond the one line in step 4 is needed.
- todo.md's rows cannot fit under TODO_LIMIT without moving an open row.
- A check still fails after your second fix (standing rule).
- merge-pr.py can't reach GitHub.
- A push is refused (never force).
- Anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies: report it under "Decided for you", and never use it to override a STOP IF.

GENERATOR (tools/d-by-dx-why/bank.py, verbatim):
#!/usr/bin/env python3
"""d by dx? Why?: question bank generator, Phase 1, differentiation (Project Claude, 26 Nov 2026). Deterministic: no randomness.

Five stages of 12 items, Level 3 (EAL AME3-004, assessment 004C). Built to the item TYPES of Jon's paper, never its wording
or numbers. Every expression is held as a list of terms; TeX is written from the terms here, and the page shows only the
TeX. Every distractor comes from a named error (canon SR-4) and carries that error's key, so the page can show its line.

Term kinds (coefficients and powers are exact fractions, written "p" or "p/q"):
  ["pow", c, n]      c * v^n           ["const", c]        c
  ["sin", c, a]      c * sin(a v)      ["cos", c, a]       c * cos(a v)
  ["exp", c, a]      c * e^(a v)       ["ln", c, a]        c * ln(a v)
  ["over", c, d]     c / (d v)         ["recipln", c, a]   c / ln(a v)
  ["xexp", c, a]     c * v * e^(a v - 1)   ["overpow", c, d, m]   c / (d v^m)
Options are TeX strings; dataset.val is the answer's or decoy's "tex" exactly.
"""
import hashlib
import json
import math
import sys
from fractions import Fraction as F

STAGES = {1: "Power terms", 2: "Rewrite first", 3: "Sin and cos", 4: "e and ln", 5: "Sums of terms"}
FORMS = ["wrt", "bare", "fn"]


def fs(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def T(kind, *args):
    return [kind] + [fs(a) for a in args]


# ------------------------------------------------------------------------------------------------ TeX
def frac_tex(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return ("-" if x < 0 else "") + r"\frac{%d}{%d}" % (abs(x.numerator), x.denominator)


def coef(c, lead, attach=True):
    c = F(c)
    sign = "-" if c < 0 else ("" if lead else "+")
    a = abs(c)
    if a == 1 and attach:
        return sign
    return sign + frac_tex(a)


def ang(a, v):
    a = F(a)
    return v if a == 1 else f"{frac_tex(a)}{v}"


def term_tex(t, v, lead):
    k, args = t[0], [F(x) for x in t[1:]]
    c = args[0]
    if k == "const":
        return coef(c, lead, attach=False)
    if k == "pow":
        n = args[1]
        if n == 0:
            return coef(c, lead, attach=False)
        return coef(c, lead) + (v if n == 1 else f"{v}^{{{frac_tex(n)}}}")
    if k in ("sin", "cos"):
        return coef(c, lead) + rf"\{k} {ang(args[1], v)}"
    if k == "exp":
        return coef(c, lead) + f"e^{{{ang(args[1], v)}}}"
    if k == "ln":
        return coef(c, lead) + rf"\ln {ang(args[1], v)}"
    if k == "xexp":
        return coef(c, lead) + f"{v}e^{{{ang(args[1], v)}-1}}"
    sign = "-" if c < 0 else ("" if lead else "+")
    if k == "over":
        d = args[1]
        return sign + r"\frac{%s}{%s}" % (frac_tex(abs(c)), v if d == 1 else f"{frac_tex(d)}{v}")
    if k == "overpow":
        d, m = args[1], args[2]
        return sign + r"\frac{%s}{%s%s}" % (frac_tex(abs(c)), frac_tex(d), v if m == 1 else f"{v}^{{{frac_tex(m)}}}")
    if k == "recipln":
        return sign + r"\frac{%s}{\ln %s}" % (frac_tex(abs(c)), ang(args[1], v))
    raise ValueError(k)


def tex(terms, v):
    return "".join(term_tex(t, v, i == 0) for i, t in enumerate(terms))


# ------------------------------------------------------------------------------------------------ values (for the checks)
def value(terms, x):
    s = 0.0
    for t in terms:
        k, a = t[0], [float(F(y)) for y in t[1:]]
        c = a[0]
        s += {"const": lambda: c, "pow": lambda: c * x ** a[1], "sin": lambda: c * math.sin(a[1] * x),
              "cos": lambda: c * math.cos(a[1] * x), "exp": lambda: c * math.exp(a[1] * x),
              "ln": lambda: c * math.log(a[1] * x), "over": lambda: c / (a[1] * x),
              "recipln": lambda: c / math.log(a[1] * x), "overpow": lambda: c / (a[1] * x ** a[2]), "xexp": lambda: c * x * math.exp(a[1] * x - 1)}[k]()
    return s


POINTS = (0.37, 0.61, 1.7, 2.3)   # positive, away from ln's zero at a v = 1 for every a used


# ------------------------------------------------------------------------------------------------ prompts and working
def prompt(form, v, q):
    if form == "wrt":
        return rf"Differentiate with respect to \({v}\): \(y = {q}\)"
    if form == "bare":
        return rf"Differentiate: \({q}\)"
    return rf"If \(f({v}) = {q}\), find \(f'({v})\)"


def answer_line(form, v, q, ans):
    if form == "wrt":
        return rf"\(\dfrac{{dy}}{{d{v}}} = {ans}\)"
    if form == "fn":
        return rf"\(f'({v}) = {ans}\)"
    return rf"\(\dfrac{{d}}{{d{v}}}\left({q}\right) = {ans}\)"


def pow_steps(c, n, v):
    """The two power-rule lines: bring the power down, take one off."""
    return [rf"Bring the power down: \({frac_tex(c)} \times {'(' + frac_tex(n) + ')' if n < 0 else frac_tex(n)} = {frac_tex(c * n)}\)",
            rf"Take one off the power: \({frac_tex(n)} - 1 = {frac_tex(n - 1)}\)"]


# ------------------------------------------------------------------------------------------------ the bank
items = []


def add(stage, v, form, q_terms, q_tex, answer, decoys, working, rows):
    n = sum(1 for i in items if i["stage"] == stage) + 1
    qt = q_tex if q_tex is not None else tex(q_terms, v)
    ans_tex = tex(answer, v)
    items.append({"id": f"s{stage}-{n:02d}", "stage": stage, "var": v, "form": form, "q": q_terms, "qtex": qt,
                  "prompt": prompt(form, v, qt),
                  "answer": {"tex": ans_tex, "terms": answer},
                  "decoys": [{"err": e, "tex": tex(t, v), "terms": t} for e, t in decoys],
                  "rows": rows,
                  "working": working + [answer_line(form, v, qt, ans_tex)]})


def stage1():
    for i, (v, a, n) in enumerate([("x", 5, 4), ("t", 3, 5), ("r", 7, 2), ("x", 6, 3), ("t", 2, 6), ("r", 4, 5),
                                   ("z", 9, 2), ("x", -3, 4), ("t", 8, 3)]):
        add(1, v, FORMS[i % 3], [T("pow", a, n)], None, [T("pow", a * n, n - 1)],
            [("power_kept", [T("pow", a * n, n)]), ("coeff_lost", [T("pow", n, n - 1)]),
             ("new_power_used", [T("pow", a * (n - 1), n - 1)])],
            pow_steps(F(a), F(n), v), ["axn"])
    for i, (v, a) in enumerate([("x", 7), ("t", 12), ("r", -5)]):
        add(1, v, FORMS[(i + 1) % 3], [T("pow", a, 1)], None, [T("const", a)],
            [("kept_variable", [T("pow", a, 1)]), ("coeff_lost", [T("const", 1)]), ("treated_as_constant", [T("const", 0)])],
            [rf"\({v}\) on its own differentiates to \(1\), so the \({v}\) goes and the number stays: \({frac_tex(a)} \times 1 = {frac_tex(a)}\)"],
            ["x"])


def stage2():
    for i, (v, a, n) in enumerate([("x", 3, 2), ("t", 4, 3), ("r", 6, 1), ("x", 5, 4), ("z", 8, 2), ("t", -2, 3)]):
        den = v if n == 1 else f"{v}^{n}"
        qt = (r"\frac{%d}{%s}" % (a, den)) if a > 0 else (r"-\frac{%d}{%s}" % (-a, den))
        bottom = [T("overpow", a, n, n - 1)] if n > 1 else [T("const", a)]
        add(2, v, FORMS[i % 3], [T("pow", a, -n)], qt, [T("pow", -a * n, -n - 1)],
            [("sign_lost", [T("pow", a * n, -n - 1)]), ("power_wrong_way", [T("pow", -a * n, -n + 1)]),
             ("bottom_differentiated", bottom)],
            [rf"Rewrite first: \({qt} = {tex([T('pow', a, -n)], v)}\)"] + pow_steps(F(a), F(-n), v), ["axn"])
    for i, (v, c, m, k) in enumerate([("x", 1, 5, 2), ("r", 1, 2, 3), ("t", 4, 3, 2), ("x", 1, 7, 2), ("r", 6, 4, 3),
                                      ("t", 2, 5, 3)]):
        root = (r"\sqrt{%s^{%d}}" % (v, m)) if k == 2 else (r"\sqrt[%d]{%s^{%d}}" % (k, v, m))
        qt = ("" if c == 1 else str(c)) + root
        p = F(m, k)
        add(2, v, FORMS[(i + 1) % 3], [T("pow", c, p)], qt, [T("pow", c * p, p - 1)],
            [("root_upside_down", [T("pow", F(c) / p, 1 / p - 1)]), ("power_kept", [T("pow", c * p, p)]),
             ("power_wrong_way", [T("pow", c * p, p + 1)])],
            [rf"Rewrite first: \({qt} = {tex([T('pow', c, p)], v)}\) (the root's number goes on the bottom of the power)"]
            + pow_steps(F(c), p, v), ["axn"])


def stage3():
    for i, (f, v, c, a) in enumerate([("sin", "x", 1, 4), ("cos", "t", 1, 5), ("sin", "t", 3, 2), ("cos", "x", 2, 6),
                                      ("sin", "r", 5, 3), ("cos", "t", 4, 2), ("sin", "x", 1, 7), ("cos", "z", 1, 8),
                                      ("sin", "t", 2, 10), ("cos", "r", 3, 4), ("sin", "x", 6, 5), ("cos", "t", 5, 3)]):
        g, s = ("cos", 1) if f == "sin" else ("sin", -1)
        rule = (rf"\(\sin a{v} \to a\cos a{v}\): the \({a}\) comes out front and stays in the angle"
                if f == "sin" else
                rf"\(\cos a{v} \to -a\sin a{v}\): the \({a}\) comes out front, stays in the angle, and cos gives a minus")
        work = [rule] + ([rf"\({c} \times {a} = {c * a}\)"] if c != 1 else [])
        add(3, v, FORMS[i % 3], [T(f, c, a)], None, [T(g, s * c * a, a)],
            [("a_forgotten", [T(g, s * c, a)]), ("sign_slip", [T(g, -s * c * a, a)]),
             ("a_dropped_from_angle", [T(g, s * c * a, 1)])], work, [f])


def stage4():
    for i, (v, c, a) in enumerate([("x", 1, 3), ("t", 2, 4), ("z", 5, 2), ("x", 3, 6), ("t", 1, 7), ("r", 4, 3)]):
        work = [rf"\(e^{{a{v}}} \to ae^{{a{v}}}\): the \({a}\) comes down and the power stays the same"] + \
               ([rf"\({c} \times {a} = {c * a}\)"] if c != 1 else [])
        add(4, v, FORMS[i % 3], [T("exp", c, a)], None, [T("exp", c * a, a)],
            [("a_forgotten", [T("exp", c, a)]), ("integrated_instead", [T("exp", F(c, a), a)]),
             ("power_rule_used", [T("xexp", c * a, a)])], work, ["exp"])
    for i, (v, c, a) in enumerate([("x", 1, 4), ("t", 3, 2), ("x", 2, 5), ("r", 6, 3), ("t", 1, 9), ("z", 4, 7)]):
        work = [rf"\(\ln a{v} \to \frac{{1}}{{{v}}}\): the \({a}\) cancels out, \(\frac{{{a}}}{{{a}{v}}} = \frac{{1}}{{{v}}}\)"] + \
               ([rf"\({c} \times \frac{{1}}{{{v}}} = \frac{{{c}}}{{{v}}}\)"] if c != 1 else [])
        add(4, v, FORMS[(i + 1) % 3], [T("ln", c, a)], None, [T("over", c, 1)],
            [("a_kept", [T("over", c * a, 1)]), ("a_divided", [T("over", c, a)]), ("ln_flipped", [T("recipln", c, a)])],
            work, ["ln"])


def stage5():
    for i, (v, p, q, n, k) in enumerate([("t", 5, 2, 3, None), ("t", 4, 3, 2, None), ("x", 2, 5, 4, None),
                                         ("t", 7, 2, 5, None), ("r", 3, 4, 3, None), ("t", 6, 2, 4, None),
                                         ("t", 2, 3, 3, 9), ("x", 8, 2, 2, 4), ("t", 5, 6, 2, -3), ("t", 9, 1, 4, 7),
                                         ("z", 4, 5, 3, None), ("t", 3, 7, 2, -8)]):
        qt = [T("pow", p, 1), T("pow", q, n)] + ([T("const", k)] if k is not None else [])
        ans = [T("const", p), T("pow", q * n, n - 1)]
        decoys = [("kept_variable", [T("pow", p, 1), T("pow", q * n, n - 1)]), ("power_kept", [T("const", p), T("pow", q * n, n)])]
        decoys.append(("constant_kept", ans + [T("const", k)]) if k is not None else ("coeff_lost", [T("const", p), T("pow", n, n - 1)]))
        work = [r"Differentiate each term on its own:",
                rf"\({tex([T('pow', p, 1)], v)} \to {p}\)",
                rf"\({tex([T('pow', q, n)], v)} \to {tex([T('pow', q * n, n - 1)], v)}\)"]
        if k is not None:
            work.append(rf"\({k}\) on its own is a constant: it doesn't change, so it differentiates to \(0\)")
        add(5, v, "fn" if i % 4 != 3 else "wrt", qt, None, ans, decoys, work, ["x", "axn"])


# Which stages each named error may appear in: a key's feedback line is written for these stages only.
ERR_STAGES = {
    "power_kept": {1, 2, 5}, "coeff_lost": {1, 5}, "new_power_used": {1}, "kept_variable": {1, 5}, "treated_as_constant": {1},
    "sign_lost": {2}, "power_wrong_way": {2}, "bottom_differentiated": {2}, "root_upside_down": {2},
    "a_forgotten": {3, 4}, "sign_slip": {3}, "a_dropped_from_angle": {3},
    "integrated_instead": {4}, "power_rule_used": {4}, "a_kept": {4}, "a_divided": {4}, "ln_flipped": {4},
    "constant_kept": {5},
}
ROWS = ["x", "axn", "sin", "cos", "exp", "ln"]


def bank():
    items.clear()
    stage1(); stage2(); stage3(); stage4(); stage5()
    return list(items)


# ------------------------------------------------------------------------------------------------ checks
def check(bank_items):
    from collections import Counter
    assert Counter(i["stage"] for i in bank_items) == {1: 12, 2: 12, 3: 12, 4: 12, 5: 12}
    assert len({i["id"] for i in bank_items}) == 60 and len({i["prompt"] for i in bank_items}) == 60
    for it in bank_items:
        opts = [it["answer"]] + it["decoys"]
        assert len(it["decoys"]) == 3 and len({o["tex"] for o in opts}) == 4, it["id"]
        for x in POINTS:
            h = 1e-6
            d = (value(it["q"], x + h) - value(it["q"], x - h)) / (2 * h)
            assert abs(d - value(it["answer"]["terms"], x)) < 1e-4 * max(1, abs(d)), (it["id"], x)
        for i in range(4):
            for j in range(i + 1, 4):
                gap = max(abs(value(opts[i]["terms"], x) - value(opts[j]["terms"], x)) for x in POINTS)
                assert gap > 1e-3, (it["id"], opts[i]["tex"], opts[j]["tex"])
        for d in it["decoys"]:
            assert it["stage"] in ERR_STAGES[d["err"]], (it["id"], d["err"])
        assert it["rows"] and set(it["rows"]) <= set(ROWS)
    return True


if __name__ == "__main__":
    b = bank()
    check(b)
    blob = "".join(json.dumps(i, separators=(",", ":"), ensure_ascii=False) + "\n" for i in b)
    print("total", len(b))
    print("sha256", hashlib.sha256(blob.encode("utf-8")).hexdigest())
    if "--out" in sys.argv:
        open(sys.argv[sys.argv.index("--out") + 1], "w", encoding="utf-8", newline="\n").write(blob)
    if "--show" in sys.argv:
        for i in b:
            print(i["id"], "|", i["prompt"], "|", i["answer"]["tex"], "|", [(d["err"], d["tex"]) for d in i["decoys"]])
            for w in i["working"]:
                print("     ", w)
```
