# EC2Build agent — CHANGELOG

## 1.3.0 — 2026-10-11
- Install with `npx ec2build install` (npm package `ec2build`, no dependencies, Windows/macOS/Linux). Commands: install, update, uninstall, status, doctor, validate, swimlanes, help.
- Removed the shell/PowerShell/Python installer scripts. Other routes: Claude Code plugin, `npx github:raketbizdev/ec2build`, manual copy.

## 1.2.1 — 2026-10-11
- Cross-platform installer `install.py` (Windows/macOS/Linux, needs only Python 3); README documents plugin install and manual copy for users without `sh`.
- Windows fix: all bundled tools now read/write UTF-8 explicitly and never crash on non-ASCII console output (diagrams contain characters like — × ≥).
- SKILL.md: Python command per OS (`py -3` on Windows).

## 1.2.0 — 2026-10-11
- Free & open source: MIT LICENSE.
- Accounts setup assistant: every project gets `docs/SETUP.md`, `docs/setup.json` and `docs/SHARED_RESPONSIBILITY.md`; steps labelled AUTO / ASSISTED / OWNER-ONLY; new verbs `setup` and `doctor`; new tool `scripts/doctor.py` (checks CLIs, env var names and pending owner steps per stage; never prints secrets).
- Shared responsibility model (owner / EC2Build / coding agent / providers) in `references/SETUP_AND_RESPONSIBILITY.md`.
- Default stack: Supabase database (local Docker first), Expo for native Android/iOS + web; discovery always asks web vs native vs both.
- Implementation plans start with PROMPT 00 (accounts & environment setup); Gauntlet check C11; validator checks the setup files.

## 1.1.0 — 2026-10-11
- Installable anywhere: canonical skill moved to `skills/ec2build/` (SKILL.md + references + scripts), with `install.sh` / `install.ps1` (Claude Code user skills, Codex skills, or per-project) and a Claude Code plugin + marketplace (`.claude-plugin/`).
- Output location works in any folder: `./ec2build/<slug>/`, `./projects/<slug>/` in an EC2Build workspace, or `--out`.
- `help` command and placeholder guard (template text like `<New Name>` is no longer applied).
- Horizontal swimlanes via bundled `scripts/swimlanes.py`; `scripts/validate.py` checks swimlane outputs.
- Implementation plans are written as a prompt sequence with a completion audit.
- Document file names unified to `PRD.md … IMPLEMENTATION_PLAN.md` under `<project>/docs/`.

## 1.0.0
- Initial EC2Build workflow (repo-local skill).
