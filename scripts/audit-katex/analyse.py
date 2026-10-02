# analyse.py -> results.json (+ a console summary)
# Classifies every string KaTeX received, runtime and fallback, with B7's own
# prose test (bank_common.katex_prose_hazard), unchanged.
import glob, json, os, re, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CODE = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get("AUDIT_KATEX_WORK") or os.path.join(__import__("tempfile").gettempdir(), "audit-katex")
os.makedirs(WORK, exist_ok=True)
KATEX = os.environ.get("AUDIT_KATEX_DIR") or os.path.join(WORK, "package", "dist")
HERE = WORK
sys.path.insert(0, os.path.join(REPO, "scripts"))
sys.path.insert(0, CODE)
from collections import defaultdict
import bank_common as bc

ROOT = REPO
WR = {r["file"]: r for r in json.load(open(os.path.join(HERE, "wrappers.json")))}
SITES = json.load(open(os.path.join(HERE, "sites.json")))


def slug_of_file(path):
    m = re.match(r"/games/([^/]+)/(index\.html|_withdrawn\.html)?$", path)
    return m.group(1) if m else None


def gamefile(slug, path):
    return "games/%s/%s" % (slug, "_withdrawn.html" if path.endswith("_withdrawn.html") else "index.html")


# line -> enclosing function name, for every direct KaTeX / MaffsText.html call
DIRECT = {f: {d["line"]: d["in"] for d in r.get("direct", [])} for f, r in WR.items()}
WRNAMES = {f: {w["name"]: w for w in r.get("wrappers", [])} for f, r in WR.items()}
SITE_AT = {f: defaultdict(list) for f in SITES}
for f, ss in SITES.items():
    for s in ss:
        SITE_AT[f][s["line"]].append(s)


def bank_index(slug):
    """string -> sorted field paths (container keys, list levels as [])."""
    p = os.path.join(ROOT, "data", "banks", slug + ".json")
    idx = defaultdict(set)
    if not os.path.isfile(p):
        return idx
    d = json.load(open(p))
    for lv in d.get("levels", {}).values():
        for g in lv.get("groups", []):
            def walk(v, path):
                if isinstance(v, str):
                    idx[v].add(".".join([g["variable"]] + path))
                elif isinstance(v, dict):
                    for k, x in v.items():
                        walk(x, path + [k])
                elif isinstance(v, list):
                    for x in v:
                        walk(x, path[:-1] + [path[-1] + "[]"] if path else ["[]"])
            for q in g["questions"]:
                walk(q, [])
    return idx


def attribute(slug, frames):
    """(wrapper, caller_line) from a record's stack."""
    fr = [x for x in frames if not (x["file"] == "<anonymous>" and x["fn"].startswith("k.render"))]
    via_mt = any("mathtext.js" in x["file"] for x in fr[:2])
    game = [x for x in fr if slug_of_file(x["file"]) == slug]
    if not game:
        return ("(not from game code)", None, None)
    f = gamefile(slug, game[0]["file"])
    l0 = game[0]["line"]
    name = DIRECT.get(f, {}).get(l0) or game[0]["fn"]
    wrapper = ("MaffsText.html via " if via_mt else "") + str(name)
    caller = game[1]["line"] if len(game) > 1 else None
    return (wrapper, l0, caller)


def main():
    recs = defaultdict(list)   # slug -> records
    for path in sorted(glob.glob(os.path.join(HERE, "rt_m*.jsonl"))):
        for line in open(path):
            r = json.loads(line)
            if "kind" not in r:
                continue
            m = re.search(r"/games/([^/?]+)/", r.get("url") or "")
            slug = m.group(1) if m else None
            r["source"] = "runtime"
            r["src_string"] = None
            recs[slug].append(r)
    for line in open(os.path.join(HERE, "fb.jsonl")):
        r = json.loads(line)
        if "kind" not in r:
            continue
        if not (r.get("mode") or "").startswith("fallback|"):
            slug = None
            for x in r["frames"]:
                slug = slug or slug_of_file(x["file"])
            if slug:
                r["source"] = "runtime"; r["src_string"] = None
                recs[slug].append(r)
            continue
        tag, src = r["mode"].split("\u0001", 1)
        _, gfile, callee, sline, fields = tag.split("|", 4)
        r["source"] = "literal" if fields == "(source literal)" else "bank"
        r["src_string"] = src
        r["site_callee"], r["site_line"], r["site_fields"] = callee, int(sline), fields
        slug = gfile.split("/")[1]
        recs[slug].append(r)
    # fallback records carry no game frame when the callee is katex.* directly; recover slug
    # from the wrapper file order is not possible, so fb.py also writes site rows: map them.
    results = {}
    for slug, rs in recs.items():
        if slug is None:
            continue
        idx = bank_index(slug)
        strings = {}
        for r in rs:
            wrapper, l0, caller = attribute(slug, r["frames"])
            if r["source"] != "runtime" and r["site_callee"].startswith("katex."):
                wrapper = r["site_callee"]
            key = r["s"]
            e = strings.setdefault(key, {"s": r["s"], "visual": r["visual"], "display": r["display"],
                                         "hazard": bc.katex_prose_hazard(r["s"]),
                                         "sources": set(), "wrappers": set(), "callers": set(),
                                         "src_strings": set(), "fields": set()})
            e["sources"].add(r["source"])
            e["wrappers"].add(wrapper)
            if r["source"] == "runtime":
                if caller:
                    e["callers"].add(caller)
                if r.get("mode"):
                    e["fields"].add("mode:" + r["mode"])
            else:
                e["callers"].add(r["site_line"])
                e["src_strings"].add(r["src_string"])
                if r["site_fields"] != "(source literal)":
                    e["fields"].update(r["site_fields"].split(","))
                else:
                    e["fields"].add("(source literal)")
            for p in idx.get(r["s"], ()):
                e["fields"].add(p)
            for ss in e["src_strings"]:
                for p in idx.get(ss, ()):
                    e["fields"].add(p)
        for e in strings.values():
            for k in ("sources", "wrappers", "callers", "src_strings", "fields"):
                e[k] = sorted(e[k], key=str)
        results[slug] = strings
    json.dump(results, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    rows = []
    for slug, strings in results.items():
        n = len(strings)
        nrt = sum(1 for e in strings.values() if "runtime" in e["sources"])
        hz = [e for e in strings.values() if e["hazard"]]
        hrt = sum(1 for e in hz if "runtime" in e["sources"])
        rows.append((len(hz), slug, n, nrt, hrt))
    for h, slug, n, nrt, hrt in sorted(rows, reverse=True):
        print("%-26s strings=%5d (runtime %5d)  prose-hazard=%4d (runtime %4d)" % (slug, n, nrt, h, hrt))


if __name__ == "__main__":
    main()
