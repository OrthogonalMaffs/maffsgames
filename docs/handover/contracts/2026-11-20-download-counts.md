DOWNLOAD-COUNTS, one part.
LANE: home. Send now. TIER: Small. MODEL: Claude Code, Sonnet 5.5, medium effort.

TASK: Every download link on the site reports to the Events sheet through the existing section-click listener, with its own action "download", and a CI check keeps every future download link labelled (Jon, 20 Nov 2026).

ROOT CAUSE: On main 2e7c9d2: schools/assets/analytics.js:230-258 sends section_clicked for any [data-mfg-item] inside a [data-mfg-section], but only GA4's automatic file_download sees the five downloads on core-maths/counting-players/index.html:105-109 (no labels), and the CSV buttons on ugh-stats/flu-and-answers/index.html:86 and ugh-stats/one-class/index.html:114 (no labels). GA4's count is blocked by ad-blockers and many school networks. printables/index.html:283 is labelled but reports a download as "open-link", the same as any link.

CLASS CHECK: A class: any download link not labelled is invisible to the sheet, on any page. The fix is at the shared layer: the one listener tells a download from a link, and a CI check fails any unlabelled download link, so no page can miss it again. Labelling the four pages is the migration.

EXACT CHANGE:
1. First commit: close out COUNTING-PLAYERS (#855, merge 2e7c9d2): MERGED line and main's runs on the merge commit from the API into its home.md entry; contract to docs/history/contracts/; its todo row per TODO-TRIM if any part is finished. Save this contract verbatim as docs/handover/contracts/2026-11-20-download-counts.md.
2. analytics.js listener: an <a> with a download attribute gets action "download" (filter_value "v1|pos=N;action=download"); every other case unchanged. Update the comment above it and canon's section_clicked row (docs/canon.md:256) to name the action.
3. Labels. core-maths/counting-players/index.html: the downloads list gets data-mfg-section="counting-players"; items pdf-preliminary-material, pdf-practice-paper, pdf-mark-scheme, csv-site-data, csv-game-records. ugh-stats/flu-and-answers and ugh-stats/one-class: the CSV link's nearest container gets data-mfg-section="ugh-stats-flu-and-answers" / "ugh-stats-one-class" and the link data-mfg-item="csv-data". printables/index.html unchanged (already labelled). Any other non-game page the check finds: label it on the same pattern and report it under "Decided for you".
4. scripts/check-download-labels.py, in CI: every <a> with a download attribute in every served .html has data-mfg-item and sits inside a data-mfg-section. Plant that must FAIL: one label removed.
5. scripts/test-section-clicks.py: also loads core-maths/counting-players/ and printables/ and proves each download link fires exactly one section_clicked with action download and the right item, and an ordinary link still fires open-link.
6. privacy/index.html:151: "we log anonymous gameplay events to our own secure database" becomes "we log anonymous gameplay events, and which features and downloads are used, to our own secure database". Nothing else on the page changes.
7. home.md entry. No /updates/ line.
8. PR, Gate and phone-fit-full green, merge with python -X utf8 scripts/merge-pr.py <n> --watch --wait 3600; report its last line.

DO NOT TOUCH: the Sheet's columns and the Apps Script; any other event or its fields; game_card_clicked and the fact_* events; the pages' look and wording apart from the attributes; the Counting Players PDFs and CSVs; games; canon beyond the one row.

SUCCESS CONDITION: a click on any of the eight download links (five, two, one) posts one section_clicked with action download and its item; the check in CI with its plant failing; test-section-clicks.py covers downloads; the privacy sentence updated; COUNTING-PLAYERS closed out; merged GREEN; home.md records it.

STOP IF: the listener change alters the payload of any non-download click; a game page has a download link (report it; label nothing in games); merge-pr.py can't reach GitHub; anything in docs/history/contracts/2026-10-27-standing-stop-rules.md applies (report under "Decided for you").
END OF CONTRACT
