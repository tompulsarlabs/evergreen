#!/usr/bin/env python3
"""Evidence completeness gate. Validates receipts, not the truth of a grader's judgment."""
import argparse
import hashlib
import json
import re
from pathlib import Path


def task_digest(text):
    # State and outcome timestamps change during execution; freeze the actual assignment.
    task = text.split('## Task', 1)
    if len(task) != 2:
        raise ValueError('missing Task section')
    return hashlib.sha256(task[1].split('\noutcome:', 1)[0].strip().encode()).hexdigest()


def verdict(required, checks, revision):
    """Fail closed: every declared requirement needs independent evidence at this revision."""
    if (not isinstance(required, list) or not required
            or not all(isinstance(x, str) and x for x in required)
            or len(required) != len(set(required))
            or not isinstance(checks, list)
            or not all(isinstance(c, dict) and isinstance(c.get('id'), str) for c in checks)
            or not isinstance(revision, str) or not re.fullmatch(r'[0-9a-f]{40,64}', revision)):
        return 'unverified'
    if len(checks) != len(required) or {c.get('id') for c in checks} != set(required):
        return 'unverified'
    statuses = []
    for check in checks:
        if (check.get('source') not in ('external-tool', 'human-review')
                or not isinstance(check.get('evidence'), str) or not check['evidence'].strip()
                or check.get('revision') != revision):
            statuses.append('unverified')
        else:
            statuses.append(check.get('status'))
    if 'fail' in statuses:
        return 'fail'
    return 'pass' if all(s == 'pass' for s in statuses) else 'unverified'


def contract_verdict(path, root):
    text = path.read_text()
    # Requirements are declared in the contract, not chosen by the grader after seeing output.
    m = re.search(r'^verification_checks: (\[.*\])$', text, re.M)
    receipt_path = root / 'dispatch' / 'verification' / (path.stem + '.json')
    if not m or not receipt_path.is_file():
        return 'unverified'
    try:
        required = json.loads(m.group(1))
        receipt = json.loads(receipt_path.read_text())
        if (not isinstance(required, list) or not all(isinstance(x, str) for x in required)
                or receipt.get('contract') != path.stem
                or receipt.get('task_sha256') != task_digest(text)
                or not receipt.get('checked_at') or not receipt.get('verifier')):
            return 'unverified'
        return verdict(required, receipt['checks'], receipt['revision'])
    except (ValueError, KeyError, TypeError, AttributeError):
        return 'unverified'


def eligible_ids(root):
    return {p.stem for p in (root / 'dispatch' / 'done').glob('*.md')
            if contract_verdict(p, root) == 'pass'}


def audit(root):
    rows = []
    for directory in ('queue', 'done', 'failed'):
        for path in sorted((root / 'dispatch' / directory).glob('*.md')):
            text = path.read_text()
            actual = contract_verdict(path, root)
            declared = bool(re.search(r'^  verified: true\s*$', text, re.M))
            rows.append({'contract': path.stem, 'status': actual,
                         'invalid_pass': declared and actual != 'pass'})
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--digest', type=Path, help='Print the frozen assignment digest for a receipt')
    args = parser.parse_args()
    if args.digest:
        print(task_digest(args.digest.read_text()))
        raise SystemExit(0)
    rows = audit(args.root)
    print(json.dumps({'contracts': rows, 'invalid_passes': sum(r['invalid_pass'] for r in rows)}, indent=2))
    raise SystemExit(1 if any(r['invalid_pass'] for r in rows) else 0)
