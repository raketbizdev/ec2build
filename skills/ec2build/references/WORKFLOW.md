# EC2Build execution protocol

## Entrypoints
- Create: `/ec2build --app web --name "Project Name" --brief "..."` (Claude Code skill invocation)
- Codex: `$ec2build --app web --name "Project Name" --brief "..."` or `Use the ec2build skill to create ...`.
- Update: `/ec2build update --name "Project Name" --doc PRD --change "..."`
- Sync: `/ec2build sync --name "Project Name"`
- Check: `/ec2build validate --name "Project Name"`
- Plan: `/ec2build plan --name "Project Name"`
- Build: `/ec2build build --name "Project Name" --phase 1` (explicit invocation, never automatic).

## Execution steps
1. Parse user request; detect command `create`, `update`, `sync`, `validate`, `plan`, `build` (default `create`). Ask a concise question only if essential information is absent, not for optional stack choices that can be marked proposed.
2. Determine slug from name; avoid collisions. Existing projects must be loaded, never silently overwritten. For an existing repo, inspect its code, schema, CI and deployment conventions before authoring requirements.
3. Discover target users, problem, goals, main scenarios, platforms and non-negotiable constraints. Distinguish confirmed, inferred and unresolved information. Ask only high-impact questions; batch linked questions where appropriate.
4. Produce each full file in `<OUTPUT_ROOT>/<slug>/docs/` (see SKILL.md "Where output goes") according to `references/TEMPLATES.md`, with section IDs and cross-references. No empty placeholder outputs masquerading as complete documents.
5. Swimlanes must be **horizontal**: one row per user role or system, flow left to right with arrows, with branches for happy path, validation failure, auth denial, timeout, cancellation, retry, offline where relevant; include all critical flows in APP_FLOW.md. Explicitly number each flow and map to FR IDs. Produce them with the agent tool: write `<OUTPUT_ROOT>/<slug>/docs/diagrams/flows.json`, then run `python3 <SKILL_DIR>/scripts/swimlanes.py <OUTPUT_ROOT>/<slug>` (SVG images + generated Mermaid `flowchart LR` text version). See EC2BUILD_AGENT.md Phase 3.
6. IMPLEMENTATION_PLAN.md must be a prompt sequence — one self-contained copy/paste prompt per task, run one after another until complete, then a completion-audit prompt. It must contain directly executable, sequential **prompts for a coding agent**, from bootstrap to production readiness. Each phase defines inputs and required docs, code paths/files, detailed actions, commands where stack known, dependencies, security guards, verifications, acceptance gates, rollback where relevant, and a STOP condition. Do not invent execution results.
7. Output only the six documents (plus App Flow images). Keep versions in each document control table, the change history in the PRD, and the traceability matrix in IMPLEMENTATION_PLAN Appendix A. Use Git commits for history when user authorizes commits; otherwise preserve Git working-tree diffs.
8. Run `python3 <SKILL_DIR>/scripts/validate.py <OUTPUT_ROOT>/<slug>` (structure + swimlane outputs). Gauntlet: validate requirements coverage, architecture feasibility, data design, security, access, UI and workflow consistency, task sequencing, measurable acceptance tests, and TODO/unknown blockers. Iterate on validation failures, disclose unresolved blockers.
9. For `update`, edit chosen source document, analyze all downstream links, update **affected sections** in other documents plus the traceability appendix and a PRD change-history row. Never erase unrelated approved decisions. If change conflicts with approved requirements, show trade-off and request decision.
10. `sync` reconciles drift from code and docs, proposes changes and makes safe edits. `validate` checks without editing except if user explicitly requested auto-fix.
10b. `setup` runs the accounts setup assistant for a stage (default `local`): run AUTO steps after the owner logs in through the provider CLI, give exact URLs/clicks for ASSISTED steps and verify them, list OWNER-ONLY steps (terms, payments, identity, policy declarations), then run `python3 <SKILL_DIR>/scripts/doctor.py <project> --stage <stage> --app <app-dir>`. Never request secrets in chat; never accept terms or pay on the owner's behalf.
11. `build` runs PROMPT 00 (setup) first if the doctor is not green, then reads current approved docs and actual repository state, chooses next safe incomplete phase, implements tasks one by one with tests, logs progress and stops at approval gates. Writing a plan alone is not building.
12. Return: project directory, changed docs, assumptions, unresolved questions, validation result, next suggested command.

## Required document names
`PRD.md`, `TRD.md`, `APP_FLOW.md`, `DESIGN_BRIEF.md`, `DATABASE_SCHEMA.md`, `IMPLEMENTATION_PLAN.md`. Nothing else. Context, assumptions, open decisions and change history live in the PRD; accounts setup, shared responsibility and traceability live in the IMPLEMENTATION_PLAN.

TRD -> IMPLEMENTATION_PLAN §2A/§2B (every third-party service in the TRD must appear in the setup and responsibility sections).

## Dependencies
PRD -> TRD, APP_FLOW, DESIGN_BRIEF, DATABASE_SCHEMA, IMPLEMENTATION_PLAN.
TRD -> DATABASE_SCHEMA, APP_FLOW, IMPLEMENTATION_PLAN.
APP_FLOW -> DESIGN_BRIEF, DATABASE_SCHEMA, IMPLEMENTATION_PLAN.
DESIGN_BRIEF -> IMPLEMENTATION_PLAN.
DATABASE_SCHEMA -> IMPLEMENTATION_PLAN.
Changes can propagate backward if they expose infeasibility; report conflicts rather than silently rewriting the requirement.
