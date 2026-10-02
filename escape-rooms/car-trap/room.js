/* Room data for "car-trap" — shared by index.html (the game) and
   teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand. */
window.ROOM = {
  slug: 'escape-car-trap',
  title: 'The Headteacher’s Car Trap',
  level: 'gcse',
  levelLabel: 'GCSE / Core Maths',
  minutes: 15,
  penalty: 45,
  art: 'car-trap',
  sceneAlt: 'An underground staff car park under strip lighting, early morning, with concrete pillars and puddles on the floor. Bays at the near end are cordoned off with red and white tape between posts, and a folding stand beside them carries a sign reading RESERVED. A yellow line-painting robot sits to the left with its control panel hinged open. An electric vehicle charging post stands part way along the row with its cable hanging from it, a boom barrier waits at the foot of the entrance ramp with daylight beyond, and VISITOR is painted in worn white letters on the floor by the lift doors.',
  failAlt: 'An underground school car park in the rain. A gleaming orange electric sports car is parked across the cordoned bays at a slight angle, not a mark on it, with a folding stand beside it carrying a sign that reads HEADTEACHER. Through the ramp opening behind, a school minibus has been shoved out onto a muddy grass verge. Staff in coats file past towards the lift without looking at it, carrying bags and a box of exercise books.',
  winAlt: 'An underground school car park under cold strip lighting. A bright orange electric sports car is halfway through reversing into a visitor bay plainly shorter than the car — a small white box on the wet concrete with VISITOR stencilled in it — sitting well out of square with its reversing lights on, curved tyre scuffs behind it from the earlier attempts. The yellow line-painting robot is parked beside its work, the charging post shows a small red light, and the barrier arm is down immediately behind the boot. A dozen staff in coats have stopped on their way to the lift to watch, none of them laughing.',

  hook: 'The Headteacher has bought an electric sports car. It is the colour of a boiled sweet, it makes no noise ' +
        'at all, and three bays by the lift have been repainted, taped off and labelled for it — the three the ' +
        'minibus used to use. He arrives at ten past eight.',
  brief: 'Fifteen minutes in the car park before he comes down the ramp. The bay is not painted yet, the barrier ' +
         'takes its swing angle from a panel on the wall, and the charging post is still in commissioning mode. ' +
         'Leave him exactly one place to put it.',
  stakes: 'Get this wrong and he parks, beautifully, across all three bays. The minibus stays on the verge, the ' +
          'reserved sign goes from laminated to engraved, and at Monday&rsquo;s briefing there is a slide about ' +
          'respecting the new arrangements in the car park.',
  win: 'The bot lays out a bay that a shopping trolley would find tight. The barrier comes down just close enough ' +
       'to fold his wing mirror in for him. The charger declines, politely, in a voice designed to sound reassuring. ' +
       'He reverses into the visitor space over four attempts, with an audience, and walks in carrying his bag in ' +
       'front of him like a shield.',

  objects: [
    { id: 'spec', name: 'The bay specification', where: 'on a clipboard hooked to the taped-off stand',
      clue: '<b>VIP BAY — to be laid this morning.</b> Length <b>{{bay.L}} m</b>, width <b>{{bay.W}} m</b>, each ' +
            'measured to the nearest metre. Contractor to paint to specification.' },
    { id: 'botcard', name: 'Instruction card on the painting bot', where: 'slotted into the open control panel',
      clue: '&ldquo;The bot lays <b>one square metre per litre</b> and will refuse any figure below what the ' +
            'specification permits. Give it the <b>smallest area the specification still allows</b> and it will ' +
            'paint that, and log it as compliant.&rdquo;' },
    { id: 'maintlog', name: 'Barrier maintenance log', where: 'in a plastic wallet zip-tied to the barrier post',
      clue: 'BOOM ARM: <b>{{gate.r}} m</b> from pivot to tip. Counterweight checked. Arm replaced last term after ' +
            'the incident with the fish van.' },
    { id: 'sensor', name: 'Collision sensor fault sheet', where: 'taped inside the barrier control box',
      clue: '&ldquo;Error 12 latches when the <b>tip of the arm travels an arc of exactly {{gate.kpi}} metres</b>. ' +
            'The sensor watches how far the tip travels, not how high the arm lifts.&rdquo;' },
    { id: 'commission', name: 'Charger commissioning label', where: 'stuck inside the charging post cover',
      clue: 'LOAD LIMITER: <b>L(x) = x&sup2; &minus; {{amp.b}}x + {{amp.c}}</b>, for a charging current of x amps. ' +
            '<b>The bay unlocks at zero load.</b>' },
    { id: 'alarmnote', name: 'Note from the site electrician', where: 'biro on the back of a delivery slip',
      clue: '&ldquo;Anything <b>above {{amp.lim}} A</b> on that circuit and the network alarm goes off in the front ' +
            'office. It has done it twice this term and they blame me both times.&rdquo;' },
    { id: 'cone', name: 'A traffic cone', where: 'on its side by the ramp', clue: null,
      flavour: 'Someone has written a name on it in marker and someone else has scribbled it out. Under the cone: ' +
               'the floor of a car park.' },
    { id: 'trolley', name: 'A supermarket trolley', where: 'wedged behind the pillar', clue: null,
      flavour: 'It has been there since before any of you started at this school. It contains a hi-vis tabard, one ' +
               'glove, and about &pound;1.40 in change that nobody has ever felt brave enough to take.' }
  ],

  locks: [
    {
      id: 'visitor-space-bounds',
      key: 'bay',
      name: 'The line-painting bot',
      art: 'carpark-visitor-space-bounds',
      artAlt: 'Close on a yellow line-painting robot in an underground car park, its control panel hinged open to show a blank readout labelled litres beside a plain round setting knob with no pointer on it. The taped-off bays, the barrier and the lift doors sit behind it.',
      brief: 'The bot takes a paint volume and lays out a bay of exactly that many square metres. Ask it for less ' +
             'than the specification permits and it refuses; ask it for the least the specification permits and it ' +
             'gets to work.',
      instrument: { kind: 'dial', label: 'Paint volume', min: 0, max: 20, step: 0.25, decimals: 2,
                    unit: 'litres', start: 0, verb: 'Set the volume' },
      variants: [
        {
          "L": 6,
          "W": 3,
          "answer": 13.75,
          "miss": 18.0,
          "lbL": "5.5",
          "lbW": "2.5",
          "aTxt": "13.75",
          "mTxt": "18.00"
        },
        {
          "L": 4,
          "W": 2,
          "answer": 5.25,
          "miss": 8.0,
          "lbL": "3.5",
          "lbW": "1.5",
          "aTxt": "5.25",
          "mTxt": "8.00"
        },
        {
          "L": 3,
          "W": 3,
          "answer": 6.25,
          "miss": 9.0,
          "lbL": "2.5",
          "lbW": "2.5",
          "aTxt": "6.25",
          "mTxt": "9.00"
        },
        {
          "L": 4,
          "W": 4,
          "answer": 12.25,
          "miss": 16.0,
          "lbL": "3.5",
          "lbW": "3.5",
          "aTxt": "12.25",
          "mTxt": "16.00"
        },
        {
          "L": 5,
          "W": 4,
          "answer": 15.75,
          "miss": 20.0,
          "lbL": "4.5",
          "lbW": "3.5",
          "aTxt": "15.75",
          "mTxt": "20.00"
        },
        {
          "L": 3,
          "W": 2,
          "answer": 3.75,
          "miss": 6.0,
          "lbL": "2.5",
          "lbW": "1.5",
          "aTxt": "3.75",
          "mTxt": "6.00"
        },
        {
          "L": 5,
          "W": 3,
          "answer": 11.25,
          "miss": 15.0,
          "lbL": "4.5",
          "lbW": "2.5",
          "aTxt": "11.25",
          "mTxt": "15.00"
        },
        {
          "L": 4,
          "W": 3,
          "answer": 8.75,
          "miss": 12.0,
          "lbL": "3.5",
          "lbW": "2.5",
          "aTxt": "8.75",
          "mTxt": "12.00"
        },
        {
          "L": 7,
          "W": 2,
          "answer": 9.75,
          "miss": 14.0,
          "lbL": "6.5",
          "lbW": "1.5",
          "aTxt": "9.75",
          "mTxt": "14.00"
        }
      ],
      missTitle: '{{bay.mTxt}} litres is {{bay.L}} &times; {{bay.W}} with the bounds never opened.',
      missSays: 'A length given to the nearest metre is not {{bay.L}} m — it is anything from {{bay.lbL}} m ' +
                'upwards. Multiplying the stated figures gives a bay in the middle of what the specification ' +
                'allows, not at the bottom of it, and he will park in that one without noticing.',
      hints: [
        '&ldquo;To the nearest metre&rdquo; is a range, not a number. What is the shortest the length could ' +
        'actually be and still round to {{bay.L}} m?',
        'The length is at least {{bay.lbL}} m and the width at least {{bay.lbW}} m. The smallest area comes from ' +
        'the smallest of each — and an area is a product, not a sum.',
        '{{bay.lbL}} &times; {{bay.lbW}} = <b>{{bay.aTxt}}</b> square metres, and the bot wants one litre per ' +
        'square metre.'
      ],
      solve: 'Lower bounds of {{bay.lbL}} m and {{bay.lbW}} m multiply to <b>{{bay.aTxt}} m&sup2;</b>, so the dial ' +
             'goes to <b>{{bay.aTxt}} litres</b>.',
      onOpen: 'The bot sets off, turns four crisp corners, and produces a parking bay of impeccable legality that ' +
              'a milk float would struggle to get into.'
    },
    {
      id: 'boom-gate-sector',
      key: 'gate',
      name: 'The boom gate',
      art: 'carpark-boom-gate-sector',
      artAlt: 'The pivot end of a red and white boom barrier at the foot of a car park ramp, its grey control box hinged open beside it. Inside, among coiled wiring, a bare circular dial face with tick graduations round the edge and a centre pivot boss carrying no needle or pointer.',
      brief: 'The barrier takes its swing angle from this panel. High enough and a car goes under untouched; at one ' +
             'particular angle the tip of the arm passes through the space a wing mirror is about to occupy.',
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
                'angle you need to cover the same arc — and at {{gate.miss}}&deg; the arm is well clear of the car.',
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
      onOpen: 'The barrier drops to the new angle and stops there, at precisely the height of something expensive.'
    },
    {
      id: 'ev-charger-quadratic',
      key: 'amp',
      name: 'The charging post',
      art: 'carpark-ev-charger-quadratic',
      artAlt: 'An electric vehicle charging post in an underground car park with its cover hinged open. Inside, a blank display with a small A beside it and, below that, a bare knurled setting ring with no pointer or index mark on it. A blank white label is taped inside the open cover and the charging cable hangs coiled on a hook at the side.',
      brief: 'The post is still in commissioning mode: set a current that balances its load limiter and it hands ' +
             'the bay over to you. The circuit is also wired to the front office.',
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
      missSays: 'Both {{amp.answer}} and {{amp.miss}} make the load zero — the equation has no opinion about which ' +
                'one you use. The electrician&rsquo;s note does: {{amp.miss}} is above {{amp.lim}} A, so that root ' +
                'unlocks the bay and sets the alarm off at the same time.',
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
      onOpen: 'The post accepts it, thinks, and reassigns the bay to VISITOR. No alarm. Somewhere above you, a ' +
              'kettle in the front office carries on boiling.'
    }
  ]
};
