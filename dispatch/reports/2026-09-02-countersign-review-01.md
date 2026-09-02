# Report — 2026-09-02-countersign-review-01

Produced by the frontier/openai lane, 9.6 wall-minutes.

# PR #1 review — REBUILD.md

Contract: `2026-09-02-countersign-review-01`  
PR: [tompulsarlabs/countersign#1](https://github.com/tompulsarlabs/countersign/pull/1)  
Head: `4bdfd15d0240ff06787effc6a91ee68c247e75aa`  
Base/current main: `b1f1c0f1221bca793def150d0c981ee79a7d6589`

## Verdict

Keep the PR in draft.

There is no intervening code drift: current main is still the prototype commit against which `REBUILD.md` was written. The document closely matches the happy-path implementation of vendors, numbering, threshold routing, status transitions, audit entries, and the Board/Finance screens.

It is not yet a dependable rebuild specification, however. Several retry, validation, configuration, and failure-path claims are false or incomplete.

## Findings

### High — Late webhooks can affect a new approval round after reopen

`REBUILD.md:264-270` promises harmless, audited late deliveries, while `REBUILD.md:274-277` clears `envelope_id` during reopen and `REBUILD.md:315-318` prescribes the stable ID `mock-env-<poId>`.

The implementation follows this combination:

- `src/lib/signature.ts:23-31` generates the same envelope ID on every submission of a PO.
- `src/lib/service.ts:249-260` clears the old association and approvals.
- `src/lib/service.ts:177-192` rejects an unresolvable old envelope rather than auditing it as ignored.
- `src/lib/service.ts:156-163` restores the reused ID after resubmission.

Before resubmission, a prior-round delivery returns an error with no audit trace. After resubmission, that same delivery can sign or decline a fresh approval row. This directly contradicts `REBUILD.md:593`.

Require a unique envelope identity per approval round and retain enough retired-envelope history to recognize and ignore late events.

### High — Unsupported or missing webhook events are processed as signatures

The documented contract describes `signed` and `declined` (`REBUILD.md:251-263`, `REBUILD.md:335`, `REBUILD.md:387`), but the route passes unvalidated JSON directly to the service (`src/app/api/webhooks/signature/route.ts:8-14`).

The TypeScript union at `src/lib/service.ts:170-175` provides no runtime protection. The implementation checks only whether the value is exactly `"declined"`; every other value follows the signed branch (`src/lib/service.ts:195-207`). A missing event or an event such as `"viewed"` can therefore sign a PO when the envelope and approver are valid.

Require runtime validation of all webhook fields and rejection of any event outside the exact enum, with a negative acceptance test.

### High — The advertised real-provider webhook verification cannot use the specified interface

`REBUILD.md:295-322` says a real provider requires changing one exported constant and will perform a signature-header check. However, `verifyWebhook(payload)` receives only a parsed payload (`src/lib/signature.ts:15-20`), and the route supplies neither request headers nor raw body bytes (`src/app/api/webhooks/signature/route.ts:8-14`).

The stated header verification is therefore impossible through this contract. The abstraction also lacks a verified normalization step from a provider payload to the internal `{ envelopeId, approver, event, reason? }` event.

Pass headers and raw request bytes into verification and define provider-specific event normalization before claiming a one-file swap.

### Medium — The pre-submit routing preview is not authoritative

`REBUILD.md:439-442` calls the previewed routing consequence crucial. The displayed total, however, is calculated differently from the submitted payload:

- `src/app/new/page.tsx:38-45` totals every row and treats blank or zero quantity as zero.
- `src/app/new/page.tsx:71-77` drops rows with blank descriptions and changes blank or zero quantity to one.
- The service then recomputes routing from that submitted payload (`src/lib/service.ts:124-133`).

For example, a blank-description row can make the preview show `≥ £5,000 / both` and then disappear before submission, producing `< £5,000 / either`. The inverse is possible with a zero quantity that becomes one.

Build one normalized item list and use it for both preview and submission.

### Medium — “Routing is configuration” is not true end-to-end

The central-configuration claim appears at `REBUILD.md:25-28` and `REBUILD.md:109-123`. Server routing correctly reads `ROUTING` (`src/lib/service.ts:131`), but the UI duplicates the values:

- `src/app/new/page.tsx:45,180-185` hard-codes `500_000`, `£5,000`, `RAN`, and `RAF`.
- `src/app/pos/[id]/page.tsx:77-81` hard-codes the threshold wording.

Changing `ROUTING` can make the preview and printed PO disagree with actual routing. The screen contract at `REBUILD.md:439-455` should explicitly require deriving thresholds, approvers, and labels from shared configuration.

### Medium — A reopened PO cannot actually be fixed

`REBUILD.md:231-233` describes a “rejected-then-fixed” PO, and `REBUILD.md:274-277` calls reopening a clean second attempt. In practice:

- `src/lib/service.ts:67-103` only creates drafts.
- `src/lib/service.ts:249-261` only clears approval metadata and changes status.
- `src/app/api/pos/[id]/route.ts:4-7` is GET-only.
- `src/app/api/pos/[id]/actions/route.ts:11-23` exposes no edit operation.
- `src/components/actions.tsx:93-101` can only resubmit the unchanged draft.

Number preservation itself works, but there is no path to change items, memo, vendor, or terms. Add draft editing to the service/API/screen contract or explicitly document reopen as unchanged resubmission and list editing as deferred.

### Medium — Provider lifecycle failures are unspecified and can strand POs

Submission commits the number, approvals, audit rows, and `awaiting_signature` state before awaiting envelope creation (`src/lib/service.ts:108-165`). If the provider call fails, the PO remains awaiting signature with no envelope. Signer controls require an envelope (`src/app/pos/[id]/page.tsx:116-123`), resubmission fails the draft-only guard, and the remaining UI recovery is cancellation (`src/components/actions.tsx:93-117`).

A crash after provider creation but before `envelope_id` persistence creates the inverse inconsistency. Additionally, the provider interface has no cancellation/void operation (`src/lib/signature.ts:15-20`), while reopen and cancel only mutate local state (`src/lib/service.ts:249-269`).

`REBUILD.md:295-322`, `REBUILD.md:334`, and `REBUILD.md:540-541` need idempotent creation, retry/reconciliation, and envelope-revocation semantics—or a narrower swappability claim.

### Medium — The audit guarantee is not transactionally enforced

The document says nothing mutates without an audit row (`REBUILD.md:39-41`) and every mutation is audited (`REBUILD.md:279-285`, `REBUILD.md:595-596`).

For several operations, the state write and audit insert are separate autocommit statements (`src/lib/service.ts:20-32`), including vendor creation, draft creation, envelope persistence, and standalone schedule/pay/cancel operations (`src/lib/service.ts:41-55`, `src/lib/service.ts:67-102`, `src/lib/service.ts:162-163`, `src/lib/service.ts:232-269`).

The normal happy path produces the described rows, but a crash or failed audit insert can leave a successful mutation unaudited. Couple each mutation and its audit row in one transaction or soften the invariant.

### Medium — Due dates are host-timezone dependent despite the UTC contract

`REBUILD.md:130-132`, `REBUILD.md:256-258`, and `REBUILD.md:594` prescribe UTC dates and signature date plus `netDays`. The implementation uses local-time `getDate`/`setDate` and then slices a UTC ISO value (`src/lib/service.ts:222-225`).

This is DST-sensitive. Under `TZ=Europe/Berlin`, the current algorithm turns `2026-03-29T00:30:00Z + 1 day` into due date `2026-03-29`, rather than `2026-03-30`.

Specify UTC calendar arithmetic or an explicit company business timezone and include a DST-boundary test.

### Medium — Acceptance checks do not prove several load-bearing requirements

The executable sequence at `REBUILD.md:554-583` does not cover much of the checklist at `REBUILD.md:586-599`:

- One PO per vendor cannot verify same-vendor sequencing or concurrency.
- The £1,795 and £7,500 seed values (`src/app/api/dev/seed/route.ts:11-35`) do not test exactly £5,000.
- Steps 7 and 8 are comments, not executable checks.
- Webhook replay is posted but its unchanged state and `webhook:ignored` audit row are not asserted.
- Out-of-order delivery, due dates, complete audit coverage, and print output are not exercised.

Because the opening instruction tells a rebuilding agent to stop at these checks (`REBUILD.md:7-15`), false-positive completion is likely. Add executable assertions for every checklist item, especially the exact threshold, reopening, approval rounds, and malformed/stale webhooks.

### Low — Vendor input behavior is underspecified

Core vendor schema, defaults, and code normalization match (`REBUILD.md:114-143`, `REBUILD.md:350-358`; `src/lib/config.ts:4-15`, `src/lib/schema.ts:7-15`, `src/lib/service.ts:41-57`).

Minor omitted behavior includes alphabetical listing and persisted-name trimming (`src/lib/service.ts:37-49`). More importantly, neither the spec nor implementation constrains `netDays` to a sensible non-negative integer (`src/lib/service.ts:41-50`, `src/lib/service.ts:67-88`), although it drives due-date arithmetic. Missing or non-string name/code values also throw before the promised friendly validation because normalization precedes the guard (`src/lib/service.ts:42-43`).

Document the input constraints and require boundary validation.

### Low — Small self-containedness and UI discrepancies remain

- The file tree omits `src/lib/signature.ts` (`REBUILD.md:74-101`), despite section 8 requiring it and the implementation containing it (`src/lib/signature.ts:1-35`).
- `REBUILD.md:35` says “Three screens,” while `REBUILD.md:81-84`, `REBUILD.md:426-475`, and `src/app/pos/[id]/page.tsx:8` identify four page routes including PO detail.
- `REBUILD.md:441-442` promises vendor net terms in the New PO footer, but inline-created vendor terms are suppressed by the existing-vendor condition at `src/app/new/page.tsx:185`.
- The clean-print claim (`REBUILD.md:467-468`, `REBUILD.md:599`) is not guaranteed under dark preference because print rules do not reset the dark `--surface` tokens used by `.podoc` (`src/app/globals.css:20-40`, `src/app/globals.css:132-158`).

## Confirmed alignment

The following areas accurately reflect the current implementation:

- Vendor schema, defaults, configuration, and normal code sanitation.
- Transactional per-vendor numbering, zero-padding, and preserving an existing number on resubmission (`REBUILD.md:223-249`; `src/lib/service.ts:108-153`).
- `>= 500_000` routing, creation of both approval rows, and `not_required` handling on the happy path (`REBUILD.md:235-259`; `src/lib/service.ts:124-153`, `src/lib/service.ts:206-227`).
- Happy-path signed/declined processing, immediate `signed → with_finance`, schedule/pay/reopen/cancel guards, and actor selection (`REBUILD.md:187-215`, `REBUILD.md:251-291`; `src/lib/service.ts:170-269`).
- Board and Finance queue contents, ordering, status display, and actions (`REBUILD.md:426-475`; `src/app/page.tsx:7-52`, `src/app/finance/page.tsx:8-60`, `src/lib/service.ts:298-324`).
- PO detail, action components, layout, and design tokens are otherwise close transcriptions of the implementation.

## Verification

- GitHub reports PR #1 as open, draft, and mergeable at head `4bdfd15`; it still targets `b1f1c0f`, which remains current main.
- GitHub reports zero submitted reviews, zero discussion comments, and no commit status checks. `created_at` and `updated_at` are both 2026-08-29.
- Using the GitHub MCP at the exact PR head, non-empty content was fetched successfully for `REBUILD.md`, `src/lib/service.ts`, `src/app/api/webhooks/signature/route.ts`, and `src/app/page.tsx`, satisfying the requested path spot-check.
- The PR changes only `README.md` and `REBUILD.md`; `git diff --check` is clean.
- Review was source-level under the contract’s read-only rule. No dependencies were installed and no application/database writes were performed.

## Recommendation

Resolve the three high-severity webhook/provider issues and the medium correctness/acceptance gaps before marking ready for review. The document can then serve as a faithful rebuild contract; currently it is a strong happy-path walkthrough that would reproduce several unsafe edge cases and omit important recovery behavior.
