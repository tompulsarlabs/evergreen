# Cloud verification and scheduling reference

Read when checking contributions or changing routine schedules.

**Ops note (cloud environment, mapped live 2026-08-23, two test runs):** the routine
sandbox has no `gh` preinstalled and ALL github.com egress is proxy-scoped to this
repo — GraphQL is blocked, unscoped REST is blocked, and even the public
contributions HTML 403s ("sessions are bound to their configured repositories").
`scripts/check.sh` therefore exits 2 (no signal) in the cloud; that is expected,
never a reason to guess. What works: (1) git push/pull to this repo via the
credential proxy; (2) the **built-in GitHub MCP tools** (`mcp__github__*`, load via
ToolSearch), which are user-scoped — `get_me` confirms identity, `list_commits` reads
this repo, and `search_commits` / `search_issues` / `search_pull_requests` see
cross-repo activity. Don't waste run time installing or authenticating `gh`.

**Cloud verification path (when check.sh exits 2):** today is GREEN if any of:
(a) `mcp__github__list_commits` on this repo shows a commit on `main` today
(Europe/Berlin) whose author email is the connected `commit_email`;
(b) `mcp__github__search_commits` finds commits by `author:tompulsarlabs` today
(search covers default branches only, matching counting rule 1 — ignore hits in
forks);
(c) `search_issues` / `search_pull_requests` show an issue or PR opened by
`tompulsarlabs` today.
Bot-authored commits (`bot@ivy.invalid`; historical `bot@evergreen.invalid`) NEVER
count as green — they don't light the graph. If the MCP tools are also unavailable, ALERT; never guess.
Note search indexing can lag a fresh push by a minute — prefer (a) for verifying a
failsafe commit you just made.

**Ops note (DST):** cron schedules are pinned in UTC (07:00 / 16:00 / 20:30). When
Berlin flips CEST→CET in late October, local fire times shift to 08:00 / 17:00 /
21:30 — a safe direction (failsafe moves *earlier*). The retro nearest the flip
should re-pin the UTC crons if the original local times matter.
