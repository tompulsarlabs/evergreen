---
subject: tompulsarlabs/c2-client-matrix
type: repo
updated: 2026-08-30
---

# c2-client-matrix

Public. No observed commit activity in the window 2026-08-23→27 — the repo is
dormant apart from one long-open PR.

## PR #1 — the standing candidate that never converts

"Portfolio optimization — 6 decisions from 20 Apr team feedback." Opened
2026-04-21, **not a draft**, 0 comments, no review activity since opening, and
the author's own test plan is already filled in [cite:2026-08-24].

For seven consecutive scout runs it has been the only long-stale non-draft
open PR org-wide, and the scout's fallback "cheapest real contribution
available today" pick whenever fresher work isn't [cite:2026-08-24]
[cite:2026-08-25][cite:2026-08-26][cite:2026-08-27][cite:2026-08-28]
[cite:2026-08-29][cite:2026-08-30]. It has never been taken. Also has a
queued-but-unclaimed review contract (`2026-08-27-c2cm-review-01`), stalled
on the dispatch runner rather than on the candidate itself [[patterns]].

## Nudge history

| Date | Recorded in | Outcome |
|------|-------------|---------|
| 2026-08-24 | `state.json` (push channel) | not converted [cite:2026-08-24] |

Resolved 2026-08-27 (contract 2026-08-27-ivy-nudge-audit-01): the second
and third "nudge cycles" the journals describe [cite:2026-08-26]
[cite:2026-08-27] were scout picks and carry-overs, not sends — the recorded
count of **1 nudge, 0 conversions** is confirmed. Full reconciliation in
[[patterns]].

## Reading

The candidate is cheap by construction (small, ready, self-tested) and
expensive by revealed preference: new work has consistently won over it
[[patterns]]. The 2026-08-27 scout raised the question of whether this PR
should be closed or declined rather than nudged again [cite:2026-08-27].

**Retro decision (2026-08-30):** not closing or declining it, and not
demoting its ranking, yet. The real evidence for "nudging isn't working" is
still 1 nudge / 0 conversions — too thin to act on without risking a
false-negative call on a PR that has simply never had to compete for a
*grey* day. The scout's revealed-preference ranking already deprioritizes it
behind fresh work on its own, which is the behavior a demotion rule would
try to encode. Revisit if it accumulates further nudges without conversion,
or if the queued review contract (`2026-08-27-c2cm-review-01`) executes and
still doesn't move it.

## Changelog

- 2026-08-30 (retro) — reviewed the close/decline question raised
  2026-08-27; decided not to act (n=1 nudge, insufficient signal); logged
  two more fallback-pick exposures (08-29, 08-30) with the same outcome.
- 2026-08-27 — nudge history corrected: 1 recorded nudge confirmed; journal
  "cycles" were scout picks (contract 2026-08-27-ivy-nudge-audit-01).
- 2026-08-27 — page created from journals 2026-08-23→27 and `state.json`.
