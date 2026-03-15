---
name: gh
description: |
  GitHub 작업 시 gh CLI만 사용하도록 안내하는 스킬.
  PR 조회/생성/리뷰, 이슈 관리, 코드 검색, 릴리즈 등 모든 GitHub 작업에 적용.
  Use when: GitHub 관련 작업 요청 시 (PR, issue, review, search, release 등)
version: 1.0.0
---

# gh CLI 전용 GitHub 작업 가이드

## 원칙
- GitHub 관련 모든 작업은 `gh` CLI로 수행한다.
- `gh api`로 REST API 전체에 접근 가능하므로 모든 작업이 가능하다.

## 환경
- GitHub Enterprise: `GITHUB_HOST` 환경변수로 설정됨
- 인증: `GITHUB_PERSONAL_ACCESS_TOKEN` 환경변수 사용

## 주요 명령어 레퍼런스

### PR 작업
```bash
# PR 목록/조회
gh pr list
gh pr view <number>
gh pr view <number> --json title,body,reviews,comments
gh pr diff <number>
gh pr checks <number>

# PR 생성 (HEREDOC으로 body 전달)
gh pr create --title "제목" --body "$(cat <<'EOF'
## Summary
...
EOF
)"

# PR 리뷰 제출
gh pr review <number> --approve
gh pr review <number> --request-changes --body "피드백"
gh pr review <number> --comment --body "코멘트"
```

### 라인별 리뷰 코멘트 (pending review 워크플로우)
```bash
# 1) pending review 생성
gh api repos/{owner}/{repo}/pulls/{number}/reviews \
  -f event=PENDING

# 2) 리뷰에 inline comment 추가
gh api repos/{owner}/{repo}/pulls/{number}/comments \
  -f body="코멘트 내용" \
  -f path="파일경로" \
  -F line=42 \
  -f side=RIGHT

# 3) pending review 제출
gh api repos/{owner}/{repo}/pulls/{number}/reviews/{review_id}/events \
  -f event=COMMENT
```

### PR 코멘트 조회
```bash
gh api repos/{owner}/{repo}/pulls/{number}/comments
gh api repos/{owner}/{repo}/issues/{number}/comments
```

### 이슈 작업
```bash
gh issue list
gh issue view <number>
gh issue create --title "제목" --body "내용"
gh search issues "검색어" --repo owner/repo
```

### 코드/PR/이슈 검색
```bash
gh search code "패턴" --repo owner/repo
gh search prs "검색어" --repo owner/repo
gh search issues "검색어" --repo owner/repo
```

### 파일 내용 조회
```bash
gh api repos/{owner}/{repo}/contents/{path}?ref={branch}
```

### 릴리즈/태그
```bash
gh release list
gh release view <tag>
gh api repos/{owner}/{repo}/tags
```

### 브랜치/커밋
```bash
gh api repos/{owner}/{repo}/branches
gh api repos/{owner}/{repo}/commits/{sha}
gh api repos/{owner}/{repo}/commits?sha={branch}&per_page=10
```

### 기타 API 접근
```bash
# 모든 GitHub REST API 엔드포인트에 접근 가능
gh api <endpoint> [flags]

# GET (기본)
gh api repos/{owner}/{repo}/actions/runs

# POST
gh api repos/{owner}/{repo}/issues -f title="제목" -f body="내용"

# pagination
gh api repos/{owner}/{repo}/pulls --paginate
```

## 금지 사항
- `gh pr comment` — deny 목록에 등록됨 (실수 방지)
- `gh pr merge` — 승인 없이 머지 금지
- `git push` — deny 목록에 등록됨 (별도 승인 필요)
