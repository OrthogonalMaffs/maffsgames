/* Room data for "prom-budget" — shared by index.html (the game) and
   teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand.

   PREMISE — corrected 2026-09-08. The statue is not being made. It is made:
   cast, crated and on a pallet in a foundry waiting for the money to land,
   which is why the practice maquette has stood on his desk for months. The
   room is set A WEEK BEFORE the prom, not on the night — a bronze cannot be
   cast, delivered and craned into a hall between four o'clock and seven, and a
   prom cannot be rebuilt from nothing in the same window either. The clock is
   his phone call, not the bank: the portal only reverses a commission from the
   account that placed it, his is logged in on that desk, and it closes when he
   comes back and sits down. The old "clears in thirty-five minutes" line is
   cut — it was a second clock and it was never explained.

   ONE FAILURE — the call ends and he walks back in. He is not angry. He is
   delighted, because now the gesture is on the record and the prom committee
   really did do it themselves. Both pictures are prom night, a week later:
   they are the flash-forward at the end of `stakes` and `win`.

   VOICE — Mr D Tension, headmaster, ten years. Long-winded, self-important,
   a bore. Taught Business Studies for eleven years and will tell you so; he
   set these locks himself and is not as good at maths as he thinks he is. He
   loses stoically and is crying inside. The initial is the joke and is never
   spelled out anywhere in the prose. He is offstage in car-trap (the sports
   car) and, per the standing rule, speaks only here.

   The wrong-entry slot is one half of an overheard phone call, and every entry
   is one more obstacle cleared on his end — his problems get solved while the
   players' do not. The last line repeats, which is the joke.

   ART — instrument pictures are dropped set-wide (scene, fail and win only);
   the engine draws the live control anyway, so the `art`/`artAlt` fields are
   gone from all three locks below.

   ART COMPLETE 2026-09-08. All three pictures are the new empty-room style,
   filed at 1600x873, and all three alts describe what is actually on disk.
   The failure and victory pair came back with the generator's sparkle in the
   same place in both, sitting on a court line where interpolation smears, so
   both were framed out on the SAME crop — 0,0,2500,1364 — which is possible
   only because they share a camera. The crop keeps the ceiling in both, because
   the strip lights are the point of one and the mirrorball is the point of the
   other. Exact commands in docs/escape-room-image-prompts.md.

   Two lines moved to match the pictures rather than the other way round: the
   mirrorball is hung and turning, not sitting unhung on the floor (which also
   settled a contradiction with the stepladder line three paragraphs above it),
   and the failure table carries a laptop and crisps with no speaker on it.

   NOTE — object `id`s are load-bearing: teacher.html maps clues to locks by id
   in its `clueMap`. Renaming one silently breaks the teacher page. */
window.ROOM = {
  slug: 'escape-prom-budget',
  title: 'The Prom Budget Embezzlement',
  level: 'gcse',
  minutes: 15,
  penalty: 45,
  art: 'prom-budget',
  sceneAlt: 'A cramped school finance office at night, lit by a single desk lamp. A beige computer monitor and keyboard stand on a heavy wooden desk among stacks of paper and buff folders, with a small grey cash box and a mug beside them. Grey metal filing cabinets fill the left-hand wall, one drawer hanging open and crammed with folders, and loose sheets have spilled across the floor. A worn swivel chair is pushed back from the desk. The walls are pale green and marked, and a dark window looks out on the night at the right.',
  failAlt: 'A school sports hall under harsh strip lighting with nobody in it. Bare white walls, steel roof trusses and ductwork overhead, high windows dark with night, and wooden wall bars along the right hung with one paper garland. A folding trestle table on the left carries a closed laptop and a single small bowl of crisps. The parquet floor and its court markings are empty apart from the middle, where a life-sized bronze statue of a smiling man in a suit stands on a low wooden plinth, arms at his sides, lit from above.',
  winAlt: 'The same school sports hall at night with the lights down and nobody in it yet. A mirrorball hangs from the roof trusses and turns, throwing coloured spots across the walls, the floor and the ceiling, with a row of small stage lamps in blue, amber and purple on a bar behind it. Fairy lights, bunting and paper garlands are draped along the wooden wall bars on the right. A folding trestle table on the left carries a laptop between two speakers, an ice bucket of bottles and a row of plastic cups. In the middle of the empty parquet floor stands a low wooden plinth with nothing on it.',

  hook: 'Sit down. All of you. No, there aren&rsquo;t enough chairs &mdash; some of you will have to stand. ' +
        'That&rsquo;s the nature of a working office and frankly it does no harm.<br><br>' +
        'Now. I&rsquo;ve asked you in because there&rsquo;s been a <i>repositioning</i> of the prom fund. Let me ' +
        'finish before anybody reacts, because people do have a habit of reacting before I&rsquo;ve finished and ' +
        'it is rarely productive.<br><br>' +
        'A prom is one evening. Four hours. Gone by midnight and remembered by nobody. Whereas an <i>asset</i> ' +
        '&mdash; and I use the word advisedly, I taught Business Studies for eleven years before I was asked, ' +
        'repeatedly, to lead this school &mdash; an asset endures. It says something to every parent who walks ' +
        'through that door for the next forty years.<br><br>' +
        'And I think, on reflection, you&rsquo;ll find this was your idea. The prom committee&rsquo;s own ' +
        'initiative. Unprompted, unsolicited, and &mdash; I&rsquo;ll be honest with you &mdash; rather ' +
        'moving.<br><br>' +
        'Do you know how long I have been headmaster of this school? Ten years. Ten years, and a man of my ' +
        'stature&mdash;<br><br>' +
        '<em>His phone goes. He looks at it the way other people look at a birthday card.</em><br><br>' +
        'Ah. I&rsquo;ll have to take this. Wait there. Don&rsquo;t touch anything, there&rsquo;s nothing in here ' +
        'that concerns you.<br><br>' +
        '<em>The door doesn&rsquo;t quite shut. Through the glass he is pacing the corridor with his back to ' +
        'you, already talking. The portal on the desk is still logged in, under his name. And beside it, about ' +
        'the size of a bag of sugar, is a small bronze bust of a smiling man in a suit &mdash; the practice ' +
        'version, sent months ago, kept where he can see it. You have all met him. He has just left the ' +
        'room.</em>',
  brief: 'He will be out there for exactly as long as the crane company keeps finding problems, and they are ' +
         'running out. That is your fifteen minutes.<br><br>' +
         'The statue is not being made. It is made. It is on a pallet in a foundry waiting for the money to ' +
         'land, and the portal will only take a cancellation from the account that placed the order &mdash; ' +
         'which is his, and which is open on that desk until he comes back and sits down.<br><br>' +
         'Reverse the commission for the exact figure the sculptor was quoted, not the figure he was charged. ' +
         'Get the old prom reserve released, because the main fund is gone and something has to pay for the ' +
         'night. And get the network filter to pass the playlist, because the hall has speakers in it and ' +
         'nothing coming out of them.<br><br>' +
         'Every wrong setting in here makes a noise and costs you time. Out in the corridor, another one of his ' +
         'problems gets solved.',
  stakes: 'The call ends. It was always going to end. He comes back through the door mid-sentence, because he ' +
          'is always mid-sentence, and finds the prom committee standing round a logged-in finance portal with ' +
          'the invoice in their hands.<br><br>' +
          'And he is delighted. Genuinely, warmly delighted &mdash; because now the gesture is on the record, ' +
          'and the prom committee really did do it themselves.<br><br>' +
          'It goes up on the Wednesday. It takes four men, a crane and half the car park, and he watches all of ' +
          'it from the steps with his hands behind his back.<br><br>' +
          'By Friday the hall has the main lights on, a laptop on a trestle table and a single bowl of crisps, ' +
          'and a life-sized bronze headmaster beaming from the middle of the dance floor while nobody dances ' +
          'anywhere near him.',
  win: 'The commission reverses. The reserve lands. The playlist comes through the hall speakers loudly enough ' +
       'to be heard four hundred metres away, in a finance office, by a man on a phone.<br><br>' +
       'He is in the doorway. The corridor went quiet at some point and nobody noticed.<br><br>' +
       'He looks at the screen for a long moment, and then down the corridor at the hall, where somebody has ' +
       'finally worked out the stepladder.<br><br>' +
       '&ldquo;Well,&rdquo; he says. &ldquo;Yes. I did wonder whether the timing was right. On reflection, the ' +
       'young people should have their evening. I would have said as much myself, in due course.&rdquo;<br><br>' +
       'He picks the little bronze up off the desk, weighs it in his hand, and puts it in the drawer.<br><br>' +
       '&ldquo;A man of my stature doesn&rsquo;t need&mdash;&rdquo; He stops. Starts again. &ldquo;Have a ' +
       'marvellous evening. All of you. That&rsquo;s an instruction.&rdquo;<br><br>' +
       'Then he goes back to his own office and sits in it with the light off for slightly longer than the walk ' +
       'requires.<br><br>' +
       'On the Friday the hall gets the lights low, a mirrorball turning up under the roof trusses and throwing ' +
       'spots across the boards, and a room full of people dancing in the middle of it, around a space where ' +
       'nothing is standing.',

  /* Wrong-entry lines, indexed by how many wrong settings have been made so
     far; the last one repeats. You only ever hear his half of the call, and
     every line is one more obstacle cleared on his end: his problems get
     solved while yours do not. The last entry repeats for the rest of the
     game, so a player who keeps getting it wrong hears him agree to conclude
     the call over and over without it ever concluding — which is why `win`
     says the corridor went quiet rather than that anybody heard him finish.
     The engine reads this array, indexed by st.wrongs - 1 and clamped to the
     last entry. A misconception hit consumes an index without printing a line,
     which is intended — see wrongLine() in engine.js. */
  wrongLines: [
    { head: 'The field clears itself and asks again.',
      body: 'From the corridor, unhurried: &ldquo;The gates are wider than they look. I&rsquo;ve measured them. ' +
            'Personally, with a tape.&rdquo;' },
    { head: 'Something in the desk resets with a clunk.',
      body: '&ldquo;Ground pressure, yes. No &mdash; it can&rsquo;t stand on the field, the field is ' +
            'booked.&rdquo; A pause. &ldquo;Then it will have to come off my space. Fine. Fine, I&rsquo;ll ' +
            'walk.&rdquo;' },
    { head: 'The setting slides back to where it was.',
      body: '&ldquo;If it&rsquo;s a road closure, it&rsquo;s a road closure. I&rsquo;ll speak to Hendricks. ' +
            'He&rsquo;s a governor, he&rsquo;ll wave it through, he&rsquo;s very supportive of me. Everyone is, ' +
            'really.&rdquo;' },
    { head: 'Another one. The corridor is no further away than it was.',
      body: '&ldquo;Right. So we&rsquo;re agreed.&rdquo;' }
  ],

  objects: [
    { id: 'invoice', name: 'The invoice', where: 'face down under the desk lamp',
      clue: '<b>BRONZE COMMISSION &mdash; ST MARTHA&rsquo;S SECONDARY.</b> Cast, crated and awaiting ' +
            'collection. Total charged, including the {{quote.pct}}% vanity levy: ' +
            '<b>&pound;{{quote.total}}.00</b>. Non-refundable once cleared.' },
    { id: 'helpcard', name: 'Portal help card', where: 'taped to the side of the monitor',
      clue: '&ldquo;REVERSING AN ORDER: the portal will only cancel a commission for the <b>exact price the ' +
            'sculptor was quoted</b> &mdash; the figure before the levy was added. Whole pounds. Four ' +
            'digits.&rdquo;' },
    { id: 'passbook', name: 'Old passbook', where: 'in the back of the desk drawer',
      clue: 'PROM RESERVE &mdash; opened by a form group nobody can now name. <b>Opening deposit ' +
            '&pound;{{acct.dep}}. Fixed {{acct.rate}}% compound interest, paid annually.</b>' },
    { id: 'statement', name: 'Bank statement', where: 'in the recycling, dated today',
      clue: 'PROM RESERVE &mdash; balance today: <b>&pound;{{acct.bal}}</b>. &ldquo;Funds released only on ' +
            'confirmation of the account&rsquo;s age in whole years.&rdquo;' },
    { id: 'printout', name: 'Network printout', where: 'still warm in the printer tray',
      clue: 'LIVE NETWORK &mdash; hall and corridors. Devices connected: <b>{{venn.total}}</b>. Requesting ' +
            'Spotify: <b>{{venn.A}}</b>. Requesting YouTube: <b>{{venn.B}}</b>. Requesting neither: ' +
            '<b>{{venn.neither}}</b>.' },
    { id: 'itnote', name: 'IT department note', where: 'pinned to the corkboard',
      clue: '&ldquo;The filter will not pass any traffic until the router&rsquo;s dual-service allocation is ' +
            'set to the number of devices asking for <b>both services at once</b>. Do not guess it. It ' +
            'counts.&rdquo;' },
    { id: 'plant', name: 'Spider plant', where: 'on top of the filing cabinet', clue: null,
      flavour: 'Three quarters dead, and watered at some point with coffee. Somebody has propped a Christmas ' +
               'card against the pot. It is not December.' },
    { id: 'bust', name: 'The bronze bust', where: 'on the desk, watching you', clue: null,
      flavour: 'The practice version, sent by the sculptor months ago. It is a very good likeness, which ' +
               'somehow makes it worse. It weighs about as much as a bag of sugar, and it has stood here long ' +
               'enough to have left a clean ring in the dust around it.' }
  ],

  locks: [
    {
      id: 'finance-reverse-percentage',
      key: 'quote',
      grade: 5,
      name: 'Tax refund',
      brief: 'The portal will reverse the commission, but only from the account that placed it and only for the ' +
             'exact amount the sculptor was quoted &mdash; not the amount he was charged. Four digits, whole ' +
             'pounds.',
      instrument: { kind: 'keypad', label: 'Transfer amount — whole pounds', digits: 4, verb: 'Enter the amount' },
      variants: [
        {
          "total": 2160,
          "pct": 20,
          "answer": 1800,
          "miss": 1728,
          "whole": 120,
          "onepct": "18"
        },
        {
          "total": 5320,
          "pct": 25,
          "answer": 4256,
          "miss": 3990,
          "whole": 125,
          "onepct": "42.56"
        },
        {
          "total": 6920,
          "pct": 25,
          "answer": 5536,
          "miss": 5190,
          "whole": 125,
          "onepct": "55.36"
        },
        {
          "total": 1812,
          "pct": 50,
          "answer": 1208,
          "miss": 906,
          "whole": 150,
          "onepct": "12.08"
        },
        {
          "total": 4698,
          "pct": 50,
          "answer": 3132,
          "miss": 2349,
          "whole": 150,
          "onepct": "31.32"
        },
        {
          "total": 7512,
          "pct": 50,
          "answer": 5008,
          "miss": 3756,
          "whole": 150,
          "onepct": "50.08"
        },
        {
          "total": 3480,
          "pct": 50,
          "answer": 2320,
          "miss": 1740,
          "whole": 150,
          "onepct": "23.2"
        },
        {
          "total": 7700,
          "pct": 25,
          "answer": 6160,
          "miss": 5775,
          "whole": 125,
          "onepct": "61.6"
        },
        {
          "total": 8360,
          "pct": 25,
          "answer": 6688,
          "miss": 6270,
          "whole": 125,
          "onepct": "66.88"
        },
        {
          "total": 8470,
          "pct": 10,
          "answer": 7700,
          "miss": 7623,
          "whole": 110,
          "onepct": "77"
        }
      ],
      missTitle: '&pound;{{quote.miss}} — that is {{quote.pct}}% off the wrong number.',
      missSays: 'Taking {{quote.pct}}% off &pound;{{quote.total}} gives &pound;{{quote.miss}}, but the levy was added ' +
                'to the <i>quote</i>, not to the total. {{quote.pct}}% of the smaller number is a smaller amount. ' +
                'Check it: add {{quote.pct}}% back on to &pound;{{quote.miss}} and you do not get ' +
                '&pound;{{quote.total}}.',
      hints: [
        'The &pound;{{quote.total}} already has the levy inside it. So &pound;{{quote.total}} is not the 100% you are ' +
        'looking for — it is more than 100%. How much more?',
        'The quote is 100%. Adding a {{quote.pct}}% levy makes the total {{quote.whole}}%. Get from {{quote.whole}}% ' +
        'to 1%, then up to 100% — or divide by {{quote.whole}} and multiply by 100 in one go.',
        '{{quote.whole}}% = &pound;{{quote.total}}, so 1% = {{quote.total}} &divide; {{quote.whole}} = ' +
        '&pound;{{quote.onepct}}, and 100% = <b>&pound;{{quote.answer}}</b>.'
      ],
      solve: '&pound;{{quote.total}} is {{quote.whole}}% of the quote. {{quote.total}} &divide; {{quote.whole}} ' +
             '&times; 100 = <b>&pound;{{quote.answer}}</b>.',
      onOpen: 'The portal thinks about it for four long seconds and then prints COMMISSION REVERSED in a font ' +
              'from 1998. Somewhere a foundry gets an email it is going to enjoy considerably less than you did.'
    },
    {
      id: 'dj-deposit-compound',
      key: 'acct',
      grade: 5,
      name: 'The prom reserve',
      brief: 'This account was never his and he has never known it was there. The bank will release it to anyone ' +
             'who can say how long the money has been sitting in it. Whole years.',
      instrument: { kind: 'slider', label: 'Account age', min: 1, max: 20, step: 1, decimals: 0,
                    unit: 'years', start: 1, verb: 'Confirm the age' },
      variants: [
        {
          "dep": 1000,
          "rate": 10,
          "bal": "1610.51",
          "answer": 5,
          "miss": 6,
          "mult": "1.1",
          "interest": "610.51"
        },
        {
          "dep": 1200,
          "rate": 20,
          "bal": "2488.32",
          "answer": 4,
          "miss": 5,
          "mult": "1.2",
          "interest": "1288.32"
        },
        {
          "dep": 800,
          "rate": 20,
          "bal": "1382.40",
          "answer": 3,
          "miss": 4,
          "mult": "1.2",
          "interest": "582.40"
        },
        {
          "dep": 2500,
          "rate": 20,
          "bal": "7464.96",
          "answer": 6,
          "miss": 10,
          "mult": "1.2",
          "interest": "4964.96"
        }
      ],
      missTitle: '{{acct.miss}} years — you have treated the interest as flat.',
      missSays: '&pound;{{acct.interest}} of interest divided by {{acct.rate}}% of the opening deposit comes out ' +
                'near {{acct.miss}}, but the interest is not the same every year. Year two earns {{acct.rate}}% of ' +
                'a bigger balance than year one. Compound growth arrives faster than flat interest, so it takes ' +
                '<i>fewer</i> years, not more.',
      hints: [
        'Each year does not <i>add</i> a fixed amount of money — it <i>multiplies</i>. What single number does one ' +
        'year do to the balance?',
        'Every year multiplies the balance by {{acct.mult}}. So you want the power of {{acct.mult}} that turns ' +
        '{{acct.dep}} into {{acct.bal}}. Build it up a year at a time: {{acct.mult}}&sup2;, {{acct.mult}}&sup3;, and ' +
        'on from there.',
        '{{acct.dep}} &times; {{acct.mult}}&#8319; = {{acct.bal}}. Working the powers up one year at a time, the ' +
        'balance first reaches &pound;{{acct.bal}} at n = <b>{{acct.answer}} years</b>.'
      ],
      solve: '{{acct.dep}} &times; {{acct.mult}}&#8319; = {{acct.bal}}, which gives n = ' +
             '<b>{{acct.answer}} years</b>.',
      onOpen: 'RESERVE RELEASED. Opened by a form group nobody can name, forgotten for years, and quietly doing ' +
              'the one thing nobody in this office has managed: getting bigger.'
    },
    {
      id: 'wifi-venn-router',
      key: 'venn',
      grade: 4,
      name: 'Network router',
      brief: 'The hall speakers are wired, powered and silent. The filter passes nothing until the router&rsquo;s ' +
             'dual-service allocation matches what the network is actually doing right now.',
      instrument: { kind: 'dial', label: 'Dual-service allocation', min: 0, max: 100, step: 1, decimals: 0,
                    unit: 'devices', start: 0, verb: 'Set the dial' },
      variants: [
        {
          "total": 80,
          "A": 48,
          "B": 37,
          "neither": 12,
          "answer": 17,
          "miss": 0,
          "atleast": 68,
          "sum": 85
        },
        {
          "total": 85,
          "A": 57,
          "B": 49,
          "neither": 13,
          "answer": 34,
          "miss": 0,
          "atleast": 72,
          "sum": 106
        },
        {
          "total": 75,
          "A": 57,
          "B": 52,
          "neither": 9,
          "answer": 43,
          "miss": 0,
          "atleast": 66,
          "sum": 109
        },
        {
          "total": 85,
          "A": 57,
          "B": 37,
          "neither": 13,
          "answer": 22,
          "miss": 0,
          "atleast": 72,
          "sum": 94
        },
        {
          "total": 95,
          "A": 72,
          "B": 64,
          "neither": 15,
          "answer": 56,
          "miss": 0,
          "atleast": 80,
          "sum": 136
        },
        {
          "total": 90,
          "A": 45,
          "B": 28,
          "neither": 23,
          "answer": 6,
          "miss": 0,
          "atleast": 67,
          "sum": 73
        },
        {
          "total": 90,
          "A": 69,
          "B": 61,
          "neither": 9,
          "answer": 49,
          "miss": 0,
          "atleast": 81,
          "sum": 130
        },
        {
          "total": 90,
          "A": 66,
          "B": 46,
          "neither": 7,
          "answer": 29,
          "miss": 0,
          "atleast": 83,
          "sum": 112
        },
        {
          "total": 95,
          "A": 33,
          "B": 58,
          "neither": 15,
          "answer": 11,
          "miss": 0,
          "atleast": 80,
          "sum": 91
        },
        {
          "total": 100,
          "A": 81,
          "B": 79,
          "neither": 17,
          "answer": 77,
          "miss": 0,
          "atleast": 83,
          "sum": 160
        }
      ],
      missTitle: 'Zero says nobody is doing both at once.',
      missSays: 'If no device wanted both, the numbers would be {{venn.A}} + {{venn.B}} + {{venn.neither}} devices ' +
                'on a network with only {{venn.total}} on it. Naming two services separately does not make them ' +
                'exclusive — plenty of people have both open.',
      hints: [
        'Add the two service figures together and compare the total with how many devices are actually connected. ' +
        'Something has been counted twice.',
        '{{venn.total}} &minus; {{venn.neither}} = {{venn.atleast}} devices want at least one of the two services. ' +
        'But {{venn.A}} + {{venn.B}} = {{venn.sum}} counts every both-services device in each list. The overlap is ' +
        'the difference between those.',
        '{{venn.atleast}} = {{venn.A}} + {{venn.B}} &minus; both, so both = {{venn.sum}} &minus; {{venn.atleast}} = ' +
        '<b>{{venn.answer}} devices</b>.'
      ],
      solve: '{{venn.total}} &minus; {{venn.neither}} = {{venn.atleast}} want something. {{venn.A}} + {{venn.B}} ' +
             '&minus; both = {{venn.atleast}}, so both = <b>{{venn.answer}}</b>.',
      onOpen: 'Every light on the router goes green at once, and four hundred metres away a speaker in the hall ' +
              'coughs and starts playing something nobody&rsquo;s dad has ever heard of.'
    }
  ]
};
