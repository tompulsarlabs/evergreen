# Evergreen

A self-learning daily loop that keeps the [`tompulsarlabs`](https://github.com/tompulsarlabs)
contribution graph green — by getting real work shipped first, and guaranteeing the
floor with a genuine daily journal entry when it isn't.

No empty commits, no backdating, no synthetic noise.

- **[DESIGN.md](DESIGN.md)** — full architecture, GitHub counting-rule constraints,
  escalation ladder, failure modes.
- **[playbook.md](playbook.md)** — the routines' operating instructions. The weekly
  retro edits the tunable sections (`learn:` commits, version tags); immutable
  sections require a human commit.
- **[config.yml](config.yml)** — timezone, schedule, watchlist rules, commit identity.
- **[state.json](state.json)** — streak and per-day outcomes (machine-readable).
- **[journal/](journal/)** — one entry per day: candidates, what happened, streak.
- **[scripts/check.sh](scripts/check.sh)** — the authoritative "is today green?"
  check (GraphQL `contributionsCollection`).

This repo's git history is the system's learning record: `journal:` entries,
`learn:` adjustments, `config:` changes — every behavior change is a readable,
revertible diff.
