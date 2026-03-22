# claude-soul

Claude Code 영혼 분실을 대비한 커스텀 설정 백업

> [!NOTE]
> 빠른 개발보다 안전한 개발을 우선하도록 설계되었습니다.  
> 가드레일로 인해 동작이 일부 제한될 수 있으며, 업무용에 더 적합합니다.  
> 특히 `Kotlin` + `WebFlux` 기반 백엔드 개발 환경을 기준으로 설계되었으며, 다른 환경에서 사용할 경우 프롬프트와 rule 구성을 검수 후 사용하는 것을 권장합니다.

---

## 철학

- **보안 중심 설계** — 외부 저장소/인프라에 영향을 줄 수 있는 작업은 차단하며, read-only 커맨드만 허용합니다.
- **중단 없는 실행** — ask를 지양하고 allow/deny로 즉시 판단하여, 작업이 중단 없이 끝까지 수행되도록 합니다.
- **가드레일 단일화** — Bash 명령과 파일 접근(Read/Edit/Write)을 모두 [`hooks/guardrail.py`](hooks/guardrail.py)에서 통합 제어합니다.
- **시크릿 분리 관리** — 민감 정보는 git-ignored된 `settings.local.json`에서 관리됩니다.

---

## Guardrails

다음 작업을 최대한 차단합니다:

- **외부 Write 작업** — git push, PR 생성 등
- **Claude 설정 파일 접근/수정** — self-modification 및 권한 상승 방지
- **시크릿 파일 접근**
- **차단 우회 명령어** — `eval`, `sh -c` 등

차단 규칙은 [`hooks/guardrail.py`](hooks/guardrail.py)에서 관리됩니다.  
`settings.json`의 deny 설정으로도 차단 가능하나 미동작 버그([#8961](https://github.com/anthropics/claude-code/issues/8961))로 인해 사용하지 않습니다.

---

> [!WARNING]
> `bypassPermissions: true` 설정 시 PreToolUse 훅이 비동기로 동작하면서  
> `exit code 2` 기반 차단이 정상적으로 적용되지 않는 문제가 있습니다.  
>
> 이로 인해 일부 차단 로직이 우회될 수 있으므로,  
> `bypassPermissions` 옵션은 사용하지 않는 것을 권장합니다.  
>
> 관련 이슈: [#20946](https://github.com/anthropics/claude-code/issues/20946), [#26923](https://github.com/anthropics/claude-code/issues/26923)

---

## Setup

```bash
git clone https://github.com/lauvsong/claude-soul.git
cd claude-soul && ./install.sh
```

기존 `~/.claude`가 있으면 자동으로 `~/.claude.bak`에 백업합니다.

---

### 시크릿 설정

`settings.json`에는 토큰을 넣지 않습니다.  
`~/.claude/settings.local.json`에 env 섹션을 만들어 머신별로 관리하세요.

```json
{
  "env": {
    "GITHUB_HOST": "...",
    "GITHUB_PERSONAL_ACCESS_TOKEN": "..."
  }
}
```

`settings.local.json`은 `.gitignore`에 포함되어 있어 git에 올라가지 않습니다.

---

### 차단 명령어 추가

`settings.json`과 `guardrail.py`는 Claude를 통한 조회·수정이 불가합니다  
(자기 자신의 가드레일을 우회하지 못하도록 하기 위함).

직접 편집해야 합니다.

차단 룰 목록은 [`hooks/guardrail.py`](hooks/guardrail.py)를 참고하세요.

```python
# Bash 명령 차단
DENY = {
    "my new rule": r"\bsome-dangerous-command\b",
}

# 파일 접근 차단 (Bash + Read/Edit/Write 모두 적용)
PROTECTED_FILES = [
    r"\.my-secret-file\b",
]
```

---

## Structure

```
.
├── CLAUDE.md                  # 핵심 정책 요약 (entry router)
├── settings.json              # Permission allow, hooks 등록
├── rules/                     # 상세 룰셋 (00~13)
├── hooks/
│   └── guardrail.py           # 통합 가드레일 (Bash + Read/Edit/Write)
├── commands/                  # 슬래시 커맨드
├── skills/
└── scheduled-tasks/           # 예약 작업 (cron)
    ├── brew-upgrade/          # brew upgrade 자동 실행
    └── github-notification-cleanup/  # merged PR 알림 자동 정리
```

---

## Commands

| 커맨드 | 설명 |
|--------|------|
| `/backup-customs` | `~/.claude/` 설정을 이 레포에 동기화 |
| `/handoff` | 세션 인수인계 문서 생성 |

---

## Skills

| 스킬 | 설명 |
|------|------|
| `/ask` | 코드 수정 없이 코드베이스 질의응답 |
| `/claude-security-review` | 보안 설정(settings.json, hook, rules) 검수 |
| `/codex` | Codex CLI 연동 (토큰 절약용) |
| `/gh` | GitHub 작업 시 gh CLI 가이드 |
| `/lesson` | 프로젝트 로컬 교훈 기록 |
| `/lesson-global` | 전역 rules에 교훈 반영 |

---

## Scheduled Tasks

| 태스크 | 설명 |
|--------|------|
| `brew-upgrade` | `brew upgrade` 자동 실행 |
| `github-notification-cleanup` | merged PR의 GitHub 알림을 자동으로 done 처리 |