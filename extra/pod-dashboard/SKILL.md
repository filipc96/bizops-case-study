---
name: pod-dashboard
description: Builds the pod recap dashboard (extra/pod-dashboard/dashboard.html) from calls.csv for a date range, using B1's own maths, checks it against scripts/b1_metrics.py, comments on the data in chat, then opens the page. Use when the user asks for the pod dashboard or for recap numbers by pod over a period.
argument-hint: "[from YYYY-MM-DD] [to YYYY-MM-DD] [minutes]"
---

# Pod dashboard for a date range

Arguments, in order: from date, to date, threshold in minutes (optional, default 60). No dates means the whole log.

`dashboard.py` is the only thing that writes `dashboard.html`. Each run rebuilds the page for the dates given, with the same layout every time; no dates gives the whole log.

## Steps
1. **Dates.** Use YYYY-MM-DD as given. If a date is written another way ("21 Sep", "last week"), read it against `brain/NOW.md` (now = the week of 21 Sep 2026), not the system clock, and say how you read it in the commentary's first bullet. One date only: from = to. From after to: stop and ask.
2. **Run.** From the repo root: `python3 extra/pod-dashboard/dashboard.py [minutes] --from FROM --to TO` (no `--from`/`--to` for the whole log). It prints everything on the page as text: the per-pod table, recorded calls with no recap, on-time recaps still needed for 80%, capture × speed, agent vs AM medians, weekly share, platforms (calls by platform, each pod's mix, recorded/recapped by platform) and the `adoption.csv` comparison.
3. **Check.** Run this with the same arguments; no output means the tables match:
   `diff <(python3 extra/pod-dashboard/dashboard.py ARGS | sed -n '/^pod /,/^All /p;/^All /q') <(python3 scripts/b1_metrics.py ARGS | sed -n '/^pod /,/^All /p;/^All /q')`
   Any difference: stop and report it.
4. **Commentary.** Before opening the page, write a short commentary in chat (about 5–8 bullets), using only numbers from the printout:
   - Headline: the dates, the number of calls, and each pod's share against 80%, with the on-time recaps it still needs.
   - What holds each pod below target back: capture (calls not recorded) or speed (recaps late), and agent vs AM speed from the medians.
   - The trend in the weekly share; for a date range, how the starred weeks compare with the rest. Flag weeks with few calls instead of reading much into them.
   - Platforms: which platform each pod uses most, and which platforms go unrecorded or without a recap.
   - Recorded calls with no recap, by call id.
   - Whole log only: any pod where `adoption.csv` differs from `calls.csv`.
   Talk about pods, not people: no opinions about anyone (`brain/SANITIZER.md`). Mark an inference as one. Cite any file you add context from (e.g. `brain/NOW.md`).
5. **Open.** `open extra/pod-dashboard/dashboard.html`

## Reply
The commentary is the reply. After opening the page, add at most one line, e.g. "Opened `extra/pod-dashboard/dashboard.html` (whole log, 140 calls; table matches B1)." No checklist, no recap of the steps, no list of what you did or didn't change. Only if the check fails or the script errors, say that instead.

## Never
- Edit `dashboard.html` or `dashboard.py`. If the page looks wrong, report it; don't patch it.
- Edit `scripts/b1_metrics.py`, `calls.csv` or `adoption.csv`.
- Copy a number from the page onto a brain page: brain pages link the sheet (`brain/RESOLVER.md:29`).
