---
subject: tompulsarlabs/tomgreen.ai
type: repo
updated: 2026-08-27
---

# tomgreen.ai

Public. Created 2026-08-24 and shipped v1 the same day [cite:2026-08-24]. Since
then it has been the highest-volume repo on the account by a wide margin and
the usual reason a day is green.

## Activity

| Date | Non-bot commits | Note |
|------|-----------------|------|
| 2026-08-24 | 12 | v1: all routes, live proof strip, motion pass [cite:2026-08-24] |
| 2026-08-25 | 1 | `f88d03d` Obsidian-style knowledge graph, 14:19 local [cite:2026-08-25] |
| 2026-08-26 | 26 | 11:17–20:52 local; design system round + WebGL rebuild [cite:2026-08-26] |
| 2026-08-27 | 6 | 06:42–07:55 local — **none countable**, see below [cite:2026-08-27] |

The 2026-08-26 run covered a full design-system round trip (white primary
ground, twilight planetary map, career corridor walkthrough, per-stop company
impact pages, CI green, accessibility hardening) plus a black-hole entrance
rebuilt as a WebGL raymarched Schwarzschild render after the 2D version did not
clear the bar [cite:2026-08-26].

## It consumes Ivy's `state.json`

The site's live proof strip reads GitHub contributions **and Ivy's own
`state.json`** [cite:2026-08-24]. This repo is therefore a downstream consumer
of [[repos/ivy]]: changing the shape of `state.json` is a cross-repo breaking
change, not a local refactor. Ivy's cloud runs are scoped to `ivy` alone
[[ops]], so the consuming code cannot be inspected from a routine — treat
`state.json` keys as a public contract and add rather than rename.

## Attribution incident, 2026-08-27

Six real commits landed on `main` authored `Tom Green
<tom@Toms-MacBook-Air.local>` — an address not connected to the account, so
none of them count [cite:2026-08-27]. Cause and detection are in [[ops]]. The
fix is Mac-side `git config` and was not resolvable from a cloud run.

## Open threads

- Launch waits on DNS cutover and the `SITE_LAUNCHED` flag [cite:2026-08-26].
- Vercel hookup pending — the integration lacks project-create permission
  [cite:2026-08-24].

## Changelog

- 2026-08-27 — page created from journals 2026-08-24→27 and `state.json`.
