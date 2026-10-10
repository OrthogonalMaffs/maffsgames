/* Room data for "rightful-king" — shared by play.html (the game, for now) and
   teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand.

   BUILT 2026-10-10 (contract RIGHTFUL-KING-BUILD) from the draft Jon approved in
   full on 10 Oct (docs/escape-room-drafts/rightful-king-draft.md, merged #247).
   It replaces the withdrawn it-vengeance room, whose three locks leave with it:
   their bank entries and generator libraries are kept as history. The three
   locks here are bank batch 9 (docs/lock-bank-batch9.txt). Mr Brian Narry is
   Jon's character and speaks only in this room; the Head is mentioned once,
   offstage, and never speaks (he speaks only in prom-budget). The bully is
   offstage, unnamed, and not in the win.

   The room sits behind its holding page (index.html) until Jon has play-tested
   it at play.html; it has no hub card until its release contract.

   GRADES (canon §11.3, ESCAPE-DIFFICULTY): the passcode's product rule without
   repeats is Higher content (6); the overwrite builds powers of one multiplier,
   the method #253 graded 5 in Prom Budget; the audit's conditional probability
   from a Venn diagram is Higher (7). The hardest lock makes the room ★★★
   Challenge.

   NOTE — object `id`s are load-bearing: teacher.html maps clues to locks by id
   in its `clueMap`. `prompt` and `stage-screen` are the two blanks.

   NOTE — not one numeral is typed into a clue string. The overwrite's threshold
   is a word token ({{ow.part}}: "half" or "a quarter"), so it is no clue figure.
   The only figures in the prose outside tokens are "fifteen minutes" and "half
   past three", in words.

   ART: none yet (art pending; ART-PENDING, #244). Jon generates the three
   pictures after his play-test; add `art` with them, never before. The alts
   below are the draft's, to be checked against the pictures.

   RULE — the fail picture will show the crown already down, which is only true
   at time-out. Never set `missArt` on any lock in this room. */
window.ROOM = {
  slug: 'escape-rightful-king',
  title: 'The Rightful King',
  level: 'gcse',
  minutes: 15,
  penalty: 45,
  sceneAlt: 'A school IT suite after the last lesson. Rows of monitors are switched off except one big display at the front, glowing with a neon pop-concert stage: sparkles, a sweeping spotlight, and a crown hanging over an empty space. At the back a server cupboard stands open, its lights blinking. On the side wall a corkboard holds a single printed sheet with a gold star stuck to it, and the desk by the door has a keyboard pushed back and a mug of tea gone cold.',
  failAlt: 'The same IT suite, the room lights off. The big display blazes: the crown lowered and glowing, the spotlight full on, sparkles frozen mid-fall. The server cupboard is shut and the chairs are pushed in.',
  winAlt: 'The same IT suite in morning light. The big display is calm and dark blue, with a small plain crown in one corner and no sparkles. On the desk a printed sheet lies face down beside a pencil, and the gold star is stuck to the edge of the monitor.',

  hook: 'Mr Brian Narry teaches IT. He loves his job, he likes nearly all of you, and last month he built the ' +
        'online vote for prom king the way he builds most things now: he asked an AI to do it. His prompt is ' +
        'printed out and pinned to the corkboard behind his desk, with a gold star on it.<br><br>' +
        'He meets you at the door of the IT suite before you are properly through it.<br><br>' +
        '&ldquo;You have to help me, my coding had a bug, and it&rsquo;s about to be unrecoverable.&rdquo;',
  brief: 'It wasn&rsquo;t his coding, and it isn&rsquo;t a bug. The AI did exactly what it was asked. The voting ' +
         'screen is a pop-concert stage, all neon and sparkles, and it looks amazing. Nobody asked for the vote to ' +
         'be secret, so it isn&rsquo;t: anyone who knows where to look can see who voted for whom.<br><br>' +
         'One boy in the year knew where to look, and made sure people knew he was looking. A lot of them voted ' +
         'for him. The kindest boy in the year would have won a free vote.<br><br>' +
         'The result goes up on every screen in the school at half past three, with a crown and a drum roll. That ' +
         'is your fifteen minutes.<br><br>' +
         'Nobody in this room changes a vote, his or anyone else&rsquo;s. You are going to close the leak, save ' +
         'the vote log before it is overwritten, and prove from the totals that the leak changed the result, so ' +
         'a fresh vote opens with the ballot secret again. Then everyone can vote for whoever they like. The ' +
         'audit counts; it never names anyone.<br><br>' +
         'Every wrong setting costs you time, and Mr Narry&rsquo;s hand keeps drifting back towards the chat ' +
         'window.',
  /* There is no `fail` slot: the engine shows `stakes` after "If you get it
     wrong." on the start screen and after "And so:" on the time-out screen, so
     the failure is written here and reads after both. */
  stakes: 'At half past three the drum roll plays on every screen in the school, the crown comes down, and his ' +
          'name goes up under it in neon. The year group claps, because everyone can see who is clapping. Mr ' +
          'Narry watches it from the back of the IT suite, and for once he doesn&rsquo;t reach for the keyboard. ' +
          'There is nothing left to ask it.',
  win: 'The leak page is gone, the old log is safe, and the audit is on the Head&rsquo;s desk in one line of ' +
       'totals. The fresh vote runs overnight. Nobody can see anybody&rsquo;s ballot, and this time nobody ' +
       'tries.<br><br>' +
       'At registration the drum roll plays, the crown comes down, and the name under it is the kindest boy in ' +
       'the year. He looks round as though somebody has made a mistake. Nobody has.<br><br>' +
       'Mr Narry takes his prompt down off the corkboard and peels the gold star off it.<br><br>' +
       '&ldquo;It wasn&rsquo;t a bug,&rdquo; he says. &ldquo;And it wasn&rsquo;t my coding. It did exactly what ' +
       'I asked it to.&rdquo; He turns the sheet over. &ldquo;It was my prompt.&rdquo;<br><br>' +
       'He writes a new one on the back, by hand, slowly. The first line is a question: <i>who should be able ' +
       'to see the votes?</i>',

  /* Wrong-entry lines, indexed by how many wrong settings have been made so
     far; the last one repeats (the point: every time, he chooses not to hand it
     over). Each head is the room's reaction; each body is Mr Narry reaching for
     the AI and stopping himself. None of them mentions the students. */
  wrongLines: [
    { head: 'A burst of sparkles, and the setting clears.',
      body: 'Mr Narry&rsquo;s hand goes to the chat window. &ldquo;I&rsquo;ll just ask it what we&mdash; no. ' +
            'No. That&rsquo;s how we got here.&rdquo;' },
    { head: 'The screen flashes and resets.',
      body: 'He has typed &ldquo;how do I fix&rdquo; before he notices, and deletes it a letter at a time. ' +
            '&ldquo;Habit. Sorry. Carry on.&rdquo;' },
    { head: 'The setting slides back. The countdown doesn&rsquo;t care.',
      body: '&ldquo;I used to do all this on paper, you know. Flowcharts. I had a pencil I liked.&rdquo; He ' +
            'looks at his hand as if the pencil might still be in it.' },
    { head: 'Another one. The countdown keeps going.',
      body: 'He reaches for the keyboard, stops, and puts both hands in his pockets.' }
  ],

  objects: [
    { id: 'sticky-note', name: 'Sticky note', where: 'on the edge of Mr Narry’s monitor',
      clue: 'In his handwriting: <b>ADMIN PASSCODE: {{pc.L}} DIFFERENT KEYS, NEVER THE SAME KEY TWICE.</b> Under ' +
            'it, underlined twice: &ldquo;The AI picked it. Ask the AI.&rdquo;' },
    { id: 'login-pad', name: 'The admin login', where: 'on the big screen, under the sparkles',
      clue: 'A pad of <b>{{pc.k}} keys</b>, every one a different glittering shape. Under it, in small grey type: ' +
            'too many wrong guesses; reset only by answering the guard.' },
    { id: 'server-log', name: 'Server log', where: 'scrolling on the monitor inside the server cupboard',
      clue: 'OVERWRITE RUNNING. <b>Each minute, {{ow.r}}% of the original records still left are replaced.</b>' },
    { id: 'audit-policy', name: 'Audit policy', where: 'pinned inside the server cupboard door',
      clue: '&ldquo;A vote can only be audited from its original records. <b>Once fewer than {{ow.part}} of them ' +
            'survive, the log is unrecoverable.</b>&rdquo;' },
    { id: 'results-page', name: 'Results page', where: 'behind the sparkles, if you scroll down',
      clue: 'VOTES CAST: <b>{{au.N}}</b>. His name is at the top, with <b>{{au.V}}</b> votes. You don&rsquo;t need ' +
            'to read it twice.' },
    { id: 'access-log', name: 'Access log', where: 'still warm in the printer tray',
      clue: 'A printout of totals, no names. <b>Opened the ballot page before voting: {{au.S}}. Never opened it ' +
            'and did not vote for him: {{au.neither}}.</b>' },
    { id: 'prompt', name: 'The prompt', where: 'pinned to the corkboard, with a gold star on it', clue: null,
      flavour: 'One line, printed large: &ldquo;Make sure the voting screen looks amazing, like a proper ' +
               'pop-concert stage with neon and sparkles, concentrate on aesthetics over all other ' +
               'considerations.&rdquo; Underneath, in biro: &ldquo;Nailed it.&rdquo;' },
    { id: 'stage-screen', name: 'The voting screen', where: 'on the big display at the front', clue: null,
      flavour: 'Neon, sparkles, a spotlight sweeping an empty stage, and a crown turning slowly over a space where ' +
               'a name will go. It does look amazing. That was the whole brief.' }
  ],

  locks: [
    {
      id: 'admin-passcode-product-rule',
      key: 'pc',
      grade: 6,
      name: 'The admin login',
      brief: 'Mr Narry is locked out of his own system. He never knew the passcode; he let the AI choose it. The ' +
             'guard lets a new passcode be set only by someone who can tell it exactly how many different ' +
             'passcodes it would have to try to be sure of getting in.',
      instrument: { kind: 'keypad', label: 'PASSCODES TO TRY', maxDigits: 3, verb: 'Enter count' },
      variants: [
        {
          "k": 7,
          "L": 3,
          "answer": 210,
          "miss": 343,
          "prod": "7 &times; 6 &times; 5"
        },
        {
          "k": 8,
          "L": 3,
          "answer": 336,
          "miss": 512,
          "prod": "8 &times; 7 &times; 6"
        },
        {
          "k": 9,
          "L": 3,
          "answer": 504,
          "miss": 729,
          "prod": "9 &times; 8 &times; 7"
        },
        {
          "k": 5,
          "L": 3,
          "answer": 60,
          "miss": 125,
          "prod": "5 &times; 4 &times; 3"
        },
        {
          "k": 6,
          "L": 3,
          "answer": 120,
          "miss": 216,
          "prod": "6 &times; 5 &times; 4"
        }
      ],
      missTitle: 'That count lets a key be used twice.',
      missSays: '{{pc.miss}} is {{pc.k}} multiplied by itself {{pc.L}} times, which allows the same key again. The ' +
                'note says never the same key twice, so every key used leaves one fewer for the next.',
      hints: [
        'How many keys could go first? Once one is used, how many are left to go second?',
        'No key is used twice, so each position has one fewer choice than the one before it. Multiply the ' +
        'choices.',
        '{{pc.prod}}: one factor for each of the {{pc.L}} keys in the passcode.'
      ],
      solve: '{{pc.k}} choices, then one fewer each time: {{pc.prod}} = <b>{{pc.answer}}</b>.',
      onOpen: 'The guard accepts the count and asks for a new passcode. Mr Narry types one himself, slowly, and ' +
              'writes nothing down. Then he takes the ballot page offline. The leak is shut.'
    },
    {
      id: 'vote-log-overwrite',
      key: 'ow',
      grade: 5,
      name: 'The recovery tool',
      brief: 'The overwrite can&rsquo;t be stopped from here, only outrun. The recovery tool will copy the ' +
             'original records out, but it has to be given its deadline: the number of whole minutes until fewer ' +
             'than {{ow.part}} of them survive.',
      instrument: { kind: 'dial', label: 'MINUTES UNTIL UNRECOVERABLE', min: 1, max: 20, step: 1, decimals: 0,
                    start: 1, verb: 'Set deadline' },
      variants: [
        {
          "r": 20,
          "f": "1/2",
          "answer": 4,
          "miss": 3,
          "part": "half",
          "fdec": "0.5",
          "keep": 80,
          "mult": "0.8",
          "prev": 3,
          "prevval": "0.512",
          "ansval": "0.410"
        },
        {
          "r": 8,
          "f": "1/4",
          "answer": 17,
          "miss": 10,
          "part": "a quarter",
          "fdec": "0.25",
          "keep": 92,
          "mult": "0.92",
          "prev": 16,
          "prevval": "0.263",
          "ansval": "0.242"
        },
        {
          "r": 29,
          "f": "1/4",
          "answer": 5,
          "miss": 3,
          "part": "a quarter",
          "fdec": "0.25",
          "keep": 71,
          "mult": "0.71",
          "prev": 4,
          "prevval": "0.254",
          "ansval": "0.180"
        },
        {
          "r": 20,
          "f": "1/4",
          "answer": 7,
          "miss": 4,
          "part": "a quarter",
          "fdec": "0.25",
          "keep": 80,
          "mult": "0.8",
          "prev": 6,
          "prevval": "0.262",
          "ansval": "0.210"
        },
        {
          "r": 7,
          "f": "1/2",
          "answer": 10,
          "miss": 8,
          "part": "half",
          "fdec": "0.5",
          "keep": 93,
          "mult": "0.93",
          "prev": 9,
          "prevval": "0.520",
          "ansval": "0.484"
        },
        {
          "r": 9,
          "f": "1/2",
          "answer": 8,
          "miss": 6,
          "part": "half",
          "fdec": "0.5",
          "keep": 91,
          "mult": "0.91",
          "prev": 7,
          "prevval": "0.517",
          "ansval": "0.470"
        },
        {
          "r": 40,
          "f": "1/4",
          "answer": 3,
          "miss": 2,
          "part": "a quarter",
          "fdec": "0.25",
          "keep": 60,
          "mult": "0.6",
          "prev": 2,
          "prevval": "0.360",
          "ansval": "0.216"
        },
        {
          "r": 11,
          "f": "1/4",
          "answer": 12,
          "miss": 7,
          "part": "a quarter",
          "fdec": "0.25",
          "keep": 89,
          "mult": "0.89",
          "prev": 11,
          "prevval": "0.278",
          "ansval": "0.247"
        },
        {
          "r": 12,
          "f": "1/4",
          "answer": 11,
          "miss": 7,
          "part": "a quarter",
          "fdec": "0.25",
          "keep": 88,
          "mult": "0.88",
          "prev": 10,
          "prevval": "0.279",
          "ansval": "0.245"
        },
        {
          "r": 9,
          "f": "1/4",
          "answer": 15,
          "miss": 9,
          "part": "a quarter",
          "fdec": "0.25",
          "keep": 91,
          "mult": "0.91",
          "prev": 14,
          "prevval": "0.267",
          "ansval": "0.243"
        }
      ],
      missTitle: 'That takes the same amount every minute.',
      missSays: '{{ow.miss}} minutes is what you get if each minute replaced {{ow.r}}% of the <i>original</i> ' +
                'records. It replaces {{ow.r}}% of what is left, so it slows down, and the records last longer ' +
                'than that.',
      hints: [
        'Each minute takes {{ow.r}}% of what is <i>left</i>, not of what there was at the start, so each minute ' +
        'takes a little less than the one before.',
        'Keeping {{ow.keep}}% each minute means multiplying by {{ow.mult}} each minute. Keep multiplying, and ' +
        'count the minutes.',
        'Find the first whole minute when {{ow.mult}} to that power is below {{ow.fdec}}.'
      ],
      solve: 'After <i>n</i> minutes, {{ow.mult}}<sup><i>n</i></sup> of the records survive. ' +
             '{{ow.mult}}<sup>{{ow.prev}}</sup> = {{ow.prevval}} is not yet below {{ow.fdec}}; ' +
             '{{ow.mult}}<sup>{{ow.answer}}</sup> = {{ow.ansval}} is. <b>{{ow.answer}} minutes.</b>',
      onOpen: 'The recovery tool runs ahead of the overwrite and copies every original record into a sealed ' +
              'file. Nobody opens it. It only has to exist.'
    },
    {
      id: 'leak-audit-conditional',
      key: 'au',
      grade: 7,
      name: 'The audit',
      brief: 'The fresh vote opens only if the audit shows the leak changed the result. It asks one question: of ' +
             'the voters who opened the ballot page before voting, what percentage voted for him? It works from ' +
             'totals only. Nobody&rsquo;s vote gets looked at.',
      instrument: { kind: 'keypad', label: 'PERCENT OF THOSE WHO SAW IT', digits: 2, verb: 'Enter' },
      variants: [
        {
          "N": 120,
          "V": 50,
          "S": 40,
          "neither": 60,
          "answer": 75,
          "miss": 25,
          "inside": 60,
          "both": 30,
          "notS": "25%"
        },
        {
          "N": 200,
          "V": 100,
          "S": 50,
          "neither": 90,
          "answer": 80,
          "miss": 20,
          "inside": 110,
          "both": 40,
          "notS": "40%"
        },
        {
          "N": 240,
          "V": 80,
          "S": 120,
          "neither": 100,
          "answer": 50,
          "miss": 25,
          "inside": 140,
          "both": 60,
          "notS": "about 17%"
        },
        {
          "N": 230,
          "V": 130,
          "S": 125,
          "neither": 90,
          "answer": 92,
          "miss": 50,
          "inside": 140,
          "both": 115,
          "notS": "about 14%"
        },
        {
          "N": 100,
          "V": 40,
          "S": 50,
          "neither": 45,
          "answer": 70,
          "miss": 35,
          "inside": 55,
          "both": 35,
          "notS": "10%"
        },
        {
          "N": 120,
          "V": 45,
          "S": 50,
          "neither": 55,
          "answer": 60,
          "miss": 25,
          "inside": 65,
          "both": 30,
          "notS": "about 21%"
        },
        {
          "N": 150,
          "V": 45,
          "S": 75,
          "neither": 60,
          "answer": 40,
          "miss": 20,
          "inside": 90,
          "both": 30,
          "notS": "20%"
        }
      ],
      missTitle: 'That is out of every voter.',
      missSays: '{{au.miss}}% is {{au.both}} out of all {{au.N}} voters. The audit asked about the ones who opened ' +
                'the page, so the {{au.both}} is out of {{au.S}}.',
      hints: [
        'Draw two overlapping circles: voted for him, and opened the page. The voters who did neither go outside ' +
        'both.',
        'Everyone inside the circles is {{au.N}} &minus; {{au.neither}}. The two circles added together come to ' +
        'more than that, because the overlap gets counted twice.',
        'Find the overlap, then ask what percentage it is of the {{au.S}} who opened the page.'
      ],
      solve: 'Inside the circles: {{au.N}} &minus; {{au.neither}} = {{au.inside}}. Overlap: {{au.V}} + {{au.S}} ' +
             '&minus; {{au.inside}} = {{au.both}}. {{au.both}} out of {{au.S}} is <b>{{au.answer}}%</b>.',
      onOpen: 'The audit prints one line. Of the voters who saw the page, {{au.answer}}% voted for him. Of those ' +
              'who never saw it, {{au.notS}}. A fresh vote opens across the year group, secret this time.'
    }
  ]
};
