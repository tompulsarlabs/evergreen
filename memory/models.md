---
subject: execution-lane routing evidence
type: evidence
updated: 2026-08-30
---

# Models: lane × task-class outcomes

Routing evidence for the dispatch layer ([[ops]] for environment limits;
policy lives in `playbook.md` and `config.yml`, never here). One row per
**verified** contract — claimed-done never lands on this page. Quota events
(throttles, refusals) are observations too: record them per pool.

## Verified outcomes

| Contract | Type | Lane / pool | First-pass | Wall min | Note |
|----------|------|-------------|------------|----------|------|
| 2026-08-27-ivy-nudge-audit-01 | chore | workhorse / anthropic | yes | 8 | Memory reconciliation; interactive D1 manual run [cite:2026-08-27] |

## Pool health

No throttle or refusal events recorded on either pool yet [cite:2026-08-27].

## Fleet metrics (weekly, retro-computed)

| Week ending | Verified done | Failed / waste min | Expired | Throttles | Note |
|-------------|--------------|--------------------|---------|-----------|------|
| 2026-08-28 (partial) | 1 | 0 / 0 | 0 | 0 | D1-D2 bring-up week; first contract 8 wall-min first-pass [cite:2026-08-27] |
| 2026-08-30 | 1 | 0 / 0 | 0 | 0 | No new verified outcomes this week — 3 contracts still queued unclaimed, D2 runner not yet live [cite:2026-08-29][cite:2026-08-30] |

## Reading

n=1 still — no routing signal yet, and no waste to eliminate either (0
failed, 0 expired). Per the Pareto rule, no lane move is warranted: nothing
has reached the ≥3-verified-outcomes bar. The binding constraint is
execution capacity (D2 runner), not lane policy — a config change here
would not move the number. Comparative evidence still arrives only once the
D2 runner executes the queued openai-pinned review contract
(`2026-08-27-c2cm-review-01`) [cite:2026-08-27].

## Changelog

- 2026-08-30 (retro) — weekly fleet-metrics row added; still n=1, still no
  lane move (Pareto bar unmet); flagged runner capacity, not policy, as the
  binding constraint.
- 2026-08-27 — page created with the D1 proof contract as first entry.
