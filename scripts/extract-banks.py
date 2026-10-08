#!/usr/bin/env python3
"""Checker tier 4, layer A, step 1: pull every game's question bank out of the
live page and write it to data/banks/<slug>.json.

WHY A LIVE PAGE, NOT JUST THE SOURCE FILE
------------------------------------------
A static read of the source sees an object literal as authored. It cannot see
what the page actually ends up holding once init code has run -- and this
project's history is exactly the gap between those two: normal-navigator's
`QUESTIONS[n] = {...}` patches (canon, docs/history/claude-md-archive.md "the lesson of the last
session") land AFTER the literal and change what a student is served, but a
source read of the literal alone would miss them entirely. Reading the bank
back from the page under Playwright, after the game's own script has run,
gets the number a student would actually see.

HOW A GAME'S BANK IS FOUND, GENERICALLY
----------------------------------------
No per-game lookup table. `bank_common.top_level_declarations()` reads the
static AST for every var/let/const declared at Program scope -- the only
bindings `page.evaluate` can reach by name, since a name hidden inside an
IIFE or a function body was never on the page's global lexical scope in the
first place (that absence is itself the finding: see STOP IF below). Every
such name is evaluated on the live page, per level query the game declares in
game-roster.md; whatever comes back is walked by
`bank_common.find_question_groups()`, which does not care whether the shape
is a flat array (normal-navigator), an array keyed by level then topic
(matrix-crunch), or several separate named arrays (factor-theorem's
examples/practice/test) -- it just finds every array whose elements are
majority question-like dicts (carry `correct` or `correct_override`),
wherever it sits.

A game with no such array anywhere, at any level, is recorded as a
generator: PLATFORM-WIDE and PER-QUESTION distractor/scenario computation
(trig-worms, modular-battle, split-it, ...) has nothing here to read
statically, by design -- checker tier 4 layer D (proposed, not built; see
docs/checker-tier4-design.md) is where a generator's own output range gets
checked, not this layer.

OUTPUT
------
data/banks/<slug>.json, one per roster game (94):
    {
      "slug": ..., "generator": bool,
      "read_method": "live" | "unreadable",
      "variables": ["QUESTIONS", ...],           # names that yielded a bank
      "levels": {
        "<level query, or 'default' for a single-level game>": {
          "count": N,
          "groups": [{"variable": "QUESTIONS", "path": ["further","det"],
                       "count": 15, "questions": [...]}]
        }
      }
    }
    plus, for B7's KaTeX half (to-do §1.31): "katex_sites" (how many render
    sites), "katex_wrappers", "katex_renders" (every resolved string as it
    rendered through its site's own callee: path, source, callee, line,
    rendered, katex, error), "katex_unresolved" and "katex_runtime_only"
    (sites listed by check-banks --ci, never a failure); and
    "mathtext_hazards" (B7's MaffsText half).

USAGE
-----
    python scripts/extract-banks.py                  # every roster game
    python scripts/extract-banks.py --only matrix-crunch
    python scripts/extract-banks.py --workers 6

Reuses check-site.py's stub server (serve-stubbed.py), started through
bank_common.start_stub_server() so a server that cannot start is an error and
not a classification, and the roster's level table (bank_common.roster_levels(),
scripts/roster-levels.json), so the same level-query list check-site.py loads
applies here unchanged.
"""
import argparse
import asyncio
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bank_common as bc  # noqa: E402

ROOT = bc.ROOT
BANKS_DIR = bc.BANKS_DIR


import re as _re

# Every real bank across all 94 games is named in SCREAMING_SNAKE_CASE
# (QUESTIONS, BANK, SCENARIOS, YEAR6_BANK, ...) -- checked directly rather
# than assumed. Runtime session state (pool, currentQ, roundQuestions,
# bearings) is always lowerCamelCase, and reading it back can silently
# collide with the real bank: estimation-golf's `roundQuestions` (the
# current 9-hole session, already populated by page load) looked like a
# second, smaller "bank" sitting next to QUESTIONS.ks3 and made every one of
# its holes register as a B3 "duplicate question" against its own source --
# a false positive from comparing a bank to a copy of itself, not a real
# repeat. Restricting candidates to the naming convention this codebase
# actually uses removes the false positive without needing to know that any
# particular game has a `roundQuestions`.
_BANK_NAME_RE = _re.compile(r"^[A-Z][A-Z0-9_]*$")


def candidate_names(tree):
    """[name, ...] for every top-level var/let/const, SCREAMING_CASE-named,
    whose init is an Array or Object literal -- a scalar or function-valued
    top-level const can never hold questions, so there's no point reading it
    back.
    """
    decls = bc.top_level_declarations(tree)
    return [n for n, init, k in decls
            if init.type in ("ArrayExpression", "ObjectExpression") and _BANK_NAME_RE.match(n)]


def iife_candidates(tree):
    """(name, init_node) pairs for the same shape, one level inside a
    top-level self-invoking function -- see bank_common's IIFE fallback.
    """
    decls = bc.iife_scoped_declarations(tree)
    return [(n, init) for n, init, k in decls
            if init.type in ("ArrayExpression", "ObjectExpression") and _BANK_NAME_RE.match(n)]


# B7's KaTeX half (to-do §1.31, 2 Oct 2026): every string a render site can
# receive, rendered in the game's own page through the site's own callee -- the
# game's wrapper, MaffsText.html, or katex.* with the site's options -- so a
# wrapper that splits, gates or rewrites its input is measured as it behaves.
# What a student sees is the visual text: .katex-html (the hidden .katex-mathml
# keeps the source's spaces and would mask the defect), each positive-width
# .mspace read as a space (KaTeX draws operator and relation spacing as empty
# spans), zero-width spaces dropped. Strings the page must compute (a game
# function on bank values, or a value in the state a question puts the game
# in) are computed here first: the item's seed statements run, then its
# expression, both at the page's global scope.
SITE_RENDER_JS = r"""async (spec) => {
  const ELEMENT = /^(el|elem|element|node|target|container|div|span|box|parent|host|slot|cell|card|btn|button|b|t?el\w*)$/i;
  const ELEMENT_ARG = /\b(el|elem|div|span|node|box|slot|cell|card|btn|b|c|li|td|getElementById|querySelector|createElement)\b|\$\(/;
  const visual = (root) => {
    const out = [];
    (function walk(n) {
      if (n.nodeType === 3) { out.push(n.nodeValue); return; }
      if (n.nodeType !== 1) return;
      const c = n.classList;
      if (c && c.contains('katex-mathml')) return;
      if (n.tagName === 'SCRIPT' || n.tagName === 'STYLE') return;
      if (c && c.contains('mspace')) {
        const m = (n.getAttribute('style') || '').match(/(?:margin-right|width):\s*(-?[\d.]+)em/);
        if (m && parseFloat(m[1]) > 0) out.push(' ');
      }
      for (const ch of n.childNodes) walk(ch);
    })(root);
    return out.join('').replace(/\u200b/g, '').replace(/[\s\u00a0\u2000-\u200a\u202f\u205f\u3000]+/g, ' ');
  };
  const holder = document.createElement('div');
  holder.style.cssText = 'position:absolute;visibility:hidden;left:-9999px;top:0';
  document.body.appendChild(holder);
  let fn = null, how = 'callee';
  const evalOpts = (t) => { try { return t ? (0, eval)('(' + t + ')') : null; } catch (e) { return null; } };
  if (spec.callee === 'katex.render' || spec.callee === 'window.katex.render') {
    const o = evalOpts(spec.opts) || {throwOnError: false};
    fn = (s, el) => katex.render(s, el, o);
  } else if (spec.callee === 'katex.renderToString' || spec.callee === 'window.katex.renderToString') {
    const o = evalOpts(spec.opts) || {throwOnError: false};
    fn = (s) => katex.renderToString(s, o);
  } else if (spec.callee === 'MaffsText.html') {
    fn = (s) => MaffsText.html(s);
  } else {
    let f = null;
    try { f = (0, eval)(spec.callee); } catch (e) { f = null; }
    if (typeof f === 'function') {
      const n = Math.max(spec.params.length, spec.args.length, spec.param + 1);
      fn = (s, el, allEls) => {
        const a = [];
        for (let i = 0; i < n; i++) {
          if (i === spec.param) { a.push(s); continue; }
          const sa = spec.args[i];
          if (sa && sa.literal !== null && sa.literal !== undefined) { a.push(sa.literal); continue; }
          const looksEl = ELEMENT.test(spec.params[i] || '') || (sa && ELEMENT_ARG.test(sa.text || ''));
          a.push(looksEl || allEls ? document.createElement('span') : undefined);
        }
        const els = a.filter(x => x instanceof HTMLElement);
        els.forEach(x => el.appendChild(x));
        return f.apply(null, a);
      };
    } else if (spec.replica) {
      how = 'replica';
      const o = evalOpts(spec.replica.opts) || {throwOnError: false};
      fn = spec.replica.kind === 'render' ? (s, el) => katex.render(s, el, o)
         : spec.replica.kind === 'mathtext' ? (s) => MaffsText.html(s)
         : (s) => katex.renderToString(s, o);
    }
  }
  const results = [];
  for (const it of spec.items) {
    let sources;
    try {
      if (it.seed && it.seed.length) (0, eval)(it.seed.join('\n'));
      if (it.js !== undefined) {
        const v = (0, eval)(it.js);
        sources = it.many ? Array.from(v || []) : [v];
      } else {
        sources = [it.source];
      }
    } catch (e) {
      results.push({key: it.key, error: 'evaluating: ' + String(e && e.message || e).slice(0, 200)});
      continue;
    }
    for (const src of sources) {
      // A value the callee receives may be a string or, for a wrapper whose
      // KaTeX input it builds itself (renderValue(el, {n, d})), an object.
      if (src === null || src === undefined || src === '') continue;
      // a page-computed string that read a field the question lacks
      if (it.js !== undefined && typeof src === 'string' && /undefined|\[object Object\]/.test(src)) continue;
      if (!fn) { results.push({key: it.key, source: src, error: 'callee not reachable in the page'}); continue; }
      const outs = [], ins = [];
      const k = katex, rts = k.renderToString, r = k.render;
      k.renderToString = function (s, o) { const h = rts.apply(this, arguments); outs.push(h); ins.push(String(s)); return h; };
      k.render = function (s, el, o) { const x = r.apply(this, arguments); outs.push(el); ins.push(String(s)); return x; };
      const vis = (o) => { if (typeof o === 'string') { const b = document.createElement('div'); b.innerHTML = o; return visual(b); } return visual(o); };
      let rec = null;
      for (const allEls of [false, true]) {
        const el = document.createElement('div');
        holder.appendChild(el);
        outs.length = 0; ins.length = 0;
        try {
          const ret = fn(src, el, allEls);
          if (typeof src !== 'string') {
            // the strings KaTeX received are the sources, each as it rendered
            rec = ins.map((s, i) => ({key: it.key, source: s, rendered: vis(outs[i]), how: how, katex: true}));
            el.remove();
            break;
          }
          let text;
          if (typeof ret === 'string') {
            const box = document.createElement('div');
            box.innerHTML = ret;
            text = visual(box);
          } else if (el.textContent.length) {
            text = visual(el);
          } else if (outs.length) {
            text = outs.map(vis).join('');
          } else {
            text = null;
          }
          rec = {key: it.key, source: src, rendered: text, how: how, katex: outs.length > 0};
          el.remove();
          break;
        } catch (e) {
          el.remove();
          rec = {key: it.key, source: typeof src === 'string' ? src : JSON.stringify(src),
                 error: 'rendering: ' + String(e && e.message || e).slice(0, 200)};
        }
      }
      k.renderToString = rts; k.render = r;
      if (Array.isArray(rec)) results.push(...rec); else results.push(rec);
    }
  }
  holder.remove();
  return results;
}"""


def _replica(wrapper, wrappers, depth=0):
    """A wrapper the page cannot reach by name (given-that's kx and log-laws'
    Solve helpers, inside an IIFE) is reproduced when all it does to the
    string is hand its own parameter, untouched, to one renderer: katex.*
    with that call's options, MaffsText.html, or another wrapper reproduced
    the same way. Ported from the audit's prototype
    (scripts/audit-katex/fallback.py), which did the katex.* case."""
    if not wrapper or len(wrapper["calls"]) != 1 or depth > 5:
        return None
    c = wrapper["calls"][0]
    if c["arg"].strip() != wrapper["param_name"]:
        return None
    if c["callee"].startswith(("katex.", "window.katex.")):
        return {"kind": "render" if c["callee"].endswith(".render") else "renderToString",
                "opts": c["options"].strip()}
    if c["callee"] == "MaffsText.html":
        return {"kind": "mathtext"}
    return _replica(wrappers.get(c["callee"]), wrappers, depth + 1)


def resolve_render_sites(html, bank):
    """(wrappers, [(site, resolution)]) for a game page and its extracted bank."""
    wrappers, sites = bc.katex_render_sites(html)
    if sites is None:
        return {}, []
    return wrappers, [(s, bc.resolve_render_site(s, bank)) for s in sites]


async def katex_render_block(context, base, slug, html, bank, timeout_ms):
    """The bank-file fields for B7's KaTeX half: every wrapper found, every
    resolved string as rendered, and the sites that could not be (unresolved,
    or runtime-only: built by the game as it runs, with no bank behind it).
    A generator game is not rendered: its sites are listed, not linted."""
    wrappers, resolved = resolve_render_sites(html, bank)
    unresolved, runtime_only = [], []
    for s, r in resolved:
        row = {"callee": s["callee"], "line": s["line"], "enclosing": s["enclosing"],
               "reason": r["unresolved"]}
        if r["runtime_only"]:
            runtime_only.append(row)
        elif r["unresolved"]:
            unresolved.append(row)
    renders = []
    if not bank.get("generator"):
        renders, failures = await render_sites(context, base + "/games/" + slug + "/",
                                               wrappers, resolved, timeout_ms)
        unresolved += [dict(f, enclosing=None) for f in failures]
    return {"katex_sites": len(resolved),
            "katex_wrappers": [{"name": w["name"], "line": w["line"], "param": w["param"],
                                "splits": w["splits"], "depth": w["depth"]}
                               for w in wrappers.values()],
            "katex_renders": renders, "katex_unresolved": unresolved,
            "katex_runtime_only": runtime_only}


async def render_sites(context, url, wrappers, resolved, timeout_ms):
    """Render every resolved item through its site's own callee in the page.
    Returns (renders, failures): renders are records for check-banks.py;
    failures name a site whose items could not be rendered at all."""
    renders, failures = [], []
    todo = [(s, r) for s, r in resolved if r["items"] and not r["unresolved"]]
    if not todo:
        return renders, failures
    page = await context.new_page()
    try:
        await page.goto(url, wait_until="load", timeout=timeout_ms)
        await page.wait_for_timeout(300)
        for s, r in todo:
            w = wrappers.get(s["callee"])
            oi = 2 if s["callee"].endswith(".render") else 1
            spec = {"callee": s["callee"], "param": s["param"],
                    "params": (w or {}).get("params") or [],
                    "args": [{"text": a["text"], "literal": a["literal"]} for a in s["args"]],
                    "opts": s["args"][oi]["text"] if s["callee"].startswith(("katex.", "window.katex."))
                            and len(s["args"]) > oi else None,
                    "replica": _replica(w, wrappers),
                    "items": [dict(it, key=k) for k, it in r["items"].items()]}
            try:
                out = await page.evaluate(SITE_RENDER_JS, spec)
            except Exception as e:
                failures.append({"callee": s["callee"], "line": s["line"],
                                 "reason": "page error: %s" % str(e)[:160]})
                continue
            items = r["items"]
            ok = 0
            for rec in out:
                it = items.get(rec.get("key"), {})
                if rec.get("error") and not rec.get("source"):
                    continue
                ok += 1 if not rec.get("error") else 0
                renders.append({"path": it.get("path", "literal"), "source": rec.get("source"),
                                "callee": s["callee"], "enclosing": s["enclosing"],
                                "line": s["line"], "rendered": rec.get("rendered"),
                                "katex": rec.get("katex", False), "error": rec.get("error")})
            if not ok:
                errs = sorted({rec.get("error") for rec in out if rec.get("error")})
                failures.append({"callee": s["callee"], "line": s["line"],
                                 "reason": "nothing rendered" + (": " + errs[0] if errs else "")})
    finally:
        await page.close()
    return renders, failures


async def render_mathtext_throw_check(context, base, slug, segments, timeout_ms):
    """B7's MaffsText half: a \\( ... \\) segment MaffsText.html() will hand
    straight to katex.renderToString(). The runtime renders it with
    throwOnError:false so a bad segment never breaks the page -- it just
    shows KaTeX's own red error span, which a checker running with the same
    lenient setting would never see. Rendering with throwOnError:true here,
    once per unique segment, is deliberately stricter than production so a
    broken segment is caught at commit time, not discovered on screen by a
    student.
    """
    if not segments:
        return {}
    page = await context.new_page()
    try:
        await page.goto(base + "/games/" + slug + "/", wait_until="load", timeout=timeout_ms)
        await page.wait_for_timeout(200)
        segs = sorted(segments)
        results = await page.evaluate(bc.MATHTEXT_THROW_JS, segs)
        if results is None:
            return {}
        return dict(zip(segs, results))
    except Exception:
        return {}
    finally:
        await page.close()


async def read_one(page, name):
    js = (
        "() => { try { const v = " + name + "; "
        "return {ok: true, value: JSON.parse(JSON.stringify(v === undefined ? null : v))}; "
        "} catch (e) { return {ok: false, error: String(e)}; } }"
    )
    try:
        return await page.evaluate(js)
    except Exception as e:
        return {"ok": False, "error": str(e)}


async def extract_game(context, base, slug, levels, timeout_ms):
    html_path = os.path.join(ROOT, "games", slug, "index.html")
    with open(html_path, "r", encoding="utf-8") as fh:
        html = fh.read()
    tree, _src = bc.parse_game_source(html)
    if tree is None:
        return {"slug": slug, "generator": False, "read_method": "parse_error",
                 "variables": [], "levels": {}}
    names = candidate_names(tree)

    queries = levels if levels else [None]
    level_results = {}
    variables_seen = set()
    any_readable = False

    for lv in queries:
        key = lv if lv else "default"
        url = base + "/games/" + slug + "/" + ("?level=" + lv if lv else "")
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="load", timeout=timeout_ms)
            await page.wait_for_timeout(300)
            groups = []
            for name in names:
                res = await read_one(page, name)
                if not res.get("ok"):
                    continue
                found = bc.find_question_groups(res["value"], path=())
                for path, qs, marking in found:
                    groups.append({"variable": name, "path": list(path),
                                    "count": len(qs), "marking": marking,
                                    "questions": qs})
                    variables_seen.add(name)
            if groups:
                any_readable = True
            # A keyed bank (matrix-crunch: QUESTIONS.further.*, QUESTIONS.level4.*)
            # is level-invariant to read -- the whole object is visible at any
            # query -- so if any group's top path segment names THIS level,
            # only those groups are the pool this level actually draws from.
            # Union everything only when nothing in the shape names a level at
            # all, which is the flat-bank case (normal-navigator) this query
            # can't disambiguate further.
            scoped = [g for g in groups if lv and g["path"] and g["path"][0] == lv]
            pool_groups = scoped if scoped else groups
            for g in groups:
                g["in_pool"] = g in pool_groups
            total = sum(g["count"] for g in pool_groups)
            level_results[key] = {
                "count": total,
                "groups": groups,
                "scoped_to_level": bool(scoped),
            }
        except Exception as e:
            level_results[key] = {"count": 0, "groups": [], "error": str(e)}
        finally:
            await page.close()

    if any_readable:
        all_questions = [q for lv in level_results.values() for g in lv["groups"]
                          if g.get("in_pool", True) for q in g["questions"]]

        # B7's MaffsText half (28 Sep): a bank string authored with \( \)
        # (schools/assets/mathtext.js's own convention) is scanned regardless
        # of field name -- \( never occurs by accident, so this needs no
        # per-game field list the way the K()-call check above does. Two
        # failure modes: delimiters that don't balance (MaffsText.html's
        # split silently mis-segments the string, e.g. truncating at a
        # nested \)), and a segment KaTeX can't parse at all.
        mathtext_hazards = []
        mathtext_strings = sorted({s for q in all_questions for s in bc.all_strings(q)
                                    if bc.mathtext_has_delimiters(s)})
        if mathtext_strings:
            balanced, unbalanced = [], []
            for s in mathtext_strings:
                (balanced if bc.mathtext_delimiters_balanced(s) else unbalanced).append(s)
            for s in unbalanced:
                mathtext_hazards.append({"kind": "unbalanced", "original": s})
            seg_owner = {}
            for s in balanced:
                for seg in bc.mathtext_segments(s):
                    seg_owner.setdefault(seg, s)
            if seg_owner:
                errors = await render_mathtext_throw_check(
                    context, base, slug, list(seg_owner), timeout_ms)
                for seg, err in errors.items():
                    if err:
                        mathtext_hazards.append({"kind": "throws", "segment": seg,
                                                   "error": err, "original": seg_owner[seg]})

        out = {"slug": slug, "generator": False, "read_method": "live",
               "variables": sorted(variables_seen), "levels": level_results,
               "mathtext_hazards": mathtext_hazards}
        out.update(await katex_render_block(context, base, slug, html, out, timeout_ms))
        return out

    # Nothing on the page's global scope yielded a bank. Before calling this
    # a generator, try the one other place a real bank can legitimately
    # live: one level inside a top-level module-pattern IIFE, read statically
    # from the AST (given-that's shape). A name found there is invisible to
    # page.evaluate by construction, not because the page failed to load.
    static_groups = {}
    static_ok = False
    for name, init in iife_candidates(tree):
        value = bc.static_bank_value(name, init, tree)
        if value is None:
            continue
        for path, qs, marking in bc.find_question_groups(value, path=()):
            static_groups.setdefault(name, []).append(
                {"variable": name, "path": list(path), "count": len(qs),
                 "marking": marking, "in_pool": True, "questions": qs})
            static_ok = True
            variables_seen.add(name)

    if not static_ok:
        out = {"slug": slug, "generator": True, "read_method": "unreadable",
               "variables": [], "levels": {}}
        out.update(await katex_render_block(context, base, slug, html, out, timeout_ms))
        return out

    all_groups = [g for gs in static_groups.values() for g in gs]
    queries = levels if levels else [None]
    level_results = {}
    for lv in queries:
        key = lv if lv else "default"
        scoped = [g for g in all_groups if lv and g["path"] and g["path"][0] == lv]
        pool = scoped if scoped else all_groups
        level_results[key] = {"count": sum(g["count"] for g in pool),
                                "groups": all_groups, "scoped_to_level": bool(scoped)}
    out = {"slug": slug, "generator": False, "read_method": "static_fallback",
           "variables": sorted(variables_seen), "levels": level_results}
    out.update(await katex_render_block(context, base, slug, html, out, timeout_ms))
    return out


DEFAULT_PORT = 0  # 0 = a free port chosen per run


async def run(only, workers, timeout_ms, port=DEFAULT_PORT):
    from playwright.async_api import async_playwright

    levels_by_slug, order = bc.roster_levels()
    slugs = [s for s in order if not only or only in s]

    # Raises bc.StubServerError, naming the cause, if the server cannot start.
    # Without this a dead server made every page load fail, and every game was
    # then reported as a "true generator".
    server, base = bc.start_stub_server(port)

    os.makedirs(BANKS_DIR, exist_ok=True)
    results = []
    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            sem = asyncio.Semaphore(workers)
            contexts = [await browser.new_context() for _ in range(workers)]
            pool = asyncio.Queue()
            for ctx in contexts:
                pool.put_nowait(ctx)

            async def one(slug):
                async with sem:
                    ctx = await pool.get()
                    try:
                        r = await extract_game(ctx, base, slug, levels_by_slug.get(slug, []),
                                                timeout_ms)
                    finally:
                        pool.put_nowait(ctx)
                    return r

            done = 0
            for coro in asyncio.as_completed([one(s) for s in slugs]):
                r = await coro
                results.append(r)
                done += 1
                tag = ("generator" if r["generator"]
                       else "bank (static)" if r["read_method"] == "static_fallback"
                       else "bank")
                print("  [%3d/%3d] %-30s %s" % (done, len(slugs), r["slug"], tag))
            await browser.close()
    finally:
        server.terminate()

    for r in results:
        path = os.path.join(BANKS_DIR, r["slug"] + ".json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(r, fh, indent=1, ensure_ascii=False)

    return results


def main():
    ap = argparse.ArgumentParser(description="Extract every game's question bank to data/banks/.")
    ap.add_argument("--only", help="substring filter on slug")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=20000)
    ap.add_argument("--port", type=int, default=DEFAULT_PORT,
                    help="port for the local stub server (default: a free one)")
    args = ap.parse_args()

    t0 = time.time()
    try:
        results = asyncio.run(run(args.only, args.workers, args.timeout, args.port))
    except bc.StubServerError as exc:
        print("ERROR: the local stub server could not be started, so NO bank was read.")
        print("       " + str(exc))
        print("       Nothing was classified. This is not a generator result, and the")
        print("       data/banks/ files were not touched.")
        return 2

    banks = [r for r in results if not r["generator"] and r["read_method"] == "live"]
    static_fb = [r for r in results if r["read_method"] == "static_fallback"]
    unreadable = [r for r in results if r["read_method"] == "unreadable"]
    parse_err = [r for r in results if r["read_method"] == "parse_error"]

    # Of the banks, how many games have EVERY question in an "ungraded" or
    # "unrecognised" group -- a real static bank Layer A's B1/B2/B5 have
    # nothing to check in, because no unit in it carries a recognised answer
    # key. Worth surfacing distinctly; it is not a failure of either game.
    no_recognised = []
    for r in banks + static_fb:
        markings = {g["marking"] for lv in r["levels"].values() for g in lv["groups"]}
        if markings and "recognised" not in markings:
            no_recognised.append(r)

    print("\n%d games: %d bank (live), %d bank (static fallback), %d generator, %d parse error"
          % (len(results), len(banks), len(static_fb), len(unreadable), len(parse_err)))
    if no_recognised:
        print("BANK WITH NO RECOGNISED ANSWER KEY (correctness is computed, not stored -- "
              "B1/B2/B5 find nothing to check; B3/B4/B6/B7/B8/B9/B10 still run):")
        for r in no_recognised:
            print("  %s  (%s)" % (r["slug"], ", ".join(r["variables"])))
    if static_fb:
        print("STATIC FALLBACK (IIFE-scoped, read from AST not the live page):")
        for r in static_fb:
            print("  " + r["slug"])
    if unreadable:
        print("TRUE GENERATOR (no static question array found anywhere in the source):")
        for r in unreadable:
            print("  " + r["slug"])
    if parse_err:
        print("PARSE ERROR (esprima could not read the source at all):")
        for r in parse_err:
            print("  " + r["slug"])
    # True generators (no static array anywhere) are the EXPECTED outcome for
    # a procedural game, not a failure -- "record generator and skip" is the
    # spec, so they never count toward this. A parse error is the only thing
    # here that means the extraction design itself needs a look.
    if len(parse_err) > 10:
        print("\nSTOP: more than 10 games' source could not be parsed at all -- "
              "the extraction design needs revisiting before trusting this run.")
        return 1
    print("(%.1fs)" % (time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
