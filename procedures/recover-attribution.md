# Recover commits authored with a disconnected email

**Trigger:** `local-wip.json` reports `author_email_ok: false` or
`last_commit_email_ok: false`, or `search_commits` shows commits whose
author has no resolved GitHub `author.login`.

**Why it matters:** git invents `user@hostname.local` at commit time when
no identity is configured, and never warns. Those commits are real work
that will never count toward the contribution graph. `git config
user.email` reads as merely *unset* in exactly this case, which is why the
scanner checks `git var GIT_AUTHOR_IDENT` instead.

**Executed for real on 2026-08-28** against `tomgreen.ai`: six commits
recovered, author dates preserved, zero commits left on the invented
address org-wide [cite:2026-08-28].

**Cost curve:** one `git config` line before the commits are pushed; a
public-history rewrite afterwards. Fix forward first, always.

---

## Step 0 — fix identity first, so no new bad commits land mid-rewrite

```bash
git config --global user.name  "tompulsarlabs"
git config --global user.email "249609836+tompulsarlabs@users.noreply.github.com"

cd <REPO>
git config --unset user.email 2>/dev/null; git config --unset user.name 2>/dev/null
git var GIT_AUTHOR_IDENT     # MUST show the noreply address
```

Stop here if `git var` shows anything else — something is shadowing the
config, and rewriting history under a wrong identity makes it worse.

If the bad commits have **not** been pushed yet, stop entirely: they are
fixed by `git commit --amend --reset-author` (last commit) or a short
interactive rebase, with no force-push and no recovery risk.

## Step 1 — see exactly what will be rewritten

```bash
git fetch origin && git checkout main && git pull --ff-only origin main
git status --porcelain        # must be empty; commit or stash first
# The invented address embeds the machine hostname, so it differs per
# machine — Toms-MacBook-Air.local and C2-LAP32-TomGreen.local both exist.
# Read the real one off the offending commit rather than assuming:
git log -1 --format='%ae' <BAD_COMMIT_SHA>
BAD="<paste that address>"
git log --author="$BAD" --format='%h %ad %s' --date=format:'%m-%d %H:%M' main
```

Only commits matching that address are touched. Correctly-attributed
history stays byte-identical.

## Step 2 — back up, then rewrite

```bash
git branch backup-pre-rewrite main

BASE=$(git log --reverse --format=%H --author="$BAD" main | head -1)
git filter-branch -f --env-filter '
  if [ "$GIT_AUTHOR_EMAIL" = "'"$BAD"'" ]; then
    export GIT_AUTHOR_NAME="tompulsarlabs"
    export GIT_AUTHOR_EMAIL="249609836+tompulsarlabs@users.noreply.github.com"
  fi
  if [ "$GIT_COMMITTER_EMAIL" = "'"$BAD"'" ]; then
    export GIT_COMMITTER_NAME="tompulsarlabs"
    export GIT_COMMITTER_EMAIL="249609836+tompulsarlabs@users.noreply.github.com"
  fi
' -- "${BASE}^..main"

git log --author="$BAD" main | head -1   # must print NOTHING
```

`--env-filter` rather than `--reset-author`: it preserves author dates, so
recovered commits count on the day they were actually written.

## Step 3 — push

```bash
git push --force-with-lease origin main
```

## Step 4 — verify from outside

```bash
gh api repos/tompulsarlabs/<REPO>/commits \
  --jq '.[0:10][] | .commit.author.date + "  " + .commit.author.email'
```

Every recovered commit must show the noreply address. Then confirm the
count moved for the affected day:

```bash
gh api graphql -f query='query { user(login: "tompulsarlabs") {
  contributionsCollection(from: "<DAY>T00:00:00+02:00", to: "<DAY>T23:59:59+02:00") {
    contributionCalendar { weeks { contributionDays { date contributionCount } } } } }' \
  --jq '.data.user.contributionsCollection.contributionCalendar.weeks[].contributionDays[]
        | select(.date=="<DAY>") | .contributionCount'
```

Graph recalculation can lag up to 24h. Trust the API number; re-run later
rather than re-pushing.

## Step 5 — aftercare

- **Open PRs from before the rewrite** sit on old SHAs. Rebase each:
  `git checkout <branch> && git rebase main && git push --force-with-lease origin <branch>`.
  If that branch has its own bad-email commits, run Step 2 on it first.
- **Other clones** must `git fetch && git reset --hard origin/main`, never pull.
- **Deploy hooks** will fire on the new SHAs. Harmless, but expect a rebuild.
- **Cleanup once satisfied:**
  `git branch -D backup-pre-rewrite` and
  `git for-each-ref --format='%(refname)' refs/original/ | xargs -n1 git update-ref -d`

## Undo

Before the force-push: `git reset --hard backup-pre-rewrite`.
After: the backup branch still holds the original history locally, so the
same reset plus another force-push restores it.

## Known pending uses

`ai-capability-app`'s last local commit (2026-06-23) carries
`last_commit_email_ok: false` and stays uncountable until this runs
[cite:2026-08-29]. It sits below the same-morning nudge bar because
nothing is queued behind it — a deliberate call, not an oversight.
