---
id: 2026-09-02-tomgreenai-copy-02
type: build
state: failed
repo: tompulsarlabs/tomgreen.ai
lane: frontier
pool: anthropic
created: 2026-09-02T18:30:00+02:00
created_by: tom
expires: 2026-09-04T18:30:00+02:00
budget: { wall_minutes: 40 }
---

## Task

Re-queue of `2026-08-28-tomgreenai-copy-01`, which the runner refused on
2026-09-01 at the attribution gate because of a runner bug (equality against
one address; fixed 2026-09-02), not on merit.

**Establish current state first.** `main` has moved since 08-28 (PRs #6,
#10, #12 merged; a full Home recomposition on 09-01→02). Read every header,
eyebrow label, and section lead on the current `main` before rewriting. A
header that already passes the rules below stays. If the whole site already
passes, open no PR: say so in the summary between the report markers and
stop.

Rewrite the site's copy in simple, sharp, human language. The 08-28 headers
were AI slop: "The problem worth solving.", "Decisions, not theatre.",
"01 · THE MANDATE" — portentous fragments built from the same molds,
carrying atmosphere instead of information.

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

A branch dispatch/2026-09-02-tomgreenai-copy-02 pushed to
tompulsarlabs/tomgreen.ai with a DRAFT pull request. The PR description
lists each header before → after. Branch from the default branch;
independent of the other open tomgreen.ai contracts. No push to the default
branch. Or, if nothing needed changing, no PR and a summary that says so.

## Verification (cloud-checkable)

A draft PR opened by tompulsarlabs exists on tompulsarlabs/tomgreen.ai
referencing this contract id, created on or after 2026-09-02 — or the
contract's report states that the current site already passes every rule,
naming the headers checked.

## Notes

First `build` contract to reach a worker on the Mac runner; the three
2026-08-28/31 builds never executed. Whatever this run shows about
`claude -p` opening draft PRs from the Mac is routing evidence in itself.

outcome:
  claimed_at: 2026-09-02T19:06:50+02:00
  exit: attribution
  note: next commit would author 'tompulsarlabs <tom@pulsarlabsai.com>' — not the connected address
