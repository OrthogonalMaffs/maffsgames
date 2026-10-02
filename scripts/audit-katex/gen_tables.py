# gen_tables.py -> tables.md : the data sections of docs/audit-katex-wrappers.md
import json, os, re, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CODE = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get("AUDIT_KATEX_WORK") or os.path.join(__import__("tempfile").gettempdir(), "audit-katex")
os.makedirs(WORK, exist_ok=True)
KATEX = os.environ.get("AUDIT_KATEX_DIR") or os.path.join(WORK, "package", "dist")
HERE = WORK
sys.path.insert(0, os.path.join(REPO, "scripts"))
sys.path.insert(0, CODE)
from collections import Counter
import bank_common as bc
ROOT = REPO
R = json.load(open(os.path.join(HERE, "results.json")))
W = json.load(open(os.path.join(HERE, "wrappers.json")))
WF = {r["file"]: r for r in W}

roster = []
for l in open(os.path.join(ROOT, ".claude/rules/game-roster.md")):
    if not l.startswith("|"):
        continue
    c = [x.strip() for x in l.strip().strip("|").split("|")]
    if len(c) > 3 and re.fullmatch(r"`[a-z0-9-]+`", c[2]):
        roster.append((c[1], c[2].strip("`")))

CAT = [("hint", r"hint"), ("explanation", r"crExplanation|bayesWorking|misconception|explanation|working(?!Steps)"),
       ("step", r"steps|\.s\[\]|workingSteps|lines"),
       ("option", r"\.correct$|\.d\[\]|distractors|wrong|options|answerDisplay|valueDisplay|\.answer$|\.opts"),
       ("prompt", r"\.q$|prompt|title|\.s$|\.eq$|formula|display$|label|givenLatex|expr$|\.prop$|\.content$")]


def cats(fields):
    out = set()
    for f in fields:
        if f == "(source literal)":
            out.add("source literal")
            continue
        if "." not in f:
            continue
        for name, rx in CAT:
            if re.search(rx, f):
                out.add(name)
                break
        else:
            out.add("other")
    return out


def esc(s):
    return s.replace("|", "\\|").replace("\n", " ")


def src_of(e):
    return e["src_strings"][0] if e["src_strings"] else e["s"]


def examples(es, k=3):
    es = sorted(es, key=lambda e: ("runtime" not in e["sources"], len(src_of(e)), src_of(e)))
    out = []
    for e in es[:k]:
        s = src_of(e)
        line = "  - `%s` → `%s`" % (esc(s[:110]), esc(e["spaced_visual"][:110]))
        if s != e["s"]:
            line += " (KaTeX received `%s`)" % esc(e["s"][:80])
        out.append(line)
    return out


def bank_paths(es):
    c = Counter()
    for e in es:
        ps = [f for f in e["fields"] if "." in f and not f.startswith("mode:")]
        for p in sorted(set(ps)) or (["(source literal)"] if "(source literal)" in e["fields"] else ["(no bank match: generated or built at the call site)"]):
            c[p] += 1
    return ", ".join("`%s` %d" % (p, n) for p, n in c.most_common())


def split(es):
    rt = sum(1 for e in es if "runtime" in e["sources"])
    return rt, len(es) - rt


summary = []
sections = []
files_by_slug = {}
for r in W:
    files_by_slug.setdefault(r["slug"], []).append(r)

for name, slug in roster + [("(withdrawn file) Regression Rumble", "regression-rumble")]:
    pass

for slug in sorted(R):
    d = R[slug]
    es = list(d.values())
    b7 = [e for e in es if e["hazard"]]
    nw = [e for e in es if e["space_loss"]]
    rt_all, fb_all = split(es)
    summary.append((len(b7), len(nw), slug, len(es), rt_all, fb_all, split(b7), split(nw)))

summary.sort(key=lambda x: (-x[0], -x[1], x[2]))
out = []
out.append("| Game | B7 test (headline) | of which runtime / fallback only | Second count | of which runtime / fallback only | Strings KaTeX received | runtime / fallback only |")
out.append("|---|---:|---|---:|---|---:|---|")
tb = tn = ts = 0
for b7, nw, slug, n, rt, fb, (b7r, b7f), (nwr, nwf) in summary:
    out.append("| `%s` | **%d** | %d / %d | %d | %d / %d | %d | %d / %d |" % (slug, b7, b7r, b7f, nw, nwr, nwf, n, rt, fb))
    tb += b7; tn += nw; ts += n
out.append("| **Total, %d games** | **%d** | | **%d** | | **%d** | |" % (len(summary), tb, tn, ts))
SUMMARY = "\n".join(out)

# per-game sections
sec = []
for b7n, nwn, slug, n, rt, fb, _, _ in sorted(summary, key=lambda x: x[2]):
    d = R[slug]; es = list(d.values())
    b7 = [e for e in es if e["hazard"]]; nw = [e for e in es if e["space_loss"] and not e["hazard"]]
    sec.append("### `%s`" % slug)
    for r in files_by_slug[slug]:
        if not (r["wrappers"] or r["direct"]):
            continue
        ws = []
        for w in sorted(r["wrappers"], key=lambda w: (w["depth"], w["line"])):
            via = ", ".join(w["via"])
            route = "splits on `\\( \\)` via MaffsText" if "MaffsText" in w["splits_on"] else "whole string to KaTeX"
            if w["depth"] > 1 and "MaffsText" not in w["splits_on"]:
                route = "passes its argument on to `%s`" % via
            ws.append("`%s` :%d (%s mode, %s%s)" % (w["name"], w["line"], w["display"],
                                                    "via `%s`, " % via if w["depth"] == 1 else "", route))
        anon = [x for x in r["direct"] if not x["in"] or x["in"] not in {w["name"] for w in r["wrappers"]}]
        for x in anon:
            ws.append("direct `%s` :%d in `%s`" % (x["callee"], x["line"], x["in"] or "(anonymous callback)"))
        label = "" if r["file"].endswith("index.html") else " (`%s`, withdrawn, not served)" % r["file"]
        sec.append("- **Wrappers%s:** %s" % (label, "; ".join(ws)))
    if n == 0:
        sec.append("- **Strings rendered:** none. The wrapper is defined and never called.")
        sec.append("")
        continue
    nl = sum(1 for e in es if set(e["sources"]) == {"literal"})
    sec.append("- **Strings KaTeX received:** %d distinct (%d seen at runtime; %d from the bank fallback only; %d of those are source literals)." % (n, rt, fb - 0, nl))
    if b7:
        r1, f1 = split(b7)
        sec.append("- **B7 test: %d lose prose spaces** (%d runtime, %d bank fallback only). Fields: %s. As rendered:" % (len(b7), r1, f1, ", ".join(sorted(set().union(*[cats(e["fields"]) for e in b7])))))
        sec += examples(b7)
        sec.append("  - Bank paths: %s" % bank_paths(b7))
    else:
        sec.append("- **B7 test: 0.**")
    if nw:
        r2, f2 = split(nw)
        sec.append("- **Second count only (not B7): %d** (%d runtime, %d bank fallback only). Fields: %s. As rendered:" % (len(nw), r2, f2, ", ".join(sorted(set().union(*[cats(e["fields"]) for e in nw])))))
        sec += examples(nw)
    sec.append("")
SECTIONS = "\n".join(sec)

# B7 coverage today
b7_seen = [(r["slug"], r["b7_fields"]) for r in W if r["b7_fields"] and r["file"].endswith("index.html")]
B7SEEN = "\n".join("| `%s` | %s |" % (s, ", ".join("`%s`" % f for f in fs)) for s, fs in sorted(b7_seen))

kx_files = {r["slug"] for r in W if r["file"].endswith("index.html") and (r["wrappers"] or r["direct"])}
loads_only = sorted(r["slug"] for r in W if r["file"].endswith("index.html") and r["loads_katex"] and not (r["wrappers"] or r["direct"]))
no_katex = sorted(s for _, s in roster if s not in kx_files and s not in loads_only)
open(os.path.join(HERE, "tables.md"), "w").write(
    "SUMMARY\n" + SUMMARY + "\n\nSECTIONS\n" + SECTIONS + "\n\nB7SEEN\n" + B7SEEN +
    "\n\nLOADS_ONLY %d\n" % len(loads_only) + ", ".join("`%s`" % s for s in loads_only) +
    "\n\nNO_KATEX %d\n" % len(no_katex) + ", ".join("`%s`" % s for s in no_katex) +
    "\n\nKX %d\n" % len(kx_files))
print(len(roster), len(kx_files), len(loads_only), len(no_katex), tb, tn, ts)
print(sum(1 for x in summary if x[0]), sum(1 for x in summary if x[1]))
