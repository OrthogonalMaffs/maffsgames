/* Room data for "pe-shed-rebellion" — shared by index.html (the game) and
   teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand.

   PREMISE — corrected 2026-09-08. The flood is the tool, not the failure.
   Lungey holds the doorway and nothing moves while he is standing in it.
   Opening the sprinkler to exactly the grounds staff's limit sends him across
   the field at a sprint, too fast to take his coat with him; the coat then
   goes behind his own padlock. One failure state only — run the clock out and
   the whistle goes, cross-country happens as timetabled, and he does it dry.

   VOICE — Mr Barry Lunge, "Lungey", Head of P.E., twenty-six years. He carries
   the hook directly and the narration around him is wrapped in <em>, which the
   house CSS renders in accent weight rather than italic. He never swears and
   never insults anybody. The nostalgic aside unspools across `wrongLines` and
   never arrives anywhere. The room is a store, not a shed, and he will tell
   you so. Renamed to The P.E. Store Rebellion 08/09/2026; the slug, directory, image
   filenames, canonical link and sitemap entry stay `pe-shed-rebellion`, because the
   page has been live and indexed since 01/09 and moving it would break the URL.

   ART — instrument pictures are dropped set-wide (scene, fail and win only);
   the engine draws the live control anyway, so the `art`/`artAlt` fields are
   gone from all three locks below. The engine guards the instrument frame as
   of 2026-09-08, so a lock with no art emits no image and makes no request.

   ART COMPLETE 2026-09-08. All three pictures are the new empty-room style,
   filed at 1600x873, and all three alts describe what is actually on disk.

   The failure and victory PNGs both carried the generator's sparkle, and
   strip-gen-watermark.py did not see it — the shape test needs the whole star
   to survive thresholding and these were too soft, scoring k4=0.19 against a
   required 0.85. Inpainting them made it worse: one mark sat against the door
   frame and one on a court-line vertex, and the fill smeared both. They were
   framed out instead, which is why the two are cropped differently — the
   failure picture lost its floor and left edge because its right-hand strip is
   the coat the whole picture is about, and the victory picture lost its right
   edge and ceiling because that strip is only wall bars. Exact crops are in
   docs/escape-room-image-prompts.md.

   NOTE — object `id`s are load-bearing: teacher.html maps clues to locks by id
   in its `clueMap`. Renaming one silently breaks the teacher page. */
window.ROOM = {
  slug: 'escape-pe-shed-rebellion',
  title: 'The P.E. Store Rebellion',
  level: 'ks3',
  levelLabel: 'KS3 / GCSE',
  minutes: 15,
  penalty: 45,
  art: 'pe-shed-rebellion',
  sceneAlt: 'The inside of a breeze-block P.E. store on a wet afternoon. Bare grey blockwork with damp streaks and cobwebs in the corners, dark timber roof beams overhead, and a small metal-framed window looking out on rain and a green field with posts in the far distance. A long wooden rail of empty coat hooks runs along the back wall above two slatted benches. On the left a trestle table is stacked with traffic cones and marker discs, a heap of unwashed bibs slumped over the edge. A net sack of balls leans against the wall and muddy footballs, volleyballs and rugby balls lie scattered across the concrete floor. On the right a chipped sink with a dripping tap, a mop in a bucket and a broom against the wall.',
  failAlt: 'The inside of a breeze-block P.E. store after a cross-country run in the rain. Bare grey blockwork walls, dark timber roof beams and a small metal-framed window looking out on rain and a green field. Soaked, mud-caked kit is dumped across the concrete floor in heaps, with muddy trainers on their sides, wet socks, a mop lying in a puddle and trails of mud everywhere, faint steam rising off the piles. Coloured bibs hang over a bench at the left edge. On the rail of hooks by the door on the right, one large waxed coat hangs alone, completely dry, clean and undisturbed.',
  winAlt: 'A school sports hall with a herringbone parquet floor, wall bars along the right-hand wall and a badminton net still up. An inflatable dodgeball arena in faded red and blue stands fully inflated in the middle of the floor, full of balls, with more scattered across the parquet around it and a small electric blower still connected beside it. A trolley of stacked mats stands at the back. Rain runs down the high windows on the left, and beyond them a grey, waterlogged, completely empty playing field. In the foreground an old kettle steams on a wooden bench beside an abandoned muddy yellow cross-country bib.',

  hook: 'Right. It&rsquo;s on. It is always on.<br><br>' +
        'Four degrees is not a reason, it&rsquo;s a temperature. A bit of weather never hurt anybody &mdash; it ' +
        'builds you. You&rsquo;ll thank me. Six kilometres. Round the field, up the lane, back past the tennis ' +
        'courts, and I&rsquo;ll be counting.<br><br>' +
        'Store&rsquo;s open. It&rsquo;s a store, not a shed &mdash; I have told you lot that since Year 7. And ' +
        'it&rsquo;s not a free-for-all either &mdash; ' +
        'nobody touches anything that isn&rsquo;t a BIB, because the equipment has been walking off since ' +
        'February and I have had enough of it. Padlock goes back on the second we&rsquo;re moving.<br><br>' +
        'Fifteen minutes. Get changed.<br><br>' +
        '<em>He plants himself in the doorway with the register. Bare breeze block, one small window, mud dried ' +
        'up the walls where forty terms of filthy kit has been thrown at them, and colder inside than it is out. ' +
        'The rail of hooks along the back wall is bare. The one by the door is not &mdash; his coat hangs ' +
        'on it, waxed, enormous and bone dry.</em>',
  brief: 'There is no radiator in here and there never has been. Everything you want is forty metres away in a ' +
         'warm sports hall, and he will not leave that doorway for the weather, or the register, or you. He will ' +
         'leave it for the cricket square. The standpipe is round the gable end, out of his eyeline, and the ' +
         'override was never locked, because it never occurred to anybody that it would need to be. That is ' +
         'the one thing you can reach with him standing there. Open the sprinkler far enough to send ' +
         'him across that field at a sprint &mdash; and not one degree further, because past what the grounds ' +
         'staff are allowed on that square you have not made a diversion, you have made an incident. Then get ' +
         'the compressor set so the arena inflates instead of splitting, and get the equipment locker open. The ' +
         'dodgeballs are in the locker. Without them this is just a very large empty room.',
  stakes: 'the whistle goes and cross-country happens exactly as timetabled. Six kilometres, sideways rain, and ' +
          'kit that will not be dry by Thursday. Lungey stands at the gate in the waxed coat with a flask and ' +
          'counts you through, then counts you through again, because he always counts twice. He is not smug ' +
          'about it. That is somehow worse.',
  win: 'He goes across that field like a man half his age &mdash; no coat, no flask, nothing over the tracksuit, ' +
       'because the cricket square does not wait while you find your coat.<br><br>' +
       'By the time he has the standpipe shut off the compressor is running, and the folded nylon block in the ' +
       'corner has begun, slowly and then all at once, to become a room. The arena goes up between the badminton ' +
       'posts with a noise like a held breath. The locker gives up twelve dodgeballs and, inexplicably, a ' +
       'kettle. The coat goes back on its hook in the store, and the store gets the padlock he put on it in ' +
       'February.<br><br>' +
       'He appears in the hall doorway seven minutes later, wet through to the shoulders, and stands dripping on ' +
       'the parquet while twenty-eight people who were supposed to be running six kilometres carry on not doing ' +
       'it.<br><br>' +
       '&ldquo;Right,&rdquo; he says. &ldquo;Builds character, this.&rdquo;<br><br>' +
       'Then he gets his whistle out. &ldquo;Two teams. Bibs on. And somebody fetch my coat, I&rsquo;m not ' +
       'asking twice.&rdquo;<br><br>' +
       'He is asking twice. He asks four more times before the end of the lesson.',

  /* Wrong-entry lines, indexed by how many wrong settings have been made so
     far; the last one repeats. Lungey is not looking and never looks. The
     twenty-six-mile walk to school arrives in pieces and finishes on a line
     that then repeats for the rest of the game, which is the joke.
     WIRED 2026-09-08: the engine reads this array, indexed by st.wrongs - 1 and
     clamped to the last entry. A misconception hit consumes an index without
     printing a line, which is intended — see wrongLine() in engine.js. */
  wrongLines: [
    { head: 'Nothing gives.',
      body: 'Somewhere behind you, not looking up: &ldquo;Two minutes, you lot. Two.&rdquo;' },
    { head: 'The setting slides back to where it was.',
      body: '&ldquo;Nobody ever got round that field standing still thinking about it.&rdquo; He is not talking ' +
            'to you. He is talking to the register.' },
    { head: 'Something resets itself with a clack.',
      body: '&ldquo;I walked to this school. Twenty-six miles. No shoes.&rdquo; Nobody has asked.' },
    { head: 'Another one. The whistle is no further off than it was.',
      body: '&ldquo;&hellip;and I was grateful.&rdquo;' }
  ],

  objects: [
    { id: 'log', name: 'Groundsman’s log', where: 'hanging on a nail by the standpipe',
      clue: '&ldquo;Cricket square, watering limits. The wet patch <b>must never exceed {{arc.K}}&pi; square ' +
            'metres</b>. Any more than that and the square floods, and then we are all in trouble.&rdquo;' },
    { id: 'spec', name: 'Irrigation spec sheet', where: 'folded into a bucket in the store',
      clue: 'ST MARTHA’S GROUNDS — irrigation. <b>Rotary heads, reach {{arc.r}} m.</b> Arc adjustable in ' +
            'ten-degree steps.' },
    { id: 'clipboard', name: 'P.E. teacher’s clipboard', where: 'on a hook behind the door',
      clue: 'Scrawled on the back: &ldquo;Codes I have already used, so I stop repeating myself. ' +
            'Day {{seq.d1}} &mdash; <b>{{seq.c1}}</b>. Day {{seq.d2}} &mdash; <b>{{seq.c2}}</b>. ' +
            'Day {{seq.d3}} &mdash; <b>{{seq.c3}}</b>.&rdquo;' },
    { id: 'calendar', name: 'Wall calendar', where: 'above the kit shelves, one date ringed in biro',
      clue: 'Today is ringed, and the ring is labelled in the teacher’s handwriting: <b>day {{seq.dT}} of term</b>.' },
    { id: 'card', name: 'Laminated card', where: 'in the bottom of a kit bag',
      clue: 'COMPRESSOR — read before use. &ldquo;Pressure is <b>inversely proportional</b> to volume. ' +
            'Folded flat, the arena holds <b>{{psi.V1}} cubic metres at {{psi.P1}} psi</b>. Too much pressure ' +
            'splits the seams.&rdquo;' },
    { id: 'arena', name: 'The folded arena', where: 'a vast nylon block in the corner',
      clue: 'A sewn-in label, half under the straps: <b>INFLATABLE DODGEBALL ARENA — {{psi.V2}} cubic metres ' +
            'fully open.</b>' },
    { id: 'bibs', name: 'Bag of bibs', where: 'by the door', clue: null,
      flavour: 'Forty bibs, none of which have been washed this term. You put them back down immediately.' },
    { id: 'coat', name: 'The waterproof coat', where: 'hanging where he left it', clue: null,
      flavour: 'Enormous. Waxed. Smells faintly of a man who has never once been rained on. It is going back ' +
               'on its hook, and the store is getting his own padlock.' }
  ],

  locks: [
    {
      id: 'sprinkler-sector-area',
      key: 'arc',
      name: 'Sprinkler override',
      brief: 'The override sets how far round the sprinkler sweeps. Set the arc so the wet patch comes exactly ' +
             'to the limit the grounds staff are allowed on that square — no more. Short of it and he will not ' +
             'budge. Past it and you have not made a diversion, you have flooded the square.',
      instrument: { kind: 'dial', label: 'Sprinkler arc', min: 10, max: 360, step: 10, decimals: 0,
                    unit: '°', start: 10, sweep: 360, wedge: true, verb: 'Set the arc' },
      variants: [
        {
          "r": 12,
          "K": 48,
          "answer": 120,
          "miss": 40,
          "r2": 144,
          "frac": "1/3"
        },
        {
          "r": 15,
          "K": 200,
          "answer": 320,
          "miss": 100,
          "r2": 225,
          "frac": "8/9"
        },
        {
          "r": 24,
          "K": 288,
          "answer": 180,
          "miss": 60,
          "r2": 576,
          "frac": "1/2"
        },
        {
          "r": 18,
          "K": 252,
          "answer": 280,
          "miss": 90,
          "r2": 324,
          "frac": "7/9"
        },
        {
          "r": 18,
          "K": 36,
          "answer": 40,
          "miss": 10,
          "r2": 324,
          "frac": "1/9"
        },
        {
          "r": 6,
          "K": 24,
          "answer": 240,
          "miss": 80,
          "r2": 36,
          "frac": "2/3"
        },
        {
          "r": 24,
          "K": 128,
          "answer": 80,
          "miss": 30,
          "r2": 576,
          "frac": "2/9"
        },
        {
          "r": 24,
          "K": 160,
          "answer": 100,
          "miss": 30,
          "r2": 576,
          "frac": "5/18"
        },
        {
          "r": 12,
          "K": 104,
          "answer": 260,
          "miss": 80,
          "r2": 144,
          "frac": "13/18"
        },
        {
          "r": 12,
          "K": 120,
          "answer": 300,
          "miss": 100,
          "r2": 144,
          "frac": "5/6"
        }
      ],
      missTitle: '{{arc.miss}} degrees — the &pi; went missing on one side.',
      missSays: 'That is what you get by comparing {{arc.K}} with the whole circle worked out as a decimal ' +
                '(&pi; &times; {{arc.r2}} &asymp; {{arc.r2}}&pi;). The limit is <b>{{arc.K}}&pi;</b>, not {{arc.K}} — ' +
                'keep the &pi; on both sides and it cancels, leaving a fraction you can do in your head.',
      hints: [
        'The limit is written with a &pi; in it, and so is the area of the whole circle this sprinkler could cover. ' +
        'Work out that whole circle first and watch what happens to the &pi;.',
        'A full circle of radius {{arc.r}} m has area &pi;r&sup2; = {{arc.r2}}&pi; m&sup2;. The wet patch is a sector ' +
        'of that circle. What fraction of {{arc.r2}}&pi; is {{arc.K}}&pi;? Take the same fraction of 360&deg;.',
        '{{arc.K}}&pi; &divide; {{arc.r2}}&pi; = {{arc.frac}} — the &pi; cancels and never has to become a decimal. ' +
        '{{arc.frac}} of 360&deg; is <b>{{arc.answer}}&deg;</b>.'
      ],
      solve: 'Whole circle = &pi; &times; {{arc.r}}&sup2; = {{arc.r2}}&pi;. {{arc.K}}&pi; &divide; {{arc.r2}}&pi; = ' +
             '{{arc.frac}}, and {{arc.frac}} of 360&deg; is <b>{{arc.answer}}&deg;</b>.',
      onOpen: 'The head clunks round and settles, and through the little window the far edge of the arc walks ' +
              'out across the grass toward the cricket square. Behind you the register hits the floor. He does ' +
              'not say anything. He just goes.'
    },
    {
      id: 'dodgeball-pressure-boyle',
      key: 'psi',
      name: 'The compressor',
      brief: 'The compressor holds whatever pressure you leave on the gauge and pumps until the arena reaches it. ' +
             'Set it for the arena fully open, not folded flat.',
      instrument: { kind: 'dial', label: 'Compressor pressure', min: 0, max: 100, step: 1, decimals: 0,
                    unit: 'psi', start: 0, verb: 'Set the gauge' },
      variants: [
        {
          "V1": 20,
          "P1": 60,
          "V2": 25,
          "answer": 48,
          "miss": 75,
          "k": 1200
        },
        {
          "V1": 20,
          "P1": 35,
          "V2": 28,
          "answer": 25,
          "miss": 49,
          "k": 700
        },
        {
          "V1": 24,
          "P1": 60,
          "V2": 40,
          "answer": 36,
          "miss": 100,
          "k": 1440
        },
        {
          "V1": 30,
          "P1": 40,
          "V2": 60,
          "answer": 20,
          "miss": 80,
          "k": 1200
        },
        {
          "V1": 12,
          "P1": 30,
          "V2": 24,
          "answer": 15,
          "miss": 60,
          "k": 360
        },
        {
          "V1": 12,
          "P1": 30,
          "V2": 36,
          "answer": 10,
          "miss": 90,
          "k": 360
        },
        {
          "V1": 18,
          "P1": 90,
          "V2": 20,
          "answer": 81,
          "miss": 100,
          "k": 1620
        },
        {
          "V1": 32,
          "P1": 80,
          "V2": 40,
          "answer": 64,
          "miss": 100,
          "k": 2560
        }
      ],
      missTitle: '{{psi.miss}} psi, and the seams have gone.',
      missSays: '{{psi.P1}} &times; {{psi.V2}}&frasl;{{psi.V1}} = {{psi.miss}} scales the pressure <i>up</i> ' +
                'alongside the volume. That is direct proportion, and the card says inverse: as the arena gets ' +
                'bigger the same air is spread thinner, so the pressure must come <i>down</i>.',
      hints: [
        '&ldquo;Inversely proportional&rdquo; does not mean the two go up together — it means one rises as the other ' +
        'falls. There is a number that stays the same whatever the volume does. Find that before you touch the gauge.',
        'For inverse proportion, pressure &times; volume is constant. Multiply the two folded figures to get that ' +
        'constant, then divide it by the new volume.',
        'k = {{psi.V1}} &times; {{psi.P1}} = {{psi.k}}. Then P &times; {{psi.V2}} = {{psi.k}}, so P = {{psi.k}} ' +
        '&divide; {{psi.V2}} = <b>{{psi.answer}} psi</b>.'
      ],
      solve: 'Inverse proportion: P&times;V is constant. k = {{psi.V1}}&times;{{psi.P1}} = {{psi.k}}, so ' +
             'P = {{psi.k}}&divide;{{psi.V2}} = <b>{{psi.answer}} psi</b>.',
      onOpen: 'The compressor thumps into life and the folded nylon block in the corner begins, slowly and then all ' +
              'at once, to become a room.'
    },
    {
      id: 'locker-nth-term',
      key: 'seq',
      name: 'Equipment locker',
      brief: 'The code changes every day of term. He only writes one down when he has forgotten one, so the ' +
             'clipboard is patchy — and today is not on it.',
      instrument: { kind: 'dial', label: 'Locker combination', min: 0, max: 99, step: 1, decimals: 0,
                    unit: '', start: 0, verb: 'Turn the dial' },
      variants: [
        {
          "d1": 3,
          "c1": 23,
          "d2": 7,
          "c2": 43,
          "d3": 12,
          "c3": 68,
          "dT": 15,
          "step": 5,
          "answer": 83,
          "miss": 88,
          "span": 9,
          "rise": 45,
          "ahead": 3,
          "check": 4
        },
        {
          "d1": 3,
          "c1": 20,
          "d2": 6,
          "c2": 38,
          "d3": 10,
          "c3": 62,
          "dT": 12,
          "step": 6,
          "answer": 74,
          "miss": 80,
          "span": 7,
          "rise": 42,
          "ahead": 2,
          "check": 3
        },
        {
          "d1": 3,
          "c1": 22,
          "d2": 6,
          "c2": 31,
          "d3": 12,
          "c3": 49,
          "dT": 14,
          "step": 3,
          "answer": 55,
          "miss": 58,
          "span": 9,
          "rise": 27,
          "ahead": 2,
          "check": 3
        },
        {
          "d1": 2,
          "c1": 19,
          "d2": 5,
          "c2": 40,
          "d3": 10,
          "c3": 75,
          "dT": 12,
          "step": 7,
          "answer": 89,
          "miss": 96,
          "span": 8,
          "rise": 56,
          "ahead": 2,
          "check": 3
        },
        {
          "d1": 4,
          "c1": 23,
          "d2": 7,
          "c2": 32,
          "d3": 13,
          "c3": 50,
          "dT": 17,
          "step": 3,
          "answer": 62,
          "miss": 59,
          "span": 9,
          "rise": 27,
          "ahead": 4,
          "check": 3
        },
        {
          "d1": 3,
          "c1": 13,
          "d2": 7,
          "c2": 25,
          "d3": 11,
          "c3": 37,
          "dT": 14,
          "step": 3,
          "answer": 46,
          "miss": 49,
          "span": 8,
          "rise": 24,
          "ahead": 3,
          "check": 4
        },
        {
          "d1": 4,
          "c1": 25,
          "d2": 7,
          "c2": 37,
          "d3": 13,
          "c3": 61,
          "dT": 15,
          "step": 4,
          "answer": 69,
          "miss": 73,
          "span": 9,
          "rise": 36,
          "ahead": 2,
          "check": 3
        },
        {
          "d1": 2,
          "c1": 11,
          "d2": 5,
          "c2": 32,
          "d3": 10,
          "c3": 67,
          "dT": 14,
          "step": 7,
          "answer": 95,
          "miss": 88,
          "span": 8,
          "rise": 56,
          "ahead": 4,
          "check": 3
        },
        {
          "d1": 4,
          "c1": 13,
          "d2": 7,
          "c2": 22,
          "d3": 11,
          "c3": 34,
          "dT": 13,
          "step": 3,
          "answer": 40,
          "miss": 43,
          "span": 7,
          "rise": 21,
          "ahead": 2,
          "check": 3
        }
      ],
      missTitle: '{{seq.miss}} — you treated day {{seq.d3}} as yesterday.',
      missSays: 'Adding the gap between the first two written entries assumes {{seq.c3}} was yesterday’s code and ' +
                'that the gap is one day’s worth. It is not: {{seq.c3}} was set on day {{seq.d3}} and today is day ' +
                '{{seq.dT}}. Work out what <i>one</i> day is worth first.',
      hints: [
        'Three codes and three days. The days are not one after another, so the jumps between the codes are not ' +
        'one day’s worth of jump.',
        'Find the daily step: take two entries, divide the difference in the codes by the difference in the days. ' +
        'Check it against the third entry, then step forward from the last one to day {{seq.dT}}.',
        'Day {{seq.d1}} to day {{seq.d3}} is {{seq.span}} days, and {{seq.c3}} &minus; {{seq.c1}} = {{seq.rise}}, so ' +
        'the step is {{seq.rise}} &divide; {{seq.span}} = {{seq.step}} a day. Check day {{seq.d2}}: {{seq.c1}} + ' +
        '{{seq.check}}&times;{{seq.step}} = {{seq.c2}} &#10003;. Day {{seq.dT}} = {{seq.c3}} + ' +
        '{{seq.ahead}}&times;{{seq.step}} = <b>{{seq.answer}}</b>.'
      ],
      solve: 'Step = ({{seq.c3}}&minus;{{seq.c1}}) &divide; ({{seq.d3}}&minus;{{seq.d1}}) = {{seq.step}} a day. ' +
             'Day {{seq.dT}} = {{seq.c3}} + {{seq.ahead}}&times;{{seq.step}} = <b>{{seq.answer}}</b>.',
      onOpen: 'The dial stops with a sound like a knuckle cracking, and the locker swings open on twelve dodgeballs ' +
              'and, inexplicably, a kettle.'
    }
  ]
};
