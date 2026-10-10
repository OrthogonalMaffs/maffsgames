/* Room data for "canteen-hack" — shared by index.html (the game) and
   teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand.

   PREMISE — corrected 2026-09-12. Healthy Week is Ms Cinnamon's, the home
   economics teacher: vegan, activist, respected, and this morning she stopped
   asking. She did not ban the cookie, she re-priced it, so that she can say
   accurately that she has banned nothing. The students are not fighting the
   kale and the win does not remove it — the board ends the room carrying BOTH,
   at prices a person can pay, which is the argument she should have made at
   seven o'clock. Beating the room is not beating her.

   THE STEP TOO FAR IS THE FRAME, NOT THE KALE. She did it at seven o'clock on
   the catering manager's till, under the catering manager's administrator
   login, and left it standing in the manager's name. That is the thing a
   respected teacher does not do, and it is the whole reason the room exists.
   Do not soften it into her acting boldly and standing by it — an earlier draft
   had her ready to put her hand up and it was WRONG. She is not owning this.

   THE LOGIN SYMMETRY — caught in review, 12/09/2026. The students work the same
   administrator session Cinnamon used, so mechanically they do the thing the
   room calls unforgivable. The win alone does not answer that: it says nobody
   looked, which is getting away with it, not being different. The BRIEF answers
   it instead, and that clause is load-bearing — everything on their list puts
   something back rather than sets something up, an entry goes in somebody's
   name and a reversal leaves nothing in anybody's. Do not cut it for length.

   ONE FAILURE — the bell. If Healthy Week is still standing when it goes it is
   signed off in the manager's name, and the manager will disprove it: she was
   not in the building at seven and she can show it. The moment she does, the
   question stops being about kale and becomes about who used her account, and
   there is exactly one answer. The students roll the morning back so there is
   nothing to sign off and nothing to prove — no printout, no investigation, no
   question. They are saving Cinnamon from what she has already done, and the
   manager from carrying it in the meantime. They are saving her from herself.

   VOICE — Cinnamon carries the wrong-entry slot (see `wrongLines`),
   monologuing through the hatch from her room across the corridor at a Year 8
   who went in to ask a question and has not been released. She never appears
   and never addresses the players. She is never wrong about the facts and never
   shrill; the room does not work if she is a crank.

   THE COOKIE'S HEALTHY WEEK PRICE IS £8.40 AND THAT FIGURE IS LOAD-BEARING.
   The till lock draws last term's cookie baseline from its variants library,
   where it runs £1–£7. The old prose said £5, which in one variant matched
   the baseline exactly and in another sat BELOW it — Healthy Week made the
   cookie cheaper. Any replacement figure must clear £7, and must clear the
   dial's max of 10 if that library is ever regenerated wider. It is unrounded
   because she costed it rather than picked it.

   ART — instrument pictures are dropped set-wide (scene, fail and win only);
   the engine draws the live control anyway, so the `art`/`artAlt` fields are
   gone from all three locks below.

   NOTE — object `id`s are load-bearing: teacher.html maps clues to locks by id
   in its `clueMap`. Renaming one silently breaks the teacher page. The six
   clue-carrying ids below are unchanged from the original build.

   ART ON DISK: all three pictures filed 12/09/2026 in the new empty-room style
   — scene, fail and win, 1600x873 WebP, none carrying a generator watermark. */
window.ROOM = {
  slug: 'escape-canteen-hack',
  title: 'The Canteen Menu Hack',
  level: 'ks3',
  minutes: 15,
  penalty: 45,
  art: 'canteen-hack',
  sceneAlt: 'A school canteen servery a few minutes before lunch, seen along the length of the counter. Stacks of coloured plastic trays wait at the near end, the hot wells beyond them are empty and gleaming, and a steel gantry runs above the counter beneath an extraction hood. A smart till stands at the far end beside the cutlery rack. Past the servery the dining hall is empty, its tables bare and most of the chairs still stacked.',
  failAlt: 'A school canteen servery after lunch has finished, the shutter half down and the heat lamps still on. The steel trays beneath them are almost full of dark baked kale, barely served from, and the spoons rest unused beside them. The stack of clean plastic trays at the end of the counter has not been touched. On the counter, alone under a glass dome on a paper doily, sits a single chocolate cookie. Beyond the servery the dining hall is empty and the chairs are up on the tables.',
  winAlt: 'A school canteen servery a few minutes into a busy lunch, the shutter fully up. Wide steel trays of pizza sit steaming under the heat lamps, and beside them a deep tray of dark baked kale stands half emptied with a serving spoon left standing in it. The stack of plastic trays at the end of the counter has been worked down to the last few. The smart till has printed a receipt long enough to have reached the floor and coiled there. Beyond the servery the dining hall tables are down and waiting.',

  hook: 'Healthy Week started at eight this morning. Nobody was asked. The chips are gone, the heat lamps are ' +
        'holding trays of baked kale, and the last chocolate cookie in the building is under a glass dome at ' +
        '&pound;8.40. Ms Cinnamon is in her room across the corridor, explaining. The smart till on the counter ' +
        'is still logged in as an administrator — as the catering manager, who does not get in until eight.',
  brief: 'Fifteen minutes before the bell. Get a day of specials past the nutrition check she built, put last ' +
         'term&rsquo;s prices back on the tags, and clear the shelf space the pizza delivery needs — in whatever ' +
         'order the room lets you. Every one of those puts something back rather than sets something up, which is ' +
         'the whole difference between you and her: an entry goes in somebody&rsquo;s name, and a reversal leaves ' +
         'nothing in anybody&rsquo;s. Leave the kale on the menu. The kale was never the problem.',
  stakes: 'Miss the bell and Healthy Week is signed off in the catering manager&rsquo;s name — every entry on ' +
          'that till timed at seven o&rsquo;clock, an hour before she got in. She can prove she was not there, and ' +
          'when she does there is only one question left and only one answer to it.',
  win: 'The till chimes and drops every price in the building back to where it was last term. The chute takes ' +
       'what it is allowed to take and no more. Somewhere behind the shutter an oven that has not been switched ' +
       'on since July starts to warm up. There is nothing left to sign off now and nothing left for anybody to ' +
       'disprove, so there will be no printout, no awkward morning, and no question about whose login was open at ' +
       'seven o&rsquo;clock. When Ms Cinnamon comes back at half past she will find her kale still on the board, ' +
       'at a price a person could actually pay, a pizza beside it, and a queue in front of both — which is the ' +
       'argument she was trying to make this morning, made properly, by the people it was about. She will never ' +
       'know how close it was.',

  wrongLines: [
    { head: 'The panel clears itself and waits.',
      body: 'Through the hatch, from her room across the corridor: &ldquo;Nobody has banned anything. I want to ' +
            'be very clear about that, because it will be the first thing you hear.&rdquo; A Year 8 went in four ' +
            'minutes ago to ask whether there was anything at lunch that was not kale.' },
    { head: 'The entry is refused, politely, twice.',
      body: '&ldquo;Everything that was on that counter yesterday is on it today. It is simply priced at what it ' +
            'actually costs.&rdquo; The Year 8 has sat down.' },
    { head: 'Something inside the panel resets with a clunk.',
      body: '&ldquo;Have you seen the contract? No. Nor had I, and I have been here eleven years. You have eaten ' +
            'what that document tells you to eat since Year 7 and not one of you has ever asked to read it. That ' +
            'is not an accident. That is a design.&rdquo; She has not raised her voice once.' },
    { head: 'The lock gives nothing back at all.',
      body: '&ldquo;&mdash; and somebody had to stop asking politely. If that costs somebody an awkward ' +
            'afternoon then I am sorry for it, I am. But they did not write the contract either, and they will ' +
            'understand that.&rdquo; A chair scrapes. The Year 8 has got as far as the door. She has started ' +
            'again from the beginning.' }
  ],

  objects: [
    { id: 'menuboard', name: 'The specials board', where: 'chalked up behind the counter',
      clue: '<b>TODAY&rsquo;S SPECIALS — logged.</b> Four entered so far: <b>{{meal.e1}}</b>, <b>{{meal.e2}}</b>, ' +
            '<b>{{meal.e3}}</b> and <b>{{meal.e4}}</b> kcal. Fifth slot: empty, awaiting entry.' },
    { id: 'compliance', name: 'Nutrition compliance notice', where: 'laminated this morning, screwed to the wall by the hatch',
      clue: '&ldquo;A day&rsquo;s specials are published only when the <b>mean</b> of all <b>five</b> comes to ' +
            'exactly <b>{{meal.T}} kcal</b>. Not near it. Exactly it.&rdquo;' },
    { id: 'receipt', name: 'Crumpled receipt', where: 'in the apron pocket by the door',
      clue: '<b>ST MARTHA&rsquo;S CANTEEN — last term.</b> COOKIE &times;{{till.a1}}, PIZZA &times;{{till.b1}} — ' +
            '<b>&pound;{{till.t1}}</b>. Same week: COOKIE &times;{{till.a2}}, PIZZA &times;{{till.b2}} — ' +
            '<b>&pound;{{till.t2}}</b>. The item prices have been torn off the bottom.' },
    { id: 'tilldrawer', name: 'Note in the till drawer', where: 'taped inside, under the coin tray',
      clue: '&ldquo;PRICE ROLLBACK: the till reverts only when <b>both baseline tags</b> are set to what the items ' +
            'cost last term. Whole pounds. It checks the pair together, so a right number on the wrong tag is a ' +
            'wrong answer.&rdquo;' },
    { id: 'stocksheet', name: 'Stock sheet', where: 'on a clipboard hanging off the cold store handle',
      clue: 'COLD STORE — <b>KALE, baked: {{chute.N}} portions.</b> PIZZA, incoming: one delivery, no shelf space ' +
            'allocated.' },
    { id: 'inspection', name: 'Letter from the health inspector', where: 'pinned to the corkboard by the sinks',
      clue: '&ldquo;At inspection, exactly <sup>{{chute.n}}</sup>&frasl;<sub>{{chute.d}}</sub> of the original stock ' +
            'must still be on the shelf. An empty shelf is a failed inspection. <b>The chute logs what it ' +
            'destroys.</b>&rdquo;' },
    { id: 'kale', name: 'A tray of the kale', where: 'under the heat lamps, third from the left', clue: null,
      flavour: 'It went under the lamps at half past seven and it has been there ever since. It has stopped ' +
               'being a vegetable and become a texture. Whatever else she got right this morning, she has held a ' +
               'green vegetable at serving temperature for four hours, which is the one thing she has told three ' +
               'year groups never to do. There is nothing under the tray except more of the tray.' },
    { id: 'suggestions', name: 'The suggestions box', where: 'screwed to the wall, never emptied', clue: null,
      flavour: 'Forty-odd slips of paper, thirty-eight of which say &ldquo;chips&rdquo;. One says &ldquo;chips ' +
               'please&rdquo;. The last one, in different handwriting, asks whether they can do the food bank ' +
               'thing again next term, and somebody has written &ldquo;yes&rdquo; under it in green pen.' }
  ],

  locks: [
    {
      id: 'canteen-mean-calories',
      key: 'meal',
      grade: 3,
      name: 'The dietary slider',
      brief: 'The menu system will not publish today&rsquo;s specials until the nutrition check passes. Four items ' +
             'are already logged. The fifth is a dummy entry, and its calorie value is yours to choose.',
      instrument: { kind: 'slider', label: 'Fifth special — calories', min: 0, max: 1000, step: 1, decimals: 0,
                    unit: 'kcal', start: 0, verb: 'Log the entry' },
      variants: [
        {
          "e1": 520,
          "e2": 480,
          "e3": 550,
          "e4": 600,
          "T": 450,
          "answer": 100,
          "miss": 450,
          "total": 2250,
          "sum4": 2150
        },
        {
          "e1": 470,
          "e2": 530,
          "e3": 600,
          "e4": 450,
          "T": 450,
          "answer": 200,
          "miss": 450,
          "total": 2250,
          "sum4": 2050
        },
        {
          "e1": 530,
          "e2": 590,
          "e3": 660,
          "e4": 510,
          "T": 550,
          "answer": 460,
          "miss": 550,
          "total": 2750,
          "sum4": 2290
        },
        {
          "e1": 450,
          "e2": 390,
          "e3": 480,
          "e4": 360,
          "T": 400,
          "answer": 320,
          "miss": 400,
          "total": 2000,
          "sum4": 1680
        },
        {
          "e1": 600,
          "e2": 660,
          "e3": 730,
          "e4": 590,
          "T": 600,
          "answer": 420,
          "miss": 600,
          "total": 3000,
          "sum4": 2580
        },
        {
          "e1": 390,
          "e2": 440,
          "e3": 340,
          "e4": 420,
          "T": 350,
          "answer": 160,
          "miss": 350,
          "total": 1750,
          "sum4": 1590
        },
        {
          "e1": 430,
          "e2": 340,
          "e3": 370,
          "e4": 330,
          "T": 350,
          "answer": 280,
          "miss": 350,
          "total": 1750,
          "sum4": 1470
        },
        {
          "e1": 690,
          "e2": 600,
          "e3": 630,
          "e4": 590,
          "T": 550,
          "answer": 240,
          "miss": 550,
          "total": 2750,
          "sum4": 2510
        },
        {
          "e1": 490,
          "e2": 550,
          "e3": 620,
          "e4": 460,
          "T": 500,
          "answer": 380,
          "miss": 500,
          "total": 2500,
          "sum4": 2120
        },
        {
          "e1": 650,
          "e2": 590,
          "e3": 680,
          "e4": 580,
          "T": 600,
          "answer": 500,
          "miss": 600,
          "total": 3000,
          "sum4": 2500
        }
      ],
      missTitle: '{{meal.miss}} kcal is the target mean, not the missing item.',
      missSays: 'Entering the mean itself only works when every item is identical, and these are not. The four ' +
                'already logged come to {{meal.sum4}} kcal between them — more than four items at {{meal.T}} would ' +
                '— so the fifth has to pull the total <i>down</i>, not sit on the line.',
      hints: [
        'A mean is a total shared out. You are told what the mean has to be and how many items are sharing it, so ' +
        'you can work out the total for the day before you know anything at all about the missing item.',
        'Five items at {{meal.T}} kcal is a total of {{meal.total}} kcal. The four already logged use up ' +
        '{{meal.sum4}} of that total. What is left over is not shared with anybody.',
        '{{meal.total}} &minus; {{meal.sum4}} = <b>{{meal.answer}} kcal</b>.'
      ],
      solve: '{{meal.T}} &times; 5 = {{meal.total}} kcal for the day. The four logged come to {{meal.sum4}}, so the ' +
             'fifth is {{meal.total}} &minus; {{meal.sum4}} = <b>{{meal.answer}} kcal</b>.',
      onOpen: 'NUTRITION CHECK: PASSED. The board fills itself in. She built this check herself and it has just ' +
              'been satisfied exactly, to the calorie, which is the only kind of argument she has ever accepted.'
    },
    {
      id: 'cookie-price-simultaneous',
      key: 'till',
      grade: 5,
      name: 'The price tags',
      brief: 'The till will roll every price back to last term, but only once both baseline tags are set. It checks ' +
             'them as a pair. Whole pounds.',
      instrument: { kind: 'pair', label: 'Baseline prices — whole pounds', verb: 'Set both tags',
        a: { kind: 'dial', label: 'Cookie', min: 0, max: 10, step: 1, decimals: 0, unit: '', start: 0 },
        b: { kind: 'dial', label: 'Pizza', min: 0, max: 10, step: 1, decimals: 0, unit: '', start: 0 } },
      variants: [
        {
          "a1": 3,
          "b1": 2,
          "t1": 12,
          "a2": 1,
          "b2": 4,
          "t2": 14,
          "C": 2,
          "P": 3,
          "mult": 3,
          "answer": [
            2,
            3
          ],
          "miss": [
            3,
            2
          ],
          "eC": 3,
          "eP": 12,
          "eT": 42,
          "pcoef": 10,
          "ptot": 30
        },
        {
          "a1": 2,
          "b1": 1,
          "t1": 10,
          "a2": 1,
          "b2": 3,
          "t2": 15,
          "C": 3,
          "P": 4,
          "mult": 2,
          "answer": [
            3,
            4
          ],
          "miss": [
            4,
            3
          ],
          "eC": 2,
          "eP": 6,
          "eT": 30,
          "pcoef": 5,
          "ptot": 20
        },
        {
          "a1": 2,
          "b1": 1,
          "t1": 17,
          "a2": 1,
          "b2": 2,
          "t2": 19,
          "C": 5,
          "P": 7,
          "mult": 2,
          "answer": [
            5,
            7
          ],
          "miss": [
            7,
            5
          ],
          "eC": 2,
          "eP": 4,
          "eT": 38,
          "pcoef": 3,
          "ptot": 21
        },
        {
          "a1": 3,
          "b1": 2,
          "t1": 17,
          "a2": 1,
          "b2": 3,
          "t2": 22,
          "C": 1,
          "P": 7,
          "mult": 3,
          "answer": [
            1,
            7
          ],
          "miss": [
            7,
            1
          ],
          "eC": 3,
          "eP": 9,
          "eT": 66,
          "pcoef": 7,
          "ptot": 49
        },
        {
          "a1": 2,
          "b1": 1,
          "t1": 7,
          "a2": 1,
          "b2": 3,
          "t2": 16,
          "C": 1,
          "P": 5,
          "mult": 2,
          "answer": [
            1,
            5
          ],
          "miss": [
            5,
            1
          ],
          "eC": 2,
          "eP": 6,
          "eT": 32,
          "pcoef": 5,
          "ptot": 25
        },
        {
          "a1": 2,
          "b1": 3,
          "t1": 27,
          "a2": 1,
          "b2": 2,
          "t2": 17,
          "C": 3,
          "P": 7,
          "mult": 2,
          "answer": [
            3,
            7
          ],
          "miss": [
            7,
            3
          ],
          "eC": 2,
          "eP": 4,
          "eT": 34,
          "pcoef": 1,
          "ptot": 7
        },
        {
          "a1": 3,
          "b1": 2,
          "t1": 21,
          "a2": 1,
          "b2": 3,
          "t2": 28,
          "C": 1,
          "P": 9,
          "mult": 3,
          "answer": [
            1,
            9
          ],
          "miss": [
            9,
            1
          ],
          "eC": 3,
          "eP": 9,
          "eT": 84,
          "pcoef": 7,
          "ptot": 63
        },
        {
          "a1": 3,
          "b1": 1,
          "t1": 5,
          "a2": 1,
          "b2": 3,
          "t2": 7,
          "C": 1,
          "P": 2,
          "mult": 3,
          "answer": [
            1,
            2
          ],
          "miss": [
            2,
            1
          ],
          "eC": 3,
          "eP": 9,
          "eT": 21,
          "pcoef": 8,
          "ptot": 16
        },
        {
          "a1": 2,
          "b1": 1,
          "t1": 23,
          "a2": 1,
          "b2": 2,
          "t2": 25,
          "C": 7,
          "P": 9,
          "mult": 2,
          "answer": [
            7,
            9
          ],
          "miss": [
            9,
            7
          ],
          "eC": 2,
          "eP": 4,
          "eT": 50,
          "pcoef": 3,
          "ptot": 27
        },
        {
          "a1": 2,
          "b1": 3,
          "t1": 26,
          "a2": 1,
          "b2": 4,
          "t2": 28,
          "C": 4,
          "P": 6,
          "mult": 2,
          "answer": [
            4,
            6
          ],
          "miss": [
            6,
            4
          ],
          "eC": 2,
          "eP": 8,
          "eT": 56,
          "pcoef": 5,
          "ptot": 30
        }
      ],
      missTitle: '&pound;{{till.P}} for a cookie and &pound;{{till.C}} for a pizza — the right pair, swapped.',
      missSays: 'Both numbers are correct and both are on the wrong tag. Try them on the first line: {{till.a1}} ' +
                'cookies at &pound;{{till.P}} and {{till.b1}} pizzas at &pound;{{till.C}} does not come to ' +
                '&pound;{{till.t1}}. The other way round, it does.',
      hints: [
        'Two unknowns and two lines. Neither line gives you a price on its own — but one of them can be scaled up ' +
        'until it has as many cookies in it as the other.',
        'Multiply the second line by {{till.mult}}: COOKIE &times;{{till.eC}}, PIZZA &times;{{till.eP}}, ' +
        '&pound;{{till.eT}}. Both lines now buy the same number of cookies, so the difference between them is ' +
        'pizzas and nothing else.',
        'Taking the first line away from that leaves {{till.pcoef}} pizzas costing &pound;{{till.ptot}}, so a pizza ' +
        'is <b>&pound;{{till.P}}</b>. Put that back into the first line and a cookie is <b>&pound;{{till.C}}</b>.'
      ],
      solve: 'Second line &times; {{till.mult}}: {{till.eC}}C + {{till.eP}}P = {{till.eT}}. Subtract the first line ' +
             '({{till.a1}}C + {{till.b1}}P = {{till.t1}}): {{till.pcoef}}P = {{till.ptot}}, so P = ' +
             '<b>&pound;{{till.P}}</b> and C = <b>&pound;{{till.C}}</b>.',
      onOpen: 'Every price in the building drops at once. Under its glass dome the cookie goes back to being ' +
              'something a person might buy on the way past, rather than a point being made.'
    },
    {
      id: 'kale-fraction-drain',
      key: 'chute',
      grade: 3,
      name: 'The disposal chute',
      brief: 'The chute destroys whatever number of portions it is set to. The inspection wants a specific amount ' +
             'still on the shelf afterwards, and an empty shelf fails it outright.',
      instrument: { kind: 'dial', label: 'Disposal chute', min: 0, max: 200, step: 1, decimals: 0,
                    unit: 'portions', start: 0, verb: 'Set the chute' },
      variants: [
        {
          "N": 180,
          "n": 2,
          "d": 9,
          "kept": 40,
          "answer": 140,
          "miss": 40,
          "one": 20
        },
        {
          "N": 200,
          "n": 1,
          "d": 8,
          "kept": 25,
          "answer": 175,
          "miss": 25,
          "one": 25
        },
        {
          "N": 70,
          "n": 1,
          "d": 7,
          "kept": 10,
          "answer": 60,
          "miss": 10,
          "one": 10
        },
        {
          "N": 120,
          "n": 2,
          "d": 5,
          "kept": 48,
          "answer": 72,
          "miss": 48,
          "one": 24
        },
        {
          "N": 200,
          "n": 3,
          "d": 8,
          "kept": 75,
          "answer": 125,
          "miss": 75,
          "one": 25
        },
        {
          "N": 150,
          "n": 3,
          "d": 10,
          "kept": 45,
          "answer": 105,
          "miss": 45,
          "one": 15
        },
        {
          "N": 60,
          "n": 5,
          "d": 12,
          "kept": 25,
          "answer": 35,
          "miss": 25,
          "one": 5
        },
        {
          "N": 90,
          "n": 4,
          "d": 9,
          "kept": 40,
          "answer": 50,
          "miss": 40,
          "one": 10
        },
        {
          "N": 180,
          "n": 1,
          "d": 9,
          "kept": 20,
          "answer": 160,
          "miss": 20,
          "one": 20
        },
        {
          "N": 110,
          "n": 2,
          "d": 11,
          "kept": 20,
          "answer": 90,
          "miss": 20,
          "one": 10
        }
      ],
      missArt: true,
      missTitle: '{{chute.miss}} portions is the amount that was supposed to survive.',
      missSays: '<sup>{{chute.n}}</sup>&frasl;<sub>{{chute.d}}</sub> of {{chute.N}} is {{chute.miss}}, and the ' +
                'letter wants that still sitting on the shelf when the inspector arrives. Send it down the chute ' +
                'and you have destroyed exactly the wrong portions and left {{chute.answer}} behind.',
      hints: [
        'Read the letter and the dial next to each other. One of them is about what stays and the other is about ' +
        'what goes, and they are not the same number.',
        'One {{chute.d}}th of {{chute.N}} portions is {{chute.one}}, so ' +
        '<sup>{{chute.n}}</sup>&frasl;<sub>{{chute.d}}</sub> of the stock is {{chute.kept}} portions. That is the ' +
        'part that must not move.',
        '{{chute.N}} &minus; {{chute.kept}} = <b>{{chute.answer}} portions</b> for the chute.'
      ],
      solve: '<sup>{{chute.n}}</sup>&frasl;<sub>{{chute.d}}</sub> of {{chute.N}} = {{chute.kept}} portions stay on ' +
             'the shelf, so <b>{{chute.answer}} portions</b> go down the chute.',
      onOpen: 'The chute opens with a sound like a drawbridge and takes precisely what it is allowed to take. ' +
              'What stays is still a great deal of kale, and it is still going on the board, because the kale was ' +
              'never the problem.'
    }
  ]
};
