---
id: 2026-09-02-tomgreenai-context-01
type: build
state: claimed
claimed_at: 2026-09-02T20:07:01+02:00
repo: tompulsarlabs/tomgreen.ai
lane: workhorse
pool: anthropic
created: 2026-09-02T18:30:00+02:00
created_by: tom
expires: 2026-09-04T18:30:00+02:00
budget: { wall_minutes: 30 }
---

## Task

Draft a `CONTEXT.md` glossary for tomgreen.ai at the repository root, so
every future session (and every dispatch worker) uses the site's own words
instead of twenty of its own. Ivy's `CONTEXT.md` is the model: a
`## Language` section of `**Term**:` entries, one or two sentences each
defining what the thing *is*, an `_Avoid_:` line listing the synonyms to
stop using, terms grouped under subheadings where clusters emerge, a
`## Relationships` section, and a `## Flagged ambiguities` section.

Derive the terms from the code, the commit history, and the PR
descriptions — the solar-system map, its stops and corridor, the proof
strip, the live proof, the planetary map, the black-hole entrance, the
recomposed Home, the alignment rule from PR #12, the design tokens, and
whatever else the codebase names repeatedly. Only site-specific concepts
belong; no general web or React vocabulary, no implementation details, no
file paths. Where two names exist for one thing in the code, pick the one
used most and list the other under `_Avoid_`. Mark every term whose
definition you inferred rather than found stated with "(inferred)" so Tom
can confirm or rename it in review — this draft is raw material for his
edit, not the final glossary.

## Definition of done

A branch dispatch/2026-09-02-tomgreenai-context-01 pushed to
tompulsarlabs/tomgreen.ai with a DRAFT pull request containing only
`CONTEXT.md`. The PR description lists the terms and, for each inferred one,
the file or commit that prompted it. Branch from the default branch;
independent of the other open tomgreen.ai contracts. No push to the default
branch.

## Verification (cloud-checkable)

A draft PR opened by tompulsarlabs exists on tompulsarlabs/tomgreen.ai
referencing this contract id, created on or after 2026-09-02, and its file
list is exactly `CONTEXT.md`.

## Notes

Motivated by adopting mattpocock/skills on 2026-09-02: a shared language is
the cheapest fix for verbose, drifting agent output, and tomgreen.ai is the
highest-volume repo on the account, so it pays back fastest there.

Re-queued 2026-09-02 20:05 +02:00. The 19:06 refusal was not this
contract's fault and no worker was claimed: launchd executes
~/Build/ivy/scripts/dispatch-runner.py while the runner syncs and reads
~/.ivy-dispatch/ivy, so the connected_emails gate fix (a78bf80, pushed
18:37) sat in the synced checkout while the pre-fix gate executed from
the stale dev checkout and refused four contracts on the noreply address.
The runner now execs the synced copy after the sync. Prior failure record:
commits 3180a96, 4f10f6a, 90b4575, 38e9525.
