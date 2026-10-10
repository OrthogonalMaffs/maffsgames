/* Room data for "library-jam" — shared by play.html (the game, for now) and
   teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand.

   BUILT 2026-10-10 (contract LIBRARY-JAM-BUILD) from the draft Jon approved in
   full on 10 Oct (docs/escape-room-drafts/library-draft.md, merged #248). A new
   Warm-up room for the priority audience. Mrs Barb Phile, "Bibby", is Jon's
   character and speaks only in this room. Wrong-entry line 3 is Jon's line,
   verbatim. The three locks are bank batch 10 (docs/lock-bank-batch10.txt).

   The room sits behind its holding page (index.html) until Jon has play-tested
   it at play.html; it has no hub card until its release contract.

   GRADES (canon §11.3, ESCAPE-DIFFICULTY): ordering decimals with different
   numbers of decimal places (2); angles on a straight line, one subtraction
   from 180 (1); a fine multiplied out, then pence to pounds, no calculator (2).
   The hardest lock makes the room ★ Warm-up. There is no `levelLabel`: #253
   removed it from every room (display only); the stars replace it.

   NOTE — object `id`s are load-bearing: teacher.html maps clues to locks by id
   in its `clueMap`. `memo` and `biography` are the two blanks.

   NOTE — not one numeral is typed into a clue string: every Dewey number, the
   angle, the fine, the days and the count are tokens. The only figure in the
   prose outside tokens is "half past three", in words.

   ART: none yet (art pending; ART-PENDING, #244). Jon generates the three
   pictures after his play-test; add `art` with them, never before. The alts
   below are the draft's, to be checked against the pictures.

   RULE — the fail picture will show the end of the day, which is only true at
   time-out. Never set `missArt` on any lock in this room. */
window.ROOM = {
  slug: 'escape-library-jam',
  title: 'The Library Jam',
  level: 'gcse',
  minutes: 15,
  penalty: 45,
  sceneAlt: 'The backroom of a school library, seen past a loaded returns trolley. An old metal drop-box is built into the wall, and a sorting belt runs out of it towards a chute and a wire bin. A mechanical arm has stopped over the belt with one book in its grip, and a flat deflector arm sits at a slant across the belt. Shelves of books line the walls, a few sticking out at odd angles, and a small screen glows on a desk beside a date stamp and a cup of tea.',
  failAlt: 'The same backroom at the end of the day. The belt is still, the arm frozen with its book, and the wire bin is empty. The screen on the desk glows red. The returns trolley stands where it was.',
  winAlt: 'The same backroom. The wire bin is full of books, neatly stacked, and the arms are at rest. Every book on the shelves is pushed in level. The screen on the desk glows green.',

  hook: 'The library at St Martha&rsquo;s belongs, as far as anyone can tell, to Mrs Barb Phile. Officially she ' +
        'is the librarian. To every student in the school she is Bibby. She likes books a great deal more than ' +
        'she likes children, though she will make an exception for a bookworm. She calls the books her babies, ' +
        'and she means it.<br><br>' +
        'Behind the returns trolley is a hatch, and behind the hatch is the backroom where the returns drop-box ' +
        'empties onto an old sorting belt. Budget cuts. The machine is older than most of the staff, and today it ' +
        'has jammed with your whole class&rsquo;s returned books inside it.',
  brief: 'The library system can&rsquo;t see inside a jammed machine. As far as it knows, every one of those books ' +
         'is lost. At half past three it emails every parent in the class about a lost book, and charges a fine ' +
         'for each one.<br><br>' +
         'Bibby will not overturn a fine, and she will not take a child&rsquo;s word over the system&rsquo;s. It ' +
         'isn&rsquo;t spite. The budget is tight, a lost book is unlikely ever to be replaced, and she wants those ' +
         'stories still on the shelves for the year groups after yours.<br><br>' +
         'So don&rsquo;t ask her. Make the record true. Get the machine running, get the books into the cleared ' +
         'bin, and the system will see them home and stop the emails itself.<br><br>' +
         'She is out among the shelves, finding books in places they shouldn&rsquo;t be. Every wrong setting costs ' +
         'you time, and she always finds another one.',
  /* There is no `fail` slot: the engine shows `stakes` after "If you get it
     wrong." on the start screen and after "And so:" on the time-out screen, so
     the failure is written here and reads after both. */
  stakes: 'At half past three the emails go out: every parent in the class, one lost book each, one fine each. ' +
          'Bibby reads the list on her screen without a flicker, because the system is never wrong, and starts the ' +
          'replacement forms the budget will never pay for. Inside the drop-box, under the jam, every one of those ' +
          'books sits in the dark.',
  win: 'The arm swings, the belt runs, and the books come down the chute one at a time into the cleared bin. Each ' +
       'one beeps as it lands. On the screen, LOST turns to RETURNED, name by name, and the half-past-three run ' +
       'cancels itself.<br><br>' +
       'Bibby comes round the end of the shelves with Pride and Prejudice under her arm. She looks at the screen, ' +
       'then at the bin. She lifts out the top book, checks the spine, and holds it for a moment longer than she ' +
       'needs to.<br><br>' +
       '&ldquo;They were here all along,&rdquo; she says, to the book.<br><br>' +
       'Then she puts it on the trolley, spine out, and goes to find a shelf for Pride and Prejudice that ' +
       'isn&rsquo;t Biography.',

  /* Wrong-entry lines, indexed by how many wrong settings have been made so
     far; the last one repeats (the joke: she finds one every time). Each head
     is the machine; each body is Bibby, out in the library, finding something
     in the wrong place. None of them is aimed at the students. Line 3 is Jon's,
     verbatim. */
  wrongLines: [
    { head: 'The machine clunks and the setting clears.',
      body: 'Out in the library, a book slides off a shelf. A tut. &ldquo;A cookbook. In Astronomy.&rdquo; It ' +
            'slides back in somewhere else.' },
    { head: 'The belt shudders and stops again.',
      body: '&ldquo;Atlases are not for leaning on.&rdquo; The sound of a large book being carried, with great ' +
            'care, back to where it lives.' },
    { head: 'The setting slides back. The clock over the desk doesn&rsquo;t.',
      body: 'Her voice comes through the hatch, quite clearly: &ldquo;Pride and Prejudice is NOT staying in the ' +
            'Biography section.&rdquo;' },
    { head: 'Another one. The clock keeps going.',
      body: 'From somewhere in the stacks: &ldquo;Wrong place.&rdquo; A pause. A book moving. &ldquo;Better.&rdquo;' }
  ],

  objects: [
    { id: 'trolley', name: 'The returns trolley', where: 'behind the hatch, still loaded from this morning',
      clue: 'Every spine has a white label, and every label starts the same. In the order they were dropped in: ' +
            '<b>{{dw.list}}</b>.' },
    { id: 'jammed-book', name: 'Book in the sorting arm', where: 'held fast in the arm over the belt',
      clue: 'A book about {{dw.subject}}, gripped by its corner. Spine label <b>{{dw.book}}</b>. A sticker on the ' +
            'arm: FILES SMALLEST FIRST ALONG THE SHELF.' },
    { id: 'belt-plate', name: 'Maintenance plate', where: 'riveted to the side of the belt',
      clue: 'Stamped into the metal: <b>DEFLECTOR ARM: {{df.x}}&deg; TO THE BELT.</b>' },
    { id: 'reset-card', name: 'Reset card', where: 'taped inside the machine’s cover',
      clue: '&ldquo;RESET: set the dial to the angle between the arm and the belt <b>on the other side of the ' +
            'arm</b>. The belt is straight.&rdquo;' },
    { id: 'fines-screen', name: 'The library system', where: 'on the screen on Bibby’s desk',
      clue: 'LOST BOOKS. Fine: <b>{{fn.p}}p a day</b> for each book. Days overdue: <b>{{fn.d}}</b>.' },
    { id: 'drop-counter', name: 'Drop-box counter', where: 'a little mechanical counter on the drop-box',
      clue: '<b>{{fn.n}}</b> books posted today, one from everyone in your class. The counter, at least, saw them ' +
            'go in.' },
    { id: 'memo', name: 'Memo', where: 'pinned over the drop-box', clue: null,
      flavour: 'From the business office. The drop-box repair has been moved to next year&rsquo;s budget. Somebody ' +
               'has written &ldquo;AGAIN&rdquo; under it, in very neat capitals.' },
    { id: 'biography', name: 'The Biography shelf', where: 'through the hatch, nearest the door', clue: null,
      flavour: 'Lives of explorers, scientists and queens, all in order. And one book that isn&rsquo;t the life of ' +
               'anybody at all.' }
  ],

  locks: [
    {
      id: 'dewey-sort-arm',
      key: 'dw',
      grade: 2,
      name: 'The sorting arm',
      brief: 'The arm files books by the number on the spine, smallest first along the shelf. It has stopped with ' +
             'one book in its grip, and it won&rsquo;t let go until it is told which slot that book goes in.',
      instrument: { kind: 'dial', label: 'SLOT ON THE SHELF', min: 1, max: 8, step: 1, decimals: 0,
                    start: 1, verb: 'Set slot' },
      variants: [
        {
          "shelf": "520",
          "subject": "stars and planets",
          "parts": [
            "35",
            "5",
            "15",
            "62",
            "4"
          ],
          "book": "520.4",
          "answer": 3,
          "miss": 1,
          "list": "520.35, 520.5, 520.15, 520.62, 520.4",
          "sorted": "520.15, 520.35, 520.4, 520.5, 520.62"
        },
        {
          "shelf": "567",
          "subject": "dinosaurs",
          "parts": [
            "6",
            "4",
            "07",
            "13",
            "86",
            "65"
          ],
          "book": "567.6",
          "answer": 4,
          "miss": 2,
          "list": "567.6, 567.4, 567.07, 567.13, 567.86, 567.65",
          "sorted": "567.07, 567.13, 567.4, 567.6, 567.65, 567.86"
        },
        {
          "shelf": "641",
          "subject": "cooking",
          "parts": [
            "3",
            "7",
            "8",
            "18",
            "97"
          ],
          "book": "641.7",
          "answer": 3,
          "miss": 2,
          "list": "641.3, 641.7, 641.8, 641.18, 641.97",
          "sorted": "641.18, 641.3, 641.7, 641.8, 641.97"
        },
        {
          "shelf": "551",
          "subject": "volcanoes and weather",
          "parts": [
            "9",
            "3",
            "06",
            "77",
            "76"
          ],
          "book": "551.9",
          "answer": 5,
          "miss": 3,
          "list": "551.9, 551.3, 551.06, 551.77, 551.76",
          "sorted": "551.06, 551.3, 551.76, 551.77, 551.9"
        },
        {
          "shelf": "942",
          "subject": "British history",
          "parts": [
            "4",
            "1",
            "8",
            "9",
            "63",
            "77"
          ],
          "book": "942.9",
          "answer": 6,
          "miss": 4,
          "list": "942.4, 942.1, 942.8, 942.9, 942.63, 942.77",
          "sorted": "942.1, 942.4, 942.63, 942.77, 942.8, 942.9"
        },
        {
          "shelf": "796",
          "subject": "sport",
          "parts": [
            "8",
            "2",
            "37",
            "61",
            "39"
          ],
          "book": "796.8",
          "answer": 5,
          "miss": 2,
          "list": "796.8, 796.2, 796.37, 796.61, 796.39",
          "sorted": "796.2, 796.37, 796.39, 796.61, 796.8"
        },
        {
          "shelf": "598",
          "subject": "birds",
          "parts": [
            "1",
            "6",
            "8",
            "63",
            "58",
            "59"
          ],
          "book": "598.6",
          "answer": 4,
          "miss": 2,
          "list": "598.1, 598.6, 598.8, 598.63, 598.58, 598.59",
          "sorted": "598.1, 598.58, 598.59, 598.6, 598.63, 598.8"
        },
        {
          "shelf": "821",
          "subject": "poetry",
          "parts": [
            "5",
            "7",
            "2",
            "8",
            "16",
            "53"
          ],
          "book": "821.5",
          "answer": 3,
          "miss": 2,
          "list": "821.5, 821.7, 821.2, 821.8, 821.16, 821.53",
          "sorted": "821.16, 821.2, 821.5, 821.53, 821.7, 821.8"
        }
      ],
      missTitle: 'That reads the digits after the point as a whole number.',
      missSays: 'Slot {{dw.miss}} is where {{dw.book}} would go if a longer number after the point meant a bigger ' +
                'number. It doesn&rsquo;t. Line them up by the tenths first, then the hundredths.',
      hints: [
        'Every book on the trolley starts with the same whole number, so only the part after the decimal point ' +
        'matters.',
        'Compare the tenths first. Only if two books have the same tenths do you look at the hundredths. More ' +
        'digits after the point doesn&rsquo;t make a number bigger.',
        'Smallest first: {{dw.sorted}}. Count along to {{dw.book}}.'
      ],
      solve: 'Smallest first: {{dw.sorted}}. {{dw.book}} is number <b>{{dw.answer}}</b>.',
      onOpen: 'The arm swings the book into its slot with a satisfied clunk, and lets go.'
    },
    {
      id: 'deflector-straight-line',
      key: 'df',
      grade: 1,
      name: 'The deflector arm',
      brief: 'The deflector knocks each book off the belt and down the chute to the cleared bin. It has slipped. To ' +
             'reset it, the dial wants the angle between the arm and the belt on the other side of the arm.',
      instrument: { kind: 'dial', label: 'ANGLE ON THE OTHER SIDE', min: 0, max: 180, step: 1, decimals: 0,
                    unit: '°', start: 0, verb: 'Set angle' },
      variants: [
        {
          "x": 37,
          "answer": 143,
          "miss": 53,
          "half": 180,
          "quarter": 90
        },
        {
          "x": 46,
          "answer": 134,
          "miss": 44,
          "half": 180,
          "quarter": 90
        },
        {
          "x": 63,
          "answer": 117,
          "miss": 27,
          "half": 180,
          "quarter": 90
        },
        {
          "x": 68,
          "answer": 112,
          "miss": 22,
          "half": 180,
          "quarter": 90
        },
        {
          "x": 24,
          "answer": 156,
          "miss": 66,
          "half": 180,
          "quarter": 90
        },
        {
          "x": 56,
          "answer": 124,
          "miss": 34,
          "half": 180,
          "quarter": 90
        },
        {
          "x": 32,
          "answer": 148,
          "miss": 58,
          "half": 180,
          "quarter": 90
        },
        {
          "x": 51,
          "answer": 129,
          "miss": 39,
          "half": 180,
          "quarter": 90
        }
      ],
      missTitle: 'That makes a right angle, not a straight line.',
      missSays: '{{df.miss}}&deg; is {{df.quarter}} &minus; {{df.x}}, the angles that make a right angle. The belt ' +
                'is a straight line, so the two angles make {{df.half}}&deg;.',
      hints: [
        'The belt is a straight line, and the arm meets it at one point. There is an angle on each side of the arm.',
        'Angles on a straight line add up to {{df.half}}&deg;.',
        '{{df.half}} &minus; {{df.x}}.'
      ],
      solve: '{{df.half}} &minus; {{df.x}} = <b>{{df.answer}}&deg;</b>.',
      onOpen: 'The arm clicks into place, and the first book drops down the chute.'
    },
    {
      id: 'fines-pence-to-pounds',
      key: 'fn',
      grade: 2,
      name: 'The reconciliation screen',
      brief: 'Once the books are in the cleared bin, the system can reverse the fines itself. It won&rsquo;t ' +
             'cancel the half-past-three run until it is given the total it charged, in pounds.',
      instrument: { kind: 'keypad', label: 'TOTAL TO REVERSE, IN POUNDS', maxDigits: 4, verb: 'Enter total' },
      variants: [
        {
          "p": 15,
          "d": 12,
          "n": 30,
          "answer": 54,
          "miss": 5400,
          "each": 180,
          "hundred": 100
        },
        {
          "p": 20,
          "d": 15,
          "n": 26,
          "answer": 78,
          "miss": 7800,
          "each": 300,
          "hundred": 100
        },
        {
          "p": 20,
          "d": 15,
          "n": 32,
          "answer": 96,
          "miss": 9600,
          "each": 300,
          "hundred": 100
        },
        {
          "p": 20,
          "d": 10,
          "n": 24,
          "answer": 48,
          "miss": 4800,
          "each": 200,
          "hundred": 100
        },
        {
          "p": 10,
          "d": 20,
          "n": 28,
          "answer": 56,
          "miss": 5600,
          "each": 200,
          "hundred": 100
        },
        {
          "p": 5,
          "d": 8,
          "n": 30,
          "answer": 12,
          "miss": 1200,
          "each": 40,
          "hundred": 100
        },
        {
          "p": 10,
          "d": 14,
          "n": 20,
          "answer": 28,
          "miss": 2800,
          "each": 140,
          "hundred": 100
        },
        {
          "p": 15,
          "d": 14,
          "n": 20,
          "answer": 42,
          "miss": 4200,
          "each": 210,
          "hundred": 100
        },
        {
          "p": 10,
          "d": 20,
          "n": 31,
          "answer": 62,
          "miss": 6200,
          "each": 200,
          "hundred": 100
        },
        {
          "p": 5,
          "d": 15,
          "n": 32,
          "answer": 24,
          "miss": 2400,
          "each": 75,
          "hundred": 100
        }
      ],
      missTitle: 'That is the total in pence.',
      missSays: '{{fn.miss}} is how many pence the system charged. The screen wants pounds, and there are ' +
                '{{fn.hundred}} pence in a pound.',
      hints: [
        'Start with one student: so many pence a day, for so many days.',
        'Then the whole class: one fine for every book posted.',
        'That total is in pence. There are {{fn.hundred}} pence in a pound.'
      ],
      solve: '{{fn.p}}p &times; {{fn.d}} days = {{fn.each}}p each. {{fn.each}}p &times; {{fn.n}} = {{fn.miss}}p = ' +
             '<b>&pound;{{fn.answer}}</b>.',
      onOpen: 'The screen thinks about it, then cancels the half-past-three run. No emails. No fines.'
    }
  ]
};
