# C2: the recap skill, before and after

## 1. What changed in the skill

The old skill is the original from the first commit (`git show $(git rev-list --max-parents=0 HEAD):workers/skills/skill-recap.md`). The new skill is [`workers/skills/skill-recap.md`](workers/skills/skill-recap.md). Problem numbers refer to [`c1-bad-recap-review.md`](c1-bad-recap-review.md).

| Old line | Problem it caused | New rule |
|---|---|---|
| :10 "You turn a recorded client call into a recap for the brain." | Nothing says who reads the page, so the private DM went in (1). | :9 "…anyone in the brain can read it, so write every line as if the client is reading it." |
| :13 "The transcript of one call." | The agent never saw RESOLVER, SANITIZER, the sheet or earlier recaps (2, 4, 5). | :12 Read RESOLVER, then SANITIZER, then the brand's sheet row, then every earlier recap with its open action items. |
| :16 "A file in `brain/knowledge/meetings/`." | No template, file name or required sections (5). | :14 file name pattern. :34-56 template copied from `RESOLVER.md:41-62`. :32 self-check 5. |
| :19 "Read the whole transcript." | It read past "[Theo Grant left the call]" into the pasted DM (1). | :13 Stop when the client leaves. Asides, pasted DMs and "between us" stay out even before that. :22 nothing said after the client left. |
| :20 "Include everything relevant, so nothing gets lost." | The DM counted as "relevant", the summary was a prose paragraph, and it opened with "Great call" (1, 5, 6). | :15 3–6 bullets of facts, decisions and what the client told us, attributed. :16 link earlier threads. :21-24 hard privacy rules "no exceptions, even when the line seems useful", including no opinions of its own. |
| :21 "Include the key numbers mentioned on the call, so the team has them handy." | "$95K GMV" was typed in, and the conflict with the sheet wasn't flagged (2). | :18 Never type GMV, ad spend, active affiliates or retention. Link the sheet, and flag a disagreement without the figure. Client-agreed targets, budgets and rates are recorded as said. :29 self-check 2. |
| :22 "List the next steps." | Tasks with no owner or date, the unowned size chart presented as a step, and the DM turned into a "risk" step (3, 1). | :17 One named owner and one YYYY-MM-DD date per row, with relative dates converted. Anything without an owner or date goes to Open questions. :25 a held-back item never becomes an action, question or risk. :31 self-check 4. |
| :23 "Post it." | Posted without any check (1, 2, 5). | :19 Save and post only when the self-check passes. :27-32 five-question self-check that reruns from step 1 on any "no". :25 and :60 one Flags line for anything held back. |

The two examples at :58-60 are new, with no old line behind them. The action-item row (:59) comes from Kettle & Crumb's [17 Sep recap](brain/knowledge/meetings/2026-09-17-kettle-and-crumb-weekly.md). The held-back flag (:60) is generic wording from no account, but it fits the Loop case exactly, and the rerun copied it word for word ([after-recap.md](workers/output/after-recap.md):28). The stress tests adapted the same flag to their own calls ("two items…" for `call-1.md`, "six items… one of them from after the client left" for [`call-3.md`](workers/tests/call-3.md)), which shows the agent treats it as a pattern rather than copying it.

## 2. Rerun setup

- **Folder:** a clean folder (`~/c2-test`) outside the repo, holding only three things:
  - `brain/` as it was at commit `b57ee9a`, before the A1/A2 recaps;
  - the edited `workers/skills/skill-recap.md`;
  - the transcript, saved as `inbox/bad-recap-source.md`.
- **Session:** a brand-new Claude session with no global instructions, no `CLAUDE.md`, no C1 notes and no subagent.
- **Prompt used:** "Follow workers/skills/skill-recap.md to recap inbox/bad-recap-source.md."
- **Checked against the repo:** the skill and the transcript were identical to the repo copies, and `brain/` matched `b57ee9a` apart from the new recap.
- **Output:** the skill wrote `brain/knowledge/meetings/2026-09-15-loop-athletic-weekly.md` in the test folder. It's copied here as `after-recap.md`, with its 5 links re-pointed so they work from `workers/output/`. The content is otherwise unchanged.
  - `source: inbox/bad-recap-source.md` still reflects the test folder's layout. In this repo the transcript is `workers/output/bad-recap-source.md`.
- **Two more stress tests**, same folder and skill:
  - `inbox/call-1.md` (Kettle & Crumb, 22 Sep);
  - a custom [`call-3.md`](workers/tests/call-3.md) (Loop Athletic, 24 Sep), built to contain every trap.
  - Both passed; see [`log.md`](log.md).

## 3. Before and after

- **Before:** [`workers/output/bad-recap.md`](workers/output/bad-recap.md)
- **After:** [`workers/output/after-recap.md`](workers/output/after-recap.md)

## 4. Scorecard

Line numbers refer to `after-recap.md`. Result: **all 6 problems fixed, 24 of 24 sub-points.** A search of the recap for fee, CEO, review, Q1, frustrat, risk, 95, ninety, $, great and DM finds nothing.

| C1 problem | Fixed? | Evidence (quote) |
|---|---|---|
| **1. Private DM, fees, remark about a person** | | |
| 1a. Pasted DM included | Yes | No trace of it in the recap; only :28 refers to it: "Held back under SANITIZER: one item from after the client left the call. Not repeated here." |
| 1b. Our agency fees named | Yes | No mention of fees anywhere. |
| 1c. Client CEO's feelings | Yes | No mention of the CEO anywhere. |
| 1d. "Review risk" made a next step | Yes | The only action is :20, "Send the brief for the October batch…". Open questions has nothing about it. |
| 1e. No held-back note | Yes | :28 (quoted in 1a). |
| **2. GMV typed in, conflicts with the sheet, no flag** | | |
| 2a. Figure typed | Yes | :13: "Current numbers are in the [accounts sheet]… row `loop-athletic`." No figure appears. |
| 2b. Conflict not flagged | Yes | :27: "Sheet conflict: the GMV figure Theo gave on the call disagrees with the [accounts sheet]… The figure is not repeated here and the sheet was not changed." |
| 2c. "About" made exact | Yes | No figure appears at all. |
| 2d. "This month" vs last 30 days | Yes | :27: "Theo's figure was for 'this month' and the sheet column covers the last 30 days." |
| **3. No real action items** | | |
| 3a. Bare tasks, not action items | Yes | :18-20 is an Owner / Action / Due table. |
| 3b. Brief's owner and date dropped | Yes | :20: "\| Lena Varga \| Send the brief for the October batch of 12 try-on videos \| 2026-09-18 \|" |
| 3c. Size chart had no owner but was listed as a step | Yes | :23: "Who will look at the size chart issue on the product page, and by when?" |
| 3d. Leaked DM as a step | Yes | Only one action row, :20. |
| 3e. Doesn't meet the definition of a recap | Yes | It has a summary (:11-15) and an action item with an owner and a date (:20). |
| **4. Thread treated as new, 10 Sep not linked** | | |
| 4a. No link to 10 Sep | Yes | :12: "This continues the [2026-09-10 weekly], when 8 of 12 were delivered." |
| 4b. Lena's 10 Sep action not closed | Yes | :12: "Lena's action from that call to brief creators on try-on for the last 4 is done." |
| 4c. Size chart vs Theo's open action | Yes | :15: "The size chart also came up on the [2026-09-10 weekly]". :24: "Is Theo's action from the [2026-09-10 weekly] to send the fall size chart done? This call didn't say." |
| **5. Template not followed** | | |
| 5a. No attendees or source | Yes | :5: "attendees: [Theo Grant, Lena Varga]". :6: "source: inbox/bad-recap-source.md" |
| 5b. Wrong title format | Yes | :9: "# Loop Athletic: weekly" |
| 5c. Prose paragraph instead of 3–6 bullets | Yes | 4 bullets, :12-15. |
| 5d. "Next steps" instead of an Action items table | Yes | :17: "## Action items" with a table. |
| 5e. No Open questions or Flags section | Yes | :22: "## Open questions". :26: "## Flags for a person". |
| **6. Editorialising, unattributed claim** | | |
| 6a. "Great call with Theo" | Yes | Gone; :12 opens with "Fall collection creator videos: all 12 are now delivered". |
| 6b. Performance claim stated as fact | Yes | :13: "Theo says the try-on videos are performing much better." |

**Small issue, not a C1 problem:** :15 says "nobody took it on", but Lena said "we'll look into it". The recap still handles it correctly as an open question.

**Skill change not yet made:** step 2 (:13) says "stop when the client leaves." In [`call-3.md`](workers/tests/call-3.md) two client attendees left at different times. The run correctly waited for the last one, but the wording allows stopping at the first. The fix is "the last client attendee".

## 5. What a skill file can't fix

These still fail after the last round. [`fde-ticket.md`](fde-ticket.md) asks engineering for five of them: speed, capture, cutting the private talk, a hard check before posting, and an alert when a recorded call gets no recap. The other two aren't engineering asks: a private route for held-back items needs a decision about who may see them, and the dashboard counting any post is for the dashboard's owner.

- **Speed:** the agent posts 45–91 min after a call. Its median is 65 min, and only 29 of 59 agent recaps land within 60 min ([`calls.csv`](calls.csv)). South skips it in favour of their own notes ([`slack-thread.txt`](slack-thread.txt):4,7).
- **Capture:** 34 of 140 calls (on WhatsApp or by phone) are never recorded, including 26 of West's 30, so the agent never sees them ([`NOW.md`](brain/NOW.md):16, [`calls.csv`](calls.csv)).
- **Private talk reaches the agent:** the recording keeps running after the client leaves ([`bad-recap-source.md`](workers/output/bad-recap-source.md):19-20, [`call-1.md`](inbox/call-1.md):25-27). The skill filters it out on each run, but nothing removes it before the model reads it.
- **No hard check before posting:** the self-check is the model grading itself. The bad recap was posted at 17:21 with no check at all ([`calls.csv`](calls.csv):85).
- **Held-back items have no private route:** when someone needs a held-back item (in [`call-3.md`](workers/tests/call-3.md), the AM asked for the retainer to reach finance), the recap can only say "something was held back", and the AM is never told.
- **Recorded calls with no recap:** two recorded Kettle & Crumb calls never got one ([`calls.csv`](calls.csv):118, :141). The data doesn't show why.
- **The dashboard counts any post:** the bad recap counts as on time ([`calls.csv`](calls.csv):85), even though it had no owners or dates.
