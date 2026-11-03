**Time:** ~3 human hours · ~2 AI hours (two sessions often ran in parallel)
**Skipped:** none

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

**A**
- A1, A2: ran `extra/process-call/SKILL.md` on `inbox/call-1.md` and `inbox/call-2.md`. Both recaps pass the checker; it warns only on client-agreed budgets and targets, which are recorded as said.
- A1 stops when Dana leaves at 01:44; the two items said after are one Flags line. A2: Dana's GMV conflicts with the sheet, so the recap flags it without the figure, and both figures go to `proposed-changes.md` for the export owner to verify.
- Dates read from the calls: Wednesday = 23 Sep and Friday = 25 Sep (A1); "next Tuesday" = 29 Sep and "the Thursday before" = 1 Oct, before the 6 Oct launch (A2).
- `proposed-changes.md`: 7 rows, one per page + field (Dana's role, what she told us and open threads; a new page for Jess; the account's contacts, focus and meetings). No brain page edited.
- A3: `answer.md` opens with what Dana has already told us and when, links a source on every bullet, and raises two risks from the brain: the $600 cap covers 75 boxes against ~70 fall flavor samples, and the targeted plan is top-10 only while 25 more creators were lined up for samples.

**B**
- Wrote `scripts/b1_metrics.py` (standard library, threshold argument, `--from`/`--to`) to rebuild each pod's number from `calls.csv`; checked it against a separate calculation.
- B1: the dashboard shows East at 75%, but per calls held it's 21/30 = 70% (that cell divides by recorded). For the extra number, AI proposed the agent's on-time rate; I chose capture × speed.
- B2: South first (capture 90%, speed 39%; the agent's median is 74 min and no AM posts). East went from 50% to 93% once AMs posted, from 15 Sep. Not West: its gap is capture (26 of 30 calls on WhatsApp).
- B3: `plan.md` for the week of 28 Sep: one ask of Marcus in his own words, and 70% expected by Fri 2 Oct (range 55–90%), up from 40%.

**C**
- C1: 6 problems in `bad-recap.md`, ranked by severity, each with evidence, the rule it breaks and the line of the old skill that caused it.
- C2: rewrote `skill-recap.md` and reran it in a clean folder (`~/c2-test`: only the skill, the brain at `b57ee9a` and the transcript). All 6 C1 problems fixed. It also passed `inbox/call-1.md` and a stress-test transcript I had AI write (`workers/tests/call-3.md`: a private chat during the call, fees said openly, an AM telling the bot to record them, two clients leaving at different times).
- C3: `fde-ticket.md`, under 150 words: post within 15 min and alert on missing recaps; capture WhatsApp calls; cut transcripts at the last client exit and check in code before posting.

**Extra**
- Built `extra/process-call/check_recap.py` (standard library): 6 checks fail a recap, 2 only warn; exits 1 on any FAIL. Tested it before trusting it: it fails `bad-recap.md`, passes `after-recap.md`, and fails a copy with "Between us, Dana is flaky." planted.
- Wrote `extra/process-call/SKILL.md` (38 lines): points to RESOLVER, SANITIZER and `skill-recap.md` instead of restating them, runs the checker until there's no FAIL, and keeps `proposed-changes.md` at one row per page + field. Used it for A1 and A2.
- Built `extra/pod-dashboard/dashboard.py` (standard library): it imports B1's own functions from `scripts/b1_metrics.py`, so the two can't disagree, and writes one self-contained `dashboard.html` (share vs the 80% target with the `adoption.csv` flag, capture × speed, agent vs AM medians, weekly share, recorded calls with no recap). Checked every number on the page against B1's output: 85 of 85 match.

**What the AI got wrong**
1. **A3:** the first `answer.md` never said Dana had already explained the affiliate flow end to end twice (12 Aug, 3 Sep), and it sent the reader to Marcus for the held-back remarks. **Caught by:** reviewing it against RESOLVER rule 5 and SANITIZER. **Fixed the instruction:** three rules in `CLAUDE.md`; a fresh session rerun with the same prompt fixed both.
2. **Extra:** the checker failed the known-good `after-recap.md`, because "left the call" was a red flag but also appears in the approved held-back line. **Caught by:** testing it on a known-good recap before trusting it. **Fixed the instruction (in code):** it now flags only a pasted `[<name> left the call]`.
3. **B2:** said "Marcus and Tomas" would use the bot at 10–15 min; only Marcus said it. **Caught by:** checking the quote against `slack-thread.txt:10`. **Fixed the output only:** a one-off misquote, not a rule problem.
