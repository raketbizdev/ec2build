# EC2Build

An installable agent skill for Claude Code and OpenAI Codex. It turns an app idea into **exactly six** consistent, versioned build specs, plus **one HTML page** that shows all six in your browser (PRD, TRD, App Flow with horizontal swimlanes, Design Brief, Database Schema, and an Implementation Plan written as prompts you run one after another), ready for a coding agent.

**Free and open source (MIT).** EC2Build costs nothing to install or use. The third-party services your app uses (Supabase, Google Play, Apple, Stripe, hosting, email…) run on **your own accounts**. Some have free tiers and some charge fees. EC2Build helps you create and connect them, as automatically as each provider allows (see "Accounts & shared responsibility" below).

Requires: Claude Code and/or Codex, and Python 3 (for the bundled tools; no extra packages).

## Install (one command, any OS)
Needs Node.js 18+ (for `npx`). Python 3 is needed for the bundled diagram/doctor/validate tools.
```text
npx ec2build install            # Claude Code + Codex, for your user (works in every folder)
npx ec2build install --claude   # Claude Code only
npx ec2build install --codex    # Codex only
npx ec2build install --project ./my-app   # only inside one project
npx ec2build update             # get the latest version
npx ec2build status             # where it is installed, which version
npx ec2build uninstall
```
Works the same on Windows, macOS and Linux (PowerShell, cmd, Terminal, VS Code terminal). No shell scripts.

**Other ways**
- **Claude Code plugin** (no terminal): in Claude Code chat run `/plugin marketplace add raketbizdev/ec2build`, then `/plugin install ec2build@ec2build`. The command becomes `/ec2build:ec2build`.
- **Before the npm package is published:** `npx github:raketbizdev/ec2build install`, or from a local copy: `npx /path/to/ec2build install`.
- **Manual:** copy `skills/ec2build` to `~/.claude/skills/ec2build` (Windows: `%USERPROFILE%\.claude\skills\ec2build`).

The CLI also runs the tools: `npx ec2build html <project>` (one-page view), `npx ec2build doctor <project> --stage local`, `npx ec2build validate <project>`, `npx ec2build swimlanes <project>`.

## Use
Open Claude Code or Codex in any folder:
```text
/ec2build help
/ec2build --app web --name "Balayku" --brief "Rental management software for landlords"
/ec2build update   --name "Balayku" --doc PRD --change "Add landlord approval"
/ec2build setup    --name "Balayku" --stage local
/ec2build doctor   --name "Balayku" --stage local
/ec2build validate --name "Balayku"
/ec2build build    --name "Balayku" --phase 0
```
In Codex, type `$ec2build …` instead of `/ec2build …`.

**Output location:** `./ec2build/<slug>/` in the folder where you run it, or `./projects/<slug>/` inside an EC2Build workspace like this repo. Use `--out <dir>` to choose.

## Accounts & shared responsibility
The Implementation Plan includes an accounts setup section (§2A, feeds PROMPT 00) and a shared responsibility matrix (§2B):
- **AUTO:** the agent runs it after you log in through the provider's own CLI (e.g., create the Supabase project, push the database, register webhooks, upload an Android build to a Play testing track).
- **ASSISTED:** the agent gives exact links and clicks, waits, then verifies (e.g., create the app in Play Console, create a service-account key).
- **OWNER-ONLY:** you do it because it is legally yours (accept terms, pay registration fees, verify identity, store policy answers).
- Secrets go straight into your `.env.local`, never into chat. `/ec2build doctor --name "X" --stage local` shows what is still missing without revealing values.

| Who | Responsible for |
|---|---|
| **You (owner)** | Decisions and approvals, your accounts and billing, secrets, legal/tax/privacy, store submissions, production go-live |
| **EC2Build agent** | Consistent specs, setup guide, responsibility matrix, flagging risks and costs |
| **Coding agent** | Code, tests, migrations, automated provisioning and deploys you approved, honest reports |
| **Providers** (Supabase, Google, Apple, Stripe…) | Their platforms: uptime, security of their infrastructure, reviews and payouts per their terms |

Default stack: **Supabase** (local via Docker, free), **Expo** for native Android/iOS + web from one codebase, free-tier hosting that allows your use.

## What's inside
```
skills/ec2build/            the installable skill (everything the agent needs)
  SKILL.md                  entry point: arguments, output location, tools, help
  references/               EC2BUILD_AGENT.md, WORKFLOW.md, TEMPLATES.md, SETUP_AND_RESPONSIBILITY.md
  scripts/swimlanes.py      renders horizontal swimlanes from docs/diagrams/flows.json
  scripts/validate.py       checks the six documents, swimlane images and setup block
  scripts/onepage.py        builds docs/<slug>.html: all six documents on one page (open in any browser)
  scripts/doctor.py         shows what is missing for local/staging/production (never prints secrets)
.claude-plugin/             plugin.json + marketplace.json (Claude Code plugin install)
bin/ec2build.js              npx CLI: install / update / uninstall / status / doctor / validate / swimlanes
package.json                npm package (name: ec2build)
.claude/skills, .agents/skills   workspace pointers to skills/ec2build (for use inside this repo)
projects/                   example output (TestKo PH)
```

## Developing EC2Build
Edit only `skills/ec2build/`. Then bump `version` in `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, add a `CHANGELOG.md` entry, bump `version` in `package.json`, then `npm publish` (owner) and `npx ec2build update` (or `/reload-plugins`). Check the plugin with `claude plugin validate .`.

## Notes
Documentation reduces rework, but delivery time depends on scope and risk. EC2Build does not deploy anything by itself; sensitive actions need your explicit approval.
