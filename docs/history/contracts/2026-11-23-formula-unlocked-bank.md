FORMULA-UNLOCKED-BANK. Home lane. Tier: Medium: merge on green with merge-pr.py (no hold). Send: now (#891 merged as 38895242; main green). Branch from origin/main (5ac0fe99 or later).
From Project Claude; Jon, 23 Nov 2026, 16:29 (A-Level mode repeated a question in 19), 16:31 ("high priority as it is student facing").
Recommended: Claude Code, Opus, medium effort. Every value is given below and the game's own verifier checks every one in SymPy (Project Claude's trial run: PASS).

TASK: Stop Formula Unlocked's A-Level mode repeating questions, and bring every level to at least 40 questions by adding 57 checked questions (GCSE 11, A-Level 20, Level 4 26).

ROOT CAUSE: Shown: games/formula-unlocked/index.html:423 builds the A-Level bank as GCSE stage 2-4 plus Q_ALEVEL, splits it by stage (:427-430), takes 5 from each of stages 2, 3 and 4 (which already include Q_ALEVEL's items), then (:436) adds 5 more drawn from Q_ALEVEL again; with 6 A-Level questions, a session repeats one 99.8% of the time (Project Claude's simulation of that code, 100 000 sessions). Shown: the banks hold GCSE 29, Q_ALEVEL 6 (stages 2/3/4: 2/2/2), Q_LEVEL4 14 (read from the page; scripts/verify-formula-unlocked.py:40), so every level serves fewer than 40 (A-Level 25 distinct: 19 GCSE stage 2-4 + 6). Inferred, not shown here (the cloud lane will test it separately): check-banks.py's B4 passes the game because it counts all three arrays on the page (49) at every level.

CLASS CHECK: The repeat is local: one game's startGame() draws twice from overlapping lists; no shared code builds its pool. The fix is local, and the game's verifier gains a session check so the shape cannot come back in this game. The site-wide B4 gap (a level's count taken from every array on the page, not what the level serves) is shared infrastructure and goes to the cloud lane in its own contract: do not touch check-banks.py here.

EXACT CHANGE:
1. First commit: the standing close-out for WWIUT-RESTORE-7 (#891): record its merge commit 38895242, route and main's run IDs (check-site 45223623100, phone-fit-full 45223623121, pages 45223622181) in docs/handover/home.md; git mv docs/handover/contracts/2026-11-23-wwiut-restore-7.md docs/history/contracts/. Record Project Claude's ruling on the 5 sources in the same entry, verbatim: "Ruling (Project Claude, 23 Nov): keep all five sources and all seven jobs. Each page was fetched by Project Claude on 23 Nov and answers with the content the job cites: the 403s and the 522 are the sites refusing automated clients; the two 404s (uhsussex ?p=5862, the FSA hot-holding PDF) answer for a browser fetch. The BNMS redirect is noted; that job keeps its other source. No change to data/uses.json." Also record in the same entry: "#888: the end-task refusal is expected. 3058b98 is the cloud lane's WWIUT-BATCH-MERGE commit (it took #888 over by contract); #888 merged as a5b3742 and was closed out in the cloud entry. Nothing to do on that branch." In the same commit save this contract verbatim as docs/handover/contracts/2026-11-23-formula-unlocked-bank.md.
2. Questions: append the APPENDIX blocks, verbatim, to the end of Q_GCSE, Q_ALEVEL and Q_LEVEL4 respectively (each block after the array's last item, a comma between). Do not change any existing question. Expected after: Q_GCSE 40 (stages 1/2/3/4: 14/12/9/5), Q_ALEVEL 26 (2/3/4: 9/9/8), Q_LEVEL4 40 (1/2/3/4: 8/12/12/8).
3. The A-Level draw (:435-436): replace
       pool=[...s2.slice(0,5),...s3.slice(0,5),...s4.slice(0,5),...shuffle([...Q_ALEVEL]).slice(0,5)];
   with
       pool=[...s2.slice(0,6),...s3.slice(0,7),...s4.slice(0,7)];
   with a one-line comment: each stage's list holds the GCSE and A-Level questions of that stage once each, so slices never repeat a question. GCSE and Level 4 draws are unchanged (they already take distinct slices).
4. scripts/verify-formula-unlocked.py:
   a. BANKS (:40) becomes {'Q_GCSE': 40, 'Q_ALEVEL': 26, 'Q_LEVEL4': 40}; update the docstring's counts.
   b. GREEK (:43) becomes {'pi': 'PI', 'rho': 'rho', 'sigma': 'sigma', 'epsilon': 'epsilon', 'tau': 'tau', 'lambda': 'lambda_', 'alpha': 'alpha', 'delta': 'delta', 'mu': 'mu', 'omega': 'omega', 'eta': 'eta', 'beta': 'beta'} (the new questions use these letters; lambda maps to lambda_ because lambda is a Python keyword).
   c. In tokens(), the \ln branch (:94-104): after the loop that skips spaces, skip a following \left so that \ln\left( ... \right) reads as ln of the bracket. Insert, before "if s[j] == '{':":
              if s.startswith('\\left', j):
                  j += 5
   d. Add a session check: for each level, run startGame()'s pool building in Chromium 1000 times and fail if any session holds the same question twice or has fewer than 20 questions; a self-test plant restores the old A-Level line and must be caught. Every existing self-test plant still caught.
   Project Claude ran a-c on a copy of main with the appendix and step 3 applied: PASS, every existing plant caught (d is new and was not run).
5. /updates/: one dated line, e.g. "23 Nov 2026: Formula Unlocked: 57 new questions (every level now has 40 or more), and A-Level games no longer repeat a question."
6. Merge with merge-pr.py when the Gate is green; record the merge commit and main's run IDs in docs/handover/home.md; run end-task.

DO NOT TOUCH: any existing question in the three banks; the GCSE and Level 4 draws; scoring, hints logic, timer, level buttons and the URL (the level-in-the-URL fix is a separate shared change); check-banks.py, bank_common.py and data/check-ledger.json (B4 goes to the cloud lane; regenerate the ledger only if CI's own ledger step requires it, and say so); schools/assets/; any other game; canon, AGENTS.md, the roster, docs/todo.md, docs/handover/cloud.md; .github/workflows/, scripts/ci-*, merge-pr.py.

SUCCESS CONDITION: the three banks hold 40 / 26 / 40 with the stage counts in step 2; verify-formula-unlocked.py passes with every question read into SymPy and clicked in Chromium (106 questions), its session check passing for all three levels and every self-test plant caught; Gate green; merged; main green; home.md records it.

STOP IF: any appended question fails the verifier (report the item and the failure; do not edit its maths: Project Claude rules); an existing self-test plant is missed after the BANKS change; KATEX-ERRORS (cloud) has an open PR that edits games/formula-unlocked/index.html (report before pushing); a check still fails after your second fix (standing rule); merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").

APPENDIX (verbatim; each block goes at the end of the named array):
// ---- append to Q_GCSE ----
{stage:1,formula:'A = lw',target:'w',correct:'w = \\dfrac{A}{l}',d:['w = Al','w = A - l','w = \\dfrac{l}{A}'],
hints:['w is multiplied by l','Divide both sides by l'],
steps:['A = lw','\\dfrac{A}{l} = w','w = \\dfrac{A}{l}']},

{stage:1,formula:'v = \\dfrac{d}{t}',target:'d',correct:'d = vt',d:['d = \\dfrac{v}{t}','d = v + t','d = \\dfrac{t}{v}'],
hints:['d is divided by t','Multiply both sides by t'],
steps:['v = \\dfrac{d}{t}','vt = d','d = vt']},

{stage:1,formula:'P = 4s',target:'s',correct:'s = \\dfrac{P}{4}',d:['s = 4P','s = P - 4','s = \\dfrac{4}{P}'],
hints:['s is multiplied by 4','Divide both sides by 4'],
steps:['P = 4s','\\dfrac{P}{4} = s','s = \\dfrac{P}{4}']},

{stage:1,formula:'C = 2\\pi r',target:'r',correct:'r = \\dfrac{C}{2\\pi}',d:['r = 2\\pi C','r = C - 2\\pi','r = \\dfrac{2\\pi}{C}'],
hints:['r is multiplied by 2π','Divide both sides by 2π'],
steps:['C = 2\\pi r','\\dfrac{C}{2\\pi} = r','r = \\dfrac{C}{2\\pi}']},

{stage:2,formula:'P = 2l + 2w',target:'l',correct:'l = \\dfrac{P - 2w}{2}',d:['l = P - 2w','l = \\dfrac{P}{2} - 2w','l = \\dfrac{P + 2w}{2}'],
hints:['Subtract 2w from both sides','Divide both sides by 2'],
steps:['P = 2l + 2w','P - 2w = 2l','l = \\dfrac{P - 2w}{2}']},

{stage:2,formula:'y = 3x - 5',target:'x',correct:'x = \\dfrac{y + 5}{3}',d:['x = \\dfrac{y - 5}{3}','x = \\dfrac{y}{3} + 5','x = 3y + 5'],
hints:['Add 5 to both sides','Divide both sides by 3'],
steps:['y = 3x - 5','y + 5 = 3x','x = \\dfrac{y + 5}{3}']},

{stage:2,formula:'E = mgh',target:'h',correct:'h = \\dfrac{E}{mg}',d:['h = Emg','h = \\dfrac{mg}{E}','h = E - mg'],
hints:['h is multiplied by m and by g','Divide both sides by mg'],
steps:['E = mgh','\\dfrac{E}{mg} = h','h = \\dfrac{E}{mg}']},

{stage:2,formula:'V = \\dfrac{1}{3}\\pi r^2 h',target:'h',correct:'h = \\dfrac{3V}{\\pi r^2}',d:['h = \\dfrac{V}{3\\pi r^2}','h = \\dfrac{3V}{\\pi r}','h = 3V\\pi r^2'],
hints:['Multiply both sides by 3','Divide both sides by πr²'],
steps:['V = \\dfrac{1}{3}\\pi r^2 h','3V = \\pi r^2 h','h = \\dfrac{3V}{\\pi r^2}']},

{stage:3,formula:'E = mc^2',target:'c',correct:'c = \\sqrt{\\dfrac{E}{m}}',d:['c = \\dfrac{E}{m}','c = \\dfrac{\\sqrt{E}}{m}','c = \\sqrt{Em}'],
hints:['Divide both sides by m','Square root both sides'],
steps:['E = mc^2','\\dfrac{E}{m} = c^2','c = \\sqrt{\\dfrac{E}{m}}']},

{stage:3,formula:'A = 4\\pi r^2',target:'r',correct:'r = \\sqrt{\\dfrac{A}{4\\pi}}',d:['r = \\dfrac{A}{4\\pi}','r = \\sqrt{4\\pi A}','r = \\dfrac{\\sqrt{A}}{4\\pi}'],
hints:['Divide both sides by 4π','Square root both sides'],
steps:['A = 4\\pi r^2','\\dfrac{A}{4\\pi} = r^2','r = \\sqrt{\\dfrac{A}{4\\pi}}']},

{stage:4,formula:'\\dfrac{x}{a} + \\dfrac{x}{b} = 1',target:'x',correct:'x = \\dfrac{ab}{a + b}',d:['x = a + b','x = \\dfrac{a + b}{ab}','x = ab'],
hints:['Multiply every term by ab','Factorise out x, then divide by (a + b)'],
steps:['\\dfrac{x}{a} + \\dfrac{x}{b} = 1','bx + ax = ab','x(a + b) = ab','x = \\dfrac{ab}{a + b}']},

// ---- append to Q_ALEVEL ----
{stage:2,formula:'s = \\dfrac{(u + v)t}{2}',target:'t',correct:'t = \\dfrac{2s}{u + v}',d:['t = \\dfrac{s}{2(u + v)}','t = 2s - (u + v)','t = \\dfrac{2s}{u} + v'],
hints:['Multiply both sides by 2','Divide both sides by (u + v)'],
steps:['s = \\dfrac{(u + v)t}{2}','2s = (u + v)t','t = \\dfrac{2s}{u + v}']},

{stage:2,formula:'s = \\dfrac{(u + v)t}{2}',target:'u',correct:'u = \\dfrac{2s}{t} - v',d:['u = \\dfrac{2s - v}{t}','u = \\dfrac{s}{2t} - v','u = \\dfrac{2s}{t} + v'],
hints:['Multiply by 2 and divide by t','Subtract v from both sides'],
steps:['s = \\dfrac{(u + v)t}{2}','\\dfrac{2s}{t} = u + v','u = \\dfrac{2s}{t} - v']},

{stage:2,formula:'A = P(1 + r)^n',target:'P',correct:'P = \\dfrac{A}{(1 + r)^n}',d:['P = A(1 + r)^n','P = \\dfrac{A}{1 + r^n}','P = A - (1 + r)^n'],
hints:['P is multiplied by (1 + r)ⁿ','Divide both sides by (1 + r)ⁿ'],
steps:['A = P(1 + r)^n','P = \\dfrac{A}{(1 + r)^n}']},

{stage:2,formula:'v^2 = u^2 + 2as',target:'a',correct:'a = \\dfrac{v^2 - u^2}{2s}',d:['a = \\dfrac{v^2 + u^2}{2s}','a = \\dfrac{v^2 - u^2}{s}','a = \\dfrac{(v - u)^2}{2s}'],
hints:['Subtract u² from both sides','Divide both sides by 2s'],
steps:['v^2 = u^2 + 2as','v^2 - u^2 = 2as','a = \\dfrac{v^2 - u^2}{2s}']},

{stage:2,formula:'F = \\dfrac{mv^2}{r}',target:'r',correct:'r = \\dfrac{mv^2}{F}',d:['r = Fmv^2','r = \\dfrac{F}{mv^2}','r = \\dfrac{mv}{F}'],
hints:['Multiply both sides by r','Divide both sides by F'],
steps:['F = \\dfrac{mv^2}{r}','Fr = mv^2','r = \\dfrac{mv^2}{F}']},

{stage:2,formula:'E = \\dfrac{1}{2}kx^2',target:'k',correct:'k = \\dfrac{2E}{x^2}',d:['k = \\dfrac{E}{2x^2}','k = \\dfrac{2E}{x}','k = 2Ex^2'],
hints:['Multiply both sides by 2','Divide both sides by x²'],
steps:['E = \\dfrac{1}{2}kx^2','2E = kx^2','k = \\dfrac{2E}{x^2}']},

{stage:2,formula:'y = ae^{kx}',target:'k',correct:'k = \\dfrac{1}{x}\\ln\\left(\\dfrac{y}{a}\\right)',d:['k = \\ln\\left(\\dfrac{y}{ax}\\right)','k = \\dfrac{\\ln y - a}{x}','k = x\\ln\\left(\\dfrac{y}{a}\\right)'],
hints:['Divide both sides by a','Take ln of both sides, then divide by x'],
steps:['y = ae^{kx}','\\dfrac{y}{a} = e^{kx}','\\ln\\left(\\dfrac{y}{a}\\right) = kx','k = \\dfrac{1}{x}\\ln\\left(\\dfrac{y}{a}\\right)']},

{stage:3,formula:'F = \\dfrac{mv^2}{r}',target:'v',correct:'v = \\sqrt{\\dfrac{Fr}{m}}',d:['v = \\dfrac{Fr}{m}','v = \\sqrt{\\dfrac{m}{Fr}}','v = \\sqrt{Frm}'],
hints:['Multiply both sides by r, then divide by m','Square root both sides'],
steps:['F = \\dfrac{mv^2}{r}','\\dfrac{Fr}{m} = v^2','v = \\sqrt{\\dfrac{Fr}{m}}']},

{stage:3,formula:'F = \\dfrac{Gm_1 m_2}{r^2}',target:'r',correct:'r = \\sqrt{\\dfrac{Gm_1 m_2}{F}}',d:['r = \\dfrac{Gm_1 m_2}{F}','r = \\sqrt{\\dfrac{F}{Gm_1 m_2}}','r = \\dfrac{\\sqrt{Gm_1 m_2}}{F}'],
hints:['Multiply both sides by r², then divide by F','Square root both sides'],
steps:['F = \\dfrac{Gm_1 m_2}{r^2}','r^2 = \\dfrac{Gm_1 m_2}{F}','r = \\sqrt{\\dfrac{Gm_1 m_2}{F}}']},

{stage:3,formula:'A = P(1 + r)^n',target:'r',correct:'r = \\sqrt[n]{\\dfrac{A}{P}} - 1',d:['r = \\sqrt[n]{\\dfrac{A}{P} - 1}','r = \\dfrac{A}{nP} - 1','r = \\sqrt[n]{A - P}'],
hints:['Divide both sides by P','Take the nth root, then subtract 1'],
steps:['A = P(1 + r)^n','\\dfrac{A}{P} = (1 + r)^n','\\sqrt[n]{\\dfrac{A}{P}} = 1 + r','r = \\sqrt[n]{\\dfrac{A}{P}} - 1']},

{stage:3,formula:'y = ae^{kx}',target:'x',correct:'x = \\dfrac{1}{k}\\ln\\left(\\dfrac{y}{a}\\right)',d:['x = \\ln\\left(\\dfrac{y}{ak}\\right)','x = k\\ln\\left(\\dfrac{y}{a}\\right)','x = \\dfrac{\\ln y}{ak}'],
hints:['Divide both sides by a','Take ln of both sides, then divide by k'],
steps:['y = ae^{kx}','\\ln\\left(\\dfrac{y}{a}\\right) = kx','x = \\dfrac{1}{k}\\ln\\left(\\dfrac{y}{a}\\right)']},

{stage:3,formula:'E = \\dfrac{1}{2}kx^2',target:'x',correct:'x = \\sqrt{\\dfrac{2E}{k}}',d:['x = \\dfrac{2E}{k}','x = \\sqrt{\\dfrac{E}{2k}}','x = \\sqrt{2Ek}'],
hints:['Multiply both sides by 2, then divide by k','Square root both sides'],
steps:['E = \\dfrac{1}{2}kx^2','\\dfrac{2E}{k} = x^2','x = \\sqrt{\\dfrac{2E}{k}}']},

{stage:3,formula:'v = \\omega\\sqrt{A^2 - x^2}',target:'x',correct:'x = \\sqrt{A^2 - \\dfrac{v^2}{\\omega^2}}',d:['x = A - \\dfrac{v}{\\omega}','x = \\sqrt{A^2 + \\dfrac{v^2}{\\omega^2}}','x = \\sqrt{\\dfrac{v^2}{\\omega^2} - A^2}'],
hints:['Divide by ω, then square both sides','Rearrange for x², then square root'],
steps:['\\dfrac{v}{\\omega} = \\sqrt{A^2 - x^2}','\\dfrac{v^2}{\\omega^2} = A^2 - x^2','x = \\sqrt{A^2 - \\dfrac{v^2}{\\omega^2}}']},

{stage:3,formula:'y = \\ln(3x - 2)',target:'x',correct:'x = \\dfrac{e^y + 2}{3}',d:['x = \\dfrac{e^y - 2}{3}','x = \\dfrac{e^{y + 2}}{3}','x = \\dfrac{\\ln y + 2}{3}'],
hints:['Undo ln: raise e to the power of both sides','Add 2, then divide by 3'],
steps:['y = \\ln(3x - 2)','e^y = 3x - 2','x = \\dfrac{e^y + 2}{3}']},

{stage:4,formula:'y = \\dfrac{3x - 1}{x + 2}',target:'x',correct:'x = \\dfrac{2y + 1}{3 - y}',d:['x = \\dfrac{2y - 1}{3 - y}','x = \\dfrac{2y + 1}{y - 3}','x = \\dfrac{y + 1}{3 - 2y}'],
hints:['Multiply both sides by (x + 2) and expand','Collect the x terms on one side and factorise'],
steps:['y(x + 2) = 3x - 1','xy + 2y = 3x - 1','2y + 1 = 3x - xy = x(3 - y)','x = \\dfrac{2y + 1}{3 - y}']},

{stage:4,formula:'y = \\dfrac{x}{x + k}',target:'x',correct:'x = \\dfrac{ky}{1 - y}',d:['x = \\dfrac{ky}{y - 1}','x = \\dfrac{y}{1 - ky}','x = \\dfrac{k}{1 - y}'],
hints:['Multiply both sides by (x + k)','Collect the x terms and factorise'],
steps:['y(x + k) = x','xy + ky = x','ky = x - xy = x(1 - y)','x = \\dfrac{ky}{1 - y}']},

{stage:4,formula:'\\dfrac{1}{x} + \\dfrac{1}{y} = \\dfrac{1}{2}',target:'y',correct:'y = \\dfrac{2x}{x - 2}',d:['y = \\dfrac{2x}{2 - x}','y = x - 2','y = \\dfrac{x - 2}{2x}'],
hints:['Multiply every term by 2xy','Collect the y terms and factorise'],
steps:['2y + 2x = xy','2x = xy - 2y = y(x - 2)','y = \\dfrac{2x}{x - 2}']},

{stage:4,formula:'y = \\dfrac{a - x}{a + x}',target:'x',correct:'x = \\dfrac{a(1 - y)}{1 + y}',d:['x = \\dfrac{a(1 + y)}{1 - y}','x = \\dfrac{a(y - 1)}{1 + y}','x = \\dfrac{1 - y}{a(1 + y)}'],
hints:['Multiply both sides by (a + x) and expand','Collect the x terms on one side and factorise'],
steps:['y(a + x) = a - x','ay + xy = a - x','x + xy = a - ay','x(1 + y) = a(1 - y)','x = \\dfrac{a(1 - y)}{1 + y}']},

{stage:4,formula:'y = \\dfrac{e^x + 1}{e^x - 1}',target:'x',correct:'x = \\ln\\left(\\dfrac{y + 1}{y - 1}\\right)',d:['x = \\ln\\left(\\dfrac{y - 1}{y + 1}\\right)','x = \\dfrac{y + 1}{y - 1}','x = \\ln\\left(y + 1\\right) - 1'],
hints:['Multiply both sides by (eˣ − 1) and collect the eˣ terms','Make eˣ the subject, then take ln'],
steps:['y(e^x - 1) = e^x + 1','ye^x - e^x = y + 1','e^x = \\dfrac{y + 1}{y - 1}','x = \\ln\\left(\\dfrac{y + 1}{y - 1}\\right)']},

{stage:4,formula:'p = \\dfrac{q}{1 - qr}',target:'q',correct:'q = \\dfrac{p}{1 + pr}',d:['q = \\dfrac{p}{1 - pr}','q = \\dfrac{p}{1 - r}','q = \\dfrac{p}{1 + r}'],
hints:['Multiply both sides by (1 − qr) and expand','Collect the q terms and factorise'],
steps:['p(1 - qr) = q','p - pqr = q','p = q + pqr = q(1 + pr)','q = \\dfrac{p}{1 + pr}']},

// ---- append to Q_LEVEL4 ----
{stage:1,formula:'Q = It',target:'I',ctx:'Charge',correct:'I = \\dfrac{Q}{t}',d:['I = Qt','I = Q - t','I = \\dfrac{t}{Q}'],
hints:['I is multiplied by t','Divide both sides by t'],
steps:['Q = It','I = \\dfrac{Q}{t}']},

{stage:1,formula:'W = Fs',target:'s',ctx:'Work done',correct:'s = \\dfrac{W}{F}',d:['s = WF','s = W - F','s = \\dfrac{F}{W}'],
hints:['s is multiplied by F','Divide both sides by F'],
steps:['W = Fs','s = \\dfrac{W}{F}']},

{stage:1,formula:'P = \\dfrac{W}{t}',target:'W',ctx:'Power',correct:'W = Pt',d:['W = \\dfrac{P}{t}','W = P + t','W = \\dfrac{t}{P}'],
hints:['W is divided by t','Multiply both sides by t'],
steps:['P = \\dfrac{W}{t}','W = Pt']},

{stage:1,formula:'f = \\dfrac{1}{T}',target:'T',ctx:'Frequency and period',correct:'T = \\dfrac{1}{f}',d:['T = f','T = 1 - f','T = f^2'],
hints:['Multiply both sides by T','Divide both sides by f'],
steps:['fT = 1','T = \\dfrac{1}{f}']},

{stage:1,formula:'\\rho = \\dfrac{m}{V}',target:'V',ctx:'Density',correct:'V = \\dfrac{m}{\\rho}',d:['V = \\rho m','V = \\dfrac{\\rho}{m}','V = m - \\rho'],
hints:['Multiply both sides by V','Divide both sides by ρ'],
steps:['\\rho V = m','V = \\dfrac{m}{\\rho}']},

{stage:2,formula:'R = \\dfrac{\\rho L}{A}',target:'L',ctx:'Resistivity',correct:'L = \\dfrac{RA}{\\rho}',d:['L = \\dfrac{R\\rho}{A}','L = \\dfrac{A}{R\\rho}','L = RA\\rho'],
hints:['Multiply both sides by A','Divide both sides by ρ'],
steps:['RA = \\rho L','L = \\dfrac{RA}{\\rho}']},

{stage:2,formula:'\\dfrac{T}{J} = \\dfrac{\\tau}{r}',target:'\\tau',ctx:'Torsion equation',correct:'\\tau = \\dfrac{Tr}{J}',d:['\\tau = \\dfrac{TJ}{r}','\\tau = \\dfrac{J}{Tr}','\\tau = \\dfrac{T}{Jr}'],
hints:['τ is divided by r','Multiply both sides by r'],
steps:['\\dfrac{T}{J} = \\dfrac{\\tau}{r}','\\tau = \\dfrac{Tr}{J}']},

{stage:2,formula:'\\sigma = \\dfrac{My}{I}',target:'M',ctx:'Bending stress',correct:'M = \\dfrac{\\sigma I}{y}',d:['M = \\dfrac{\\sigma y}{I}','M = \\sigma Iy','M = \\dfrac{y}{\\sigma I}'],
hints:['Multiply both sides by I','Divide both sides by y'],
steps:['\\sigma I = My','M = \\dfrac{\\sigma I}{y}']},

{stage:2,formula:'P = \\dfrac{2\\pi NT}{60}',target:'T',ctx:'Power from torque (N in rev/min)',correct:'T = \\dfrac{60P}{2\\pi N}',d:['T = \\dfrac{2\\pi NP}{60}','T = \\dfrac{P}{120\\pi N}','T = \\dfrac{60P}{N}'],
hints:['Multiply both sides by 60','Divide both sides by 2πN'],
steps:['60P = 2\\pi NT','T = \\dfrac{60P}{2\\pi N}']},

{stage:2,formula:'v = f\\lambda',target:'\\lambda',ctx:'Wave speed',correct:'\\lambda = \\dfrac{v}{f}',d:['\\lambda = vf','\\lambda = \\dfrac{f}{v}','\\lambda = v - f'],
hints:['λ is multiplied by f','Divide both sides by f'],
steps:['v = f\\lambda','\\lambda = \\dfrac{v}{f}']},

{stage:2,formula:'x = \\alpha L t',target:'\\alpha',ctx:'Thermal expansion: x is the extension, t the temperature rise',correct:'\\alpha = \\dfrac{x}{Lt}',d:['\\alpha = xLt','\\alpha = \\dfrac{Lt}{x}','\\alpha = \\dfrac{xL}{t}'],
hints:['α is multiplied by L and by t','Divide both sides by Lt'],
steps:['x = \\alpha Lt','\\alpha = \\dfrac{x}{Lt}']},

{stage:2,formula:'X_L = 2\\pi fL',target:'f',ctx:'Inductive reactance',correct:'f = \\dfrac{X_L}{2\\pi L}',d:['f = 2\\pi LX_L','f = \\dfrac{2\\pi L}{X_L}','f = \\dfrac{X_L}{L} - 2\\pi'],
hints:['f is multiplied by 2πL','Divide both sides by 2πL'],
steps:['X_L = 2\\pi fL','f = \\dfrac{X_L}{2\\pi L}']},

{stage:3,formula:'X_C = \\dfrac{1}{2\\pi fC}',target:'C',ctx:'Capacitive reactance',correct:'C = \\dfrac{1}{2\\pi fX_C}',d:['C = 2\\pi fX_C','C = \\dfrac{X_C}{2\\pi f}','C = \\dfrac{2\\pi f}{X_C}'],
hints:['Multiply both sides by C','Divide both sides by \\(X_C\\)'],
steps:['CX_C = \\dfrac{1}{2\\pi f}','C = \\dfrac{1}{2\\pi fX_C}']},

{stage:3,formula:'f = \\dfrac{1}{2\\pi\\sqrt{LC}}',target:'C',ctx:'Resonant frequency',correct:'C = \\dfrac{1}{4\\pi^2 f^2 L}',d:['C = \\dfrac{1}{2\\pi f^2 L}','C = \\dfrac{1}{4\\pi^2 fL}','C = 4\\pi^2 f^2 L'],
hints:['Square both sides','Multiply by C, then divide by 4π²f²'],
steps:['f^2 = \\dfrac{1}{4\\pi^2 LC}','C = \\dfrac{1}{4\\pi^2 f^2 L}']},

{stage:3,formula:'E = \\dfrac{1}{2}CV^2',target:'V',ctx:'Energy stored in a capacitor',correct:'V = \\sqrt{\\dfrac{2E}{C}}',d:['V = \\dfrac{2E}{C}','V = \\sqrt{\\dfrac{E}{2C}}','V = \\sqrt{2EC}'],
hints:['Multiply by 2, then divide by C','Square root both sides'],
steps:['\\dfrac{2E}{C} = V^2','V = \\sqrt{\\dfrac{2E}{C}}']},

{stage:3,formula:'\\delta = \\dfrac{FL^3}{3EI}',target:'L',ctx:'Cantilever deflection',correct:'L = \\sqrt[3]{\\dfrac{3EI\\delta}{F}}',d:['L = \\dfrac{3EI\\delta}{F}','L = \\sqrt{\\dfrac{3EI\\delta}{F}}','L = \\sqrt[3]{\\dfrac{F\\delta}{3EI}}'],
hints:['Multiply by 3EI, then divide by F','Take the cube root'],
steps:['L^3 = \\dfrac{3EI\\delta}{F}','L = \\sqrt[3]{\\dfrac{3EI\\delta}{F}}']},

{stage:3,formula:'Z = \\sqrt{R^2 + X^2}',target:'X',ctx:'Impedance',correct:'X = \\sqrt{Z^2 - R^2}',d:['X = Z - R','X = \\sqrt{Z^2 + R^2}','X = \\sqrt{Z - R^2}'],
hints:['Square both sides','Subtract R², then square root'],
steps:['Z^2 = R^2 + X^2','X = \\sqrt{Z^2 - R^2}']},

{stage:3,formula:'v = \\sqrt{\\dfrac{T}{\\mu}}',target:'T',ctx:'Wave on a string',correct:'T = \\mu v^2',d:['T = \\dfrac{v^2}{\\mu}','T = \\mu v','T = \\sqrt{\\mu v}'],
hints:['Square both sides','Multiply both sides by μ'],
steps:['v^2 = \\dfrac{T}{\\mu}','T = \\mu v^2']},

{stage:3,formula:'P = \\dfrac{V^2}{R}',target:'V',ctx:'Power in a resistor',correct:'V = \\sqrt{PR}',d:['V = PR','V = \\sqrt{\\dfrac{P}{R}}','V = \\dfrac{\\sqrt{P}}{R}'],
hints:['Multiply both sides by R','Square root both sides'],
steps:['PR = V^2','V = \\sqrt{PR}']},

{stage:3,formula:'\\omega = \\sqrt{\\dfrac{k}{m}}',target:'m',ctx:'Natural frequency (rad/s)',correct:'m = \\dfrac{k}{\\omega^2}',d:['m = \\dfrac{k}{\\omega}','m = k\\omega^2','m = \\dfrac{\\omega^2}{k}'],
hints:['Square both sides','Rearrange for m'],
steps:['\\omega^2 = \\dfrac{k}{m}','m = \\dfrac{k}{\\omega^2}']},

{stage:4,formula:'R_T = R_1 + \\dfrac{R_2 R_3}{R_2 + R_3}',target:'R_2',ctx:'Series-parallel resistors',correct:'R_2 = \\dfrac{R_3(R_T - R_1)}{R_3 - R_T + R_1}',d:['R_2 = \\dfrac{R_3(R_T - R_1)}{R_3 + R_T - R_1}','R_2 = R_T - R_1 - R_3','R_2 = \\dfrac{R_T - R_1}{R_3}'],
hints:['Subtract R₁, then multiply by (R₂ + R₃)','Collect the R₂ terms and factorise'],
steps:['(R_T - R_1)(R_2 + R_3) = R_2 R_3','R_3(R_T - R_1) = R_2(R_3 - R_T + R_1)','R_2 = \\dfrac{R_3(R_T - R_1)}{R_3 - R_T + R_1}']},

{stage:4,formula:'\\dfrac{1}{C_T} = \\dfrac{1}{C_1} + \\dfrac{1}{C_2}',target:'C_2',ctx:'Capacitors in series',correct:'C_2 = \\dfrac{C_T C_1}{C_1 - C_T}',d:['C_2 = \\dfrac{C_T C_1}{C_T - C_1}','C_2 = C_1 - C_T','C_2 = \\dfrac{C_1 - C_T}{C_T C_1}'],
hints:['Subtract 1/C₁ and write as one fraction','Turn both sides upside down'],
steps:['\\dfrac{1}{C_2} = \\dfrac{C_1 - C_T}{C_T C_1}','C_2 = \\dfrac{C_T C_1}{C_1 - C_T}']},

{stage:4,formula:'V_o = \\dfrac{V_i R_2}{R_1 + R_2}',target:'R_1',ctx:'Potential divider',correct:'R_1 = \\dfrac{R_2(V_i - V_o)}{V_o}',d:['R_1 = \\dfrac{R_2(V_o - V_i)}{V_o}','R_1 = \\dfrac{R_2 V_i}{V_o}','R_1 = \\dfrac{R_2(V_i - V_o)}{V_i}'],
hints:['Multiply both sides by (R₁ + R₂)','Make R₁ the subject'],
steps:['V_o(R_1 + R_2) = V_i R_2','V_o R_1 = R_2(V_i - V_o)','R_1 = \\dfrac{R_2(V_i - V_o)}{V_o}']},

{stage:4,formula:'V_o = \\dfrac{V_i R_2}{R_1 + R_2}',target:'R_2',ctx:'Potential divider',correct:'R_2 = \\dfrac{R_1 V_o}{V_i - V_o}',d:['R_2 = \\dfrac{R_1 V_o}{V_o - V_i}','R_2 = \\dfrac{R_1 V_i}{V_i - V_o}','R_2 = \\dfrac{R_1 V_o}{V_i}'],
hints:['Multiply both sides by (R₁ + R₂) and expand','Collect the R₂ terms and factorise'],
steps:['V_o R_1 + V_o R_2 = V_i R_2','V_o R_1 = R_2(V_i - V_o)','R_2 = \\dfrac{R_1 V_o}{V_i - V_o}']},

{stage:4,formula:'\\eta = 1 - \\dfrac{T_C}{T_H}',target:'T_H',ctx:'Carnot efficiency',correct:'T_H = \\dfrac{T_C}{1 - \\eta}',d:['T_H = \\dfrac{T_C}{\\eta - 1}','T_H = T_C(1 - \\eta)','T_H = \\dfrac{1 - \\eta}{T_C}'],
hints:['Rearrange so \\(\\dfrac{T_C}{T_H}\\) is on its own','Multiply by \\(T_H\\), then divide by \\((1 - \\eta)\\)'],
steps:['\\dfrac{T_C}{T_H} = 1 - \\eta','T_H = \\dfrac{T_C}{1 - \\eta}']},

{stage:4,formula:'G = \\dfrac{A}{1 + A\\beta}',target:'A',ctx:'Closed-loop gain with feedback',correct:'A = \\dfrac{G}{1 - G\\beta}',d:['A = \\dfrac{G}{1 + G\\beta}','A = \\dfrac{G}{1 + \\beta}','A = \\dfrac{G}{\\beta - 1}'],
hints:['Multiply both sides by (1 + Aβ) and expand','Collect the A terms and factorise'],
steps:['G + GA\\beta = A','G = A(1 - G\\beta)','A = \\dfrac{G}{1 - G\\beta}']},
