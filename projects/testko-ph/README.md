# TestKo PH — EC2Build package

Slug `testko-ph` · renamed from "itphteste" on 2026-10-11.

Closed-testing marketplace: developers pay (Stripe) to publish Google Play / TestFlight closed tests; IT Philippines community testers join with their store email, submit proof check-ins, and earn a reward withdrawable via PayPal from US$25.

| Doc | Version | Status |
|---|---|---|
| [PRD](docs/PRD.md) | 0.2.0 | draft |
| [TRD](docs/TRD.md) | 0.2.0 | draft |
| [APP_FLOW](docs/APP_FLOW.md) — horizontal swimlanes ([diagrams](docs/diagrams/)) | 0.3.0 | draft |
| [DESIGN_BRIEF](docs/DESIGN_BRIEF.md) | 0.2.0 | draft |
| [DATABASE_SCHEMA](docs/DATABASE_SCHEMA.md) | 0.2.0 | draft |
| [IMPLEMENTATION_PLAN](docs/IMPLEMENTATION_PLAN.md) — PROMPT 00 setup + 28 sequential prompts | 0.4.0 | draft |

Setup: [SETUP](docs/SETUP.md) · [SHARED_RESPONSIBILITY](docs/SHARED_RESPONSIBILITY.md) · run `/ec2build setup --name "TestKo PH" --stage local` first.

Supporting: [PROJECT_CONTEXT](docs/PROJECT_CONTEXT.md) · [ASSUMPTIONS](docs/ASSUMPTIONS.md) · [DECISIONS](docs/DECISIONS.md) · [TRACEABILITY](docs/TRACEABILITY.md) · [VALIDATION_REPORT](docs/VALIDATION_REPORT.md) · [CHANGELOG](docs/CHANGELOG.md) · [manifest.json](manifest.json)

## How to use (command samples)
Always use the **current** project name in `--name`. Write the change in plain words inside `--change "..."`. Do not leave template placeholders such as `<New Name>`: they are not applied.

### Rename the app
```text
# Display name only (folder stays projects/testko-ph/)
/ec2build update --name "TestKo PH" --doc PRD --change "Rename app to TestKo Pinas, display only"

# Full rename (folder, slug, repo name, Supabase project id all change)
/ec2build update --name "TestKo PH" --doc PRD --change "Rename app to TestKo Pinas, full rename"
```
After a full rename, use the new name in later commands, e.g. `--name "TestKo Pinas"`. ("TestKo Pinas" is only an example.)

### Change a requirement or assumption
```text
/ec2build update --name "TestKo PH" --doc PRD --change "Set tester reward to US$4.00 and price per slot to US$6.00"
/ec2build update --name "TestKo PH" --doc PRD --change "Missed check-in grace period is 72 hours instead of 48"
/ec2build update --name "TestKo PH" --doc TRD --change "Replace Stripe with PayMongo for developer payments"
/ec2build update --name "TestKo PH" --doc DESIGN --change "Use red #CE1126 as primary brand colour"
```

### Check, sync, build
```text
/ec2build validate --name "TestKo PH"       # run the consistency checks, report only
/ec2build sync --name "TestKo PH"           # repair drift after editing the docs by hand
/ec2build build --name "TestKo PH" --phase 0  # start PROMPT 01 (only when you ask)
```

### Run the implementation prompts yourself
Open a coding agent in an empty app folder and paste PROMPT 01 from [IMPLEMENTATION_PLAN §6](docs/IMPLEMENTATION_PLAN.md), review its report, then paste PROMPT 02, and so on through PROMPT 28 and the FINAL CHECK.
