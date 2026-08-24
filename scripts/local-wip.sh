#!/usr/bin/env bash
# Scan local project roots for git repos and publish their WIP state to
# local-wip.json so the cloud scout sees local truth (dirty trees, unpushed
# commits, repos with no remote at all — the tomgreen.ai-shaped gaps).
#
# Guards: explicit PATH (launchd runs with a bare env); quiet no-op on any
# git/network failure (never clobber good state with partial data); rebase-
# tolerant push (cloud routines write to the same main); no commit when
# nothing changed (no daily noise).
set -uo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

IVY="${IVY_DIR:-$HOME/Build/ivy}"
OUT="$IVY/local-wip.json"

# Roots from config.yml (local_wip: roots: [...]), fallback ~/Build
ROOTS=$(awk '/^local_wip:/{f=1;next} f&&/^[^ ]/{f=0} f&&/^  roots:/{r=1;next} f&&r&&/^    - /{print $2} f&&r&&!/^    - /{r=0}' "$IVY/config.yml" 2>/dev/null)
[ -z "$ROOTS" ] && ROOTS="$HOME/Build"

TMP=$(mktemp)
{
  echo "{"
  echo "  \"generated_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
  echo "  \"host\": \"$(hostname -s)\","
  echo "  \"repos\": ["
  first=1
  for ROOT in $ROOTS; do
    ROOT="${ROOT/#\~/$HOME}"
    [ -d "$ROOT" ] || continue
    while IFS= read -r gitdir; do
      repo=$(dirname "$gitdir")
      cd "$repo" 2>/dev/null || continue
      branch=$(git branch --show-current 2>/dev/null || echo "")
      [ -z "$branch" ] && branch="(detached)"
      dirty=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
      if [ -z "$(git remote 2>/dev/null)" ]; then
        remote="none"
        unpushed=$(git rev-list --count HEAD 2>/dev/null || echo 0)
      else
        remote=$(git remote get-url origin 2>/dev/null | sed 's|https://github.com/||;s|\.git$||' || echo "other")
        unpushed=$(git rev-list --count --branches --not --remotes 2>/dev/null || echo 0)
      fi
      last=$(git log -1 --format=%cs 2>/dev/null || echo "")
      [ $first -eq 0 ] && echo "    ,"
      first=0
      printf '    {"path": "%s", "remote": "%s", "branch": "%s", "dirty_files": %s, "unpushed_commits": %s, "last_commit": "%s"}\n' \
        "${repo/#$HOME/~}" "$remote" "$branch" "$dirty" "$unpushed" "$last"
    done < <(find "$ROOT" -maxdepth 3 -name .git -type d 2>/dev/null)
  done
  echo "  ]"
  echo "}"
} > "$TMP"

# No-op if nothing but the timestamp changed
if [ -f "$OUT" ] && diff -q <(grep -v generated_at "$OUT") <(grep -v generated_at "$TMP") >/dev/null 2>&1; then
  rm -f "$TMP"; exit 0
fi

mv "$TMP" "$OUT"
cd "$IVY" || exit 0
git add local-wip.json
git -c user.name=ivy-bot -c user.email=bot@ivy.invalid \
  commit -q -m "wip: local scan — $(grep -c '"path"' local-wip.json) repos" || exit 0
git pull --rebase -q 2>/dev/null || { git rebase --abort 2>/dev/null; exit 0; }
git push -q 2>/dev/null || exit 0
