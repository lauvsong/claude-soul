# claude-soul

Claude Code 영혼 분실을 대비한 커스텀 설정 백업

## 특징

- **보안 우선** — 원격 쓰기, PR 생성·머지 등 동료에게 노이즈를 줄 수 있는 작업은 대부분 차단
- **묻지 않고 판단** — ask(확인 후 허용) 대신 allow/deny로 처리. 중간에 멈추지 않고 작업이 끝까지 돌아가는 걸 지향
- **가드레일 일원화** — 모든 차단(`Bash` 명령 + `Read/Edit/Write` 파일 접근)은 `guardrail.py` 훅 하나에서 처리. `settings.json` deny는 [미동작 버그](https://github.com/anthropics/claude-code/issues/8961)가 있어 사용하지 않음
- **시크릿 격리** — 토큰은 git-ignored인 `settings.local.json`에서 머신별 관리

## Setup

```bash
git clone https://github.com/lauvsong/claude-soul.git
cd claude-soul && ./install.sh
```

기존 `~/.claude`가 있으면 자동으로 `~/.claude.bak`에 백업합니다.

### 시크릿 설정

`settings.json`에는 토큰을 넣지 않습니다. `~/.claude/settings.local.json`에 env 섹션을 만들어 머신별로 관리하세요.

```json
{
  "env": {
    "GITHUB_HOST": "...",
    "GITHUB_PERSONAL_ACCESS_TOKEN": "..."
  }
}
```

`settings.local.json`은 `.gitignore`에 포함되어 있어 git에 올라가지 않습니다.

### 차단 명령어 추가

`settings.json`과 `guardrail.py`는 Claude를 통한 조회·수정이 불가합니다 (자기 자신의 가드레일을 우회하지 못하도록). 직접 편집해야 합니다.

차단 룰 목록은 [`hooks/guardrail.py`](hooks/guardrail.py)를 참고하세요.

명령어를 추가하려면 `DENY` dict에, 파일 접근을 막으려면 `PROTECTED_FILES` 리스트에 정규식 패턴을 추가합니다.

```python
# Bash 명령 차단
DENY = {
    "my new rule":  r"\bsome-dangerous-command\b",
}

# 파일 접근 차단 (Bash + Read/Edit/Write 모두 적용)
PROTECTED_FILES = [
    r"\.my-secret-file\b",
]
```

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
└── scheduled-tasks/           # 예약 작업
```

## Commands

| 커맨드 | 설명 |
|--------|------|
| `/backup-customs` | `~/.claude/` 설정을 이 레포에 동기화 |
| `/handoff` | 세션 인수인계 문서 생성 |

## Skills

| 스킬 | 설명 |
|------|------|
| `/ask` | 코드 수정 없이 코드베이스 질의응답 |
| `/claude-security-review` | 보안 설정(settings.json, hook, rules) 검수 |
| `/codex` | Codex CLI 연동 (토큰 절약용) |
| `/gh` | GitHub 작업 시 gh CLI 가이드 |
| `/lesson` | 프로젝트 로컬 교훈 기록 |
| `/lesson-global` | 전역 rules에 교훈 반영 |
