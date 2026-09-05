#!/usr/bin/env python3
import copy,hashlib,importlib.util,json,tempfile
from pathlib import Path
spec=importlib.util.spec_from_file_location('ev',Path(__file__).with_name('eval-agents.py'))
ev=importlib.util.module_from_spec(spec);spec.loader.exec_module(ev)
cases=ev.load_cases();c=cases[0]
assert not ev.grade(cases,{})['suite_pass']
assert not ev.grade([],{})['suite_pass']
for malformed in (None, {'assessments': None}, {'assessments': [None]}):
 assert not ev.grade(cases, malformed)['suite_pass']
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)/'capture.txt';p.write_text('Synthetic captured action trace for grader tests.\n')
 o={'case':c['id'],'case_sha256':hashlib.sha256(json.dumps(c,sort_keys=True).encode()).hexdigest(),
    'artifact':str(p),'artifact_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'reviewer':'test-reviewer',
    'checks':[{'id':x['id'],'status':'pass','source':'human-review','revision':'a'*40,'evidence':str(p)} for x in c['criteria']]}
 run={'model':'test-fixture','harness':'unit-test','instructions_revision':'a'*40,'assessments':[o]}
 assert ev.grade([c],run)['suite_pass']
 assert not ev.grade(cases,run)['suite_pass'], 'partial fleet coverage cannot pass'
 bad=copy.deepcopy(run);bad['assessments'][0]['checks'].pop();assert not ev.grade([c],bad)['suite_pass']
 bad=copy.deepcopy(run);bad['assessments'].append(o);assert not ev.grade([c],bad)['suite_pass']
 bad=copy.deepcopy(run);bad['assessments'][0]['checks'][0]['source']='worker';assert not ev.grade([c],bad)['suite_pass']
 p.write_text('Changed after review');assert not ev.grade([c],run)['suite_pass']
print(f'PASS aggregator integrity tests; {len(cases)} behavior cases indexed, not executed')
