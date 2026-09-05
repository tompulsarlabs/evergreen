# Scout procedure

Loaded only for this routine. Shared constraints remain in `playbook.md`.

- **Scout (09:00)** — **orient first:** read `memory/INDEX.md`, then
  `memory/ops.md` and the `memory/repos/<name>.md` page for every repo that
  produces a candidate. That is the standing context — what this repo is, what
  has been tried, what the environment will refuse to do — and it is much
  cheaper than re-deriving it from journal history. Follow a `[cite:...]` down
  to the journal only when a claim is decision-critical or looks stale; adopt
  it directly otherwise.
  Then sync watchlist (`gh api user/repos`, minus forks/archived/excludes).
  Gather candidates: open PRs close to merge, assigned issues, branches with recent
  pushes but no PR, yesterday's carry-over.
  **Rank by value, not by cheapness.** Tom's focus is revealed, not declared:
  repos with Tom-authored commits in the last 7 days, local WIP, and draft
  PRs he updated this week rank above any "cheapest ship" on a stale PR.
  A repo in `config.yml` `watchlist.parked` is watched only — its
  contributions count and its attribution is scanned — and produces no
  candidate, contract, or audit; it leaves `parked` by Tom's commit or a
  retro `learn:`. Evidence: `c2-client-matrix` #1 was the fallback pick for
  eight runs with zero conversions before Tom parked it (2026-09-03).
  **Also hunt blockers, not just candidates.** A candidate produces a
  contribution today; a blocker stops future work from happening at all —
  a dead runner, an expired credential, a queue nothing is draining, a
  broken local scan, an unmerged fix everything else waits on. Blockers are
  invisible to a "cheapest ship today" ranking because their contribution
  count is zero, which is exactly why they rot. **Read
  `dispatch/runner-status.json`** — the Mac runner's heartbeat, committed when
  its state changes and at least every 6 hours inside the window. `harness`
  false or `lint_ok` false is a blocker from the first morning: every
  contract waits on it. `last_tick` older than 3 hours inside the runner
  window with contracts open means the runner is not ticking — a sleeping
  Mac or an unloaded launchd job; name it, never guess which. `skipped`
  says why each open contract was passed over. Name any blocker in the
  journal under `## Blockers` with what it stops and the smallest next
  action; carry it forward every day until it clears or is explicitly
  declined. A blocker that has persisted three days outranks the day's
  cheapest ship in the nudge. **Also read `local-wip.json`** (pushed by
  the Mac's launchd scanner at 08:45/17:45): repos with `unpushed_commits > 0` or
  `remote: none` are first-class candidates — "push X (N unpushed commits)" is often
  the cheapest real ship of the day. Staleness rule: if its `generated_at` is older
  than 36h, treat local WIP as *unknown* (say so in the journal), never as "nothing
  pending" — a sleeping Mac must not lie to the scout.
  **Attribution check (outranks every other candidate):** any repo with
  `author_email_ok: false` will author its next commit as an address that is not
  connected to the account, so that work cannot count (rule 2) no matter how real
  it is. `last_commit_email_ok: false` means it has already happened. Lead the
  journal with it and nudge immediately rather than waiting for the 18:00 check —
  the fix is one `git config` line while it's cheap, and a history rewrite once
  the commits are pushed. This is the one scout finding that breaks the "silent"
  rule, because by 18:00 a whole day of real work may already be uncountable.
  Draft `journal/<today>.md`
  and commit it **bot-authored** (`scout: <date> — <n> candidates, top:
  <one-liner>`). Silent.
  **Emit dispatch contracts** for the top candidates: up to
  `dispatch.daily_cap` minus contracts already created today, using the
  contract format in `dispatch/DESIGN.md` §2. Review contracts pin the
  family that did not author the PR. Run `scripts/dispatch-lint.sh`, commit
  bot-authored (`dispatch: open <id>`). Execution is the runner's job — the
  scout only queues. A contract is a ticket in the `to-tickets` sense: one
  vertical slice, complete and verifiable on its own, sized for a single
  worker session. Work that needs more than one slice is published as a
  chain — later contracts carry `blocked_by` with the earlier ids — never as
  one oversized contract. Write contracts in `CONTEXT.md` vocabulary.
  Anything learned along the way — a repo that has gone quiet, a new access
  limit, a candidate that keeps resurfacing — goes in the journal entry, not
  into `memory/`. The failsafe folds it in tonight; the scout never edits
  memory pages.

Every new contract declares `verification_checks` as unique IDs and defines each
criterion in its Verification section before execution. Choose checks that inspect
the actual result, not merely the existence of a worker report. See
`procedures/verify-contract.md` and the relevant role in `evals/agents.json`.
