# Changelog

## v2 — 2026-08-24

The agent has a name: **Ivy** (repo renamed evergreen → ivy; bot identity now
`ivy-bot <bot@ivy.invalid>`, historical `bot@evergreen.invalid` commits remain
valid non-counting bookkeeping). Same system, same rules. Also in v2: Phase 4
local-WIP pipeline (launchd scanner → local-wip.json, 36h staleness rule),
narrative reframe (agentic DevOps daily-shipping), tomgreen.ai now public and
tracked.

## v1 — 2026-08-23

Ladder live: four cloud routines (scout 09:00 / check 18:00 / failsafe 22:30 daily,
retro Sun 10:00, Berlin). Two forced failsafe test runs mapped the cloud sandbox:
all github.com egress is repo-scoped, so verification there goes through the
built-in GitHub MCP tools (playbook ops note); check.sh keeps GraphQL + public-HTML
paths for local/unproxied use. Nudge channel: PushNotification (verified reaching
mobile from cloud), calendar event as fallback. Attribution model enforced:
bot-authored bookkeeping, connected-author journal/work commits only.

## v0 — 2026-08-23

Initial scaffold: design doc, playbook (immutable counting/verification/no-synthetic
rules + tunable ladder), config, state, check script, first journal entry.
Phases 2–3 (cloud routines, weekly retro) pending.
