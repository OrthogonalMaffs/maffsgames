# site_fields.py -> sites.json
# For every call into KaTeX (katex.render/renderToString, MaffsText.html, or a
# wrapper found by find_wrappers.py), resolve where the rendered argument comes
# from: a source literal, or which bank fields feed it (following locals,
# forEach/map/filter callbacks and for..of inside the enclosing function).
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import find_wrappers as fw
bc = fw.bc
ROOT = fw.REPO
HERE = fw.WORK
W = {r["file"]: r for r in json.load(open(os.path.join(HERE, "wrappers.json")))}

ITER = ("forEach", "map", "filter", "some", "every", "find", "flatMap", "reduce")


def literal_value(n):
    if n.type == "Literal" and isinstance(n.value, str):
        return n.value
    if n.type == "TemplateLiteral" and not n.expressions:
        return n.quasis[0].value.cooked
    if n.type == "BinaryExpression" and n.operator == "+":
        a, b = literal_value(n.left), literal_value(n.right)
        if a is not None and b is not None:
            return a + b
    return None


def build_parent(tree):
    par = {}
    def v(x, p):
        par[id(x)] = p
    fw.walk(tree, v)
    return par


def binding_sources(name, fn, par):
    """Expressions a local `name` inside fn takes its value from."""
    srcs, is_param_of = [], []
    def v(x, p):
        if x.type == "VariableDeclarator" and x.id.type == "Identifier" and x.id.name == name and x.init is not None:
            srcs.append(x.init)
        elif x.type == "AssignmentExpression" and x.left.type == "Identifier" and x.left.name == name:
            srcs.append(x.right)
        elif x.type in ("ForOfStatement", "ForInStatement"):
            l = x.left
            nm = l.declarations[0].id.name if l.type == "VariableDeclaration" and l.declarations[0].id.type == "Identifier" \
                else (l.name if l.type == "Identifier" else None)
            if nm == name:
                srcs.append(x.right)
        elif x.type in fw.FN and x is not fn:
            for i, pn in enumerate(fw.param_names(x)):
                if pn == name:
                    call = par.get(id(x))
                    if call is not None and call.type == "CallExpression" and call.callee.type == "MemberExpression" \
                            and not call.callee.computed and call.callee.property.name in ITER and i == 0:
                        srcs.append(call.callee.object)
                    else:
                        is_param_of.append(x)
    fw.walk(fn, v)
    if fn is not None and fn.type in fw.FN and name in fw.param_names(fn):
        call = par.get(id(fn))
        if call is not None and call.type == "CallExpression" and call.callee.type == "MemberExpression" \
                and not call.callee.computed and call.callee.property.name in ITER and fw.param_names(fn).index(name) == 0:
            srcs.append(call.callee.object)
        else:
            is_param_of.append(fn)
    return srcs, is_param_of


def resolve(expr, fn, par, depth=0, seen=None):
    seen = seen if seen is not None else set()
    fields, params = set(), set()
    if depth > 6:
        return fields, params
    called = set()
    def cv(x, p):
        if x.type == "CallExpression" and x.callee.type == "MemberExpression":
            called.add(id(x.callee))
    fw.walk(expr, cv)
    def v(x, p):
        if x.type == "MemberExpression" and not x.computed and id(x) not in called:
            fields.add(x.property.name)
    fw.walk(expr, v)
    for name in fw.value_ids_in(expr) | fw.ids_in(expr):
        if name in seen:
            continue
        seen.add(name)
        # search outward through enclosing functions for the binding
        scope = fn
        while scope is not None:
            srcs, pof = binding_sources(name, scope, par)
            if srcs or pof:
                for s in srcs:
                    f2, p2 = resolve(s, scope, par, depth + 1, seen)
                    fields |= f2; params |= p2
                for f in pof:
                    params.add(name)
                break
            # climb to the next enclosing function
            n = par.get(id(scope))
            while n is not None and n.type not in fw.FN:
                n = par.get(id(n))
            scope = n
    return fields, params


def main():
    out = {}
    for f, r in W.items():
        if r.get("parse_error") or not (r["direct"] or r["wrappers"]):
            continue
        html = open(os.path.join(ROOT, f), encoding="utf-8").read()
        tree, src = bc.parse_game_source(html)
        shim = bc._shim_for_parser(src)
        par = build_parent(tree)
        wr = {w["name"]: w for w in r["wrappers"]}
        sinks = {"katex.render": 0, "katex.renderToString": 0, "MaffsText.html": 0}
        sinks.update({n: w["param"] for n, w in wr.items()})
        res = []
        def v(x, p):
            if x.type != "CallExpression":
                return
            cn = fw.callee_name(x)
            if cn not in sinks:
                return
            pi = sinks[cn]
            if len(x.arguments) <= pi:
                return
            a = x.arguments[pi]
            # enclosing function
            n = par.get(id(x))
            while n is not None and n.type not in fw.FN:
                n = par.get(id(n))
            enc = n
            enc_name = None
            if enc is not None:
                enc_name = fw.fn_name(enc, par.get(id(enc)))
            # a call inside a wrapper on that wrapper's own parameter is the wrapper's body
            inside_wrapper = enc_name in wr and (fw.value_ids_in(a) & set(p for p in fw.param_names(enc) if p))
            lit = literal_value(a)
            binding = None
            if a.type == "Identifier" and enc is not None:
                decls = []
                def bv(x, pp):
                    if x.type == "VariableDeclarator" and x.id.type == "Identifier" and x.id.name == a.name and x.init is not None:
                        decls.append(x.init)
                fw.walk(enc, bv)
                if len(decls) == 1:
                    binding = shim[decls[0].range[0]:decls[0].range[1]]
            fields, params = (set(), set()) if lit is not None else resolve(a, enc, par)
            res.append({"callee": cn, "line": bc.line_of(src, x.range[0]), "in": enc_name,
                        "arg": shim[a.range[0]:a.range[1]], "binding": binding, "literal": lit,
                        "fields": sorted(fields), "params": sorted(params),
                        "wrapper_body": bool(inside_wrapper),
                        "argc": len(x.arguments),
                        "opts": shim[x.arguments[-1].range[0]:x.arguments[-1].range[1]][:200]
                                 if cn.startswith("katex.") and len(x.arguments) > (2 if cn == "katex.render" else 1) else None})
        fw.walk(tree, v)
        out[f] = res
    json.dump(out, open(os.path.join(HERE, "sites.json"), "w"), indent=1)
    for f, res in out.items():
        for s in res:
            if s["wrapper_body"]:
                continue
            print("%-28s %-14s :%-5d %-18s lit=%s fields=%s params=%s" % (
                f.split("/")[1][:28], s["callee"][:14], s["line"], (s["in"] or "")[:18],
                "Y" if s["literal"] is not None else "-", s["fields"], s["params"]))


if __name__ == "__main__":
    main()
