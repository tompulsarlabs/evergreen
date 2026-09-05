#!/usr/bin/env python3
import json
import tempfile
from pathlib import Path
from verification import verdict, task_digest, contract_verdict, eligible_ids

root = Path(__file__).resolve().parents[1]
cases = json.loads((root / 'evals/verification-cases.json').read_text())
for c in cases:
    actual = verdict(c['required'], c['checks'], c['revision'])
    assert actual == c['expect'], (c['id'], actual)
    print('PASS', c['id'])
for malformed in (None, {}, [None], [{'id': []}]):
    assert verdict(['artifact'], malformed, 'a' * 40) == 'unverified'
with tempfile.TemporaryDirectory() as d:
    r = Path(d)
    (r / 'dispatch/done').mkdir(parents=True)
    (r / 'dispatch/verification').mkdir()
    p = r / 'dispatch/done/c1.md'
    p.write_text('---\nverification_checks: ["artifact"]\n---\n## Task\nCheck report\n\noutcome:\n  verified: true\n')
    assert not eligible_ids(r), 'legacy self-report must not unblock work'
    receipt = {'contract': 'c1', 'task_sha256': task_digest(p.read_text()), 'revision': 'a' * 40,
               'checked_at': '2026-09-05T12:00:00Z', 'verifier': 'independent-fixture',
               'checks': [cases[0]['checks'][0]]}
    f = r / 'dispatch/verification/c1.json'
    f.write_text(json.dumps(receipt))
    assert contract_verdict(p, r) == 'pass'
    assert eligible_ids(r) == {'c1'}
    p.write_text(p.read_text().replace('Check report', 'Check report and security'))
    assert contract_verdict(p, r) == 'unverified', 'edited assignment must invalidate receipt'
    f.write_text('not json')
    assert contract_verdict(p, r) == 'unverified'
print('PASS receipt binding, dependency gate, and malformed receipt')
