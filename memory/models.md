---
subject: execution-lane routing evidence
type: evidence
updated: 2026-09-02
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
| 2026-08-27-c2cm-review-01 | review | frontier / openai | yes | 9.7 | D2 runner's first live execution (2026-09-01); six real findings, request-changes verdict [cite:2026-09-02] |
| 2026-09-02-countersign-review-01 | review | frontier / openai | yes | 9.6 | Second D2 execution; keep-in-draft verdict, late-webhook race as top finding [cite:2026-09-02] |

## Pool health

No throttle or refusal events recorded on either pool yet [cite:2026-08-27].

## Fleet metrics (weekly, retro-computed)

| Week ending | Verified done | Failed / waste min | Expired | Throttles | Note |
|-------------|--------------|--------------------|---------|-----------|------|
| 2026-08-28 (partial) | 1 | 0 / 0 | 0 | 0 | D1-D2 bring-up week; first contract 8 wall-min first-pass [cite:2026-08-27] |
| 2026-08-30 | 1 | 0 / 0 | 0 | 0 | No new verified outcomes this week — 3 contracts still queued unclaimed, D2 runner not yet live [cite:2026-08-29][cite:2026-08-30] |

## Reading

n=3 now (1 chore, 2 review), all first-pass, all frontier/openai or
workhorse/anthropic — still short of the ≥3-verified-outcomes-per-class bar
the Pareto rule requires before any lane move, since the two new outcomes
are both `review`/frontier/openai rather than adding depth to a different
class. Zero waste so far (0 failed, 0 expired) among *verified* contracts;
today's four tomgreen.ai build contracts that failed at the attribution
gate and were returned to `queue/` (not `failed/`, no worker claimed, no
budget spent) are a runner-reliability incident, not routing waste — see
[[ops]] for the stale-checkout/PATH root causes, fixed same day
[cite:2026-09-02].

## Changelog

- 2026-09-02 — both queued review contracts verified done (request-changes
  on c2-client-matrix, keep-in-draft on countersign); n=1→3, still under
  the per-class Pareto bar.
- 2026-08-30 (retro) — weekly fleet-metrics row added; still n=1, still no
  lane move (Pareto bar unmet); flagged runner capacity, not policy, as the
  binding constraint.
- 2026-08-27 — page created with the D1 proof contract as first entry.
