# MM-OVERFLOW-DIAG: why Moments Master scrolled sideways once on main

Contract MM-OVERFLOW-DIAG (Jon, 15 Oct 2026). Report only: no game, verifier, `theme.css`, CI file or KaTeX source was changed.
All measurements were taken on 15 Oct 2026 with Playwright Chromium 153 at 320 px (the contract's `is_mobile` + touch context), against
`origin/main` at 0c9bc71.

## Short answer

**Neither a test race nor a slow-load overflow. It is a partial CDN failure: `katex.min.css` fails to arrive while `katex.min.js` does.**
The page then renders every `\sqrt` as an unconstrained SVG about 5,770 px wide, and the page scrolls sideways. The verifier measured it
faithfully; the failure is real page behaviour, triggered by the verifier's dependence on the live CDN.

- Reproduced: blocking only `katex.min.css` (JS normal) gives `scrollWidth` **5897 px** at 320 px; main's failure was **5901 px**. The
  real verifier logic with the stylesheet aborted prints the same line as CI:
  `FAIL  alevel[6] at 320px: the page scrolls sideways (5897px; moments-master-t5-013)`.
- NOT reproduced by delay: KaTeX delayed 3 s (CSS and JS, either, or both) measures **320 px**, identical to normal. The stylesheet is in
  `<head>`, so the browser holds rendering and the `load` event until it arrives; there is no pre-render state to measure.
- NOT raw LaTeX: nothing in the page shows raw TeX before KaTeX arrives. With KaTeX's JS late or absent the game does not draw raw TeX, it
  throws (see 2 and 4).
- Why `alevel[6]` only: it is the **only item in the whole Moments Master bank that uses `\sqrt`** (`10\sqrt{3} \approx 17.3 \text{ Nm}`; the
  40 N at 60° on 0.5 m item). `\sqrt` is the construct that draws an `<svg>` whose size KaTeX's stylesheet normally pins.
- Why 320 px only in CI: the log shows the 390 px pass was clean and the 320 px pass failed, in the main (non-selftest) run. Each viewport
  opens a fresh browser context and fetches KaTeX again, and the selftest plants add more loads, so one failed stylesheet request among
  those loads fits what was seen.

**What is inferred, not proved:** that the CI request for `katex.min.css` failed. The log has no network trace, and the job's one rerun
passed. The width match (5901 vs 5897; it varies with which option is shuffled in), the single viewport and the single bank item all point
at it, and no other state I could construct produces the failure.

## 1. Reproduction (Moments Master `alevel[6]` / `moments-master-t5-013`, 320 px)

Method: Playwright context as the verifier builds it (320×568, touch, mobile), the verifier's own routes (everything but the stub server
and KaTeX aborted), the page served from the repo, `startGame()` then the item shown with `showQ()` as `SWEEP_JS` does. KaTeX requests
(`cdn.jsdelivr.net/npm/katex@0.16.9/...`) routed per row. Script in the appendix.

| KaTeX condition | load event | `katex` defined | KaTeX CSS applied | page `scrollWidth` | widest element |
|---|---|---|---|---|---|
| normal (live CDN) | 0.2 s | yes | yes | **320** | `path` 5769 px, clipped by KaTeX's own CSS |
| all KaTeX delayed 3 s | 6.2 s | yes | yes | **320** | same, clipped |
| CSS only delayed 3 s | 3.2 s | yes | yes | **320** | same, clipped |
| JS only delayed 3 s | 3.2 s | yes | yes | **320** | same, clipped |
| **CSS blocked, JS normal** | 0.2 s | yes | **no** | **5897** | `button.opt-btn` 5796 px, text `20 Nm20 \text{ Nm}20 Nm`; inside it the `svg` `path` 5769 px and `span.katex-html` 5764 px |
| JS blocked (CSS normal) | 0.1 s | no | yes | n/a: verifier's `wait_for_function` times out (15 s), a different failure | n/a |
| all KaTeX blocked | 0.1 s | no | no | n/a: same timeout | n/a |

Two details worth knowing. The 5769 px SVG exists even when everything is fine; it is `width="400em"` in KaTeX's markup and only KaTeX's
stylesheet (`.katex svg{position:absolute;width:100%…}`, `.hide-tail{overflow:hidden}`) keeps it from taking layout. And the CSS-blocked
page also shows every formula three times (the `.katex-mathml` copy is no longer visually hidden), visible in the button text above.

**Verifier-level proof.** A throwaway copy of `verify-moments-master.py` with one extra route aborting `katex.min.css`, run with
`--no-selftest`: `alevel[6] at 390px ... (5897px; moments-master-t5-013)` and the same at 320 px, FAILED. (390 px fails too here because the
abort is in every context; in CI only 320 px did, consistent with one failed request.) The unmodified verifier on the live CDN passes.
The throwaway copy was deleted; `git status` is clean.

## 2. Does the verifier wait for KaTeX, and on what?

`scripts/verify-moments-master.py` (`play()`):

1. `page.goto(..., wait_until='load')`, which waits for the stylesheet and for the `defer` script to run.
2. `page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=15000)`.

So it waits for **KaTeX's JavaScript**. It never checks that **KaTeX's stylesheet applied**. A stylesheet that *errored* does not hold up
`load` (an error counts as finished), so `load` fires, `katex` is defined, the gate passes, and the sweep measures an unstyled page. The
sweep itself (`SWEEP_JS`) is synchronous, so it never races KaTeX rendering; the only gap is the stylesheet.

It also sends KaTeX to the **live CDN**: its route lets any URL containing `/katex@` through, and `--katex-dir` is not passed in CI. Pinned
copies already exist (`scripts/fonts/katex/`, served by `bc.real_font_response`), and `measure-phone-fit.py` and `check-site.py` use
them, which is why those cannot flake this way.

## 3. Survey

### 3a. Games, at 320 px, first question

Every roster game whose page loads KaTeX: **66 of 66 under `games/`** (all link `katex.min.css` from the CDN; 42 load the JS `defer`, 24
without). Each was loaded fresh at 320×568 through `measure-phone-fit.py`'s own driver (a throwaway patched copy, deleted), taken to the
first question, in three conditions. 66 games per condition, 114 s each. The 7 "unreached" in the normal column are games that driver can't
play at all (not KaTeX-related).

| Condition | Page scrolls sideways | Game not reached |
|---|---|---|
| normal (pinned KaTeX, as phone-fit runs) | 1 (`distinctly-average` 334 px; unrelated to KaTeX, see 5) | 7 |
| **KaTeX CSS blocked, JS normal** | **5** | 7 |
| **all KaTeX blocked** | 1 (same) | **22** (15 more than normal) |

Games that differ from normal:

| Game | normal | CSS blocked | all blocked |
|---|---|---|---|
| `surd-simplifier` | fits | **sideways 14178 px** | not reached |
| `force-resolver` | fits | **sideways 6039 px** | not reached |
| `index-laws` | fits | **sideways 4481 px** | not reached |
| `characteristic-quest` | fits | **sideways 335 px** (the triple-printed MathML) | fits |
| `distinctly-average` | sideways 334 px | sideways 334 px | sideways 334 px |
| `binomial-blaster`, `boolean-blitz`, `complex-converter`, `differentiation-duel`, `factor-theorem`, `log-laws`, `matrix-crunch`, `moments-master`, `partial-fractions-duel`, `proportion-blaster`, `standard-form-blitz`, `trig-identity-duel` | fits | fits | **not reached** (`katex is not defined` on the first question) |

**This is a floor, not a count.** One question per game is one sample. `moments-master` shows as "fits" under CSS-blocked because its first
question has no `\sqrt`, yet `alevel[6]` is 5897 px. A static count is the better measure of exposure: **28 of the 66 KaTeX games contain
TeX that draws an SVG** (`\sqrt`, `\overline`, `\vec`, `\widehat`, `\cancel`, `\xrightarrow`, braces) in their page source: binomial-blaster,
boolean-blitz, circle-theorem-spotter, complex-converter, curling-friction, differentiation-duel, eigenvalue-extractor, estimation-engine,
force-resolver, formula-forge, formula-unlocked, graph-transformer, higher-power, index-laws, integration-duel, just-pythag-it-bruv,
log-laws, moments-master, proof-builder, proportion-blaster, quadratic-factoriser, simultaneous-solver, standard-form-blitz, stat-attack,
surd-simplifier, test-the-claim, trig-identity-duel, truth-will-set-you-free. Every one is exposed to a width blow-up whenever its question
reaches that construct without KaTeX's stylesheet.

### 3b. Verifiers and scripts that measure layout

21 scripts read `scrollWidth` (15 `verify-*.py`, 6 others). Classified by reading each for how it reaches KaTeX (grep of the route
patterns, then read; "waits" means a gate on KaTeX being ready):

| Script | KaTeX source | Waits for KaTeX JS | Waits for KaTeX CSS |
|---|---|---|---|
| `verify-moments-master.py` | **live CDN** (`--katex-dir` optional, off in CI) | yes (`typeof katex`) | **no** |
| `verify-force-resolver.py` | **live CDN** | yes | **no** |
| `verify-factor-theorem.py` | **live CDN** | yes | **no** |
| `verify-linear-equation-solver.py` | **live CDN** | yes | **no** |
| `verify-eigenvector-engine.py` | **live CDN** | yes | **no** |
| `verify-proof-builder.py` | **live CDN** | yes | **no** |
| `verify-truth-will-set-you-free.py` | **live CDN** | yes | **no** |
| `check-site.py`, `measure-phone-fit.py`, `test-real-fonts.py` | pinned copy (`bc.real_font_response`) | n/a (no network) | n/a |
| `verify-estimation-engine.py`, `verify-simultaneous-solver.py`, `verify-free-daily-pizza.py`, `verify-correlation-or-coincidence.py`, `verify-just-pythag-it-bruv.py`, `verify-unit-converter.py` | pinned copy referenced (`--katex-dir` on two) | partly | no |
| `check-keypad.py`, `test-calculator-js.py`, `test-escape-rating.py`, `verify-probability-paradox.py`, `verify-screening-room.py` | no KaTeX use found | n/a | n/a |

The seven "live CDN" verifiers are the class. Treat the classification of the pinned and no-KaTeX rows as grep-level, not line-by-line.
`force-resolver` is in both lists (live-CDN verifier, and a page that overflows at 6039 px without the stylesheet), so it is the most
likely to flake next; `moments-master` is the only one seen failing.

## 4. Conclusion

**Test fragility *and* a real page fault, but not the two the contract guessed.**

- *Test race:* refuted for the render. The sweep is synchronous and runs only after `katex` exists; delaying KaTeX never produces the
  failure. The test's real weakness is that it depends on the live CDN and gates on the JS alone.
- *Real overflow on slow load:* refuted. A slow stylesheet delays the whole page (nothing draws, so nothing overflows); a slow script
  leaves no raw TeX.
- *What is real:* a stylesheet that **fails** (not slow) while the script loads gives a student the same 5.9k-px page. That is a rare event
  for a student but a real one, and 28 games carry the exposure.
- *A second, different real fault found on the way:* if KaTeX's script is late and a student presses Start first, `startGame()` throws
  `katex is not defined` and the game is dead (no question, no options) **even after KaTeX arrives** (verified: Start clicked 0 s after
  navigation with the script delayed 3 s; still 0 options at 4.5 s later). The same happens if the script never arrives. 15 of the 66
  games cannot reach a question at all with KaTeX's script absent. This is not a layout fault and no CSS fixes it.

## 5. Proposed fixes (not applied)

### Test layer: stop the verifiers depending on the live CDN, and fail clearly when it does

1. **Serve the pinned KaTeX in the seven live-CDN verifiers**, as `measure-phone-fit.py` does (`bc.real_font_response`). A verifier that
   never touches the network for KaTeX cannot flake on it. Covers `moments-master`, `force-resolver`, `factor-theorem`,
   `linear-equation-solver`, `eigenvector-engine`, `proof-builder`, `truth-will-set-you-free`. This is the real fix for the flake.
2. **A shared readiness helper in `bank_common.py`** for any verifier that measures layout after KaTeX: wait for the script (as now) *and*
   assert the stylesheet applied (a probe `.katex > .katex-mathml` computes `position: absolute`), failing with "KaTeX stylesheet did not
   load" instead of a 5.9k-px overflow. Cheap, and turns a misleading failure into an accurate one even if a verifier is later left on the CDN.

### Page layer: a rule so unstyled maths cannot widen the page

`schools/assets/theme.css` is **the wrong place**: only **5 of 66** KaTeX games load it, and it has no KaTeX rule today. The assets that
all 66 load are `site-footer.css`, `opendyslexic.css`, `level.js`, `analytics.js`; a stylesheet rule belongs in **`site-footer.css`** (66/66)
or in a new `katex-fallback.css` linked by every page.

A candidate, tested here by injecting it into the CSS-blocked pages (these repeat KaTeX's own rules, so they change nothing when the real
stylesheet loads):

```css
.katex svg{display:block;position:absolute;width:100%;height:inherit}
.katex .hide-tail,.katex .svg-align{position:relative;overflow:hidden}
.katex-mathml{position:absolute;clip:rect(1px,1px,1px,1px);width:1px;height:1px;overflow:hidden;padding:0;border:0}
```

| Page, CSS blocked, 320 px | without rule | with rule |
|---|---|---|
| Moments Master `alevel[6]` | 5897 | **320** |
| `surd-simplifier` | 14178 | **320** |
| `force-resolver` | 6039 | **320** |
| `index-laws` | 4481 | **320** |
| `characteristic-quest` | 335 | **320** |
| `distinctly-average` | 334 | 334 (not a KaTeX fault: 334 px with KaTeX normal) |

(Only the SVG rules fix the width; `.katex{max-width:100%;overflow:hidden}` alone did nothing, since the button sizes from the SVG. The
MathML rule removes the triple-printed formula and the last 15 px at `characteristic-quest`.) It would cover **all 66 KaTeX games**,
including the 28 with SVG-drawing TeX. It would not cover the dead game on an early Start (4), which needs the games to wait for KaTeX
before starting (a shared guard in the pages' start path, a larger change and Jon's call), nor `distinctly-average` (its own layout bug).

### Which layer first

The test-layer change 1 removes the flake that CI saw. The page rule is worth doing independently, because it is the only thing that
protects a student; it is cheap and inert when KaTeX loads. Neither needs a `theme.css` change.

## Not done / limits

- One viewport (320 px), the first question of each game, one shuffle; all-KaTeX-blocked reaches fewer games by design.
- Survey conditions were induced by routing, not a real flaky network, so the exact trigger of main's failure stays inferred.
- The "pinned / no KaTeX" rows in 3b were classified by grep and a read of the routes, not run.
- `distinctly-average`'s 334 px at 320 is a separate pre-existing finding, left for Jon.

## Appendix: the reproduction script

```python
import sys, os, re, time, json, importlib.util
REPO = r'<worktree>'; sys.path.insert(0, os.path.join(REPO, 'scripts'))
import bank_common as bc
spec = importlib.util.spec_from_file_location('vmm', os.path.join(REPO, 'scripts', 'verify-moments-master.py'))
vmm = importlib.util.module_from_spec(spec); spec.loader.exec_module(vmm)
from playwright.sync_api import sync_playwright
html = open(vmm.GAME, encoding='utf-8').read()
MODE = sys.argv[1]   # normal | delay3 | delay3-css | delay3-js | blocked | css-blocked | js-blocked
STEP = "([lvl, idx]) => { level=lvl; startGame(); const it=QUESTIONS[lvl][idx]; questions=[it]; qIdx=0; showQ(); return document.documentElement.scrollWidth; }"
proc, base = bc.start_stub_server()
with sync_playwright() as pw:
    br = pw.chromium.launch()
    ctx = br.new_context(viewport={'width': 320, 'height': 568}, has_touch=True, is_mobile=True)
    ctx.route(lambda u: not u.startswith(base) and '/katex@' not in u, lambda r: r.abort())
    def kat(route):
        u = route.request.url; css = u.endswith('.css'); js = u.endswith('.js')
        if MODE == 'blocked' or (MODE == 'css-blocked' and css) or (MODE == 'js-blocked' and js): return route.abort()
        if MODE == 'delay3' or (MODE == 'delay3-css' and css) or (MODE == 'delay3-js' and js): time.sleep(3)
        route.continue_()
    ctx.route(lambda u: '/katex@' in u, kat)
    pu = re.compile(r'/games/%s/(\?[^/]*)?$' % vmm.SLUG)
    ctx.route(lambda u: bool(pu.search(u)), lambda r: r.fulfill(status=200, content_type='text/html; charset=utf-8', body=html))
    ctx.add_init_script(bc.NO_NEXT_FLOOR_INIT); ctx.add_init_script(bc.NO_LOCK_FRESH_INIT)
    page = ctx.new_page()
    page.goto(base + '/games/moments-master/?cb=verify', wait_until='load', timeout=30000)
    page.wait_for_function('typeof QUESTIONS !== "undefined" && typeof katex !== "undefined"', timeout=6000)
    print(MODE, page.evaluate(STEP, ['alevel', 6]))
    br.close()
proc.terminate()
```

The survey drove `measure-phone-fit.py`'s `measure_one` at 320×568 for each KaTeX game, with `route()` patched to abort `/katex@` requests
(CSS only, or all) and, for the fix test, an init script appending the candidate rule on `DOMContentLoaded`.
