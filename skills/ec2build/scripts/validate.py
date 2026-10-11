#!/usr/bin/env python3
"""EC2Build structural check: the six documents, swimlane images, setup block and the one-page HTML.
Usage: python3 <SKILL_DIR>/scripts/validate.py <project-dir>   (or a folder of projects)
Semantic cross-document validation (Gauntlet) remains the agent's responsibility."""
from pathlib import Path
import json, re, sys
for _s in (sys.stdout, sys.stderr):
  try: _s.reconfigure(encoding='utf-8', errors='replace')
  except Exception: pass

DOCS = ['PRD.md', 'TRD.md', 'APP_FLOW.md', 'DESIGN_BRIEF.md', 'DATABASE_SCHEMA.md', 'IMPLEMENTATION_PLAN.md']
base = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('projects')
projects = [base] if (base / 'docs').exists() else [p for p in base.iterdir() if (p / 'docs').is_dir()] if base.exists() else []
if not projects:
  print('No generated project found'); sys.exit(1)
failed = False
for project in projects:
  print('Checking', project)
  docs = project / 'docs'
  for name in DOCS:
    p = docs / name
    ok = p.exists() and len(p.read_text(encoding='utf-8').strip()) > 500
    print('OK' if ok else 'MISSING/TOO SHORT', name); failed |= not ok
  extra = sorted(p.name for p in docs.glob('*') if p.is_file() and p.name not in DOCS and p.name != f'{project.resolve().name}.html')
  if extra:
    print('NOTE extra files (EC2Build outputs only the six documents):', ', '.join(extra))
  flows = docs / 'diagrams' / 'flows.json'
  app = (docs / 'APP_FLOW.md').read_text(encoding='utf-8') if (docs / 'APP_FLOW.md').exists() else ''
  if not flows.exists():
    print('MISSING docs/diagrams/flows.json (App Flow swimlane data)'); failed = True
  else:
    bad = [f['id'] for f in json.loads(flows.read_text(encoding='utf-8'))['flows']
           if not (docs / 'diagrams' / (f['id'] + ('-' + f['part'] if f.get('part') else '') + '.svg')).exists()
           or f'<!-- swimlane:{f["id"]} -->' not in app]
    print('OK swimlanes' if not bad else 'MISSING swimlanes: ' + ', '.join(sorted(set(bad)))); failed |= bool(bad)
  page = docs / f'{project.resolve().name}.html'
  newest = max((docs / n).stat().st_mtime for n in DOCS if (docs / n).exists()) if any((docs / n).exists() for n in DOCS) else 0
  if not page.exists():
    print(f'MISSING one-page HTML docs/{page.name} (run onepage.py)'); failed = True
  elif page.stat().st_mtime < newest:
    print(f'STALE one-page HTML docs/{page.name}: a document changed after it was generated (re-run onepage.py)'); failed = True
  else:
    print(f'OK one-page HTML docs/{page.name}')
  plan = (docs / 'IMPLEMENTATION_PLAN.md').read_text(encoding='utf-8') if (docs / 'IMPLEMENTATION_PLAN.md').exists() else ''
  ok = bool(re.search(r'```json\n\{\s*"format":\s*"ec2build-setup/1"', plan)) and '<!-- setup:begin -->' in plan
  print('OK setup block (IMPLEMENTATION_PLAN §2A)' if ok else 'MISSING setup block in IMPLEMENTATION_PLAN §2A'); failed |= not ok
sys.exit(1 if failed else 0)
