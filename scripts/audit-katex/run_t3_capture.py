# run_t3_capture.py <repo> <out.jsonl> <menu_choice> <slug,slug,...> [check-site args...]
# Runs scripts/check-site.py's tier 3 UNCHANGED (imported as a module), with:
#  - the sandbox network recipe of docs/sandbox-checks.md (local KaTeX, inert Firebase,
#    other externals answered empty, Chromium from /opt/pw-browsers);
#  - kx_hook.js added to every context, logging every KaTeX call to <out.jsonl>;
#  - only the named games in the page list;
#  - the setup-menu click (tier 3 always takes entry 0) redirected to entry <menu_choice>.
import importlib.util, json, os, sys
from playwright._impl import _browser_type as bt, _network as nw, _browser as br, _page as pg

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CODE = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get("AUDIT_KATEX_WORK") or os.path.join(__import__("tempfile").gettempdir(), "audit-katex")
os.makedirs(WORK, exist_ok=True)
KATEX = os.environ.get("AUDIT_KATEX_DIR") or os.path.join(WORK, "package", "dist")
HOOK = open(os.path.join(CODE, "kx_hook.js")).read()
FIREBASE_STUB = ("(function(){var h={get:function(t,k){return k==='then'?undefined:P;},apply:function(){return P;}};"
                 "var P=new Proxy(function(){},h);window.firebase=P;})();")
root, out_path, menu_choice, slugs = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4].split(",")
OUT = open(out_path, "a")

_launch = bt.BrowserType.launch
async def launch(self, *a, **kw):
    kw["executablePath"] = kw.get("executablePath") or "/opt/pw-browsers/chromium"
    return await _launch(self, *a, **kw)
bt.BrowserType.launch = launch

_cont = nw.Route.continue_
async def continue_(self, *a, **kw):
    u = self.request.url
    if u.startswith("https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/"):
        f = os.path.join(KATEX, u.split("/dist/", 1)[1].split("?")[0])
        if os.path.isfile(f):
            return await self.fulfill(path=f)
    if u.startswith("https://www.gstatic.com/firebasejs/"):
        return await self.fulfill(status=200, contentType="application/javascript", body=FIREBASE_STUB)
    if u.startswith("http") and "127.0.0.1" not in u and "localhost" not in u:
        ct = "text/css" if "fonts.googleapis" in u else "application/octet-stream"
        return await self.fulfill(status=200, contentType=ct, body="")
    return await _cont(self, *a, **kw)
nw.Route.continue_ = continue_

_nc = br.Browser.new_context
async def new_context(self, *a, **kw):
    ctx = await _nc(self, *a, **kw)
    def handler(source, rec):
        try:
            rec["url"] = source["page"].url
        except Exception:
            rec["url"] = None
        rec["menu_choice"] = menu_choice
        OUT.write(json.dumps(rec) + "\n")
        OUT.flush()
    await ctx.expose_binding("__kxlog", handler)
    await ctx.add_init_script(HOOK)
    return ctx
br.Browser.new_context = new_context

# Menu redirection: tier 3 clicks a setup screen's entry with exactly this
# expression; answers go through "(i) => window.__mfgClickOpt(i)" and are untouched.
_ev = pg.Page.evaluate
async def evaluate(self, expression, arg=None, *a, **kw):
    if expression == "window.__mfgClickOpt(0)" and menu_choice:
        n = (await _ev(self, "window.__mfgProbe()"))["n"]
        idx = menu_choice if menu_choice < n else n - 1
        await _ev(self, "(m) => { window.__kxMode = m; }", "menu%d/%d" % (idx, n))
        OUT.write(json.dumps({"menu_event": True, "url": self.url, "choice": idx, "n": n}) + "\n")
        return await _ev(self, "window.__mfgClickOpt(%d)" % idx)
    if expression == "window.__mfgClickOpt(0)":
        n = (await _ev(self, "window.__mfgProbe()"))["n"]
        OUT.write(json.dumps({"menu_event": True, "url": self.url, "choice": 0, "n": n}) + "\n")
    return await _ev(self, expression, arg, *a, **kw) if arg is not None else await _ev(self, expression, *a, **kw)
pg.Page.evaluate = evaluate

spec = importlib.util.spec_from_file_location("check_site", os.path.join(root, "scripts", "check-site.py"))
cs = importlib.util.module_from_spec(spec)
sys.argv = ["check-site.py"] + sys.argv[5:]
spec.loader.exec_module(cs)
_bpl = cs.build_page_list
def build_page_list(only=None):
    return [p for p in _bpl(only) if p[0].startswith("game:") and p[0].split(":", 1)[1] in slugs]
cs.build_page_list = build_page_list
os.chdir(root)
cs.main()
