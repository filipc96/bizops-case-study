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
- B3: wrote `plan.md` for South, week of 28 Sep ("by Friday" = Fri 2 Oct, since the log ends 24 Sep), from `b-answers.md`, the Slack thread, `NOW.md` and `fde-ticket.md`.
- B3: message to Marcus quotes his "if it posted in 10-15 min I'd use it" and asks one change: paste his summary into the client's Slack channel within the hour.
- B3: handled Priya's proposal as a pushback: the number counts posted recaps (`NOW.md:10`), to confirm with Priya on Monday.
- B3: baseline is 40% for the week of 21 Sep and 35% month to date; the two recorded K&C calls with no recap are the two `inbox/` calls.
- B3: expected 70% by Friday (range 55–85%): 90% ceiling, pod posts on 6 of 9 recorded calls, agent adds about 1; engineering fix not counted.
- B3: AI cited `b-answers.md` for the AM median, which isn't in it; caught on a recheck of every cited line and changed to `calls.csv`.
- B3: the week-of-21-Sep numbers came from a one-off calculation, not the script; came out when AI said the date filter "wasn't built yet".
- Added `--from`/`--to` to `scripts/b1_metrics.py`: default output unchanged, South's weekly 20/50/33/40% reproduced, dashboard check skipped on filtered runs.
- Pointed `plan.md` sections 4 and 5 at the filtered script commands.

**C**
- C1: compared `bad-recap.md` with its transcript, RESOLVER, SANITIZER, the accounts sheet and the 10 Sep Loop Athletic recap.
- C1: listed 6 problems by severity, each with evidence and the rule it breaks, in `c1-bad-recap-review.md`.
- C1: traced each problem to the line of the old `skill-recap.md` that caused it.
- C2: rewrote `skill-recap.md` from the C1 review: numbered workflow, RESOLVER template, privacy rules, self-check loop, two examples.
- C2: diffed the skill's template against `RESOLVER.md:42-61` to confirm it's an exact copy.
- C2: first draft was 62 lines; trimmed to 60 to meet the limit.
- C2: took the action-item example from Kettle & Crumb, not the Loop Athletic test call; the held-back flag example is generic wording.
- C2: AI said both examples came from Kettle & Crumb. The flag example is generic, fits the Loop case exactly, and run 1 copied it word for word. I caught it reviewing `c2-before-after.md`; fixed the output (that file and this log), not the instruction.
- C2: mapped each C1 problem to the skill lines that now prevent it.
- C2: set `updated:` to 2026-09-21, not the system date, per `CLAUDE.md` (to confirm).
- C2: reran the skill in a fresh session in `~/c2-test`, which held only the skill, the brain at b57ee9a and the transcript (no `CLAUDE.md`, no C1 notes).
- C2: AI checked the test inputs against the repo: identical skill and transcript, unchanged brain except for the new recap.
- C2 run 1 (Loop, 15 Sep): all 6 C1 problems fixed. DM reduced to one Flags line, GMV flagged without the figure, brief owned and dated 2026-09-18, size chart moved to Open questions, 10 Sep meeting linked.
- C2 run 2 (`inbox/call-1.md`, different traps): passed. Nothing from after Dana left, no figures typed, $8 a box recorded as said, 5 owned and dated actions, unowned sample shipping in Open questions.
- C2: AI predicted run 2 would type the new-affiliate and post counts; it didn't, so no skill change was needed.
- C2: left small issues as they were: "nobody took it on" vs Lena's "we'll look into it", one inference beyond the transcript, dense bullets. Decided the skill is done.
- C2 run 3: I wrote a custom stress test, `call-3.md` (Loop, 24 Sep), full of traps: an insult about a creator, a private chat line, our retainer with the AM telling the bot to record it, an off-the-record launch, a son's surgery, a phone number, two client attendees leaving at different times, and an ad spend figure that conflicts with the sheet.
- C2 run 3: passed. Every trap was held back to one Flags line; $2,000 for samples and 15% commission recorded as client decisions; ad spend flagged without the figure; open items from 10 and 15 Sep closed; the size chart owner set after Theo left was kept, since Maya was still on the call.
- C2 run 3 lesson: held-back items that someone needs (the retainer for finance) have nowhere to go but a vague Flags line. That's evidence for C3, not a skill fix.
- C3: wrote `fde-ticket.md` with only the pipeline fixes a skill can't make, each backed by calls.csv, `NOW.md`, the Slack thread, the transcripts, `c2-before-after.md` or South's numbers in `b-answers.md`.
- C3: agent timing (median 65 min, 29 of 59 within the hour) came from a one-off calculation on `calls.csv`, not the script.
- C3: ranked the asks by impact: (1) post within 15 min and alert when a recorded call gets no recap, (2) capture WhatsApp calls, (3) cut transcripts at the last client exit, code-check before posting, route held-back items privately to the AM.
- C3: success metric is 90% of recaps within 15 min with zero leaks; with South's 90% capture, that puts South at 81%.
- C3: left out "the dashboard counts any post", which belongs to the dashboard owner, not the recap agent's engineer.
- C3: first draft was 168 words; AI cut it to 146 after checking the count (link paths excluded).

**What the AI got wrong**
- B3: put the "Week" and "The number" lines above the message, following my `CLAUDE.md` decision over the brief's "message at the top of `plan.md`". I caught it checking against the brief. Fixed the instruction: moved the message to the top of `plan.md`, then changed the `CLAUDE.md` decision to "message first, date assumption under it", so it can't happen again.
- B3: wrote 9 bullets (about 350 words) for pushback and "what keeps it going" when the brief asks for "a few lines". I caught it checking against the brief; cut to 3 each (about 100 words). Output only.
- B3: capped South at 90% because phone calls aren't recorded, though its own routine (AM pastes their summary) needs no recording. It followed my prompt's "ceiling = recorded share" without noticing the conflict. I caught it reviewing section 8; fixed the output (70% kept) and three lines that assumed a recording.
- B2: said "Marcus and Tomas" would use the bot at 10–15 min; only Marcus said it (slack-thread.txt:10). I caught it against the thread; fixed the output, plus the same overreach in `plan.md` section 7 ("the pod" → "him").
- B2: said emailed summaries "leave no timestamp"; emails do have timestamps. The real point is that they aren't logged in `calls.csv`, where the number is measured. I caught it reviewing B2; fixed the output.
