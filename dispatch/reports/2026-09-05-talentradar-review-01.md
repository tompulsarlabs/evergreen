# Report — 2026-09-05-talentradar-review-01

Produced by the frontier/openai lane, 7.8 wall-minutes.

# PR #1 adversarial review

Reviewed the workspace’s recorded PR head `6e510c3eebdcbab7572118fbf09bf3f553349029` against `main` at `4633ba08303c1ebc2c87747809627171486acae2`. The `code-review` skill was not installed. Network access was unavailable to refresh the PR ref.

## Findings

### 1. [P1] A public anon key authorises service-role mutations

**Location:** `supabase/migrations/20260903231000_fetch_schedule.sql:7`, `supabase/functions/fetch-jobs/index.ts:163`

The scheduler deliberately uses the Supabase anon key. Default JWT verification accepts that publicly distributable credential, while the handler performs no further authorisation before using its module-wide service-role client. Anyone with the project’s anon key can start runs, supply arbitrary `run_id`/`hop` values, poll third-party boards, and mutate job and verification state. Malformed JSON and non-POST requests also become new runs because parse failures are treated as `{}`.

**Proposed fix:** Require POST and validate the request body, then authenticate a separate high-entropy scheduler secret stored in both Vault and the Edge Function’s secrets before any database access. Alternatively require and verify a service-role claim, though a dedicated scoped secret is preferable. Add unauthorised, wrong-method, malformed-body, and forged-hop tests.

### 2. [P1] A board losing its final posting leaves every old job open forever

**Location:** `supabase/functions/fetch-jobs/index.ts:114`

`close_vanished_jobs` only runs when `result.jobs.length > 0`. A structurally valid `200` response containing an empty jobs collection therefore never closes the board’s previous jobs. Once the last vacancy disappears, stale roles remain `open` indefinitely and continue feeding downstream scoring and UI queries.

**Proposed fix:** Distinguish a valid empty board from an invalid/moved response. After structural validation, close missing jobs on an empty response, optionally after two consecutive successful empty polls if a safety buffer is desired. This only changes job status; it need not alter pipeline rows. Add a regression covering one posting followed by a valid empty board.

### 3. [P1] Silently dropped records can cause legitimate jobs to be closed

**Location:** `supabase/functions/_shared/adapters/greenhouse.ts:43`, `supabase/functions/_shared/adapters/greenhouse.ts:48`, `supabase/functions/fetch-jobs/index.ts:117`

All adapters silently skip records without the expected ID/title and return `[]` for an unexpected top-level shape. If a response contains nine valid jobs and one temporarily malformed job, the poll is treated as successful and non-empty; the omitted job key is then passed to `close_vanished_jobs`, closing the previously valid posting. The tests currently codify malformed input as an empty result rather than an incomplete/error result.

**Proposed fix:** Return parse metadata such as raw count, accepted count, rejected count, and completeness. Treat unexpected shapes or rejected elements as an incomplete poll and prohibit closure for that company. Validate external timestamps and field types before persistence. Add mixed-validity payload tests that prove no closure occurs.

### 4. [P1] A company is marked complete before its jobs are safely persisted

**Location:** `supabase/functions/fetch-jobs/index.ts:83`, `supabase/functions/fetch-jobs/index.ts:191`

`recordVerification` updates `last_polled_at` before `persist` begins. Persistence then performs one RPC per job and can fail partway through. If an RPC fails or the worker is killed after the timestamp update, the company is excluded from the remainder of that run even though only part—or none—of its response was saved. The stalled-run sweeper cannot repair this because it also relies on `last_polled_at`.

**Proposed fix:** Persist an entire validated board through one transactional bulk RPC, including closure and the successful-poll timestamp. Track `last_attempted_at` separately for HTTP failures so the queue can advance without claiming persistence succeeded. Add injected mid-board failure and killed-hop recovery tests.

### 5. [P1] The Radar UI does not consume the live fetch layer

**Location:** `src/lib/board.ts:5`, `src/lib/board.ts:13`, `src/app/page.tsx:64`

`buildRadar` reads `seed/radar.csv`, contacts, and pipeline CSV files exclusively. No UI path queries Supabase. Consequently the fetched jobs, job-source breadth, current scores, closures, and run health never appear in the Radar, and the deployed UI still tells the user that nothing has been polled. `src/lib/seed.ts:163` also returns every historical seed row while `src/app/page.tsx:17` labels the entire count “new.”

**Proposed fix:** Replace the seed-backed board repository with an async server-only Supabase repository querying open talent jobs plus companies, sources, current scores, pipeline, and contacts. Move remaining manual/network sightings into the same tables or explicitly merge them by canonical key. Derive poll state from `runs`/`job_sources`, and either filter “new” to the documented 24-hour window or relabel it. Add repository contract and rendered-page tests using fetched database fixtures.

### 6. [P2] The database cannot populate the UI contract without invented defaults

**Location:** `src/lib/types.ts:57`, `src/lib/types.ts:11`, `supabase/migrations/20260903170000_init_talent_radar.sql:85`, `supabase/migrations/20260903170000_init_talent_radar.sql:182`

`RadarRole` requires work mode, sponsorship, LinkedIn presence, signals, and `seenBy`, but the fetch result and `jobs` schema do not provide those fields. The database score model also permits `reject`, while the UI `Band` type cannot represent it. The UI expects to recompute geography and edge value, although some required enrichment inputs are absent and the database already stores audited values for those dimensions.

Role identity is also incompatible with live data: `src/lib/seed.ts:137` derives IDs from company plus title, and `src/components/RadarBoard.tsx:102` uses the same pair as its key. Two postings with the same title at one company but different locations collide, and `src/lib/board.ts:36` resolves both links to the first match.

**Proposed fix:** Define a canonical `radar_items` view/RPC or typed mapper. Decide which stored score fields are authoritative, add structured enrichment fields needed for dynamic recomputation, explicitly support or exclude rejected jobs, and use `jobs.id` or `job_key` for routes and React keys. Test duplicate titles across locations and every score band.

### 7. [P2] The oversized-board guard runs after the expensive work it is meant to prevent

**Location:** `supabase/functions/_shared/poll.ts:83`

The response is fully materialised and every posting is normalised and SHA-1 hashed before the 1,000-posting limit is checked. A large aggregator can therefore exhaust memory or CPU before reaching the guard, reproducing the failure described in the handoff. Because the limit uses the accepted normalized count, malformed/skipped records can also let an oversized raw board pass.

**Proposed fix:** Have adapters expose and validate the raw collection before transformation, reject excessive raw counts before hashing descriptions, and enforce a response-byte limit where possible. Add a test proving adapter parsing is not invoked for an oversized collection.

### 8. [P2] Fetch orchestration assumes runs and hops never overlap

**Location:** `supabase/functions/fetch-jobs/index.ts:48`, `supabase/functions/fetch-jobs/index.ts:143`, `supabase/migrations/20260903234000_hops_from_the_database.sql:48`

Every request without `run_id` creates a new run, and `dueCompanies` selects rows without claiming or locking them. Concurrent cron/manual/retried invocations can poll the same companies. The SQL upsert first selects and then inserts rather than using an atomic conflict path, so concurrent first sightings can race into a unique violation and trigger the partial-persistence problem above.

**Proposed fix:** Enforce one active fetch run, atomically claim per-run company work with a database function (`FOR UPDATE SKIP LOCKED` or an explicit run-company queue), make hop requests idempotent, and implement job creation with `INSERT ... ON CONFLICT ... DO UPDATE`. Add overlapping-run and duplicate-hop integration tests.

### 9. [P2] One 404 permanently removes a previously healthy board

**Location:** `supabase/functions/_shared/poll.ts:155`, `supabase/functions/fetch-jobs/index.ts:53`

A single `http 404` changes verification to `broken`; `dueCompanies` never selects broken boards again. A transient CDN/routing failure or temporary ATS response can therefore disable polling permanently with no automatic recheck.

**Proposed fix:** Track consecutive failures and last successful verification, require repeated 404s before demotion, and periodically reverify broken tokens. Preserve the immediate error in the run record. Test state transitions for transient and repeated 404s.

### 10. [P2] The migration overwrites shared-project PostgREST configuration

**Location:** `supabase/migrations/20260903232000_service_role_access.sql:24`

The project is documented as an existing shared Supabase project, but this statement replaces `authenticator`’s complete exposed-schema list with exactly three schemas. Any other custom schema previously exposed by another application is silently removed.

**Proposed fix:** Preserve and append to the existing schema configuration, or make the required dashboard/API configuration an explicit preflight that refuses to proceed when it would remove schemas. Add a migration test starting with an additional exposed schema.

### 11. [P2] CI does not exercise the deployed handler or database behaviour

**Location:** `.github/workflows/ci.yml:30`, `tests/poll.test.ts:39`, `tests/sql.test.ts:1`

The tests cover pure adapters and polling helpers, while the edge handler’s auth, request parsing, persistence ordering, scheduling, and error paths are untested. The SQL suite tests only string quoting; no migration or RPC is applied to Postgres. This leaves the most consequential paths unprotected despite the handoff documenting multiple failures found only after deployment.

**Proposed fix:** Extract an injectable handler factory for unit tests and add a local Supabase/Postgres CI job that applies all migrations from scratch. Cover authorisation, valid/invalid payloads, empty and partial boards, atomic upserts, closure, concurrent calls, hop resumption, permissions, and preservation of shared configuration.

## Confirmed sound

- `supabase/functions/_shared/poll.ts:69` constructs Tier-1 requests through escaped adapter endpoints, sends the identified user agent, applies a timeout, polls sequentially with a gap, and contains ordinary HTTP/network/parser failures per board.
- `supabase/functions/_shared/talent-filter.ts:38` retains non-talent postings with a flag rather than deleting them, which makes filter mistakes auditable.
- `supabase/migrations/20260903170000_init_talent_radar.sql:327` enables RLS and revokes schema access from `anon` and `authenticated`; the object-level service-role-only database boundary is sound independently of the Edge Function endpoint issue above.
- `src/components/RadarBoard.tsx:27` keeps browser-side filtering/search isolated from server-only loading and operates on serialisable view models.
- `git diff --check` passed, the worktree remained unchanged, and every path referenced above exists on the recorded PR head.

## Verification limitation

The PR test suite was not rerun because the read-only workspace is checked out at the base commit, has no dependencies installed, and cannot check out or materialise the PR tree. Review and path verification were performed directly against Git objects. No files, commits, or remote state were modified.
