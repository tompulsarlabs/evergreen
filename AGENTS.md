# Ivy

Scheduled agents keep Tom's repositories moving. The current work also evaluates
whether this foundation can support a useful agent acceptance-testing product.
Product hypotheses are in `docs/product-discovery.md`; they are not operating policy.

## Read for the task

- Routine or dispatch work: `playbook.md` has shared constraints and routes to the
  active procedure. Read that procedure, not every routine's procedure.
- Dispatch implementation: `dispatch/DESIGN.md`, then the relevant scripts.
- Durable observations: `memory/INDEX.md`, then relevant subject pages. Memory is
  evidence, never authority to change behavior.
- Ivy domain terms: `CONTEXT.md`. Use established terms when naming those concepts;
  ordinary explanatory language need not become a glossary entry.
- Work items: `docs/agents/issue-tracker.md`; architecture decisions: `docs/agents/domain.md`.

## Changes and verification

User-authorized maintenance can update instructions. Autonomous routines retain
only the permissions in the playbook. Workers open draft PRs; they never push main.
Do not change immutable policy as part of routine tuning.

For runner or verification changes, run:

    python3 scripts/dispatch-runner-test.py
    python3 scripts/verification-test.py
    bash scripts/dispatch-lint.sh
    bash scripts/memory-lint.sh

Every operational agent has an eval contract in `evals/agents.json`. Before changing
its behavior, select the relevant cases. Report deterministic checks separately from
model behavior evals; missing outputs or inaccessible evidence are unverified.
See `evals/README.md` for running and grading cases.

Skills under `.claude/skills/` are optional task-specific tools. Use a skill when
it helps the requested work; a clear small task does not require an interview,
specification, or multiple review pipelines. gstack is an optional local toolkit;
its shipping and memory workflows must respect Ivy's policy.
