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

COUNT=$(query_count)
attempt=1
while [ "$COUNT" -lt 1 ] && [ "$attempt" -lt "$RETRIES" ]; do
  sleep "$RETRY_WAIT"
  COUNT=$(query_count)
  attempt=$((attempt + 1))
done

echo "$TODAY ($TZ_NAME) $LOGIN: $COUNT contribution(s) [attempt $attempt/$RETRIES]"
[ "$COUNT" -ge 1 ]
