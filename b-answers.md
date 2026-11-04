## B1

The number is the share of calls held that got a recap posted within 60 minutes of call end. Source: `calls.csv`, 1–24 Sep, via `scripts/b1_metrics.py`.

| Rank | Pod | Lead | Calls held | Recap within 60 min | Share |
|---|---|---|---|---|---|
| 1 | North | Sam Whitaker | 40 | 36 | 90% |
| 2 | East | Aisha Rahman | 30 | 21 | 70% |
| 3 | South | Marcus Obi | 40 | 14 | 35% |
| 4 | West | Lena Varga | 30 | 3 | 10% |

**Dashboard mismatch:** `adoption.csv` shows East at 75%, but its own counts give 21/30 = 70%. That one cell divides by calls recorded instead of calls held. Every count matches `calls.csv`.

**Extra number: capture × speed.** Each pod's share splits into two parts, capture (recorded ÷ held) and speed (within 60 ÷ recorded).

| Pod | Capture | × Speed | = Share |
|---|---|---|---|
| North | 38/40 = 95% | 36/38 = 95% | 90% |
| East | 28/30 = 93% | 21/28 = 75% | 70% |
| South | 36/40 = 90% | 14/36 = 39% | 35% |
| West | 4/30 = 13% | 3/4 = 75% | 10% |

This split shows which part holds each pod back. West can't pass 13% even with an instant agent, while North, East and South could each reach 90% and lose points only on speed. So West needs a way to record its WhatsApp calls, and the other three need faster recaps, South most of all at 39%.

## B2

**Work on South first.** At 35% (14 of 40 calls), it has the biggest gap Biz Ops can close this week: 18 more on-time recaps takes it to 80%. Its capture is fine at 90%; its speed is 39% (B1).

**The cause is the agent's speed, with nobody posting faster.** The agent posted all 34 South recaps, at a median of 74 minutes; 20 missed the hour. No AM posts. Marcus and Tomas send their own notes first, and Marcus says he'd use the bot if it posted within 10–15 minutes (`slack-thread.txt`). East shows the fix works: once AMs started posting on 15 Sep, East went from 50% to 93% (`calls.csv`, `brain/NOW.md`).

**Why not West (10%)?** Its gap is capture: 26 of its 30 calls are unrecorded WhatsApp calls, so even an instant agent leaves it at 13%. Its clients prefer WhatsApp (`brain/NOW.md`), so moving them to Meet is an ask, not a fix we control (Theo did switch once). Its next step is the same paste as South's, which needs no recording; a capture tool, which Lena is looking for, comes later.

**Priya's proposal: no.** Emailed summaries aren't logged in `calls.csv`, where the number is measured, and nobody checks they have owners and due dates. Counting them makes South look done while hiding the agent's latency. Instead, post that summary to the client's channel within the hour, which counts honestly.
