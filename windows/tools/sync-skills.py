#!/usr/bin/env python3
"""Refresh generated project skills from penpot-kit; overwrites generated copies only."""
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'penpot-kit/skills'
DEST = ROOT / '.agents/skills'


def main():
    manifest = json.loads((ROOT / 'penpot-kit/skills.json').read_text(encoding='utf-8'))
    names = {entry['id'] for entry in manifest['skills']}
    if not names or any(not isinstance(n, str) or not re.fullmatch(r'penpot-[a-z0-9-]+', n) for n in names):
        raise ValueError('Invalid skill manifest.')
    # Refuse links/junctions that could redirect writes outside this workspace.
    for base in (SOURCE, DEST):
        if not base.resolve().is_relative_to(ROOT):
            raise ValueError('Skill path escapes this workspace.')
        for p in [base, *base.rglob('*')]:
            if p.is_symlink() or (p.exists() and p.resolve() != p.absolute()):
                raise ValueError('Skill trees must contain regular files and directories only.')
    if DEST.exists() and {p.name for p in DEST.iterdir()} - names:
        raise ValueError('Unexpected skill entries; review and remove obsolete copies manually.')
    for name in names:
        if not (SOURCE / name / 'SKILL.md').is_file():
            raise ValueError(name + ': missing source SKILL.md.')
    for name in sorted(names):
        source, dest = SOURCE / name, DEST / name
        source_paths = {p.relative_to(source) for p in source.rglob('*')}
        # Remove only obsolete generated files, never recurse through external paths.
        if dest.exists():
            for p in sorted(dest.rglob('*'), key=lambda p: len(p.parts), reverse=True):
                if p.relative_to(dest) not in source_paths:
                    p.rmdir() if p.is_dir() else p.unlink()
        shutil.copytree(source, dest, dirs_exist_ok=True)
    print(f'Synchronized {len(names)} project skill directories.')


if __name__ == '__main__':
    main()
