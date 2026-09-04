---
subject: tompulsarlabs/c2-client-matrix
type: repo
updated: 2026-09-04
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
[cite:2026-08-29][cite:2026-08-30]. It has never been taken.

## Review contract `2026-08-27-c2cm-review-01` — request changes

Executed by the frontier/openai lane 2026-09-01 (the D2 runner's first live
run), 9.7 wall-minutes, against PR head `685c1cd`. Verdict: **request
changes**, all six of the PR's own decisions found partial, incomplete, or
broken against the code. Top finding: visibility is metadata, not
enforcement — `visibility` is optional on `src/types.ts:14,40`, so every
legacy record publishes by default, and the card/drawer/chat/bundle paths
all skip the check regardless (`src/components/ClientCard.tsx:181-271`,
`src/components/DetailDrawer.tsx:85-132`, `api/chat.ts:7-24`,
`src/App.tsx:3-11`). A second finding: filter-choice Sets are captured
before React batches the reset, so European country selection silently
drops all 14 UK clients. Full findings in
`dispatch/reports/2026-08-27-c2cm-review-01.md`. Verified true on the
checkable portion 2026-09-02 (report exists, non-empty, file:line-specific);
the PR-head spot-check itself could not run from this cloud session —
c2-client-matrix is outside its repo scope [[ops]] — a confirmed
environment constraint, not a gap in the review.

The review landed, unread by a human, without moving the PR: still open,
still not converted [[patterns]].

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
try to encode. Revisit if it accumulates further nudges without conversion.
The queued review contract has now executed (request changes, six real
defects) and still hasn't moved it — one more data point toward "nudging
isn't converting this PR," still short of the bar to act on [[patterns]].

## Parked (2026-09-03, effective 2026-09-04)

Tom: "not WIP or something to devote my time to atm — Ivy should be focused
on what creates value" [cite:e7e918b]. Added to `config.yml`
`watchlist.parked`: still watched for counting and attribution, but the
scout no longer proposes it as a candidate, contract, or audit, and
`dispatch-lint.sh` refuses new contracts against it. Cause was exactly the
pattern below — PR #1 as the fallback pick for eight consecutive runs with
zero conversions, one of them a full review contract that still didn't
move it [[patterns]]. Leaves `parked` only by Tom's commit or a retro
`learn:`.

## Changelog

- 2026-09-04 — parked by Tom; no longer a scout candidate. PR #1 and the
  review below stay as the historical record of why.
- 2026-09-02 — review contract `2026-08-27-c2cm-review-01` outcome recorded
  (request changes, six findings); PR still unconverted after the review.
- 2026-08-30 (retro) — reviewed the close/decline question raised
  2026-08-27; decided not to act (n=1 nudge, insufficient signal); logged
  two more fallback-pick exposures (08-29, 08-30) with the same outcome.
- 2026-08-27 — nudge history corrected: 1 recorded nudge confirmed; journal
  "cycles" were scout picks (contract 2026-08-27-ivy-nudge-audit-01).
- 2026-08-27 — page created from journals 2026-08-23→27 and `state.json`.
