# TRACEABILITY — TestKo PH (package 0.5.0)

Requirement → flow → screen → API → data → task → test. PRD/TRD/DESIGN_BRIEF/DATABASE_SCHEMA at 0.2.0; APP_FLOW at 0.3.0; IMPLEMENTATION_PLAN at 0.4.0.

## 1. Functional requirements
| FR | P | Flow | UI | API | DB | Task | Test |
|---|---|---|---|---|---|---|---|
| FR-001 Sign-up/in/out/reset | P0 | FLOW-001, FLOW-002 | UI-002, UI-003, UI-004 | API-001 | DB-001 | TASK-008 | TEST-001, TEST-002 |
| FR-002 Role onboarding | P0 | FLOW-001 | UI-005 | API-002 | DB-001, DB-002 | TASK-009 | TEST-003 |
| FR-003 Tester identities | P0 | FLOW-003 | UI-006 | API-003 | DB-003 | TASK-010 | TEST-004 |
| FR-004 PayPal email + hold | P0 | FLOW-003, FLOW-012 | UI-006, UI-011 | API-002 | DB-001 | TASK-009, TASK-020 | TEST-021 |
| FR-005 Campaign draft | P0 | FLOW-004 | UI-012, UI-013 | API-004 | DB-004, DB-018 | TASK-011 | TEST-006 |
| FR-006 Server quote | P0 | FLOW-004 | UI-013 | API-004, API-005 | DB-004, DB-015 | TASK-011, TASK-012 | TEST-007 |
| FR-007 Stripe payment | P0 | FLOW-004 | UI-013, UI-014 | API-005, API-006 | DB-005, DB-014 | TASK-012 | TEST-008, TEST-009 |
| FR-008 Admin review | P0 | FLOW-005 | UI-019 | API-016 | DB-004, DB-006, DB-013 | TASK-014 | TEST-010 |
| FR-009 Recruiting & listing | P0 | FLOW-006 | UI-007, UI-008 | API-007 | DB-004, DB-007, v_campaign_listings | TASK-005, TASK-015 | TEST-011, TEST-012 |
| FR-010 Roster & access | P0 | FLOW-007 | UI-015 | API-009 | DB-007, DB-008, DB-013 | TASK-016 | TEST-014 |
| FR-011 Start testing | P0 | FLOW-007 | UI-015 | API-010 | DB-004, DB-007, DB-008 | TASK-006, TASK-016 | TEST-015 |
| FR-012 Verdicts & auto-pass | P0 | FLOW-009 | UI-016 | API-012, API-021 | DB-007, DB-010 | TASK-018, TASK-019 | TEST-019 |
| FR-013 Settlement & refunds | P0 | FLOW-011, FLOW-005, FLOW-013 | UI-015 | API-021, API-006 | DB-004, DB-005, DB-006 | TASK-013, TASK-018 | TEST-025 |
| FR-014 Cancellation | P0 | FLOW-013 | UI-012, UI-015, UI-019 | API-024, API-016, API-021 | DB-004, DB-006 | TASK-013, TASK-014, TASK-018 | TEST-026 |
| FR-015 Browse | P0 | FLOW-006 | UI-007, UI-008 | API-007 | v_campaign_listings | TASK-015 | TEST-011 |
| FR-016 Join | P0 | FLOW-006 | UI-008, UI-009 | API-008 | DB-003, DB-007 | TASK-006, TASK-015 | TEST-013 |
| FR-017 Opt-in & activation | P0 | FLOW-008 | UI-010 | API-011 | DB-008, DB-017 | TASK-017 | TEST-012, TEST-016 |
| FR-018 Check-ins | P0 | FLOW-008 | UI-009, UI-010, UI-015 | API-011, API-021 | DB-008, DB-017 | TASK-006, TASK-017, TASK-018 | TEST-015, TEST-016, TEST-018 |
| FR-019 Withdraw | P0 | FLOW-006, FLOW-008 | UI-010 | API-008 | DB-007 | TASK-015, TASK-017 | TEST-037 |
| FR-020 Wallet | P0 | FLOW-012 | UI-011 | API-014 | DB-010, wallet_balances | TASK-020 | TEST-038 |
| FR-021 Reward crediting | P0 | FLOW-009, FLOW-010 | UI-011, UI-016 | API-012, API-013, API-021 | DB-010 | TASK-006, TASK-019 | TEST-022 |
| FR-022 Payout request | P0 | FLOW-012 | UI-011 | API-015 | DB-010, DB-011 | TASK-020 | TEST-020 |
| FR-023 PayPal execution | P0 | FLOW-012 | UI-021 | API-017, API-018 | DB-010, DB-011, DB-014 | TASK-021 | TEST-024 |
| FR-024 Disputes | P0 | FLOW-010 | UI-010, UI-020 | API-013 | DB-009, DB-007 | TASK-019 | TEST-023 |
| FR-025 Moderation | P0 | FLOW-014 | UI-022 | API-019 | DB-001, DB-002, DB-013 | TASK-006, TASK-022 | TEST-028 |
| FR-026 Fraud controls | P0 | FLOW-003, FLOW-008, FLOW-012 | UI-021 | API-003, API-011, API-017 | DB-001, DB-003, DB-008, DB-016 | TASK-010, TASK-017, TASK-021 | TEST-004, TEST-017 |
| FR-027 Notifications | P0 | all | UI-017 | API-022 | DB-012 | TASK-007, TASK-024 | TEST-030 |
| FR-028 Admin console | P0 | FLOW-005, FLOW-010, FLOW-012, FLOW-014 | UI-018 | API-025 | multiple | TASK-022 | TEST-041 |
| FR-029 Settings | P0 | FLOW-004 (consumer) | UI-023 | API-020 | DB-015 | TASK-022 | TEST-031 |
| FR-030 Audit log | P0 | admin flows | UI-024 | API-025 | DB-013 | TASK-004, TASK-007, TASK-022 | TEST-027 |
| FR-031 Account deletion | P1 | FLOW-015 | UI-006 | API-023 | DB-001, DB-003, DB-017 | TASK-023 | TEST-029 |
| FR-032 Policies & disclosures | P0 | FLOW-001 | UI-002, UI-005, UI-026 | API-001, API-002 | DB-001 | TASK-003, TASK-008, TASK-009 | TEST-039 |
| FR-033 Platform rules | P0 | FLOW-004 | UI-013 | API-004 | DB-015 | TASK-011 | TEST-040 |

## 2. Non-functional requirements
| NFR | Task | Verification |
|---|---|---|
| NFR-001 Security | TASK-000 (secrets handling), TASK-005, TASK-007, TASK-026 | TEST-005, TEST-034 |
| NFR-002 Payment integrity | TASK-006, TASK-012, TASK-021, TASK-024 | TEST-009, TEST-020, TEST-022, TEST-024, TEST-036 |
| NFR-003 Privacy | TASK-005, TASK-017, TASK-023 | TEST-005, TEST-029; legal review OD-003 |
| NFR-004 Availability | TASK-027 | uptime monitor evidence |
| NFR-005 Performance | TASK-026 | TEST-033 |
| NFR-006 Accessibility | TASK-003, TASK-025 | TEST-032 |
| NFR-007 Observability | TASK-007, TASK-024, TASK-027 | TEST-030; alert drill (TASK-027) |
| NFR-008 Backup/recovery | TASK-027 | restore drill record |
| NFR-009 Localisation | TASK-003 | money/time unit tests |
| NFR-010 Compatibility | TASK-002, TASK-025 | Playwright chromium/webkit/Pixel 7 |
| NFR-011 Rate limiting | TASK-007, TASK-008, TASK-017, TASK-020 | TEST-002, TEST-016, TEST-020 |
| NFR-012 Retention | TASK-023 | TEST-035 |
| NFR-013 Scale | TASK-026 | TEST-033 |
| NFR-014 Email deliverability | TASK-008, TASK-027 | DNS check record |

## 3. Coverage of IDs (reverse checks)
| Artifact | All referenced? | Notes |
|---|---|---|
| UI-001…UI-026 | yes | UI-001 → TASK-003/025; UI-025/026 → TASK-003 |
| API-001…API-025 | yes | API-025 added in TRD 0.1.0 for FR-028/FR-030 |
| DB-001…DB-018 | yes | DB-016 rate_limits via TASK-007 |
| FLOW-001…FLOW-015 | yes | |
| JOB-001…JOB-008 | yes | JOB-001/002 TASK-018; 003 TASK-012; 004 TASK-021; 005 TASK-023; 006 TASK-013; 007/008 TASK-024 |
| TASK-000…TASK-028 | yes | DAG acyclic (IMPLEMENTATION_PLAN §3); TASK-000 = accounts setup (SETUP.md, doctor) |
| TEST-001…TEST-042 | yes | each mapped to ≥1 task |
