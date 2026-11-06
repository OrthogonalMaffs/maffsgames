# LOGO-CENTRE (Jon, 6 Nov 2026), saved verbatim

LANE: cloud (one session) · TIER: Shared (homepage and about page) · start from current main (a05ed7d or later)

COORDINATION: the home lane has codex/escape-herrings open (escape-room engine). Do not touch escape-rooms/, tools/pack-generator/ or docs/handover/home.md. Record in docs/handover/cloud.md.

TASK: Centre the logo's equals bars on the M's right leg in every copy of the logo, and stop the copies drifting again.

ROOT CAUSE: The right leg runs x 220 to 260 (centre 240); the bars run 215 to 250 (centre 232.5), 7.5 units left. Jon approved the corrected mark (bars at x 222.5, width 35) on 4 Nov.

CLASS CHECK: Yes, a class: the mark is hand-copied five times and the copies have drifted three ways. schools/assets/m_plus_logo.svg, schools/assets/favicon.svg, index.html's header (~line 736) and about/index.html (~line 116) put the bars at 215; index.html and about/index.html also use the old teal #4CB5B0 where the files and canon use #0d9488; schools/assets/og-image.svg has the bars centred but 30 wide, not 35. Fixing one copy leaves four wrong. The fix is one master geometry and a check that every copy matches it. (parents/trigonometry/index.html's x="215" is diagram text, not the logo: leave it.)

EXACT CHANGE:
1. Master: schools/assets/m_plus_logo.svg, bars at x="222.5", width 35. A comment at its top says it is the master and names the check.
2. favicon.svg, index.html's header logo, about/index.html's logo: bars at x="222.5"; bar fill #0d9488. The M and the plus keep their colours in each copy (the header is white on navy on purpose).
3. og-image.svg (its own coordinates, origin at 140,100): bars x="82.5", width 35. Regenerate og-image.png from it the way the repo already does; if there is no generator in the repo, leave the PNG as it is (do not hand-make one) and list it in the PR as a follow-up for Jon.
4. A check (new scripts/check-logo.py with a ci-line header): every copy's M path, plus path and bar rectangles, translated and scaled into the master's coordinates, equal the master's; bars are #0d9488. Self-test with a planted off-centre bar and a planted old teal.
5. /updates/: no line (a 7.5-unit nudge is not a change a teacher would notice).

DO NOT TOUCH: the M and plus shapes, the header layout, page titles, tools/pack-generator (it reads m_plus_logo.svg in place, so it follows automatically), any other SVG, parents/trigonometry/index.html, the files under COORDINATION.

SUCCESS CONDITION: All five copies match the master by the new check, which also catches both plants; the homepage header, about page, browser-tab icon and og-image show the bars centred on the right leg. Committed, PR open, Gate green, entry in docs/handover/cloud.md; stop for Project Claude's review and Jon's "merge".

STOP IF: a sixth copy turns up that isn't SVG or HTML (e.g. an apple-touch-icon PNG) with no generator; changing the teal changes anything other than the bars.
