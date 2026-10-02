/* Room data for "it-vengeance" — shared by index.html (the game) and
   teacher.html (answers, hint ladder, misconceptions).

   Numbers are not written into the prose. Each lock carries a `variants`
   library and one set is drawn per play; {{key.token}} in any string below is
   filled from the drawn set. The libraries are generated and verified by
   scripts/gen-escape-variants.py — do not edit them by hand. */
window.ROOM = {
  slug: 'escape-it-vengeance',
  title: 'The IT Teacher’s Vengeance',
  level: 'gcse',
  levelLabel: 'GCSE Higher',
  minutes: 15,
  penalty: 45,
  art: 'it-vengeance',
  sceneAlt: 'A school gym hall at dusk, lit blue through high windows. Wall bars, climbing ropes, a vaulting horse and a stack of blue mats. On the near wall a locked AV cabinet glows, with an elaborate mechanical keyboard wired into it spilling cyan light across the floor. A wooden board on the right reads St Martha’s Secondary Honours Board.',
  failAlt: 'A school gym hall where an enormous concertinaed heap of blue mats fills the middle of the floor. A gymnastics team carries on performing around it while everyone watching clamps their hands over their ears, two huge speakers blasting at either side. A man stands in the doorway with his arms folded, delighted.',
  winAlt: 'A school gym hall at dusk with the lights on. Blue landing mats are unfolded flat and true across the floor in a neat tiled rectangle, and a student in P.E. kit is clearing the vaulting horse mid-flight while others stretch at the wall bars behind. The AV cabinet at the side is closed and quiet with its lights green. In the open doorway a middle-aged man in a shirt and lanyard watches with his arms hanging at his sides.',

  hook: 'Somebody reported the IT teacher for the state of the network, and the IT teacher has worked out who. ' +
        'The gym hall is locked, the gymnastics team have their county qualifier in forty minutes, and the PA is ' +
        'playing a fourteen-second loop of dial-up modem handshake at considerable volume. The way in is his own ' +
        'prized custom mechanical keyboard, wired into the AV cabinet where anyone can reach it. He is that confident.',
  brief: 'You have fifteen minutes. Get past the macro pad, get the vaulting horse to the right height, and get the ' +
         'mats to deploy in one piece.',
  stakes: 'Get the mat size wrong and they deploy at the wrong size and concertina into one enormous folded lump in ' +
          'the middle of the floor — and the PA locks to modem tones at full volume for the entire routine. The team ' +
          'performs around the lump. He watches from the doorway with his arms folded, happier than he has ever been.',
  win: 'The macro pad gives up, the horse comes up to meet him at exactly the top of his flight, and the mats unfold ' +
       'flat and true across the floor. Their music comes through the PA about nine seconds later. He is still ' +
       'standing in the doorway, but the arms have come unfolded.',

  objects: [
    { id: 'note', name: 'Taped note', where: 'inside the AV cabinet door',
      clue: '<b>MACRO PAD.</b> &ldquo;Passcode is {{perm.n}} keys long and uses <b>{{perm.keys}}</b> in some order. ' +
            'Written down because I am not worried about you.&rdquo;' },
    { id: 'guardspec', name: 'Printed spec', where: 'pinned above the cabinet',
      clue: 'BRUTE-FORCE GUARD. &ldquo;Trips only when told <b>exactly how many different passcodes that ' +
            'allows</b>. One wrong figure and it stays shut.&rdquo;' },
    { id: 'notebook', name: 'Coaching notebook', where: 'open on the bench',
      clue: 'Her flight, modelled off the video: <b>h = &minus;{{vault.a}}t&sup2; + {{vault.b}}t + {{vault.c}}</b>, ' +
            'with h in metres and t in seconds.' },
    { id: 'physiocard', name: 'Physio’s card', where: 'in the first-aid box',
      clue: '&ldquo;The horse must be set to <b>the height she actually reaches at the top of her flight</b>. ' +
            'Anywhere else and she comes down on the frame. This is not negotiable.&rdquo;' },
    { id: 'plan', name: 'Floor plan', where: 'screwed to the wall by the honours board',
      clue: 'TUMBLING FLOOR — <b>{{mat.W}} m by {{mat.L}} m</b>. Sprung. Do not drag equipment across it.' },
    { id: 'deploy', name: 'Deployment manual', where: 'in the mat store',
      clue: '&ldquo;Mats deploy from the wall as <b>identical squares</b> of whatever size you dial in. No gaps, no ' +
            'overlaps, nothing cut. Dial the <b>largest size that works</b> — anything smaller wastes deployment ' +
            'cycles and the floor sensor logs it.&rdquo;' },
    { id: 'ropes', name: 'Climbing ropes', where: 'tied off at the wall', clue: null,
      flavour: 'Tied off in a knot you are fairly sure is not the regulation one. Not your problem today.' },
    { id: 'honours', name: 'Honours board', where: 'above the wall bars', clue: null,
      flavour: 'Gold lettering, going back to 1974. The last four years are gymnastics, gymnastics, gymnastics, ' +
               'gymnastics. Which is rather the point.' }
  ],

  locks: [
    {
      id: 'mechanical-keyboard-perms',
      key: 'perm',
      name: 'The macro pad',
      art: 'it-mechanical-keyboard-perms',
      artAlt: 'A custom mechanical keyboard wired into a glowing AV cabinet, with a four-key macro pad beside it and a bare overload-limit dial numbered 1 to 100.',
      brief: 'The pad’s brute-force guard trips only if you tell it exactly how many passcodes it would have to try. ' +
             'Set the overload dial to that number.',
      instrument: { kind: 'dial', label: 'Overload limit', min: 1, max: 100, step: 1, decimals: 0,
                    unit: '', start: 1, verb: 'Set the limit' },
      variants: [
        {
          "keys": "A, A, B, C",
          "n": 4,
          "denom": 2,
          "answer": 12,
          "miss": 24
        },
        {
          "keys": "A, A, B, B",
          "n": 4,
          "denom": 4,
          "answer": 6,
          "miss": 24
        }
      ],
      missTitle: '{{perm.miss}} counts codes that are not different.',
      missSays: '{{perm.n}}! = {{perm.miss}} is the number of orderings of {{perm.n}} <i>distinct</i> keys. These ' +
                'keys are not all distinct: swap two identical letters and the passcode you type is the same one. ' +
                'Every real passcode has been counted more than once.',
      hints: [
        '{{perm.n}} keys in a row would be {{perm.n}}! arrangements if they were all different. Some of them repeat. ' +
        'Does swapping two identical keys produce a passcode the pad could tell apart?',
        'Count all {{perm.n}}! orderings first, then divide by the number of ways the identical letters could be ' +
        'rearranged among themselves — a factorial for each repeated letter, multiplied together.',
        '{{perm.n}}! = {{perm.miss}} orderings. The repeats account for a factor of {{perm.denom}}, so ' +
        '{{perm.miss}} &divide; {{perm.denom}} = <b>{{perm.answer}}</b>.'
      ],
      solve: '{{perm.n}}! &divide; {{perm.denom}} = {{perm.miss}} &divide; {{perm.denom}} = ' +
             '<b>{{perm.answer}}</b> distinct passcodes.',
      onOpen: 'The pad accepts the figure, decides you are staff, and lights up green. Somewhere behind the wall a ' +
              'relay closes.'
    },
    {
      id: 'vault-trajectory-vertex',
      key: 'vault',
      name: 'The vaulting horse',
      art: 'it-vault-trajectory-vertex',
      artAlt: 'A vaulting horse on a gym floor with a powered height column beside it, the column’s scale marked in metres with no handle set.',
      brief: 'The horse rises to meet the gymnast at the top of her flight. Set it anywhere else and she comes down ' +
             'on the frame.',
      instrument: { kind: 'slider', label: 'Horse height', min: 0, max: 5, step: 0.1, decimals: 1,
                    unit: 'm', start: 0, verb: 'Raise the horse' },
      variants: [
        {
          "a": 2,
          "b": "4.8",
          "c": "0.12",
          "t": 1.2,
          "answer": 3.0,
          "miss": 1.2,
          "aTxt": "3.0",
          "mTxt": "1.2"
        },
        {
          "a": 4,
          "b": "8",
          "c": "0.2",
          "t": 1.0,
          "answer": 4.2,
          "miss": 1.0,
          "aTxt": "4.2",
          "mTxt": "1.0"
        },
        {
          "a": 2,
          "b": "3.6",
          "c": "0.08",
          "t": 0.9,
          "answer": 1.7,
          "miss": 0.9,
          "aTxt": "1.7",
          "mTxt": "0.9"
        },
        {
          "a": 2,
          "b": "4",
          "c": "0.1",
          "t": 1.0,
          "answer": 2.1,
          "miss": 1.0,
          "aTxt": "2.1",
          "mTxt": "1.0"
        },
        {
          "a": 2,
          "b": "4.4",
          "c": "0.28",
          "t": 1.1,
          "answer": 2.7,
          "miss": 1.1,
          "aTxt": "2.7",
          "mTxt": "1.1"
        },
        {
          "a": 2,
          "b": "5.2",
          "c": "0.32",
          "t": 1.3,
          "answer": 3.7,
          "miss": 1.3,
          "aTxt": "3.7",
          "mTxt": "1.3"
        },
        {
          "a": 3,
          "b": "6",
          "c": "0.4",
          "t": 1.0,
          "answer": 3.4,
          "miss": 1.0,
          "aTxt": "3.4",
          "mTxt": "1.0"
        },
        {
          "a": 2,
          "b": "4",
          "c": "0.4",
          "t": 1.0,
          "answer": 2.4,
          "miss": 1.0,
          "aTxt": "2.4",
          "mTxt": "1.0"
        },
        {
          "a": 3,
          "b": "7.2",
          "c": "0.18",
          "t": 1.2,
          "answer": 4.5,
          "miss": 1.2,
          "aTxt": "4.5",
          "mTxt": "1.2"
        }
      ],
      missTitle: '{{vault.mTxt}} is <i>when</i>, not <i>how high</i>.',
      missSays: '&minus;b&frasl;2a = {{vault.mTxt}} is the time at which she reaches the top — {{vault.mTxt}} ' +
                'seconds. The height only appears when that t is substituted back into the equation. You are one ' +
                'step from it.',
      hints: [
        'You have been asked for a height, and the equation gives height in terms of time. The turning point tells ' +
        'you a <i>time</i> first.',
        'The peak of a quadratic is at t = &minus;b &divide; 2a. Work that out, then put it back into ' +
        'h = &minus;{{vault.a}}t&sup2; + {{vault.b}}t + {{vault.c}}.',
        't = {{vault.b}} &divide; (2 &times; {{vault.a}}) = {{vault.t}} s. Then h = ' +
        '&minus;{{vault.a}}({{vault.t}}&sup2;) + {{vault.b}}({{vault.t}}) + {{vault.c}} = ' +
        '<b>{{vault.aTxt}} m</b>.'
      ],
      solve: 't at the peak = &minus;b/2a = {{vault.t}} s, and substituting back gives h = ' +
             '<b>{{vault.aTxt}} m</b>.',
      onOpen: 'The column runs up and stops with a hydraulic sigh. She will meet it at the top of the arc and never ' +
              'know it moved.'
    },
    {
      id: 'mat-tiling-hcf',
      key: 'mat',
      name: 'Mat tiling',
      art: 'it-mat-tiling-hcf',
      artAlt: 'A stack of blue gym mats beside a wall-mounted deployment panel, its mat-size slider track marked in metres with no handle set.',
      brief: 'The mats deploy as identical squares of whatever size you dial in. Any gap or overlap and the floor ' +
             'sensor refuses the routine.',
      instrument: { kind: 'slider', label: 'Mat size', min: 0.1, max: 5, step: 0.1, decimals: 1,
                    unit: 'm', start: 0.1, verb: 'Deploy the mats' },
      variants: [
        {
          "W": "4.8",
          "L": "7.2",
          "w10": 48,
          "l10": 72,
          "across": 2,
          "along": 3,
          "answer": 2.4,
          "miss": 1.2,
          "aTxt": "2.4",
          "mTxt": "1.2"
        },
        {
          "W": "3.6",
          "L": "8.4",
          "w10": 36,
          "l10": 84,
          "across": 3,
          "along": 7,
          "answer": 1.2,
          "miss": 0.6,
          "aTxt": "1.2",
          "mTxt": "0.6"
        },
        {
          "W": "10.2",
          "L": "13.6",
          "w10": 102,
          "l10": 136,
          "across": 3,
          "along": 4,
          "answer": 3.4,
          "miss": 1.7,
          "aTxt": "3.4",
          "mTxt": "1.7"
        },
        {
          "W": "8.4",
          "L": "11.2",
          "w10": 84,
          "l10": 112,
          "across": 3,
          "along": 4,
          "answer": 2.8,
          "miss": 1.4,
          "aTxt": "2.8",
          "mTxt": "1.4"
        },
        {
          "W": "5.4",
          "L": "12.6",
          "w10": 54,
          "l10": 126,
          "across": 3,
          "along": 7,
          "answer": 1.8,
          "miss": 0.9,
          "aTxt": "1.8",
          "mTxt": "0.9"
        },
        {
          "W": "8.4",
          "L": "12.6",
          "w10": 84,
          "l10": 126,
          "across": 2,
          "along": 3,
          "answer": 4.2,
          "miss": 2.1,
          "aTxt": "4.2",
          "mTxt": "2.1"
        },
        {
          "W": "7.6",
          "L": "11.4",
          "w10": 76,
          "l10": 114,
          "across": 2,
          "along": 3,
          "answer": 3.8,
          "miss": 1.9,
          "aTxt": "3.8",
          "mTxt": "1.9"
        },
        {
          "W": "9.6",
          "L": "14.4",
          "w10": 96,
          "l10": 144,
          "across": 2,
          "along": 3,
          "answer": 4.8,
          "miss": 2.4,
          "aTxt": "4.8",
          "mTxt": "2.4"
        }
      ],
      missTitle: '{{mat.mTxt}} tiles it — but it is not the largest that does.',
      missSays: '{{mat.mTxt}} m does divide both {{mat.W}} and {{mat.L}} exactly, so it really would tile the floor. ' +
                'But the manual asks for the <b>largest</b> size that works, and {{mat.aTxt}} m divides both as ' +
                'well — it is a common factor, just not the highest one.',
      hints: [
        'The mat has to fit a whole number of times along <i>both</i> sides. Which sizes divide {{mat.W}} and ' +
        '{{mat.L}} exactly?',
        'Work in tenths of a metre and the floor is {{mat.w10}} by {{mat.l10}}. You want the largest number that ' +
        'divides both — the highest common factor.',
        'The highest common factor of {{mat.w10}} and {{mat.l10}} is {{mat.answer}} &times; 10 tenths, so the mat is ' +
        '<b>{{mat.aTxt}} m</b> — {{mat.across}} along the {{mat.W}} m side and {{mat.along}} along the {{mat.L}} m side.'
      ],
      solve: 'In tenths, HCF({{mat.w10}}, {{mat.l10}}) gives the largest square mat: <b>{{mat.aTxt}} m</b> ' +
             '({{mat.across}} by {{mat.along}} of them).',
      onOpen: 'The mats come out of the wall, unfold flat, and meet edge to edge across the whole tumbling floor ' +
              'without a single gap. The sensor goes green and stays green.'
    }
  ]
};
