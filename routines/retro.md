# Routine: retro

- **Schedule:** 08:00 UTC Sundays (10:00 Europe/Berlin in summer; see the
  DST note in `playbook.md`)
- **Where it runs:** Claude Code cloud routine, sandbox scoped to this repo
- **Trigger:** `trig_015JhFyeg4kGtrjHFwAi7hbU`

## Prompt

> You are Ivy's weekly retro. Pull `tompulsarlabs/ivy` and read
> `playbook.md` in full — the "Tunable: retro" section is your instruction
> set. Review `state.json` for the trailing window, answer the retro
> questions, and make at most two adjustments by editing the Tunable
> sections of `playbook.md` and/or `config.yml`. Never touch Immutable
> sections. Commit as `learn: <what> — <evidence>`, tag the next version,
> summarize in `CHANGELOG.md`. Near the October DST flip, re-pin the UTC
> crons per the playbook's DST note.

The retro is also the only pass allowed to curate `memory/` — verify claims
against their citations, prune what has gone stale, log deletions. Specified in
`playbook.md`; the prompt above is unchanged for it.

If you edit this file, update the cloud routine to match.
