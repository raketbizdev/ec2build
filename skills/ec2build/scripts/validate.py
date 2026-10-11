#!/usr/bin/env python3
"""Local structural checks; semantic cross-document validation remains agent responsibility."""
from pathlib import Path
import sys
for _s in (sys.stdout, sys.stderr):
  try: _s.reconfigure(encoding='utf-8', errors='replace')
  except Exception: pass
base=Path(sys.argv[1]) if len(sys.argv)>1 else Path('projects')
required=['PRD.md','TRD.md','APP_FLOW.md','DESIGN_BRIEF.md','DATABASE_SCHEMA.md','IMPLEMENTATION_PLAN.md']
projects=[base] if (base/'docs').exists() else [p for p in base.iterdir() if p.is_dir()] if base.exists() else []
if not projects:
 print('No generated project found');sys.exit(1)
failed=False
for project in projects:
 print('Checking',project)
 for name in required:
  p=project/'docs'/name
  ok=p.exists() and len(p.read_text(encoding='utf-8').strip())>500
  print(('OK' if ok else 'MISSING/TOO SHORT'),name)
  failed |= not ok
 for name in ['manifest.json','docs/TRACEABILITY.md']:
  ok=(project/name).exists()
  print(('OK' if ok else 'MISSING'),name);failed |= not ok
 for name in ['SETUP.md','setup.json','SHARED_RESPONSIBILITY.md']:
  ok=(project/'docs'/name).exists()
  print(('OK' if ok else 'MISSING'),'docs/'+name);failed |= not ok
 flows=project/'docs'/'diagrams'/'flows.json'
 if not flows.exists():
  print('MISSING docs/diagrams/flows.json (run <SKILL_DIR>/scripts/swimlanes.py <project-dir>)');failed=True
 else:
  import json
  app=(project/'docs'/'APP_FLOW.md').read_text(encoding='utf-8') if (project/'docs'/'APP_FLOW.md').exists() else ''
  for f in json.loads(flows.read_text(encoding='utf-8'))['flows']:
   svg=project/'docs'/'diagrams'/(f['id']+('-'+f['part'] if f.get('part') else '')+'.svg')
   ok=svg.exists() and f'<!-- swimlane:{f["id"]} -->' in app
   if not ok: print('MISSING swimlane',svg.name);failed=True
  print('OK swimlanes' if not failed else 'CHECK swimlanes')
sys.exit(1 if failed else 0)
