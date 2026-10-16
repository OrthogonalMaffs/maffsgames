/* Room data for "big-school-begins" — shared by index.html (the holding page), play.html (the room, live but
   unlisted) and teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand.

   BUILT 2026-10-16 (contract BSB-ROOM-BUILD, saved as docs/handover/contracts/2026-10-16-bsb-room-build.md) from
   the draft Jon approved with rulings the same day (docs/escape-room-drafts/big-school-begins-draft.md, merged in
   #422). A transition-day room: the students' first visit to the school they start at in September, a hunt of
   four stops round it, and William, a new student who knows nobody, kept with the group from the map to the
   lunch table. Daisy Reddington is the group's buddy and carries every wrong-entry and misconception line. Mrs
   Barb Phile ("Bibby", the librarian, who speaks in The Library Jam) is never quoted here: she hands over a
   written card (Jon's ruling 4). Every character is invented. The lines Jon wrote are used word for word (ruling
   11): the last paragraph of the hook, the four wrongLines bodies, the four missSays, William's line in the win,
   and the stakes (ruling 6).

   NAMED EXCEPTIONS FOR THIS ROOM (Jon, 16 Oct 2026, ruling 1): FOUR locks and a TWENTY-minute clock (every other
   room has three locks and fifteen minutes). Both are data the engine already reads (`minutes`, R.locks.length);
   no shared code changed. The 45-second penalty is the house figure.

   SR-14 EXCEPTION (Jon, 16 Oct 2026, ruling 11e): William's line in the win ("My big brother said I'd definitely
   get my head flushed down the toilet, but you guys are really nice.") is kept by Jon's ruling. It names the myth
   a new student fears in order to show it is untrue. Canon records it via the home-lane label contract.

   NAME (ruling 8, draft item 17): no line plays on William's surname. He is named in full once, in the hook, and
   is "William" after that. None of the eight words draft item 17 lists appears anywhere in this room, about him
   or anyone (they are not repeated here). One drafted item contains one of them inside another word: lock D's
   set 5 has "a milkshake" on the tray, kept as drafted and approved, and flagged to Jon in the build PR.

   SR-11: no student-facing slot names a year group, key stage, primary or secondary. The "Starter" label on
   student surfaces (ruling 2) is the home lane's label contract: there is no label or star field here, and the
   derived rating is ★ Warm-up (every lock grade 1).

   STATUS: LIVE BUT UNLISTED, not released. The room is playable at /escape-rooms/big-school-begins/play.html for
   Jon's play-test: noindex, analytics off, linked from nowhere (not in the hub, the front page or the sitemap);
   index.html is the holding page. Release is a separate instruction from Jon.

   GRADES (canon §11.3, ESCAPE-DIFFICULTY): every lock is grade 1 (first-quadrant coordinates; turns in eighths of
   a whole turn; durations across the hour; change from five pounds with exchanges across zeros), so the room is
   ★ Warm-up. `level` is 'year6' (draft item 9: an existing analytics key).

   NOTE — object `id`s are load-bearing: teacher.html maps clues to locks by id in its `clueMap`.
   `lost-property` and `trolley` are the two blanks.

   NOTE — not one numeral is typed into the prose: every coordinate, compass point, time, length and price is a
   token, and every maths constant in a hint or solve is a token too (`dir.whole`, `dir.eighth`, `tt.hourmins`,
   `till.card`). The fixed numbers are in words: "four stops", "eight compass points", "four digits",
   "twenty-four-hour clock", "five pounds" (the lunch card: a numeral there would be a clue figure, draft item 15),
   and Jon's "sixty" and "a hundred" in lock C's missSays.

   NOTE — the four cards can be done in any order (the engine has no gating, draft item 11), so every lock's brief
   and onOpen stands on its own.

   RULE — the stakes are the lunch bell, which is only true at time-out. Never set `missArt` on any lock in this
   room (the kiln, comic and library rule).

   RULE — the hint ladders are generic: every student sees them, so none assumes a particular mistake. The one
   misconception on each lock is handled by missTitle and missSays alone, and no wrong-entry response gives the
   answer.

   ART: pending (contract ART-PENDING). There is no `art` field, so the engine requests no scene, fail or win
   picture; Project Claude writes the prompts after this build. The draft's provisional alts are in the draft, to
   be rewritten against the pictures when they are filed. */
window.ROOM = {
  slug: 'escape-big-school-begins',
  title: 'Big School Begins',
  level: 'year6',
  minutes: 20,
  penalty: 45,

  hook: 'It&rsquo;s transition day at St Martha&rsquo;s: the day you come and see the school you start at in ' +
        'September, and find out it is much, much bigger than the one you are leaving. You arrived this morning ' +
        'as a crowd of strangers in new shoes. By now you have been put in a group, handed a clipboard each and ' +
        'given a buddy: Daisy Reddington, who started here last September and still remembers exactly what it ' +
        'felt like.<br><br>' +
        'There is one more of you. William Trembles has come from a school none of the rest of you went to. He ' +
        'knows nobody, says almost nothing and holds his clipboard with both hands. The building is a lot bigger ' +
        'than he is used to, and it keeps swallowing him.<br><br>' +
        '&ldquo;I&rsquo;m so glad I&rsquo;m looking after you guys, I&rsquo;m missing French AND English.&rdquo;',
  brief: 'Daisy explains the hunt. There are four stops, a clue card for each, and the whole school to find them ' +
         'in. Every card has a box for the answer. Daisy has the answer sheet, and when she ticks a box, that stop ' +
         'is done. She says it isn&rsquo;t a test, and then admits she got every card wrong when she did ' +
         'it.<br><br>' +
         'There is one rule she is strict about: a group finishes together, or it doesn&rsquo;t finish.<br><br>' +
         'The hunt ends when the lunch bell goes. Every wrong answer costs you time: Daisy sends you back to look ' +
         'again, and the clock in the hall doesn&rsquo;t wait.',
  /* There is no `fail` slot: the engine shows `stakes` after "If you get it
     wrong." on the start screen and after "And so:" on the time-out screen, so
     the failure is written here and reads after both. Jon's words (ruling 6). */
  stakes: 'The lunch bell goes with boxes still blank on the card. The canteen is heaving, and you end up ' +
          'squeezed onto the end of a table of older students, eating in silence. Across the room, William is ' +
          'laughing with the group who found him first. Daisy catches your eye: &ldquo;September, then. ' +
          'You&rsquo;ll get another go.&rdquo;',
  win: 'The lunch bell goes, and every box on the card has a tick in it. Daisy finds a table by the window big ' +
       'enough for all of you, and you all sit down at it: William too, between two people he hadn&rsquo;t met ' +
       'this morning, eating and, for the first time today, talking.<br><br>' +
       'Daisy hands in the card and sits down at the end.<br><br>' +
       'William says, &ldquo;My big brother said I&rsquo;d definitely get my head flushed down the toilet, but ' +
       'you guys are really nice.&rdquo;<br><br>' +
       '&ldquo;Same table in September?&rdquo; she says.<br><br>' +
       'William says yes first.',

  /* Wrong-entry lines, indexed by how many wrong settings have been made so
     far; the last one repeats. There is no antagonist, so the voice is an
     ally's (the Kiln precedent). Each head is the hunt going on around you;
     each body is Daisy, in Jon's words (ruling 11b). None is about the maths,
     and none is about William or the students. */
  wrongLines: [
    { head: 'Daisy checks her sheet and pulls a face. Not that one.',
      body: '&ldquo;One time I got so lost I ended up in the staff room.&rdquo;' },
    { head: 'A bell goes somewhere. The corridors fill up, then empty again.',
      body: '&ldquo;There was the time I accidentally sneezed my pencil at a teacher.&rdquo;' },
    { head: 'The clock in the hall is further on than you&rsquo;d like.',
      body: '&ldquo;Did you know there&rsquo;s a school cat? His name&rsquo;s Mr Furrypants.&rdquo;' },
    { head: 'Daisy crosses something out, and smiles anyway.',
      body: '&ldquo;Come on guys, you can do this.&rdquo;' }
  ],

  objects: [
    { id: 'map', name: 'The school map', where: 'on an easel by the stage in the hall',
      clue: 'A big map of the whole school, every building drawn on a grid. The grid lines are numbered along ' +
            'the bottom and up the side, counting from the bottom-left corner. The library is the little open ' +
            'book, drawn where two grid lines cross: <b>{{map.y}} up</b> and <b>{{map.x}} along</b>.' },
    { id: 'rose', name: 'The compass rose', where: 'set into the library carpet',
      clue: 'Set into the carpet in front of the desk: north at the top and then, going round clockwise, ' +
            'north-east, east, south-east, south, south-west, west and north-west.' },
    { id: 'bibby-card', name: 'Bibby’s directions', where: 'on a card she slides across the library desk',
      clue: 'In very neat capitals: <b>FACE {{dir.fromU}}. YOUR NEXT STOP IS {{dir.toU}}. TURN CLOCKWISE.</b> ' +
            'Signed B. PHILE, and underlined once, exactly.' },
    { id: 'timetable', name: 'William’s timetable', where: 'clipped to his clipboard',
      clue: 'TASTER LESSON: SCIENCE. Starts at <b>{{tt.start}}</b>. Lasts <b>{{tt.m}} minutes</b>. Underneath, ' +
            'in a teacher&rsquo;s writing: <i>please collect from the lab door when the lesson ends</i>.' },
    { id: 'tray', name: 'William’s tray', where: 'in the canteen queue',
      clue: 'On the tray: {{till.i1}}, <b>{{till.p1}}</b>; {{till.i2}}, <b>{{till.p2}}</b>; and {{till.i3}}, ' +
            '<b>{{till.p3}}</b>. Every price is on a sticker.' },
    { id: 'lunch-card', name: 'William’s lunch card', where: 'in his hand, held out to the till',
      clue: 'LUNCH CARD. Topped up this morning with <b>five pounds</b>. The till takes off what lunch costs and ' +
            'keeps the rest on the card.' },
    { id: 'lost-property', name: 'Lost property', where: 'a box by the hall doors', clue: null,
      flavour: 'Odd socks, one football boot, a recorder, and a coat that has been here so long it looks like ' +
               'part of the furniture. Nobody ever comes back for anything.' },
    { id: 'trolley', name: 'The returns trolley', where: 'beside the library desk', clue: null,
      flavour: 'Every book on it spine out, in order, and level with the edge of the shelf. Nobody would dare put ' +
               'one back wrong.' }
  ],

  locks: [
    {
      id: 'school-map-coordinates',
      key: 'map',
      grade: 1,
      name: 'The hall map',
      brief: 'Daisy&rsquo;s clue card for the hall says: FIND THE LIBRARY ON THE MAP. WRITE ITS COORDINATES AS A ' +
             'CODE: NO BRACKETS, NO COMMA. The map is on an easel by the stage, and every group in the hall is ' +
             'crowded round it.',
      instrument: { kind: 'keypad', label: 'LIBRARY: COORDINATES AS A CODE', maxDigits: 2, verb: 'Write it in' },
      variants: [
        {
          "x": 3,
          "y": 7,
          "answer": 37,
          "miss": 73
        },
        {
          "x": 6,
          "y": 2,
          "answer": 62,
          "miss": 26
        },
        {
          "x": 8,
          "y": 4,
          "answer": 84,
          "miss": 48
        },
        {
          "x": 2,
          "y": 9,
          "answer": 29,
          "miss": 92
        },
        {
          "x": 4,
          "y": 6,
          "answer": 46,
          "miss": 64
        },
        {
          "x": 9,
          "y": 3,
          "answer": 93,
          "miss": 39
        },
        {
          "x": 7,
          "y": 1,
          "answer": 71,
          "miss": 17
        },
        {
          "x": 6,
          "y": 8,
          "answer": 68,
          "miss": 86
        },
        {
          "x": 2,
          "y": 4,
          "answer": 24,
          "miss": 42
        },
        {
          "x": 4,
          "y": 9,
          "answer": 49,
          "miss": 94
        }
      ],
      missTitle: 'Daisy has seen this one before.',
      missSays: '&ldquo;Ugh, I did that! Along the corridor first, then up the stairs.&rdquo;',
      hints: [
        'Find the little open book on the map, and the two grid lines that cross where it is drawn.',
        'Coordinates always go across first, then up.',
        'The code is the two coordinates written next to each other, with no brackets and no comma.'
      ],
      solve: 'The library is where grid line {{map.x}} along crosses grid line {{map.y}} up, so its coordinates ' +
             'are ({{map.x}}, {{map.y}}): across first, then up. The code is <b>{{map.answer}}</b>.',
      onOpen: 'Daisy ticks the box: the library, found. At the edge of the crowd, standing much too close to the ' +
              'map, is William. He drifted off to look for it on his own and got as far as the map. When you call ' +
              'him, he comes.'
    },
    {
      id: 'library-compass-turn',
      key: 'dir',
      grade: 1,
      name: 'Bibby’s directions',
      brief: 'The library is silent, and Mrs Barb Phile, the librarian, whom every student calls Bibby, intends ' +
             'to keep it that way. She does not give directions out loud. She writes them on a card, slides it ' +
             'across the desk and goes back to her shelves. You find William in the reading corner with a book: ' +
             'he slipped away from the group looking for somewhere quiet, and Bibby, who will make an exception ' +
             'for a bookworm, has let him stay. Stand on the compass rose and set the dial to the turn on her ' +
             'card.',
      instrument: { kind: 'dial', label: 'TURN CLOCKWISE', min: 0, max: 360, step: 45, decimals: 0,
                    unit: '°', start: 0, sweep: 360, wedge: true, verb: 'Turn' },
      variants: [
        {
          "from": "south",
          "to": "west",
          "steps": 2,
          "answer": 90,
          "miss": 270,
          "fromU": "SOUTH",
          "toU": "WEST",
          "whole": 360,
          "eighth": 45
        },
        {
          "from": "north",
          "to": "north-west",
          "steps": 7,
          "answer": 315,
          "miss": 45,
          "fromU": "NORTH",
          "toU": "NORTH-WEST",
          "whole": 360,
          "eighth": 45
        },
        {
          "from": "north-east",
          "to": "north-west",
          "steps": 6,
          "answer": 270,
          "miss": 90,
          "fromU": "NORTH-EAST",
          "toU": "NORTH-WEST",
          "whole": 360,
          "eighth": 45
        },
        {
          "from": "east",
          "to": "south-west",
          "steps": 3,
          "answer": 135,
          "miss": 225,
          "fromU": "EAST",
          "toU": "SOUTH-WEST",
          "whole": 360,
          "eighth": 45
        },
        {
          "from": "south-east",
          "to": "north",
          "steps": 5,
          "answer": 225,
          "miss": 135,
          "fromU": "SOUTH-EAST",
          "toU": "NORTH",
          "whole": 360,
          "eighth": 45
        },
        {
          "from": "south-west",
          "to": "west",
          "steps": 1,
          "answer": 45,
          "miss": 315,
          "fromU": "SOUTH-WEST",
          "toU": "WEST",
          "whole": 360,
          "eighth": 45
        },
        {
          "from": "west",
          "to": "north",
          "steps": 2,
          "answer": 90,
          "miss": 270,
          "fromU": "WEST",
          "toU": "NORTH",
          "whole": 360,
          "eighth": 45
        },
        {
          "from": "north-west",
          "to": "south-west",
          "steps": 6,
          "answer": 270,
          "miss": 90,
          "fromU": "NORTH-WEST",
          "toU": "SOUTH-WEST",
          "whole": 360,
          "eighth": 45
        }
      ],
      missTitle: 'Daisy looks at the dial, then at the compass rose.',
      missSays: '&ldquo;Other way! Clockwise, like the hands on a clock. I always forget too.&rdquo;',
      hints: [
        'Stand facing the way the card says, then turn the way a clock&rsquo;s hands go until you face your next ' +
        'stop.',
        'A whole turn is {{dir.whole}}&deg;. There are eight compass points round the rose, so each step from ' +
        'one point to the next is {{dir.eighth}}&deg;.',
        'Count the steps clockwise from where you face to your next stop, then multiply by {{dir.eighth}}.'
      ],
      solve: 'From {{dir.from}} to {{dir.to}} is {{dir.steps}} steps clockwise round the rose. Each step is ' +
             '{{dir.eighth}}&deg;, so the turn is {{dir.steps}} &times; {{dir.eighth}} = ' +
             '<b>{{dir.answer}}&deg;</b>.',
      onOpen: 'You turn, and there is the door to the science corridor, exactly where the card said. Bibby does ' +
              'not look up, but she lets William take the book with him. He marks his page and comes with you.'
    },
    {
      id: 'taster-lesson-end-time',
      key: 'tt',
      grade: 1,
      name: 'William’s lesson',
      brief: 'William&rsquo;s card has something the rest of yours don&rsquo;t: a taster lesson, on his own, in ' +
             'a lab he has never seen. He has gone in. Your clue card says to be at the lab door the moment the ' +
             'lesson ends, so nobody walks off without him. Write down when that is. The keypad has no colon, so ' +
             'type the four digits of the time on the twenty-four-hour clock.',
      instrument: { kind: 'keypad', label: 'LESSON ENDS (NO COLON)', maxDigits: 4, verb: 'Write the time' },
      variants: [
        {
          "hh": 10,
          "mm": 35,
          "m": 55,
          "answer": 1130,
          "miss": 1090,
          "start": "10:35",
          "end": "11:30",
          "next": "11:00",
          "tohour": 25,
          "rest": 30,
          "hourmins": 60
        },
        {
          "hh": 10,
          "mm": 15,
          "m": 50,
          "answer": 1105,
          "miss": 1065,
          "start": "10:15",
          "end": "11:05",
          "next": "11:00",
          "tohour": 45,
          "rest": 5,
          "hourmins": 60
        },
        {
          "hh": 10,
          "mm": 25,
          "m": 45,
          "answer": 1110,
          "miss": 1070,
          "start": "10:25",
          "end": "11:10",
          "next": "11:00",
          "tohour": 35,
          "rest": 10,
          "hourmins": 60
        },
        {
          "hh": 11,
          "mm": 25,
          "m": 45,
          "answer": 1210,
          "miss": 1170,
          "start": "11:25",
          "end": "12:10",
          "next": "12:00",
          "tohour": 35,
          "rest": 10,
          "hourmins": 60
        },
        {
          "hh": 11,
          "mm": 20,
          "m": 45,
          "answer": 1205,
          "miss": 1165,
          "start": "11:20",
          "end": "12:05",
          "next": "12:00",
          "tohour": 40,
          "rest": 5,
          "hourmins": 60
        },
        {
          "hh": 11,
          "mm": 30,
          "m": 50,
          "answer": 1220,
          "miss": 1180,
          "start": "11:30",
          "end": "12:20",
          "next": "12:00",
          "tohour": 30,
          "rest": 20,
          "hourmins": 60
        },
        {
          "hh": 11,
          "mm": 5,
          "m": 55,
          "answer": 1200,
          "miss": 1160,
          "start": "11:05",
          "end": "12:00",
          "next": "12:00",
          "tohour": 55,
          "rest": 0,
          "hourmins": 60
        },
        {
          "hh": 10,
          "mm": 20,
          "m": 55,
          "answer": 1115,
          "miss": 1075,
          "start": "10:20",
          "end": "11:15",
          "next": "11:00",
          "tohour": 40,
          "rest": 15,
          "hourmins": 60
        },
        {
          "hh": 10,
          "mm": 30,
          "m": 50,
          "answer": 1120,
          "miss": 1080,
          "start": "10:30",
          "end": "11:20",
          "next": "11:00",
          "tohour": 30,
          "rest": 20,
          "hourmins": 60
        },
        {
          "hh": 10,
          "mm": 40,
          "m": 55,
          "answer": 1135,
          "miss": 1095,
          "start": "10:40",
          "end": "11:35",
          "next": "11:00",
          "tohour": 20,
          "rest": 35,
          "hourmins": 60
        }
      ],
      missTitle: 'That time isn&rsquo;t on any clock.',
      missSays: '&ldquo;Hang on, that&rsquo;s not a real time! There&rsquo;s sixty minutes in an hour, not a ' +
                'hundred.&rdquo;',
      hints: [
        'Count on from the start time in two jumps: first to the next o&rsquo;clock, then the minutes that are ' +
        'left.',
        'There are {{tt.hourmins}} minutes in an hour.',
        'Write the end time on the twenty-four-hour clock and type its four digits, without the colon.'
      ],
      solve: '{{tt.start}} to {{tt.next}} is {{tt.tohour}} minutes. That leaves {{tt.m}} &minus; {{tt.tohour}} ' +
             '= {{tt.rest}} minutes, so the lesson ends at {{tt.end}}: type <b>{{tt.answer}}</b>.',
      onOpen: 'The lab door opens on the dot. William is first out, goggle marks round his eyes, looking for you, ' +
              'and you are there. This time he is smiling.'
    },
    {
      id: 'lunch-card-change',
      key: 'till',
      grade: 1,
      name: 'The lunch card',
      brief: 'The last stop on the card is lunch, and the canteen is loud. William has a lunch card and a tray ' +
             'with three things on it, and he&rsquo;s too nervous to ask how much he will have left. The card ' +
             'says the till keeps the rest. Work it out for him before he gets to the front: how much will be ' +
             'left on his card, in pence?',
      instrument: { kind: 'keypad', label: 'LEFT ON THE CARD (PENCE)', maxDigits: 3, verb: 'Write it in' },
      variants: [
        {
          "card": 500,
          "answer": 135,
          "miss": 265,
          "i1": "a pasta pot",
          "p1": "&pound;1.85",
          "i2": "a fruit cup",
          "p2": "60p",
          "i3": "a carton of milk",
          "p3": "&pound;1.20",
          "total": 365,
          "totalP": "&pound;3.65"
        },
        {
          "card": 500,
          "answer": 255,
          "miss": 345,
          "i1": "a sandwich",
          "p1": "&pound;1.75",
          "i2": "an apple",
          "p2": "40p",
          "i3": "a bottle of water",
          "p3": "30p",
          "total": 245,
          "totalP": "&pound;2.45"
        },
        {
          "card": 500,
          "answer": 85,
          "miss": 115,
          "i1": "a slice of pizza",
          "p1": "&pound;2.10",
          "i2": "a smoothie",
          "p2": "&pound;1.35",
          "i3": "a cookie",
          "p3": "70p",
          "total": 415,
          "totalP": "&pound;4.15"
        },
        {
          "card": 500,
          "answer": 175,
          "miss": 225,
          "i1": "a jacket potato",
          "p1": "&pound;1.90",
          "i2": "a yoghurt",
          "p2": "85p",
          "i3": "a carton of apple juice",
          "p3": "50p",
          "total": 325,
          "totalP": "&pound;3.25"
        },
        {
          "card": 500,
          "answer": 215,
          "miss": 385,
          "i1": "a bowl of soup",
          "p1": "&pound;1.55",
          "i2": "a bread roll",
          "p2": "40p",
          "i3": "a rice pudding",
          "p3": "90p",
          "total": 285,
          "totalP": "&pound;2.85"
        },
        {
          "card": 500,
          "answer": 65,
          "miss": 135,
          "i1": "a hot dinner",
          "p1": "&pound;2.45",
          "i2": "a flapjack",
          "p2": "80p",
          "i3": "a milkshake",
          "p3": "&pound;1.10",
          "total": 435,
          "totalP": "&pound;4.35"
        },
        {
          "card": 500,
          "answer": 125,
          "miss": 275,
          "i1": "a wrap",
          "p1": "&pound;2.05",
          "i2": "a bag of crisps",
          "p2": "55p",
          "i3": "a carton of orange juice",
          "p3": "&pound;1.15",
          "total": 375,
          "totalP": "&pound;3.75"
        },
        {
          "card": 500,
          "answer": 235,
          "miss": 365,
          "i1": "a cheese toastie",
          "p1": "&pound;1.50",
          "i2": "a carton of squash",
          "p2": "70p",
          "i3": "a biscuit",
          "p3": "45p",
          "total": 265,
          "totalP": "&pound;2.65"
        },
        {
          "card": 500,
          "answer": 105,
          "miss": 295,
          "i1": "a plate of curry and rice",
          "p1": "&pound;2.25",
          "i2": "a piece of garlic bread",
          "p2": "60p",
          "i3": "a carton of fruit juice",
          "p3": "&pound;1.10",
          "total": 395,
          "totalP": "&pound;3.95"
        },
        {
          "card": 500,
          "answer": 275,
          "miss": 325,
          "i1": "a pasta bake",
          "p1": "&pound;1.40",
          "i2": "a salad pot",
          "p2": "50p",
          "i3": "a banana",
          "p3": "35p",
          "total": 225,
          "totalP": "&pound;2.25"
        }
      ],
      missTitle: 'Daisy has done exactly that.',
      missSays: '&ldquo;I did exactly that in maths last year. You can&rsquo;t just take the small number off the ' +
                'big one.&rdquo;',
      hints: [
        'Add up the three prices first, all in pence.',
        'Then take that total away from the card&rsquo;s {{till.card}}p.',
        'Line the numbers up in columns. Where the top digit is smaller, exchange from the column to its left.'
      ],
      solve: '{{till.p1}} + {{till.p2}} + {{till.p3}} = {{till.totalP}}, which is {{till.total}}p. ' +
             '{{till.card}}p &minus; {{till.total}}p = <b>{{till.answer}}p</b> left on the card.',
      onOpen: 'The till beeps and shows exactly what you said. William looks at the screen, then at you, and says ' +
              'the most he has said all morning: &ldquo;Thanks.&rdquo;'
    }
  ]
};
