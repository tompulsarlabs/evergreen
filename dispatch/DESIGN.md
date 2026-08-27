# Ivy Dispatch — executive function and cross-provider routing

**Goal:** Ivy grows from a nudge-and-verify loop into an executive: it turns
scouted candidates into *dispatch contracts* — self-contained, verifiable units
of work — routes each to the best execution lane across two flat-rate frontier
pools (Anthropic and OpenAI subscriptions), and learns from verified outcomes
which lanes actually finish work first-pass.

**Stance:** the intelligence lives in the contract, not the router. Verification
is external (git/CI), never a worker's self-report. With flat-rate pools the
scarce resources are **quota liquidity** and **Tom's attention**, not dollars —
route for those. Evidence before policy: no lane rule exists without cited
outcomes behind it.

---

## 1. Architectural decisions

| # | Decision | Chosen | Rejected alternative | Why |
|---|----------|--------|----------------------|-----|
| D1 | Message bus | **The repo.** Contracts are files under `dispatch/`; every state change is a commit | External queue (DB, SQS, webhook service) | Volume is tiny (≤ ~10 contracts/day); git gives audit, replay, and the same bus the rest of Ivy already uses. An external queue is a second source of truth to keep honest |
| D2 | Where execution happens | **Split:** cloud executes Anthropic lanes (`create_session`); the Mac runner executes everything else | All-cloud; all-Mac | Cloud sandbox egress is repo-scoped — it *cannot* reach OpenAI (measured, `memory/ops.md`). The Mac already runs a launchd job (local-wip) and holds all CLI auth. Anthropic lanes stay cloud-dispatchable so the Mac being asleep never blocks Claude-side work |
| D3 | Lane abstraction | **Coarse tiers** (`frontier` / `workhorse` / `fast-cheap`), mapped to concrete (harness, model, settings) in `config.yml` | Per-model knob translation table | Effort/reasoning knobs don't map 1:1 across providers and lineups change monthly. Tiers are stable; the mapping is config data a `learn:` commit can update |
| D4 | Contract format | **Markdown + YAML frontmatter**, lint-gated like memory pages | Pure JSON/YAML | Same format family as `memory/`; readable by humans and every harness; the body carries prose the worker needs, the frontmatter carries state machines |
| D5 | Done-ness | **Two-level:** runner records *claimed done*; only the cloud failsafe's external check makes it *verified done* | Trust worker exit status | Worker output is untrusted by definition; only verified-done feeds routing evidence. This is the existing Ivy verification principle extended to workers |
| D6 | Cost metric | **Outcome proxies per verified-done** (first-pass rate, rework commits ≤24h, retries, wall time) + whatever usage the CLI reports | Token/dollar accounting | Flat-rate pools make marginal dollars ~0; tokenizers don't compare across providers. Throttle events are recorded per pool — quota is the real budget |
| D7 | Worker write access | **Branches + PRs only.** Workers never push to `main` of any repo | Workers commit to main | Keeps counting rules, review, and rollback intact; a bad worker run is a closed PR, not a history rewrite |
| D8 | Routing authority | Scout *assigns* lanes per policy; **only the retro changes policy** (≤2 changes/week, evidence-cited); Ivy never changes its own routines' models (platform contract: human-only) | Per-task self-routing by the worker or scout improvisation | Same observation/instruction split that guards memory: evidence accumulates daily, behavior changes weekly under review |

---

## 2. The unit: a dispatch contract

One file in `dispatch/queue/`, e.g. `2026-08-30-c2cm-review-01.md`:

```markdown
---
id: 2026-08-30-c2cm-review-01
type: review              # build | review | chore | experiment
state: open               # open → claimed → done | failed; expired on timeout
repo: tompulsarlabs/c2-client-matrix
lane: frontier            # tier; config.yml resolves to harness+model+settings
pool: openai              # optional pin (review lane pins the non-author family)
created: 2026-08-30T09:00:00+02:00
created_by: scout         # scout | tom
expires: 2026-09-01T09:00:00+02:00
budget: { wall_minutes: 30 }
---

## Task
Review PR #1 ("Portfolio optimization") on its current head. Adversarial
pass: correctness, unstated assumptions, missing tests. Findings as
file:line with a proposed fix each.

## Definition of done
A findings report exists at dispatch/reports/2026-08-30-c2cm-review-01.md,
each finding tied to file:line, committed and pushed.

## Verification (cloud-checkable)
The report file exists on main of ivy, is non-empty, and every referenced
path exists on the PR head.
```

The runner appends an `outcome:` block on completion (claimed_at, harness,
model, exit, wall_minutes, usage-if-reported, artifacts: branch/PR/report) and
sets `state`. Terminal contracts move to `dispatch/done/` or `dispatch/failed/`
in the same commit. The failsafe later stamps `verified: true|false` after
running the Verification section — that stamp, not the move, is what feeds
`memory/models.md`.

**Claim protocol:** claiming is a commit that sets `state: claimed` + a
timestamp. Two runners racing resolve by git push conflict — the loser pulls,
sees the claim, picks the next contract. A claim older than `budget.wall_minutes
× 3` with no outcome is re-opened by the failsafe (runner died mid-task).

**Attribution gate:** before executing a `build` contract, the runner checks the
target repo's `author_email_ok` (same `git var` check as local-wip). A repo that
would author uncountable commits refuses the contract with a `failed:
attribution` outcome — the 2026-08-27 incident class, made structural.

## 3. Lanes and pools

`config.yml` gains:

```yaml
lanes:
  frontier:
    anthropic: { harness: claude-code, model: claude-opus-5, effort: xhigh }
    openai:    { harness: codex, model: VERIFY }   # pin after checking the tier's CLI lineup
  workhorse:
    anthropic: { harness: claude-code, model: claude-opus-5, effort: medium }
    openai:    { harness: codex, model: VERIFY }
  fast-cheap:
    anthropic: { harness: claude-code, model: claude-haiku-4-5, effort: low }
pools:
  anthropic: { auth: mac-local }    # keys/logins live on the Mac only,
  openai:    { auth: mac-local }    # never in the cloud sandbox
```

Model IDs here are **config data, not design**: the retro updates them with
`learn:` commits as lineups change. `VERIFY` entries block that lane until Tom
confirms what his OpenAI tier exposes to CLI/agent use — a five-minute check,
listed in §10. Pool health is observed, not configured: the runner records
throttle/429 events in outcomes; a pool with a recent throttle makes the scout
prefer the other pool for non-pinned contracts that day.

## 4. Topology — who does what, where

```
             ┌──────────────  tompulsarlabs/ivy (the bus)  ──────────────┐
             │  dispatch/queue/ · dispatch/done/ · dispatch/reports/     │
             │  config.yml lanes · memory/models.md · journal/           │
             └─────────────────────────────────────────────────────────--┘
   cloud (Claude routines)                        Mac (launchd)
   ── scout 09:00: candidates → contracts         ── runner, every 30 min
   ── may spawn Anthropic-lane sessions              09:15–21:00: claim next
      directly (create_session)                      open contract, execute via
   ── check 18:00: + contract states in nudge        the lane's CLI, commit
   ── failsafe 22:30: green first; then             outcome, push
      verify DoDs, synthesize memory             ── holds ALL provider auth
   ── retro Sun: tune lane policy (≤2 changes)    ── enforces budgets/timeouts
```

The executive never executes; workers never decide. The Mac being asleep
degrades gracefully: contracts queue, Anthropic lanes still run via cloud
dispatch, and `expires` + the staleness rule keep a dead queue from lying about
itself (same principle as local-wip's 36h rule).

## 5. Routing policy and evidence

- **Policy** (playbook, tunable): task-class → tier defaults. Starting policy:
  effort before tier (drop `frontier→workhorse` by lowering effort first);
  one workhorse per project per task-class — no per-task provider coin-flips
  (context and cache continuity beat marginal fit); review contracts pin the
  **non-author** family for uncorrelated findings; `chore` → fast-cheap.
- **Evidence** (`memory/models.md`, observations-only, cited to contract ids):
  first-pass rate, rework, wall time, throttles — per lane × task-class × repo.
- **Experiments:** an `experiment` contract runs the same task through two
  lanes (flat rate makes the duplicate free) and records the diff. Capped at
  one per week — deliberately manufactured evidence, not noise.
- The retro reads the evidence page and moves policy — never the scout, never
  a worker, never a memory page.

## 6. The first lane: cross-family review

Smallest full-loop proof, highest standalone value: every open non-draft PR
whose head changed since its last report gets a `review` contract pinned to the
family that did *not* author it. Findings land in `dispatch/reports/`; the
scout surfaces new reports next morning; triage stays with Tom (or a Claude
session he opens). Review is near-stateless — no project-cache forfeiture, no
write access needed beyond the report file — so it exercises contract, runner,
verification, and evidence with the lowest blast radius.

## 7. Guardrails (immutable once adopted into playbook)

1. **Workers are untrusted.** Verified-done comes only from the cloud check of
   the contract's Verification section. Worker branches merge via PR, never
   direct to main.
2. **Contracts are lint-gated** (`scripts/dispatch-lint.sh`: frontmatter
   schema, known repo, known lane, DoD + Verification present, expiry sane).
   The runner refuses non-clean contracts and contracts authored by anyone
   but scout/Tom commits.
3. **Policy changes are retro-only**, evidence-cited, capped — same regime as
   every other behavior change.
4. **Provider auth never enters the cloud sandbox.** Keys live on the Mac;
   the bus carries contracts and outcomes, never credentials.
5. **Ivy's own four routines keep their human-set model** (platform contract).
   The executive routes workers, never itself.
6. **The daily ladder is senior.** Dispatch never delays or replaces a
   ladder duty: the failsafe secures the day (green determination, journal,
   streak) *before* touching contract verification, exactly as it already
   does for memory synthesis — a hung or failing dispatch step can cost that
   day's routing evidence, never the streak. The scout's candidate list and
   nudge remain complete and correct even when every lane is down.
7. **No synthetic work.** A contract exists because a candidate is real;
   `experiment` duplicates are capped and marked. Dispatch volume is never a
   goal — verified-done is.

## 8. Failure modes

| Failure | Mitigation |
|---------|-----------|
| Mac asleep / runner dead | Contracts queue and expire honestly; Anthropic lanes cloud-dispatchable; stale claims re-opened by failsafe |
| Double execution | Claim-commit race resolves via git push conflict; loser re-pulls |
| Worker produces garbage | Branch+PR only; verification external; failed verification = `verified: false` evidence, PR closed |
| Prompt injection via contract body | Runner executes only lint-clean contracts from scout/Tom commits; workers get the contract + a scoped checkout, never Ivy's playbook authority |
| Provider throttled/down | Throttle recorded per pool; scout prefers the healthy pool; pinned contracts wait |
| Uncountable worker commits | Attribution gate refuses build contracts in repos with `author_email_ok: false` |
| Routing table overfits (n too small) | Policy changes require cited evidence; experiments manufacture comparisons; retro cap limits churn |
| Runaway usage against quota | Per-contract wall-clock budgets; runner window 09:15–21:00; daily contract cap in config |

## 9. Build phases

| Phase | Scope | Exit criterion |
|-------|-------|----------------|
| **D0 — Design** (this doc) | Decisions recorded, open questions listed | Tom signs off on §1 + §10 |
| **D1 — Contract plumbing** | `dispatch/` scaffolding, `dispatch-lint.sh`, lane config, scout emits contracts; execution still manual | A hand-run contract flows open → done → verified and lands as evidence in `memory/models.md` |
| **D2 — Mac runner + review lane** | launchd runner, Codex CLI wired, cross-family review on open PRs | A PR review report produced end-to-end by the OpenAI lane, verified by the failsafe, with zero cloud-side credentials |
| **D3 — Cloud dispatch + experiments** | Anthropic lanes via `create_session`; `experiment` contracts; retro policy loop | First `learn:` commit that changes a lane rule citing contract-outcome evidence |

## 10. Open decisions (Tom)

1. **OpenAI lane concretes:** confirm what the Max-tier subscription exposes to
   CLI/agentic use (Codex CLI auth mode + which models) — fills the `VERIFY`
   entries in §3. Blocking for D2, not D1.
2. **Runner window and cadence:** proposed 09:15–21:00 every 30 min (clear of
   the 22:30 failsafe and midnight margin). Confirm or adjust.
3. **Auto-PR authority:** may `build`-contract workers open PRs themselves
   (proposed: yes, as drafts), or only push branches for Tom to PR?
4. **Daily contract cap:** proposed 6/day to start (quota safety margin on
   both pools).
