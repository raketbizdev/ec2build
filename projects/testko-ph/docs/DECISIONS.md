# DECISIONS — TestKo PH

## 1. Product decisions
| ID | Decision | Status | Source |
|---|---|---|---|
| PD-001 | Web app (responsive, mobile-first for testers) | Confirmed | C-001 |
| PD-002 | Supports Google Play closed testing and Apple TestFlight | Confirmed | C-003 |
| PD-003 | Developers pay up front with Stripe before publication | Confirmed | C-004, C-008 |
| PD-004 | Testers paid via PayPal Payouts; minimum payout US$25 | Confirmed | C-005, C-007 |
| PD-005 | Verification = check-ins with proof + developer verdict; admin resolves disputes | Confirmed | C-006 |
| PD-006 | Auto-pass when developer doesn't review within 3 days | Assumed | A-008 |
| PD-007 | Admin approves campaigns and payout batches manually | Assumed | A-012 |
| PD-008 | Pricing US$5.00/slot, reward US$3.50, fee US$1.50 | Assumed | A-003 |
| PD-009 | Refund unearned rewards at settlement; platform fee retained after testing starts | Assumed | A-011 |

## 2. Architecture decisions
ADR-001…ADR-011 are recorded in `TRD.md` §1 (status: **proposed**, pending owner approval).

## 3. Open decisions (owner action)
| ID | Decision needed | Why it matters | Blocks | Owner | Suggested next step |
|---|---|---|---|---|---|
| OD-001 | Which legal entity/country holds the Stripe account? | Stripe's supported-country list must include the account's country; a Philippines-only entity may not qualify (verify on Stripe's site). | Production payments (TASK-028) | Owner | Check Stripe's current country list; consider an entity in a supported country, or switch provider via `/ec2build update` |
| OD-002 | PayPal Business account with Payouts enabled | Payouts API requires enablement/approval | Production payouts (TASK-028) | Owner | Apply early; test in sandbox meanwhile |
| OD-003 | Legal review: ToS, Privacy Notice (PH Data Privacy Act), Tester/Developer Rules, consumer refund terms, and compatibility with Google Play / Apple testing policies | Paying testers could conflict with store policies if not structured carefully; incentivized reviews are prohibited | Production (TASK-028) | Owner + counsel | Engage counsel; supply approved texts for UI-026 |
| OD-004 | Tax and record-keeping obligations for platform revenue and tester payouts (e.g., BIR), possible need to collect tax info | Compliance; may add fields (TIN) and flows | Production payouts | Owner + accountant | Accountant consultation; may trigger schema update |
| OD-005 | Final pricing, reward split, fee absorption | Unit economics after Stripe + PayPal fees | Production settings | Owner | Model with current fee schedules |
| OD-006 | Restrict sign-up to verified IT Philippines members? | Trust vs growth | R2 (no MVP block) | Owner | Decide verification method (e.g., invite codes) |
| OD-007 | Permission to use "IT Philippines" name/branding | Brand/legal | Landing copy & logo | Owner | Obtain written permission or rebrand |
| OD-008 | Production domain name | Email DNS, OAuth redirects, Stripe/PayPal webhooks | TASK-027/028 | Owner | Register domain |

## 4. Override log
| Date | Item | Old | New | Rationale | By |
|---|---|---|---|---|---|
| 2026-10-11 | App name / slug (C-002) | itphteste / `itphteste` | TestKo PH / `testko-ph` | Owner requested full rename | Owner via `/ec2build update` |
