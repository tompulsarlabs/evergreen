# Retro procedure

Loaded only for this routine. Shared constraints remain in `playbook.md`.

## Tunable: retro (Sunday 10:00)

Read `memory/INDEX.md` and the pages it lists first — that is the synthesized
view of the trailing window, and cheaper than re-mining raw history. Then read
the last 7–30 days of `state.json` for the numbers. Answer: how often did the
failsafe fire? Did nudges convert to real activity within 4 hours? Which repos
produced shipped work?

The retro then has two jobs.

**Tune behavior.** At most two adjustments (nudge time, wording, ranking,
excludes) by editing the Tunable policy in `playbook.md`, its linked routine procedures, and/or `config.yml`.
Commit as `learn: <what> — <evidence>`, naming the page or journal entry the
evidence came from; tag the next version; summarize in `CHANGELOG.md`.

**Curate memory.** The daily pass only adds — this is the only pass that
removes, and the only one allowed to rewrite a page wholesale:

- **Verify** a sample of claims against their citations, weighted toward the
  ones that have been influencing candidate ranking. A claim its evidence no
  longer supports gets corrected or dropped, never left standing. Contradictions
  between sources are worth recording explicitly rather than silently resolving.
- **Prune** what has stopped being true: a repo gone dormant, an access limit
  that no longer applies, an open thread that closed. Outdated context is worse
  than missing context, because it reads as current.
- **Log** every removal in that page's `## Changelog` with the date and reason.
  Git holds the diff; the changelog line is what makes it findable without
  archaeology.
- **Merge or split** pages when a subject has outgrown or emptied its page, and
  keep `memory/INDEX.md` inside its line budget — it is read on every run, so
  it stays a map, not a summary.
- Re-run `scripts/memory-lint.sh`, then commit bot-authored as
  `memory: retro — <what changed>`.

**Prune the steering files.** `AGENTS.md` and shared policy are standing context. Routine procedures and
skill bodies load only when relevant; measure actual loading before pruning.
Once a week, call the Skill tool with `writing-for-agents` and apply its
tests to them: delete no-ops (instructions the agent already follows by
default), collapse restatements into a leading word, state a target
positively where a prohibition is not a hard guardrail, and push reference
that only some runs need behind a pointer. A deletion that provably changes
no behaviour does not count toward the two adjustments; a wording change
that does, does. Immutable sections stay untouched. Then curate
`CONTEXT.md`: call the Skill tool with `domain-modeling`, resolve the week's
`## Vocabulary gaps` from the journals, correct any page or journal that used
a term against its definition, and record in `docs/adr/` any decision that
is hard to reverse, surprising without context, and the result of a real
trade-off — all three, or no ADR.

**Run the fleet, not the sessions.** The retro optimizes lane *policy* against
per-class targets, never individual runs (adapted from Uber's software-factory
findings, 2026-08-28):

- **Per-class target metrics** — review: share of findings that survive
  triage; build: first-pass verified-done rate; chore: wall-minutes per
  verified-done; every class: zero waste. Judge lanes on these, not vibes.
- **Waste is the first lever, model choice the last.** Waste = wall-minutes
  on `dispatch/failed/` contracts + contracts that expired unexecuted +
  repeated unresolvable-lane skips. Compute it weekly before touching lane
  assignments — eliminating zero-value consumption beats downgrading a lane
  and losing quality.
- **Pareto rule for lane moves.** Step a task class down to a cheaper lane
  only when its target metric held there (experiment evidence or ≥3 verified
  outcomes); step it up when failures show quality is the binding
  constraint. Never trade a target metric for cost — flat-rate pools make
  that a bad trade by definition.
- **Experiments are the benchmark instrument.** When a lane decision is
  pending and the evidence is thin, spend that week's one `experiment`
  contract on exactly that comparison rather than waiting for organic
  volume.
- **Record fleet metrics weekly** in `memory/models.md` (verified-done
  count, waste minutes, per-class rates, throttles) so trends are one page,
  not an archaeology dig.

Compare changed instructions on the relevant cases in `evals/agents.json`.
Record unrun cases as unrun; do not infer a behavior pass from lint or file size.
Use only receipt-verified contracts for current routing metrics.

