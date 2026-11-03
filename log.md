**Time:** ~ human hours · ~Y AI hours
**Sessions:** <start>–<stop> · …
**Skipped:** none / <list>

**First instruction I gave the AI:**

> Before we touch any task, I want to understand the client. Read everything in brain/,
> slack-thread.txt, adoption.csv and calls.csv. Don't write files or solve anything yet.
> Brief me on Brightline the way you'd brief a new hire, in under a page:
>
> 1. What Brightline does, and how its brain and recap agent work.
> 2. The four pods: lead, current focus, and their number on the dashboard.
> 3. The two accounts: what they sell, who the contacts are, current focus, history so far,
>    and open threads.
> 4. What's going on this week.
> 5. What the brain doesn't tell us that you'd want to know.
>    Cite the file for every fact. Describe, don't diagnose: no judgments on the numbers or
>    the recaps yet.

**B**
- Wrote `scripts/b1_metrics.py` (standard library only, threshold argument, default 60) to recompute each pod's number from `calls.csv`.
- Checked the script's output against a separate one-off calculation; all counts matched.
- Compared with `adoption.csv`: counts match, but the dashboard shows East at 75% instead of 70% (that cell divides by recorded, not held).
- Reran at 15–90 min: no recap lands at 60–64 min, so the cutoff doesn't change results; South reaches 82% at 90 min.
- Split median minutes by who posted (agent 56–74, AM 18) and East before/after 15 Sep (50% → 93%).
- AI proposed two extra numbers and picked agent on-time rate; I chose capture × speed instead.
- B1: wrote the ranking table, the mismatch line and the capture × speed table into `b-answers.md`.
- B2: picked South (speed 39%) over West (capture 13%) and rejected Priya's emailed-summaries proposal.
- B2 first came out at 241 words; AI cut it to 200 after checking the word count.
- Reverted B2 so B1 would come first, then re-added it under B1.
