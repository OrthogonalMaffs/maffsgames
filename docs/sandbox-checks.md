# Running the checks in a Claude Code cloud sandbox

Written 1 Oct 2026, after phone-fit batch 1. **CI on GitHub needs none of this**; it is for a cloud
session that has to run the checkers locally before pushing. Every point below cost real time once.

## What goes wrong, and why

| Symptom | Cause |
|---|---|
| `playwright` not importable | Not installed in the sandbox's Python. `pip install playwright` (do **not** run `playwright install`; Chromium is already at `/opt/pw-browsers/chromium`). |
| `Executable doesn't exist at /opt/pw-browsers/chromium_headless_shell-1243/...` | The pip Playwright expects a newer Chromium build than the one installed. Launch with `executable_path="/opt/pw-browsers/chromium"`. `measure-phone-fit.py` takes `--chromium`; `check-site.py` does not, so use the wrapper below. |
| Tier 1 / tier 3 FAIL with `katex is not defined`, `firebase is not defined` or `net::ERR_TUNNEL_CONNECTION_FAILED` | The sandbox's egress policy refuses `cdn.jsdelivr.net` and `www.gstatic.com`. These fail identically on `main`, so they say nothing about a change. |
| `page.goto` times out under a request-routing patch | Playwright's internal `Route.fulfill` takes camelCase (`contentType`, not `content_type`); a TypeError there is swallowed by `check-site.py`'s `except: pass` and the request hangs. |

## The recipe

1. KaTeX, locally (once per session):

   ```
   cd <scratchpad> && npm pack katex@0.16.9 && tar xzf katex-0.16.9.tgz    # gives package/dist/
   ```

2. **Phone-fit report:** `measure-phone-fit.py` has the options it needs. Regenerate it in full (it writes
   the whole report; `--only` would overwrite it with one game):

   ```
   python3 scripts/measure-phone-fit.py --katex-dir <scratchpad>/package/dist --chromium /opt/pw-browsers/chromium --workers 4
   ```

3. **Tiers 1 and 3:** run `check-site.py` unchanged through this wrapper, which makes the network
   deterministic (Chromium from `/opt/pw-browsers`, KaTeX from step 1, an inert Firebase stand-in — the
   checker's own guard blocks every Firebase write anyway — and every other external request, i.e. fonts,
   answered empty). Save it in the scratchpad next to `package/`:

   ```python
   # run_check_site_offline.py <repo root> [check-site args...]
   import runpy, sys, os
   from playwright._impl import _browser_type as bt, _network as nw
   HERE = os.path.dirname(os.path.abspath(__file__))
   KATEX = os.path.join(HERE, "package", "dist")
   FIREBASE_STUB = ("(function(){var h={get:function(t,k){return k==='then'?undefined:P;},apply:function(){return P;}};"
                    "var P=new Proxy(function(){},h);window.firebase=P;})();")
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
   root = sys.argv[1]
   sys.argv = ["check-site.py"] + sys.argv[2:]
   runpy.run_path(os.path.join(root, "scripts", "check-site.py"), run_name="__main__")
   ```

   ```
   python3 run_check_site_offline.py <repo> --tier 3 --only game:<slug>
   ```

4. **Compare like with like.** Make a worktree of `main` in the scratchpad
   (`git worktree add <scratchpad>/main-wt origin/main`) and run the same command against it. A tier 3
   baseline taken any other way in this sandbox is meaningless. Run the two one after the other, not
   at once: tier 3 waits on real timers.

5. **Labels for `--only`:** `game:<slug>`, `room:<slug>`, and the portal is `page:index.html` (a path
   with no slash keeps its whole name). `--only index.html` matches every page.

## Bank extraction in a cloud sandbox

Added 2 Oct 2026 (Contract 2), from the item 7, item 10 and Contract 2 sessions, which all extracted every
bank in a cloud sandbox. **CI needs none of this.**

1. **Python packages.** `pip install -r requirements-ci.txt` (no venv was needed). If `esprima==4.0.1`
   fails to build with `AttributeError: install_layout`, install it first with
   `SETUPTOOLS_USE_DISTUTILS=stdlib pip install esprima==4.0.1`, then re-run the requirements install.
2. **KaTeX, locally:** step 1 of the recipe above (`npm pack katex@0.16.9`, giving `package/dist/`).
3. **Run `extract-banks.py` unchanged through this wrapper**, saved in the scratchpad next to
   `package/`. It launches `/opt/pw-browsers/chromium` and adds a `context.route` that serves the KaTeX
   CDN from the local copy; nothing else is routed, and `extract-banks.py` is not edited:

   ```python
   # run_extract_offline.py <repo root> [extract-banks args...]
   # Runs scripts/extract-banks.py UNCHANGED, with Chromium from /opt/pw-browsers and the
   # KaTeX CDN served from a local copy (the sandbox refuses cdn.jsdelivr.net).
   import runpy, sys, os
   from playwright._impl import _browser_type as bt, _browser as br
   HERE = os.path.dirname(os.path.abspath(__file__))
   KATEX = os.path.join(HERE, "package", "dist")
   _launch = bt.BrowserType.launch
   async def launch(self, *a, **kw):
       kw["executablePath"] = kw.get("executablePath") or "/opt/pw-browsers/chromium"
       return await _launch(self, *a, **kw)
   bt.BrowserType.launch = launch
   async def katex(route, request=None):
       u = route.request.url
       f = os.path.join(KATEX, u.split("/dist/", 1)[1].split("?")[0])
       if os.path.isfile(f):
           return await route.fulfill(path=f)
       return await route.abort()
   _nc = br.Browser.new_context
   async def new_context(self, *a, **kw):
       ctx = await _nc(self, *a, **kw)
       await ctx.route("https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/**", katex)
       return ctx
   br.Browser.new_context = new_context
   root = sys.argv[1]
   os.chdir(root)
   sys.argv = [os.path.join(root, "scripts", "extract-banks.py")] + sys.argv[2:]
   sys.path.insert(0, os.path.join(root, "scripts"))
   runpy.run_path(sys.argv[0], run_name="__main__")
   ```

   ```
   python3 <scratchpad>/run_extract_offline.py <repo> --workers 6
   ```

4. **Never trust a ledger write unless `differentiation-duel`, `index-laws` and `integration-duel` all
   extracted as "live".** The summary must read "82 bank (live), 1 bank (static fallback), 13 generator".
   Without KaTeX those three come back as generators with empty banks. Since PR 53, `--write-ledger`
   refuses (exit 1, nothing written) when that happens, and `--ci` fails with "BANK NOT READ"; check the
   summary anyway.
5. The route handler takes `(route, request)`: a handler written with one parameter raises
   `TypeError … takes 1 positional argument but 2 were given` at the first KaTeX request.

## Measuring every question, not one

`measure-phone-fit.py` samples one random first question per size, so a game near the fold flips
between runs (five untouched games did on 1 Oct). A batch is measured on **every** question instead,
with a short Playwright script per game in the scratchpad. The pattern, used for all of batch 1:

- start the game (`startGame()`), then for each item in the game's own bank set the session to that one
  item and call the game's own render function (`renderQuestion()`, `loadQuestion()` …);
- record the bottom of the lowest answer control (`getBoundingClientRect().bottom + scrollY`) against
  the fold (`innerHeight` minus the 40px `.site-footer`);
- answer wrongly through the game's own function, wait out its feedback, record the bottom of
  `.maffs-next` (or the game's Next), and **press it** before the next item — re-rendering without
  pressing leaves a 20s fallback pending, which fires later and ends the session mid-loop;
- for every wrong option, not just the first, where the screen depends on which was picked;
- before (on the `main` worktree) and after, at 320×568, 375×667 and 390×844.

Then play the game through once to `game_completed` at 320×568, alternating right and wrong, and check
every `question_answered` index arrives once and in order (hook `window.mfg` with
`check-site.py`'s `TIER3_INIT` and `measure-phone-fit.py`'s `CORRECT_INIT`).

## Traps found in batch 1

- **An inline style beats a stylesheet rule.** `better-value`'s `renderQuestion()` sets the options
  row's `display` inline, so hiding it on feedback needed `!important`. Check what the game's JS sets
  before trusting a CSS rule.
- **A game's own Enter handler plus the focused Next control** can advance twice on one key press.
  Route Enter through the handle `MaffsNext.wrong()` returns (`.advance()`), as `formula-plug-in`
  and `new-shapes` do.
- **Games share templates.** `formula-plug-in` is New Shapes' template (same `formula-card`, `numpad`,
  `feedback-panel`); its fix was New Shapes' block nearly unchanged. Look for a sibling before writing
  a layout from scratch.
