#!/usr/bin/env python3
"""EC2Build setup doctor: is everything ready for a stage? Never prints secret values.

Usage:  python3 <SKILL_DIR>/scripts/doctor.py <project-dir> [--stage local|staging|production] [--app <app-repo-dir>]
        python3 <SKILL_DIR>/scripts/doctor.py <project-dir> --render     # (re)generate docs/SETUP.md from setup.json
Reads <project-dir>/docs/setup.json (format ec2build-setup/1, see references/SETUP_AND_RESPONSIBILITY.md).
Env vars are looked up in the process environment and in <app>/<env_file> (default .env.local).
Exit code 1 when a CLI or env var required for the stage is missing.
"""
import json, os, pathlib, shutil, sys

for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass

STAGES = ["local", "staging", "production"]

def read_env_file(path):
    names = set()
    if path and path.exists():
        for line in path.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                if value.strip().strip('"').strip("'"):
                    names.add(key.replace("export ", "").strip())
    return names

def render(project, spec):
    o = [f"# SETUP — accounts & environment ({project.resolve().name})", "",
         "Generated from `docs/setup.json` by the EC2Build doctor. Do not edit by hand; update setup.json and re-render.", "",
         "**Levels:** AUTO = the agent runs it after you log in · ASSISTED = you follow exact steps, the agent verifies · "
         "OWNER-ONLY = legally yours (terms, payments, identity).", "",
         f"**Secrets:** put values only in `{spec.get('env_file', '.env.local')}` of the app repo (or your host's env settings). "
         "Never paste them into chat. Check progress with `/ec2build doctor --stage <stage>`.", "",
         "| Service | Needed for | Cost note |", "|---|---|---|"]
    for svc in spec["services"]:
        o.append(f"| {svc['name']} | {', '.join(svc.get('stages', []))} | {svc.get('cost', '')} |")
    for stage in STAGES:
        o += ["", f"## Stage: {stage}"]
        for svc in spec["services"]:
            steps = [s for s in svc.get("steps", []) if s.get("stage", "local") == stage]
            env = svc.get("env", {}).get(stage, [])
            if not steps and not env:
                continue
            o += ["", f"### {svc['name']}: {svc.get('purpose', '')}"]
            if svc.get("cli") and stage == svc.get("stages", ["local"])[0]:
                o.append(f"- Tools on PATH: {', '.join('`'+c+'`' for c in svc['cli'])}")
            for i, s in enumerate(steps, 1):
                o.append(f"{i}. **{s['level']}** ({'agent' if s['who'] == 'agent' else 'you'}): {s['text']}")
            if env:
                o.append(f"- Env variables (names only): {', '.join('`'+e+'`' for e in env)}")
            if svc.get("verify", {}).get(stage):
                o.append(f"- Verify: `{svc['verify'][stage]}`")
    (project / "docs" / "SETUP.md").write_text("\n".join(o) + "\n", encoding='utf-8')
    print("wrote", project / "docs" / "SETUP.md")

def main(argv):
    args = argv[1:]
    if not args or args[0].startswith("-"):
        sys.exit(__doc__)
    project = pathlib.Path(args[0])
    stage = args[args.index("--stage") + 1] if "--stage" in args else "local"
    app = pathlib.Path(args[args.index("--app") + 1]) if "--app" in args else None
    if stage not in STAGES:
        sys.exit(f"--stage must be one of {STAGES}")
    spec = json.loads((project / "docs" / "setup.json").read_text(encoding='utf-8'))
    if spec.get("format") != "ec2build-setup/1":
        sys.exit("setup.json: unsupported format")
    if "--render" in args:
        render(project, spec); return 0
    upto = STAGES[: STAGES.index(stage) + 1]
    env_names = set(os.environ) | read_env_file(app / spec.get("env_file", ".env.local") if app else None)

    problems = 0
    print(f"EC2Build doctor: {project.resolve().name}, stage '{stage}'" + (f", app {app}" if app else " (no --app: checking process env only)"))
    for svc in spec["services"]:
        if not set(svc.get("stages", [])) & set(upto):
            continue
        lines = []
        for cli in svc.get("cli", []):
            if shutil.which(cli) is None:
                lines.append(f"  ✗ CLI missing: {cli}"); problems += 1
        for st in upto:
            for var in svc.get("env", {}).get(st, []):
                if var not in env_names:
                    lines.append(f"  ✗ env missing ({st}): {var}"); problems += 1
        todo = [s for s in svc.get("steps", []) if s.get("who") == "owner" and s.get("stage", "local") in upto and not s.get("done")]
        for s in todo:
            lines.append(f"  • owner step ({s.get('level', 'OWNER-ONLY')}): {s['text']}")
        status = "READY" if not any(l.startswith("  ✗") for l in lines) else "NOT READY"
        print(f"\n[{status}] {svc['name']}: {svc.get('purpose', '')}")
        for l in lines:
            print(l)
        if svc.get("verify", {}).get(stage):
            print(f"  verify with: {svc['verify'][stage]}")
    print(f"\n{'All required items present' if not problems else f'{problems} required item(s) missing'} for stage '{stage}'. "
          "Owner steps marked • are reminders; mark them \"done\": true in setup.json once completed.")
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
