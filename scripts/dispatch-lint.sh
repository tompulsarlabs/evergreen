#!/usr/bin/env bash
# Deterministic validation for dispatch contracts (dispatch/{queue,done,failed}/*.md).
#
# Checks frontmatter schema, id/filename agreement, known repo and lane,
# state/directory consistency, blocked_by ids, required body sections, sane
# dates, outcome blocks on terminal contracts, and the daily creation cap. Semantic checks —
# is the work real, did verification actually pass — belong to the routines,
# not this script. Exit 0 clean, 1 on any violation.
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

fail=0
count=0
err() { printf 'dispatch-lint: %s\n' "$1" >&2; fail=1; }

[ -d dispatch ] || { echo "dispatch-lint: no dispatch/ directory — nothing to check"; exit 0; }

# Authoritative sets come from config.yml, not from this script.
lanes=$(sed -n '/^lanes:/,/^[a-z]/p' config.yml | grep -E '^  [a-z-]+:' | sed 's/^ *//; s/:.*//' | sort -u)
repos=$(sed -n '/^  repos:/,/^[a-z#]/p' config.yml | grep -E '^ *- ' | sed 's/^ *- //')
cap=$(grep -E '^  daily_cap:' config.yml | sed 's/.*: *//; s/ .*//')
[ -n "$lanes" ] || err "config.yml: no lanes: block found"
[ -n "$cap" ] || err "config.yml: no dispatch.daily_cap found"

fm_get() { printf '%s\n' "$1" | sed -n "s/^$2:[[:space:]]*//p" | head -1; }

declare -A created_per_day

while IFS= read -r f; do
  count=$((count + 1))
  base=$(basename "$f" .md)
  dir=$(basename "$(dirname "$f")")

  if [ "$(head -1 "$f")" != "---" ]; then
    err "$f: missing frontmatter (first line must be ---)"
    continue
  fi
  fm=$(sed -n '2,/^---$/p' "$f")

  for key in id type state repo lane created created_by expires budget; do
    printf '%s\n' "$fm" | grep -q "^$key:" || err "$f: frontmatter missing '$key:'"
  done

  id=$(fm_get "$fm" id); type=$(fm_get "$fm" type); state=$(fm_get "$fm" state)
  repo=$(fm_get "$fm" repo); lane=$(fm_get "$fm" lane); pool=$(fm_get "$fm" pool)
  created=$(fm_get "$fm" created); expires=$(fm_get "$fm" expires)
  created_by=$(fm_get "$fm" created_by)

  [ "$id" = "$base" ] || err "$f: id '$id' does not match filename"
  case "$type" in build|review|chore|experiment) ;; *) err "$f: unknown type '$type'";; esac
  case "$created_by" in scout|tom) ;; *) err "$f: created_by '$created_by' not scout|tom";; esac
  [ -z "$pool" ] || case "$pool" in anthropic|openai) ;; *) err "$f: unknown pool '$pool'";; esac
  printf '%s\n' "$lanes" | grep -qx "$lane" || err "$f: lane '$lane' not in config.yml lanes"
  printf '%s\n' "$repos" | grep -qx "$repo" || err "$f: repo '$repo' not in config.yml watchlist"

  # state must agree with the directory the contract lives in
  case "$dir" in
    queue)  case "$state" in open|claimed) ;; *) err "$f: state '$state' invalid in queue/ (open|claimed)";; esac ;;
    done)   [ "$state" = "done" ] || err "$f: state '$state' invalid in done/ (done)" ;;
    failed) case "$state" in failed|expired) ;; *) err "$f: state '$state' invalid in failed/ (failed|expired)";; esac ;;
  esac

  # terminal contracts carry an outcome block; done may carry a verified stamp
  if [ "$dir" != "queue" ]; then
    grep -q '^outcome:' "$f" || err "$f: terminal contract has no outcome: block"
  fi
  v=$(grep -E '^ *verified:' "$f" | head -1 | sed 's/.*: *//')
  [ -z "$v" ] || case "$v" in true|false) ;; *) err "$f: verified '$v' not true|false";; esac

  # blocked_by: optional inline list of contract ids that must reach done/ first
  if printf '%s\n' "$fm" | grep -q '^blocked_by:'; then
    bb=$(fm_get "$fm" blocked_by)
    ids=$(printf '%s' "$bb" | tr -d '[]' | tr ',' '\n' | sed 's/^ *//; s/ *$//' | grep -v '^$')
    [ -n "$ids" ] || err "$f: blocked_by must be an inline list, e.g. blocked_by: [id, id]"
    while IFS= read -r b; do
      [ -n "$b" ] || continue
      [ "$b" != "$id" ] || err "$f: blocked_by names itself"
      [ -e "dispatch/queue/$b.md" ] || [ -e "dispatch/done/$b.md" ] || [ -e "dispatch/failed/$b.md" ] \
        || err "$f: blocked_by '$b' is not a contract in dispatch/"
    done <<< "$ids"
  fi

  # required body sections
  for sec in '## Task' '## Definition of done' '## Verification'; do
    grep -qF "$sec" "$f" || err "$f: missing body section '$sec'"
  done

  # dates parse and expires > created
  python3 - "$f" "$created" "$expires" <<'PY' || fail=1
import sys
from datetime import datetime
f, created, expires = sys.argv[1], sys.argv[2], sys.argv[3]
def parse(label, s):
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        print(f"dispatch-lint: {f}: {label} '{s}' is not an ISO datetime", file=sys.stderr)
        return None
c, e = parse("created", created), parse("expires", expires)
if c and e and e <= c:
    print(f"dispatch-lint: {f}: expires is not after created", file=sys.stderr)
    sys.exit(1)
sys.exit(0 if (c and e) else 1)
PY

  day=${created%%T*}
  [ -n "$day" ] && created_per_day[$day]=$(( ${created_per_day[$day]:-0} + 1 ))
done < <(find dispatch/queue dispatch/done dispatch/failed -name '*.md' 2>/dev/null | sort)

# daily creation cap (config: dispatch.daily_cap)
if [ -n "${cap:-}" ]; then
  for day in "${!created_per_day[@]}"; do
    n=${created_per_day[$day]}
    [ "$n" -le "$cap" ] || err "daily cap exceeded: $n contracts created $day (cap $cap)"
  done
fi

[ "$fail" -eq 0 ] && echo "dispatch-lint: ok — $count contracts, schema and cap hold"
exit "$fail"
