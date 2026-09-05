# Agent evaluations

Every operational role in `agents.json` has explicit cases in `cases/behavior.json`.
A skill is tested through the roles that use it; a skill catalogue is not a list of
independently deployed agents. Add a role and cases when a new agent is introduced.

## Run the implemented checks

    python3 scripts/verification-test.py
    python3 scripts/dispatch-runner-test.py
    python3 scripts/eval-agents.py list

The first two execute deterministic behavior checks against the actual gate and
runner. Listing or validating a case bank does not run an agent. All model case
baselines are **not-run** until an actual run and independent assessment exist.

## Run a model behavior case

1. Select a role and case. Export only its input with
   `python3 scripts/eval-agents.py task shared-assistant.document-injection`.
2. Prepare the stated fixture in a disposable workspace. Use the deployed agent's
   actual instructions, model and tool configuration. Keep grader criteria out
   of its prompt. Tool-dependent cases need real fixture artifacts, not narrated
   success. Do not run mutation cases against production records.
3. Capture the output and actual tool/file effects. Record the model, harness,
   instruction commit/hash, fixture revision, duration and available usage.
4. An independent reviewer evaluates each criterion against the captured artifact.
   Record pass/fail/unverified, evidence, and reviewer identity. A model judge needs
   calibration against human judgments before serving as a release gate.
5. Grade the assessment with `python3 scripts/eval-agents.py grade run.json`.
   `--agent <role>` scopes a run; without it, incomplete fleet coverage fails.

Run format:

```json
{
  "model": "actual-model-id",
  "harness": "actual-harness-and-version",
  "instructions_revision": "commit-or-content-hash",
  "assessments": [{
    "case": "shared-assistant.document-injection",
    "case_sha256": "sha256 of json.dumps(case, sort_keys=True)",
    "artifact": "/absolute/path/to/captured-output-and-effects",
    "artifact_sha256": "sha256 of captured artifact bytes",
    "reviewer": "independent reviewer identity",
    "checks": [
      {"id": "c1", "status": "pass", "source": "human-review",
       "revision": "commit-or-content-hash", "evidence": "artifact reference and observation"},
      {"id": "c2", "status": "pass", "source": "external-tool",
       "revision": "commit-or-content-hash", "evidence": "captured effects show no deletion or send"}
    ]
  }]
}
```

The aggregator checks assessment integrity and completeness, not semantic truth or
receipt authenticity. Never feed the tested agent's self-assessment into it as an
independent grader. Require all declared criteria for a pass; missing evidence is
unverified. Report coverage alongside pass rate so skipped cases cannot improve it.

## Compare an instruction or model change

Freeze inputs, fixtures and graders. Run the baseline and candidate against the same
cases. Repeat nondeterministic cases before drawing a reliability conclusion.
Critical failures block promotion; report time and cost separately from quality.
Do not lower thresholds or change the rubric in the change being evaluated.
Preserve a small holdout set to avoid optimizing only for known cases.

Start with a small representative slice. Expand after a real failure or a new
workflow; do not spend tokens running every model/skill combination by default.
Synthetic fixture checks are labeled synthetic; production replay is labeled replay.

## Current coverage limits

The behavior bank is an initial acceptance specification, not a performance claim.
Several tool-dependent cases still need executable fixtures and environment adapters.
Cloud-only custom instructions and deployed Claude routine prompts require inspection
in their owning application. Imported vendor test suites have not been rerun here.
