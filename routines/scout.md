# Routine: scout

- **Schedule:** 07:00 UTC daily (09:00 Europe/Berlin in summer; see the DST
  note in `playbook.md`)
- **Where it runs:** Claude Code cloud routine, sandbox scoped to this repo
- **Trigger:** `trig_01P42rzh3kFT9yVTW1E6WoXW`

## Prompt

> You are Ivy's morning scout. Pull `tompulsarlabs/ivy` and read
> `playbook.md` in full — the "Tunable: the daily ladder" → **Scout** entry
> is your instruction set for this run; the Immutable sections are hard
> constraints. Sync the watchlist, gather today's candidates (including
> `local-wip.json` per the staleness rule), draft `journal/<today>.md`, and
> commit it bot-authored. Silent — no notifications from this routine.

The prompt is deliberately thin: `playbook.md` is the single source of
operating truth, so the retro can tune behavior without touching the cloud
configuration. If you edit this file, update the cloud routine to match.
