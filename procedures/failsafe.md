# Failsafe procedure

Loaded only for this routine. Shared constraints remain in `playbook.md`.

- **Failsafe (22:30)** — still grey → finalize today's journal entry, commit it
  **Tom-authored** per the attribution rule, push, verify per the immutable rule.
  Record outcome either way — `state.json` gets `{date: {green_by, method,
  contributions: <final count from check>, signal_source, cite, nudge_sent,
  nudge_converted, failsafe_fired}}` (bot-authored); bump or reset `streak`.
  Keep `signal_source` to a short source label and put the verification
  narrative in the journal entry under `## Verification`, with `cite` pointing
  at that file.

  **Then verify dispatch contracts** — after the day is secured, never
  before: for each contract in `dispatch/done/` without a passing independent receipt,
  run every declared check using `procedures/verify-contract.md`.
  Missing access remains unverified; move contracts past `expires` to `dispatch/failed/`
  with `state: expired`. Two more cases, because the runner's bookkeeping is
  a claim like any worker's:
  - A contract in `dispatch/failed/` whose outcome says `exit: timeout` or
    `no_report` may have finished the work and only missed printing the
    report (2026-09-03: `copy-02` opened its draft PR at 10:32 and was
    recorded as a 40-minute timeout at 10:53). Run its Verification too. If
    it passes, set `state: done`, move it to `dispatch/done/`, record a passing receipt and stamp
    `verified: true` with a `verified_note` saying the report never landed,
    and count its wall-minutes as work, not waste. If it fails, leave it.
  - A contract in `dispatch/queue/` with `state: claimed` and no outcome
    whose `claimed_at` is older than `budget.wall_minutes × 3` is a runner
    that died mid-task: set `state: open`, drop `claimed_at`, and say so in
    the journal. It runs again on the next tick.
  Run `scripts/dispatch-lint.sh`; commit bot-authored
  (`dispatch: verify <ids>`). Verified outcomes feed `memory/models.md` in
  the synthesis pass below.

  **Then synthesize memory** — always *after* the day is green and recorded,
  never before: a memory problem must never eat the failsafe window. This is
  the daily pass that keeps `memory/` current:
  1. **Attach facts to subjects.** Every observation from today worth keeping
     goes to its page — repo facts to `memory/repos/<name>.md`, environment
     behavior to `memory/ops.md`, rhythm and conversion to
     `memory/patterns.md`. Write the citation as you write the claim.
  2. **Create a page** only for a subject with real, durable signal, and add it
     to `memory/INDEX.md` in the same commit. One quiet day does not earn a
     repo a page; a first real commit does.
     If the day involved a non-obvious operational sequence that will recur,
     write the recipe to `procedures/` while the details are exact — a
     memory page saying "someone should run the same recipe we used for X"
     means that recipe should have been written down.
  3. **Making no change is a valid outcome.** If the wiki is already correct,
     write nothing — an unchanged page is a stronger signal than a page
     restated daily.
     A concept today's journal needed that `CONTEXT.md` lacks, or used
     against its definition, goes in the journal under `## Vocabulary gaps`.
     The failsafe never edits the glossary; the retro does.
  4. Run `scripts/memory-lint.sh`; it must pass before committing. Commit
     bot-authored as `memory: <what changed>` and set
     `memory_last_synthesized` in `state.json` to today.
