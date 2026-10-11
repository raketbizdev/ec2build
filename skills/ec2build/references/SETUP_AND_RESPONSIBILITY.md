# Accounts setup assistant & shared responsibility

EC2Build is free and open source. The **third-party services** a project uses (database, app stores, payments, hosting, email…) run on the **owner's own accounts**, which may be free or paid. EC2Build's job is to make those accounts as painless as possible: automate what can be automated, guide click-by-click what cannot, verify everything, and state clearly who is responsible for what.

## 1. Default stack choices (unless the owner prefers otherwise)
| Need | Default | Notes |
|---|---|---|
| Database, auth, file storage | **Supabase**: local via Supabase CLI + Docker (free, offline); cloud project for staging/production | Cloud free tier has limits and may pause idle projects; verify current limits at setup |
| Web app | Next.js (or the stack chosen in the TRD) | |
| Native mobile (Android/iOS) | **Expo (React Native + TypeScript)**, one codebase for Android, iOS and web | Ask during discovery: web, mobile or both. Never silently limit to web/PWA when native is wanted |
| Android build | Local Gradle build (free) or Expo EAS Build free tier | |
| iOS build | Local Xcode on macOS, or EAS Build | Apple Developer Program is paid |
| Web hosting | A free tier that allows the project's use (check commercial-use terms) | e.g., Cloudflare Pages / Netlify; some free tiers are non-commercial only |
| Store upload automation | fastlane (free, open source) or `eas submit` with a Google service account / App Store Connect API key | |
Always state unavoidable third-party costs (e.g., Google Play developer registration, Apple Developer Program, payment processing fees) in `SETUP.md`. Prices change: tell the owner to confirm on the provider's site, and never present a price as verified unless it was checked.

## 2. Automation levels (label every setup step)
- **AUTO**: the agent runs it (CLI/API) once the owner has logged in or provided a token (e.g., `supabase projects create`, `supabase db push`, `stripe webhook_endpoints create`, `gh repo create`).
- **ASSISTED**: the agent opens or gives the exact URL and the exact clicks/fields, waits, then **verifies** the result (e.g., create the app in Play Console, create a service account key).
- **OWNER-ONLY**: legal identity, payments to providers, accepting terms, 2FA, KYC, store policy declarations. The agent explains why and verifies afterwards where possible.
Logins use the provider's own CLI/browser flow (`supabase login`, `stripe login`, `gh auth login`, `eas login`, `wrangler login`…). The agent never asks for passwords.

## 3. Secrets rules
1. The owner creates keys in the provider dashboard and pastes them **directly into the local `.env.local`** (or a secret manager / host env settings). They are never pasted into chat.
2. Agents read secrets only through the environment; never print, log or commit them. `.env*` (except `.env.example`) is git-ignored.
3. The setup doctor checks that each variable is **present**, never its value.
4. Separate test/sandbox keys from live keys; live keys only at production release with explicit owner approval.

## 4. Required project outputs
- `docs/SETUP.md`: **generated** from setup.json with `python3 <SKILL_DIR>/scripts/doctor.py <project-dir> --render` (never hand-edited). Per service: purpose, cost note, environments (local/staging/production), automation level per step, exact owner steps with URLs, agent commands, env variable names, how it is verified, troubleshooting. Ordered so `local` works first with zero paid accounts where possible.
- `docs/setup.json`: machine-readable version used by `scripts/doctor.py` (format below).
- `docs/SHARED_RESPONSIBILITY.md`: project-specific responsibility matrix (section 6) plus each service's provider-side responsibilities.
- The implementation plan starts with **PROMPT 00: accounts & environment setup** (uses SETUP.md, runs AUTO steps, walks ASSISTED steps, stops for OWNER-ONLY steps, ends with `doctor.py` green for `local`). Later prompts re-run the doctor for `staging`/`production` before deploying.

### `setup.json` format (`ec2build-setup/1`)
```json
{"format": "ec2build-setup/1",
 "env_file": ".env.local",
 "services": [
  {"id": "supabase", "name": "Supabase", "purpose": "Database, auth, storage",
   "stages": ["local", "staging", "production"],
   "cost": "Free tier available; confirm limits",
   "cli": ["supabase", "docker"],
   "env": {"local": ["NEXT_PUBLIC_SUPABASE_URL", "NEXT_PUBLIC_SUPABASE_ANON_KEY", "SUPABASE_SERVICE_ROLE_KEY"],
           "staging": ["SUPABASE_ACCESS_TOKEN"]},
   "steps": [
     {"who": "owner", "level": "OWNER-ONLY", "text": "Create a Supabase account at https://supabase.com", "stage": "staging"},
     {"who": "agent", "level": "AUTO", "text": "supabase start (local stack)", "stage": "local"}
   ],
   "verify": {"local": "supabase status"}}
 ]}
```
`stages` = where the service is needed. `env[stage]` lists variables needed for that stage (cumulative with earlier stages). `cli` = executables that must be on PATH.

### Doctor
`python3 <SKILL_DIR>/scripts/doctor.py <project-dir> --stage local|staging|production [--app <app-repo-dir>]` reports per service: CLIs found/missing, env vars present/missing (from the environment and `<app>/.env.local`), and the owner steps still to do. Exit code 1 when anything required for that stage is missing.

## 5. Provider playbook (verify details at setup time: providers change)
| Service | Owner (one-time) | Agent can automate after login/token |
|---|---|---|
| Supabase | Create account/org; for cloud, generate an access token | `supabase init/start` (local), `supabase login`, `projects create`, `link`, `db push`, `gen types`, storage buckets via migrations |
| Google Play Console | Register developer account (one-time fee), identity verification, create the app entry, store listing & policy declarations, first release upload for a new app (if Google still requires it), Google Cloud project + enable Play Developer API + service account JSON key, invite the service-account email in Play Console Users & permissions | Upload AAB to internal/closed tracks, manage testers, release notes, promote tracks (fastlane `supply` or `eas submit`) |
| Apple App Store / TestFlight | Enrol in the Apple Developer Program (annual fee), create app record, App Store Connect API key | Build & upload to TestFlight (fastlane `pilot` / `eas submit`), manage testers |
| Expo / EAS | Create free Expo account | `eas login`, `eas build`, `eas submit` |
| Stripe | Account + business verification (country support varies), live-mode activation | `stripe login`, test keys use, webhook endpoints via CLI/API, local forwarding `stripe listen` |
| PayPal | Business account, Developer app (sandbox/live), Payouts enablement if needed | Webhook registration via REST API, sandbox testing |
| Hosting (Cloudflare Pages / Netlify / Vercel) | Account; custom domain DNS | `wrangler login` + `pages deploy` / `netlify deploy` / `vercel deploy`, env var setup via CLI |
| Email (e.g., Resend) | Account, API key, DNS records for the sending domain | Send test email, template wiring |
| GitHub | Account | `gh auth login`, `gh repo create`, Actions secrets via `gh secret set` (owner pastes value in the terminal prompt) |
| Domain | Purchase domain (paid) | DNS record instructions, verification |

## 6. Shared responsibility model (generic; tailor per project)
Legend: **R** = does it · **A** = accountable / approves · **S** = supports / guides · **—** = not involved.

| Area | You (owner) | EC2Build agent (specs) | Coding agent (build) | Third-party provider |
|---|---|---|---|---|
| Product decisions, scope, pricing | A/R | S (proposes, records assumptions) | — | — |
| Spec quality & cross-doc consistency | A (approves) | R | S (reports conflicts) | — |
| Accounts, terms, identity/KYC, billing with providers | A/R | S (SETUP.md, links, checks) | S (verifies with doctor) | R (their platform) |
| Creating & storing secrets | A/R | S (lists names, rules) | S (uses via env only, never prints) | R (key issuance, rotation tools) |
| Provisioning (DB project, hosting, webhooks, buckets) | A (authorises) | S (plans) | R (AUTO steps) | R (runs the infrastructure) |
| Application code, tests, migrations | A (reviews/approves merges) | S (prompts, acceptance criteria) | R | — |
| App-level security (access rules, validation, auth flows) | A (accepts residual risk) | R (specifies) | R (implements + tests) | — |
| Platform security, uptime, physical infra, managed patching | — | — | — | R |
| Store listings, policy declarations, submissions | A/R (submits/answers) | S (prepares text & checklists) | S (builds & uploads artifacts) | R (review & decision) |
| Production deployment & live keys | A (explicit approval) | S | R (executes after approval) | R (hosting) |
| Legal, privacy notice, tax, consumer rules | A/R (with professionals) | S (flags issues) | — | — |
| End-user data (controller duties, deletion requests) | A/R | S (specifies retention/deletion) | R (implements features) | R (processor duties per their terms) |
| Monitoring, backups, incident response | A/R | S (runbooks) | R (sets up alerts, scripts) | R (platform backups/status) |
| Costs and usage limits | A/R | S (notes cost drivers) | S (reports usage) | R (billing) |

Rules: no agent accepts terms, pays, verifies identity, or uses live money on the owner's behalf; any action outside the local machine needs owner authorisation first; every automated step is verified and reported with its real result.
