"""Increment an add-on patch version and its export stamp, recording the fix."""
import ast
import json
import re
import sys
from pathlib import Path


def bump(package, reason, ledger):
    package, ledger = Path(package).resolve(), Path(ledger).resolve()
    entry = package / '__init__.py'
    stamp = package / 'vrchat/export/sidecar.py'
    source, sidecar = entry.read_text(encoding='utf-8'), stamp.read_text(encoding='utf-8')
    tree = ast.parse(source)
    info = next(ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == 'bl_info' for target in node.targets))
    old = tuple(info['version'])
    new = (*old[:2], old[2] + 1)
    before, after = '.'.join(map(str, old)), '.'.join(map(str, new))
    source, changed = re.subn(r'("version"\s*:\s*)\(\s*' + r',\s*'.join(map(str, old)) + r'\s*\)',
                             lambda m: m.group(1) + str(new), source, count=1)
    assert changed == 1
    sidecar, changed = re.subn(r'(BONEFORGE_VERSION\s*=\s*")' + re.escape(before) + '"',
                              lambda m: m.group(1) + after + '"', sidecar, count=1)
    assert changed == 1, 'Add-on metadata and export stamp must agree before incrementing'
    entry.write_text(source, encoding='utf-8', newline='\n')
    stamp.write_text(sidecar, encoding='utf-8', newline='\n')
    records = json.loads(ledger.read_text(encoding='utf-8')) if ledger.exists() else []
    record = {'product': info['name'], 'before': before, 'after': after, 'fix': reason}
    records.append(record)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    ledger.write_text(json.dumps(records, indent=2), encoding='utf-8')
    print(json.dumps(record))


if __name__ == '__main__':
    bump(*sys.argv[1:])
