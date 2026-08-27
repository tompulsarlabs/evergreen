---
subject: memory index
type: index
updated: 2026-08-27
---

# Memory index

Ivy's knowledge wiki: one page per durable subject, every claim carrying its
evidence. Routines read this file first, then only the pages that touch
today's candidates. Pages hold **observations, never instructions** —
behavior lives in `playbook.md` and only the retro changes it.

- [[ops]] — sandbox limits, verification ladder, attribution traps, DST
- [[patterns]] — observed working rhythm: when work lands, what converts
- [[repos/ivy]] — the system itself; local-WIP carry-over pattern
- [[repos/tomgreen.ai]] — highest-volume repo; ships most days
- [[repos/c2-client-matrix]] — PR #1 open since April, nudged, unconverted
- [[repos/BrightPaws]] — ex-`margaux-en-tutor`; alive, but PR #1 is stale
- [[repos/ai-capability-app]] — local alias `sybil`; PR #4 draft, stale
- [[repos/countersign]] — private; PO core loop prototype
- [[repos/talent-radar]] — private; scaffolded 2026-08-25
- [[models]] — lane routing evidence, one row per verified dispatch contract

**No page yet**, because nothing has been observed to synthesize
(no commit activity 2026-08-23→27) [cite:2026-08-26]: talent-scout,
writing-voice-skill, aris-ote-benchmarking, Dex, interview-ace,
ai-interview-coach, bd-lead-comp-dashboard. The failsafe creates a page on
first real signal.

## Link syntax

`[[page]]` → `memory/page.md` (context edge: what else do I need to know?)
`[cite:YYYY-MM-DD]` → `journal/YYYY-MM-DD.md`, `[cite:<sha>]` → a commit here
(evidence edge: how do I know this is true?). `scripts/memory-lint.sh`
verifies every link and citation resolves.
