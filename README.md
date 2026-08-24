# Ivy

Ivy is my personal workflow for keeping small software projects moving.

Four scheduled Claude Code routines run each day:

- scout open work in the morning
- check for activity in the evening
- send one concrete reminder when nothing has moved
- write an end-of-day engineering note when needed

This repository contains Ivy’s configuration, state, journal, local-WIP
scanner, and operating notes. The scheduled routines are configured
outside the repository.

## Status

Experimental. Running since August 2026.

## Repository layout

- `config.yml` — schedule and repository watchlist
- `playbook.md` — routine instructions and guardrails
- `state.json` — daily outcomes
- `journal/` — engineering notes
- `scripts/check.sh` — contribution check
- `scripts/local-wip.sh` — local repository scanner

See `DESIGN.md` for architecture and known limitations.
