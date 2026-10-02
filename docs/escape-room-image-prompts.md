# Escape-room image prompts — the record

> ## ⚠ Superseded for new art — 2026-09-08
>
> **The style below is the old one, and the six-picture model is dropped.** New art is drawn to a
> different brief: **three pictures a room** — scene, failure, victory — hand-inked with visible
> uneven linework, muted, and **empty of people and of lettering**, which is where the old
> generation kept failing. Instrument art is gone; the engine draws the live control. The current
> style block and judging rules are in `docs/escape-room-voice-rewrite.md` §6, and every image goes
> through `scripts/strip-gen-watermark.py` before filing.
>
> **Seven rooms are on the new brief** — `hamster-heist`, `pe-shed-rebellion`, `prom-budget`,
> `canteen-hack`, `heatwave-mutiny` (13/09), `rugby-mud` (15/09) and the new `comic-caper` (17/09). The
> other two still carry the old art and are being redone alongside that room's voice rewrite. **The H (Heatwave) section further
> down is the OLD six-picture record** — the current pictures are in the section immediately below.
>
> This file is kept because the *lessons* still hold — blank labels, counting the controls against
> the lock, reroll compositions but inpaint words, and watching what a texture word turns into. The
> prompts themselves are now history.

## Kiln Disaster — the three, 2026-09-17

All three from one viewpoint of the same art room, filed through `strip-gen-watermark.py --frame 1600x873`
(JPG downloads, no watermark found in any of the three).

**Scene — re-rolled once, for palette.** The first take came back warm: cream walls, warm light, a rust-streaked
kiln. The failure and victory pictures of the same room came back cool grey. Laid side by side they read as two
different rooms at two different times of day, which is exactly what the judging rule about "the same hand" is
for. The re-roll kept the composition and moved the palette to the cool grey of the other two. **The warm take
was filed first and overwritten**, so the lesson is the order: generate the three, lay them together, and only
then file.

**A difference left standing:** the cool scene has no loose paper on the floor; fail and win both show sheets
near the portfolio stack. Nothing in the room's text depends on a sheet being on the floor at the start.

**Fail — first take.** The floor under foam, the emergency stop pushed in, the portfolios soaked. It shows the
suppression system already fired, so it is **only** true at time-out — this room must never set `missArt`.

**Win — first take.** The kiln open and cold, the controller dark, the portfolios dry.

**Accepted flaw:** in fail and win, the frayed strap ends on the portfolio stack splay into shapes that read as
fingers at thumbnail size. They are straps. The scene does not have it.

## Comic Caper — the three, 2026-09-17

All three share one viewpoint of the same classroom, filed through `strip-gen-watermark.py --frame 1600x873`
(JPG downloads, no watermark found). Alts approved by Jon.

**Scene — rerolled once.** The first take lettered the leaflet on the teacher's desk "TRAVEL BROCHURE" and
drew a tall wardrobe that hid the clock wall, which the win picture contradicts. The reroll attached the
**fail picture** as the reference and wrote every rule into the prompt: add the cupboard where the pale
rectangle is, top below the clock, doors shut, a round dial on each door, a brass slider bar across both,
a blank riveted plate and a blank sticker, a folded leaflet with a completely blank cover, and no text,
lettering, numbers or logos anywhere. It came back clean. **Accepted flaw:** the clock is centred above the
cupboard here and above-right in fail and win, and reads just after twelve here and just before in both.

**Fail — first take.** The cupboard gone, a pale unfaded rectangle and a line of dust where it stood. It
shows the cupboard already taken, so it is **only** true at time-out — this room must never set `missArt`.

**Win — first take.** The cupboard open and bare, the comics poking out of bags on the chairs, warm light.
The comic covers are plain diagonal colour bands, no lettering. Differences from the scene (a shorter
cupboard, no brass slider, loose chains on the dials) do not contradict any text.

## Rugby Mud Bath — the new three, 2026-09-15

**Win — filed, an EDIT of `Rugby Open.jpg`.** The establishing shot from the batch of eight showed a
pitch already churned to mud from a changing-room doorway: the ending, not the beginning, so it
became the victory picture. **Its boots carried three diagonal stripes** — a brand mark, caught on
filing. Edit prompt: keep everything exactly as it is, make the boots plain with no stripes, logos or
markings. Came back with nothing else moved. **Every later rugby prompt attaches this edited version,
not the original.**

**Fail — filed, an edit of the cleaned win.** Came back clean first time, boots spotless white. Same camera, doorway, door and bench; the pitch
turned perfect: mown in pale and dark stripes, rolled flat, bone dry, crisp lines, clear blue sky,
the same boots clean. "Almost too tidy — like a lawn, not a sports pitch." Negative: people,
players, text, lettering, numbers, signage, logos, stripes on boots, mud, puddles, rain, photoreal.
Fail and win are a matched pair from one camera, like prom-budget's.

**Scene — filed, new image, edited win attached as style reference only.** Came back softer and
warmer than the doorway pair, and the zoom check found scribbled pseudo-characters on the timer face;
left on Jon's call because the timer is ~25px wide at 1600px. The gate board, catalogue and envelope
label were clean. The side of Mower's
wooden hut at the pitch edge on a bright dry late-summer afternoon: window onto a counter with an
open seed catalogue; a torn padded envelope on the step; two brass taps on a pipe in a padlocked
wire-mesh cage; a cheap plastic timer on one tap; two flat hoses across a gravel path, one split; a
painted gate with a BLANK board; the pitch perfect and striped beyond, posts at the far end, corner
flag upright. Negative adds `sprinkler` — the P.E. store room already owns the sprinkler.
**Zoom-check** the catalogue pages, timer face, padlock and gate board for lettering before filing.

```
python scripts/strip-gen-watermark.py --width 1600 --frame 1600x873 "<edited win>.jpg" docs/art/rugby-mud-win.webp
python scripts/strip-gen-watermark.py --width 1600 --frame 1600x873 "<failure>.jpg"    docs/art/rugby-mud-fail.webp
python scripts/strip-gen-watermark.py --width 1600 --frame 1600x873 "<scene>.jpg"      docs/art/rugby-mud-scene.webp
```

## Heatwave Mutiny — the new three, filed 2026-09-13

**Scene — an EDIT, not a new image.** `heatwave open.jpg` from the batch of eight showed a classroom
with no air conditioning, and the rewritten room is about turning it back on. Rather than reroll, the
JPG was attached with an edit prompt: "keep everything exactly as it is, add only two plain white
wall-mounted air-conditioning units, louvres shut, unbranded, no display screens". It came back with
everything else untouched. **Order mattered:** the failure and victory prompts attach the *edited*
scene, so the units match across all three.

**Failure** — the same classroom, same camera, days later: units still dead, orange glare through the
blinds, empty bottles, curled exercise books, a wilted plant. **Victory** — same camera, units running
with drawn streams of cold air, the room shifted to cool blues while outside stays hot yellow, a
water bottle beaded with condensation. `snow, ice, frost` went in the victory negative because "cold
air" drifts towards a winter scene.

**Both came back with the chairs still UP on the desks**, though both prompts asked for them down.
**The prose moved to the pictures, not the reverse** ("Nobody has even taken the chairs down yet"):
the three share one camera and read as a matched set, and a reroll to fix a detail would likely have
broken that.

All four downloads were JPGs, 2816x1536, no watermark; filed with `--width 1600` alone:

```
python scripts/strip-gen-watermark.py --width 1600 "<scene edit>.jpg" docs/art/heatwave-mutiny-scene.webp
python scripts/strip-gen-watermark.py --width 1600 "<failure>.jpg"    docs/art/heatwave-mutiny-fail.webp
python scripts/strip-gen-watermark.py --width 1600 "<victory>.jpg"    docs/art/heatwave-mutiny-win.webp
```

**A fourth picture was drawn and then NOT filed.** A canteen-freezer meltdown for the wire lock's
misconception, which would have needed a per-lock misconception picture in the engine. Review dropped
the freezer failure altogether, so the picture was deleted and the engine work cancelled. It is worth
knowing it came back well — and that its electrical box carried a small hazard pictogram with a stick
figure, which a zoom check caught and the no-signage rule would have rejected.

**Zoom-check the spots lettering hides in** before filing: air-con badges and display windows, book
pages, appliance control panels, box covers. A 1400px-wide crop sheet of those regions took one look.

## P.E. Store Rebellion — the new three, filed 2026-09-08

The first room drawn to the three-picture brief after `hamster-heist`. Prompts and the exact filing
commands, because the crops are not obvious and will be needed again.

**Scene** — `PE Store Open.jpg` from the batch of eight establishing shots. Clean, and 2816x1536,
which is the house ratio already:

```
python scripts/strip-gen-watermark.py --width 1600 "PE Store Open.jpg" docs/art/pe-shed-rebellion-scene.webp
```

**Failure** — the store after the run: every scrap of kit soaked and mud-caked on the floor, and the
waxed coat on its hook by the door, dry and immaculate, the only clean thing in the room.

**Victory** — the sports hall: the arena up and the blower still running, balls scattered, and
through the high windows the rain falling on an empty field. Kettle steaming on a bench with the
abandoned cross-country bib, which pays off the locker's "twelve dodgeballs and, inexplicably, a
kettle".

Both came back **2752x1536** — a different aspect from the scene's 2816x1536, which silently filed
them 1600x893, twenty pixels taller than every other image on the site. Both also carried the
sparkle, and **the detector missed both**: it needs the whole star to survive thresholding and these
were too soft, scoring k4=0.19 against a required 0.85. Do not fix that by loosening the thresholds —
that is how the first version flagged 30 of 53 clean images.

Inpainting made it worse. One mark sat against the door frame, the other on a court-line vertex, and
the fill interpolates across the patch, so both came out as visible pale smudges. `--at` and
`--clone` exist now for marks that *are* on plain ground; these were not. **They were framed out
instead**, and the two crops differ because the strips differ:

```
python scripts/strip-gen-watermark.py --crop 489,0,2752,1235 --frame 1600x873 in.png docs/art/pe-shed-rebellion-fail.webp
python scripts/strip-gen-watermark.py --crop 0,184,2478,1536 --frame 1600x873 in.png docs/art/pe-shed-rebellion-win.webp
```

The mark sits about 10% in from the right and 19% up from the bottom, so a crop that clears it costs
one or the other. **Look at the strip before choosing a side.** On the failure picture the right-hand
strip is the coat the whole picture is about, so it lost its floor and its left edge instead; on the
victory picture the right-hand strip is only wall bars, so it lost that and its ceiling. Neither
needed a stretch in the end — both landed on the house ratio by crop alone.

## Prom Budget Embezzlement — the new three, filed 2026-09-08

All three done in one session. The interesting one is the failure/victory pair: same camera, same
watermark position, **one shared crop**.

**Scene — FILED.** `Prom Open.jpg` from the batch of eight. Clean (JPG downloads carry no sparkle)
and already 2816x1536:

```
python scripts/strip-gen-watermark.py --width 1600 "<Downloads>/Prom Open.jpg" docs/art/prom-budget-scene.webp
```

Came back 1600x873 on the width alone, no crop needed. It is a cramped finance office at night: one
lit desk lamp, a beige CRT, filing cabinets with a drawer hanging open, papers over the desk and the
floor, a cash box, a mug, a dark window. No lettering anywhere, which is the new style working.

**Failure — FILED.** The prom you get when the money stayed spent. The sports hall under harsh
strip lighting with nobody in it: bare walls, roof trusses and ductwork, one paper garland on the
wall bars, a trestle table with a closed laptop and a single bowl of crisps, and in the middle of
the empty parquet a life-sized bronze statue of a smiling man in a suit on a low wooden plinth.

**Victory — FILED.** The same hall, lights down: a mirrorball hung from the trusses and turning,
throwing coloured spots over walls, floor and ceiling, a bar of blue, amber and purple stage lamps
behind it, fairy lights and garlands along the wall bars, a trestle table with a laptop between two
speakers and an ice bucket. In the middle of the floor, a low plinth with nothing on it — that
empty plinth is the whole point of the picture and pays off the last line of `win`.

**Both came back 2816x1536, the house aspect, and both carried the sparkle in the SAME PLACE**
— source (2580, 1298), about 8% in from the right and 15% up from the bottom — **and the detector
missed both again**, exactly as on the P.E. pair. In both it sits directly on a painted court line,
which is the case interpolation smears, so neither was inpainted.

**They were framed out on one shared crop, which is new.** The two pictures are the same hall from
the same camera, so a single crop clears the mark in both and keeps them looking like a matched
pair — the P.E. failure and victory needed different crops and are subtly different framings as a
result. The crop keeps the ceiling in both, because the strip lights are the point of one and the
mirrorball is the point of the other, and pays for it out of the foreground floor and the
right-hand strip:

```
python scripts/strip-gen-watermark.py --crop 0,0,2500,1364 --frame 1600x873 "Gemini_Generated_Image_7714jb7714jb7714.png" docs/art/prom-budget-fail.webp
python scripts/strip-gen-watermark.py --crop 0,0,2500,1364 --frame 1600x873 "Gemini_Generated_Image_lyx8wxlyx8wxlyx8.png" docs/art/prom-budget-win.webp
```

2500x1364 is 1.8328 against the house 1.8327, so `--frame` does almost nothing and nothing is
stretched. The crop tightened both compositions rather than costing them anything — the statue and
the plinth both sit more centrally for it.

**The statue generated first time.** The "public figures" refusal recorded below did not fire,
because nothing in the prompt named a role: it was described as a bronze statue of a smiling man in
a suit, and that is all it needed to be.

**Two lines of prose moved to match the pictures, not the other way round.** The mirrorball came
back hung and turning rather than sitting unhung on the floor, and the failure table came back with
no speaker on it. Both alts and both prose lines were rewritten to what is on disk — and the
mirrorball fix also settled a contradiction already sitting inside `win`, which said somebody had
finally worked out the stepladder three paragraphs before saying nobody managed to hang the ball.

**The statue is the known refusal trigger.** See "If a model refuses on public figures" below: a
sculpture of a person in a named role reads as a monument to somebody real. Describe it as a bronze
statue of an invented cartoon man in a suit, never as a headteacher, and generate from text with no
reference image attached if it still refuses.

**Both are empty rooms, and the failure's statue is the only figure-shaped thing in either.** The
style block forbids people; a bronze on a plinth is not a person and is the subject of the picture,
but it is the part most likely to come back wrong. Judge it hard, and reroll rather than inpaint —
five attempts to remove a figure from the canteen all failed.

**Expect the sparkle and expect the detector to miss it**, exactly as on both P.E. pictures. Look at
the bottom-right corner yourself before filing. Plain ground takes `--at X,Y`; an edge or a line does
not, because the fill smears — frame it out with `--crop` and choose the side by what the picture can
afford to lose. Pass `--frame 1600x873` every time; the generator does not return a consistent
aspect.

**No year on the bunting.** The prom bunting has come back reading PROM 2024 before.

---

**The queue is empty.** All fifty-three images are filed in `docs/art/`: five cast sheets, and six
apiece for rooms C to J — an establishing shot, three instruments, a failure picture and a victory
picture. Nothing is outstanding for a built room.

Winning used to pay off in prose over the **establishing shot** — the room as you found it, not the
room you had just fixed — because the victory pictures did not exist. All eight were drawn on
2026-09-01 and that is over. The engine shows `<room>-win.webp` only where `room.js` defines a
`winAlt`, so the picture and its alt text arrive together and `check-escape-rooms.py` enforces the
pairing; a room with neither still falls back cleanly, which is how they went up before they were
drawn.

This file is now the record of how each picture was made and what went wrong on the way. **Read the
style line in "How to run one" before generating anything** — it is the single thing that decides
whether a picture comes back in the house style, and the four checks below it are what a picture has
to pass before it is filed.

## What is left

Nothing for rooms C to J. Rooms **A and B** have never been prompted, and need their maths repaired
first — see the note at the foot of this file.

## Where each room is

| Room | State |
|---|---|
| **C** — The P.E. Shed Rebellion — KS3 | **6 of 6 — complete.** `pe-shed-rebellion-win` filed 2026-09-01 |
| **D** — The Prom Budget Embezzlement — GCSE | **3 of 3 on the new brief — complete.** All three refiled 2026-09-08; fail and win share one crop |
| **E** — The Great Hamster Heist — KS3 | **6 of 6 — complete.** `hamster-heist-win` filed 2026-09-01 on the third attempt |
| **F** — The Rugby Mud Sabotage — GCSE | **6 of 6 — complete.** `rugby-mud-win` filed 2026-09-01 |
| **G** — The IT Teacher's Vengeance — GCSE Higher | **6 of 6 — complete.** `it-vengeance-win` filed 2026-09-01 |
| **H** — The Heatwave Mutiny — KS3 / GCSE | **6 of 6 — complete.** `heatwave-mutiny-win` filed 2026-09-01 |
| **I** — The Canteen Menu Hack — KS3 / GCSE | **6 of 6 — complete.** `canteen-hack-win` filed 2026-09-01, with one flaw: see below |
| **J** — The Headteacher's Car Trap — GCSE / Core Maths | **6 of 6 — complete.** `car-trap-win` filed 2026-09-01 on the rewritten prompt |

Each room needs six: an establishing shot, three instruments, a failure picture and a victory
picture. All six are done for every room C to J.

## How to run one

1. **Attach `docs/art/heatwave-mutiny-fail.webp`** as a style reference, every time — **and open
   the prompt with the style line**, because the attachment on its own does not hold it:

   > Flat-shaded cartoon illustration, clean dark linework, warm muted palette, soft even shading,
   > in the style of the attached reference. No photographic texture.

   with `photograph, photorealistic, 3D render, CGI, depth of field, bokeh, film grain` at the
   front of the negative.
2. **Attach the room's own scene** for its instruments, and the **cast sheet** named in the block.
3. **Paste the prompt, then the negative** below it.
4. **Save WebP quality 80** — 1600px wide for scenes and failures, 1200+ for instruments. Generate
   at 2048 where the tool offers it: the panel-border crop eats about 8%.

Round gauge came back with a painted needle? Don't reroll:
`python scripts/strip-dial-needle.py in.jpg docs/art/out.webp`.

## Four checks before filing

1. **Nothing legible on a puzzle surface.** Gauge faces, keypads, sticky notes, clipboards, chart
   axes: blank. The clue text is HTML so the Aa toggle and screen readers can reach it. Sign-writing
   in a scene or failure is welcome — put what it says in the `alt`.
2. **The art contains the housing, and only the housing.** The empty slot, the bare face, the pivot
   boss — never the needle, handle or marker, and never the instrument at its answer.
3. **British, not American.** Caretaker not janitor, football not soccer, tea not coffee.
4. **No year anywhere**, and no brand marks. This material gets reused next September.

The school is **St Martha's Secondary** throughout.

---

# E. The Great Hamster Heist — KS3

# C. The P.E. Shed Rebellion — KS3

### `pe-shed-rebellion-win` — **filed 2026-09-01, replaced same day**

The first take was fine; the replacement is better — a fuller hall, badminton posts either side of
the arena, wall bars and a mat trolley behind, and a proper blower rather than a desk fan. It is
also unmistakably the same hall as room D's prom, which the first pair were not.

**It carries a lettered `whirrr` beside the blower** — the only sound-effect lettering anywhere in
the set, and against this prompt's own "no readable text". It was kept: it is small, it is in the
alt text, and it does no harm. Worth knowing it is there before adding more of them.

Flat-shaded cartoon illustration, clean dark linework, warm muted palette, soft even shading, in
the style of the attached reference. No photographic texture.

A school sports hall with an inflatable dodgeball arena fully up, filling the floor between the
badminton posts, its walls taut and its inflator still running. Twenty-odd students in P.E. kit are
inside it and around it, mid-game, throwing soft balls at each other and laughing. Through the high
windows it is grey and hammering with rain. Warm indoor light, wooden floor, wall bars, a folded
cross-country running bib abandoned on a bench in the foreground.

**Negative:** photograph, photorealistic, 3D render, CGI, depth of field, bokeh, film grain. No
teacher, no brand marks, no year, no readable text, no American signage, nobody outdoors.

# D. The Prom Budget Embezzlement — GCSE

### `prom-budget-win` — **filed 2026-09-01, replaced same day**

The replacement moves the prom into the school hall proper — wall bars, basketball hoop and stacked
mats still round the edges under the bunting — where the first take could have been any village
hall. Same room as C's sports hall, which is the point. The empty plinth, the tablecloth, the bowl
of crisps and the mirrorball on the floor by the stepladder all survived the reroll.

Flat-shaded cartoon illustration, clean dark linework, warm muted palette, soft even shading, in
the style of the attached reference. No photographic texture.

A school hall mid-prom, properly decorated at last: bunting up, coloured lights, a big speaker stack
either side of a small stage, students in prom clothes actually dancing. A mirrorball sits on the
floor near a stepladder, still waiting to be hung, and the light catches it anyway. On the plinth in
the middle of the floor, where the bronze statue was going to stand, is an empty plinth with a
tablecloth thrown over it and a bowl of crisps on top. Warm party lighting, streamers, motion.

**Negative:** photograph, photorealistic, 3D render, CGI, depth of field, bokeh, film grain. No
statue or bust anywhere, no teacher, no brand marks, no year, no readable text, no American signage.

# E. The Great Hamster Heist — KS3

### `hamster-heist-win` — **filed 2026-09-01, on the third attempt**

The hardest of the eight, and the two failures are the useful part. Attempt one: a modern grey
plant room with a live hamster eating in the cage. Attempt two: the right room and the right toy,
then invented lettering on every plate in it. Attempt three, with both fixes written into the
prompt below, landed — blank plates, the newspaper back to its own headline, and a plush hamster
sitting very still under the lamp.

**Attach `hamster-heist-scene.webp` as well as the style reference** — this is the same bench from
almost the same angle, and it is the one room where a palette drift shows. The first attempt came
back in a modern grey-and-steel plant room and had to be dropped.

Flat-shaded cartoon illustration, clean dark linework, warm muted palette, soft even shading, in
the style of the attached reference. No photographic texture.

The same warm boiler room as the attached scene — brass and copper pipework, ochre walls, a caged
bulb — and the same wooden workbench. The elaborate hamster cage is closed and lit by its heat lamp,
the exercise wheel is turning steadily with a belt running off it to a small dynamo, and the feeder
hopper is full. Inside the cage, propped upright beside a full food bowl, is a **plush toy hamster**:
plump, pristine, stitched, sitting just slightly too still and too neat to be alive. On the floor
beside the bench a grey school backpack is unzipped just enough to show the real hamster fast asleep
in a nest of sock. Warm lamp glow, copper everywhere.

Every label plate, wall notice and gauge face in the room is blank — empty cream rectangles, exactly
as in the attached scene. The only lettering anywhere in the picture is the newspaper masthead on
the bench.

**Negative:** photograph, photorealistic, 3D render, CGI, depth of field, bokeh, film grain. No live
or animate hamster inside the cage, no hamster eating or holding food in the cage, no grey or steel
pipework, no lettering on the gauge panel, no labelled gauges, no wall notices with words, no
invented sign text, no words anywhere except the newspaper masthead, no people, no brand marks, no
year, no American signage.

**Why the toy matters:** the heist is that Pythagoras leaves in the backpack and the instruments go
on believing a hamster is in there. A live hamster in the cage means no heist happened, and the
caretaker's line about it never having looked healthier stops being a joke.

**Say the labels are blank, in the prompt itself.** Attempt two got the room and the toy right and
then wrote on everything: five invented plates on the gauge panel (MUDDLED MESS, DRAMATIC
PRESSURE, STALEMATE twice, GENTLEMEN'S AGREEMENT) and a nonsense notice on the wall. The scene
leaves every one of those blank, and rule 1 says gauge faces stay blank. The four-checks list is
not enough on its own — the generator only honours it if the prompt repeats it. So the prompt now
carries this line, and the negative names it:

> Every label plate, wall notice and gauge face in the room is blank — empty cream rectangles,
> exactly as in the attached scene. The only lettering anywhere in the picture is the newspaper
> masthead on the bench.

and in the negative: `no lettering on the gauge panel, no labelled gauges, no wall notices with
words, no invented sign text, no words anywhere except the newspaper masthead`.

# F. The Rugby Mud Sabotage — GCSE

### `rugby-mud-win` — **filed 2026-09-01**

Landed first time on this prompt. One thing the prompt never asked for and the picture therefore
has not got: the H posts. It reads as a ruined field rather than unmistakably a ruined *rugby*
field. Not worth a reroll on its own — add "rugby posts on the far touchline" if it is ever redone.

Flat-shaded cartoon illustration, clean dark linework, warm muted palette, soft even shading, in
the style of the attached reference. No photographic texture.

A school rugby pitch that has been comprehensively ruined: the near half is standing water and
churned mud, the far half is going the same way, the try line barely visible. A minibus is parked
at the touchline with its doors open and a team in immaculate away kit standing beside it, one of
them looking down at his spotless boots. The electronic scoreboard on its post shows two lit score
panels. Flat grey afternoon light, sheeting water, one gull.

**Negative:** photograph, photorealistic, 3D render, CGI, depth of field, bokeh, film grain. No
readable numbers on the scoreboard, no brand marks, no year, no readable text, no American signage,
nobody being mocked by name.

# G. The IT Teacher's Vengeance — GCSE Higher

### `it-vengeance-win` — **filed 2026-09-01**

Landed first time and matched the closing line exactly — the arms hanging at his sides in the
doorway. The vaulter came back male, so the win line's "meet her at the top of her flight" was
changed to "him" to match the picture.

Flat-shaded cartoon illustration, clean dark linework, warm muted palette, soft even shading, in
the style of the attached reference. No photographic texture.

A school gym hall at dusk with the lights on. Blue landing mats are unfolded flat and true across
the floor in a neat tiled rectangle, a vaulting horse stands at the right height with a student in
P.E. kit clearing it mid-flight, and the AV cabinet at the side is closed and quiet with its lights
green. In the open doorway a middle-aged man in a shirt and lanyard watches with his arms hanging at
his sides rather than folded. Warm light, dust in the air, music implied by everyone moving.

**Negative:** photograph, photorealistic, 3D render, CGI, depth of field, bokeh, film grain. No
brand marks, no year, no readable text, no American signage, no student being humiliated.

# H. The Heatwave Mutiny — KS3 / GCSE

### `heatwave-mutiny-win` — **filed 2026-09-01**

Landed first time on this prompt. Rendered a shade softer than the flat-shaded reference — more
gradient in the walls, lighter linework — but it is never seen beside the failure picture, so it
was filed as it came.

Flat-shaded cartoon illustration, clean dark linework, warm muted palette, soft even shading, in
the style of the attached reference. No photographic texture.

A school classroom in a heatwave with the air conditioning finally on: cold air visibly falling from
the ceiling vents in pale streams, papers lifting at the corners, students sitting up with their
eyes shut and their faces tipped towards it, one with arms spread. Through the open door, the
corridor freezer cabinet stands closed and humming, packed with ice lollies. Bright hot light
outside the windows, cool blue tint inside.

**Negative:** photograph, photorealistic, 3D render, CGI, depth of field, bokeh, film grain. No
melted ice cream, no teacher, no brand marks, no year, no readable text, no American signage.

# I. The Canteen Menu Hack — KS3 / GCSE

### `canteen-hack-win` — **filed 2026-09-01, with one flaw**

The receipt coiled on the floor and the rewritten PIZZA board are exactly right, and the two servery
staff are not the catering manager — she is older, grey, in a floral apron, and stays out of the
win. **But the queue is in polo shirts and shorts and reads primary-age**, where the failure picture
puts the same queue in blazers and ties. Nobody sees both endings in one play, so it was filed. If
it is ever redone, add: "students in secondary uniform — blazers and ties, ages 11 to 16, as in the
failure picture".

Flat-shaded cartoon illustration, clean dark linework, warm muted palette, soft even shading, in
the style of the attached reference. No photographic texture.

A school canteen servery restored: the kale trays are gone and in their place, under the heat lamps,
are wide steel trays of pizza being slid into position. The smart till is printing a receipt long
enough to have reached the floor and coiled there. Behind the counter the chalkboard has been wiped
and rewritten to read PIZZA. A queue of students is arriving fast and cheerfully. Warm lamp light,
steam, the shutter now fully up.

**Negative:** photograph, photorealistic, 3D render, CGI, depth of field, bokeh, film grain. No
kale anywhere, no prices visible, no catering manager, no brand marks, no year, no readable text
beyond the word PIZZA on the board, no American signage.

# J. The Headteacher's Car Trap — GCSE / Core Maths

### `car-trap-win` — rewritten and **filed 2026-09-01**

**No wing-mirror instruction.** The first prompt asked for both mirrors folded in and the generator
could not do it — repeatedly. It never needed them: the mirror joke is a line of prose, the beat is
the barrier, and at this scale a folded mirror is a few pixels. The camera is behind the car, where
the mirrors are not the subject. Do not put "folded mirrors" in the negative either; naming them
brings them back. The prose only ever folded **one** mirror anyway.

The comedy is carried instead by geometry, which the generator renders reliably: a bay plainly
shorter than the car, tyre scuffs from the earlier attempts, the barrier down close enough to touch
the boot, and the charging post's red light.

Flat-shaded cartoon illustration, clean dark linework, warm muted palette, soft even shading, in
the style of the attached reference. No photographic texture.

An underground school car park, seen from behind the car and slightly above. A bright orange
electric sports car is halfway through reversing into a comically undersized visitor bay by the lift
doors, well out of square, one front wheel still across the painted line, its reversing lights on.
The bay is a small white box painted on the wet concrete with VISITOR stencilled inside it, plainly
shorter than the car. Curved black tyre scuffs on the wet floor record three earlier attempts. The
yellow line-painting robot is parked beside its work with its roller down. An electric charging post
stands beside the bay, its cable coiled on its hook and a small red light showing. The barrier arm
is down immediately behind the car, close enough to almost touch the boot. A dozen staff in coats
have stopped on their way to the lift to watch, several with the particular blank expression of
people not laughing. Cold strip lighting, wet concrete, puddles.

**Negative:** photograph, photorealistic, 3D render, CGI, depth of field, bokeh, film grain. No
number plate, no badges on the car, no driver visible through the glass, no students, no brand
marks, no year, no readable text beyond VISITOR painted in the bay, no American signage.

# Appendix

## Art already filed — all 53 in `docs/art/`

| File | Note |
|---|---|
| `cast-caretaker.webp` | Room E's scene and failure |
| `cast-pe-teacher.webp` | Room C's failure |
| `cast-geography-teacher.webp` | Room F's scene and failure; third pose is already the ruined patch |
| `cast-headteacher.webp` | Room D's failure; includes the bronze statue in the matching pose, plaque blank |
| `cast-it-teacher.webp` | Room G's scene and failure |
| `pe-shed-rebellion-scene.webp` | Room C establishing. FOOTBALL and MUD RULES! fixed by inpaint |
| `pe-shed-dodgeball-pressure-boyle.webp` | Room C. Needle removed with `strip-dial-needle.py` |
| `pe-shed-locker-nth-term.webp` | Room C. Reroll: dial centred and larger, clipboard clean white. 943px — under the 1200 target, acceptable for a close-up |
| `pe-shed-sprinkler-sector-area.webp` | Room C. Reroll landed clean: bare arc, pivot boss, no pointer |
| `pe-shed-rebellion-fail.webp` | Room C failure. Every beat landed first time; umbrella came back rainbow rather than navy, which is funnier |
| `prom-finance-reverse-percentage.webp` | Room D. Blank keys and blank display; the paper is headed INVOICE, which is decoration and stays |
| `prom-wifi-venn-router.webp` | Room D. Two glowing rings, bare pivot boss, no pointer. Best instrument shot in the set |
| `prom-budget-fail.webp` | Room D failure. Year and brand mark both inpainted out in one pass |
| `hamster-feeder-bounds.webp` | Room E. Empty release slot present. Hopper came back a box rather than a triangular prism — still a prism, and the clue only fixes its cross-section |
| `hamster-heist-scene.webp` | Room E establishing. Text pass done: school corrected, five labels blanked, newspaper kept |
| `hamster-wheel-rpm.webp` | Room E. Belt, dynamo and an empty slider slot, clean first time. Cage wall reads as mesh rather than glass — fine for a close-up from inside |
| `prom-budget-scene.webp` | Room D establishing. Only lettering in the frame is the hall sign — the blanking clause worked first time |
| `prom-dj-deposit-compound.webp` | Room D. Empty brass track, no lever, passbook and desk bell. Clean first time |
| `hamster-heat-lamp-gradient.webp` | Room E. Empty slider slot, and the pinned chart has axes but **no plotted line** — the gradient stays unsolved |
| `hamster-heist-fail.webp` | Room E failure. Done: both beats land, crest gone, six labels blanked |
| `rugby-mud-scene.webp` | Room F establishing. Big sign blanked; one small fence sign behind the posts is still garbled |
| `rugby-mud-fail.webp` | Room F failure. **Two signs to fix:** CHANGING ROOMS ROOMS and PIT BOUNDARY. LOST LEFT SHOES stays |
| `rugby-scoreboard-bases.webp` | Room F. Two blank digit windows and two slotted knobs — the slot is the index, so the live control rotates the whole knob |
| `rugby-elbow-patch-scale.webp` | Room F. Patch, split hose, offcuts and chalk; cutter dial is a blank knurled disc with no pointer |
| `it-vengeance-scene.webp` | Room G establishing. Only lettering is the honours board, spelt correctly. Cleanest scene yet |
| `rugby-sprinkler-flow-rates.webp` | Room F. Two brass handwheels, bare timer face, pivot boss, drip caught mid-fall. Clean |
| `it-vengeance-fail.webp` | Room G failure. Generated without a refusal. Two grinning bearded men rather than one — the doorway is the IT teacher, the other reads as someone filming it |
| `heatwave-mutiny-scene.webp` | Room H establishing. Every word spelt right, including CONTROL ROOM down the corridor and four exercise books |
| `heatwave-patrol-lcm-timer.webp` | Room H. Blank grey LCD, three sashed prefects out of focus behind it, heat shimmer |
| `heatwave-cube-surface-volume.webp` | Room H. Reroll: twelve blank keys in four rows of three, everything else unchanged |
| `heatwave-canteen-freezer-inequality.webp` | Room H. Blank tuner face and pivot boss, blank tag on every wire, one sparking. Clean |
| `it-vault-trajectory-vertex.webp` | Room G. Powder inpainted out, chalk arc and rig untouched |
| `it-mat-tiling-hcf.webp` | Room G. Second version kept: tiled floor makes the tiling visible, and the offcuts show what "nothing cut" means |
| `it-mechanical-keyboard-perms.webp` | Room G. Four blank keycaps, cyan under-glow, bare dial with a centre boss. The last one |
| `heatwave-mutiny-fail.webp` | Room H failure, and the house style reference |
| `canteen-hack-scene.webp` | Room I establishing. Rerolled in style 2026-08-31 and clean first time: HEALTHY WEEK unobstructed, COOKIE £5 legible, till screen and laminated notice both blank |
| `canteen-mean-calories.webp` | Room I. Rerolled in style. Bare slider track with graduations and no handle, blank screen carrying only the kcal label — the instrument the lock actually needs |
| `canteen-cookie-price-simultaneous.webp` | Room I. Two blank tags reading COOKIE and PIZZA, two bare knurled dials with no index mark, and a receipt whose writing is scribble. Clean first time |
| `canteen-kale-fraction-drain.webp` | Room I. Chute hatch, bare round dial, blank display window, a stack of empty gastronorm trays. Clean first time |
| `canteen-hack-fail.webp` | Room I failure. Rerolled in style, and both notes from the photoreal attempt landed: the manager stands clear of the board so HEALTHY WEEK reads in full, and every student is holding a tray with one portion of kale on it |
| `car-trap-scene.webp` | Room J establishing. Clean first time. RESERVED on the folding stand and VISITOR worn into the floor by the lift are the only lettering, and both earn their place — the second is the bay he ends up in |
| `carpark-visitor-space-bounds.webp` | Room J. Panel hinged open, blank readout labelled litres, plain round knob with no pointer. The knob reads as housing rather than as a needle, which is the safe shape |
| `carpark-boom-gate-sector.webp` | Room J. The textbook version of the safe dial: bare face, tick graduations, centre pivot boss, no needle at all. Coiled wiring behind it and the barrier arm in frame |
| `carpark-ev-charger-quadratic.webp` | Room J. Blank display with a small A, a bare knurled setting ring, a blank label taped inside the open cover. Green standby glow does the lighting |
| `car-trap-fail.webp` | Room J failure, and the set's last image. Blank number plate, no badges, rain, the minibus out on the verge through the ramp opening, staff filing past without looking. Nobody under eighteen in the frame |

| `pe-shed-rebellion-win.webp` | Room C victory. Second take: badminton posts either side of the arena, wall bars and a mat trolley behind, a proper blower. Carries a lettered `whirrr` — the only sound-effect lettering in the set, kept deliberately |
| `prom-budget-win.webp` | Room D victory. Second take: the prom moved into the school hall proper, wall bars and basketball hoop under the bunting, so it is visibly the same building as C. Empty plinth, tablecloth, crisps, mirrorball still on the floor |
| `hamster-heist-win.webp` | Room E victory. **Third attempt** — see the prompt for the two failures. Copper boiler room matching the scene, blank plates throughout, a plush toy sitting very still in the cage while the real hamster sleeps in the backpack |
| `rugby-mud-win.webp` | Room F victory. Clean first time. No rugby posts in frame, which the prompt never asked for — add them if it is ever redone |
| `it-vengeance-win.webp` | Room G victory. Clean first time, and it matched the closing line exactly: the arms hanging at his sides in the doorway. The vaulter came back male, so the win prose now says "him" |
| `heatwave-mutiny-win.webp` | Room H victory. Clean first time. Renders a shade softer than the house style — more gradient, lighter linework — and was filed as it came |
| `canteen-hack-win.webp` | Room I victory. Clean first time; the receipt coiled on the floor is the best thing in it. **The queue is in polos and shorts and reads primary-age** where the failure picture has blazers and ties. Filed anyway: no play shows both endings |
| `car-trap-win.webp` | Room J victory. Second take, on a prompt rewritten to stop asking for folded wing mirrors. VISITOR in the bay is the only lettering, and it is the space he is reversing into |

## Alt text written so far

Every scene and failure needs one — they carry sign-writing and the joke often lives in it.

**The eight `-win` alts are not repeated here.** They live in each room's `room.js` as `winAlt`,
which is the authoritative copy and the thing the engine actually reads — a victory picture is
shown only where its room defines one, and `check-escape-rooms.py` enforces the pairing.

- `canteen-hack-scene` — "A school canteen servery a few minutes before lunch, the shutter half
  up. A chalkboard behind the counter reads HEALTHY WEEK, steel trays of baked kale sit under the
  heat lamps, and a laminated notice hangs by the hatch. On the counter a smart till stands with its
  administrator screen open, next to a small sign reading COOKIE £5. An apron hangs on a hook by the
  door and a clipboard rests on the cold store handle."
- `canteen-hack-fail` — "A school canteen at lunchtime under Healthy Week. A long queue of students
  in uniform stretches away from the counter and is not moving, and every tray in the frame holds a
  single portion of dark baked kale and nothing else. In the foreground one chocolate cookie sits
  alone on a doily under a glass dome, with a handwritten £5 card propped in front of it. Beside the
  HEALTHY WEEK chalkboard the catering manager stands in a hairnet and floral apron, arms folded,
  beaming with pride at the queue."
- `heatwave-mutiny-fail` — "A school canteen in chaos. A chest freezer stands open with a rainbow
  river of melted ice cream spreading across the floor, lolly sticks stranded in it. Students sob,
  sweat and fan themselves at the tables. A notice on the freezer reads 'freezer turned off by
  students (their own fault!)' and the menu board reads: chicken (hot!), ice cream = gone."
- `pe-shed-rebellion-scene` — "A rusting P.E. store shed on a rain-lashed school field, door open on
  a warm-lit heap of cones, kit bags and ball nets. A sprinkler arcs water across the grass toward
  the St Martha's Secondary School sports hall. Two students hurry past under an umbrella. Graffiti
  on the shed reads MUD RULES!"
- `hamster-heist-scene` — "A school boiler room of copper pipes and pressure gauges. On a workbench
  stands an elaborate hamster cage with a running wheel, a food hopper and a heat lamp over it, a
  mug of tea beside it. A hamster peers out of a school backpack badged St Martha's Secondary. A
  newspaper on the bench reads: Local Gazette — unsettling hamster plots reported."
- `heatwave-mutiny-scene` — "A sweltering classroom with sunlight striping through half-closed blinds. Students sweat over their desks, fanning themselves with exercise books marked St Martha's Secondary, a dead fan sits on a cupboard beside a wilting plant, and a wall thermometer is pushed to the top. Through the doorway a prefect patrols a corridor towards a door marked CONTROL ROOM."
- `it-vengeance-scene` — "A school gym hall at dusk, lit blue through high windows. Wall bars, climbing ropes, a vaulting horse and a stack of blue mats. On the near wall a locked AV cabinet glows, with an elaborate mechanical keyboard wired into it spilling cyan light across the floor. A wooden board on the right reads St Martha's Secondary Honours Board."
- `it-vengeance-fail` — "A school gym hall where an enormous concertinaed heap of blue mats fills the middle of the floor. A gymnastics team carries on performing around it while everyone watching clamps their hands over their ears, two huge speakers blasting at either side. A man stands in the doorway with his arms folded, delighted."
- `hamster-heist-fail` — "A school caretaker with a grey moustache fills a boiler-room doorway, holding up a stitched toy hamster with mismatched button eyes by one ear and looking distinctly unimpressed. Three horrified students stand in a drift of spilt food pellets that has buried the floor. Behind them the real hamster runs in its wheel under a blazing red heat lamp."
- `rugby-mud-scene` — "A pristine rugby pitch at sunset with white lines and posts. An open sprinkler control cabinet stands on a post beside a split hose spraying water into a muddy patch. A tweed jacket with leather elbow patches hangs on a fence post, and a St Martha's Secondary minibus is arriving at the far gate."
- `prom-budget-scene` — "A cramped school finance office at night, lit by one desk lamp. Papers, ring binders and filing cabinets everywhere, a dying spider plant on top, an old beige computer on the desk and a small bronze bust of a smiling man in a suit. Through the open door a hall is half decorated with bunting, a stepladder and a disco ball on the floor, under a sign reading St Martha's Secondary."
- `prom-budget-fail` — "A school prom in a sports hall under harsh strip lighting. A life-sized
  bronze statue of a grinning man in a suit stands on a plinth in the middle of the dance floor,
  with students in prom clothes standing awkwardly around it. One boy in a blue suit dances anyway.
  A laptop and two speakers sit on a trestle table beside one bowl of crisps. Bunting reads PROM."
- `pe-shed-rebellion-fail` — "A whole class trudges a cross-country course through mud and driving
  rain in soaked PE kit, one carrying a lost shoe, another wringing out a sock, three huddled
  together. Their P.E. teacher stands dry under a huge rainbow umbrella with a flask, delighted,
  while a sprinkler soaks the pile of kit bags beside him." 

Name the distinctive thing in words, not just in the reference image — it works. The heat lamp
came back on the same cage as the scene, having been told so in the prompt. Room E's cage is a
glass-walled box with a brass frame and copper pipework; a close-up generated cold will draw a
generic wire cage instead, and attaching the scene is not reliably enough to stop it — a reference
steers palette and light far better than it steers objects.

**The blanking clause reduces invented signage but does not stop it.** Both scenes since it was added still produced garbled signs — RUCKUS RUGBY: NO SLIPPING ALLOWED (ILNESSS HUMOROUS) on the rugby pitch, six labels in the hamster reroll. Budget a text pass on every dense scene rather than hoping.

**Dense scenes invent signage, and garble it.** The hamster boiler room came back with five made-up
labels — MUDDLED MESS, GENTLEMEN'S AGREEMENT, a school name that was not ours. Scene prompts now
end by naming which signs may carry lettering and blanking the rest. Cheaper than a text pass over
a picture you otherwise like.

**Dated text ages the art.** The prom bunting came back reading PROM 2024. Nothing in these rooms
should carry a year — the material is meant to be reusable next September and the one after.

**Watch for brand marks.** A laptop arrived with an apple-shaped mark on the lid despite `corporate
logo` in the negative. Inpaint it flat.

**If a model refuses on "public figures", it is the statue.** A sculpture or portrait of a person
in a named role reads as a monument to somebody real, and an attached character sheet pushes it
further that way. Say *invented cartoon character, not a real person* in the prompt, describe the
sculpture by what it looks like rather than by the job title, and if it still refuses, generate
from text with no reference image attached.

## Notes worth keeping

**Watch what a texture word turns into.** "Chalk dust on the floor" in a dark gym came back as heaps of white powder with footprints trodden through them. Nothing in the prompt was wrong; the picture was unusable. Scan each finished image for what it accidentally depicts, not only for what was asked.

**Count the controls against the lock, not just their kind.** "Four-digit keypad" produced a pad with four buttons; the code is 3375, so it needs ten. Same class of error as the feeder that came back with no slider at all — the art has to be the housing the *specific* control mounts into, so check the number of keys, dials and tracks against the lock's INSTRUMENT line.

**Two shapes of instrument are safe, and both turned up by luck rather than by prompt.** A rotating dial with no index mark (`locker-nth-term`), and a knob whose own slot or notch is the index (`rugby-scoreboard-bases`) — in both, the live control can rotate the whole drawn part, so there is nothing to conflict with. Ask for one of those wherever a lock needs a dial.

**Naming the style in the prompt is not optional.** Three of room I's pictures were generated with
`heatwave-mutiny-fail.webp` attached as a style reference and came back photoreal anyway — good
pictures, wrong set. An attached image steers composition and mood; it does not hold the rendering
style. Put the style in words at the top of the prompt and the photographic terms in the negative.

**Order per room:** establishing shot first, then instruments with that scene attached as a second
reference, then the failure. Instruments generated cold drift away from the room they belong to.

**Reroll compositions, inpaint words.** The shed's SOCCER and MID RULES! were fixed in one pass with
nothing else moving. Five attempts to remove a *figure* from the canteen all failed. Flat lettering
yes, people no.

**A matched pair from one camera can share one crop, and should.** The prom failure and victory
are the same hall from the same viewpoint, and the sparkle landed on the identical pixel in both.
One crop cleared both and kept the two framings identical, which matters because a player sees them
as alternatives to each other. Check whether a room's two outcome pictures share a camera before
choosing crops separately.

**Panel borders and painted needles are scripted fixes, not rerolls.** `strip-dial-needle.py` does
both for round gauges.

**Failure pictures fire at the misconception.** Each lock names the specific wrong value a student
is most likely to reach — show the picture on *that* value, not on any wrong answer, and the
mistake gets named while it is still funny.

**A victory picture is not optional after all.** The end card showed the *establishing shot* on a
win — the room as you found it, before you fixed anything — under prose describing everything you
changed. The picture quietly contradicted the text. All eight `-win` pictures are filed. The engine shows one only where the room defines a `winAlt`, so the two
arrive together and the alt text always describes what is actually on screen.

**Still to prompt:** rooms A and B, once their rejected locks are repaired.