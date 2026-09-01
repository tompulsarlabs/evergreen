---
id: 2026-08-28-tomgreenai-copy-01
type: build
state: failed
repo: tompulsarlabs/tomgreen.ai
lane: frontier
pool: anthropic
created: 2026-08-28T16:40:00+02:00
created_by: tom
expires: 2026-09-04T16:40:00+02:00
budget: { wall_minutes: 40 }
---

## Task

Rewrite the site's copy in simple, sharp, human language. Tom flagged the
current headers as AI slop and he is right: "The problem worth solving.",
"Decisions, not theatre.", "01 · THE MANDATE" — every header is a
portentous fragment built from the same recognizable molds, carrying
atmosphere instead of information.

Rewrite rules — apply to every header, eyebrow label, and section lead
across the whole site:

1. **The deletion test.** If removing a header loses no information, it is
   decoration, not copy. Every header must state a specific claim the
   section then proves.
2. **Ban the formulas.** No "X, not Y" contrast pairs. No "It's about X" /
   "isn't just X". No definite-article abstractions ("The mandate", "The
   problem worth solving"). No em-dash aphorisms, no rule-of-three
   flourishes, no rhetorical questions.
3. **Concrete beats abstract, always.** The site already holds the
   specifics — £1M bootstrapped in two years, Monzo, Two Sigma, Quadrature,
   Aviva, Santander, the systems built. Put the number, the name, or the
   decision in the header, not a gesture toward it.
4. **Write like a person talking.** First person where natural. Plain
   sentences, one idea each. If it can't be said out loud to a colleague
   without feeling theatrical, rewrite it.
5. **Break the pattern.** Even good fragments become slop when every
   section uses the same shape. Vary header length and structure; let some
   headers be full sentences.
6. **Keep the voice, lose the costume.** Direct and confident is right for
   this site; the fix is substituting substance for drama, not flattening
   the tone.

Body copy: same rules, lighter touch — fix formula sentences and empty
abstractions, do not rewrite paragraphs that already read as human and
specific.

## Definition of done

A branch dispatch/2026-08-28-tomgreenai-copy-01 pushed to
tompulsarlabs/tomgreen.ai with a DRAFT pull request. The PR description
lists each header before → after. Branch from the default branch;
independent of the layout contract's branch. No push to the default branch.

## Verification (cloud-checkable)

A draft PR opened by tompulsarlabs exists on tompulsarlabs/tomgreen.ai
referencing this contract id, created on or after 2026-08-28.

outcome:
  claimed_at: 2026-09-01T17:01:18+02:00
  exit: attribution
  note: next commit would author 'tompulsarlabs <tom@pulsarlabsai.com>' — not the connected address
