# Triage labels

Ivy has no inbound issue queue: nobody files bugs against it, and the scout
already surfaces every open PR across the watchlist each morning. `/triage`
is therefore not a flow here. When a skill nevertheless asks for a triage
role, this is what each one means in Ivy.

| Role in mattpocock/skills | In Ivy | Meaning |
|---------------------------|--------|---------|
| `needs-triage` | a candidate in today's journal, unranked | The scout has not yet ranked it |
| `needs-info` | not used | A contract is published only once its Task, Definition of done, and Verification are complete; grill first (`/grill-with-docs`), then publish |
| `ready-for-agent` | contract `state: open` in `dispatch/queue/` | The runner may claim it |
| `ready-for-human` | journal `## Blockers`, or the check's nudge | Only Tom can move it (a credential, a merge, a decision) |
| `wontfix` | left unqueued, reason noted in the journal | Declined as a candidate; nothing is filed |

Category roles (`bug`, `enhancement`) have no Ivy equivalent; a contract's
`type` (`build`, `review`, `chore`, `experiment`) is the classification that
matters.
