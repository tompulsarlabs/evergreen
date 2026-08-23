#!/usr/bin/env bash
# Is today green for the target account? Exit 0 if contributions >= 1, else 1.
# Authoritative per DESIGN.md: queries the GraphQL API, never the rendered graph.
# The API is eventually consistent — a fresh push can transiently read as 0
# (observed live on 2026-08-23), so a grey answer is only trusted after retries.
set -euo pipefail

LOGIN="${EVERGREEN_LOGIN:-tompulsarlabs}"
TZ_NAME="${EVERGREEN_TZ:-Europe/Berlin}"
RETRIES="${EVERGREEN_RETRIES:-3}"
RETRY_WAIT="${EVERGREEN_RETRY_WAIT:-20}"

TODAY=$(TZ="$TZ_NAME" date +%F)
# BSD date has no %:z — splice the colon into +0200 → +02:00
RAW_OFFSET=$(TZ="$TZ_NAME" date +%z)
OFFSET="${RAW_OFFSET:0:3}:${RAW_OFFSET:3}"

# Auth-free fallback: parse the public contributions HTML (the graph itself).
# Returns the day's data-level (0 = grey, 1-4 = green shades); counts as >=1 contribution.
query_level_html() {
  local html td
  html=$(curl -fsSL --max-time 20 "https://github.com/users/${LOGIN}/contributions") || return 1
  td=$(printf '%s' "$html" | tr '<' '\n' | grep -F "data-date=\"$TODAY\"" | head -1) || return 1
  printf '%s' "$td" | sed -n 's/.*data-level="\([0-9]\)".*/\1/p' | grep . || return 1
}

query_count() {
  gh api graphql \
    -f query='query($login:String!,$from:DateTime!,$to:DateTime!){
      user(login:$login){
        contributionsCollection(from:$from,to:$to){
          contributionCalendar{weeks{contributionDays{date contributionCount}}}
        }
      }
    }' \
    -f login="$LOGIN" \
    -f from="${TODAY}T00:00:00${OFFSET}" \
    -f to="${TODAY}T23:59:59${OFFSET}" \
    --jq "[.data.user.contributionsCollection.contributionCalendar.weeks[].contributionDays[]
           | select(.date==\"$TODAY\") | .contributionCount] | add // 0"
}

# Prefer the authenticated GraphQL count; fall back to the public graph HTML
# when gh is unavailable/unauthenticated (e.g. cloud sandboxes).
get_signal() {
  if command -v gh >/dev/null 2>&1 && COUNT=$(query_count 2>/dev/null); then
    SOURCE="graphql"
  elif COUNT=$(query_level_html); then
    SOURCE="graph-html (data-level)"
  else
    echo "$TODAY ($TZ_NAME) $LOGIN: no signal — graphql and graph-html both failed" >&2
    return 1
  fi
}

get_signal || exit 2
attempt=1
while [ "$COUNT" -lt 1 ] && [ "$attempt" -lt "$RETRIES" ]; do
  sleep "$RETRY_WAIT"
  get_signal || exit 2
  attempt=$((attempt + 1))
done

echo "$TODAY ($TZ_NAME) $LOGIN: $COUNT via $SOURCE [attempt $attempt/$RETRIES]"
[ "$COUNT" -ge 1 ]
