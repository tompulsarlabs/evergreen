#!/usr/bin/env python3
"""List agent cases, export task inputs, and grade independent assessments. No model calls."""
import argparse
import hashlib
import json
from pathlib import Path
from verification import verdict
ROOT = Path(__file__).resolve().parents[1]

def load_cases():
    cases = json.loads((ROOT / 'evals/cases/behavior.json').read_text())
    ids = [c['id'] for c in cases]
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate case IDs')
    registry = json.loads((ROOT / 'evals/agents.json').read_text())['agents']
    declared = [cid for agent in registry for cid in agent['cases']]
    if sorted(declared) != sorted(ids):
        raise ValueError('registry does not exactly cover cases')
    return cases

def grade(cases, run):
    rows=[]
    if not isinstance(run, dict):
        run = {}
    observations=run.get('assessments', [])
    malformed = (not isinstance(observations, list) or not all(
        isinstance(o, dict) and isinstance(o.get('case'), str) for o in observations))
    if malformed:
        observations = []
    for c in cases:
        found=[o for o in observations if o.get('case') == c['id']]
        status='unverified'
        if len(found)==1 and run.get('model') and run.get('harness') and run.get('instructions_revision'):
            o=found[0]
            expected_hash=hashlib.sha256(json.dumps(c,sort_keys=True).encode()).hexdigest()
            try:
                artifact = Path(o.get('artifact', ''))
                artifact_ok = (artifact.is_file() and artifact.stat().st_size > 0
                               and hashlib.sha256(artifact.read_bytes()).hexdigest() == o.get('artifact_sha256'))
            except (OSError, TypeError, ValueError):
                artifact_ok = False
            if o.get('case_sha256')==expected_hash and artifact_ok and o.get('reviewer'):
                status=verdict([x['id'] for x in c['criteria']],o.get('checks',[]),run['instructions_revision'])
        rows.append({'case':c['id'],'status':status})
    unknown=sorted({o.get('case','') for o in observations}-{c['id'] for c in cases})
    return {'kind':'independently assessed behavior results','cases':rows,'unknown_cases':unknown,
            'pass':sum(r['status']=='pass' for r in rows),'fail':sum(r['status']=='fail' for r in rows),
            'unverified':sum(r['status']=='unverified' for r in rows),
            'suite_pass':bool(rows) and not malformed and not unknown and all(r['status']=='pass' for r in rows)}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['list','task','grade'])
    p.add_argument('input',nargs='?')
    p.add_argument('--agent')
    p.add_argument('--out',type=Path)
    a=p.parse_args()
    cases=load_cases()
    if a.agent:
        cases=[c for c in cases if c['agent']==a.agent]
        if not cases: p.error('unknown agent')
    if a.action=='list': result=[{'id':c['id'],'agent':c['agent'],'status':'not-run'} for c in cases]
    elif a.action=='task':
        found=[c for c in cases if c['id']==a.input]
        if not found: p.error('unknown case')
        result={'id':found[0]['id'],'input':found[0]['input']}
    else:
        if not a.input: p.error('grade requires an assessment JSON file')
        result=grade(cases,json.loads(Path(a.input).read_text()))
    rendered=json.dumps(result,indent=2)+'\n'
    if a.out: a.out.write_text(rendered)
    print(rendered,end='')
    if a.action=='grade': raise SystemExit(0 if result['suite_pass'] else 1)
