# Setting Ivy up from scratch

Two halves: four cloud routines (scheduled Claude Code runs) and one local
launchd job (the WIP scanner). Everything else is state in this repo.

## 1. Prerequisites

- A GitHub account whose noreply address matches `commit_email` in
  `config.yml` (the connected-address rule in `playbook.md` is what makes
  contributions count).
- Claude Code with cloud routines (claude.ai/code → routines).
- A Mac (or any always-on-ish machine) for the local scanner. Python 3 and
  git on PATH; nothing else.

## 2. Cloud routines

Create one scheduled routine per file in [`routines/`](../routines/) —
scout, check, failsafe, retro. Each file records the schedule (UTC cron +
local intent), the prompt text, and the live trigger ID. The prompts are
deliberately thin pointers into `playbook.md`, which is the single source
of operating truth; the retro tunes behavior by editing the playbook, so
the cloud configuration rarely needs touching.

The routine sandbox is repo-scoped (see the ops notes in `playbook.md`):
no `gh`, no GraphQL, only this repo's git remote plus the built-in GitHub
MCP tools. The playbook's cloud verification path exists because of this.

## 3. Local WIP scanner

The scanner publishes each local repo's name, branch, and dirty/unpushed
counts (no hostname, no paths) to `local-wip.json` so the morning scout
sees work that only exists on the laptop.

```bash
cp setup/ai.tomgreen.ivy-wip.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/ai.tomgreen.ivy-wip.plist
```

The plist runs `scripts/local-wip.sh` (a thin wrapper around
`scripts/local-wip.py`) at 08:45 and 17:45 local — just before the scout
and check routines fire. Adjust `local_wip.roots` in `config.yml` to
choose which directories are scanned. Run `./scripts/local-wip.sh` once by
hand to verify.

## 4. Nudges

Grey-day nudges use Claude Code's push notifications (verified reaching a
phone from cloud runs); Google Calendar events are the documented
fallback. Nothing to configure beyond being signed into the Claude app on
the phone.

## 5. Sanity checks

- `scripts/check.sh` locally: exits 0 on a green day, 1 on grey (needs
  `gh` authed; in the cloud sandbox it exits 2 — expected, the routines
  use the MCP verification path instead).
- After the first failsafe commit, confirm the contribution square lit;
  if not, walk the misconfig checklist in `playbook.md`.
