# Counting Players: approved text, first edition

Source text for tools/counting-players/. Written by Project Claude, 20 Nov 2026, from the prototype Jon approved on 20 Nov 2026, rewritten for the window 20 September to 19 November 2026.

Every number that comes from the data appears as {{key}}. The generator computes every key from the two CSVs and fills it in. **Values** at the end gives each key's definition and the value it must have for this edition; the generator fails if a computed value differs. **Conditions** lists the facts the wording relies on; the generator fails if any is false. Numbers that are not keys (mark totals, question numbers, the 30-minute and 10-second definitions) are fixed text.

Register: exam board, neutral, no humour. TABLE and CHART in capitals. Marks in square brackets, right-aligned. Footer on every page of all three PDFs: `MaffsGames · Counting Players · Level 3 Core Maths practice material · First edition, November 2026 · Page n`.

---

## PRELIMINARY MATERIAL

**Counting Players**
Level 3 Core Maths · Preliminary Material
Read this material before the practice paper. A clean copy should be provided with the paper.

### Background
MaffsGames (maffsgames.co.uk) is a free maths games website for students aged 11 to 18 and for apprentices. Users do not sign up or create accounts. The website records how it is used with a tool called Google Analytics 4 (GA4). This material and its data file show what GA4 recorded between 20 September and 19 November 2026: {{days}} days in all.

### Definitions used by GA4
**Session.** One visit to the site by one web browser. A session ends after 30 minutes with no activity.
**Engaged session.** A session that lasted longer than 10 seconds, or included an action the site marks as important, or viewed at least 2 pages.
**Active users.** The number of different web browsers that used the site. GA4 identifies a browser, not a person.
**Source and medium.** Where a session came from. The source is the website or tool (for example google or facebook.com). The medium is the type of route, listed in TABLE 1.
**Landing page.** The first page of the site seen in that session.
**Small numbers.** When counts are very small, GA4 may withhold some of them to protect privacy.

### The data file
The file maffsgames-site-data-sep-nov-2026.csv has {{rows}} rows. Each row is one combination of date, source, medium, device and landing page, with the number of sessions, engaged sessions and active users for that combination on that day. The names of individual schools have been replaced by school platform A, school platform B and school platform C. Tracking codes added by other websites have been removed from the landing pages, and rows that then matched have been added together.
The data includes visits made by the owner of the website while testing the games. The number of these visits is not known.

**TABLE 1: Sessions by medium** (columns: Medium · Sessions · Engaged sessions; rows in this order, largest first)
- organic (search results, not adverts) · {{m_organic_s}} · {{m_organic_e}}
- (none): no source recorded · {{m_none_s}} · {{m_none_e}}
- referral (a link on another website) · {{m_referral_s}} · {{m_referral_e}}
- ai-assistant (AI chat tools) · {{m_ai_s}} · {{m_ai_e}}
- (not set): GA4 could not tell · {{m_notset_s}} · {{m_notset_e}}
- cpc (labelled as a paid advert click) · {{m_cpc_s}} · {{m_cpc_e}}
- Total · {{sessions}} · {{engaged}}

**TABLE 2: Sessions by device** (Device · Sessions · Engaged sessions)
- desktop · {{d_desktop_s}} · {{d_desktop_e}}
- mobile · {{d_mobile_s}} · {{d_mobile_e}}
- tablet · {{d_tablet_s}} · {{d_tablet_e}}

**TABLE 3: Sessions by month** (Month · Sessions). Labels exactly "Sep 2026", "Oct 2026", "Nov 2026", with no note that two are part months.
- Sep 2026 · {{mon_sep}}
- Oct 2026 · {{mon_oct}}
- Nov 2026 · {{mon_nov}}

**TABLE 4: Sessions from school learning platforms** (Source · Sessions · Engaged sessions · Days seen; rows largest first by sessions)
- Google Classroom · {{p_classroom_s}} · {{p_classroom_e}} · {{p_classroom_d}}
- School platform A · {{p_a_s}} · {{p_a_e}} · {{p_a_d}}
- Microsoft OneNote · {{p_onenote_s}} · {{p_onenote_e}} · {{p_onenote_d}}
- Microsoft Teams · {{p_teams_s}} · {{p_teams_e}} · {{p_teams_d}}
- School platform C · {{p_c_s}} · {{p_c_e}} · {{p_c_d}}
- School platform B · {{p_b_s}} · {{p_b_e}} · {{p_b_d}}
Note under the table: Days seen is the number of different days on which that source sent at least one session.

**CHART 1: Sessions per week.** A vertical bar chart, one bar per week, weeks beginning on a Monday. Horizontal-axis labels are the Mondays, "14 Sep" to "16 Nov" ({{weeks}} bars). **Deliberately imperfect, and the mark scheme depends on it:** no vertical-axis label; nothing marks the first or last bar as a part week; sessions per week, not per day. Values on top of each bar.

### Game records
TABLES 1 to 4 and CHART 1 come from GA4. TABLE 5 and CHART 2 come from the website's own game records. Each time a game is started or a question is answered, the game sends an anonymous record.

**TABLE 5: Accuracy by game, 13 to 19 November 2026**
Line above the table: Games with at least 100 marked answers that week. Over all games that week, {{wk_answers}} answers were marked and {{wk_overall_pct}}% were correct.
Columns: Game · Answers · Correct · Accuracy. Rows ordered by accuracy, lowest first; accuracy to the nearest whole number. Game names are the site's short names (for example escape-comic-caper).

**CHART 2: Games started and questions answered each day, 20 October to 19 November 2026.** Bars: questions answered (left axis, labelled). Line: games started (right axis, labelled). Horizontal axis: dates, every 7th labelled. Both axes labelled; this chart is not the deliberately imperfect one.

END OF PRELIMINARY MATERIAL

---

## PRACTICE PAPER

Cover page:
**Counting Players**
Level 3 Core Maths · Practice paper: critical analysis
Time allowed: 1 hour 30 minutes
**Materials.** For this paper you must have: a clean copy of the Preliminary Material; the data file maffsgames-site-data-sep-nov-2026.csv and access to a spreadsheet; a scientific or graphical calculator; a ruler.
**Instructions.** Answer all questions. Answer the questions in the spaces provided. Show all necessary working; otherwise marks for method may be lost.
**Information.** The marks for questions are shown in brackets. The maximum mark for this paper is 56.
This practice paper is written in the style of Level 3 Core Maths examinations. It is not an exam board paper and is not endorsed by any exam board.

**1 (a)** Use TABLE 1 in the Preliminary Material. Calculate the percentage of all sessions that were engaged. Give your answer to 1 decimal place. [2 marks]
**1 (b)** Use TABLE 2 in the Preliminary Material. Calculate the percentage of mobile sessions that were engaged. [1 mark]
**1 (c)** {{desk_pct}}% of desktop sessions were engaged. Compare this with your answer to part (b). [1 mark]

**2** Sam uses TABLE 3 in the Preliminary Material. He writes: *Visits to MaffsGames fell by {{sam_fall}}% from October to November.*
**2 (a)** Show how Sam obtained {{sam_fall}}%. [2 marks]
**2 (b)** Critically analyse Sam's statement. [2 marks]
**2 (c)** Use a more appropriate method to compare the number of sessions in October and November. Give your answer as a percentage change. [3 marks]

**3** The number of sessions on each day was recorded. The information below summarises these values.
Weekdays ({{wd_n}} days): lowest value {{wd_min}}, lower quartile {{wd_lq}}, median {{wd_med}}, upper quartile {{wd_uq}}, highest value {{wd_max}}
Weekends ({{we_n}} days): lowest value {{we_min}}, lower quartile {{we_lq}}, median {{we_med}}, upper quartile {{we_uq}}, highest value {{we_max}}
**3 (a)** On a common scale, draw box plots to represent the number of sessions per day on weekdays and at weekends. [3 marks] (Provide a grid from 0 to 180.)
**3 (b)** Make two comparisons between the number of sessions per day on weekdays and at weekends. [2 marks]
**3 (c)** Use your answer to part (b) to suggest when MaffsGames is mainly used. Give a reason for your answer. [1 mark]

**4** A report states: *MaffsGames had {{users_sum}} users between 20 September and 19 November 2026.* The figure was obtained by adding together all the values in the active_users column of the data file. Critically analyse the figure in the report. [2 marks]

**5 (a)** Use the data file. Calculate the percentage of all sessions that had the source google. Include all mediums. [2 marks]
**5 (b)** The owner of the website claims: *Most of our visitors find us on Google.* Use your answer to part (a) and the Preliminary Material to comment on this claim. [2 marks]

**6 (a)** Suggest two improvements to CHART 1 in the Preliminary Material. [2 marks]
**6 (b)** Ali states: *Visits dropped in the week beginning 16 November.* Comment on Ali's statement. [1 mark]

**7** Use TABLE 2 in the Preliminary Material. Kai concludes: *The games must be worse on mobile phones.* Does the data support Kai's conclusion? Give a reason for your answer. [2 marks]

**8** The website has never paid for an advert. {{cpc_s}} sessions in the data file have the medium cpc, which records a paid advert click. Use the data file to describe these sessions. Suggest two possible explanations for this data. State, with a reason, which explanation the data suggests is more likely. [4 marks]

**9** Use TABLE 4 in the Preliminary Material. A teacher claims: *Students using Microsoft Teams are less interested in maths than students using school platform A.* Comment on the teacher's claim. [2 marks]

**10** Use TABLE 5 in the Preliminary Material.
**10 (a)** Sam calculates the mean of the {{t5_n}} percentages in TABLE 5. He obtains {{sam_mean_round}}%, to the nearest whole number. Show how Sam obtained this value. [2 marks]
**10 (b)** Sam notices that his value is the same as the {{wk_overall_pct}}% given above TABLE 5. He says: *This shows my method gives the right answer.* Comment on Sam's statement. [2 marks]
**10 (c)** Calculate the percentage of answers that were correct for the {{t5_n}} games in TABLE 5 together. [2 marks]
**10 (d)** A newspaper article states: *Comic Caper is the hardest game on MaffsGames.* (Comic Caper is the escape room listed as escape-comic-caper.) Evaluate this statement. [2 marks]

**11** Use CHART 2 in the Preliminary Material and the information below.
3 November 2026: {{nov3_g}} games started, {{nov3_q}} questions answered
23 October 2026: {{oct23_g}} games started, {{oct23_q}} questions answered
**11 (a)** Calculate the mean number of questions answered per game started on each of these days. [2 marks]
**11 (b)** Jo states: *MaffsGames is growing fast. On 3 November more than ten times as many games were started as on 2 November.* Comment on Jo's statement. [2 marks]
**11 (c)** Give two pieces of additional information that would help you decide whether the high value on 3 November was caused by one class. [2 marks]

**12** You are an analyst for the website. Write a short report for the owner of the website. Your report should include:
- three findings from the data, supported by figures
- one question the owner may want to answer that this data cannot answer, with a reason. [8 marks]

END OF QUESTIONS

---

## MARK SCHEME

**Counting Players**
Level 3 Core Maths · Practice paper: critical analysis · Mark scheme

**Notes for teachers.** Issue the Preliminary Material and the data file before the paper is sat. Questions 1 to 3 assess analysis of data (AQA 1350 Paper 1, 3.1). Questions 4 to 12 assess critical analysis (AQA 1350 Paper 2, 3.4, assessed in every Paper 2 option). The data is real. The only changes are the anonymised school names and the removal of tracking codes from web addresses. CHART 1 is deliberately imperfect: it has no vertical-axis label and does not identify its two part weeks.
M: method mark. A: accuracy mark, dependent on the preceding M mark. B: independent mark. E: mark for explanation. ft: follow through. oe: or equivalent. Answers to questions requiring explanation must refer to the context; generic statements without reference to the data score E0.

| Q | Marking guidance | Total |
|---|---|---|
| 1 (a) | M1 {{engaged}} ÷ {{sessions}} × 100. A1 {{eng_pct}}%. | 2 |
| 1 (b) | B1 {{d_mobile_e}} ÷ {{d_mobile_s}} × 100 = {{mob_pct}}% (accept {{mob_pct}} or {{mob_pct_whole}}). | 1 |
| 1 (c) | E1ft: desktop sessions were more likely to be engaged ({{desk_pct}}% against {{mob_pct}}%), a difference of about {{desk_mob_gap}} percentage points. Do not accept "desktop had more sessions" (that is the count, not the rate). | 1 |
| 2 (a) | M1 ({{mon_nov}} − {{mon_oct}}) ÷ {{mon_oct}}. A1 {{sam_change_signed}}%, so a fall of about {{sam_fall}}%. | 2 |
| 2 (b) | E1 the November figure covers only 19 days, but October covers 31. E1 so the comparison is not like for like / he should compare the rate per day / November is not finished. A conclusion without a reason scores E1 E0. | 2 |
| 2 (c) | M1 rate per day for one month: October {{mon_oct}} ÷ 31 = {{oct_rate}}; November {{mon_nov}} ÷ 19 = {{nov_rate}}. M1 percentage change of the rates. A1 an increase of {{rate_change}}% (accept {{rate_change_lo}} to {{rate_change_hi}}). Note: the rate per day increases although the monthly total decreases. | 3 |
| 3 (a) | B3 both box plots on a common, labelled scale. B2 one correct, or both with one error. B1 one with one error. | 3 |
| 3 (b) | E1 a comparison of averages in context: the median on weekdays ({{wd_med}}) is more than twice the weekend median ({{we_med}}). E1 a comparison of spread in context: weekday IQR {{wd_iqr}} against weekend IQR {{we_iqr}}, so weekday numbers vary much more. Do not accept comparisons with no figures or no context. | 2 |
| 3 (c) | E1 the site is used more on school days, which suggests much of the use is in lessons, set by teachers or in school time. Accept "for homework set on weekdays" with a reason. | 1 |
| 4 | E1 the same browser is counted again in every row it appears in, on every day it visits, so adding the column overcounts: the true number of different browsers is lower than {{users_sum}}. E1 a browser is not a person: one person on two devices counts twice, a class sharing a computer counts once. Do not accept "the number is too big" with no reason. | 2 |
| 5 (a) | M1 total sessions with source google (organic and cpc rows) ÷ {{sessions}}. A1 {{google_s}} ÷ {{sessions}} = {{google_pct}}% (accept {{google_pct_lo}} to {{google_pct_hi}}). Special case: organic search from all engines gives {{organic_pct}}%, B1 only. | 2 |
| 5 (b) | E1 {{google_pct}}% is less than half, so "most" is not supported. E1 a further valid point, for example: Google is still the largest single source; {{none_pct}}% of sessions have no source recorded, so the true share from Google could be higher; some google sessions are labelled as paid adverts and may not be real visitors. | 2 |
| 6 (a) | E1 E1 any two of: label the vertical axis (sessions); the first bar covers only {{first_week_days}} day and the last only {{last_week_days}} days, so mark them as part weeks or leave them out; the first label says 14 Sep but the data starts on 20 September; show sessions per day so weeks of different lengths can be compared. Do not accept colour or style changes. | 2 |
| 6 (b) | E1 the last week covers only {{last_week_days}} days. Its {{last_week_s}} sessions are {{last_week_rate}} a day, higher than any complete week (the best was {{best_week_rate}} a day, week beginning {{best_week_label}}), so visits did not drop. | 1 |
| 7 | E1 No. E1 a valid reason, for example: the difference is small ({{desk_pct}}% against {{mob_pct}}%); different people use phones, for example at home or from social media links, rather than in lessons set by a teacher; there is a third factor; correlation does not show causation. A "No" with no reason scores E1 E0. | 2 |
| 8 | B1 a description from the data: {{cpc_day1_s}} sessions on 07 October from {{cpc_day1_u}} different users and {{cpc_day2_s}} on 16 October, all on desktop, all landing on the home page, none engaged. E1 E1 two possible explanations, for example: automated traffic (a program, not people); a link to the site carrying an advert-click tag, created by someone else; GA4 has labelled the visits wrongly. E1 a justified choice: automated traffic is more likely, because {{cpc_day1_u}} users on one day all left without engaging, all on desktop and all on the same page. The data cannot prove which explanation is right; accept a well-argued alternative. | 4 |
| 9 | E1 Teams sessions were less often engaged ({{teams_pct}}% against {{a_pct}}%). E1 but this does not show students are less interested: the numbers are small ({{p_teams_s}} and {{p_a_s}} sessions); Teams sessions may come from many schools while platform A is probably one class; teachers clicking to check a link count too; the games linked are different. | 2 |
| 10 (a) | M1 add the {{t5_n}} percentages: {{t5_sum}}. A1 ÷ {{t5_n}} = {{sam_mean}}, about {{sam_mean_round}}%. | 2 |
| 10 (b) | E1 the two methods are different: Sam gives every game equal weight, but the games had very different numbers of answers ({{t5_max_game}} had {{t5_max_n}}, {{t5_min_game}} had {{t5_min_n}}); the {{wk_overall_pct}}% counts every answer, including the {{t5_left_n}} answers in games with fewer than 100, which TABLE 5 leaves out. E1 so the match is a coincidence and does not show the method is right; with other data the two would differ (for the {{t5_n}} games together the figure is {{t5_pooled}}%, part (c)). | 2 |
| 10 (c) | M1 {{t5_correct}} ÷ {{t5_answers}}. A1 {{t5_pooled}}% (accept {{t5_pooled_lo}} to {{t5_pooled_hi}}). | 2 |
| 10 (d) | E1 Comic Caper had the lowest accuracy that week ({{cc_pct}}%, from {{cc_n}} answers). E1 a valid criticism: an escape room lets a group try a lock again and again, so every guess counts as an answer and its accuracy is not comparable with a game where each question is answered once; one week only; accuracy depends on who played it (their level, or one class), not only on the game; games with fewer than 100 answers are not in the table. A conclusion with no reason scores E1 E0. | 2 |
| 11 (a) | M1 questions ÷ games for either day. A1 3 November {{nov3_ratio}}, 23 October {{oct23_ratio}} (over the 31 days in CHART 2 the mean is {{c2_mean}}). | 2 |
| 11 (b) | E1 the spike is a single day: the next day had {{nov4_g}} games started, so it does not show steady growth. E1 2 November had only {{nov2_g}} games, so the comparison starts from a low day; a fair comparison uses weekly totals or a longer period. Accept: a single class can cause a spike. | 2 |
| 11 (c) | B1 B1 any two, for example: which games were started; the times of the starts (all in one lesson?); how many different browsers; which level; the source (a school platform?); whether the same happens on other days. | 2 |
| 12 | Up to 8 marks. B1 for each of three valid findings supported by a correct figure (max B3). E1 for each finding interpreted in context (max E3). E1 for a valid limitation, for example: GA4 cannot tell people apart; no data on whether anyone learned anything; owner's testing included; small numbers withheld. E1 for explaining why the data cannot answer it. | 8 |
| | Total | 56 |

---

## Values (first edition: the generator must reproduce every one)

Site data = maffsgames-site-data-sep-nov-2026.csv. Game records = maffsgames-game-records-sep-nov-2026.csv. Percentages to 1 d.p. unless stated; thousands with a comma.

| Key | Definition | Value |
|---|---|---|
| days | days from 20 Sep to 19 Nov 2026 inclusive | 61 |
| rows | data rows in the site data | 1,804 |
| sessions, engaged | sum of sessions, engaged_sessions | 4,220; 2,326 |
| m_*_s, m_*_e | sessions, engaged by medium (organic, (none), referral, ai-assistant, (not set), cpc) | 2,052/1,305; 1,625/717; 387/219; 119/84; 20/1; 17/0 |
| d_*_s, d_*_e | by device (desktop, mobile, tablet) | 3,245/1,828; 915/465; 60/33 |
| mon_sep, mon_oct, mon_nov | sessions by calendar month | 596; 1,831; 1,793 |
| p_classroom_* | source classroom.google.com: sessions, engaged, distinct dates | 53, 41, 11 |
| p_a_* | school platform A | 45, 40, 7 |
| p_onenote_* | euc-onenote.officeapps.live.com | 32, 22, 8 |
| p_teams_* | teams.public.onecdn.static.microsoft and statics.teams.cdn.office.net together (dates: distinct across both) | 28, 12, 16 |
| p_c_*, p_b_* | school platform C; school platform B | 4, 1, 2; 1, 1, 1 |
| weeks | Monday-start weeks touched by the window | 10 |
| eng_pct | engaged ÷ sessions | 55.1 |
| mob_pct, mob_pct_whole | mobile engaged rate; same to whole number | 50.8; 51 |
| desk_pct | desktop engaged rate | 56.3 |
| desk_mob_gap | desk_pct − mob_pct | 5.5 |
| sam_change_signed, sam_fall | (mon_nov − mon_oct) ÷ mon_oct × 100 to 1 d.p.; its magnitude to nearest whole | −2.1; 2 |
| oct_rate, nov_rate | mon_oct ÷ 31, mon_nov ÷ 19 | 59.1; 94.4 |
| rate_change (lo, hi) | (nov_rate ÷ oct_rate − 1) × 100, from unrounded rates; lo from rates rounded to 1 d.p., hi = rate_change | 59.8 (59.7, 59.8) |
| wd_*, we_* | daily session totals, Mon–Fri / Sat–Sun: n, min, lower quartile, median, upper quartile, max; quartiles by linear interpolation (spreadsheet QUARTILE.INC) | 44, 36, 52, 78, 102.5, 162; 17, 18, 25, 30, 47, 97 |
| wd_iqr, we_iqr | upper − lower quartile | 50.5; 22 |
| users_sum | sum of active_users | 3,580 |
| google_s, google_pct (lo, hi) | sessions with source google, any medium; ÷ sessions; lo/hi = google_pct ∓ 0.1 | 1,718; 40.7 (40.6, 40.8) |
| organic_pct | medium organic ÷ sessions | 48.6 |
| none_pct | medium (none) ÷ sessions | 38.5 |
| first_week_days, last_week_days | days of the window in the first and last Monday-start weeks | 1; 4 |
| last_week_s, last_week_rate | sessions in the last week; ÷ its days | 576; 144 |
| best_week_rate, best_week_label | highest sessions per day among complete weeks; its Monday as dd/mm | 91.9; 09/11 |
| cpc_s | sessions with medium cpc | 17 |
| cpc_day1_s, cpc_day1_u, cpc_day2_s | cpc sessions and active users on 2026-10-07; cpc sessions on 2026-10-16 | 15, 15, 2 |
| teams_pct, a_pct | engaged ÷ sessions to whole number: Teams, school platform A | 43; 89 |
| wk_answers, wk_overall_pct | game records 2026-11-13 to 2026-11-19: sum answers_marked; correct ÷ marked to whole number | 3,839; 68 |
| t5_n | games with at least 100 marked answers that week | 14 |
| t5_sum | sum of their accuracies, each rounded to whole number first | 945 |
| sam_mean, sam_mean_round | t5_sum ÷ t5_n; to whole number (half up) | 67.5; 68 |
| t5_answers, t5_correct, t5_pooled (lo, hi) | totals over the TABLE 5 games; correct ÷ answers; lo = t5_pooled, hi = t5_pooled rounded to whole | 2,561; 1,783; 69.6 (69.6, 70) |
| t5_left_n | wk_answers − t5_answers | 1,278 |
| t5_max_game, t5_max_n, t5_min_game, t5_min_n | TABLE 5 games with most and fewest answers | formula-plug-in, 290; sequence-solver, 108 |
| cc_pct, cc_n | escape-comic-caper accuracy to 1 d.p., answers | 10.7; 159 |
| nov2_g, nov3_g, nov3_q, nov4_g | games started / answers marked on those dates | 28; 375, 3,667; 58 |
| oct23_g, oct23_q | on 2026-10-23 | 196; 3,099 |
| nov3_ratio, oct23_ratio | answers ÷ games started, 1 d.p. | 9.8; 15.8 |
| c2_mean | over 2026-10-20 to 2026-11-19: total answers ÷ total games started, 1 d.p. | 6.8 |

## Conditions (the wording is false if any fails)

1. mon_nov < mon_oct (Sam's "fell"), and nov_rate > oct_rate.
2. desk_pct > mob_pct.
3. Every weekday statistic is above its weekend counterpart, and wd_med > 2 × we_med; wd_max ≤ 180.
4. google_pct < 50; google is the source with the most sessions.
5. The last Monday-start week has fewer sessions than the week before it (Ali's "dropped"), and last_week_rate > best_week_rate.
6. All cpc rows: source google, device desktop, landing page /, engaged 0, dates only 2026-10-07 and 2026-10-16.
7. teams_pct < a_pct.
8. sam_mean_round = wk_overall_pct (the premise of 10(b)), and t5_pooled ≠ wk_overall_pct when both are to 1 d.p.
9. escape-comic-caper is in TABLE 5 and has its lowest accuracy.
10. nov3_g > 10 × nov2_g; nov4_g < nov3_g ÷ 2.
11. No source in the site data names a school, college or other single institution, other than as school platform A, B or C.
