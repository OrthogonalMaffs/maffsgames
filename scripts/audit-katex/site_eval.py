# site_eval.py: rebuild, per bank question, the exact string a KaTeX call site
# builds from that question -- for arguments made of literals, +, template
# literals, ||, ?: (both branches), .replace(regex, str) and member chains.
# Anything that calls a game function returns None: not reproducible from the
# bank, so that site is runtime-only.
import re
import esprima


class Unsupported(Exception):
    pass


def js_str(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return str(int(v)) if v.is_integer() else repr(v)
    if v is None:
        return "undefined"
    return str(v)


def chain(n):
    """member chain -> (root, [prop or '*'])"""
    props = []
    while n.type == "MemberExpression":
        if n.computed:
            if n.property.type == "Literal":
                props.append(n.property.value)
            else:
                props.append("*")
        else:
            props.append(n.property.name)
        n = n.object
    if n.type != "Identifier":
        raise Unsupported("chain root")
    return n.name, list(reversed(props))


def resolve_chain(obj, props):
    vals = [obj]
    for p in props:
        nxt = []
        for v in vals:
            if p == "*":
                if isinstance(v, list):
                    nxt += v
                elif isinstance(v, dict):
                    nxt += list(v.values())
            elif isinstance(v, dict) and p in v:
                nxt.append(v[p])
            elif isinstance(v, list) and isinstance(p, int) and p < len(v):
                nxt.append(v[p])
            elif isinstance(v, str) and p == "length":
                nxt.append(len(v))
            else:
                nxt.append(None)
        vals = nxt
    return vals


def ev(n, obj, bare_values):
    """list of possible values for node n against bank object obj."""
    t = n.type
    if t == "Literal":
        return [n.value]
    if t == "TemplateLiteral":
        outs = [""]
        for i, q in enumerate(n.quasis):
            outs = [o + q.value.cooked for o in outs]
            if i < len(n.expressions):
                vs = ev(n.expressions[i], obj, bare_values)
                outs = [o + js_str(v) for o in outs for v in vs]
        return outs
    if t == "BinaryExpression" and n.operator == "+":
        L, R = ev(n.left, obj, bare_values), ev(n.right, obj, bare_values)
        return [(js_str(a) + js_str(b)) if (isinstance(a, str) or isinstance(b, str)) else
                (a + b if a is not None and b is not None else None) for a in L for b in R]
    if t == "LogicalExpression" and n.operator == "||":
        out = []
        for a in ev(n.left, obj, bare_values):
            out += [a] if a else ev(n.right, obj, bare_values)
        return out
    if t == "ConditionalExpression":
        return ev(n.consequent, obj, bare_values) + ev(n.alternate, obj, bare_values)
    if t == "MemberExpression":
        root, props = chain(n)
        return resolve_chain(obj, props)
    if t == "Identifier":
        if bare_values is None:
            raise Unsupported("bare identifier " + n.name)
        return list(bare_values)
    if t == "CallExpression" and n.callee.type == "MemberExpression" and not n.callee.computed:
        m = n.callee.property.name
        if m == "replace" and len(n.arguments) == 2 and n.arguments[0].type == "Literal" \
                and getattr(n.arguments[0], "regex", None) and n.arguments[1].type == "Literal":
            pat = n.arguments[0].regex.pattern
            flags = n.arguments[0].regex.flags
            rep = n.arguments[1].value
            return [re.sub(pat, rep, v, count=0 if "g" in flags else 1) if isinstance(v, str) else v
                    for v in ev(n.callee.object, obj, bare_values)]
        if m in ("toString", "trim"):
            return [js_str(v).strip() if m == "trim" else js_str(v) for v in ev(n.callee.object, obj, bare_values)]
    if t == "CallExpression" and n.callee.type == "Identifier" and n.callee.name == "String" and len(n.arguments) == 1:
        return [js_str(v) for v in ev(n.arguments[0], obj, bare_values)]
    raise Unsupported(t)


def chains_in(n):
    out = []
    def walk(x):
        if x is None or not hasattr(x, "type"):
            return
        if x.type == "MemberExpression":
            try:
                out.append(chain(x))
                return
            except Unsupported:
                pass
        for k, v in vars(x).items():
            if k in ("range", "loc", "type"):
                continue
            if isinstance(v, list):
                for y in v:
                    walk(y)
            elif hasattr(v, "type"):
                walk(v)
    walk(n)
    return out


def parse_expr(text):
    tree = esprima.parseScript("(" + text + ")")
    return tree.body[0].expression


def is_plain(n):
    return n.type == "Identifier" or (n.type == "MemberExpression" and all(
        p != "*" or True for p in [1]) and _plain_chain(n))


def _plain_chain(n):
    try:
        chain(n)
        return True
    except Unsupported:
        return False


def all_dicts(v):
    if isinstance(v, dict):
        yield v
        for x in v.values():
            yield from all_dicts(x)
    elif isinstance(v, list):
        for x in v:
            yield from all_dicts(x)


def site_strings(expr, questions, bare_values):
    """{string: label} for every value this expression builds from any bank
    object carrying the first property of one of its member chains."""
    firsts = {props[0] for root, props in chains_in(expr) if props and props[0] != "*"}
    out = {}
    if not firsts:
        for v in ev(expr, {}, bare_values):
            if isinstance(v, str) and v:
                out[v] = "(expression)"
        return out
    for q in questions:
        for d in all_dicts(q):
            if not (firsts & set(d)):
                continue
            for v in ev(expr, d, bare_values):
                if isinstance(v, str) and v and "undefined" not in v:
                    out.setdefault(v, "+".join(sorted(firsts & set(d))))
    return out
