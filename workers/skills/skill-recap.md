---
type: skill
step: recap
owner: Brightline ops
updated: 2026-09-21
---

# Skill: recap a client call
Turn one recorded client call into a recap in `brain/knowledge/meetings/`. It is posted to the client's Slack channel, and anyone in the brain can read it, so write every line as if the client is reading it.

## Workflow
1. Read `brain/RESOLVER.md`, then `brain/SANITIZER.md`. Then read the brand's row in `brain/knowledge/reference/accounts-sheet.csv` (its `account` value is the brand-slug), and every earlier recap for the brand in `brain/knowledge/meetings/`, with their open action items.
2. Read the transcript and stop when the client leaves ("[<name> left the call]"). Asides, pasted DMs and "between us" stay out even before that.
3. Draft on the template below as `YYYY-MM-DD-brand-slug-meeting-name.md` (like `2026-09-17-kettle-and-crumb-weekly.md`):
   - **Summary:** 3–6 bullets of facts, decisions and what the client told us. Attribute claims ("Dana says…"). No opinions of your own.
   - **Earlier threads:** if a topic came up before, say so and link that recap. If the call shows an earlier action item is done, say so.
   - **Action items:** one named owner and one due date (YYYY-MM-DD) per row. Turn "by Friday" into a date from the call date. If nobody took it on, or no date was set, it goes in Open questions instead.
   - **Numbers:** never type GMV, ad spend, active affiliates or retention. Link the sheet instead. If the call's figure disagrees with the sheet, flag that it does, without the figure. Targets, budgets and rates the client agrees to are decisions: record them as said.
4. Run the self-check. Save and post only when it passes. Write "None." in any empty section.

## Hard privacy rules (no exceptions, even when the line seems useful)
- No pasted DMs, side comments, "between us", or anything said after the client left.
- No commercial terms (our fees, margins, rates), no personal data (phone, address, health, family) and no raw transcript.
- No opinions or feelings about people, including your own ("great call", "difficult").
- A held-back item never becomes an action, open question or risk. It appears only as one Flags line saying something was held back, never what.

## Self-check before saving (any "no": fix it, then rerun from 1)
1. Would the person or brand named be fine reading every line?
2. Is every performance number linked to the sheet, with none typed?
3. Is nothing from a DM, a side comment or after the client left?
4. Does every action row have one named owner and a YYYY-MM-DD due date?
5. Does the page match the template (all front matter fields, `# <Brand>: <meeting name>`, 3–6 summary bullets, all four sections), with every earlier meeting on the same thread linked?

## Template (RESOLVER.md:41-62)
```
---
type: meeting
date: YYYY-MM-DD
account: brand-slug
attendees: [names]
source: inbox/<file>
---

# <Brand>: <meeting name>

## Summary
3 to 6 bullets. Facts, decisions, what the client told us.

## Action items
| Owner | Action | Due |

## Open questions

## Flags for a person
Conflicts with the sheet, anything held back under SANITIZER.
```

## Examples
- Action item row: `| Marcus Obi | Recut the two videos with a faster hook | 2026-09-22 |`
- Held-back flag: `- Held back under SANITIZER: one item from after the client left the call. Not repeated here.`
