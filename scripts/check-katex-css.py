#!/usr/bin/env python3
"""No CSS rule on a KaTeX page forces display:block on every span (or every element) under a selector.

Contract PIZZA-CARDS, Amendment 1 (Jon, 7 Nov 2026); canon §7.1.1.

    python scripts/check-katex-css.py              # every page under games/ that loads KaTeX (stdlib; a site-wide check)
    python scripts/check-katex-css.py --selftest   # each planted fault must fail, each planted pass must pass

KaTeX lays a formula out in nested <span>s, most of them inline-block, positioned by its own stylesheet. A game rule
such as `.stage-btn span{display:block}` is a descendant selector: it reaches every span inside the KaTeX output in
that element as well as the game's own span, and stacks the formula into separate lines. Free Daily Pizza's stage 3
card showed "25% of 80," then 3, 5 and "of 45" down the card; the same rule shape sat latent in Log Laws (`.mode-btn
span`). The fix is a child combinator (`.stage-btn > span`), which reaches only the element's own children.

The rule (a failure): on a page that loads KaTeX (a <script src> or <link href> naming katex), a CSS rule whose
selector list contains a selector whose LAST compound is exactly `span` or `*`, reached by a descendant (whitespace)
combinator, and whose declarations include `display:block` (any case, with or without !important).

Where it looks: every <style> block of every .html page under games/ that loads KaTeX, nested @media/@supports
included, and every local stylesheet such a page links (a rule there applies to the page just as much). KaTeX's own
CDN stylesheet is not read. Not covered: CSS a script writes at run time, and style="" attributes (no selector).

Reported, never failed (so the pattern can be tightened only by a ruling): a rule of the same kind whose last compound
is `span` or `*` with more on it (`span:first-child`, `span.x`), or with no ancestor at all (`span{...}`), or whose
combinator is `+` or `~`.
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import plant_common as pc  # noqa: E402  (scripts/ on the path above)

KATEX_TAG = re.compile(r"""<(?:script|link)\b[^>]*\b(?:src|href)\s*=\s*["'][^"']*katex[^"']*["']""", re.I)
STYLE = re.compile(r"<style\b[^>]*>(.*?)</style\s*>", re.I | re.S)
LINK = re.compile(r"""<link\b[^>]*>""", re.I)
HREF = re.compile(r"""\bhref\s*=\s*["']([^"']+)["']""", re.I)
STYLESHEET = re.compile(r"""\brel\s*=\s*["'][^"']*\bstylesheet\b""", re.I)
DISPLAY_BLOCK = re.compile(r"(?:^|;)\s*display\s*:\s*block\s*(?:!\s*important\s*)?(?:;|$)", re.I)
SPAN_OR_STAR = re.compile(r"^(?:span|\*)(?![\w-])", re.I)


def blank_comments(css):
    """CSS with /* */ comments replaced by spaces, newlines kept, so line numbers stay true."""
    return re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), css, flags=re.S)


def rules(css):
    """(prelude, body, offset of the prelude) for every rule whose body holds declarations, at any @-block depth.
    @-rule preludes (@media ...) are containers; @font-face, @page and the frames of @keyframes are skipped."""
    out, stack, start, i, n = [], [], 0, 0, len(css)
    while i < n:
        ch = css[i]
        if ch in "\"'":                                   # a string: skip to its close
            j = i + 1
            while j < n and css[j] != ch:
                j += 2 if css[j] == "\\" else 1
            i = j + 1
            continue
        if ch == "{":
            stack.append((css[start:i], start, i))
            start = i + 1
        elif ch == "}":
            if stack:
                prelude, pstart, brace = stack.pop()
                body = css[brace + 1:i]
                inside_at = any(p.strip().startswith("@") and not p.strip().lower().startswith(("@media", "@supports",
                                "@layer", "@container", "@document")) for p, _, _ in stack)
                if "{" not in body and not prelude.strip().startswith("@") and not inside_at:
                    lead = len(prelude) - len(prelude.lstrip())
                    out.append((prelude.strip(), body, pstart + lead))
            start = i + 1
        elif ch == ";" and not stack:
            start = i + 1                                 # a top-level @import/@charset statement
        i += 1
    return out


def split_top(s, seps):
    """Split s at characters in seps that are outside (), [] and strings."""
    parts, depth, cur, q = [], 0, [], None
    for ch in s:
        if q:
            cur.append(ch)
            if ch == q:
                q = None
            continue
        if ch in "\"'":
            q = ch
        elif ch in "([":
            depth += 1
        elif ch in ")]":
            depth -= 1
        if ch in seps and depth == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    return parts


def last_step(selector):
    """(combinator before the last compound, last compound). combinator is ' ' (descendant), '>', '+', '~', or ''
    when the selector is a single compound."""
    s, depth, q, i = selector.strip(), 0, None, len(selector.strip()) - 1
    # Walk back from the end to the last combinator outside () [] and strings.
    while i >= 0:
        ch = s[i]
        if q:
            if ch == q:
                q = None
        elif ch in "\"'":
            q = ch
        elif ch in ")]":
            depth += 1
        elif ch in "([":
            depth -= 1
        elif depth == 0 and (ch in ">+~" or ch.isspace()):
            break
        i -= 1
    compound = s[i + 1:]
    if i < 0:
        return "", compound
    head = s[:i + 1].rstrip()
    if head and head[-1] in ">+~":
        return head[-1], compound
    return " ", compound


def classify(selector):
    """'fail' (the rule's shape), 'near' (reported: span or * with more on it, no ancestor, or + ~), or None."""
    comb, compound = last_step(selector)
    if not SPAN_OR_STAR.match(compound):
        return None
    exact = compound.lower() in ("span", "*")
    if comb == " " and exact:
        return "fail"
    if comb in (" ", "") or (comb in "+~" and exact):
        return "near"
    return None


def css_findings(css, where, line0):
    """(fails, nears) for one stylesheet's text; where is its path, line0 the line its text starts on."""
    css = blank_comments(css)
    fails, nears = [], []
    for prelude, body, off in rules(css):
        if not DISPLAY_BLOCK.search(body):
            continue
        line = line0 + css.count("\n", 0, off)
        decl = " ".join(body.split())
        decl = decl if len(decl) <= 80 else decl[:79] + "…"
        for sel in split_top(prelude, ","):
            kind = classify(sel)
            if kind:
                (fails if kind == "fail" else nears).append("%s:%d: `%s{%s}`" % (where, line, sel.strip(), decl))
    return fails, nears


def linked_sheets(root, page_rel, src):
    """Local stylesheets the page links, as repo-relative paths that exist."""
    out = []
    for tag in LINK.findall(src):
        if not STYLESHEET.search(tag):
            continue
        h = HREF.search(tag)
        if not h:
            continue
        href = h.group(1).split("?")[0].split("#")[0]
        if re.match(r"^(?:[a-z]+:)?//", href, re.I):
            continue                                       # CDN or other host: not ours
        rel = href.lstrip("/") if href.startswith("/") else os.path.normpath(
            os.path.join(os.path.dirname(page_rel), href)).replace(os.sep, "/")
        if os.path.isfile(os.path.join(root, rel)):
            out.append(rel)
    return out


def pages(root):
    games = os.path.join(root, "games")
    for dirpath, _, files in os.walk(games):
        for f in sorted(files):
            if f.endswith(".html"):
                p = os.path.join(dirpath, f)
                yield os.path.relpath(p, root).replace(os.sep, "/"), p


def scan(root=ROOT, texts=None):
    """(fails, nears, number of KaTeX pages). texts: {repo-relative path: text} overriding files (the plants)."""
    texts = texts or {}
    read = lambda rel, p: texts[rel] if rel in texts else open(p, encoding="utf-8").read()  # noqa: E731
    fails, nears, n, sheets = [], [], 0, {}
    found = {rel for rel, _ in pages(root)}
    extra = [(rel, None) for rel in texts if rel.startswith("games/") and rel.endswith(".html") and rel not in found]
    for rel, p in list(pages(root)) + extra:
        src = read(rel, p)
        if not KATEX_TAG.search(src):
            continue
        n += 1
        for m in STYLE.finditer(src):
            f, nr = css_findings(m.group(1), rel, src.count("\n", 0, m.start(1)) + 1)
            fails += f
            nears += nr
        for sheet in linked_sheets(root, rel, src):
            if sheet not in sheets:
                sheets[sheet] = css_findings(read(sheet, os.path.join(root, sheet)), sheet, 1)
            f, nr = sheets[sheet]
            fails += ["%s (linked by %s)" % (x, rel) for x in f]
            nears += ["%s (linked by %s)" % (x, rel) for x in nr]
    return fails, nears, n


KATEX_HEAD = ('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">'
              '<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>')


def page(css, katex=True):
    return "<!doctype html><html><head>%s<style>\n%s\n</style></head><body></body></html>" % (KATEX_HEAD if katex else "", css)


def plants():
    """(name, texts, expect a failure?). The four of the amendment first, then the guards on scope and on the fix."""
    t = "games/zz-plant/index.html"
    out = [
        ("(a) `.x span{display:block}` fails", {t: page(".x span{display:block}")}, True),
        ("(b) `.x > span{display:block}` passes", {t: page(".x > span{display:block}")}, False),
        ("(c) `.x span{color:red}` passes", {t: page(".x span{color:red}")}, False),
        ("(d) `.x *{display:block}` fails", {t: page(".x *{display:block}")}, True),
        ("inside @media, in a selector list, with !important and a comment, fails",
         {t: page("@media (max-width:400px){ .a, .x  span /* c */ { color:red; DISPLAY : Block !important } }")}, True),
        ("(a) on a page that does not load KaTeX passes", {t: page(".x span{display:block}", katex=False)}, False),
        ("`.x span{display:inline-block}` passes", {t: page(".x span{display:inline-block}")}, False),
        ("`.x span.y{display:block}` passes (reported)", {t: page(".x span.y{display:block}")}, False),
    ]
    for rel, old, new, name in [
        ("games/free-daily-pizza/index.html", ".stage-btn > span{display:block", ".stage-btn span{display:block",
         "Free Daily Pizza's old `.stage-btn span` restored"),
        ("games/log-laws/index.html", ".mode-btn > span { display: block", ".mode-btn span { display: block",
         "Log Laws' old `.mode-btn span` restored"),
    ]:
        src = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        try:
            out.append((name + " fails", {rel: pc.apply_plant(src, old, new, name=name)}, True))
        except pc.StalePlant as e:
            out.append((name, e, True))
    # A rule in a local stylesheet that a KaTeX page links: the first one Free Daily Pizza links.
    fdp = "games/free-daily-pizza/index.html"
    linked = linked_sheets(ROOT, fdp, open(os.path.join(ROOT, fdp), encoding="utf-8").read())
    name = "the rule in a stylesheet a KaTeX game links (%s)" % (linked[0] if linked else "none found")
    try:
        if not linked:
            raise pc.StalePlant(name, "free-daily-pizza links no local stylesheet")
        src = open(os.path.join(ROOT, linked[0]), encoding="utf-8").read()
        out.append((name + " fails", {linked[0]: pc.apply_re_plant(src, r"\Z", "\n.zz-plant span{display:block}\n",
                                                                   name=name)}, True))
    except pc.StalePlant as e:
        out.append((name, e, True))
    return out


def selftest():
    ok = True
    for name, texts, expect in plants():
        if isinstance(texts, pc.StalePlant):
            print("  %s" % texts)
            ok = False
            continue
        try:
            fails, nears, _ = scan(ROOT, texts)
            err = None
        except Exception as e:  # an error is never a catch (plant_common)
            fails, nears, err = [], [], e
        # Only findings the plant introduced count: the plant file, or the sheet it edits.
        mine = [f for f in fails if any(f.startswith(k + ":") for k in texts)]
        got = pc.is_caught(mine, err)
        good = (got == expect) and err is None
        ok = ok and good
        print("  %s  %s%s" % ("ok  " if good else "FAIL", name,
                              (": " + (mine[0] if mine else "no finding")) if expect or mine else ""))
        if err is not None:
            print("        error: %r" % err)
    print("selftest: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    fails, nears, n = scan()
    print("KaTeX CSS (canon 7.1.1): %d page(s) under games/ load KaTeX" % n)
    for x in nears:
        print("  note  %s: span or * with display:block, not the failing shape (reported only)" % x)
    for x in fails:
        print("  FAIL  %s: a descendant `span`/`*` with display:block reaches into KaTeX's spans; use `>`" % x)
    print("PASS" if not fails else "FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
