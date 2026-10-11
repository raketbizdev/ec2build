# SHARED_RESPONSIBILITY — TestKo PH

Who does what, from planning to running the live marketplace. Legend: **R** = does it · **A** = accountable / approves · **S** = supports / guides · **—** = not involved.
EC2Build (the spec agent) is free. The services below run on the **owner's own accounts** (see [SETUP.md](SETUP.md) for costs and steps).

## 1. Matrix
| Area | You (owner / TestKo PH operator) | EC2Build agent | Coding agent | Providers |
|---|---|---|---|---|
| Product scope, pricing (A-003/OD-005), timing rules | A/R | S: proposes, records assumptions | — | — |
| Spec consistency (six docs, traceability) | A: approves | R | S: reports conflicts | — |
| Accounts & terms: Supabase, Stripe, PayPal, Resend, Vercel, GitHub, Sentry, domain | A/R | S: SETUP.md, links | S: verifies with doctor | R: their platforms |
| Business verification / KYC (Stripe live, PayPal Business + Payouts) | A/R | S: flags OD-001/OD-002 | — | R: approval decisions |
| Secrets (API keys, webhook secrets, service-role key) | A/R: create, store in `.env.local` / host env | S: lists names, rules | S: uses via env only, never prints or commits | R: issuance, rotation |
| Provisioning (Supabase projects, buckets, webhooks, Vercel project, cron) | A: authorises each stage | S | R: AUTO steps | R: runs infrastructure |
| Code, migrations, tests (TASK-001…028) | A: reviews each PROMPT report, approves commits | S: prompts + acceptance criteria | R | — |
| App security: RLS, ledger integrity, webhook verification, rate limits | A: accepts residual risk | R: specifies (TRD §10, SCHEMA §7) | R: implements + tests (TEST-005, 009, 020–024) | — |
| Platform security & uptime (DB servers, hosting, card data at Stripe) | — | — | — | R |
| Campaign approval, disputes, payout approval, fraud review | A/R: admin role | S: rules in PRD | R: builds admin tools | — |
| Money movement (charges, refunds, payouts) | A: approves payout batches; owns losses (e.g., chargebacks R-03) | S | R: implements idempotent flows | R: processing per their terms |
| Legal: ToS, privacy notice (PH Data Privacy Act), tester/developer rules, tax (OD-003/OD-004) | A/R with counsel/accountant | S: flags issues | R: publishes approved texts | — |
| Store programs (Google Play closed testing, TestFlight) | — (TestKo PH itself is a web app) | S: explains rules to users | — | R: Google/Apple decide production access |
| Developers' own Play Console / App Store Connect accounts | — | — | — | Each **developer user** is responsible for adding tester emails and their own store compliance |
| End-user data (testers' emails, PayPal emails, screenshots) | A/R: data controller | S: retention/deletion spec (NFR-012) | R: deletion & retention jobs | R: processors per their terms |
| Staging & production deployment, live keys | A: explicit approval (PROMPT 27/28) | S | R: executes after approval | R: hosting |
| Monitoring, backups, incidents, daily admin queues | A/R | S: runbooks | R: alerts, reconciliation, scripts | R: platform backups/status pages |
| Costs and usage limits | A/R | S: notes cost drivers (TRD §13) | S: reports usage | R: billing |

## 2. Lines nobody crosses
- No agent accepts terms, pays fees, verifies identity, answers store/policy declarations or turns on live money for you.
- No agent asks you to paste secrets into chat; values go into `.env.local` or your host's settings.
- Anything outside your machine (creating cloud projects, deploying, sending real payouts) needs your approval first, and the agent reports the real result.

## 3. Provider-side responsibilities (summary; their terms prevail)
| Provider | They are responsible for |
|---|---|
| Supabase | Database/auth/storage infrastructure, platform security, backups per plan |
| Stripe | Card data security (hosted Checkout), payment processing, disputes process |
| PayPal | Payout delivery, recipient account handling, holds/returns |
| Vercel | Hosting, edge network, cron execution per plan |
| Resend | Email delivery infrastructure |
| GitHub | Code hosting, Actions runners |
| Sentry | Error data storage per their retention |
