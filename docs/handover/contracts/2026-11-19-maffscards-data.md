=== PART 1 OF 2 ===
MAFFSCARDS-DATA, part 1 of 2. Do not start until part 2 has arrived; it ends with "END OF CONTRACT".
LANE: cloud. Send now. TIER: Medium. MODEL: Claude Code, Opus 5.5, medium effort.

TASK: MaffsCards, Jon's free compare-and-win number card deck, gets one source in the repo: a generator that computes all 48 cards, an independent check in CI, the card data file the online game will read, and the printable PDF as a free download on /printables/.

ROOT CAUSE: New capability. The deck was built and checked in Project Claude's workspace (18 Nov 2026), which does not survive, and is live on Tes as a free resource (CC BY-ND, https://www.tes.com/teaching-resource/-13673762). An online game against the computer is next (Jon, 19 Nov 2026). It and the printed deck must read the same values, so a card can never differ between the two.

CLASS CHECK: Not a bug; new shared data. One generator writes one data file. The PDF and the coming game both read that file and never recompute or retype a value.

EXACT CHANGE:
1. First commit: close out 52DLE-REBUILD (#850, merge a675eea, run 44740406716) in docs/handover/cloud.md: main's runs on its merge commit from the API; contract docs/handover/contracts/2026-11-19-52dle-rebuild.md to docs/history/contracts/. Leave the calculator contract and home.md to the home lane. Save this contract verbatim (both parts) as docs/handover/contracts/2026-11-19-maffscards-data.md.
2. tools/maffscards/gen.py writes data/maffscards.json: for each card, n, deck ("main" or "extra"), nickname, sof, lpf, roman, dist, powers (list, in the order prime, square, cube, triangular, Fibonacci, palindrome), pi; plus the six categories in card order, each with its label and winner (highest, except distance: lowest). The definitions are in part 2.
   The deck list and nicknames are fixed (part 2); the generator computes every value, never reads them.
3. tools/maffscards/check.py, in CI (every PR touching tools/maffscards/ or data/maffscards.json): recompute every value by a second method (pi by Machin's formula, and the generator's spigot; decimals 1-10 = 1415926535 and 991-1000 = 2164201989); compare all 48 cards with part 2's table and with data/maffscards.json. Any difference fails. Plants that must FAIL: one pi count off by one; 1 counted as prime; a hand edit in the JSON.
4. tools/maffscards/build_pdf.py: the printable deck from data/maffscards.json, rendered in Chromium. A4, nine playing cards a page with cut lines. Each card: the number large, nickname (Outfit Bold, teal, at most two lines), the number drawn as dots in its squarest rectangle, the six values with "lowest wins" on distance, the superpower badges inside the card (shrink to no less than 4.4pt, then wrap). Mono-printer safe: nothing relies on colour. Light theme (canon 7.5), Outfit and JetBrains Mono, no emoji. Pages: main 32 plus a rules card and a "how to read your card" card; then the extra 16; then a teacher sheet with every value, how each category works, and five conversation starters (why a single digit beats every two-digit number on pi; why only 1,000 digits, pi not known to be normal; why 1 is not prime; 28 is perfect; why primes lose on sum of factors). Never the words "Top Trumps" anywhere (registered trade mark).
5. Commit the built PDF as printables/maffscards.pdf (it is free; Jon's ruling, 18 Nov 2026). /printables/: one card, "MaffsCards: a compare-and-win number card game", with the free PDF and "View on Tes". One /updates/ line: "MaffsCards, our free number card game, is now on the printables page." cloud.md entry.
6. PR, Gate and phone-fit-full green, merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line.

DO NOT TOUCH: any game; schools/assets/; tools/pack-generator/; canon; docs/handover/home.md; docs/handover/contracts/2026-11-20-calc-implied-mult.md (the home lane's).

SUCCESS CONDITION: gen.py reproduces part 2 exactly; check.py passes in CI and all three plants fail; data/maffscards.json committed; the PDF builds from it and is linked from /printables/; 52DLE-REBUILD closed out; merged GREEN; cloud.md records it all.

STOP IF: any computed value differs from part 2 (report the card and category; change neither); a nickname needs a third line; a badge row can't fit at 4.4pt even wrapped; the PDF needs anything outside KaTeX, Google Fonts and the repo; merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
=== PART 2 OF 2 ===
MAFFSCARDS-DATA, part 2 of 2.
Definitions for item 2:
   a. Sum of factors: every positive divisor, 1 and n included.
   b. Largest prime factor; 1 has none and scores 0 (shown "none").
   c. Roman numeral length, standard subtractive (IV, IX, XL, XC); the numeral is in the data.
   d. Distance to the nearest square of 0,1,4,...,100; lowest wins.
   e. Superpowers: one point each for prime, square, cube, triangular, Fibonacci, palindrome. 1 counts as square, cube, triangular and Fibonacci; 1 is not prime; single digits are palindromes.
   f. In pi's first 1,000 digits: occurrences of n's digits in a row among the 1,000 decimals after the point, overlaps counted, the leading 3 not counted. The label always states the 1,000-digit limit.
The 32 main cards, one per line: n|sum of factors|largest prime factor (0 = none)|Roman numeral|distance to nearest square|superpowers|pi count|nickname
1|1|0|I|0|square,cube,triangular,Fibonacci,palindrome|116|Technically Everything
2|3|2|II|1|prime,Fibonacci,palindrome|103|The Only Even Prime, and Insufferable About It
7|8|7|VII|2|prime,palindrome|95|Lucky for Some, Prime for All
11|12|11|XI|2|prime,palindrome|16|Prime From Both Ends
17|18|17|XVII|1|prime|18|One Past Sixteen and Still Not a Square
21|32|7|XXI|4|triangular,Fibonacci|15|Blackjack, Triangle AND Fibonacci
26|42|13|XXVI|1|-|9|One Letter for Every Superpower It Doesn't Have
27|40|3|XXVII|2|cube|14|Three Threes Walk Into a Cube
28|56|7|XXVIII|3|triangular|13|Perfect, and Knows It
33|48|11|XXXIII|3|palindrome|10|Mirror, Mirror
36|91|3|XXXVI|0|square,triangular|9|The Show-Off Square
37|38|37|XXXVII|1|prime|12|The Loner
43|44|43|XLIII|6|prime|7|Prime, Miles From Any Square
46|72|23|XLVI|3|-|16|The Chromosome Count
48|124|3|XLVIII|1|-|13|Factor Hoarder
49|57|7|XLIX|0|square|11|Seven Sevens, Very Tidy
51|72|17|LI|2|-|10|Looks Prime, Isn't
53|54|53|LIII|4|prime|15|Prime, Ordinary, Proud
55|72|11|LV|6|triangular,Fibonacci,palindrome|6|The Triple Threat
60|168|5|LX|4|-|14|Twelve Factors and a Clock
61|62|61|LXI|3|prime|9|One Minute Over
64|127|2|LXIV|0|square,cube|13|Square AND Cube, and Won't Shut Up About It
68|126|17|LXVIII|4|-|6|Four 17s in a Trench Coat
71|72|71|LXXI|7|prime|13|Prime, Stuck in the Seventies
74|114|37|LXXIV|7|-|7|Two 37s Holding Hands
77|96|11|LXXVII|4|palindrome|9|Sevens All the Way Down
88|180|11|LXXXVIII|7|palindrome|9|LXXXVIII: Roman for "Ouch"
89|90|89|LXXXIX|8|prime,Fibonacci|9|Fibonacci's Lanky Prime
93|128|31|XCIII|7|-|14|Also Looks Prime, Also Isn't
94|144|47|XCIV|6|-|11|Two 47s, No Plan
96|252|3|XCVI|4|-|9|The Factor Factory
100|217|5|C|0|square|1|The Big Round One
The 16 extra cards, same columns:
4|7|2|IV|0|square,palindrome|93|Two Twos, Squared Away
5|6|5|V|1|prime,Fibonacci,palindrome|97|High Five: Prime, Fibonacci, Palindrome
13|14|13|XIII|3|prime,Fibonacci|12|Unlucky? It's Prime AND Fibonacci
19|20|19|XIX|3|prime|16|One Short of a Score
34|54|17|XXXIV|2|Fibonacci|12|Fibonacci in Disguise
38|60|19|XXXVIII|2|-|12|No Powers, Just Vibes
47|48|47|XLVII|2|prime|5|Two Short of a Square
59|60|59|LIX|5|prime|16|Last Prime Before Sixty
63|104|7|LXIII|1|-|6|One Short of a Square AND a Cube
66|144|11|LXVI|2|triangular,palindrome|11|Route 66: Triangular Palindrome
73|74|73|LXXIII|8|prime|10|Prime Both Ways
75|124|5|LXXV|6|-|12|Three Quarters of a Hundred
80|186|5|LXXX|1|-|6|So Close to 81 It Hurts
87|120|29|LXXXVII|6|-|9|The Prime Impersonator
92|168|23|XCII|8|-|13|Four 23s Pretending to Be One Number
95|120|19|XCV|5|-|16|Five 19s and a Dream
END OF CONTRACT
