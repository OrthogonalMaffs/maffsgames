# Help / Instructions Audit (2026-03-24, updated 2026-08-26)

## Games with Substantial Pre-Game Guidance
These have dedicated how-to sections, worked examples, tutorials, or reference tables:

| Game | Slug | What they have |
|------|------|----------------|
| Angle Ace | `angle-ace` | 2-para explanation + full 8-rule geometric reason reference grid |
| Bearing Blitz | `bearing-blitz` | 4-line how-to + tolerance + lives + compass reminder |
| Circle Theorem Spotter | `circle-theorem-spotter` | A labelled SVG diagram on every one of the 55 questions (added 2026-08-26) |
| Characteristic Quest | `characteristic-quest` | Full 4-step worked example (KaTeX) + quick formula |
| Constructions Lab | `constructions-lab` | Tutorial modal (compass, ruler, point, lock radius) + per-task step instructions |
| Decimal Detective | `decimal-detective` | 3 type-preview cards describing each challenge |
| Differentiation Duel | `differentiation-duel` | KaTeX how-to rules list + persistent in-game Quick Reference |
| Dimension Checker | `dimension-checker` | Full SI dimensions reference table + homogeneity explanation |
| Eigenvalue Extractor | `eigenvalue-extractor` | Full worked example (KaTeX, quadratic formula) |
| Eigenvector Engine | `eigenvector-engine` | Full worked example (KaTeX) + key insight box |
| Equatle | `equatle` | "?" button -> full How to Play modal (rules, colours, examples, hard mode) |
| Expectation Station | `expectation-station` | "How it works" section with 3 labelled stages |
| Expected Damage | `expected-damage` | 3 level-preview cards with difficulty descriptions |
| Factor Race | `factor-race` | 4-bullet how-to with worked factor examples |
| Factor Theorem | `factor-theorem` | Full Learn tab: 4 worked examples, step-by-step, "Why?" tooltips, exam vocab |
| Fermi Lab | `fermi-lab` | 5-bullet how-to explaining chain estimation process |
| Formula Forge | `formula-forge` | 4 stage-preview cards + hint system explanation |
| Formula Plug-In | `formula-plug-in` | Live worked example card (formula + values + question) |
| Formula Unlocked | `formula-unlocked` | 4 stage pills + menu-info explaining hints/worked solutions |
| Four Quadrant Explorer | `four-quadrant-explorer` | Confidence framing paragraph + 3 type-preview cards |
| Fraction Snap | `fraction-equivalence` | 4-bullet how-to with cross-multiply check method |
| Graph Transformer | `graph-transformer` | Menu-info: blue=yours/red=target + GCSE vs A-Level differences |
| Index Laws | `index-laws` | KaTeX how-to listing all 6 laws + in-game Quick Reference |
| Integration Duel | `integration-duel` | KaTeX how-to rules list + in-game Quick Reference |
| Like Terms Collector | `like-terms-collector` | Motivational framing + 3 stage-preview cards (Fruit->Letters->Full) |
| Log Laws | `log-laws` | All log laws in KaTeX + in-game Quick Reference |
| Modular Battle | `modular-battle` | 4-bullet how-to with worked example (47 mod 5 = 2) |
| Negative Number Line | `negative-number-line` | 3 type-preview cards (Place It, Order Them, Calculate) |
| New Shapes | `new-shapes` | Motivational framing + 3 section cards with KaTeX formulas |
| Normal Navigator | `normal-navigator` | Calculator requirement + scope + visual intuition note |
| Percentage Flip | `percentage-flip` | 4-bullet how-to explaining flip mechanic |
| Prime Sprint | `prime-factorisation` | 5-bullet how-to with worked example (60 -> 2x2x3x5) |
| Probability Paradox | `probability-paradox` | 3 detailed mode cards with full descriptions |
| Probability Pioneer | `probability-pioneer` | Real-world motivation paragraph + 3 stage-preview cards |
| Proof Builder | `proof-builder` | 3 mode cards with description + mode tags |
| Quadratic Factoriser | `quadratic-factoriser` | KaTeX worked example + "watch out for negatives" |
| Scale Factor Scaling | `scale-factor-scaling` | Menu-info with concrete examples (double -> x4 area, x8 volume) |
| Shape Shifter | `shape-shifter` | 4 selectable mode cards (Translation, Reflection, Rotation, Random Mix) with instructions |
| Spot the Muppet | `spot-the-muppet` | Start screen subtitle explaining the game mechanic |
| SUVAT Selector | `suvat` | All 5 variable definitions + in-game 5-equation reference panel |
| Tax Theft | `tax-theft` | 3 difficulty bands with descriptions + guided step-instructions during play |
| Test the Claim | `test-the-claim` | Menu-info describing 6-step guided hypothesis testing |
| Think of a Number | `think-of-a-number` | Professor Puzzler character card explaining reverse-operations |
| Trig Worms | `trig-worms` | 5-bullet SOH CAH TOA how-to + 3 trig chip quick reference |
| Truth Buster | `truth-buster` | Game mechanic explanation + 3 tier-preview cards |
| Unit Converter | `unit-converter` | Menu-info with concrete misconception example (1 m squared != 100 cm squared) |
| Wrong on the Internet | `wrong-on-the-internet` | "How it works" section with 2 stages + scoring rules |
| 52-dle | `52dle` | "?" button -> How to Play modal + in-game hint system |

## Games with Minimal Guidance (level/content breakdowns, brief subtitles)
Better Value, Binomial Blaster, Chart Interrogator, Complex Converter, Component Crusher, Coordinate Geometry Dash, Core Maths Paper 1 Practice, Core Maths Paper 2A Practice, Core Maths Paper 2B Practice, Core Maths Paper 2C Practice, Correlation or Coincidence, Curling Friction, Equation Builder, Estimation Engine, Estimation Golf, Force Resolver, Glorious Gantt, Gradient Hunter, Graph Sketcher, Growth and Decay, Maths Court, Matrix Crunch, Moments Master, Partial Fractions Duel, Proportion Blaster, Regression Rumble, Sequence Solver, Simultaneous Solver, Split It, Spot the Error, Standard Form Blitz, Stat Attack, Surd Simplifier, Trig Identity Duel, Word Problem Decoder

## Games with NO Help Section
**None.** All three were fixed in August 2026:

| Game | Slug | What it got | When |
|------|------|-------------|------|
| Prime or Composite | `prime-or-composite` | 6/7 mnemonic intro panel filling the empty help slot | 2026-08-26 (`2640d74`) |
| Trig Wars | `trig-wars` | Full Mission Briefing overlay: objective, controls, the Vx/Vy decomposition, how to read the live trig panel, and an explicit "your first shot is not supposed to hit" ranging note. First visit auto-opens; `? BRIEFING` reopens it | 2026-08-26 |
| Terrible Advice | `terrible-advice` | 3-step "How it works" + per-level topic list. Makes the actual skill explicit: you are marking the *method*, and every distractor is a real misconception | 2026-08-26 |

## Notes for the next audit

- **Trig Wars had no start screen at all** — not merely a missing help section. Players landed
  directly on a live battlefield with two unlabelled sliders. Worth checking whether any other
  game boots straight into play.
- **Graph Transformer's entry says "Menu-info"** and that is still true, but the reason for its
  14% accuracy turned out to be a rendering bug, not missing guidance — `buildEquation()` returns
  LaTeX which was being written with `.textContent`, so 23 of its 50 puzzles showed the student
  raw markup like `y = \sqrt{(x-2)}+3`. Fixed 2026-08-26. **A help-section audit would never have
  caught that** — worth spot-checking that games actually *render* what they intend to.
