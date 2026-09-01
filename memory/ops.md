---
subject: Ivy's runtime environment
type: ops
updated: 2026-08-30
---

# Ops: how the environment actually behaves

Environment facts learned by running, not by reading docs. Each one cost a
run to discover; none of it is re-derivable cheaply.

## Cloud sandbox egress is repo-scoped

Routines run in Claude Code cloud sandboxes whose github.com egress is scoped
to `tompulsarlabs/ivy` alone. GraphQL is blocked, unscoped REST is blocked,
and even the *public* contributions HTML 403s ("sessions are bound to their
configured repositories") [cite:b85b8af]. `scripts/check.sh` therefore exits 2
(no signal) in every cloud run — expected, never a reason to guess.

Repo-scoped MCP tools (`list_branches`, `get_file_contents`) are likewise
restricted to this repo; calls against the other 13 return "not configured for
this session" [cite:2026-08-24][cite:2026-08-25]. **Consequence:** "branch
pushed recently with no PR" is not verifiable from a cloud run at all —
`search_commits` only sees default branches. Open PRs and assigned issues are
fully covered; stranded branches are a blind spot.

What does work: git push/pull to this repo via the credential proxy, and the
built-in `mcp__github__*` tools, which are user-scoped rather than repo-scoped
(`get_me`, `list_commits` here, `search_commits` / `search_issues` /
`search_pull_requests` across the org).

## The contributions signal is not stable

The contributions API flaps — 0/2/3/5 across replicas within minutes — so a
grey reading is only trusted after retries [cite:d96eeef]. Separately, commit
*search* indexing lags a fresh push by around a minute: to verify a commit
just made, prefer `list_commits` over `search_commits` [cite:b85b8af].

## Attribution traps

Two distinct failure modes, both silent:

1. **The invented identity.** With no `user.email` configured, git does not
   warn — it silently invents `user@hostname.local` at commit time. So
   `git config user.email` reads as merely *unset* in exactly the case that
   bites. `git var GIT_AUTHOR_IDENT` reports what the next commit would
   actually use, which is why the scanner reports `author_email_ok` /
   `last_commit_email_ok` as booleans derived from it [cite:60535f0]. Booleans,
   not addresses: the invented identity embeds the machine hostname and
   `local-wip.json` is public [cite:5f41f0a].
   Observed live — six real `tomgreen.ai` commits on 2026-08-27 authored
   `tom@Toms-MacBook-Air.local`, none of them countable [cite:2026-08-27].
   A second invented identity exists from another machine:
   `tom@C2-LAP32-TomGreen.local`, on `ai-capability-app` `24cda31`
   (2026-06-19) — no resolved `author.login`, still uncounted
   [cite:2026-09-01]. The hostname varies by machine, so the check must ask
   "is the author one of the verified addresses", never "is it not this one
   known-bad string".
   **Recovered 2026-08-28**: identity fixed on the Mac, history rewritten
   (`filter-branch --env-filter`, author dates preserved), force-pushed;
   all six now carry the connected author with a resolved GitHub login, and
   zero commits org-wide remain on the invented address [cite:2026-08-28].
   Cost of the day's delay: a one-line config fix became a public-main
   history rewrite — the escalation curve the scout's same-morning nudge
   exists to prevent.
   **Caught pre-push, 2026-08-30:** `ivy`'s own Mac checkout showed 1
   unpushed commit with `last_commit_email_ok: false` — the scout nudged
   same-morning per the playbook's outranking rule, before the commit ever
   reached `main` [cite:2026-08-30]. First observed case of the nudge
   working as designed rather than after the fact [[patterns]].
   **Below the bar, 2026-08-29:** `ai-capability-app` (local `sybil`) has
   `last_commit_email_ok: false` on its one commit from 2026-06-23, but the
   repo is dormant with nothing queued behind it — no same-day work at risk,
   so the "nudge immediately" bar correctly does not fire
   [cite:2026-08-29] [[repos/ai-capability-app]]. Stays uncountable until a
   history rewrite runs, same recipe as the `tomgreen.ai` recovery.
2. **More than one address is connected, and checking against one produced
   false alarms.** `tom@pulsarlabsai.com` is verified on the account — 72
   commits carry it and every one resolves `author.login` [cite:2026-09-01].
   The scanner compared `git var GIT_AUTHOR_IDENT` against `commit_email`
   alone, so repos correctly configured with that address reported
   `author_email_ok: false` and drew same-morning nudges on 2026-08-30 and
   08-31 with nothing to fix [cite:2026-08-30][cite:2026-08-31]. Fixed
   2026-09-01: `config.yml` gained `connected_emails` and the check became
   membership. The cost was not the wasted nudges but the noise — a real
   alarm and a false one looked identical.
3. **Committer is not author.** Only the *author* field decides whether a
   commit counts. Amending the committer of a bot-authored commit to the
   connected address does not make it count — `bc11dd6` was amended that way
   and still does not [cite:2026-08-26].

Bot identity `ivy-bot <bot@ivy.invalid>` (historical:
`bot@evergreen.invalid`) never lights the graph, by design.

## Scheduling

Crons are pinned in **UTC** (07:00 / 16:00 / 20:30) against local Berlin times
of 09:00 / 18:00 / 22:30. When Berlin flips CEST→CET in late October, local
fire times shift to 08:00 / 17:00 / 21:30 — a safe direction, since the
failsafe moves *earlier* and away from the midnight margin.

`local-wip.json` is written by the Mac's launchd scanner at 08:45 and 17:45
local. Past 36h old it means *unknown*, never "nothing pending" — a sleeping
Mac must not read as a clean tree.

## Routine configuration

Routines created without explicit MCP connections inherit **all** of the
account's connectors by default; least privilege requires clearing them
explicitly [cite:b85b8af].

## Changelog

- 2026-09-01 — recorded that `tom@pulsarlabsai.com` is also connected, that
  the single-address check produced false-alarm nudges (now fixed), and that
  a second invented hostname identity exists on `ai-capability-app`.
- 2026-08-30 (retro) — recorded the pre-push attribution catch on `ivy`
  itself and the below-the-bar `sybil` finding; both confirm the attribution
  rule's severity ordering is calibrated correctly, no change made.
- 2026-08-28 — attribution incident marked recovered: Mac identity fixed,
  tomgreen.ai history rewritten and verified clean org-wide.
- 2026-08-27 — page created, synthesized from `playbook.md` ops notes,
  `DESIGN.md` §6, and journals 2026-08-23→27.
