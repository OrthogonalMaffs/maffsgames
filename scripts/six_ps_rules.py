"""Rules every The 6 P's bank must pass, whichever game it came from (SIX-PS-REVIEW-FIXES, 27 Oct 2026).

An independent review of 1,805 questions found every stored answer correct but a handful of faults of eight kinds. Each is a
rule here, run over every bank by `gen-six-ps.py --check`, with a planted case in `selftest()` that must be caught:

  a  no choice question has two options of equal value
  b  a question whose accept rule is "simplest" says "simplest form" (or "lowest terms") in its stem
  c  a slip is stored at the full-precision value of its misconception, not rounded  (per-topic recomputation, SLIP_RULES)
  d  the last worked line states the stored answer
  e  no text shows a raw backslash or escape (outside maths)
  f  a diagram whose working uses a right angle marks it
  g  every likelihood item stores the probability its word comes from, and the word matches that probability's band
  h  words are never typeset inside KaTeX: maths only (numbers, expressions, P(red)); context and instructions are plain text

`faults(q)` is one question's faults as [(rule letter, message)]. Pure functions, no browser: the planted cases run in
milliseconds.
"""
import math
import re
from fractions import Fraction

# ─────────────────────────────── helpers ───────────────────────────────
MATH = re.compile(r"\\\((.*?)\\\)", re.S)
UNITS = {"m", "cm", "mm", "km", "kg", "g", "mg", "l", "ml", "s", "h", "min", "mph", "p", "m/s", "km/h", "g/cm", "kg/m", "cm^2",
         "m^2", "cm^3", "m^3", "N", "Pa", "mins", "hrs", "secs", "sec", "hr", "ml", "cl", "tonnes", "°C", "cm²", "m²", "km²"}
# the letters of a macro are not words
MACRO = re.compile(r"\\[a-zA-Z]+")


def texts(q):
    """(where, text) for every string a student reads in a question."""
    out = [("stem", q.get("stem", ""))]
    out += [("option %s" % o.get("val"), o.get("label", "")) for o in q.get("options") or []]
    out += [("worked %d" % (i + 1), w) for i, w in enumerate(q.get("worked") or [])]
    out += [("slip %d" % (i + 1), s.get("line", "")) for i, s in enumerate(q.get("slip") or [])]
    return out


def outside_maths(s):
    return MATH.sub(" ", s)


def label_value(label):
    """A label's numeric value (Fraction or float) when it is a plain number or a simple power/fraction/root; else None."""
    s = label.replace("\\(", "").replace("\\)", "").strip()
    s = s.replace("\\dfrac", "\\frac").replace("\\times", "*").replace("\\div", "/").replace("\\cdot", "*").replace("−", "-")
    s = s.replace("\\left", "").replace("\\right", "").replace("\\,", "").replace("\\ ", "").replace("\\!", "")
    s = re.sub(r"\\text\{[^}]*\}|\\mathrm\{[^}]*\}", "", s)
    s = s.replace("£", "").replace("°", "").replace("%", "/100")
    s = re.sub(r"(?<=\d),(?=\d{3}\b)", "", s)                  # a comma is a thousands separator only before three digits
    for _ in range(4):
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
        s = re.sub(r"\\sqrt\[(\d+)\]\{([^{}]*)\}", r"((\2)**(1/\1))", s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", r"((\1)**0.5)", s)
    s = re.sub(r"\^\{([^{}]*)\}", r"**(\1)", s)
    s = s.replace("^", "**").replace("{", "(").replace("}", ")")
    s = re.sub(r"(?<=\d)\s*\(", "*(", s)                       # 3(4) and a mixed number are not both handled: only the first
    if re.search(r"[A-Za-z\\]", s):
        return None
    try:
        v = eval(s, {"__builtins__": {}}, {})
    except Exception:
        return None
    return v if isinstance(v, (int, float, Fraction)) else None


def same_value(a, b):
    va, vb = label_value(a), label_value(b)
    if va is not None and vb is not None:
        return math.isclose(float(va), float(vb), rel_tol=1e-9, abs_tol=1e-12)
    na = re.sub(r"\s+|\\dfrac|\\frac|\\left|\\right", "", a)
    nb = re.sub(r"\s+|\\dfrac|\\frac|\\left|\\right", "", b)
    return na == nb


# ─────────────────────────────── (a) ───────────────────────────────
def rule_a(q):
    if q.get("format") != "choice":
        return []
    o = q.get("options") or []
    out = []
    for i in range(len(o)):
        for j in range(i + 1, len(o)):
            if same_value(o[i]["label"], o[j]["label"]):
                out.append(("a", "options %s and %s are equal in value: %s | %s" % (o[i]["val"], o[j]["val"], o[i]["label"], o[j]["label"])))
    return out


# ─────────────────────────────── (b) ───────────────────────────────
def rule_b(q):
    if (q.get("accept") or {}).get("rule") == "simplest" and not re.search(r"simplest form|lowest terms|simplest", q.get("stem", ""), re.I):
        return [("b", "accepts only the simplest form but the stem does not say 'simplest form'")]
    return []


# ─────────────────────────────── (e) ───────────────────────────────
def rule_e(q):
    out = []
    for where, t in texts(q):
        o = outside_maths(t)
        if "\\" in o:
            out.append(("e", "%s shows a backslash outside maths: %r" % (where, o[max(0, o.index("\\") - 12):o.index("\\") + 12])))
    return out


# ─────────────────────────────── (h) ───────────────────────────────
def _words_in_maths(m):
    """The words inside one \\( ... \\), or []. A unit or a single label in \\text{} is allowed."""
    found = []
    for t in re.findall(r"\\(?:text|mathrm|textbf|mbox)\{([^{}]*)\}", m):
        w = t.strip()
        if not w or w in UNITS or re.fullmatch(r"[A-Za-z]+(?:/[A-Za-z]+)?\^?\d?", w):
            continue                                              # a unit, or a single label (one word)
        found.append(w)
    rest = re.sub(r"\\(?:text|mathrm|textbf|mbox)\{[^{}]*\}", " ", m)
    rest = re.sub(r"\\(?:begin|end)\{[a-zA-Z*]+\}", " ", rest)     # pmatrix is an environment's name, not a word
    rest = MACRO.sub(" ", rest)
    for w in re.findall(r"[A-Za-z]{4,}", rest):             # four letters running: a word, not the product of variables
        found.append(w)
    # P( ... ) holds a short event only
    for ev in re.findall(r"P\(([^()]*)\)", m):
        if " " in ev.strip() and len(re.findall(r"[A-Za-z]{2,}", ev)) >= 2:
            found.append("P(%s)" % ev)
    return found


def rule_h(q):
    out = []
    for where, t in texts(q):
        for m in MATH.findall(t):
            for w in _words_in_maths(m):
                out.append(("h", "%s sets words in the maths font: %s" % (where, w)))
    return out


# ─────────────────────────────── (d) ───────────────────────────────
def _nums(s):
    s = re.sub(r"(?<=\d)[, ](?=\d{3}\b)", "", s)                          # 26 350 and 26,350 are one number
    s = re.sub(r"[-−]\s*\\d?frac\{(\d+)\}\{(\d+)\}", r"-\1 \2", s)        # -\frac{2}{5}: the sign belongs to the numerator
    s = s.replace("−", "-")
    return [float(x) for x in re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?", s)]


def _fmt(v):
    return ("%g" % v) if isinstance(v, float) else str(v)


def answer_numbers(q):
    """The numbers the last worked line must show for this question's stored answer (not for a choice: see rule_d)."""
    a, f = q["answer"], q["format"]
    if f in ("number", "number_unit"):
        return [float(a["value"])]
    if f == "money":
        return [a["pence"] / 100.0]
    if f == "fraction":
        return [float(a["n"]), float(a["d"])]
    if f in ("coordinates", "pair"):
        return [float(a["x"]), float(a["y"])]
    if f == "standard_form":
        return [float(a["m"]), float(a["e"])]
    if f == "ratio":
        return [float(x) for x in a["parts"]]
    return []


def _norm_text(s):
    return re.sub(r"\s+|\\dfrac|\\tfrac|\\frac|\\left|\\right|\\\(|\\\)|\\,|[’'.]", "", s).lower()


def rule_d(q):
    w = q.get("worked") or []
    if not w:
        return []
    last = w[-1]
    if q["format"] == "choice":
        lab = next((o["label"] for o in q.get("options") or [] if o["val"] == q["answer"]["val"]), "")
        if _norm_text(lab) in _norm_text(last):
            return []
        # a numeric label may be written differently ("3^6" and "3^{6}"): compare its numbers too
        want = _nums(re.sub(r"\\[a-zA-Z]+", " ", lab))
        have = _nums(last)
        if want and not re.search(r"[a-zA-Z]", re.sub(r"\\[a-zA-Z]+", "", lab)) and all(x in have for x in want):
            return []
        return [("d", "the last worked line does not state the answer %s: %r" % (lab, last[:70]))]
    have = _nums(re.sub(r"\\(?:text|mathrm)\{[^}]*\}", " ", last))
    have += [float(x) for x in re.findall(r"(?<=\{)(\d+)(?=\})", last)]       # \frac{3}{4}
    for x in answer_numbers(q):
        if not any(math.isclose(x, h, rel_tol=1e-9, abs_tol=1e-9) for h in have):
            return [("d", "the last worked line does not state the answer (%s): %r" % (_fmt(x), last[:70]))]
    return []


def answer_line(q):
    """'The answer: ...' for a question's stored answer, in the words and notation the page shows it in."""
    a, f = q["answer"], q["format"]
    unit = q.get("unit") or a.get("unit") or ""
    num = lambda v: ("%g" % v) if isinstance(v, float) else str(v)
    if f in ("number", "number_unit"):
        txt = num(a["value"]) + ((" " + unit) if unit else "")
        txt = "\\(%s\\)%s" % (num(a["value"]), (" " + unit) if unit else "")
    elif f == "money":
        txt = "£%.2f" % (a["pence"] / 100.0)
    elif f == "fraction":
        txt = "\\(\\dfrac{%d}{%d}\\)" % (a["n"], a["d"])
    elif f in ("coordinates", "pair"):
        txt = "\\((%s, %s)\\)" % (num(a["x"]), num(a["y"]))
    elif f == "standard_form":
        txt = "\\(%s \\times 10^{%s}\\)" % (num(a["m"]), num(a["e"]))
    elif f == "ratio":
        txt = "\\(%s\\)" % ":".join(num(x) for x in a["parts"])
    else:
        txt = next((o["label"] for o in q.get("options") or [] if o["val"] == a["val"]), "")
    return "The answer: %s." % txt.rstrip(".")


# ─────────────────────────────── (f) ───────────────────────────────
def has_right_angle_mark(svg):
    """True if the drawing holds a small right-angle mark: a polyline or path of three points whose two arms are at right
    angles and no longer than 24 px (the corner a textbook draws)."""
    cands = [re.findall(r"-?\d+(?:\.\d+)?", m) for m in re.findall(r'<polyline[^>]*points="([^"]*)"', svg)]
    for d in re.findall(r'<path[^>]*\sd="([^"]*)"', svg):
        if len(re.findall(r"[ML]", d)) in (3, 4) and d.count("Z") <= 1:
            cands.append(re.findall(r"-?\d+(?:\.\d+)?", d))
    for nums in cands:
        pts = [(float(nums[i]), float(nums[i + 1])) for i in range(0, len(nums) - 1, 2)]
        for i in range(len(pts) - 2):
            a, b, c = pts[i], pts[i + 1], pts[i + 2]
            u, v = (a[0] - b[0], a[1] - b[1]), (c[0] - b[0], c[1] - b[1])
            lu, lv = math.hypot(*u), math.hypot(*v)
            if 0 < lu <= 24 and 0 < lv <= 24 and abs(u[0] * v[0] + u[1] * v[1]) < 0.02 * lu * lv:
                return True
    return False


RIGHT_USED = re.compile(r"right[- ]angle|perpendicular|Pythagoras|hypotenuse", re.I)


def rule_f(q):
    d = q.get("diagram")
    if not d:
        return []
    said = " ".join(t for _, t in texts(q))
    if RIGHT_USED.search(said) and not has_right_angle_mark(d) \
            and not re.search(r"right[- ]angle|perpendicular", q.get("stem", ""), re.I):
        return [("f", "the working uses a right angle but the diagram does not mark it and the stem does not state it")]
    return []


# ─────────────────────────────── (g) ───────────────────────────────
BANDS = ("impossible", "unlikely", "even chance", "likely", "certain")


def band_of(p):
    p = Fraction(p)
    if p == 0:
        return "impossible"
    if p == 1:
        return "certain"
    if p == Fraction(1, 2):
        return "even chance"
    return "unlikely" if p < Fraction(1, 2) else "likely"


def rule_g(q):
    if not q.get("likelihood"):
        return []
    p = q["likelihood"]
    if not (isinstance(p, dict) and isinstance(p.get("n"), int) and isinstance(p.get("d"), int) and p["d"] > 0 and 0 <= p["n"] <= p["d"]):
        return [("g", "a likelihood item must store the probability its word comes from as {n, d}")]
    want = band_of(Fraction(p["n"], p["d"]))
    lab = next((o["label"] for o in q.get("options") or [] if o["val"] == q["answer"].get("val")), "")
    word = re.sub(r"[\s]+", " ", outside_maths(lab).strip().lower())
    if word != want:
        return [("g", "stored probability %d/%d is %s but the answer's word is %r" % (p["n"], p["d"], want, word))]
    return []


# ─────────────────────────────── (c) ───────────────────────────────
SLIP_RULES = {}          # topic -> function(q) -> [(slip index, expected full-precision value, why)]; filled by gen-six-ps.py


# ─────────────────────────────── slips: recomputed at full precision (rule c) ───────────────────────────────
WRONG_N = "You multiplied the mean by the wrong number of values."


def _avg_data(stem):
    m = re.search(r"data set:\s*([^.]*)\.", stem)
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", m.group(1))] if m else []


def avg_slips(q):
    """averages: the mean as a slip is S/n, the total is S, and 'the wrong number of values' is S/(n-1) (S/2 for one value)."""
    data = _avg_data(q["stem"])
    if not data:
        return []
    n, tot = len(data), sum(data)
    out = []
    for i, s in enumerate(q["slip"]):
        line = s["line"]
        if line.startswith("That is the mean"):
            out.append((i, _to_dp(q, tot / n), "the mean, total ÷ %d" % n))
        elif line.startswith("That is the total"):
            out.append((i, tot, "the total"))
        elif line == WRONG_N or line.startswith("You divided the total by"):
            k = n - 1 if n > 1 else n + 1
            out.append((i, tot / k, "the total ÷ %d (one %s than the %d values)" % (k, "less" if n > 1 else "more", n)))
            if line == WRONG_N:
                out.append((i, None, "slip text names the wrong mistake: it should say the total was divided by %d, not %d" % (k, n)))
    return out


def cm_slips(q):
    """compound-measures: the two numbers in the stem, a and b; a slip is a×b, a÷b or b÷a, whichever the line names and the
    stored (rounded) value belongs to."""
    nums = [float(x) for x in re.findall(r"(?<![\w.£])\d+(?:\.\d+)?", re.sub(r"\d+(?:\.\d+)?\s*(?=/)", "", q["stem"]))]
    if len(nums) < 2:
        return []
    a, b = nums[0], nums[1]
    key = float(q["answer"]["value"])
    out = []
    for i, s in enumerate(q["slip"]):
        line, v = s["line"], float(s["answer"]["value"])
        cands = {"mul": a * b, "div": a / b if b else None, "inv": b / a if a else None}
        if line.startswith("You multiplied"):
            want = cands["mul"]
        elif "wrong way round" in line:
            want = cands["inv"] if cands["div"] is not None and math.isclose(cands["div"], key, rel_tol=1e-6) else cands["div"]
        elif line.startswith("You divided"):
            ok = [c for c in (cands["div"], cands["inv"]) if c is not None and (round(c) == v or round(c, 1) == v or math.isclose(c, v, rel_tol=1e-9))]
            want = ok[0] if ok else cands["div"]
        else:
            continue
        out.append((i, _to_dp(q, want), "%s from the numbers %g and %g" % (line.split(".")[0].lower(), a, b)))
    return out


def _to_dp(q, x):
    """x as the question's own rounding instruction would give it (a question that says 'to 1 decimal place' stores its slips
    at 1 dp); full precision when the question has none."""
    dp = (q.get("answer") or {}).get("dp")
    return round(x, dp) if isinstance(dp, int) else x


def py_slips(q):
    """pythagoras: 'You added instead of subtracting' is the root of the sum of the squares of the two sides shown."""
    labels = [float(x) for x in re.findall(r">(\d+(?:\.\d+)?)\s*(?:mm|cm|m|km)<", q.get("diagram") or "")]
    out = []
    for i, s in enumerate(q["slip"]):
        if s["line"].startswith("You added") and len(labels) == 2:
            out.append((i, _to_dp(q, math.sqrt(labels[0] ** 2 + labels[1] ** 2)), "the root of the sum of the squares of %g and %g" % tuple(labels)))
    return out


SLIP_RULES.update({"averages": avg_slips, "compound-measures": cm_slips, "pythagoras": py_slips})


def rule_c(q):
    fn = SLIP_RULES.get(q.get("topic"))
    if not fn:
        return []
    out = []
    for i, want, why in fn(q):
        if want is None:
            out.append(("c", "slip %d: %s" % (i + 1, why)))
            continue
        got = q["slip"][i]["answer"]["value"]
        if not math.isclose(float(got), float(want), rel_tol=1e-9, abs_tol=1e-9):
            out.append(("c", "slip %d stores %s but %s is %s" % (i + 1, got, why, _fmt(float(want)))))
    return out


# ─────────────────────────────── the mechanical fixes, applied to every bank by gen-six-ps.py ───────────────────────────────
WORDY = re.compile(r"\\(?:text|mathrm|textbf|mbox)\{([^{}]*)\}")


def unword_maths(t):
    r"""Move the words out of the maths: in each \( ... \) that holds a \text{} of more than one word, every \text{} becomes
    plain text and the maths between them stays maths. '\(\text{Subtract } 7 \text{ from both sides}\)' becomes
    'Subtract \(7\) from both sides'."""
    def one(m):
        body = m.group(1)
        texts_ = [w.strip() for w in WORDY.findall(body)]
        if not any(len(w.split()) > 1 or len(w) > 20 for w in texts_):
            return m.group(0)
        out, last = [], 0
        for g in WORDY.finditer(body):
            out.append(("m", body[last:g.start()]))
            out.append(("t", g.group(1).strip()))
            last = g.end()
        out.append(("m", body[last:]))
        parts = []
        for kind, x in out:
            if kind == "t":
                if x:
                    parts.append(x)
            elif re.search(r"[A-Za-z0-9\\]", x):
                parts.append("\\(" + x.strip() + "\\)")
            elif x.strip():
                parts.append(x.strip())                                   # a lone sign or bracket stays as it is
        return " ".join(parts)
    return MATH.sub(one, t)


def fix_texts(q):
    """(h): words out of the maths in every string. Returns the number of strings changed."""
    n = 0
    for k in ("stem",):
        new = unword_maths(q[k])
        n += new != q[k]
        q[k] = new
    for o in q.get("options") or []:
        new = unword_maths(o["label"])
        n += new != o["label"]
        o["label"] = new
    q["worked"] = [unword_maths(w) for w in q["worked"]]
    for sl in q["slip"]:
        sl["line"] = unword_maths(sl["line"])
    return n


def fix_simplest(q):
    """(b): the stem of a 'simplest' question says so."""
    if (q.get("accept") or {}).get("rule") != "simplest" or re.search(r"simplest", q["stem"], re.I):
        return False
    st = q["stem"].rstrip()
    if st.count(". ") == 0 and st.endswith("."):
        q["stem"] = st[:-1] + " in its simplest form."
    else:
        q["stem"] = st + " Give your answer in its simplest form."
    return True


def fix_answer_line(q):
    """(d): a worked solution ends on the answer. Adds 'The answer: ...' as a last line, or joins it to the last line when
    the solution already has five."""
    if not q.get("worked") or rule_d(q) == []:
        return False
    line = answer_line(q)
    if len(q["worked"]) >= 5:
        q["worked"][-1] = q["worked"][-1].rstrip() + " " + line
    else:
        q["worked"].append(line)
    return True


def fix_slips(q):
    """(c): each recomputed slip stored at its full-precision value; a slip text that names the wrong mistake replaced."""
    fn = SLIP_RULES.get(q.get("topic"))
    n = 0
    if not fn:
        return 0
    for i, want, why in fn(q):
        sl = q["slip"][i]
        if want is None:
            m = re.search(r"divided by (\d+), not (\d+)", why)
            sl["line"] = "You divided the total by %s instead of %s, the number of values." % (m.group(1), m.group(2))
            n += 1
        elif not math.isclose(float(sl["answer"]["value"]), float(want), rel_tol=1e-9, abs_tol=1e-9):
            sl["answer"]["value"] = float(want) if not float(want).is_integer() else int(want)
            n += 1
    return n


def fix_common_difference(q):
    """(sequences 89ffd6dc, 877a0792): a falling sequence's common difference is negative; the stem, the answer and the working
    agree on that, and the size of the step is a slip."""
    if "common difference" not in q["stem"] or q["answer"].get("value", 0) >= 0:
        return False
    d = -q["answer"]["value"]
    dtxt = ("%g" % d)
    if any("negative" in w for w in q["worked"]):
        return False
    q["worked"] = ["Each term is \\(%s\\) less than the one before." % dtxt,
                   "The terms go down, so the common difference is negative: \\(-%s\\)." % dtxt]
    if not any(sl["answer"].get("value") == d for sl in q["slip"]):
        q["slip"].append({"answer": {"value": int(d) if float(d).is_integer() else d},
                          "line": "That is the size of the step. The terms are going down, so the common difference is \\(-%s\\), not \\(%s\\)." % (dtxt, dtxt)})
    return True


RULES = (rule_a, rule_b, rule_c, rule_d, rule_e, rule_f, rule_g, rule_h)


def faults(q):
    out = []
    for r in RULES:
        try:
            out += r(q)
        except Exception as exc:                              # a rule that cannot read a question is a fault in the rule's reach
            out.append((r.__name__[-1], "rule could not read the question: %s" % exc))
    return out


# ─────────────────────────────── planted cases ───────────────────────────────
def _q(**kw):
    q = {"id": "t-1", "topic": "t", "stem": "Work it out.", "format": "number", "answer": {"value": 4}, "worked": ["\\(2 + 2 = 4\\)"],
         "slip": [], "diagram": None, "options": None}
    q.update(kw)
    return q


def _choice(labels, key="a", **kw):
    return _q(format="choice", answer={"val": key}, options=[{"val": "abcd"[i], "label": l} for i, l in enumerate(labels)], **kw)


def selftest():
    """[(name, ok)]: each rule's planted fault is caught, and a clean question passes."""
    cases = []

    def caught(rule, q, name):
        cases.append(("rule %s catches: %s" % (rule, name), any(r == rule for r, _ in faults(q))))

    def clean(q, name):
        f = faults(q)
        cases.append(("clean passes: %s (%s)" % (name, "; ".join(m for _, m in f)[:80]), not f))

    clean(_q(), "a number question")
    caught("a", _choice(["\\(5^6\\)", "\\(5^8\\)", "\\(5^5\\)", "\\(25^3\\)"]), "5^6 and 25^3 are the same value")
    caught("a", _choice(["\\(\\frac{1}{2}\\)", "0.5", "\\(\\frac{1}{3}\\)", "\\(\\frac{1}{4}\\)"]), "a half and 0.5")
    clean(_choice(["\\(5^6\\)", "\\(5^8\\)", "\\(5^5\\)", "\\(5^9\\)"], worked=["\\(5^6\\)"]), "four different powers")
    caught("b", _q(format="fraction", answer={"n": 1, "d": 2}, accept={"rule": "simplest"}, stem="Write \\(0.5\\) as a fraction.", worked=["\\(\\frac{1}{2}\\)"]), "simplest with no 'simplest form'")
    clean(_q(format="fraction", answer={"n": 1, "d": 2}, accept={"rule": "simplest"}, stem="Write \\(0.5\\) as a fraction in its simplest form.", worked=["\\(\\frac{1}{2}\\)"]), "simplest form stated")
    caught("d", _q(worked=["Multiply each amount by 4."], answer={"value": 12}), "a last line that stops before the answer")
    clean(_q(worked=["Multiply by 4: \\(3 \\times 4 = 12\\)."], answer={"value": 12}), "a last line stating the answer")
    caught("e", _q(stem="Write an expression for each person\\'s share."), "a raw backslash in the stem")
    clean(_q(stem="Write \\(\\frac{b}{3}\\) for each person's share."), "a backslash inside maths")
    caught("f", _q(diagram="<svg><path d='M0 0'/></svg>", worked=["Use the perpendicular height."]), "right angle used, not marked")
    clean(_q(diagram='<svg><polyline points="0,10 10,10 10,0"/></svg>', worked=["Use the perpendicular height: \\(4\\)."]), "right angle marked")
    lk = lambda n, d, word: _choice([word, "impossible", "certain", "likely"], likelihood={"n": n, "d": d})
    caught("g", _choice(["unlikely", "likely", "certain", "impossible"]) | {} if False else _choice(["likely", "unlikely", "certain", "impossible"], likelihood={"n": 1, "d": 6}), "likely stored at 1/6")
    caught("g", _choice(["unlikely", "likely", "certain", "impossible"], likelihood={"n": 1, "d": 2}), "unlikely stored at 1/2")
    caught("g", _choice(["unlikely", "likely", "certain", "impossible"], likelihood=True), "no probability stored")
    clean(_choice(["even chance", "likely", "certain", "impossible"], likelihood={"n": 3, "d": 6}, worked=["even chance"]), "even chance at 3/6")
    caught("h", _q(stem="\\(P(\\text{rolling a 7 on a standard die}) = 7/6\\)"), "words in \\text inside maths")
    caught("h", _q(stem="Find \\(P(rolling 7 on a die)\\)."), "a long event inside P( )")
    clean(_q(stem="Find \\(P(\\text{red})\\) for the bag.", worked=["\\(4\\)"]), "a single label in P( )")
    clean(_q(stem="A car travels \\(20\\text{ m}\\) in \\(10\\text{ s}\\).", worked=["\\(4\\)"]), "units in \\text")
    old = SLIP_RULES.get("t")
    SLIP_RULES["t"] = lambda q: [(0, 13.928388, "the sum of squares √194")]
    caught("c", _q(slip=[{"answer": {"value": 14.0}, "line": "You added."}]), "a slip rounded to 14")
    clean(_q(slip=[{"answer": {"value": 13.928388}, "line": "You added."}]), "a slip at full precision")
    if old is None:
        del SLIP_RULES["t"]
    return cases
