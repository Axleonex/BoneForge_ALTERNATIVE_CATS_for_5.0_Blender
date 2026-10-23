"""Build a version-named local release, preserving existing archives.

[PowerShell] python scripts/build_release.py <package-folder> <release-directory>
"""
import ast
import sys
from pathlib import Path

from build_mmd_fix import build


def main(package, destination):
    package = Path(package).resolve()
    tree = ast.parse((package / '__init__.py').read_text(encoding='utf-8'))
    info = next(ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == 'bl_info' for target in node.targets))
    prefix = {'BoneForge': 'BoneForge', 'BoneCraft': 'BoneCraft-BFA'}[info['name']]
    version = '.'.join(map(str, info['version']))
    build(package, Path(destination) / f'{prefix}-{version}.zip', candidate='local-bugfix-release')


if __name__ == '__main__':
    main(*sys.argv[1:])
