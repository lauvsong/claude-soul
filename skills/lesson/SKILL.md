---
name: lesson
description: |
  사용자 피드백/교정을 받았을 때 교훈을 기록하는 스킬.
  같은 실수를 반복하지 않도록 패턴을 tasks/lessons.md에 저장한다.
  Use when: 사용자가 교정/피드백을 주었을 때, "lesson 기록해", "이거 기억해", "/lesson" 등
---

# Lesson — 교훈 기록

사용자의 교정/피드백을 받으면 재발 방지를 위해 교훈을 기록한다.
rules/03-task-management.md R5 항목의 실행 도구.

## Workflow

1. 사용자의 피드백에서 **교훈(패턴)**을 추출한다.
2. `tasks/lessons.md` 파일이 존재하고 쓰기 가능하면 파일에 기록한다.
3. 파일이 없거나 쓸 수 없으면 채팅에 동일 포맷으로 출력한다.

## Format

아래 템플릿을 따른다:

```markdown
### [날짜 or 순번]
- **Lesson**: 무엇을 배웠는가
- **Trigger**: 어떤 상황에서 재발할 수 있는가
- **Prevention Rule**: 1줄 짧은 규칙
- **Example**:
  - Bad: 잘못된 예
  - Good: 올바른 예
```

## Rules

- 기존 lessons.md 내용을 덮어쓰지 않는다. 항상 **append**.
- 중복 교훈이 이미 있으면 기존 항목을 보강하거나 스킵한다.
- 교훈은 간결하게 — 1개 피드백에 1개 항목.
