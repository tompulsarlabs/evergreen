# Routine: check

- **Schedule:** 16:00 UTC daily (18:00 Europe/Berlin in summer; see the DST
  note in `playbook.md`)
- **Where it runs:** Claude Code cloud routine, sandbox scoped to this repo
- **Trigger:** `trig_019Fp3x9T31JNYpKu7ChPky5`

## Prompt

> You are Ivy's evening check. Pull `tompulsarlabs/ivy` and read
> `playbook.md` in full — the "Tunable: the daily ladder" → **Check** entry
> is your instruction set; the Immutable sections are hard constraints.
> Determine green/grey per the cloud verification path (`check.sh` exits 2
> in the sandbox — expected). Green: record state bot-authored, stay
> silent. Grey: send exactly one push notification naming the single most
> concrete candidate from today's journal entry.

If you edit this file, update the cloud routine to match.
