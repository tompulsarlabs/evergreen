# Procedures

A task done well once, written down so it never has to be re-derived.

`memory/` records what happened. `procedures/` records **how to do it
again** — enough detail that an agent or a person can execute it from the
file alone, without reconstructing the reasoning from journal history.

The rule for adding one: after finishing something non-obvious that will
recur, write the recipe here the same day, while the details are still
exact. If a memory page ever says "someone should run the same recipe we
used for X", that recipe belongs in this directory.

## What belongs here

- Recurring operational fixes with sharp edges (history rewrites, identity
  repair, force-push recovery)
- Multi-step sequences where the order matters and getting it wrong is
  expensive
- Anything a dispatch contract would otherwise have to re-explain in full

## What does not

- One-off work with no expected repeat
- Behavior rules — those live in `playbook.md`
- Observations and evidence — those live in `memory/`

## Format

Each file states its trigger, its preconditions, the exact commands, how to
verify success, and how to undo. Commands are copy-pasteable. Every claim
about what a step does is something that was actually observed, with a
citation to the journal entry where it ran.

## Index

- [`recover-attribution.md`](recover-attribution.md) — commits authored with
  a disconnected email; fix identity and rewrite history so they count
