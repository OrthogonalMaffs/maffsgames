/* Room data for "comic-caper" — shared by index.html (the game) and
   teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand. The locks are
   batch 6 of the audited bank (docs/lock-bank-batch6.txt).

   BUILT 2026-09-17 for a GCSE resit class (grade 3/4), from a site user's
   request. Four clue-carrying objects and four blanks; the HCF lock takes its
   two figures from two different objects.

   NOTE — object `id`s are load-bearing: teacher.html maps clues to locks by id
   in its `clueMap`. Renaming one silently breaks the teacher page.

   ART: scene, fail and win filed 2026-09-17, all from one viewpoint. The alts
   below were approved by Jon against those three pictures. Known and accepted:
   the clock hangs centred above the cupboard in the scene and above-right in
   the fail and win pictures.

   RULE — the fail picture shows the cupboard already gone, which is only true at
   time-out. Never set `missArt` on any lock in this room: the engine shows the
   fail picture beside a misconception response only when that flag is set. */
window.ROOM = {
  slug: 'escape-comic-caper',
  title: 'The Comic Caper',
  level: 'gcse',
  levelLabel: 'GCSE',
  minutes: 15,
  penalty: 45,
  art: 'comic-caper',
  sceneAlt: 'A classroom with the chairs tucked in and old green textbooks, held together with tape, lying open on every desk. At the back stands a tall wooden cupboard with its two doors shut: a round combination dial on each door, a brass slider bar across both at handle height, a small riveted metal plate and a plain sticker below. A clock hangs above it. To the right are a sink and a door with frosted glass; the teacher’s desk in the front corner has a folded leaflet on top and a sheet of paper taped to its drawer.',
  failAlt: 'The same classroom with the old cupboard gone. A pale, clean rectangle on the back wall shows where it stood, with a line of dust along the floor and scraps of paper left behind. Textbooks lie open on the desks, a leaflet with a blank cover sits on the teacher’s desk, and a sheet of paper is taped to its drawer.',
  winAlt: 'The same classroom in warm light. The old cupboard stands open with both doors swung wide and its shelves bare, the combination dials still on the doors and short chains hanging loose. Brightly coloured comics poke out of school bags hanging on the chairs, and the old taped textbooks lie open on the desks.',

  hook: 'Ms Fromage has set a chapter from the old green textbooks, the ones held together with tape, and ' +
        'stepped outside. Her shape is on the frosted glass in the door. She&rsquo;s telling a colleague about ' +
        'her cruise.',
  brief: 'Mr Babel&rsquo;s French comics are in the old cupboard at the back of the room. Everyone calls it the ' +
         'Chokey. Ms Fromage locked them in there and then forgot all about them. The key went in the bin. ' +
         'Estates have put a sticker on the door, and the Chokey goes today. It still has its backup combination ' +
         'locks. Open all three before she comes back in.',
  stakes: 'The Estates van takes the Chokey at the end of the day, and Mr Babel&rsquo;s comics go with it.',
  win: 'The last lock gives. The comics are inside, exactly where she left them. By the time the door opens, ' +
       'they&rsquo;re in bags, and everyone is looking at the textbook.',

  /* Wrong-entry lines, indexed by how many wrong settings have been made so
     far; the last one repeats. Ms Fromage, outside the door, about her cruise. */
  wrongLines: [
    { head: 'Outside, the conversation carries on.',
      body: '&ldquo;It&rsquo;s an adults-only cruise. I checked.&rdquo;' },
    { head: 'She stops mid-sentence, then carries on a little louder.',
      body: '&ldquo;My travel buddy is very excited. I&rsquo;ve got him registered as an emotional support ' +
            'reptile.&rdquo;' },
    { head: 'The talking stops. Her silhouette turns towards the door.',
      body: '&ldquo;I&rsquo;m going to speak loudly and slowly in English like the other Brits. If anyone finds ' +
            'out I speak French, I&rsquo;ll be interpreting for the whole ship.&rdquo;' },
    { head: 'Her silhouette fills the glass. The handle turns.',
      body: '&ldquo;I hope you&rsquo;re conjugating those verbs correctly, you lot.&rdquo;' }
  ],

  objects: [
    { id: 'asset-plate', name: 'Asset plate', where: 'Riveted to the Chokey door',
      clue: 'An old metal plate, painted over more than once. <b>ASSET No. {{fc.N}}</b>' },
    { id: 'series-label', name: 'Series label', where: 'Inside the textbook cupboard lid',
      clue: 'A yellowed label: <b>FRENCH COURSE, VOLUMES 1&ndash;{{pv.V}}</b>' },
    { id: 'delivery-docket', name: 'Delivery docket', where: 'Stuffed in a textbook',
      clue: 'A carbon-copy docket from the original order. <b>GRAMMAR BOOKS: {{hcf.a}}</b>' },
    { id: 'stock-card', name: 'Stock card', where: 'Pinned above the sink',
      clue: 'A handwritten stock card. <b>DICTIONARIES: {{hcf.b}}</b>' },
    { id: 'itinerary', name: 'Cruise itinerary', where: 'On her desk', clue: null,
      flavour: 'Every port circled. Brest is underlined twice.' },
    { id: 'feeding-chart', name: 'Feeding chart', where: 'Taped to her drawer', clue: null,
      flavour: 'M. TORTUE. Dandelions Monday. No lettuce after Brest.' },
    { id: 'estates-sticker', name: 'Estates sticker', where: 'On the Chokey door', clue: null,
      flavour: 'REMOVE AT END OF YEAR. Signed by someone in Estates.' },
    { id: 'textbook', name: 'Chapter she set', where: 'Open on every desk', clue: null,
      flavour: 'A dialogue about buying a cassette at the railway station.' }
  ],

  locks: [
    {
      id: 'chokey-factor-count',
      key: 'fc',
      name: 'Dial on the hinge side',
      brief: 'A dial on the hinge side, numbered all the way round. It opens at the number of factors of the ' +
             'cupboard&rsquo;s asset number.',
      instrument: { kind: 'dial', label: 'NUMBER OF FACTORS', min: 0, max: 20, step: 1, decimals: 0,
                    start: 0, verb: 'Set dial' },
      variants: [
        {
          "N": 24,
          "answer": 8,
          "miss": 6,
          "facN": "1, 2, 3, 4, 6, 8, 12, 24"
        },
        {
          "N": 72,
          "answer": 12,
          "miss": 10,
          "facN": "1, 2, 3, 4, 6, 8, 9, 12, 18, 24, 36, 72"
        },
        {
          "N": 76,
          "answer": 6,
          "miss": 4,
          "facN": "1, 2, 4, 19, 38, 76"
        },
        {
          "N": 80,
          "answer": 10,
          "miss": 8,
          "facN": "1, 2, 4, 5, 8, 10, 16, 20, 40, 80"
        }
      ],
      missTitle: 'Not every factor is there.',
      missSays: 'Factors come in pairs &mdash; check you&rsquo;ve found every pair.',
      hints: [
        'Factors come in pairs that multiply to make the number.',
        'Start at 1 &times; {{fc.N}} and work up. Stop when the pairs start repeating.',
        'Write down every number in every pair, then count them.'
      ],
      solve: '{{fc.facN}} &rarr; <b>{{fc.answer}}</b> factors.',
      onOpen: 'The hinge-side dial clicks and stays put.'
    },
    {
      id: 'chokey-prime-volumes',
      key: 'pv',
      name: 'Dial on the lock plate',
      brief: 'A second dial, set into the lock plate. It opens at how many of the textbook series&rsquo; volume ' +
             'numbers are prime.',
      instrument: { kind: 'dial', label: 'PRIME VOLUMES IN THE SERIES', min: 0, max: 30, step: 1, decimals: 0,
                    start: 0, verb: 'Set dial' },
      variants: [
        {
          "V": 30,
          "answer": 10,
          "miss": 11,
          "primes": "2, 3, 5, 7, 11, 13, 17, 19, 23, 29"
        },
        {
          "V": 55,
          "answer": 16,
          "miss": 17,
          "primes": "2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53"
        },
        {
          "V": 20,
          "answer": 8,
          "miss": 9,
          "primes": "2, 3, 5, 7, 11, 13, 17, 19"
        },
        {
          "V": 50,
          "answer": 15,
          "miss": 16,
          "primes": "2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47"
        },
        {
          "V": 60,
          "answer": 17,
          "miss": 18,
          "primes": "2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59"
        },
        {
          "V": 35,
          "answer": 11,
          "miss": 12,
          "primes": "2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31"
        },
        {
          "V": 45,
          "answer": 14,
          "miss": 15,
          "primes": "2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43"
        },
        {
          "V": 25,
          "answer": 9,
          "miss": 10,
          "primes": "2, 3, 5, 7, 11, 13, 17, 19, 23"
        },
        {
          "V": 40,
          "answer": 12,
          "miss": 13,
          "primes": "2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37"
        }
      ],
      missTitle: 'One too many.',
      missSays: '1 isn&rsquo;t prime &mdash; it only has one factor.',
      hints: [
        'Draw a grid of 1 to {{pv.V}}. You&rsquo;re going to cross out everything that isn&rsquo;t prime.',
        'Cross out 1. Circle 2 and cross out its other multiples. Do the same for 3 and 5, then 7 if your grid ' +
        'goes past 49.',
        'Count the circled numbers. Check 1 isn&rsquo;t one of them.'
      ],
      solve: '{{pv.primes}} &rarr; <b>{{pv.answer}}</b>.',
      onOpen: 'Something inside the lock plate drops into place.'
    },
    {
      id: 'chokey-hcf-bundles',
      key: 'hcf',
      name: 'Slider across the handle',
      brief: 'A brass slider across the handle. Every bundle has the same number of grammar books and ' +
             'dictionaries, and every book is used.',
      instrument: { kind: 'slider', label: 'MOST IDENTICAL BUNDLES, EVERY BOOK USED', min: 0, max: 120, step: 1,
                    decimals: 0, start: 0, verb: 'Set slider' },
      variants: [
        {
          "a": 18,
          "b": 45,
          "answer": 9,
          "miss": 90,
          "facA": "1, 2, 3, 6, 9, 18",
          "facB": "1, 3, 5, 9, 15, 45"
        },
        {
          "a": 18,
          "b": 24,
          "answer": 6,
          "miss": 72,
          "facA": "1, 2, 3, 6, 9, 18",
          "facB": "1, 2, 3, 4, 6, 8, 12, 24"
        },
        {
          "a": 20,
          "b": 50,
          "answer": 10,
          "miss": 100,
          "facA": "1, 2, 4, 5, 10, 20",
          "facB": "1, 2, 5, 10, 25, 50"
        },
        {
          "a": 15,
          "b": 20,
          "answer": 5,
          "miss": 60,
          "facA": "1, 3, 5, 15",
          "facB": "1, 2, 4, 5, 10, 20"
        },
        {
          "a": 22,
          "b": 33,
          "answer": 11,
          "miss": 66,
          "facA": "1, 2, 11, 22",
          "facB": "1, 3, 11, 33"
        },
        {
          "a": 24,
          "b": 36,
          "answer": 12,
          "miss": 72,
          "facA": "1, 2, 3, 4, 6, 8, 12, 24",
          "facB": "1, 2, 3, 4, 6, 9, 12, 18, 36"
        },
        {
          "a": 14,
          "b": 35,
          "answer": 7,
          "miss": 70,
          "facA": "1, 2, 7, 14",
          "facB": "1, 5, 7, 35"
        },
        {
          "a": 16,
          "b": 24,
          "answer": 8,
          "miss": 48,
          "facA": "1, 2, 4, 8, 16",
          "facB": "1, 2, 3, 4, 6, 8, 12, 24"
        },
        {
          "a": 28,
          "b": 42,
          "answer": 14,
          "miss": 84,
          "facA": "1, 2, 4, 7, 14, 28",
          "facB": "1, 2, 3, 6, 7, 14, 21, 42"
        },
        {
          "a": 26,
          "b": 39,
          "answer": 13,
          "miss": 78,
          "facA": "1, 2, 13, 26",
          "facB": "1, 3, 13, 39"
        }
      ],
      missTitle: 'That&rsquo;s the lowest common multiple &mdash; bigger than either pile.',
      missSays: 'You need the biggest number that goes into both.',
      hints: [
        'Identical bundles using every book means the number of bundles divides both amounts.',
        'List the factors of {{hcf.a}} and the factors of {{hcf.b}}.',
        'Find the largest number that appears in both lists.'
      ],
      solve: 'Factors of {{hcf.a}}: {{hcf.facA}}. Factors of {{hcf.b}}: {{hcf.facB}}. Highest common factor ' +
             '<b>{{hcf.answer}}</b>.',
      onOpen: 'The slider bottoms out. The handle turns.'
    }
  ]
};
