---
name: process-call
description: Turns a client call transcript into a brain recap plus proposed page edits, following RESOLVER and SANITIZER, and verifies it with check_recap.py. Use when a new transcript is in inbox/ or the user asks to recap or process a call.
argument-hint: "[inbox/<transcript>.md]"
---

This file only registers the `/process-call` shortcut. The skill lives in `extra/process-call/`.

Read `extra/process-call/SKILL.md` and follow it exactly, for this transcript: $ARGUMENTS
If no transcript is named, ask which file in `inbox/` to process.
