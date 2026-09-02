# Ivy

Ivy is a set of scheduled agents that keep my software projects moving, and
that remember what they learn while doing it.

It runs three times a day in the cloud (plus a weekly retro), watches 15 repositories, and writes
everything it knows back into this repo as plain files. Nothing is hidden in
a database or a vendor's memory store — the whole system is markdown, JSON,
and git history you can read top to bottom.

## The daily loop

| Run | Time (Berlin) | What it does |
|-----|--------------|--------------|
| Scout | 09:00 | Reads its own memory, syncs the repo list, finds real work worth doing today, writes the candidates into a journal entry. Silent. |
| Check | 18:00 | Asks GitHub whether today counts yet. Green: records it, says nothing. Grey: one push notification naming one specific next action. |
| Failsafe | 22:30 | Confirms the day, verifies finished dispatch work, folds the day's facts into memory. If the day is still grey, writes a real engineering note and commits it. |
| Retro | Sun 10:00 | Reads a week of outcomes, changes at most two things, cites the evidence for each change. |

The failsafe is the floor: if a day would otherwise be empty, Ivy writes a
genuine journal entry rather than faking activity. It has not been needed
once in ten recorded days.

## Four layers of state

Each layer answers a different question, and they stay in their own lanes.

- **`journal/`** — one entry per day. What was available, what happened,
  how the day was verified. This is the raw record.
- **`state.json`** — machine-readable outcomes: streak, per-day counts,
  whether a nudge was sent and whether it converted. Terse; it cites the
  journal for detail. `tomgreen.ai` reads this file live, so the schema is
  append-only.
- **`memory/`** — 12 pages, one per subject: each repo, the environment,
  observed working patterns, routing evidence. Every claim carries a
  citation to a journal date or a commit. Pages link to each other with
  `[[wikilinks]]`. This is the layer that makes run number fifty smarter
  than run number one.
- **`dispatch/`** — work contracts. A scouted candidate becomes a file
  stating the task, the definition of done, and a check that proves it.
- **`procedures/`** — recipes. A task done well once, written down with
  exact commands so it never has to be re-derived from journal history.

## How memory works

Journals and `state.json` are chronological, so answering "has this PR been
nudged before?" used to mean re-reading five days of entries. The `memory/`
wiki fixes that: one page per subject, read at the start of every run.

Two kinds of link do the work. `[[page]]` connects subjects sideways — the
`tomgreen.ai` page links to `ops` because the sandbox limits explain its
verification path. `[cite:2026-08-27]` connects a claim down to the journal
entry that proves it. `scripts/memory-lint.sh` checks that every link and
citation resolves, so the wiki can't rot into confident nonsense.

The failsafe adds facts daily. Only the weekly retro removes them, verifies
claims against their citations, and logs what it pruned.

## How dispatch works

A contract is a markdown file with frontmatter — task, definition of done,
a cloud-checkable verification, a lane, a wall-clock budget. The repo is the
message bus: every state change is a commit, and terminal contracts move
between `queue/`, `done/`, and `failed/`.

Lanes are coarse on purpose: `frontier`, `workhorse`, `fast-cheap`, each
mapped in `config.yml` to a concrete harness and model per provider. Model
names change monthly, so they live in config as data the retro can update,
not baked into behavior.

Execution splits across two machines because it has to. The cloud sandbox's
network access is scoped to this repo alone — it cannot reach OpenAI at all
— so a launchd runner on the Mac executes contracts and holds every
provider login. The cloud never sees a credential.

Workers are not trusted. They push branches and open draft pull requests,
never to a default branch. A contract is only *verified done* when the
failsafe independently runs its verification step and stamps the result.
Worker exit codes are claims; the check is the evidence.

## Rules that don't change

These are marked immutable in `playbook.md`. The weekly retro can tune
timing, wording, and ranking, but it cannot touch these — that needs a
human commit.

1. **Contributions must be real.** No empty commits, no backdating, no
   filler. The failsafe's journal entry is genuine writing about the day.
2. **Verification is external.** "Green" comes from querying GitHub, never
   from a routine's own say-so. Same rule applies to dispatch workers.
3. **Attribution encodes intent.** Bookkeeping commits are authored by
   `ivy-bot` at an address GitHub doesn't recognize, so they never count.
   Only real work and genuine journal entries carry the connected address.
4. **Memory records observations, never instructions.** A page may say
   "nudges on this PR have not converted, 0 of 1 recorded." It may not say
   "stop nudging this PR." Behavior lives in `playbook.md`, and only the
   retro edits it. A memory the agent writes and then obeys is a
   prompt-injection channel with extra steps.
5. **The daily loop outranks everything.** The failsafe secures the day
   before it touches dispatch or memory. A broken sub-system can cost
   routing evidence; it can never cost the streak.

## What it has done

Ten recorded days (23 August–1 September), 142 contributions, all from real
work — the failsafe has never had to fire. Volume is uneven by nature: 46
contributions one day, 1 the next, and both days cleared the bar.

The clearest thing it has caught: on 27 August, six real commits on
`tomgreen.ai` were authored with an email GitHub didn't recognise, so none
of them counted. Git invents `user@hostname.local` silently when identity
is unset, and `git config user.email` reads as merely empty in exactly that
case. The scout spotted it at 07:12 the same morning. Within a day the
scanner had gained a check that uses `git var` instead, the playbook had
been changed to rank attribution failures above every other candidate, the
dispatch layer had gained a gate that refuses to build in a repo that would
author uncountable commits, and the six commits had been rewritten and
recovered. All of it is on the `ops` memory page with citations.

## What isn't working yet

The Mac dispatch runner went live on 1 September, after the queue had sat
unclaimed since 27–28 August — a gap the 30 August retro correctly logged as
infrastructure rather than policy, declining to retune routing when nothing
had run. Its first contract, a cross-family review executed by the OpenAI
lane, produced a findings report and awaits the failsafe's verification
stamp. The same afternoon its attribution gate refused three `tomgreen.ai`
build contracts because the check compared against a single address while
the account has two connected ones — a false positive, fixed by making the
check membership over `connected_emails`. The gate did its job; the test
under it was too narrow.

Two other things are honestly thin. Exactly one nudge has ever been sent
and it didn't convert, which is far too little data to tune notification
timing on. And the dispatch fleet has one verified outcome, well short of
the three the retro requires before moving any lane.

## Layout

```
config.yml       schedule, watchlist, lanes, dispatch limits
playbook.md      operating instructions — immutable rules + tunable behavior
state.json       machine-readable daily outcomes
memory/          the knowledge wiki (INDEX, ops, patterns, models, repos/)
journal/         one engineering note per day
dispatch/        work contracts (DESIGN.md, queue/, done/, failed/, reports/)
procedures/      recipes for recurring operational work
routines/        the four cloud routine definitions
scripts/         check.sh, local-wip.py, memory-lint.sh, dispatch-lint.sh,
                 dispatch-runner.py
setup/           launchd jobs and install helpers
```

`DESIGN.md` covers architecture and failure modes. `dispatch/DESIGN.md`
covers the executive layer. `CHANGELOG.md` tracks every version.

## Influences

Two systems shaped this, both credited in the design docs. Perplexity's
Brain gave the memory model: a wiki of linked markdown over raw evidence,
with citations down and context links sideways. Uber's software-factory
write-up validated the dispatch thesis — optimize a fleet of specialized
agents against per-class targets, and cut waste before you ever downgrade a
model.

Neither was copied wholesale. No vector store, no MCP gateway, no benchmark
suite. At this size `grep` over a small git repo is the retrieval layer,
and a capped weekly experiment is the benchmark.
