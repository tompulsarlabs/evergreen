# Check procedure

Loaded only for this routine. Shared constraints remain in `playbook.md`.

- **Check (18:00)** — run `scripts/check.sh`. Green → record outcome in state
  (bot-authored commit), stay silent. Grey → nudge with the single most concrete
  candidate. **Before picking that candidate, read its
  `memory/repos/<name>.md`** — nudge history and conversion record live there.
  A candidate carrying recorded unconverted nudges is a weaker pick than a
  fresh one of similar cost; say so in the journal when you pick it anyway.
  Note open/claimed contract states (`dispatch/queue/`) when recording the
  check — a claimed contract may land before failsafe.
  Nudge channel: **PushNotification** (verified working from cloud runs
  2026-08-23, "Mobile push requested"). Fallback if PushNotification reports
  not-sent/unavailable: a Google Calendar event ~15 min out titled with the
  candidate. Never both; never anything on a green day.
