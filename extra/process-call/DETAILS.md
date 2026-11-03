# process-call

Turns one client call transcript into a brain recap plus proposed page edits, then checks the recap before anyone calls it done. Used for the A1 and A2 recaps.

| File | What it is |
|---|---|
| `SKILL.md` | The workflow an agent follows: a 6-step checklist, from reading the rules to reporting back. |
| `check_recap.py` | A checker for one or more recaps against `brain/RESOLVER.md` and `brain/SANITIZER.md`. Python 3, standard library only. |

## Why it exists
`workers/skills/skill-recap.md` says how to write a recap. This adds what goes around it: the context to read first, where the output goes, a check the recap must pass, and a report of the open points. The checker catches mechanically what went wrong in the original bad recap (`c1-bad-recap-review.md`): leaked side comments, retyped numbers, actions without one owner and a date.

## How to use it
Run it as `/process-call inbox/call-1.md` (registered in `.claude/skills/`), or from the repo root tell the agent:

```
Follow extra/process-call/SKILL.md for inbox/call-1.md
```

The agent writes the recap to `brain/knowledge/meetings/`, updates `proposed-changes.md` (one row per page + field, plus a "Not proposed (and why)" section), and reports: the file written, the checker result with a reason for each WARN, Flags, Open questions, proposals, and every date it read from relative wording ("next Tuesday").

To run the checker on its own:

```
python3 extra/process-call/check_recap.py brain/knowledge/meetings/*.md
```

It prints PASS / WARN / FAIL per check for each file, then a summary. Exit code 1 if any check FAILs, 0 otherwise (WARNs allowed).

## What the checker checks
| # | Check | Level | Looks for |
|---|---|---|---|
| 1 | path | FAIL | A file under `brain/` is `brain/knowledge/meetings/YYYY-MM-DD-<slug>.md`. Skipped outside `brain/`. |
| 2 | front | FAIL | Front matter with `type: meeting`, `date`, `account`, `attendees`, `source`. |
| 3 | sections | FAIL | `## Summary`, `## Action items`, `## Open questions`, `## Flags for a person`. |
| 4 | actions | FAIL | Each action row has one owner (no "and", "/", "&", "or", ",") and a `YYYY-MM-DD` due date. |
| 5 | links | FAIL | Every relative link resolves from the recap's own folder. |
| 6 | redflags | FAIL | SANITIZER phrases: "between us", "don't mention", "DM", "flaky", "difficult", "checked out", "agency fee", "our fee", "margin", and a pasted "[<name> left the call]" marker. |
| 7 | numbers | WARN | A `$` amount, or GMV / ad spend / affiliates / retention within 5 words of a number. |
| 8 | bullets | WARN | Summary has 3 to 6 bullets. |

Things to know:
- **WARN on numbers is expected** for targets and budgets the client agreed to, which recaps record as said (`brain/RESOLVER.md:29`). The agent must say why each one is allowed.
- **"left the call" fails only as a bracketed transcript marker,** so the approved held-back line in Flags passes.
- **Red flags are a phrase list, not a reading.** An opinion about someone that avoids the listed words passes. SANITIZER's 3-question check still applies.

## Rules this adds on top of `skill-recap.md`
- Stop at the **last** client attendee's "[<name> left the call]", not the first.
- Write only to `brain/knowledge/meetings/` and `proposed-changes.md`. People, account and reference pages change only by proposal, approved by a pod lead.
- Mention a held-back item only in the recap's "Flags for a person" section, never anywhere else and never where to find it.

## Tested on
- `workers/output/after-recap.md`: PASS. `workers/output/bad-recap.md`: FAIL (front matter, sections, a red-flag phrase). A copy of the good recap with a "between us" line added: FAIL.
- Made-up recaps with a wrong path, two owners, "Friday" as a due date, a broken link and DMs all FAIL; names like "Jordan" and words like "admin" don't trip it.
- All 6 recaps in `brain/knowledge/meetings/`: no FAIL. Four WARN, each on a client-agreed target or budget.
