/* Room data for "roll-for-initiative" — shared by index.html (the room, live but unlisted) and
   teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand.

   BUILT 2026-10-15 (contract DND-ROOM-BUILD) from the draft Jon approved with six changes the same day
   (docs/escape-room-drafts/dnd-club-draft.md, merged in #415; contract saved as
   docs/handover/contracts/2026-10-15-dnd-room-build.md). A new Core room: the school D&D club, the students
   as the DMs teaching their teacher her first game. Mrs Rogers is a real teacher and speaks only in this room,
   and only the lines she approved, word for word: the start line (end of the hook), lock 1's open, lock 2's
   open, and the ending and character choice (the win). No student is named anywhere. Strictmane is the BBEG,
   invented, mapping to no real person; Mr Strictman is a cameo, recognised and never speaking.

   CREDIT: "Built from a teacher's idea. Thank you, Mrs Rogers." (teacher page footer.) Mrs Rogers has agreed to
   her real name being used: consent recorded by Jon, 15 Oct 2026 (docs/handover/home.md).

   STATUS: LIVE BUT UNLISTED, not released. The room is playable at /escape-rooms/roll-for-initiative/ for Jon's
   play-test and Mrs Rogers's preview: noindex, analytics off, linked from nowhere (not in the hub, the front
   page or the sitemap). Release is a separate instruction from Jon.

   GRADES (canon §11.3, ESCAPE-DIFFICULTY): the gate, a probability from the faces of a twenty-sided die with
   bonuses and a penalty (4); the plans, a scale drawing and units (3); the fireball, the area of a circle (4).
   The hardest lock makes the room ★★ Core. There is no star field and no label here: the stars are derived.

   NOTE — object `id`s are load-bearing: teacher.html maps clues to locks by id in its `clueMap`. `mug` and
   `sign` are the two blanks.

   NOTE — not one numeral is typed into a clue string: every DC, bonus, penalty, scale, length, square size and
   radius is a token. The only figures in the prose outside tokens are "two point six centimetres" (Strictmane's
   own line, in words), "Form R-1" (a form's name, in lock 3's open, never in a clue) and "fifth level" and
   "twenty-sided", in words. "nat 20" is `nat {{gate.die}}`. Form G has no number on purpose (Jon, 15 Oct 2026):
   a numbered form would plant a false clue beside the DCs.

   NOTE — token names are distinct across locks: `plan.sq` is the club's square size (2 m, in every set);
   the circle's radius in squares is `fb.rsq`; there is no `fb.sq` and no `sqr` token.

   RULE — the fail picture is the end of the club, which is only true at time-out. Never set `missArt` on any
   lock in this room (the kiln, comic and library rule).

   RULE — the hint ladders are generic: every student sees them, so none assumes a particular mistake. The one
   misconception on each lock is handled by missTitle and missSays alone, and no wrong-entry response gives the
   answer (Jon, 15 Oct 2026).

   ART: docs/art/roll-for-initiative-{scene,fail,win}.webp, Jon's three pictures filed through
   scripts/strip-gen-watermark.py. The alts below match them. */
window.ROOM = {
  slug: 'escape-roll-for-initiative',
  title: 'Roll for Initiative',
  level: 'gcse',
  minutes: 15,
  penalty: 45,
  art: 'roll-for-initiative',
  sceneAlt: 'A school classroom after the last lesson, rain running down the tall window. Four tables are pushed together with a gridded battle mat across them, three drilled blocks of small green goblin figures standing in ranks and a pair of figures in the middle. Character sheets, pencils and handfuls of dice sit at the places. A cardboard folding screen stands at the far side, a mug of tea and a tall pile of marking on the right, and on the brick wall by the whiteboard a blank pinboard.',
  failAlt: 'The same classroom, dim, with the rain still falling. Chairs are stacked upside down on the tables, the battle mat is rolled up under an elastic band, and the dice and goblin figures are boxed in clear tubs. The folding screen lies flat on a loose pile of papers.',
  winAlt: 'The same classroom, brighter. On the battle mat the goblins lie scattered and knocked over around a scorched black ring. On the nearest character sheet a twenty-sided die shows its top number beside a small drawing of a flame. The tea mug and the marking stand to the right.',

  hook: 'Mrs Rogers runs the school D&amp;D club. It exists because you asked her to start it. She has never ' +
        'played. She has watched you do it for weeks, nodded politely at the dice, and marked a great deal of ' +
        'homework at the end of the table.<br><br>' +
        'Tonight you are the DMs. You explain to her that a DM is the player who runs the game: you describe the ' +
        'world, you play everybody in it, and you teach the rules to anyone who needs them. She is the new ' +
        'player. You&rsquo;ve built her a short adventure, and because making a character from nothing is a lot ' +
        'to ask on a first night, you have handed her a ready-made one: an adventurer with golden curls, in ' +
        'battered blue plate armour, engraved all over.<br><br>' +
        'She sits down with a mug of tea and a pile of marking, picks up a twenty-sided die and turns it ' +
        'over.<br><br>' +
        '&ldquo;Right. I&rsquo;ve got my tea, I&rsquo;ve got my marking, and I&rsquo;ve got&hellip; a ' +
        'twenty-sided dice. Remind me why there are twenty sides?&rdquo;',
  brief: 'Every adventure needs a villain. You tell her that the one in charge, the big bad evil guy, is called ' +
         'the BBEG, and yours is Commandant Strictmane: a tyrant in starched robes who has built a fortress and ' +
         'measured every inch of it. He has put three obstacles between her adventurer and the end of the ' +
         'story: a gate, a corridor and, at the end, a grid of his goblins. Each one comes down to a number she ' +
         'has to be shown how to find.<br><br>' +
         'When you get one right, she will start to want the next. That is what you are here for. The club ends ' +
         'when the caretaker comes round to stack the chairs, and every wrong setting costs you time.',
  /* There is no `fail` slot: the engine shows `stakes` after "If you get it
     wrong." on the start screen and after "And so:" on the time-out screen, so
     the failure is written here and reads after both. */
  stakes: 'The caretaker puts the chairs up on the tables, rolls up the mat and boxes the goblins. Mrs Rogers ' +
          'finishes her tea, gathers her marking and says, kindly, that it was lovely to try something new. She ' +
          'does not say next week. The club goes back to being something she watches from the end of the table.',
  win: 'The last goblin helmet stops smouldering. Mrs Rogers looks at the mat, at the scorch mark, at the ' +
       'goblins lying every which way, and then at you, as if she has only just noticed that the room is full ' +
       'of people who know exactly what they&rsquo;re doing.<br><br>' +
       '&ldquo;Same time next week? I want to be a wizard. One that throws fireballs.&rdquo;<br><br>' +
       '&ldquo;You can&rsquo;t cast fireball until fifth level, Miss.&rdquo;<br><br>' +
       '&ldquo;Then I suppose we&rsquo;d better play every week.&rdquo;<br><br>' +
       'She slides the golden-curled adventurer in its battered blue armour to the edge of the mat and picks up ' +
       'a blank character sheet.<br><br>' +
       '&ldquo;Miss, you&rsquo;d definitely be a barbarian.&rdquo;<br><br>' +
       '&ldquo;Everyone keeps telling me what I&rsquo;d be. Dwarf. Wizard. Final answer.&rdquo; She writes ' +
       'DWARF in the species box and WIZARD in the class box, and then, after a beat: &ldquo;Don&rsquo;t tell ' +
       'my husband he was right.&rdquo;',

  /* Wrong-entry lines, indexed by how many wrong settings have been made so
     far; the last one repeats (the joke: he just keeps coming). Each head is
     the room; each body is Strictmane, gloating about the lock from beyond
     it. None of them is aimed at the students. Line 1 is the Car Trap voice
     moved into the fortress, with its figure in words. */
  wrongLines: [
    { head: 'The setting clears with a clunk that echoes down a stone corridor.',
      body: 'Beyond the lock, the scratch of a pen on a plan. &ldquo;This corridor is two point six centimetres ' +
            'narrower than the plans. This is not how it is done in MY fortress.&rdquo;' },
    { head: 'Nothing opens. The goblin on the gate stamps a form, very slowly, and slides it back across the table.',
      body: '&ldquo;Form G is incomplete. Form G is always incomplete. That is rather the point of Form G.&rdquo;' },
    { head: 'The setting slides back to where it was.',
      body: '&ldquo;Every gate in this fortress is inspected at dawn. Every lock is measured twice. No intruder ' +
            'has ever got through all three. I have the paperwork to prove it.&rdquo;' },
    { head: 'Another one. The pen is nearer than it was.',
      body: '&ldquo;Next form.&rdquo;' }
  ],

  objects: [
    { id: 'charsheet', name: 'Her character sheet', where: 'at her place at the table',
      clue: '<b>ADVENTURER.</b> Species: human <i>(what kind of person she is: human, dwarf, elf)</i>. Class: ' +
            'fighter <i>(what she does: fighter, wizard, barbarian)</i>. Golden curls, battered blue plate ' +
            'armour, engraved. <b>Strength (Athletics): +{{gate.str}}</b> <i>(Strength is how strong she is; ' +
            'Athletics is what she uses it for: climbing, jumping)</i>. <b>Charisma (Persuasion): ' +
            '+{{gate.cha}}</b> <i>(Charisma is how well she gets on with people; Persuasion is talking them ' +
            'round)</i>.' },
    { id: 'dmscreen', name: 'The DM screen', where: 'standing at the far side of the table',
      clue: '<b>THE GATE.</b> <i>Climb the wall</i>: Strength (Athletics), <b>DC {{gate.dcc}}</b>. <i>Talk to ' +
            'the guard</i>, who wants Form G in triplicate: Charisma (Persuasion), <b>DC {{gate.dcp}}</b>. ' +
            '<i>(DC means difficulty class: the number the roll has to reach.)</i> To make a check, roll the ' +
            'twenty-sided die, add your bonus, and <b>meet or beat the DC</b>. Every face is equally likely.' },
    { id: 'window', name: 'The window', where: 'over the radiator',
      clue: 'Rain runs down the glass: proper drizzle, the kind that gets into everything. A card is stuck to ' +
            'the frame in the club&rsquo;s handwriting: <b>HOUSE RULE: WET WEATHER. &minus;{{gate.wet}} to ' +
            'Strength (Athletics) checks.</b>' },
    { id: 'plans', name: 'Strictmane’s plans', where: 'folded inside the marking pile, where you hid them so she wouldn’t peek',
      clue: '<b>DRAWN TO REGULATION.</b> Scale <b>1 : {{plan.S}}</b>. Main corridor on the plan: ' +
            '<b>{{plan.L}} cm.</b> Signed, in very straight capitals: COMMANDANT STRICTMANE.' },
    { id: 'mat', name: 'The battle mat', where: 'spread across the tables',
      clue: 'In pen along the edge, the club&rsquo;s own rule: <b>ONE SQUARE = {{plan.sq}} m.</b> <i>(' +
            '&ldquo;Homebrew&rdquo;: a rule the club made up and the rulebooks don&rsquo;t have.)</i>' },
    { id: 'dice', name: 'The dice', where: 'in a heap beside the mat, a spell card under them',
      clue: '<b>FIREBALL.</b> <i>AoE: area of effect, everything inside the blast.</i> The blast is a ' +
            '<b>circle, radius {{fb.r}} m</b>, centred on the target.' },
    { id: 'mug', name: 'The tea mug', where: 'by the marking', clue: null,
      flavour: 'Her tea, gone lukewarm. The pile beside it has not moved. A tea ring has appeared on the top ' +
               'essay.' },
    { id: 'sign', name: 'The blank sign', where: 'pinned to the brick wall by the whiteboard', clue: null,
      flavour: 'A pinboard with nothing on it but a label in the corner in very straight capitals: NOTICES. ' +
               'Nothing has been noticed.' }
  ],

  locks: [
    {
      id: 'gate-modifiers-probability',
      key: 'gate',
      grade: 4,
      name: 'The gate',
      brief: 'The fortress gate is shut, and it is drizzling. There are two ways through: climb the wall, or ' +
             'talk to the guard and his paperwork. Her adventurer can try either. Work out which path she is ' +
             'more likely to pass, and tell the DM its chance of success, as a percentage.',
      instrument: { kind: 'keypad', label: 'CHANCE OF SUCCESS (%)', maxDigits: 3, verb: 'Enter chance' },
      variants: [
        {
          "dcc": 12,
          "str": 2,
          "wet": 2,
          "dcp": 14,
          "cha": 3,
          "pc": 45,
          "pp": 50,
          "answer": 50,
          "miss": 55,
          "die": 20,
          "needC": 12,
          "needP": 11,
          "chC": 9,
          "chP": 10
        },
        {
          "dcc": 11,
          "str": 1,
          "wet": 3,
          "dcp": 13,
          "cha": 1,
          "pc": 40,
          "pp": 45,
          "answer": 45,
          "miss": 55,
          "die": 20,
          "needC": 13,
          "needP": 12,
          "chC": 8,
          "chP": 9
        },
        {
          "dcc": 11,
          "str": 2,
          "wet": 2,
          "dcp": 13,
          "cha": 3,
          "pc": 50,
          "pp": 55,
          "answer": 55,
          "miss": 60,
          "die": 20,
          "needC": 11,
          "needP": 10,
          "chC": 10,
          "chP": 11
        },
        {
          "dcc": 13,
          "str": 1,
          "wet": 2,
          "dcp": 14,
          "cha": 1,
          "pc": 35,
          "pp": 40,
          "answer": 40,
          "miss": 45,
          "die": 20,
          "needC": 14,
          "needP": 13,
          "chC": 7,
          "chP": 8
        },
        {
          "dcc": 13,
          "str": 1,
          "wet": 3,
          "dcp": 16,
          "cha": 2,
          "pc": 30,
          "pp": 35,
          "answer": 35,
          "miss": 45,
          "die": 20,
          "needC": 15,
          "needP": 14,
          "chC": 6,
          "chP": 7
        },
        {
          "dcc": 14,
          "str": 1,
          "wet": 3,
          "dcp": 16,
          "cha": 1,
          "pc": 25,
          "pp": 30,
          "answer": 30,
          "miss": 40,
          "die": 20,
          "needC": 16,
          "needP": 15,
          "chC": 5,
          "chP": 6
        },
        {
          "dcc": 11,
          "str": 3,
          "wet": 2,
          "dcp": 12,
          "cha": 3,
          "pc": 55,
          "pp": 60,
          "answer": 60,
          "miss": 65,
          "die": 20,
          "needC": 10,
          "needP": 9,
          "chC": 11,
          "chP": 12
        },
        {
          "dcc": 10,
          "str": 3,
          "wet": 2,
          "dcp": 11,
          "cha": 3,
          "pc": 60,
          "pp": 65,
          "answer": 65,
          "miss": 70,
          "die": 20,
          "needC": 9,
          "needP": 8,
          "chC": 12,
          "chP": 13
        },
        {
          "dcc": 10,
          "str": 4,
          "wet": 2,
          "dcp": 11,
          "cha": 4,
          "pc": 65,
          "pp": 70,
          "answer": 70,
          "miss": 75,
          "die": 20,
          "needC": 8,
          "needP": 7,
          "chC": 13,
          "chP": 14
        }
      ],
      missTitle: '{{gate.miss}}% is the climb on a dry day.',
      missSays: '{{gate.miss}}% is how often she&rsquo;d get over the wall if it weren&rsquo;t raining. The card ' +
                'on the window is there for a reason.',
      hints: [
        'Have you looked outside? It&rsquo;s drizzling.',
        'A bonus helps her. Does she need a higher roll or a lower one?',
        'Count the rolls that succeed on each path, out of {{gate.die}}.'
      ],
      solve: 'Climb: the penalty takes {{gate.wet}} off her bonus, so she needs {{gate.needC}} or more on the ' +
             'die, which is {{gate.chC}} faces out of {{gate.die}}, {{gate.pc}}%. Persuade: she needs ' +
             '{{gate.needP}} or more, which is {{gate.chP}} out of {{gate.die}}, {{gate.pp}}%. Persuasion is ' +
             'the better path, at <b>{{gate.answer}}%</b>.',
      onOpen: 'She rolls for the guard and the die stops on a nat {{gate.die}}: a natural twenty, the die itself ' +
              'showing the top number, no adding needed. The guard salutes and stamps her Form G. Mrs Rogers ' +
              'looks at the die, then at the two DCs on the screen. &ldquo;Hang on, so the lower number ' +
              'isn&rsquo;t the better bet? That&rsquo;s actually quite clever.&rdquo;'
    },
    {
      id: 'fortress-plan-scale',
      key: 'plan',
      grade: 3,
      name: 'Strictmane’s plans',
      brief: 'The plans say the main corridor is drawn to regulation, at the Commandant&rsquo;s scale. The party ' +
             'has to walk it. The club moves in squares on the mat, and the club has its own rule for how big a ' +
             'square is. Tell the DM how many squares the party must move.',
      instrument: { kind: 'keypad', label: 'SQUARES TO MOVE', maxDigits: 4, verb: 'Enter squares' },
      variants: [
        {
          "S": 500,
          "L": 4,
          "sq": 2,
          "answer": 10,
          "miss": 1000,
          "cm": 2000,
          "real": 20,
          "cmperm": 100
        },
        {
          "S": 100,
          "L": 8,
          "sq": 2,
          "answer": 4,
          "miss": 400,
          "cm": 800,
          "real": 8,
          "cmperm": 100
        },
        {
          "S": 250,
          "L": 4,
          "sq": 2,
          "answer": 5,
          "miss": 500,
          "cm": 1000,
          "real": 10,
          "cmperm": 100
        },
        {
          "S": 250,
          "L": 8,
          "sq": 2,
          "answer": 10,
          "miss": 1000,
          "cm": 2000,
          "real": 20,
          "cmperm": 100
        },
        {
          "S": 500,
          "L": 2,
          "sq": 2,
          "answer": 5,
          "miss": 500,
          "cm": 1000,
          "real": 10,
          "cmperm": 100
        },
        {
          "S": 500,
          "L": 6,
          "sq": 2,
          "answer": 15,
          "miss": 1500,
          "cm": 3000,
          "real": 30,
          "cmperm": 100
        },
        {
          "S": 500,
          "L": 8,
          "sq": 2,
          "answer": 20,
          "miss": 2000,
          "cm": 4000,
          "real": 40,
          "cmperm": 100
        }
      ],
      missTitle: '{{plan.miss}} comes from squares counted straight off the centimetres.',
      missSays: 'The scale gives centimetres, and the mat is measured in metres. {{plan.miss}} would be a ' +
                'corridor longer than the whole fortress.',
      hints: [
        'Did you use the Commandant&rsquo;s scale?',
        'There are {{plan.cmperm}} cm in a metre.',
        'One square on the mat is {{plan.sq}} m. How many fit along the corridor?'
      ],
      solve: 'The corridor is {{plan.L}} cm on the plan and the scale is 1 : {{plan.S}}, so it is ' +
             '{{plan.L}} &times; {{plan.S}} = {{plan.cm}} cm. That is {{plan.real}} m. One square is ' +
             '{{plan.sq}} m, so the party moves <b>{{plan.answer}} squares</b>.',
      onOpen: 'The corridor&rsquo;s plan flips over in the dark and every square of it is exactly where it ' +
              'should be. Somewhere beyond it a pen stops writing. Mrs Rogers leans in. &ldquo;Is that&hellip; ' +
              'is that Mr Strictman? You&rsquo;ve put Mr Strictman in the game? I&rsquo;m totally in.&rdquo;'
    },
    {
      id: 'fireball-circle-area',
      key: 'fb',
      grade: 4,
      name: 'The fireball',
      brief: 'The goblins have seen you. &ldquo;Roll for initiative,&rdquo; you tell her: it&rsquo;s how a fight ' +
             'decides who goes first. Strictmane&rsquo;s goblins stand drilled in a grid, one square each, in ' +
             'perfect ranks, and she goes first. The fireball is an AoE, an area of effect: everything inside ' +
             'the blast is hit. Tell the DM how much ground it covers, to the nearest square metre.',
      instrument: { kind: 'keypad', label: 'AREA COVERED (SQUARE METRES)', maxDigits: 3, verb: 'Enter area' },
      variants: [
        {
          "r": 6,
          "answer": 113,
          "miss": 38,
          "rsq": 3,
          "exact": "113.10"
        },
        {
          "r": 4,
          "answer": 50,
          "miss": 25,
          "rsq": 2,
          "exact": "50.27"
        },
        {
          "r": 8,
          "answer": 201,
          "miss": 50,
          "rsq": 4,
          "exact": "201.06"
        },
        {
          "r": 10,
          "answer": 314,
          "miss": 63,
          "rsq": 5,
          "exact": "314.16"
        },
        {
          "r": 12,
          "answer": 452,
          "miss": 75,
          "rsq": 6,
          "exact": "452.39"
        }
      ],
      missTitle: '{{fb.miss}} is the distance round the edge.',
      missSays: '{{fb.miss}} is what you get from the length round the blast, not the ground inside it. The ' +
                'fireball fills the inside.',
      hints: [
        'The fireball covers the space inside the circle.',
        'Area uses the radius squared.',
        'Square the radius, multiply by &pi;, then round.'
      ],
      solve: 'The radius is {{fb.r}} m ({{fb.rsq}} squares at {{plan.sq}} m each). Area = &pi; &times; ' +
             'r&sup2; = &pi; &times; {{fb.r}}&sup2; = {{fb.exact}}, which is <b>{{fb.answer}} m&sup2;</b> to ' +
             'the nearest square metre. (With &pi; = 3.14 the answer is the same.)',
      onOpen: 'The fireball lands. The goblins scatter with smouldering helmets, ranks knocked flat, and ' +
              'Commandant Strictmane cries out. &ldquo;Formation! FORMATION! &hellip;Who authorised the ' +
              'fire?&rdquo; Then he straightens his starched robes. &ldquo;A tactical withdrawal. I shall be ' +
              'submitting Form R-1, requesting a rematch.&rdquo; A pause. &ldquo;In triplicate.&rdquo;'
    }
  ]
};
