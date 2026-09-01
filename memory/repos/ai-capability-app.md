---
subject: tompulsarlabs/ai-capability-app
type: repo
updated: 2026-08-30
---

# ai-capability-app

Checked out locally as **`sybil`** — the local-WIP scanner reports it under
that name, so a `local-wip.json` entry for `sybil` and a watchlist entry for
`ai-capability-app` are the same repo [cite:2026-08-25]. Worth knowing before
treating them as two candidates.

## PR #7 — the dormancy-breaking ship

Opened 2026-08-28 08:09 CEST via the Cursor app, not a draft: Cloud Agent
dev-environment config (`.cursor/environment.json` + idempotent
`install.sh`) so a Cloud Agent boots into a working Next.js dev server on
placeholder Supabase env. Fully self-validated before the scout even saw it
(lint clean, build succeeds across 27 routes, all public demo routes 200,
gated route redirects correctly) — first real activity on this repo since
2026-06-23, over two months dormant [cite:2026-08-28]. Scout ranked it the
day's cheapest ship (validated, self-contained, no owner decision blocking
it) and it **merged the same day** [cite:2026-08-28].

Local checkout (`sybil`) remains clean, 0 unpushed commits, `git`-tracked as
dormant since the 06-23 commit despite the merge landing via PR
[cite:2026-08-29].

## Attribution: one uncounted commit, below the nudge bar

The repo carries a genuinely uncounted commit — `24cda31` (2026-06-19),
authored `tom@C2-LAP32-TomGreen.local`, an invented identity from a second
machine with no resolved `author.login` [cite:2026-09-01]. Same failure
class as the `tomgreen.ai` 2026-08-27 incident (this one survived the
2026-09-01 false-alarm review, unlike the `tomgreen.ai` and `talent-scout`
flags [[ops]]) — but
with nothing queued behind it, so it sits below the "nudge immediately" bar
(that bar is for live misconfigurations about to eat *today's* work)
[cite:2026-08-29] [[ops]]. Stays uncountable until someone runs
`procedures/recover-attribution.md` against it.

## PR #4 — a planning artifact, not shipped work

"docs: audit TODOs against codebase" (draft, docs-only). Open since
2026-04-26, no recent activity. It surfaces 8 real bugs with a recommended fix
sequence, which makes it trivially mergeable but substantively empty — merging
it ships documentation of work, not the work [cite:2026-08-24]
[cite:2026-08-25].

The scout has consistently ranked it third of three open PRs for that reason
[cite:2026-08-26][cite:2026-08-27].

## Changelog

- 2026-09-01 — named the actual uncounted commit (`24cda31`,
  `tom@C2-LAP32-TomGreen.local`); confirmed real, not a false alarm.
- 2026-08-30 (retro) — dormancy note pruned (superseded by the PR #7 merge);
  added the shipped-PR and below-the-bar attribution facts from 08-28→29.
- 2026-08-27 — page created from journals 2026-08-24→27.
