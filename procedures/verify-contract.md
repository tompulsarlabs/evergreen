# Verify a dispatch contract

Run after securing the day. This procedure implements the existing external
verification rule; it does not expand the worker's write permissions.

1. Before execution, declare check IDs as a JSON list in the contract frontmatter:
   `verification_checks: ["artifact", "paths"]`. Explain each check and its pass
   criteria in the Verification section. Changes to criteria require review;
   a verifier cannot remove a failing requirement to obtain a pass.
2. Independently inspect the artifact at a pinned revision. GitHub file lists,
   git objects, test execution and human adjudication are evidence. A worker's
   PR body or completion message is a claim. Read every required source.
3. Write `dispatch/verification/<contract-id>.json` using the schema below.
   Include source URLs or command output locations, not just "checked". Preserve
   inaccessible checks with status `unverified`; actual observed violations fail.
4. Run `python3 scripts/verification.py`. Set `verified: true` only when
   `contract_verdict` is `pass`; otherwise set `verified: false` and
   `verification_status: fail|unverified`. Correcting evidence never turns
   missing access into successful verification. Run dispatch lint before commit.

```json
{
  "contract": "contract-id",
  "task_sha256": "output of python3 scripts/verification.py --digest path/to/contract.md",
  "revision": "full artifact commit SHA or SHA256 snapshot digest",
  "checked_at": "ISO timestamp",
  "verifier": "identity of the independent verifier",
  "checks": [
    {"id": "artifact", "status": "pass", "source": "external-tool",
     "revision": "same immutable revision", "evidence": "source URL and observed result"},
    {"id": "paths", "status": "unverified", "source": "external-tool",
     "revision": "same immutable revision", "evidence": "required repository returned 403"}
  ]
}
```

The gate checks completeness, task binding, revision consistency and declared
provenance. It cannot authenticate a fabricated receipt or judge semantic truth.
Receipts need an independent verifier and review; workers must not author them.
A future product needs enforceable access separation before making stronger claims.

A `done/` file records execution completion. Only a passing receipt unlocks its
dependents and contributes to current verified routing metrics. Historical
outcomes without receipts remain visible and unverified until rechecked.
