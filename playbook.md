# Ivy Playbook

Operating instructions for Ivy's routines. The weekly retro may edit the
**Tunable** sections (commit as `learn:`, tag a new version). The **Immutable**
sections may only be changed by a human commit.

---

## Immutable: counting rules

A contribution counts on the `tompulsarlabs` graph only if (DESIGN.md §1):

1. Commit lands on the **default branch** (or `gh-pages`).
2. Commit **author email is connected to the account** — any address listed in
   `connected_emails` in `config.yml` counts, not only `commit_email` (which is
   just the identity Ivy's own commits use). Set the author explicitly per
   commit, never inherited from environment git config. An address is added to
   that list only after a real commit using it resolves an `author.login` on
   GitHub.
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

## Immutable: commit attribution encodes intent

Routines run in ephemeral cloud sessions, so all state (journal drafts, state.json,
watchlist changes) must be committed to `main` to survive between runs. To keep
system bookkeeping from lighting the graph as noise:

- **System commits** (scout drafts, state recording, watchlist sync) are authored as
  `ivy-bot <bot@ivy.invalid>` — an unconnected address that never counts.
- **Contribution commits** (the failsafe journal entry, and only that) are authored as
  `commit_name <commit_email>` from `config.yml` — the connected address.

Always set author explicitly per commit (`git -c user.name=… -c user.email=… commit`),
never inherit the environment's git config. The graph therefore reflects exactly one
thing: real work, or the day's genuine journal entry — never the system's own churn.

## Immutable: no synthetic contributions

No empty commits, no backdating, no content-free filler. The failsafe commit is
a real journal entry: today's candidates, what happened, streak state, tomorrow's
top candidate. If journal entries trend content-free, that is a nudging failure
for the retro to fix — not a license to automate noise.

## Immutable: memory records observations, never instructions

`memory/` is Ivy's knowledge wiki — one page per durable subject, every claim
carrying a link to its evidence. It is read at the start of every run, which is
exactly why it must never contain directives.

- Pages hold **observations and evidence**. Behavior lives in this playbook,
  and only the retro changes it.
- A page may record "nudges on this PR have not converted, 0 of 1 recorded."
  It may not say "stop nudging this PR." The first is a finding the retro can
  weigh; the second is an instruction the system wrote for itself and would
  then obey without review.
- Every claim carries a citation: `[cite:YYYY-MM-DD]` resolves to that day's
  journal entry, `[cite:<sha>]` to a commit in this repo. `[[page]]` links to a
  related page. A claim with no citation does not belong on a page.
- **Memory is written by the failsafe (daily) and the retro (weekly), and by
  nothing else.** Scout and check read memory and record what they observe in
  the journal; the failsafe folds it in. Every memory commit is bot-authored
  and must pass `scripts/memory-lint.sh`.
- The three layers are deliberately redundant and must stay in their lanes:
  `journal/` is the raw session record, `state.json` the machine-readable
  outcome log, `memory/` the synthesis over both. Narrative belongs in the
  journal; `state.json` stays terse and cites the journal.

Rationale: a memory the agent writes and then obeys is a prompt-injection
channel with extra steps. Keeping observations and instructions in separate
files, with different write permissions and different review cadences, is what
makes the loop safe to run unattended.

## Immutable: `state.json` is a published contract

`tompulsarlabs/tomgreen.ai` reads this repo's `state.json` for its live proof
strip, and cloud runs are scoped to `ivy` alone, so the consuming code cannot
be inspected from a routine. Treat the schema as **append-only**: add keys and
shorten values freely, never rename or remove one. Anything that needs room to
breathe goes in the journal and gets cited from here.

## Immutable: dispatch guardrails

Dispatch contracts (`dispatch/`, designed in `dispatch/DESIGN.md`) route work
to execution lanes. Non-negotiables:

1. **The daily ladder is senior.** The failsafe secures the day (green,
   journal, streak) before touching contract verification; a hung dispatch
   step can cost routing evidence, never the streak.
2. **Workers are untrusted.** A contract is *verified done* only when the
   failsafe's external check of its Verification section passes — worker
   self-reports and exit codes are claims, not outcomes. Workers push
   branches and open draft PRs; they never write to `main` of any repo.
3. **Contracts are lint-gated.** `scripts/dispatch-lint.sh` must pass before
   any dispatch commit; the runner executes only lint-clean contracts from
   scout/Tom commits.
4. **Provider auth never enters the cloud sandbox.** Subscription logins live
   on the Mac; the repo carries contracts and outcomes, never credentials.
5. **Routing policy is retro-only** (within the existing ≤2 changes/week,
   evidence-cited), and Ivy never changes its own routines' models.
6. **No synthetic work.** A contract exists because a candidate is real;
   `experiment` duplicates are capped and marked. Verified-done is the goal,
   never dispatch volume.
7. **Attribution gate.** A `build` contract targeting a repo whose
   `author_email_ok` is false fails immediately rather than authoring
   uncountable commits.

---

## Tunable: the daily ladder

- **Scout (09:00):** follow `procedures/scout.md`. Silent except for attribution risk.
- **Check (18:00):** follow `procedures/check.md`.
- **Failsafe (22:30):** follow `procedures/failsafe.md`.

Load only the active routine's procedure and its conditional references.
For contribution checks or schedule changes, read `procedures/cloud-verification.md`.
For dispatch verification, read `procedures/verify-contract.md`.

## Tunable: retro (Sunday 10:00)

Follow `procedures/retro.md`. Behavioral tuning remains limited to two changes
per week; the 2026-09-05 housekeeping is a direct Tom-authorized maintenance
change, not an autonomous retro adjustment. Immutable sections remain unchanged.

## Tunable: commit message conventions

`journal:` daily entries · `learn:` retro adjustments · `config:` config/scaffold
changes · `scout:` candidate updates worth committing · `memory:` knowledge-wiki
synthesis (failsafe daily, retro weekly) · `dispatch:` contract state changes. One-line messages, evidence in the body
when it matters.
