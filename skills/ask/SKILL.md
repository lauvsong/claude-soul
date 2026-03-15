---
name: ask
description: 코드 수정 없이 코드베이스에 대한 질의응답을 수행하는 스킬. 코드 구조, 동작 원리, 설계 의도, 의존 관계, 데이터 흐름 등을 분석하고 설명한다. Use when the user asks questions about the codebase such as "이 코드 어떻게 동작해?", "이 클래스 역할이 뭐야?", "이 API 호출 흐름 설명해줘", "이 모듈 의존성 알려줘", "/ask", or any codebase understanding question that does NOT require code changes. Do NOT use when the user wants to modify, fix, refactor, or add code.
---

# Ask — Codebase Q&A (Read-Only)

코드베이스를 읽고 분석하여 질문에 답변한다. 코드를 수정하지 않는다.

## Rules

1. **Read-only**: 절대 파일을 생성/수정/삭제하지 않는다. Edit, Write, NotebookEdit 도구를 사용하지 않는다.
2. **Context mode**: `Analysis/Review` 모드로 동작한다. 빌드/테스트 실행을 강제하지 않는다.
3. **Evidence-based**: 답변에는 반드시 소스 코드 근거(파일 경로 + 라인 번호)를 포함한다.
4. **Secrets safety**: 시크릿/credential 값은 절대 출력하지 않는다.

## Workflow

1. **질문 파악**: 사용자의 질문 의도를 파악한다 (구조/동작/설계/의존성/데이터흐름 등).
2. **탐색**: Glob, Grep, Read 도구로 관련 코드를 탐색한다. 넓은 범위 탐색이 필요하면 Explore 에이전트를 활용한다.
3. **분석**: 코드를 읽고 질문에 대한 답을 구성한다.
4. **답변**: 근거(파일:라인)와 함께 간결하게 답변한다.

## Answer Format

```
### [질문 요약]

[답변 본문 — 간결하게, 코드 스니펫 인용 포함]

**근거**
- `src/main/kotlin/com/example/Foo.kt:42` — 설명
- `src/main/kotlin/com/example/Bar.kt:15-30` — 설명
```

## Tips

- 클래스/함수 역할 질문 → 해당 파일을 읽고 핵심 로직 요약
- 호출 흐름 질문 → 진입점에서 시작해 호출 체인을 추적
- 의존 관계 질문 → import/주입 지점을 Grep으로 탐색
- "왜 이렇게 했는지" 질문 → git log/blame 활용 가능
- 복잡한 탐색 → `Task(subagent_type=Explore)` 활용
