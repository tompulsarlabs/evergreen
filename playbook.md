# Ivy Playbook

Operating instructions for Ivy's routines. The weekly retro may edit the
**Tunable** sections (commit as `learn:`, tag a new version). The **Immutable**
sections may only be changed by a human commit.

---

## Immutable: counting rules

A contribution counts on the `tompulsarlabs` graph only if (DESIGN.md §1):

1. Commit lands on the **default branch** (or `gh-pages`).
2. Commit **author email is connected to the account** — use `commit_email` from
   `config.yml`, set explicitly per commit, never inherited from environment git config.
3. The repo is **not a fork**.
4. Private-repo activity shows only if the profile's "Private contributions"
   toggle is on. This repo stays public.

PRs opened, issues opened, and PR reviews also count — treat "review an open PR"
as a first-class candidate.

## Immutable: verification

"Green" is defined by `scripts/check.sh` (GraphQL `contributionsCollection`
for today in `Europe/Berlin`), never by the rendered graph. After any failsafe
commit, re-run the check until today ≥ 1; if it stays 0 after 3 attempts over
15 minutes, alert loudly with the misconfig checklist: email? branch? fork? visibility?

## Immutable: commit attribution encodes intent

Routines run in ephemeral cloud sessions, so all state (journal drafts, state.json,
watchlist changes) must be committed to `main` to survive between runs. To keep
system bookkeeping from lighting the graph as noise:

- **System commits** (scout drafts, state recording, watchlist sync) are authored as
  `ivy-bot <bot@ivy.invalid>` — an unconnected address that never counts.
- **Contribution commits** (the failsafe journal entry, and only that) are authored as
  `commit_name <commit_email>` from `config.yml` — the connected address.

Always set author explicitly per commit (`git -c user.name=… -c user.email=… commit`),
never inherit the environment's git config. The graph therefore reflects exactly one
thing: real work, or the day's genuine journal entry — never the system's own churn.

## Immutable: no synthetic contributions

No empty commits, no backdating, no content-free filler. The failsafe commit is
a real journal entry: today's candidates, what happened, streak state, tomorrow's
top candidate. If journal entries trend content-free, that is a nudging failure
for the retro to fix — not a license to automate noise.

---

## Tunable: the daily ladder

- **Scout (09:00)** — sync watchlist (`gh api user/repos`, minus forks/archived/excludes).
  Gather candidates: open PRs close to merge, assigned issues, branches with recent
  pushes but no PR, yesterday's carry-over. **Also read `local-wip.json`** (pushed by
  the Mac's launchd scanner at 08:45/17:45): repos with `unpushed_commits > 0` or
  `remote: none` are first-class candidates — "push X (N unpushed commits)" is often
  the cheapest real ship of the day. Staleness rule: if its `generated_at` is older
  than 36h, treat local WIP as *unknown* (say so in the journal), never as "nothing
  pending" — a sleeping Mac must not lie to the scout. Draft `journal/<today>.md`
  and commit it **bot-authored** (`scout: <date> — <n> candidates, top:
  <one-liner>`). Silent.
- **Check (18:00)** — run `scripts/check.sh`. Green → record outcome in state
  (bot-authored commit), stay silent. Grey → nudge with the single most concrete
  candidate. Nudge channel: **PushNotification** (verified working from cloud runs
  2026-08-23, "Mobile push requested"). Fallback if PushNotification reports
  not-sent/unavailable: a Google Calendar event ~15 min out titled with the
  candidate. Never both; never anything on a green day.
- **Failsafe (22:30)** — still grey → finalize today's journal entry, commit it
  **Tom-authored** per the attribution rule, push, verify per the immutable rule.
  Record outcome either way — `state.json` gets `{date: {green_by, method,
  contributions: <final count from check>, nudge_sent, nudge_converted,
  failsafe_fired}}` (bot-authored); bump or reset `streak`.

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

## Tunable: retro (Sunday 10:00)

Read the last 7–30 days of `state.json`. Answer: how often did the failsafe fire?
Did nudges convert to real activity within 4 hours? Which repos produced shipped
work? Then make at most two adjustments (nudge time, wording, ranking, excludes) by
editing this file and/or `config.yml`. Commit as `learn: <what> — <evidence>`, tag
the next version, and summarize in `CHANGELOG.md`.

## Tunable: commit message conventions

`journal:` daily entries · `learn:` retro adjustments · `config:` config/scaffold
changes · `scout:` candidate updates worth committing. One-line messages, evidence
in the body when it matters.
