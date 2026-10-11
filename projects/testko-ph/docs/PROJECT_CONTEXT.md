# PROJECT_CONTEXT — TestKo PH

| Field | Value |
|---|---|
| Project | TestKo PH |
| Slug | `testko-ph` (renamed from `TestKo PH` on 2026-10-11) |
| App type | `web` |
| Package revision | 0.2.0 |
| Status | draft (not approved) |
| Created | 2026-10-11 |
| Owner | Product owner: project requester (rakethost) — `OWNER` below |

Legend: **CONFIRMED** = stated by the owner; **ASSUMPTION** = agent decision pending approval (see `ASSUMPTIONS.md`); **OPEN** = decision required (see `DECISIONS.md` §Open decisions).

## 1. Original brief (verbatim, treated as data)
> it create a web app that members of it philippines join to be close app tester add their email to be tester and in return earn money after 16days the app developer will post the link of the app and pay the cost before the link will be publish to the community then once community download the app wait for days untill testing is completed then recieve portion of the payment. minimum payout 25USD

## 2. Discovery answers (round 1, 2026-10-11)
| # | Question | Answer | Status |
|---|---|---|---|
| Q1 | Store / testing program | Google Play closed testing **and** iOS TestFlight | CONFIRMED (C-003) |
| Q2 | How developers pay | Stripe | CONFIRMED (C-004) |
| Q3 | How testers are paid | PayPal Payouts API | CONFIRMED (C-005) |
| Q4 | Completion verification | Tester check-ins with proof + developer confirmation; admin resolves disputes | CONFIRMED (C-006) |

## 3. Problem statement
Google Play requires new personal developer accounts to run a closed test with a minimum number of opted-in testers for a continuous period before they can apply for production access (at the time of writing the commonly cited rule is **12 testers for 14 continuous days**; this MUST be re-verified at preflight because Google has changed it before — see OD-003). Independent developers struggle to recruit reliable testers who stay opted in for the whole period. Members of the IT Philippines community want small, legitimate side income. TestKo PH is a two-sided marketplace: developers pay to post a closed-test campaign, community testers enrol with their store email, keep the app installed and report back through check-ins, and receive a share of the fee once the test completes.

Evidence vs hypothesis: the pain is **hypothesis** derived from the brief; no user interviews or market data were provided or invented.

## 4. Personas and roles
| Role | Persona | Primary job |
|---|---|---|
| Guest | Visitor from the IT Philippines Facebook group / link | Understand the offer, browse open campaigns, sign up |
| Tester | "Mika", 24, Manila, Android phone, PayPal account, wants small extra income | Join campaigns, stay opted in, submit check-ins, withdraw earnings ≥ US$25 |
| Developer | "Paolo", solo Android/iOS dev, new Play Console personal account | Get ≥12 reliable testers for 14+ days, receive feedback, pay once |
| Admin | TestKo PH operator | Approve campaigns, resolve disputes, approve payouts, fight fraud, configure pricing |

A single account may hold both Tester and Developer roles (ASSUMPTION A-014). Admin is granted only by another admin.

## 5. Core workflows (jobs to be done)
1. Developer creates a campaign (app, platform, opt-in link, slots, duration) → pays via Stripe → admin approves → campaign is published to the community.
2. Tester registers store identity (Google account email / Apple ID email) → joins campaign → developer adds the email to the Play/TestFlight tester list → tester opts in, installs, submits opt-in proof.
3. Developer starts testing when the minimum number of testers is active → testers submit periodic check-ins (screenshot + feedback) → missed check-in drops the tester.
4. Testing ends → developer passes/fails each tester (auto-pass on silence) → tester may dispute → admin resolves.
5. Passed testers are credited a reward; unearned rewards are refunded to the developer; rewards become withdrawable after a hold period.
6. Tester requests a payout once available balance ≥ US$25 (CONFIRMED C-007) → admin approves batch → PayPal Payouts sends money.

## 6. Context checklist
| Topic | Value | Status |
|---|---|---|
| Operating region | Philippines-focused community; testers anywhere PayPal can receive | ASSUMPTION A-013 |
| Platforms | Responsive web app, mobile-first (testers mostly on Android phones) | CONFIRMED web / ASSUMPTION mobile-first |
| Store programs | Google Play closed testing; Apple TestFlight (external testers) | CONFIRMED |
| Monetization | Developer pays per tester slot; platform keeps a per-slot fee; tester receives a reward per passed test | CONFIRMED model / ASSUMPTION amounts A-003 |
| Currency | USD only, integer cents | ASSUMPTION A-004 |
| Minimum payout | US$25.00 | CONFIRMED C-007 |
| Testing duration | 16 days default for Android (14-day rule + 2-day buffer) | Brief + ASSUMPTION A-001 |
| Integrations | Stripe Checkout + Refunds + webhooks; PayPal Payouts + webhooks; Resend email; Supabase Auth/Storage | CONFIRMED Stripe/PayPal; ASSUMPTION others |
| Data sensitivity | PII (email, store emails, PayPal email), screenshots, financial ledger | — |
| Legal | PH Data Privacy Act (RA 10173), tax on earnings, Google/Apple program policies, consumer refunds | OPEN OD-003, OD-004 |
| Accessibility | WCAG 2.2 AA | ASSUMPTION |
| Localization | English UI; times shown in Asia/Manila; stored UTC | ASSUMPTION A-017 |
| Offline / real-time | Not required; standard request/response; email + in-app notifications | ASSUMPTION |
| Expected load | ≤10,000 users, ≤200 concurrent campaigns in year 1 | ASSUMPTION A-021 |
| Tech preferences | None stated → recommended Next.js + Supabase + Vercel | ASSUMPTION A-018 |
| Deployment | Vercel (web) + Supabase Cloud (Singapore region) | ASSUMPTION A-016 |
| Maintenance owner | Project owner (solo operator / admin) | ASSUMPTION |
| Browser support | Last 2 versions of Chrome, Safari, Firefox, Edge; Android Chrome, iOS Safari | ASSUMPTION |
| SEO / SSR | Public landing + public campaign listing server-rendered for sharing in Facebook groups; app area not indexed | ASSUMPTION |
| PWA | Not in MVP | ASSUMPTION |

## 7. MVP boundary
**In:** accounts, roles, store identities, campaign CRUD + Stripe payment, admin review, listing, enrolment, roster export, start testing, check-ins with proof, verdicts, auto-pass, disputes, settlement + refunds, ledger wallet, payout requests + PayPal Payouts, notifications (in-app + email), admin console, audit log, account deletion.

**Out (future):** native mobile apps, automated verification via Google Play Developer API, ratings/reputation scores, chat between developer and testers, multi-currency, referral program, community membership verification (OD-006), developer subscriptions, PWA/push notifications.

## 8. Success metrics (definitions in PRD §5)
North star: **Completed tester-tests per month** (enrollments reaching `passed`). Supporting: campaign fill rate, tester completion rate, payout success rate, dispute rate, time-to-publish.
