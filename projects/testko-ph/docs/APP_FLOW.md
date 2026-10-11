# APP_FLOW — TestKo PH Application Flows

## 0. Document control
| Field | Value |
|---|---|
| Document | `APP_FLOW.md` (03) |
| Version | 0.3.0 · draft |
| Date | 2026-10-11 |
| Upstream | PRD 0.2.0, TRD 0.2.0 |
| Downstream | DESIGN_BRIEF, DATABASE_SCHEMA, IMPLEMENTATION_PLAN |

## 1. Conventions
- **Swimlanes are horizontal:** each **row is a lane** (a user role or a system), and the flow reads **left to right** with arrows.
  - Shapes: green pill = start/end · white box = step · amber diamond = decision · red box = error/alternate outcome.
  - Solid arrow = next step; **dashed arrow = go back / retry**; arrow labels give the decision answer.
  - Numbered badges give the reading order.
- Diagrams are images in `docs/diagrams/FLOW-###.svg`, generated from the diagram data `docs/diagrams/flows.json` by the EC2Build agent tool (`skills/ec2build/scripts/swimlanes.py`, bundled with the ec2build skill). Under each image a generated Mermaid text version (lanes as `subgraph`s) is kept for diffing and for tools that only read Mermaid.
- **To change a flow diagram**, use `/ec2build update --name "TestKo PH" --doc FLOW --change "..."` (the agent edits `flows.json` and re-renders); never hand-edit the SVGs or the text between `<!-- swimlane:... -->` markers.
- Standard failure handling that applies to **every** flow (not repeated in each diagram unless flow-specific):
  | Condition | Behaviour |
  |---|---|
  | **Unauthenticated** (no/expired session) | API 401 `UNAUTHENTICATED`; UI redirects to UI-003 with `?next=<path>`; after login returns to the step |
  | **Forbidden** (wrong role/owner) | API 403; UI shows UI-025 403 state with link home; event logged (warn) |
  | **Suspended** | API 403 `ACCOUNT_SUSPENDED` on mutations; banner on all pages |
  | **Validation error** | API 422 with field `details`; UI keeps input, shows inline errors, focuses first invalid field, announces summary (aria-live) |
  | **Timeout / network offline** | Client fetch timeout 15 s → toast "Connection problem — your data wasn't lost" + Retry; forms keep state; mutations are safe to retry (state guards / idempotency) |
  | **Service unavailable** (DB/provider 5xx) | API 502/503 `PROVIDER_UNAVAILABLE`/`INTERNAL`; UI shows retry with backoff; no partial money state (single DB transaction) |
  | **Duplicate submission** | Submit buttons disabled while pending; server guards (status checks, unique indexes) make repeats no-ops or 409 `INVALID_STATE` which UI treats as "already done" and refreshes |
  | **Rate limited** | 429 + `Retry-After`; UI shows wait time |
- Offline-first behaviour is out of scope (PROJECT_CONTEXT §6); reconnect = user retries.

## 2. Flow index
| Flow | Name | Actors | FR | UI | API |
|---|---|---|---|---|---|
| FLOW-001 | Sign-up, verification & onboarding | Guest | FR-001, FR-002, FR-032 | UI-002, UI-005 | API-001, API-002 |
| FLOW-002 | Sign-in, sign-out & password reset | User | FR-001 | UI-003, UI-004 | API-001 |
| FLOW-003 | Tester identity & PayPal profile setup | Tester | FR-003, FR-004 | UI-006 | API-002, API-003 |
| FLOW-004 | Create campaign & pay | Developer, Stripe | FR-005…FR-007 | UI-012…UI-014 | API-004, API-005, API-006 |
| FLOW-005 | Admin campaign review | Admin, Stripe | FR-008, FR-013 | UI-019 | API-016 |
| FLOW-006 | Browse & join campaign / withdraw before start | Tester | FR-009, FR-015, FR-016, FR-019 | UI-007, UI-008, UI-009 | API-007, API-008 |
| FLOW-007 | Grant access & start testing | Developer | FR-010, FR-011 | UI-015 | API-009, API-010 |
| FLOW-008 | Opt-in proof & periodic/final check-ins | Tester, Cron | FR-017, FR-018, FR-019, FR-026 | UI-009, UI-010 | API-011, API-021 |
| FLOW-009 | Developer verdicts & auto-pass | Developer, Cron | FR-012, FR-021 | UI-016 | API-012, API-021 |
| FLOW-010 | Dispute | Tester, Admin | FR-024 | UI-010, UI-020 | API-013 |
| FLOW-011 | Settlement & refund | Cron, Stripe | FR-013 | UI-015 | API-021, API-006 |
| FLOW-012 | Payout request & PayPal execution | Tester, Admin, PayPal | FR-020…FR-023 | UI-011, UI-021 | API-014, API-015, API-017, API-018 |
| FLOW-013 | Campaign cancellation & recruiting expiry | Developer, Cron, Stripe | FR-014 | UI-012, UI-015 | API-024, API-021 |
| FLOW-014 | Admin suspension | Admin | FR-025 | UI-022 | API-019 |
| FLOW-015 | Account deletion | User | FR-031 | UI-006 | API-023 |

---

## FLOW-001 — Sign-up, verification & onboarding
| Field | Value |
|---|---|
| Trigger | Guest clicks "Join as tester" / "Post your app" on UI-001 or "Sign up" anywhere |
| Actors | Guest → User |
| Preconditions | Not signed in |
| Entry / exit | UI-002 → UI-005 → role home (tester: UI-007; developer: UI-012) |
| Links | FR-001, FR-002, FR-032 · UI-002, UI-005 · API-001, API-002 · DB-001, DB-002 |

<!-- swimlane:FLOW-001 -->
**Sign-up, verification & onboarding**

![FLOW-001 Sign-up, verification & onboarding — horizontal swimlane](diagrams/FLOW-001.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_g["Guest / User"]
    direction LR
    g1(["Open Sign up"])
    g2["Enter name, email, password; tick 18+ and Terms"]
    g3["Click link in email"]
    g4["Choose Tester and/or Developer"]
  end
  subgraph L_ui["Web UI"]
    direction LR
    u1{"Form valid?"}
    u2["Show inline errors"]
    u4["Busy / rate limited: try later"]
    u3["'Check your inbox' (same message if email exists)"]
    u5["Link expired: resend"]
    u6["Show onboarding"]
    u7["Show error"]
    u8(["Go to role home"])
  end
  subgraph L_auth["Supabase Auth"]
    direction LR
    a1{"Sign-up accepted?"}
    a2{"Link valid?"}
  end
  subgraph L_mail["Email"]
    direction LR
    m1["Send verification email"]
  end
  subgraph L_api["API"]
    direction LR
    p1{"Roles valid? (admin not allowed)"}
  end
  subgraph L_db["Database"]
    direction LR
    d1["Create profile row"]
    d2["Save roles, mark onboarded"]
  end
  g1 --> g2
  g2 -- "submit" --> u1
  u1 -- "no" --> u2
  u2 -- "fix" --> g2
  u1 -- "yes" --> a1
  a1 -- "no" --> u4
  a1 -- "yes" --> m1
  a1 --> d1
  d1 --> u3
  m1 -- "email" --> g3
  u3 --> g3
  g3 --> a2
  a2 -- "no" --> u5
  u5 -- "resend" --> g3
  a2 -- "yes" --> u6
  u6 --> g4
  g4 --> p1
  p1 -- "no" --> u7
  u7 -- "retry" --> g4
  p1 -- "yes" --> d2
  d2 --> u8
```
</details>
<!-- /swimlane:FLOW-001 -->
| # | Lane | Input | Output | Next |
|---|---|---|---|---|
| 1 | Guest | name, email, password, 18+, terms_version | — | 2 |
| 2 | UI | form | Zod check (email, password ≥10, name 2–50, both boxes ticked) | 3 / errors |
| 3 | Auth | `signUp` with `options.data` | user (unconfirmed); trigger creates DB-001 | 4 |
| 4 | UI | — | Neutral "check your inbox" (no account enumeration) | 5 |
| 5 | Guest | email link → `/auth/callback` | session cookie | 6 |
| 6 | UI | — | UI-005 forced until ≥1 role (FR-002 AC1) | 7 |
| 7 | API | `{roles}` | user_roles rows, `onboarded_at`, audit `auth.role_granted` | role home |

| Path | Outcome / final state |
|---|---|
| Success | Verified, onboarded user with ≥1 role |
| Cancel | Guest leaves; unverified auth user remains (Supabase cleans per config) |
| Validation error | Inline errors; nothing created |
| Duplicate submission / existing email | Same neutral response; existing owner gets no extra account |
| Expired link | Error on callback page with "Resend verification" |
| Unauthorized/forbidden | Requesting `admin` role → 403 |
| Timeout / unavailable | Auth outage → "Sign-up temporarily unavailable, try again" |
| Recovery | Resend verification (rate-limited) |

---

## FLOW-002 — Sign-in, sign-out & password reset
| Field | Value |
|---|---|
| Trigger | User opens UI-003 or is redirected by guard |
| Preconditions | Verified account |
| Exit | Original `next` path or role home; UI-003 after sign-out |
| Links | FR-001 · UI-003, UI-004 · API-001 · DB-001 |

<!-- swimlane:FLOW-002 -->
**Sign-in**

![FLOW-002 Sign-in — horizontal swimlane](diagrams/FLOW-002-a.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_u["User"]
    direction LR
    u1(["Enter email + password"])
  end
  subgraph L_ui["Web UI"]
    direction LR
    e1["Too many attempts: wait N min"]
    e2["'Email or password is incorrect'"]
    e3["Not verified: resend email"]
    s1(["Signed in: go to next page"])
  end
  subgraph L_api["API (rate limit)"]
    direction LR
    r1{"Under 5 tries in 15 min?"}
  end
  subgraph L_auth["Supabase Auth"]
    direction LR
    a1{"Credentials OK?"}
  end
  u1 -- "submit" --> r1
  r1 -- "no" --> e1
  r1 -- "yes" --> a1
  a1 -- "wrong" --> e2
  e2 -- "retry" --> u1
  a1 -- "unverified" --> e3
  a1 -- "ok" --> s1
```
</details>

**Password reset & sign-out**

![FLOW-002 Password reset & sign-out — horizontal swimlane](diagrams/FLOW-002-b.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_u["User"]
    direction LR
    u2(["Forgot password: enter email"])
    u3["Open link, set new password"]
    u4(["Click Sign out"])
  end
  subgraph L_ui["Web UI"]
    direction LR
    e4["Neutral 'check your inbox'"]
    e5["Expired: request new link"]
    s2(["Signed in"])
    s3(["Sign-in page"])
  end
  subgraph L_auth["Supabase Auth"]
    direction LR
    a2["Send reset link (if account exists)"]
    a3{"Link valid?"}
    a4["Update password; sign out other sessions"]
    a5["Clear session cookie"]
  end
  u2 --> a2
  a2 --> e4
  e4 -- "email link" --> u3
  u3 --> a3
  a3 -- "no" --> e5
  e5 -- "again" --> u2
  a3 -- "yes" --> a4
  a4 --> s2
  u4 --> a5
  a5 --> s3
```
</details>
<!-- /swimlane:FLOW-002 -->
Notes: suspended users can sign in (read-only + banner, FR-025). Password change signs out other sessions (`scope: 'global'`).

| Path | Outcome |
|---|---|
| Success | Session cookie; protected routes accessible |
| Validation / invalid creds | Generic error; counter increments |
| Throttled | 429 with wait time (FR-001 AC5) |
| Reset for unknown email | Same neutral message (AC4) |
| Expired reset link | Offer new link |
| Sign-out | Cookie cleared server-side; back button shows UI-003 (no cached private pages: `Cache-Control: no-store`) |
| Unavailable | "Sign-in temporarily unavailable" |

---

## FLOW-003 — Tester identity & PayPal profile setup
| Field | Value |
|---|---|
| Trigger | Tester opens UI-006, or is sent there by IDENTITY_REQUIRED / PAYPAL_EMAIL_REQUIRED |
| Preconditions | Signed in; Tester role |
| Links | FR-003, FR-004, FR-026 · UI-006 · API-002, API-003 · DB-001, DB-003, DB-013 |

<!-- swimlane:FLOW-003 -->
**Tester identity & PayPal profile**

![FLOW-003 Tester identity & PayPal profile — horizontal swimlane](diagrams/FLOW-003.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_t["Tester"]
    direction LR
    t1(["Enter Google / Apple test email"])
    t2(["Enter PayPal email + current password"])
  end
  subgraph L_ui["Web UI"]
    direction LR
    x1["Inline error"]
    x2["IDENTITY_TAKEN / IN_USE"]
    ok1(["Identity saved"])
    x3["Re-auth failed"]
    x4["PAYPAL_EMAIL_TAKEN (audited)"]
    ok2(["Saved: payouts locked 48 h"])
  end
  subgraph L_api["API"]
    direction LR
    p1{"Valid email?"}
    p2{"Free for platform and not in an open test?"}
    p3{"Password correct?"}
    p4{"PayPal email unused?"}
  end
  subgraph L_db["Database"]
    direction LR
    d1["Save identity"]
    d2["Save email, start 48 h payout hold, audit"]
  end
  subgraph L_mail["Email"]
    direction LR
    m1["Alert sent to account email"]
  end
  t1 -- "save" --> p1
  p1 -- "no" --> x1
  x1 -- "fix" --> t1
  p1 -- "yes" --> p2
  p2 -- "no" --> x2
  p2 -- "yes" --> d1
  d1 --> ok1
  t2 -- "save" --> p3
  p3 -- "no" --> x3
  p3 -- "yes" --> p4
  p4 -- "no" --> x4
  p4 -- "yes" --> d2
  d2 --> m1
  m1 --> ok2
```
</details>
<!-- /swimlane:FLOW-003 -->
| Path | Outcome |
|---|---|
| Success | Identity/PayPal saved; PayPal change starts 48 h hold (A-019) |
| Validation | Bad email format → 422 |
| Duplicate | IDENTITY_TAKEN / PAYPAL_EMAIL_TAKEN |
| Forbidden | Non-tester calling identity API → 403 |
| Conflict | Identity used by open enrollment → IDENTITY_IN_USE |
| Recovery | Contact support link (mailto admin) for taken emails |

---

## FLOW-004 — Create campaign & pay
| Field | Value |
|---|---|
| Trigger | Developer clicks "New campaign" on UI-012 |
| Preconditions | Developer role, active account |
| Entry / exit | UI-013 → Stripe Checkout → UI-014 → UI-015 (status `pending_review`) |
| Links | FR-005, FR-006, FR-007, FR-033 · UI-012, UI-013, UI-014 · API-004, API-005, API-006 · DB-004, DB-005, DB-014, DB-015, DB-018 |

<!-- swimlane:FLOW-004 -->
**Create campaign & pay**

![FLOW-004 Create campaign & pay — horizontal swimlane](diagrams/FLOW-004.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_d["Developer"]
    direction LR
    d1(["New campaign: fill form"])
    d2["Click Pay"]
    d3{"Pay or cancel?"}
  end
  subgraph L_ui["Web UI"]
    direction LR
    x1["Inline errors"]
    u1["Show quote: slots × US$5.00"]
    x2["Fix missing fields"]
    x3["'Payment not completed': Pay again"]
    ok(["Paid: under review"])
  end
  subgraph L_api["API"]
    direction LR
    a1{"Valid? (rules, opt-in URL matches package)"}
    a2{"Draft complete?"}
    a3{"Signature valid and event new?"}
    x4["400 / ignore duplicate"]
  end
  subgraph L_db["Database"]
    direction LR
    db1["Save draft"]
    db2["Lock price; payment pending"]
    db3{"Amount matches?"}
    db4["Mark failed, alert admin"]
  end
  subgraph L_s["Stripe"]
    direction LR
    s1["Hosted Checkout page"]
    s2["Webhook: session completed"]
  end
  d1 -- "save" --> a1
  a1 -- "no" --> x1
  x1 -- "fix" --> d1
  a1 -- "yes" --> db1
  db1 --> u1
  u1 --> d2
  d2 --> a2
  a2 -- "no" --> x2
  a2 -- "yes" --> db2
  db2 -- "create session" --> s1
  s1 --> d3
  d3 -- "cancel" --> x3
  x3 -- "retry" --> d2
  d3 -- "pay" --> s2
  s2 --> a3
  a3 -- "no" --> x4
  a3 -- "yes" --> db3
  db3 -- "no" --> db4
  db3 -- "yes" --> ok
```
</details>
<!-- /swimlane:FLOW-004 -->
| # | Lane | Input | Output | Next |
|---|---|---|---|---|
| 1 | Developer | form fields | — | 2 |
| 2 | API | Zod + platform rules (FR-033) | DB-004 draft; `min_testers` snapshot | 3 |
| 3 | API | Pay | prices snapshotted (FR-006), DB-005 `pending`, campaign `pending_payment`, Stripe session URL | 4 |
| 4 | Stripe | card / wallet | session completed | 5 |
| 5 | API webhook | event | DB-014 row; `svc_mark_payment_paid` | 6 |
| 6 | UI-014 | `session_id` | polls `GET /dev/campaigns/:id` every 3 s up to 60 s | UI-015 |

| Path | Outcome / final state |
|---|---|
| Success | Campaign `pending_review`, payment `paid`, developer emailed |
| Cancel on Stripe | Campaign `pending_payment`; "Pay again" reuses unexpired session; after 24 h JOB-003 → `draft` |
| Validation | OPT_IN_URL_MISMATCH, slot/duration bounds, icon type/size |
| Duplicate webhook | No-op (unique event id) |
| Webhook before row exists | `svc_mark_payment_paid` raises NOT_FOUND → 500 → Stripe retries |
| Amount mismatch | Payment `failed`, campaign stays `pending_payment`, admin alerted |
| Async method fails | `async_payment_failed` → payment failed; developer emailed to retry |
| Unavailable | Stripe down → 502, retry later |
| Forbidden | Editing another developer's campaign → 404 (no existence leak) |

---

## FLOW-005 — Admin campaign review
| Field | Value |
|---|---|
| Trigger | Campaign enters `pending_review`; admin opens UI-019 |
| Preconditions | Admin role |
| Exit | `recruiting` (published) or `rejected` + full refund |
| Links | FR-008, FR-013 · UI-019 · API-016 · DB-004, DB-006, DB-013 |

<!-- swimlane:FLOW-005 -->
**Admin campaign review**

![FLOW-005 Admin campaign review — horizontal swimlane](diagrams/FLOW-005.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_a["Admin"]
    direction LR
    a1(["Open review queue"])
    a2{"Campaign acceptable?"}
    x1["409: already changed, refresh"]
    e1(["Campaign listed"])
    a3["Enter rejection reason"]
  end
  subgraph L_api["API"]
    direction LR
    p1["Approve"]
    p2["Reject"]
  end
  subgraph L_db["Database"]
    direction LR
    db1{"Still under review?"}
    db2["Recruiting: published, deadline +10 days"]
    db3["Rejected; full refund queued"]
  end
  subgraph L_s["Stripe"]
    direction LR
    s1["Refund (job retries)"]
  end
  subgraph L_n["Notifications"]
    direction LR
    n1["Notify developer + testers"]
    n2(["Developer: rejected + refund"])
  end
  a1 --> a2
  a2 -- "yes" --> p1
  p1 --> db1
  db1 -- "no" --> x1
  db1 -- "yes" --> db2
  db2 --> n1
  n1 --> e1
  a2 -- "no" --> a3
  a3 --> p2
  p2 --> db3
  db3 --> s1
  s1 --> n2
```
</details>
<!-- /swimlane:FLOW-005 -->
| Path | Outcome |
|---|---|
| Approve | Campaign listed (UI-007), testers notified |
| Reject | `rejected`, full refund; reason shown to developer |
| Missing reason | 422 REASON_REQUIRED |
| Concurrent developer cancel | One wins via row lock; loser gets 409 |
| Stripe refund failure | refund `failed`, retried by JOB-006; admin alert after 5 attempts |

---

## FLOW-006 — Browse & join campaign / withdraw before start
| Field | Value |
|---|---|
| Trigger | Tester opens UI-007 (or shared link to UI-008) |
| Preconditions | Listing public; joining requires Tester role, active, identity for platform |
| Exit | Enrollment `applied` (UI-009) or `withdrawn` |
| Links | FR-009, FR-015, FR-016, FR-019 · UI-007, UI-008, UI-009 · API-007, API-008 · DB-004, DB-007, v_campaign_listings |

<!-- swimlane:FLOW-006 -->
**Browse & join / withdraw before start**

![FLOW-006 Browse & join / withdraw before start — horizontal swimlane](diagrams/FLOW-006.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_t["Tester / Guest"]
    direction LR
    t1(["Browse campaigns"])
    t2["Open detail, click Join"]
    t3(["Click Withdraw, confirm"])
  end
  subgraph L_ui["Web UI"]
    direction LR
    u1{"Signed in as tester?"}
    x1["Go to sign-in (returns here)"]
    x2["Full / limit / add test email / own app"]
    ok1(["Joined: wait for access"])
    x3["Counts as drop, no reward (FLOW-008)"]
    ok2(["Withdrawn"])
  end
  subgraph L_api["API"]
    direction LR
    p1["Join request (rate limited)"]
    p2{"Testing not started yet?"}
  end
  subgraph L_db["Database"]
    direction LR
    db1{"Slot free and eligible?"}
    db2["Enrollment 'applied'"]
    db3["Withdrawn; slot reopens"]
  end
  subgraph L_n["Notifications"]
    direction LR
    n1["Developer: new applicant"]
  end
  t1 --> t2
  t2 --> u1
  u1 -- "no" --> x1
  u1 -- "yes" --> p1
  p1 --> db1
  db1 -- "no" --> x2
  db1 -- "yes" --> db2
  db2 --> n1
  n1 --> ok1
  t3 --> p2
  p2 -- "no" --> x3
  p2 -- "yes" --> db3
  db3 --> ok2
```
</details>
<!-- /swimlane:FLOW-006 -->
| Path | Outcome |
|---|---|
| Success | `applied`; slot reserved |
| Race for last slot | Exactly one succeeds (TEST-013) |
| Duplicate click | Second call → ALREADY_ENROLLED treated as success refresh |
| Guest | Redirect to sign-in, returns to UI-008 |
| Campaign not recruiting | 409 INVALID_STATE, detail shows status |
| Withdraw before start | `withdrawn`, no penalty |

---

## FLOW-007 — Grant access & start testing
| Field | Value |
|---|---|
| Trigger | Developer opens UI-015 for a `recruiting` campaign |
| Preconditions | Owner developer; campaign `recruiting` |
| Exit | Campaign `testing`; check-ins scheduled |
| Links | FR-010, FR-011, FR-018 · UI-015 · API-009, API-010 · DB-004, DB-007, DB-008, DB-013 |

<!-- swimlane:FLOW-007 -->
**Grant access & start testing**

![FLOW-007 Grant access & start testing — horizontal swimlane](diagrams/FLOW-007.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_d["Developer"]
    direction LR
    d1(["Open roster"])
    d2["Download CSV / copy emails"]
    d3["Select testers, mark access granted"]
    d4["Click Start testing"]
  end
  subgraph L_st["Play Console / App Store Connect"]
    direction LR
    s1["Developer adds tester emails"]
  end
  subgraph L_ui["Web UI"]
    direction LR
    x1["Need N more active testers"]
    ok(["Testing started"])
  end
  subgraph L_api["API"]
    direction LR
    p1["Export CSV (audited)"]
    p2["Grant access"]
    p3["Start request"]
  end
  subgraph L_db["Database"]
    direction LR
    db1["Access granted; opt-in check-in due"]
    db2{"Active testers ≥ minimum?"}
    db3["Testing: end date set, non-active released, check-ins scheduled"]
  end
  subgraph L_n["Notifications"]
    direction LR
    n1["Testers: opt in now"]
    n2["Everyone gets the schedule"]
  end
  d1 --> d2
  d2 --> p1
  p1 -- "CSV" --> s1
  s1 --> d3
  d3 --> p2
  p2 --> db1
  db1 --> n1
  n1 -- "testers opt in" --> d4
  d4 --> p3
  p3 --> db2
  db2 -- "no" --> x1
  x1 -- "wait" --> d4
  db2 -- "yes" --> db3
  db3 --> n2
  n2 --> ok
```
</details>
<!-- /swimlane:FLOW-007 -->
| Path | Outcome |
|---|---|
| Success | `testing`, `testing_ends_at = start + duration`, `review_ends_at = +3 d`; non-active testers released |
| Not enough active | 409 with `{active, required}`; developer waits or cancels (FLOW-013) |
| Developer never starts | Recruiting expiry (FLOW-013) |
| Forbidden | Other developer's campaign → 404 |
| Duplicate start | Second request 409; UI refreshes |

---

## FLOW-008 — Opt-in proof & periodic/final check-ins
| Field | Value |
|---|---|
| Trigger | Enrollment `access_granted` (opt-in) or a check-in window opens (reminder) |
| Preconditions | Tester owns enrollment |
| Exit | Enrollment `active` → `awaiting_verdict`, or `dropped` |
| Links | FR-017, FR-018, FR-019, FR-026 · UI-009, UI-010 · API-011, API-021 · DB-007, DB-008, DB-017 |

<!-- swimlane:FLOW-008 -->
**Opt-in proof & check-ins**

![FLOW-008 Opt-in proof & check-ins — horizontal swimlane](diagrams/FLOW-008.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_c["Cron jobs"]
    direction LR
    c1(["Check-in window opens"])
    c2(["Grace ended, nothing submitted"])
  end
  subgraph L_n["Notifications"]
    direction LR
    n1["Remind tester"]
    n2["Alert developer + admin"]
    n3(["Tester + developer told; dispute 3 days"])
  end
  subgraph L_t["Tester"]
    direction LR
    t1["Open test (opt-in: open link, install)"]
    t2["Upload screenshot + feedback"]
  end
  subgraph L_ui["Web UI"]
    direction LR
    u1{"File and feedback OK?"}
    x1["Inline error"]
    x2["422 / 429 shown"]
    x3["Too early / too late (file deleted)"]
    ok(["Received: next due date shown"])
  end
  subgraph L_api["API"]
    direction LR
    p1{"Type, size, rate limit OK?"}
  end
  subgraph L_fs["Storage"]
    direction LR
    f1["Store proof, compute SHA-256"]
  end
  subgraph L_db["Database"]
    direction LR
    db1{"Window open and state OK?"}
    db2{"Same image used by another tester?"}
    db3["Mark flagged"]
    db4["Mark received (opt-in: tester active)"]
    db5["Missed: tester dropped"]
  end
  c1 --> n1
  n1 --> t1
  t1 --> t2
  t2 --> u1
  u1 -- "no" --> x1
  x1 -- "fix" --> t2
  u1 -- "yes" --> p1
  p1 -- "no" --> x2
  p1 -- "yes" --> f1
  f1 --> db1
  db1 -- "no" --> x3
  db1 -- "yes" --> db2
  db2 -- "yes" --> db3
  db3 --> n2
  db2 -- "no" --> db4
  db3 --> ok
  db4 --> ok
  c2 --> db5
  db5 --> n3
```
</details>
<!-- /swimlane:FLOW-008 -->
Schedule example (Android, 16 days, start Day 0): opt-in before start; periodic due Day 4, 8, 12 (open 24 h before, grace 48 h after); final due Day 16 (open 48 h before, grace 24 h).

| Path | Outcome |
|---|---|
| Success opt-in | Enrollment `active` |
| Success periodic/final | Check-in `submitted` (or `flagged`) |
| Too early / too late | 409 with open/close time |
| Invalid file | 422, nothing stored |
| Upload ok but RPC fails | Object deleted, error shown, retry possible |
| Duplicate submit | Second submit → 409 INVALID_STATE (already submitted), UI shows submitted |
| Missed grace | `missed` → enrollment `dropped`; tester may dispute within 3 days (FLOW-010) |
| Offline | Retry; window countdown shown so tester knows deadline |

---

## FLOW-009 — Developer verdicts & auto-pass
| Field | Value |
|---|---|
| Trigger | JOB-002 moves campaign to `developer_review` at `testing_ends_at` |
| Preconditions | Owner developer; enrollments `awaiting_verdict` |
| Exit | Each enrollment `passed` (reward credited) / `failed` / `dropped` |
| Links | FR-012, FR-021 · UI-016 · API-012, API-021 · DB-007, DB-008, DB-010 |

<!-- swimlane:FLOW-009 -->
**Developer verdicts & auto-pass**

![FLOW-009 Developer verdicts & auto-pass — horizontal swimlane](diagrams/FLOW-009.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_c["Cron jobs"]
    direction LR
    c1(["Testing ends: 3-day review opens"])
    c2(["Deadline passed, no verdict"])
  end
  subgraph L_d["Developer"]
    direction LR
    d1["Review proofs and feedback"]
    d2{"Pass or fail?"}
    d3["Write fail reason"]
  end
  subgraph L_ui["Web UI"]
    direction LR
    x1["Already decided / not allowed"]
  end
  subgraph L_api["API"]
    direction LR
    p1["Save verdict"]
  end
  subgraph L_db["Database"]
    direction LR
    db1{"Allowed? (in window, final check-in in)"}
    db2{"Verdict"}
    db3["Passed + reward (available in 3 days)"]
    db4["Failed + reason"]
    db5["Auto-pass + reward"]
  end
  subgraph L_n["Notifications"]
    direction LR
    n0["Developer: review now"]
    n1(["Tester: passed"])
    n2(["Tester: failed, may dispute"])
    n3(["Tester: passed"])
  end
  c1 --> n0
  n0 --> d1
  d1 --> d2
  d2 -- "pass" --> p1
  d2 -- "fail" --> d3
  d3 --> p1
  p1 --> db1
  db1 -- "no" --> x1
  db1 -- "yes" --> db2
  db2 -- "pass" --> db3
  db3 --> n1
  db2 -- "fail" --> db4
  db4 --> n2
  c2 --> db5
  db5 --> n3
```
</details>
<!-- /swimlane:FLOW-009 -->
| Path | Outcome |
|---|---|
| Pass | Reward credited exactly once (TEST-022) |
| Fail | Requires reason; tester can dispute |
| No action | Auto-pass at deadline (FR-012 AC1) |
| Changing verdict | 409 VERDICT_FINAL |
| Forbidden | Non-owner → 404 |

---

## FLOW-010 — Dispute
| Field | Value |
|---|---|
| Trigger | Tester clicks "Dispute" on a failed or missed-check-in dropped enrollment |
| Preconditions | Within 3 days of `ended_at`; no existing dispute |
| Exit | Dispute `upheld` (enrollment `passed`) or `rejected` |
| Links | FR-024 · UI-010, UI-020 · API-013 · DB-009, DB-007, DB-010 |

<!-- swimlane:FLOW-010 -->
**Dispute**

![FLOW-010 Dispute — horizontal swimlane](diagrams/FLOW-010.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_t["Tester"]
    direction LR
    t1(["Open failed / dropped test, write reason"])
  end
  subgraph L_ui["Web UI"]
    direction LR
    x1["Window closed / already disputed"]
  end
  subgraph L_api["API"]
    direction LR
    p1{"Within 3 days and first dispute?"}
  end
  subgraph L_db["Database"]
    direction LR
    db1["Dispute open"]
    db2["Upheld: tester passed + reward"]
    db3["Rejected: fail stands"]
  end
  subgraph L_n["Notifications"]
    direction LR
    n1["Admin + developer alerted"]
    n2(["Both parties told the outcome"])
  end
  subgraph L_a["Admin"]
    direction LR
    a1["Review proofs, feedback, both reasons"]
    a2{"Decision"}
  end
  t1 --> p1
  p1 -- "no" --> x1
  p1 -- "yes" --> db1
  db1 --> n1
  n1 --> a1
  a1 --> a2
  a2 -- "upheld" --> db2
  a2 -- "rejected" --> db3
  db2 --> n2
  db3 --> n2
```
</details>
<!-- /swimlane:FLOW-010 -->
Settlement of the campaign waits until no dispute is `open` (FLOW-011).

---

## FLOW-011 — Settlement & refund
| Field | Value |
|---|---|
| Trigger | JOB-002: campaign `developer_review` with `now ≥ review_ends_at + 3 d` and no open disputes |
| Exit | Campaign `completed`; refund of unearned rewards |
| Links | FR-013 · UI-015 · API-021, API-006 · DB-004, DB-005, DB-006 |

<!-- swimlane:FLOW-011 -->
**Settlement & refund**

![FLOW-011 Settlement & refund — horizontal swimlane](diagrams/FLOW-011.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_c["Cron jobs"]
    direction LR
    c1(["Review + dispute windows over, no open disputes"])
    c2["Refund job runs"]
  end
  subgraph L_db["Database"]
    direction LR
    db1["Count passed testers"]
    db2{"Unused rewards > 0? (slots − passed) × reward"}
    db3["Completed, no refund"]
    db4["Completed; refund queued"]
    db5["Refund succeeded; payment updated"]
    db6["Attempts +1, retry later"]
  end
  subgraph L_s["Stripe"]
    direction LR
    s1{"Refund OK?"}
  end
  subgraph L_n["Notifications"]
    direction LR
    n1(["Developer: completed + refund amount"])
  end
  subgraph L_a["Admin"]
    direction LR
    a1["Alert admin after 5 failures"]
  end
  c1 --> db1
  db1 --> db2
  db2 -- "no" --> db3
  db2 -- "yes" --> db4
  db3 --> n1
  db4 --> c2
  c2 --> s1
  s1 -- "yes" --> db5
  db5 --> n1
  s1 -- "no" --> db6
  db6 -- "retry" --> c2
  db6 -- "5th fail" --> a1
```
</details>
<!-- /swimlane:FLOW-011 -->
Example: 15 slots × US$3.50 reward; 13 passed → rewards US$45.50, refund 2 × 3.50 = US$7.00; platform keeps 15 × 1.50 = US$22.50 (A-011).

---

## FLOW-012 — Payout request & PayPal execution
| Field | Value |
|---|---|
| Trigger | Tester clicks "Withdraw to PayPal" on UI-011 |
| Preconditions | Available ≥ US$25.00, PayPal email set and not in hold, no open payout, active |
| Exit | Payout `paid`, or released back to balance (`rejected`/`cancelled`/`failed`/`returned`) |
| Links | FR-020…FR-023 · UI-011, UI-021 · API-014, API-015, API-017, API-018 · DB-010, DB-011, DB-014 |

<!-- swimlane:FLOW-012 -->
**Payout request & PayPal**

![FLOW-012 Payout request & PayPal — horizontal swimlane](diagrams/FLOW-012.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_t["Tester"]
    direction LR
    t1(["Open wallet, enter amount"])
  end
  subgraph L_ui["Web UI"]
    direction LR
    x1["Show reason (e.g. US$3 more needed)"]
  end
  subgraph L_api["API"]
    direction LR
    p1{"≥ US$25, PayPal set, no hold, none open?"}
    p2["Send PayPal batch"]
    p3{"Signature valid?"}
    x3["Reject 400"]
  end
  subgraph L_db["Database"]
    direction LR
    db1["Payout requested; balance held"]
    db2["Rejected; balance released"]
    db3["Processing"]
    db4{"Result?"}
    db5["Paid"]
    db6["Failed / returned; balance released"]
  end
  subgraph L_a["Admin"]
    direction LR
    a1["Review queue + fraud signals"]
    a2{"Approve?"}
    x2["Stays requested; retry"]
  end
  subgraph L_pp["PayPal"]
    direction LR
    pp1{"Batch accepted?"}
    pp2["Result webhook per item"]
  end
  subgraph L_n["Notifications"]
    direction LR
    n1["Tester: request received"]
    n4(["Tester: rejected"])
    n2(["Tester: paid"])
    n3(["Tester: fix PayPal email"])
  end
  t1 -- "request" --> p1
  p1 -- "no" --> x1
  p1 -- "yes" --> db1
  db1 --> n1
  n1 --> a1
  a1 --> a2
  a2 -- "no" --> db2
  db2 --> n4
  a2 -- "yes" --> p2
  p2 --> pp1
  pp1 -- "no" --> x2
  x2 -- "retry" --> a2
  pp1 -- "yes" --> db3
  db3 --> pp2
  pp2 --> p3
  p3 -- "no" --> x3
  p3 -- "yes" --> db4
  db4 -- "succeeded" --> db5
  db5 --> n2
  db4 -- "failed" --> db6
  db6 --> n3
```
</details>
<!-- /swimlane:FLOW-012 -->
| Path | Outcome |
|---|---|
| Success | `paid`; ledger shows hold; balance reduced |
| Below minimum | 422 with remaining needed ("US$3.00 more to withdraw") |
| Double request | One open payout max (TEST-020) |
| PayPal down | Payouts stay `requested`; JOB-004 reconciles any ambiguous batch |
| Wrong PayPal email | Unclaimed → returned → released; tester prompted to fix email (48 h hold applies) |
| Suspension while open | Requested payout rejected + released (FLOW-014) |

---

## FLOW-013 — Campaign cancellation & recruiting expiry
| Field | Value |
|---|---|
| Trigger | Developer clicks Cancel (UI-012/UI-015) or JOB-002 detects `recruiting_ends_at` passed |
| Preconditions | Status ∈ draft, pending_payment, pending_review, recruiting |
| Exit | `cancelled`; full refund if paid; enrollments released |
| Links | FR-014, FR-013 · UI-012, UI-015 · API-024, API-021 · DB-004, DB-006, DB-007 |

<!-- swimlane:FLOW-013 -->
**Cancellation & recruiting expiry**

![FLOW-013 Cancellation & recruiting expiry — horizontal swimlane](diagrams/FLOW-013.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_d["Developer"]
    direction LR
    d1(["Click Cancel + reason"])
    x1["409: testing started, contact admin"]
  end
  subgraph L_c["Cron jobs"]
    direction LR
    c1(["Recruiting deadline passed"])
  end
  subgraph L_api["API"]
    direction LR
    p1["Cancel request"]
  end
  subgraph L_db["Database"]
    direction LR
    db1{"Status allows cancel?"}
    db2["Cancelled; testers released"]
    db3{"Was it paid?"}
  end
  subgraph L_s["Stripe"]
    direction LR
    s1["Full refund"]
  end
  subgraph L_n["Notifications"]
    direction LR
    n1(["Developer + testers told"])
  end
  d1 --> p1
  p1 --> db1
  c1 -- "job" --> db1
  db1 -- "no" --> x1
  db1 -- "yes" --> db2
  db2 --> db3
  db3 -- "yes" --> s1
  db3 -- "no" --> n1
  s1 --> n1
```
</details>
<!-- /swimlane:FLOW-013 -->

---

## FLOW-014 — Admin suspension
| Field | Value |
|---|---|
| Trigger | Admin decides to suspend user (fraud, policy) on UI-022 |
| Exit | User `suspended`; side effects applied; reinstatement restores status only |
| Links | FR-025 · UI-022 · API-019 · DB-001, DB-007, DB-011, DB-004, DB-013 |

<!-- swimlane:FLOW-014 -->
**Admin suspension**

![FLOW-014 Admin suspension — horizontal swimlane](diagrams/FLOW-014.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_a["Admin"]
    direction LR
    a1(["Open user, click Suspend, reason"])
    a2["Check impact summary, confirm"]
    x1["409 refused"]
    a3(["Reinstate + reason"])
  end
  subgraph L_api["API"]
    direction LR
    p1{"Not self / not last admin?"}
  end
  subgraph L_db["Database"]
    direction LR
    db1["Suspended; tests dropped; payouts rejected; campaigns refunded"]
    db2["Status active; audited"]
  end
  subgraph L_au["Supabase Auth"]
    direction LR
    au1["Sign out all sessions"]
  end
  subgraph L_n["Notifications"]
    direction LR
    n1(["User + affected people told"])
    n2(["User told"])
  end
  a1 --> a2
  a2 --> p1
  p1 -- "no" --> x1
  p1 -- "yes" --> db1
  db1 --> au1
  au1 --> n1
  a3 --> db2
  db2 --> n2
```
</details>
<!-- /swimlane:FLOW-014 -->
Processing payouts (`processing`) cannot be recalled; admin is shown them in the impact summary.

---

## FLOW-015 — Account deletion
| Field | Value |
|---|---|
| Trigger | User clicks "Delete account" in UI-006 |
| Preconditions | Signed in; password re-entry |
| Exit | Account anonymised and signed out, or blocked with reasons |
| Links | FR-031 · UI-006 · API-023 · DB-001, DB-003, DB-017 |

<!-- swimlane:FLOW-015 -->
**Account deletion**

![FLOW-015 Account deletion — horizontal swimlane](diagrams/FLOW-015.svg)

<details><summary>Text version (Mermaid, generated)</summary>

```mermaid
flowchart LR
  subgraph L_u["User"]
    direction LR
    u1(["Delete account, enter password"])
    u2{"Small balance under US$25?"}
    u3["Tick 'I forfeit my balance'"]
  end
  subgraph L_ui["Web UI"]
    direction LR
    x1["Re-auth failed"]
    x2["Show blockers with links"]
    ok(["Goodbye page"])
  end
  subgraph L_api["API"]
    direction LR
    p1{"Password correct?"}
    p2{"Any blockers? (open tests, campaigns, payouts, balance)"}
  end
  subgraph L_db["Database"]
    direction LR
    db1["Anonymise profile, remove emails, delete proofs"]
  end
  subgraph L_au["Supabase Auth"]
    direction LR
    au1["Scramble email, ban, sign out"]
  end
  u1 --> u2
  u2 -- "yes" --> u3
  u2 -- "no" --> p1
  u3 --> p1
  p1 -- "no" --> x1
  x1 -- "retry" --> u1
  p1 -- "yes" --> p2
  p2 -- "yes" --> x2
  p2 -- "no" --> db1
  db1 --> au1
  au1 --> ok
```
</details>
<!-- /swimlane:FLOW-015 -->

## 3. Screen navigation map
```mermaid
flowchart LR
  UI001["UI-001 Landing"] --> UI007["UI-007 Listing"] --> UI008["UI-008 Detail"]
  UI001 --> UI002["UI-002 Sign up"] --> UI005["UI-005 Onboarding"]
  UI001 --> UI003["UI-003 Sign in"] --> UI004["UI-004 Reset"]
  UI005 --> UI007
  UI005 --> UI012["UI-012 Dev dashboard"]
  UI008 --> UI009["UI-009 My tests"] --> UI010["UI-010 Enrollment"]
  UI009 --> UI011["UI-011 Wallet"]
  UI012 --> UI013["UI-013 Campaign editor"] --> UI014["UI-014 Checkout result"] --> UI015["UI-015 Manage campaign"] --> UI016["UI-016 Review"]
  UIx["Header"] --> UI017["UI-017 Notifications"]
  UIx --> UI006["UI-006 Settings"]
  UI018["UI-018 Admin overview"] --> UI019["UI-019 Campaign review"]
  UI018 --> UI020["UI-020 Disputes"]
  UI018 --> UI021["UI-021 Payouts"]
  UI018 --> UI022["UI-022 Users"]
  UI018 --> UI023["UI-023 Settings"]
  UI018 --> UI024["UI-024 Audit log"]
```
