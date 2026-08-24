# Ivy

**Ivy is the agent that keeps Tom's projects moving.** Agentic DevOps for a
working portfolio: every morning Ivy scouts the backlog across every repo (and
the local machine's WIP), stays in the loop with one sharp nudge when the day
stalls, closes the day with a genuine engineering log if nothing shipped, and
tunes its own playbook every Sunday.

The contribution graph is Ivy's heartbeat metric — a green day means something
real moved: a PR merged, an issue closed, a review landed, or the day's
engineering log committed. Never noise: no empty commits, no backdating, no
synthetic activity.

## The daily loop

- **Scout (09:00)** — syncs the project watchlist from the GitHub API and drafts
  the day's shippable candidates: PRs one review from merge, assigned issues,
  branches pushed but never PR'd, unpushed local work, yesterday's carry-over.
- **Check (18:00)** — the day already moved → silent. Otherwise → one push
  notification naming the single most concrete next action, never a generic
  reminder.
- **Failsafe (22:30)** — nothing shipped → the day closes with a genuine
  engineering journal entry (candidates, outcomes, tomorrow's top pick),
  verified end-to-end against the live signal.
- **Retro (Sundays)** — reads the outcome log, tunes its own playbook and config
  with `learn:` commits and version tags. **The git history is the learning
  record** — every behavior change is a readable, revertible diff.

## Map

- **[DESIGN.md](DESIGN.md)** — architecture, constraints, escalation ladder,
  as-built notes from live cloud testing.
- **[playbook.md](playbook.md)** — Ivy's operating instructions: immutable rules
  (verification, attribution, no-synthetic-activity) and the tunable sections
  the retro evolves.
- **[config.yml](config.yml)** — timezone, schedule, watchlist rules, commit identity.
- **[state.json](state.json)** — streak and per-day outcomes, machine-readable.
- **[journal/](journal/)** — one entry per day: what was shippable, what shipped.
- **[local-wip.json](local-wip.json)** — the local machine's dirty/unpushed/no-remote
  repos, scanned twice daily so local work is never invisible.
- **[scripts/check.sh](scripts/check.sh)** — the "did today move?" signal
  (GraphQL, with an auth-free graph fallback).

## Attribution

Ivy's bookkeeping commits are bot-authored (`ivy-bot`) so agent churn never reads
as human activity; only journal entries and shipped work carry the connected
identity. What the graph shows is exactly what moved.

*(Ivy was born as "Evergreen" on 2026-08-23; renamed 2026-08-24. Early history
carries the old name — that's correct historiography, not drift.)*
