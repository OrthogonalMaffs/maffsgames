/* Room data for "hamster-heist" — shared by index.html (the game) and
   teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand.

   PREMISE — corrected 2026-09-08. There is no theft, no toy and no deception:
   Lungey confiscated Pythagoras at lunchtime and shut him in the old cage at
   the back of Beaker's lab, and the students are putting that right. One
   failure state only — the 3:30 bell wakes Mr Beaker, who is asleep in the
   store room and knows nothing about any hamster. The technician's round is at
   quarter to four and is the last beat of the win, not a threat.

   VOICE — Beaker's sleep-talk carries the wrong-entry slot (see `wrongLines`).
   He never wakes; only the bell does that. Lungey is named as the cause and
   never speaks — he speaks in his own room. The technician has no lines.

   ART — instrument pictures are dropped set-wide (scene, fail and win only);
   the engine draws the live control anyway, so the `art`/`artAlt` fields are
   gone from all three locks below. Removed here 2026-09-08 — this room predates
   the decision and had kept the wheel, the feeder and the heat lamp, which no
   longer match the empty-room style. The three .webp files are left on disk,
   as pe-shed-rebellion's are.

   NOTE — object `id`s are load-bearing: teacher.html maps clues to locks by id
   in its `clueMap`. Renaming one silently breaks the teacher page. The six
   clue-carrying ids below are unchanged from the original build.

   PENDING ART: sceneAlt describes the new laboratory picture, failAlt and
   winAlt the two agreed on 2026-09-08. None of the three is on disk yet — the
   image swap is the immediately-following job and this room should not ship
   until it lands. */
window.ROOM = {
  slug: 'escape-hamster-heist',
  title: 'The Great Hamster Heist',
  level: 'ks3',
  minutes: 15,
  penalty: 45,
  art: 'hamster-heist',
  sceneAlt: 'A cluttered school science prep room. Benches run down both sides under shelves of jars, flasks and bottles, with a fume cupboard against the far wall and a desk lamp lit over the central bench among test tubes, clamps and trailing leads. Animal cages stand on the near bench. The store room door in the background is ajar with the light on inside. Old diagrams are pinned to the walls.',
  failAlt: 'A close view of the old wire cage on the laboratory bench, its door shut and the latch still across it. Inside, on a thin scatter of sawdust, a small brown and white hamster sits facing out. A dynamo is bolted to the top of the cage, a feed hopper hangs inside the bars, and a heat lamp is angled over it on a bracket. Glass jars and round-bottomed flasks stand on the bench behind, with a rack of test tubes by the window.',
  winAlt: 'A tidy corner of a school classroom after home time. A clean hamster cage stands on a low cabinet with wood shavings, a full water bottle and a small wheel, and a hamster asleep in a nest of bedding. A clipboard hangs on a hook beside the cage. Late afternoon sun comes low through the window, warm and settled, with the rest of the room in soft shadow and the chairs up on the desks.',

  hook: 'Pythagoras has his own cage, in his own room, and a line on the technician&rsquo;s list that gets ticked ' +
        'every day at quarter to four. At lunchtime Mr Lunge found him out by the field. Head of P.E., twenty-six ' +
        'years, and absolutely certain that a loose hamster is a health and safety matter. He confiscated him with ' +
        'total confidence, and that was as far as the thinking went. The nearest cage he could find was ' +
        'the ancient thing at the back of Mr Beaker&rsquo;s lab, so that is where Pythagoras is. Lungey has ' +
        'told nobody. Lungey has gone back to his lesson.',
  brief: 'Mr Beaker built that cage twenty years ago for an animal nobody will name. Three instruments hold the ' +
         'latch shut, and nobody has had cause to open it since. He is asleep in the store room with the door ' +
         'ajar, having an argument in his sleep about the shape of the Earth with a colleague called ' +
         'Geoffrey. Geoffrey is not in the store room. Geoffrey retired in 1994. You have fifteen ' +
         'minutes until the bell. Get the latch open, get Pythagoras out, and get him back where he lives before ' +
         'the round at quarter to four. Mr Beaker is deaf to almost everything. He is not deaf to the bell.',
  stakes: 'Every wrong setting makes a noise, and every noise costs you time you have not got. Run the clock out ' +
          'and the bell goes at half past three, Mr Beaker wakes, and he comes through to find three students in a ' +
          'lab they are not supposed to be in, with their hands in equipment they are not supposed to touch. He ' +
          'knows nothing about a hamster. He has no reason to think there is one. There is nothing you could say ' +
          'to him that would help.',
  win: 'The last catch goes and the door swings. Pythagoras is entirely unbothered by the whole affair and mildly ' +
       'annoyed to have been woken. He is back in his own cage, with his own wheel and his own water bottle, ' +
       'several minutes before anybody comes looking. At quarter to four the technician comes round with his ' +
       'clipboard, the way he does every day. Hamster: present. Water: full. Bedding: clean. Wheel: turning ' +
       'freely. He ticks all four and moves on, and never finds out that for one afternoon there was nothing ' +
       'there to tick.',

  /* Wrong-entry lines, indexed by how many wrong settings have been made so
     far; the last one repeats. Beaker is arguing the hull-first horizon proof,
     correctly, in his sleep, with a colleague who left in 1994. He never wakes,
     never helps and never notices.
     WIRED 2026-09-08: the engine reads this array, indexed by st.wrongs - 1 and
     clamped to the last entry. A misconception hit consumes an index without
     printing a line, which is intended — see wrongLine() in engine.js. */
  wrongLines: [
    { head: 'The dynamo whines and drops away.',
      body: 'Through the store-room door, fast asleep and mid-argument: &ldquo;&hellip;it&rsquo;s the ships, ' +
            'Geoffrey.&rdquo;' },
    { head: 'The hopper latch clacks, loudly.',
      body: '&ldquo;Watch one go out. You lose the hull first. Then the funnel. Then the mast.&rdquo; He does not ' +
            'stir.' },
    { head: 'Something inside the frame resets itself with a clunk.',
      body: '&ldquo;If it were flat you would see the whole ship at once. All of it. The whole ship, ' +
            'Geoffrey.&rdquo;' },
    { head: 'Another one. The bell is no further off than it was.',
      body: '&ldquo;&hellip;Geoffrey?&rdquo;' }
  ],

  objects: [
    { id: 'invoice', name: 'Yellowed invoice', where: 'spiked on a nail by the prep-room door',
      clue: 'ST MARTHA&rsquo;S &mdash; SUNDRIES. &ldquo;Replacement running wheel, <b>{{rpm.d}} cm ' +
            'diameter</b>.&rdquo; The date has gone brown along with the rest of the paper. The biro ' +
            'underneath has not: &ldquo;Do not order the cheap ones again.&rdquo;' },
    { id: 'clipboard', name: 'Clipboard on the cage frame', where: 'hanging where it has hung for twenty years',
      clue: 'FIRST CATCH. &ldquo;Releases when the wheel is covering <b>{{rpm.K}}&pi; cm every second</b>. Dial is ' +
            'marked in <b>revolutions per minute</b>. Not the same thing. Watch the units.&rdquo;' },
    { id: 'hopperlabel', name: 'Peeling label', where: 'coming away from the side of the hopper',
      clue: '<b>HOPPER.</b> Cross-section <b>{{bnd.X}} square centimetres exactly</b> &mdash; cut it myself, it is ' +
            'exact. Depth <b>{{bnd.D}} centimetres</b>, measured to the nearest centimetre.' },
    { id: 'slip', name: 'Instruction slip', where: 'in the bottom of the pellet tin',
      clue: '&ldquo;The hopper drops its catch when it is told <b>the smallest volume it could possibly be ' +
            'holding</b>. Not what is in it. The least it could be.&rdquo;' },
    { id: 'jotter', name: 'The cage log', where: 'a ruled jotter, kept up for twenty years and never once read',
      clue: 'Warming, plotted, and it comes out straight: <b>{{grad.t1}} minutes &mdash; {{grad.T1}} degrees. ' +
            '{{grad.t2}} minutes &mdash; {{grad.T2}} degrees.</b>' },
    { id: 'manual', name: 'Heat lamp manual', where: 'being used to prop up a bench leg',
      clue: '&ldquo;The lamp holds the last catch until it is set to the <b>warming rate it should expect, in ' +
            'degrees per minute</b>. Get it wrong and it simply goes on holding.&rdquo;' },
    { id: 'planets', name: 'Solar system model', where: 'on the top shelf, dusty', clue: null,
      flavour: 'Pluto is still on it. Someone has re-attached Pluto by hand, more than once, with different glue ' +
               'each time.' },
    { id: 'mug', name: 'Mr Beaker’s mug', where: 'on the bench, stone cold', clue: null,
      flavour: 'There is a spoon standing up in it. You are not going to be the one who moves it.' }
  ],

  locks: [
    {
      id: 'hamster-wheel-rpm',
      key: 'rpm',
      grade: 5,
      name: 'The hamster wheel',
      brief: 'The first catch runs off the dynamo, and it will not let go until the dynamo is turning at the speed ' +
             'the wheel is supposed to produce.',
      instrument: { kind: 'slider', label: 'Dynamo speed', min: 0, max: 500, step: 1, decimals: 0,
                    unit: 'RPM', start: 0, verb: 'Set the dynamo' },
      variants: [
        {
          "d": 20,
          "K": 120,
          "answer": 360,
          "miss": 6
        },
        {
          "d": 10,
          "K": 50,
          "answer": 300,
          "miss": 5
        },
        {
          "d": 34,
          "K": 238,
          "answer": 420,
          "miss": 7
        },
        {
          "d": 36,
          "K": 144,
          "answer": 240,
          "miss": 4
        },
        {
          "d": 36,
          "K": 288,
          "answer": 480,
          "miss": 8
        },
        {
          "d": 10,
          "K": 30,
          "answer": 180,
          "miss": 3
        }
      ],
      missTitle: '{{rpm.miss}} is right &mdash; {{rpm.miss}} per <i>second</i>.',
      missSays: '{{rpm.miss}} turns a second is exactly the right piece of work. But the dial is marked RPM: ' +
                'revolutions per <b>minute</b>. One step left, and it is a &times;60.',
      hints: [
        'One turn of the wheel covers one circumference. Work out that circumference, then how many turns ' +
        '{{rpm.K}}&pi; cm is &mdash; and then read the dial&rsquo;s units very carefully.',
        'Circumference = &pi;d = {{rpm.d}}&pi; cm. Turns per second = {{rpm.K}}&pi; &divide; {{rpm.d}}&pi;. The ' +
        '&pi; cancels. Then convert from per second to per minute.',
        '{{rpm.K}}&pi; &divide; {{rpm.d}}&pi; = {{rpm.miss}} turns per second. {{rpm.miss}} &times; 60 = ' +
        '<b>{{rpm.answer}} RPM</b>.'
      ],
      solve: 'Circumference = {{rpm.d}}&pi; cm. {{rpm.K}}&pi; &divide; {{rpm.d}}&pi; = {{rpm.miss}} turns a second, ' +
             '&times;60 = <b>{{rpm.answer}} RPM</b>.',
      onOpen: 'The dynamo catches and settles. Somewhere inside the frame there is a single dry click, and the ' +
              'first catch comes off a cage that has not been opened in twenty years.'
    },
    {
      id: 'hamster-feeder-bounds',
      key: 'bnd',
      grade: 5,
      name: 'The feeder',
      brief: 'The second catch is on the hopper, and it will not lift until it is told the smallest volume the ' +
             'hopper could possibly be holding. It is a prism, and Mr Beaker cut the cross-section exactly.',
      instrument: { kind: 'slider', label: 'Feeder release volume', min: 0, max: 1000, step: 1, decimals: 0,
                    unit: 'cm³', start: 0, verb: 'Set the release' },
      variants: [
        {
          "X": 40,
          "D": 15,
          "answer": 580,
          "miss": 600,
          "lb": "14.5"
        },
        {
          "X": 76,
          "D": 12,
          "answer": 874,
          "miss": 912,
          "lb": "11.5"
        },
        {
          "X": 14,
          "D": 22,
          "answer": 301,
          "miss": 308,
          "lb": "21.5"
        },
        {
          "X": 56,
          "D": 15,
          "answer": 812,
          "miss": 840,
          "lb": "14.5"
        },
        {
          "X": 20,
          "D": 11,
          "answer": 210,
          "miss": 220,
          "lb": "10.5"
        },
        {
          "X": 80,
          "D": 10,
          "answer": 760,
          "miss": 800,
          "lb": "9.5"
        },
        {
          "X": 48,
          "D": 14,
          "answer": 648,
          "miss": 672,
          "lb": "13.5"
        },
        {
          "X": 26,
          "D": 16,
          "answer": 403,
          "miss": 416,
          "lb": "15.5"
        },
        {
          "X": 18,
          "D": 9,
          "answer": 153,
          "miss": 162,
          "lb": "8.5"
        },
        {
          "X": 38,
          "D": 19,
          "answer": 703,
          "miss": 722,
          "lb": "18.5"
        }
      ],
      missTitle: '{{bnd.miss}} treats a rounded measurement as exact.',
      missSays: '{{bnd.X}} &times; {{bnd.D}} = {{bnd.miss}} uses the depth as if it were exactly {{bnd.D}} cm. It ' +
                'was measured <i>to the nearest centimetre</i>, so the true depth is anywhere from {{bnd.lb}} cm ' +
                'up to (but not reaching) {{bnd.D}}.5 cm &mdash; and the hopper asked for the <b>smallest</b> ' +
                'volume it could be holding, which is the shallowest it could be.',
      hints: [
        '&ldquo;To the nearest centimetre&rdquo; means the depth is almost certainly not exactly {{bnd.D}}. What is ' +
        'the <i>shallowest</i> it could be and still have been written down as {{bnd.D}}?',
        'The lower bound of a length measured to the nearest cm is half a centimetre below it &mdash; and that ' +
        'depth really does round to {{bnd.D}}. The volume of a prism is cross-section &times; depth, and the ' +
        'cross-section here is exact.',
        'Lower bound of the depth = {{bnd.lb}} cm. Volume = {{bnd.X}} &times; {{bnd.lb}} = ' +
        '<b>{{bnd.answer}} cm&sup3;</b>.'
      ],
      solve: 'Lower bound of depth = {{bnd.lb}} cm. Volume = {{bnd.X}} &times; {{bnd.lb}} = ' +
             '<b>{{bnd.answer}} cm&sup3;</b>.',
      onOpen: 'The hopper latch lifts a quarter of an inch and stays lifted. Second catch off.'
    },
    {
      id: 'heat-lamp-gradient',
      key: 'grad',
      grade: 4,
      name: 'The heat lamp',
      brief: 'The last catch is held by the thermostat. It wants to be told how fast the cage should be warming.',
      instrument: { kind: 'slider', label: 'Expected warming rate', min: 0, max: 20, step: 0.1, decimals: 1,
                    unit: '°C/min', start: 0, verb: 'Set the rate' },
      variants: [
        {
          "t1": 4,
          "T1": 21,
          "t2": 16,
          "T2": 39,
          "rise": 18,
          "run": 12,
          "answer": 1.5,
          "miss": 18.0,
          "aTxt": "1.5",
          "mTxt": "18.0"
        },
        {
          "t1": 3,
          "T1": 19,
          "t2": 13,
          "T2": 37,
          "rise": 18,
          "run": 10,
          "answer": 1.8,
          "miss": 18.0,
          "aTxt": "1.8",
          "mTxt": "18.0"
        },
        {
          "t1": 5,
          "T1": 15,
          "t2": 21,
          "T2": 31,
          "rise": 16,
          "run": 16,
          "answer": 1.0,
          "miss": 16.0,
          "aTxt": "1.0",
          "mTxt": "16.0"
        },
        {
          "t1": 3,
          "T1": 15,
          "t2": 18,
          "T2": 27,
          "rise": 12,
          "run": 15,
          "answer": 0.8,
          "miss": 12.0,
          "aTxt": "0.8",
          "mTxt": "12.0"
        },
        {
          "t1": 6,
          "T1": 20,
          "t2": 21,
          "T2": 38,
          "rise": 18,
          "run": 15,
          "answer": 1.2,
          "miss": 18.0,
          "aTxt": "1.2",
          "mTxt": "18.0"
        },
        {
          "t1": 4,
          "T1": 15,
          "t2": 14,
          "T2": 35,
          "rise": 20,
          "run": 10,
          "answer": 2.0,
          "miss": 20.0,
          "aTxt": "2.0",
          "mTxt": "20.0"
        },
        {
          "t1": 5,
          "T1": 24,
          "t2": 13,
          "T2": 44,
          "rise": 20,
          "run": 8,
          "answer": 2.5,
          "miss": 20.0,
          "aTxt": "2.5",
          "mTxt": "20.0"
        }
      ],
      missTitle: '{{grad.rise}} is the whole climb, not the rate.',
      missSays: '{{grad.T2}} &minus; {{grad.T1}} = {{grad.rise}} is how much warmer it got &mdash; but that took ' +
                '{{grad.run}} minutes to happen. A rate is per <i>one</i> minute, so the rise still has to be ' +
                'divided by the run.',
      hints: [
        'A rate is per minute. You have two readings, and they are not one minute apart.',
        'On a straight-line graph the rate is the gradient: rise &divide; run. The rise is the temperature ' +
        'difference; the run is the time between the readings.',
        'Rise = {{grad.T2}} &minus; {{grad.T1}} = {{grad.rise}}&deg;. Run = {{grad.t2}} &minus; {{grad.t1}} = ' +
        '{{grad.run}} minutes. Gradient = {{grad.rise}} &divide; {{grad.run}} = ' +
        '<b>{{grad.aTxt}} &deg;C per minute</b>.'
      ],
      solve: 'Gradient = ({{grad.T2}}&minus;{{grad.T1}}) &divide; ({{grad.t2}}&minus;{{grad.t1}}) = {{grad.rise}} ' +
             '&divide; {{grad.run}} = <b>{{grad.aTxt}} &deg;C/min</b>.',
      onOpen: 'The lamp dims to a low steady red, satisfied. The last catch slides back and the door swings a ' +
              'couple of inches on its own.'
    }
  ]
};
