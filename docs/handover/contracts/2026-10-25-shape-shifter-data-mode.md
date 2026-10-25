# Contract SHAPE-SHIFTER-DATA-MODE (Jon, 25 Oct 2026), verbatim

TASK: Give Shape Shifter's four mode cards data-mode attributes so a burst can open Random Mix.

ROOT CAUSE: The mode cards are bare onclick elements, so burst.js has nothing to press, and a burst lands on the menu.

CLASS CHECK: No. burst.js's interface (press [data-mode]) is correct. This one game doesn't take part in it. Fixing it in the game is right.

EXACT CHANGE: games/shape-shifter/index.html: add data-mode="<slug>" to each of the four mode cards. Use short lowercase slugs, with random-mix for Random Mix. Leave the onclick handlers, how the cards look and the order they appear in unchanged.

DO NOT TOUCH: schools/assets/burst.js (the home lane is changing it). Shape Shifter's questions, scoring or analytics. Any other game.

SUCCESS CONDITION:
  - /games/shape-shifter/?burst=5&from=six-ps&topic=transformations&mode=random-mix starts Random Mix, and the game's own start state confirms it.
  - Played normally (no burst), the menu works exactly as before.
  - check-changed.py passes, then the PR merges with main green. Handover in the cloud lane's own file only.

STOP IF: The cards share a handler that burst.js's press would fire twice. Or Random Mix needs more setup than one press.
