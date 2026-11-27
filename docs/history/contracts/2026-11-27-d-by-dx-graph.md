D-BY-DX-GRAPH (Project Claude, Fri 27 Nov 2026 20:15; checked against main e91a25a)
Jon, 27 Nov 2026, 18:11-18:50 (rulings listed in ROOT CAUSE); 19:22: this goes before every other queued contract. Spec: Project Claude's d-by-dx-graph spec of 27 Nov (its content is all below; nothing else is needed).
RECOMMENDED: Claude Code, Opus 5.5, effort high. A new shared asset (the plotter), a game rebuilt round a regenerated bank, its verifier, the large-screen layer joined.
LANE: home. SEND: now. First commit carries NEXT-NO-FALLBACK's close-out (AGENTS.md:62): #937 squash-merged as e91a25a at 19:38 UTC, 27 Nov, on a green Gate at 1640c8e0 (check-site 46055742396, phone-fit-full 46055742477); merge-pr.py's last line "main e91a25a run 46058091551: GREEN"; main's runs on e91a25a: check-site 46058091551, phone-fit-full 46058091615, pages 46058090668, each success; move docs/handover/contracts/2026-11-27-next-no-fallback.md to docs/history/contracts/. Save this contract verbatim as docs/handover/contracts/2026-11-27-d-by-dx-graph.md in the same commit.
TIER: Medium (merge on green; the game stays unlisted; Jon plays it after).

TASK: Give d by dx? Why? its graph (f with the question, the gradient function f' drawn over it once answered) through a new shared plotter, with its start-screen animation, a regenerated bank (notation, readable numbers, Stage 2 answers written back, board-style working), Next after a right answer, and the large-screen layer.

ROOT CAUSE (Jon's rulings, 27 Nov 2026, and the facts they rest on; file:line on e91a25a):
- The graph (18:11): "draw the graph as part of the question, when you get the answer draw the gradient line on the same graph in a different colour, really hammer home that we are finding the gradient function". The function, not a tangent (18:13). The student's wrong option is never drawn: "just muddies the water" (18:15). Beside the question on laptops, a fold-out on phones (18:15). A shared plotter, used here first and by integration's check step later; a follow-up moves the other graphing games onto it (18:15). No shared plotter exists: Y So Steep?, Graph Transformer, Graph Sketcher and Gradient Hunter each draw their own canvas.
- Numbers (18:18): "change the numbers so that the graphs are readable". For k sin at, k cos at and k e^(at), f' is a times as tall as f in any window; with a up to 10 (bank items s3-04, s3-07, s3-08, s3-09, s3-11, s4-04, s4-05) f was a flat ripple. Rule: neither curve more than 4 times the other's height over the item's window; the new bank meets it for every item.
- Notation (18:16-18:18): 16 prompts said only "Differentiate: ..." (no variable named) and none asked for dy/dx. Every prompt now names its variable; three forms, 20 items each; not always x and y; Leibniz always a stacked \dfrac; every fraction on the line \dfrac (a fraction in a power stays \frac).
- Index laws both ways (18:21): Stage 2's options come back in the question's form: -6/r^2, (5/2)sqrt(x^3), 2/(3 cbrt r).
- The working (18:44): board-style, one line per move, each following from the one before, with a short label beside it. The wrong answer's "The answer is ..." line goes (18:32): games/d-by-dx-why/index.html:495.
- A right answer waits for Next (18:30-18:32): today it moves on after RIGHT_MS = 1000 (:262, :486), before the drawn f' can be seen. Canon §7.6 now says a right answer that reveals something new waits for Next (NEXT-NO-FALLBACK, #937).
- The start screen (18:48-18:50): two pens draw f and f' together at the same x; three pairs in turn, looping, each left to settle; equations written in; none of them a question in the game.
- Big screens (18:19, a 2560 px screenshot): "bigger answer boxes"; the game is not one of the large-screen layer's pilot pages (schools/assets/large-screen.js, #927).
- A placeholder slip line of Project Claude's is untrue on cube roots: root_upside_down (:356) "A square root is the power 1/2 ...".

CLASS CHECK: The plotter is a class fix: the same job (axes, curves, labels) is done four times in four games' own canvases, and this game and integration's check step would make six. One shared SVG plotter in schools/assets/; this game uses it first; the four existing games move onto it in a follow-up (step 9's todo row), not here. Everything else is local to this game: its bank, page, verifier and placeholder lines, which no other game reads.

EXACT CHANGE:
1. tools/d-by-dx-why/bank.py: replace it with the generator at the end of this contract, verbatim. It prints total 60 and sha256 c6c0c8dce9658c16d4d37fa6094320a3cdeb84685203fa0d3f8e6d5d9bb7c960, and runs check() and check_start(). Embed its items in the page's BANK one item a line, as now, and START_SHOW's pairs (start_show()) as data beside it. Each item now has "dep", "graph" {"x", "y", "ticks"}, "back", and "working" as a list of {"why", "lhs", "rhs"} (bare TeX); "prompt" is final text with \( \) maths.
2. schools/assets/plot.js (new; window.MaffsPlot), SVG, no canvas, no dependency beyond KaTeX:
   - Draws one pair of axes over a window [x0, x1] x [y0, y1] the caller gives (it never chooses one): axes through 0 where 0 is in the window, otherwise along the edge; a light grid at nice steps; ticks at nice numbers, or multiples of pi/2 when ticks is "pi".
   - Curves are functions of one letter, sampled at least once per 2 px of width; a non-finite value breaks the line, never joins across it.
   - All text is KaTeX in an HTML layer over the SVG: tick labels, the axis letters (the item's own: t and s, r and A, x and y, or the letter and f), each curve's label at its right-hand end in its curve's colour.
   - A curve added later draws in left to right over about 0.6 s (prefers-reduced-motion: at once). A "pens" mode draws two curves together at the same x, each with a blinking tip (the start screen).
   - Colours from the page's CSS variables; the two curves also differ in width or dash, never colour alone; each curve's colour 3:1 or better against the background.
   - viewBox scaling; each curve's path carries data attributes naming the curve and window, so a verifier can map pixels back to values.
   - A header comment saying what it is for and who uses it, as the other shared assets have.
3. games/d-by-dx-why/index.html, the graph:
   - With the question: f on the item's window, labelled as the prompt names it (f(t), or y, s or A).
   - On answering, right or wrong: the true f' draws in over f, labelled f'(t) or a stacked \dfrac{ds}{dt}. Never a decoy.
   - 1024 px wide and over: the graph beside the question and options; the derivative table where it is. Narrower: a "Graph" fold-out, closed while the question stands; after answering its button reads "See the gradient function"; it closes on Next. Nothing pushes Next below the fold (canon §7.6.1). Pro mode: the graph unchanged.
4. The same page, answering:
   - A right answer: "Right" with the answer, f' draws in, then Next through the shared control (schools/assets/next-control.js; Enter or Space advances); it never moves on by itself. Its floor is no longer than the f' draw-in: if the helper cannot take a floor per call, add an optional floorMs option to it (default and every existing caller unchanged) with a case in scripts/test-next-control.py.
   - A wrong answer: the slip's line, the working, the table rows, Next. The "The answer is" line (:495) goes.
   - The working is laid out as label | lhs | = rhs, the "=" signs aligned, all maths in KaTeX; below 1024 px each label sits above its line in small text.
   - LINES: root_upside_down becomes "A root is a fractional power: the root's number goes on the bottom." (a placeholder, as the others; the comment above LINES stays).
5. The start screen: the plotter in pens mode over START_SHOW's three pairs, about 4 s drawing each, the finished pair settling about 3 s before the next, looping; as each pair's pens finish, y = ... and a stacked dy/dx = ... are written under the graph. prefers-reduced-motion: the first pair finished and still, with its labels. A hidden tab pauses the loop. Sized as other start art (40% to full size), never pushing Play below the fold at 320 x 568, 375 x 667, 1280 x 720 or 1920 x 1080, normal or Aa.
6. Big screens: the page joins the large-screen layer (scripts/check-large-screen.py MIGRATED, a measurement for every stage and Pro by scripts/measure-large-screen.py, scripts/apply-large-screen.py). Options' maths at least 1.35 x the body size, padding to match. If larger maths breaks the 375 x 667 Aa fold, the size steps down below 1024 px, never the fold.
7. scripts/verify-d-by-dx-why.py, kept independent of the generator (it reads ERR_STAGES and START_SHOW as data, never runs it):
   - SHA256 (:72) becomes the new digest; prompts, TeX, working and the Stage 2 written-back forms re-rendered by its own code from terms (its renderer, :126-254, updated to the new conventions), and every working line checked in sympy to equal the question's function (lhs f(..) or y/s/A) or its derivative (an f' or d../d.. lhs, and every continuation line after one).
   - Graph: for every item, both curves finite and inside its y-range at every sample of its window, and neither curve more than 4 times the other's height; the drawn path's sampled points map back to f and f' within 1 px.
   - Play: a right answer draws f' and waits for Next (no advance in 30 s on a fast clock); a wrong answer draws the true f', never the chosen decoy; no "The answer is" line.
   - Start screen: each START_SHOW pair is a function and its derivative (sympy), none equal to any bank question, each readable as above; pens at the same x at every sample; reduced motion shows the first pair still.
   - Fit: the existing fit units at their sizes, normal and Aa, with the graph and the fold-out, plus the start screen at the four sizes in step 5.
   - Plants, each must FAIL: a decoy drawn on the graph; a right answer that advances by itself; a START_SHOW pair equal to a bank question; a working line that is not equal to its side; f' drawn as a tangent at a point.
8. scripts/test-plot.py (or the plotter's own check, named in the report), in CI: axes and ticks for a window, a curve broken at a non-finite value, pi ticks, the reveal and pens modes, reduced motion, pixel readback. Plants for each.
9. docs/todo.md: a row PLOT-MIGRATE (move Y So Steep?, Graph Transformer, Graph Sketcher and Gradient Hunter onto schools/assets/plot.js where they only draw; their interaction stays in the page; Jon, 27 Nov 2026), and the D-BY-DX row's Phase 1 text updated to say the graph is built. docs/handover/home.md entry. /updates/: none (the game is unlisted).

DO NOT TOUCH:
- The four other graphing games; every other game; the derivative table's content (as on Jon's paper); the Pro switch's behaviour and boards; the leaderboard boards and keys.
- schools/assets/next-control.js beyond the optional floorMs option in step 4; large-screen.js; site-nav.js.
- Every LINES line except root_upside_down; the tagline and look placeholders (Jon's to write).
- scripts/merge-pr.py; every workflow; canon (§7.6 already has the rule); docs/handover/cloud.md.
- No force-push.

SUCCESS CONDITION:
- The bank as generated, sha256 c6c0c8dc...bb7c960, embedded; the generator's check() and check_start() pass.
- The plotter in schools/assets/ with its check and plants in CI; the game uses it for the question graph, the reveal and the start screen as above.
- The verifier's new checks and five plants run in CI; every existing unit passes, updated to the new bank; the large-screen measurement committed and its check green.
- todo row added; home.md entry; merged on green through python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600, run from main's checkout (merge main in and re-run if main moves first); last line and main's run IDs in home.md; a screenshot of a wrong answer at 1366 x 768 with f and f' drawn, in the report to Jon.

STOP IF:
- The generator below does not print total 60 and the digest above, or its checks fail: report it; do not edit it.
- An item's graph cannot meet its fold at a measured size without dropping the graph on that size: report the item and size.
- The large-screen layer cannot measure the page (for example, the fold-out or the start animation defeats it): report it; join it without the start screen only if the report says why.
- Adding floorMs to next-control.js would change any existing caller's behaviour: report it.
- main is red when you come to merge: report it; do not use --override.
- merge-pr.py cannot reach GitHub or refuses: report its output; do not merge another way.

THE GENERATOR (tools/d-by-dx-why/bank.py, verbatim):
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
FORMS = ["wrt", "leib", "fn"]
# The dependent letter for the wrt and leib forms (Jon, 27 Nov 2026: "we need students to not always look at x and y"):
# A for r, as the mock's A = 3r^2; s for every other t item; y otherwise. The fn form always uses f.
def dep(v, k):
    return "A" if v == "r" else ("s" if v == "t" and k % 2 == 0 else "y")



def fs(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def T(kind, *args):
    return [kind] + [fs(a) for a in args]


# ------------------------------------------------------------------------------------------------ TeX
def frac_tex(x, big=False):
    """A number. big: a stacked \\dfrac (Jon, 27 Nov 2026: "proper fractions"), for every fraction on the line;
    a fraction in a power stays \\frac (a \\dfrac there would be taller than the line)."""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    return ("-" if x < 0 else "") + (r"\dfrac{%d}{%d}" if big else r"\frac{%d}{%d}") % (abs(x.numerator), x.denominator)


def coef(c, lead, attach=True):
    c = F(c)
    sign = "-" if c < 0 else ("" if lead else "+")
    a = abs(c)
    if a == 1 and attach:
        return sign
    return sign + frac_tex(a, big=True)


def ang(a, v):
    a = F(a)
    return v if a == 1 else f"{frac_tex(a)}{v}"


def root_tex(v, n):
    """v^n for a positive fraction n = m/k (k > 1) as a root: v^(3/2) -> sqrt(v^3), v^(2/3) -> cbrt(v^2)."""
    m, k = n.numerator, n.denominator
    inner = v if m == 1 else f"{v}^{{{m}}}"
    return (r"\sqrt{%s}" % inner) if k == 2 else (r"\sqrt[%d]{%s}" % (k, inner))


def back_tex(t, v, lead):
    """A power term written back in the question's form (Stage 2; Jon, 27 Nov 2026: "try and get them to remember
    their index laws"): a negative power as a fraction with a positive power, a fractional power as a root."""
    c, n = F(t[1]), F(t[2])
    sign = "-" if c < 0 else ("" if lead else "+")
    a = abs(c)
    if n == 0:
        return coef(c, lead, attach=False)
    if n > 0:
        body = root_tex(v, n) if n.denominator > 1 else (v if n == 1 else f"{v}^{{{n}}}")
        return coef(c, lead) + body
    p = -n
    body = root_tex(v, p) if p.denominator > 1 else (v if p == 1 else f"{v}^{{{p}}}")
    den = ("" if a.denominator == 1 else str(a.denominator)) + body
    return sign + r"\dfrac{%d}{%s}" % (a.numerator, den)


def term_tex(t, v, lead, back=False):
    k, args = t[0], [F(x) for x in t[1:]]
    c = args[0]
    if back and k == "pow":
        return back_tex(t, v, lead)
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
        return sign + r"\dfrac{%s}{%s}" % (frac_tex(abs(c)), v if d == 1 else f"{frac_tex(d)}{v}")
    if k == "overpow":
        d, m = args[1], args[2]
        return sign + r"\dfrac{%s}{%s%s}" % (frac_tex(abs(c)), frac_tex(d), v if m == 1 else f"{v}^{{{frac_tex(m)}}}")
    if k == "recipln":
        return sign + r"\dfrac{%s}{\ln %s}" % (frac_tex(abs(c)), ang(args[1], v))
    raise ValueError(k)


def tex(terms, v, back=False):
    return "".join(term_tex(t, v, i == 0, back) for i, t in enumerate(terms))


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
def prompt(form, v, q, y):
    """Every prompt names its variable (Jon, 27 Nov 2026). Leibniz is always a stacked fraction, never d/dx with a slash."""
    if form == "wrt":
        return rf"Differentiate \({y} = {q}\) with respect to \({v}\)"
    if form == "leib":
        return rf"\({y} = {q}\). Find \(\dfrac{{d{y}}}{{d{v}}}\)"
    return rf"If \(f({v}) = {q}\), find \(f'({v})\)"


# The working, board-style (Jon, 27 Nov 2026, 18:44): the maths as a teacher writes it on the board, one line per move,
# each line following from the one before, with a short label in the margin naming the move. A step is
# (label, side, rhs): side "f" puts the function on the left (f(t), or y, s, A), "d" its derivative (f'(t), or the
# stacked dy/dt), "" nothing (a line that carries on with "="). rhs is bare TeX.
def lhs_of(side, form, v, y):
    if side == "f":
        return f"f({v})" if form == "fn" else y
    if side == "d":
        return f"f'({v})" if form == "fn" else rf"\dfrac{{d{y}}}{{d{v}}}"
    return ""


def factor(x):
    """A number as a second factor: a negative one in brackets."""
    t = frac_tex(x, big=True)
    return f"({t})" if F(x) < 0 else t


def power_down(c, n, v):
    """c v^n -> c x n v^(n-1), written before tidying."""
    c, n = F(c), F(n)
    p = rf"{v}^{{{frac_tex(n)}-1}}"
    if c == 1:
        return frac_tex(n, big=True) + p
    return rf"{frac_tex(c, big=True)} \times {factor(n)}\,{p}"


def pow_steps(c, n, v):
    return [("power down, take one off", "d", power_down(c, n, v)),
            ("tidy up", "", tex([T("pow", F(c) * F(n), F(n) - 1)], v))]

# ------------------------------------------------------------------------------------------------ the graph
# Jon, 27 Nov 2026: draw f with the question and f' over it once answered, "really hammer home that we are finding
# the gradient function". Both curves share one pair of axes (a gradient is in the same units on the same picture).
# READABLE: neither curve's height in its window is more than this many times the other's (checked below); the
# item numbers were changed until every item passes (Jon: "change the numbers so that the graphs are readable").
READABLE = 4
SAMPLES = 400


def window(stage, q):
    """(lo, hi, ticks) for the item's own letter: a window inside the function's domain, chosen by family."""
    k = q[0][0]
    if stage == 3:
        return 0.0, 2 * math.pi, "pi"                       # labelled in multiples of pi/2
    if k == "exp":
        a = float(F(q[0][2]))
        return -2 / a, 1 / a, "num"                         # e^(at) from e^-2 to e^1 of its size
    if k == "ln":
        return 0.2, 4.0, "num"                              # ln needs a positive letter
    if stage == 2:
        n = F(q[0][2])
        if n < 0:
            return max(0.5, float(-n) / READABLE), 3.0, "num"   # clear of the asymptote at 0, f' within READABLE of f
        return 0.25, 4.0, "num"                             # fractional powers: positive letter only
    return -2.0, 2.0, "num"                                 # powers and sums: both sides of 0, so even powers show f' = 0


def nice_out(lo, hi):
    span = (hi - lo) or 1.0
    step = 10 ** math.floor(math.log10(span)) / 2
    return math.floor(lo / step) * step, math.ceil(hi / step) * step


def graph(stage, q, ans):
    lo, hi, ticks = window(stage, q)
    xs = [lo + (hi - lo) * i / SAMPLES for i in range(SAMPLES + 1)]
    f = [value(q, x) for x in xs]
    g = [value(ans, x) for x in xs]
    ys = f + g + [0.0]
    pad = 0.08 * (max(ys) - min(ys))
    ylo, yhi = nice_out(min(ys) - pad, max(ys) + pad)
    return {"x": [round(lo, 6), round(hi, 6)], "y": [ylo, yhi], "ticks": ticks}


def readable(it):
    """max |f| / max |f'| and its inverse over the item's window: both at most READABLE."""
    lo, hi = it["graph"]["x"]
    xs = [lo + (hi - lo) * i / SAMPLES for i in range(SAMPLES + 1)]
    mf = max(abs(value(it["q"], x)) for x in xs)
    mg = max(abs(value(it["answer"]["terms"], x)) for x in xs)
    return max(mf / mg, mg / mf)


# ------------------------------------------------------------------------------------------------ the bank
items = []


def add(stage, v, form, q_terms, q_tex, answer, decoys, working, rows, back=False):
    n = sum(1 for i in items if i["stage"] == stage) + 1
    qt = q_tex if q_tex is not None else tex(q_terms, v)
    ans_tex = tex(answer, v, back)
    if back:   # the last step: write the answer back in the question's form
        working = working + [("write it back", "", ans_tex)]
    y = "f" if form == "fn" else dep(v, n)
    assert working[-1][2] == ans_tex, (stage, n, working[-1][2], ans_tex)   # the chain ends on the answer
    items.append({"id": f"s{stage}-{n:02d}", "stage": stage, "var": v, "form": form, "dep": y, "q": q_terms, "qtex": qt,
                  "prompt": prompt(form, v, qt, y),
                  "graph": graph(stage, q_terms, answer),
                  "answer": {"tex": ans_tex, "terms": answer},
                  "decoys": [{"err": e, "tex": tex(t, v, back), "terms": t} for e, t in decoys],
                  "back": back,
                  "rows": rows,
                  "working": [{"why": w, "lhs": lhs_of(sd, form, v, y), "rhs": r} for w, sd, r in working]})


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
            [("the letter goes, the number stays", "d", frac_tex(a))],
            ["x"])


def stage2():
    for i, (v, a, n) in enumerate([("x", 3, 2), ("t", 4, 3), ("r", 6, 1), ("x", 5, 4), ("z", 8, 2), ("t", -2, 3)]):
        den = v if n == 1 else f"{v}^{n}"
        qt = (r"\dfrac{%d}{%s}" % (a, den)) if a > 0 else (r"-\dfrac{%d}{%s}" % (-a, den))
        bottom = [T("overpow", a, n, n - 1)] if n > 1 else [T("const", a)]
        add(2, v, FORMS[i % 3], [T("pow", a, -n)], qt, [T("pow", -a * n, -n - 1)],
            [("sign_lost", [T("pow", a * n, -n - 1)]), ("power_wrong_way", [T("pow", -a * n, -n + 1)]),
             ("bottom_differentiated", bottom)],
            [("rewrite as a power", "f", tex([T('pow', a, -n)], v))] + pow_steps(F(a), F(-n), v), ["axn"], back=True)
    for i, (v, c, m, k) in enumerate([("x", 1, 5, 2), ("r", 1, 2, 3), ("t", 4, 3, 2), ("x", 1, 7, 2), ("r", 6, 4, 3),
                                      ("t", 2, 5, 3)]):
        root = (r"\sqrt{%s^{%d}}" % (v, m)) if k == 2 else (r"\sqrt[%d]{%s^{%d}}" % (k, v, m))
        qt = ("" if c == 1 else str(c)) + root
        p = F(m, k)
        add(2, v, FORMS[(i + 1) % 3], [T("pow", c, p)], qt, [T("pow", c * p, p - 1)],
            [("root_upside_down", [T("pow", F(c) / p, 1 / p - 1)]), ("power_kept", [T("pow", c * p, p)]),
             ("power_wrong_way", [T("pow", c * p, p + 1)])],
            [("root to a power: its number on the bottom", "f", tex([T('pow', c, p)], v))]
            + pow_steps(F(c), p, v), ["axn"], back=True)


def stage3():
    for i, (f, v, c, a) in enumerate([("sin", "x", 1, 4), ("cos", "t", 1, 3), ("sin", "t", 3, 2), ("cos", "x", 2, 3),
                                      ("sin", "r", 5, 3), ("cos", "t", 4, 2), ("sin", "x", 1, 3), ("cos", "z", 1, 4),
                                      ("sin", "t", 2, 4), ("cos", "r", 3, 4), ("sin", "x", 6, 2), ("cos", "t", 5, 3)]):
        g, s = ("cos", 1) if f == "sin" else ("sin", -1)
        A = ang(a, v)
        if f == "sin":
            first = ("a out front, and in the angle", "d", (rf"{a}\cos {A}" if c == 1 else rf"{c} \times {a}\cos {A}"))
        else:
            first = ("a out front; cos gives a minus", "d", (rf"-{a}\sin {A}" if c == 1 else rf"{c} \times ({-a})\sin {A}"))
        work = [first] + ([("tidy up", "", tex([T(g, s * c * a, a)], v))] if c != 1 else [])
        add(3, v, FORMS[i % 3], [T(f, c, a)], None, [T(g, s * c * a, a)],
            [("a_forgotten", [T(g, s * c, a)]), ("sign_slip", [T(g, -s * c * a, a)]),
             ("a_dropped_from_angle", [T(g, s * c * a, 1)])], work, [f])


def stage4():
    for i, (v, c, a) in enumerate([("x", 1, 3), ("t", 2, 4), ("z", 5, 2), ("x", 3, 2), ("t", 1, 4), ("r", 4, 3)]):
        E = rf"e^{{{ang(a, v)}}}"
        work = [("a comes down; the power stays", "d", (rf"{a}{E}" if c == 1 else rf"{c} \times {a}{E}"))] + \
               ([("tidy up", "", tex([T("exp", c * a, a)], v))] if c != 1 else [])
        add(4, v, FORMS[i % 3], [T("exp", c, a)], None, [T("exp", c * a, a)],
            [("a_forgotten", [T("exp", c, a)]), ("integrated_instead", [T("exp", F(c, a), a)]),
             ("power_rule_used", [T("xexp", c * a, a)])], work, ["exp"])
    for i, (v, c, a) in enumerate([("x", 1, 4), ("t", 3, 2), ("x", 2, 5), ("r", 6, 3), ("t", 1, 9), ("z", 4, 7)]):
        work = [("ln: the a cancels", "d", (rf"\dfrac{{1}}{{{v}}}" if c == 1 else rf"{c} \times \dfrac{{1}}{{{v}}}"))] + \
               ([("tidy up", "", tex([T("over", c, 1)], v))] if c != 1 else [])
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
        first = rf"{p} + {power_down(q, n, v)}" + (" + 0" if k is not None else "")
        work = [("each term on its own" + ("; a number alone goes to 0" if k is not None else ""), "d", first),
                ("tidy up", "", tex(ans, v))]
        add(5, v, FORMS[i % 3], qt, None, ans, decoys, work, ["x", "axn"])


# The start screen (Jon, 27 Nov 2026, 18:48-18:50): two pens draw f and f' together, always at the same x, so f''s pen
# crests a hill exactly as f''s pen crosses the axis; three pairs in turn, looping, each left to settle before the next;
# each pair's equations written in as its pens finish. None of them may be a question in the game (checked below).
# Each passes READABLE on its own window. Terms as the bank's.
START_SHOW = [
    {"q": [T("pow", 1, 3), T("pow", -3, 1)], "d": [T("pow", 3, 2), T("const", -3)], "x": [-2.2, 2.2]},
    {"q": [T("pow", F(1, 4), 4), T("pow", -2, 2)], "d": [T("pow", 1, 3), T("pow", -4, 1)], "x": [-3.0, 3.0]},
    {"q": [T("pow", F(1, 5), 5), T("pow", F(-4, 3), 3), T("pow", 3, 1)], "d": [T("pow", 1, 4), T("pow", -4, 2), T("const", 3)],
     "x": [-2.2, 2.2]},
]


def start_show():
    out = []
    for p in START_SHOW:
        lo, hi = p["x"]
        xs = [lo + (hi - lo) * i / SAMPLES for i in range(SAMPLES + 1)]
        f = [value(p["q"], x) for x in xs]
        g = [value(p["d"], x) for x in xs]
        ys = f + g + [0.0]
        pad = 0.08 * (max(ys) - min(ys))
        ylo, yhi = nice_out(min(ys) - pad, max(ys) + pad)
        out.append({"q": p["q"], "d": p["d"], "qtex": tex(p["q"], "x"), "dtex": tex(p["d"], "x"),
                    "graph": {"x": [lo, hi], "y": [ylo, yhi], "ticks": "num"}})
    return out


def check_start(bank_items):
    for p in start_show():
        lo, hi = p["graph"]["x"]
        xs = [lo + (hi - lo) * i / SAMPLES for i in range(SAMPLES + 1)]
        mf = max(abs(value(p["q"], x)) for x in xs)
        mg = max(abs(value(p["d"], x)) for x in xs)
        assert max(mf / mg, mg / mf) <= READABLE, p["qtex"]
        for x in POINTS:   # p["d"] is the derivative of p["q"]
            h = 1e-6
            assert abs((value(p["q"], x + h) - value(p["q"], x - h)) / (2 * h) - value(p["d"], x)) < 1e-4 * max(1, abs(value(p["d"], x)))
        for it in bank_items:  # never a question in the game, in any letter (Jon, 18:50)
            assert max(abs(value(p["q"], x) - value(it["q"], x)) for x in POINTS) > 1e-6, (p["qtex"], it["id"])
    return True


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
        assert readable(it) <= READABLE + 1e-9, (it["id"], round(readable(it), 2))
        lo, hi = it["graph"]["x"]
        for x in (lo + (hi - lo) * i / SAMPLES for i in range(SAMPLES + 1)):
            for terms in (it["q"], it["answer"]["terms"]):
                yv = value(terms, x)
                assert math.isfinite(yv) and it["graph"]["y"][0] <= yv <= it["graph"]["y"][1], (it["id"], x)
    from collections import Counter as C
    assert set(C(i["form"] for i in bank_items).values()) == {20}, C(i["form"] for i in bank_items)
    return True


if __name__ == "__main__":
    b = bank()
    check(b)
    check_start(b)
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
