# fallback.py -> fb.jsonl
# Bank fallback and source literals: for every KaTeX call site, take the strings
# that can reach it (the bank fields the site reads, or its source literal) and
# hand each one to that site's own callee IN THE GAME PAGE -- the game's wrapper
# itself, so the string is rendered exactly as that function renders it. The
# kx_hook logs what KaTeX received and the visual text it produced.
import asyncio, json, os, sys
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CODE = os.path.dirname(os.path.abspath(__file__))
WORK = os.environ.get("AUDIT_KATEX_WORK") or os.path.join(__import__("tempfile").gettempdir(), "audit-katex")
os.makedirs(WORK, exist_ok=True)
KATEX = os.environ.get("AUDIT_KATEX_DIR") or os.path.join(WORK, "package", "dist")
HERE = WORK
sys.path.insert(0, os.path.join(REPO, "scripts"))
sys.path.insert(0, CODE)
import bank_common as bc
import site_eval
from playwright.async_api import async_playwright

ROOT = REPO
HOOK = open(os.path.join(CODE, "kx_hook.js")).read()
SITES = json.load(open(os.path.join(HERE, "sites.json")))
WR = {r["file"]: r for r in json.load(open(os.path.join(HERE, "wrappers.json")))}
OUT = open(os.path.join(HERE, "fb.jsonl"), "w")
SITE_LOG = open(os.path.join(HERE, "fb_sites.jsonl"), "w")
FIREBASE_STUB = ("(function(){var h={get:function(t,k){return k==='then'?undefined:P;},apply:function(){return P;}};"
                 "var P=new Proxy(function(){},h);window.firebase=P;})();")


def bank_questions(slug):
    p = os.path.join(ROOT, "data", "banks", slug + ".json")
    if not os.path.isfile(p):
        return None
    d = json.load(open(p))
    if d.get("generator"):
        return None
    qs = []
    for lv in d["levels"].values():
        for g in lv.get("groups", []):
            qs += g["questions"]
    return qs


def field_strings(qs, fields):
    """Every string under any of `fields`, at any depth, including strings
    inside lists (steps arrays, [expr, law] pairs) under those fields."""
    out = {}
    def strings_in(v):
        if isinstance(v, str):
            yield v
        elif isinstance(v, list):
            for x in v:
                yield from strings_in(x)
    def walk(v, path):
        if isinstance(v, dict):
            for k, val in v.items():
                if k in fields:
                    for s in strings_in(val):
                        out.setdefault(s, k)
                walk(val, path + [k])
        elif isinstance(v, list):
            for x in v:
                walk(x, path)
    for q in qs:
        walk(q, [])
    return out


CALL_JS = r"""async ([callee, strings, argIndex, nparams, opts, replica, tag]) => {
  const scratch = document.createElement('div');
  scratch.style.cssText = 'position:absolute;visibility:hidden;left:-9999px';
  document.body.appendChild(scratch);
  let fn = null, how = 'callee';
  try {
    if (callee === 'katex.render') fn = (s) => katex.render(s, scratch, opts || {throwOnError:false});
    else if (callee === 'katex.renderToString') fn = (s) => katex.renderToString(s, opts || {throwOnError:false});
    else if (callee === 'MaffsText.html') fn = (s) => MaffsText.html(s);
    else {
      const f = eval(callee);
      if (typeof f === 'function') {
        const m = f.toString().match(/^\s*(?:async\s+)?(?:function\s*[\w$]*\s*)?\(?([^)=]*?)\)?\s*(?:=>|\{)/);
        const names = m ? m[1].split(',').map(x => x.trim().replace(/=.*$/, '')) : [];
        fn = (s) => {
          const args = [];
          for (let i = 0; i < Math.max(names.length, argIndex + 1); i++)
            args.push(/^(el|elem|element|node|target|container|div|span|box|parent|host|t?el\w*)$/i.test(names[i] || '') ? scratch : undefined);
          args[argIndex] = s;
          return f.apply(null, args);
        };
      }
    }
  } catch (e) { fn = null; }
  if (!fn && replica) {
    how = 'replica';
    try { replica.opts = (0, eval)('(' + replica.optsText + ')'); } catch (e) { replica.opts = {throwOnError:false}; }
    fn = (s) => replica.kind === 'render' ? katex.render(s, scratch, replica.opts) : katex.renderToString(s, replica.opts);
  }
  if (!fn) return {how: 'unreachable', errors: strings.length};
  let errors = 0;
  for (const s of strings) {
    window.__kxMode = tag + '\u0001' + s;
    try { fn(s); } catch (e) { errors++; }
  }
  window.__kxMode = null;
  scratch.remove();
  return {how, errors};
}"""


def replica_for(wrapper):
    """A depth-1 wrapper whose KaTeX argument is its own parameter, untouched,
    can be reproduced exactly from its call's options if it is not reachable."""
    if not wrapper or wrapper["depth"] != 1 or len(wrapper["calls"]) != 1:
        return None
    c = wrapper["calls"][0]
    if c["arg"].strip() != wrapper["param_name"]:
        return None
    return {"kind": "render" if c["callee"].endswith(".render") else "renderToString", "optsText": c["options"].strip()}


async def main():
    server, base = bc.start_stub_server()
    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(executable_path="/opt/pw-browsers/chromium")
            ctx = await browser.new_context()
            def handler(source, rec):
                OUT.write(json.dumps(rec) + "\n")
            await ctx.expose_binding("__kxlog", handler)
            await ctx.add_init_script(HOOK)
            async def route(r, req=None):
                u = r.request.url
                if u.startswith("https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/"):
                    f = os.path.join(KATEX, u.split("/dist/", 1)[1].split("?")[0])
                    if os.path.isfile(f):
                        return await r.fulfill(path=f)
                if u.startswith("https://www.gstatic.com/firebasejs/"):
                    return await r.fulfill(status=200, content_type="application/javascript", body=FIREBASE_STUB)
                if "127.0.0.1" in u or "localhost" in u:
                    return await r.continue_()
                return await r.fulfill(status=200, body="")
            await ctx.route("**/*", route)
            summary = {}
            for f, sites in SITES.items():
                slug = f.split("/")[1]
                if f.endswith("_withdrawn.html"):
                    url = base + "/games/regression-rumble/_withdrawn.html"
                else:
                    url = base + "/games/" + slug + "/"
                qs = bank_questions(slug) or []
                wr = {w["name"]: w for w in WR[f]["wrappers"]}
                page = await ctx.new_page()
                await page.goto(url, wait_until="load")
                await page.wait_for_timeout(300)
                for s in sites:
                    if s["wrapper_body"]:
                        continue
                    how_src = "field"
                    if s["literal"] is not None:
                        strings = {s["literal"]: "(source literal)"}
                        how_src = "literal"
                    else:
                        text = s["binding"] or s["arg"]
                        try:
                            expr = site_eval.parse_expr(text)
                        except Exception:
                            expr = None
                        if expr is not None and (expr.type == "Identifier" or site_eval._plain_chain(expr)) and not s["binding"]:
                            strings = field_strings(qs, set(s["fields"])) if qs else {}
                        elif expr is None:
                            strings = {}; how_src = "unsupported"
                        else:
                            bare = list(field_strings(qs, set(s["fields"])).keys()) if qs else []
                            try:
                                strings = site_eval.site_strings(expr, qs, bare) if qs else {}
                                how_src = "expression"
                            except site_eval.Unsupported as e:
                                strings = {}; how_src = "unsupported: " + str(e)
                    SITE_LOG.write(json.dumps({"file": f, "line": s["line"], "callee": s["callee"],
                                               "how": how_src, "n": len(strings)}) + "\n")
                    if not strings:
                        continue
                    callee = s["callee"]
                    w = wr.get(callee)
                    nparams = (w["param"] + 1) if w else 1
                    opts = None
                    if callee.startswith("katex.") and s.get("opts"):
                        try:
                            opts = await page.evaluate("(t) => { try { return (0, eval)('(' + t + ')'); } catch (e) { return null; } }", s["opts"])
                        except Exception:
                            opts = None
                    tag = "fallback|%s|%s|%d|%s" % (f, callee, s["line"], ",".join(sorted(set(strings.values()))))
                    try:
                        r = await page.evaluate(CALL_JS, [callee, list(strings), w["param"] if w else 0, nparams,
                                                          opts, replica_for(w), tag])
                    except Exception as e:
                        r = {"how": "error", "error": str(e)[:200]}
                    OUT.write(json.dumps({"site": True, "file": f, "callee": callee, "line": s["line"],
                                          "n": len(strings), "result": r,
                                          "fields": sorted(set(strings.values()))}) + "\n")
                    summary.setdefault(f, []).append((callee, s["line"], len(strings), r.get("how"), r.get("errors")))
                await page.close()
            await browser.close()
    finally:
        server.terminate()
    OUT.close()
    for f, rows in summary.items():
        print(f, rows)


asyncio.run(main())
