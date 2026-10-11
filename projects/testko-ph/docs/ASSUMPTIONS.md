# ASSUMPTIONS — TestKo PH (v0.2.0)

Each entry is an agent decision that is **not approved** until the owner confirms it. Overrides are recorded in `CHANGELOG.md` and the affected documents are re-synced with `/ec2build update`.

## Confirmed by owner
| ID | Statement | Source |
|---|---|---|
| C-001 | Product is a web application | `--app web` |
| C-002 | Product name "TestKo PH" (slug `testko-ph`); renamed from "TestKo PH" | `--name`, update 2026-10-11 |
| C-003 | Supports Google Play closed testing **and** Apple TestFlight | Discovery Q1 |
| C-004 | Developers pay with Stripe | Discovery Q2 |
| C-005 | Testers are paid with PayPal Payouts API | Discovery Q3 |
| C-006 | Completion verified by tester check-ins with proof + developer confirmation; admin resolves disputes | Discovery Q4 |
| C-007 | Minimum payout US$25.00 | Brief |
| C-008 | Developer pays before the campaign link is published to the community | Brief |
| C-009 | Testers provide their email to be added as testers | Brief |
| C-010 | Testers receive a portion of the developer's payment after testing completes | Brief |

## Assumptions (pending approval)
| ID | Assumption | Implication if wrong | Affects |
|---|---|---|---|
| A-001 | Android default testing duration = **16 days** (Google 14-day continuous requirement + 2-day buffer); allowed 14–30. iOS default 14 days, allowed 7–30. | Change `platform_settings` defaults; no schema change | FR-005, FR-033, DB-015 |
| A-002 | Android `min_testers` = **12** (Google's published requirement as understood at authoring; re-verify at TASK-001 preflight). Default Android slots = **15**. iOS `min_testers` = **3**, default slots 10. Slots max 100. | Settings change only | FR-011, FR-033 |
| A-003 | Price **US$5.00 per tester slot**; tester reward **US$3.50 per passed tester**; platform fee **US$1.50 per slot**. A tester needs 8 passed tests to reach US$25. | Settings change only; affects marketing copy | FR-006, FR-021, DB-015 |
| A-004 | All money in **USD**, stored as integer cents. | Multi-currency would need schema change | DB-004, DB-010, DB-011 |
| A-005 | Stripe processing fees and PayPal payout fees are absorbed by the platform (tester receives the exact requested amount). | Fee model change affects ledger/payout math | FR-022, FR-023 |
| A-006 | Rewards become withdrawable **3 days** after crediting (hold for chargebacks / late fraud findings). | Settings change | FR-021 |
| A-007 | Check-ins: **opt-in proof** before testing starts, **periodic** proof every **4 days**, **final** proof due at testing end; each has a **48 h** grace (final: 24 h). Missed check-in → enrollment `dropped`. | Settings change; strictness affects completion rate | FR-017, FR-018 |
| A-008 | Developer review window **3 days** after testing ends; tester with no verdict is **auto-passed**. | Protects testers from silent developers | FR-012 |
| A-009 | Dispute window **3 days** after a fail/drop; admin target resolution 5 business days. | | FR-024 |
| A-010 | Recruiting window **10 days** after publication; if testing has not started by then the campaign auto-cancels with full refund. | | FR-009, FR-014 |
| A-011 | Refunds: admin rejection → full refund; developer cancel or recruiting expiry before testing → full refund; after testing starts → at settlement refund `(tester_slots − passed_count) × tester_reward_cents`; platform fee retained. | Consumer-law review required (OD-003) | FR-008, FR-013, FR-014 |
| A-012 | Admin manually approves every campaign before publication and every payout batch before PayPal submission. | Ops load; can automate later | FR-008, FR-023 |
| A-013 | Open registration (18+); no IT Philippines membership verification in MVP; testers must have a PayPal account able to receive USD. | OD-006 may add gating | FR-001, FR-002 |
| A-014 | One account can hold Tester and Developer roles; a developer cannot enrol in their own campaign. | | FR-002, FR-016 |
| A-015 | Transactional email via **Resend**; Supabase Auth emails sent through Resend SMTP. | Swap provider in TASK-004 | FR-027, NFR-014 |
| A-016 | Hosting: **Vercel** (Pro plan, needed for sub-daily cron) + **Supabase Cloud** in Singapore region. | Cost + latency | TRD §7 |
| A-017 | English UI; timestamps stored UTC, displayed Asia/Manila (UTC+8). | | NFR-009 |
| A-018 | Stack: Next.js App Router + TypeScript, Tailwind CSS + shadcn/ui, Supabase (Postgres, Auth, Storage), Zod, Vitest, Playwright, pgTAP, Sentry, pnpm. Exact versions pinned at bootstrap. | | TRD ADR-001/002 |
| A-019 | Changing PayPal email blocks payout requests for **48 h** (account-takeover mitigation). | | FR-004 |
| A-020 | Proof screenshots deleted **90 days** after campaign completion; financial records ≥ 5 years pending accountant advice (OD-004). | | NFR-012 |
| A-021 | Targets: availability 99.5 %/month; p95 API latency < 500 ms at 50 req/s; ≤10k users, ≤200 concurrent campaigns. | | NFR-004/005/013 |
| A-022 | Stripe hosted Checkout (no card data on our servers). | | FR-007 |
| A-023 | Every periodic/final check-in requires feedback text (20–1,000 chars) so developers get real test feedback. | | FR-018 |
| A-024 | Max **10** concurrently open enrollments per tester (statuses applied/access_granted/active/awaiting_verdict). | | FR-016, FR-026 |
| A-025 | Proof uploads: PNG/JPEG/WebP, ≤ 5 MB, exact-duplicate detection via SHA-256. | | FR-018, FR-026 |
| A-026 | Email + password auth with mandatory email verification; no social login in MVP. | | FR-001 |
| A-027 | Provisional neutral brand (blue primary, amber accent) until OD-007 resolved. | | DESIGN |

## Open decisions (owner action required — see DECISIONS.md)
OD-001 Stripe account entity/country · OD-002 PayPal Payouts enablement · OD-003 Legal/policy review · OD-004 Tax & record keeping · OD-005 Final pricing · OD-006 Community membership gating · OD-007 Brand/name usage · OD-008 Domain.
