# Plan: South pod, week of 28 Sep 2026

## 1. Message to Marcus

> Marcus, on the 18th you wrote "if it posted in 10-15 min I'd use it. the content is fine when it shows up". I've asked engineering for exactly that.
>
> Until it ships, one change for this week: when you or Tomas send a client your summary, paste it into their Slack channel too, within the hour, with each action's owner and due date.
>
> I'll make that a two-minute paste: a fill-in template in #pod-south by Monday morning, and I'll join your first call on Monday and post that recap myself so you can see the routine.
>
> If a day gets packed, drop a line in #pod-south and I'll post it for you.
>
> Can we try it through Friday and look at how it went together?

**Week:** Mon 28 Sep to Fri 2 Oct 2026. The call log ends Thu 24 Sep, so "by Friday" means Fri 2 Oct.
**The number:** the share of South's calls held that get a recap (summary plus action items) posted in the client's Slack channel within 60 minutes of call end ([NOW.md:10](brain/NOW.md)).

## 2. What Marcus will push back with

- **"Priya said our emailed summaries count."** That was a suggestion in the thread ([slack-thread.txt:13](slack-thread.txt)). The number counts recaps posted ([NOW.md:10](brain/NOW.md)). Pasting the same summary into Slack makes that work count, and I'm confirming this with Priya on Monday.
- **"Fix the bot instead."** Agreed, and it's ask 1 in [fde-ticket.md](fde-ticket.md), but it won't ship by Friday. Your own notes are already faster: AM-posted recaps in North and East take a median 18 minutes ([calls.csv](calls.csv)).
- **"It's one more step in a busy month."** It's a paste of what you already write, and on a packed day I post it.

## 3. What keeps it going after I stop checking in

- **The call ends with the recap.** The last two minutes of each call read back the action items, each with an owner and a due date, so the recap is already written when the call ends.
- **Clients come to expect it.** Once clients get the recap in their channel within the hour, they look for it there, and a missing one gets noticed without me.
- **The system takes over.** Once the agent posts within 15 minutes and alerts on missing recaps (ask 1 in [fde-ticket.md](fde-ticket.md)), the AM reviews its recap instead of writing one.

## 4. Where we are

Source: [calls.csv](calls.csv) via `scripts/b1_metrics.py`. The week uses `--from 2026-09-21 --to 2026-09-24`; month to date uses no filter.

| South | Calls held | Recorded | Recap within 60 min | Share |
|---|---|---|---|---|
| Week of 21 Sep (Mon–Thu 21–24; the log has no Friday) | 10 | 10 | 4 | **40%** |
| Month to date (1–24 Sep) | 40 | 36 | 14 | **35%** |

- **The agent posted every South recap; no AM posted one.** In the week of 21 Sep, 4 of 8 were on time (47–53 min) and 4 were late (71–85 min). The month-to-date median is 74 minutes ([calls.csv](calls.csv)).
- **Two Kettle & Crumb calls got no recap at all.** The 22 Sep and 24 Sep calls were recorded but never got a recap ([calls.csv:118](calls.csv), [calls.csv:141](calls.csv)). With those two posted on time, the week would have been 60%.
- **No trend.** Weekly shares since 1 Sep are 20%, 50%, 33% and 40%. Capture is fine at 90% month to date; speed is 39% ([b-answers.md:20](b-answers.md)).

## 5. What I do myself

- **Mon, first thing:** save a recap template in #pod-south: 3–6 summary bullets, then action items with owner, action and due date. It matches the brain's recap shape ([RESOLVER.md:41-62](brain/RESOLVER.md)).
- **Mon:** confirm with Priya that October reporting keeps the [NOW.md:10](brain/NOW.md) definition (posted within the hour). Posting the emailed summary in Slack is how that work counts.
- **Mon:** join Marcus's first call and post its recap within 15 minutes using the template.
- **Tue:** ask Sam for North's call routine and share it with Marcus and Tomas. North is already helping East copy it ([NOW.md:13](brain/NOW.md)).
- **Daily, 9:00:** check the previous day's South calls with `python3 scripts/b1_metrics.py --from <yesterday> --to <yesterday>`, and cover any call the pod flags in #pod-south.
- **This week:** write the two missing Kettle & Crumb recaps (22 and 24 Sep) from `inbox/call-1.md` and `inbox/call-2.md`, so the client's channel and the brain are complete. They come too late to count toward the number.
- **Fri:** go through the week with Marcus call by call, decide together whether to keep the routine, and send the result to Priya.

## 6. What I ask of the pod

- **The one change:** whoever ran the call posts the summary they already write into the client's Slack channel, within 60 minutes of call end, using the template.
- **Every action item gets one owner and one due date.** That is what makes a summary a recap ([NOW.md:10](brain/NOW.md), [RESOLVER.md:35](brain/RESOLVER.md)).
- **If you can't post within the hour, say so in #pod-south,** and I'll post it from the recording, or from your notes for a phone call.
- **Nothing else this week.** That includes phone calls: the same paste covers them, because it doesn't need a recording.

## 7. What I ask of engineering

The full ticket is [fde-ticket.md](fde-ticket.md). This week:
- **A date for ask 1, posting within 15 minutes.** It's the change Marcus said would make him use the bot ([slack-thread.txt:10](slack-thread.txt)). It won't land by Friday, but the date tells the pod when the routine hands over to the agent.
- **The no-recap alert from ask 1.** Two Kettle & Crumb calls last week were recorded and got no recap ([calls.csv:118](calls.csv), [calls.csv:141](calls.csv)).
- **A check that AM posts are logged.** AM posts in South's client channels should be logged with `posted_by = AM`, as North's and East's are, so the pod's posts count.
- Asks 2 (WhatsApp capture) and 3 (leak guard) stay in the ticket. They don't change South's number this week.

## 8. The number I expect by Friday

**70%**: about 7 of 10 South calls held from 28 Sep to 2 Oct get a recap within the hour. That's up from 40% the week before, and short of 80%.

- **About 10 calls.** South held 10, 8, 12 and 10 calls in its four September weeks.
- **The routine covers phone calls too.** An AM pasting their own summary doesn't need a recording, so every call can count, not just the 90% that get recorded. Only the agent is limited to recorded calls.
- **6 of 10 get a pod-posted recap, all on time.** AM posts in North and East hit the hour 45 times out of 45, all within 28 minutes. I assume about 60% take-up because this is a new habit for South.
- **The agent covers the other 4 at South's current 40% on-time rate**, when they're recorded, which adds about 1.
- **6 + 1 = 7 of 10, or 70%.** I'm not counting on the engineering fix, which won't ship by Friday.
- **Range: about 55% to 90%.** 55% if the pod posts on only 3 calls. About 90% if it takes up the routine the way East did after 15 Sep, when AMs posted on 12 of 14 calls and East reached 93%. With about 10 calls, each call moves the number by 10 points.
