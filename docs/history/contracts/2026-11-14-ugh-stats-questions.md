UGH-STATS-QUESTIONS (Project Claude, Sat 14 Nov 2026 17:10; Jon's rulings 14 Nov 14:36–16:49)
(Saved copy: the one place name in Case 4 is generalised to "the south-west of England" and its CSV column to daylight_hours, Jon, 14 Nov 2026, at the pre-push personal-details scan. Nothing else differs from the contract as given.)
Recommended: Opus, effort high: student-facing maths on a live page, every answer computed from the numbers shown, and one change to a listed game's bank.
LANE: home. TIER: Medium (merge on green; Project Claude reviews after merge; Jon reads the live pages after). START: now. One PR. Branch from current origin/main (22e1e16 or newer).
PARALLEL LANE: cloud is running ANSWER-BOX-CHECK in tools/pack-generator/. Touch nothing there; if docs/todo.md conflicts, merge main in and keep both sides.
MERGE: merge-pr.py on a green Gate.

JON'S RULINGS (verbatim in the PR body):
- 14 Nov 14:54–14:58: questions inside each case, replacing each case's static "Your turn" list (the CSV button stays); answers logged anonymously ("new collection approved by Jon"); typed numbers plus multiple choice, an explanation after every answer, no score; launch dates from git, "option a makes more sense, it can be a one off file, all new games will have a githistory, anything showing the 2oct can be checked against the "old" list".
- 14 Nov 14:36: the foreword, "Yes please." (text in Appendix A).
- 14 Nov 15:11: Case 4 "a) is a nice point" (flu as the headline, daylight as the follow-up). 15:16: "Agree with a class in X country, case 4 multiple choice is fine." 16:44: "yes ok" to the SR-14 rewording of Case 4 and to the Correlation or Coincidence item.
- 14 Nov 16:42: "lets build as is for now": no width change.
- 14 Nov 16:49: "fine" to: a separate event name, stats_question_answered; the Decide lines and card texts below; Case 4 Q1 option C reworded for SR-14.

TASK: Add the interactive questions to Cases 1 and 2, add Case 3 (outliers) and Case 4 (correlation), add the foreword to the landing page, commit a launch-dates file, and add one MaffsGames item to Correlation or Coincidence.

ROOT CAUSE: The two live cases end in a static "Your turn" list a student can't answer on the page, the section has no case on outliers or correlation, and the per-day questions need each game's launch date, which nothing in the repo records (this repo's history starts 2 Oct 2026; earlier history is in OrthogonalMaffs/maffsgames-archive).

CLASS CHECK: The question widget is used by four pages, so it is built once in schools/assets/ugh-stats.js (with its CSS in ugh-stats/ugh-stats.css) and each page supplies only its questions as data; no per-page copies of the widget. Launch dates are one committed file read by every page that needs them, kept complete by a check, not per-page constants. The answers are logged under their own event name so that nothing which counts game answers (question_answered) has to filter them out. The Correlation or Coincidence item is local: one entry in that game's existing bank, in its existing format.

EXACT CHANGE:
1. Launch dates. A one-off script (scripts/build-launch-dates.py, kept for audit) writes schools/assets/launch-dates.json: {"<slug>": "YYYY-MM-DD", ...} for every games/<slug>/ and escape-rooms/<slug>/ directory with an index.html. Date = the UK date of the commit that first added that index.html in this repo; where that is 2026-10-02 (the fresh start), use the first commit adding the same path in OrthogonalMaffs/maffsgames-archive (clone it read-only outside the repo); found in neither, keep 2026-10-02 and list it in the PR. From now on a new game adds its own line at launch: scripts/check-ugh-stats.py fails if a game or room directory has no entry or an entry is not a valid date. AGENTS.md is not changed; the check is the rule.
2. The widget, in ugh-stats.js. Each question: typed (whole number, keypad-friendly input, "to the nearest whole number" in the stem, the exact rounded value accepted, up to 3 tries, then the working) or multiple choice (four options, shuffled once per page load, one try, then the explanation for the chosen option and, if wrong, the right one). "Next" after each; no score. Questions render in place of each page's "Your turn" list, in the same box; the CSV button stays where it is. Every number in a live question comes from the JSON the page already loads (answer-counts.json, ugh-stats.json) or launch-dates.json, and the answer is computed in the page from the same numbers it shows; a question whose numbers include "<10", are missing, or fail their shape check is skipped (the next one shows). KaTeX is not needed; plain text with the true minus sign (−) and × ÷.
3. Logging: each answer sends one event, window.mfg('stats_question_answered', {game_slug: "ugh-stats", level: "case1" | "case2" | "case3" | "case4", question_index: 1–4, correct: right first time (multiple choice: the one choice), attempts}). Never question_answered. docs/apps-script-endpoint.js doPost stores any event name (it rejects only a missing event), so no Apps Script change; confirm that, and that analytics.js passes the event to both GA4 and the Sheet unchanged. Privacy page (privacy/index.html, the list under "we log anonymous gameplay events"): add one item, "Answers to the questions on our Ugh, stats pages, logged the same way." Nothing else about collection changes.
4. Case 1 (ugh-stats/half-our-games/) and Case 2 (ugh-stats/whos-playing/): replace the "Your turn" list with Appendix B's questions, verbatim.
5. Case 3: new page ugh-stats/one-class/ ("One class, 3,667 answers"), Appendix C, laid out like the existing cases (Ask, Collect, Picture it, Decide; the "can't tell us" box; the questions box with a CSV button that downloads Appendix C's CSV, committed as ugh-stats/one-class/data.csv). Chart: daily answers 15 Oct – 11 Nov as bars (the existing chart helper in ugh-stats.js), the two class days in the accent colour, caption as given. Frozen data: no live JSON on this page.
6. Case 4: new page ugh-stats/flu-and-answers/ ("Flu tests and maths answers"), Appendix D, same layout; CSV ugh-stats/flu-and-answers/data.csv (Appendix D's). Chart: scatter of flu positivity (x) against weekly answers (y), nine points; the three weeks with a class day as hollow points, a key saying so. If ugh-stats.js has no scatter helper, add one there (a function of the shared module, not page code). Frozen data.
7. Landing page ugh-stats/index.html: the foreword (Appendix A) after the h1 "Ugh, stats." and before the four-step strip, as a short section with its heading and Jon's first-name sign-off; two new cards after the existing two (Appendix E's text), in the same .cards grid. "More coming soon." stays.
8. Correlation or Coincidence (games/correlation-or-coincidence/index.html): append to the "Something else causes both" group, after B28, Appendix F's item verbatim. Run the game's verifiers and the answer-lock and content-safety checks; update any count a check holds for this bank (84 to 85) and say where.
9. sitemap.xml: the two new case pages, lastmod the merge date, monthly, 0.6. /updates/: "<strong>Ugh, stats</strong>: questions to try in every case, and two new cases, on outliers and on correlation." scripts/check-ugh-stats.py: covers the two new pages (they load, every question renders, every stated answer is the one computed from the shown numbers, the CSV matches the table on the page, Case 4's r values computed from its CSV match the page), the launch-dates rule, the widget (a typed answer accepted only when exact; a skipped question when a number is "<10"), and that no ugh-stats page sends question_answered. Selftest plants for each. home.md entry.
DO NOT TOUCH: ugh-stats.css widths (Jon: as is); the existing cases' text other than the "Your turn" box; answer-counts.json, ugh-stats.json and the workflow that writes them; Apps Script code (docs/apps-script-endpoint.js read only) and its deployments; every other game; tools/pack-generator/ (cloud lane); canon, AGENTS.md. No new external runtime.
SUCCESS CONDITION: Cases 1 and 2 show their four questions each with live numbers, and every answer matches the numbers shown; Cases 3 and 4 live with their charts, questions and CSVs; the foreword and two new cards on the landing page; launch-dates.json complete and checked; one stats_question_answered event per answer, with the privacy line; Correlation or Coincidence has B29 and passes its checks; check-ugh-stats.py and its plants pass; every page passes the site's phone-fit and theme checks; Gate green; merged; main's check-site and phone-fit-full on the merge commit green and reported; home.md updated.
STOP IF: any figure in Appendices C or D disagrees with its CSV or its arithmetic; a live question's computed answer would differ from the working it shows; the archive cannot be read for a game showing 2026-10-02 (list them and ask); the endpoint or analytics.js would need a code change for stats_question_answered; any SR-14 hit in the new text (scripts/check-content-safety.py or your reading); the widget would need a page-specific copy; anything in DO NOT TOUCH would need a change.

APPENDIX A — the foreword (verbatim; heading, three paragraphs, sign-off)
A confession from the person who built this
I didn't enjoy statistics at university. Even with a maths degree, stats was the bit that never clicked. I disliked it so much that in my final year I took Quantum Mechanics just to avoid it. If you know anything about Quantum Mechanics, you'll know how bad that makes stats sound. Would I have chosen differently if my lecturers had used real numbers with real context? Probably.
Then I built this site, and it started producing data: thousands of answers, none of it identifying a student. I've had to work hard to tell the numbers that matter from the noise. When is a trend not a trend? When is a difference actually significant?
So this section is the version I wish I'd been taught: real numbers, real decisions, and a nudge to think before you punch the buttons on a calculator. Computers are better at calculating. It still takes a human (for now) to make sure the right numbers go in.
Jon

APPENDIX B — Cases 1 and 2 questions (verbatim; {braces} are live values; → is the explanation)
Rules: D (days) = the number of UK calendar dates from max(1 Sep 2026, launch date) to the counts file's as-of date, both counted. Rounding: half up. A live question is skipped if any of its numbers is "<10" or missing.

Case 1
Q1 (typed, live). "Six Sevens, Bruv went on the site on {launch, e.g. 7 October 2026}. Since 1 September it has been available for {D} days and has {N} answers. What is its mean number of answers per day, to the nearest whole number?" Answer round(N/D). Working: "{N} ÷ {D} = {N/D to 1 dp} ≈ {answer}."
Q2 (typed, live). The same for Factor Theorem (slug from launch-dates.json; if its N is under 10, the lowest-answered game with N ≥ 10 that has a launch date, named in the stem).
Q3 (multiple choice, live numbers in the stem). "Six Sevens gets about {a} answers a day; {game 2} about {b}. Which is the best reason to be careful comparing these two numbers?"
 A ✓ "They're aimed at very different numbers of students: times tables are for almost everyone, factor theorem is for A level students only." → "Answers per day already allows for when each game launched, but not for how many people could ever play it. A fair comparison would need the size of each audience." (If game 2 is not Factor Theorem, the option says "{game 2} is for a much smaller group of students" and the explanation is unchanged.)
 B "You can't work out a mean for a game with so few answers." → "You can always work out a mean. The problem with few answers is that the mean can swing a lot with a single class, so it's less reliable, not impossible."
 C "Dividing by the number of days already makes the comparison fair." → "It makes it fairer, because it removes the launch-date difference. It doesn't remove the difference in who the games are for."
 D "The bigger number must include a mistake." → "Big differences are normal in skewed data like this. A surprising number is a reason to check, not proof of a mistake."
Q4 (multiple choice, frozen 12 Nov figures). "If we removed Six Sevens (4,181 answers) from the 116 games, which would change more?"
 A ✓ "The mean" → "The mean adds every value, so one huge value pulls it a long way. 25,438 ÷ 116 ≈ 219; without Six Sevens, 21,257 ÷ 115 ≈ 185. The median only moves by one place in the queue."
 B "The median" → "The median only looks at the middle of the queue. Removing the top game shifts it by half a place, so it barely moves."
 C "Both by the same amount" → as A.
 D "Neither" → as A.

Case 2
Q1 (typed, live, from the daily series). "Over the last 30 days, {W} weekdays had {Sw} games started in total. What is the mean number of games started per weekday, to the nearest whole number?" Answer round(Sw/W). Working: "{Sw} ÷ {W} = {to 1 dp} ≈ {answer}."
Q2 (typed, live). "The other {E} days were weekends, with {Se} games started. What is the mean per weekend day, to the nearest whole number?" Answer round(Se/E). Working as Q1.
Q3 (multiple choice, live numbers in the stem). "Weekdays average about {x} games started; weekend days about {y}. Which conclusion does this best support?"
 A ✓ "Most play happens on school days, which fits classroom use, but doesn't prove it." → "Homework is set on school days too, and plenty of students play at home in the evening. The pattern supports classroom use; it can't prove it on its own."
 B "It proves students play MaffsGames in lessons." → "A pattern that fits an explanation isn't proof of it. What else happens on weekdays and not at weekends?"
 C "Weekend play is low because the site doesn't work at weekends." → "Nothing about the site changes at weekends. Look for a reason in how people's weeks work."
 D "There's no real difference." → "{x} against {y} is a big gap, and it repeats every week in the chart. That's a pattern, not noise."
Q4 (multiple choice). "Which extra evidence would best tell classroom play apart from play at home, without knowing who anyone is?"
 A ✓ "Whether play drops during school holidays, like half-term." → "Classes stop in the holidays and homework mostly does too. A dip at half-term is evidence we already have: look at the daily chart for the last week of October."
 B "Students' names and schools." → "That would settle it, but we never collect them, and we never will."
 C "Which browser each player uses." → "Schools and homes use the same browsers, so it wouldn't separate them."
 D "The total number of answers since September." → "A bigger total doesn't say where or when anyone played."

APPENDIX C — Case 3, ugh-stats/one-class/ (verbatim)
Tag line: OUTLIERS · MEAN V MEDIAN
Title: One class, 3,667 answers
1 Ask: On 12 November I looked at the last four weeks: 13,664 answers in 28 days, a mean of 488 a day. I was pleased. That looked like growth. Was it?
2 Collect: Then I looked at the days. On Tuesday 3 November a single class in Malaysia answered 3,667 questions. On 23 October a class in Wales answered 3,099. Take those two days out and the other 26 days average 265. Two classes, on two days, had nearly doubled my "typical" day.
 Table, "The week of 2 November": Mon 2 | Tue 3 | Wed 4 | Thu 5 | Fri 6 / 108 | 3,667 | 402 | 228 | 578
3 Picture it: bar chart, answers per day, 15 Oct – 11 Nov, the two class days in the accent colour. Caption: "The two tall bars are single classes."
4 Decide: A value that sits far away from the rest is an outlier. The mean adds every value, so one outlier drags it a long way. The median only looks at the middle value, so it barely notices. This is why the Office for National Statistics reports the median wage as its headline figure for pay. A few very high earners pull the mean up, so the mean describes nobody's pay packet. The median is what the person in the middle earns. So when we talk about a typical day now, we use the median, and we report big class days on their own.
Can't tell us: "We can't be certain a big day is one class: we see a burst of answers from one country in a short time, not who sent them." / "Answers aren't students." / "Our own testing is in the numbers."
Questions:
Q1 (typed). "Find the mean number of answers per day for Monday 2 to Friday 6 November, to the nearest whole number." Answer 997. Working: "108 + 3,667 + 402 + 228 + 578 = 4,983. 4,983 ÷ 5 = 996.6 ≈ 997."
Q2 (typed). "Find the median number of answers per day for the same five days." Answer 402. Working: "In order: 108, 228, 402, 578, 3,667. The middle value is 402."
Q3 (multiple choice). "Which number best describes a typical weekday that week?"
 A ✓ "The median, 402." → "Only one day got anywhere near 997. Four of the five days were between 108 and 578, and the median sits among them. Without Tuesday, the mean would be 329 and the median 315: the median hardly moved, the mean fell by two-thirds."
 B "The mean, 997." → "Four of the five days were under 600. A 'typical' value that is higher than almost every day isn't typical."
 C "The biggest value, 3,667." → "That's the outlier itself: one class on one day."
 D "The range, 3,559." → "The range measures how spread out the values are, not what a typical day looks like."
Q4 (multiple choice). "Should we delete 3 November from our data?"
 A ✓ "No. It's real, so keep it, but use the median for a typical day and report the class separately." → "The class really did answer 3,667 questions. Deleting it would hide something true. Choose the average that answers your question, and say what you did."
 B "Yes, outliers are always mistakes." → "Some outliers are mistakes: always check. This one isn't: we know it was one class."
 C "Yes, it makes the site look busier than it is." → "That's a reason to describe it carefully, not to delete it."
 D "No, and the mean is the right average to report." → "Keeping it is right. But the mean of 997 still misdescribes a typical day."
data.csv (verbatim):
date,day,answers,games_started,whole_class_day
2026-10-15,Thu,513,98,no
2026-10-16,Fri,451,88,no
2026-10-17,Sat,71,28,no
2026-10-18,Sun,140,31,no
2026-10-19,Mon,214,35,no
2026-10-20,Tue,142,38,no
2026-10-21,Wed,118,41,no
2026-10-22,Thu,586,86,no
2026-10-23,Fri,3099,195,yes
2026-10-24,Sat,85,16,no
2026-10-25,Sun,124,37,no
2026-10-26,Mon,732,61,no
2026-10-27,Tue,172,33,no
2026-10-28,Wed,735,122,no
2026-10-29,Thu,80,22,no
2026-10-30,Fri,27,11,no
2026-10-31,Sat,51,11,no
2026-11-01,Sun,93,24,no
2026-11-02,Mon,108,28,no
2026-11-03,Tue,3667,375,yes
2026-11-04,Wed,402,58,no
2026-11-05,Thu,228,54,no
2026-11-06,Fri,578,100,no
2026-11-07,Sat,228,48,no
2026-11-08,Sun,115,34,no
2026-11-09,Mon,310,70,no
2026-11-10,Tue,357,82,no
2026-11-11,Wed,238,55,no
(Checks: 28 rows; answers sum 13,664, mean 488.0; without the two "yes" days 6,898 ÷ 26 = 265.3.)

APPENDIX D — Case 4, ugh-stats/flu-and-answers/ (verbatim)
Tag line: CORRELATION · LURKING VARIABLES · CORE MATHS
Title: Flu tests and maths answers
1 Ask: Every week the UK Health Security Agency publishes the percentage of flu tests in England that come back positive. This autumn it rose almost every week. So did the number of questions answered on MaffsGames. Do they move together, and if they do, why?
2 Collect: the table (Week beginning | Answers | Flu tests positive (%)): 7 Sep 1,141 3.4 / 14 Sep 875 3.8 / 21 Sep 2,291 5.0 / 28 Sep 2,846 6.5 / 5 Oct 2,169 6.2 / 12 Oct 1,887 6.4 / 19 Oct 4,368 6.6 / 26 Oct 1,890 7.8 / 2 Nov 5,326 8.1. Below it: "Flu: UK Health Security Agency, national flu and COVID-19 surveillance reports, 2026 to 2027 season (laboratory flu positivity, England, the 7 days to each Sunday, latest published figure). Answers: our own anonymous log."
3 Picture it: scatter, flu % (x) against answers (y); the weeks of 28 Sep, 19 Oct and 2 Nov as hollow points, key: "Hollow: a week with one whole-class day."
4 Decide: The correlation coefficient, r, measures how closely two sets of numbers follow a straight line. It runs from −1 (a perfect line going down) through 0 (no straight-line pattern) to +1 (a perfect line going up). For these two, r = 0.70. Does one cause the other? Neither: both follow the school term. So we don't read a rising line as growth until we can compare the same weeks next year.
Can't tell us: "Nine weeks is very few points." / "Flu positivity is the share of tests that are positive, not the number of people with flu." / "Our own testing is in the numbers."
Questions (multiple choice only):
Q1. "What does r = 0.70 tell you?"
 A ✓ "Weeks with more flu tended to have more answers: a fairly strong positive correlation." → "That's all r tells you: how closely the points follow a rising straight line. It says nothing about why."
 B "70% of the answers were caused by flu." → "r isn't a percentage, and it can't tell you about causes."
 C "Weeks with more flu caused more answers." → "r can't show what causes what. Keep going."
 D "70% of the points lie on the line." → "r measures how close the points are to a line overall, not how many sit exactly on it."
Q2. "What is the most likely explanation?"
 A ✓ "Something else drives both: the school term." → "In September schools go back. Classes start playing MaffsGames, and children mixing in classrooms spread flu. Both rise through the term, and neither causes the other. A hidden cause like this is called a lurking variable."
 B "More flu makes students practise more maths." → "Then the extra answers would come from students off sick. Case 3 showed the biggest weeks came from whole classes in school."
 C "It proves the site is getting more popular." → "The site may well be growing, but a correlation with flu can't show that. Growth would need its own evidence."
 D "It's just a coincidence." → "With only 9 weeks, chance can't be ruled out. But we already know a shared cause that explains both, so 'coincidence' isn't the best explanation."
Q3. "The number of hours of daylight in the south-west of England also correlates with our answers: r = −0.72. Daylight and flu correlate with each other: r = −0.96. What do all three have in common?"
 A ✓ "They all follow the time of year." → "Daylight shrinks every week of autumn whatever we do; flu and term-time play both grow. Anything that changes steadily through autumn will correlate with our numbers. That's why 'it correlates' is the start of an argument, never the end."
 B "Each one causes the next." → "Three causes in a chain, with no evidence for any of them. The time of year explains all three at once."
 C "Daylight is the real cause of our answers." → "Daylight correlates just as strongly as flu, for the same reason. Swapping one non-cause for another doesn't help."
 D "Nothing: three strong correlations must be proof." → "Three correlations that share one hidden cause are really one pattern, seen three times."
Q4. "Three of those weeks contained a single class that answered thousands of questions in one day (28 Sep, 23 Oct, 3 Nov). Take those three days out and r between flu and answers falls from 0.70 to 0.43. What does this show?"
 A ✓ "A few extreme values can make a correlation look much stronger than it is." → "Like the mean in Case 3, r uses every value, so outliers pull it. Two of the three classes came late in term, when flu was highest, and that alone made the pattern look much tighter."
 B "There was never any link." → "0.43 is still a weak positive correlation: the term effect is still there, just smaller."
 C "You should always remove outliers before working out r." → "Not always. Check them, understand them, and report r with and without them, as we've done here."
 D "Nine weeks is plenty to be sure." → "Nine points is very few. Three days cut r by more than a third. Treat any r from a small sample with care."
data.csv (verbatim):
week_beginning,answers,answers_without_class_days,games_started,flu_tests_positive_pct,daylight_hours
2026-09-07,1141,1141,198,3.4,12.86
2026-09-14,875,875,176,3.8,12.40
2026-09-21,2291,2291,309,5.0,11.95
2026-09-28,2846,1385,449,6.5,11.49
2026-10-05,2169,2169,280,6.2,11.05
2026-10-12,1887,1887,419,6.4,10.61
2026-10-19,4368,1269,448,6.6,10.18
2026-10-26,1890,1890,284,7.8,9.78
2026-11-02,5326,1659,697,8.1,9.39
(Checks, Pearson r from these columns, 2 dp: flu~answers 0.70; flu~answers_without_class_days 0.43; daylight~answers −0.72; daylight~flu −0.96.)

APPENDIX E — landing-page cards
Card 3: tag "OUTLIERS · MEAN V MEDIAN"; title "One class, 3,667 answers"; text "Our busiest month looked like growth. Was it?"; link "Read the case" → /ugh-stats/one-class/
Card 4: tag "CORRELATION · LURKING VARIABLES · CORE MATHS"; title "Flu tests and maths answers"; text "Our weekly answers rise with the share of positive flu tests in England. Does one cause the other?"; link "Read the case" → /ugh-stats/flu-and-answers/

APPENDIX F — Correlation or Coincidence, the new item (verbatim)
{id:'B29', cat:'both', x:['Hours of daylight in a day',9,13,0], y:['Questions answered on MaffsGames in a week',800,5400,1], dir:-1, str:'strong', n:12,
 lurk:'the autumn term: the days shorten while more classes find the site', explain:'Dark days don\'t make anyone do maths. Through the autumn term the days get shorter while more classes find the site, so both change together. We saw this in our own numbers in autumn 2026.'},
