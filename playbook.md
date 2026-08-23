# Evergreen Playbook

Operating instructions for the Evergreen routines. The weekly retro may edit the
**Tunable** sections (commit as `learn:`, tag a new version). The **Immutable**
sections may only be changed by a human commit.

---

## Immutable: counting rules

A contribution counts on the `tompulsarlabs` graph only if (DESIGN.md §1):

1. Commit lands on the **default branch** (or `gh-pages`).
2. Commit **author email is connected to the account** — use `commit_email` from
   `config.yml`, set explicitly per commit, never inherited from environment git config.
3. The repo is **not a fork**.
4. Private-repo activity shows only if the profile's "Private contributions"
   toggle is on. This repo stays public.

PRs opened, issues opened, and PR reviews also count — treat "review an open PR"
as a first-class candidate.

## Immutable: verification

"Green" is defined by `scripts/check.sh` (GraphQL `contributionsCollection`
for today in `Europe/Berlin`), never by the rendered graph. After any failsafe
commit, re-run the check until today ≥ 1; if it stays 0 after 3 attempts over
15 minutes, alert loudly with the misconfig checklist: email? branch? fork? visibility?

## Immutable: no synthetic contributions

No empty commits, no backdating, no content-free filler. The failsafe commit is
a real journal entry: today's candidates, what happened, streak state, tomorrow's
top candidate. If journal entries trend content-free, that is a nudging failure
for the retro to fix — not a license to automate noise.

---

## Tunable: the daily ladder

- **Scout (09:00)** — sync watchlist (`gh api user/repos`, minus forks/archived/excludes).
  Gather candidates: open PRs close to merge, assigned issues, branches with recent
  pushes but no PR, yesterday's carry-over. Draft `journal/<today>.md` locally in the
  run (committed only by failsafe or by real activity notes). Silent.
- **Check (18:00)** — run `scripts/check.sh`. Green → record outcome in state, stay
  silent. Grey → one notification naming the single most concrete candidate.
- **Failsafe (22:30)** — still grey → finalize today's journal entry, commit to
  `main` with author from `config.yml`, push, verify per the immutable rule.
  Record outcome either way: `state.json` gets `{date: {green_by, method, nudge_sent,
  nudge_converted, failsafe_fired}}`; bump or reset `streak`.

## Tunable: retro (Sunday 10:00)

Read the last 7–30 days of `state.json`. Answer: how often did the failsafe fire?
Did nudges convert to real activity within 4 hours? Which repos produced shipped
work? Then make at most two adjustments (nudge time, wording, ranking, excludes) by
editing this file and/or `config.yml`. Commit as `learn: <what> — <evidence>`, tag
the next version, and summarize in `CHANGELOG.md`.

## Tunable: commit message conventions

`journal:` daily entries · `learn:` retro adjustments · `config:` config/scaffold
changes · `scout:` candidate updates worth committing. One-line messages, evidence
in the body when it matters.
