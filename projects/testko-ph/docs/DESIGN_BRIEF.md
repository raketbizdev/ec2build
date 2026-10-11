# DESIGN_BRIEF — TestKo PH

## 0. Document control
| Field | Value |
|---|---|
| Document | `DESIGN_BRIEF.md` (04) |
| Version | 0.2.0 · draft |
| Date | 2026-10-11 |
| Upstream | PRD 0.3.0, APP_FLOW 0.3.1 |
| Downstream | IMPLEMENTATION_PLAN 0.5.0 |
| Prototype | **None built.** This brief contains specifications and wireframe descriptions only. |

## 1. Intended experience
- **Trustworthy money app, not a hype site.** Every amount, deadline and rule is explicit. Testers always know: what to do next, by when (Manila time), and how much they will earn.
- **Mobile-first for testers** (most use Android phones on mobile data); **desktop-comfortable for developers and admins** (rosters, review tables).
- **Calm urgency:** deadlines are prominent with countdowns, but copy is supportive, never threatening.

### Design principles
1. *Next action first* — each dashboard leads with the single most urgent task card.
2. *Show the money math* — quotes, rewards, refunds and payout minimums are always shown with the formula.
3. *Evidence over trust* — proofs and feedback are visible to the parties who need them, nowhere else.
4. *Nothing hidden in colour* — status uses text + icon + colour.
5. *Forgiving forms* — inputs survive errors and network failures.

## 2. Personas in context
| Persona | Device / context | Design implication |
|---|---|---|
| Mika (tester) | Android phone, intermittent data, uses Facebook links | Light pages, big tap targets, upload from gallery, clear countdowns |
| Paolo (developer) | Laptop, Play Console open in another tab | Copy-to-clipboard emails, CSV export, bulk select |
| Admin | Laptop, processes queues | Dense tables, keyboard shortcuts, filters, impact summaries before destructive actions |

## 3. Brand treatment (provisional — A-027, OD-007)
Neutral, technical, friendly. Wordmark "TestKo PH" in the heading font; no use of "IT Philippines" logos until permission (OD-007). Illustration: simple line icons (Lucide). Tone: plain English, short sentences, second person ("You'll earn US$3.50").

## 4. Design tokens (`src/styles/tokens.css`, mirrored in Tailwind config)
### 4.1 Colour (semantic; light / dark)
| Token | Light | Dark | Use | Contrast note |
|---|---|---|---|---|
| `--color-bg` | #FFFFFF | #0B1220 | page | — |
| `--color-surface` | #F6F8FB | #111A2E | cards | — |
| `--color-border` | #D9DFE8 | #26324A | dividers, inputs (≥3:1 vs bg for inputs: use `--color-border-strong`) | |
| `--color-border-strong` | #8A94A6 | #6B7A96 | input borders | ≥ 3:1 on bg |
| `--color-text` | #0F172A | #E6EAF2 | body | ≥ 15:1 |
| `--color-text-muted` | #475569 | #A3AEC2 | secondary | ≥ 4.5:1 |
| `--color-primary` | #1D4ED8 | #6E9BFF | primary buttons, links | white on #1D4ED8 ≈ 6.7:1 |
| `--color-primary-fg` | #FFFFFF | #0B1220 | text on primary | |
| `--color-accent` | #B45309 | #F2B13C | money highlights (amber) | #B45309 on white ≥ 4.5:1 |
| `--color-success` | #15803D | #4ADE80 | passed, paid | ≥ 4.5:1 on bg |
| `--color-warning` | #A16207 | #FACC15 | due soon, pending | text use only with icon |
| `--color-danger` | #B91C1C | #F87171 | failed, dropped, destructive | ≥ 4.5:1 |
| `--color-info` | #0369A1 | #38BDF8 | informational | |
| `--color-focus` | #2563EB | #93C5FD | 2 px focus ring + 2 px offset | ≥ 3:1 vs adjacent |
All pairs must be verified with an automated contrast check in TASK-003 (values above are design intent; adjust if any check fails).

### 4.2 Typography
| Token | Value |
|---|---|
| Font | `Inter` (self-hosted via `next/font`), fallback system-ui; tabular numerals for money (`font-variant-numeric: tabular-nums`) |
| Scale (rem) | xs 0.75 · sm 0.875 · base 1 · lg 1.125 · xl 1.25 · 2xl 1.5 · 3xl 1.875 · 4xl 2.25 |
| Line height | body 1.5, headings 1.25 |
| Weights | 400 body, 500 labels, 600 headings, 700 money totals |
Min body size 16 px on mobile (prevents iOS zoom on inputs).

### 4.3 Spacing, radius, elevation, motion, breakpoints
- Spacing: 4 px base — 1(4) 2(8) 3(12) 4(16) 6(24) 8(32) 12(48) 16(64).
- Radius: sm 6 px (inputs), md 10 px (cards, buttons), lg 16 px (dialogs), full (badges/avatars).
- Elevation: e0 none; e1 `0 1px 2px rgb(15 23 42 / .08)` cards; e2 `0 8px 24px rgb(15 23 42 / .12)` popovers/dialogs.
- Motion: 150 ms ease-out (hover/focus), 200 ms (dialogs), disabled when `prefers-reduced-motion: reduce`.
- Breakpoints: `sm` 640, `md` 768, `lg` 1024, `xl` 1280. Layout min width 320 px.
- Touch targets ≥ 44 × 44 px; spacing between targets ≥ 8 px.

## 5. Layout and navigation architecture
| Area | Layout | Navigation |
|---|---|---|
| Public (UI-001, 007, 008, 026) | Header (logo, Campaigns, Sign in, Join) + footer (Terms, Privacy, Tester Rules) | Top nav; mobile hamburger |
| App — tester | Mobile: bottom tab bar **Campaigns · My tests · Wallet · Alerts · Me**; desktop: left sidebar | Badge counts for due check-ins and unread notifications |
| App — developer | Sidebar **My campaigns · New campaign · Alerts · Me**; mobile uses bottom bar with same items | Users with both roles get a role switcher ("Testing / Developing") in header |
| Admin | Desktop-first sidebar **Overview · Campaigns · Disputes · Payouts · Users · Settings · Audit log** | Keyboard: `g o`, `g c`, `g d`, `g p`, `g u` |
Global: suspended banner (danger) on all app pages; email-unverified state handled in auth area only.

## 6. Component inventory
| Component | Variants / states | Notes |
|---|---|---|
| Button | primary, secondary, ghost, destructive; sizes sm/md/lg; loading (spinner + `aria-busy`), disabled | Loading keeps width; text changes to "Saving…" |
| Input / Textarea | default, focus, error (message below, `aria-describedby`), disabled, with counter | Counters for limited fields (e.g., 0/1000) |
| Select, RadioGroup (platform), Checkbox, Switch | Radix | |
| FileDrop | idle, dragging, selected (thumbnail preview), uploading (progress), error | On mobile opens gallery/camera; shows size/type rules |
| Card, CampaignCard | default, full, closing-soon | Icon, name, platform chip, reward, slots left, deadline |
| StatusBadge | per enum (campaign, enrollment, check-in, payout, dispute) | text + icon + colour mapping §6.1 |
| MoneyAmount | normal, large, muted, negative | `US$1,234.56`, tabular nums |
| Countdown | normal, due soon (< 24 h, warning), overdue grace (danger) | Absolute Manila time in tooltip and `aria-label` |
| Stepper / Timeline | enrollment journey, campaign lifecycle | |
| DataTable | sortable, selectable rows, bulk action bar, empty, loading skeleton, pagination | Roster, admin queues |
| Dialog / AlertDialog | confirm, destructive confirm with typed reason | Focus trap, Esc closes (except while submitting) |
| Toast | success, error, info | `role=status`/`alert` |
| EmptyState | illustration icon, text, primary action | |
| Banner | info, warning, danger | suspension, PayPal hold, policy |
| NotificationItem | unread/read | |
| ProofViewer | image lightbox with zoom, flagged label, SHA duplicate notice | Signed URL refresh on expiry |
| QuoteSummary | slots × price = total; reward and fee breakdown | |
| Skeleton | for each list/card | |

### 6.1 Status mapping
| Enum value | Label | Colour | Icon |
|---|---|---|---|
| campaign draft / pending_payment / pending_review | Draft / Awaiting payment / Under review | muted / warning / info | FileEdit / CreditCard / Hourglass |
| recruiting / testing / developer_review | Recruiting / Testing / In review | primary / info / warning | Users / FlaskConical / ClipboardCheck |
| completed / cancelled / rejected | Completed / Cancelled / Rejected | success / muted / danger | CheckCircle / XCircle / Ban |
| enrollment applied / access_granted / active | Applied / Opt in now / Testing | muted / warning / info | Clock / KeyRound / Smartphone |
| awaiting_verdict / passed / failed | Awaiting review / Passed / Failed | warning / success / danger | Hourglass / BadgeCheck / XCircle |
| dropped / withdrawn / released | Dropped / Withdrawn / Released | danger / muted / muted | AlertTriangle / LogOut / Undo2 |
| check-in due / submitted / flagged / missed / cancelled | Due / Received / Flagged / Missed / Cancelled | warning / success / danger / danger / muted | |
| payout requested / processing / paid / unclaimed / returned / failed / rejected / cancelled | Requested / Sending / Paid / Unclaimed / Returned / Failed / Rejected / Cancelled | info / info / success / warning / danger / danger / danger / muted | |

## 7. Screen catalogue
Each screen lists: purpose · audience/permission · hierarchy (top→bottom) · inputs & validation · actions · states · accessibility · flows.

### UI-001 Landing (public)
Purpose: explain both sides, build trust, drive sign-up. Audience: guests. Hierarchy: hero ("Get paid to test apps from fellow Filipino devs" / "Get your 12 closed testers"), two CTAs (Join as tester / Post your app), how-it-works (3 steps each side), money math ("Earn US$3.50 per completed test · Withdraw from US$25 via PayPal" — values from settings), live open-campaign count, FAQ (including "We don't guarantee Google approval", "No paid reviews"), footer. States: loading counts skeleton; count unavailable → hide. A11y: single h1, landmarks. Flows: FLOW-001, FLOW-006.

### UI-002 Sign up
Inputs: display name (2–50), email, password (≥10, show/hide, strength hint), checkbox "I'm 18 or older", checkbox "I agree to Terms, Privacy Notice and Tester/Developer Rules" (links open in new tab). Validation inline on blur + on submit. Actions: Create account; link to sign in. States: submitting, success ("Check your inbox at m***@gmail.com" + resend with cooldown), error (generic), throttled. A11y: error summary at top with links to fields. Flow: FLOW-001.

### UI-003 Sign in
Inputs: email, password. Actions: Sign in, Forgot password, Sign up. States: invalid (generic), unverified (resend), throttled (minutes remaining), unavailable. Flow: FLOW-002.

### UI-004 Password reset
Two views: request (email) → neutral confirmation; set new password (password + confirm). States: expired link → request again. Flow: FLOW-002.

### UI-005 Onboarding
Purpose: choose roles, confirm terms version if changed. Cards: "I want to test apps" (Tester) / "I want testers for my app" (Developer), multi-select. Tester path continues to "Add your Google/Apple test email" (optional skip) and PayPal (optional skip). Actions: Continue (disabled until ≥1 role). Flow: FLOW-001.

### UI-006 Settings / profile
Sections: Profile (display name, country), Roles (add role), **Tester identities** (Android Google email, iOS Apple ID email; each with status "Used in N open tests" and edit/remove disabled when in use), **PayPal** (masked email, change dialog requiring password; hold banner with unlock time), Notifications (new campaign emails switch), Security (change password), **Danger zone** (Delete account → dialog listing blockers). Validation per FR-003/FR-004. Flows: FLOW-003, FLOW-015.

### UI-007 Campaign listing
Audience: everyone. Hierarchy: filter chips (All · Android · iOS), sort (Newest · Closing soon), grid/list of CampaignCards (icon, app name, platform chip, short description, **reward US$3.50**, duration "16 days", slots left "4 of 15 left", recruiting deadline countdown). Empty: "No open campaigns right now — turn on new campaign emails" (link UI-006). Loading: 6 skeleton cards. Pagination: "Load more" (cursor). Flow: FLOW-006.

### UI-008 Campaign detail
Hierarchy: header (icon, name, platform, developer display name), key facts row (reward, duration, slots left, deadline), description, "What you'll do" timeline (join → developer adds you → opt in + proof → check-ins on days 4/8/12/16 → review → reward), requirements (identity for platform, rules). Primary action states: Join / Sign in to join / Add your Android test email first / Full / Already joined (link UI-010) / Your own campaign / Closed. Opt-in link **not** shown here. Flow: FLOW-006.

### UI-009 My tests (tester dashboard)
Hierarchy: "Next action" card (most urgent due check-in with countdown, or "Opt in now"), tabs Active · Waiting · Finished, list items with status badge, next due date, reward. Empty: "You haven't joined any tests yet" → Browse. Flow: FLOW-006, FLOW-008.

### UI-010 Enrollment detail / check-in
Hierarchy: status timeline; when `access_granted`: **Opt-in panel** (opt-in URL button "Open Play testing page" / TestFlight link or "Check your email for TestFlight invite", instructions from developer, copy store email) + upload opt-in proof; when `active`: check-in list (due/open/received/missed) with current open check-in form (FileDrop + feedback textarea with counter + "What to include" tips); verdict panel; dispute button (when eligible, with window countdown) + dispute form; Withdraw (secondary, destructive confirm explaining consequences by phase). States: window not open (shows opens-at), closed, submitted (thumbnail + feedback), flagged notice (neutral wording: "Under review"), upload progress/failure retry. Flows: FLOW-008, FLOW-010.

### UI-011 Wallet & payouts
Hierarchy: balance cards (Available — large, accent; Pending — with "available on" dates), progress bar to US$25 minimum ("US$7.00 more to withdraw"), Withdraw button (states: enabled; disabled with reason: below minimum / no PayPal email (link) / PayPal hold until … / payout already open), open payout status card (cancel while requested), ledger table (date, description, campaign, amount ±). Withdraw dialog: amount (default full, min 25.00, max available, 2 decimals), PayPal email masked, confirm. Flow: FLOW-012.

### UI-012 Developer dashboard
Hierarchy: "New campaign" primary, list of campaigns with status badge, key metric per status (Recruiting: active/min testers; Testing: day X of N, active testers; Review: verdicts left + deadline), actions (Continue draft, Pay, Manage, Cancel when allowed). Empty: explainer + New campaign. Flows: FLOW-004, FLOW-013.

### UI-013 Campaign editor
Steps (single page with sections, sticky summary on desktop): 1 Platform (radio Android/iOS — changes rules text), 2 App details (name, package/bundle ID, short description with counter, description, icon FileDrop), 3 Testing setup (opt-in URL with format helper and examples, instructions, tester slots stepper (min..100, default from settings), duration (min..30, default 16/14)), 4 QuoteSummary ("15 testers × US$5.00 = US$75.00; testers earn US$3.50 each; unearned rewards are refunded"), terms checkbox "I own this app and won't ask testers for reviews". Actions: Save draft, Pay with Stripe. Validation: inline (OPT_IN_URL_MISMATCH explains expected `https://play.google.com/apps/testing/<package>`). Locked fields after payment shown read-only with lock icon. Flow: FLOW-004.

### UI-014 Checkout result
Success: spinner "Confirming payment…" (polls up to 60 s) → "Paid — under review (usually within 24 h)" → button to UI-015. Still processing: "We'll email you when confirmed." Cancel: "Payment not completed" + Pay again + Back to draft. Flow: FLOW-004.

### UI-015 Manage campaign (developer)
Header: status, timeline with dates, quote/payment summary, Cancel (when allowed). Tabs: **Roster** (DataTable: select, display name, store email (copy), status, applied/granted/active times, opt-in proof thumbnail; bulk "Mark access granted"; "Copy emails" & "Download CSV" for applied; row action Remove with reason), **Progress** (during testing: per-tester check-in grid days 4/8/12/16 with status icons; flagged highlights; dropped list), **Feedback** (chronological feedback stream with proof thumbnails), **Settlement** (after completion: passed count, refund amount and status). Start testing button: enabled when active ≥ min ("Start testing (13 active, 12 required)"); disabled reason otherwise; confirm dialog explaining releases of non-active testers and the end date. Flows: FLOW-007, FLOW-011, FLOW-013.

### UI-016 Developer review
Visible in `developer_review`. Header countdown to review deadline + note "Testers you don't review will pass automatically". List per tester: proofs carousel, feedback, flags; Pass / Fail buttons; Fail opens reason dialog (20–500). Bulk "Pass all remaining". Final verdicts read-only. Flow: FLOW-009.

### UI-017 Notifications
List grouped by day; unread dot; click marks read and navigates to `link_path`; "Mark all as read". Empty state. Flow: all.

### UI-018 Admin overview
Count tiles linking to queues: pending reviews, open disputes, requested payouts (sum US$), failed refunds, flagged check-ins (24 h), failed webhooks, job heartbeat status, negative balances. Flow: FLOW-005, FLOW-010, FLOW-012.

### UI-019 Admin campaign review
Queue table (submitted at, developer, app, platform, slots, amount); detail with all fields, opt-in URL (open in new tab), developer history (campaigns, fail-verdict rate, disputes), checklist (FR-008), Approve / Reject (reason required) / Cancel (for live campaigns, with refund preview). Flow: FLOW-005, FLOW-013.

### UI-020 Admin disputes
Queue (age, tester, campaign, type failed/dropped); detail: timeline, all check-ins with proofs, developer reason, tester reason, both parties' history; resolution form (upheld/rejected + note ≥10). Flow: FLOW-010.

### UI-021 Admin payouts
Table of `requested` payouts: tester, amount, PayPal email (full for admin), account age, completed tests, flags (duplicate proofs, prior failed payouts, PayPal email changed < 7 d); select → "Approve & send (N, US$X)" with confirm dialog; reject with reason. Tabs for processing/unclaimed/failed with "Sync status". Flow: FLOW-012.

### UI-022 Admin users
Search by email/name; user detail: roles, status, identities, PayPal email, enrollments, campaigns, ledger, audit trail; actions Suspend (impact summary), Reinstate, Grant/Revoke admin, Ledger adjustment (amount ±, note). Flow: FLOW-014.

### UI-023 Admin settings
Form grouped (Pricing, Payouts, Android, iOS, Check-ins, Windows, Limits); each field with description and validation; save shows diff confirm; note "applies to campaigns paid after saving". Flow: FR-029.

### UI-024 Admin audit log
Filter by action, entity, actor, date; table; row expands metadata JSON (pretty, read-only). Flow: FR-030.

### UI-025 Error pages
401 → redirect; 403 "You don't have access to this page"; 404 "Not found"; 500 "Something went wrong (ref req_…)"; maintenance. All with home link.

### UI-026 Legal pages
Terms of Service, Privacy Notice, Tester Rules, Developer Rules, Disclaimer — Markdown-rendered static pages with version + effective date. Content requires counsel (OD-003); placeholders clearly marked "DRAFT — NOT LEGAL ADVICE" until approved.

## 8. Copy guidance (samples)
| Context | Copy |
|---|---|
| Reward line | "Earn **US$3.50** when you complete this 16-day test." |
| Opt-in step | "1. Open the testing page with **mika@gmail.com** signed in. 2. Tap *Become a tester*. 3. Install the app. 4. Upload a screenshot showing you're a tester." |
| Due soon | "Check-in 2 is due **Tue, 21 Oct, 9:00 PM** (in 5 h)." |
| Dropped | "You missed check-in 2, so you're no longer in this test. If this was a mistake, you can dispute until **Fri, 24 Oct**." |
| Below minimum | "You need **US$7.00** more to withdraw (minimum US$25.00)." |
| PayPal hold | "For your security, withdrawals are paused until **Thu, 23 Oct, 4:12 PM** because your PayPal email changed." |
| Developer fail reason helper | "Explain what the tester didn't do (e.g., uninstalled the app on day 9). The tester will see this." |
| Disclaimer | "TestKo PH helps you run a closed test. Google and Apple decide on production access — we can't guarantee approval." |
Never use: "guaranteed", "easy money", "instant payout".

## 9. Responsive and mode-specific behaviour
- Tester flows fully usable at 320 px; FileDrop uses `<input type="file" accept="image/png,image/jpeg,image/webp">` (opens gallery/camera on mobile).
- Tables collapse to stacked cards < 768 px (roster, admin tables keep horizontal scroll with sticky first column for admin only).
- Bottom tab bar respects safe-area insets.
- Desktop shortcuts (admin): `/` focus search, `j/k` move rows, `x` select, `a` approve dialog (never executes without confirm).

## 10. Accessibility requirements (WCAG 2.2 AA)
- Keyboard: every action reachable; visible focus (token `--color-focus`); no keyboard traps except modal focus trap with Esc.
- Screen readers: form errors linked via `aria-describedby`, error summary with `role="alert"`; live region for upload progress and toasts; countdown has static accessible text (not ticking announcements).
- Target size ≥ 24 × 24 CSS px minimum (WCAG 2.5.8), design standard 44 px.
- Images: proof thumbnails `alt="Check-in 2 proof submitted 21 Oct 8:45 PM"`; decorative icons `aria-hidden`.
- Colour independence: statuses use text labels.
- Reduced motion respected; no auto-playing media.
- Language `lang="en"`; dates also in machine-readable `<time datetime>`.

## 11. Empty / loading / error / success state matrix
| Screen | Empty | Loading | Error | Success |
|---|---|---|---|---|
| UI-007 | No campaigns + notify CTA | 6 skeleton cards | Retry block | — |
| UI-009 | No tests + browse CTA | list skeleton | Retry | Toast on join |
| UI-010 | — | timeline skeleton | upload error with retry, window closed message | "Check-in received" + next due |
| UI-011 | Zero balance explainer | cards skeleton | Retry | Payout requested card |
| UI-012 | Explainer + New campaign | list skeleton | Retry | Toasts per action |
| UI-015 | Roster empty: "Share your campaign link" + copy link | table skeleton | Retry | Granted/skipped summary |
| UI-016 | "Nothing to review" | skeleton | Retry | Verdict saved |
| Admin queues | "Queue clear" | table skeleton | Retry | Toast + row removed |

## 12. Design QA and handoff checklist
- [ ] Tokens implemented as CSS variables; Tailwind theme reads variables; dark mode via `prefers-color-scheme` + toggle.
- [ ] Automated contrast check passes for all token pairs (TASK-003).
- [ ] Every UI-### implements all states in §11 and status mapping §6.1.
- [ ] Copy reviewed against §8; money always via `MoneyAmount`; times via `formatManila()`.
- [ ] axe: 0 serious/critical on every route (TEST-032).
- [ ] 320 px, 768 px, 1280 px screenshots reviewed for UI-001, 007, 008, 010, 011, 013, 015.
- [ ] Keyboard-only walkthrough of FLOW-004, FLOW-008, FLOW-012.
- [ ] No prototype claims; screenshots come from the real build.
