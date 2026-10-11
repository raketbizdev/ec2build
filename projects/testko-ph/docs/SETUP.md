# SETUP — accounts & environment (testko-ph)

Generated from `docs/setup.json` by the EC2Build doctor. Do not edit by hand; update setup.json and re-render.

**Levels:** AUTO = the agent runs it after you log in · ASSISTED = you follow exact steps, the agent verifies · OWNER-ONLY = legally yours (terms, payments, identity).

**Secrets:** put values only in `.env.local` of the app repo (or your host's env settings). Never paste them into chat. Check progress with `/ec2build doctor --stage <stage>`.

| Service | Needed for | Cost note |
|---|---|---|
| Local toolchain | local, staging, production | Free |
| Supabase | local, staging, production | Local: free. Cloud: free tier (limits; idle projects may pause); Pro plan recommended for production backups (TQ-4) |
| Stripe | local, staging, production | No monthly fee; per-transaction fees. Account country support must be confirmed (OD-001) |
| PayPal Payouts | local, staging, production | Sandbox free; per-payout fees in live (confirm); Payouts must be enabled (OD-002) |
| Resend (email) | staging, production | Free tier available; confirm limits |
| Vercel (web hosting + cron) | staging, production | Free Hobby plan is for non-commercial use; the TRD assumes Pro (paid) for commercial use and sub-daily cron (A-016). A free commercial-friendly host would need a TRD update. |
| GitHub | staging, production | Free tier available |
| Sentry | staging, production | Free developer tier available |
| Domain | production | Paid (yearly, varies by registrar) |

## Stage: local

### Local toolchain: Node.js, pnpm, git, Docker for local development
- Tools on PATH: `node`, `pnpm`, `git`, `docker`
1. **OWNER-ONLY** (you): Install Docker Desktop (https://www.docker.com/products/docker-desktop/) and start it
2. **AUTO** (agent): Install pnpm via corepack (corepack enable) and generate CRON_SECRET / AUDIT_IP_SALT with openssl rand -hex 32 into .env.local
- Env variables (names only): `NEXT_PUBLIC_APP_URL`, `CRON_SECRET`, `AUDIT_IP_SALT`
- Verify: `node -v && pnpm -v && docker info`

### Supabase: Postgres database, auth, storage (DB-001…DB-018)
- Tools on PATH: `supabase`
1. **AUTO** (agent): supabase init && supabase start; copy API URL / anon key / service_role key from `supabase status` into .env.local
- Env variables (names only): `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`
- Verify: `supabase status`

### Stripe: Developer payments and refunds (FR-007, FR-013)
- Tools on PATH: `stripe`
1. **OWNER-ONLY** (you): Create a Stripe account at https://dashboard.stripe.com/register (test mode is enough for local/staging)
2. **ASSISTED** (you): Run `stripe login`; copy the test secret key (Developers > API keys) into .env.local as STRIPE_SECRET_KEY
3. **AUTO** (agent): stripe listen --forward-to localhost:3000/api/v1/webhooks/stripe; owner pastes the printed whsec_ value into .env.local as STRIPE_WEBHOOK_SECRET
- Env variables (names only): `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
- Verify: `stripe config --list`

### PayPal Payouts: Tester payouts (FR-023)
1. **OWNER-ONLY** (you): Log in at https://developer.paypal.com with a PayPal account
2. **ASSISTED** (you): Apps & Credentials > Sandbox > Create App; put Client ID/Secret in .env.local; PAYPAL_API_BASE=https://api-m.sandbox.paypal.com
- Env variables (names only): `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_API_BASE`
- Verify: `agent runs an OAuth token request against the sandbox and reports success (no secrets printed)`

## Stage: staging

### Supabase: Postgres database, auth, storage (DB-001…DB-018)
1. **OWNER-ONLY** (you): Create a Supabase account and organisation at https://supabase.com/dashboard
2. **ASSISTED** (you): Run `supabase login` (browser) or create an access token (Account > Access Tokens) and put it in .env.local as SUPABASE_ACCESS_TOKEN
3. **AUTO** (agent): supabase projects create testko-ph-staging --region ap-southeast-1; supabase link; supabase db push
- Env variables (names only): `SUPABASE_ACCESS_TOKEN`
- Verify: `supabase projects list`

### Stripe: Developer payments and refunds (FR-007, FR-013)
1. **AUTO** (agent): Register the staging webhook endpoint via Stripe CLI/API with the events in TRD §7.1

### PayPal Payouts: Tester payouts (FR-023)
1. **AUTO** (agent): Register the staging webhook via PayPal REST API (POST /v1/notifications/webhooks); owner copies the webhook id into env as PAYPAL_WEBHOOK_ID
- Env variables (names only): `PAYPAL_WEBHOOK_ID`

### Resend (email): Transactional email + Supabase Auth SMTP (FR-027)
1. **OWNER-ONLY** (you): Create a Resend account at https://resend.com and an API key
2. **ASSISTED** (you): Add the DNS records Resend shows for your sending domain (needs a domain, OD-008)
3. **AUTO** (agent): Send a test email and configure Supabase Auth SMTP settings
- Env variables (names only): `RESEND_API_KEY`, `EMAIL_FROM`, `ADMIN_ALERT_EMAIL`
- Verify: `agent sends a test email to ADMIN_ALERT_EMAIL`

### Vercel (web hosting + cron): Host the Next.js app and run cron jobs (ADR-001, ADR-006)
- Tools on PATH: `vercel`
1. **OWNER-ONLY** (you): Create a Vercel account at https://vercel.com and choose a plan
2. **ASSISTED** (you): Run `vercel login`
3. **AUTO** (agent): vercel link; vercel env add (owner types each secret value at the prompt); vercel deploy
- Verify: `curl -fsS <staging-url>/api/health`

### GitHub: Code hosting and CI (TRD §14)
- Tools on PATH: `gh`
1. **ASSISTED** (you): Run `gh auth login`
2. **AUTO** (agent): gh repo create (private) and push; gh secret set for CI (owner types values)
- Verify: `gh auth status`

### Sentry: Error tracking (NFR-007)
1. **OWNER-ONLY** (you): Create a Sentry account and a Next.js project at https://sentry.io; copy the DSN into env
- Env variables (names only): `SENTRY_DSN`, `NEXT_PUBLIC_SENTRY_DSN`
- Verify: `agent triggers a test error and confirms it appears`

## Stage: production

### Supabase: Postgres database, auth, storage (DB-001…DB-018)
1. **OWNER-ONLY** (you): Approve creating the production project and choose the plan

### Stripe: Developer payments and refunds (FR-007, FR-013)
1. **OWNER-ONLY** (you): Activate live mode (business verification) and approve live keys

### PayPal Payouts: Tester payouts (FR-023)
1. **OWNER-ONLY** (you): PayPal Business account with Payouts enabled; approve live credentials

### Domain: Production URL, email sending domain (OD-008)
1. **OWNER-ONLY** (you): Buy the domain and give the agent access to edit DNS or apply records it lists
- Verify: `dig +short <domain>`
