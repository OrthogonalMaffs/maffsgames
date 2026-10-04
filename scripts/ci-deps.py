#!/usr/bin/env python3
"""Which content verifiers must run for a change? A dependency map DERIVED from the files, never kept by hand.

    python scripts/ci-deps.py --explain                    # every verifier and what it depends on
    python scripts/ci-deps.py --files games/split-it/index.html schools/assets/answer.js
    python scripts/ci-deps.py --changed-from origin/main   # the files changed since a commit (git diff)
    python scripts/ci-deps.py --all                        # select everything (push to main, schedule)
    python scripts/ci-deps.py --selftest                   # the selection proofs (CI runs this first)

CI (canon §7.8, 4 Oct 2026). The checks live in .github/workflows/check-site.yml, as before. Groups whose name
starts "Content verifiers" are per-game: on a pull request each of their lines runs only when this script
selects it. Every other group, and the leaderboard-coverage job, always runs (site-wide checks). On a push to
main, the weekly schedule and a manual run, everything runs.

A verifier's dependencies, derived from its source and the pages it tests:
  - the script itself and every local module it imports (recursively), or names as a file;
  - every repo path its string literals name (a file, or a folder as a prefix);
  - each game it names (a literal equal to a games/ folder name, or containing games/<slug>/): that whole
    folder, plus every local file the game's page loads (src/href and quoted asset paths), followed through
    the shared JS and CSS it loads in turn.
A verifier that names no page and is not a library's own self-test (`python scripts/<module>.py --selftest`
for a module other scripts import) cannot be mapped, so it ALWAYS runs; so does one whose pages load a local
file through a computed path (a fetch, import() or script element whose target is not a literal).

A changed path selects:
  - ALL verifiers: anything under .github/, scripts/ci-*, requirements*.txt, or a path in no known area;
  - the verifiers whose dependencies include it;
  - nothing extra: a known area no verifier depends on (other games and pages, docs, data, site-wide check
    scripts). The site-wide checks, which always run, cover those.
"""
import argparse, ast, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKFLOW = ".github/workflows/check-site.yml"
SELECTIVE_PREFIX = "Content verifiers"
ALL_PREFIXES = (".github/", "scripts/ci-", "requirements")
# Top-level areas whose files are classified (not "unknown"): the published site, docs and the checks.
KNOWN_TOP = {"games", "escape-rooms", "schools", "parents", "about", "feedback", "leaderboards", "privacy",
             "resit", "spec-map", "updates", "year6", "op", "6-7", "data", "docs", ".claude", "scripts"}
KNOWN_ROOT_FILES = {"index.html", "sitemap.xml", "robots.txt", "CNAME", "_config.yml", "CLAUDE.md",
                    ".gitignore", ".gitleaks.toml"}
# Folders too wide to be a dependency: a literal naming one is a URL prefix or a search root, not a file
# the verifier reads (its games come from the slugs it names). Never a prefix match.
WIDE = {"", ".", "..", "games", "schools", "schools/assets", "docs", "data", "scripts", "escape-rooms"}
ASSET_EXT = (".js", ".css", ".json", ".csv", ".txt", ".svg", ".png", ".webp", ".jpg", ".woff2", ".woff", ".mjs")


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, "/")


def exists(r):
    return bool(r) and os.path.exists(os.path.join(ROOT, r))


def game_slugs():
    g = os.path.join(ROOT, "games")
    return {d for d in os.listdir(g) if os.path.isfile(os.path.join(g, d, "index.html"))}


# ---------------------------------------------------------------- the workflow's checks
def checks():
    """[(group, selective, label, command, script)] from check-site.yml, in order."""
    import yaml
    with open(os.path.join(ROOT, WORKFLOW), encoding="utf-8") as f:
        wf = yaml.safe_load(f)
    out = []
    for inc in wf["jobs"]["check-site"]["strategy"]["matrix"]["include"]:
        sel = inc["name"].startswith(SELECTIVE_PREFIX)
        for line in inc["checks"].strip().splitlines():
            label, cmd = line.split("|", 1)
            m = re.search(r"scripts/[\w.-]+\.py", cmd)
            out.append((inc["name"], sel, label.strip(), cmd.strip(), m.group(0) if m else None))
    return out


# ---------------------------------------------------------------- a Python script's own dependencies
# A literal is tagged by where it came from: OWN (the verifier itself), LIB (a module it imports: names
# files it reads, never the games or pages a verifier tests), and JOIN (built by os.path.join or Path /,
# so it is a path even with no "/" in it).
OWN, LIB = "own", "lib"


def py_literals(tree):
    """[(text, is_join)]: every string constant, plus the paths os.path.join(ROOT, "a", "b") and
    Path / "a" / "b" spell out."""
    lits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            lits.append((node.value, False))
        if isinstance(node, ast.Call) and getattr(node.func, "attr", getattr(node.func, "id", "")) in ("join", "Path"):
            # A path from the repo root only when every part after the first (ROOT) is a literal:
            # os.path.join(GAMES_DIR, SLUG, "index.html") is not the portal's index.html.
            tail = node.args[1:] if node.args and not isinstance(node.args[0], ast.Constant) else node.args
            if tail and all(isinstance(a, ast.Constant) and isinstance(a.value, str) for a in tail):
                lits.append(("/".join(a.value for a in tail), True))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            parts, n, ok = [], node, True
            while isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div):
                if isinstance(n.right, ast.Constant) and isinstance(n.right.value, str):
                    parts.insert(0, n.right.value)
                else:
                    ok = False                       # root / slug / "index.html": not a fixed path
                n = n.left
            if not ok:
                continue
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                parts.insert(0, n.value)
            if parts:
                lits.append(("/".join(parts), True))
    return lits


def script_deps(script, seen=None, origin=OWN):
    """(paths, [(text, is_join, origin)]) for a script and, recursively, the local modules it imports."""
    seen = set() if seen is None else seen
    if script in seen or not exists(script):
        return set(), []
    seen.add(script)
    tree = ast.parse(open(os.path.join(ROOT, script), encoding="utf-8").read())
    paths = {script}
    lits = [(t, j, origin) for t, j in py_literals(tree)]
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module.split(".")[0])
    for t, _, _ in lits:                             # importlib by file: spec_from_file_location("x", ".../x.py")
        if t.endswith(".py") and exists("scripts/" + os.path.basename(t)):
            mods.add(os.path.basename(t)[:-3])
    for m in mods:
        if exists("scripts/%s.py" % m):
            p, l = script_deps("scripts/%s.py" % m, seen, LIB)
            paths |= p
            lits += l
    return paths, lits


PATHLIKE = re.compile(r"/|\.[A-Za-z0-9]{2,5}$")


def literal_paths(lits):
    """Repo paths the literals name: a file, or a folder (as 'folder/', never a WIDE one, never from a
    library). Only path-like literals count (a '/', a file extension, or built by a join), so a word such
    as "feedback" is not the feedback/ folder. A template ("parents/%s/index.html") names the folder before
    its first placeholder. A library's literals never name a page."""
    out = set()
    for text, joined, origin in lits:
        s = text.strip()
        if not s or "\n" in s or " " in s or len(s) > 200:
            continue
        if not (joined or PATHLIKE.search(s)):
            continue
        cut = min([s.index(c) for c in "%{" if c in s] or [len(s)])
        if cut < len(s):
            s = s[:cut].rsplit("/", 1)[0] + "/"
        s = s.split("?")[0].split("#")[0]
        while s.startswith("./") or s.startswith("/"):
            s = s[1:] if s.startswith("/") else s[2:]
        # A bare file name ("index.html", "roster-levels.json") is a file beside the scripts, never a page:
        # only a literal with a folder in it, or one built by a join, is a path from the repo root.
        bare = not joined and "/" not in text.strip().rstrip("/")
        for cand in (("scripts/" + s,) if bare else (s, "scripts/" + s)):
            cand = os.path.normpath(cand).replace(os.sep, "/") + ("/" if cand.endswith("/") else "")
            if cand.startswith("..") or cand in ("./", "/") or not exists(cand):
                continue
            if os.path.isdir(os.path.join(ROOT, cand)):
                if origin == OWN and cand.rstrip("/") not in WIDE:
                    out.add(cand.rstrip("/") + "/")
            elif not (origin == LIB and cand.endswith(".html")):
                out.add(cand)
    return out


def named_games(lits, slugs):
    """The games a verifier names in its OWN source: a literal equal to a games/ folder, or containing
    games/<slug>."""
    found = set()
    for text, _, origin in lits:
        if origin != OWN:
            continue
        if text in slugs:
            found.add(text)
        for m in re.finditer(r"games/([a-z0-9-]+)", text):
            if m.group(1) in slugs:
                found.add(m.group(1))
    return found


# ---------------------------------------------------------------- what a page loads
REF = re.compile(r"""(?:src|href)\s*=\s*["']([^"'#?]+)|["'`]([^"'`\s]+\.(?:js|css|json|csv|txt|svg|png|webp|jpg|woff2?|mjs))["'`]|url\(\s*["']?([^"')]+)""")
DYNAMIC = re.compile(r"""\b(fetch|import)\s*\(\s*([^)'"`\s][^),]*)|createElement\(\s*['"]script['"]\s*\)""")


def resolve(ref, base_dir):
    if re.match(r"^[a-z]+:|^//|^data:|^mailto:|^#", ref):
        return None
    p = ref.lstrip("/") if ref.startswith("/") else os.path.normpath(os.path.join(base_dir, ref)).replace(os.sep, "/")
    if p.endswith("/"):
        p += "index.html"
    return p if exists(p) else None


def page_deps(page, seen=None, hazards=None):
    """Local files a page (or a JS/CSS file) loads, transitively; hazards = computed-path loads found."""
    seen = set() if seen is None else seen
    hazards = [] if hazards is None else hazards
    if page in seen or not exists(page):
        return seen, hazards
    seen.add(page)
    text = open(os.path.join(ROOT, page), encoding="utf-8", errors="replace").read()
    base = os.path.dirname(page)
    for m in REF.finditer(text):
        ref = next(g for g in m.groups() if g)
        p = resolve(ref, base)
        if p and (p.endswith(ASSET_EXT) or p.endswith(".html")) and not p.endswith("/index.html") or p == page:
            if p and p.endswith(ASSET_EXT):
                page_deps(p, seen, hazards)
    for m in DYNAMIC.finditer(text):
        if m.group(0).startswith("createElement"):
            # A script element: fine when every .src it is given in this file is a literal.
            if re.search(r"\.src\s*=\s*(?![\"'`])", text):
                hazards.append("%s: a script element with a computed src" % page)
            continue
        arg = m.group(2).strip()
        lit = re.search(r"\b%s\s*=\s*['\"`]([^'\"`]+)" % re.escape(arg), text) if re.match(r"^[A-Za-z_$][\w$]*$", arg) else None
        if lit and re.match(r"^https?://", lit.group(1)):
            continue                                 # a constant external endpoint (analytics)
        if lit and resolve(lit.group(1), base):
            page_deps(resolve(lit.group(1), base), seen, hazards)
            continue
        hazards.append("%s: %s(%s) loads a computed path" % (page, m.group(1), arg[:40]))
    return seen, hazards


# ---------------------------------------------------------------- the map
def dependency_map():
    """{script: {"deps": set, "games": set, "always": reason or None}} for every script the workflow runs."""
    slugs = game_slugs()
    libs = set()                                     # modules other scripts import
    for _, _, _, _, s in checks():
        if s:
            p, _ = script_deps(s)
            libs |= {x for x in p if x != s}
    out = {}
    for group, sel, label, cmd, s in checks():
        if not s or s in out:
            continue
        paths, lits = script_deps(s)
        games = named_games(lits, slugs)
        deps = set(paths) | literal_paths(lits)
        hazards = []
        pages = {d for d in deps if d.endswith(".html")} | {"games/%s/index.html" % g for g in games}
        for d in list(deps):
            if d.endswith("/"):
                for dp, _, fs in os.walk(os.path.join(ROOT, d)):
                    pages |= {rel(os.path.join(dp, f)) for f in fs if f.endswith(".html")}
        for g in games:
            deps.add("games/%s/" % g)
        for pg in pages:
            loaded, hz = page_deps(pg)
            deps |= loaded
            hazards += hz
        always = None
        if hazards:
            always = "; ".join(sorted(set(hazards)))
        elif not games and not pages and not (s in libs and "--selftest" in cmd):
            always = "names no page and is not a library's self-test"
        out[s] = {"deps": deps, "games": games, "always": always, "selective": sel, "label": label}
    return out


def in_deps(path, deps):
    return any(path == d or (d.endswith("/") and path.startswith(d)) for d in deps)


def classify(path):
    """'all' | 'known' | 'unknown' for a changed path no verifier depends on."""
    if path.startswith(ALL_PREFIXES):
        return "all"
    top = path.split("/", 1)[0]
    if "/" not in path:
        return "known" if path in KNOWN_ROOT_FILES or path.endswith(".md") else "unknown"
    return "known" if top in KNOWN_TOP else "unknown"


def select(changed, dmap=None):
    """(run_all, reasons, {script: [why]}) for a list of changed paths."""
    dmap = dependency_map() if dmap is None else dmap
    picked, reasons = {}, []
    for s, info in dmap.items():
        if info["selective"] and info["always"]:
            picked.setdefault(s, []).append("always runs: " + info["always"])
    for path in changed:
        path = path.replace("\\", "/").strip()
        if not path:
            continue
        kind = classify(path)
        if kind == "all":
            reasons.append("%s changes CI itself: everything runs" % path)
            return True, reasons, {}
        hit = [s for s, info in dmap.items() if info["selective"] and in_deps(path, info["deps"])]
        for s in hit:
            picked.setdefault(s, []).append(path)
        if not hit and kind == "unknown":
            reasons.append("%s is in no known area: everything runs" % path)
            return True, reasons, {}
    return False, reasons, picked


def changed_since(base):
    out = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True)
    return [l for l in out.stdout.splitlines() if l.strip()]


# ---------------------------------------------------------------- the selection proofs
def selftest():
    dmap = dependency_map()
    sel = {s: i for s, i in dmap.items() if i["selective"]}
    fails = []

    def check(name, ok, detail):
        print("  %s  %-62s %s" % ("PASS" if ok else "FAIL", name, detail))
        if not ok:
            fails.append(name)

    always = {s for s, i in sel.items() if i["always"]}
    # (a) one game's page runs the verifiers that name that game, and no other.
    for g in sorted({g for i in sel.values() for g in i["games"]}):
        _, _, picked = select(["games/%s/index.html" % g], dmap)
        want = {t for t, j in sel.items() if g in j["games"]} | always
        check("(a) games/%s/index.html" % g, set(picked) == want and bool(picked),
              "-> " + ", ".join(sorted(os.path.basename(p) for p in picked)))
    # (b) a shared asset fans out to every verifier whose pages load it, and to none that don't.
    for asset in ("schools/assets/answer.js", "schools/assets/theme.css", "schools/assets/calculator.js",
                  "schools/assets/teacher-invite.js"):
        _, _, picked = select([asset], dmap)
        want = {s for s, i in sel.items() if asset in i["deps"]} | always
        loaders = {s for s, i in sel.items() for g in i["games"]
                   if re.search(re.escape(os.path.basename(asset)), open(os.path.join(ROOT, "games", g, "index.html"), encoding="utf-8").read())}
        check("(b) %s" % asset, set(picked) == want and loaders <= set(picked),
              "-> %d verifiers: %s" % (len(picked), ", ".join(sorted(os.path.basename(p) for p in picked))))
    # (c) CI itself, and a path in no known area, run everything.
    for p in (".github/workflows/check-site.yml", "scripts/ci-deps.py", "requirements-ci.txt", "newdir/x.txt", "package.json"):
        run_all, why, _ = select([p], dmap)
        check("(c) %s runs everything" % p, run_all, why[0] if why else "")
    # A doc-only change runs no verifier (beyond any that always run).
    _, _, picked = select(["docs/todo.md", "CLAUDE.md"], dmap)
    check("docs-only change runs no verifier", set(picked) == always, "-> %d" % len(picked))
    # Every selective verifier is reachable: some path selects it (or it always runs).
    for s, i in sorted(sel.items()):
        _, _, picked = select([s], dmap)
        check("its own script selects %s" % os.path.basename(s), s in picked, "")
    print("selftest: %s" % ("FAILED: " + ", ".join(fails) if fails else "PASS"))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--files", nargs="*")
    ap.add_argument("--changed-from")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--explain", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--github-output", help="write run_all and selected (JSON list of scripts) here")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    dmap = dependency_map()
    if a.explain:
        for s, i in dmap.items():
            if not i["selective"]:
                continue
            print("%s%s" % (s, "   [ALWAYS: %s]" % i["always"] if i["always"] else ""))
            print("   games: %s" % (", ".join(sorted(i["games"])) or "-"))
            print("   deps:  %s" % ", ".join(sorted(d for d in i["deps"] if d != s)))
        return 0
    if a.all:
        run_all, reasons, picked = True, ["full run requested"], {}
    else:
        changed = a.files if a.files is not None else changed_since(a.changed_from or "origin/main")
        print("changed: %d file(s)" % len(changed))
        for c in changed[:40]:
            print("  " + c)
        run_all, reasons, picked = select(changed, dmap)
    selected = sorted(s for s, i in dmap.items() if i["selective"]) if run_all else sorted(picked)
    for r in reasons:
        print(r)
    print("verifiers selected: %s" % ("ALL (%d)" % len(selected) if run_all else len(selected)))
    for s in selected:
        print("  %s%s" % (s, "" if run_all else "  <- " + ", ".join(picked[s][:3])))
    if a.github_output:
        with open(a.github_output, "a", encoding="utf-8") as f:
            f.write("run_all=%s\n" % ("true" if run_all else "false"))
            f.write("selected=%s\n" % json.dumps(selected))
    return 0


if __name__ == "__main__":
    sys.exit(main())
