# KaTeX wrapper audit: scripts

**The production version now lives in `scripts/bank_common.py`, `scripts/extract-banks.py` and `scripts/check-banks.py` (B7's KaTeX half, rebuilt 2 Oct 2026, to-do §1.31); these scripts stay as the reference prototype.**

The scripts behind `docs/audit-katex-wrappers.md` (2 Oct 2026), kept so the audit can be rerun and so
a rebuilt B7 has a working prototype to start from (report §6). **Read-only:** they change no game,
asset or checker file. **Not in CI.** Committing them changed one thing: paths are no longer tied to
the session that wrote them. Rerun from these copies, they reproduce the report's tables byte for byte.

## What each does

| File | Does |
|---|---|
| `find_wrappers.py` | Finds every KaTeX wrapper **by data flow, not name**: a function whose parameter (or a local derived from it) reaches `katex.render`/`renderToString` or `MaffsText.html`, directly or through another wrapper. Also lists every call site and what B7's name match sees today. → `wrappers.json` |
| `site_fields.py` | For each call site: a source literal, or the bank fields that feed it (following locals, `forEach`/`map` callbacks, `for…of`), plus a local's binding expression. → `sites.json` |
| `kx_hook.js` | Init script. Traps the `window.katex` the CDN sets and wraps `render`/`renderToString`, logging each input, `displayMode`, caller stack and visual text through a `__kxlog` binding. |
| `run_t3_capture.py` | Runtime capture. Imports `scripts/check-site.py` and runs **tier 3 unchanged**, with the hook in every context, the sandbox network recipe, only the named games, and tier 3's setup-menu click sent to entry `<menu>` instead of 0. Appends to the given `.jsonl`. |
| `site_eval.py` | Rebuilds, per bank question, the exact string a call site builds (literals, `+`, templates, `\|\|`, `?:`, `.replace`). A site that calls a game function returns nothing (runtime-only). |
| `fallback.py` | Bank fallback. Hands every string that can reach each site to **that site's own callee in the game page** (the wrapper itself), with the hook logging what KaTeX received. → `fb.jsonl`, `fb_sites.jsonl` |
| `analyse.py` | Merges runtime (`rt_m*.jsonl`) and fallback, maps stack frames to wrappers, applies B7's `katex_prose_hazard()` unchanged, names bank fields. → `results.json` |
| `rerender.js` | Node: renders `[string, displayMode]` pairs with the given KaTeX. Used by `spacecount.py`. |
| `spacecount.py` | The second count: a word (B7's definition) that loses, in what the student sees, a space it had in the source. A positive-width `.mspace` counts as a space. Adds it to `results.json`. |
| `gen_tables.py` | The report's data sections. → `tables.md` |

## Where things go

- **Work directory:** all inputs and outputs. `AUDIT_KATEX_WORK`, default `$TMPDIR/audit-katex`. Nothing is written into the repo.
- **KaTeX:** `AUDIT_KATEX_DIR`, default `<work>/package/dist`. Use the version the site loads (0.16.9).
- **Banks:** read from `data/banks/` (gitignored), produced by `scripts/extract-banks.py`.

## Sandbox recipe (a Claude Code cloud sandbox)

Follow `docs/sandbox-checks.md` once per session:

1. `pip install -r requirements-ci.txt` (if `esprima` fails, `SETUPTOOLS_USE_DISTUTILS=stdlib pip install esprima==4.0.1` first).
2. KaTeX, locally: `cd "$AUDIT_KATEX_WORK" && npm pack katex@0.16.9 && tar xzf katex-0.16.9.tgz` (the sandbox refuses the CDN).
3. Extract the banks through that doc's `run_extract_offline.py`. Its summary must read "82 bank (live), 1 bank (static fallback), 13 generator".

Chromium is launched from `/opt/pw-browsers/chromium`; do not run `playwright install`.

## Run order (from the repo root)

```
export AUDIT_KATEX_WORK=/path/to/work AUDIT_KATEX_DIR=$AUDIT_KATEX_WORK/package/dist
python3 scripts/audit-katex/find_wrappers.py
python3 scripts/audit-katex/site_fields.py
# runtime: every KaTeX-calling game at menu entry 0, then the menu games at each other entry
SLUGS=$(python3 -c "import json,os;w=json.load(open(os.environ['AUDIT_KATEX_WORK']+'/wrappers.json'));print(','.join(r['slug'] for r in w if r['file'].endswith('index.html') and (r['direct'] or r['wrappers'])))")
python3 scripts/audit-katex/run_t3_capture.py . "$AUDIT_KATEX_WORK/rt_m0.jsonl" 0 "$SLUGS" --tier 3 --questions 50 --workers 8
python3 scripts/audit-katex/run_t3_capture.py . "$AUDIT_KATEX_WORK/rt_m1.jsonl" 1 complex-converter,factor-theorem,proof-builder --tier 3 --questions 50 --workers 4
python3 scripts/audit-katex/run_t3_capture.py . "$AUDIT_KATEX_WORK/rt_m2.jsonl" 2 complex-converter,factor-theorem,proof-builder --tier 3 --questions 50 --workers 4
python3 scripts/audit-katex/run_t3_capture.py . "$AUDIT_KATEX_WORK/rt_m3.jsonl" 3 factor-theorem --tier 3 --questions 50 --workers 4
python3 scripts/audit-katex/fallback.py
python3 scripts/audit-katex/analyse.py
python3 scripts/audit-katex/spacecount.py
python3 scripts/audit-katex/gen_tables.py
```

The full runtime pass took about 12 minutes with 8 workers. Every other step takes a minute or two.
Which games have a setup menu shows up in `rt_m0.jsonl` as `menu_event` records.

**One input is not here.** test-the-claim cannot be driven by tier 3. In the report, its runtime
column came from a one-off script that called the game's own `checkStep3()` with a wrong value on
every question (report finding 4), saved as `rt_mttc.jsonl`. Without that file the same 15 strings
still appear, labelled bank fallback instead of runtime. Every other figure is unchanged.
