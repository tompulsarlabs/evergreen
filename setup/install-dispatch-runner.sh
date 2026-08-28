#!/usr/bin/env bash
# Install/uninstall the Ivy dispatch runner launchd job (Mac).
# The plist fires every 30 min; the runner itself enforces the 09:15-21:00
# window from config.yml, so off-hours fires exit immediately and silently.
set -euo pipefail
LABEL="ai.tomgreen.ivy-dispatch"
PLIST_SRC="$(cd "$(dirname "$0")" && pwd)/${LABEL}.plist"
PLIST_DST="$HOME/Library/LaunchAgents/${LABEL}.plist"
UID_N=$(id -u)

case "${1:-}" in
  install)
    mkdir -p "$HOME/Library/LaunchAgents"
    cp "$PLIST_SRC" "$PLIST_DST"
    launchctl bootout "gui/$UID_N" "$PLIST_DST" 2>/dev/null || true
    launchctl bootstrap "gui/$UID_N" "$PLIST_DST"
    echo "installed: $LABEL (every 30 min; runner enforces 09:15-21:00 window)"
    echo "log: /tmp/ivy-dispatch.log   workdir: ~/.ivy-dispatch/"
    ;;
  uninstall)
    launchctl bootout "gui/$UID_N" "$PLIST_DST" 2>/dev/null || true
    rm -f "$PLIST_DST"
    echo "uninstalled: $LABEL"
    ;;
  status)
    launchctl print "gui/$UID_N/$LABEL" 2>/dev/null | head -20 || echo "not loaded"
    tail -5 /tmp/ivy-dispatch.log 2>/dev/null || true
    ;;
  *)
    echo "usage: $0 install|uninstall|status"; exit 1;;
esac
