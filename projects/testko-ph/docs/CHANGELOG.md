# CHANGELOG — TestKo PH

## 0.5.0 — 2026-10-11 — Accounts setup & shared responsibility
- **Request:** "the agent is free, not the database and third parties; they need accounts which the agent will help automatically; add instruction on use of shared responsibility".
- **Added:** `docs/setup.json` (machine-readable setup for 9 services), `docs/SETUP.md` (generated from it by the EC2Build doctor), `docs/SHARED_RESPONSIBILITY.md` (owner / EC2Build / coding agent / providers).
- **Plan:** new PROMPT 00 / TASK-000 "Accounts & environment setup" before PROMPT 01; PROMPT 27/28 now start with a doctor check for staging/production. TASK-001 depends on TASK-000.
- **Flagged:** Vercel's free plan is non-commercial; TRD A-016 assumes the paid Pro plan. Decide whether to keep it or switch hosting (TRD update).
- **Versions:** IMPLEMENTATION_PLAN 0.3.1 → 0.4.0; overall 0.4.1 → 0.5.0. Other documents unchanged (upstream references updated).

## 0.4.1 — 2026-10-11 — Swimlane generator moved to the EC2Build agent
- **Request:** "this is for the agent not the project; project is the output".
- **Change:** the generator moved from `projects/testko-ph/tools/swimlanes.py` to the EC2Build repository as `scripts/swimlanes.py` (agent tool). This project now holds only outputs: `docs/diagrams/flows.json` (diagram data) and the generated SVGs/marker blocks. The re-generated diagrams are byte-identical.
- **Agent-level:** EC2BUILD_AGENT.md, WORKFLOW.md and templates now require horizontal swimlanes (via `scripts/swimlanes.py`) and the prompt-sequence implementation plan for every project; `scripts/validate.py` checks swimlane outputs.
- **Project docs:** APP_FLOW conventions, VALIDATION_REPORT and PROMPT 01 references updated (no version bump: wording only). Manifest `diagram_source` → `docs/diagrams/flows.json`.

## 0.4.0 — 2026-10-11 — Horizontal swimlanes for APP_FLOW
- **Request:** "the app flow should be a swimlane that is easy to follow with arrow a horizontal swimlane where the row is the users and the system".
- **Change:** all 15 flows (16 diagrams; FLOW-002 has two parts) are now horizontal swimlanes: one row per user role or system, read left to right, numbered steps, labelled arrows, dashed retry arrows, colour-coded start/step/decision/error. Rendered as `docs/diagrams/FLOW-###.svg` from a single source `tools/swimlanes.py`, which also writes a Mermaid text version under each image (keeps WORKFLOW.md's Mermaid swimlane rule).
- **Unchanged:** flow content, step tables, outcomes, all IDs. Only diagram form changed.
- **Also:** PROMPT 01 now copies docs recursively (incl. diagrams) and the generator.
- **Versions:** APP_FLOW 0.2.0 → 0.3.0; IMPLEMENTATION_PLAN 0.3.0 → 0.3.1; DESIGN_BRIEF/DATABASE_SCHEMA upstream references updated (content unchanged); overall 0.3.0 → 0.4.0.

## 0.3.0 — 2026-10-11 — Full rename: itphteste → TestKo PH
- **Request:** `/ec2build update --name "itphteste" --doc PRD --change "Rename app to TestKo PH, full rename"`.
- **Display name:** "itphteste" → "TestKo PH" in every document (titles, product copy, wordmark, disclaimer, email sender name, prompts).
- **Identifiers (slug `testko-ph`):** project folder `projects/itphteste/` → `projects/testko-ph/`; manifest `project_id`; app repo root and `pnpm create next-app` target; Supabase `project_id`; roster CSV filename prefix; `--name` in command samples.
- **Unchanged:** all requirement IDs, scope, flows, schema, tasks and tests. "IT Philippines" community references and OD-007 (brand-usage permission) remain as they were. Earlier changelog entries keep the old name as history.
- **Versions:** PRD, TRD, APP_FLOW, DESIGN_BRIEF, DATABASE_SCHEMA 0.1.0 → 0.2.0; IMPLEMENTATION_PLAN 0.2.0 → 0.3.0; overall revision 0.2.1 → 0.3.0. DECISIONS override log updated; C-002 updated.
- **Validation:** no remaining "itphteste" outside history/rename notes; structural check passes.
- **Follow-up for you:** check that "TestKo PH" is free to use (trademark, domain, app-store names) — tracked under OD-007/OD-008.

## 0.2.1 — 2026-10-11 — Usage samples (README only)
- **Request:** `update … --change "Rename app to <New Name> (display only | full rename)"` + "there should be a sample on how to use it".
- **Not applied:** the rename — the change text was the template placeholder, so no new name was given. App name remains "itphteste".
- **Added:** README "How to use (command samples)" with concrete rename, requirement-change, validate/sync/build and prompt-run examples. No document content or IDs changed.

## 0.2.0 — 2026-10-11 — Implementation plan restructured as a prompt sequence
- **Request:** "Implementation plan is a prompt after prompt until everything is complete."
- **Change:** IMPLEMENTATION_PLAN §6 rewritten so each TASK-001…TASK-028 is one self-contained copy/paste prompt (PROMPT 01…28) that embeds objective, files, contract, instructions, verify commands, required tests, rollback, evidence, commit message, a stop-and-report step and NEXT. §4 now explains manual prompt-by-prompt execution and adds an optional Autopilot prompt that runs the sequence and stops at failures/approval gates. Added a FINAL CHECK completion-audit prompt after PROMPT 28.
- **Scope preserved:** no task content, IDs, dependencies, tests or acceptance criteria changed; metadata tables were folded into the prompts.
- **Affected:** IMPLEMENTATION_PLAN 0.1.0 → 0.2.0; manifest overall_revision 0.1.0 → 0.2.0. Other documents unchanged (no downstream impact; plan has no dependents).
- **Validation:** C7 (DAG) and C10 re-checked — PASS.

## 0.1.0 — 2026-10-11 — Initial package (draft)
- **Request:** `/ec2build --app web --name "itphteste" --brief "…closed app tester marketplace…minimum payout 25USD"`.
- **Discovery round 1:** platforms = Google Play + TestFlight; collection = Stripe; payouts = PayPal Payouts API; verification = check-ins + developer confirmation.
- **Created:** PROJECT_CONTEXT, ASSUMPTIONS, PRD, TRD, APP_FLOW, DESIGN_BRIEF, DATABASE_SCHEMA, IMPLEMENTATION_PLAN, TRACEABILITY, DECISIONS, VALIDATION_REPORT, CHANGELOG, manifest.json, README.
- **IDs introduced:** FR-001…FR-033, NFR-001…NFR-014, FLOW-001…FLOW-015, UI-001…UI-026, API-001…API-025, DB-001…DB-018, JOB-001…JOB-008, TASK-001…TASK-028, TEST-001…TEST-042, ADR-001…ADR-011, OD-001…OD-008, A-001…A-027.
- **Gauntlet repair pass 1 (same session):** added `developer_display_name` to `v_campaign_listings` (C4); defined service-role display-name reads for roster/review (C4); made the opt-in URL locked after draft and moved the change workflow to R2 (C5/C7 — no API existed); specified applicant digest and preferences link for emails (C2); fixed `svc_mark_payment_paid` so the amount-mismatch flag is not rolled back by a raised exception (C3); API-025 added and linked from FR-028/FR-030 (C2).
- **Versions:** all documents 0.0.0 → 0.1.0; overall revision 0.1.0.
- **Remaining issues:** see VALIDATION_REPORT.md (WARNs) and DECISIONS.md OD-001…OD-008.
