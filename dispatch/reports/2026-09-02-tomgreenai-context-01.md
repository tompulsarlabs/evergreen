# Report — 2026-09-02-tomgreenai-context-01

Produced by the workhorse/anthropic lane, 14.5 wall-minutes.

**Contract `2026-09-02-tomgreenai-context-01` — complete.**

- **Branch:** `dispatch/2026-09-02-tomgreenai-context-01`, pushed to `tompulsarlabs/tomgreen.ai`. Nothing pushed to `main`.
- **PR:** https://github.com/tompulsarlabs/tomgreen.ai/pull/14 — **draft**, base `main`, author `tompulsarlabs`, file list exactly `["CONTEXT.md"]`, contract id in the body.
- **Commits:** two, authored `tompulsarlabs <tom@pulsarlabsai.com>`.

**What's in it.** A 344-line glossary on Ivy's `CONTEXT.md` model: `## Language` in six clusters, `## Relationships`, `## Flagged ambiguities`. 37 terms, each with a definition and an `_Avoid_` line — the front door (Home, the opening, the three statements, the masthead, the positioning line, the operating record, case study, tier, the Lab, Voices, the proof strip, live proof); the navigation (the Moon, the island, the navigation row); the world behind the moon (the portal, the planetary map, a section's system, planet/body, nameplate, the core, capture, travel, the burst, the poster, the membrane, the deep field); the corridor (career corridor, station, hyperspace); type and ground (paper/ink, the width axis, record voice, live green/clay, the air scale, the alignment rule); publishing (the owner, owner ruling, named claim, content guard).

**Three terms marked (inferred)**, with sources in the PR body: *the proof strip* (name exists only as an identifier), *live proof* (three competing phrases in DESIGN.md and the content modules), *the air scale* (the `--u`/`--air-1..4` set has jobs but no collective name). Two naming calls flagged rather than settled: **core** over nucleus/black hole on count (105 / 67 / 9), and **station** over stop (143 / 56).

**Four code facts the work surfaced**, listed in the PR for separate action: the proof strip is not mounted by any route; `data-opening="replay"` has no caller since the Moon stopped navigating; DESIGN.md and DESIGN-MOTION.md describe a site that no longer exists on four counts; and the Voices content module's comment overstates its own gate.

**Review.** `/code-review` ran against the diff and checked the file's assertions against HEAD. Most held; three claims did not and were corrected in the second commit (the operating record's eyebrow, the Voices gate, and a definition using three words the file itself bans). Docs-only, so no build or test surface was touched.
