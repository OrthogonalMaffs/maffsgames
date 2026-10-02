Status: **DONE 28 Sep 2026** (PR #7, merged as `7f0d3e5`). Record: `docs/audit-parent-guides.md`, which ends with Jon's rulings. Drafted by Project Claude; issued by Jon 28 Sep 2026, verbatim below. Queued fourth: after the OpenDyslexic fix, Chart Interrogator Contract B and the Spot the Error audit. MathsWins parent guides: read-only audit contract drafted by Project Claude, queued after the OpenDyslexic fix.

TASK: Produce a read-only audit of the 20 MathsWins parent guides (mathswins.co.uk/parents/) to establish what must be fixed before they migrate to MaffsGames.

ROOT CAUSE: The parent guides live on MathsWins, which is being wound down and which also hosts gambling and crypto content that a schools resource should not sit beside. They are the part worth keeping, but a spot-check of one guide (negative-numbers) found: a game link that may not resolve (/games/negative-number-line/); an internal contradiction ("adding always means moving right", then "adding a negative is the same as subtracting"); an FAQ claiming long division replaced older methods; and a "no data collected" claim that does not match MaffsGames' disclosed cookieless analytics. GSC shows only 8 linked MaffsGames targets from 20 guides. Nothing has been checked systematically.

CLASS CHECK: Yes, this is a bug class: all 20 guides share one template (same five sections, same closing "Let them practise" blurb, same index-page FAQ). Any defect in template text is one finding, not 20. The audit must separate TEMPLATE findings (text repeated across guides) from PER-GUIDE findings, so the eventual fix lands once at the template layer. This contract only finds; it fixes nothing.

EXACT CHANGE:
1. Locate the source. Check whether the MathsWins source is available as a repo; if so, read from it. If not, read the live pages at mathswins.co.uk/parents/ and each linked guide. State which source was used.
2. Create docs/audit-parent-guides.md in the maffsgames repo. The only file created or changed.
3. Header: guide count per level (KS3/GCSE); total game links; how many resolve; how many are broken; counts of claims in each verdict below.
4. TEMPLATE section: every sentence that appears verbatim (or near-verbatim) in 3 or more guides, plus the whole index-page FAQ. Give each a verdict: OK / WRONG / CHECK (a pedagogy or factual claim for Jon to rule on).
5. One section per guide:
   (a) URL, title, level;
   (b) every link to maffsgames.co.uk: anchor text, target, whether the slug exists under games/ in this repo, whether it is in .claude/rules/game-roster.md, and whether the game actually serves the level the guide is for;
   (c) every worked example, with its arithmetic recomputed and any MISMATCH flagged;
   (d) every mathematical claim, verdict OK / WRONG / CHECK with a one-line reason;
   (e) every "how schools teach it now" claim, marked CHECK (pedagogy; Jon rules);
   (f) any notation not in LaTeX, i.e. ASCII maths such as x^2 or sqrt;
   (g) any claim about data, privacy, cookies or safety, compared against privacy/index.html;
   (h) internal contradictions within the guide.
6. Redirect map: a table of old MathsWins URL → proposed maffsgames.co.uk/parents/<same-slug>/. A proposal only; nothing is created.

DO NOT TOUCH: any file on either site other than creating docs/audit-parent-guides.md; the MathsWins repo, if present (read only); any MathsWins page outside /parents/ (the academy, tools, everyday and games sections are out of scope). Do not create /parents/ on MaffsGames, set up redirects, edit games, fix any finding, or rewrite any guide text. Make no commit except the audit doc.

SUCCESS CONDITION: docs/audit-parent-guides.md exists with the header counts, the TEMPLATE section, 20 per-guide sections covering (a) to (h), and the redirect map. Every MaffsGames link is marked resolves / broken, every worked example is recomputed, and every claim carries a verdict. One commit containing only that file.

STOP IF: the guide count is not 20; the guides are generated from a data file or template engine rather than hand-written pages (report the structure and audit the source data instead, after confirming with Jon); neither the source repo nor the live site is reachable from this environment (report the network error; do not guess content); a guide links to any external site other than maffsgames.co.uk; any guide carries content that is not a parent maths guide.

---

Context found 28 Sep 2026 (not part of the contract; re-verify before relying on it):

- **Source.** A Claude Code web session cannot reach `mathswins.co.uk`; the egress gateway refuses it (403, "organization policy"). The source is a public repo, `OrthogonalMaffs/MathsWins`, which clones read-only through the session's git proxy. It was last pushed on 5 May 2026, so it may lag the live site.
- **The guides in that repo.** `parents/` holds 21 static HTML pages: an index and 20 topic guides, each titled "… — A Parent's Guide". Whether they were generated was not checked.
- **Links.** 20 of the 21 pages link into `maffsgames.co.uk`: 29 links to 24 distinct games. All 24 slugs, including `negative-number-line`, existed under `games/` on 28 Sep. Five links point at `maffsgames.co.uk/schools`, a redirect page, and show that path as their link text.
- **GCSE tier.** By `data/dfe-gcse-parts.json`, three of the 20 topics are Higher-only (bold): circle theorems (G10), surds (N8, the `indices-surds` guide in part) and graph transformations (A13).
