---
name: pod-dashboard
description: Builds the pod recap dashboard (extra/pod-dashboard/dashboard.html) from calls.csv for a date range, using B1's own maths, checks it against scripts/b1_metrics.py, comments on the data in chat, then opens the page. Use when the user asks for the pod dashboard or for recap numbers by pod over a period.
argument-hint: "[from YYYY-MM-DD] [to YYYY-MM-DD] [minutes]"
---

This file only registers the `/pod-dashboard` shortcut. The skill lives in `extra/pod-dashboard/`.

Read `extra/pod-dashboard/SKILL.md` and follow it exactly, with these arguments: $ARGUMENTS
