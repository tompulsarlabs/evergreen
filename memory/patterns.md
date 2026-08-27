---
subject: observed working rhythm
type: patterns
updated: 2026-08-27
---

# Patterns: how the work actually happens

Observations about the rhythm of real work, drawn from outcome history. These
are findings, not directives — the retro decides whether any of them should
change the ladder, and `playbook.md` is the only place behavior lives.

## Real work carries every day so far; the failsafe has never fired

Five recorded days (2026-08-23→27), all green by real work, streak 5. The
failsafe journal entry has not once been needed [cite:2026-08-26]
[cite:2026-08-27]. The system is currently a *nudge* system in practice, not
a floor system — the floor has never been tested in anger.

## Volume is bursty, not steady

Contributions per day: 9, 19, 2, 31 [cite:2026-08-23][cite:2026-08-24]
[cite:2026-08-25][cite:2026-08-26]. A single day (2026-08-26) carried more
than the other three combined. A quiet day is therefore weak evidence of a
stalling week, and the 2-contribution day (2026-08-25) still cleared the bar.

## Work routinely continues past the 18:00 check

On 2026-08-24 and 2026-08-26 real commits kept landing well after the check —
2026-08-26 ran 11:17 to 20:52 local [cite:2026-08-26]. On 2026-08-25 nothing
landed after 18:00 [cite:2026-08-25]. Work also starts early: six commits
between 06:42 and 07:55, before the 09:00 scout, on 2026-08-27
[cite:2026-08-27]. So the check sits inside the working day rather than after
it, and a grey reading at 18:00 has often been a *mid-day* reading.

## New work outcompetes old open PRs, consistently

Across 2026-08-23→27 the three open PRs (opened April and May) drew zero
activity, while two new repos were created (`talent-radar`, `countersign`) and
`tomgreen.ai` alone took 26 commits in one day [cite:2026-08-26]
[cite:2026-08-27]. The revealed preference is for shipping new work over
clearing old review queues.

This matters for candidate ranking: `c2-client-matrix` #1 has been the scout's
"cheapest real contribution" pick repeatedly and has never been taken
[[repos/c2-client-matrix]].

## Nudge conversion is 0 for 1 — resolved count

Exactly one nudge has ever been sent: 2026-08-24, push channel, candidate
`c2-client-matrix #1`, `nudge_converted: false` [cite:2026-08-24]. Every
other day was green before the check, so no nudge fired.

**Discrepancy resolved (2026-08-27, contract 2026-08-27-ivy-nudge-audit-01):**
journals described two, then three "nudge cycles" [cite:2026-08-26]
[cite:2026-08-27], but the inflation came from counting scout *top-picks and
carry-overs* as nudges. The "earlier" nudge claimed on 2026-08-26 is
impossible — the system did not exist before 2026-08-23 [cite:2026-08-23],
and 2026-08-23 sent none. The 2026-08-25 journal is consistent with the
single recorded nudge [cite:2026-08-25]. True count: **1 nudge, 0
conversions** — real but n=1; still too thin to tune on alone. Journals'
"nudge cycle" language should be read as "scout pick" unless `state.json`
records a send [cite:2026-08-27].

## The watchlist grows fast

11 → 12 → 14 repos over three days [cite:2026-08-24][cite:2026-08-25]
[cite:2026-08-26], plus one rename in place (`margaux-en-tutor` → `BrightPaws`)
that arrived as a simultaneous add and drop [cite:2026-08-27]. Auto-sync
earns its keep; a hand-curated list would already be wrong.

## Changelog

- 2026-08-27 — nudge-count discrepancy resolved: journals had counted scout
  picks as nudge cycles; recorded count (1 nudge, 0 conversions) confirmed
  against primary sources (contract 2026-08-27-ivy-nudge-audit-01).
- 2026-08-27 — page created from `state.json` outcome history and journals
  2026-08-23→27.
- 2026-08-27 (failsafe) — extended the never-fired streak note to 5 recorded
  days; no other pattern changed today.
