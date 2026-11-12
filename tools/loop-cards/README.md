# Printable loop cards

A loop-card pack is an A4 PDF of "I have … / Who has …?" cards made from a game's own question bank, for a whole
class to play on paper (contract LOOP-CARDS, 12 Nov 2026). Two packs exist: **Six Sevens, Bruv** (free) and **Like
Terms Collector** (paid, £3 on Tes). **The PDF is the product: never commit it, upload it or attach it anywhere.**
`dist-packs/` is gitignored, and the build refuses to write anywhere git would track. `tools/` is excluded from the
website (`_config.yml`).

## The loop, in plain words

- Every card has a front ("I have 42") and a back ("Who has 7 × 8?").
- The back of one card asks for the answer on the front of the next card. The last card's back asks for the first
  card's answer, so the questions go round every card once and come back to the start. Nobody is left out.
- Only the person holding the answer turns their card over, so the class has to listen.
- Taking cards out breaks the loop, so smaller classes get their own complete deck: each pack has a 16, a 24 and a 32
  deck. Each deck is its own loop with its own code (SS-16, SS-24, SS-32; LT-16, LT-24, LT-32), printed on every card
  with the card's ID. The IDs are shuffled, so they don't give the order away.
- Six Sevens, Bruv only: the card that asks for 42 says "WHO HAS SIX SEVENS?" (in words), and the card with 42 on it
  says "SHOUT: I'VE GOT SIX SEVENS, BRUV!" under the 42. No other card shouts.

## Build it (Jon, at home)

From the repo root, in the WSL venv (it needs only Playwright and its Chromium, which the repo's checks already use):

```sh
python -X utf8 tools/loop-cards/build_deck.py six-sevens-bruv
python -X utf8 tools/loop-cards/build_deck.py like-terms-collector
```

Each writes `dist-packs/<slug>-loop-cards.pdf` (40 pages) and prints what it checked. The same seed gives the same
decks every time; the seed is in `decks/<slug>/config.json` and in every teacher page's footer. Any failed check prints
`BUILD FAILED` with the reason, and no PDF is written. `--proofs` also writes the PNG proofs to
`docs/screens/loop-cards/`; `--selftest` plants the contract's faults and builds nothing.

To copy a PDF to Windows: `cmd /c 'wsl -d maffs --exec cat /home/maffs/maffsgames/dist-packs/six-sevens-bruv-loop-cards.pdf > "%USERPROFILE%\Downloads\six-sevens-bruv-loop-cards.pdf"'`
(build it in the clone you name).

## Print it

- Page 1 tells the teacher how to run it and which pages to print; pages 2–4 are the answer sheets (one per deck, in
  loop order). Then every deck's double-sided sheets (pages 5–22), then every deck's fold-over pages (23–40).
- **Double-sided, flip on long edge, actual size (100%).** Each deck's sheets are front, back, front, back…, starting
  on an odd page, and each back is mirrored so it lands behind its own front. Print one sheet first and hold it to the
  light: each card's back should sit exactly behind its front.
- Every sheet has the same grid of 8 A7 cards edge to edge, so a stack is cut with 4 guillotine cuts (1 down the
  middle, 3 across). The dashed lines on the fronts are the cuts. All text sits at least 8 mm inside each card, so a
  slightly-off cut or a printer's margin loses nothing.
- **No double-sided printer?** Print the fold-over pages single-sided: each strip is one card, front on the left, back
  on the right. Cut along the dashed lines, fold along the dotted line, glue or tape.
- It is designed for black and white: the shout is white on black, and the web address is 60% grey.

## Approve it

Whether Jon has approved a pack's teacher wording lives in its `decks/<slug>/config.json`, once:
`"wording_approved": {"by": "Jon", "date": "YYYY-MM-DD"}`, or `null`. While it is `null`, every teacher page carries
the "DRAFT: Jon's wording" badge; once approved, the build fails if any page says DRAFT. Copies for Tes are built with
`--final`, which refuses an unapproved pack:

```sh
python -X utf8 tools/loop-cards/build_deck.py like-terms-collector --final
```

The teacher page's wording is Project Claude's draft, verbatim (`STEPS`, `TIPS`, `NEVER_REMOVE`, `PRINTING` in
`build_deck.py`; the Six Sevens line is `TEACHER_EXTRA` in `six_sevens.py`). The build holds it to the contract's
limits: page 1 at most 120 words outside its table (Six Sevens is exactly 120; the title and footer are not counted,
as build_pack.py counts its page 1), no step over 15 words, no text block over 3 lines, the Printing box at most 3
lines. Change it only with Jon's word.

## What the build checks (contract item 10)

It reads what the pages **print**, in Chromium with the network shut (fonts from the repo's pinned copies), and fails
unless, for every deck:

- the deck has 16, 24 or 32 cards as its code says, each card's code is its deck's, and the IDs are 1 to N once each;
- every answer is distinct, every back's question equals exactly one other card's front, and following the backs
  visits every card once and comes back: one loop of full length. Questions and answers are recomputed by the
  adapter's own parser from the printed text, never trusted from the bank (Six Sevens: the product of the printed
  "a × b", and "SIX SEVENS" read as 6 × 7; Like Terms: a coefficient for each letter, compared as maps, never strings,
  and only the true minus U+2212 accepted);
- every back is on the next page at its mirrored place (front row r, column c → back row r, column 2 − c), every
  front sheet has its cut lines drawn full length, and no two loop neighbours sit side by side or have consecutive IDs;
- every text sits inside the 8 mm safe zone; questions, answers and the shout line are at least 20 pt; labels, IDs
  and the web address at least 9 pt (the address exactly 9 pt); nothing overlaps the address or the code;
- every face, both fold-over halves included, carries `maffsgames.co.uk`, and the fold-over cards match the
  double-sided ones word for word;
- Six Sevens: every deck holds 6 × 7, exactly one shout pair (the 42 card and the card asking for it), the shout line
  larger than the 42; no other card, and nothing in Like Terms, shouts or writes a number in words;
- the answer sheets list every card in loop order with the cards' own text, the shout rows marked "(shout)";
- the teacher page's limits above; DRAFT on every teacher page exactly while the wording is unapproved;
- the PDF's page count equals the pages built.

## How it works

`build_deck.py` holds no game's facts. A pack's `decks/<slug>/config.json` names its adapter, title, seed and pack
version. The adapter (`six_sevens.py`, `like_terms.py`) gives:

- `choose(n, rng)`: the deck's questions and answers. Six Sevens: facts a × b, 2 ≤ a ≤ b ≤ 12 without ×10, every
  product distinct, weighted 3 to 1 towards the 6, 7, 8, 9 and 12 tables, 6 × 7 always in. Like Terms: the 30 STAGE3
  items and the first 2 STAGE2 items of `games/like-terms-collector/index.html`, read from the page each build (never
  copied); the 32 deck is all of them, the 16 and 24 decks seeded subsets.
- `value_q()` and `value_a()`: the independent recomputation of a printed question and answer.
- `html()`: the typesetting (Like Terms: KaTeX's fonts, letters italic, true minus).
- `SHOUT` and `TEACHER_EXTRA`: the special cards and the teacher-page line, or none.

Approval, the DRAFT badge, `--final`, the offline browser, `page()` and the gitignore and page-count helpers are
imported from `tools/pack-generator/build_pack.py`, not copied. The footer string follows `build_pack.py`'s
`build_html()`, which builds it inline (there is no public function to import).

A new game needs one adapter and one config; the layout and loop code do not change.
