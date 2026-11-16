BETTER-VALUE-GCSE-40 (Project Claude, Mon 16 Nov 2026 15:55; Jon 15:18 "yes please")
Recommended: Sonnet, effort medium: twenty checked items pasted into one bank, the verifier's review table extended with the lines given; the verifiers do the maths.
LANE: cloud. SEND: now, in a new cloud session (cloud lane free since #795; main at ef92245). TIER: Small (merge on green; Project Claude reviews after the merge; Jon plays GCSE after it). One PR, branched from current origin/main.
CLOSE-OUT (first commit, AGENTS.md:61): ANGLE-ACE-GCSE-45 (with Amendments 1 and 2) merged #795 by merge-pr.py as 833f6e1 (its last line "main 833f6e1 run 43882219345: GREEN", exit 0); main check-site 43882219345 success (14:19:57 UTC), phone-fit-full 43882219278 success (14:06:17 UTC), both push-triggered. Move docs/handover/contracts/2026-11-16-angle-ace-gcse-45.md to docs/history/contracts/ with those figures. Save this contract verbatim as docs/handover/contracts/2026-11-16-better-value-gcse-40.md in the same commit.
MERGE: python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600, unpiped; report its last line. No other route: if merge-pr.py cannot reach GitHub, STOP and report; the PR waits.

TASK: Bring Better Value's GCSE bank from 20 to 40 questions with the twenty items below, verbatim, so the level the Essentials page and the portal link (?level=gcse) meets the site's 40-50 minimum.

ROOT CAUSE (main ef92245): QUESTIONS.gcse in games/better-value/index.html (:958-1222) has 20 items (bv_gcse_001-020), half the 40 minimum (check-banks B4; data/check-ledger.json entry "better-value::gcse"; todo LEDGER-B4-BETTER-VALUE). Better Value is on the Essentials page (essentials/index.html links games/better-value/?level=gcse). scripts/verify-better-value.py holds COUNTS = {'gcse': 20, 'core': 50} (:46) and a REVIEW entry per item (:65-), and fails any item not in REVIEW.

CLASS CHECK: Local. One game's bank is short; content was the missing piece. Correctness is already held architecturally by two verifiers that recompute every item from its own numbers: scripts/verify-better-value-claims.py (each item's declared measure computed from its inputs; the key's claim true, every distractor's false; every text figure in its claim) and scripts/verify-better-value.py (every keyed and explanation figure recomputed, one true card in four, every card marked in Chromium). The new items go through both unchanged; the only verifier change is the data it needs (counts, REVIEW lines, the break-even and wording lists), as for every existing item. No shared code changes. Derived files: none (scripts/gen-six-ps.py and scripts/gen-exam-topics.py do not read this game; Project Claude grepped scripts/ for the slug).

EXACT CHANGE:
1. games/better-value/index.html: append these twenty items to QUESTIONS.gcse, verbatim, after bv_gcse_020 (whose explanation ends "From bottle 16 onwards, the reusable bottle is cheaper.'}"; add a comma after its closing brace) and before the closing ] of the gcse array:

// === Direct Comparison, more (6, added 16 Nov 2026) ===
{id:'bv_gcse_021',level:'gcse',type:'direct',
criterion:'Mia wants her 8 gym visits this month for the least money.',measure:'total_cost',inputs:{visits:8,A:{terms:[{name:'day pass',amount:6,times:['visits']}]},B:{terms:[{name:'monthly fee',amount:40}]}},
scenario:'Mia plans to go to the gym 8 times this month. She can buy a day pass each time or pay a monthly fee. Mia wants her 8 gym visits this month for the least money.',
optionA:{label:'Day passes',details:[{key:'Day pass',value:'£6 each'}]},
optionB:{label:'Monthly membership',details:[{key:'Monthly fee',value:'£40'}]},
conclusions:[
{text:'Day passes are cheaper: £6 vs £40',correct:false,claim:{winner:'A',figures:[{option:'A',value:6,of:'amount:day pass'},{option:'B',value:40}]}},
{text:'The monthly membership is cheaper: £40 vs £48 for day passes',correct:true,claim:{winner:'B',figures:[{option:'B',value:40},{option:'A',value:48}]}},
{text:'They cost the same for 8 visits',correct:false,claim:{winner:'equal',figures:[{option:null,value:8,of:'given'}]}},
{text:'The monthly membership saves £12',correct:false,claim:{winner:'B',figures:[{option:null,value:12,of:'difference'}]}}
],
explanation:'Day passes: 8 × £6 = £48. Monthly membership: £40. The membership saves £8.'},

{id:'bv_gcse_022',level:'gcse',type:'direct',
criterion:'Leo wants his 10 driving lessons for the least money.',measure:'total_cost',inputs:{lessons:10,A:{terms:[{name:'per lesson',amount:30,times:['lessons']}]},B:{terms:[{name:'block of 10',amount:270}]}},
scenario:'Leo needs 10 driving lessons. Instructor A charges per lesson. Instructor B sells a block of 10 lessons. Leo wants his 10 driving lessons for the least money.',
optionA:{label:'Instructor A',details:[{key:'Per lesson',value:'£30'}]},
optionB:{label:'Instructor B',details:[{key:'Block of 10',value:'£270'}]},
conclusions:[
{text:'Instructor A is cheaper: £30 per lesson vs £270',correct:false,claim:{winner:'A',figures:[{option:'A',value:30,of:'amount:per lesson'},{option:'B',value:270}]}},
{text:'Instructor B is cheaper: £270 vs £300 for Instructor A',correct:true,claim:{winner:'B',figures:[{option:'B',value:270},{option:'A',value:300}]}},
{text:'They cost the same for 10 lessons',correct:false,claim:{winner:'equal',figures:[{option:null,value:10,of:'given'}]}},
{text:'Instructor A is better because you can stop at any time',correct:false,claim:{winner:'A',figures:[]}}
],
explanation:'Instructor A: 10 × £30 = £300. Instructor B: £270. Instructor B saves £30.'},

{id:'bv_gcse_023',level:'gcse',type:'direct',
criterion:'Aisha wants 2 tickets for the least money.',measure:'total_cost',inputs:{tickets:2,A:{terms:[{name:'ticket',amount:35,times:['tickets']},{name:'booking fee',amount:4.5,times:['tickets']}]},B:{terms:[{name:'ticket',amount:38,times:['tickets']}]}},
scenario:'Aisha is buying 2 concert tickets. Site A adds a booking fee to each ticket. Site B has no booking fee. Aisha wants 2 tickets for the least money.',
optionA:{label:'Site A',details:[{key:'Ticket',value:'£35 each'},{key:'Booking fee',value:'£4.50 per ticket'}]},
optionB:{label:'Site B',details:[{key:'Ticket',value:'£38 each'},{key:'Booking fee',value:'None'}]},
conclusions:[
{text:'Site A is cheaper: £35 vs £38 per ticket',correct:false,claim:{winner:'A',figures:[{option:'A',value:35,of:'amount:ticket'},{option:'B',value:38,of:'amount:ticket'}]}},
{text:'Site B is cheaper: £76 vs £79 for Site A',correct:true,claim:{winner:'B',figures:[{option:'B',value:76},{option:'A',value:79}]}},
{text:'They cost the same for 2 tickets',correct:false,claim:{winner:'equal',figures:[{option:null,value:2,of:'given'}]}},
{text:'Site B saves £6',correct:false,claim:{winner:'B',figures:[{option:null,value:6,of:'difference'}]}}
],
explanation:'Site A: 2 × (£35 + £4.50) = 2 × £39.50 = £79. Site B: 2 × £38 = £76. Site B saves £3.'},

{id:'bv_gcse_024',level:'gcse',type:'direct',
criterion:'Ben wants to get to the airport for the least money.',measure:'total_cost',inputs:{A:{terms:[{name:'fixed fare',amount:45}]},B:{terms:[{name:'base fare',amount:2.5},{name:'per mile',amount:1.6,times:[25]}]}},
scenario:'Ben needs a taxi to the airport, 25 miles away. Ben wants to get to the airport for the least money.',
optionA:{label:'Airport Cars',details:[{key:'Fixed fare',value:'£45'}]},
optionB:{label:'Metro Taxis',details:[{key:'Base fare',value:'£2.50'},{key:'Per mile',value:'£1.60'},{key:'Distance',value:'25 miles'}]},
conclusions:[
{text:'Airport Cars is cheaper: £45 vs £2.50 to start',correct:false,claim:{winner:'A',figures:[{option:'A',value:45},{option:'B',value:2.5,of:'amount:base fare'}]}},
{text:'Metro Taxis is cheaper: £42.50 vs £45 for Airport Cars',correct:true,claim:{winner:'B',figures:[{option:'B',value:42.5},{option:'A',value:45}]}},
{text:'They cost the same for the trip',correct:false,claim:{winner:'equal',figures:[]}},
{text:'Metro Taxis costs £40',correct:false,claim:{winner:'B',figures:[{option:'B',value:40}]}}
],
explanation:'Airport Cars: £45. Metro Taxis: £2.50 + (25 × £1.60) = £2.50 + £40 = £42.50. Metro Taxis saves £2.50.'},

{id:'bv_gcse_025',level:'gcse',type:'direct',
criterion:'Kai wants the phone case for the least money.',measure:'total_cost',inputs:{A:{terms:[{name:'price',amount:8}]},B:{terms:[{name:'price',amount:5.5},{name:'delivery',amount:2.99}]}},
scenario:'Kai wants a phone case. A market stall sells it for collection. An online shop is cheaper but charges for delivery. Kai wants the phone case for the least money.',
optionA:{label:'Market stall',details:[{key:'Price',value:'£8'},{key:'Delivery',value:'N/A (collect)'}]},
optionB:{label:'Online shop',details:[{key:'Price',value:'£5.50'},{key:'Delivery',value:'£2.99'}]},
conclusions:[
{text:'The online shop is cheaper: £5.50 vs £8',correct:false,claim:{winner:'B',figures:[{option:'B',value:5.5,of:'amount:price'},{option:'A',value:8}]}},
{text:'The market stall is cheaper: £8 vs £8.49 for the online shop',correct:true,claim:{winner:'A',figures:[{option:'A',value:8},{option:'B',value:8.49}]}},
{text:'They cost the same once delivery is added',correct:false,claim:{winner:'equal',figures:[]}},
{text:'The online shop saves £2.50',correct:false,claim:{winner:'B',figures:[{option:null,value:2.5,of:'difference'}]}}
],
explanation:'Market stall: £8. Online shop: £5.50 + £2.99 = £8.49. The market stall is 49p cheaper.'},

{id:'bv_gcse_026',level:'gcse',type:'direct',
criterion:'Zoe wants her 10 journeys this week for the least money.',measure:'total_cost',inputs:{journeys:10,A:{terms:[{name:'per journey',amount:2,times:['journeys']}]},B:{terms:[{name:'weekly ticket',amount:18.5}]}},
scenario:'Zoe makes 10 journeys to college this week. She can pay for each bus journey or buy a weekly train ticket. Zoe wants her 10 journeys this week for the least money.',
optionA:{label:'Bus',details:[{key:'Per journey',value:'£2'}]},
optionB:{label:'Train',details:[{key:'Weekly ticket',value:'£18.50'}]},
conclusions:[
{text:'The bus is cheaper: £2 vs £18.50',correct:false,claim:{winner:'A',figures:[{option:'A',value:2,of:'amount:per journey'},{option:'B',value:18.5}]}},
{text:'The train is cheaper: £18.50 vs £20 for the bus',correct:true,claim:{winner:'B',figures:[{option:'B',value:18.5},{option:'A',value:20}]}},
{text:'They cost the same for 10 journeys',correct:false,claim:{winner:'equal',figures:[{option:null,value:10,of:'given'}]}},
{text:'The train saves £3.50',correct:false,claim:{winner:'B',figures:[{option:null,value:3.5,of:'difference'}]}}
],
explanation:'Bus: 10 × £2 = £20. Train: £18.50. The train saves £1.50.'},

// === Hidden Cost, more (5, added 16 Nov 2026) ===
{id:'bv_gcse_027',level:'gcse',type:'hidden',
criterion:'Sara wants the laptop with 2-year cover for the least money.',measure:'total_cost',inputs:{A:{terms:[{name:'laptop',amount:399}]},B:{terms:[{name:'laptop',amount:349},{name:'2-year cover',amount:59}]}},
scenario:'Store A sells a laptop for £399 with 2-year cover included. Store B sells the same laptop for £349, but 2-year cover costs £59 extra. Sara wants the laptop with 2-year cover for the least money.',
optionA:{label:'Store A',details:[{key:'Laptop',value:'£399'},{key:'2-year cover',value:'Included'}]},
optionB:{label:'Store B',details:[{key:'Laptop',value:'£349'},{key:'2-year cover',value:'£59'}]},
conclusions:[
{text:'Store B is cheaper: £349 vs £399',correct:false,claim:{winner:'B',figures:[{option:'B',value:349,of:'amount:laptop'},{option:'A',value:399}]}},
{text:'Store A is cheaper with cover: £399 vs £408 for Store B',correct:true,claim:{winner:'A',figures:[{option:'A',value:399},{option:'B',value:408}]}},
{text:'They cost the same with cover',correct:false,claim:{winner:'equal',figures:[]}},
{text:'Store B saves £50',correct:false,claim:{winner:'B',figures:[{option:null,value:50,of:'difference'}]}}
],
explanation:'Store A: £399, cover included. Store B: £349 + £59 = £408. Store A is £9 cheaper.'},

{id:'bv_gcse_028',level:'gcse',type:'hidden',
criterion:'Josh wants the ticket delivered for the least money.',measure:'total_cost',inputs:{A:{terms:[{name:'ticket',amount:120},{name:'booking fee',amount:12.5},{name:'delivery',amount:5}]},B:{terms:[{name:'ticket',amount:135}]}},
scenario:'Site A sells a festival ticket for £120, then adds a £12.50 booking fee and £5 delivery at the checkout. Site B sells it for £135 with fees and delivery included. Josh wants the ticket delivered for the least money.',
optionA:{label:'Site A',details:[{key:'Ticket',value:'£120'},{key:'Booking fee',value:'£12.50'},{key:'Delivery',value:'£5'}]},
optionB:{label:'Site B',details:[{key:'Ticket',value:'£135'},{key:'Fees and delivery',value:'Included'}]},
conclusions:[
{text:'Site A is cheaper: £120 vs £135',correct:false,claim:{winner:'A',figures:[{option:'A',value:120,of:'amount:ticket'},{option:'B',value:135}]}},
{text:'Site B is cheaper overall: £135 vs £137.50 for Site A',correct:true,claim:{winner:'B',figures:[{option:'B',value:135},{option:'A',value:137.5}]}},
{text:'They cost the same once fees are added',correct:false,claim:{winner:'equal',figures:[]}},
{text:'Site A saves £15',correct:false,claim:{winner:'A',figures:[{option:null,value:15,of:'difference'}]}}
],
explanation:'Site A: £120 + £12.50 + £5 = £137.50. Site B: £135. Site B is £2.50 cheaper.'},

{id:'bv_gcse_029',level:'gcse',type:'hidden',
criterion:'Priya wants the flight, a suitcase and a seat for the least money.',measure:'total_cost',inputs:{A:{terms:[{name:'flight',amount:39},{name:'suitcase',amount:25},{name:'seat',amount:8}]},B:{terms:[{name:'flight',amount:65}]}},
scenario:'Airline A advertises a flight for £39, but a suitcase costs £25 and choosing a seat costs £8. Airline B charges £65 with a suitcase and a seat included. Priya wants the flight, a suitcase and a seat for the least money.',
optionA:{label:'Airline A',details:[{key:'Flight',value:'£39'},{key:'Suitcase',value:'£25'},{key:'Seat',value:'£8'}]},
optionB:{label:'Airline B',details:[{key:'Flight',value:'£65'},{key:'Suitcase and seat',value:'Included'}]},
conclusions:[
{text:'Airline A is cheaper: £39 vs £65',correct:false,claim:{winner:'A',figures:[{option:'A',value:39,of:'amount:flight'},{option:'B',value:65}]}},
{text:'Airline B is cheaper overall: £65 vs £72 for Airline A',correct:true,claim:{winner:'B',figures:[{option:'B',value:65},{option:'A',value:72}]}},
{text:'They cost the same with a suitcase and a seat',correct:false,claim:{winner:'equal',figures:[]}},
{text:'Airline A saves £26',correct:false,claim:{winner:'A',figures:[{option:null,value:26,of:'difference'}]}}
],
explanation:'Airline A: £39 + £25 + £8 = £72. Airline B: £65. Airline B is £7 cheaper.'},

{id:'bv_gcse_030',level:'gcse',type:'hidden',
criterion:'Tom wants 6 months at a gym for the least money.',measure:'total_cost',inputs:{months:6,A:{terms:[{name:'monthly fee',amount:15,times:['months']},{name:'joining fee',amount:30}]},B:{terms:[{name:'monthly fee',amount:19,times:['months']}]}},
scenario:'Gym A costs £15 a month but charges a £30 joining fee. Gym B costs £19 a month with no joining fee. Tom wants 6 months at a gym for the least money.',
optionA:{label:'Gym A',details:[{key:'Monthly fee',value:'£15'},{key:'Joining fee',value:'£30'}]},
optionB:{label:'Gym B',details:[{key:'Monthly fee',value:'£19'},{key:'Joining fee',value:'None'}]},
conclusions:[
{text:'Gym A is cheaper: £15 vs £19 a month',correct:false,claim:{winner:'A',figures:[{option:'A',value:15,of:'amount:monthly fee'},{option:'B',value:19,of:'amount:monthly fee'}]}},
{text:'Gym B is cheaper over 6 months: £114 vs £120 for Gym A',correct:true,claim:{winner:'B',figures:[{option:'B',value:114},{option:'A',value:120},{option:null,value:6,of:'given'}]}},
{text:'They cost the same over 6 months',correct:false,claim:{winner:'equal',figures:[{option:null,value:6,of:'given'}]}},
{text:'Gym A saves £24',correct:false,claim:{winner:'A',figures:[{option:null,value:24,of:'difference'}]}}
],
explanation:'Gym A: 6 × £15 + £30 = £90 + £30 = £120. Gym B: 6 × £19 = £114. Gym B is £6 cheaper.'},

{id:'bv_gcse_031',level:'gcse',type:'hidden',
criterion:'Nina wants the phone on a 24-month contract for the least money.',measure:'total_cost',inputs:{months:24,A:{terms:[{name:'monthly cost',amount:20,times:['months']},{name:'upfront cost',amount:99}]},B:{terms:[{name:'monthly cost',amount:24,times:['months']}]}},
scenario:'Deal A costs £20 a month for 24 months, plus £99 upfront for the phone. Deal B costs £24 a month for 24 months with nothing upfront. Nina wants the phone on a 24-month contract for the least money.',
optionA:{label:'Deal A',details:[{key:'Monthly cost',value:'£20'},{key:'Upfront cost',value:'£99'}]},
optionB:{label:'Deal B',details:[{key:'Monthly cost',value:'£24'},{key:'Upfront cost',value:'None'}]},
conclusions:[
{text:'Deal A is cheaper: £20 vs £24 a month',correct:false,claim:{winner:'A',figures:[{option:'A',value:20,of:'amount:monthly cost'},{option:'B',value:24,of:'amount:monthly cost'}]}},
{text:'Deal B is cheaper overall: £576 vs £579 for Deal A',correct:true,claim:{winner:'B',figures:[{option:'B',value:576},{option:'A',value:579}]}},
{text:'They cost the same over the contract',correct:false,claim:{winner:'equal',figures:[]}},
{text:'Deal A saves £96',correct:false,claim:{winner:'A',figures:[{option:null,value:96,of:'difference'}]}}
],
explanation:'Deal A: 24 × £20 + £99 = £480 + £99 = £579. Deal B: 24 × £24 = £576. Deal B is £3 cheaper.'},

// === Rate Comparison, more (6, added 16 Nov 2026) ===
{id:'bv_gcse_032',level:'gcse',type:'rate',
criterion:'A shopper is choosing between them. Whichever box she buys, she will use all of it. She wants the most cereal for the money.',measure:'unit_cost',inputs:{A:{terms:[{name:'price',amount:2}],per:[0.5]},B:{terms:[{name:'price',amount:2.7}],per:[0.75]}},
scenario:'Two boxes of cereal. Box A: 500 g for £2.00. Box B: 750 g for £2.70. A shopper is choosing between them. Whichever box she buys, she will use all of it. She wants the most cereal for the money.',
optionA:{label:'Box A',details:[{key:'Weight',value:'500 g'},{key:'Price',value:'£2.00'}]},
optionB:{label:'Box B',details:[{key:'Weight',value:'750 g'},{key:'Price',value:'£2.70'}]},
conclusions:[
{text:'Box A is better value: £4.00/kg vs £3.60/kg for Box B',correct:false,claim:{winner:'A',figures:[{option:'A',value:4},{option:'B',value:3.6}]}},
{text:'Box B is better value: £3.60/kg vs £4.00/kg for Box A',correct:true,claim:{winner:'B',figures:[{option:'B',value:3.6},{option:'A',value:4}]}},
{text:'They cost the same per kg',correct:false,claim:{winner:'equal',figures:[]}},
{text:'Box A is better because it costs less',correct:false,claim:{winner:'A',figures:[]}}
],
explanation:'Box A: £2.00 ÷ 0.5 kg = £4.00/kg. Box B: £2.70 ÷ 0.75 kg = £3.60/kg.'},

{id:'bv_gcse_033',level:'gcse',type:'rate',
criterion:'A shopper is choosing between them. Whichever bottle she buys, she will use all of it. She wants the most juice for the money.',measure:'unit_cost',inputs:{A:{terms:[{name:'price',amount:1.2}],per:[1]},B:{terms:[{name:'price',amount:1.65}],per:[1.5]}},
scenario:'Two bottles of orange juice. Bottle A: 1 litre for £1.20. Bottle B: 1.5 litres for £1.65. A shopper is choosing between them. Whichever bottle she buys, she will use all of it. She wants the most juice for the money.',
optionA:{label:'Bottle A',details:[{key:'Volume',value:'1 litre'},{key:'Price',value:'£1.20'}]},
optionB:{label:'Bottle B',details:[{key:'Volume',value:'1.5 litres'},{key:'Price',value:'£1.65'}]},
conclusions:[
{text:'Bottle A is better value: £1.20 vs £1.65',correct:false,claim:{winner:'A',figures:[{option:'A',value:1.2,of:'total'},{option:'B',value:1.65,of:'total'}]}},
{text:'Bottle B is better value: £1.10 per litre vs £1.20 per litre for Bottle A',correct:true,claim:{winner:'B',figures:[{option:'B',value:1.1},{option:'A',value:1.2}]}},
{text:'They cost the same per litre',correct:false,claim:{winner:'equal',figures:[]}},
{text:'Bottle B costs £1.15 per litre',correct:false,claim:{winner:'B',figures:[{option:'B',value:1.15}]}}
],
explanation:'Bottle A: £1.20 ÷ 1 = £1.20 per litre. Bottle B: £1.65 ÷ 1.5 = £1.10 per litre.'},

{id:'bv_gcse_034',level:'gcse',type:'rate',
criterion:'Ollie wants the best pay for each hour worked.',measure:'hourly_rate',inputs:{A:{terms:[{name:'pay',amount:45}],per:[5]},B:{terms:[{name:'pay',amount:68}],per:[8]}},
scenario:'Two weekend jobs. Job A pays £45 for a 5-hour shift. Job B pays £68 for an 8-hour shift. Ollie wants the best pay for each hour worked.',
optionA:{label:'Job A',details:[{key:'Pay',value:'£45'},{key:'Hours',value:'5'}]},
optionB:{label:'Job B',details:[{key:'Pay',value:'£68'},{key:'Hours',value:'8'}]},
conclusions:[
{text:'Job A pays better per hour: £9/hour vs £8.50/hour for Job B',correct:true,claim:{winner:'A',figures:[{option:'A',value:9},{option:'B',value:8.5}]}},
{text:'Job B pays better per hour, because £68 is more than £45 for Job A',correct:false,claim:{winner:'B',figures:[{option:'B',value:68,of:'total'},{option:'A',value:45,of:'total'}]}},
{text:'They pay the same hourly rate',correct:false,claim:{winner:'equal',figures:[]}},
{text:'Job B pays £9.50/hour',correct:false,claim:{winner:'B',figures:[{option:'B',value:9.5}]}}
],
explanation:'Job A: £45 ÷ 5 = £9.00/hour. Job B: £68 ÷ 8 = £8.50/hour.'},

{id:'bv_gcse_035',level:'gcse',type:'rate',
criterion:'Amir will use all the data in whichever plan he picks. He wants the most data for the money.',measure:'unit_cost',inputs:{A:{terms:[{name:'price',amount:8}],per:[10]},B:{terms:[{name:'price',amount:15}],per:[25]}},
scenario:'Two monthly data plans. Plan A: 10 GB for £8. Plan B: 25 GB for £15. Amir will use all the data in whichever plan he picks. He wants the most data for the money.',
optionA:{label:'Plan A',details:[{key:'Data',value:'10 GB'},{key:'Price',value:'£8'}]},
optionB:{label:'Plan B',details:[{key:'Data',value:'25 GB'},{key:'Price',value:'£15'}]},
conclusions:[
{text:'Plan A is better value: £8 vs £15',correct:false,claim:{winner:'A',figures:[{option:'A',value:8,of:'total'},{option:'B',value:15,of:'total'}]}},
{text:'Plan B is better value: £0.60 per GB vs £0.80 per GB for Plan A',correct:true,claim:{winner:'B',figures:[{option:'B',value:0.6},{option:'A',value:0.8}]}},
{text:'They cost the same per GB',correct:false,claim:{winner:'equal',figures:[]}},
{text:'Plan A is better value: £0.80 per GB vs £0.60 per GB for Plan B',correct:false,claim:{winner:'A',figures:[{option:'A',value:0.8},{option:'B',value:0.6}]}}
],
explanation:'Plan A: £8 ÷ 10 = £0.80 per GB. Plan B: £15 ÷ 25 = £0.60 per GB.'},

{id:'bv_gcse_036',level:'gcse',type:'rate',
criterion:'A shopper is choosing between them. Whichever box she buys, she will use all of it. She wants the most eggs for the money.',measure:'unit_cost',inputs:{A:{terms:[{name:'price in pence',amount:150}],per:[6]},B:{terms:[{name:'price in pence',amount:330}],per:[15]}},
scenario:'Two boxes of eggs. Box A: 6 eggs for £1.50. Box B: 15 eggs for £3.30. A shopper is choosing between them. Whichever box she buys, she will use all of it. She wants the most eggs for the money.',
optionA:{label:'Box A',details:[{key:'Eggs',value:'6'},{key:'Price',value:'£1.50'}]},
optionB:{label:'Box B',details:[{key:'Eggs',value:'15'},{key:'Price',value:'£3.30'}]},
conclusions:[
{text:'Box A is better value: 25p per egg vs 22p per egg for Box B',correct:false,claim:{winner:'A',figures:[{option:'A',value:25},{option:'B',value:22}]}},
{text:'Box B is better value: 22p per egg vs 25p per egg for Box A',correct:true,claim:{winner:'B',figures:[{option:'B',value:22},{option:'A',value:25}]}},
{text:'They cost the same per egg',correct:false,claim:{winner:'equal',figures:[]}},
{text:'Box A is better because it costs less',correct:false,claim:{winner:'A',figures:[]}}
],
explanation:'Box A: £1.50 ÷ 6 = 25p per egg. Box B: £3.30 ÷ 15 = 22p per egg.'},

{id:'bv_gcse_037',level:'gcse',type:'rate',
criterion:'Lily wants the best pay for each hour worked.',measure:'hourly_rate',inputs:{A:{terms:[{name:'pay',amount:30}],per:[4]},B:{terms:[{name:'pay',amount:40}],per:[5]}},
scenario:'Two babysitting jobs. Family A pays £30 for 4 hours. Family B pays £40 for 5 hours. Lily wants the best pay for each hour worked.',
optionA:{label:'Family A',details:[{key:'Pay',value:'£30'},{key:'Hours',value:'4'}]},
optionB:{label:'Family B',details:[{key:'Pay',value:'£40'},{key:'Hours',value:'5'}]},
conclusions:[
{text:'Family A pays better per hour: £7.50/hour vs £8/hour',correct:false,claim:{winner:'A',figures:[{option:'A',value:7.5},{option:'B',value:8}]}},
{text:'Family B pays better per hour: £8/hour vs £7.50/hour for Family A',correct:true,claim:{winner:'B',figures:[{option:'B',value:8},{option:'A',value:7.5}]}},
{text:'They pay the same hourly rate',correct:false,claim:{winner:'equal',figures:[]}},
{text:'Family A pays better per hour, because the job is shorter',correct:false,claim:{winner:'A',figures:[]}}
],
explanation:'Family A: £30 ÷ 4 = £7.50/hour. Family B: £40 ÷ 5 = £8.00/hour.'},

// === Break-Even, more (3, added 16 Nov 2026) ===
{id:'bv_gcse_038',level:'gcse',type:'breakeven',
criterion:'How many films a month make the card worth it? (Worth it means cheaper, not the same price.)',measure:'crossover',inputs:{unit:'films',A:{fixed:20,per_unit:0},B:{fixed:0,per_unit:5}},
scenario:'A cinema card costs £20 a month for unlimited films. Without it, each film costs £5. How many films a month make the card worth it? (Worth it means cheaper, not the same price.)',
optionA:{label:'Cinema card',details:[{key:'Monthly cost',value:'£20'},{key:'Films',value:'Unlimited'}]},
optionB:{label:'Pay per film',details:[{key:'Per film',value:'£5'}]},
conclusions:[
{text:'The card is worth it if you see more than 4 films a month — from the 5th film onwards',correct:true,claim:{winner:'A',figures:[{option:null,value:5,of:'first'}],threshold:{value:4,from:'above',discrete:true}}},
{text:'The card is worth it if you see 3 or more films a month',correct:false,claim:{winner:'A',figures:[],threshold:{value:3,from:'at least',discrete:true}}},
{text:'Paying per film is always cheaper, however many films you see',correct:false,claim:{winner:'B',figures:[],threshold:{value:null}}},
{text:'The card is only worth it if you see 8 or more films a month, two a week',correct:false,claim:{winner:'A',figures:[],threshold:{value:8,from:'at least',discrete:true}}}
],
explanation:'£20 ÷ £5 = 4. After 4 films both cost £20, so the card is not yet cheaper. From the 5th film onwards the card is better value.'},

{id:'bv_gcse_039',level:'gcse',type:'breakeven',
criterion:'How many bus journeys must the bike replace to save money? (Saving money means cheaper, not the same price.)',measure:'crossover',inputs:{unit:'journeys',A:{fixed:180,per_unit:0},B:{fixed:0,per_unit:1.5}},
scenario:'A bike costs £180. Each bus journey costs £1.50. How many bus journeys must the bike replace to save money? (Saving money means cheaper, not the same price.)',
optionA:{label:'Bike',details:[{key:'Upfront cost',value:'£180'},{key:'Per journey',value:'£0'}]},
optionB:{label:'Bus',details:[{key:'Per journey',value:'£1.50'}]},
conclusions:[
{text:'The bike saves money after more than 120 journeys — from journey 121 onwards',correct:true,claim:{winner:'A',figures:[{option:null,value:121,of:'first'}],threshold:{value:120,from:'above',discrete:true}}},
{text:'The bike saves money from the 90th journey onwards',correct:false,claim:{winner:'A',figures:[],threshold:{value:90,from:'at least',discrete:true}}},
{text:'The bus is always cheaper, however many journeys you make',correct:false,claim:{winner:'B',figures:[],threshold:{value:null}}},
{text:'The bike saves money from the 12th journey onwards',correct:false,claim:{winner:'A',figures:[],threshold:{value:12,from:'at least',discrete:true}}}
],
explanation:'£180 ÷ £1.50 = 120. After 120 journeys both cost £180. From journey 121 onwards, the bike is cheaper.'},

{id:'bv_gcse_040',level:'gcse',type:'breakeven',
criterion:'How many pages make Printer B the cheaper choice? (Cheaper means cheaper, not the same price.)',measure:'crossover',inputs:{unit:'pages',A:{fixed:40,per_unit:0.05},B:{fixed:70,per_unit:0.02}},
scenario:'Printer A costs £40 and its ink costs 5p per page. Printer B costs £70 and its ink costs 2p per page. How many pages make Printer B the cheaper choice? (Cheaper means cheaper, not the same price.)',
optionA:{label:'Printer A',details:[{key:'Printer',value:'£40'},{key:'Ink',value:'5p per page'}]},
optionB:{label:'Printer B',details:[{key:'Printer',value:'£70'},{key:'Ink',value:'2p per page'}]},
conclusions:[
{text:'Printer B is cheaper for more than 1,000 pages — from page 1,001 onwards',correct:true,claim:{winner:'B',figures:[{option:null,value:1001,of:'first'}],threshold:{value:1000,from:'above',discrete:true}}},
{text:'Printer B is cheaper from 600 pages onwards',correct:false,claim:{winner:'B',figures:[],threshold:{value:600,from:'at least',discrete:true}}},
{text:'Printer A is always cheaper, because it costs less to buy',correct:false,claim:{winner:'A',figures:[],threshold:{value:null}}},
{text:'Printer B is always cheaper, because its ink costs less',correct:false,claim:{winner:'B',figures:[],threshold:{value:null}}}
],
explanation:'Printer B costs £30 more to buy and saves 3p per page. £30 ÷ £0.03 = 1,000 pages. At 1,000 pages both cost £90. From page 1,001 onwards, Printer B is cheaper.'}

2. scripts/verify-better-value.py:
   a. :46 COUNTS = {'gcse': 40, 'core': 50}; the docstring's "(70 items: gcse 20, core 50)" (:5) becomes "(90 items: gcse 40, core 50)".
   b. REVIEW: insert these twenty lines directly after the bv_gcse_020 line (:86), verbatim:
    r('bv_gcse_021', [8*6], [48-40], 'monthly membership is cheaper', 'lt'),
    r('bv_gcse_022', [10*30], [300-270], 'Instructor B is cheaper', 'lt'),
    r('bv_gcse_023', [2*(35+F('4.5')), 2*38], [35+F('4.5'), 79-76], 'Site B is cheaper', 'lt'),
    r('bv_gcse_024', [F('2.5')+25*F('1.6')], [25*F('1.6'), 45-(F('2.5')+25*F('1.6'))], 'Metro Taxis is cheaper', 'lt'),
    r('bv_gcse_025', [F('5.5')+F('2.99')], [F('5.5')+F('2.99')-8], 'market stall is cheaper', 'lt'),
    r('bv_gcse_026', [10*2], [20-F('18.5')], 'train is cheaper', 'lt'),
    r('bv_gcse_027', [349+59], [349+59-399], 'Store A is cheaper with cover', 'lt'),
    r('bv_gcse_028', [120+F('12.5')+5], [120+F('12.5')+5-135], 'Site B is cheaper overall', 'lt'),
    r('bv_gcse_029', [39+25+8], [39+25+8-65], 'Airline B is cheaper overall', 'lt'),
    r('bv_gcse_030', [6*15+30, 6*19], [6*15, 6*15+30-6*19], 'Gym B is cheaper over 6 months', 'lt'),
    r('bv_gcse_031', [24*20+99, 24*24], [24*20, 24*20+99-24*24], 'Deal B is cheaper overall', 'lt'),
    r('bv_gcse_032', [2/F('0.5'), F('2.7')/F('0.75')], [F('0.5'), F('0.75')], 'Box B is better value', 'lt'),
    r('bv_gcse_033', [F('1.65')/F('1.5')], [F('1.2')], 'Bottle B is better value', 'lt'),
    r('bv_gcse_034', [45/5, 68/8], [], 'Job A pays better per hour', 'gt'),
    r('bv_gcse_035', [15/25, 8/10], [], 'Plan B is better value', 'lt'),
    r('bv_gcse_036', [F('1.5')/6, F('3.3')/15], [], 'Box B is better value', 'lt'),
    r('bv_gcse_037', [40/5, 30/4], [], 'Family B pays better per hour', 'gt'),
    r('bv_gcse_038', [20/5], [], 'worth it if you see more than 4'),
    r('bv_gcse_039', [180/F('1.5')], [121], 'saves money after more than 120 journeys'),
    r('bv_gcse_040', [(70-40)/(F('0.05')-F('0.02'))], [70-40, F('0.05')-F('0.02'), 40+1000*F('0.05'), 1001], 'Printer B is cheaper for more than 1,000 pages'),
   c. BREAK_EVEN (:238): add 'bv_gcse_038': F(20, 5), after the bv_gcse_019 entry.
   d. MUST_SAY: after ('bv_gcse_020', 'scenario', 'cheaper, not the same price'), add the same tuple for bv_gcse_038, bv_gcse_039 and bv_gcse_040.
   Project Claude ran both verifiers with exactly this page and these verifier changes: verify-better-value-claims.py "better-value claims: 90 items, 360 conclusions; 0 known failure(s)" ... "PASS"; verify-better-value.py "better-value: 90 items, every keyed and explanation figure recomputed, every card clicked in Chromium" ... "PASS", every self-test caught; check-banks --only better-value: B1-B11 all 0 (B4 0); verify-better-value-tax.py PASS; check-tax-year.py OK.
3. data/check-ledger.json: remove the B4 entry "better-value::gcse" the way the repo removes a fixed entry (python -X utf8 scripts/extract-banks.py, then python -X utf8 scripts/check-banks.py --write-ledger --only better-value); that entry is the only ledger change.
4. /updates/: one line in the site's plain wording: "Better Value: twenty more GCSE questions, including hidden fees, price per kilogram and break-even points."
5. docs/handover/cloud.md: an entry for this PR, ending with the rows for the home lane: close todo LEDGER-B4-BETTER-VALUE; the roster row (.claude/rules/game-roster.md, Better Value) says "50 questions" and should say GCSE 40, Core 50 (a home-lane edit).

DO NOT TOUCH: bv_gcse_001-020 and every Core item; the twenty new items' text, numbers, claims and explanations (if any fails a check, STOP; do not edit it); every function in the page; both verifiers beyond the four data edits in 2; the roster; schools/assets/; docs/todo.md; canon; Gate files; every other game.

SUCCESS CONDITION: Better Value GCSE has 40 items, the twenty above verbatim; verify-better-value-claims.py and verify-better-value.py both PASS with their self-tests; check-banks passes B4 for better-value at both levels and the ledger's better-value::gcse entry is gone; /updates/ has the line; merged by merge-pr.py; main's check-site and phone-fit-full green on the merge commit and reported with their IDs; cloud.md updated and the work committed.

STOP IF: either verifier or check-banks fails on any of the twenty items (report the item and the failure; change nothing in it); any self-test stops catching its planted fault; the Gate fails for any other reason (report the step and its error before changing anything); merge-pr.py cannot reach GitHub; main's run on the merge commit does not start.
