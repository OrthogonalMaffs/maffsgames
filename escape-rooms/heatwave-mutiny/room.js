/* Room data for "heatwave-mutiny" — shared by index.html (the game) and
   teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand.

   VOICE REWRITE, 13/09/2026. Antagonist: Mr Robin Banks, the trust's energy
   contractor. He is a ridiculous individual, not a critique of a system: the
   school is on a FIXED-PRICE energy contract, so his company makes less money
   when the air conditioning runs, and his bonus rides on it. He is never in
   the building. His voice is a radio doorstep interview (after thirty-six
   holes of golf) that the breakfast show is replaying; each wrong entry plays
   the next beat, and the last beat repeats because the show restarts the clip.

   Load-bearing, do not tidy out:
   - The brief's fixed-contract clause is the answer to "why is this not
     sabotage": the power is already paid for, and the students switch off the
     one box put in to stop the school using it.
   - Banks has no authority over the school beyond the electricity. Line one's
     "You're the electricity contractor." / "I am a great deal more than that."
     is there to make that plain. Do not give him lines about running schools.
   - Estates have no code and no control; they want it on too. The door clue is
     his engineer's slip, relayed by Estates. The students' maths is the only
     way in.
   - He sees his defeat: the end-of-month report. Not a never-knew ending.
   - "Five times" is USAGE against his bonus figure. On a fixed contract the
     school's bill does not move, so never write it as the bill.

   The freezer failure was dropped in review, and with it the engine work it
   prompted (per-lock misconception pictures, a three-strikes ending). That
   work is CANCELLED, not deferred. A wrong frequency costs 45 seconds and
   nothing else.

   Protected lock text changed deliberately, no number moved: patrol lock
   instrument label (the 12:00 start was a timing fault: the corridor cleared
   two to three hours into a fifteen-minute room), its missTitle and first hint
   ("prefects" -> "Supervisors"); the third lock's name, instrument label,
   missTitle and missSays (wire -> disruptor, canteen freezers removed), and its
   missArt flag. All instrument art dropped set-wide. */
window.ROOM = {
  slug: 'escape-heatwave-mutiny',
  title: 'The Heatwave Mutiny',
  level: 'ks3',
  levelLabel: 'KS3 / GCSE',
  minutes: 15,
  penalty: 45,
  art: 'heatwave-mutiny',
  sceneAlt: 'An empty secondary school classroom before the day starts, the chairs still upside down on the desks. Hard white sunlight pours through half-open blinds, one hanging crooked, and lays bright stripes across the floor. Two air-conditioning units sit high on the wall, silent. A desk fan stands on the teacher’s desk, a dark jacket hangs over the teacher’s chair, and a plastic water bottle lies on its side on a desk by the window.',
  failAlt: 'The same classroom at the end of another day of the heatwave. The air-conditioning units are still shut, the light through the blinds has turned a heavy orange, and the room is hazy with heat. Empty water bottles lie among exercise books left open, a crumpled worksheet sits abandoned, the desk fan is still unplugged with its lead trailing to the floor, and a plant on the windowsill has wilted flat.',
  winAlt: 'The same classroom a few minutes before the bell, gone cool and blue. Both air-conditioning units are running, pale streams of cold air curling out across the room, while the sun outside is still a hot yellow-white. A water bottle is beaded with condensation, the dark jacket still hangs over the teacher’s chair, and the chairs are still up on the desks.',

  hook: 'Thirty-two degrees at twenty past eight, and the air conditioning in every school in the trust has been ' +
        'off since Monday, when the trust’s energy contractor, Mr Robin Banks, had it switched off. The chairs are ' +
        'still up on the desks. On the radio, the breakfast show is playing a clip from yesterday evening: a reporter ' +
        'who caught Mr Banks in a golf club car park after thirty-six holes, and asked him about it. He told her. ' +
        'The only cool people in the building are the Student Supervisors, each with a small fan clipped to their ' +
        'uniform, and they are patrolling the corridor to the control room.',
  brief: 'Fifteen minutes before the bell. Get past the patrol, through the control-room door, and shut down the ' +
         'disruptor Mr Banks bolted onto the air conditioning. The school is on a fixed contract and pays the same ' +
         'whether the air conditioning runs or not, so every bit of that power is already paid for. You are not ' +
         'taking anything. You are switching off the one box somebody put in to stop the school using what it has bought.',
  stakes: 'Miss the bell and the air conditioning stays off for as long as the heatwave lasts: every lesson, every ' +
          'day, thirty-two degrees and climbing. Mr Banks gets his bonus. The Student Supervisors will be fine.',
  win: 'Under the floor the compressors shudder and start, and then every room in the building starts with them. ' +
       'Nobody has even taken the chairs down yet, and the air is already cold enough to notice. Nobody at the ' +
       'energy company notices anything, because nobody from the energy company is ever in the building. Mr Banks ' +
       'notices at the end of the month, when his report arrives and the trust’s usage is five times the figure his ' +
       'bonus was worked out on. He has described this to his manager as a development opportunity.',

  wrongLines: [
    { head: 'The lock stays exactly where it is.',
      body: 'A car park, and a golf bag going into a boot. “Mr Banks, every school you supply is at thirty-two ' +
            'degrees.” “At no extra cost to them, which I think people forget, and I would say it is excellent ' +
            'preparation for the next generation of worker, who are going to be working in the heat, so really I am ' +
            'doing the schools’ job for them.” “You’re the electricity contractor.” “I am a great deal more than that.”' },
    { head: 'Something clicks and thinks better of it.',
      body: '“So what should schools be running on?” “Coal, and I say that as a very forward-thinking person, clean ' +
            'coal, which is coal that has been properly looked after, and the country shut all its coal power ' +
            'stations without asking me, which in my view was very short-sighted of the country.” She asks what ' +
            'makes coal clean. He says, “Attitude.”' },
    { head: 'The panel resets with a clunk.',
      body: '“Have you really just played thirty-six holes?” “Thirty-six holes is a great deal of thinking time, and ' +
            'I would say global warming, which in my view is not real, is going to make the weather a lot lovelier, ' +
            'and those are the kind of insights that do not show up on a payslip.” She says “Sorry, what?” on air.' },
    { head: 'The lock gives nothing back at all.',
      body: '“Is there anything you would like to say to the staff at St Martha’s?” A long pause. The boot shuts. ' +
            '“I would say that I am underpaid for the extraordinary leadership and vision I bring to the energy ' +
            'sector.” The breakfast show has gone back to the start of the clip.' }
  ],

  objects: [
    { id: 'rota', name: 'Student Supervisors’ rota', where: 'pinned inside the store cupboard',
      clue: '<b>CORRIDOR PATROL — Student Supervisors.</b> Supervisor A: one lap every <b>{{lcm.a}} minutes</b>. ' +
            'Supervisor B: every <b>{{lcm.b}}</b>. Supervisor C: every <b>{{lcm.c}}</b>. All three set off together ' +
            'from the staffroom.' },
    { id: 'clock', name: 'Wall clock', where: 'above the door, with a note taped to the glass',
      clue: 'The clock stopped at some point in the night, which in this heat is fair enough. The note says: ' +
            '“Corridor is only clear when all three Supervisors are back in the staffroom <i>at the same time</i>. ' +
            'Not before.”' },
    { id: 'sticky', name: 'Sticky note', where: 'stuck to the underside of a desk',
      clue: '“His engineer told me the code is what the coolant tank <i>holds</i>, in cubic centimetres, and then he ' +
            'laughed. I have been trying numbers since Monday. If anybody here can do cubes, be my guest.” — Estates' },
    { id: 'label', name: 'Maintenance label', where: 'on the back of the cupboard door',
      clue: '<b>COOLANT TANK.</b> A perfect cube. Total surface area <b>{{cube.SA}} square centimetres</b>. ' +
            'Do not overfill. Do not repaint.' },
    { id: 'manual', name: 'Installation manual', where: 'in the tool drawer, one page folded over',
      clue: 'Disruptor, shutdown procedure: “Cancel the unit on the single frequency <b>f</b> that satisfies ' +
            '<b>{{freq.lo}} &lt; {{freq.m}}f &minus; {{freq.k}} &lt; {{freq.hi}}</b>.”' },
    { id: 'memo', name: 'Crumpled memo', where: 'near the top of the bin',
      clue: '“… and for the last time, the disruptor only runs on a <b>prime</b> frequency. It will not sit on ' +
            'anything else, so stop asking me to set it to a round number.”' },
    { id: 'fan', name: 'Desk fan', where: 'on the teacher’s desk', clue: null,
      flavour: 'Unplugged. Taped to the plug is a note from Mr Banks’s company setting out what a desk fan costs to ' +
               'run for a year, and the sum is wrong.' },
    { id: 'thermo', name: 'Jacket', where: 'over the teacher’s chair', clue: null,
      flavour: 'Your teacher’s, left there on the way to the morning briefing. Nobody has needed a jacket in this ' +
               'building since Monday.' }
  ],

  locks: [
    {
      id: 'patrol-lcm-timer',
      key: 'lcm',
      name: 'Patrol window',
      brief: 'A countdown timer wired into the corridor door release. Set it to the number of minutes after the ' +
             'Supervisors set off when it is safe to cross, and it will let you through at that moment and no other.',
      instrument: { kind: 'slider', label: 'Corridor release — minutes after they set off', min: 1, max: 200, step: 1,
                    decimals: 0, unit: 'min', start: 1, verb: 'Set the timer' },
      variants: [
        {
          "a": 12,
          "b": 15,
          "c": 18,
          "answer": 180,
          "miss": 45,
          "factors": "12 = 2<sup>2</sup> &times; 3, 15 = 3 &times; 5, 18 = 2 &times; 3<sup>2</sup>",
          "lcmfactors": "2<sup>2</sup> &times; 3<sup>2</sup> &times; 5"
        },
        {
          "a": 7,
          "b": 16,
          "c": 28,
          "answer": 112,
          "miss": 51,
          "factors": "7 = 7, 16 = 2<sup>4</sup>, 28 = 2<sup>2</sup> &times; 7",
          "lcmfactors": "2<sup>4</sup> &times; 7"
        },
        {
          "a": 6,
          "b": 14,
          "c": 18,
          "answer": 126,
          "miss": 38,
          "factors": "6 = 2 &times; 3, 14 = 2 &times; 7, 18 = 2 &times; 3<sup>2</sup>",
          "lcmfactors": "2 &times; 3<sup>2</sup> &times; 7"
        },
        {
          "a": 5,
          "b": 7,
          "c": 20,
          "answer": 140,
          "miss": 32,
          "factors": "5 = 5, 7 = 7, 20 = 2<sup>2</sup> &times; 5",
          "lcmfactors": "2<sup>2</sup> &times; 5 &times; 7"
        },
        {
          "a": 7,
          "b": 11,
          "c": 14,
          "answer": 154,
          "miss": 32,
          "factors": "7 = 7, 11 = 11, 14 = 2 &times; 7",
          "lcmfactors": "2 &times; 7 &times; 11"
        }
      ],
      missTitle: '{{lcm.miss}} minutes, and the corridor is full of Supervisors.',
      missSays: 'That is {{lcm.a}} + {{lcm.b}} + {{lcm.c}} — the three lap times added together. Adding them ' +
                'describes nothing that actually happens: at {{lcm.miss}} minutes all three of them are mid-lap. ' +
                'You want the first moment all three are back at the start <i>at once</i>.',
      hints: [
        'Two of the notes are about the same thing — when all three Supervisors are in the same place. ' +
        'Each one is back in the staffroom at whole multiples of their own lap time. What kind of number is a ' +
        'multiple of {{lcm.a}} <i>and</i> of {{lcm.b}} <i>and</i> of {{lcm.c}}?',
        'You want the <b>lowest common multiple</b> of {{lcm.a}}, {{lcm.b}} and {{lcm.c}}. Break each one into ' +
        'prime factors, then build a number that contains enough of each prime to be divisible by all three.',
        '{{lcm.factors}}. Take the highest power of each prime: {{lcm.lcmfactors}} = <b>{{lcm.answer}}</b>. ' +
        'Set the timer to {{lcm.answer}} minutes.'
      ],
      solve: 'LCM of {{lcm.a}}, {{lcm.b}} and {{lcm.c}}: {{lcm.factors}}, so the LCM is {{lcm.lcmfactors}} = ' +
             '<b>{{lcm.answer}} minutes</b>.',
      onOpen: 'At that many minutes after they set off, all three Student Supervisors are back in the staffroom at ' +
              'once, comparing fans. The corridor is empty for about ninety seconds. You use forty of them.'
    },
    {
      id: 'cube-surface-volume',
      key: 'cube',
      name: 'Security door',
      brief: 'A four-digit keypad on the control-room door. Mr Banks’s company changed the code on Monday, and ' +
             'Estates have not been able to get in since.',
      instrument: { kind: 'keypad', label: 'Door keypad — four digits', digits: 4, verb: 'Enter the code' },
      variants: [
        {
          "SA": 1350,
          "edge": 15,
          "face": 225,
          "answer": 3375,
          "miss": 225
        },
        {
          "SA": 600,
          "edge": 10,
          "face": 100,
          "answer": 1000,
          "miss": 100
        },
        {
          "SA": 864,
          "edge": 12,
          "face": 144,
          "answer": 1728,
          "miss": 144
        },
        {
          "SA": 1176,
          "edge": 14,
          "face": 196,
          "answer": 2744,
          "miss": 196
        },
        {
          "SA": 1536,
          "edge": 16,
          "face": 256,
          "answer": 4096,
          "miss": 256
        },
        {
          "SA": 1734,
          "edge": 17,
          "face": 289,
          "answer": 4913,
          "miss": 289
        },
        {
          "SA": 1944,
          "edge": 18,
          "face": 324,
          "answer": 5832,
          "miss": 324
        },
        {
          "SA": 2166,
          "edge": 19,
          "face": 361,
          "answer": 6859,
          "miss": 361
        },
        {
          "SA": 2400,
          "edge": 20,
          "face": 400,
          "answer": 8000,
          "miss": 400
        },
        {
          "SA": 2646,
          "edge": 21,
          "face": 441,
          "answer": 9261,
          "miss": 441
        }
      ],
      missTitle: '{{cube.miss}} is one face, not the tank.',
      missSays: 'Dividing {{cube.SA}} by 6 is the right first move — but it gives you the area of <i>one square ' +
                'face</i>, not the capacity of the tank. You are two steps short: that area still has to become an ' +
                'edge length, and the edge still has to become a volume.',
      hints: [
        'You have been handed an <i>area</i> and asked for a <i>volume</i>. There is a length hiding between the ' +
        'two, and the word &ldquo;cube&rdquo; is what lets you find it.',
        'A cube has six identical square faces. Divide the total surface area by 6 to get one face. Square-root ' +
        'that to get one edge. Then cube the edge to get the volume.',
        '{{cube.SA}} &divide; 6 = {{cube.face}} cm&sup2; for one face. &radic;{{cube.face}} = {{cube.edge}} cm along ' +
        'each edge. {{cube.edge}}&sup3; = <b>{{cube.answer}}</b> cubic centimetres.'
      ],
      solve: 'One face = {{cube.SA}} &divide; 6 = {{cube.face}} cm&sup2;. Edge = &radic;{{cube.face}} = ' +
             '{{cube.edge}} cm. Volume = {{cube.edge}}&sup3; = <b>{{cube.answer}} cm&sup3;</b>.',
      onOpen: 'Four worn buttons, one flat clack each, and the bolt goes back. The air conditioning panel inside is in ' +
              'perfect working order. There is nothing wrong with it except the grey box bolted over its controls.'
    },
    {
      id: 'canteen-freezer-inequality',
      key: 'freq',
      name: 'The disruptor',
      brief: 'Bolted over the air-conditioning controls is Mr Banks’s disruptor, a grey box putting out a signal that ' +
             'jams the whole system. A disruptor can only be shut down by its own frequency sent straight back at ' +
             'it: match it exactly and the two signals cancel out, but one hertz either side and it carries on ' +
             'jamming. Tune the dial to it.',
      instrument: { kind: 'dial', label: 'Disruptor frequency', min: 0, max: 50, step: 1, decimals: 0,
                    unit: 'Hz', start: 0, verb: 'Send it back' },
      variants: [
        {
          "lo": 20,
          "m": 3,
          "k": 5,
          "hi": 32,
          "band": "9, 10, 11, 12",
          "low": "8.33",
          "high": "12.33",
          "answer": 11,
          "miss": 12,
          "lok": 25,
          "hik": 37
        },
        {
          "lo": 39,
          "m": 3,
          "k": 4,
          "hi": 52,
          "band": "15, 16, 17, 18",
          "low": "14.33",
          "high": "18.67",
          "answer": 17,
          "miss": 18,
          "lok": 43,
          "hik": 56
        },
        {
          "lo": 12,
          "m": 3,
          "k": 3,
          "hi": 25,
          "band": "6, 7, 8, 9",
          "low": "5",
          "high": "9.33",
          "answer": 7,
          "miss": 9,
          "lok": 15,
          "hik": 28
        },
        {
          "lo": 58,
          "m": 2,
          "k": 2,
          "hi": 67,
          "band": "31, 32, 33, 34",
          "low": "30",
          "high": "34.5",
          "answer": 31,
          "miss": 34,
          "lok": 60,
          "hik": 69
        },
        {
          "lo": 35,
          "m": 2,
          "k": 6,
          "hi": 46,
          "band": "21, 22, 23, 24, 25",
          "low": "20.5",
          "high": "26",
          "answer": 23,
          "miss": 25,
          "lok": 41,
          "hik": 52
        },
        {
          "lo": 59,
          "m": 2,
          "k": 11,
          "hi": 67,
          "band": "36, 37, 38",
          "low": "35",
          "high": "39",
          "answer": 37,
          "miss": 38,
          "lok": 70,
          "hik": 78
        }
      ],
      missTitle: '{{freq.miss}} Hz. Still jamming.',
      missSays: 'The inequality is solved correctly — {{freq.miss}} really is inside it. But it was never going to ' +
                'pick out one frequency on its own: {{freq.band}} all satisfy it. Taking the largest one and stopping ' +
                'there ignores the condition doing the other half of the work, and the disruptor carries on.',
      hints: [
        'Solve the inequality and count what is left. If it leaves you with more than one whole number, the ' +
        'inequality was never the whole instruction — something else in the room finishes the job.',
        'Work on all three parts at once: add {{freq.k}} throughout, then divide throughout by {{freq.m}}. List ' +
        'every whole number that survives, then apply the other condition to that short list.',
        '{{freq.lo}} &lt; {{freq.m}}f &minus; {{freq.k}} &lt; {{freq.hi}} gives {{freq.lok}} &lt; {{freq.m}}f &lt; ' +
        '{{freq.hik}}, so {{freq.low}} &lt; f &lt; {{freq.high}} — that is f = {{freq.band}}. Of those, only ' +
        '<b>{{freq.answer}}</b> is prime.'
      ],
      solve: '{{freq.lok}} &lt; {{freq.m}}f &lt; {{freq.hik}}, so {{freq.low}} &lt; f &lt; {{freq.high}}, leaving ' +
             '{{freq.band}}. Only <b>{{freq.answer}}</b> is prime.',
      onOpen: 'The dial clicks onto the frequency, the box gives one long falling whine and goes quiet, and somewhere ' +
              'under the floor a compressor coughs into life.'
    }
  ]
};
