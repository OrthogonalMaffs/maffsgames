# Items for individually written worked lines (25 Oct 2026)

For Project Claude (contract SIX-PS-BANKS, part C of the 25 Oct addition): the two sets of items as they appear in
the games, read by `scripts/extract-banks.py` from the live pages, unedited. The worked lines for them are written
individually, so they stay on the missing-worked list until they arrive.

## equation-builder, level ks3, topic "Forming Equations" (9 items, `QUESTIONS[i]`)

`type` is `assembly` (build the answer from `tiles`; `slots` is the correct order) or `gapfill`.

```json
// QUESTIONS[0]
{"id": "eb_ks3_001", "level": "ks3", "type": "assembly", "topic": "Forming Equations", "text": "A taxi company charges a fixed booking fee of £3 plus £2.50 for every mile of the journey. A customer wants to know the total cost C pounds of a journey of m miles. Write a formula for C.", "slots": ["C", "=", "2.50m", "+", "3"], "tiles": ["C", "=", "2.50m", "+", "3", "−", "×", "2.50", "m", "3m"]}
// QUESTIONS[1]
{"id": "eb_ks3_002", "level": "ks3", "type": "assembly", "topic": "Forming Equations", "text": "A farmer mixes sand and cement in the ratio 5:1 to make mortar. He uses x kg of cement. Write a formula for the total mass T kg of the mortar mixture.", "slots": ["T", "=", "6x"], "tiles": ["T", "=", "6x", "5x", "+6", "x+5", "÷", "×", "5"]}
// QUESTIONS[2]
{"id": "eb_ks3_003", "level": "ks3", "type": "assembly", "topic": "Forming Equations", "text": "A plumber charges £45 for each hour he works, plus a fixed call-out charge of £60. Write a formula for the total charge T pounds when the plumber works for h hours.", "slots": ["T", "=", "45h", "+", "60"], "tiles": ["T", "=", "45h", "+", "60", "−", "×", "105h", "45", "h"]}
// QUESTIONS[3]
{"id": "eb_ks3_004", "level": "ks3", "type": "assembly", "topic": "Forming Equations", "text": "Ellie is e years old. Her brother is 4 years younger than her. Their mum is three times Ellie’s age. Write a formula for S, the sum of all three ages.", "slots": ["S", "=", "e", "+", "(e−4)", "+", "3e"], "valid": ["4e"], "tiles": ["S", "=", "e", "+", "(e−4)", "+", "3e", "−", "4e", "×", "(e+4)"]}
// QUESTIONS[10]
{"id": "eb_ks3_011", "level": "ks3", "type": "assembly", "topic": "Forming Equations", "text": "Packets of crisps come in boxes of 24. A school canteen orders x boxes and keeps 6 packets aside as samples. Write a formula for the number of packets N available to sell.", "slots": ["N", "=", "24x", "−", "6"], "tiles": ["N", "=", "24x", "−", "6", "+", "×", "18x", "24", "÷"]}
// QUESTIONS[19]
{"id": "eb_ks3_020", "level": "ks3", "type": "assembly", "topic": "Forming Equations", "text": "A swimming pool holds V litres when full. It is currently three-eighths full and contains 360 litres. Write an equation to find V.", "slots": ["3V", "÷", "8", "=", "360"], "valid": ["×"], "tiles": ["3V", "÷", "8", "=", "360", "+", "×", "3V", "8V", "−"]}
// QUESTIONS[29]
{"id": "eb_ks3_030", "level": "ks3", "type": "gapfill", "topic": "Forming Equations", "text": "A plumber charges £45 per hour plus £60 call-out. A customer pays £T. Write the formula for the number of hours h worked.", "slots": ["h", "=", "(T", "−", "60)", "÷", "45"], "tiles": ["−", "+", "×", "÷"], "prefilled": [0, 1, 2, 4, 5, 6]}
// QUESTIONS[35]
{"id": "eb_ks3_036", "level": "ks3", "type": "gapfill", "topic": "Forming Equations", "text": "A number n is doubled and then 9 is subtracted to give 25. Write the equation.", "slots": ["2n", "−", "9", "=", "25"], "tiles": ["−", "+", "×", "÷"], "prefilled": [0, 2, 3, 4]}
// QUESTIONS[39]
{"id": "eb_ks3_040", "level": "ks3", "type": "gapfill", "topic": "Forming Equations", "text": "A water tank is three-eighths full and holds 360 litres. Write the equation for the full capacity V litres.", "slots": ["3V", "÷", "8", "=", "360"], "tiles": ["÷", "×", "+", "−"], "prefilled": [0, 2, 3, 4]}
```

## probability-pioneer, stage 1 (10 items, `STAGE1[i]`)

`answer` is the event's position on the 0 to 1 scale; `label` is the game's word for it.

```json
// STAGE1[0]
{"event": "You will breathe today", "answer": 1, "label": "Certain"}
// STAGE1[1]
{"event": "You will roll a 7 on a standard die", "answer": 0, "label": "Impossible"}
// STAGE1[2]
{"event": "It will rain somewhere in Britain this week", "answer": 0.75, "label": "Likely: very likely, but not certain. Certain means it must happen"}
// STAGE1[3]
{"event": "You will flip heads on a fair coin", "answer": 0.5, "label": "Even Chance"}
// STAGE1[4]
{"event": "A randomly chosen month starts with J", "answer": 0.25, "label": "Unlikely"}
// STAGE1[5]
{"event": "You pick a red card from a standard pack", "answer": 0.5, "label": "Even Chance"}
// STAGE1[6]
{"event": "You roll an even number on a die", "answer": 0.5, "label": "Even Chance"}
// STAGE1[7]
{"event": "You win the lottery with one ticket", "answer": 0.25, "label": "Unlikely: about 1 in 45 million, but possible"}
// STAGE1[8]
{"event": "A baby born today is a boy", "answer": 0.5, "label": "Even Chance"}
// STAGE1[9]
{"event": "The sun will rise tomorrow", "answer": 1, "label": "Certain"}
```
