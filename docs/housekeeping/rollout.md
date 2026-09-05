# Instruction and eval housekeeping — 2026-09-05

Status: review package prepared; architecture paused for Tom to start Astra Ultra.

## Start, stop, continue

| Start | Stop | Continue |
|---|---|---|
| Explicit acceptance cases per operational role | Treating a worker claim or skipped check as a pass | Independent evidence and human review of consequential decisions |
| One shared instruction source with task-specific reads | Loading every procedure or mandatory interview for every task | Useful domain constraints, attribution and existing repo policy |
| Comparing behavior against frozen cases before promotion | Arbitrary percentage cuts and unbounded review polling | Preserving meaning, uncertainty and Tom's voice |

## Applied locally

- Personal Codex `~/.codex/AGENTS.md` is the shared preference source; Claude imports it.
  Resolved conflicting attribution mandates while keeping both verified addresses.
- Narrowed the scaffold reminder, browser alias and human-review triggers. Synced the
  Claude and Codex human-review copies and bounded each requested feedback wait.
  Kept the explicitly invoked ADHD mode, replacing unsupported generalizations and
  invented precision with adjustable preferences.
- Talent Radar's Claude file imports its existing AGENTS file. Yeva's original
  teaching instructions now live in AGENTS, imported by Claude. These changes are
  local and uncommitted; Talent Radar has unrelated work that must stay separate.
- Personal/project originals and change manifests are backed up at
  `~/.codex/backups/ivy-housekeeping-20260905/`. Restore only the intended file after
  checking for subsequent user edits. Do not overwrite the whole configuration.

## Prepared for GitHub review

Ivy: shared AGENTS entry point, conditional routine procedures, scoped skills,
explicit eval inventory and receipt-based dispatch verification. The immutable
playbook policy is unchanged. Six historical passing stamps are quarantined as
unverified pending independent receipts; their original outcome narratives remain.
This is not a finding that all six jobs failed. Dependencies now require passing
receipts, so pending dependent jobs can wait until predecessors are rechecked.

Writing skill: [draft PR 2](https://github.com/tompulsarlabs/writing-voice-skill/pull/2)
removes forced shortening, preserves uncertainty and respects voice-only requests.
It includes two additional eval cases. The branch is not installed or merged.

The vendored Ivy ask-matt and implement skills have intentional local overrides:
conditional interviews/reviews, task-appropriate testing and repository-controlled
shipping. `skills-lock.json` still records their upstream source versions; any
future skill refresh must preserve or explicitly reassess these local differences.
Vendor gstack and plugin caches were not rewritten.

## Evidence and limits

The deterministic runner, receipt gate, grader and lint checks are executable and
run locally. They test infrastructure, not agent quality. The registry defines 33
behavior cases across 13 roles. The full model baseline is **not run**; some cases
still need realistic tool fixtures and harness adapters.

One isolated writing smoke test preserved a tight sentence and uncertainty, and
returned voice analysis without rewriting. Its CLI model ID was not captured,
there is no before/after baseline and no calibrated blind grading. The saved result
therefore remains **unverified for promotion**. See `evals/results/`.

Receipts bind the declared checks to the task and revision. They enforce evidence
completeness; they cannot authenticate a fabricated receipt or establish that a
reviewer's judgment is correct. Independent verification remains necessary.

## Remaining rollout

1. Review and merge the Ivy and writing-skill drafts when acceptable. Deploy the
   updated runner and its verification module together through the existing runner
   checkout/update process. Keep new contracts unverified until receipts exist.
2. Update the actual saved Claude cloud routine prompts from `routines/*.md` after
   the repository changes land. Only the versioned source prompts were changed here.
   Check the first scheduled run uses the matching procedure and receipts.
3. Commit the small Talent Radar and Yeva instruction changes separately from other
   project work. Install the writing skill from its approved revision if used locally.
4. Confirm whether Dex and BrightPaws are deployed or reference projects. Dex looks
   like an unconfigured template; BrightPaws documents an eval runner that is absent.
   Their case specifications are recorded, but neither has a proven runnable baseline.
5. Inspect cloud-only ChatGPT/Claude project instructions when available. Local
   files do not establish what those products currently load. Run relevant frozen
   behavior cases before claiming fleet-wide improvement or reducing model cost.

## Astra Ultra handoff

Read `docs/product-discovery.md`, this report, `evals/README.md` and the current
runner before design. Establish the buyer, costly recurring job, existing workaround,
budget owner, demo decision and bounded experiment with a stop condition. The
housekeeping exposes internal failures; it does not prove external customer demand.
Tom will start that pass. No broader product architecture or MVP build began here.
