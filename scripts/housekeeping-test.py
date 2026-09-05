#!/usr/bin/env python3
"""Integration checks for the dispatch receipt gate in an isolated repository fixture."""
import shutil,subprocess,tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
 r=Path(tmp);(r/'scripts').mkdir()
 for d in ['queue','done','failed']:(r/'dispatch'/d).mkdir(parents=True)
 for name in ['dispatch-lint.sh','verification.py']:shutil.copy2(root/'scripts'/name,r/'scripts'/name)
 shutil.copy2(root/'config.yml',r/'config.yml')
 old=next((root/'dispatch/done').glob('*.md')).read_text()
 import re
 old=re.sub(r'^id: .*$', 'id: fixture',old,flags=re.M)
 p=r/'dispatch/done/fixture.md';p.write_text(old)
 def lint():return subprocess.run(['bash',str(r/'scripts/dispatch-lint.sh')],text=True,capture_output=True)
 assert lint().returncode==0,'unverified historical outcome should remain representable'
 p.write_text(old.replace('  verified: false','  verified: true'))
 assert lint().returncode!=0,'false pass must fail dispatch lint'
 p.write_text(re.sub(r'^created: .*$', 'created: 2026-09-05T09:00:00+02:00',old,flags=re.M))
 # Expiry must remain after fixture creation.
 p.write_text(re.sub(r'^expires: .*$', 'expires: 2026-09-07T09:00:00+02:00',p.read_text(),flags=re.M))
 assert lint().returncode!=0,'new assignment must declare checks'
 p.write_text(p.read_text().replace('id: fixture','id: fixture\nverification_checks: ["artifact"]'))
 assert lint().returncode==0,lint().stdout
print('PASS dispatch lint rejects false passes and new assignments without checks')
