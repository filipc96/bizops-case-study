# Recap agent: fixes a skill file can't make

**Problem:** The rewritten skill writes clean recaps ([c2-before-after.md](c2-before-after.md)). The pipeline still fails: lateness, unrecorded calls, unblocked leaks.

**Evidence**
- Agent median 65 min; 30 of 59 recaps miss the hour ([calls.csv](calls.csv)). South: 74 min, 20 of 34 late ([b-answers.md](b-answers.md):29).
- Marcus: "if it posted in 10-15 min I'd use it" ([slack-thread.txt](slack-thread.txt):10).
- 34 of 140 calls never recorded, 26 of them West's WhatsApp calls ([calls.csv](calls.csv); [NOW.md](brain/NOW.md):16).
- Recording runs after the client leaves; a leaked DM got posted ([bad-recap-source.md](workers/output/bad-recap-source.md):19-20, [calls.csv](calls.csv):85).

**Ask, ranked by impact**
1. Post within 15 min. Alert when a recorded call gets no recap ([calls.csv](calls.csv):118,141).
2. Capture WhatsApp calls.
3. Cut transcripts at the last client exit, and code-check before posting.

**Success metric:** 90% of recaps posted within 15 min; zero SANITIZER leaks over 2 weeks. South already captures 90% ([b-answers.md](b-answers.md):20), so it reaches 81%.
