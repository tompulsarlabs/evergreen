# Evergreen

**Agentic DevOps for a working portfolio.** Autonomous agents keep every project
moving and the backlog clearing, daily: scout the work each morning, stay in the
loop with one sharp nudge, ship before the day closes, learn and iterate weekly.

The contribution graph is the heartbeat metric — a green day means something real
moved: a PR merged, an issue closed, a review landed, or the day's engineering log
committed. Never noise: no empty commits, no backdating, no synthetic activity.

## The daily loop

- **Scout (09:00)** — syncs the project watchlist from the GitHub API and drafts
  the day's shippable candidates: PRs one review from merge, assigned issues,
  branches pushed but never PR'd, yesterday's carry-over.
- **Check (18:00)** — the day already moved → silent. Otherwise → one push
  notification naming the single most concrete next action, never a generic reminder.
- **Failsafe (22:30)** — nothing shipped → the day closes with a genuine engineering
  journal entry (candidates, outcomes, tomorrow's top pick), verified end-to-end
  against the live signal.
- **Retro (Sundays)** — reads the outcome log, tunes its own playbook and config
  with `learn:` commits and version tags. **The git history is the learning record**
  — every behavior change is a readable, revertible diff.

## Map

- **[DESIGN.md](DESIGN.md)** — architecture, constraints, escalation ladder,
  as-built notes from live cloud testing.
- **[playbook.md](playbook.md)** — the agents' operating instructions: immutable
  rules (verification, attribution, no-synthetic-activity) and the tunable sections
  the retro evolves.
- **[config.yml](config.yml)** — timezone, schedule, watchlist rules, commit identity.
- **[state.json](state.json)** — streak and per-day outcomes, machine-readable.
- **[journal/](journal/)** — one entry per day: what was shippable, what shipped.
- **[scripts/check.sh](scripts/check.sh)** — the "did today move?" signal
  (GraphQL, with an auth-free graph fallback).

## Attribution

System bookkeeping commits are bot-authored (`evergreen-bot`) so agent churn never
reads as human activity; only journal entries and shipped work carry the connected
identity. What the graph shows is exactly what moved.
