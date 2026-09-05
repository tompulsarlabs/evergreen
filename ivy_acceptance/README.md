# Acceptance preview and runtime probe

Extra High added a durable local attempt ledger, verified input materialization,
bounded supervisor capture, a credential-free Docker probe, recovery commands and
independent citation controls. **The first real preparation attempt failed at
`docker cp`; the runtime proof and milestone A have not passed.** See
[the current High handoff](../docs/next-phase/runtime-handoff.md). The 27 deterministic
tests pass; they are not evidence of a working model evaluation.

The explicit `probe` command executes a fixed Python infrastructure test. It never
uses a model, account credential or a primary model-comparison slot. `plan` retains
its read-only behavior. `recover-probe` inspects and stops an attempt-owned container
after a supervisor failure; it cannot erase the consumed attempt. `verify-probe`
checks saved artifact hashes without executing anything.

New modules: `storage.py` (locked, atomic reservations), `materialization.py`
(recompiled plan and byte checks), `docker_probe.py` (container lifecycle and capture),
`probe_cli.py` (explicit commands) and `grading.py` (citation integrity only).
Checksums assume a trusted local supervisor and detect changed artifacts; they are
not signed attestations against a hostile host operator. Model adapters, authenticated
benchmark approval, semantic grading and a comparison report remain unfinished.

The rest of this document describes the underlying architecture scaffold.

Python 3.11+; standard library only. Run from the repository root; no installation,
server or provider credential is needed for this stage.

```sh
python3 -B -m ivy_acceptance plan examples/acceptance/preview.json
python3 -B -m unittest discover -s tests -v
```

`plan` reads the specified input trees and prints a JSON envelope with a detached
`plan_sha256`. `-B` suppresses interpreter bytecode writes, including first-run imports.
The command performs no checkout, subprocess execution, network calls or file writes.
A successful plan command means the preview was compiled; it is not a benchmark pass.

The example plans eight primary slots: two draft cases × two instruction versions ×
two repetitions. The planner supports the approved six-case/24-slot proof; the other
four real fixtures and human approval are build-stage work. The instruction versions
are draft illustrative inputs, not a validated improvement or deployed configuration.

## Component boundaries

| Module | Implemented responsibility | Next-stage boundary |
|---|---|---|
| `canonical.py` | Canonical JSON, detached hashes, strict JSON reads and explicit file-tree snapshots | Trusted artifact persistence and hostile-worker isolation |
| `planning.py` | Closed preview config, same visible runtime for both variants, content binding, disjoint visible/grader trees, fixed paired schedule | Live preflight, import resolution, owner approval and execution manifest validation |
| `budget.py` | Reserve-before-launch semantics, consumed attempt IDs, remaining wall time and unconfirmed-termination blocking | Persistent ledger, real clocks, runtime ownership and provider cost enforcement |
| `ports.py` | Adapter request/result boundaries, explicit primary/diagnostic distinction and unavailable live adapter | Actual preparation, structured capture and confirmed container termination |
| `__main__.py` | Read-only plan CLI | Execution, grading, comparison and report commands |

The compiled envelope is an ordinary JSON value; treating it as frozen requires
verifying its detached digest before use. The compiler owns copies of its inputs.
Plan integrity is not authenticated owner approval. The build must revalidate input
snapshots immediately before materialization and validate persisted plans, results
and assessments before trusting them.

The config exposes one shared `runtime` object; each variant selects only an
instruction directory. This intentionally makes a model/tool/config change outside
the instruction-only comparison schema. Unknown keys fail validation. No automatic
imports are resolved here. Symlinks and portable case-insensitive path collisions
are rejected; support for more complex trees is deferred.

## Honest current state

Every preview returns `execution_ready: false`. Missing harness configuration,
draft owner review and the absent live adapter are explicit blockers. Changing a
label file to `owner_reviewed` does not authenticate approval or enable execution.
The default adapter raises `CapabilityUnavailable` for prepare/run/cancel; it never
returns simulated success.

Execution, criterion and benchmark states have distinct types. There is deliberately
no implemented aggregator that can produce a benchmark pass yet. The tests prove
local architecture rules and synthetic fixture behavior, not model performance,
isolation, complete evidence capture or real cancellation.

The compiler checks path separation across every visible tree and every grader tree.
This prevents accidental grader selection in the plan; it is not a sandbox. The
future adapter must mount only worker-visible files in the isolated environment and
keep authoritative evidence and grading outside that namespace. Never mount the
repository root or the `acceptance_fixtures` parent tree into a worker.

See [the build handoff](../docs/next-phase/build-handoff.md) for the exact Extra High
and High stages and [the accepted design](../docs/next-phase/system-design.md).
