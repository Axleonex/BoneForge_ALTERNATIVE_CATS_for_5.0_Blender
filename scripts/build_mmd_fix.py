"""Build a non-overwriting local MMD repair candidate and parity receipt.

[PowerShell] python scripts/build_mmd_fix.py <package-folder> <output.zip>
"""
import ast
import hashlib
import json
import sys
import zipfile
from pathlib import Path


def build(package, output, *, candidate='mmd-fix'):
    package, output = Path(package).resolve(), Path(output).resolve()
    tree = ast.parse((package / '__init__.py').read_text(encoding='utf-8'))
    metadata = next(ast.literal_eval(node.value) for node in tree.body
                    if isinstance(node, ast.Assign) and any(
                        isinstance(t, ast.Name) and t.id == 'bl_info' for t in node.targets))
    files = sorted(p for p in package.rglob('*') if p.is_file()
                   and '__pycache__' not in p.parts
                   and not p.name.endswith(('.pyc', '.pyo', '.blend1', '.blend2')))
    if metadata['name'] == 'BoneForge':
        assert not any(p.name in ('bfa_guard.py', 'BFA_EXCLUSIVE.md') for p in files)
        assert '_is_bforartists' not in (package / '__init__.py').read_text(encoding='utf-8')
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'x', zipfile.ZIP_DEFLATED) as archive:
        for file in files:
            archive.write(file, 'boneforge/' + file.relative_to(package).as_posix())
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        expected = {'boneforge/' + file.relative_to(package).as_posix(): file for file in files}
        assert set(archive.namelist()) == set(expected)
        for name, file in expected.items():
            assert archive.read(name) == file.read_bytes(), name
    receipt = {'product': metadata['name'], 'version': metadata['version'],
               'candidate': candidate, 'source': str(package), 'files': len(files),
               'crc': 'PASS', 'source_parity': 'PASS',
               'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}
    output.with_suffix('.receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    print(json.dumps({'output': str(output), **receipt}))


if __name__ == '__main__':
    build(*sys.argv[1:])
