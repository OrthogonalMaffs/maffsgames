LANE: cloud (Claude Code on the web). SEND: now. I DROPPED MY ICE CREAM merged as #820 (5e1c236), and this goes ahead of DAILY-ANSWERS (Jon, 18 Nov 2026, 08:49). If the Ice Cream session is still watching main's runs, send this once it has reported main's check-site and phone-fit-full run IDs.
RECOMMENDED: Opus 5.5, high effort. A new five-stage game with two looks, a link-fragment greeting, a 226-item bank and a verifier.

TASK: SUMS-IN-DISGUISE. Build a new game, "Sums in Disguise" (slug sums-in-disguise): adding within 100 by using a known fact (4 + 2 = 6, so 44 + 2 = 46, 40 + 20 = 60, and 7 + 5 = 12, so 27 + 5 = 32). It has five stages and two looks on one page: a grown-up look by default, and a kid look opened by the link fragment. Merge it UNLISTED, so Jon can play both looks first.

ROOT CAUSE: The site has no addition game. The roster has no row for addition, number bonds or mental addition, and /essentials/ links 39 games, none of them on the fact fluency the rest depends on. Jon, 18 Nov 2026: a Year 11 he tutors still counts on her fingers for simple addition, and "there are plenty of students who are sitting or resitting gcse who need this practice". His daughter's primary class is working on the same skill now.

CLASS CHECK: A new build, not a fix. It reuses the shared layers and duplicates none of them:
- MaffsLevel.resolve, options.js (MaffsOptions.shuffle), MaffsLock, MaffsNext, the fold components, stage-exit.js, teacher-invite.js, analytics.js (mfg), MaffsLeaderboard and MaffsScoreHistory, and the theme.
- The two looks are ONE page with ONE bank, ONE marking path and ONE verifier. Only the CSS look and the LINES text differ. Two pages would put the maths in two places, where a fix to one can miss the other.
- It ships checked (canon SR-30): its verifier runs in CI in this PR, it is in every shared check's MIGRATED and registration lists, and it has a findings file docs/audits/findings/sums-in-disguise.yml.
- Patterns to follow: games/i-dropped-my-ice-cream/index.html (a staged game merged unlisted: stages as boards, MaffsLock, MaffsNext, stage-exit, question_id) and games/like-terms-collector/index.html (a year6 light-theme game).
- Phone-fit lesson from #811: every answer button gets its own click handler where it is built. Never delegate answer clicks to a parent (check-site's option probe only sees buttons with their own handler).

JON'S DECISIONS, 18 Nov 2026 (record verbatim in the PR body):
- 08:12: "they're currently working on using known facts to help with addition to 100, so 4+2=6 so 44+2=46. It needs to be silly and fun (Thats what we do)."
- 08:22: the idea "disguise please" (each big sum is a little sum in disguise).
- 08:25: the class's own version by link, "they can have their own personalised version of the game, which is not indexed".
- 08:38: "this could still be an essentials skill, I have a year 11 tutee who still does counting on her fingers for simple addition, so this is not just a primary skill, there are plenty of students who are sitting or resitting gcse who need this practice"
- 08:39: "we can make it a bit more grown up on the main site, this game for her class can be the kid friendly version"
- 08:40: crossing a ten, "lets build it in there" (Stage 5).
- 08:46: "if we're having the disguises, they can be the ones giving the feedback, "aha, I tricked you", then the learning. we should have a big "67" pop up on the screen anytime they both appear in a question."
- 08:49: the 67 trigger is "a 6 and a 7 anywhere, popping after she answers" ("middle row"); "if you come up with some placeholders it will help me mould them"; "before daily answers please".

EXACT CHANGE:
0. First commit: the close-out of #820 I-DROPPED-MY-ICE-CREAM per AGENTS.md's close-out rule: merge commit 5e1c236; main's check-site and phone-fit-full run IDs and conclusions, read back from the API in this session; its contract to docs/history/contracts/. Then save this contract verbatim as docs/handover/contracts/2026-11-18-sums-in-disguise.md.

1. games/sums-in-disguise/index.html: one page on the shared assets.
   - Light theme (canon §7.5.1: the lowest tier served is Starter).
   - Title "Sums in Disguise". Under it, the title line from LINES.
   - Level: MaffsLevel.resolve({slug: 'sums-in-disguise', levels: ['year6'], fallback: 'year6'}). One level, no level picker. Shown to students as "Starter" (SR-11); no year-group or key-stage wording anywhere a student sees.
   - Calculator: not allowed.
   - The bank as one QUESTIONS array: the 226 items the generator below prints, unchanged and in order.
   - Every user-facing line comes from ONE object, LINES = { grown: {...}, kids: {...} }, near the top of the script, with the placeholders below, verbatim. Jon will rewrite them after playing, so no line may be written anywhere else in the page. A comment above it: "Placeholders by Project Claude, 18 Nov 2026, for Jon to rewrite."

2. Looks and the class greeting (the link fragment).
   - Parse location.hash once, at start, inside try/catch:
     - "#kids" (any letter case) → kid look, no class greeting.
     - "#kids/<name>" → kid look and a class greeting. The name: decodeURIComponent, trimmed. Letters, spaces, hyphens and apostrophes only, 1 to 20 characters; anything else → kid look, no greeting. If it already ends with "class" (any case), "Class" is not added again. "#kids/Maple" → "Welcome, Maple Class!"; "#kids/Maple%20Class" → the same.
     - Anything else, or no hash → grown-up look, no greeting.
   - Shown with textContent only, never innerHTML.
   - The look is a class on <body> (look-kids). The kid look is brighter and rounder, with bigger disguises. It has the same layout, items, marking and boards as the grown-up look.
   - The fragment, the look and the name are never sent anywhere and never stored: not in any mfg() parameter, not in a board, not in localStorage or sessionStorage. Google's gtag documentation says page_location's default value excludes the fragment. analytics.js reads location.hostname only (lines 37 and 92), so no new collection arises. If anything in this build would send the fragment, STOP.
   - Any URL rewrite the page makes (for example MaffsLevel) keeps location.hash.

3. Stages, keyed stage-1 to stage-5, chosen on the start screen. A run is 10 items drawn from that stage's items, with no repeat within a run (MaffsOptions.shuffle). The score is the number of big answers right, out of 10.
   Each stage has its own disguise, an inline SVG (no emoji). The disguise sits on the big sum. When it comes off, the tens leave with it: the disguise carries a tag showing p − a (ones and cross items), or the zeros for tens items, and the sum underneath changes to the little sum.
   - Stage 1, "The Moustache" (type ones, no crossing):
     1. Show the big sum, e.g. 44 + 2, in KaTeX, wearing the moustache.
     2. She taps the moustache (a button). It comes off and 4 + 2 shows.
     3. She answers the little sum on tiles 0 to 10.
     4. The moustache goes back on, and she answers the big sum: four options, the answer and its three decoys.
   - Stage 2, "The Glasses" (type tens): the same flow, with 40 + 20 → 4 + 2.
   - Stage 3, "The Wig" (mixed): the wig stays on and she answers the big sum straight away (four options). A "Peek" button lifts the wig to show the little sum, then puts it back. Peeking costs nothing. The end screen shows the score and "Done without peeking: n of 10".
   - Stage 4, "The Duck" (spot the disguise): show the little fact, e.g. 2 + 4 = 6, with the duck. Ask "Which one is 2 + 4 in disguise?" Three options in KaTeX: answer_sum and the two decoy sums. Each option's dataset.val is its sum written "p+q", e.g. "20+40".
   - Stage 5, "The Top Hat" (type cross: crossing a ten): the Stage 1 flow, with little-sum tiles 0 to 20.
   - A wrong little-sum tile: show the right one and carry on to the big sum (no score either way).
   - Every big-sum option's dataset.val is its number. Marking is by dataset.val only, never by rendered HTML.

4. Feedback: the disguise speaks, then the learning.
   - Right: a line from LINES.<look>.right (picked at random), then the learning line.
   - Wrong (Stages 1, 2, 3 and 5): the "aha" line for the decoy picked, keyed by that decoy's name in the item (tens, concat, off_by_one, forgot_disguise, extra_zero, ones, forgot_ten); concat on a cross item uses aha.concat_cross. Then the learning line, and MaffsNext.wrong as in Ice Cream.
   - Wrong in Stage 4: LINES.<look>.duck_wrong, then the learning line for the right option.
   - The learning line is built by the code from the item, never typed into LINES:
     - ones: "4 + 2 = 6, so 44 + 2 = 46."
     - tens: "4 + 2 = 6, so 40 + 20 = 60."
     - cross: "7 + 5 = 12, so 27 + 5 = 20 + 12 = 32."
     - Stage 4: "2 + 4 = 6, so 20 + 40 = 60 is 2 + 4 in disguise."
     Rendered in KaTeX. The numbers come from the item's little, big (or answer_sum) and answer.
   - When the disguise comes off (step 2 of Stages 1, 2 and 5, and Stage 3's Peek), show LINES.<look>.reveal[<stage>] beside it.
   - End of a run: LINES.<look>.end, the score, and (Stage 3) the no-peek count.

5. The 67.
   - After a big answer is marked (right or wrong), and never before, check the item. Write the two numbers of its big sum (Stage 4: answer_sum) and its answer as digits. If they contain both a 6 and a 7, show a big "67" over the play area for about 1.5 s; a tap closes it sooner. It never blocks marking, the answer lock or Next, and it never changes the score.
   - prefers-reduced-motion: show it without animation.
   - With this bank it fires on 6 of 50 Stage 1 items, 2 of 36 Stage 2, 7 of 50 Stage 3, 4 of 40 Stage 4 and 14 of 50 Stage 5. The verifier checks these counts.

6. Integration, each as #820 did it:
   - Leaderboard: one board per stage, keys stage-1 to stage-5. Their labels already exist in firebase-leaderboard.js, so that file is not changed. Submit only at a run's end, through MaffsLock.finishOnce. MaffsScoreHistory as in Ice Cream.
   - Analytics: game_started, question_answered (with question_id = the item's id) and game_completed, as in Ice Cream, with level 'year6' and mode the stage key. Nothing else.
   - stage-exit.js, teacher-invite.js and fold, as in Ice Cream.
   - schools/assets/launch-dates.json: one line, "sums-in-disguise": "2026-11-18" (additive; as #820).
   - .claude/rules/game-roster.md: a row under Unlisted, with levels Year 6, topic Number, calculator not allowed, "5 stages, 226 questions; two looks (#kids)". Plus its note.
   - data/games.json entry (unlisted), then apply-meta.py and check-meta.py. Search phrase "Adding with known facts". Keywords include "number bonds", "adding within 100", "mental addition", "essentials".
   - The findings file. The MIGRATED and registration lists #820 touched (check-answer-lock.py, check-levels.py, check-theme.py, check-teacher-invite.py, check-start-mount.py, audit-register.py, verify-stage-exit.py).
   - check-leaderboard-coverage.js NOT_ON_HUB: "new, unlisted until Jon has played and approved it; hub row added at listing".
   - No noindex: new unlisted games carry none (as #810 and #820), and the kid look is a fragment, which search engines don't index separately.
   - /updates/: no line while unlisted.
   - docs/todo.md, two short rows:
     - SUMS-IN-DISGUISE-LIST: Jon plays all five stages in both looks (/games/sums-in-disguise/ and /games/sums-in-disguise/#kids/Maple), rewrites LINES, then rules on listing with an /essentials/ card.
     - NUMBER-BONDS: a number bonds to 10 and 20 fluency game, "needs building soon" (Jon, 18 Nov 2026); spec from Project Claude.
     todo.md is 152,745 bytes against TODO_LIMIT 153,600. If the rows would cross the cap, move closed rows to docs/history/todo-done.md verbatim, oldest first, until they fit. Never move an open row.
   - docs/handover/cloud.md.

7. scripts/verify-sums-in-disguise.py, in CI (its # ci-shards header), with --selftest.
   - The page's bank, written one item per line as json.dumps(item, separators=(",", ":")) with a newline after each, has SHA-256 19e415561cb6baecdaf01d2bde6f23f367a6aff2802d33b8d152dce6561068a8 (the generator's output).
   - Counts: stage 1: 50, 2: 36, 3: 50 (25 ones, 25 tens), 4: 40 (25 ones, 15 tens), 5: 50. Ids unique.
   - Recompute everything independently from little (and t = the big sum's tens):
     - little_answer = a + b;
     - answer = the big sum's total;
     - ones: the big sum is (10t + a) + b with a + b ≤ 9 (no crossing);
     - tens: the big sum is 10a + 10b with a + b ≤ 9;
     - cross: the big sum is (10t + a) + b with a + b ≥ 10 and the total ≤ 99.
   - Decoys by rule:
     - tens = p + 10q;
     - concat = the digits of p − a, then of a + b (406);
     - concat on cross items = the digits of t, then of a + b (212 for 27 + 5);
     - off_by_one = answer ± 1 (± 10 where the rule's fallback applied);
     - forgot_disguise = a + b;
     - extra_zero = 100(a + b);
     - ones = p + b;
     - forgot_ten = answer − 10.
     The three decoys are distinct, never the answer, and never negative.
   - Stage 4: answer_sum is the little fact in its disguise. Each decoy sum is a different fact (its little fact is not the same pair {a, b} in either order), stays in range with no crossing, and the three options are distinct.
   - Coverage:
     - Stage 1 uses all 36 (a, b) pairs, Stage 2 all 36 and Stage 5 all 45.
     - No big sum repeats within a stage.
     - No ones big sum is in more than one of Stages 1, 3 and 4.
   - The 67 counts in step 5.
   - In play, in both looks:
     - each tile, option and Stage 4 sum marks by dataset.val, its key and only its key;
     - each decoy shows its own aha line, then the learning line with the item's numbers;
     - the 67 shows after marking on exactly the firing items;
     - one board submission per run, on stage-N;
     - the greeting reads "Welcome, Maple Class!" for #kids/Maple, nothing for #kids/<script>, and the grown-up look for no hash;
     - no mfg() payload contains "kids", "Maple" or "#".
   - Plants that must fail:
     - an answer 1 out;
     - a decoy equal to the answer;
     - a Stage 1 item that crosses a ten;
     - a Stage 5 item that doesn't;
     - a Stage 4 decoy that is the same fact swapped (42 + 4 for 44 + 2);
     - an option marked by its rendered text;
     - the 67 shown before marking;
     - the class name written with innerHTML;
     - "Maple" in an mfg() payload.

8. Merge with scripts/merge-pr.py when the Gate is green, and phone-fit-full is green when dispatched on the branch. That is the only merge route.

THE PLACEHOLDER LINES (verbatim, into LINES; Jon will rewrite them):
grown:
  title: "Every big sum is a small sum in a cheap disguise. You have seen through worse."
  welcome: "Some sums are hiding. Badly."
  reveal: { stage-1: "Rumbled. It was the little sum all along.", stage-2: "I was wearing these ironically.", stage-3: "This is my real hair.", stage-4: "The duck was a distraction.", stage-5: "There was a ten in the hat. There is always a ten in the hat." }
  right: ["Rumbled.", "Disguise: ruined.", "Seen straight through.", "The sum is embarrassed. Good.", "Correct. The moustache is in tears.", "Exposed."]
  aha: { tens: "Aha. I tricked you. You gave the tens a number that wasn't theirs.", concat: "Aha. You wrote the disguise down, then the sum. Just the answer, please.", off_by_one: "Aha. Off by one. Count less, know more.", forgot_disguise: "Aha. You took the disguise off and forgot to put it back on.", extra_zero: "Aha. One zero too many. Zeros are not free.", ones: "Aha. Those were tens in a ones costume.", forgot_ten: "Aha. The ten in the little sum escaped. Tens must be counted.", concat_cross: "Aha. You wrote that ten as a digit and not as a ten." }
  duck_wrong: "That is a different duck. Similar hat."
  duck_right: "The duck concedes."
  end: "Every disguise removed. The fancy dress shop has filed for bankruptcy."
kids:
  title: "Every big sum is just a little sum in a silly disguise. Unmask them all!"
  welcome: "Welcome, sum detectives!"
  welcome_class: "Welcome, {name} Class!"
  reveal: { stage-1: "Noooo! My magnificent moustache!", stage-2: "Hey! I can't see a thing without those!", stage-3: "My hair! Give it back!", stage-4: "Quack. That's duck for 'you found me'.", stage-5: "Hey! There was a ten hiding in my hat!" }
  right: ["Unmasked!", "Caught you!", "Disguise destroyed!", "You saw right through it!", "Ha! Gotcha!", "Nobody fools you!"]
  aha: { tens: "Aha! I tricked you into giving my number to the tens!", concat: "Aha! I tricked you into writing it the long way!", off_by_one: "Aha! Missed me by one! So close!", forgot_disguise: "Aha! You forgot I was in disguise!", extra_zero: "Aha! I sneaked in an extra zero!", ones: "Aha! You thought my tens were ones!", forgot_ten: "Aha! I hid a ten in my hat and you missed it!", concat_cross: "Aha! You wrote my hidden ten the long way!" }
  duck_wrong: "Quack! That's my cousin. Different sum!"
  duck_right: "Quack! You found me!"
  end: "All the sums are unmasked. The disguise shop has closed down!"
Shared, both looks: the pop-up text is "67" alone; the Stage 3 button reads "Peek".

THE BANK: 226 items, made by the generator below. Project Claude ran it (Python 3.13) and checked its output with a separate script: 0 errors. Before building:
1. Save the generator as a scratch file, outside the repo.
2. Run it. It writes bank.jsonl and prints "50 36 50 40 50 226".
3. Check that bank.jsonl's SHA-256 is 19e415561cb6baecdaf01d2bde6f23f367a6aff2802d33b8d152dce6561068a8. If it differs, STOP and report both hashes.
4. Recompute every item yourself by the rules in step 7.
5. Embed the 226 items in the page, unchanged and in order. Don't commit the generator; this contract holds it.
Fields:
- id;
- stage;
- type (ones, tens or cross);
- big: the big sum [p, q] (stages 1, 2, 3, 5);
- little: [a, b];
- little_answer;
- answer;
- decoys: named numbers (stages 1, 2, 3, 5) or a list of {kind, sum} (stage 4);
- answer_sum: stage 4 only.
Examples:
{"id":"s1_017","stage":1,"type":"ones","big":[42,4],"little":[2,4],"little_answer":6,"answer":46,"decoys":{"tens":82,"concat":406,"off_by_one":47}}
{"id":"s2_017","stage":2,"type":"tens","big":[20,40],"little":[2,4],"little_answer":6,"answer":60,"decoys":{"forgot_disguise":6,"extra_zero":600,"ones":24}}
{"id":"s4_002","stage":4,"type":"tens","little":[2,4],"little_answer":6,"answer_sum":[20,40],"answer":60,"decoys":[{"kind":"changed_first","sum":[10,40]},{"kind":"changed_second","sum":[20,30]}]}
{"id":"s5_001","stage":5,"type":"cross","big":[58,3],"little":[8,3],"little_answer":11,"answer":61,"decoys":{"forgot_ten":51,"concat":511,"off_by_one":62}}

THE GENERATOR (verbatim):
import random, json
R = random.Random(20261118)

def off1(ans, k):
    return ans+1 if k % 2 == 0 else ans-1

def decoys_ones(t, a, b, k):
    ans = 10*t + a + b; c = a + b
    d = {"tens": 10*(t+b) + a, "concat": int(str(10*t) + str(c)), "off_by_one": off1(ans, k)}
    return ans, d

def decoys_tens(a, b, k):
    c = a + b; ans = 10*c
    d = {"forgot_disguise": c, "extra_zero": 100*c, "ones": 10*a + b}
    return ans, d

def decoys_cross(t, a, b, k):
    c = a + b; ans = 10*t + c
    d = {"forgot_ten": ans - 10, "concat": int(str(t) + str(c)), "off_by_one": off1(ans, k)}
    return ans, d

def fix(ans, d):
    # distinctness, fallback per spec: off by one other way, then off by ten
    vals = []
    out = {}
    for k, v in d.items():
        cands = [v]
        if k == "off_by_one": cands += [ans - (v - ans), ans + 10, ans - 10]
        for cv in cands:
            if cv != ans and cv not in vals and cv >= 0:
                out[k] = cv; vals.append(cv); break
        else:
            raise SystemExit(f"no decoy {k} {ans} {d}")
    return out

ones_pairs = [(a, b) for a in range(1, 9) for b in range(1, 10 - a)]            # 36
tens_pairs = ones_pairs[:]                                                        # 36
cross_pairs = [(a, b) for a in range(1, 10) for b in range(1, 10) if a + b >= 10] # 45

def spread_ts(n, lo, hi):
    ts = []
    while len(ts) < n:
        block = list(range(lo, hi + 1)); R.shuffle(block); ts += block
    return ts[:n]

items = []
used_big = set()

def add(stage, typ, t, a, b, k, sid):
    if typ == "ones":
        big = [10*t + a, b]; little = [a, b]; ans, d = decoys_ones(t, a, b, k)
    elif typ == "tens":
        big = [10*a, 10*b]; little = [a, b]; ans, d = decoys_tens(a, b, k)
    else:
        big = [10*t + a, b]; little = [a, b]; ans, d = decoys_cross(t, a, b, k)
    d = fix(ans, d)
    return {"id": sid, "stage": stage, "type": typ, "big": big, "little": little,
            "little_answer": a + b, "answer": ans, "decoys": d}

# Stage 1: 50 ones items: 36 pairs once + 14 more, t spread 1-9, no duplicate big sum
s1 = []
pairs = ones_pairs[:]; R.shuffle(pairs)
extra = ones_pairs[:]; R.shuffle(extra); pairs += extra[:14]
ts = spread_ts(50, 1, 9)
seen = set()
for i, (a, b) in enumerate(pairs):
    t = ts[i]
    while (t, a, b) in seen: t = t % 9 + 1
    seen.add((t, a, b))
    s1.append(add(1, "ones", t, a, b, i, f"s1_{i+1:03d}"))
# Stage 2: all 36 tens pairs
p2 = tens_pairs[:]; R.shuffle(p2)
s2 = [add(2, "tens", None, a, b, i, f"s2_{i+1:03d}") for i, (a, b) in enumerate(p2)]
# Stage 3: 25 ones (not in stage 1) + 25 tens (from the 36)
s3 = []
pool = [(t, a, b) for t in range(1, 10) for (a, b) in ones_pairs if (t, a, b) not in seen]
R.shuffle(pool); s3o = pool[:25]; seen3 = set(s3o)
p3 = tens_pairs[:]; R.shuffle(p3); s3t = p3[:25]
mix = [("ones", x) for x in s3o] + [("tens", x) for x in s3t]; R.shuffle(mix)
for i, (typ, x) in enumerate(mix):
    if typ == "ones": s3.append(add(3, "ones", x[0], x[1], x[2], i, f"s3_{i+1:03d}"))
    else: s3.append(add(3, "tens", None, x[0], x[1], i, f"s3_{i+1:03d}"))
# Stage 4: 25 ones (new) + 15 tens; 3 options: answer + 2 decoys (a changed, b changed)
s4 = []
pool4 = [(t, a, b) for t in range(1, 10) for (a, b) in ones_pairs if (t, a, b) not in seen and (t, a, b) not in seen3]
R.shuffle(pool4); s4o = pool4[:25]
p4 = tens_pairs[:]; R.shuffle(p4); s4t = p4[:15]
mix4 = [("ones", x) for x in s4o] + [("tens", x) for x in s4t]; R.shuffle(mix4)
def ok(a, b): return 1 <= a <= 9 and 1 <= b <= 9 and a + b <= 9
for i, (typ, x) in enumerate(mix4):
    if typ == "ones": t, a, b = x
    else: t = None; a, b = x
    # decoy A: change a by +1 or -1; decoy B: change b by +1 or -1; neither may be the same fact (multiset)
    def mk(aa, bb):
        if typ == "ones": return [10*t + aa, bb]
        return [10*aa, 10*bb]
    order = [1, -1, 2, -2] if i % 2 == 0 else [-1, 1, -2, 2]
    ca = [("changed_first", (a+dd, b)) for dd in order if ok(a+dd, b) and sorted([a+dd, b]) != sorted([a, b])]
    cb = [("changed_second", (a, b+dd)) for dd in order if ok(a, b+dd) and sorted([a, b+dd]) != sorted([a, b])]
    picks = []
    if ca: picks.append(ca[0])
    if cb: picks.append(cb[0])
    for c in ca[1:] + cb[1:]:
        if len(picks) >= 2: break
        if c[1] not in [p[1] for p in picks]: picks.append(c)
    assert len(picks) == 2, (a, b)
    ans = mk(a, b)
    s4.append({"id": f"s4_{i+1:03d}", "stage": 4, "type": typ, "little": [a, b], "little_answer": a + b,
               "answer_sum": ans, "answer": sum(ans),
               "decoys": [{"kind": k, "sum": mk(*p)} for k, p in picks]})
# Stage 5: 50 crossing: 45 pairs once + 5 more, t 1-8
pairs5 = cross_pairs[:]; R.shuffle(pairs5); e5 = cross_pairs[:]; R.shuffle(e5); pairs5 += e5[:5]
ts5 = spread_ts(50, 1, 8); seen5 = set(); s5 = []
for i, (a, b) in enumerate(pairs5):
    t = ts5[i]
    while (t, a, b) in seen5: t = t % 8 + 1
    seen5.add((t, a, b))
    s5.append(add(5, "cross", t, a, b, i, f"s5_{i+1:03d}"))
bank = s1 + s2 + s3 + s4 + s5
with open("bank.jsonl", "w") as f:
    for it in bank: f.write(json.dumps(it, separators=(",", ":")) + "\n")
print(len(s1), len(s2), len(s3), len(s4), len(s5), len(bank))

DO NOT TOUCH:
- Any other game.
- schools/assets/, except the one additive line in launch-dates.json above.
- canon (home lane), escape-rooms/, tools/pack-generator/.
- The bank's numbers, types and ids. If you think an item is wrong, STOP; do not "fix" it.
- The placeholder lines: verbatim, Jon rewrites them later.
- No listing, sitemap entry, portal card, /essentials/ card or hub row while unlisted.
- No draft PR.

SUCCESS CONDITION:
- /games/sums-in-disguise/ plays all five stages in the grown-up look.
- /games/sums-in-disguise/#kids/Maple plays them in the kid look, greeting "Welcome, Maple Class!".
- Every answer is marked by dataset.val. Each decoy shows its own aha line and then the learning line.
- The 67 shows after marking, on exactly the items step 5 counts.
- verify-sums-in-disguise.py passes with every plant failing.
- check-site, phone-fit (dispatched on the branch), answer-lock, check-levels, check-calculator, check-answer-inputs, check-theme, check-meta and leaderboard coverage all pass.
- Unlisted.
- Merged by merge-pr.py, with its last line, the merge commit and main's check-site and phone-fit-full run IDs reported.
- Handover and todo committed.

STOP IF:
- Any bank value disagrees with your independent recomputation (report the id and both values).
- Anything in the build would send the fragment, the look or the class name to analytics, a board or storage.
- A shared check needs an exemption for this game, or the light theme check fails for the kid look.
- Tiles 0 to 20 or the disguises cannot fit phone-fit at 360 px.
- todo.md's two rows cannot fit under TODO_LIMIT without moving an open row.
- merge-pr.py refuses for a reason other than a transient 5xx it already retries.

AMENDMENT 1 to SUMS-IN-DISGUISE (Jon, 18 Nov 2026, 09:19: "all 4 please"). Record it verbatim in the saved contract (docs/handover/contracts/2026-11-18-sums-in-disguise.md) and in the PR body, and build it into this same PR. Where it differs from the contract, this wins.

WHY (Jon, 09:17): "the students in the class are not the best at reading (they're getting better), we need to be careful with long instructions. It will be introduced by the teacher, so she will be able to talk them through when they first meet it, but they may want to play it at home." The same applies to weak readers among resit students, so changes 1, 2 and 4 apply to both looks.

1. MATHS INSTEAD OF WORDS (both looks).
   - The big-sum question is the sum itself, in KaTeX: "64 + 3 = ?". It never says "So what is 64 + 3?". The same in Stages 1, 2, 3 and 5.
   - The learning line (contract step 4) is no longer a sentence. It is the sums stacked in KaTeX, aligned on the first "=", with the tens digit(s) of the big sum and of its answer in bold and the accent colour:
       ones:   4 + 3 = 7
              64 + 3 = 67      (the 6 of 64 and the 6 of 67 highlighted)
       tens:   4 + 2 = 6
              40 + 20 = 60     (the 0s highlighted)
       cross:  7 + 5 = 12
              27 + 5 = 20 + 12 = 32   (the 2 of 27, the 20 and the 3 of 32 highlighted)
       Stage 4: 2 + 6 = 8
               32 + 6 = 38
     Every number comes from the item (little, big or answer_sum, answer), never typed.
   - The Stage 4 question comes from LINES: grown.find "Find {little} in disguise." and kids.find "Find {little}!", where {little} renders as the KaTeX sum, e.g. "2 + 6".

2. ONE FEEDBACK LINE AT A TIME (both looks).
   - Feedback shows at most ONE string from LINES, then the stacked sums. Never two LINES strings together.
   - Stage 4 wrong: duck_wrong only. Stage 4 right: duck_right only. The reveal lines are shown only when a disguise comes off (step 2 of Stages 1, 2 and 5, and Stage 3's Peek), never with answer feedback.
   - Kid look: every LINES.kids string is 6 words or fewer, not counting {name} or {little}. The new kid set below meets this. The grown set is unchanged.

3. SHORTER INSTRUCTIONS AND A POINTING HAND (kid look).
   - Button labels come from LINES: kids.take_off "Take it off!", grown.take_off "Take off the disguise". Peek stays "Peek" in both.
   - The disguise itself is also tappable (it does what the button does), as a real button with its own click handler and an aria-label.
   - Kid look: on the FIRST question of every run, a pointing hand (inline SVG, no emoji) pulses on the disguise until it is tapped. Stage 4 has no take-off, so the hand points at the options instead. With prefers-reduced-motion, the hand is shown still.

4. READ ALOUD (both looks).
   - A speaker button (inline SVG icon, aria-label "Read aloud") on the play screen, with its own click handler. It speaks only when tapped, never by itself.
   - It uses window.speechSynthesis with a voice whose localService is true, so the speech is made on the device. If the browser has no speechSynthesis or no local voice (check after voiceschanged), the button is not shown. Never use a voice whose localService is false.
   - What it reads is built from the item, with sums spoken in words ("64 plus 3 equals what?"):
     - before answering: the question;
     - after answering: the one feedback line, then the working ("4 plus 3 is 7, so 64 plus 3 is 67");
     - Stage 4: "Find 2 plus 6".
     It never reads the class greeting.
   - speechSynthesis.cancel() on Next, on leaving the play screen and on stage exit.
   - Nothing about it is sent or stored: no mfg() event or parameter, no storage. No new collection.
   - It fits phone-fit at 360 px.

THE NEW KID PLACEHOLDER SET (replaces the contract's kids: block, verbatim; Jon will still rewrite):
kids:
  title: "Every sum is in disguise!"
  welcome: "Welcome, sum detectives!"
  welcome_class: "Welcome, {name} Class!"
  take_off: "Take it off!"
  find: "Find {little}!"
  reveal: { stage-1: "Noooo! My moustache!", stage-2: "Hey! My glasses!", stage-3: "My hair! Give it back!", stage-4: "Quack! You found me!", stage-5: "Hey! A ten in my hat!" }
  right: ["Unmasked!", "Caught you!", "Gotcha!", "You saw through it!", "Disguise destroyed!", "Nobody fools you!"]
  aha: { tens: "Aha! I tricked your tens!", concat: "Aha! Too many digits!", off_by_one: "Aha! Missed by one!", forgot_disguise: "Aha! You forgot my disguise!", extra_zero: "Aha! One zero too many!", ones: "Aha! Those were tens!", forgot_ten: "Aha! You missed my ten!", concat_cross: "Aha! Too many digits!" }
  duck_wrong: "Quack! Wrong duck!"
  duck_right: "Quack! You found me!"
  end: "All sums unmasked!"
ADD to the grown: block: take_off: "Take off the disguise", find: "Find {little} in disguise."

VERIFIER (add to scripts/verify-sums-in-disguise.py):
- In play, in both looks:
  - the question shows the sum and "= ?", with no other words;
  - the stacked working's numbers match the item;
  - feedback never holds two LINES strings;
  - every LINES.kids string is 6 words or fewer;
  - the hand shows on question 1 of a kid run only;
  - the disguise and the button both take it off.
- Read aloud, against a mocked speechSynthesis:
  - the button is hidden when there is no local voice;
  - only a localService voice is ever passed to speak();
  - nothing is spoken before a tap;
  - the spoken text is built from the item's numbers;
  - cancel() is called on Next;
  - no mfg() payload or storage write mentions it.
- New plants that must fail:
  - feedback showing two LINES strings;
  - a kid line of 7 words;
  - a non-local voice used;
  - speech on load without a tap;
  - a working number typed rather than taken from the item.

STOP IF (added): any part of read-aloud would send text off the device, or cannot be tested without a real voice even with a mocked speechSynthesis.
