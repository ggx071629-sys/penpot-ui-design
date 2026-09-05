#!/usr/bin/env python3
"""Read-only checks for this workspace; no configuration reads or network calls."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / 'penpot-kit'


def verify():
    checks, errors = {}, {}
    node = shutil.which('node')

    def check(name, action):
        try:
            action()
            checks[name] = True
        except (OSError, ValueError, KeyError, TypeError, RuntimeError,
                subprocess.SubprocessError) as exc:
            checks[name] = False
            # Keep diagnostics portable; do not emit absolute local paths.
            message = str(exc).replace(str(ROOT), '.')
            errors[name] = message

    def require(condition, message):
        if not condition:
            raise ValueError(message)

    def node_runtime():
        require(node is not None, 'Node.js 22+ is required; install it and reopen the terminal/client.')
        result = subprocess.run([node, '--version'], capture_output=True, text=True, timeout=10)
        match = re.fullmatch(r'v(\d+)\.\d+\.\d+[^\s]*', result.stdout.strip())
        require(result.returncode == 0 and match and int(match[1]) >= 22,
                'Node.js 22+ is required; check node --version.')

    def workspace_files():
        required = ['AGENTS.md', 'README.md', 'docs/start-task.md',
                    'docs/maintenance.md', 'business-projects/README.md']
        missing = [name for name in required if not (ROOT / name).is_file()]
        require(not missing, 'Missing workspace files: ' + ', '.join(missing))

    def skill_links():
        manifest = json.loads((KIT / 'skills.json').read_text())
        names = {entry['id'] for entry in manifest['skills']}
        require(bool(names), 'skills.json contains no skills.')
        links = ROOT / '.agents/skills'
        require(links.is_dir(), 'Missing .agents/skills; include hidden directories when copying.')
        for name in sorted(names):
            require(isinstance(name, str) and re.fullmatch(r'penpot-[a-z0-9-]+', name),
                    'Invalid skill ID in skills.json.')
            link = links / name
            target = KIT / 'skills' / name
            require(link.is_symlink(), '.agents/skills/' + name + ': expected a symbolic link.')
            require(not link.readlink().is_absolute() and link.resolve() == target
                    and (target / 'SKILL.md').is_file(),
                    '.agents/skills/' + name + ': broken or non-portable link; restore the relative link.')
        actual = {p.name for p in links.iterdir() if p.name.startswith('penpot-')}
        require(actual == names, 'Skill entry names differ from skills.json.')

    def template():
        for name in ['briefs', 'design-specs', 'reviews', 'deliverables', 'handoffs']:
            require((ROOT / 'business-projects/_template' / name).is_dir(),
                    'Missing business-projects/_template/' + name)

    def guards():
        for name in ['install', 'install-seed', 'install-behavior', 'update',
                     'uninstall', 'write-mcp-config']:
            lines = (KIT / 'scripts/install' / (name + '.mjs')).read_text().splitlines()
            require(len(lines) > 1 and lines[1].startswith('import "./workspace-guard.mjs";'),
                    'Lifecycle guard missing: ' + name + '; restore it before maintenance.')
        require('process.exit(2)' in (KIT / 'scripts/install/workspace-guard.mjs').read_text(),
                'workspace-guard.mjs must retain its exit protection.')

    def run_kit(script, args):
        require(checks.get('node_runtime'), 'Not run: fix node_runtime first.')
        result = subprocess.run([node, str(KIT / 'scripts/dev' / script), *args],
                                cwd=ROOT, capture_output=True, text=True, timeout=60)
        require(result.returncode == 0,
                (result.stdout + result.stderr).strip() or script + ' failed.')

    check('python_runtime', lambda: require(sys.version_info >= (3, 9), 'Python 3.9+ is required.'))
    check('node_runtime', node_runtime)
    check('workspace_files', workspace_files)
    check('project_skill_links', skill_links)
    check('business_template', template)
    check('lifecycle_guards', guards)
    check('kit_content', lambda: run_kit('validate-kit.mjs', []))
    check('content_lock', lambda: run_kit('update-lock.mjs', ['--check']))
    print(json.dumps({'checks': checks, 'errors': errors, 'passed': sum(checks.values()),
                      'total': len(checks)}, ensure_ascii=False, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['verify'], nargs='?', default='verify')
    parser.parse_args()
    raise SystemExit(verify())
