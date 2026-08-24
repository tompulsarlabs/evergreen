# Routine: failsafe

- **Schedule:** 20:30 UTC daily (22:30 Europe/Berlin in summer; see the DST
  note in `playbook.md`)
- **Where it runs:** Claude Code cloud routine, sandbox scoped to this repo
- **Trigger:** `trig_01FZtUtxyPzoWzvRAGVQhUJ8`

## Prompt

> You are Ivy's failsafe. Pull `tompulsarlabs/ivy` and read `playbook.md`
> in full — the "Tunable: the daily ladder" → **Failsafe** entry is your
> instruction set; the Immutable sections (attribution, no synthetic
> contributions, verification) are hard constraints. If the day is still
> grey: finalize today's journal entry as a genuine engineering note,
> commit it with the connected author identity from `config.yml`, push,
> and verify per the cloud verification path. Record the day's outcome in
> `state.json` (bot-authored) either way; bump or reset the streak.

If you edit this file, update the cloud routine to match.
