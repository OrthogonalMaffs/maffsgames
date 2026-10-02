# find_wrappers.py <repo root> -> wrappers.json
# Read-only. Finds KaTeX wrappers BY BEHAVIOUR: any function whose parameter
# reaches katex.render / katex.renderToString's first argument (directly, or
# through another such function, to a fixed point), plus every direct KaTeX
# call site. Uses bank_common's own parser so line numbers match the file.
import json, os, re, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CODE = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get("AUDIT_KATEX_WORK") or os.path.join(__import__("tempfile").gettempdir(), "audit-katex")
os.makedirs(WORK, exist_ok=True)
KATEX = os.environ.get("AUDIT_KATEX_DIR") or os.path.join(WORK, "package", "dist")
ROOT = REPO
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import bank_common as bc

FN = ("FunctionDeclaration", "FunctionExpression", "ArrowFunctionExpression")


def children(n):
    if isinstance(n, list):
        return [c for c in n if hasattr(c, "type")]
    out = []
    for k, v in vars(n).items():
        if k in ("range", "loc", "type"):
            continue
        if isinstance(v, list):
            out += [c for c in v if hasattr(c, "type")]
        elif hasattr(v, "type"):
            out.append(v)
    return out


def walk(n, visit, parent=None):
    visit(n, parent)
    for c in children(n):
        walk(c, visit, n)


def ids_in(n):
    """Identifier names referenced in an expression (not property names)."""
    out = set()
    def v(x, p):
        if x.type == "Identifier":
            if p is not None and p.type == "MemberExpression" and p.property is x and not p.computed:
                return
            if p is not None and p.type == "Property" and p.key is x and not p.computed and not p.shorthand:
                return
            out.add(x.name)
    walk(n, v)
    return out


def value_ids_in(n):
    """Like ids_in, but an identifier used only as the object of a plain
    field read (`q.prompt`) does not count: that is a call site passing a
    field, not a wrapper passing its argument. A method call on it
    (`s.replace(...)`, `s.split(...)`) still counts: a transform of the value."""
    out = set()
    def v(x, p):
        if x.type != "Identifier":
            return
        if p is not None and p.type == "MemberExpression" and p.property is x and not p.computed:
            return
        if p is not None and p.type == "Property" and p.key is x and not p.computed and not p.shorthand:
            return
        out.add(x.name)
    def strip(x, p):
        pass
    # collect identifiers that are objects of a field read
    field_objs = set()
    def fv(x, p):
        if x.type == "MemberExpression" and not x.computed and x.object.type == "Identifier":
            field_objs.add(id(x.object))
    walk(n, fv)
    called = set()
    def cv(x, p):
        if x.type == "CallExpression" and x.callee.type == "MemberExpression" and x.callee.object.type == "Identifier":
            called.add(id(x.callee.object))
    walk(n, cv)
    def v2(x, p):
        if x.type != "Identifier":
            return
        if p is not None and p.type == "MemberExpression" and p.property is x and not p.computed:
            return
        if p is not None and p.type == "Property" and p.key is x and not p.computed and not p.shorthand:
            return
        if id(x) in field_objs and id(x) not in called:
            return
        out.add(x.name)
    walk(n, v2)
    return out


def callee_name(call):
    c = call.callee
    if c.type == "Identifier":
        return c.name
    if c.type == "MemberExpression" and not c.computed:
        obj = c.object
        if obj.type == "Identifier":
            return obj.name + "." + c.property.name
        if obj.type == "MemberExpression" and not obj.computed and obj.object.type == "Identifier":
            return obj.object.name + "." + obj.property.name + "." + c.property.name
        return "?." + c.property.name
    return None


def fn_name(node, parent):
    if node.type == "FunctionDeclaration" and node.id:
        return node.id.name
    if parent is not None:
        if parent.type == "VariableDeclarator" and parent.id.type == "Identifier":
            return parent.id.name
        if parent.type == "Property":
            return bc.literal_key(parent.key)
        if parent.type == "AssignmentExpression":
            l = parent.left
            if l.type == "Identifier":
                return l.name
            if l.type == "MemberExpression" and not l.computed:
                return (l.object.name + "." if l.object.type == "Identifier" else "") + l.property.name
    if node.type == "FunctionExpression" and node.id:
        return node.id.name
    return None


def param_names(fn):
    out = []
    for p in fn.params:
        if p.type == "Identifier":
            out.append(p.name)
        elif p.type == "AssignmentPattern" and p.left.type == "Identifier":
            out.append(p.left.name)
        else:
            out.append(None)
    return out


def tainted_locals(fn, seeds):
    """Intra-function taint: a local is tainted when assigned from an
    expression that mentions a tainted name. Iterated to a fixed point."""
    t = set(seeds)
    changed = True
    while changed:
        changed = False
        def v(x, p):
            nonlocal changed
            if x.type == "VariableDeclarator" and x.id.type == "Identifier" and x.init is not None:
                if x.id.name not in t and value_ids_in(x.init) & t:
                    t.add(x.id.name); changed = True
            elif x.type == "AssignmentExpression" and x.left.type == "Identifier":
                if x.left.name not in t and value_ids_in(x.right) & t:
                    t.add(x.left.name); changed = True
            elif x.type in ("ForOfStatement", "ForInStatement"):
                l = x.left
                nm = None
                if l.type == "VariableDeclaration" and l.declarations[0].id.type == "Identifier":
                    nm = l.declarations[0].id.name
                elif l.type == "Identifier":
                    nm = l.name
                if nm and nm not in t and ids_in(x.right) & t:
                    t.add(nm); changed = True
            elif x.type == "CallExpression" and x.callee.type == "MemberExpression" \
                    and not x.callee.computed and x.callee.property.name in ("forEach", "map", "replace"):
                # arr.forEach(seg => ...) / s.replace(re, (m, inner) => ...): callback params
                # inherit taint from the receiver.
                if value_ids_in(x.callee.object) & t:
                    for a in x.arguments:
                        if a.type in FN:
                            for pn in param_names(a):
                                if pn and pn not in t:
                                    t.add(pn); changed = True
        walk(fn.body, v)
    return t


def options_text(src, call, idx):
    if len(call.arguments) > idx:
        a = call.arguments[idx]
        return src[a.range[0]:a.range[1]]
    return ""


def analyse(slug, html):
    tree, src = bc.parse_game_source(html)
    if tree is None:
        return {"slug": slug, "parse_error": True}
    shim = bc._shim_for_parser(src)
    fns = []
    def v(x, p):
        if x.type in FN:
            fns.append((x, fn_name(x, p)))
    walk(tree, v)

    # direct KaTeX call sites
    direct = []
    def dv(x, p):
        if x.type == "CallExpression":
            cn = callee_name(x)
            if cn in ("katex.render", "katex.renderToString", "window.katex.render",
                      "window.katex.renderToString", "MaffsText.html"):
                direct.append(x)
    walk(tree, dv)

    def enclosing(node):
        best = None
        for f, nm in fns:
            if f.range[0] <= node.range[0] and node.range[1] <= f.range[1]:
                if best is None or (f.range[1] - f.range[0]) < (best[0].range[1] - best[0].range[0]):
                    best = (f, nm)
        return best

    # wrapper map: name -> {param index that reaches render, ...}
    wrappers = {}   # name -> dict
    sink_calls = {"katex.render": 0, "katex.renderToString": 0,
                  "window.katex.render": 0, "window.katex.renderToString": 0}
    # MaffsText.html is the shared splitter; record it as a known wrapper so a
    # game function routing through it is seen (and marked as splitting).
    known = {"MaffsText.html": {"param": 0, "splits": True, "mode": "inline (per \\( \\) segment)",
                                 "via": "katex.renderToString", "shared": True, "depth": 1}}
    changed = True
    rounds = 0
    while changed and rounds < 10:
        changed = False; rounds += 1
        for f, nm in fns:
            if not nm or nm in wrappers:
                continue
            pn = param_names(f)
            if not any(pn):
                continue
            for i, p in enumerate(pn):
                if not p:
                    continue
                t = tainted_locals(f, {p})
                hits = []
                def cv(x, par):
                    if x.type != "CallExpression":
                        return
                    cn = callee_name(x)
                    if cn in sink_calls and x.arguments and value_ids_in(x.arguments[0]) & t:
                        # only if this call is inside f, not a nested named wrapper
                        hits.append(("katex", cn, x))
                    elif cn in known and x.arguments:
                        k = known[cn]
                        ai = k["param"]
                        if len(x.arguments) > ai and value_ids_in(x.arguments[ai]) & t:
                            hits.append(("wrapper", cn, x))
                walk(f.body, cv)
                if hits:
                    kind, cn, call = hits[0]
                    calls = [h for h in hits]
                    info = {"name": nm, "param": i, "param_name": p,
                            "line": bc.line_of(src, f.range[0]),
                            "via": sorted({h[1] for h in hits}),
                            "depth": max(1 if h[0] == "katex" else 1 + known[h[1]].get("depth", 1) for h in hits),
                            "calls": []}
                    for kind2, cn2, c2 in hits:
                        info["calls"].append({
                            "callee": cn2, "line": bc.line_of(src, c2.range[0]),
                            "arg": shim[c2.arguments[0].range[0]:c2.arguments[0].range[1]][:160],
                            "options": options_text(shim, c2, 2 if cn2.endswith(".render") else 1)[:160]})
                    body = shim[f.range[0]:f.range[1]]
                    info["splits_on"] = []
                    if re.search(r"\\\\\(|\\\\\\\\\(", body):
                        info["splits_on"].append("\\( \\)")
                    if re.search(r"split\(\s*/[^/]*\\\$", body) or re.search(r"/\\\$[^/]*\\\$/", body) \
                            or re.search(r"/\\\$\\\$", body):
                        info["splits_on"].append("$ $")
                    if any(h[1] == "MaffsText.html" for h in hits) or "MaffsText" in body:
                        info["splits_on"].append("MaffsText")
                    info["text_wrap"] = bool(re.search(r"\\\\text\{['\"]?\s*\+|\\\\text\{\$\{", body))
                    opts = " ".join(c["options"] for c in info["calls"])
                    info["display"] = ("display" if re.search(r"displayMode\s*:\s*true", opts)
                                       else "conditional" if re.search(r"displayMode\s*:\s*[A-Za-z_!(]", opts)
                                       else "inline")
                    wrappers[nm] = info
                    known[nm] = {"param": i, "depth": info["depth"]}
                    changed = True
                    break

    # call sites of every wrapper (and of the direct calls) with their argument text
    all_sinks = set(wrappers) | set(sink_calls) | {"MaffsText.html"}
    sites = []
    def sv(x, p):
        if x.type == "CallExpression":
            cn = callee_name(x)
            if cn in all_sinks and x.arguments:
                ai = wrappers[cn]["param"] if cn in wrappers else 0
                if len(x.arguments) > ai:
                    a = x.arguments[ai]
                    enc = enclosing(x)
                    sites.append({"callee": cn, "line": bc.line_of(src, x.range[0]),
                                  "arg": shim[a.range[0]:a.range[1]][:200],
                                  "in": enc[1] if enc else "(top level)"})
    walk(tree, sv)

    direct_info = []
    for c in direct:
        enc = enclosing(c)
        cn = callee_name(c)
        direct_info.append({"callee": cn, "line": bc.line_of(src, c.range[0]),
                            "arg": shim[c.arguments[0].range[0]:c.arguments[0].range[1]][:200] if c.arguments else "",
                            "options": options_text(shim, c, 2 if cn.endswith(".render") else 1)[:200],
                            "in": enc[1] if enc else "(top level)"})
    return {"slug": slug, "wrappers": list(wrappers.values()), "sites": sites, "direct": direct_info,
            "b7_fields": sorted(bc.katex_field_names(html))}



def main():
    out = []
    for slug in sorted(os.listdir(os.path.join(ROOT, "games"))):
        for fname in ("index.html", "_withdrawn.html"):
            p = os.path.join(ROOT, "games", slug, fname)
            if os.path.isfile(p):
                html = open(p, encoding="utf-8").read()
                r = analyse(slug, html)
                r["file"] = "games/%s/%s" % (slug, fname)
                r["loads_katex"] = "katex.min.js" in html
                r["loads_mathtext"] = "mathtext.js" in html
                out.append(r)
    json.dump(out, open(os.path.join(WORK, "wrappers.json"), "w"), indent=1)
    for r in out:
        if r.get("parse_error"):
            print(r["file"], "PARSE ERROR"); continue
        if not r["direct"] and not r["wrappers"]:
            continue
        print("==", r["file"], "B7 fields:", r["b7_fields"])
        for w in r["wrappers"]:
            print("   W %-18s :%-5d p%d(%s) via=%s depth=%d disp=%s split=%s textwrap=%s" % (
                w["name"], w["line"], w["param"], w["param_name"], w["via"], w["depth"], w["display"],
                w["splits_on"], w["text_wrap"]))
        for d in r["direct"]:
            if d["in"] not in {w["name"] for w in r["wrappers"]}:
                print("   D %-18s :%-5d %s(%s, %s)" % (d["in"], d["line"], d["callee"], d["arg"][:60], d["options"][:50]))


if __name__ == "__main__":
    main()
