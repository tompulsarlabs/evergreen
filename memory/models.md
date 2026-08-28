---
subject: execution-lane routing evidence
type: evidence
updated: 2026-08-27
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

## Reading

n=1 — no routing signal yet. The first comparative evidence arrives when the
D2 runner executes the queued openai-pinned review contract
[cite:2026-08-27].

## Changelog

- 2026-08-27 — page created with the D1 proof contract as first entry.
