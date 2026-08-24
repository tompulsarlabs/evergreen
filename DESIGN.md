# Ivy — Agentic Daily Shipping

**Goal:** projects move forward every day — backlog scouted each morning, one real thing shipped before the day closes, outcomes logged and learned from. The `tompulsarlabs` contribution graph is the heartbeat metric (≥1 genuine contribution per day): the system nudges toward shipping real project work first, closes the day with a real engineering journal entry when needed, learns from its own outcome history, and tracks its entire evolution in git.

**Stance:** no empty commits, no backdating, no synthetic noise. The failsafe commit is a genuine daily engineering journal — the system makes you ship, it doesn't fake it.

---

## 1. Hard constraints: GitHub's counting rules

Rules 1–5 verified against GitHub's docs on 2026-08-22. Rule 6 (timezone) is not confirmed in the docs pages checked — the design covers it with scheduling margin plus API verification, which makes the exact boundary rule immaterial. These are the rules most likely to make the system "work" while the graph stays grey, so they are design constraints, not footnotes.

| # | Rule | Design consequence |
|---|------|--------------------|
| 1 | Only commits on the **default branch** (or `gh-pages`) count | Failsafe commits go straight to `main` of the state repo |
| 2 | Commit **author email must be connected to the GitHub account** | Setup verifies `git config user.email` against `gh api user/emails`; safest value is the noreply form `<id>+tompulsarlabs@users.noreply.github.com` |
| 3 | Commits in **forks never count** | Watchlist excludes forks; state repo is standalone |
| 4 | **Private-repo** contributions show only anonymized, and only if the profile's "Private contributions" toggle is on | Decision: make the state repo **public** (journal content kept non-sensitive). Fallback: private repo + toggle on |
| 5 | Graph rendering can lag **up to 24h** (usually minutes) | Verification queries the GraphQL API, never the rendered graph |
| 6 | The day a commit lands on follows the **commit timestamp's timezone** | All schedules and timestamps pinned to `Europe/Berlin`; nothing runs within 90 minutes of midnight |

---

## 2. Architecture

One source of truth: a public repo **`tompulsarlabs/ivy`**. It is simultaneously the system's config, its memory, its guaranteed-green floor, and its version history.

```
ivy/
├── config.yml        # watchlist repos, cutoff times, timezone, notification prefs
├── playbook.md       # the agent's own operating instructions — the learning loop edits THIS
├── state.json        # machine-readable: streak, last-green date, per-day outcome log
├── journal/
│   └── 2026-08-22.md # one entry per day: what was shippable, what happened, streak
└── CHANGELOG.md      # human summary of playbook revisions, tagged v1, v2, …
```

**Runtime:** Claude Code **cloud scheduled agents** (routines) — chosen so the loop runs even when the Mac is asleep or closed. Three daily runs implement the escalation ladder:

| Run | Time (Berlin) | Behavior |
|-----|--------------|----------|
| **Scout** | 09:00 | First auto-sync the watchlist from `gh api user/repos` (forks and archived excluded — forks can't count anyway), honoring manual excludes in `config.yml`, so "all projects" never depends on a hand-curated list. Then enumerate real shippable candidates: open PRs one review from merge, assigned issues, stale branches, yesterday's carry-over. Write candidates into today's journal entry (uncommitted draft in state.json). Quiet — no notification unless the streak is at risk from day one. |
| **Check + nudge** | 18:00 | Query `contributionsCollection` for today. **Green → log outcome, stay silent.** Grey → push notification with the single most concrete candidate: "Grey so far. sybil PR #12 is one review from merge." |
| **Failsafe** | 22:30 | Still grey → finalize today's journal entry (scout findings, what actually happened, streak state, tomorrow's top candidate), commit to `main`, push. Then **verify**: re-query the API until today's count ≥ 1. If verification fails, alert loudly — that catches email/branch/visibility misconfig the moment it happens, not weeks later. |

The ladder prefers real work by construction: 13.5 hours of runway between scout and failsafe, and the nudge always points at a concrete next action in a real project rather than a generic reminder.

**Attribution note (cloud):** the failsafe commit runs in the cloud sandbox, where this Mac's `git config` doesn't exist — inheriting environment config there is exactly the silent-grey email failure from rule #2. Author identity must be explicit per commit: either pass author/email in the commit command, or commit via GitHub's Contents API (`PUT /repos/{owner}/{repo}/contents/{path}`), which attributes to the token owner when author is omitted — confirm that behavior against the REST docs during Phase 1.

**The authoritative check** (this is what "green" means — commits, PRs, issues, and reviews all count, exactly matching the graph):

```graphql
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks { contributionDays { date contributionCount } }
      }
      restrictedContributionsCount   # private-repo activity
    }
  }
}
```

`from`/`to` are set to today's 00:00:00 and 23:59:59 **with the +02:00/+01:00 Berlin offset**, so "today" means the same thing to the checker and to the graph.

Because PRs, issues, and reviews count too, the scout treats "review that open PR" as a first-class candidate — often the cheapest real contribution of the day.

---

## 3. The self-learning loop

A weekly **retro run** (Sunday 10:00) closes the loop:

1. **Read** the last 7–30 days of `state.json` outcomes: how often did the failsafe fire? Which nudges converted into real commits within 4 hours? Which repos actually produce shipped work? What time of day do real commits land?
2. **Decide** one or two adjustments: shift the nudge earlier, reword it, re-rank the watchlist, add a second nudge, retire a dead repo.
3. **Act** by editing `playbook.md` / `config.yml` — the next day's runs read the updated playbook, so behavior changes take effect immediately.
4. **Record** with a `learn:` commit and a version tag.

The system's git history *is* its learning record. Every behavior change is a readable, revertible diff:

```
journal: 2026-08-22 — grey at 22:30, failsafe fired (streak 12)
learn:   shift nudge 18:00 → 17:00 — 3 of 4 failsafe days had no activity after 18:00   (tag: v3)
config:  add tompulsarlabs/sybil to watchlist
scout:   2026-08-23 — 3 candidates, top: sybil #12 needs review
```

Commit-message prefixes (`journal:` `learn:` `config:` `scout:`) plus tags on every playbook revision satisfy the clear-history and version-tracking requirements without any extra machinery.

**Guardrail:** the retro may tune timing, wording, and ranking. It may not change the counting rules (§1), the verification step, or the no-synthetic-commits stance — those are marked immutable in `playbook.md`, and changing them requires a human commit.

---

## 4. Prerequisites (current blockers)

1. **`gh` re-auth** — the token for `tompulsarlabs` on this Mac is expired. Run `! gh auth login` in this session (interactive, so it needs you).
2. **Email verification** — after auth: `gh api user/emails`, then set the state repo's `user.email` to a connected address (rule #2). This is the single most common silent-grey cause; the session's default email `tom@tomgreen.ai` may not be on the `tompulsarlabs` account.
3. **Cloud agent GitHub access** — the routines run in Claude's cloud, so they need their own path to GitHub: the Claude GitHub connector covering `ivy` (and read access to watchlist repos), or a fine-grained PAT (contents: write on `ivy` only) stored for the routine.
4. **Repo visibility decision** — public `ivy` (recommended) or private + "Private contributions" toggle on.
5. **Timezone confirmation** — Mac says `Europe/Berlin`; confirm that's the intended anchor for "today."

---

## 5. Build phases

| Phase | Scope | Exit criterion |
|-------|-------|----------------|
| **0 — Unblock** (~15 min) | Prereqs 1–5 above | `gh auth status` clean; email confirmed connected |
| **1 — Prove counting** | Create `ivy` repo, journal template, `check` script wrapping the GraphQL query. Run the loop **manually once**: journal commit → API shows today ≥ 1 | Green verified via API minutes after a journal commit |
| **2 — Schedule** | Three cloud routines (scout / check / failsafe) + push notifications; 3-day soak. Soak must also confirm notifications from *cloud* runs actually reach the phone — if they don't, pick a fallback channel (email/Slack) before relying on the nudge | Ladder observed end-to-end on a real grey day; silent on a green day; nudge confirmed received |
| **3 — Learn** | Weekly retro run; playbook + CHANGELOG + tags; tag `v1` | First `learn:` commit produced from real outcome data |
| **4 — Local enrichment** (optional) | launchd job on the Mac pushes local WIP status (dirty repos, unpushed branches in `~/Build`) into `state.json` so the scout sees local truth | Scout candidates include local uncommitted work when the Mac is awake |

Phase 4 is deliberately optional: the cloud-only core never depends on the Mac being awake, which is the whole reason the streak is safe.

---

## 6. As built (2026-08-23)

Deviations from the plan above, discovered via three forced cloud test runs:

- **The cloud sandbox's github.com egress is entirely repo-scoped** — GraphQL, REST,
  and even the public contributions HTML all 403 there. Verification is now a ladder:
  GraphQL `contributionsCollection` (local/gh) → public contributions-HTML `data-level`
  parse (anywhere unproxied; `scripts/check.sh` does both) → **built-in GitHub MCP
  tools** in cloud runs (`list_commits` on ivy + `search_commits`/`search_issues`/
  `search_pull_requests` cross-repo; user-scoped, verified working).
- **Nudge channel is PushNotification** — verified reaching mobile from cloud runs;
  the Google Calendar event is the fallback, not the primary.
- **Attribution encodes intent**: cloud runs are ephemeral, so scout drafts and state
  must be committed to survive between runs; those bookkeeping commits are authored
  `ivy-bot <bot@ivy.invalid>` (unconnected → never lights the graph), and
  only failsafe journal entries + real work carry the connected author. Validated
  live: bot-authored state commit pushed from cloud, graph unaffected.
- **The contributions API flaps** (0/2/3/5 across replicas within minutes) — grey is
  only trusted after retries; a fresh push can transiently read as 0.
- Routines created with no explicit MCP connections get **all** the user's connectors
  attached by default — least-privilege requires explicitly clearing them.

## 7. Failure modes

| Failure | Mitigation |
|---------|-----------|
| Mac asleep/off | Core loop is cloud-side by design |
| Cloud token/auth expires | Every run alerts on auth failure; failsafe verification catches silent write failures |
| Committed but still grey | Verification step fails loudly same-night → checklist in playbook (email? branch? fork? visibility?) |
| Near-midnight timezone edge | Nothing scheduled after 22:30; timestamps pinned to Europe/Berlin |
| Notification fatigue | Silent when green; retro tunes frequency and time using conversion data |
| Journal rot (entries become filler) | Entries are structured around real candidates and outcomes; retro flags low-content streaks as a smell — the failsafe firing daily means the *nudging* is failing, which is exactly what the retro is for |
| Runaway self-modification | Immutable sections in playbook; every change is a tagged, revertible commit |
