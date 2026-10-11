# split-it fraction scan (report-only, 11 Oct 2026)

Run for SPLIT-IT-KATEX. Nothing here was fixed: every item is outside split-it. Pattern scans, so
a division assigned to a variable and interpolated later is not caught.

## (a) Fractions built with CSS instead of KaTeX (canon 7.1.1)

- `games/fraction-equivalence/index.html:34-38` (`.fractions-row`, `.fraction`, `.frac-num`, `.frac-line`,
  `.frac-den`) and `:153-163` (the two displayed fractions, filled by id `n1/d1/n2/d2`). Loads no KaTeX.
- `games/split-it/index.html` `.frac-wrap` / `.frac-line`: the fractions-mode answer input (two boxes and a
  bar). A control, not a displayed fraction; kept on purpose.

`games/partial-fractions-duel` uses KaTeX `\dfrac`; not a hit.

## (b) Generated text interpolating an unrounded division

Excluding anything wrapped in `toFixed` / `Math.round|floor|ceil` and non-text uses (URLs, CSS):

- `games/test-the-claim/index.html:1791`, `:1792` — `${q.sig / 2}%` (halves, so terminating, no artefact).
- `games/trig-worms/index.html:587` — `${score/10} hits` (one decimal place, terminating).
- `games/boolean-blitz/index.html:801`, `games/trig-wars/index.html:743`, `:749` — layout/colour values,
  not working lines.
- `games/52dle/index.html:891` — share text `n/6`, a score, not a computed quotient.

No hit found that prints a recurring decimal.
