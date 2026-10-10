/* Room data for "car-trap" — shared by index.html (the game) and
   teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand.

   REWRITTEN 2026-10-10 (contract CAR-TRAP-BUILD) from the draft Jon approved on
   9 Oct, 22:53 (docs/escape-room-drafts/car-trap-draft.md, with his three changes).
   The governors are coming, the deputy head, Mr Strictman, has rigged the staff
   car park, and the students put three machines back to their own paperwork. Mr
   Strictman is invented and maps to no real person (Jon confirmed). The Head never
   speaks: he speaks only in prom-budget. Lock 1, head-bay-lower-bound, is bank
   batch 8 (docs/lock-bank-batch8.txt) and replaces visitor-space-bounds, whose
   bank entry and generator library are kept as history. Locks 2 and 3 keep every
   maths field; only their framing changed.

   NOTE — object `id`s are load-bearing: teacher.html maps clues to locks by id
   in its `clueMap`. The six clue ids are the old room's; `hatchback` and `sign`
   are the two blanks.

   NOTE — not one numeral is typed into a clue string. Lock 1's precision is
   written "to the nearest ten centimetres" in words: as a numeral, the 10 would
   be a clue figure and collide with the other locks' (check-escape-rooms.py).
   The only figures in the prose outside tokens are in words: "two point six
   centimetres" (wrong-entry line 1, Jon's line), "ten" and "five centimetres"
   (lock 1's constant precision), "fifteen minutes" and "eight sharp".

   ART: pending, the ART-PENDING way (#244, 10 Oct): this room has no `art` field,
   so the engine requests no picture at all (no scene, fail thumbnail or end-card
   picture) and check-escape-rooms.py lists it as art pending. The six old pictures
   (car-trap-scene, -fail, -win and the three carpark-* lock pictures) show the old
   premise (the orange sports car, the VISITOR bay) and stay in docs/art/ untouched.
   When Jon's three new pictures are filed, add `art:` naming them and check the
   alts below against them (rewrite winAlt for the win picture's view). No lock has
   art.

   RULE — the fail picture shows the barrier down in front of the Head's car, which
   is only true at time-out. Never set `missArt` on any lock in this room: the
   engine shows the fail picture beside a misconception response only when that
   flag is set. */
window.ROOM = {
  slug: 'escape-car-trap',
  title: 'The Headteacher’s Car Trap',
  level: 'gcse',
  levelLabel: 'GCSE / Core Maths',
  minutes: 15,
  penalty: 45,
  sceneAlt: 'An underground staff car park under cold strip lighting, early morning, with concrete pillars and a wet floor. In a row of bays by the lift, one bay is plainly narrower than the rest, its new white line bright beside the faint ghost of the old one. A small hatchback with stick-on eyelashes on its headlights is parked in the wide bay beside it. A walk-behind line-marking machine stands by the fresh line. A charging post with its cover open is at the head of the narrow bay, a barrier arm is down at the foot of the entrance ramp, and at the far end of the row a measuring wheel leans against a bollard.',
  failAlt: 'The same car park from the foot of the ramp. A plain, sensible grey hybrid car has stopped at the barrier, its arm down across the lane just in front of the bonnet. Beyond the arm the row of bays stands waiting, the narrow bay among them, and a clipboard rests on top of the barrier post.',
  winAlt: 'The same row of bays. Every line is crisp and even. The grey hybrid is parked squarely in its bay, its charging cable plugged in and a small green light on the post. In the bay beside it, the eyelash hatchback sits across the new white line, half in one bay and half in the next. The barrier arm is up.',

  hook: 'It is the morning of the governors&rsquo; visit. The Head is driving in to meet them, in an old plug-in ' +
        'hybrid that he calls a statement of environmental leadership and everybody else calls the dullest car in ' +
        'the county.<br><br>' +
        'Nobody here has any illusions about the Head. But the school also has a deputy head, and the deputy head ' +
        'is Mr Strictman: ex-military, marches between lessons, civvies starched so stiff they could stand to ' +
        'attention on their own. He wants the Head&rsquo;s job. He already talks as though he has it.<br><br>' +
        'He is down in the staff car park now with a clipboard and a measuring wheel, doing what he calls an ' +
        'efficiency survey of the bays. You are the student welcome party. You were told to wait by the lift and ' +
        'look smart.',
  brief: 'It is not a survey. He was in before the caretaker this morning. He has repainted the Head&rsquo;s bay ' +
         'narrower than the specification allows, set the barrier to come down early, and set the charging post ' +
         'to trip. When the Head arrives in front of the governors it will be a farce, and the report Mr ' +
         'Strictman has already half written will say that the school lacks discipline at the top.<br><br>' +
         'He is at the far end of the row, measuring one bay at a time and marching towards you. That is your ' +
         'fifteen minutes.<br><br>' +
         'He set three machines against their own paperwork. You are setting each one back to it: the line where ' +
         'the specification puts it, the barrier to its calibration, the charger inside its limit. All the ' +
         'paperwork is down here with you. Every wrong setting makes a noise that carries in concrete, and costs ' +
         'you time.',
  /* There is no `fail` slot: the engine shows `stakes` after "If you get it
     wrong." on the start screen and after "And so:" on the time-out screen, so
     the failure is written here and reads after both. */
  stakes: 'The Head comes down the ramp in his plug-in hybrid and stops at the barrier, its arm already down in ' +
          'front of his bonnet, with the governors waiting on the other side of it. Mr Strictman steps forward ' +
          'with his clipboard, looks at the car, and says one word: &ldquo;Disappointing.&rdquo; If the top job ' +
          'goes to him, it is drill in the yard every morning and uniform inspections at the gate.',
  win: 'The barrier lifts. The Head comes down the ramp at the speed of a man who knows he is being watched, and ' +
       'glides into his bay without touching a line. He gets out, straightens his tie and goes to shake hands ' +
       'with the governors, with no idea that anything has happened to him this morning. That is how he gets ' +
       'through most mornings.<br><br>' +
       'The governors aren&rsquo;t looking at him. They are looking at the bay next door, where, with every line ' +
       'back to specification, the one car in the row parked across two bays is a small hatchback with stick-on ' +
       'eyelashes on its headlights.<br><br>' +
       'Mr Strictman reaches the end of the row with his clipboard. He looks at the car. He looks at the line ' +
       'under it. Then he explains, at some length and standing very straight, that the car is his ' +
       'daughter&rsquo;s, that his own is in the garage, and that it was parked correctly when he left it.<br><br>' +
       '&ldquo;Out of specification,&rdquo; he says at last. &ldquo;My error. It will be corrected.&rdquo; He moves ' +
       'it himself, in one perfect manoeuvre, and marches off to start his report again from the beginning.',

  /* Wrong-entry lines, indexed by how many wrong settings have been made so
     far; the last one repeats (the joke: he just keeps coming). Each head is the
     car park's reaction; each body is Mr Strictman dictating into his phone as he
     comes down the row. None of them mentions the students. */
  wrongLines: [
    { head: 'The setting clears with a beep that carries.',
      body: 'From the far end of the row, the tick of a measuring wheel, then a parade-ground voice dictating into ' +
            'a phone: &ldquo;Those two bays differ by two point six centimetres. This is not how it is done in MY ' +
            'school.&rdquo;' },
    { head: 'Something in a control box resets with a clunk.',
      body: 'Closer. The wheel ticks along another line. &ldquo;Paint wandering on the left-hand side. Bollard out ' +
            'of true. Noted.&rdquo; A pen clicks. &ldquo;When this is MY car park, the lines will be inspected every ' +
            'morning. By me.&rdquo;' },
    { head: 'The setting slides back to where it was.',
      body: '&ldquo;Drill in the yard, eight sharp, every morning. Uniform inspected at the gate, top button to ' +
            'toecap. Standards start at the top.&rdquo; The wheel ticks on. &ldquo;And the top is about to ' +
            'change.&rdquo;' },
    { head: 'Another one. The ticking is closer than it was.',
      body: '&ldquo;Next bay.&rdquo;' }
  ],

  objects: [
    { id: 'spec', name: 'The bay specification', where: 'on a clipboard hooked to the reserved sign',
      clue: '<b>HEADTEACHER&rsquo;S BAY.</b> Width <b>{{bay.W}} m</b>, to the nearest ten centimetres. Lines to be ' +
            'maintained to specification.' },
    { id: 'botcard', name: 'Card on the line marker', where: 'taped to the handle',
      clue: '&ldquo;RE-MARKING: measures from the line next door. Set it to <b>the smallest width the ' +
            'specification allows</b>. Anything wider comes out of the bay next door.&rdquo;' },
    { id: 'maintlog', name: 'Barrier maintenance log', where: 'in a plastic wallet zip-tied to the barrier post',
      clue: 'BOOM ARM: <b>{{gate.r}} m</b> from pivot to tip. Counterweight checked. Arm replaced last term after ' +
            'the incident with the fish van. Today&rsquo;s entry, in very straight capitals: SETTINGS REVISED. ' +
            'EFFICIENCY. Initialled.' },
    { id: 'sensor', name: 'Calibration sheet', where: 'taped inside the barrier control box',
      clue: '&ldquo;The control box resets to its proper swing when it is given <b>the angle the arm turns through ' +
            'while its tip travels an arc of exactly {{gate.kpi}} metres</b>. It measures how far the tip travels ' +
            'round the pivot, not how high the arm lifts.&rdquo;' },
    { id: 'commission', name: 'Charger commissioning label', where: 'stuck inside the charging post cover',
      clue: 'LOAD LIMITER: <b>L(x) = x&sup2; &minus; {{amp.b}}x + {{amp.c}}</b>, for a charging current of x amps. ' +
            '<b>Commissioning completes at zero load.</b>' },
    { id: 'alarmnote', name: 'Note from the site electrician', where: 'biro on the back of a delivery slip',
      clue: '&ldquo;Anything <b>above {{amp.lim}} A</b> on that circuit and the network alarm goes off in the front ' +
            'office. It has done it twice this term and they blame me both times.&rdquo;' },
    { id: 'hatchback', name: 'A small hatchback', where: 'in the deputy head’s bay', clue: null,
      flavour: 'It has stick-on eyelashes on both headlights and a fluffy cover on the steering wheel. It is parked ' +
               'in the deputy head&rsquo;s bay, which this morning is the widest bay in the row, and it is using ' +
               'all of it.' },
    { id: 'sign', name: 'The reserved sign', where: 'on a post at the end of the Head’s bay', clue: null,
      flavour: 'RESERVED, in old enamel. Underneath, a new laminated label has been stuck on perfectly level: UNDER ' +
               'REVIEW.' }
  ],

  locks: [
    {
      id: 'head-bay-lower-bound',
      key: 'bay',
      name: 'The line marker',
      brief: 'Mr Strictman narrowed the Head&rsquo;s bay with this. The marker measures from the line next door and ' +
             'paints a new line at whatever width it is set to. The card on its handle says which width to give it.',
      instrument: { kind: 'slider', label: 'Bay width', min: 2, max: 3, step: 0.01, decimals: 2,
                    unit: 'm', start: 2, verb: 'Set the width' },
      variants: [
        {
          "W": 2.4,
          "answer": 2.35,
          "miss": 2.4,
          "half": "0.05",
          "lb": "2.35",
          "ub": "2.45",
          "aTxt": "2.35",
          "mTxt": "2.40"
        },
        {
          "W": 2.6,
          "answer": 2.55,
          "miss": 2.6,
          "half": "0.05",
          "lb": "2.55",
          "ub": "2.65",
          "aTxt": "2.55",
          "mTxt": "2.60"
        },
        {
          "W": 2.2,
          "answer": 2.15,
          "miss": 2.2,
          "half": "0.05",
          "lb": "2.15",
          "ub": "2.25",
          "aTxt": "2.15",
          "mTxt": "2.20"
        },
        {
          "W": 2.8,
          "answer": 2.75,
          "miss": 2.8,
          "half": "0.05",
          "lb": "2.75",
          "ub": "2.85",
          "aTxt": "2.75",
          "mTxt": "2.80"
        },
        {
          "W": 2.5,
          "answer": 2.45,
          "miss": 2.5,
          "half": "0.05",
          "lb": "2.45",
          "ub": "2.55",
          "aTxt": "2.45",
          "mTxt": "2.50"
        },
        {
          "W": 2.7,
          "answer": 2.65,
          "miss": 2.7,
          "half": "0.05",
          "lb": "2.65",
          "ub": "2.75",
          "aTxt": "2.65",
          "mTxt": "2.70"
        },
        {
          "W": 2.9,
          "answer": 2.85,
          "miss": 2.9,
          "half": "0.05",
          "lb": "2.85",
          "ub": "2.95",
          "aTxt": "2.85",
          "mTxt": "2.90"
        },
        {
          "W": 2.3,
          "answer": 2.25,
          "miss": 2.3,
          "half": "0.05",
          "lb": "2.25",
          "ub": "2.35",
          "aTxt": "2.25",
          "mTxt": "2.30"
        }
      ],
      missTitle: '{{bay.mTxt}} m is the width on the sheet, not the smallest it allows.',
      missSays: 'The specification says {{bay.W}} m to the nearest ten centimetres, so any width from {{bay.lb}} m ' +
                'up to (but not reaching) {{bay.ub}} m would have been written down as {{bay.W}} m. {{bay.mTxt}} m ' +
                'is in the middle of that range. The marker wants the bottom of it.',
      hints: [
        '&ldquo;To the nearest ten centimetres&rdquo; is a range, not a number. What is the narrowest the bay could ' +
        'be and still be written down as {{bay.W}} m?',
        'Half of ten centimetres is five centimetres, which is {{bay.half}} m. A width that rounds to {{bay.W}} m ' +
        'can be up to {{bay.half}} m below it.',
        '{{bay.W}} &minus; {{bay.half}} = <b>{{bay.aTxt}} m</b>. That width really does round to {{bay.W}} m, so ' +
        'the specification allows it.'
      ],
      solve: 'To the nearest ten centimetres, {{bay.lb}} m &le; width &lt; {{bay.ub}} m. The smallest width allowed ' +
             'is <b>{{bay.aTxt}} m</b>.',
      onOpen: 'The marker trundles down the old line and lays a new one beside it, crisp and wet, exactly where the ' +
              'specification says. The bay next door has lost a little. Something in it is now sitting on a line.'
    },
    {
      id: 'boom-gate-sector',
      key: 'gate',
      name: 'The barrier',
      brief: 'Mr Strictman has changed the barrier&rsquo;s swing, so the arm comes down before a car is clear of ' +
             'it. The control box goes back to its proper setting only when it is given its calibration angle.',
      instrument: { kind: 'dial', label: 'Barrier swing angle', min: 0, max: 180, step: 5, decimals: 0,
                    unit: '°', start: 0, verb: 'Set the angle' },
      variants: [
        {
          "r": 3,
          "th": 45,
          "k": "0.75",
          "answer": 45,
          "miss": 90,
          "circ": 6,
          "frac": "1/8",
          "kpi": "0.75&pi;",
          "turns": 8
        },
        {
          "r": 7,
          "th": 90,
          "k": "3.5",
          "answer": 90,
          "miss": 180,
          "circ": 14,
          "frac": "1/4",
          "kpi": "3.5&pi;",
          "turns": 4
        },
        {
          "r": 3,
          "th": 15,
          "k": "0.25",
          "answer": 15,
          "miss": 30,
          "circ": 6,
          "frac": "1/24",
          "kpi": "0.25&pi;",
          "turns": 24
        },
        {
          "r": 3,
          "th": 60,
          "k": "1",
          "answer": 60,
          "miss": 120,
          "circ": 6,
          "frac": "1/6",
          "kpi": "&pi;",
          "turns": 6
        },
        {
          "r": 9,
          "th": 30,
          "k": "1.5",
          "answer": 30,
          "miss": 60,
          "circ": 18,
          "frac": "1/12",
          "kpi": "1.5&pi;",
          "turns": 12
        },
        {
          "r": 9,
          "th": 20,
          "k": "1",
          "answer": 20,
          "miss": 40,
          "circ": 18,
          "frac": "1/18",
          "kpi": "&pi;",
          "turns": 18
        },
        {
          "r": 9,
          "th": 10,
          "k": "0.5",
          "answer": 10,
          "miss": 20,
          "circ": 18,
          "frac": "1/36",
          "kpi": "0.5&pi;",
          "turns": 36
        },
        {
          "r": 9,
          "th": 40,
          "k": "2",
          "answer": 40,
          "miss": 80,
          "circ": 18,
          "frac": "1/9",
          "kpi": "2&pi;",
          "turns": 9
        }
      ],
      missTitle: '{{gate.miss}}&deg; is what you get from half the circumference.',
      missSays: 'That is the angle you land on if the circle round the pivot is worked out as &pi; &times; ' +
                '{{gate.r}} rather than 2 &times; &pi; &times; {{gate.r}}. Halving the circumference doubles the ' +
                'angle you need to cover the same arc, and the control box won&rsquo;t calibrate to it.',
      hints: [
        'The tip of the arm is not travelling in a straight line. It is going round a circle whose radius is the ' +
        'arm itself, and the angle is what fraction of that circle it covers.',
        'A full turn of the tip would be 2 &times; &pi; &times; {{gate.r}} = {{gate.circ}}&pi; metres. You want ' +
        '{{gate.kpi}} metres of it. The &pi; is on both sides, so it cancels.',
        '{{gate.kpi}} out of {{gate.circ}}&pi; is <sup>1</sup>&frasl;<sub>{{gate.turns}}</sub> of a full turn, so ' +
        'the angle is 360 &divide; {{gate.turns}} = <b>{{gate.th}}&deg;</b>.'
      ],
      solve: 'Full circumference = 2&pi; &times; {{gate.r}} = {{gate.circ}}&pi; m. The arc is {{gate.kpi}} m, which ' +
             'is <sup>1</sup>&frasl;<sub>{{gate.turns}}</sub> of the circle, so the angle is <b>{{gate.th}}&deg;</b>.',
      onOpen: 'The arm lifts, settles and stays up. A car could go under it now and come out the other side with ' +
              'both wing mirrors.'
    },
    {
      id: 'ev-charger-quadratic',
      key: 'amp',
      name: 'The charging post',
      brief: 'The Head&rsquo;s plug-in hybrid charges here, and Mr Strictman has set the post to trip the moment ' +
             'anything is plugged in. Take it back through commissioning: set a current that balances its load ' +
             'limiter and it goes back to normal. The circuit is also wired to the front office.',
      instrument: { kind: 'dial', label: 'Charging current', min: 0, max: 15, step: 1, decimals: 0,
                    unit: 'A', start: 0, verb: 'Set the current' },
      variants: [
        {
          "p": 5,
          "q": 7,
          "b": 12,
          "c": 35,
          "lim": 6,
          "answer": 5,
          "miss": 7
        },
        {
          "p": 4,
          "q": 6,
          "b": 10,
          "c": 24,
          "lim": 5,
          "answer": 4,
          "miss": 6
        },
        {
          "p": 8,
          "q": 12,
          "b": 20,
          "c": 96,
          "lim": 11,
          "answer": 8,
          "miss": 12
        },
        {
          "p": 3,
          "q": 9,
          "b": 12,
          "c": 27,
          "lim": 4,
          "answer": 3,
          "miss": 9
        },
        {
          "p": 7,
          "q": 11,
          "b": 18,
          "c": 77,
          "lim": 9,
          "answer": 7,
          "miss": 11
        },
        {
          "p": 6,
          "q": 10,
          "b": 16,
          "c": 60,
          "lim": 9,
          "answer": 6,
          "miss": 10
        },
        {
          "p": 9,
          "q": 11,
          "b": 20,
          "c": 99,
          "lim": 10,
          "answer": 9,
          "miss": 11
        },
        {
          "p": 10,
          "q": 12,
          "b": 22,
          "c": 120,
          "lim": 11,
          "answer": 10,
          "miss": 12
        }
      ],
      missTitle: '{{amp.miss}} A balances the limiter and brings the office down here.',
      missSays: 'Both {{amp.answer}} and {{amp.miss}} make the load zero, and the equation has no opinion about ' +
                'which one you use. The electrician&rsquo;s note does: {{amp.miss}} is above {{amp.lim}} A, so that ' +
                'root resets the post and sets the alarm off at the same time.',
      hints: [
        'Zero load does not mean zero current. It means solving the equation — and the biro note by the post is ' +
        'part of the puzzle, not scenery.',
        'x&sup2; &minus; {{amp.b}}x + {{amp.c}} factorises into two brackets: find two numbers that multiply to ' +
        '{{amp.c}} and add to {{amp.b}}.',
        '(x &minus; {{amp.answer}})(x &minus; {{amp.miss}}) = 0, so the load is zero at {{amp.answer}} A and at ' +
        '{{amp.miss}} A. Only <b>{{amp.answer}} A</b> is inside the {{amp.lim}} A limit.'
      ],
      solve: 'x&sup2; &minus; {{amp.b}}x + {{amp.c}} = (x &minus; {{amp.answer}})(x &minus; {{amp.miss}}), so x = ' +
             '{{amp.answer}} or {{amp.miss}}. The alarm limit of {{amp.lim}} A rules out {{amp.miss}}, leaving ' +
             '<b>{{amp.answer}} A</b>.',
      onOpen: 'The post clicks, thinks, and its light goes from red to a calm green. No alarm. When the Head plugs ' +
              'in, his car will charge without anyone noticing, which is how it does everything.'
    }
  ]
};
