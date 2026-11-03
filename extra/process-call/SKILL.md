---
name: process-call
description: Turns a client call transcript into a brain recap plus proposed page edits, following RESOLVER and SANITIZER, and verifies it with check_recap.py. Use when a new transcript is in inbox/ or the user asks to recap or process a call.
---

# Process a client call

Input: one transcript in `inbox/`. Output: one recap in `brain/knowledge/meetings/`, updates to `proposed-changes.md`, and a short report.
The recap rules live in `brain/RESOLVER.md`, `brain/SANITIZER.md` and `workers/skills/skill-recap.md`. Follow them; they are not repeated here.

Copy this checklist into your reply and tick each item as you finish it:

```
- [ ] 1. Read RESOLVER.md, SANITIZER.md, skill-recap.md
- [ ] 2. Read account page, attendees' people pages, this account's meetings/, its sheet row
- [ ] 3. Recap written to brain/knowledge/meetings/
- [ ] 4. check_recap.py run from the repo root: no FAIL; every WARN fixed or explained
- [ ] 5. proposed-changes.md read first, then one row per page + field; Not proposed section kept; no held-back mention
- [ ] 6. Reported to the user, including every inferred date
```

## Steps
1. **Rules.** Read `brain/RESOLVER.md`, then `brain/SANITIZER.md`, then `workers/skills/skill-recap.md`.
2. **Context.** Read `brain/knowledge/accounts/<brand-slug>.md`, the `brain/knowledge/people/` page of each attendee (where one exists), every `brain/knowledge/meetings/` file for this account, and the account's row in `brain/knowledge/reference/accounts-sheet.csv`.
3. **Recap.** Write it per `workers/skills/skill-recap.md` to `brain/knowledge/meetings/YYYY-MM-DD-brand-slug-meeting-name.md`, with `source: inbox/<file>`.
4. **Check.** From the repo root, run `python3 extra/process-call/check_recap.py <recap>`. Fix every FAIL and re-run until there are none. For each WARN, fix it or say why it's allowed (e.g. a client-agreed budget or target, recorded as said).
5. **Proposals.** Read `proposed-changes.md` first. Keep one row per page + field:
   - If a pending row exists for the same page and field, update it to the final value and add this call as a second source. Otherwise, add a row.
   - Keep a `## Not proposed (and why)` section at the end for things deliberately not proposed, such as a sheet figure that conflicts with the call.
   - Never mention a held-back item in this file, not even that one exists. It lives only as the recap's Flags line.
   - If the file is missing, create it with the title `# Proposed changes: for a pod lead to approve. Nothing has been edited.`, the header `| page | field | current | proposed | source | why |`, and the `## Not proposed (and why)` section.
   - Write file names in backticks. Never edit `brain/knowledge/people/`, `accounts/` or `reference/` directly; a pod lead approves proposals.
6. **Report.** Tell the user: the file written, the checker result (with the reason for each WARN), Flags, Open questions and proposals ("None." where empty). List every date inferred from relative or ambiguous wording ("next Tuesday", "the Thursday before") and how you read it. Don't say it's done until the checker shows no FAIL.

## Never
- Anything after the **last** client attendee's "[<name> left the call]" marker.
- Writing anywhere but `brain/knowledge/meetings/` and `proposed-changes.md`.
- Mentioning a held-back item, or where it could be found, anywhere but the recap's "Flags for a person" section.
