/* Room data for "rugby-mud" — shared by index.html (the game) and
   teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand.

   VOICE REWRITE, 15/09/2026. Antagonist: Mr Mower, the groundskeeper. He
   loves his grass, would keep every child off every pitch if he could, and
   dreams of a medal at the Chelsea Flower Show. Mr Lunge (Head of P.E., who
   speaks only in pe-shed-rebellion) ordered the pitch kept dry after parents'
   letters about muddy kit; Mower does as he is told, and this is the one order
   he has ever been glad of. Lunge is named offstage as the cause and has NO
   spoken lines here — keep it that way. Mower's voice is overheard through the
   hut window, costing up a rare-grass order for his home lawn. Not a phone
   call: prom-budget already owns the overheard call.

   Load-bearing, do not tidy out:
   - The brief's "a rugby pitch is for playing rugby on" is the answer to "why
     is this not sabotage". The students restore a pitch to what it is for.
     Retitled from The Rugby Mud Sabotage for the same reason; slug unchanged.
   - Set THE AFTERNOON BEFORE. A pitch cannot be soaked in fifteen minutes, and
     a soaked pitch cannot be recovered in a day.
   - Mower is OUT the next day until just before kick-off, collecting the grass
     he orders in `wrongLines`. This is what keeps every draw coherent: the tap
     timer answers run 4 to 24 HOURS from about 3:40, so on the long draws the
     taps are still running the next morning, and a Mower on site would simply
     turn them off. Do not put him back on site the next morning, and do not
     put a clock time on when the drains were beaten.
   - One scale throughout: a "full soaking". His log, the timer and the
     referee's threshold are all measured in it. Short of one soaking the drains
     win; over it the pitch is waterlogged and the referee calls the match off,
     which is Mower's ideal outcome. The flow lock's dial is labelled TAP timer,
     not flood timer, because flooding is now the failure.
   - He sees his defeat from the touchline. Not a never-knew ending.
   - No brand names: the three gadgets came in "one padded envelope".

   Protected lock text changed deliberately, no number moved (Jon, 15/09):
   flow lock instrument label ("Flood timer" -> "Tap timer") and unit
   (min -> h), missSays, all three hints and solve (minutes -> hours, valves ->
   taps, pitch -> soaking); scoreboard lock hints[1] (pointed at "the slip in
   the cabinet", an object that no longer exists); and on Jon's ask, every
   caret power on the scoreboard lock (clue, missTitle, missSays, hints[1],
   solve, plus teacher.html's clueMap label) now renders as <sup> — notation
   only, same indices. All instrument art dropped.

   ART COMPLETE 15/09/2026, all three in the new style at 1600x873, all alts
   written against what is on disk. Win is Jon's `Rugby Open.jpg`, edited to
   take brand stripes off the boots; fail is an edit of that picture, so the
   two share one camera. The scene's tap timer carries a few scribbled marks on
   its face, left on Jon's call: at 1600px it is about 25px across and
   unreadable. Prompts in docs/escape-room-image-prompts.md.

   NOTE — object `id`s are load-bearing: teacher.html maps clues to locks by id
   in its `clueMap`. They still carry the old names (jacket, teamsheet, slip);
   renaming one silently breaks the teacher page. */
window.ROOM = {
  slug: 'escape-rugby-mud',
  title: 'The Rugby Mud Bath',
  level: 'gcse',
  levelLabel: 'GCSE',
  minutes: 15,
  penalty: 45,
  art: 'rugby-mud',
  sceneAlt: 'The side of a wooden groundsman’s hut at the edge of a school rugby pitch, in low, warm late-afternoon sun. A seed catalogue lies open on the hut’s counter with a pencil beside it, and a torn padded envelope sits on the wooden step. Against the wall, two brass taps stand inside a wire-mesh cage with a padlock on its door and a small timer fixed to one tap. Two hoses run from the taps across a gravel path, one leaking from a split. Beyond a white gate with a blank board on it, the pitch lies perfectly striped and dry, with the posts and corner flags far off.',
  failAlt: 'The view out of a changing-room doorway onto a school rugby pitch on a bright day with a few small clouds. The peeling steel door stands open and beyond the step the pitch is perfect: mown in pale and dark stripes, flat and dry, the white lines crisp and the posts standing at the far end. Not a puddle anywhere. A pair of spotless white rugby boots sits by a wooden bench just inside the door.',
  winAlt: 'The view out of a changing-room doorway onto a school rugby pitch under a flat grey sky. The steel door stands open, its paint peeling, and beyond the step the pitch is churned brown mud from end to end, with water standing in the ruts and the white lines barely showing. The posts stand at the far end. A pair of plain, muddy rugby boots sits by a wooden bench just inside the door.',

  hook: 'Tomorrow at four the Year 9 mixed team play at home, and the pitch is perfect. Not good. Perfect. ' +
        'Striped, rolled, cut to a height Mr Mower checks with a ruler, and as dry as a carpet.<br><br>' +
        'Because there have been letters. Kit going home with three inches of mud on it after every match, and ' +
        'parents who have had enough of the washing machine. So Mr Lunge has told the groundskeeper to keep that ' +
        'pitch dry &mdash; the same Mr Lunge who once told a Year 7 that sideways hail builds character, and who ' +
        'folded after four letters.<br><br>' +
        'Mr Mower has never been so pleased to be told anything.',
  brief: 'Half past three, the afternoon before. In fifteen minutes Mr Mower locks his hut and walks his rounds, and ' +
         'his rounds end at the taps. Right now he is at the hut counter with a seed catalogue, costing up an order ' +
         'he is collecting in person tomorrow, and he will not be back until just before kick-off. He is not looking ' +
         'out of the window. The team play better in mud, the girls most of all, and a rugby pitch is for playing ' +
         'rugby on. It is not a lawn, whatever he has decided. Two taps feed that pitch. Patch the split in the ' +
         'reserve hose, get his padlock off the tap cage, and set the timer to put exactly one full soaking on the ' +
         'pitch before tomorrow &mdash; enough to beat his drains, not so much that the referee calls it off. ' +
         'Everything he bought to stop you came in one padded envelope, and the budget did not stretch to reading ' +
         'the instructions.',
  stakes: 'At quarter to four the hut door opens. He walks his rounds and turns both taps off without breaking ' +
          'stride. Tomorrow the Year 9s play on a pitch like a snooker table, the kit goes home clean, and nobody ' +
          'gets a single slide.',
  win: 'Mr Mower is out all the next day, collecting two kilos of velvet bent from a nursery three counties away, ' +
       'and he gets back with twenty minutes to spare. By then it is far too late. The drains he dug himself were ' +
       'beaten in the night, the stripes have gone, and so has the ruler-height cut. There is no standing water. ' +
       'The referee walks the pitch, presses a boot into it and calls it fit, which from where Mr Mower is standing ' +
       'is worse than a flood.<br><br>' +
       'The first try is a slide from the twenty-two, and it is one of the girls. By half-time both teams are the ' +
       'same colour. By the end nobody can tell who is playing for which side, including, at one point, the ' +
       'players. The Year 9s win again, by a margin the referee works out partly by counting heads.<br><br>' +
       'Mr Mower watches all of it from the touchline with the bag of seed under his arm. He says nothing until ' +
       'the final whistle. Then, very quietly: &ldquo;Chelsea&rsquo;s in May.&rdquo;',

  /* Wrong-entry lines, indexed by how many wrong settings have been made so
     far; the last one repeats. Mower at the hut counter, costing his home-lawn
     order out loud to nobody. Velvet bent and chewings fescue are real
     fine-lawn grasses. Line four repeats, and the total only ever goes up. */
  wrongLines: [
    { head: 'Nothing gives.',
      body: 'Through the hut window, to nobody: &ldquo;Velvet bent. Finest leaf in the country. Wouldn&rsquo;t ' +
            'have it on a school pitch. Wouldn&rsquo;t waste it.&rdquo;' },
    { head: 'The setting slides back to where it was.',
      body: '&ldquo;Forty grams a square metre&hellip; call it two kilos with the edges. Hand-sown. Obviously ' +
            'hand-sown.&rdquo;' },
    { head: 'Something resets itself with a click.',
      body: '&ldquo;Chewings fescue for the shady side. It&rsquo;s not a lawn, that. It&rsquo;s a <i>sward</i>. ' +
            'The judges know the difference.&rdquo;' },
    { head: 'Another one. Nothing has moved.',
      body: 'Through the window, he crosses the total out and writes a bigger one.' }
  ],

  objects: [
    { id: 'jacket', name: 'Repair kit card', where: 'in the torn padded envelope on the hut step',
      clue: '&ldquo;HOSE MENDING PATCH. Sample patch <b>length {{patch.L1}} cm, area {{patch.A1}} square ' +
            'centimetre</b>. Cutter cut any size, same shape. Very strong!&rdquo;' },
    { id: 'hose', name: 'The reserve hose', where: 'lying across the path from the tap',
      clue: 'The split is <b>exactly the shape of the kit’s sample patch</b>, only smaller: <b>{{patch.L2}} cm ' +
            'long</b>. A patch bigger than the split puckers and lets go in the night. A smaller one will not cover it.' },
    { id: 'board', name: 'Mr Mower’s watering log', where: 'on a nail inside the tap cage',
      clue: 'DROUGHT, AUGUST. &ldquo;One full soaking of the pitch. <b>Main tap alone, {{flow.a}} hours. Reserve ' +
            'tap alone, {{flow.b}} hours.</b> Never both together. Never outside a drought.&rdquo;' },
    { id: 'addendum', name: 'Tap timer card', where: 'cable-tied to the timer',
      clue: '&ldquo;<b>BOTH TAP OPEN.</b> Set timer for time of job. Timer close both tap when job is finish. ' +
            'Not before! Not after!&rdquo;' },
    { id: 'teamsheet', name: 'Pencil on the hut wall', where: 'by the light switch, in careful capitals',
      clue: 'PADLOCK &mdash; AS PER INSTRUCTIONS &mdash; SECRET POWER SUM: <b>2<sup>H</sup> &times; 4<sup>A</sup> = ' +
            '2<sup>{{score.N}}</sup></b>. Underlined twice.' },
    { id: 'slip', name: 'Framed newsletter cutting', where: 'above the hut counter',
      clue: 'The only match the Year 9s have lost in two seasons, played at home the day after his new drainage ' +
            'went in. <b>The visitors beat St Martha’s by exactly {{score.diff}}.</b> Underneath, in pencil: ' +
            '&ldquo;Not a mark on the grass.&rdquo;' },
    { id: 'flag', name: 'Corner flag', where: 'at the twenty-two', clue: null,
      flavour: 'Perfectly upright. There is a pencil mark on the post where he checks it with a spirit level. Daily.' },
    { id: 'skip', name: 'The gate sign', where: 'on the gate to the pitch', clue: null,
      flavour: 'KEEP OFF THE GRASS, on a rugby pitch. The P.E. department have painted over it twice. It has been ' +
               'repainted by hand, twice.' }
  ],

  locks: [
    {
      id: 'elbow-patch-scale',
      key: 'patch',
      name: 'The split hose',
      brief: 'The kit’s cutter takes an area and cuts a patch the same shape as its sample. Give it exactly the area ' +
             'of the split. Too big and it puckers and lets go at two in the morning; too small and it does not ' +
             'cover it. The reserve tap is no use to anyone with a hole in its hose.',
      instrument: { kind: 'dial', label: 'Fabric cutter — area', min: 1, max: 100, step: 1, decimals: 0,
                    unit: 'cm²', start: 1, verb: 'Set the cutter' },
      variants: [
        {
          "L1": 15,
          "A1": 90,
          "L2": 5,
          "k": 3,
          "answer": 10,
          "miss": 30,
          "k2": 9
        },
        {
          "L1": 10,
          "A1": 60,
          "L2": 5,
          "k": 2,
          "answer": 15,
          "miss": 30,
          "k2": 4
        },
        {
          "L1": 28,
          "A1": 84,
          "L2": 14,
          "k": 2,
          "answer": 21,
          "miss": 42,
          "k2": 4
        },
        {
          "L1": 28,
          "A1": 100,
          "L2": 14,
          "k": 2,
          "answer": 25,
          "miss": 50,
          "k2": 4
        },
        {
          "L1": 8,
          "A1": 80,
          "L2": 2,
          "k": 4,
          "answer": 5,
          "miss": 20,
          "k2": 16
        }
      ],
      missTitle: '{{patch.miss}} divides by the length scale factor.',
      missSays: '{{patch.A1}} &divide; {{patch.k}} = {{patch.miss}} uses the <i>length</i> scale factor on an ' +
                '<i>area</i>. Halve the length of a shape and you quarter its area; make it ' +
                '<sup>1</sup>&frasl;<sub>{{patch.k}}</sub> as long and you get ' +
                '<sup>1</sup>&frasl;<sub>{{patch.k2}}</sub> of the area.',
      hints: [
        'The split is <sup>1</sup>&frasl;<sub>{{patch.k}}</sub> of the length of the patch. That does not make it ' +
        '<sup>1</sup>&frasl;<sub>{{patch.k}}</sub> of the area — think about what happens to a square when you make ' +
        'its side shorter.',
        'If lengths scale by k, areas scale by k&sup2;. Here k = {{patch.L2}} &divide; {{patch.L1}} = ' +
        '<sup>1</sup>&frasl;<sub>{{patch.k}}</sub>, so the area scale factor is that squared.',
        'Length scale factor <sup>1</sup>&frasl;<sub>{{patch.k}}</sub>, so area scale factor ' +
        '<sup>1</sup>&frasl;<sub>{{patch.k2}}</sub>. {{patch.A1}} &divide; {{patch.k2}} = ' +
        '<b>{{patch.answer}} cm&sup2;</b>.'
      ],
      solve: 'Length s.f. = {{patch.L2}}/{{patch.L1}}, so area s.f. is that squared. {{patch.A1}} &divide; ' +
             '{{patch.k2}} = <b>{{patch.answer}} cm&sup2;</b>.',
      onOpen: 'The patch goes on flat and holds. The hose now looks like a hose that has never had anything wrong ' +
              'with it.'
    },
    {
      id: 'sprinkler-flow-rates',
      key: 'flow',
      name: 'The tap timer',
      brief: 'Both taps open, and the cheap timer shuts them both off when it runs out. Set it to how long the two ' +
             'together take to put one full soaking on the pitch. Short of that and his drains have it dry by ' +
             'kick-off. Over it and the pitch is under water, the referee calls the match off, and Mr Mower gets his ' +
             'grass back without a game played on it.',
      instrument: { kind: 'dial', label: 'Tap timer', min: 1, max: 60, step: 1, decimals: 0,
                    unit: 'h', start: 1, verb: 'Set the timer' },
      variants: [
        {
          "a": 20,
          "b": 30,
          "answer": 12,
          "miss": 25
        },
        {
          "a": 30,
          "b": 70,
          "answer": 21,
          "miss": 50
        },
        {
          "a": 12,
          "b": 60,
          "answer": 10,
          "miss": 36
        },
        {
          "a": 40,
          "b": 60,
          "answer": 24,
          "miss": 50
        },
        {
          "a": 8,
          "b": 24,
          "answer": 6,
          "miss": 16
        },
        {
          "a": 20,
          "b": 80,
          "answer": 16,
          "miss": 50
        },
        {
          "a": 6,
          "b": 12,
          "answer": 4,
          "miss": 9
        },
        {
          "a": 24,
          "b": 72,
          "answer": 18,
          "miss": 48
        },
        {
          "a": 12,
          "b": 24,
          "answer": 8,
          "miss": 18
        }
      ],
      missTitle: '{{flow.miss}} is the average of the two times.',
      missSays: 'Two taps running together cannot possibly be slower than the faster one on its own — and ' +
                '{{flow.miss}} is slower than {{flow.a}}. Times do not average and they do not add. <i>Rates</i> ' +
                'add: work out what fraction of a soaking each tap puts on in one hour.',
      hints: [
        'Sanity check first: both taps open must beat {{flow.a}} hours. Whatever you set has to be less than that.',
        'Work in soakings per hour. The main tap puts on <sup>1</sup>&frasl;<sub>{{flow.a}}</sub> of a soaking an ' +
        'hour, the reserve <sup>1</sup>&frasl;<sub>{{flow.b}}</sub>. Add those two rates, then see how long one ' +
        'whole soaking takes at that combined rate.',
        '<sup>1</sup>&frasl;<sub>{{flow.a}}</sub> + <sup>1</sup>&frasl;<sub>{{flow.b}}</sub> comes to ' +
        '<sup>1</sup>&frasl;<sub>{{flow.answer}}</sub> of a soaking an hour, so one whole soaking takes ' +
        '<b>{{flow.answer}} hours</b>.'
      ],
      solve: 'Rates add: 1/{{flow.a}} + 1/{{flow.b}} = 1/{{flow.answer}} of a soaking an hour, so one full soaking ' +
             'takes <b>{{flow.answer}} hours</b>.',
      onOpen: 'Both taps go over together. Nothing much happens, which is the point. Somewhere under all that ' +
              'stripe, very slowly, the pitch starts to stop being a pitch.'
    },
    {
      id: 'rugby-scoreboard-bases',
      key: 'score',
      name: 'The tap-cage padlock',
      brief: 'Two dials, which the translation on the packet has labelled HOME and AWAY. Mr Mower has set them to the ' +
             'score of his favourite match, and the instructions told him to write the code down as a secret power ' +
             'sum so that no thief would understand it. He did exactly as he was told. Both dials.',
      instrument: { kind: 'pair', label: 'Predicted result', verb: 'Set both dials',
        a: { kind: 'dial', label: 'Home', min: 0, max: 100, step: 1, decimals: 0, unit: '', start: 0 },
        b: { kind: 'dial', label: 'Away', min: 0, max: 100, step: 1, decimals: 0, unit: '', start: 0 } },
      variants: [
        {
          "N": 17,
          "diff": 4,
          "H": 3,
          "A": 7,
          "missH": 13,
          "missA": 17,
          "answer": [
            3,
            7
          ],
          "miss": [
            13,
            17
          ]
        },
        {
          "N": 11,
          "diff": 4,
          "H": 1,
          "A": 5,
          "missH": 7,
          "missA": 11,
          "answer": [
            1,
            5
          ],
          "miss": [
            7,
            11
          ]
        },
        {
          "N": 12,
          "diff": 3,
          "H": 2,
          "A": 5,
          "missH": 9,
          "missA": 12,
          "answer": [
            2,
            5
          ],
          "miss": [
            9,
            12
          ]
        },
        {
          "N": 13,
          "diff": 2,
          "H": 3,
          "A": 5,
          "missH": 11,
          "missA": 13,
          "answer": [
            3,
            5
          ],
          "miss": [
            11,
            13
          ]
        },
        {
          "N": 13,
          "diff": 5,
          "H": 1,
          "A": 6,
          "missH": 8,
          "missA": 13,
          "answer": [
            1,
            6
          ],
          "miss": [
            8,
            13
          ]
        },
        {
          "N": 14,
          "diff": 4,
          "H": 2,
          "A": 6,
          "missH": 10,
          "missA": 14,
          "answer": [
            2,
            6
          ],
          "miss": [
            10,
            14
          ]
        },
        {
          "N": 15,
          "diff": 3,
          "H": 3,
          "A": 6,
          "missH": 12,
          "missA": 15,
          "answer": [
            3,
            6
          ],
          "miss": [
            12,
            15
          ]
        },
        {
          "N": 15,
          "diff": 6,
          "H": 1,
          "A": 7,
          "missH": 9,
          "missA": 15,
          "answer": [
            1,
            7
          ],
          "miss": [
            9,
            15
          ]
        },
        {
          "N": 16,
          "diff": 2,
          "H": 4,
          "A": 6,
          "missH": 14,
          "missA": 16,
          "answer": [
            4,
            6
          ],
          "miss": [
            14,
            16
          ]
        },
        {
          "N": 16,
          "diff": 5,
          "H": 2,
          "A": 7,
          "missH": 11,
          "missA": 16,
          "answer": [
            2,
            7
          ],
          "miss": [
            11,
            16
          ]
        }
      ],
      missTitle: 'Home {{score.missH}}, Away {{score.missA}} — that reads 4<sup>A</sup> as 2<sup>A</sup>.',
      missSays: 'Taking A straight from the {{score.N}} in 2<sup>{{score.N}}</sup> assumes both terms are already powers of 2 ' +
                'with the index written in. They are not: 4 = 2<sup>2</sup>, so 4<sup>A</sup> is 2<sup>2A</sup> and A counts <b>twice</b> in ' +
                'the index. The equation is H + 2A = {{score.N}}.',
      hints: [
        'Everything on the left of that equation can be written as a power of the same base. Do that first and the ' +
        'indices will do the rest of the work for you.',
        '4 = 2<sup>2</sup>, so 4<sup>A</sup> = 2<sup>2A</sup>, and 2<sup>H</sup> &times; 2<sup>2A</sup> = 2<sup>H + 2A</sup>. Powers of the same base are equal only ' +
        'when the indices are equal, so H + 2A = {{score.N}}. The cutting above the hut counter gives you the second equation.',
        'H + 2A = {{score.N}} and A = H + {{score.diff}}. Substituting: H + 2(H + {{score.diff}}) = {{score.N}}, so ' +
        '3H = {{score.N}} &minus; {{score.diff}} &minus; {{score.diff}}, giving <b>H = {{score.H}}</b> and ' +
        '<b>A = {{score.A}}</b>.'
      ],
      solve: '2<sup>H</sup> &times; 4<sup>A</sup> = 2<sup>H+2A</sup> = 2<sup>{{score.N}}</sup>, so H + 2A = {{score.N}}, with A = H + {{score.diff}}. ' +
             'That gives <b>Home {{score.H}}, Away {{score.A}}</b>.',
      onOpen: 'The padlock lets go of the cage first time. For what it cost, it was very nearly a lock.'
    }
  ]
};
