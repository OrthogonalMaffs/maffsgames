#!/usr/bin/env python3
# ci-line: Child-look fragment (schools/assets/kids-look.js, MaffsKids: the #kids and #kids/<name> rule, the class page's bare #<name>, the "no second Class" greeting, the game and class links; nothing stored, sent or made global but MaffsKids; the class page's cards current with data/games.json; the class-name privacy rule; planted faults caught) |
# ci-deps: schools/assets/kids-look.js class/index.html data/games.json scripts/apply-class-page.py scripts/check-site.py
"""The child look's fragment rule, MaffsKids (schools/assets/kids-look.js; contract CLASS-PAGE, Jon 21 Nov 2026).

    python scripts/test-kids-look.py

No browser: kids-look.js runs in Node's vm module (as scripts/test-percentile.py runs firebase-leaderboard.js), in a
sandbox whose window, localStorage, sessionStorage, document.cookie, fetch, XMLHttpRequest, navigator.sendBeacon and
Image are spies. What it proves:
  (a) read(hash): "#kids" in any case is the child look with no name; "#kids/<name>" names the class when the name,
      decoded and trimmed, is 1 to 20 letters, spaces, hyphens or apostrophes (' or ’) with at least one letter; any
      other name (a digit, a tag, a slash, 21 letters, no letter, a malformed escape) gives no name but still the child
      look; anything else ("", "#", "#kidsx", "#Maple") is not the child look;
  (b) read(hash, 'bare'), the class page's: "#<name>" alone names the class by the same rule; "#kids" and
      "#kids/<name>" read as in (a);
  (c) greeting(): {name} filled in, and a name ending "class" (any case) not given a second "Class";
  (d) gameLink() and classLink(): "#kids/<encoded>" / "#kids" and "#<encoded>" / ""; every name read back unchanged;
  (e) nothing touched any spy, and the only new global is MaffsKids.
The expected values are written here, not taken from kids-look.js. Also: class/index.html's cards are what
scripts/apply-class-page.py writes from data/games.json ("kids": true), and check-site.py's class-name rule
(class_name_faults) passes on the repo and catches its plants.

Planted faults, each a one-line change that must make a check fail: names up to 30 characters (a), the second-Class
rule dropped (c), the bare mode ignored (b), the name written to localStorage (e), the name sent with fetch (e); and for
the page and the privacy rule: a card removed from the page, "Maple" in a served script's string, a hard-coded
#kids/<name> link in the class page, a name from MAFFS_CLASS_NAMES in a page. "Maple" in a comment is not a fault.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "schools", "assets", "kids-look.js")
sys.path.insert(0, HERE)
import plant_common as pc  # noqa: E402

HARNESS = r"""
const fs = require('fs'), vm = require('vm');
const src = fs.readFileSync(process.argv[2], 'utf8');
const cases = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const touched = [];
function spy(name) {
  return new Proxy(function () {}, {
    get(t, k) { if (k === Symbol.toPrimitive || k === 'then') return undefined; touched.push(name + '.' + String(k)); return spy(name + '.' + String(k)); },
    set(t, k) { touched.push(name + '.' + String(k) + '='); return true; },
    apply() { touched.push(name + '()'); return spy(name + '()'); },
    construct() { touched.push('new ' + name); return spy(name); }
  });
}
const doc = {};
Object.defineProperty(doc, 'cookie', { get() { touched.push('document.cookie'); return ''; }, set() { touched.push('document.cookie='); } });
const sandbox = { console: { log() {}, warn() {}, error() {} }, document: doc,
  localStorage: spy('localStorage'), sessionStorage: spy('sessionStorage'), fetch: spy('fetch'),
  XMLHttpRequest: spy('XMLHttpRequest'), Image: spy('Image'), navigator: { sendBeacon: spy('navigator.sendBeacon') } };
sandbox.window = sandbox;
['localStorage', 'sessionStorage', 'fetch', 'XMLHttpRequest', 'Image', 'navigator', 'document', 'console', 'window']
  .forEach(k => Object.defineProperty(sandbox, k, { value: sandbox[k], enumerable: false, writable: false }));
vm.createContext(sandbox);
const before = Object.keys(sandbox);
const fails = [];
try { vm.runInContext(src, sandbox); } catch (e) { fails.push('kids-look.js threw: ' + e); }
const K = sandbox.MaffsKids;
if (!K) { console.log(JSON.stringify({ fails: fails.concat(['no MaffsKids']), touched })); process.exit(0); }
const added = Object.keys(sandbox).filter(k => !before.includes(k));
if (added.join() !== 'MaffsKids') fails.push('globals added: ' + JSON.stringify(added) + ', expected only MaffsKids');
const eq = (a, b) => JSON.stringify(a) === JSON.stringify(b);
for (const [hash, mode, want] of cases.read) {
  const got = JSON.parse(JSON.stringify(mode ? K.read(hash, mode) : K.read(hash)));
  if (!eq(got, want)) fails.push('(' + (mode ? 'b' : 'a') + ') read(' + JSON.stringify(hash) + (mode ? ", '" + mode + "'" : '') + ') = ' + JSON.stringify(got) + ', expected ' + JSON.stringify(want));
}
for (const [tpl, name, want] of cases.greeting) {
  const got = K.greeting(tpl, name);
  if (got !== want) fails.push('(c) greeting(' + JSON.stringify(tpl) + ', ' + JSON.stringify(name) + ') = ' + JSON.stringify(got) + ', expected ' + JSON.stringify(want));
}
for (const [name, game, back] of cases.links) {
  if (K.gameLink(name) !== game) fails.push('(d) gameLink(' + JSON.stringify(name) + ') = ' + JSON.stringify(K.gameLink(name)) + ', expected ' + JSON.stringify(game));
  if (K.classLink(name) !== back) fails.push('(d) classLink(' + JSON.stringify(name) + ') = ' + JSON.stringify(K.classLink(name)) + ', expected ' + JSON.stringify(back));
  if (name && K.read(K.gameLink(name)).name !== name) fails.push('(d) ' + JSON.stringify(name) + ' does not survive gameLink then read');
  if (name && K.read(K.classLink(name), 'bare').name !== name) fails.push('(d) ' + JSON.stringify(name) + ' does not survive classLink then read bare');
}
if (touched.length) fails.push('(e) kids-look.js touched ' + JSON.stringify([...new Set(touched)].slice(0, 6)) + ': nothing may be stored or sent');
console.log(JSON.stringify({ fails }));
"""

NO = {"kids": False, "name": None}
KIDS = {"kids": True, "name": None}


def named(n):
    return {"kids": True, "name": n}


TWENTY = "Abcdefghijklmnopqrst"
CASES = {
    "read": [
        ["", None, NO], ["#", None, NO], ["#kidsx", None, NO], ["#Maple", None, NO], ["#kid", None, NO],
        ["#kids", None, KIDS], ["#KIDS", None, KIDS], ["kids", None, KIDS],
        ["#kids/Maple", None, named("Maple")], ["#Kids/Maple", None, named("Maple")],
        ["#kids/Maple%20Class", None, named("Maple Class")], ["#kids/%20Maple%20", None, named("Maple")],
        ["#kids/O'Brien", None, named("O'Brien")], ["#kids/St%E2%80%99s", None, named("St’s")],
        ["#kids/Anne-Marie", None, named("Anne-Marie")], ["#kids/Zo%C3%AB", None, named("Zoë")],
        ["#kids/" + TWENTY, None, named(TWENTY)],
        ["#kids/", None, KIDS], ["#kids/%20%20", None, KIDS], ["#kids/Year%206", None, KIDS],
        ["#kids/<script>", None, KIDS], ["#kids/%3Cscript%3Ealert(1)%3C%2Fscript%3E", None, KIDS],
        ["#kids/Maple/Class", None, KIDS], ["#kids/" + TWENTY + "u", None, KIDS], ["#kids/---", None, KIDS],
        ["#kids/'", None, KIDS], ["#kids/%E0%A4%A", None, KIDS], ["#kids/Maple.", None, KIDS],
        ["#Maple", "bare", named("Maple")], ["#Maple%20Class", "bare", named("Maple Class")],
        ["#kids", "bare", KIDS], ["#kids/Maple", "bare", named("Maple")], ["#Year6", "bare", KIDS],
        ["#%3Cb%3E", "bare", KIDS], ["#%E0%A4%A", "bare", KIDS], ["", "bare", NO], ["#", "bare", NO],
    ],
    "greeting": [
        ["Welcome, {name} Class!", "Maple", "Welcome, Maple Class!"],
        ["Welcome, {name} Class!", "Maple Class", "Welcome, Maple Class!"],
        ["Welcome, {name} Class!", "Maple class", "Welcome, Maple class!"],
        ["Welcome, {name} Class!", "MAPLE CLASS", "Welcome, MAPLE CLASS!"],
        ["Welcome, {name} Class!", "Classy", "Welcome, Classy Class!"],
        ["Welcome, {name} Class!", "O'Brien", "Welcome, O'Brien Class!"],
    ],
    "links": [
        [None, "#kids", ""], ["Maple", "#kids/Maple", "#Maple"],
        ["Maple Class", "#kids/Maple%20Class", "#Maple%20Class"], ["St’s", "#kids/St%E2%80%99s", "#St%E2%80%99s"],
        ["O'Brien", "#kids/O'Brien", "#O'Brien"], ["Zoë", "#kids/Zo%C3%AB", "#Zo%C3%AB"],
    ],
}

PLANTS = [
    ("names up to 30 characters", "var NAME = /^[\\p{L}' ’-]{1,20}$/u", "var NAME = /^[\\p{L}' ’-]{1,30}$/u", "(a)"),
    ("the second-Class rule dropped", "    if (/class$/i.test(name)) g = g.replace(/(class)\\s+class\\b/i, '$1');\n", "", "(c)"),
    ("the bare mode ignored", "} else if (mode === 'bare' && frag) {", "} else if (false) {", "(b)"),
    ("the name written to localStorage", "    return NAME.test(nm) && LETTER.test(nm) ? nm : null;",
     "    try { window.localStorage.setItem('k', nm); } catch (e) {}\n    return NAME.test(nm) && LETTER.test(nm) ? nm : null;", "(e)"),
    ("the name sent with fetch", "    return NAME.test(nm) && LETTER.test(nm) ? nm : null;",
     "    if (typeof fetch === 'function') fetch('/log?' + nm);\n    return NAME.test(nm) && LETTER.test(nm) ? nm : null;", "(e)"),
]


def find_node():
    node = shutil.which("node")
    if node:
        return node
    try:
        import playwright
        cand = os.path.join(os.path.dirname(playwright.__file__), "driver", "node")
        if os.path.exists(cand) or os.path.exists(cand + ".exe"):
            return cand
    except ImportError:
        pass
    sys.exit("FAIL  no node on PATH and no Playwright driver node")


def run(node, source, work, tag):
    path = os.path.join(work, "kl-%s.js" % tag)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(source)
    p = subprocess.run([node, os.path.join(work, "harness.js"), path, os.path.join(work, "cases.json")],
                       capture_output=True, text=True, encoding="utf-8")
    if p.returncode != 0:
        return None, p.stderr.strip()
    return json.loads(p.stdout)["fails"], None


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def page_and_privacy():
    """[fault] for the real files, then [(plant, caught?)] for the page and the privacy rule."""
    ap = load("apply_class_page", os.path.join("scripts", "apply-class-page.py"))
    cs = load("check_site", os.path.join("scripts", "check-site.py"))
    real = ap.faults() + cs.class_name_faults(names=[cs.CLASS_NAME_EXAMPLE])
    with open(ap.PAGE, encoding="utf-8") as f:
        page = f.read()
    results = []
    block = ap.current(page)
    first_card = block[block.index('<a class="card"'):block.index('</a>') + len('</a>\n')]
    results.append(("a card removed from the class page", bool(ap.faults(pc.apply_plant(page, first_card, "", name="a card")))))
    kl = open(SRC, encoding="utf-8").read()
    planted = pc.apply_plant(kl, "  'use strict';\n", "  'use strict';\n  var EXAMPLE = 'Maple';\n", name="Maple in a string")
    results.append(('"Maple" in a served script\'s string', bool(cs.class_name_faults({"schools/assets/kids-look.js": planted}, ["Maple"]))))
    results.append(('"Maple" in a comment held as no fault', not cs.class_name_faults({"schools/assets/kids-look.js": kl}, ["Maple"])))
    planted = pc.apply_plant(page, "var TEMPLATE = ", "var LINK = '#kids/Oak'; var TEMPLATE = ", name="a hard-coded link")
    results.append(("a hard-coded #kids/<name> link in the class page", bool(cs.class_name_faults({"class/index.html": planted}, ["Maple"]))))
    planted = pc.apply_plant(page, "<h1>Pick a game!</h1>", "<h1>Pick a game, Oakwood!</h1>", name="an env name")
    results.append(("a MAFFS_CLASS_NAMES name in a page", bool(cs.class_name_faults({"class/index.html": planted}, ["Maple", "Oakwood"]))))
    return real, results


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    src = open(SRC, encoding="utf-8").read()
    node = find_node()
    work = tempfile.mkdtemp(prefix="test-kids-look-")
    failed = []
    try:
        with open(os.path.join(work, "harness.js"), "w", encoding="utf-8", newline="") as f:
            f.write(HARNESS)
        with open(os.path.join(work, "cases.json"), "w", encoding="utf-8", newline="") as f:
            json.dump(CASES, f)
        fails, err = run(node, src, work, "real")
        if fails is None:
            print("FAIL  the harness did not run on the real file: " + err)
            return 1
        for x in fails:
            print("FAIL  " + x)
        failed += fails
        print("kids-look.js: %d read, %d greeting and %d link cases, the spies and the globals: %s"
              % (len(CASES["read"]), len(CASES["greeting"]), len(CASES["links"]), "PASS" if not fails else "FAILED"))
        for i, (what, old, new, part) in enumerate(PLANTS):
            try:
                planted = pc.apply_plant(src, old, new, name=what)
            except pc.StalePlant as e:
                print("  plant %-40s %s" % (what, e))
                failed.append(str(e))
                continue
            got, err = run(node, planted, work, "plant%d" % i)
            caught = got is not None and any(x.startswith(part) for x in got)
            print("  plant %-40s %s" % (what, "caught: " + [x for x in got if x.startswith(part)][0][:90] if caught
                                         else "*** MISSED *** %s" % (err or got)))
            if not caught:
                failed.append("plant missed: " + what)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    try:
        real, results = page_and_privacy()
    except pc.StalePlant as e:
        print("FAIL  " + str(e))
        return 1
    for x in real:
        print("FAIL  " + x)
    failed += real
    print("class page cards and the class-name rule on the repo: %s" % ("PASS" if not real else "FAILED"))
    for what, ok in results:
        print("  plant %-48s %s" % (what, ("caught" if "no fault" not in what else "ok") if ok else "*** MISSED ***"))
        if not ok:
            failed.append("plant missed: " + what)
    print("FAILED (%d)" % len(failed) if failed else "PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
