---
name: github-notification-cleanup
description: GitHub merged PR Done 처리
---

GitHub 알림 inbox에서 merged된 PR 알림을 done 처리해줘.
되묻거나 확인하지 말고 즉시 수행하세요.
gh 스킬을 참고하여 `gh` CLI로만 작업을 수행한다.

  1. PR 알림 조회 - `gh api "notifications?all=true&per_page=100"` 로 조회 (subject.type == "PullRequest")
  2. 각 PR의 merged 여부 확인
  3. merged=true인 알림의 thread를 done 처리
  4. 결과 요약 보고