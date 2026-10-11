# PRD — TestKo PH Product Requirements Document

## 0. Document control
| Field | Value |
|---|---|
| Document | `PRD.md` (01) |
| Version | 0.2.0 |
| Status | draft — approval is owner-provided, never assumed |
| Owner | Product owner (project requester) |
| Date | 2026-10-11 |
| Upstream inputs | Brief (PROJECT_CONTEXT §1), discovery answers Q1–Q4 |
| Downstream | TRD, APP_FLOW, DESIGN_BRIEF, DATABASE_SCHEMA, IMPLEMENTATION_PLAN |
| Assumptions | `ASSUMPTIONS.md` (C-001…C-010, A-001…A-027) |

## 1. Executive summary
TestKo PH is a responsive web marketplace connecting app developers who need closed-test testers (Google Play closed testing, Apple TestFlight) with members of the IT Philippines community who want to earn money testing apps. A developer creates a campaign, pays up front with Stripe, and — after admin approval — the campaign is published to the community. Testers enrol with their Google/Apple account email, the developer adds those emails to the store's tester list, testers opt in, keep the app installed for the testing period (16 days by default on Android) and submit proof check-ins with feedback. When testing ends the developer confirms each tester (silence = pass), disputes go to an admin, and passed testers earn a reward that becomes withdrawable to PayPal once their available balance reaches **US$25**.

## 2. Customer problem
| Problem | Type |
|---|---|
| New Google Play personal developer accounts must run a closed test with a minimum count of opted-in testers for a continuous period before requesting production access (re-verify rule at preflight, OD-003). | External rule — to verify |
| Solo developers lack a pool of reliable testers; testers drop out early, resetting the clock. | Hypothesis |
| Community members want legitimate small income and have Android/iOS devices. | Hypothesis |
| Informal arrangements (Facebook posts, group chats) have no payment guarantee for testers and no completion guarantee for developers. | Hypothesis |

No interviews, surveys or market sizes were provided; none are claimed.

## 3. Vision and differentiated value
"Reliable closed testers from a trusted Filipino tech community, with escrow-style payment that protects both sides."
- **Escrow-like flow:** developer pays before publication; testers are paid only for passed tests; unearned rewards are refunded.
- **Evidence trail:** dated screenshot check-ins + written feedback give developers material for Google's production-access questionnaire.
- **Fair-by-default:** auto-pass when a developer does not review; admin dispute resolution.

## 4. Users, roles and jobs
| Role | Jobs | Pains | Measurable outcome |
|---|---|---|---|
| Guest | Learn offer, see open campaigns | Unsure if legit | Sign-up conversion ≥ 10 % of landing visitors (target, A-021) |
| Tester | Find campaigns, enrol, stay compliant, get paid | Forgetting check-ins; non-payment risk | ≥ 80 % of active enrollments reach `passed` |
| Developer | Recruit ≥ min testers quickly, keep them for full period, get feedback | Drop-outs reset clock | Campaign fills to `min_testers` within 5 days median |
| Admin | Keep marketplace trustworthy and solvent | Fraud, disputes, payout errors | Payout failure rate < 2 %; disputes resolved ≤ 5 business days |

### 4.1 Permission matrix
Legend: ✅ allowed · 🔸 own records only · ❌ denied.

| Capability | Guest | Tester | Developer | Admin |
|---|---|---|---|---|
| View landing, legal pages | ✅ | ✅ | ✅ | ✅ |
| View public campaign listing (no opt-in link) | ✅ | ✅ | ✅ | ✅ |
| Manage own profile, PayPal email | ❌ | 🔸 | 🔸 | 🔸 |
| Manage tester store identities | ❌ | 🔸 | ❌ | ❌ |
| Enrol / withdraw / check in | ❌ | 🔸 (not own campaigns) | ❌ | ❌ |
| View opt-in link & instructions | ❌ | 🔸 enrolled only | 🔸 own campaign | ✅ |
| Create/edit/pay/cancel campaign | ❌ | ❌ | 🔸 | ✅ (cancel only) |
| View roster incl. tester store emails, proofs, feedback | ❌ | ❌ | 🔸 own campaign | ✅ |
| Mark access granted, start testing, give verdicts | ❌ | ❌ | 🔸 | ❌ |
| Open dispute | ❌ | 🔸 own failed/dropped enrollment | ❌ | ❌ |
| Wallet, request payout | ❌ | 🔸 | ❌ | ❌ |
| Approve/reject campaigns, resolve disputes, approve payouts, suspend users, settings, audit log | ❌ | ❌ | ❌ | ✅ |
| Grant/revoke admin role | ❌ | ❌ | ❌ | ✅ (not self-revoke last admin) |

Suspended users: can sign in and view own data only; all mutations except account deletion request are denied.

## 5. Goals and metrics
| Metric | Definition | Target (ASSUMPTION A-021) | Source |
|---|---|---|---|
| North star: completed tests / month | Count of enrollments transitioning to `passed` per calendar month (Asia/Manila) | 500 by month 6 | `enrollments` |
| Campaign fill rate | Campaigns reaching `min_testers` active within recruiting window ÷ published campaigns | ≥ 85 % | `campaigns`, `enrollments` |
| Tester completion rate | `passed` ÷ (enrollments that were `active` at testing start) | ≥ 80 % | `enrollments` |
| Time-to-publish | Median `published_at − paid_at` | ≤ 24 h | `campaigns`, `campaign_payments` |
| Payout success rate | `paid` ÷ payouts submitted to PayPal | ≥ 98 % | `payouts` |
| Dispute rate | Disputes ÷ verdicts of `fail` + drops | tracked, no target | `disputes` |
| Fraud flags | Duplicate-proof flags per 100 check-ins | tracked | `checkins` |

## 6. Scope and prioritisation
| Release | Contents | Rationale |
|---|---|---|
| **MVP (R1)** | FR-001…FR-033, NFR-001…NFR-014 | End-to-end money loop is the product; partial loops are not shippable |
| R2 | Tester reputation score, developer ratings of testers, Play Developer API verification, membership gating (OD-006), referral codes | Trust & growth after real usage data |
| R3 | Multi-currency, local payouts (GCash/Maya), PWA push notifications, developer subscriptions | Market expansion |
| **Excluded** | Native apps, in-app chat, paid reviews/ratings (forbidden by policy), app hosting/distribution of APK/IPA files, automated device verification | Policy, scope, risk |

Priority scale: **P0** = MVP blocker, **P1** = MVP but may slip to R1.1 with owner approval, **P2** = future.

## 7. Epics, user stories and functional requirements

### Epic A — Accounts and identities

**US-A1** As a guest I want to sign up with email and password so I can join as tester or developer. Preconditions: not signed in. Trigger: "Sign up". Steps: enter email, password, display name, confirm 18+, accept Terms/Privacy/Tester Rules → verification email → click link → onboarding (choose roles). Alternates: email already registered (generic message, no enumeration), weak password, link expired (resend), email provider outage (retry later message).

**FR-001 Sign-up, sign-in, sign-out, password reset** — P0
- Email + password (min 10 chars, checked against breached-password list if Supabase setting available — else length + complexity), mandatory email verification, 18+ attestation, Terms acceptance with `terms_version`.
- AC1: *Given* a new email, *when* the guest submits valid sign-up data, *then* an unverified account is created, a verification email is sent, and the UI shows "Check your inbox" without revealing whether the email already existed.
- AC2: *Given* an unverified account, *when* the user tries to sign in, *then* sign-in is refused with "Verify your email" and a resend action (rate-limited 3/hour).
- AC3: *Given* a verified user, *when* they sign out, *then* the session cookie is cleared server-side and protected pages redirect to UI-003.
- AC4: *Given* a password-reset request for any email, *then* the response is identical whether or not the account exists; reset links expire per Supabase setting (default 1 h).
- AC5: 5 failed sign-ins per email per 15 min → further attempts throttled with HTTP 429 (NFR-011).
- Deps: none. Links: FLOW-001, FLOW-002, UI-002…UI-005, API-001.

**FR-002 Role onboarding** — P0
- After first sign-in the user selects Tester and/or Developer (at least one). Roles can be added later from settings. Admin role only via admin (FR-025).
- AC1: *Given* a verified user without roles, *when* they open any app page, *then* they are redirected to UI-005 until ≥ 1 role is chosen.
- AC2: *Given* a user submits role `admin` via API, *then* API returns 403 `FORBIDDEN_ROLE`.
- Links: FLOW-001, UI-005, API-002, DB-001, DB-002.

**FR-003 Tester store identities** — P0
- Tester registers up to one active identity per platform: Android = Google account email (any domain allowed, since Google accounts can use non-Gmail addresses); iOS = Apple ID email.
- An identity email is unique per platform across all non-deleted users.
- Identity cannot be edited/removed while used by an open enrollment (statuses applied, access_granted, active, awaiting_verdict).
- AC1: *Given* tester enters `mika@gmail.com` for Android, *when* another user already registered it for Android, *then* the API returns 409 `IDENTITY_TAKEN` and the UI asks them to contact support.
- AC2: *Given* an identity in an open enrollment, *when* tester tries to delete it, *then* 409 `IDENTITY_IN_USE`.
- Links: FLOW-003, UI-006, API-003, DB-003.

**FR-004 Payout profile (PayPal email)** — P0
- Tester sets a PayPal receiver email; unique across non-deleted users. Changing it requires the current password re-entry (re-auth) and starts a 48 h payout hold (A-019); an email notification goes to the account email.
- AC1: *Given* PayPal email changed at T, *when* tester requests payout before T+48h, *then* 409 `PAYOUT_EMAIL_HOLD` with the unlock time.
- AC2: duplicate PayPal email → 409 `PAYPAL_EMAIL_TAKEN`; event logged to audit log for fraud review.
- Links: FLOW-003, UI-006, API-002, DB-001.

### Epic B — Developer campaigns

**US-B1** As a developer I want to post my app's closed test and pay once so community testers can join.

**FR-005 Create and edit draft campaign** — P0
- Fields: platform (`android`|`ios`), app name (2–60), package name / bundle ID (reverse-DNS regex), short description (10–140), description (≤4,000), icon (PNG/JPEG/WebP ≤1 MB; square ≥ 128 px recommended, not enforced), opt-in URL, testing instructions (≤4,000), tester slots, duration days. Android opt-in URL must match `https://play.google.com/apps/testing/<package_name>` **or** a Google Groups URL `https://groups.google.com/g/<name>`; iOS opt-in URL optional, if present must match `https://testflight.apple.com/join/<code>`.
- Slots: between platform `min_testers` and 100. Duration: Android 14–30 (default 16), iOS 7–30 (default 14).
- Editable only in `draft`; after payment only description/instructions/icon may change and require no re-review (ASSUMPTION). Platform, package, opt-in URL, slots and duration are locked after draft (`CAMPAIGN_LOCKED`). An in-app opt-in-URL change workflow is **R2**; in MVP a developer whose link must change contacts the admin, who can cancel the campaign before testing (full refund) so it can be re-created.
- AC1: *Given* platform android and package `com.example.app`, *when* opt-in URL is `https://play.google.com/apps/testing/com.other.app`, *then* 422 `OPT_IN_URL_MISMATCH`.
- AC2: *Given* status ≠ draft, *when* developer edits slots/duration/platform/package, *then* 409 `CAMPAIGN_LOCKED`.
- Links: FLOW-004, UI-013, API-004, DB-004, DB-018.

**FR-006 Server-side quote** — P0
- Quote = `tester_slots × price_per_slot_cents`; `tester_reward_cents` and `price_per_slot_cents` are snapshotted onto the campaign at checkout creation from `platform_settings` (A-003). Client-provided prices are ignored.
- AC1: *Given* slots 15 and price 500, *then* total 7,500 cents displayed as "US$75.00" and charged exactly.
- AC2: *Given* admin changes price after a campaign's checkout is created, *then* that campaign keeps its snapshot.
- Links: UI-013, API-004, API-005, DB-004, DB-015.

**FR-007 Pay via Stripe Checkout** — P0
- Developer clicks Pay → server creates a Stripe Checkout Session (mode `payment`, USD, single line item, metadata `campaign_id`, idempotency key) → campaign `pending_payment` → redirect to Stripe → webhook `checkout.session.completed` with `payment_status=paid` (or `async_payment_succeeded`) marks payment `paid`, campaign `pending_review`.
- The success page never marks payment as paid by itself; it polls status (UI-014).
- Session expiry (24 h) or `checkout.session.expired` → payment `expired`, campaign back to `draft`.
- AC1: duplicate webhook delivery → processed exactly once (unique `webhook_events(provider,event_id)`).
- AC2: webhook amount ≠ snapshot total → payment flagged `failed`, admin alerted, campaign not advanced.
- AC3: *Given* developer cancels on Stripe page, *then* UI-014 cancel state shows "Payment not completed" and campaign remains `pending_payment` with "Pay again" (re-uses open session if not expired).
- Links: FLOW-004, UI-013, UI-014, API-005, API-006, DB-005, DB-014.

**FR-008 Admin campaign review** — P0
- Admin sees `pending_review` queue; approves → `recruiting`, `published_at=now`, `recruiting_ends_at=now+10d` (A-010); rejects with reason → `rejected` + full refund (FR-013 refund engine) + notification.
- Review checklist: opt-in URL format & reachable (manual), app name not misleading, no prohibited content (gambling, adult, malware, impersonation), developer not suspended.
- AC1: rejection without reason → 422.
- AC2: approval notifies all users with Tester role who opted into "new campaign" emails (default on) — sent in batches by JOB-007.
- Links: FLOW-005, UI-019, API-016, DB-004, DB-006, DB-013.

**FR-009 Recruiting and listing** — P0
- Campaign in `recruiting` appears on UI-007 with platform, app name, icon, short description, reward per tester, duration, slots remaining, recruiting deadline.
- Slots remaining = `tester_slots − count(enrollments in applied|access_granted|active)`.
- AC1: when slots remaining = 0 the Join button is disabled ("Full — check back, slots reopen if testers withdraw").
- AC2: listing never exposes `opt_in_url`, `testing_instructions`, developer email.
- Links: FLOW-006, UI-007, UI-008, API-007, DB-004, DB-007.

**FR-010 Roster and access granting** — P0
- Developer sees roster (UI-015): tester display name, platform store email, status, opt-in proof thumbnail, timestamps. Export CSV of store emails for status `applied` (for pasting into Play Console / App Store Connect / Google Group). Developer marks selected testers `access_granted` (bulk). Developer may remove an `applied`/`access_granted` tester before testing starts (status `released`, reason required).
- AC1: CSV contains only emails of the developer's own campaign; download is audit-logged.
- AC2: marking access for an enrollment not in `applied` → skipped and reported in response `skipped[]`.
- Links: FLOW-007, UI-015, API-009, DB-007, DB-013.

**FR-011 Start testing** — P0
- Allowed when status `recruiting` and `active` enrollments ≥ `min_testers`. On start: `testing_started_at=now`, `testing_ends_at=now+duration_days`, `review_ends_at=testing_ends_at+3d`; enrollments not `active` become `released` (notified); check-in schedule generated (FR-018). Campaign → `testing`; listing hides it.
- AC1: active < min_testers → 409 `NOT_ENOUGH_ACTIVE_TESTERS` with counts.
- AC2: double-click/duplicate request → single transition (row lock + status guard), second call returns 409 `INVALID_STATE`.
- Links: FLOW-007, UI-015, API-010, DB-004, DB-007, DB-008.

**FR-012 Developer verdicts** — P0
- During `developer_review` (testing_ends_at → review_ends_at), developer sets each `awaiting_verdict` enrollment to pass or fail; fail requires a reason (20–500 chars) and is only allowed if the tester's final check-in is `submitted` or `flagged` (otherwise the enrollment would already be `dropped`). At `review_ends_at`, remaining `awaiting_verdict` → auto-pass (`auto_passed=true`).
- Passing credits the reward immediately (FR-021).
- AC1: *Given* no verdict by deadline, *then* JOB-002 passes the tester and credits reward exactly once.
- AC2: verdict changes after being set → 409 `VERDICT_FINAL` (admin can override only via dispute).
- Links: FLOW-009, UI-016, API-012, DB-007, DB-010.

**FR-013 Settlement and refunds** — P0
- Campaign completes when `now ≥ review_ends_at + dispute_window` and no `open` disputes. Settlement computes refund `= (tester_slots − passed_count) × tester_reward_cents` (A-011) and issues a Stripe refund against the original PaymentIntent with idempotency key `refund:<payment_id>:settlement`. Campaign → `completed`.
- Refund engine also handles: admin rejection (full), developer cancel / recruiting expiry (full).
- AC1: refund amount 0 → no Stripe call; refund row not created.
- AC2: Stripe refund failure → refund `failed`, JOB-006 retries up to 5 times with backoff, then alerts admin; campaign still `completed`.
- Links: FLOW-011, FLOW-013, API-021, DB-004, DB-005, DB-006.

**FR-014 Cancellation** — P0
- Developer may cancel in `draft` (no money), `pending_payment` (expires Stripe session), `pending_review` or `recruiting` (full refund; enrolled testers released and notified). Not allowed in `testing` or later (admin only, with reason; refund per A-011 rules computed by admin at override — P1).
- Recruiting expiry (JOB-002) → `cancelled`, reason `recruiting_expired`, full refund.
- Links: FLOW-013, UI-012, UI-015, API-024, DB-004, DB-006.

### Epic C — Testing

**FR-015 Browse campaigns** — P0. Filter by platform; sort newest / closing soon. Paginated 20/page (cursor). Guests see listing; Join prompts sign-in. Links: UI-007, UI-008, API-007.

**FR-016 Join campaign** — P0
- Preconditions: Tester role, status `active`, verified identity for the campaign platform, not campaign owner, < 10 open enrollments (A-024), slot available, not previously enrolled in this campaign (any status).
- Enrollment snapshot: `store_email`, `reward_cents`. Status `applied`. Developer notified (digest).
- AC1: two testers race for the last slot → exactly one succeeds; the other gets 409 `CAMPAIGN_FULL`.
- AC2: tester with no Android identity joining Android campaign → 422 `IDENTITY_REQUIRED` and UI links to UI-006.
- AC3: tester can withdraw while `applied`/`access_granted`/`active` and campaign `recruiting` → `withdrawn`, slot reopens.
- Links: FLOW-006, UI-008, UI-009, API-008, DB-007.

**FR-017 Opt-in and activation** — P0
- After `access_granted`, tester sees opt-in URL + instructions (UI-010) and must upload an **opt-in proof** screenshot (e.g., Play "You're a tester" page or TestFlight app showing the app) → check-in kind `opt_in` submitted → enrollment `active`.
- AC1: upload before `access_granted` → 409 `ACCESS_NOT_GRANTED`.
- AC2: invalid file type/size → 422 `INVALID_FILE`; nothing stored.
- Links: FLOW-008, UI-010, API-011, DB-008, DB-017.

**FR-018 Periodic and final check-ins** — P0
- At testing start, for each active enrollment generate periodic check-ins due at `start + k×4d` for k ≥ 1 while `< testing_ends_at`, plus a final check-in due at `testing_ends_at` (A-007). Submission window: opens 24 h before `due_at` (final: 48 h before), closes at `grace_ends_at` (periodic `due_at+48h`, final `due_at+24h`).
- Each submission: screenshot proof (app installed / still a tester) + feedback 20–1,000 chars (A-023).
- Reminders: email + in-app at window open and 12 h before grace end.
- Missed (grace passed, not submitted) → check-in `missed`, enrollment `dropped` (`drop_reason='missed_checkin'`), developer notified, the enrollment's remaining `due` check-ins are set to `cancelled`.
- When testing ends, `active` enrollments → `awaiting_verdict`.
- AC1 (16-day Android): check-ins due on days 4, 8, 12 (periodic) and 16 (final).
- AC2: submitting outside the window → 409 `CHECKIN_WINDOW_CLOSED` / `CHECKIN_NOT_OPEN`.
- AC3: same image (SHA-256) previously used by a **different** tester → check-in accepted but `flagged` with reason `duplicate_proof`, admin + developer notified (FR-026).
- Links: FLOW-008, UI-009, UI-010, API-011, API-021, DB-008.

**FR-019 Withdraw** — P0. Before testing start → `withdrawn` (no penalty). During testing → `dropped` with `drop_reason='tester_withdrew'`, no reward, no dispute. Confirmation dialog required. Links: FLOW-006, FLOW-008, UI-010, API-008.

### Epic D — Earnings and payouts

**FR-020 Wallet** — P0. Shows available, pending (held) balances, open payout, ledger history (date, type, campaign, amount). Available = Σ ledger amounts with `available_at ≤ now`; pending = Σ positive amounts with `available_at > now`. Links: UI-011, API-014, DB-010.

**FR-021 Reward crediting** — P0. On enrollment → `passed` insert one `reward` ledger entry (`amount = reward_cents`, `available_at = now + 3d`, A-006). Unique per enrollment. Tester notified. AC: two concurrent pass operations → one ledger row. Links: FLOW-009, FLOW-010, DB-010.

**FR-022 Payout request** — P0
- Preconditions: Tester role, account `active`, PayPal email set and not in 48 h hold, no open payout (`requested|processing|unclaimed`), available ≥ 2,500 cents (C-007).
- Amount: tester chooses ≥ 2,500 and ≤ available (default = full available). Creates payout `requested` and a `payout_hold` ledger debit atomically.
- Tester can cancel while `requested` → `cancelled` + `payout_release` credit.
- AC1: available 2,499 → 422 `BELOW_MINIMUM_PAYOUT`.
- AC2: two concurrent requests → one succeeds, other 409 `PAYOUT_ALREADY_OPEN`.
- Links: FLOW-012, UI-011, API-015, DB-010, DB-011.

**FR-023 Payout execution (PayPal Payouts)** — P0
- Admin reviews `requested` payouts (fraud signals displayed: flags, account age, duplicate proofs, disputes) and approves a batch (≤ 500 items) or rejects individual payouts with reason (→ `rejected` + `payout_release`).
- Approval sends one PayPal Payouts batch (`sender_batch_id` = generated UUID stored), items `recipient_type=EMAIL`, `amount.currency=USD`, `sender_item_id=payout.id`; payouts → `processing`.
- Webhooks `PAYMENT.PAYOUTS-ITEM.SUCCEEDED` → `paid`; `.UNCLAIMED` → `unclaimed`; `.RETURNED` / `.FAILED` / `.BLOCKED` / `.REFUNDED` / `.DENIED` → `returned`/`failed` + `payout_release` credit; tester notified to fix PayPal email. JOB-004 polls items stuck in `processing` > 6 h.
- AC1: PayPal API 5xx/timeout on batch creation → payouts stay `requested`, admin sees error; retry uses same `sender_batch_id` (PayPal rejects duplicates → treat as already submitted and reconcile).
- AC2: release credit is created once per payout (unique `(payout_id, entry_type)`).
- Links: FLOW-012, UI-021, API-017, API-018, DB-011, DB-010, DB-014.

### Epic E — Trust, disputes, moderation

**FR-024 Disputes** — P0. Tester can open one dispute per enrollment within 3 days of `failed` or `dropped` (`missed_checkin` only) with reason 20–1,000 chars. Admin sees proofs, feedback, developer reason; resolves `upheld` (enrollment → `passed`, reward credited) or `rejected`. Both parties notified. Settlement waits for open disputes. Links: FLOW-010, UI-010, UI-020, API-013, DB-009.

**FR-025 User moderation** — P0. Admin suspends/reinstates users with reason; suspension: blocks new enrollments, check-ins continue? → **No**: suspended testers' open enrollments are `dropped` (`drop_reason='suspended'`); open `requested` payouts are rejected and released; developer campaigns in `pending_review`/`recruiting` are cancelled with refund (admin confirms). Admin can grant/revoke admin role (cannot remove last admin). Links: FLOW-014, UI-022, API-019, DB-001, DB-002, DB-013.

**FR-026 Fraud controls** — P0. Unique store emails per platform; unique PayPal email; duplicate proof hash flagging; per-user rate limits (NFR-011); max 10 open enrollments; admin view of fraud signals on payouts; audit of CSV exports, payout approvals, suspensions, settings changes. Links: DB-003, DB-001, DB-008, DB-016, UI-021.

### Epic F — Notifications, admin, privacy

**FR-027 Notifications** — P0. In-app (UI-017) + email for events in §8. "New campaign" emails can be turned off in UI-006 (link in each such email; one-click tokenised unsubscribe is R2); transactional emails (payout, check-in reminders, verdicts) cannot be disabled except by account deletion. Links: API-022, DB-012.

**FR-028 Admin console** — P0. Overview counts (pending reviews, open disputes, requested payouts, failed refunds, flagged check-ins, webhook failures). Links: UI-018…UI-024, API-025.

**FR-029 Platform settings** — P0. Admin edits keys in DB-015 with validation (e.g., reward < price; min payout ≥ 100). Changes affect only campaigns whose checkout is created afterwards. Audit-logged. Links: UI-023, API-020.

**FR-030 Audit log** — P0. Immutable log of security- and money-relevant actions (§8.2). Admin read-only view with filters. Links: UI-024, API-025, DB-013.

**FR-031 Account deletion** — P1. User requests deletion (UI-006): blocked with 409 `DELETION_BLOCKED` while any open enrollment, open campaign (not completed/cancelled/rejected), open payout, or available balance > 0 (tester must withdraw first or explicitly forfeit balance < US$25 with confirmation). On deletion: profile anonymised, identities and PayPal email removed, proofs deleted, auth user banned and email scrambled; ledger/payout/payment rows retained for finance (NFR-012). Links: FLOW-015, API-023, DB-001.

**FR-032 Policies and disclosures** — P0. Terms of Service, Privacy Notice, Tester Rules (no paid reviews or ratings, no sharing of builds, keep app installed, honest feedback), Developer Rules (own the app, no malware, no requests for reviews), and disclaimer: "TestKo PH does not guarantee Google Play production access or App Store approval." Version accepted stored on profile; re-acceptance prompted on version change. Legal text requires counsel (OD-003). Links: UI-026, UI-005, DB-001.

**FR-033 Platform rules** — P0. Android: min testers 12 (A-002), duration 14–30 default 16, opt-in URL formats per FR-005. iOS: min testers 3, duration 7–30 default 14, TestFlight public link optional (developer may invite by email). Values come from DB-015. Links: FR-005, FR-011, DB-015.

## 8. Notifications and events
### 8.1 Notification matrix
| Event | Recipient | In-app | Email |
|---|---|---|---|
| Account verification / password reset | User | — | ✅ (Supabase Auth) |
| Payment confirmed, campaign under review | Developer | ✅ | ✅ |
| Campaign approved / rejected (+refund) | Developer | ✅ | ✅ |
| New campaign published | Testers (opt-in pref) | ✅ | ✅ batched |
| Tester applied (daily digest) | Developer | ✅ | ✅ digest |
| Access granted — opt in now | Tester | ✅ | ✅ |
| Released / removed from campaign | Tester | ✅ | ✅ |
| Testing started | Developer, active testers | ✅ | ✅ |
| Check-in window open / 12 h before grace end | Tester | ✅ | ✅ |
| Check-in missed → dropped | Tester, Developer | ✅ | ✅ |
| Duplicate proof flagged | Admin, Developer | ✅ | — |
| Testing ended — review now | Developer | ✅ | ✅ |
| Verdict pass/fail, auto-pass | Tester | ✅ | ✅ |
| Dispute opened / resolved | Admin / both parties | ✅ | ✅ |
| Campaign completed + refund amount | Developer | ✅ | ✅ |
| Reward available | Tester | ✅ | — |
| Payout requested / paid / failed / unclaimed / rejected | Tester | ✅ | ✅ |
| PayPal email changed | Tester (account email) | ✅ | ✅ |
| Webhook/refund/payout job failure | Admin | ✅ | ✅ |

### 8.2 Audit events (DB-013 `action`)
`auth.role_granted`, `auth.role_revoked`, `profile.paypal_email_changed`, `campaign.created`, `campaign.paid`, `campaign.approved`, `campaign.rejected`, `campaign.cancelled`, `campaign.started`, `campaign.completed`, `campaign.roster_exported`, `enrollment.access_granted`, `enrollment.released`, `enrollment.verdict`, `enrollment.auto_passed`, `checkin.flagged`, `dispute.opened`, `dispute.resolved`, `ledger.adjustment`, `payout.requested`, `payout.cancelled`, `payout.approved`, `payout.rejected`, `payout.status_changed`, `refund.created`, `refund.failed`, `user.suspended`, `user.reinstated`, `user.deleted`, `settings.updated`.

## 9. Non-functional requirements
| ID | Category | Requirement | Target / verification | Status |
|---|---|---|---|---|
| NFR-001 | Security | Deny-by-default RLS on every table; clients have SELECT-only policies; all writes via server route handlers calling service-role DB functions; OWASP ASVS L2 controls for auth/session/input. | pgTAP RLS suite passes; ZAP baseline scan has no High findings | ASSUMPTION |
| NFR-002 | Payment integrity | Integer cents; idempotent webhooks; append-only ledger (UPDATE/DELETE blocked by trigger); daily reconciliation report of Stripe payments vs campaigns and PayPal items vs payouts. | Reconciliation job zero unexplained diffs; tests for duplicate webhooks | ASSUMPTION |
| NFR-003 | Privacy | Collect minimum PII; store emails visible only to the enrolled campaign's developer and admins; proofs in private bucket via signed URLs (TTL 120 s); privacy notice aligned with PH Data Privacy Act (counsel review OD-003). | RLS tests; manual privacy review | OPEN |
| NFR-004 | Availability | 99.5 % monthly for web + API (excl. provider outages). | Uptime monitor | ASSUMPTION A-021 |
| NFR-005 | Performance | p95 server response < 500 ms for API-007/008/011(without upload)/014 at 50 req/s; LCP < 2.5 s on 4G mid-range Android for UI-007. | k6 load test, Lighthouse CI | ASSUMPTION |
| NFR-006 | Accessibility | WCAG 2.2 AA for all UI; keyboard-operable; visible focus; form errors announced. | axe-core in Playwright = 0 serious/critical | ASSUMPTION |
| NFR-007 | Observability | Structured JSON logs with request id; Sentry for errors; alerts on webhook processing failure, refund failure, payout failure, cron job not run within 2 h. | Alert test in staging | ASSUMPTION |
| NFR-008 | Backup / recovery | Supabase daily backups (PITR if plan allows); RPO 24 h (≤ 5 min with PITR), RTO 4 h; quarterly restore drill. | Restore drill record | ASSUMPTION |
| NFR-009 | Localisation | English; Asia/Manila display; USD formatting `US$1,234.56`. | UI tests | ASSUMPTION A-017 |
| NFR-010 | Compatibility | Responsive 320–1440 px; last 2 versions evergreen browsers; iOS Safari 16+. | Playwright projects chromium/webkit/mobile | ASSUMPTION |
| NFR-011 | Abuse / rate limiting | Per-IP and per-user limits: auth 5/15 min/email; enrol 20/h/user; check-in upload 10/h/user; payout request 5/day/user; API general 120/min/user. | Integration tests for 429 | ASSUMPTION |
| NFR-012 | Retention | Proof files deleted 90 days after campaign completion; notifications 180 days; audit logs 5 years; payments/ledger/payouts ≥ 5 years (OD-004). | JOB-005 tests | ASSUMPTION A-020 |
| NFR-013 | Scale | 10k users, 200 concurrent campaigns, 5k active enrollments, 2k check-ins/day without schema change. | Load test + index review | ASSUMPTION |
| NFR-014 | Email deliverability | SPF, DKIM, DMARC configured for sending domain; bounce handling logs. | DNS check at release | ASSUMPTION |

## 10. Integrations
| Integration | Purpose | Notes |
|---|---|---|
| Stripe Checkout, Refunds, Webhooks | Collect developer payments, refund unearned amounts | Account country/entity unresolved (OD-001) |
| PayPal Payouts REST + Webhooks | Pay testers | Requires Payouts enablement on PayPal Business (OD-002) |
| Supabase Auth / Postgres / Storage | Identity, data, files | Singapore region |
| Resend | Transactional email + Auth SMTP | A-015 |
| Sentry | Error tracking | |
| Google Play Console / App Store Connect | **No API integration** in MVP; developer manually adds tester emails | R2 candidate |

## 11. Edge cases and abuse cases
| # | Case | Handling |
|---|---|---|
| E-01 | Last-slot race | Row-locked enrol function (FR-016 AC1) |
| E-02 | Developer never grants access | Recruiting expiry cancels + full refund (A-010); testers released |
| E-03 | Developer never reviews | Auto-pass (FR-012) |
| E-04 | Developer fails everyone to avoid paying | Fail needs reason; disputes; admin sees pattern (fail rate shown on UI-019/UI-020); suspension |
| E-05 | Tester uses same screenshot for multiple accounts | SHA-256 duplicate flag (FR-026) |
| E-06 | Tester creates multiple accounts | Unique store email per platform, unique PayPal email, admin review before payout |
| E-07 | Stripe chargeback after rewards credited | `charge.dispute.created` → admin alert, developer flagged; platform bears loss in MVP (risk R-03) |
| E-08 | PayPal email wrong / unclaimed | Unclaimed after PayPal hold → returned → ledger release credit; tester notified |
| E-09 | Webhook arrives before checkout session row committed | Handler upserts by session id; retries via Stripe's retry schedule return 500 until resolvable |
| E-10 | Opt-in URL must change after publication | Locked in MVP; admin cancels before testing (full refund) and developer re-creates; in-app change workflow is R2 |
| E-11 | Time zone confusion on due dates | All due dates shown with absolute Manila time + relative countdown |
| E-12 | Tester asked by developer to leave a rating | Forbidden by Developer Rules; report button → admin (P1: report form on UI-010) |
| E-13 | Developer deletes app from Play Console mid-test | Testers report via check-in feedback; admin can cancel campaign with partial refund manually (P1) |
| E-14 | Admin approves payout twice | Payout status guard + PayPal `sender_item_id` uniqueness |
| E-15 | Clock drift between jobs | Jobs compare against DB `now()`, idempotent transitions |

## 12. Constraints and risks
| ID | Risk | Likelihood / impact | Mitigation | Owner |
|---|---|---|---|---|
| R-01 | Stripe may not onboard a PH-based business (OD-001) | High / High | Decide entity (e.g., entity in Stripe-supported country) before go-live; dev uses test mode | Owner |
| R-02 | PayPal Payouts not enabled / account limited | Medium / High | Apply early (OD-002); fallback manual PayPal sends recorded in admin (P1) | Owner |
| R-03 | Chargebacks after payouts | Medium / Medium | 3-day hold, admin review of payouts, Stripe Radar default rules | Owner |
| R-04 | Google/Apple policy treats paid testing negatively; Google may reject production access despite test | Medium / High | Disclaimer FR-032; forbid incentivised reviews; legal review OD-003 | Owner |
| R-05 | Tax/regulatory obligations on payouts (OD-004) | Medium / High | Accountant review before go-live | Owner |
| R-06 | Fraudulent testers faking proofs | High / Medium | Proof flags, developer verdicts, admin review, suspension | Admin |
| R-07 | Single admin bottleneck | Medium / Medium | Queues + SLA targets; R2 automation | Owner |
| R-08 | Use of "IT Philippines" name/brand | Unknown | OD-007 | Owner |

## 13. Open decisions
See `DECISIONS.md` §Open decisions OD-001…OD-008. **Production release is blocked by OD-001, OD-002, OD-003, OD-004.** Development and staging (test-mode Stripe, PayPal sandbox) are not blocked.

## 14. Acceptance checklist (PRD level)
- [ ] Owner approves pricing (A-003/OD-005) and timing assumptions (A-001, A-006…A-010).
- [ ] Every P0 FR has GWT acceptance criteria and mapped flows/screens/APIs/tables/tasks/tests (TRACEABILITY.md).
- [ ] Legal texts drafted and reviewed (OD-003).
- [ ] Payment provider accounts approved (OD-001, OD-002).

## 15. Glossary
| Term | Meaning |
|---|---|
| Campaign | One developer's closed-test request for one app on one platform |
| Slot | One paid tester seat in a campaign |
| Enrollment | A tester's participation in a campaign |
| Store identity | Tester's Google account email (Android) or Apple ID email (iOS) |
| Check-in | Proof screenshot (+ feedback) submitted by a tester at a scheduled time |
| Verdict | Developer's pass/fail for an enrollment after testing |
| Reward | Amount credited to a tester for a passed enrollment |
| Ledger | Append-only record of tester balance movements |
| Payout | Transfer of available balance to tester's PayPal |
| Settlement | Campaign completion: refund of unearned rewards |
