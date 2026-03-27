---
name: github-notification-cleanup
description: GitHub 알림 정리 — 내가 리뷰해야 할 open PR만 남기고 나머지 done 처리
---

GitHub 알림 inbox를 정리해줘. 내가 당장 리뷰해야 하는 PR 알림만 남기고 나머지는 전부 done 처리.
되묻거나 확인하지 말고 즉시 수행하세요.
gh 스킬을 참고하여 `gh` CLI로만 작업을 수행한다.

주의: 이 작업은 unread 정리가 아니라 Inbox triage다. 따라서 unread만 조회하면 안 되고, 전체 알림(all=true) 을 기준으로 처리해야 한다.

## 절차

1. 내 GitHub 사용자명 조회 — `gh api user --jq '.login'`
2. 알림 전체 조회 — `gh api --paginate "notifications?all=true&per_page=100"`
   - `all=false`는 unread만 가져오므로 사용하지 않는다.
   - 페이지가 여러 개인 경우를 위해 반드시 `--paginate`를 사용한다.
3. 알림 1차 필터링:
   - `subject.type != "PullRequest"` → done 후보
   - 리뷰 요청 성격이 아닌 알림 → done 후보
   - PR이면서 리뷰 요청 관련 알림으로 보이는 항목만 상세 조회 대상으로 넘긴다.
4. PR 상세 조회 후 최종 판정:
   - PR 상세 정보에서 아래를 확인한다:
     - PR 상태가 open인지
     - `requested_reviewers`에 내 GitHub username이 포함되는지
     - `requested_teams` 중 내가 속한 팀이 포함되는지
   - **남길 것 (skip)**: subject.type == "PullRequest" AND PR이 open AND (내가 reviewer이거나 내가 속한 팀이 reviewer로 지정됨)
   - **done 처리**: 그 외 전부 (closed/merged PR, 내가 reviewer가 아닌 PR, Issue, CI 등 모든 알림)
5. done 대상 알림의 thread를 done 처리 — `gh api -X PATCH "notifications/threads/{thread_id}"`
6. 결과 요약 보고:
   - done 처리된 알림 수 및 목록 (repo/title)
   - 남긴 알림 수 및 목록 (repo/title — 리뷰 필요)
