---
subject: tompulsarlabs/ivy
type: repo
updated: 2026-08-27
---

# ivy

Public. The system itself: config, playbook, memory, journal, state, scripts.
Renamed from `evergreen` on 2026-08-24 when the agent got its name.

Being public matters operationally — a green day confirmed by a commit here
needs no "private contributions" toggle to show on the graph [cite:2026-08-24].
It is the fallback proof when the day's real work landed somewhere private
([[repos/countersign]], [[repos/talent-radar]]).

## `state.json` is a published contract

[[repos/tomgreen.ai]] reads this repo's `state.json` for its live proof strip
[cite:2026-08-24]. Keys are consumed outside this repo by code that cloud runs
cannot see [[ops]], so treat the schema as append-only: add keys, shorten
values, never rename or remove.

## The local-WIP carry-over pattern

The Mac checkout of this repo repeatedly held work the cloud clone could not
see: 1 unpushed commit flagged on both 2026-08-25 and 2026-08-26, carried over
unresolved and named as the day's top pick both times [cite:2026-08-25]
[cite:2026-08-26]. Resolved by 2026-08-27, when the scan showed all five
tracked repos clean [cite:2026-08-27].

The pattern is worth remembering: "push the Mac's unpushed commit" is the
cheapest real ship available, it recurs, and it is invisible to any cloud-only
check — it depends entirely on `local-wip.json` being fresh [[ops]].

## Activity

7 non-bot commits on 2026-08-24 (the ladder build) [cite:2026-08-24]; 4 on
2026-08-26 [cite:2026-08-26]; 3 on 2026-08-27 (memory-wiki build +
state-schema refactor), plus 2 PRs opened same day [cite:2026-08-27]. Bot-authored
bookkeeping commits are excluded everywhere and never count [[ops]].

## Changelog

- 2026-08-27 — page created from journals 2026-08-23→27, `state.json`, and
  `CHANGELOG.md`.
- 2026-08-27 (failsafe) — added 2026-08-27 activity row: the memory system
  documented on this page shipped the same day, on this repo, by real work.
