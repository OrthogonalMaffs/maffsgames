/* Room data for "kiln-disaster" — shared by index.html (the game) and
   teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand. The locks are
   batch 7 of the audited bank (docs/lock-bank-batch7.txt).

   BUILT 2026-09-17 for a GCSE resit class (grade 3/4). Five clue-carrying
   objects and three blanks; the sensor lock and the fan lock each take their
   two figures from two different objects.

   NOTE — object `id`s are load-bearing: teacher.html maps clues to locks by id
   in its `clueMap`. Renaming one silently breaks the teacher page.

   NOTE — not one numeral is typed into a clue string. The engine counts every
   figure a student reads in a clue when it decides which joint draws are VALID
   (see scripts/check-escape-rooms.py), so a literal number here would collide
   with another lock's figures and cut the number of draws the room can serve.

   ART: scene, fail and win filed 2026-09-17, all from one viewpoint. The scene
   was re-rolled for palette — the first take was warm cream against the cool
   grey of the other two. The alts below were approved by Jon against those
   three pictures.

   RULE — the fail picture shows the suppression system already fired, which is
   only true at time-out. Never set `missArt` on any lock in this room: the
   engine shows the fail picture beside a misconception response only when that
   flag is set. */
window.ROOM = {
  slug: 'escape-kiln-disaster',
  title: 'The Kiln Disaster',
  level: 'gcse',
  levelLabel: 'GCSE',
  minutes: 15,
  penalty: 45,
  art: 'kiln-disaster',
  sceneAlt: 'An empty art room at the end of the day. An old top-loading kiln stands against the back wall, its lid clamped shut and scorched around the rim, with a newer grey control box and a red emergency stop bolted to the wall beside it. A stack of banded portfolios sits on the floor alongside.',
  failAlt: 'The art room floor under foam. The emergency stop is pushed in, and the portfolios are sitting in it, soaked through.',
  winAlt: 'The kiln stands open and cold, the controller dark. The portfolios are laid out dry on a table, still tied shut.',

  hook: 'Mr Stephen Mudge teaches Art. He has been Smudgey since about his first week, and he gave up ' +
        'correcting it long ago. Smudgey was clearing the tables and put the portfolios down on the kiln ' +
        'shelf, the way anyone would. Then he nudged the lid shut on his way past.',
  brief: 'The kiln was already loaded and already programmed. It was only waiting for the lid. Now the countdown ' +
         'is running, your portfolios are inside, and the only safe way to stop it is the cancel code. Three ' +
         'locks on the controller, and IT left their paperwork all over the room.',
  stakes: 'Smudgey hits the emergency stop. &ldquo;Soggy we can dry out. Ash we can&rsquo;t.&rdquo;',
  win: 'The controller beeps twice and the countdown clears. The lid comes up. Cold clay, and every portfolio dry.',

  /* Wrong-entry lines, indexed by how many wrong settings have been made so
     far; the last one repeats. Smudgey, working out what his subject is made
     of while the kiln counts down. */
  wrongLines: [
    { head: 'Smudgey leans over your shoulder.',
      body: '&ldquo;Don&rsquo;t focus on the details. Does it feel like the right answer?&rdquo;' },
    { head: 'He&rsquo;s found a whiteboard pen.',
      body: '&ldquo;Seurat painted with dots. Thousands of them, in neat rows. Same number in every row&hellip; ' +
            'hang on, isn&rsquo;t that just times tables?&rdquo;' },
    { head: 'He&rsquo;s drawing lines across the whiteboard.',
      body: '&ldquo;Every perspective drawing starts with a vanishing point and a ruler. I&rsquo;ve taught that ' +
            'for years. That&rsquo;s&hellip; geometry, isn&rsquo;t it? Nobody told me.&rdquo;' },
    { head: 'The kiln hums louder. His hand hovers near the red button.',
      body: '&ldquo;Escher fitted lizards across a whole page without a single gap. Oh no. Oh no, it&rsquo;s been ' +
            'maths the whole time.&rdquo;' }
  ],

  objects: [
    { id: 'asset-tag', name: 'Asset tag', where: 'Stuck to the side of the controller',
      clue: 'A printed tag from the install. <b>AUXILIARY SENSOR IDs ARE MULTIPLES OF {{sl.k}}</b>' },
    { id: 'cable-label', name: 'Cable label', where: 'Wrapped round the data cable',
      clue: 'A flag of tape round the cable, written on in marker. <b>MAXIMUM ID {{sl.L}}</b>' },
    { id: 'install-sheet', name: 'Installation sheet', where: 'Folded behind the controller',
      clue: 'A commissioning sheet, folded in half. <b>INTAKE FAN CYCLE {{fr.a}} MIN</b>' },
    { id: 'calibration-log', name: 'Calibration log', where: 'On a clipboard by the sink',
      clue: 'A log sheet with one line filled in. <b>EXTRACTOR FAN CYCLE {{fr.b}} MIN</b>' },
    { id: 'instruction-card', name: 'Instruction card', where: 'Laminated, screwed to the wall',
      clue: 'A laminated card, screwed on at the corners. <b>CHECK VALUE = {{cc.a}} + {{cc.b}} &divide; {{cc.c}}</b>' },
    { id: 'helpdesk-ticket', name: 'Helpdesk ticket', where: 'Still in the folder', clue: null,
      flavour: 'The install job, closed and signed off. Someone has written &ldquo;customer happy&rdquo; at the bottom.' },
    { id: 'stop-button', name: 'Emergency stop', where: 'Under the controller', clue: null,
      flavour: 'A red mushroom head, and a warning card beside it. Pressing it floods the kiln. IT fitted the same ' +
               'system they use in the server room.' },
    { id: 'firing-screen', name: 'Firing screen', where: 'On the controller', clue: null,
      flavour: 'A countdown, going down.' }
  ],

  locks: [
    {
      id: 'kiln-sensor-limit',
      key: 'sl',
      name: 'Keypad on the controller',
      brief: 'A keypad under the display. It opens at the highest sensor ID that still fits under the network limit.',
      instrument: { kind: 'keypad', label: 'HIGHEST SENSOR ID UNDER THE LIMIT', digits: 2, verb: 'Enter code' },
      variants: [
        {
          "k": 9,
          "L": 85,
          "answer": 81,
          "miss": 90,
          "mults": "72, 81, 90"
        },
        {
          "k": 9,
          "L": 66,
          "answer": 63,
          "miss": 72,
          "mults": "54, 63, 72"
        },
        {
          "k": 13,
          "L": 59,
          "answer": 52,
          "miss": 65,
          "mults": "39, 52, 65"
        },
        {
          "k": 8,
          "L": 31,
          "answer": 24,
          "miss": 32,
          "mults": "16, 24, 32"
        },
        {
          "k": 7,
          "L": 41,
          "answer": 35,
          "miss": 42,
          "mults": "28, 35, 42"
        },
        {
          "k": 10,
          "L": 43,
          "answer": 40,
          "miss": 50,
          "mults": "30, 40, 50"
        },
        {
          "k": 6,
          "L": 35,
          "answer": 30,
          "miss": 36,
          "mults": "24, 30, 36"
        },
        {
          "k": 8,
          "L": 77,
          "answer": 72,
          "miss": 80,
          "mults": "64, 72, 80"
        },
        {
          "k": 6,
          "L": 94,
          "answer": 90,
          "miss": 96,
          "mults": "84, 90, 96"
        },
        {
          "k": 9,
          "L": 48,
          "answer": 45,
          "miss": 54,
          "mults": "36, 45, 54"
        }
      ],
      missTitle: 'That one is over the limit.',
      missSays: 'The highest ID has to still fit under it, not step past it.',
      hints: [
        'The IDs go up in steps of the same number.',
        'Count up in those steps and stop before the limit.',
        'Take the last one you reached that is still under it.'
      ],
      solve: 'Multiples of {{sl.k}}: {{sl.mults}}. The highest under {{sl.L}} is <b>{{sl.answer}}</b>.',
      onOpen: 'The keypad beeps once and the first indicator goes out.'
    },
    {
      id: 'kiln-fan-restart',
      key: 'fr',
      name: 'Dial beside the display',
      brief: 'A dial marked in minutes. It opens at the number of minutes until both fans restart at the same moment.',
      instrument: { kind: 'dial', label: 'MINUTES UNTIL BOTH FANS RESTART TOGETHER', min: 0, max: 120, step: 1,
                    decimals: 0, start: 0, verb: 'Set dial' },
      variants: [
        {
          "a": 6,
          "b": 14,
          "answer": 42,
          "miss": 84,
          "multA": "6, 12, 18, 24, 30, 36, 42",
          "multB": "14, 28, 42"
        },
        {
          "a": 4,
          "b": 10,
          "answer": 20,
          "miss": 40,
          "multA": "4, 8, 12, 16, 20",
          "multB": "10, 20"
        },
        {
          "a": 4,
          "b": 14,
          "answer": 28,
          "miss": 56,
          "multA": "4, 8, 12, 16, 20, 24, 28",
          "multB": "14, 28"
        },
        {
          "a": 4,
          "b": 18,
          "answer": 36,
          "miss": 72,
          "multA": "4, 8, 12, 16, 20, 24, 28, 32, 36",
          "multB": "18, 36"
        },
        {
          "a": 4,
          "b": 6,
          "answer": 12,
          "miss": 24,
          "multA": "4, 8, 12",
          "multB": "6, 12"
        },
        {
          "a": 6,
          "b": 16,
          "answer": 48,
          "miss": 96,
          "multA": "6, 12, 18, 24, 30, 36, 42, 48",
          "multB": "16, 32, 48"
        },
        {
          "a": 8,
          "b": 14,
          "answer": 56,
          "miss": 112,
          "multA": "8, 16, 24, 32, 40, 48, 56",
          "multB": "14, 28, 42, 56"
        }
      ],
      missTitle: 'That&rsquo;s the two cycle lengths multiplied.',
      missSays: 'They do meet there, but they meet sooner. Look for the first time both fit exactly.',
      hints: [
        'Each fan restarts at every multiple of its own cycle.',
        'Write out the multiples of each cycle length.',
        'Find the smallest number that appears in both lists.'
      ],
      solve: 'Multiples of {{fr.a}}: {{fr.multA}}. Multiples of {{fr.b}}: {{fr.multB}}. Lowest common multiple ' +
             '<b>{{fr.answer}}</b>.',
      onOpen: 'Both fans drop to idle together.'
    },
    {
      id: 'kiln-cancel-check',
      key: 'cc',
      name: 'Slider on the controller',
      brief: 'A slider beside the display. It opens at the check value printed on IT&rsquo;s instruction card.',
      instrument: { kind: 'slider', label: 'CHECK VALUE', min: 0, max: 60, step: 1, decimals: 0,
                    start: 0, verb: 'Set slider' },
      variants: [
        {
          "a": 21,
          "b": 45,
          "c": 3,
          "answer": 36,
          "miss": 22,
          "quot": 15
        },
        {
          "a": 36,
          "b": 38,
          "c": 2,
          "answer": 55,
          "miss": 37,
          "quot": 19
        },
        {
          "a": 2,
          "b": 48,
          "c": 2,
          "answer": 26,
          "miss": 25,
          "quot": 24
        },
        {
          "a": 40,
          "b": 20,
          "c": 2,
          "answer": 50,
          "miss": 30,
          "quot": 10
        },
        {
          "a": 35,
          "b": 28,
          "c": 7,
          "answer": 39,
          "miss": 9,
          "quot": 4
        },
        {
          "a": 10,
          "b": 38,
          "c": 2,
          "answer": 29,
          "miss": 24,
          "quot": 19
        },
        {
          "a": 14,
          "b": 36,
          "c": 2,
          "answer": 32,
          "miss": 25,
          "quot": 18
        },
        {
          "a": 16,
          "b": 24,
          "c": 4,
          "answer": 22,
          "miss": 10,
          "quot": 6
        },
        {
          "a": 44,
          "b": 4,
          "c": 2,
          "answer": 46,
          "miss": 24,
          "quot": 2
        },
        {
          "a": 40,
          "b": 12,
          "c": 4,
          "answer": 43,
          "miss": 13,
          "quot": 3
        }
      ],
      missTitle: 'That&rsquo;s the calculation worked out left to right.',
      missSays: 'Division happens before addition, whatever order it is written in.',
      hints: [
        'Some operations come before others, whatever order they are written in.',
        'Division comes before addition.',
        'Do the division first, then add.'
      ],
      solve: '{{cc.b}} &divide; {{cc.c}} = {{cc.quot}}. {{cc.a}} + {{cc.quot}} = <b>{{cc.answer}}</b>.',
      onOpen: 'The countdown stops. The screen clears.'
    }
  ]
};
