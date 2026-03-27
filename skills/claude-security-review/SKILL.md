---
name: claude-security-review
description: |
  Claude Code 보안 설정(settings.json, guardrail.py, rules/)의 빈틈과 일관성을 검수하는 스킬.
  Use when: "보안 검수", "security review", "가드레일 점검", "/claude-security-review" 등
---

# Claude Security Review — 보안 설정 검수

settings.json(Hook 연결), guardrail.py(실행 차단), rules/(정책 선언) 두 계층의 보안 설정을 체크리스트 기반으로 점검한다.
보안 차단은 Hook(guardrail.py) 단일 계층에 위임하며, settings.json의 deny 배열은 사용하지 않는다.

## Workflow

1. 아래 3개 파일을 읽는다 (이 레포의 소스 파일, `~/.claude/` 아님):
   - `settings.json`
   - `hooks/guardrail.py`
   - `rules/01-safety-approvals.md`
2. 체크리스트 항목별로 pass/fail/warn 판정한다.
3. 결과를 표로 출력한다.

## Checklist

### A. settings.json

> 보안 차단은 Hook(guardrail.py) 단일 계층에 위임. deny 배열은 사용하지 않음.

| # | 항목 | 판정 기준 |
|---|------|----------|
| A1 | 시크릿 미포함 | `TOKEN`, `SECRET`, `PASSWORD`, `KEY`, `CREDENTIAL` 등의 값이 없어야 함 |
| A2 | Hook 연결 확인 | PreToolUse에 Bash/Read/Edit/Write 매처가 guardrail.py를 호출하도록 설정되어 있어야 함 |
| A3 | ask 미사용 | allow/deny only 원칙 준수. ask 섹션이 없거나 비어있어야 함 |

### B. guardrail.py

| # | 항목 | 판정 기준 |
|---|------|----------|
| B1 | PROTECTED_FILES 범위 | `settings.json`, `settings.local.json`, `guardrail.py`, `.zshrc` 등 셸 설정 파일이 포함 |
| B2 | DENY — 파괴적 명령 | `rm -rf`, `mkfs`, `dd`, `chmod 777`, `truncate` 패턴 존재 |
| B3 | DENY — Git | `git push --force`, `git push` 패턴 존재 |
| B4 | DENY — 인프라 | `kubectl delete/drain/scale 0`, `helm uninstall/delete`, `docker system prune`, `brew uninstall` 패턴 존재 |
| B5 | DENY — 원격 코드 실행 | `curl\|sh`, `wget\|sh`, `sh <` 패턴 존재 |
| B6 | DENY — 배포 | `npm publish`, `gradle publish` 패턴 존재 |
| B7 | DENY — 시크릿 노출 | `printenv`, `env`, `echo $TOKEN`, `gh auth --show-token` 패턴 존재 |
| B8 | 정규식 유효성 | 모든 DENY/PROTECTED_FILES 패턴이 `re.compile()` 가능 |
| B9 | DENY — 인코딩 우회 방어 | `base64 -d/--decode`, `printf \x`, `xxd -r` 패턴 존재. PROTECTED_FILES 리터럴 매칭을 인코딩으로 우회하는 것을 차단 |

### C. 계층 간 일관성

| # | 항목 | 판정 기준 |
|---|------|----------|
| C1 | Rules ↔ Hook | `rules/01-safety-approvals.md` R2에 명시된 금지 카테고리가 Hook DENY에 실제 구현되어 있음 |
| C2 | 시크릿 노출 방어 | 시크릿 관련 차단이 Hook DENY + PROTECTED_FILES + Rules R1 두 계층에 존재 |

## Output Format

```
## Claude Security Review 결과

| # | 항목 | 결과 | 비고 |
|---|------|------|------|
| A1 | 시크릿 미포함 | ✅ pass | — |
| A2 | Hook 연결 확인 | ✅ pass | — |
| ... | ... | ... | ... |
| B7 | 시크릿 노출 차단 | ⚠️ warn | `cat .env` 패턴 없음 |
| C1 | Rules ↔ Hook | ❌ fail | `npm publish`가 Hook에 없음 |

### 권고사항
- (fail/warn 항목에 대한 구체적 수정 제안)
```

## Rules

- 판정은 반드시 파일 내용 근거로. 추측 금지.
- fail/warn에는 **구체적 수정 제안**을 함께 제시.
- pass 항목도 표에 포함하되 비고는 생략 가능.
- 이 스킬은 read-only. 파일 수정은 사용자 승인 후에만.
