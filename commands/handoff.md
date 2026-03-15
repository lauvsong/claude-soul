---
name: handoff
description: >
  Save the current conversation context as a structured handoff document (HANDOFF.md) for seamless session continuation.
  Use when the user says "handoff", "인수인계", "세션 정리", "작업 넘기기", "context save", "save progress",
  or asks to summarize current work for a future session. Also use when the conversation is getting long and
  the user wants to capture the current state before starting a new session.
---

# Handoff

Generate a `HANDOFF.md` in the current working directory that captures conversation state for seamless continuation in a new session.

## Procedure

1. Analyze the full conversation to extract:
   - **Goal (목표)**: Overall objective
   - **Completed (완료 작업)**: Finished tasks with brief results
   - **In Progress (진행 중 작업)**: Underway but incomplete tasks
   - **Next Steps (다음 단계)**: Planned or recommended next actions
   - **Cautions (주의사항)**: Gotchas, blockers, decisions, constraints

2. Write `HANDOFF.md` using the template below. If it already exists, confirm before overwriting.

## Template

```markdown
# Handoff

> Generated: {YYYY-MM-DD HH:MM}
> Working Directory: {cwd}

## Goal (목표)

{1-3 sentences describing the overall objective}

## Completed (완료 작업)

- {completed item with brief result/outcome}

## In Progress (진행 중 작업)

- {in-progress item with current status}

## Next Steps (다음 단계)

1. {next step}

## Cautions (주의사항)

- {important context, constraints, blockers, or decisions to preserve}

## Key Files

- `{path}` - {brief description of role/changes}
```

## Guidelines

- Be concise but preserve enough context for a cold start in a new session.
- Include file paths that were created or modified.
- Capture architectural decisions or trade-offs discussed.
- Note failed approaches in Cautions to avoid repeating them.
- Write in the same language the user has been using.
