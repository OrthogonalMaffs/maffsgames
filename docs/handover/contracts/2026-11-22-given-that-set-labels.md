GIVEN-THAT-SET-LABELS. Cloud lane. Tier: Small (one CSS rule in one game, and a contrast check in its verifier). From Project Claude; Jon, 22 Nov 2026, 17:59 (screenshot: the Venn set names "Cereal" and "Toast" black on the dark diagram), 18:00 ("white on the black would work best please"), and 18:47 ("yes please").
Recommended: Claude Code, Opus, medium effort. A one-line cause; the check makes every diagram label's contrast a CI rule for this game.

TASK: Make Given That's Venn set names readable (the theme's light text colour), and check that every diagram label in every item has enough contrast.

ROOT CAUSE: .venn-set-label (games/given-that/index.html:99) sets font and alignment but no fill, so the SVG set names (vennSVG :1033-1034, data-region setA/setB) take SVG's default black, on the diagram's dark surface (--surface #1a1d27, :26). The set names have been near-invisible on all 14 Venn items, in both phases, since the game was built (the rule is unchanged from before #877). A student can't tell which circle is which.

CLASS CHECK: Local to this game: its own SVG and CSS. The same shape (SVG text with no fill on a dark theme) could exist in other games' drawings. This contract checks every text element in this game's three diagram types, and lists in the PR any other game page whose SVG text has no fill rule (a grep is enough: report, don't fix).

EXACT CHANGE:
1. First commit: the standing close-out for DECIMAL-DETECTIVE-FIT (#882, merged as 29c1749 via merge-pr.py; main runs check-site 45054990712, phone-fit-full 45054990723, Pages 45054990303; the PR's own phone-fit run 45053722874 measured decimal-detective only, normal, Aa and laptop, 1m39s: #878's first live proof, recorded as done). Contract to docs/history/contracts/, decimal-detective off the claim list (scripts/answer-lock-state.json), one line in cloud.md. Still owed: #875's docs-only and /class/ PRs. In the same commit, save this contract verbatim as docs/handover/contracts/2026-11-22-given-that-set-labels.md and claim given-that.
2. .venn-set-label gets fill:var(--text) (#e8eaf0, the theme's white text). The fade (greyed, opacity 0.2), the Total label's own muted fill and everything else are unchanged.
3. Verifier (scripts/verify-given-that.py): for every item, all three diagram types, both drawings (390x844 and 1366x768), normal and Aa, Phase 1 and Phase 2: every text element in the diagram that is not faded has a WCAG contrast ratio of at least 4.5:1 against the diagram's background (the computed fill or colour, and the nearest painted background). Faded elements are exempt (faded by design). Plant: the fill removed (caught on every Venn).
4. PR report: the contrast check's counts, and the list of other game pages with SVG text and no fill rule (report only).
5. /updates/: one dated line, e.g. Given That's Venn diagrams now show the set names clearly.
6. Merge on green via scripts/merge-pr.py; the PR's phone-fit run should measure given-that only (report its ID). Then the standing close-out (cloud.md one line) and unclaim the game.

DO NOT TOUCH: Every item's data; the fade and its rules; the layout, Why card, hints and slip lines; the circles' colours; shared assets; Gate files; other games (report only); data/uses.json, /when-will-i-use-this/, schools/assets/site-nav.js and docs/handover/home.md (the home lane's #883 is open).

SUCCESS CONDITION: On every Venn, "Cereal"/"Toast"-style set names read in the theme's white; the verifier proves every unfaded diagram label meets 4.5:1 in every item, phase, mode and drawing, with the plant caught; CI is green and the PR is merged.

STOP IF: Another diagram text element fails 4.5:1 and the fix isn't a one-line fill or colour in this page (report it). The fix would need a shared asset. Main goes red for a reason outside this change (one rerun per AGENTS.md, then stop and report).

---

STOP (Claude Code, 22 Nov 2026), reported before any edit: measured in the browser, every item, both phases, both drawings, normal and Aa. Besides the set names (black, 1.25:1), the --muted grey #7a7f90 fails at 4.22:1 on #1a1d27: the Venn "Total: N" label (all 14 Venns, Phase 1), the wide tree's branch labels (both phases), and the narrow/Aa tree list's root label and connector glyphs. Each is a one-line colour in this page, but step 2 keeps the Total label's muted fill, so the contract contradicted itself; the colour was Jon's call.

Amendment 1 (Project Claude, with Jon): your STOP is right. Change Given That's --muted token (index.html :27) from #7a7f90 to #8a8fa0 (5.22:1 on --surface), not a diagram-only grey: it fixes the Total label, tree branch labels, the tree list's root and connectors, and the start screen's muted text in one line. The Total label's colour may change (overrides step 2's "unchanged"). The verifier checks every unfaded diagram label AND the start and results screens' text at 4.5:1. Report other games' muted greys as a list only; don't change them. Everything else as written.
