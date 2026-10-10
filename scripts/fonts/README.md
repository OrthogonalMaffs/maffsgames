# Pinned web fonts, for the phone-fit checks only

Contract FONT-FIT (Jon, 10 Oct 2026). **No page loads these files.** Every page still asks the CDNs for KaTeX and
its text faces, exactly as before. The phone-fit checks intercept those requests and serve these copies instead
(`bank_common.real_font_response`), so a check measures a page in the fonts a student's phone draws, not the
runner's fallback font, with no network and the same bytes every run.

Regenerate everything here with `python scripts/fonts/fetch-fonts.py`, then re-check `SHA256SUMS` in the diff.

| Folder | What | Source | Licence |
|---|---|---|---|
| `katex/` | KaTeX **0.16.9** (the version every page loads from `cdn.jsdelivr.net`): `dist/katex.min.css`, `katex.min.js`, `contrib/auto-render.min.js`, every `fonts/*.woff2` | the npm registry's tarball, `registry.npmjs.org/katex/-/katex-0.16.9.tgz` | code: MIT (`katex/LICENSE`); fonts: SIL OFL 1.1, as their own name table says (MathJax-derived; `licences/katex-fonts-OFL.txt`) |
| `google/css/` | every Google Fonts stylesheet the site requests (each distinct `css2?…` URL in the repo's `.html`, `.js` and `.css`), as headless Chromium receives it | `fonts.googleapis.com`, fetched with Chromium's user agent | — |
| `google/gstatic/` | every font file those stylesheets name, by its `fonts.gstatic.com` path | `fonts.gstatic.com` | per family, below |
| `google/manifest.json` | each css2 query string → its stylesheet file | | |
| `licences/` | each family's licence text, from Google's fonts repository | `github.com/google/fonts` | |

Google families, as each font file's name table (ID 14) states, with the text in `licences/`:

- **SIL OFL 1.1:** Outfit, JetBrains Mono, Nunito, Press Start 2P, Share Tech Mono, Bebas Neue, Playfair Display,
  Courier Prime.
- **Apache 2.0:** Special Elite.

Both licences allow these files to be copied and redistributed, with their licence text, which is in `licences/`.

**A page that asks for a stylesheet not pinned here** (a new `css2?` query) gets it blocked, as every check did
before, and draws in the fallback font. Re-run `fetch-fonts.py` when a page changes its Google Fonts link.
