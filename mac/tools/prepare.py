#!/usr/bin/env python3
"""Restore known relative skill-link placeholders after copying this edition to macOS."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    if sys.platform != 'darwin':
        raise SystemExit('Run this command on macOS; use the windows edition on Windows.')
    manifest = json.loads((ROOT / 'penpot-kit/skills.json').read_text(encoding='utf-8'))
    planned = []
    for entry in manifest['skills']:
        name = entry['id']
        if not isinstance(name, str) or not re.fullmatch(r'penpot-[a-z0-9-]+', name):
            raise ValueError('Invalid skill ID.')
        link = ROOT / '.agents/skills' / name
        target = '../../penpot-kit/skills/' + name
        expected = ROOT / 'penpot-kit/skills' / name
        if not (expected / 'SKILL.md').is_file():
            raise ValueError(name + ': missing source SKILL.md.')
        if link.is_symlink():
            if link.readlink().is_absolute() or link.resolve() != expected:
                raise ValueError(name + ': unexpected symlink; inspect manually.')
            continue
        if not link.is_file() or link.read_text(encoding='utf-8').strip() != target:
            raise ValueError(name + ': unexpected entry; refusing to overwrite.')
        planned.append((link, target))
    for link, target in planned:
        pending = link.with_name(link.name + '.prepare-link')
        pending.symlink_to(target, target_is_directory=True)
        try:
            pending.replace(link)
        finally:
            if pending.is_symlink():
                pending.unlink()
    print(f'Restored {len(planned)} relative skill links.')


if __name__ == '__main__':
    main()
