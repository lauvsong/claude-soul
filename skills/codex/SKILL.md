---
name: codex
description: |
  Codex CLI를 사용하여 코드 분석, 생성, 변환 작업을 수행하는 스킬.
  CLI로 직접 호출하여 토큰을 절약한다.
  Use when: Codex를 활용한 코드 질의/생성/변환이 필요할 때
---

# Codex — CLI 기반 코드 AI 도우미

Codex CLI(`codex exec`)를 사용하여 코드 관련 작업을 수행한다.

## 원칙
- non-interactive 모드(`codex exec`)만 사용한다.

## 주요 명령어

### 단건 질의
```bash
codex exec "질의 내용"
```

### 디렉토리 지정
```bash
codex exec "질의 내용" -C /path/to/project
```

### 출력
```bash
# JSONL 이벤트 출력
codex exec "질의 내용" --json

# 마지막 메시지를 파일로 저장
codex exec "질의 내용" -o result.txt
```

### stdin 파이프
```bash
# 파일 내용을 파이프로 전달
cat file.kt | codex exec "이 코드를 분석해줘"

# diff를 전달
git diff | codex exec "이 변경사항을 리뷰해줘"
```

### 코드 리뷰 (내장 서브커맨드)
```bash
codex exec review
```

## 활용 예시
- 코드 리뷰: `git diff | codex exec "리뷰해줘"` 또는 `codex exec review`
- 코드 설명: `cat file.kt | codex exec "이 코드가 뭘 하는지 설명해줘"`
- 코드 생성: `codex exec "JWT 검증 유틸 함수 작성"`
