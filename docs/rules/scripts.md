# Scripts, verifiers and CI

Python must be at least 3.10 (`write_text`'s `newline=`); CI pins 3.12, enforced by `scripts/check-python-version.py`. The general invocation and pre-push rule live in AGENTS.md.

Local check planning uses two queues: heavy checks (CI time at least 60 seconds or internally concurrent browser work) run one at a time; six light checks may run beside them. Never run heavy checks together. Reason: canon §12, RULEBOOK.

Heavy checks reached only through shared files are deferred to CI and listed with the selecting file. CI's Gate still requires them; `--all-heavy` runs them locally and `--full` selects the whole local suite. SR-27 in canon specifies the verifier-only alternative checks.

Every PR runs the site-wide checks; main, weekly and manual full runs execute all verifiers. CI selection, timings, budgets, median recording and sharding are documented in canon §7.8.1. New limits warn until main meets them; use canon §7.8.4 for gate work and its worst-case test.

Groups estimated over 80% of budget fail a PR selecting their lines; over 100% fails everywhere. Main's 80–100% band warns. Passing 75% of timeout on one run warns; hard timeouts guard hangs. Persistent verifier slowdown is reported, not failed (canon §7.8.1).

The PR measured-budget check also judges grown or renamed verifiers from that PR's measured times; no hand timing before merge is needed. Long verifiers declare `# ci-shards` work units using `bc.Shard`; `ci-groups.py` chooses the parts. Never split one by hand.

Timings use the last five main runs' medians; the timings job writes only a pack passing `ci-groups.py --check`. A verifier declares its own CI lines/dependencies rather than changing the workflow or generated pack/timings files; follow canon §7.8.2 for the header syntax.

Pin tracked byte-compared paths in `.gitattributes` with `-text` or `eol=lf`; hashes and sizes must not depend on checkout line endings. Existing paths include `scripts/fonts/**`, CLAUDE.md, both handovers and todo.md. History: canon §12, RULEBOOK.

Planted-fault verifiers use `scripts/plant_common.py` (canon §7.9); older ones migrate when next edited, tracked in `docs/handover/stale-plants.md`. Read marks from page feedback, never a wrapped `mfg`. Report whether mathematical verification independently computes answers.

Answer-counts slots (05:40/11:40/17:40 UTC) may start 2–6 hours late or be skipped by GitHub throttling. Jon accepted that on 28 Oct; do not chase the minute. Fetch retries are 1/5/15 minutes. Incident detail: canon §12, RULEBOOK.
