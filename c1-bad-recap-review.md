# C1: What's wrong with `bad-recap.md`

**What I compared:** [`workers/output/bad-recap.md`](workers/output/bad-recap.md), the recap, against its transcript [`workers/output/bad-recap-source.md`](workers/output/bad-recap-source.md) (Loop Athletic weekly, Tue 15 Sep 2026). I checked both against [`brain/RESOLVER.md`](brain/RESOLVER.md), [`brain/SANITIZER.md`](brain/SANITIZER.md), [`accounts-sheet.csv`](brain/knowledge/reference/accounts-sheet.csv) and [`2026-09-10-loop-athletic-weekly.md`](brain/knowledge/meetings/2026-09-10-loop-athletic-weekly.md).

**Severity scale:**
- **Critical:** harms a person or the client relationship if read.
- **High:** the team gets wrong information, or no information it can act on.
- **Medium:** breaks the brain's structure.
- **Low:** style.

This file quotes the leaked lines on purpose, to show the mistake. It stays outside `brain/`.

## Problems, most severe first

### 1. Critical: a private DM, our fees and a remark about a person went into the brain
- **What's wrong:**
  - The recap repeats a DM that Theo sent Lena privately. Lena pasted it into her notes after Theo had left the call.
  - It names our agency fees and the client CEO's feelings.
  - It turns "review risk" into a next step.
  - Anyone in the brain can read the page, including Loop Athletic (SANITIZER.md:9).
- **Evidence:**
  - bad-recap.md:9: "Theo's CEO is frustrated with the agency fees and might put us up for review in Q1."
  - bad-recap.md:14: "Keep an eye on the account review risk."
  - In the source, Theo leaves at :19 ("[Theo Grant left the call]"). Then at :20: "(to herself, still recording) Okay. Pasting Theo's DM from this morning into my notes…"
  - The agent posted this recap at 17:21 (calls.csv:85), and the agent posts to the client's Slack channel (NOW.md:19).
- **Rules broken:**
  - SANITIZER.md:14: no pasted DMs, no side comments after a client drops off.
  - SANITIZER.md:15: no information about our fees.
  - SANITIZER.md:13: no opinions about people.
  - It fails all three checks at SANITIZER.md:22-24.
  - RESOLVER.md:33: nothing on the SANITIZER list, ever.
  - The right move was to leave it out and note under Flags that something was held back (SANITIZER.md:26). The recap has no Flags section.

### 2. High: GMV typed in, contradicting the sheet, with no flag
- **What's wrong:**
  - The recap types in a GMV figure that the sheet doesn't support, and doesn't flag the conflict.
  - It turns Theo's "about" into an exact figure.
  - Theo's "this month" isn't the sheet's "last 30 days".
- **Evidence:**
  - bad-recap.md:9: "Loop Athletic is at $95K GMV this month."
  - Source :12: "we're at about ninety-five thousand GMV this month".
  - accounts-sheet.csv:3: `gmv_last_30d_usd` is 62000, `sheet_updated` is 2026-09-21.
- **Rules broken:**
  - RESOLVER.md:29: pages link to the sheet and never retype a number.
  - RESOLVER.md:36: flag a call number that disagrees with the sheet, and don't copy it onto a page.
  - SANITIZER.md:23: the check that every performance number is linked, not typed.

### 3. High: no real action items (no owners, no due dates)
- **What's wrong:**
  - "Next steps" is three bare tasks.
  - The transcript gives the brief an owner and a deadline: Lena, by Friday, which is Fri 18 Sep 2026. The recap drops both.
  - Nobody took ownership of the size chart on the call. The recap hides this instead of raising it as an open question.
  - The third "step" is the leaked DM (problem 1).
  - INSTRUCTIONS.md:30 defines a recap as a summary plus action items, each with an owner and a due date. This doesn't meet that definition, yet calls.csv:85 logs it as a posted recap.
- **Evidence:**
  - bad-recap.md:11-14.
  - Source :14: "Brief by Friday?" Source :15: "Friday works. I'll send it." Source :17: "Noted, we'll look into it."
- **Rules broken:**
  - RESOLVER.md:35: every action item has one owner and one due date.
  - RESOLVER.md:55-56: the action items table in the template.
  - INSTRUCTIONS.md:30 and NOW.md:10: a recap is a summary plus action items.

### 4. Medium: an ongoing thread treated as new, with no link to the 10 Sep meeting
- **What's wrong:**
  - On 10 Sep, Theo asked for try-on content. The team decided the last 4 videos would switch to try-on, Lena was to brief creators, and Theo was to send the fall size chart.
  - The recap doesn't link that meeting.
  - It doesn't close Lena's 10 Sep action, which the call shows is done: all 12 videos delivered, the last 4 in try-on.
  - It doesn't say whether the "size chart issue" is the same thread as Theo's open size chart action.
- **Evidence:**
  - bad-recap.md:9: "All 12 fall videos were delivered and the try-on format is performing much better", and "There's a size chart issue on the product page."
  - 2026-09-10-loop-athletic-weekly.md:13-14 (try-on decision), :19 (Lena's brief), :20 (Theo's size chart).
  - Source :11: "the last four are the try-on format you asked for."
- **Rule broken:** RESOLVER.md:37: if someone has already told us something, say so and link the earlier meeting.

### 5. Medium: the recap template isn't followed
- **What's wrong and evidence:**
  - The front matter has no `attendees` or `source` (bad-recap.md:1-5; template at RESOLVER.md:46-47).
  - The title is "Loop Athletic weekly, 15 Sep" (bad-recap.md:7), not `# <Brand>: <meeting name>` (RESOLVER.md:50).
  - The summary is one prose paragraph (bad-recap.md:9), not 3-6 bullets (RESOLVER.md:53).
  - It has "Next steps" (bad-recap.md:11) instead of an Action items table (RESOLVER.md:55-56).
  - It has no "Open questions" or "Flags for a person" section (RESOLVER.md:58-61). The held-back DM (1), the GMV conflict (2) and the unowned size chart (3) had nowhere to go.
- **Rule broken:** RESOLVER.md:41-62, the recap template.

### 6. Low: editorialising and an unattributed claim
- **What's wrong:**
  - The recap opens with the writer's opinion.
  - It states the client's claim about performance as fact instead of attributing it to Theo.
- **Evidence:**
  - bad-recap.md:9: "Great call with Theo."
  - bad-recap.md:9: "the try-on format is performing much better". In the source (:12), Theo is the one who says it.
- **Rule broken:** RESOLVER.md:53: the summary is facts, decisions and what the client told us.

## Which line of `skill-recap.md` caused each problem

| Skill line | Text | Causes | Why |
|---|---|---|---|
| [:13](workers/skills/skill-recap.md) | "The transcript of one call." | 2, 4, 5 | The only input is the transcript. The agent never sees RESOLVER, SANITIZER, the sheet or earlier meetings, so it can't check the sheet, link 10 Sep or use the template. |
| :16 | "A file in `brain/knowledge/meetings/`." | 5 | It names a folder only: no template, file name or required sections. |
| :19 | "Read the whole transcript." | 1 | "Whole" includes everything after "[Theo Grant left the call]". Nothing says to stop when the client leaves or to drop side comments. |
| :20 | "Write a summary of the call. Include everything relevant, so nothing gets lost." | 1, 5, 6 | It invites the DM in as "relevant". It asks for an open-ended summary, with no bullets, no 3-6 limit and no facts-only rule. |
| :21 | "Include the key numbers mentioned on the call, so the team has them handy." | 2 | This directly contradicts RESOLVER.md:29 and :36. |
| :22 | "List the next steps." | 3, 1 | It asks for "next steps", not action items with an owner and due date, and lets the DM become a "step". |
| :23 | "Post it." | 1, 2, 5 | It posts with no SANITIZER check and no Flags section. |

The skill never mentions RESOLVER or SANITIZER, though RESOLVER.md:9 requires anyone writing to the brain, human or agent, to read both first. The skill was last updated 2026-09-01 (skill-recap.md:5), before both files' last update on 2026-09-21 (RESOLVER.md:4, SANITIZER.md:4).
