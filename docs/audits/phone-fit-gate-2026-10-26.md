# Phone-fit gate: games flagged on its first run (26 Oct 2026)

Contract LOOK-REDS-2, Jon's ruling of 26 Oct 2026. `scripts/measure-phone-fit.py` now fails a game whose answer options **start** below the fold
(the top of the highest answer control) at 320x568, 375x667 or 390x844, in normal or Aa mode. Its first full runs, on branch
`claude/theme-distinctly-average` at 9d7e0c5 (fonts pinned, default level, first question, seeded), flagged the games below. **Not fixed here**
(the contract's STOP IF); Jon to rule how the gate treats them. Distinctly Average passes both runs on its committed state (it was flagged only while
the median card was being moved, and that move is reverted). Every game below was already a report FAIL ("controls below fold") before the gate.

Each cell: `top of the options / fold`, in CSS px from the top of the page.

## Normal mode: 20 games

| Game | Where the options start |
|---|---|
| `truth-will-set-you-free` | 320x568 (972 / 528), 375x667 (923 / 627), 390x844 (874 / 804) |
| `52dle` | 320x568 (882 / 528), 375x667 (863 / 627), 390x844 (844 / 804) |
| `tax-theft` | 320x568 (868 / 528), 375x667 (868 / 627), 390x844 (821 / 804) |
| `differentiation-duel` | 320x568 (809 / 528), 375x667 (809 / 627), 390x844 (809 / 804) |
| `better-value` | 320x568 (772 / 528), 375x667 (716 / 627) |
| `index-laws` | 320x568 (729 / 528), 375x667 (729 / 627) |
| `suvat` | 320x568 (727 / 528), 375x667 (677 / 627) |
| `log-laws` | 320x568 (711 / 528), 375x667 (709 / 627) |
| `think-of-a-number` | 320x568 (707 / 528), 375x667 (651 / 627) |
| `integration-duel` | 320x568 (703 / 528), 375x667 (703 / 627) |
| `wrong-on-the-internet` | 320x568 (677 / 528) |
| `word-problem-decoder` | 320x568 (648 / 528) |
| `constructions-lab` | 320x568 (612 / 528) |
| `decimal-detective` | 320x568 (609 / 528) |
| `percentage-flip` | 320x568 (604 / 528) |
| `complex-converter` | 320x568 (581 / 528), 375x667 (636 / 627) |
| `higher-power` | 320x568 (578 / 528) |
| `trig-worms` | 320x568 (563 / 528) |
| `quadratic-factoriser` | 320x568 (546 / 528) |
| `given-that` | 320x568 (541 / 528) |

## Aa (OpenDyslexic) mode: 35 games

| Game | Where the options start |
|---|---|
| `truth-will-set-you-free` | 320x568 (1314 / 528), 375x667 (1141 / 627), 390x844 (1141 / 804) |
| `52dle` | 320x568 (1183 / 528), 375x667 (1089 / 627), 390x844 (1089 / 804) |
| `better-value` | 320x568 (1129 / 528), 375x667 (1024 / 627), 390x844 (996 / 804) |
| `tax-theft` | 320x568 (1071 / 528), 375x667 (1071 / 627), 390x844 (1036 / 804) |
| `suvat` | 320x568 (1066 / 528), 375x667 (936 / 627), 390x844 (914 / 804) |
| `word-problem-decoder` | 320x568 (1039 / 528), 375x667 (895 / 627), 390x844 (850 / 804) |
| `given-that` | 320x568 (990 / 528), 375x667 (775 / 627) |
| `differentiation-duel` | 320x568 (864 / 528), 375x667 (864 / 627), 390x844 (864 / 804) |
| `constructions-lab` | 320x568 (859 / 528), 375x667 (822 / 627), 390x844 (815 / 804) |
| `wrong-on-the-internet` | 320x568 (828 / 528), 375x667 (764 / 627) |
| `seven-bridges` | 320x568 (825 / 528), 375x667 (742 / 627) |
| `index-laws` | 320x568 (818 / 528), 375x667 (806 / 627), 390x844 (806 / 804) |
| `screening-room` | 320x568 (808 / 528), 375x667 (677 / 627) |
| `log-laws` | 320x568 (784 / 528), 375x667 (784 / 627) |
| `think-of-a-number` | 320x568 (771 / 528), 375x667 (766 / 627) |
| `integration-duel` | 320x568 (768 / 528), 375x667 (768 / 627) |
| `probability-paradox` | 320x568 (736 / 528) |
| `glorious-gantt` | 320x568 (704 / 528) |
| `growth-and-decay` | 320x568 (702 / 528), 375x667 (635 / 627) |
| `trig-worms` | 320x568 (696 / 528), 375x667 (655 / 627) |
| `terrible-advice` | 320x568 (692 / 528) |
| `test-the-claim` | 320x568 (684 / 528) |
| `decimal-detective` | 320x568 (676 / 528) |
| `expectation-station` | 320x568 (663 / 528) |
| `quadratic-factoriser` | 320x568 (646 / 528) |
| `percentage-flip` | 320x568 (645 / 528) |
| `spot-the-muppet` | 320x568 (611 / 528) |
| `stat-attack` | 320x568 (599 / 528) |
| `circle-theorem-spotter` | 320x568 (596 / 528) |
| `higher-power` | 320x568 (592 / 528) |
| `modular-battle` | 320x568 (588 / 528) |
| `complex-converter` | 320x568 (581 / 528), 375x667 (636 / 627) |
| `negative-number-line` | 320x568 (569 / 528) |
| `gradient-hunter` | 320x568 (567 / 528) |
| `curling-friction` | 320x568 (561 / 528) |

Only in Aa: `seven-bridges`, `screening-room`, `probability-paradox`, `glorious-gantt`, `growth-and-decay`, `terrible-advice`, `test-the-claim`, `expectation-station`, `spot-the-muppet`, `stat-attack`, `circle-theorem-spotter`, `modular-battle`, `negative-number-line`, `gradient-hunter`, `curling-friction`.

## Aa at 320x568 scrolls, options start above the fold (WARN, allowed by the 26 Oct rule): 14 games

`characteristic-quest`, `component-crusher`, `dimension-checker`, `eigenvalue-extractor`, `force-resolver`, `graph-sketcher`, `prisoners-dilemma`, `proportion-blaster`, `scale-factor-scaling`, `sequence-solver`, `standard-form-blitz`, `surd-simplifier`, `trig-identity-duel`, `unit-converter`.

`glorious-gantt` is unlisted (roster Unlisted section); every other game here is live.
