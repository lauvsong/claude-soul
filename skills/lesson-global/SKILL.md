---
name: lesson-global
description: |
  사용자 피드백/교정을 전역 규칙 파일에 반영하는 스킬.
  교훈을 ~/.claude/CLAUDE.md 또는 적절한 rules 파일(~/.claude/rules/*.md)에
  직접 반영하여 모든 프로젝트에서 재발을 방지한다.
  Use when: "전역 규칙에 반영해", "글로벌 lesson", "/lesson-global", "rules에 추가해",
  "CLAUDE.md에 반영해", "전역으로 기억해", "모든 프로젝트에 적용해" 등
---

# Lesson Global — 전역 규칙 반영

사용자의 피드백/교정을 전역 rules 파일에 직접 반영하여 모든 프로젝트에서 재발을 방지한다.
프로젝트 로컬 `tasks/lessons.md`에 기록하는 `lesson` 스킬과 달리, 이 스킬은 전역 규칙 자체를 수정한다.

## Workflow

1. 사용자의 피드백에서 **교훈(규칙)**을 추출한다.
2. 기존 rules 파일을 읽고, 교훈이 어느 파일에 속하는지 판단한다.
3. 해당 파일에 규칙을 추가/수정한다.
4. CLAUDE.md가 rules에서 컴파일되는 구조라면 CLAUDE.md도 동기화한다.
5. 변경 내용을 사용자에게 보고한다.

## 대상 파일 매핑

교훈의 성격에 따라 적절한 rules 파일을 선택한다:

| 교훈 카테고리 | 대상 파일 |
|---|---|
| 우선순위/데이터 경계/출력 형식/범위 규율 | `rules/00-core.md` |
| 보안/승인/비밀/파괴적 작업 | `rules/01-safety-approvals.md` |
| 워크플로/계획/조사/서브에이전트/검증 | `rules/02-workflow-orchestration.md` |
| 태스크 관리/교훈 기록/진행 추적 | `rules/03-task-management.md` |
| 저장소 구조/경계/읽기전용/제한 접근 | `rules/04-repo-boundaries.md` |
| Kotlin/코드 스타일/네이밍/라이브러리 | `rules/10-stack-kotlin.md` |
| WebFlux/Reactor/동시성/비동기 | `rules/11-stack-reactive.md` |
| 테스트/빌드/검증 | `rules/12-stack-testing.md` |
| 어디에도 맞지 않는 경우 | 새 rules 파일 생성 (번호 부여) |

## Rules 파일 위치

- `~/.claude/rules/` 에서 대상 파일을 찾는다.

## 편집 규칙

- 기존 rules 파일의 **구조와 포맷을 준수**한다 (SUMMARY / RULES / WHY / EXAMPLES 섹션).
- 새 규칙은 가장 관련 있는 기존 Rule 섹션 아래에 항목으로 추가한다.
- 기존 Rule에 추가하기 어려우면 새 `R번호)` 섹션을 만든다.
- EXAMPLES 섹션에 BAD/GOOD 예시를 추가한다.
- 중복 규칙이 이미 있으면 기존 항목을 보강하거나 스킵한다.
- 변경은 **최소 범위** — 해당 교훈만 반영, 다른 내용 수정 금지.
- 추가하는 텍스트의 **언어는 대상 파일의 주 언어를 따른다**. 파일이 영어면 영어로, 한국어면 한국어로 작성한다.

## CLAUDE.md 동기화

- rules 파일 수정 후, `~/.claude/CLAUDE.md`의 해당 섹션도 동일하게 업데이트한다.

## 출력 형식

변경 완료 후 다음을 보고한다:

```
## Lesson Global 반영 완료

- **교훈**: (1줄 요약)
- **대상 파일**: rules/XX-xxx.md
- **변경 위치**: RN) 섹션명
- **변경 내용**: (추가/수정된 규칙 요약)
```
