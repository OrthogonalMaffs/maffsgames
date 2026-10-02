Status: DONE, merged in PR #2 (one commit `506a6e6`, merge `1a37ad7`) on 28 Sep 2026 and live. Issued by Jon 28 Sep 2026; his rulings on its STOP IF findings are verbatim below the contract. The inventory, the rulings and the verification are in `docs/audit-opendyslexic.md`.

TASK: Make Aa mode actually load the OpenDyslexic font on every game and escape room that offers it, by self-hosting the font once and pointing every reference at that single copy.

ROOT CAUSE: Up to 92 games load OpenDyslexic from cdn.jsdelivr.net/npm/opendyslexic@latest/..., but no npm package by that name exists. jsDelivr returns "Failed to fetch version info for opendyslexic" (confirmed by Jon, 28 Sep 2026). The font has never loaded, so Aa mode has been applying its spacing changes over a fallback sans-serif, site-wide and silently. Nothing checks that a declared font actually arrives.

CLASS CHECK: Yes, this is a bug class: the same broken reference is duplicated across up to 92 files, and each file points at an external dependency rather than a shared asset. The architectural fix is one self-hosted copy of the font plus one shared stylesheet that declares it, so the reference exists in one place and future changes touch one file. Swapping the dead URL for another CDN URL in 92 places is the wrong answer.

EXACT CHANGE:
1. Inventory, before any edit. Find every reference to OpenDyslexic across games/, escape-rooms/, schools/assets/ and the portal/info pages: <link> tags, @font-face blocks, @import lines, and font-family declarations. Group the hits by exact pattern (same URL and same mechanism) and count each group. Record which files have an Aa toggle but no font reference, and vice versa. Write the result to docs/audit-opendyslexic.md.
2. Obtain the font from its official source, the OpenDyslexic GitHub repository (antijingoist/opendyslexic). Take Regular and Bold at minimum, plus Italic if any game uses italic in Aa mode. Use WOFF2 where available, WOFF otherwise. Place them in schools/assets/fonts/opendyslexic/ with the OFL licence file alongside.
3. Create schools/assets/opendyslexic.css containing only the @font-face declarations, pointing at those files with relative URLs.
4. In each file from the inventory, replace the broken jsDelivr reference with a <link> to schools/assets/opendyslexic.css, at the correct relative depth. That line is the only change per file. Leave the font-family declarations and the Aa toggle logic alone.
5. Verify before committing:
   (a) python scripts/check-site.py tiers 1 and 2, compared against the baseline;
   (b) in Chromium, on at least 6 games (3 dark GCSE+ row, 3 light KS3 row) plus 1 escape room: switch Aa on, then confirm the font files return 200 and document.fonts.check('16px OpenDyslexic') is true;
   (c) a diff check proving every changed game file differs from main by exactly one line.
6. One commit.

DO NOT TOUCH: the Aa toggle logic and its localStorage key (mfg_accessible); the font-family stacks and the spacing and sizing rules Aa applies; any other CDN reference (KaTeX, Google Fonts, Firebase); complex-converter's missing toggle (snag 5, separate); any game content or layout. No reformatting or tidying.

SUCCESS CONDITION: docs/audit-opendyslexic.md exists. No reference to cdn.jsdelivr.net/npm/opendyslexic remains anywhere. The font files and OFL licence are in schools/assets/fonts/opendyslexic/. Every file that offered Aa before now links the shared stylesheet. The font returns 200 and document.fonts.check passes on every sampled page. check-site shows 0 new fails against baseline. Each changed game file differs from main by one line. One commit.

STOP IF: the inventory finds more than one loading pattern (report the groups and counts before editing any file); any file declares OpenDyslexic inside inline JavaScript rather than HTML or CSS; the font's licence is not OFL, or the files cannot be obtained from the official repository in this environment; any changed file differs from main by more than the one reference line; font files would push any page over its size limits or add more than 200 KB in total; check-site produces any new fail or warning; tier 1 cannot run in this environment (report, and follow the branch-push-and-CI rule, never push to main).

---

Rulings (Jon, 28 Sep 2026), verbatim:

1. Size: Regular, Bold and Italic, WOFF2, ~320 KB. Accepted.
2. Diff rule: accepted. Per file, the only changes allowed are the two @font-face rules removed (or the one line edited to remove them) and one <link> to schools/assets/opendyslexic.css added. Verify mechanically for all files and report any exception.
3. Escape rooms: drop from the 5(b) sample. Record in the audit doc that rooms use Outfit/Verdana for Aa, not OpenDyslexic. Do not change it.
4. boolean-blitz and truth-will-set-you-free: include, one added <link> each.
Resample 5(b) as 6 games: 3 dark, 3 light, and include one of the two above.
Everything else in the contract stands, including branch plus CI (never main) and the handover steps afterwards.
