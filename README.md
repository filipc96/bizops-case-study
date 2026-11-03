# Ironside Biz Ops case study

My answers to Ironside's Biz Ops case study: recap adoption and the recap agent at Brightline, a fictional creator agency. The [submission page](https://claude.ai/artifact/JWNVErbJXUfMgPqzhki8YK) summarises everything; this repo holds the work.

**In short**
- **South's gap is speed.** The recap agent posts its recaps a median of 74 minutes after the call, and its account managers don't post their own. East went from 50% to 93% once its account managers posted.
- **The dashboard overstates East:** 75% shown, 70% real.
- **The recap agent posted a private message for the client to read.** Its skill is rewritten and tested on three calls, and a checker now tests recaps in code.

**Time:** ~3 human hours · ~2 AI hours. **Skipped:** none.

## Where everything is

| Question | Answer |
|---|---|
| A1 · Recap of call 1 | [`brain/knowledge/meetings/2026-09-22-kettle-and-crumb-weekly.md`](brain/knowledge/meetings/2026-09-22-kettle-and-crumb-weekly.md) |
| A2 · Recap of call 2, and page edits to approve | [`brain/knowledge/meetings/2026-09-24-kettle-and-crumb-monthly-business-review.md`](brain/knowledge/meetings/2026-09-24-kettle-and-crumb-monthly-business-review.md), [`proposed-changes.md`](proposed-changes.md) |
| A3 · Briefing for talking to Dana | [`answer.md`](answer.md) |
| B1 · Pod ranking and one more number | [`b-answers.md`](b-answers.md), built with [`scripts/b1_metrics.py`](scripts/b1_metrics.py) |
| B2 · Which pod first, and why | [`b-answers.md`](b-answers.md) |
| B3 · One-week plan | [`plan.md`](plan.md) |
| C1 · What's wrong with the bad recap | [`c1-bad-recap-review.md`](c1-bad-recap-review.md) |
| C2 · Skill fix, clean rerun, before and after | [`workers/skills/skill-recap.md`](workers/skills/skill-recap.md) (edited), [`workers/output/after-recap.md`](workers/output/after-recap.md), [`c2-before-after.md`](c2-before-after.md); stress test in [`workers/tests/call-3.md`](workers/tests/call-3.md) |
| C3 · Ticket for engineering | [`fde-ticket.md`](fde-ticket.md) |
| Extra · Two daily tools | [`extra/`](extra/): `process-call` (recap → check → propose page changes) and `pod-dashboard`; `/` shortcuts in [`.claude/skills/`](.claude/skills/) |
| Log | [`log.md`](log.md) |
| AI setup | [`CLAUDE.md`](CLAUDE.md): the brain's rules and my decisions, read by every session |

Everything else is the case as provided: [`INSTRUCTIONS.md`](INSTRUCTIONS.md), `brain/` (apart from the two recaps above), `inbox/`, `workers/output/bad-recap.md` and its source, `calls.csv`, `adoption.csv` and `slack-thread.txt`.

## Run it

Python 3, standard library only, from the repo root:

```bash
python3 scripts/b1_metrics.py                                            # each pod's number, from calls.csv
python3 extra/process-call/check_recap.py brain/knowledge/meetings/*.md  # check recaps against the brain's rules
python3 extra/pod-dashboard/dashboard.py                                 # build extra/pod-dashboard/dashboard.html
```

In Claude Code: `/process-call inbox/call-1.md` and `/pod-dashboard`.
