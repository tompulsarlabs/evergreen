#!/usr/bin/env bash
# Deterministic validation for the memory wiki (memory/**/*.md).
#
# Checks that every page carries frontmatter, that every context edge
# ([[page]]) and evidence edge ([cite:...]) resolves to something that really
# exists, that no page is unreachable from the index, and that the index stays
# small enough to read on every run.
#
# Semantic checks — is this synthesis still supported by its evidence? — are
# the retro's job, not this script's. Exit 0 clean, 1 on any violation.
set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

INDEX="memory/INDEX.md"
INDEX_MAX_LINES="${IVY_INDEX_MAX_LINES:-40}"
# Real calendar shape, not just four-two-two: month 01-12, day 01-31.
ISO_DATE='^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
fail=0
count=0

err() { printf 'memory-lint: %s\n' "$1" >&2; fail=1; }

# Links inside code spans or fenced blocks are documentation of the syntax,
# not edges — strip both before extracting anything.
strip_code() {
  awk '/^```/ { fenced = !fenced; next } !fenced' "$1" | sed 's/`[^`]*`//g'
}

[ -d memory ] || { echo "memory-lint: no memory/ directory — nothing to check"; exit 0; }
[ -f "$INDEX" ] || { err "$INDEX is missing"; exit 1; }

index_body=$(strip_code "$INDEX")

while IFS= read -r page; do
  count=$((count + 1))

  # --- frontmatter: subject, type, updated (ISO date) ---
  if [ "$(head -1 "$page")" != "---" ]; then
    err "$page: missing frontmatter (first line must be ---)"
    continue
  fi
  fm=$(sed -n '2,/^---$/p' "$page")
  for key in subject type updated; do
    printf '%s\n' "$fm" | grep -q "^$key:" || err "$page: frontmatter missing '$key:'"
  done
  updated=$(printf '%s\n' "$fm" | sed -n 's/^updated:[[:space:]]*//p' | head -1)
  printf '%s' "$updated" | grep -Eq "$ISO_DATE" \
    || err "$page: 'updated: $updated' is not a YYYY-MM-DD date"

  body=$(strip_code "$page")

  # --- context edges: [[page]] must resolve to memory/page.md ---
  while IFS= read -r link; do
    [ -n "$link" ] || continue
    [ -f "memory/$link.md" ] \
      || err "$page: [[$link]] does not resolve to memory/$link.md"
  done < <(printf '%s\n' "$body" | grep -Eo '\[\[[^]]+\]\]' | sed 's/^\[\[//; s/\]\]$//' | sort -u)

  # --- evidence edges: a date resolves to a journal, a sha to a commit ---
  while IFS= read -r c; do
    [ -n "$c" ] || continue
    if printf '%s' "$c" | grep -Eq "$ISO_DATE"; then
      [ -f "journal/$c.md" ] || err "$page: [cite:$c] has no journal/$c.md"
    elif printf '%s' "$c" | grep -Eq '^[0-9a-f]{7,40}$'; then
      git cat-file -e "$c^{commit}" 2>/dev/null \
        || err "$page: [cite:$c] is not a commit in this repo"
    else
      err "$page: [cite:$c] is neither a YYYY-MM-DD date nor a commit sha"
    fi
  done < <(printf '%s\n' "$body" | grep -Eo '\[cite:[^]]+\]' | sed 's/^\[cite://; s/\]$//' | sort -u)

  # --- no orphans: every page must be reachable from the index ---
  if [ "$page" != "$INDEX" ]; then
    rel=${page#memory/}
    rel=${rel%.md}
    printf '%s\n' "$index_body" | grep -Fq "[[$rel]]" \
      || err "$page: not linked from $INDEX (orphan page)"
  fi
done < <(find memory -name '*.md' | sort)

# --- the index is read every run, so it stays compact ---
lines=$(wc -l < "$INDEX" | tr -d ' ')
[ "$lines" -le "$INDEX_MAX_LINES" ] \
  || err "$INDEX is $lines lines, over the $INDEX_MAX_LINES-line budget"

[ "$fail" -eq 0 ] && echo "memory-lint: ok — $count pages, all links and citations resolve"
exit "$fail"
