#!/usr/bin/env python3
"""Write the one site footer into every page. Idempotent: a second run changes nothing.

    python scripts/apply-footer.py            # write
    python scripts/apply-footer.py --dry-run  # report what would change

The canonical markup, the stylesheet link and the exempt pages all come from
scripts/check-footer.py, which holds every page to them in CI. For each page this:

  1. replaces <footer class="site-footer" ...>...</footer> with the canonical markup
     (a new page needs only <footer class="site-footer"></footer> before </body>);
  2. removes every .site-footer rule from the page's <style> blocks, and from every
     .css file but the shared one (with a "/* Footer */" line heading a removed rule);
  3. links /schools/assets/site-footer.css once, just before </head>.

Two one-off cases are handled explicitly and are no-ops once applied:
  ADD     pages that had no footer at all; one is inserted before </body>.
  LEGACY  a page whose footer was a different element; it is replaced, with its CSS.

It refuses (exit 1, nothing written) on any <footer> it has no pattern for, and on a
.site-footer rule it cannot remove whole (a selector list shared with another selector,
or text before it in the same rule): those need a person, not a regex.
"""
import argparse, importlib.util, pathlib, re, sys

BASE = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("check_footer", BASE / "scripts" / "check-footer.py")
cf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cf)

EMPTY = '<footer class="site-footer"></footer>'

# Pages that had no footer. Jon's rulings: truth-will-set-you-free 29 Sep 2026, the
# regression-rumble holding page 2 Oct 2026 (visitors still land there).
ADD = {
    "games/truth-will-set-you-free/index.html",
    "games/regression-rumble/index.html",
}

# boolean-blitz carried its own in-flow <footer class="footer"> with its own CSS block
# (Jon's ruling 2 Oct 2026: bring it onto the standard footer).
LEGACY = {
    "games/boolean-blitz/index.html": [
        (re.compile(r'<footer class="footer">.*?</footer>', re.S), EMPTY),
        (re.compile(r'/\* ── Footer ─+ \*/\n\.footer \{[^{}]*\}\n\.footer a \{[^{}]*\}\n'
                    r'\.footer a:hover \{[^{}]*\}\n\n'), ''),
    ],
}

SITE_FOOTER = re.compile(r'<footer class="site-footer"[^>]*>.*?</footer>', re.S)
STYLE = re.compile(r'(<style\b[^>]*>)(.*?)(</style>)', re.S | re.I)
RULE = re.compile(r'\.site-footer\b[^{}]*\{[^{}]*\}')
MARK = "\x00"


class Refuse(Exception):
    pass


def read(path):
    with open(path, encoding="utf-8", newline="") as f:   # keep line endings as they are
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def strip_rules(css, where):
    """Remove every .site-footer rule from a block of CSS; drop lines left empty."""
    def sub(m):
        before = css[:m.start()]
        ends = [before.rfind(tok) + len(tok) for tok in ("{", "}", "*/") if tok in before]
        cut = max(ends, default=0)
        if before[cut:].strip():
            raise Refuse("%s: text before a .site-footer rule in the same rule: %r"
                         % (where, before[cut:].strip()[:80]))
        selector = m.group(0).split("{", 1)[0]
        if any(not s.strip().startswith(".site-footer") for s in selector.split(",")):
            raise Refuse("%s: selector list shares .site-footer with another selector: %r"
                         % (where, selector.strip()))
        return MARK
    marked = RULE.sub(sub, css)
    if MARK not in marked:
        return css
    lines = marked.split("\n")
    kept = []
    dropped = False
    for line in lines:
        if MARK in line and not line.replace(MARK, "").strip():
            if kept and kept[-1].strip() == "/* Footer */":
                kept.pop()
            dropped = True
            continue
        # A removed block that sat between two blank lines leaves one, not two.
        if dropped and not line.strip() and kept and not kept[-1].strip():
            dropped = False
            continue
        dropped = False
        kept.append(line.replace(MARK, ""))
    return "\n".join(kept)


def fix_page(rel, text):
    if rel in LEGACY and '<footer class="footer">' in text:
        for pat, rep in LEGACY[rel]:
            text, n = pat.subn(rep, text)
            if n != 1:
                raise Refuse("%s: legacy pattern %r matched %d times" % (rel, pat.pattern[:40], n))
    if rel in ADD and "<footer" not in text:
        if text.count("</body>") != 1:
            raise Refuse("%s: cannot place the footer (</body> count %d)" % (rel, text.count("</body>")))
        text = text.replace("</body>", EMPTY + "\n</body>")
    if "<footer" not in text:
        return text
    if len(re.findall(r"<footer\b", text)) != 1 or not SITE_FOOTER.search(text):
        raise Refuse("%s: a <footer> apply-footer.py has no pattern for" % rel)
    text = SITE_FOOTER.sub(lambda m: cf.CANONICAL, text)
    text = STYLE.sub(lambda m: m.group(1) + strip_rules(m.group(2), rel) + m.group(3), text)
    if cf.STYLESHEET not in text:
        if text.count("</head>") != 1:
            raise Refuse("%s: cannot place the stylesheet link (</head> count %d)"
                         % (rel, text.count("</head>")))
        text = text.replace("</head>", cf.STYLESHEET + "\n</head>")
    return text


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=str(BASE))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    root = pathlib.Path(args.root).resolve()

    changes = {}
    try:
        for rel in cf.pages(root):
            if cf.exemption(rel)[0]:
                continue
            old = read(root / rel)
            new = fix_page(rel, old)
            if new != old:
                changes[rel] = new
        for p in sorted(root.rglob("*.css")):
            rel = p.relative_to(root).as_posix()
            if set(rel.split("/")[:-1]) & cf.SKIP_DIRS or rel == cf.STYLESHEET_PATH:
                continue
            old = read(p)
            new = strip_rules(old, rel)
            if new != old:
                changes[rel] = new
    except Refuse as e:
        print("REFUSED, nothing written: %s" % e)
        return 1

    for rel in sorted(changes):
        print(("would change  " if args.dry_run else "changed  ") + rel)
        if not args.dry_run:
            write(root / rel, changes[rel])
    print("%d file(s) %s." % (len(changes), "would change" if args.dry_run else "changed"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
