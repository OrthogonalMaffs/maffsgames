# The second count (Jon, 2 Oct): a string counts if any real word -- B7's own
# notion of a word, a run of 2+ letters left after B7's stripping -- loses, in
# the rendered output, a space it had in the source. "Rendered output" is what
# the student sees: .katex-html text, plus a space for every positive-width
# .mspace (KaTeX draws operator/relation spacing as empty spans), zero-width
# spaces dropped, nbsp/thin spaces read as spaces.
import json, re, subprocess, os, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CODE = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get("AUDIT_KATEX_WORK") or os.path.join(__import__("tempfile").gettempdir(), "audit-katex")
os.makedirs(WORK, exist_ok=True)
KATEX = os.environ.get("AUDIT_KATEX_DIR") or os.path.join(WORK, "package", "dist")
HERE = WORK
sys.path.insert(0, os.path.join(REPO, "scripts"))
sys.path.insert(0, CODE)
from html.parser import HTMLParser
import bank_common as bc
WORD = re.compile(r"(?<![A-Za-z])[A-Za-z]{2,}(?![A-Za-z])")


class Vis(HTMLParser):
    def __init__(self):
        super().__init__(); self.out = []; self.stack = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); cls = a.get("class", "") or ""
        skip = "katex-mathml" in cls.split()
        self.stack.append(skip)
        if skip:
            self.skip += 1
        if not self.skip and "mspace" in cls.split():
            m = re.search(r"(?:margin-right|width):\s*(-?[\d.]+)em", a.get("style", "") or "")
            if m and float(m.group(1)) > 0:
                self.out.append(" ")
    def handle_endtag(self, tag):
        if self.stack and self.stack.pop():
            self.skip -= 1
    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)


def spaced_visual(html):
    v = Vis(); v.feed(html)
    t = "".join(v.out).replace("​", "")
    return re.sub(r"[  -   \s]+", " ", t)


def stripped(s):
    s2 = bc._KATEX_TEXT_MODE_WRAP.sub("", s)
    return bc._KATEX_COMMAND.sub("", s2)


def lost_words(s, vis):
    src = stripped(s)
    out = []
    for w in sorted(set(m.group(0) for m in WORD.finditer(src))):
        sb = sum(1 for m in re.finditer(r"(?<![A-Za-z])%s(?![A-Za-z])" % w, src) if m.start() > 0 and src[m.start() - 1].isspace())
        sa = sum(1 for m in re.finditer(r"(?<![A-Za-z])%s(?![A-Za-z])" % w, src) if m.end() < len(src) and src[m.end()].isspace())
        vb = sum(1 for m in re.finditer(re.escape(w), vis) if m.start() > 0 and vis[m.start() - 1] == " ")
        va = sum(1 for m in re.finditer(re.escape(w), vis) if m.end() < len(vis) and vis[m.end()] == " ")
        if vb < sb or va < sa:
            out.append(w)
    return out


def main():
    R = json.load(open(os.path.join(HERE, "results.json")))
    keys = [(slug, s, e["display"]) for slug, d in R.items() for s, e in d.items()]
    uniq = sorted({(s, d) for _, s, d in keys})
    html = json.loads(subprocess.run(["node", os.path.join(CODE, "rerender.js"), KATEX], input=json.dumps(uniq),
                                     capture_output=True, text=True, check=True).stdout)
    vis = {k: spaced_visual(h) if h else "" for k, h in zip(uniq, html)}
    for slug, s, d in keys:
        e = R[slug][s]
        e["spaced_visual"] = vis[(s, d)]
        e["lost_words"] = lost_words(s, vis[(s, d)])
        e["space_loss"] = bool(e["lost_words"])
    json.dump(R, open(os.path.join(HERE, "results.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
