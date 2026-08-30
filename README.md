# Ivy

Ivy is a set of scheduled agents that keep my software projects moving, and
that remember what they learn while doing it.

Four cloud routines run each day across 14 repositories:

- **09:00 scout** — reads its memory, finds real work worth doing, writes
  the day's candidates into a journal entry
- **18:00 check** — asks GitHub whether the day counts; if not, sends one
  notification naming one specific action
- **22:30 failsafe** — confirms the day, verifies finished work, folds new
  facts into memory, and writes a genuine engineering note if the day would
  otherwise be empty
- **Sunday retro** — reads a week of outcomes and changes at most two
  things, citing evidence for each

Everything Ivy knows lives in this repo as markdown, JSON, and git history.
Nothing is hidden in a database.

Seven days running: 115 contributions, all from real work. The failsafe has
never had to fire.

## Read next

- **[`OVERVIEW.md`](OVERVIEW.md)** — how the whole system works, what it has
  caught, and what isn't working yet
- **[`DESIGN.md`](DESIGN.md)** — architecture, constraints, failure modes
- **[`dispatch/DESIGN.md`](dispatch/DESIGN.md)** — the executive layer that
  routes work across model providers
- **[`playbook.md`](playbook.md)** — the operating instructions the routines
  actually follow
- **[`setup/SETUP.md`](setup/SETUP.md)** — running it from scratch

## Layout

```
config.yml       schedule, watchlist, lanes, dispatch limits
playbook.md      immutable rules + weekly-tunable behavior
state.json       machine-readable daily outcomes
memory/          knowledge wiki: one page per subject, every claim cited
journal/         one engineering note per day
dispatch/        work contracts and the routing design
routines/        the four cloud routine definitions
scripts/         verification, scanning, and lint tooling
setup/           launchd jobs and install helpers
```

## Status

Experimental, running since 23 August 2026. The Mac dispatch runner is
installed but has not yet executed a contract — three are queued waiting on
it.
