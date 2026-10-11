# VALIDATION_REPORT — TestKo PH (package 0.5.0)

Date: 2026-10-11 · Scope: all documents · Repair passes used: 1 of 3.
This report validates **documentation consistency only**. No code exists and no software was tested.

## Gauntlet results
| Check | Result | Evidence / affected IDs | Corrective action |
|---|---|---|---|
| C1 MVP FRs have acceptance criteria and mapped flows/screens/tasks/tests | **PASS** | TRACEABILITY §1: FR-001…FR-033 each map to ≥1 FLOW/UI/API/DB/TASK/TEST | — |
| C2 Flows reference defined UI/API/roles/DB | **PASS** (after repair) | API-025 added for FR-028/FR-030; applicant digest & email preferences specified | — |
| C3 Every API has auth, validation, success/error, consumer, data | **WARN** | TRD §5.2 complete for API-001…API-025. PayPal endpoints/event names in TRD §7.2 are from general knowledge and **not verified** against current PayPal docs (TQ-2). API-001 is Supabase Auth's contract. | TASK-021 step 1 verifies PayPal before coding; stop and update docs on mismatch |
| C4 Every displayed datum has a source + permission model | **PASS** (after repair) | Added `developer_display_name` to `v_campaign_listings`; cross-user display names read via service role after ownership check (TRD §5.1) | — |
| C5 No contradictions in names/roles/states/rules | **PASS** (after repair) | Fixed: opt-in URL lock (PRD FR-005 vs missing API), short description limits (PRD vs DB CHECK), payment amount-mismatch flag rollback in `svc_mark_payment_paid` | — |
| C6 High-risk actions have mitigations + negative tests | **PASS** | Payouts (TEST-020/021/024), rewards (TEST-022), refunds (TEST-025/026), roles (TEST-003/028), webhooks (TEST-009/024), RLS (TEST-005), uploads (TEST-016/017), deletion (TEST-029) | — |
| C7 Task dependency graph valid | **PASS** | IMPLEMENTATION_PLAN §3: 28 tasks, acyclic, all prerequisites exist | — |
| C8 Gates are objectively measurable | **PASS** | CI gates TRD §14; DONE WHEN per task; NFR targets numeric. Note: targets are assumptions (A-021) | Owner to confirm targets |
| C9 Major decisions confirmed or marked assumed/pending | **WARN** | 10 confirmed (C-001…C-010); 27 assumptions pending (A-001…A-027); 8 open decisions, of which **OD-001…OD-004 block production release** | Owner reviews ASSUMPTIONS.md and DECISIONS.md |
| C10 Changes have version + traceability updates | **PASS** | Rename to TestKo PH applied to all docs (CHANGELOG 0.3.0); PRD/TRD/APP_FLOW/DESIGN_BRIEF/DATABASE_SCHEMA 0.2.0, IMPLEMENTATION_PLAN 0.3.0; manifest hashes updated | — |

| C11 Every third-party service has setup + responsibility coverage | **PASS** | SETUP.md/setup.json cover toolchain, Supabase, Stripe, PayPal, Resend, Vercel, GitHub, Sentry, domain; SHARED_RESPONSIBILITY.md lists each; no step asks for secrets in chat. Note: Vercel's free plan is non-commercial, so the TRD's Pro assumption (A-016) means a paid host unless the TRD changes | Decide on hosting (keep Vercel Pro or switch to a free commercial-friendly host via `/ec2build update --doc TRD`) |

## Automated checks run
| Check | Command | Result |
|---|---|---|
| Setup doctor (local) | `python3 skills/ec2build/scripts/doctor.py projects/testko-ph --stage local` | Runs; on this Mac reports pnpm, docker, stripe CLIs and all local env vars missing (expected before PROMPT 00) |
| Structural (6 docs > 500 chars, manifest, traceability) | `python3 scripts/validate.py projects/testko-ph` | PASS (all six docs OK, manifest.json OK, docs/TRACEABILITY.md OK) |
| ID range & coverage (every FR/NFR/FLOW/UI/API/DB/TASK/TEST/JOB/ADR/OD defined range used, none out of range) | ad-hoc Python regex scan | PASS — no out-of-range IDs, no unused IDs |
| Swimlane diagrams | `python3 skills/ec2build/scripts/swimlanes.py projects/testko-ph` + `rsvg-convert` render of all 16 SVGs | PASS — generator checks lanes, unique cells, valid edges; all 16 rendered and visually reviewed |
| Mermaid syntax rendering | — | **NOT RUN** (no Mermaid CLI available locally) |
| SQL DDL execution | — | **NOT RUN** (no database in this workspace); executed for the first time in TASK-004/005/006 |

## Readiness
**Ready for implementation in development/staging (TASK-001 → TASK-027) once the owner approves the package**, with the WARNs above disclosed.
**Not ready for production release (TASK-028)** until OD-001, OD-002, OD-003, OD-004 are closed.

## Highest-impact items for the owner
1. **OD-001 Stripe eligibility** — confirm your Stripe account's country/entity; if Stripe can't be used, run `/ec2build update --name "TestKo PH" --doc TRD --change "Replace Stripe with <provider>"`.
2. **A-003 / OD-005 pricing** — US$5.00 per tester slot, US$3.50 reward, US$1.50 platform fee *before* Stripe/PayPal fees.
3. **A-007 strictness** — a missed check-in (48 h grace) drops the tester; confirm this is acceptable.
4. **OD-003 policy/legal** — paid closed testing must avoid incentivised ratings/reviews; get counsel before launch.
