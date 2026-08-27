# Changelog

## v4 — 2026-08-27

**Dispatch D0+D1: the executive layer.** Designed (`dispatch/DESIGN.md`) and
plumbed: scouted candidates become dispatch contracts — markdown+frontmatter
files under `dispatch/`, lint-gated (`scripts/dispatch-lint.sh`), routed
across coarse lanes (frontier/workhorse/fast-cheap) mapped in `config.yml`
onto two flat-rate pools (Anthropic; OpenAI via Codex CLI, models pinned
during D2). Repo is the message bus; execution splits cloud (Anthropic
lanes) / Mac runner (everything else, 09:15–21:00 every 30 min); workers are
untrusted, push draft PRs only, and a contract is done only when the
failsafe's external check verifies it. Guardrails adopted as a new immutable
playbook section — the daily ladder stays senior. Cap 6 contracts/day.
D1 exit criterion met with a real contract (nudge-count reconciliation:
journals had counted scout picks as nudges; confirmed 1 nudge, 0
conversions) run open → done → verified, first evidence row in
`memory/models.md`. D2 next: Mac runner + cross-family review lane.

## v3 — 2026-08-27

**Memory: the knowledge wiki.** Added `memory/` — Markdown pages, one per
durable subject, synthesized over the two layers that already existed
(`journal/` raw sessions, `state.json` outcomes). Pages carry two kinds of
link: `[[page]]` for lateral context, `[cite:<date>]` / `[cite:<sha>]` for
evidence resolving to a journal entry or a commit in this repo. Every run now
orients from `memory/INDEX.md` rather than re-deriving subject context from
day-keyed entries — the gap that let `c2-client-matrix` #1 be re-picked as
"cheapest candidate" four runs running while its unconverted nudge history sat
smeared across four files.

Written on two cadences: the failsafe attaches the day's facts (always *after*
the day is green, so memory can never eat the failsafe window), and the retro
is the only pass that verifies claims, prunes stale context, and logs
deletions. Marked immutable — pages hold observations, never instructions;
behavior stays in `playbook.md`, which only the retro edits. A memory the agent
writes and then obeys is a prompt-injection channel with extra steps.

Also in v3: `scripts/memory-lint.sh` gates every memory commit (frontmatter,
link and citation resolution, orphan pages, index line budget), verified
against each failure mode. `state.json` slimmed 64% by moving verification
narratives into `## Verification` sections of the journal entries they
describe, with a new `cite` key pointing back — schema kept append-only, since
`tomgreen.ai`'s live proof strip consumes this file. Routine prompts unchanged:
the thin-prompt design meant a whole new responsibility needed no cloud
reconfiguration.

Seeded with 10 pages from journals 2026-08-23→27. Design influence:
Perplexity's Brain.

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
