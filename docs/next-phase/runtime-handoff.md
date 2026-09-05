# Live cancellation and deadline verified; model integration still blocked

Latest checkpoint, 5 September 2026, supersedes the historical sections below.
Tom approved the proposed additive extension: 45 aggregate engineering minutes,
20 minutes for at most three fresh runtime probes, and the one remaining repair
iteration. The original ledger, start time, limits and consumed failed attempt
were preserved. No API spending was authorized by the subscription upgrade.

Repair iteration 2 adds an explicit, one-use local authorization record and a
shared preparation/run command deadline. It also disables Docker local-log
compression, after the first new probe exposed an incompatible `max-file=1`
configuration. That failed probe remains visible; it was not retried under its ID.

| New attempt | Actual result | Container stopped | Capture |
|---|---|---|---|
| `extension-complete-1` | Image built; Docker start failed on log configuration | Confirmed | Complete error stream, not worker success |
| `extension-cancel-2` | Worker ran; explicit cancellation | Confirmed | Partial |
| `extension-deadline-3` | Worker ran; deadline shutdown | Confirmed | Partial |

All three saved receipts independently verify. Actual receipt-copy tampering,
wrong-owner inspection and refusal of a fourth reservation were checked without
altering originals. There are four consumed attempts in total, with 200 seconds
reserved, no unresolved final-container reservation and no completed worker run.
The three-probe extension is spent; do not renew it or create a replacement store.
Both repair iterations are now used. The engineering ledger records the separate
additive allowance and continuation debit; handoff is never a reset.

The full deterministic suite passes **45 tests**. The read-only plan still returns
`execution_ready: false`. No real agent, model or judge attempt ran. Milestone A is
**not passed**, even though the running-container shutdown controls now work.

Remaining verification: natural completion with the corrected logging option;
daemon-side build cancellation and failures before final-container creation;
hard whole-lifecycle timing; isolated real-agent authentication, effective harness
metadata, approved neutral case and independent semantic assessment. The shared
deadline clamps Docker preparation commands and the run loop, with a separate
15-second shutdown grace; filesystem work, daemon build lifetime and a final
five-second client wait prevent claiming a hard end-to-end wall ceiling.

Host Codex 0.153.0 still reports ChatGPT login. Official documentation supports
subscription CLI authentication, but no attempt-scoped subscription credential
broker was established here. Neither a host CLI working directory nor ignoring
user config establishes the intended isolation. Do not copy/mount host auth into
the worker or reinterpret a Pro upgrade as API-key billing authorization.
See [authentication](https://learn.chatgpt.com/docs/auth) and
[non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode).

Private originals remain in `/tmp/ivy-runtime-proof-20260905`; portable, allowlisted
observations are in [the extension summary](evidence/runtime-extension-20260905.json).
No raw Docker inspection, provider credentials or machine/account paths belong in
the public evidence summary. Existing branch and stacked draft PR #20 are preserved.

## Previous recovery checkpoint (retained history)

Follow-up on 5 September 2026, after Tom asked to solve the outstanding gaps:
`recover-probe` confirmed that the original attempt-owned container is stopped
and closed its reservation. The consumed `isolation-1` attempt is retained with
`execution_error`; the ledger's original start time and limits are unchanged.
A real Docker inspection rejected a deliberately mismatched owner. A fresh CLI
probe returned `attempt or execution time budget exhausted` before creating a
new attempt; the ledger was unchanged by that refusal.

Private evidence: `recovery-controls-20260905.json` in the original store and
`isolation-1/stop-1788631255903549000.json`. These are observed recovery/ownership/
budget controls, not successful worker execution. Image build, success/cancel/
deadline paths and real agent execution are still unverified.

A proposed extension awaits Tom's answer: up to 45 additional engineering minutes,
a 20-minute runtime window for at most three new probes, the one remaining repair
iteration, and all prior attempts/debits retained. No runtime allowance was changed
and no paid model call was authorized. The recovery diagnostics were authorized
by this follow-up; they do not reopen the expired implementation budget.

## Previous High checkpoint (retained history)

High continuation, 5 September 2026: one repair iteration, 36 deterministic tests
passing. The exact original copy failure was reproduced and retained:
`Error response from daemon: container rootfs is marked read-only`.
The before/after container inspection confirmed matching ownership and created,
stopped state. The adapter now packages verified inputs through a fixed FROM/COPY
image context and records base/derived identities while preserving worker isolation.
This replacement has not been built or executed on real Docker.

The recovery helper waited approximately 390 seconds for escalation approval and
was interrupted at the budget checkpoint. No recovery result was obtained; the
original reservation remains unconfirmed. No ownership-rejection control or fresh
probe executed. The unchanged ledger's one-hour elapsed window has expired, so a
fresh attempt would also be refused after recovery. Do not create another store,
change timestamps or raise limits to bypass either condition.

Actual completion, explicit cancellation of a running container, deadline shutdown,
builder availability/offline behavior and runtime receipt verification remain
unverified. Synthetic receipt controls do reject tampering/missing evidence and
preserve incomplete states. Preparation commands have separate timeouts outside
the run-phase `--deadline`; whole-operation boundedness is not established.
No evaluated agent or judge calls occurred; milestone A remains not passed.

See [engineering review](runtime-engineering-review.md) and the portable
[sanitized evidence summary](evidence/runtime-debug-20260905.json). The original
failed attempt and added reproduction record remain in the private store. The
resource ledger carries the original debit plus this continuation; no budget reset.

## Original Extra High handoff (retained history)

5 September 2026. Worktree `/tmp/ivy-acceptance-scaffold`, branch
`codex/ivy-acceptance-scaffold`, stacked draft PR 20. Do not modify the unrelated
untracked correctness document in `/Users/tom/Build/ivy`.

## Implemented and checked

- Durable comparison-bound ledger with atomic replacement/fsync, exclusive OS lock,
  consumed IDs, worst-case time reservations and restart blocking until an
  attempt-owned container is confirmed stopped.
- Recompile the saved preview and check every copied byte against its snapshot.
  Pack only the selected fixture and instruction bundle; no grader files.
- Fixed Python runtime probe with a digest-pinned image, no credentials/network/host
  mounts, non-root user, read-only root, capability drop and resource limits.
- Supervisor stdout/stderr capture, container inspect records, bounded cancellation,
  immutable attempt directories and hash verification commands.
- Independent bad citation control. Passing citations still leave semantic status
  unverified; this module cannot award a benchmark pass.

`python3 -B -m unittest discover -s tests -v` passes **27 deterministic tests**.
Actual runtime preparation has **not** passed. No agent/model/judge calls occurred.
The new adapter is explicitly an infrastructure probe, not the real harness.

## Exact first failure

```sh
python3 -B -m ivy_acceptance probe examples/acceptance/preview.json \
  --store /tmp/ivy-runtime-proof-20260905 \
  --image python@sha256:78387bc3881b8273120a12ebe6c1ab22b018ccc2c9adf565ae1ac9b536e184ea \
  --context colima-ivy-acceptance --attempt isolation-1
```

Expected: copy only prepared bytes, run the probe, confirm stopped, verify receipt.
Observed: `docker cp - ivy-360f57ca484a8b56c935b14b87d1da52:/` returned exit 1
before start. The current CLI does not include subprocess stderr in its error output;
capture that safely when reproducing. Read-only-root materialization is the suspected
cause, not yet verified. The consumed reservation remains unconfirmed in
`/tmp/ivy-runtime-proof-20260905/ledger.json`; preparation metadata is in `isolation-1/`.

The container should be in created state; inspect ownership and status rather than
assuming. Use `recover-probe --store /tmp/ivy-runtime-proof-20260905 --attempt isolation-1`
to close the reservation only after confirming it stopped. Use a **fresh** attempt ID
for the next actual test. Never delete the ledger to get a passing result.

## Debugging scope and order

Use Astra High as Tom requested. At most **two repair iterations**, charged to the
remaining milestone-A time in `resource-ledger.json` (do not restart the two-hour cap).

1. Reproduce the copy failure; retain stderr and lifecycle evidence. Correct input
   preparation while preserving the final worker's read-only filesystem and zero
   host mounts. One possible small solution is an offline, COPY-only derived image
   built from the pinned base and verified tar bytes, recording both image identities.
   Do not loosen the worker's filesystem policy simply to make copying succeed.
2. Exercise complete, explicit cancel and deadline paths against real Docker.
   Confirm the container, not only the Docker client, stopped. Test tampering against
   the receipt, restart recovery and ownership; do not treat missing capture as pass.
   Retain failed attempts and label partial capture. Verify deterministic bad-output
   grading separately from actual runtime results.
3. Run the full deterministic suite after the fix. Save a portable synthetic evidence
   bundle/report with scope and limitations; review files for machine/account paths
   before adding artifacts to this public repo. Update PR 20's final scope and checks.

## Runtime installation and authentication

Installed with Homebrew: Colima 0.10.3, Docker CLI 29.7.2, Lima 2.2.0. Dedicated
Colima profile `ivy-acceptance` is running, 2 CPU / 2 GiB, 12 GiB disks, host mounts
disabled, SSH config integration disabled, and no change to the default Docker
context. Use `docker --context colima-ivy-acceptance ...`. Installation/start and
Docker calls require the local tool's filesystem/network escalation. They were
approved in the Extra High stage. No automatic service was enabled.

Host Codex 0.153.0 reports a ChatGPT subscription login. Its auth file was not read,
copied or mounted. No `OPENAI_API_KEY` or `CODEX_API_KEY` is present. The design excludes
provider-wide credentials in the worker. An asynchronous question asks Tom whether
he will provision a dedicated API key locally and authorize at most $5 for the proof,
or defer model authentication and keep this as runtime-only proof. No answer was
received at this checkpoint. Never ask him to paste a key in chat. A $5 answer alone
is not an implemented enforceable request/cost limit.

The existing-tool spike has not started: Promptfoo's Codex provider supports saved
CLI auth or API credentials, but does not remove the worker credential boundary.
Do not call its absence an incompatibility or silently authorize a second execution
engine. Resolve intentional authentication before spending the 30-minute wrapper
sub-cap. A suitable documented API proxy exists in OpenAI's Codex GitHub Action,
but it requires an API key and has not been integrated or tested here.

Milestone A still needs a real neutral agent case with effective harness/model/tool
configuration, owner approval binding and actual evidence. Runtime-only tests do not
pass that gate. Do not proceed to six cases or a broad product build without the
named external release owner/pending change/timed workaround gate, or Tom's explicit
internal-dogfood extension.

Sources checked for the authentication decision:
[Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode),
[Codex Action](https://github.com/openai/codex-action),
[Promptfoo Codex provider](https://www.promptfoo.dev/docs/providers/openai-codex-sdk/).
