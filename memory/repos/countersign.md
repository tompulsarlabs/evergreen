---
subject: tompulsarlabs/countersign
type: repo
updated: 2026-09-02
---

# countersign

**Private.** First seen in the 2026-08-26 watchlist sync [cite:2026-08-26].

Private matters for verification: contributions here surface only if the
profile's "private contributions" toggle is on, so a green day resting on
`countersign` alone is not independently confirmable. Every green day so far
has been confirmed by a public repo instead — [[repos/tomgreen.ai]] or
[[repos/ivy]] [cite:2026-08-25][cite:2026-08-26].

## The PO core loop prototype

`b1f1c0f`, 2026-08-26 07:33 CEST — "Countersign prototype: PO core loop with
mock signatures." A substantial, coherent feature commit in one push: vendors,
PO numbering, threshold routing, signature webhook, a status machine with
audit log, and board/queue screens [cite:2026-08-26]. It is the repo's only
recorded commit in the window — one of the 31 non-bot commits that made
2026-08-26 the highest-volume day so far [cite:2026-08-26].

**PR #1** ("Add REBUILD.md: shareable spec to rebuild Countersign from
scratch") opened 2026-08-29 — the scout's flagged candidate landed
[cite:2026-08-29].

## Review contract `2026-09-02-countersign-review-01` — keep in draft

Executed by the frontier/openai lane, 9.6 wall-minutes, against PR head
`4bdfd15` (current main still `b1f1c0f`, the prototype commit — no
intervening drift) [cite:2026-09-02]. Verdict: **keep in draft**.
REBUILD.md matches the happy-path implementation closely, but several
retry/validation/failure-path claims are false or incomplete — most
notably a late-webhook race after a PO is reopened: the mock signature
service reuses the same envelope ID per PO (`src/lib/signature.ts:23-31`),
so a prior-round delivery can silently sign or decline a fresh approval
round after resubmission, contradicting the doc's own audited-and-harmless
claim (`REBUILD.md:264-270`, `593`). Full findings in
`dispatch/reports/2026-09-02-countersign-review-01.md`. Verified true on
the checkable portion (report exists, non-empty, file:line-specific); the
PR-head spot-check itself could not run from this cloud session —
countersign is outside its repo scope [[ops]] — a confirmed environment
constraint, not a gap in the review.

Not directly inspectable from cloud runs — repo-scoped tools reach `ivy` only
[[ops]] — so everything above comes through org-wide `search_commits`/
`search_pull_requests` plus the dispatch report pushed to `ivy`.

## Changelog

- 2026-09-02 — PR #1 opening corrected (was: none opened); review contract
  outcome recorded (keep in draft, late-webhook race as top finding).
- 2026-08-27 — page created from journal 2026-08-26 and `state.json`.
